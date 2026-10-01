// Holds and confirmation: every T3+ call needs a human decision on its exact
// action digest, redeemable once. Each test is a way a model might try to run
// an action without that decision, or run it twice.
import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync, rmSync, writeFileSync } from "node:fs";
import path from "node:path";
import { decideHold, HoldStore } from "./holds.mjs";
import { generateKeys } from "./keys.mjs";
import { makeEnv, t3Grant } from "./harness.test.mjs";

const click = (extra = {}) => ({ verb: "browser.click", params: ["#submit"], ...extra });

async function approvedHold(env, broker, req = click()) {
  const held = await broker.call(req);
  assert.equal(held.status, "HOLD");
  env.decide(held.hold_id);
  return held;
}

test("a T3 call holds on first arrival and the driver is not called", async () => {
  const env = makeEnv();
  t3Grant(env);
  const r = await env.broker().call(click());
  assert.equal(r.status, "HOLD");
  assert.match(r.hold_id, /^h_[0-9a-f]{32}$/);
  assert.equal(r.executed, false);
  assert.equal(env.calls.length, 0);
  assert.equal(JSON.stringify(r).includes("sig"), false, "the tool result carries no approval material");
  assert.equal(env.recorder.entries.at(-1).status, "HOLD", "a sealed hold receipt is written before returning");
});

test("re-issuing with the hold_id before a human decides does not run", async () => {
  const env = makeEnv();
  t3Grant(env);
  const broker = env.broker();
  const held = await broker.call(click());
  const again = await broker.call(click({ hold_id: held.hold_id }));
  assert.equal(again.status, "HOLD");
  assert.equal(again.reason, "AWAITING_HUMAN");
  assert.equal(env.calls.length, 0);
});

test("an approved hold runs exactly once; reusing the hold_id is refused", async () => {
  const env = makeEnv();
  t3Grant(env);
  const broker = env.broker();
  const held = await approvedHold(env, broker);
  const ran = await broker.call(click({ hold_id: held.hold_id }));
  assert.equal(ran.status, "OK");
  assert.equal(ran.executed, true);
  assert.equal(env.calls.length, 1);
  const reuse = await broker.call(click({ hold_id: held.hold_id }));
  assert.equal(reuse.status, "REFUSED");
  assert.equal(reuse.reason, "HOLD_CONSUMED");
  assert.equal(env.calls.length, 1);
});

test("a second broker process cannot redeem the same approval", async () => {
  const env = makeEnv();
  t3Grant(env);
  const a = env.broker();
  const b = env.broker();
  const held = await approvedHold(env, a);
  const results = await Promise.all([a.call(click({ hold_id: held.hold_id })), b.call(click({ hold_id: held.hold_id }))]);
  assert.deepEqual(results.map((r) => r.status).sort(), ["OK", "REFUSED"]);
  assert.equal(env.calls.length, 1);
});

test("an approval cannot be spent on different arguments or a different target", async () => {
  const env = makeEnv();
  t3Grant(env);
  const broker = env.broker();
  const held = await approvedHold(env, broker);
  const swapped = await broker.call({ verb: "browser.click", params: ["#delete-account"], hold_id: held.hold_id });
  assert.equal(swapped.status, "HOLD");
  assert.equal(swapped.reason, "DIGEST_MISMATCH");
  assert.notEqual(swapped.hold_id, held.hold_id);
  const otherVerb = await broker.call({ verb: "browser.fill", params: ["#submit", "x"], hold_id: held.hold_id });
  assert.equal(otherVerb.status, "HOLD");
  assert.equal(env.calls.length, 0);
});

test("an approval from one session cannot be redeemed by another", async () => {
  const env = makeEnv();
  t3Grant(env);
  const held = await approvedHold(env, env.broker());
  const r = await env.broker({ sessionId: "s2" }).call(click({ hold_id: held.hold_id }));
  assert.equal(r.reason, "HOLD_OTHER_SESSION");
  assert.equal(env.calls.length, 0);
});

test("a rejection is durable for that digest; silence is never yes", async () => {
  const env = makeEnv();
  t3Grant(env);
  const broker = env.broker();
  const held = await broker.call(click());
  env.decide(held.hold_id, "reject");
  assert.equal((await broker.call(click({ hold_id: held.hold_id }))).status, "REJECTED");
  const fresh = await broker.call(click());
  assert.equal(fresh.status, "REJECTED");
  assert.equal(fresh.reason, "REJECTED_DIGEST");
  const quiet = await broker.call({ verb: "browser.click", params: ["#other"] });
  env.clock.t += 121_000;
  const late = await broker.call({ verb: "browser.click", params: ["#other"], hold_id: quiet.hold_id });
  assert.equal(late.status, "EXPIRED");
  assert.equal(env.calls.length, 0);
});

test("an approval used after its window closes raises a new hold", async () => {
  const env = makeEnv();
  t3Grant(env);
  const broker = env.broker();
  const held = await approvedHold(env, broker);
  env.clock.t += 121_000;
  const r = await broker.call(click({ hold_id: held.hold_id }));
  assert.equal(r.status, "EXPIRED");
  assert.match(r.hold_id, /^h_/);
  assert.notEqual(r.hold_id, held.hold_id);
  assert.equal(env.calls.length, 0);
});

test("forged decisions are ignored: unsigned, wrong key, or copied from another hold", async () => {
  const env = makeEnv();
  t3Grant(env);
  const broker = env.broker();
  const held = await broker.call(click());
  const decision = (id) => path.join(env.dirs.holds, `${id}.decision.json`);
  const at = new Date(env.now()).toISOString();
  writeFileSync(decision(held.hold_id), JSON.stringify({ hold_id: held.hold_id, digests: [held.action_digest], decision: "approve", decided_at: at, window_s: 120, channel: "tty" }));
  assert.equal((await broker.call(click({ hold_id: held.hold_id }))).status, "HOLD", "unsigned");

  const intruder = generateKeys();
  const other = new HoldStore({ dir: env.dirs.holds, publicKey: intruder.publicKey, now: env.now });
  rmSync(decision(held.hold_id));
  decideHold(other, held.hold_id, "approve", { privateKey: intruder.privateKey, publicKey: intruder.publicKey, isTTY: true });
  assert.equal((await broker.call(click({ hold_id: held.hold_id }))).status, "HOLD", "wrong key");

  const second = await broker.call({ verb: "browser.click", params: ["#delete-account"] });
  rmSync(decision(held.hold_id));
  env.decide(held.hold_id);
  writeFileSync(decision(second.hold_id), readFileSync(decision(held.hold_id)));
  const borrowed = await broker.call({ verb: "browser.click", params: ["#delete-account"], hold_id: second.hold_id });
  assert.equal(borrowed.status, "HOLD", "a decision copied from another hold");
  assert.equal(env.calls.length, 0);
});

test("deciding a hold needs a terminal, and only a pending hold can be decided", async () => {
  const env = makeEnv();
  t3Grant(env);
  const held = await env.broker().call(click());
  const store = new HoldStore({ dir: env.dirs.holds, publicKey: env.publicKey, now: env.now });
  assert.throws(() => decideHold(store, held.hold_id, "approve", { privateKey: env.privateKey, publicKey: env.publicKey, isTTY: false }), /interactive terminal/);
  env.decide(held.hold_id);
  assert.throws(() => env.decide(held.hold_id), /APPROVED, not PENDING|already exists|EEXIST/);
});

test("caller arguments cannot claim approval or irreversibility", async () => {
  const env = makeEnv();
  t3Grant(env);
  for (const flag of ["approve", "confirm", "yes", "allow-irreversible", "irreversible", "tier", "force"]) {
    const r = await env.broker().call(click({ flags: { [flag]: "true" } }));
    assert.equal(r.status, "REFUSED", flag);
    assert.equal(r.reason, "CALLER_APPROVAL_FLAG", flag);
  }
  assert.equal(env.calls.length, 0);
});

test("a hold that cannot be recorded does not open, and nothing runs", async () => {
  const env = makeEnv();
  t3Grant(env);
  const broken = { append() { throw new Error("disk full"); } };
  const r = await env.broker({ recorder: broken }).call(click());
  assert.equal(r.status, "REFUSED");
  assert.equal(r.reason, "RECORDER_FAILED");
  assert.equal(new HoldStore({ dir: env.dirs.holds, publicKey: env.publicKey }).pending().length, 0);
  assert.equal(env.calls.length, 0);
});

test("one approval copied onto a second hold for the same digest runs once at most", async () => {
  const env = makeEnv();
  t3Grant(env);
  const broker = env.broker();
  const a = await broker.call(click());
  const b = await broker.call(click());
  assert.equal(a.action_digest, b.action_digest);
  env.decide(a.hold_id);
  const decision = (id) => path.join(env.dirs.holds, `${id}.decision.json`);
  writeFileSync(decision(b.hold_id), readFileSync(decision(a.hold_id)));
  assert.equal((await broker.call(click({ hold_id: a.hold_id }))).status, "OK");
  const second = await broker.call(click({ hold_id: b.hold_id }));
  assert.notEqual(second.status, "OK");
  assert.equal(env.calls.length, 1);
});

test("editing a hold file after approval cannot retarget the approval", async () => {
  const env = makeEnv();
  t3Grant(env);
  const broker = env.broker();
  const held = await broker.call(click());
  env.decide(held.hold_id);
  const evil = { verb: "browser.click", params: ["#delete-account"] };
  const plan = await broker.call({ ...evil, dry_run: true });
  const file = path.join(env.dirs.holds, `${held.hold_id}.json`);
  const hold = JSON.parse(readFileSync(file, "utf8"));
  hold.digests = [plan.action_digest];
  writeFileSync(file, JSON.stringify(hold));
  const r = await broker.call({ ...evil, hold_id: held.hold_id });
  assert.notEqual(r.status, "OK");
  assert.equal(env.calls.length, 0);
});
