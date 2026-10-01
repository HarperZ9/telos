// Listing blocker 6.2: the room, workflow and proof-witness tools never read
// siblings from node_modules, never probe python when siblings are absent, and
// disclose every subprocess they start.
//
// Negative control: the installed-package test and the probe test fail on
// db475ca, where siblings resolved to the package parent and python was probed
// before siblings were checked.
import test from "node:test";
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { cpSync, existsSync, mkdirSync, mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { flagshipPreflight } from "./flagship-preflight.mjs";
import { SpawnLedger, resolveSiblingsRoot, spawnRecord, spawnRefused } from "./siblings.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const telosRoot = path.resolve(here, "..");

function scratch() {
  return mkdtempSync(path.join(tmpdir(), "telos-siblings-"));
}

test("the sibling root never comes from node_modules", () => {
  const dir = scratch();
  try {
    const installed = path.join(dir, "node_modules", "project-telos-mcp");
    mkdirSync(path.join(dir, "node_modules", "gather", "src"), { recursive: true });
    mkdirSync(path.join(installed, ".git"), { recursive: true });
    const r = resolveSiblingsRoot({ telosRoot: installed, env: {} });
    assert.equal(r.root, null);
    assert.match(r.reason, /node_modules/);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("a git checkout resolves to its parent; no .git resolves to nothing; the env wins", () => {
  const exists = (p) => p.endsWith(`${path.sep}.git`);
  assert.equal(resolveSiblingsRoot({ telosRoot: path.resolve("/w/telos"), env: {}, exists }).root, path.resolve("/w"));
  assert.equal(resolveSiblingsRoot({ telosRoot: path.resolve("/w/telos"), env: {}, exists: () => false }).root, null);
  const env = { TELOS_SIBLINGS_ROOT: path.resolve("/elsewhere") };
  assert.deepEqual(resolveSiblingsRoot({ telosRoot: path.resolve("/x/node_modules/t"), env }),
    { root: path.resolve("/elsewhere"), source: "TELOS_SIBLINGS_ROOT" });
});

test("python is never probed while any sibling is missing", () => {
  const dir = scratch();
  try {
    const calls = [];
    const probe = (c) => { calls.push(c); return { status: 0 }; };
    mkdirSync(path.join(dir, "gather", "src"), { recursive: true });
    const r = flagshipPreflight({ env: { TELOS_SIBLINGS_ROOT: dir }, probe });
    assert.equal(r.ok, false);
    assert.deepEqual(calls, []);
    assert.deepEqual(r.spawned, []);
    assert.deepEqual(r.missing.map((m) => m.name), ["crucible", "index", "forum"]);
    for (const m of r.missing) assert.ok(!m.expected_at.includes(dir), "no absolute path in the envelope");
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("with every sibling present, python is probed once and recorded", () => {
  const dir = scratch();
  try {
    for (const repo of ["gather", "crucible", "index", "forum"]) mkdirSync(path.join(dir, repo, "src"), { recursive: true });
    const calls = [];
    const r = flagshipPreflight({ env: { TELOS_SIBLINGS_ROOT: dir }, probe: (c) => { calls.push(c); return { status: 0 }; } });
    assert.equal(r.ok, true);
    assert.deepEqual(calls, ["python"]);
    assert.equal(r.python, "python");
    assert.deepEqual(r.spawned.map((s) => s.argv0), ["python"]);
    const refused = flagshipPreflight({ env: { TELOS_SIBLINGS_ROOT: dir, TELOS_NO_SPAWN: "1" }, probe: () => assert.fail("probed") });
    assert.equal(refused.ok, false);
    assert.equal(refused.missing[0].reason, "TELOS_NO_SPAWN=1");
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("spawn records carry digests, not raw argv or cwd", () => {
  const rec = spawnRecord("/usr/bin/python3", ["-c", "secret code"], "/home/someone/repo");
  assert.equal(rec.argv0, "python3");
  assert.match(rec.args_sha256, /^[a-f0-9]{64}$/);
  assert.ok(!JSON.stringify(rec).includes("secret"));
  assert.ok(!JSON.stringify(rec).includes("someone"));
  assert.equal(spawnRefused("python", { env: { TELOS_NO_SPAWN: "1" } }), true);
  assert.equal(spawnRefused(process.execPath, { env: { TELOS_NO_SPAWN: "1" } }), false);
  const ledger = new SpawnLedger({ env: { TELOS_NO_SPAWN: "1" }, spawnImpl: () => assert.fail("ran") });
  assert.throws(() => ledger.run("python", []), /TELOS_NO_SPAWN/);
  assert.deepEqual(ledger.list(), []);
});

// End to end: an installed copy beside a planted `gather` package. On db475ca
// the room tool resolved siblings to node_modules and, with python present,
// imported the planted module, which writes the marker.
test("an installed package never imports a planted node_modules sibling", () => {
  const dir = scratch();
  try {
    const nm = path.join(dir, "node_modules");
    const pkg = path.join(nm, "project-telos-mcp");
    cpSync(path.join(telosRoot, "demo"), path.join(pkg, "demo"), { recursive: true });
    cpSync(path.join(telosRoot, "package.json"), path.join(pkg, "package.json"));
    const marker = path.join(dir, "MARKER");
    for (const repo of ["gather", "crucible", "index", "forum"]) {
      const mod = repo === "index" ? "index_graph" : repo;
      mkdirSync(path.join(nm, repo, "src", mod), { recursive: true });
      writeFileSync(path.join(nm, repo, "src", mod, "__init__.py"), "");
      writeFileSync(path.join(nm, repo, "src", mod, "cli.py"),
        `def main(a):\n    open(${JSON.stringify(marker)}, "w").write("ran")\n    print("{}")\n    return 0\n`);
    }
    const env = { ...process.env };
    delete env.TELOS_SIBLINGS_ROOT;
    for (const script of ["room.mjs", "flagship-workflow.mjs"]) {
      const r = spawnSync(process.execPath, [path.join(pkg, "demo", script), "--json"], { cwd: dir, env, encoding: "utf8" });
      assert.equal(r.status, 0, r.stderr);
      const payload = JSON.parse(r.stdout);
      assert.equal(payload.status, "UNVERIFIABLE", script);
      assert.deepEqual(payload.native.spawned, [], `${script} spawned nothing`);
      assert.ok(!r.stdout.includes(dir), `${script} prints no absolute path`);
    }
    assert.equal(existsSync(marker), false, "planted sibling was imported");
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("with siblings present, the room envelope names exactly the calls it made", (t) => {
  const pre = flagshipPreflight();
  if (!pre.ok) return t.skip("sibling checkouts are not present in this layout");
  const r = spawnSync(process.execPath, [path.join(here, "room.mjs"), "--json"], { cwd: telosRoot, encoding: "utf8" });
  assert.equal(r.status, 0, r.stderr);
  const spawned = JSON.parse(r.stdout).native.spawned;
  const count = (name) => spawned.filter((s) => s.argv0 === name).length;
  // one probe, four status and four doctor calls; two node children
  assert.equal(count(pre.python), 9);
  assert.equal(count("node"), 2);
  assert.equal(spawned.length, 11);
});
