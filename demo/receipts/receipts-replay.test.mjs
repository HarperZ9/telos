// Dry run and replay (DESIGN 4.3, 4.4) against a fake world. The fakes stand in
// for the broker's gate, the ref resolver and the drivers, so these tests pin
// the receipt contract: dry run never acts, replay re-gates and re-holds every
// step, and every stop names the step and the field that diverged.
import assert from "node:assert/strict";
import { mkdtempSync, readFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { ReceiptChain } from "./chain.mjs";
import { argsSha256, fingerprintSha256, tierRank } from "./digest.mjs";
import { dryRun } from "./dry-run.mjs";
import { ephemeralSigner } from "./keys.mjs";
import { replay } from "./replay.mjs";
import { parseJsonl, sha256Hex } from "./verify.mjs";

const tmp = () => mkdtempSync(path.join(os.tmpdir(), "telos-replay-"));
const TIER = { "file.write": "T2", "browser.click": "T3", "browser.fill": "T3", "exec.run": "T4", "observe.snapshot": "T1" };

function world() {
  return {
    elements: {
      "b:1:aaaa0000:7": { role: "button", name: "Save", state: "idle" },
      "b:1:aaaa0000:9": { role: "textbox", name: "Title", state: "" }
    },
    calls: []
  };
}

function hooks(w, { grants = ["T1", "T2", "T3"], decision = "APPROVED", holdLog = [] } = {}) {
  return {
    resolve: async (step) => {
      const el = w.elements[step.target_ref];
      return el ? { ok: true, target_ref: step.target_ref, target_fingerprint: { role: el.role, name: el.name }, resolution: "ref" }
        : { ok: false, reason: "no such element" };
    },
    gate: async (step) => {
      const tier = TIER[step.verb];
      const allowed = grants.includes(tier);
      return { tier, allowed, needs_hold: tierRank(tier) >= 3, grant_id: allowed ? `g_${tier}` : null,
        scope_sha256: "c".repeat(64), reason: allowed ? "" : `no ${tier} grant` };
    },
    preState: async (step) => sha256Hex(JSON.stringify(w.elements[step.target_ref])),
    requestHold: async (req) => { holdLog.push(req); return { status: decision, hold_id: `h_${holdLog.length}`, decision_seal: "d".repeat(64) }; },
    execute: async (step, args) => { w.calls.push(step.verb); w.elements[step.target_ref].state = args.value; return { ok: true }; },
    checkPost: async (post, step) => w.elements[step.target_ref].state === post.expect
  };
}

// record - write a session as the broker would: OK receipts with refs,
// fingerprints, pre-state digests, post-conditions and args side files.
function record(w, steps) {
  const chain = ReceiptChain.open({ home: tmp(), session_id: "s_rec", signer: ephemeralSigner() });
  for (const s of steps) {
    const el = w.elements[s.target_ref];
    chain.append({
      tier: TIER[s.verb], verb: s.verb, tool: "telos.act", status: "OK", executed: true,
      target_ref: s.target_ref, target_fingerprint: fingerprintSha256({ role: el.role, name: el.name }),
      pre_state_digest: sha256Hex(JSON.stringify(el)), args_sha256: argsSha256(s.args),
      post_condition: { expect: s.args.value }, post_condition_result: true, hold_id: "h_original", decision_seal: "o".repeat(64)
    }, { side: { "args.json": s.args } });
    el.state = s.args.value;
  }
  chain.close();
  return chain;
}

const STEPS = [
  { verb: "browser.fill", target_ref: "b:1:aaaa0000:9", args: { value: "Draft" } },
  { verb: "browser.click", target_ref: "b:1:aaaa0000:7", args: { value: "saved" } }
];

function setup(opts) {
  const recordedWorld = world();
  const rec = record(recordedWorld, STEPS);
  const live = world();
  const out = ReceiptChain.open({ home: tmp(), session_id: "s_replay", signer: ephemeralSigner() });
  const h = hooks(live, opts);
  h.loadArgs = async (original) => JSON.parse(rec.readSide(original.seal, "args.json"));
  return { rec, live, out, h, text: readFileSync(rec.file, "utf8"), trustedKey: { key_id: rec.signer.key_id, public_key: rec.signer.public_key } };
}

const chainRecords = (chain) => parseJsonl(readFileSync(chain.file, "utf8")).records.map((r) => r.rec).filter((r) => r.schema === "telos.receipt/v1");

test("dry run resolves and gates every step, acts on nothing, and lists the holds", async () => {
  const w = world();
  const h = hooks(w, { grants: ["T1", "T3"] });
  const chain = ReceiptChain.open({ home: tmp(), session_id: "s_dry", signer: ephemeralSigner() });
  const before = JSON.stringify(w.elements);
  const result = await dryRun([
    { verb: "observe.snapshot", target_ref: "b:1:aaaa0000:7", args: {} },
    { verb: "browser.click", target_ref: "b:1:aaaa0000:7", args: {} },
    { verb: "exec.run", target_ref: "b:1:aaaa0000:7", args: { argv: ["git", "status"] } },
    { verb: "browser.click", target_ref: "b:1:gone:1", args: {} }
  ], { resolve: h.resolve, gate: h.gate, chain });
  assert.equal(result.executed, 0);
  assert.equal(JSON.stringify(w.elements), before, "the world is unchanged");
  assert.deepEqual(w.calls, []);
  assert.deepEqual(result.holds.map((s) => s.index), [1]);
  assert.deepEqual(result.refusals.map((s) => s.index), [2]);
  assert.deepEqual(result.unresolved.map((s) => s.index), [3]);
  const recs = chainRecords(chain);
  assert.ok(recs.every((r) => r.status === "DRY_RUN" && r.executed === false));
  assert.equal(recs[1].would_hold, true);
  assert.equal(recs[1].action_digest.length, 64);
  assert.equal(chain.verify().verdict, "MATCH");
});

test("replay re-gates, raises a fresh hold per T3 step, and cites the original seals", async () => {
  const holdLog = [];
  const s = setup({ holdLog });
  const result = await replay(s.text, s.h, { chain: s.out, trustedKey: s.trustedKey });
  assert.equal(result.status, "COMPLETE");
  assert.equal(result.replayed, 2);
  assert.equal(holdLog.length, 2, "approvals are never inherited from the recording");
  for (const req of holdLog) assert.equal(JSON.stringify(req).includes("h_original"), false);
  const recs = chainRecords(s.out);
  assert.deepEqual(recs.map((r) => r.status), ["HOLD", "APPROVED", "OK", "HOLD", "APPROVED", "OK"]);
  const originals = chainRecords(s.rec).map((r) => r.seal);
  assert.deepEqual(recs.filter((r) => r.status === "OK").map((r) => r.replay_of), originals);
  assert.equal(s.live.elements["b:1:aaaa0000:7"].state, "saved");
  assert.equal(s.out.verify().verdict, "MATCH");
});

test("a changed element stops replay with DRIFT and a field-level diff", async () => {
  const s = setup();
  s.live.elements["b:1:aaaa0000:7"].name = "Delete";
  const result = await replay(s.text, s.h, { chain: s.out, trustedKey: s.trustedKey });
  assert.equal(result.status, "DRIFT");
  assert.equal(result.stopped_at, 2);
  assert.deepEqual(result.replay_diff.map((d) => d.field), ["target_fingerprint", "pre_state_digest"]);
  assert.deepEqual(s.live.calls, ["browser.fill"], "the drifted step never executes");
});

test("a missing element and a different pre-state each stop replay", async () => {
  const s = setup();
  delete s.live.elements["b:1:aaaa0000:9"];
  const missing = await replay(s.text, s.h, { chain: s.out, trustedKey: s.trustedKey });
  assert.equal(missing.status, "DRIFT");
  assert.match(missing.reason, /target missing/);
  const p = setup();
  p.live.elements["b:1:aaaa0000:9"].state = "someone typed here";
  const pre = await replay(p.text, p.h, { chain: p.out, trustedKey: p.trustedKey });
  assert.equal(pre.status, "DRIFT");
  assert.deepEqual(pre.replay_diff.map((d) => d.field), ["pre_state_digest"]);
  assert.deepEqual(p.live.calls, []);
});

test("no current grant, a rejection, or an expiry stops replay before the effect", async () => {
  const noGrant = setup({ grants: ["T1"] });
  const refused = await replay(noGrant.text, noGrant.h, { chain: noGrant.out, trustedKey: noGrant.trustedKey });
  assert.equal(refused.status, "REFUSED");
  assert.deepEqual(noGrant.live.calls, []);
  for (const decision of ["REJECTED", "EXPIRED"]) {
    const s = setup({ decision });
    const r = await replay(s.text, s.h, { chain: s.out, trustedKey: s.trustedKey });
    assert.equal(r.status, decision);
    assert.deepEqual(s.live.calls, []);
  }
});

test("a pending hold pauses replay; it resumes from startAt", async () => {
  const s = setup({ decision: "PENDING" });
  const paused = await replay(s.text, s.h, { chain: s.out, trustedKey: s.trustedKey });
  assert.equal(paused.status, "HOLD");
  assert.equal(paused.stopped_at, 1);
  assert.equal(chainRecords(s.out).filter((r) => r.status === "HOLD").length, 1, "one hold receipt, not two");
  const approve = hooks(s.live, { decision: "APPROVED" });
  const resumed = await replay(s.text, { ...approve, loadArgs: s.h.loadArgs }, { chain: s.out, trustedKey: s.trustedKey, startAt: 1 });
  assert.equal(resumed.status, "COMPLETE");
});

test("a recording that does not verify is refused and nothing runs", async () => {
  const s = setup();
  const tampered = s.text.replace('"value":"Draft"', '"value":"Evil"').replace(/"post_condition_result":true/, '"post_condition_result":false');
  const r = await replay(tampered, s.h, { chain: s.out, trustedKey: s.trustedKey });
  assert.equal(r.status, "REFUSED");
  assert.match(r.reason, /does not verify/);
  assert.deepEqual(s.live.calls, []);
  const other = ephemeralSigner();
  const wrongKey = await replay(s.text, s.h, { chain: s.out, trustedKey: { key_id: other.key_id, public_key: other.public_key } });
  assert.equal(wrongKey.status, "REFUSED");
});

test("a failed post-condition and altered arguments both stop with DRIFT", async () => {
  const s = setup();
  s.h.checkPost = async () => false;
  const post = await replay(s.text, s.h, { chain: s.out, trustedKey: s.trustedKey });
  assert.equal(post.status, "DRIFT");
  assert.match(post.reason, /post-condition failed/);
  const a = setup();
  a.h.loadArgs = async () => ({ value: "changed" });
  const args = await replay(a.text, a.h, { chain: a.out, trustedKey: a.trustedKey });
  assert.equal(args.status, "DRIFT");
  assert.deepEqual(args.replay_diff.map((d) => d.field), ["args_sha256"]);
  assert.deepEqual(a.live.calls, []);
});
