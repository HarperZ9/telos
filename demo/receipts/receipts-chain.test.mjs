// Receipt core: canonical form, sealing, persistence before return, signing,
// resume, side files, and the writer-side field rules (DESIGN 4.1, 4.2).
import assert from "node:assert/strict";
import { existsSync, mkdtempSync, readFileSync, statSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { ReceiptChain } from "./chain.mjs";
import { actionDigest, argsSha256 } from "./digest.mjs";
import { ephemeralSigner, initKey, loadSigner, publicKeyPath } from "./keys.mjs";
import { DOES_NOT_PROVE, TIER_FIELDS, unknownFields } from "./schema.mjs";
import { GENESIS, canonical, parseJsonl, sealOf, signaturePayload, verifyChain } from "./verify.mjs";

const tmp = () => mkdtempSync(path.join(os.tmpdir(), "telos-receipts-"));
const observe = (extra = {}) => ({ tier: "T1", verb: "observe.snapshot", tool: "telos.observe", status: "OK", executed: true,
  sense: "accessibility", observation_digest: "a".repeat(64), ...extra });

test("canonical form: sorted keys, compact separators, floats refused", () => {
  assert.equal(canonical({ b: 1, a: [true, null, "x"] }), '{"a":[true,null,"x"],"b":1}');
  assert.equal(canonical({ z: { y: 2, x: 1 } }), canonical({ z: { x: 1, y: 2 } }));
  assert.throws(() => canonical({ v: 1.5 }), /non-integer/);
  assert.throws(() => canonical({ v: Number.NaN }), /non-integer/);
  assert.throws(() => canonical({ v: 2 ** 60 }), /non-integer/);
  assert.equal(canonical({ v: undefined, w: 1 }), '{"w":1}', "an undefined key is dropped, as a JSON round trip drops it");
  assert.throws(() => canonical([undefined]), /forbids undefined/);
  assert.equal(canonical({ s: "é" }), '{"s":"é"}');
});

test("append persists a sealed, linked receipt before it returns", () => {
  const home = tmp();
  const chain = ReceiptChain.open({ home, session_id: "s_unit", signer: ephemeralSigner() });
  const r1 = chain.append(observe());
  const onDisk = parseJsonl(readFileSync(chain.file, "utf8")).records.map((x) => x.rec);
  assert.equal(onDisk[0].seal, r1.seal, "the receipt is on disk when append returns");
  assert.equal(r1.prev_seal, GENESIS);
  assert.equal(r1.seq, 1);
  assert.equal(r1.seal, sealOf(r1));
  assert.equal(r1.hash_version, 3);
  assert.equal(r1.does_not_prove, DOES_NOT_PROVE.OK);
  const r2 = chain.append(observe());
  assert.equal(r2.prev_seal, r1.seal);
  assert.equal(r2.seq, 2);
  assert.equal(chain.verify().verdict, "MATCH");
});

test("every chain head is signed; signEvery batches up to 32", () => {
  const chain = ReceiptChain.open({ home: tmp(), session_id: "s_batch", signer: ephemeralSigner(), signEvery: 32 });
  for (let i = 0; i < 40; i += 1) chain.append(observe());
  const before = chain.verify();
  assert.equal(before.verdict, "UNVERIFIABLE", "8 receipts after the last batch signature are unsigned");
  assert.match(before.reason, /8 receipts after seq 32 are unsigned/);
  chain.close();
  const after = chain.verify();
  assert.equal(after.verdict, "MATCH");
  assert.equal(after.signed_through, 40);
  assert.equal(after.checkpoints, 1);
  assert.throws(() => ReceiptChain.open({ home: tmp(), signer: null, signEvery: 33 }), /signEvery/);
});

test("checkpoints are written every checkpointEvery receipts and at close", () => {
  const chain = ReceiptChain.open({ home: tmp(), session_id: "s_cp", signer: ephemeralSigner(), checkpointEvery: 4 });
  for (let i = 0; i < 9; i += 1) chain.append(observe());
  chain.close();
  const cps = readFileSync(chain.checkpointFile, "utf8").trim().split("\n").map((l) => JSON.parse(l));
  assert.deepEqual(cps.map((c) => c.seq), [4, 8, 9]);
  assert.equal(chain.verify().checkpoints, 3);
});

test("a chain resumes after restart and refuses to extend a broken file", () => {
  const home = tmp();
  const signer = ephemeralSigner();
  const a = ReceiptChain.open({ home, session_id: "s_resume", signer });
  a.append(observe());
  const b = ReceiptChain.open({ home, session_id: "s_resume", signer });
  const r = b.append(observe());
  assert.equal(r.seq, 2);
  assert.equal(b.verify().verdict, "MATCH");
  const other = ephemeralSigner();
  assert.throws(() => ReceiptChain.open({ home, session_id: "s_resume", signer: other }), /refusing to extend/);
});

test("the writer fixes chain fields, does_not_prove and enums", () => {
  const chain = ReceiptChain.open({ home: tmp(), session_id: "s_rules", signer: null });
  assert.throws(() => chain.append(observe({ seq: 9 })), /set by the chain/);
  assert.throws(() => chain.append(observe({ seal: "x" })), /set by the chain/);
  assert.throws(() => chain.append(observe({ does_not_prove: "anything" })), /fixed per status/);
  assert.throws(() => chain.append(observe({ status: "MAYBE" })), /status/);
  assert.throws(() => chain.append(observe({ tier: "T9" })), /tier/);
  assert.throws(() => chain.append(observe({ resolution: "guess" })), /resolution/);
  assert.throws(() => chain.append(observe({ duration: 1.25 })), /non-integer/);
  assert.throws(() => ReceiptChain.open({ home: tmp(), session_id: "../escape" }), /invalid session id/);
  const r = chain.append(observe({ module_extension: "kept" }));
  assert.deepEqual(unknownFields(r), ["module_extension"], "unknown fields are sealed and reported, not dropped");
});

test("a non-executing status cannot claim an effect", () => {
  const signer = ephemeralSigner();
  const chain = ReceiptChain.open({ home: tmp(), session_id: "s_exec", signer });
  assert.throws(() => chain.append({ tier: "T3", verb: "browser.click", status: "HOLD", executed: true }), /cannot carry executed/);
  // A hand-built receipt that claims an effect on a HOLD, sealed and signed, is
  // still caught by the verifier's structural check.
  const forged = { ...chain.append({ tier: "T3", verb: "browser.click", status: "HOLD", hold_id: "h_1" }), executed: true };
  forged.seal = sealOf(forged);
  const sig = { schema: "telos.receipt-signature/v1", session_id: "s_exec", seq: 1, head_seal: forged.seal,
    key_id: signer.key_id, public_key: signer.public_key };
  sig.sig = signer.sign(signaturePayload(sig));
  const v = verifyChain(`${JSON.stringify(forged)}\n${JSON.stringify(sig)}\n`);
  assert.equal(v.verdict, "DRIFT");
  assert.match(v.reason, /status HOLD cannot be executed/);
});

test("unsigned chains persist but never verify as MATCH", () => {
  const chain = ReceiptChain.open({ home: tmp(), session_id: "s_nokey", signer: null });
  chain.append(observe());
  const v = chain.verify();
  assert.equal(v.verdict, "UNVERIFIABLE");
});

test("side files hold raw content keyed by seal; receipts hold digests", () => {
  const chain = ReceiptChain.open({ home: tmp(), session_id: "s_side", signer: ephemeralSigner() });
  const args = { selector: "#email", text: "hello" };
  const r = chain.append({ tier: "T3", verb: "browser.fill", status: "OK", executed: true, args_sha256: argsSha256(args) },
    { side: { "args.json": args } });
  assert.deepEqual(JSON.parse(chain.readSide(r.seal, "args.json")), args);
  assert.equal(JSON.stringify(r).includes("hello"), false, "raw arguments never enter the receipt");
  assert.throws(() => chain.append(observe(), { side: { "../x.json": "{}" } }), /invalid side file/);
});

test("the key is created once, never overwritten, and never leaves the signer", () => {
  const home = tmp();
  const pub = initKey({ home });
  assert.equal(pub.key_id.length, 64);
  assert.throws(() => initKey({ home }), /never overwritten/);
  const signer = loadSigner({ home });
  assert.equal(signer.key_id, pub.key_id);
  assert.deepEqual(Object.keys(signer).sort(), ["key_id", "public_key", "sign"]);
  if (process.platform !== "win32") {
    assert.equal(statSync(path.join(home, "keys", "telos-ed25519.pem")).mode & 0o077, 0, "private key is owner-only");
  }
  assert.ok(existsSync(publicKeyPath(home)));
  const chain = ReceiptChain.open({ home, session_id: "s_auto" });
  chain.append(observe());
  const text = readFileSync(chain.file, "utf8");
  assert.equal(text.includes("PRIVATE KEY"), false);
  assert.equal(chain.verify().verdict, "MATCH", "signer auto-loads the local key");
});

test("action digest binds tier, verb, target, fingerprint, args, scope and grant", () => {
  const base = { tier: "T3", verb: "browser.click", target_ref: "b:1:abcd1234:42", target_fingerprint: "f".repeat(64),
    args_sha256: argsSha256({}), scope_sha256: "s".repeat(64), grant_id: "g_1" };
  const d = actionDigest(base);
  for (const field of Object.keys(base)) {
    assert.notEqual(actionDigest({ ...base, [field]: `${base[field]}x` }), d, `${field} changes the digest`);
  }
  assert.deepEqual(TIER_FIELDS.T4.slice(0, TIER_FIELDS.T3.length), TIER_FIELDS.T3);
  assert.equal(verifyChain("").verdict, "UNVERIFIABLE");
});
