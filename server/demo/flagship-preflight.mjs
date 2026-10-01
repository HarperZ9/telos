import { spawnSync } from "node:child_process";
import { existsSync, statSync } from "node:fs";
import path from "node:path";

// The five-flagship room and golden workflow drive the sibling gather, crucible,
// index, and forum source checkouts over a local `python` interpreter. On the
// operator's multi-repo dev tree those siblings sit next to this checkout and the
// tools run in full. A standalone `npm install project-telos-mcp` has neither the
// sibling repos nor a guaranteed python, so this preflight names the missing
// dependency honestly instead of letting a subprocess throw an opaque error.

const SIBLING_REPOS = ["gather", "crucible", "index", "forum"];

function pythonAvailable() {
  for (const candidate of ["python", "python3"]) {
    const probe = spawnSync(candidate, ["--version"], { encoding: "utf8" });
    if (probe.status === 0) {
      return candidate;
    }
  }
  return null;
}

// Returns { ok: true, python } when every dependency is present, or
// { ok: false, missing: [...], python } describing exactly what is absent.
export function flagshipPreflight({ publicRoot, repos = SIBLING_REPOS } = {}) {
  const missing = [];
  for (const repo of repos) {
    const repoRoot = path.join(publicRoot, repo);
    const sourceRoot = path.join(repoRoot, "src");
    const present =
      existsSync(repoRoot) &&
      statSync(repoRoot).isDirectory() &&
      existsSync(sourceRoot);
    if (!present) {
      missing.push({ kind: "sibling-repo", name: repo, expected_at: repoRoot });
    }
  }
  const python = pythonAvailable();
  if (!python) {
    missing.push({ kind: "runtime", name: "python", expected_at: "PATH" });
  }
  return { ok: missing.length === 0, missing, python };
}

// Human-readable one-liner for the console fallback.
export function describeMissing(missing) {
  return missing
    .map((item) =>
      item.kind === "runtime"
        ? `${item.name} (not on PATH)`
        : `${item.name} source checkout (expected at ${item.expected_at})`
    )
    .join(", ");
}
