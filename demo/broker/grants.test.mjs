// Grants: written only at a terminal, signed, and re-checked on every load.
// Each test is an attempt to obtain more than the human granted.
import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { canonical, digestOf } from "./canonical.mjs";
import { issueGrant, loadGrants, revokeGrant, saveGrant, validateGrant } from "./grants.mjs";
import { generateKeys, keyId, signText } from "./keys.mjs";
import { makeEnv, T0 } from "./harness.test.mjs";

const base = { tier: "T3", verbs: ["browser.click"], scope: { origins: ["https://example.test"] }, max_actions: 5 };

test("issuing a grant without an interactive terminal is refused", () => {
  const env = makeEnv();
  for (const isTTY of [false, undefined, "true", 1]) {
    assert.throws(() => issueGrant(base, { privateKey: env.privateKey, publicKey: env.publicKey, now: T0, isTTY }), /interactive terminal/);
  }
});

test("a signed grant loads and an edited copy does not", () => {
  const env = makeEnv();
  const g = env.grant(base);
  assert.equal(loadGrants(env.dirs.grants, { publicKey: env.publicKey, now: T0 }).live.length, 1);
  const file = path.join(env.dirs.grants, `${g.grant_id}.json`);
  const edited = JSON.parse(readFileSync(file, "utf8"));
  edited.verbs.push("browser.fill");
  writeFileSync(file, JSON.stringify(edited));
  const { live, rejected } = loadGrants(env.dirs.grants, { publicKey: env.publicKey, now: T0 });
  assert.equal(live.length, 0);
  assert.equal(rejected[0].reason, "bad_signature");
});

test("widening scope by hand breaks the scope digest", () => {
  const env = makeEnv();
  const g = issueGrant(base, { privateKey: env.privateKey, publicKey: env.publicKey, now: T0, isTTY: true });
  const wider = { ...g, scope: { ...g.scope, origins: ["https://example.test", "https://bank.test"] } };
  assert.equal(validateGrant(wider, { publicKey: env.publicKey, now: T0 }).reason, "scope_digest_mismatch");
});

test("a grant signed by another key is refused even when the body is valid", () => {
  const env = makeEnv();
  const other = generateKeys();
  const g = issueGrant(base, { privateKey: other.privateKey, publicKey: other.publicKey, now: T0, isTTY: true });
  assert.equal(validateGrant(g, { publicKey: env.publicKey, now: T0 }).reason, "wrong_key");
  const forged = { ...g, signature: { ...g.signature, key_id: keyId(env.publicKey) } };
  assert.equal(validateGrant(forged, { publicKey: env.publicKey, now: T0 }).reason, "bad_signature");
});

test("a grant cannot list a verb above its own tier", () => {
  const env = makeEnv();
  const keys = { privateKey: env.privateKey, publicKey: env.publicKey, now: T0, isTTY: true };
  assert.throws(() => issueGrant({ ...base, verbs: ["device.exec"] }, keys), /verb_above_grant_tier:device\.exec/);
  assert.throws(() => issueGrant({ tier: "T1", verbs: ["browser.click"], scope: {} }, keys), /verb_above_grant_tier/);
  assert.throws(() => issueGrant({ tier: "T4", verbs: ["app.input"], scope: {}, max_actions: 1 }, keys), /verb_above_grant_tier:app\.input/);
});

test("a hand-signed grant that lists a verb above its tier still fails to load", () => {
  const env = makeEnv();
  const scope = { origins: ["https://example.test"], windows: [], paths: [], sandbox_roots: [], exec_allow: [], devices: [], senses: [] };
  const body = {
    schema: "telos.grant/v1", grant_id: `g_${"a".repeat(32)}`, tier: "T3", verbs: ["browser.eval"], scope, max_actions: 1, batch: 1,
    issued_at: new Date(T0).toISOString(), expires_at: new Date(T0 + 600_000).toISOString(), owner_ref: "owner_local", scope_sha256: digestOf(scope),
  };
  const g = { ...body, signature: { alg: "ed25519", key_id: keyId(env.publicKey), sig: signText(env.privateKey, canonical(body)) } };
  assert.equal(validateGrant(g, { publicKey: env.publicKey, now: T0 }).reason, "verb_above_grant_tier:browser.eval");
});

test("wildcards: none above T1, and a T1 wildcard is not a screen grant", () => {
  const env = makeEnv();
  const keys = { privateKey: env.privateKey, publicKey: env.publicKey, now: T0, isTTY: true };
  assert.throws(() => issueGrant({ ...base, verbs: ["*"] }, keys), /wildcard_above_T1/);
  assert.ok(issueGrant({ tier: "T1", verbs: ["*"], scope: { senses: ["*"] } }, keys));
});

test("expiry beyond the tier ceiling, expired grants and revoked grants are refused", () => {
  const env = makeEnv();
  const keys = { privateKey: env.privateKey, publicKey: env.publicKey, now: T0, isTTY: true };
  assert.throws(() => issueGrant({ ...base, ttl_s: 3601 }, keys), /expiry_over_ceiling/);
  assert.throws(() => issueGrant({ tier: "T4", verbs: ["device.exec"], scope: {}, max_actions: 1, ttl_s: 901 }, keys), /expiry_over_ceiling/);
  const g = env.grant(base);
  assert.equal(validateGrant(g, { publicKey: env.publicKey, now: T0 + 3600_000 }).reason, "expired");
  assert.throws(() => revokeGrant(env.dirs.grants, g.grant_id, { isTTY: false }), /interactive terminal/);
  revokeGrant(env.dirs.grants, g.grant_id, { isTTY: true });
  const { live, rejected } = loadGrants(env.dirs.grants, { publicKey: env.publicKey, now: T0 });
  assert.equal(live.length, 0);
  assert.equal(rejected[0].reason, "revoked");
});

test("batching is capped at 10 for T3 and refused for T4 and T5; T3+ needs max_actions", () => {
  const env = makeEnv();
  const keys = { privateKey: env.privateKey, publicKey: env.publicKey, now: T0, isTTY: true };
  assert.throws(() => issueGrant({ ...base, batch: 11 }, keys), /batch_out_of_range/);
  assert.throws(() => issueGrant({ tier: "T4", verbs: ["device.exec"], scope: {}, max_actions: 1, batch: 2 }, keys), /batch_out_of_range/);
  assert.throws(() => issueGrant({ tier: "T3", verbs: ["browser.click"], scope: {} }, keys), /max_actions_required/);
  assert.ok(issueGrant({ ...base, batch: 10 }, keys));
});

test("a grant file renamed to another grant id does not load", () => {
  const env = makeEnv();
  const g = issueGrant(base, { privateKey: env.privateKey, publicKey: env.publicKey, now: T0, isTTY: true });
  saveGrant(env.dirs.grants, g);
  writeFileSync(path.join(env.dirs.grants, `g_${"b".repeat(32)}.json`), JSON.stringify(g));
  const { live, rejected } = loadGrants(env.dirs.grants, { publicKey: env.publicKey, now: T0 });
  assert.equal(live.length, 1);
  assert.equal(rejected[0].reason, "file_name_mismatch");
});
