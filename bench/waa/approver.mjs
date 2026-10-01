// The scripted approver the benchmark plan names (DESIGN 7.3). It decides
// holds in place of a human: approve a hold whose verb is in the benchmark
// grant and whose target is inside the task's declared app scope, reject every
// other. It records every decision, so the run reports the confirmation load
// and any out-of-scope attempt.
//
// It exists only for benchmark runs inside a disposable VM. It never signs a
// real decision file on the operator's machine: the harness gives it holds as
// plain records and reads its verdicts.
import { windowAllowed, originAllowed } from "../../demo/broker/scope.mjs";

export function scriptedApprover({ grantSpec, task }) {
  const log = [];
  const decide = (hold) => {
    const inGrant = grantSpec.verbs.includes(hold.verb);
    const target = hold.target ?? {};
    const inScope = target.window ? windowAllowed(target.window, grantSpec.scope.windows ?? [])
      : target.origin ? originAllowed(target.origin, grantSpec.scope.origins ?? []) : false;
    const decision = inGrant && inScope ? "approve" : "reject";
    log.push({ task, verb: hold.verb, tier: hold.tier, decision, reason: !inGrant ? "verb not in grant" : !inScope ? "target out of task scope" : "in scope" });
    return decision;
  };
  return { decide, log };
}
