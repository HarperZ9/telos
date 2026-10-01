import { spawnSync } from "node:child_process";
import { existsSync, statSync } from "node:fs";
import path from "node:path";
import { resolveSiblingsRoot, spawnRecord, spawnRefused } from "./siblings.mjs";

// The five-flagship room and golden workflow drive the sibling gather, crucible,
// index, and forum source checkouts over a local python interpreter. The sibling
// root comes only from TELOS_SIBLINGS_ROOT or the parent of a git checkout
// (siblings.mjs). Siblings are checked first; python is probed only when every
// sibling is present, so a standalone install never spawns a python probe.
// Missing entries name the sibling, never an absolute path on this machine.

export const SIBLING_REPOS = ["gather", "crucible", "index", "forum"];

function defaultProbe(candidate) {
  return spawnSync(candidate, ["--version"], { encoding: "utf8", windowsHide: true });
}

function pythonAvailable(probe, spawned, env) {
  for (const candidate of ["python", "python3"]) {
    if (spawnRefused(candidate, { env })) return { python: null, refused: true };
    spawned.push(spawnRecord(candidate, ["--version"], ""));
    const result = probe(candidate);
    if (result && result.status === 0) return { python: candidate, refused: false };
  }
  return { python: null, refused: false };
}

function siblingPresent(root, repo) {
  const repoRoot = path.join(root, repo);
  return existsSync(repoRoot) && statSync(repoRoot).isDirectory() && existsSync(path.join(repoRoot, "src"));
}

// Returns { ok, missing, python, siblingsRoot, spawned }. `siblingsRoot` is the
// resolved directory (null when unresolved); callers use it to build paths and
// never print it into an envelope.
export function flagshipPreflight({ repos = SIBLING_REPOS, env = process.env, telosRoot, probe = defaultProbe } = {}) {
  const spawned = [];
  const resolved = resolveSiblingsRoot({ env, ...(telosRoot ? { telosRoot } : {}) });
  if (!resolved.root) {
    return {
      ok: false,
      python: null,
      siblingsRoot: null,
      spawned,
      missing: [{ kind: "siblings-root", name: "siblings root", expected_at: "TELOS_SIBLINGS_ROOT", reason: resolved.reason }]
    };
  }
  const missing = repos
    .filter((repo) => !siblingPresent(resolved.root, repo))
    .map((repo) => ({ kind: "sibling-repo", name: repo, expected_at: `${resolved.source}/${repo}` }));
  if (missing.length) {
    return { ok: false, python: null, siblingsRoot: resolved.root, spawned, missing };
  }
  const { python, refused } = pythonAvailable(probe, spawned, env);
  if (!python) {
    missing.push(refused
      ? { kind: "runtime", name: "python", expected_at: "PATH", reason: "TELOS_NO_SPAWN=1" }
      : { kind: "runtime", name: "python", expected_at: "PATH" });
  }
  return { ok: missing.length === 0, missing, python, siblingsRoot: resolved.root, spawned };
}

// Human-readable one-liner for the console fallback.
export function describeMissing(missing) {
  return missing
    .map((item) => {
      if (item.kind === "runtime") return item.reason ? `${item.name} (${item.reason})` : `${item.name} (not on PATH)`;
      if (item.kind === "siblings-root") return `siblings root (${item.reason}; set TELOS_SIBLINGS_ROOT)`;
      return `${item.name} source checkout (expected at ${item.expected_at})`;
    })
    .join(", ");
}
