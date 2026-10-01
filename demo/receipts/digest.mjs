// digest.mjs - the action digest (DESIGN 1.3) and argument digests. The action
// digest binds what a human approves: sha256 of the canonical form of
// {tier, verb, target_ref, target_fingerprint, args_sha256, scope_sha256, grant_id}.
// A changed element, argument, scope or grant gives a different digest, so an
// approval for one action cannot be borrowed by another. The broker, dry run and
// replay all compute it here so the three never disagree.
import { canonical, sha256Hex } from "./verify.mjs";

export const ACTION_DIGEST_FIELDS = ["tier", "verb", "target_ref", "target_fingerprint",
  "args_sha256", "scope_sha256", "grant_id"];

// argsSha256 - digest of the canonical arguments. Floats are refused by the
// canonical form; callers pass numbers as integers or decimal strings.
export function argsSha256(args) {
  return sha256Hex(canonical(args ?? {}));
}

// fingerprintSha256 - digest of a fingerprint object (role, name, box and the
// rest, per DESIGN 5.1) so receipts and the action digest carry a fixed string.
export function fingerprintSha256(fingerprint) {
  if (fingerprint === null || fingerprint === undefined) return null;
  return typeof fingerprint === "string" ? fingerprint : sha256Hex(canonical(fingerprint));
}

export function actionDigest(fields) {
  const body = {};
  for (const f of ACTION_DIGEST_FIELDS) {
    const v = fields[f];
    body[f] = v === undefined ? null : v;
  }
  if (typeof body.tier !== "string" || typeof body.verb !== "string") {
    throw new TypeError("action digest needs tier and verb");
  }
  return sha256Hex(canonical(body));
}

export function tierRank(tier) {
  const n = /^T([0-5])$/.exec(String(tier));
  if (!n) throw new TypeError(`unknown tier ${tier}`);
  return Number(n[1]);
}
