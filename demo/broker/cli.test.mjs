// The shipped CLIs: the native-control actuation CLI goes through the tier
// gate, and the human-only commands refuse without an interactive terminal.
// Each child runs with a fresh, empty Telos state directory.
import test from "node:test";
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { existsSync, mkdirSync, mkdtempSync, readdirSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { HoldStore } from "./holds.mjs";
import { generateKeys, PRIVATE_KEY_FILE, PUBLIC_KEY_FILE } from "./keys.mjs";
import { stateDirs, stateRoot } from "./paths.mjs";

const demo = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

function runCli(script, args, home = mkdtempSync(path.join(os.tmpdir(), "telos-cli-"))) {
  const env = { ...process.env, LOCALAPPDATA: home, XDG_STATE_HOME: home, HOME: home, USERPROFILE: home, TELOS_SESSION: "cli-test" };
  const r = spawnSync(process.execPath, [path.join(demo, script), ...args], { encoding: "utf8", env, timeout: 30000, cwd: home });
  return { ...r, home };
}

test("native-control with no grant refuses every actuation verb and runs nothing", () => {
  const home = mkdtempSync(path.join(os.tmpdir(), "telos-cli-"));
  const marker = path.join(home, "marker.txt");
  for (const args of [["device", "write", marker, "x"], ["device", "exec", "whoami"], ["browser", "eval", "1+1"], ["app", "type", "hello"], ["device", "ls", "."]]) {
    const r = runCli("native-control.mjs", args, home);
    assert.equal(r.status, 1, `${args.join(" ")}: ${r.stdout}${r.stderr}`);
    const receipt = JSON.parse(r.stdout);
    assert.equal(receipt.ok, false, args.join(" "));
    assert.equal(receipt.result.status, "REFUSED", args.join(" "));
    assert.equal(receipt.result.reason, "NO_GRANT", args.join(" "));
    assert.equal(receipt.result.executed, false, args.join(" "));
  }
  assert.equal(existsSync(marker), false, "device write ran without a grant");
});

function seedKey(home) {
  const dirs = stateDirs(stateRoot({ env: { LOCALAPPDATA: home, XDG_STATE_HOME: home }, home }));
  mkdirSync(dirs.keys, { recursive: true });
  const { privateKey, publicKey } = generateKeys();
  writeFileSync(path.join(dirs.keys, PRIVATE_KEY_FILE), privateKey.export({ type: "pkcs8", format: "pem" }));
  writeFileSync(path.join(dirs.keys, PUBLIC_KEY_FILE), publicKey.export({ type: "spki", format: "pem" }));
  return { dirs, privateKey, publicKey };
}

test("a hand-written grant file without the Telos signature does not unlock the CLI", () => {
  const home = mkdtempSync(path.join(os.tmpdir(), "telos-cli-"));
  const { dirs } = seedKey(home);
  mkdirSync(dirs.grants, { recursive: true });
  const id = `g_${"c".repeat(32)}`;
  writeFileSync(path.join(dirs.grants, `${id}.json`), JSON.stringify({ schema: "telos.grant/v1", grant_id: id, tier: "T1", verbs: ["*"], scope: { senses: ["*"], paths: [home] } }));
  const r = runCli("native-control.mjs", ["device", "ls", "."], home);
  assert.equal(JSON.parse(r.stdout).result.reason, "NO_GRANT");
  const status = JSON.parse(runCli("grant.mjs", ["status"], home).stdout);
  assert.equal(status.live.length, 0);
  assert.equal(status.rejected[0].reason, "scope_digest_mismatch");
});

test("grant, confirm and keys refuse without an interactive terminal, with a key present", () => {
  const home = mkdtempSync(path.join(os.tmpdir(), "telos-cli-"));
  const { dirs, publicKey } = seedKey(home);
  const holds = new HoldStore({ dir: dirs.holds, publicKey });
  const holdId = holds.newId();
  holds.open({ hold_id: holdId, digests: ["e".repeat(64)], tier: "T3", verb: "browser.click", grant_id: "g_x", session_id: "cli", window_s: 120, review: {} });
  const cases = [
    ["grant.mjs", ["issue", "--tier=T1", "--verbs=*", "--senses=*"]],
    ["grant.mjs", ["revoke", `g_${"f".repeat(32)}`]],
    ["keys.mjs", ["init"]],
    ["confirm.mjs", ["approve", holdId]],
    ["confirm.mjs", ["reject", holdId]],
  ];
  for (const [script, args] of cases) {
    const r = runCli(script, args, home);
    assert.equal(r.status, 1, `${script} ${args.join(" ")}`);
    assert.match(r.stderr, /interactive terminal|already exists/, `${script} ${args.join(" ")}`);
  }
  assert.equal(holds.get(holdId).status, "PENDING", "no decision was written");
  assert.equal(existsSync(dirs.grants) ? readdirSync(dirs.grants).filter((n) => n.endsWith(".json")).length : 0, 0, "no grant was written");
  const list = JSON.parse(runCli("confirm.mjs", ["list"], home).stdout);
  assert.deepEqual(list.pending.map((h) => h.hold_id), [holdId]);
});
