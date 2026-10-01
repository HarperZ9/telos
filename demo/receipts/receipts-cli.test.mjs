// Conformance vectors and the `telos receipts` / `telos keys` commands. The
// vectors in docs/spec/vectors are the contract other modules pin by sha256: a
// change to the canonical form, the seal, the action digest or the signature
// payload breaks these assertions before it breaks a downstream verifier.
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { actionDigest, argsSha256 } from "./digest.mjs";
import { canonical, loadTrustedKey, parseJsonl, sealOf, sha256Hex, verifyChain } from "./verify.mjs";
import { initKey } from "./keys.mjs";
import { stateRoot } from "../broker/paths.mjs";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..");
const vec = (f) => path.join(root, "docs", "spec", "vectors", f);
const telos = path.join(root, "demo", "telos.mjs");

test("the committed conformance chain verifies against its pinned key", () => {
  const v = verifyChain(readFileSync(vec("receipt-v1-chain.jsonl"), "utf8"), {
    checkpoints: readFileSync(vec("receipt-v1-checkpoints.jsonl"), "utf8"),
    trustedKey: loadTrustedKey(vec("receipt-v1-key.pub.json"))
  });
  assert.equal(v.verdict, "MATCH", v.reason);
  assert.equal(v.count, 7);
  assert.equal(v.head_seal, "c4b25f5e82dca66681601f149cc28a24a8f54f6036080589dc6711a6f525f464");
});

test("canonical form, seal and action digest match the fixed vectors", () => {
  assert.equal(canonical({ b: [1, "x", null], a: { d: false, c: true } }), '{"a":{"c":true,"d":false},"b":[1,"x",null]}');
  assert.equal(sha256Hex(canonical({})), "44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a");
  const first = parseJsonl(readFileSync(vec("receipt-v1-chain.jsonl"), "utf8")).records[0].rec;
  assert.equal(sealOf(first), "85a0101af5567e71179d0e4180c4085dc9be51a748a2daef433d6ae045fdd0d9");
  assert.equal(actionDigest({ tier: "T3", verb: "browser.fill", target_ref: "b:1:aaaa0000:9", target_fingerprint: "f".repeat(64),
    args_sha256: argsSha256({ value: "Draft" }), scope_sha256: "5".repeat(64), grant_id: "g_vector" }),
  "7055a99f1f4a47c90c5f2b1cf44417a681a6ce1ba8b5466f3f8aeef1713f3db0");
});

test("telos keys init needs a terminal; the shared key shows no private part; receipts verify uses the sibling checkpoints", () => {
  const base = mkdtempSync(path.join(os.tmpdir(), "telos-cli-"));
  const env = { ...process.env, LOCALAPPDATA: base, XDG_STATE_HOME: base, TELOS_HOME: path.join(base, "ignored") };
  const home = stateRoot({ env, home: base });
  const run = (...args) => spawnSync(process.execPath, [telos, ...args], { encoding: "utf8", env });
  const init = run("keys", "init");
  assert.equal(init.status, 1, "an agent shell has no TTY, so init is refused");
  assert.match(init.stderr, /interactive terminal/);
  const created = initKey({ home });
  assert.equal(run("keys", "id").stdout.includes(created.key_id), true, "broker and receipts read one key");
  const shown = run("keys", "show");
  assert.equal(shown.status, 0, shown.stderr);
  assert.equal(JSON.parse(shown.stdout).key_id, created.key_id);
  assert.equal(shown.stdout.includes("PRIVATE"), false);
  assert.throws(() => initKey({ home }), /already exists/, "a second init is refused");
  assert.equal(run("receipts", "path").stdout.trim(), path.join(home, "receipts"), "TELOS_HOME no longer moves state");

  const dir = mkdtempSync(path.join(os.tmpdir(), "telos-cli-chain-"));
  for (const f of ["receipt-v1-chain.jsonl", "receipt-v1-key.pub.json"]) writeFileSync(path.join(dir, f), readFileSync(vec(f)));
  writeFileSync(path.join(dir, "checkpoints.jsonl"), readFileSync(vec("receipt-v1-checkpoints.jsonl")));
  const ok = run("receipts", "verify", path.join(dir, "receipt-v1-chain.jsonl"), "--pubkey", path.join(dir, "receipt-v1-key.pub.json"), "--json");
  assert.equal(ok.status, 0, ok.stdout);
  assert.equal(JSON.parse(ok.stdout).checkpoints, 1, "the sibling checkpoints.jsonl was used");
  const lines = readFileSync(vec("receipt-v1-chain.jsonl"), "utf8").trim().split(/\r?\n/);
  const cut = lines.filter((l) => JSON.parse(l).seq <= 5);
  writeFileSync(path.join(dir, "receipt-v1-chain.jsonl"), `${cut.join("\n")}\n`);
  const truncated = run("receipts", "verify", path.join(dir, "receipt-v1-chain.jsonl"));
  assert.equal(truncated.status, 1, truncated.stdout);
  assert.match(truncated.stdout, /suffix removed/);
  const head = run("receipts", "head", vec("receipt-v1-chain.jsonl"));
  assert.equal(JSON.parse(head.stdout).seq, 7);
});
