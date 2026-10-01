import test from "node:test";
import assert from "node:assert/strict";
import { MODULES, moduleCatalog, resolveModule, sidecarReceiptBody } from "./modules.mjs";

test("an env override names a module command and is the source", () => {
  const r = resolveModule("accountable-surface", { env: { TELOS_MODULE_ACCOUNTABLE_SURFACE: "/opt/as-mcp" }, pathLookup: () => null });
  assert.equal(r.available, true);
  assert.equal(r.command, "/opt/as-mcp");
  assert.equal(r.source, "TELOS_MODULE_ACCOUNTABLE_SURFACE");
});

test("a console script on PATH resolves without an override", () => {
  const r = resolveModule("calibrate-pro", { env: {}, pathLookup: (bin) => (bin === "calibrate-pro" ? "/usr/bin/calibrate-pro" : null) });
  assert.equal(r.available, true);
  assert.equal(r.source, "PATH");
});

test("an absent module is UNAVAILABLE with its install command, never a guessed path", () => {
  const r = resolveModule("provenance-sensorium", { env: {}, pathLookup: () => null });
  assert.equal(r.available, false);
  assert.equal(r.status, "UNAVAILABLE");
  assert.match(r.install, /provenance-sensorium/);
  assert.equal(r.command, undefined);
});

test("node_modules is never a discovery source", () => {
  // A pathLookup that would only find something under node_modules returns null,
  // because resolveModule asks for the bin by name on PATH, not a package dir.
  const env = { PATH: "/x/node_modules/.bin" };
  const r = resolveModule("accountable-surface", { env, pathLookup: (bin, e) => (e.PATH.includes("node_modules") ? null : "x") });
  assert.equal(r.available, false);
});

test("the sidecar receipt body carries a path digest, not the path", () => {
  const ok = sidecarReceiptBody({ available: true, name: "accountable-surface", command: "/opt/secret/as-mcp", source: "PATH" }, { version: "0.4.0" });
  assert.equal(ok.status, "OK");
  assert.equal(ok.module_version, "0.4.0");
  assert.equal(ok.spawned[0].argv0, "as-mcp");
  assert.ok(!JSON.stringify(ok).includes("secret"));
  const missing = sidecarReceiptBody({ available: false, name: "calibrate-pro", install: "pip install calibrate-pro" });
  assert.equal(missing.status, "UNAVAILABLE");
});

test("the catalog lists every module with availability", () => {
  const cat = moduleCatalog({ env: {}, pathLookup: () => null });
  assert.deepEqual(cat.map((m) => m.name).sort(), Object.keys(MODULES).sort());
  assert.ok(cat.every((m) => m.available === false && m.install));
});
