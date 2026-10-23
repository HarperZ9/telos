// schema.mjs - telos.receipt/v2 field contract: common field order, the tier
// fields from DESIGN section 1.5, and the fixed scope text per status.
// The verifier (verify.mjs) owns the enums and structural checks so it can run
// as one copied file; this module adds the writer-side vocabulary.
import { NON_EXECUTING, REQUIRED_FIELDS, STATUSES, TIERS } from "./verify.mjs";

export { REQUIRED_FIELDS, STATUSES, TIERS };

// What a receipt of each status records. Fixed per status: the writer always
// sets it, and a caller cannot override it.
export const SCOPE = Object.freeze({
  OK: "Telos dispatched the action and checked the named post-condition.",
  REFUSED: "Telos refused the action before dispatch.",
  HOLD: "Telos asked a human to decide on this exact action digest.",
  APPROVED: "A decision record approved this action digest for one redemption.",
  REJECTED: "A decision record rejected this action digest.",
  EXPIRED: "The grant or approval window closed before redemption.",
  DRIFT: "The recorded state and the observed state differ at the named fields.",
  NEEDS_HUMAN: "The step needs an action that a human performs.",
  DRY_RUN: "Telos resolved and gated the target without acting.",
  UNAVAILABLE: "The module or driver was absent or unreachable.",
  ERROR: "Telos called the driver, and the driver raised an error after dispatch. The target can be partly changed."
});

const T3_FIELDS = ["hold_id", "decision_seal", "target_ref", "target_fingerprint", "resolution",
  "pre_state_digest", "post_condition", "post_condition_result", "focus_effect"];

// Tier-specific fields (DESIGN 1.5), snake_case. Each tier adds to the receipt
// common fields; T4 and T5 include every T3 field.
export const TIER_FIELDS = Object.freeze({
  T0: ["output_digest"],
  T1: ["sense", "scope_match", "observation_digest", "redactions"],
  T2: ["sandbox_root", "pre_image_digest", "post_image_digest", "rollback", "verify_result"],
  T3: T3_FIELDS,
  T4: [...T3_FIELDS, "argv_digest", "exit_code", "stdout_digest", "stderr_digest", "duration_ms"],
  T5: [...T3_FIELDS, "device_id", "restore_state_digest", "restore_verify_result", "presence_check"]
});

// Fields any tier may carry: dry run, replay and argument binding.
export const SHARED_FIELDS = ["args_sha256", "would_hold", "replay_of", "replay_diff", "side_files"];

const RESOLUTIONS = ["ref", "query", "coordinate"];
const VERIFY_RESULTS = ["MATCH", "DRIFT", "UNVERIFIABLE"];

// Writer order: common fields first, tier fields, then shared, monitor and seal.
const HEAD = REQUIRED_FIELDS.filter((f) => !["monitor", "scope", "seal"].includes(f));

export function orderedReceipt(receipt) {
  const out = {};
  const tierFields = TIER_FIELDS[receipt.tier] ?? [];
  for (const f of [...HEAD, ...tierFields, ...SHARED_FIELDS, "monitor", "scope"]) {
    if (f in receipt) out[f] = receipt[f];
  }
  for (const f of Object.keys(receipt)) if (!(f in out) && f !== "seal") out[f] = receipt[f];
  out.seal = receipt.seal;
  return out;
}

// knownFields - every field name the vocabulary defines for a tier. A version 1
// receipt names the scope field does_not_prove.
export function knownFields(tier) {
  return new Set([...REQUIRED_FIELDS, "does_not_prove", ...(TIER_FIELDS[tier] ?? []), ...SHARED_FIELDS]);
}

// checkBody - writer-side checks on a caller body before sealing. Unknown fields
// are allowed (they are sealed and reported) so parallel modules can extend v1
// without breaking the chain; enum-typed fields are checked here.
export function checkBody(body) {
  if (!TIERS.includes(body.tier)) throw new TypeError(`receipt tier must be one of ${TIERS.join(", ")}`);
  if (!STATUSES.includes(body.status)) throw new TypeError(`receipt status must be one of ${STATUSES.join(", ")}`);
  if (typeof body.verb !== "string" || !body.verb) throw new TypeError("receipt verb is required");
  if (body.executed === true && NON_EXECUTING.has(body.status)) {
    throw new TypeError(`status ${body.status} cannot carry executed: true`);
  }
  if (body.scope !== undefined && body.scope !== SCOPE[body.status]) {
    throw new TypeError("scope is fixed per status and cannot be supplied");
  }
  if (body.does_not_prove !== undefined) {
    throw new TypeError("does_not_prove is the version 1 name; the writer sets scope");
  }
  if (body.resolution !== undefined && !RESOLUTIONS.includes(body.resolution)) {
    throw new TypeError(`resolution must be one of ${RESOLUTIONS.join(", ")}`);
  }
  if (body.verify_result !== undefined && !VERIFY_RESULTS.includes(body.verify_result)) {
    throw new TypeError(`verify_result must be one of ${VERIFY_RESULTS.join(", ")}`);
  }
  for (const f of ["seal", "seq", "prev_seal", "session_id", "schema", "hash_version"]) {
    if (body[f] !== undefined) throw new TypeError(`${f} is set by the chain, not the caller`);
  }
}

export function unknownFields(receipt) {
  const known = knownFields(receipt.tier);
  return Object.keys(receipt).filter((f) => !known.has(f));
}
