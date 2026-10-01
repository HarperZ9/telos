// telos.grant/v1 (DESIGN.md 1.2). A grant is written only by a human at an
// interactive terminal, signed with the Telos key, and checked again on every
// load. The model can never write, widen or approve one: an edited file fails
// its signature, and a grant that lists a verb above its own tier is refused.
import { randomBytes } from "node:crypto";
import { appendFileSync, existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { canonical, digestOf } from "./canonical.mjs";
import { keyId, requireTty, signText, verifyText } from "./keys.mjs";
import { LADDER, TIERS, tierRank, verbSpec } from "./tiers.mjs";

export const GRANT_SCHEMA = "telos.grant/v1";
export const SCOPE_KEYS = Object.freeze(["origins", "windows", "paths", "sandbox_roots", "exec_allow", "devices", "senses"]);
const REVOCATIONS = "revocations.jsonl";
const SKEW_MS = 60_000;

export function normalizeScope(scope = {}) {
  const out = {};
  for (const key of SCOPE_KEYS) out[key] = Array.isArray(scope[key]) ? scope[key] : [];
  return out;
}

const unsigned = (grant) => {
  const { signature, ...rest } = grant;
  return rest;
};

function checkVerbs(grant) {
  if (!Array.isArray(grant.verbs) || grant.verbs.length === 0) return "verbs_missing";
  for (const verb of grant.verbs) {
    if (verb === "*") {
      if (grant.tier !== "T1") return "wildcard_above_T1";
      continue;
    }
    const spec = verbSpec(verb);
    if (!spec) return `unknown_verb:${verb}`;
    if (tierRank(spec.tier) > tierRank(grant.tier)) return `verb_above_grant_tier:${verb}`;
  }
  return null;
}

function checkTimes(grant, now) {
  const issued = Date.parse(grant.issued_at);
  const expires = Date.parse(grant.expires_at);
  if (!Number.isFinite(issued) || !Number.isFinite(expires)) return "bad_timestamps";
  if (expires - issued > LADDER[grant.tier].ceiling_s * 1000) return "expiry_over_ceiling";
  if (expires <= issued) return "bad_timestamps";
  if (now >= expires) return "expired";
  if (now < issued - SKEW_MS) return "not_yet_valid";
  return null;
}

function checkLimits(grant) {
  const batch = grant.batch ?? 1;
  if (!Number.isSafeInteger(batch) || batch < 1 || batch > LADDER[grant.tier].batch_max) return "batch_out_of_range";
  if (grant.max_actions !== undefined && (!Number.isSafeInteger(grant.max_actions) || grant.max_actions < 1)) return "bad_max_actions";
  if (tierRank(grant.tier) >= tierRank("T3") && grant.max_actions === undefined) return "max_actions_required";
  return null;
}

// Pure shape and policy check, signature excluded.
export function checkGrantBody(grant, { now }) {
  if (!grant || grant.schema !== GRANT_SCHEMA) return "bad_schema";
  if (typeof grant.grant_id !== "string" || !/^g_[0-9a-f]{32}$/.test(grant.grant_id)) return "bad_grant_id";
  if (!TIERS.includes(grant.tier) || grant.tier === "T0") return "bad_tier";
  const scope = normalizeScope(grant.scope);
  if (grant.scope_sha256 !== digestOf(scope)) return "scope_digest_mismatch";
  return checkVerbs(grant) || checkTimes(grant, now) || checkLimits(grant);
}

export function validateGrant(grant, { publicKey, now = Date.now(), revoked = new Set() } = {}) {
  const body = checkGrantBody(grant, { now });
  if (body) return { ok: false, reason: body };
  if (!publicKey) return { ok: false, reason: "no_public_key" };
  const sig = grant.signature || {};
  if (sig.alg !== "ed25519" || sig.key_id !== keyId(publicKey)) return { ok: false, reason: "wrong_key" };
  if (!verifyText(publicKey, canonical(unsigned(grant)), sig.sig)) return { ok: false, reason: "bad_signature" };
  if (revoked.has(grant.grant_id)) return { ok: false, reason: "revoked" };
  return { ok: true };
}

export function issueGrant(spec, { privateKey, publicKey, now = Date.now(), isTTY, idGen } = {}) {
  requireTty(isTTY, "telos grant");
  const scope = normalizeScope(spec.scope);
  const tier = spec.tier;
  const ttl = spec.ttl_s ?? LADDER[tier]?.ceiling_s;
  const body = {
    schema: GRANT_SCHEMA,
    grant_id: idGen ? idGen() : `g_${randomBytes(16).toString("hex")}`,
    tier,
    verbs: spec.verbs,
    scope,
    max_actions: spec.max_actions,
    batch: spec.batch ?? 1,
    issued_at: new Date(now).toISOString(),
    expires_at: new Date(now + ttl * 1000).toISOString(),
    owner_ref: spec.owner_ref ?? "owner_local",
    scope_sha256: digestOf(scope),
  };
  const problem = checkGrantBody(body, { now });
  if (problem) throw new Error(`grant refused: ${problem}`);
  const signature = { alg: "ed25519", key_id: keyId(publicKey), sig: signText(privateKey, canonical(body)) };
  return { ...body, signature };
}

export function saveGrant(dir, grant) {
  mkdirSync(dir, { recursive: true, mode: 0o700 });
  const file = path.join(dir, `${grant.grant_id}.json`);
  writeFileSync(file, `${JSON.stringify(grant, null, 2)}\n`, { flag: "wx", mode: 0o600 });
  return file;
}

// Revocation only narrows, so any revocation line counts, signed or not.
export function revokeGrant(dir, grantId, { now = Date.now(), isTTY } = {}) {
  requireTty(isTTY, "telos grant revoke");
  mkdirSync(dir, { recursive: true, mode: 0o700 });
  appendFileSync(path.join(dir, REVOCATIONS), `${JSON.stringify({ grant_id: grantId, revoked_at: new Date(now).toISOString() })}\n`);
}

export function readRevocations(dir) {
  const file = path.join(dir, REVOCATIONS);
  const out = new Set();
  if (!existsSync(file)) return out;
  for (const line of readFileSync(file, "utf8").split("\n")) {
    try {
      const rec = JSON.parse(line);
      if (typeof rec.grant_id === "string") out.add(rec.grant_id);
    } catch {
      // a torn or blank line revokes nothing and hides nothing
    }
  }
  return out;
}

export function loadGrants(dir, { publicKey, now = Date.now() } = {}) {
  const live = [];
  const rejected = [];
  if (!existsSync(dir)) return { live, rejected };
  const revoked = readRevocations(dir);
  for (const name of readdirSync(dir).filter((n) => /^g_[0-9a-f]{32}\.json$/.test(n)).sort()) {
    let grant;
    try {
      grant = JSON.parse(readFileSync(path.join(dir, name), "utf8"));
    } catch {
      rejected.push({ file: name, reason: "unreadable" });
      continue;
    }
    const verdict = validateGrant(grant, { publicKey, now, revoked });
    if (verdict.ok && `${grant.grant_id}.json` === name) live.push(grant);
    else rejected.push({ file: name, grant_id: grant?.grant_id ?? null, reason: verdict.reason ?? "file_name_mismatch" });
  }
  return { live, rejected };
}
