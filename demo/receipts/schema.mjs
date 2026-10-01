// schema.mjs - telos.receipt/v1 field contract: common field order, the tier
// fields from DESIGN section 1.5, and the fixed does_not_prove text per status.
// The verifier (verify.mjs) owns the enums and structural checks so it can run
// as one copied file; this module adds the writer-side vocabulary.
import { NON_EXECUTING, REQUIRED_FIELDS, STATUSES, TIERS } from "./verify.mjs";

export { REQUIRED_FIELDS, STATUSES, TIERS };

// Fixed per status. The writer always sets this; a caller cannot override it.
export const DOES_NOT_PROVE = Object.freeze({
  OK: "The action was dispatched and the named post-condition was checked. It does not show the task succeeded or that the target system recorded the effect.",
  REFUSED: "The action was refused before dispatch. It does not show the action would have caused harm, or that no other path reached the target.",
  HOLD: "A human decision was requested for this exact action digest. It does not show that a human saw or understood the request.",
  APPROVED: "A decision record approved this action digest for one redemption. It does not show the approver checked the target, or that the action ran.",
  REJECTED: "A decision record rejected this action digest. It does not show the action would have caused harm.",
  EXPIRED: "The grant or approval window closed before redemption. It does not show why no decision arrived.",
  DRIFT: "The recorded and observed state differ at the named fields. It does not show which side is correct or what caused the difference.",
  NEEDS_HUMAN: "The step needs a human action that Telos will not perform. It does not show the step is possible.",
  DRY_RUN: "The target was resolved and gated without acting. It does not show a real run would see the same state or succeed.",
  UNAVAILABLE: "The module or driver was absent or unreachable. It does not show the action is impossible with the module present.",
  ERROR: "The driver was called and raised an error after dispatch. It does not show the target is unchanged; it may be partly changed."
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
const HEAD = REQUIRED_FIELDS.filter((f) => !["monitor", "does_not_prove", "seal"].includes(f));

export function orderedReceipt(receipt) {
  const out = {};
  const tierFields = TIER_FIELDS[receipt.tier] ?? [];
  for (const f of [...HEAD, ...tierFields, ...SHARED_FIELDS, "monitor", "does_not_prove"]) {
    if (f in receipt) out[f] = receipt[f];
  }
  for (const f of Object.keys(receipt)) if (!(f in out) && f !== "seal") out[f] = receipt[f];
  out.seal = receipt.seal;
  return out;
}

// knownFields - every field name the v1 vocabulary defines for a tier.
export function knownFields(tier) {
  return new Set([...REQUIRED_FIELDS, ...(TIER_FIELDS[tier] ?? []), ...SHARED_FIELDS]);
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
  if (body.does_not_prove !== undefined && body.does_not_prove !== DOES_NOT_PROVE[body.status]) {
    throw new TypeError("does_not_prove is fixed per status and cannot be supplied");
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
