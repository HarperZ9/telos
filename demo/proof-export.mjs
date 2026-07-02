import { verifyPacket } from "./proof-core.mjs";

// Strip the sha256: prefix; proof-surface requires bare 64-hex.
function bare(digest) {
  return typeof digest === "string" ? digest.replace(/^sha256:/, "") : digest;
}

// action-receipt policy_decisions -> proof-surface ADMISSION_DECISIONS.
const DECISION_MAP = {
  allow: "allow",
  block: "deny",
  escalate: "needs-human",
  require_review: "needs-human"
};

// action-receipt side_effect_classes -> proof-surface SIDE_EFFECT_CLASSES.
const CLASS_MAP = {
  read: "read",
  none: "read",
  write: "write",
  external_call: "external",
  human_action: "external",
  mixed: "external"
};

// proof-surface overall verdict -> decision_summary, mirroring
// proof-surface _decision.derive_decision_summary exactly.
const DECISION_SUMMARY = {
  MATCH: {
    decision: "approve",
    confidence: "high",
    reason: "the evidence matched every checked claim within tolerance",
    next_action: "proceed"
  },
  DRIFT: {
    decision: "block",
    confidence: "high",
    reason: "at least one checked claim drifted outside its tolerance",
    next_action: "investigate and remediate the drifted evidence before proceeding"
  },
  UNVERIFIABLE: {
    decision: "escalate",
    confidence: "low",
    reason: "at least one claim could not be verified from the available evidence",
    next_action: "supply the missing evidence, then re-verify"
  }
};

function deriveDecisionSummary(overall, missingEvidence) {
  const base = DECISION_SUMMARY[overall] ?? DECISION_SUMMARY.UNVERIFIABLE;
  return {
    decision: base.decision,
    reason: base.reason,
    confidence: base.confidence,
    missing_evidence: [...(missingEvidence ?? [])],
    next_action: base.next_action
  };
}

// Map a side effect and its compensation into the proof-surface side_effects
// entry. An external or write class that is not reversible becomes irreversible.
function mapSideEffect(packet, verdict) {
  const cls = packet.side_effect?.class;
  const reversible = packet.side_effect?.reversible === true;
  let mapped = CLASS_MAP[cls] ?? "read";
  if ((mapped === "external" || mapped === "write") && !reversible) {
    mapped = "irreversible";
  }
  return {
    action_id: packet.action?.action_id,
    class: mapped,
    idempotency_key: bare(packet.action?.args_hash),
    compensation: {
      reversible,
      rollback_ref: packet.compensation?.ref ?? null
    },
    before_digest: null,
    after_digest: null
  };
}

// Assemble the disclosed-limits uncertainty list. Lossy class mappings and
// witness coverage are named here so nothing is silently dropped.
function buildUncertainty(packet) {
  const notes = [];
  const cls = packet.side_effect?.class;
  const lossy = new Set(["none", "human_action", "mixed"]);
  if (lossy.has(cls)) {
    notes.push(`side-effect class ${cls} was mapped lossily to the proof-surface taxonomy`);
  }
  if (packet.witness_coverage === "not_witnessed" || packet.witness?.status === "unavailable") {
    notes.push("witness coverage is not_witnessed: no emet implementation was reachable at verify time");
  }
  notes.push("refs are declared and digest-bound but not dereferenced during export");
  return notes;
}

// Export a Telos proof packet to the proof-surface agent-action-proof-packet/v0
// shape. The corrected mapping: context is a plain object, decision_summary is
// derived from the overall verdict. proof-surface is never imported at runtime.
export function toProofSurfacePacket(packet) {
  const verdict = packet.verifier?.verdict ?? verifyPacket(packet).verdict;
  const actionId = packet.action?.action_id;

  const sources = (packet.source_refs ?? []).map((ref) => ({
    ref: ref.ref,
    sha256: bare(ref.content_hash)
  }));

  const context = {
    workspace: packet.objective?.scope ?? "unspecified workspace",
    tool_authority: packet.admission?.policy_ref ?? "unspecified policy",
    context_refs: (packet.context_refs ?? []).map((c) => c.envelope_id)
  };

  const actions = [
    {
      action_id: actionId,
      actor: packet.route?.decided_by ?? null,
      agent: packet.action?.tool_id ?? null,
      model: null,
      tool: packet.action?.tool_id,
      action_kind: packet.action?.action_kind,
      target: packet.outputs?.[0]?.ref ?? packet.action?.event_id ?? "unspecified target",
      cost: { tokens: null, wall_ms: null },
      span_digest: bare(packet.action?.args_hash)
    }
  ];

  const admission = [
    {
      action_id: actionId,
      decision: DECISION_MAP[packet.admission?.decision] ?? "needs-human",
      reasons: [packet.admission?.policy_ref ?? "policy reference not recorded"],
      authorization_ref: packet.admission?.authority_ref
    }
  ];

  const sideEffects = [mapSideEffect(packet, verdict)];

  const outputs = (packet.outputs ?? []).map((output) => ({
    name: output.name,
    sha256: bare(output.digest)
  }));

  // evidence_refs is an object of typed buckets, each {ref, sha256?}.
  const traceRefs = [];
  for (const c of packet.context_refs ?? []) {
    traceRefs.push({ ref: c.envelope_id, sha256: bare(c.envelope_hash) });
  }
  if (packet.route?.route_ref) {
    traceRefs.push({ ref: packet.route.route_ref });
  }
  const runtimeRefs = [];
  if (packet.ledger_ref?.entry_id) {
    runtimeRefs.push({ ref: packet.ledger_ref.entry_id, sha256: bare(packet.ledger_ref.ledger_hash) });
  }
  const evidence_refs = { trace_refs: traceRefs, runtime_refs: runtimeRefs };

  const verdicts = {
    overall: verdict,
    per_action: [{ action_id: actionId, status: verdict }]
  };

  return {
    version: "agent-action-proof-packet/v0",
    packet_id: packet.packet_id,
    claim: packet.objective?.claim,
    scope: packet.objective?.scope,
    sources,
    context,
    actions,
    admission,
    side_effects: sideEffects,
    outputs,
    evidence_refs,
    failure_labels: [],
    verdicts,
    uncertainty: buildUncertainty(packet),
    decision_summary: deriveDecisionSummary(verdict, [])
  };
}
