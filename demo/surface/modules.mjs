// Module discovery for the Python effector and sense modules (DESIGN.md 2.2).
//
// Accountable Surface, provenance-sensorium and Calibrate Pro are Python and
// stay installable alone; when they run under Telos they are reached as stdio
// sidecars. Discovery is explicit: TELOS_MODULE_<NAME> names a command, or the
// module's own console script is found on PATH. A module is never a path derived
// from node_modules or a sibling guess. An absent module is UNAVAILABLE with its
// install command, and its verbs stay in the catalog marked unavailable; Telos
// keeps working at every tier its own drivers cover.
import { existsSync } from "node:fs";
import path from "node:path";
import { spawnRecord } from "../siblings.mjs";

// name -> { env override var, console script on PATH, install hint, what it owns }
export const MODULES = Object.freeze({
  "accountable-surface": {
    env: "TELOS_MODULE_ACCOUNTABLE_SURFACE",
    bin: "accountable-surface-mcp",
    install: "pip install accountable-surface",
    role: "effector and perception module: construction bounds, pre-image capture, verify-by-re-read, rollback, the UIA escalation ladder"
  },
  "provenance-sensorium": {
    env: "TELOS_MODULE_PROVENANCE_SENSORIUM",
    bin: "provenance-sensorium",
    install: "pip install provenance-sensorium  # or install from source; not yet on PyPI",
    role: "T1 file and git sensors"
  },
  "calibrate-pro": {
    env: "TELOS_MODULE_CALIBRATE_PRO",
    bin: "calibrate-pro",
    install: "pip install calibrate-pro",
    role: "T5 display module: DDC/CI, LUT, ICC, instruments, CLI-driven"
  }
});

function onPath(bin, env) {
  const exts = process.platform === "win32" ? ["", ".exe", ".cmd", ".bat"] : [""];
  for (const dir of String(env.PATH || env.Path || "").split(path.delimiter).filter(Boolean)) {
    for (const ext of exts) {
      const candidate = path.join(dir, bin + ext);
      if (existsSync(candidate)) return candidate;
    }
  }
  return null;
}

// Resolve one module. { available, command, source } or { available:false,
// status:"UNAVAILABLE", install }. Never resolves from node_modules or a sibling.
export function resolveModule(name, { env = process.env, pathLookup = onPath } = {}) {
  const spec = MODULES[name];
  if (!spec) return { available: false, status: "UNKNOWN_MODULE", name };
  const override = env[spec.env];
  if (override && override.trim()) {
    return { available: true, name, command: override.trim(), source: spec.env, role: spec.role };
  }
  const found = pathLookup(spec.bin, env);
  if (found) return { available: true, name, command: found, source: "PATH", role: spec.role };
  return { available: false, status: "UNAVAILABLE", name, install: spec.install, role: spec.role };
}

// A T0 receipt body for a sidecar start (DESIGN.md 2.2): the command name, its
// resolved path digest and, when the caller supplies it, the module version. No
// absolute path reaches the receipt.
export function sidecarReceiptBody(resolved, { version = null } = {}) {
  if (!resolved.available) {
    return { tier: "T0", verb: "module.resolve", tool: `module.${resolved.name}`, status: "UNAVAILABLE",
      module: resolved.name, reason: `install with: ${resolved.install}`, executed: false };
  }
  const spawned = spawnRecord(resolved.command, [], "");
  return { tier: "T0", verb: "module.start", tool: `module.${resolved.name}`, status: "OK",
    module: resolved.name, module_version: version, executed: false,
    spawned: [spawned], reason: `resolved from ${resolved.source}` };
}

// The catalog view: every module with available true/false, so a host sees the
// whole surface and what a module would add.
export function moduleCatalog({ env = process.env, pathLookup = onPath } = {}) {
  return Object.keys(MODULES).map((name) => {
    const r = resolveModule(name, { env, pathLookup });
    return { name, role: MODULES[name].role, available: r.available,
      ...(r.available ? { source: r.source } : { install: MODULES[name].install }) };
  });
}
