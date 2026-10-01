// The tier gate: default deny, no escalation past a grant's tier or scope, and
// the targets no grant reaches. Every refusal asserts the driver never ran.
import test from "node:test";
import assert from "node:assert/strict";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { makeEnv, t3Grant } from "./harness.test.mjs";

const t1 = (env, scope = {}) => env.grant({ tier: "T1", verbs: ["*"], scope: { senses: ["*"], origins: ["https://example.test"], ...scope } });

test("a T1 grant observes and cannot act: a T3 verb is refused, not held", async () => {
  const env = makeEnv();
  t1(env);
  const broker = env.broker();
  assert.equal((await broker.call({ verb: "browser.snapshot-text" })).status, "OK");
  const act = await broker.call({ verb: "browser.click", params: ["#buy"] });
  assert.equal(act.status, "REFUSED");
  assert.equal(act.reason, "NO_GRANT");
  assert.equal(env.calls.length, 1);
});

test("coordinates raise an observe verb's floor to T3, past a T1 grant", async () => {
  const env = makeEnv();
  env.grant({ tier: "T1", verbs: ["*"], scope: { senses: ["*"], origins: ["https://example.test"] } });
  const r = await env.broker().call({ verb: "browser.input", params: ["click", "10", "20"] });
  assert.equal(r.status, "REFUSED");
  assert.equal(env.calls.length, 0);
});

test("a T2 grant cannot write outside its sandbox: the write promotes to T3", async () => {
  const env = makeEnv();
  mkdirSync(env.sandbox, { recursive: true });
  const outside = path.join(env.root, "outside");
  mkdirSync(outside, { recursive: true });
  env.grant({ tier: "T2", verbs: ["device.write"], scope: { sandbox_roots: [env.sandbox], paths: [outside] } });
  const broker = env.broker();
  const inside = await broker.call({ verb: "device.write", params: [path.join(env.sandbox, "a.txt"), "hello"] });
  assert.equal(inside.status, "OK", JSON.stringify(inside));
  assert.equal(inside.tier, "T2");
  const out = await broker.call({ verb: "device.write", params: [path.join(outside, "b.txt"), "hello"] });
  assert.equal(out.status, "REFUSED");
  assert.equal(out.reason, "TIER_ABOVE_GRANT");
  const traversal = await broker.call({ verb: "device.write", params: [path.join(env.sandbox, "..", "outside", "c.txt"), "x"] });
  assert.equal(traversal.status, "REFUSED");
  assert.equal(env.calls.length, 1);
});

test("a T2 write records its pre-image and a rollback handle", async () => {
  const env = makeEnv();
  mkdirSync(env.sandbox, { recursive: true });
  const file = path.join(env.sandbox, "notes.txt");
  writeFileSync(file, "before");
  env.grant({ tier: "T2", verbs: ["device.write"], scope: { sandbox_roots: [env.sandbox] } });
  const r = await env.broker().call({ verb: "device.write", params: [file, "after"] });
  assert.equal(r.status, "OK");
  assert.match(r.pre_image_digest, /^[0-9a-f]{64}$/);
  assert.equal(readFileSync(path.join(env.dirs.preimages, r.rollback), "utf8"), "before");
  assert.equal(r.verify_result, "DRIFT", "the fake executor wrote nothing, so re-read disagrees");
});

test("a pre-image that cannot be captured promotes the write to T3", async () => {
  const env = makeEnv();
  mkdirSync(path.join(env.sandbox, "adir"), { recursive: true });
  env.grant({ tier: "T2", verbs: ["device.write"], scope: { sandbox_roots: [env.sandbox] } });
  const r = await env.broker().call({ verb: "device.write", params: [path.join(env.sandbox, "adir"), "x"] });
  assert.equal(r.status, "REFUSED");
  assert.equal(r.reason, "TIER_ABOVE_GRANT");
  assert.equal(env.calls.length, 0);
});

test("scope is checked against the resolved target, not the caller's word", async () => {
  const env = makeEnv({ pageUrl: "https://bank.test/transfer" });
  t3Grant(env);
  const r = await env.broker().call({ verb: "browser.click", params: ["#submit"], flags: { origin: "https://example.test" } });
  assert.equal(r.status, "REFUSED");
  assert.equal(r.reason, "OUT_OF_SCOPE");
  const nav = await env.broker().call({ verb: "browser.navigate", params: ["https://evil.test/"] });
  assert.equal(nav.reason, "OUT_OF_SCOPE");
  assert.equal(env.calls.length, 0);
});

test("password, OTP and card fields cannot be targeted under any grant", async () => {
  const env = makeEnv();
  t3Grant(env);
  for (const selector of ["#password", "input[name=otp]", "#card-number", "#CVV", "#mfa-code"]) {
    const r = await env.broker().call({ verb: "browser.fill", params: [selector, "x"] });
    assert.equal(r.reason, "SECRET_FIELD", selector);
  }
  assert.equal(env.calls.length, 0);
});

test("Telos state, terminals and the approval window are protected targets", async () => {
  const env = makeEnv({ windows: [{ title: "Telos confirm", class: "X" }, { title: "PowerShell", class: "CASCADIA_HOSTING_WINDOW_CLASS" }] });
  env.grant({ tier: "T3", verbs: ["app.invoke", "app.setvalue"], scope: { windows: [{ title_contains: "e" }] }, max_actions: 5 });
  const broker = env.broker();
  for (const win of ["Telos confirm", "PowerShell"]) {
    const r = await broker.call({ verb: "app.setvalue", params: [win, "Edit", "y"] });
    assert.equal(r.reason, "PROTECTED_TARGET", win);
  }
  env.grant({ tier: "T1", verbs: ["*"], scope: { senses: ["*"], paths: [env.root] } });
  const key = await broker.call({ verb: "device.read", params: [path.join(env.dirs.keys, "telos-ed25519.key")] });
  assert.equal(key.reason, "PROTECTED_TARGET");
  assert.equal(env.calls.length, 0);
});

test("screen and clipboard are never implied by a wildcard sense", async () => {
  const env = makeEnv();
  t1(env);
  const r = await env.broker().call({ verb: "sense.screen" });
  assert.equal(r.status, "REFUSED");
  assert.equal(env.calls.length, 0);
});

test("reserved hardware verbs are refused whatever the grant", async () => {
  const env = makeEnv();
  for (const verb of ["hardware.power.shutdown", "hardware.ddc.write", "sense.camera"]) {
    const r = await env.broker().call({ verb });
    assert.equal(r.status, "REFUSED", verb);
    assert.match(r.reason, /RESERVED_VERB|PRESENCE_UNAVAILABLE/);
  }
  assert.equal((await env.broker().call({ verb: "hardware.nuke" })).reason, "UNKNOWN_VERB");
});

test("exec: shell metacharacters and argv outside the allowlist are refused; T4 still holds", async () => {
  const env = makeEnv();
  env.grant({ tier: "T4", verbs: ["device.exec"], scope: { exec_allow: [["git", "status"]] }, max_actions: 3 });
  const broker = env.broker();
  for (const cmd of [["git", "status", "&", "del", "x"], ["git", "status;", "rm"], ["git", "push"], ["powershell", "-c", "x"]]) {
    const r = await broker.call({ verb: "device.exec", params: cmd });
    assert.equal(r.status, "REFUSED", cmd.join(" "));
  }
  const ok = await broker.call({ verb: "device.exec", params: ["git", "status"] });
  assert.equal(ok.status, "HOLD");
  assert.equal(env.calls.length, 0);
});

test("max_actions caps redeemed actions under a grant", async () => {
  const env = makeEnv();
  t3Grant(env, { max_actions: 1 });
  const broker = env.broker();
  for (const [i, sel] of ["#a", "#b"].entries()) {
    const held = await broker.call({ verb: "browser.click", params: [sel] });
    env.decide(held.hold_id);
    const r = await broker.call({ verb: "browser.click", params: [sel], hold_id: held.hold_id });
    assert.equal(r.status, i === 0 ? "OK" : "REFUSED");
    if (i === 1) assert.equal(r.reason, "MAX_ACTIONS");
  }
  assert.equal(env.calls.length, 1);
});

test("synthetic input is suspended while another hold is open, and T5 binds to one session", async () => {
  const env = makeEnv();
  t3Grant(env);
  env.grant({ tier: "T5", verbs: ["app.type"], scope: { devices: ["input:synthetic"] }, max_actions: 2 });
  const broker = env.broker();
  await broker.call({ verb: "browser.click", params: ["#a"] });
  const typed = await broker.call({ verb: "app.type", params: ["123456"] });
  assert.equal(typed.reason, "SUSPENDED_DURING_HOLD");
  const other = await env.broker({ sessionId: "s2" }).call({ verb: "app.type", params: ["x"] });
  assert.equal(other.status, "HOLD", "first use binds the T5 grant to s2");
  const back = await env.broker({ sessionId: "s3" }).call({ verb: "app.type", params: ["x"] });
  assert.equal(back.reason, "SESSION_BOUND");
  assert.equal(env.calls.length, 0);
});

test("dry run computes tier and digest, opens no hold and runs nothing", async () => {
  const env = makeEnv();
  t3Grant(env);
  const r = await env.broker().call({ verb: "browser.click", params: ["#submit"], dry_run: true });
  assert.equal(r.status, "DRY_RUN");
  assert.equal(r.would_hold, true);
  assert.match(r.action_digest, /^[0-9a-f]{64}$/);
  assert.equal(existsSync(env.dirs.holds) ? (await import("node:fs")).readdirSync(env.dirs.holds).filter((n) => n.endsWith(".json")).length : 0, 0);
  assert.equal(env.calls.length, 0);
});
