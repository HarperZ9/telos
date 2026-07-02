import {
  stableStringify,
  sha256Prefixed,
  digestBytes,
  hashScope,
  canonicalBytes,
  packetHash
} from "./proof-hash.mjs";

// Re-export the hashing and canonical primitives so callers can import them
// from proof-core as a single surface.
export { stableStringify, sha256Prefixed, digestBytes, hashScope, canonicalBytes, packetHash };

const EXTERNAL_CLASSES = new Set(["write", "external_call", "mixed"]);
const SIDE_EFFECT_CLASSES = new Set(["none", "read", "write", "external_call", "human_action", "mixed"]);
const RESULT_STATES = new Set([
  "proposed",
  "admitted",
  "running",
  "completed",
  "failed",
  "cancelled",
  "compensated"
]);
const ADMISSION_DECISIONS = new Set(["allow", "block", "escalate", "require_review"]);

// Required JSON paths. Each entry is checked against the packet; a missing one
// is reported by its own path and lowers the verdict to UNVERIFIABLE.
const REQUIRED_PATHS = [
  "schema",
  "packet_id",
  "objective.claim",
  "objective.scope",
  "objective.success_criterion",
  "source_refs",
  "context_refs",
  "route.lane",
  "route.decided_by",
  "route.confidence",
  "route.route_ref",
  "admission.action_id",
  "admission.decision",
  "admission.policy_ref",
  "admission.authority_ref",
  "admission.admitted_ordinal",
  "action.action_id",
  "action.event_id",
  "action.tool_id",
  "action.action_kind",
  "action.args_hash",
  "action.executed_ordinal",
  "action.idempotency_key",
  "side_effect.class",
  "side_effect.reversible",
  "compensation.required",
  "outputs",
  "artifacts",
  "final_status.state",
  "final_status.stop_reason",
  "packet_hash"
];

function getPath(obj, path) {
  return path.split(".").reduce((node, key) => (node == null ? undefined : node[key]), obj);
}

// Assemble a canonical packet from fixture materials. Deterministic: no clock,
// no randomness inside the hash scope.
export function assemblePacket(fixture) {
  const base = {
    schema: "project-telos.proof-packet/v1",
    packet_id: fixture.packet_id,
    objective: fixture.objective,
    source_refs: fixture.source_refs,
    context_refs: fixture.context_refs,
    route: fixture.route,
    admission: fixture.admission,
    action: fixture.action,
    side_effect: fixture.side_effect,
    compensation: fixture.compensation,
    outputs: fixture.outputs,
    artifacts: fixture.artifacts,
    final_status: fixture.final_status
  };
  if (fixture.ledger_ref) {
    base.ledger_ref = fixture.ledger_ref;
  }
  const packet = { ...base, packet_hash: packetHash(base) };
  packet.wall_clock = fixture.wall_clock ?? { assembled_at: "unpinned" };
  return packet;
}

function addFailure(failures, code, verdict, detail) {
  failures.push({ code, verdict, ...detail });
}

// Pure verifier: packet in, named check results plus a derived verdict out.
// There is no path that returns a literal MATCH without a passing check set.
export function verifyPacket(packet, options = {}) {
  const checks = [];
  const failures = [];

  // check.required_fields -> UNVERIFIABLE, naming each missing path.
  const missing = [];
  for (const path of REQUIRED_PATHS) {
    const value = getPath(packet, path);
    if (value === undefined || value === null) {
      missing.push(path);
    }
  }
  if (missing.length) {
    for (const path of missing) {
      addFailure(failures, "missing_required_field", "UNVERIFIABLE", { path });
    }
  }
  let structurallyComplete = missing.length === 0;
  checks.push({ name: "check.required_fields", passed: missing.length === 0, missing });

  // Source-ref content_hash is evidence an output may claim. A missing hash is a
  // missing required field (UNVERIFIABLE evidence gap), not tamper, so it also
  // marks the packet structurally incomplete and suppresses the derivative hash
  // mismatch that deleting the field would otherwise cause.
  const sourceIds = new Set();
  const sourceRefs = Array.isArray(packet.source_refs) ? packet.source_refs : [];
  let sourceRefsOk = true;
  sourceRefs.forEach((ref, index) => {
    if (!ref || !ref.id || !ref.content_hash) {
      sourceRefsOk = false;
      structurallyComplete = false;
      addFailure(failures, "missing_required_field", "UNVERIFIABLE", {
        path: `source_refs[${index}].content_hash`
      });
    } else {
      sourceIds.add(ref.id);
    }
  });
  checks.push({ name: "check.source_refs", passed: sourceRefsOk });

  // Context-ref element fields (envelope_id, envelope_hash) are required by the
  // conventions and are surfaced into the export as trace_refs. A missing one is
  // an UNVERIFIABLE evidence gap, not tamper, matching the source-ref treatment.
  const contextRefs = Array.isArray(packet.context_refs) ? packet.context_refs : [];
  let contextRefsOk = true;
  contextRefs.forEach((ref, index) => {
    for (const field of ["envelope_id", "envelope_hash"]) {
      if (!ref || ref[field] === undefined || ref[field] === null) {
        contextRefsOk = false;
        structurallyComplete = false;
        addFailure(failures, "missing_required_field", "UNVERIFIABLE", {
          path: `context_refs[${index}].${field}`
        });
      }
    }
  });
  checks.push({ name: "check.context_refs", passed: contextRefsOk });

  // Output element fields (name, digest, ref) are required. A missing name or
  // digest defeats the digest recomputation; a missing ref breaks the join. Each
  // is an UNVERIFIABLE evidence gap named by its JSON path.
  const outputRefs = Array.isArray(packet.outputs) ? packet.outputs : [];
  let outputFieldsOk = true;
  outputRefs.forEach((output, index) => {
    for (const field of ["name", "digest", "ref"]) {
      if (!output || output[field] === undefined || output[field] === null) {
        outputFieldsOk = false;
        structurallyComplete = false;
        addFailure(failures, "missing_required_field", "UNVERIFIABLE", {
          path: `outputs[${index}].${field}`
        });
      }
    }
  });
  checks.push({ name: "check.output_fields", passed: outputFieldsOk });

  // check.state_model -> DRIFT with observed value and allowed set.
  const stateDeltas = [];
  const sec = packet.side_effect?.class;
  if (sec !== undefined && !SIDE_EFFECT_CLASSES.has(sec)) {
    stateDeltas.push({ path: "side_effect.class", observed: sec, allowed: [...SIDE_EFFECT_CLASSES] });
  }
  const state = packet.final_status?.state;
  if (state !== undefined && !RESULT_STATES.has(state)) {
    stateDeltas.push({ path: "final_status.state", observed: state, allowed: [...RESULT_STATES] });
  }
  const decision = packet.admission?.decision;
  if (decision !== undefined && !ADMISSION_DECISIONS.has(decision)) {
    stateDeltas.push({ path: "admission.decision", observed: decision, allowed: [...ADMISSION_DECISIONS] });
  }
  for (const delta of stateDeltas) {
    addFailure(failures, "state_model_violation", "DRIFT", delta);
  }
  checks.push({ name: "check.state_model", passed: stateDeltas.length === 0 });

  // check.packet_hash -> DRIFT with expected and observed. Only runs when the
  // packet is structurally complete; a missing required field is UNVERIFIABLE
  // and must not be masked by a derivative hash mismatch.
  const observedHash = packet.packet_hash;
  const expectedHash = packetHash(packet);
  const hashOk = observedHash === expectedHash;
  if (structurallyComplete && !hashOk) {
    addFailure(failures, "packet_hash_mismatch", "DRIFT", { expected: expectedHash, observed: observedHash });
  }
  checks.push({ name: "check.packet_hash", passed: hashOk, skipped: !structurallyComplete });

  // check.artifact_digests -> DRIFT recomputing each output digest over its
  // embedded artifact bytes. An output that claims a digest but carries no
  // embedded body cannot be recomputed: the digest is a load-bearing claim, so
  // a missing body is an UNVERIFIABLE evidence gap (naming artifacts.<name>),
  // never a silent pass. Trusting the claimed digest on faith would let a
  // tampered or phantom output reach MATCH with zero failures.
  const digestDeltas = [];
  const digestGaps = [];
  const outputs = Array.isArray(packet.outputs) ? packet.outputs : [];
  const artifacts = packet.artifacts ?? {};
  outputs.forEach((output, index) => {
    const name = output?.name;
    const body = artifacts[name];
    if (body === undefined) {
      digestGaps.push({ index, name });
      return;
    }
    const recomputed = digestBytes(body);
    if (output.digest !== recomputed) {
      digestDeltas.push({
        path: `outputs[${index}].digest`,
        name,
        expected: output.digest,
        recomputed
      });
    }
  });
  for (const delta of digestDeltas) {
    addFailure(failures, "artifact_digest_mismatch", "DRIFT", delta);
  }
  for (const gap of digestGaps) {
    structurallyComplete = false;
    addFailure(failures, "missing_required_field", "UNVERIFIABLE", {
      path: gap.name === undefined ? `artifacts` : `artifacts.${gap.name}`,
      output_index: gap.index,
      reason: "output digest cannot be recomputed without its embedded artifact body"
    });
  }
  checks.push({
    name: "check.artifact_digests",
    passed: digestDeltas.length === 0 && digestGaps.length === 0
  });

  // check.admission_join -> DRIFT when an action has no matching admission
  // record. Only meaningful when both blocks are present; a missing admission
  // block is UNVERIFIABLE via check.required_fields, not DRIFT here.
  let admissionJoinOk = true;
  if (packet.action?.action_id && packet.admission) {
    if (packet.admission?.action_id !== packet.action.action_id) {
      admissionJoinOk = false;
      addFailure(failures, "admission_missing_for_action", "DRIFT", {
        action_id: packet.action.action_id,
        admission_action_id: packet.admission?.action_id ?? null
      });
    }
  }
  checks.push({ name: "check.admission_join", passed: admissionJoinOk });

  // check.admission_ordering -> DRIFT when execution precedes admission.
  let orderingOk = true;
  const admitted = packet.admission?.admitted_ordinal;
  const executed = packet.action?.executed_ordinal;
  if (typeof admitted === "number" && typeof executed === "number") {
    if (executed <= admitted) {
      orderingOk = false;
      addFailure(failures, "admission_order_violation", "DRIFT", {
        admitted_ordinal: admitted,
        executed_ordinal: executed
      });
    }
  }
  checks.push({ name: "check.admission_ordering", passed: orderingOk });

  // check.compensation_path -> DRIFT when an external write has no compensation ref.
  let compensationOk = true;
  if (EXTERNAL_CLASSES.has(sec)) {
    const required = packet.compensation?.required === true;
    const ref = packet.compensation?.ref;
    if (!required || !ref) {
      compensationOk = false;
      addFailure(failures, "compensation_path_missing_for_external_write", "DRIFT", {
        side_effect_class: sec,
        missing_path: "compensation.ref"
      });
    }
  }
  checks.push({ name: "check.compensation_path", passed: compensationOk });

  // check.evidence_refs -> UNVERIFIABLE when an output claims an unresolvable source ref.
  let evidenceOk = true;
  outputs.forEach((output, index) => {
    const claim = output?.source_ref_id;
    if (claim && !sourceIds.has(claim)) {
      evidenceOk = false;
      addFailure(failures, "evidence_ref_unresolvable", "UNVERIFIABLE", {
        path: `outputs[${index}].source_ref_id`,
        ref: claim
      });
    }
  });
  checks.push({ name: "check.evidence_refs", passed: evidenceOk });

  // Derive the verdict by one fold. DRIFT dominates UNVERIFIABLE dominates MATCH.
  const hasDrift = failures.some((f) => f.verdict === "DRIFT");
  const hasUnverifiable = failures.some((f) => f.verdict === "UNVERIFIABLE");
  const derivedVerdict = hasDrift ? "DRIFT" : hasUnverifiable ? "UNVERIFIABLE" : "MATCH";

  // check.verdict_derivation: the verdict is derived from the checks alone, so a
  // canned MATCH embedded in the packet can never win. When an embedded verdict
  // disagrees with the derived one, that disagreement is recorded as a failure.
  // The recorded failure inherits the derived severity, so it flags the lie
  // without ever claiming a better verdict than the materials support: an
  // embedded MATCH over tampered materials stays DRIFT, an embedded MATCH over
  // an incomplete packet stays UNVERIFIABLE, and a clean packet with a truthful
  // embedded MATCH passes.
  let derivationOk = true;
  const embedded = options.embeddedVerdict;
  if (embedded !== undefined && embedded !== derivedVerdict) {
    derivationOk = false;
    failures.push({
      code: "embedded_verdict_not_derived",
      verdict: derivedVerdict === "MATCH" ? "DRIFT" : derivedVerdict,
      embedded,
      derived: derivedVerdict
    });
  }
  checks.push({ name: "check.verdict_derivation", passed: derivationOk });

  // The final verdict is the verdict derived from the checks. If a clean packet
  // (derived MATCH) carried a dishonest embedded verdict, that itself is DRIFT.
  const finalVerdict =
    !derivationOk && derivedVerdict === "MATCH" ? "DRIFT" : derivedVerdict;

  return {
    checks,
    failures,
    verdict: finalVerdict
  };
}
