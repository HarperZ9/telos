// Tier gate policy: checks that refuse before any grant is consulted, then the
// choice of a live grant whose tier and scope cover the resolved target.
import { deviceAllowed, execAllowed, originAllowed, pathInside, protectedPath, protectedWindow, senseAllowed, windowAllowed } from "./scope.mjs";
import { effectiveTier, tierRank } from "./tiers.mjs";

// Flags a caller might use to claim approval or irreversibility. Approval
// lives in a signed human decision and irreversibility in the grant, never in
// an argument (DESIGN.md 1.1, closes MAP.md F4 for the hosted path).
export const CALLER_APPROVAL_FLAGS = Object.freeze([
  "approve", "approved", "confirm", "confirmed", "yes", "force", "irreversible",
  "allow-irreversible", "allow_irreversible", "grant", "tier", "decision",
]);

export function precheck(spec, target, flags, { stateRoot, platform, protectedProcesses = [] }) {
  const flagHit = Object.keys(flags).find((k) => CALLER_APPROVAL_FLAGS.includes(k.toLowerCase()));
  if (flagHit) return { reason: "CALLER_APPROVAL_FLAG", detail: flagHit };
  if (spec.reserved) return { reason: spec.presence ? "PRESENCE_UNAVAILABLE" : "RESERVED_VERB" };
  if (target.secret) return { reason: "SECRET_FIELD" };
  const why = protectedWindow(target.window, protectedProcesses);
  if (why) return { reason: "PROTECTED_TARGET", detail: why };
  for (const p of [target.path, target.readPath, target.writePath]) {
    if (p && protectedPath(p, stateRoot, platform)) return { reason: "PROTECTED_TARGET", detail: "telos state directory" };
  }
  if (target.shellMeta) return { reason: "SHELL_METACHAR" };
  if (target.crossOrigin) return { reason: "OUT_OF_SCOPE", detail: "apifetch is same-origin only" };
  return null;
}

function kindInScope(spec, target, scope, platform) {
  switch (spec.target) {
    case "origin":
    case "navigate":
      return originAllowed(target.origin, scope.origins);
    case "window":
      return windowAllowed(target.window, scope.windows);
    case "path-read":
      return pathInside(target.path, scope.paths, platform);
    case "path-write":
      return pathInside(target.path, scope.sandbox_roots, platform) || pathInside(target.path, scope.paths, platform);
    case "argv":
      return execAllowed(target.argv, scope.exec_allow);
    case "foreground":
    case "device":
      return deviceAllowed(target.device, scope.devices);
    default:
      return true;
  }
}

export function inScope(spec, target, scope, platform) {
  if (!kindInScope(spec, target, scope, platform)) return false;
  if (spec.sense && !senseAllowed(spec.sense, scope.senses)) return false;
  if (target.readPath && !pathInside(target.readPath, scope.paths, platform)) return false;
  if (target.writePath && !pathInside(target.writePath, [...scope.sandbox_roots, ...scope.paths], platform)) return false;
  return true;
}

function tierUnder(verb, spec, target, scope, platform, preimage) {
  const written = spec.target === "path-write" ? target.path : target.writePath;
  const inSandbox = Boolean(written) && pathInside(written, scope.sandbox_roots, platform);
  return effectiveTier(verb, {
    resolution: target.resolution,
    writesInSandbox: inSandbox,
    writesOutsideSandbox: Boolean(written) && !inSandbox,
    preimageFailed: inSandbox && preimage !== null && !preimage.ok,
  });
}

// Returns { grant, tier } for the least-privileged covering grant, or the most
// specific refusal: NO_GRANT, then TIER_ABOVE_GRANT, then OUT_OF_SCOPE.
export function selectGrant(verb, spec, target, grants, { platform, preimage = null }) {
  let reason = "NO_GRANT";
  let best = null;
  for (const grant of grants) {
    const listed = grant.verbs.includes(verb) || (grant.verbs.includes("*") && spec.tier === "T1");
    if (!listed) continue;
    const tier = tierUnder(verb, spec, target, grant.scope, platform, preimage);
    if (tierRank(tier) > tierRank(grant.tier)) {
      if (reason === "NO_GRANT") reason = "TIER_ABOVE_GRANT";
      continue;
    }
    if (!inScope(spec, target, grant.scope, platform)) {
      reason = "OUT_OF_SCOPE";
      continue;
    }
    if (!best || tierRank(tier) < tierRank(best.tier)) best = { grant, tier };
  }
  return best ?? { reason };
}
