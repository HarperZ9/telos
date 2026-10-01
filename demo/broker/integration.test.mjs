// Integration of the three 0.7.0 slices: the tier gate (broker), the signed
// receipt chain and act-by-ref. Each test is a way the joined system could
// accept an action the separate slices would have refused, or record it in a
// form the offline verifier does not accept.
import test from "node:test";
import assert from "node:assert/strict";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { makeEnv } from "./harness.test.mjs";
import { keyId, PRIVATE_KEY_FILE, PUBLIC_KEY_FILE } from "./keys.mjs";
import { ChainRecorder } from "./recorder.mjs";
import { loadSigner } from "../receipts/keys.mjs";
import { verifyChain } from "../receipts/verify.mjs";
import { actByRef } from "../native-control.mjs";

const REF = "b:e0000000:page:12";
const F1 = "1".repeat(64);
const F2 = "2".repeat(64);

// A broker on the real signed chain, with the grant key on disk as the CLI
// would find it, so grants and receipts share one key.
function chainEnv(opts = {}) {
  const env = makeEnv(opts);
  mkdirSync(env.dirs.keys, { recursive: true });
  writeFileSync(path.join(env.dirs.keys, PRIVATE_KEY_FILE), env.privateKey.export({ type: "pkcs8", format: "pem" }));
  writeFileSync(path.join(env.dirs.keys, PUBLIC_KEY_FILE), env.publicKey.export({ type: "spki", format: "pem" }));
  env.chain = new ChainRecorder({ home: env.dirs.root, sessionId: "s1" });
  env.live = { ok: true, surface: "browser", target_ref: REF, target_fingerprint: F1, target: { origin: "https://example.test" } };
  env.drivers.resolveRef = async () => env.live;
  env.verify = () => {
    const signer = loadSigner({ home: env.dirs.root });
    const file = path.join(env.dirs.receipts, "s1.jsonl");
    const text = readFileSync(file, "utf8");
    const records = text.trim().split("\n").map((l) => JSON.parse(l)).filter((r) => r.schema === "telos.receipt/v1");
    return { v: verifyChain(text, { trustedKey: { key_id: signer.key_id, public_key: signer.public_key } }), records, signer };
  };
  env.refGrant = () => env.grant({ tier: "T3", verbs: ["browser.click-ref", "browser.fill-ref"], scope: { origins: ["https://example.test"] }, max_actions: 5 });
  return env;
}

test("hold, human approval and redemption land on one signed chain that verifies pinned", async () => {
  const env = chainEnv();
  const grant = env.refGrant();
  const broker = env.broker({ recorder: env.chain });
  const held = await broker.call({ verb: "browser.click-ref", params: [REF] });
  assert.equal(held.status, "HOLD");
  env.decide(held.hold_id);
  const ok = await broker.call({ verb: "browser.click-ref", params: [REF], hold_id: held.hold_id });
  assert.equal(ok.status, "OK", JSON.stringify(ok));
  assert.equal(env.calls.length, 1);
  const { v, records, signer } = env.verify();
  assert.equal(v.verdict, "MATCH", v.reason);
  assert.deepEqual(records.map((r) => r.status), ["HOLD", "APPROVED", "OK"]);
  assert.ok(records.every((r) => r.action_digest === held.action_digest), "one digest from hold to effect");
  assert.ok(records.every((r) => r.resolution === "ref" && r.target_ref === REF && r.target_fingerprint === F1));
  assert.equal(signer.key_id, keyId(env.publicKey), "the receipts are signed by the key that signed the grant");
  assert.equal(grant.signature.key_id, signer.key_id);
});

test("an element that changed after approval cannot borrow it: a new hold, no driver call", async () => {
  const env = chainEnv();
  env.refGrant();
  const broker = env.broker({ recorder: env.chain });
  const held = await broker.call({ verb: "browser.click-ref", params: [REF] });
  env.decide(held.hold_id);
  env.live = { ...env.live, target_fingerprint: F2 };
  const again = await broker.call({ verb: "browser.click-ref", params: [REF], hold_id: held.hold_id });
  assert.equal(again.status, "HOLD");
  assert.equal(again.reason, "DIGEST_MISMATCH");
  assert.equal(env.calls.length, 0);
  assert.equal(env.verify().v.verdict, "MATCH");
});

test("ref failures refuse before any grant decision: secret, stale, mismatch and a moved page", async () => {
  for (const [live, reason] of [
    [{ ok: false, code: "SECRET_FIELD" }, "SECRET_FIELD"],
    [{ ok: false, code: "STALE_REF" }, "STALE_REF"],
    [{ ok: false, code: "FINGERPRINT_MISMATCH" }, "FINGERPRINT_MISMATCH"],
    [{ ok: false, code: "SOMETHING_ELSE" }, "TARGET_NOT_FOUND"],
    [{ ok: true, surface: "browser", target_ref: REF, target_fingerprint: F1, target: { origin: "https://other.test" } }, "FINGERPRINT_MISMATCH"],
  ]) {
    const env = chainEnv();
    env.refGrant();
    env.live = live;
    const r = await env.broker({ recorder: env.chain }).call({ verb: "browser.fill-ref", params: [REF, "hello"] });
    assert.equal(r.status, "REFUSED", reason);
    assert.equal(r.reason, reason);
    assert.equal(env.calls.length, 0);
    assert.equal(env.verify().v.verdict, "MATCH");
  }
});

test("a broker with no ref resolver refuses act-by-ref instead of acting on a raw id", async () => {
  const env = chainEnv();
  env.refGrant();
  delete env.drivers.resolveRef;
  const r = await env.broker({ recorder: env.chain }).call({ verb: "browser.click-ref", params: ["12"] });
  assert.equal(r.status, "REFUSED");
  assert.equal(r.reason, "REF_RESOLVER_UNAVAILABLE");
  assert.equal(env.calls.length, 0);
});

test("unknown verbs and driver errors are recorded in the verifier's vocabulary", async () => {
  const env = chainEnv();
  env.grant({ tier: "T2", verbs: ["device.write"], scope: { sandbox_roots: [env.sandbox] } });
  mkdirSync(env.sandbox, { recursive: true });
  env.executor = async () => { throw new Error("disk full"); };
  const broker = env.broker({ recorder: env.chain });
  const unknown = await broker.call({ verb: "browser.teleport", params: [] });
  assert.equal(unknown.status, "REFUSED");
  assert.equal(unknown.recorder_error, undefined, "the refusal was recorded");
  const err = await broker.call({ verb: "device.write", params: [path.join(env.sandbox, "a.txt"), "x"] });
  assert.equal(err.status, "ERROR");
  assert.equal(err.recorder_error, undefined);
  const { v, records } = env.verify();
  assert.equal(v.verdict, "MATCH", v.reason);
  assert.deepEqual(records.map((r) => [r.status, r.tier, r.executed]), [["REFUSED", "T5", false], ["APPROVED", "T2", false], ["ERROR", "T2", true]]);
});

test("the dispatcher acts by ref only after re-resolution; a raw node id never reaches the page", async () => {
  const sends = [];
  const session = { send: async (m) => { sends.push(m); return {}; } };
  const refuse = (code) => async () => ({ ok: false, code });
  await assert.rejects(actByRef(session, "click-ref", ["12"]), /BAD_REF/);
  await assert.rejects(actByRef(session, "fill-ref", [REF, "x"], { resolve: refuse("SECRET_FIELD") }), /SECRET_FIELD/);
  await assert.rejects(actByRef(session, "click-ref", [REF], { resolve: refuse("FINGERPRINT_MISMATCH") }), /FINGERPRINT_MISMATCH/);
  assert.deepEqual(sends, [], "no CDP command was sent for a refused ref");
});
