// Tests for the personhood boundary: gate classification, the prepare handoff
// disposition, and that no evasion action is reachable from the shipped runner
// or via adapter path-traversal. See native-control/BOUNDARY.md. The owned-
// property guard that walls the forging surface is tested with that code, in
// native-control/redteam/guard.test.mjs.

import test from "node:test";
import assert from "node:assert/strict";

import { classifyGate, detectGateExpression, operatorAction } from "./native-control/gate.mjs";
import { disposition, requiredEmptyExpression } from "./native-control/prepare.mjs";
import { defaultRegistry, loadAdapter, isSubmitAct } from "./native-control/runner.mjs";
import { classifyAuth, authCheckExpression } from "./native-control/auth.mjs";
import { encryptBlob, decryptBlob, originMatches, fillLoginExpression, setEntry, list as vaultList } from "./native-control/vault.mjs";
import { addItems } from "./native-control/queue.mjs";
import * as compose from "./native-control/compose.mjs";
import * as sendlog from "./native-control/outreach-log.mjs";
import { guardedSend } from "./native-control/guarded-send.mjs";
import { mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";

// ---- gate classification (pure) ----

test("classifyGate flags a captcha widget as a personhood gate", () => {
  const v = classifyGate({ hasCaptchaWidget: true });
  assert.equal(v.gate, "captcha");
  assert.equal(v.personhood, true);
});

test("classifyGate flags password as login, otp as mfa", () => {
  assert.equal(classifyGate({ passwords: 1 }).gate, "login");
  assert.equal(classifyGate({ otp: 1 }).gate, "mfa");
});

test("classifyGate: an OPEN legal attestation gates and outranks a captcha", () => {
  const v = classifyGate({ hasCaptchaWidget: true, attestations: [{ checked: false, hint: "i certify" }] });
  assert.equal(v.gate, "legal");
  assert.equal(v.personhood, true);
});

test("classifyGate: a CHECKED attestation alone does not gate", () => {
  const v = classifyGate({ attestations: [{ checked: true, hint: "i certify" }] });
  assert.equal(v.gate, "none");
  assert.equal(v.personhood, false);
});

test("classifyGate: payment outranks everything", () => {
  const v = classifyGate({ hasCaptchaWidget: true, passwords: 1, esign: 1, payment: 1 });
  assert.equal(v.gate, "payment");
});

test("classifyGate: a plain filled form is not a gate", () => {
  const v = classifyGate({ hasCaptchaWidget: false, passwords: 0, otp: 0, attestations: [], esign: 0, payment: 0 });
  assert.equal(v.gate, "none");
  assert.equal(v.personhood, false);
});

test("operatorAction: payment guidance states the tool never moves money", () => {
  assert.match(operatorAction("payment"), /never moves money/i);
  for (const g of ["captcha", "login", "mfa", "legal", "esign", "none"]) {
    assert.ok(operatorAction(g).length > 0);
  }
});

test("detectGateExpression scans for every gate class", () => {
  const e = detectGateExpression();
  for (const needle of ["recaptcha", "type=password", "one-time-code", "signature", "cc-number", "under penalty"]) {
    assert.ok(e.includes(needle), `expression should probe for ${needle}`);
  }
});

// ---- prepare disposition (pure) ----

test("disposition: a personhood gate is operator-gated", () => {
  const d = disposition({ filled: ["a"] }, { personhood: true, gate: "captcha", action: "Solve it." }, []);
  assert.equal(d.disposition, "operator-gated");
  assert.equal(d.next_action, "Solve it.");
});

test("disposition: a login form (no other gate) is operator-gated", () => {
  const d = disposition({ login: true, filled: [] }, { personhood: false, gate: "none" }, []);
  assert.equal(d.disposition, "operator-gated");
});

test("disposition: unfilled required fields need operator input", () => {
  const d = disposition({ filled: [] }, { personhood: false, gate: "none" }, ["Cover letter"]);
  assert.equal(d.disposition, "needs-operator-input");
});

test("disposition: clean + no gate is ready-to-review", () => {
  const d = disposition({ filled: ["a", "b"] }, { personhood: false, gate: "none" }, []);
  assert.equal(d.disposition, "ready-to-review");
});

test("requiredEmptyExpression probes required empty fields", () => {
  assert.match(requiredEmptyExpression(), /required/);
});

// ---- the shipped runner exposes NO evasion action ----

test("defaultRegistry has the honest actions and none of the evasion ones", () => {
  const R = defaultRegistry();
  for (const good of ["navigate", "autofill", "prepare", "gate", "handoff"]) {
    assert.ok(R.has(good), `registry should expose ${good}`);
  }
  for (const banned of ["stealth", "warmup", "captcha", "token"]) {
    assert.equal(R.has(banned), false, `registry must NOT expose ${banned}`);
  }
});

// ---- auth: observe sign-in, never harvest ----

test("classifyAuth reads login form as not-authed, account affordance as authed", () => {
  assert.equal(classifyAuth({ loginForm: true }).authed, false);
  assert.equal(classifyAuth({ account: true }).authed, true);
});

test("classifyAuth returns unknown rather than guessing from absence", () => {
  assert.equal(classifyAuth({ loginForm: false, account: false }).authed, "unknown");
});

test("authCheckExpression observes the page, does not touch cookies/tokens", () => {
  const e = authCheckExpression();
  assert.ok(e.includes("input[type=password]"));
  assert.equal(/cookie|document\.cookie|localStorage|token/i.test(e), false);
});

// ---- credential vault: encrypted, host-scoped, no secret leakage, no TOTP ----

test("vault encrypt/decrypt round-trips under the passphrase and fails without it", () => {
  const blob = encryptBlob({ "example.com": { username: "u", password: "s3cret" } }, "pass");
  assert.deepEqual(decryptBlob(blob, "pass"), { "example.com": { username: "u", password: "s3cret" } });
  assert.throws(() => decryptBlob(blob, "wrong"));
  assert.ok(!blob.includes("s3cret")); // ciphertext, not plaintext
});

test("encryptBlob refuses with no passphrase (never writes plaintext)", () => {
  assert.throws(() => encryptBlob({ a: 1 }, ""), /VAULT_LOCKED/);
});

test("originMatches is exact (anti-phishing): no subdomain widening", () => {
  assert.equal(originMatches("example.com", "example.com"), true);
  assert.equal(originMatches("example.com:443", "example.com"), true);
  assert.equal(originMatches("accounts.example.com", "example.com"), false);
  assert.equal(originMatches("evil.com", "example.com"), false);
});

test("fillLoginExpression host-checks in-page and fills no second factor", () => {
  const e = fillLoginExpression("u", "p", "example.com");
  assert.ok(e.includes("location.host"));
  assert.ok(e.includes("input[type=password]"));
  assert.equal(/otp|totp|one-time-code|mfa|2fa/i.test(e), false);
});

test("vault list never returns passwords", () => {
  const dir = mkdtempSync(path.join(tmpdir(), "telos-vault-"));
  const opts = { path: path.join(dir, "v.enc"), passphrase: "pw" };
  setEntry({ host: "example.com", username: "me", password: "topsecret" }, opts);
  const rows = vaultList(opts);
  assert.equal(rows.length, 1);
  assert.equal(rows[0].host, "example.com");
  assert.equal(rows[0].username, "me");
  assert.equal("password" in rows[0], false);
  assert.equal(JSON.stringify(rows).includes("topsecret"), false);
});

// ---- queue: dedup by url ----

test("queue addItems dedups by url and marks pending", () => {
  const s = addItems({ items: [] }, ["https://a.test/1", "https://a.test/1", { url: "https://a.test/2", kind: "contact" }]);
  assert.equal(s.items.length, 2);
  assert.equal(s.items[1].kind, "contact");
  assert.ok(s.items.every((i) => i.status === "pending"));
});

// ---- outreach hygiene: compose, compliance, dedup, rate limit ----

test("compose.render fills tokens and reports missing ones (never silent-blanks)", () => {
  const { text, missing } = compose.render("Hi {{name}} at {{company}}", { name: "Sam" });
  assert.ok(text.includes("Sam"));
  assert.ok(text.includes("{{company}}")); // unresolved left visible
  assert.deepEqual(missing, ["company"]);
});

test("complianceCheck requires opt-out and physical address", () => {
  const bad = compose.complianceCheck("Buy my thing", { senderAddress: "123 Main St" });
  assert.equal(bad.compliant, false);
  assert.ok(bad.missing.some((m) => /opt-out/i.test(m)));
  const good = compose.complianceCheck("Buy my thing. Unsubscribe here. 123 Main St", { senderAddress: "123 Main St" });
  assert.equal(good.compliant, true);
});

test("sendlog dedups a recipient and honors --resend override", () => {
  const state = { sends: [{ to: "a@x.com", subject: "hi", at: "2026-01-01T00:00:00Z" }] };
  assert.equal(sendlog.checkSend(state, "A@X.com", { nowMs: Date.parse("2026-01-01T01:00:00Z") }).allow, false);
  assert.equal(sendlog.checkSend(state, "A@X.com", { nowMs: Date.parse("2026-01-01T01:00:00Z"), resend: true }).allow, true);
  assert.equal(sendlog.checkSend(state, "new@x.com", { nowMs: Date.parse("2026-01-01T01:00:00Z") }).allow, true);
});

test("sendlog rate-limits within the rolling hour", () => {
  const now = Date.parse("2026-01-01T12:00:00Z");
  const sends = Array.from({ length: 20 }, (_, i) => ({ to: `u${i}@x.com`, at: new Date(now - i * 1000).toISOString() }));
  const r = sendlog.checkSend({ sends }, "fresh@x.com", { nowMs: now, rate: { max: 20, windowMs: 3600_000 } });
  assert.equal(r.allow, false);
  assert.match(r.reason, /rate limit/);
});

// ---- guarded send: the single outbound path, used by verb AND runner ----

test("guardedSend blocks non-compliant email before it reaches the sender", async () => {
  let called = false;
  const r = await guardedSend(null, { to: "a@b.com", body: "no opt-out here", skipCompliance: false, sendFn: async () => { called = true; return { confirm: { sent: true } }; } });
  assert.equal(r.blocked, true);
  assert.equal(called, false); // never sent
});

test("guardedSend records only a CONFIRMED send (unconfirmed does not poison dedup)", async () => {
  const dir = mkdtempSync(path.join(tmpdir(), "telos-sl-"));
  const saved = { p: process.env.TELOS_SENDLOG_PATH, a: process.env.TELOS_SENDER_ADDRESS };
  process.env.TELOS_SENDLOG_PATH = path.join(dir, "sl.json");
  process.env.TELOS_SENDER_ADDRESS = "123 Main St, Town WA 98101";
  const body = "Hello. Unsubscribe here. 123 Main St, Town WA 98101";
  try {
    const un = await guardedSend(null, { to: "x@y.com", body, skipCompliance: false, nowMs: 1e12, sendFn: async () => ({ confirm: { sent: false } }) });
    assert.equal(un.recorded, false);
    assert.equal(sendlog.load().sends.length, 0); // not recorded

    const ok = await guardedSend(null, { to: "x@y.com", body, skipCompliance: false, nowMs: 1e12, sendFn: async () => ({ confirm: { sent: true } }) });
    assert.equal(ok.recorded, true);
    assert.equal(sendlog.load().sends.length, 1); // recorded once
  } finally {
    process.env.TELOS_SENDLOG_PATH = saved.p; process.env.TELOS_SENDER_ADDRESS = saved.a;
    if (saved.p == null) delete process.env.TELOS_SENDLOG_PATH;
    if (saved.a == null) delete process.env.TELOS_SENDER_ADDRESS;
  }
});

test("runner contact.send action routes through the guard (no bypass)", async () => {
  const handler = defaultRegistry().get("contact.send");
  const r = await handler({ session: null }, { to: "a@b.com", body: "no opt-out" });
  assert.equal(r.blocked, true); // compliance-blocked via the guarded path, not sent
});

// ---- adapter loading cannot path-traverse to redteam ----

test("loadAdapter refuses a path-traversal name (no reaching redteam/)", async () => {
  await assert.rejects(() => loadAdapter("../redteam/evade"), /unknown adapter/);
  await assert.rejects(() => loadAdapter("../redteam/captcha"), /unknown adapter/);
  await assert.rejects(() => loadAdapter("./x/../../secret"), /unknown adapter/);
});

test("loadAdapter loads a known adapter and null for none", async () => {
  assert.equal(await loadAdapter(null), null);
  const gh = await loadAdapter("greenhouse");
  assert.equal(gh.name, "greenhouse");
});

// ---- submit acts force a gate check ----

test("isSubmitAct catches submit and adapter.submit variants", () => {
  assert.equal(isSubmitAct("submit"), true);
  assert.equal(isSubmitAct("adapter.submit"), true);
  assert.equal(isSubmitAct("greenhouse.submit"), true);
  assert.equal(isSubmitAct("navigate"), false);
  assert.equal(isSubmitAct("autofill"), false);
});
