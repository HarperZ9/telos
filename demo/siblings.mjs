// Where sibling source checkouts live, and what Telos spawns to reach them.
//
// The room, workflow and proof-witness tools read sibling checkouts (gather,
// crucible, index, forum, emet). Before 0.7.0 they resolved those siblings to
// the parent of this package. In an npm install that parent is `node_modules`,
// so an unrelated installed package named `gather` or `emet` would have been
// imported and run. The sibling root now comes from one of two places only:
//
//   1. TELOS_SIBLINGS_ROOT, set by the operator;
//   2. the parent of a git checkout of Telos, when `<telosRoot>/.git` exists and
//      no ancestor directory is named `node_modules`.
//
// Anything else resolves to null and the tools answer UNVERIFIABLE at once.
// TELOS_NO_SPAWN=1 refuses every subprocess that is not this same node binary.

import { createHash } from "node:crypto";
import { existsSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
export const TELOS_ROOT = path.resolve(here, "..");

function sha256(text) {
  return createHash("sha256").update(String(text), "utf8").digest("hex");
}

function insideNodeModules(dir) {
  return path.resolve(dir).split(/[\\/]+/).some((part) => part.toLowerCase() === "node_modules");
}

// Returns { root, source } or { root: null, source: null, reason }.
export function resolveSiblingsRoot({ telosRoot = TELOS_ROOT, env = process.env, exists = existsSync } = {}) {
  const explicit = env.TELOS_SIBLINGS_ROOT;
  if (explicit && explicit.trim()) {
    return { root: path.resolve(explicit.trim()), source: "TELOS_SIBLINGS_ROOT" };
  }
  if (insideNodeModules(telosRoot)) {
    return { root: null, source: null, reason: "installed package: siblings are never read from node_modules" };
  }
  if (!exists(path.join(telosRoot, ".git"))) {
    return { root: null, source: null, reason: "not a git checkout and TELOS_SIBLINGS_ROOT is unset" };
  }
  return { root: path.resolve(telosRoot, ".."), source: "git-checkout-parent" };
}

export function spawnRefused(argv0, { env = process.env } = {}) {
  if (env.TELOS_NO_SPAWN !== "1") return false;
  return argv0 !== process.execPath;
}

// One disclosed subprocess, as the receipt field `spawned[]` records it. The
// raw argv and cwd stay out of the envelope: only the program name and digests.
export function spawnRecord(argv0, args = [], cwd = "") {
  const name = argv0 === process.execPath ? "node" : path.basename(String(argv0));
  return {
    argv0: name,
    args_sha256: sha256(JSON.stringify(args.map(String))),
    cwd_sha256: sha256(cwd ? path.resolve(cwd) : "")
  };
}

// A small ledger a tool fills as it spawns, then copies into its envelope.
export class SpawnLedger {
  constructor({ env = process.env, spawnImpl } = {}) {
    this.env = env;
    this.spawnImpl = spawnImpl;
    this.records = [];
  }

  run(argv0, args, options = {}) {
    if (spawnRefused(argv0, { env: this.env })) {
      const err = new Error(`TELOS_NO_SPAWN=1 refuses ${path.basename(String(argv0))}`);
      err.code = "SPAWN_REFUSED";
      throw err;
    }
    this.records.push(spawnRecord(argv0, args, options.cwd));
    return this.spawnImpl(argv0, args, options);
  }

  list() {
    return this.records.map((record) => ({ ...record }));
  }
}
