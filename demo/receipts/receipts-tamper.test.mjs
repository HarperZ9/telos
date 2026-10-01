// Tamper controls for the offline verifier (DESIGN 4.2). The four required
// negative controls are a suffix removed after a checkpoint, an edited entry, a
// reordered entry and a signature from the wrong key; each must fail. The extra
// cases pin what the verifier cannot see, so a MATCH is never read as more than
// it shows.
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { copyFileSync, mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { ReceiptChain } from "./chain.mjs";
import { ephemeralSigner } from "./keys.mjs";
import { checkpointPayload, sealOf, signaturePayload, verifyChain } from "./verify.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const tmp = () => mkdtempSync(path.join(os.tmpdir(), "telos-tamper-"));

function build({ n = 10, checkpointEvery = 5, signEvery = 1, signer = ephemeralSigner() } = {}) {
  const chain = ReceiptChain.open({ home: tmp(), session_id: "s_tamper", signer, signEvery, checkpointEvery });
  for (let i = 0; i < n; i += 1) {
    chain.append({ tier: "T1", verb: "observe.snapshot", tool: "telos.observe", status: "OK", executed: true,
      sense: "accessibility", observation_digest: String(i).padStart(64, "0") });
  }
  chain.close();
  const text = readFileSync(chain.file, "utf8");
  const checkpoints = readFileSync(chain.checkpointFile, "utf8");
  const trustedKey = { key_id: signer.key_id, public_key: signer.public_key };
  return { chain, text, checkpoints, signer, trustedKey, lines: text.trim().split("\n").map((l) => JSON.parse(l)) };
}

const join = (recs) => `${recs.map((r) => JSON.stringify(r)).join("\n")}\n`;
const receipts = (recs) => recs.filter((r) => r.schema === "telos.receipt/v1");

test("an intact chain verifies, pinned and self-asserted", () => {
  const b = build();
  const pinned = verifyChain(b.text, { checkpoints: b.checkpoints, trustedKey: b.trustedKey });
  assert.equal(pinned.verdict, "MATCH");
  assert.equal(pinned.key_trust, "pinned");
  assert.equal(pinned.checkpoints, 2);
  assert.equal(verifyChain(b.text).key_trust, "self-asserted");
});

test("control 1: a suffix removed after a checkpoint fails", () => {
  const b = build();
  const cut = b.lines.filter((r) => r.seq <= 6);
  const withoutCheckpoints = verifyChain(join(cut), { trustedKey: b.trustedKey });
  assert.equal(withoutCheckpoints.verdict, "MATCH", "honest null: a cut at a signed head is invisible without a checkpoint");
  const v = verifyChain(join(cut), { checkpoints: b.checkpoints, trustedKey: b.trustedKey });
  assert.equal(v.verdict, "DRIFT");
  assert.match(v.reason, /suffix removed: checkpoint at seq 10, chain ends at seq 6/);
});

test("control 2: an edited entry fails, and so does an edit with every seal recomputed", () => {
  const b = build();
  const edited = b.lines.map((r) => (r.seq === 3 && r.schema === "telos.receipt/v1" ? { ...r, reason: "edited" } : r));
  const v = verifyChain(join(edited), { trustedKey: b.trustedKey });
  assert.equal(v.verdict, "DRIFT");
  assert.match(v.reason, /seal does not re-derive at seq 3/);
  let prev = "0".repeat(64);
  const resealed = b.lines.map((r) => {
    if (r.schema !== "telos.receipt/v1") return r;
    const out = { ...r, prev_seal: prev, reason: r.seq === 3 ? "edited" : r.reason };
    out.seal = sealOf(out);
    prev = out.seal;
    return out;
  });
  const v2 = verifyChain(join(resealed), { trustedKey: b.trustedKey });
  assert.equal(v2.verdict, "DRIFT");
  assert.match(v2.reason, /signed head is not the seal at seq 3/);
});

test("control 3: a reordered entry fails", () => {
  const b = build();
  const recs = [...b.lines];
  const i = recs.findIndex((r) => r.seq === 4 && r.schema === "telos.receipt/v1");
  const j = recs.findIndex((r) => r.seq === 5 && r.schema === "telos.receipt/v1");
  [recs[i], recs[j]] = [recs[j], recs[i]];
  const v = verifyChain(join(recs), { trustedKey: b.trustedKey });
  assert.equal(v.verdict, "DRIFT");
  assert.match(v.reason, /signature names seq 4 before it exists|seq 5, expected 4/);
});

test("control 4: a signature from the wrong key fails", () => {
  const b = build();
  const mallory = ephemeralSigner();
  const swapped = b.lines.map((r) => {
    if (r.schema !== "telos.receipt-signature/v1" || r.seq !== 5) return r;
    const out = { ...r, key_id: mallory.key_id, public_key: mallory.public_key };
    out.sig = mallory.sign(signaturePayload(out));
    return out;
  });
  assert.equal(verifyChain(join(swapped)).verdict, "DRIFT", "self-asserted: one chain, one key");
  assert.equal(verifyChain(join(swapped), { trustedKey: b.trustedKey }).verdict, "DRIFT");
  const claimed = b.lines.map((r) => (r.schema === "telos.receipt-signature/v1" && r.seq === 5
    ? { ...r, sig: mallory.sign(signaturePayload(r)) } : r));
  const v = verifyChain(join(claimed), { trustedKey: b.trustedKey });
  assert.equal(v.verdict, "DRIFT");
  assert.match(v.reason, /signature does not verify for seq 5/);
});

test("a chain re-signed end to end by another key passes only when the key is not pinned", () => {
  const b = build();
  const mallory = ephemeralSigner();
  const resigned = b.lines.map((r) => {
    if (r.schema !== "telos.receipt-signature/v1") return r;
    const out = { ...r, key_id: mallory.key_id, public_key: mallory.public_key };
    out.sig = mallory.sign(signaturePayload(out));
    return out;
  });
  const open = verifyChain(join(resigned));
  assert.equal(open.verdict, "MATCH");
  assert.equal(open.key_trust, "self-asserted", "the result says the key was not pinned");
  const pinned = verifyChain(join(resigned), { trustedKey: b.trustedKey });
  assert.equal(pinned.verdict, "DRIFT");
});

test("inserted, deleted and duplicated entries fail", () => {
  const b = build();
  const recs = receipts(b.lines);
  const deleted = b.lines.filter((r) => !(r.schema === "telos.receipt/v1" && r.seq === 4));
  assert.equal(verifyChain(join(deleted)).verdict, "DRIFT");
  const dup = [...b.lines];
  dup.splice(dup.indexOf(recs[2]) + 1, 0, recs[2]);
  assert.equal(verifyChain(join(dup)).verdict, "DRIFT");
  assert.equal(verifyChain(`${b.text}not json\n`).verdict, "DRIFT");
  assert.equal(verifyChain(`${b.text}${JSON.stringify({ schema: "other/v1" })}\n`).verdict, "DRIFT");
});

test("signature coverage: a removed final signature leaves the tail unverifiable", () => {
  const b = build({ checkpointEvery: 1000 });
  const lastSig = b.lines.findLastIndex((r) => r.schema === "telos.receipt-signature/v1");
  const midSig = b.lines.findIndex((r) => r.schema === "telos.receipt-signature/v1" && r.seq === 3);
  const noMid = b.lines.filter((_, i) => i !== midSig);
  assert.equal(verifyChain(join(noMid)).verdict, "MATCH", "a later head signature covers earlier receipts through the chain");
  const noLast = b.lines.filter((_, i) => i !== lastSig);
  const v = verifyChain(join(noLast));
  assert.equal(v.verdict, "UNVERIFIABLE");
  assert.match(v.reason, /1 receipts after seq 9 are unsigned/);
});

test("a forged or wrong-key checkpoint fails", () => {
  const b = build();
  const cps = b.checkpoints.trim().split("\n").map((l) => JSON.parse(l));
  const forged = [{ ...cps[0], head_seal: "e".repeat(64) }];
  assert.equal(verifyChain(b.text, { checkpoints: join(forged), trustedKey: b.trustedKey }).verdict, "DRIFT");
  const mallory = ephemeralSigner();
  const wrong = { ...cps[0], key_id: mallory.key_id, public_key: mallory.public_key };
  wrong.signature = mallory.sign(checkpointPayload(wrong));
  assert.equal(verifyChain(b.text, { checkpoints: join([wrong]), trustedKey: b.trustedKey }).verdict, "DRIFT");
});

test("1,000 receipts, each head signed, verify in under one second", () => {
  const b = build({ n: 1000, checkpointEvery: 256 });
  const started = process.hrtime.bigint();
  const v = verifyChain(b.text, { checkpoints: b.checkpoints, trustedKey: b.trustedKey });
  const ms = Number(process.hrtime.bigint() - started) / 1e6;
  assert.equal(v.verdict, "MATCH");
  assert.equal(v.count, 1000);
  assert.ok(ms < 1000, `verification took ${ms.toFixed(1)} ms`);
  console.log(`# verify 1000 receipts + 1000 signatures + ${v.checkpoints} checkpoints: ${ms.toFixed(1)} ms`);
});

test("the verifier runs as one copied file with no Telos imports", () => {
  const b = build();
  const dir = tmp();
  copyFileSync(path.join(here, "verify.mjs"), path.join(dir, "verify.mjs"));
  writeFileSync(path.join(dir, "s.jsonl"), b.text);
  writeFileSync(path.join(dir, "cp.jsonl"), b.checkpoints);
  writeFileSync(path.join(dir, "pub.json"), JSON.stringify(b.trustedKey));
  const run = (file, extra = []) => spawnSync(process.execPath, [path.join(dir, "verify.mjs"), file, ...extra], { encoding: "utf8" });
  const good = run(path.join(dir, "s.jsonl"), ["--checkpoints", path.join(dir, "cp.jsonl"), "--pubkey", path.join(dir, "pub.json")]);
  assert.equal(good.status, 0, good.stdout + good.stderr);
  assert.match(good.stdout, /^MATCH/);
  writeFileSync(path.join(dir, "bad.jsonl"), b.text.replace('"reason":""', '"reason":"x"'));
  assert.equal(run(path.join(dir, "bad.jsonl")).status, 1);
  writeFileSync(path.join(dir, "none.jsonl"), "");
  assert.equal(run(path.join(dir, "none.jsonl")).status, 2);
  assert.equal(run(path.join(dir, "missing.jsonl")).status, 2);
});
