// device.mjs after the 0.7.0 move off tools/device.ps1. exec resolves argv[0]
// through absolute PATH entries only and spawns without a shell, so a program
// planted in the working folder, a batch file and shell syntax all fail.
import test from "node:test";
import assert from "node:assert/strict";
import { chmodSync, mkdtempSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { exec, ls, read, whichExecutable, write } from "./device.mjs";

const win = process.platform === "win32";

test("argv0 never resolves from the current directory or a relative PATH entry", () => {
  const dir = mkdtempSync(path.join(os.tmpdir(), "telos-which-"));
  const name = win ? "planted.exe" : "planted";
  writeFileSync(path.join(dir, name), "x");
  if (!win) chmodSync(path.join(dir, name), 0o755);
  const prev = process.cwd();
  process.chdir(dir);
  try {
    assert.equal(whichExecutable("planted", { env: { PATH: "" } }), null);
    assert.equal(whichExecutable("planted", { env: { PATH: "." } }), null);
    assert.equal(whichExecutable(`.${path.sep}${name}`, { env: { PATH: "" } }), null, "a relative path is refused");
    assert.equal(whichExecutable("planted", { env: { PATH: dir } }), path.join(dir, name), "an absolute PATH entry resolves");
  } finally {
    process.chdir(prev);
  }
});

test("batch and script files are not executables on Windows", { skip: !win }, () => {
  const dir = mkdtempSync(path.join(os.tmpdir(), "telos-which-"));
  writeFileSync(path.join(dir, "git.bat"), "@echo planted");
  writeFileSync(path.join(dir, "git.cmd"), "@echo planted");
  assert.equal(whichExecutable("git", { env: { PATH: dir } }), null);
  assert.equal(whichExecutable(path.join(dir, "git.bat")), null);
});

test("exec passes shell syntax through as plain arguments", async () => {
  const marker = path.join(mkdtempSync(path.join(os.tmpdir(), "telos-exec-")), "pwned");
  const r = await exec([process.execPath, "-e", "process.stdout.write(JSON.stringify(process.argv.slice(1)))", "&", "echo", ">", marker]);
  assert.equal(r.exit, 0, r.stderr);
  assert.deepEqual(JSON.parse(r.stdout), ["&", "echo", ">", marker]);
  assert.equal(r.executable, path.basename(process.execPath));
  await assert.rejects(read(marker), /ENOENT/, "no shell ran the redirect");
});

test("read, write and ls use the filesystem directly", async () => {
  const dir = mkdtempSync(path.join(os.tmpdir(), "telos-dev-"));
  const f = path.join(dir, "a.txt");
  assert.deepEqual(await write(f, "héllo"), { ok: true, path: f, bytes: 6 });
  assert.equal((await read(f)).content, "héllo");
  assert.equal((await read(f, 2)).truncated, true);
  const listing = await ls(dir);
  assert.deepEqual(listing.entries.map((e) => [e.name, e.type]), [["a.txt", "file"]]);
});
