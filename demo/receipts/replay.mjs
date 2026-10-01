// replay.mjs - re-execute a recorded session step by step (DESIGN 4.4).
// The recording must verify first (pinned key when given). Then for each
// recorded step that executed with status OK:
//   1. re-gate against current grants (gate); a refusal stops replay;
//   2. re-resolve the target by fingerprint (resolve); a missing or different
//      element stops replay with DRIFT and a field-level diff;
//   3. compare the pre-state digest when the recording has one (preState);
//   4. for T3 and above, raise a fresh hold (requestHold). Recorded hold ids and
//      decision seals are never passed on: approvals are not inherited;
//   5. execute, re-check the post-condition (checkPost), and cite the original
//      seal in `replay_of`. A failed post-condition stops replay with DRIFT.
// A silent wrong replay is the failure this module exists to prevent: every exit
// path names the step and the reason.
//
// Contracts (the broker slice supplies real implementations):
//   loadArgs(original) -> raw args object (from the recording's args side file)
//   gate(step) -> { tier, allowed, needs_hold, grant_id, scope_sha256, reason }
//   resolve(step) -> { ok, target_ref, target_fingerprint, reason }
//   preState(step, resolved) -> digest string or null
//   requestHold({ action_digest, step, tier }) -> { status: APPROVED|REJECTED|EXPIRED|PENDING, hold_id, decision_seal }
//   execute(step, args, resolved) -> { ok, reason, fields }   (fields: tier receipt fields)
//   checkPost(original.post_condition, step, result) -> boolean
import { actionDigest, argsSha256, fingerprintSha256, tierRank } from "./digest.mjs";
import { RECEIPT_SCHEMA, parseJsonl, verifyChain } from "./verify.mjs";

const REPLAY_TOOL = "telos.replay";

function recordedSteps(text, startAt) {
  return parseJsonl(text).records.map((r) => r.rec)
    .filter((r) => r.schema === RECEIPT_SCHEMA && r.executed === true && r.status === "OK" && r.seq >= startAt);
}

function diffFields(original, observed) {
  return ["target_ref", "target_fingerprint", "pre_state_digest"]
    .filter((f) => observed[f] !== undefined && original[f] !== undefined && original[f] !== null && observed[f] !== original[f])
    .map((f) => ({ field: f, recorded: original[f], observed: observed[f] }));
}

function base(original, extra) {
  return { tier: original.tier, verb: original.verb, tool: REPLAY_TOOL, replay_of: original.seal, ...extra };
}

async function resolveAndCompare(original, step, hooks) {
  const resolved = await hooks.resolve(step);
  if (!resolved?.ok) {
    return { stop: base(original, { status: "DRIFT", reason: `target missing: ${resolved?.reason ?? "did not resolve"}`,
      replay_diff: [{ field: "target_ref", recorded: original.target_ref ?? null, observed: null }] }) };
  }
  const observed = { target_ref: resolved.target_ref, target_fingerprint: fingerprintSha256(resolved.target_fingerprint) };
  if (original.pre_state_digest && hooks.preState) observed.pre_state_digest = await hooks.preState(step, resolved);
  const replay_diff = diffFields(original, observed);
  if (replay_diff.length) {
    return { stop: base(original, { status: "DRIFT", reason: `recorded and live state differ at ${replay_diff.map((d) => d.field).join(", ")}`, replay_diff }) };
  }
  return { resolved, observed };
}

async function holdIfNeeded(original, g, digest, hooks, chain) {
  if (tierRank(g.tier) < 3 && !g.needs_hold) return null;
  const hold = base(original, { tier: g.tier, status: "HOLD", action_digest: digest, grant_id: g.grant_id ?? null,
    scope_sha256: g.scope_sha256 ?? null, reason: "replay raises a fresh hold; the recorded approval is not inherited" });
  const held = chain.append(hold);
  const decision = await hooks.requestHold({ action_digest: digest, step: original.verb, tier: g.tier, hold_seal: held.seal });
  if (decision?.status === "APPROVED") {
    chain.append({ ...hold, status: "APPROVED", hold_id: decision.hold_id ?? null, decision_seal: decision.decision_seal ?? null, reason: "fresh approval for the replayed step" });
    return null;
  }
  if (!["REJECTED", "EXPIRED"].includes(decision?.status)) return { appended: held };
  return { stop: { ...hold, status: decision.status, hold_id: decision.hold_id ?? null, decision_seal: decision.decision_seal ?? null,
    reason: `replay stopped: hold ${decision.status.toLowerCase()}` } };
}

async function replayStep(original, hooks, chain) {
  const args = await hooks.loadArgs(original);
  const step = { verb: original.verb, target_ref: original.target_ref ?? null, target_fingerprint: original.target_fingerprint ?? null, args };
  if (original.args_sha256 && argsSha256(args) !== original.args_sha256) {
    return base(original, { status: "DRIFT", reason: "recorded arguments do not match args_sha256",
      replay_diff: [{ field: "args_sha256", recorded: original.args_sha256, observed: argsSha256(args) }] });
  }
  const g = await hooks.gate(step);
  if (!g?.allowed) return base(original, { tier: g?.tier ?? original.tier, status: "REFUSED", reason: `current grants refuse: ${g?.reason ?? "no grant"}` });
  const rc = await resolveAndCompare(original, step, hooks);
  if (rc.stop) return rc.stop;
  const digest = actionDigest({ tier: g.tier, verb: step.verb, target_ref: rc.observed.target_ref,
    target_fingerprint: rc.observed.target_fingerprint, args_sha256: argsSha256(args), scope_sha256: g.scope_sha256, grant_id: g.grant_id });
  const held = await holdIfNeeded(original, g, digest, hooks, chain);
  if (held) return held.appended ? { appended: held.appended } : held.stop;
  const result = await hooks.execute(step, args, rc.resolved);
  const post = result?.ok ? await hooks.checkPost(original.post_condition ?? null, step, result) : false;
  return base(original, { tier: g.tier, status: post ? "OK" : "DRIFT", executed: Boolean(result?.ok),
    action_digest: digest, grant_id: g.grant_id ?? null, scope_sha256: g.scope_sha256 ?? null,
    target_ref: rc.observed.target_ref, target_fingerprint: rc.observed.target_fingerprint,
    post_condition: original.post_condition ?? null, post_condition_result: post,
    reason: post ? "replayed and post-condition re-checked" : `post-condition failed: ${result?.reason ?? "check returned false"}`,
    ...(result?.fields ?? {}) });
}

// replay - returns { status: COMPLETE|DRIFT|REFUSED|HOLD|REJECTED|EXPIRED,
// replayed, stopped_at, receipts }. options: trustedKey, startAt (seq).
export async function replay(recordedText, hooks, { chain, trustedKey, startAt = 1 } = {}) {
  for (const h of ["loadArgs", "gate", "resolve", "requestHold", "execute", "checkPost"]) {
    if (typeof hooks?.[h] !== "function") throw new TypeError(`replay needs hook ${h}`);
  }
  const v = verifyChain(recordedText, { trustedKey });
  if (v.verdict !== "MATCH") {
    const r = chain.append({ tier: "T0", verb: "telos.replay", tool: REPLAY_TOOL, status: "REFUSED", reason: `recording does not verify: ${v.verdict} ${v.reason}` });
    return { status: "REFUSED", replayed: 0, stopped_at: null, reason: r.reason, receipts: [r.seal] };
  }
  const receipts = [];
  let replayed = 0;
  for (const original of recordedSteps(recordedText, startAt)) {
    const body = await replayStep(original, hooks, chain);
    // A pending hold is already on the chain; resume later with startAt.
    const r = body.appended ?? chain.append(body);
    receipts.push(r.seal);
    if (r.status !== "OK") return { status: r.status, replayed, stopped_at: original.seq, reason: r.reason, replay_diff: r.replay_diff ?? [], receipts };
    replayed += 1;
  }
  return { status: "COMPLETE", replayed, stopped_at: null, receipts };
}
