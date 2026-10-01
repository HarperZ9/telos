// dry-run.mjs - resolve and gate a list of steps without acting (DESIGN 4.3).
// Each step is resolved against the live tree through an injected `resolve`,
// gated through an injected `gate` (the broker's tier and scope check), given an
// action digest, and recorded as a DRY_RUN receipt with executed: false. The API
// takes no execute function, so a dry run has no path to an effect. The result
// lists the holds a real run would raise, so the human sees the confirmation load
// before granting anything.
//
// Contracts (the broker slice supplies real implementations):
//   resolve(step) -> { ok, target_ref, target_fingerprint, resolution, reason }
//   gate(step, resolved) -> { tier, allowed, needs_hold, grant_id, scope_sha256, reason }
import { actionDigest, argsSha256, fingerprintSha256 } from "./digest.mjs";

function plan(step, resolved, g) {
  const target_fingerprint = fingerprintSha256(resolved?.target_fingerprint);
  const args_sha256 = argsSha256(step.args);
  const fields = {
    tier: g.tier, verb: step.verb, target_ref: resolved?.target_ref ?? null, target_fingerprint,
    args_sha256, scope_sha256: g.scope_sha256 ?? null, grant_id: g.grant_id ?? null
  };
  return { ...fields, action_digest: actionDigest(fields) };
}

function reasonFor(resolved, g) {
  if (!resolved?.ok) return `would stop: target did not resolve (${resolved?.reason ?? "no reason given"})`;
  if (!g.allowed) return `would be refused: ${g.reason ?? "outside grant"}`;
  if (g.needs_hold) return "would raise a hold for a human decision";
  return "would run without a hold";
}

async function dryRunStep(step, index, { resolve, gate, chain, tool }) {
  const resolved = await resolve(step);
  const g = await gate(step, resolved);
  const p = plan(step, resolved, g);
  const would_hold = Boolean(resolved?.ok && g.allowed && g.needs_hold);
  const receipt = chain.append({
    tier: p.tier, verb: step.verb, tool, status: "DRY_RUN", executed: false,
    grant_id: p.grant_id, scope_sha256: p.scope_sha256, action_digest: p.action_digest,
    target_ref: p.target_ref, target_fingerprint: p.target_fingerprint,
    resolution: resolved?.ok ? (resolved.resolution ?? "ref") : undefined,
    args_sha256: p.args_sha256, would_hold, reason: reasonFor(resolved, g)
  });
  return { index, step: step.verb, tier: p.tier, action_digest: p.action_digest, resolved: Boolean(resolved?.ok),
    allowed: Boolean(g.allowed), would_hold, receipt_seal: receipt.seal, reason: receipt.reason };
}

// dryRun - returns { steps, holds, refusals, unresolved, executed: 0 }.
export async function dryRun(steps, { resolve, gate, chain, tool = "telos.dry_run" }) {
  if (typeof resolve !== "function" || typeof gate !== "function" || !chain) {
    throw new TypeError("dryRun needs resolve, gate and chain");
  }
  const out = [];
  for (let i = 0; i < steps.length; i += 1) out.push(await dryRunStep(steps[i], i, { resolve, gate, chain, tool }));
  return {
    steps: out,
    holds: out.filter((s) => s.would_hold),
    refusals: out.filter((s) => s.resolved && !s.allowed),
    unresolved: out.filter((s) => !s.resolved),
    executed: 0
  };
}
