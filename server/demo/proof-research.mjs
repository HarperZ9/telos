import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import {
  stableStringify,
  sha256Prefixed,
  digestBytes,
  hashScope,
  canonicalBytes,
  packetHash
} from "./proof-hash.mjs";

// Re-export the hashing and canonical primitives so callers can import them
// from proof-research as a single surface, mirroring proof-core.
export { stableStringify, sha256Prefixed, digestBytes, hashScope, canonicalBytes, packetHash };

const here = path.dirname(fileURLToPath(import.meta.url));

// Closed vocabularies, copied from the conventions state_model. A value outside
// its set is a state_model_violation (DRIFT), not a silent pass.
const ATTEMPT_RESULTS = new Set(["proved", "refuted", "incomplete", "bounded", "failed"]);
const CHECK_STATUSES = new Set(["pass", "fail", "unverifiable"]);
const CONTROL_OUTCOMES = new Set(["survived", "not_survived"]);
// Single-packet promotion rungs. PROMOTED_DISCOVERY and LAW_CANDIDATE need
// independent reproduction and review, so a single packet may never assert them.
const ASSERTABLE_PROMOTIONS = new Set([
  "SOURCE_LEAD",
  "HYPOTHESIS",
  "IDENTITY",
  "PROBE_MATCH",
  "CRUCIBLE_MATCH",
  "UNVERIFIABLE",
  "REFUTED"
]);
const RESERVED_PROMOTIONS = new Set(["PROMOTED_DISCOVERY", "LAW_CANDIDATE"]);

// Each check status folds to a per-check verdict, and the overall verdict is the
// fold of those. DRIFT dominates UNVERIFIABLE dominates MATCH.
const STATUS_TO_VERDICT = { pass: "MATCH", fail: "DRIFT", unverifiable: "UNVERIFIABLE" };

// Required JSON paths. A missing one is reported by its own path and lowers the
// verdict to UNVERIFIABLE (an evidence gap), never a silent pass.
const REQUIRED_PATHS = [
  "schema",
  "packet_id",
  "objective.claim",
  "objective.scope",
  "objective.statement",
  "objective.bounded",
  "negative_fixture.id",
  "negative_fixture.description",
  "negative_fixture.body",
  "negative_fixture.content_hash",
  "negative_fixture.control_outcome",
  "verdicts.overall",
  "promotion",
  "uncertainty",
  "packet_hash"
];

function getPath(obj, pathExpr) {
  return pathExpr.split(".").reduce((node, key) => (node == null ? undefined : node[key]), obj);
}

function loadConventions() {
  return JSON.parse(
    readFileSync(path.join(here, "integrations", "research-proof-packet-conventions.json"), "utf8")
  );
}

// Fold per-check statuses into an overall verdict. DRIFT dominates UNVERIFIABLE
// dominates MATCH. An empty check set is UNVERIFIABLE: nothing was checked.
function foldVerdict(statuses) {
  if (!statuses.length) return "UNVERIFIABLE";
  if (statuses.some((s) => s === "fail")) return "DRIFT";
  if (statuses.some((s) => s === "unverifiable")) return "UNVERIFIABLE";
  return "MATCH";
}

// Resolve a fixture into an assembled packet. Deterministic: source and
// negative-fixture content_hash placeholders ("recompute") are filled from the
// embedded bodies, and verdicts.overall ("recompute") is folded from the check
// statuses, so the fixture never carries a stale hardcoded digest. No clock and
// no randomness enter the hash scope.
export function assembleResearchPacket(input) {
  const fixture = input && input.demo ? loadConventions().conformance_fixture.happy_path : input;
  if (!fixture) {
    throw new Error("assembleResearchPacket requires a fixture object or { demo: true }");
  }

  const sourceRefs = (fixture.source_refs ?? []).map((ref) => {
    const resolved = { ...ref };
    if (resolved.content_hash === "recompute" && resolved.body !== undefined) {
      resolved.content_hash = digestBytes(resolved.body);
    }
    return resolved;
  });

  const negativeFixture = fixture.negative_fixture ? { ...fixture.negative_fixture } : undefined;
  if (
    negativeFixture &&
    negativeFixture.content_hash === "recompute" &&
    negativeFixture.body !== undefined
  ) {
    negativeFixture.content_hash = digestBytes(negativeFixture.body);
  }

  const checks = (fixture.checks ?? []).map((check) => ({ ...check }));
  const statuses = checks.map((check) => check.status);
  const overall =
    fixture.verdicts?.overall === "recompute"
      ? foldVerdict(statuses)
      : fixture.verdicts?.overall;
  const perCheck = checks.map((check) => ({
    checker: check.checker,
    status: STATUS_TO_VERDICT[check.status] ?? "UNVERIFIABLE"
  }));

  const base = {
    schema: "project-telos.research-proof-packet/v1",
    packet_id: fixture.packet_id,
    objective: fixture.objective,
    source_refs: sourceRefs,
    negative_fixture: negativeFixture,
    attempts: fixture.attempts ?? [],
    checks,
    verdicts: { overall, per_check: perCheck },
    promotion: fixture.promotion,
    uncertainty: fixture.uncertainty ?? []
  };
  if (fixture.context_refs) {
    base.context_refs = fixture.context_refs;
  }
  if (fixture.evidence_classes) {
    base.evidence_classes = fixture.evidence_classes;
  }

  const packet = { ...base, packet_hash: packetHash(base) };
  packet.wall_clock = fixture.wall_clock ?? { assembled_at: "unpinned" };
  return packet;
}

function addFailure(failures, code, verdict, detail) {
  failures.push({ code, verdict, ...detail });
}

// Pure verifier: packet in, named check results plus a derived verdict out.
// There is no path that returns a literal MATCH without a passing check set:
// the verdict is folded from the recomputed checks, and any embedded verdict is
// compared against the derived one rather than trusted.
export function verifyResearchPacket(packet, options = {}) {
  const checks = [];
  const failures = [];

  // check.required_fields -> UNVERIFIABLE, naming each missing path.
  const missing = [];
  for (const pathExpr of REQUIRED_PATHS) {
    const value = getPath(packet, pathExpr);
    if (value === undefined || value === null) {
      missing.push(pathExpr);
    }
  }
  for (const pathExpr of missing) {
    addFailure(failures, "missing_required_field", "UNVERIFIABLE", { path: pathExpr });
  }
  let structurallyComplete = missing.length === 0;
  checks.push({ name: "check.required_fields", passed: missing.length === 0, missing });

  // Source-ref element fields (id, ref, content_hash, body). A missing one is a
  // missing required field (UNVERIFIABLE evidence gap), not tamper, so it marks
  // the packet structurally incomplete and suppresses the derivative digest
  // mismatch that deleting the body would otherwise cause.
  const sourceIds = new Set();
  const sourceRefs = Array.isArray(packet.source_refs) ? packet.source_refs : [];
  let sourceFieldsOk = true;
  sourceRefs.forEach((ref, index) => {
    for (const field of ["id", "ref", "content_hash", "body"]) {
      if (!ref || ref[field] === undefined || ref[field] === null) {
        sourceFieldsOk = false;
        structurallyComplete = false;
        addFailure(failures, "missing_required_field", "UNVERIFIABLE", {
          path: `source_refs[${index}].${field}`
        });
      }
    }
    if (ref && ref.id) {
      sourceIds.add(ref.id);
    }
  });
  checks.push({ name: "check.source_fields", passed: sourceFieldsOk });

  // check.source_digests -> DRIFT recomputing each source content_hash over its
  // embedded body. A source that claims a hash but carries no embedded body
  // cannot be recomputed: the hash is a load-bearing claim, so a missing body is
  // an UNVERIFIABLE evidence gap (already named above), never a silent pass.
  const sourceDeltas = [];
  sourceRefs.forEach((ref, index) => {
    if (!ref || ref.body === undefined || ref.body === null || !ref.content_hash) {
      return;
    }
    const recomputed = digestBytes(ref.body);
    if (ref.content_hash !== recomputed) {
      sourceDeltas.push({
        path: `source_refs[${index}].content_hash`,
        id: ref.id,
        expected: ref.content_hash,
        recomputed
      });
    }
  });
  for (const delta of sourceDeltas) {
    addFailure(failures, "source_digest_mismatch", "DRIFT", delta);
  }
  checks.push({ name: "check.source_digests", passed: sourceDeltas.length === 0 });

  // check.negative_fixture -> the control the claim must survive is required.
  // Its body must be present so its digest is recomputable, its content_hash
  // must match, and its control_outcome must be recorded. A missing body or
  // outcome is an UNVERIFIABLE evidence gap; a digest mismatch is DRIFT; a
  // recorded not_survived outcome is DRIFT (the check does not discriminate, so
  // the claim is not established). The required-field pass above already names a
  // missing block; this check adds the digest and outcome semantics.
  const neg = packet.negative_fixture;
  let negativeOk = true;
  if (neg && neg.body !== undefined && neg.body !== null && neg.content_hash) {
    const recomputed = digestBytes(neg.body);
    if (neg.content_hash !== recomputed) {
      negativeOk = false;
      addFailure(failures, "negative_fixture_digest_mismatch", "DRIFT", {
        path: "negative_fixture.content_hash",
        expected: neg.content_hash,
        recomputed
      });
    }
  }
  if (neg && neg.control_outcome !== undefined && neg.control_outcome !== null) {
    if (!CONTROL_OUTCOMES.has(neg.control_outcome)) {
      negativeOk = false;
      addFailure(failures, "state_model_violation", "DRIFT", {
        path: "negative_fixture.control_outcome",
        observed: neg.control_outcome,
        allowed: [...CONTROL_OUTCOMES]
      });
    } else if (neg.control_outcome === "not_survived") {
      negativeOk = false;
      addFailure(failures, "negative_control_not_survived", "DRIFT", {
        path: "negative_fixture.control_outcome",
        observed: "not_survived",
        reason:
          "the check accepted the control variant, so it does not discriminate and the claim is not established"
      });
    }
  }
  checks.push({ name: "check.negative_fixture", passed: negativeOk });

  // check.state_model -> DRIFT with observed value and allowed set for attempt
  // results and check statuses.
  const stateDeltas = [];
  const attempts = Array.isArray(packet.attempts) ? packet.attempts : [];
  attempts.forEach((attempt, index) => {
    const result = attempt?.result;
    if (result !== undefined && !ATTEMPT_RESULTS.has(result)) {
      stateDeltas.push({
        path: `attempts[${index}].result`,
        observed: result,
        allowed: [...ATTEMPT_RESULTS]
      });
    }
  });
  const checkList = Array.isArray(packet.checks) ? packet.checks : [];
  checkList.forEach((check, index) => {
    const status = check?.status;
    if (status !== undefined && !CHECK_STATUSES.has(status)) {
      stateDeltas.push({
        path: `checks[${index}].status`,
        observed: status,
        allowed: [...CHECK_STATUSES]
      });
    }
  });
  for (const delta of stateDeltas) {
    addFailure(failures, "state_model_violation", "DRIFT", delta);
  }
  checks.push({ name: "check.state_model", passed: stateDeltas.length === 0 });

  // check.evidence_refs -> UNVERIFIABLE when a check names a source ref that is
  // not declared. A check whose evidence cannot be resolved to a declared source
  // is an evidence gap, not a pass.
  let evidenceOk = true;
  checkList.forEach((check, index) => {
    const ids = Array.isArray(check?.source_ref_ids) ? check.source_ref_ids : [];
    if (!ids.length) {
      evidenceOk = false;
      structurallyComplete = false;
      addFailure(failures, "missing_required_field", "UNVERIFIABLE", {
        path: `checks[${index}].source_ref_ids`
      });
      return;
    }
    for (const id of ids) {
      if (!sourceIds.has(id)) {
        evidenceOk = false;
        addFailure(failures, "evidence_ref_unresolvable", "UNVERIFIABLE", {
          path: `checks[${index}].source_ref_ids`,
          ref: id
        });
      }
    }
  });
  checks.push({ name: "check.evidence_refs", passed: evidenceOk });

  // check.promotion -> DRIFT when a single packet asserts a reproduction-gated
  // rung (PROMOTED_DISCOVERY, LAW_CANDIDATE). A rung outside the assertable set
  // is a state_model_violation.
  let promotionOk = true;
  const promotion = packet.promotion;
  if (promotion !== undefined && promotion !== null) {
    if (RESERVED_PROMOTIONS.has(promotion)) {
      promotionOk = false;
      addFailure(failures, "promotion_not_assertable_in_single_packet", "DRIFT", {
        path: "promotion",
        observed: promotion,
        reason: "this rung needs independent reproduction and review; a single packet may not assert it"
      });
    } else if (!ASSERTABLE_PROMOTIONS.has(promotion)) {
      promotionOk = false;
      addFailure(failures, "state_model_violation", "DRIFT", {
        path: "promotion",
        observed: promotion,
        allowed: [...ASSERTABLE_PROMOTIONS]
      });
    }
  }
  checks.push({ name: "check.promotion", passed: promotionOk });

  // check.verdict_status -> the recorded per-check verdict must be the fold of
  // the recorded check status. A recorded overall that disagrees with the fold
  // of the statuses is check_status_not_derivable (DRIFT): the verdict was not
  // derived from the checks it claims to summarize.
  let statusDerivable = true;
  const statuses = checkList.map((check) => check?.status).filter((s) => CHECK_STATUSES.has(s));
  const recomputedOverall = foldVerdict(statuses);
  const recordedOverall = packet.verdicts?.overall;
  if (
    structurallyComplete &&
    recordedOverall !== undefined &&
    recordedOverall !== recomputedOverall
  ) {
    statusDerivable = false;
    addFailure(failures, "check_status_not_derivable", "DRIFT", {
      path: "verdicts.overall",
      recorded: recordedOverall,
      recomputed: recomputedOverall
    });
  }
  checks.push({ name: "check.verdict_status", passed: statusDerivable, skipped: !structurallyComplete });

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

  // Derive the verdict by one fold over the failures. DRIFT dominates
  // UNVERIFIABLE dominates MATCH.
  const hasDrift = failures.some((f) => f.verdict === "DRIFT");
  const hasUnverifiable = failures.some((f) => f.verdict === "UNVERIFIABLE");
  const derivedVerdict = hasDrift ? "DRIFT" : hasUnverifiable ? "UNVERIFIABLE" : "MATCH";

  // check.verdict_derivation: the verdict is derived from the checks alone, so a
  // canned MATCH embedded in verdicts.overall can never win. When an embedded
  // verdict disagrees with the derived one, the disagreement is recorded as a
  // failure that inherits the derived severity, so it flags the lie without ever
  // claiming a better verdict than the materials support.
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

  const finalVerdict =
    !derivationOk && derivedVerdict === "MATCH" ? "DRIFT" : derivedVerdict;

  return {
    checks,
    failures,
    verdict: finalVerdict
  };
}

// ---------------------------------------------------------------------------
// Export to proof-surface research-claim-proof-packet/v0.
// ---------------------------------------------------------------------------

// Strip the sha256: prefix; proof-surface source sha256 is bare 64-hex or null.
function bare(digest) {
  if (typeof digest !== "string") return null;
  const stripped = digest.replace(/^sha256:/, "");
  return /^[0-9a-f]{64}$/.test(stripped) ? stripped : null;
}

// internal check status -> proof-surface CHECK_STATUSES (identity here, but
// mapped explicitly so a taxonomy change is a one-line edit).
const CHECK_STATUS_MAP = { pass: "pass", fail: "fail", unverifiable: "unverifiable" };
// internal check status -> proof-surface per_check OVERALL_VERDICTS.
const PER_CHECK_VERDICT_MAP = { pass: "MATCH", fail: "DRIFT", unverifiable: "UNVERIFIABLE" };

// proof-surface overall verdict -> decision_summary, mirroring proof-surface
// _decision.derive_decision_summary exactly.
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

// Map each Telos verifier failure code into the nearest proof-surface
// FAILURE_CODES member (closed set, verified against proof-surface HEAD
// 8757032 _failure.py FAILURE_CODES). Unmapped codes fall back to
// verification_unverifiable rather than being dropped, so no failure leaves the
// export unlabeled.
const FAILURE_LABEL_MAP = {
  missing_required_field: "evidence_gap",
  evidence_ref_unresolvable: "evidence_gap",
  source_digest_mismatch: "binding_failed",
  negative_fixture_digest_mismatch: "binding_failed",
  packet_hash_mismatch: "binding_failed",
  state_model_violation: "binding_failed",
  negative_control_not_survived: "verification_unverifiable",
  check_status_not_derivable: "verification_unverifiable",
  promotion_not_assertable_in_single_packet: "verification_unverifiable",
  embedded_verdict_not_derived: "verification_unverifiable"
};

function mapFailureLabels(failures) {
  const labels = [];
  const seen = new Set();
  for (const failure of failures ?? []) {
    const mapped = FAILURE_LABEL_MAP[failure?.code] ?? "verification_unverifiable";
    if (!seen.has(mapped)) {
      seen.add(mapped);
      labels.push(mapped);
    }
  }
  return labels;
}

// Re-derive the verdict and failures from the packet's own materials rather than
// trusting an embedded verdicts.overall. verdict_derived_not_asserted holds on
// the export surface, not only on the verify path, so a stale MATCH over
// tampered materials is caught and lowered, never copied into the export.
function deriveVerification(packet) {
  const embedded = packet.verdicts?.overall;
  return verifyResearchPacket(packet, { embeddedVerdict: embedded });
}

// Export a Telos research proof packet to the proof-surface
// research-claim-proof-packet/v0 shape. proof-surface is never imported at
// runtime; the field list is frozen as a test fixture instead. The
// reproduction-gated rungs are never emitted, and decision_summary is derived
// from the overall verdict, never from any attempt or promotion field.
export function toProofSurfaceResearchPacket(packet) {
  const verification = deriveVerification(packet);
  const verdict = verification.verdict;
  const failureLabels = mapFailureLabels(verification.failures);

  const sources = (packet.source_refs ?? []).map((ref) => ({
    ref: ref.ref,
    sha256: bare(ref.content_hash)
  }));

  const attempts = (packet.attempts ?? []).map((attempt) => {
    const entry = {
      attempt_id: attempt.attempt_id,
      method: attempt.method,
      result: attempt.result
    };
    if (attempt.artifact_ref !== undefined && attempt.artifact_ref !== null) {
      entry.artifact_ref = attempt.artifact_ref;
    }
    if (attempt.notes !== undefined && attempt.notes !== null) {
      entry.notes = attempt.notes;
    }
    return entry;
  });

  // The negative fixture is surfaced as a check so the export carries the control
  // and its recorded outcome. A survived control is a pass; a not-survived
  // control is a fail. The check names its source in evidence.
  const negative = packet.negative_fixture;
  const negativeStatus = negative?.control_outcome === "survived" ? "pass" : "fail";

  const checks = [];
  const perCheck = [];
  for (const check of packet.checks ?? []) {
    const status = CHECK_STATUS_MAP[check.status] ?? "unverifiable";
    const evidence = Array.isArray(check.evidence) ? [...check.evidence] : [];
    const entry = { checker: check.checker, status, evidence };
    if (check.notes !== undefined && check.notes !== null) {
      entry.notes = check.notes;
    }
    checks.push(entry);
    perCheck.push({
      checker: check.checker,
      status: PER_CHECK_VERDICT_MAP[check.status] ?? "UNVERIFIABLE"
    });
  }
  if (negative) {
    const negChecker = `negative_fixture:${negative.id ?? "control"}`;
    checks.push({
      checker: negChecker,
      status: negativeStatus,
      evidence: [
        `control ${negative.id ?? "control"} recorded outcome ${negative.control_outcome ?? "unrecorded"}`
      ]
    });
    perCheck.push({
      checker: negChecker,
      status: PER_CHECK_VERDICT_MAP[negativeStatus] ?? "UNVERIFIABLE"
    });
  }

  const uncertainty = [...(packet.uncertainty ?? [])];
  uncertainty.push("source bodies are embedded and digest-bound but upstream full texts are not re-fetched during export");

  // The promotion carries through only when it is assertable in a single packet
  // AND the derived verdict supports it. A reproduction-gated rung is never
  // emitted, and a positive rung is not emitted over a non-MATCH verdict: a
  // DRIFT or UNVERIFIABLE run falls back to the honest UNVERIFIABLE rung, which
  // claims no achievement. A recorded REFUTED (a standing counterexample) is
  // preserved because it is a negative result, not an overclaim.
  let promotion;
  if (!ASSERTABLE_PROMOTIONS.has(packet.promotion)) {
    promotion = "UNVERIFIABLE";
  } else if (packet.promotion === "REFUTED") {
    promotion = "REFUTED";
  } else if (verdict === "MATCH") {
    promotion = packet.promotion;
  } else {
    promotion = "UNVERIFIABLE";
  }

  const exported = {
    version: "research-claim-proof-packet/v0",
    packet_id: packet.packet_id,
    claim: packet.objective?.claim,
    scope: packet.objective?.scope,
    statement: packet.objective?.statement,
    sources,
    attempts,
    checks,
    verdicts: { overall: verdict, per_check: perCheck },
    promotion,
    uncertainty,
    decision_summary: deriveDecisionSummary(verdict, verdict === "UNVERIFIABLE" ? uncertainty : []),
    formal: null,
    failure_labels: failureLabels,
    declared_branches: null,
    witness_tier: null,
    evidence_classes: Array.isArray(packet.evidence_classes) ? [...packet.evidence_classes] : null
  };
  return exported;
}
