import {
  stableStringify,
  sha256Prefixed,
  digestBytes,
  packetHash
} from "./proof-core.mjs";

// The visual-truth lane. It assembles and verifies a read-only visual or color
// measurement proof packet, then exports it to the proof-surface
// visual-measurement-proof-packet/v0 shape. Every load-bearing measurement is
// recomputed from the artifact's own embedded sRGB samples with stdlib math, so
// the verifier can fail: a tampered value drifts, a measurement with no
// recomputable basis is an UNVERIFIABLE gap named by its path, a non-read-only
// packet is rejected, and a physical-calibration claim over a read-only packet
// is rejected. There is no code path that returns a literal MATCH without a
// passing check set.

const ARTIFACT_KINDS = new Set(["image", "render", "lut", "icc", "video"]);
const RECOMPUTE_METHODS = new Set(["relative_luminance_srgb", "delta_e_cie76"]);

// Per-method tolerance ceilings, bounded to a small fraction of each metric's
// physical range. Without a ceiling, tolerance is an author-controlled dial with
// no upper bound: a whole-range tolerance would nullify the recompute's
// discriminating power and let a value far from the recomputed truth reach MATCH.
// relative_luminance_srgb is defined on [0, 1], so a tolerance above 0.1
// (a tenth of the range) can no longer discriminate a real luminance match.
// delta_e_cie76 spans roughly [0, 100] over the sRGB gamut, and a CIE76 delta of
// 10 is already a large, plainly visible color difference, so a tolerance above
// 10 can no longer discriminate a real color match. A tolerance above its ceiling
// is a state_model_violation (DRIFT), not a silent pass.
const TOLERANCE_CEILINGS = {
  relative_luminance_srgb: 0.1,
  delta_e_cie76: 10
};

// Required JSON paths. A missing one is reported by its own path and lowers the
// verdict to UNVERIFIABLE.
const REQUIRED_PATHS = [
  "schema",
  "packet_id",
  "claim",
  "scope",
  "artifact.name",
  "artifact.digest",
  "artifact.kind",
  "artifact.samples",
  "color.color_space",
  "color.transfer",
  "read_only",
  "measurements",
  "display_caveats",
  "calibration_boundary.hardware_measurement_used",
  "calibration_boundary.physical_calibration_claim",
  "packet_hash"
];

function getPath(obj, path) {
  return path.split(".").reduce((node, key) => (node == null ? undefined : node[key]), obj);
}

// ---------------------------------------------------------------------------
// Color math. Stdlib only: no lookup tables, no external color library.
// sRGB channel [0..255] -> linear light, IEC 61966-2-1 transfer.
// ---------------------------------------------------------------------------
function srgbToLinear(channel) {
  const cs = channel / 255;
  return cs <= 0.04045 ? cs / 12.92 : Math.pow((cs + 0.055) / 1.055, 2.4);
}

// Rec. 709 relative luminance from an sRGB triple.
function relativeLuminance([r, g, b]) {
  return 0.2126 * srgbToLinear(r) + 0.7152 * srgbToLinear(g) + 0.0722 * srgbToLinear(b);
}

// sRGB -> CIE XYZ (D65), then XYZ -> CIE Lab. Used for a CIE76 delta-E.
function srgbToXyz([r, g, b]) {
  const R = srgbToLinear(r);
  const G = srgbToLinear(g);
  const B = srgbToLinear(b);
  return [
    R * 0.4124564 + G * 0.3575761 + B * 0.1804375,
    R * 0.2126729 + G * 0.7151522 + B * 0.072175,
    R * 0.0193339 + G * 0.119192 + B * 0.9503041
  ];
}

function xyzToLab([X, Y, Z]) {
  const Xn = 0.95047;
  const Yn = 1.0;
  const Zn = 1.08883;
  const f = (t) => (t > 0.008856 ? Math.cbrt(t) : 7.787 * t + 16 / 116);
  const fx = f(X / Xn);
  const fy = f(Y / Yn);
  const fz = f(Z / Zn);
  return [116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)];
}

function labOf(rgb) {
  return xyzToLab(srgbToXyz(rgb));
}

function deltaE76(a, b) {
  const la = labOf(a);
  const lb = labOf(b);
  return Math.sqrt(
    (la[0] - lb[0]) ** 2 + (la[1] - lb[1]) ** 2 + (la[2] - lb[2]) ** 2
  );
}

// A sample is a recomputable basis only when it is an array of three finite
// numbers in [0..255]. Anything else is not a recomputable basis.
function isSample(value) {
  return (
    Array.isArray(value) &&
    value.length === 3 &&
    value.every((c) => typeof c === "number" && Number.isFinite(c) && c >= 0 && c <= 255)
  );
}

// Recompute one measurement from the artifact's embedded samples. Returns either
// { ok: true, value } or { ok: false, missing: <sample id or reason> } so the
// verifier can turn a missing basis into an UNVERIFIABLE gap named by its path.
function recomputeMeasurement(measurement, samples) {
  const method = measurement?.method;
  const refs = Array.isArray(measurement?.sample_refs) ? measurement.sample_refs : [];
  const resolved = [];
  for (const ref of refs) {
    const sample = samples ? samples[ref] : undefined;
    if (!isSample(sample)) {
      return { ok: false, missing: ref };
    }
    resolved.push(sample);
  }
  if (method === "relative_luminance_srgb") {
    if (resolved.length !== 1) {
      return { ok: false, missing: "relative_luminance_srgb needs exactly one sample_ref" };
    }
    return { ok: true, value: relativeLuminance(resolved[0]) };
  }
  if (method === "delta_e_cie76") {
    if (resolved.length !== 2) {
      return { ok: false, missing: "delta_e_cie76 needs exactly two sample_refs" };
    }
    return { ok: true, value: deltaE76(resolved[0], resolved[1]) };
  }
  return { ok: false, missing: `unknown recompute method ${method}` };
}

// Canonical byte view of the artifact samples: the recompute basis serialized
// with the same sorted-key, whitespace-free rule as the packet hash. The
// artifact digest is recomputed over these bytes so a tampered sample changes
// the digest, giving a second, independent tamper signal.
function sampleBytes(samples) {
  return stableStringify(samples ?? {});
}

function recomputeArtifactDigest(samples) {
  return digestBytes(sampleBytes(samples));
}

// ---------------------------------------------------------------------------
// Assemble a canonical packet from fixture materials. Deterministic: no clock,
// no randomness inside the hash scope. The artifact digest is recomputed from
// the embedded samples so the fixture never has to hardcode it.
// ---------------------------------------------------------------------------
export function assembleVisualPacket(fixture) {
  const artifact = {
    ...fixture.artifact,
    digest: recomputeArtifactDigest(fixture.artifact?.samples)
  };
  const base = {
    schema: "project-telos.visual-proof-packet/v1",
    packet_id: fixture.packet_id,
    claim: fixture.claim,
    scope: fixture.scope,
    artifact,
    color: fixture.color,
    read_only: fixture.read_only,
    measurements: fixture.measurements,
    display_caveats: fixture.display_caveats,
    calibration_boundary: fixture.calibration_boundary
  };
  const packet = { ...base, packet_hash: packetHash(base) };
  packet.wall_clock = fixture.wall_clock ?? { assembled_at: "unpinned" };
  return packet;
}

// Convenience wrapper mirroring the sibling lane's {fixture|demo} entry.
export function assembleVisual({ fixture, demo } = {}) {
  if (fixture) return assembleVisualPacket(fixture);
  if (demo) return assembleVisualPacket(demo);
  throw new Error("assembleVisual requires a fixture or demo object");
}

function addFailure(failures, code, verdict, detail) {
  failures.push({ code, verdict, ...detail });
}

// ---------------------------------------------------------------------------
// Pure verifier: packet in, named check results plus a derived verdict out.
// ---------------------------------------------------------------------------
export function verifyVisualPacket(packet, options = {}) {
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
  for (const path of missing) {
    addFailure(failures, "missing_required_field", "UNVERIFIABLE", { path });
  }
  let structurallyComplete = missing.length === 0;
  checks.push({ name: "check.required_fields", passed: missing.length === 0, missing });

  // check.artifact_kind -> DRIFT with observed value and allowed set.
  const kindDeltas = [];
  const kind = packet.artifact?.kind;
  if (kind !== undefined && !ARTIFACT_KINDS.has(kind)) {
    kindDeltas.push({ path: "artifact.kind", observed: kind, allowed: [...ARTIFACT_KINDS] });
  }
  for (const delta of kindDeltas) {
    addFailure(failures, "state_model_violation", "DRIFT", delta);
  }
  checks.push({ name: "check.artifact_kind", passed: kindDeltas.length === 0 });

  // check.read_only -> DRIFT. A read-only visual surface never mutates hardware.
  // A packet that is not read-only is a structural violation, never a silent
  // pass: the whole non-mutation boundary rests on this flag being true.
  let readOnlyOk = true;
  if (packet.read_only !== true) {
    readOnlyOk = false;
    addFailure(failures, "read_only_not_true", "DRIFT", {
      path: "read_only",
      observed: packet.read_only ?? null,
      required: true
    });
  }
  checks.push({ name: "check.read_only", passed: readOnlyOk });

  // check.calibration_boundary -> DRIFT. A read-only packet with no hardware
  // measurement may not claim a physical calibration. This mirrors proof-surface
  // _calibration.validate_calibration_boundary: a physical_calibration_claim is
  // admissible only alongside a hardware measurement, an instrument, mutation
  // evidence, and a non-read-only packet. In this lane the packet is read-only
  // by construction, so any physical_calibration_claim is an overclaim.
  let calibrationOk = true;
  const cb = packet.calibration_boundary ?? {};
  if (cb.physical_calibration_claim === true) {
    const grounded =
      cb.hardware_measurement_used === true &&
      typeof cb.instrument === "string" &&
      cb.instrument.trim().length > 0 &&
      Array.isArray(cb.mutation_evidence) &&
      cb.mutation_evidence.length > 0 &&
      packet.read_only !== true;
    if (!grounded) {
      calibrationOk = false;
      addFailure(failures, "physical_calibration_overclaim", "DRIFT", {
        path: "calibration_boundary.physical_calibration_claim",
        reason:
          "a physical calibration claim requires a hardware measurement, an instrument, mutation evidence, and a non-read-only packet"
      });
    }
  }
  checks.push({ name: "check.calibration_boundary", passed: calibrationOk });

  // check.packet_hash -> DRIFT with expected and observed. Only runs when the
  // packet is structurally complete; a missing required field is UNVERIFIABLE
  // and must not be masked by a derivative hash mismatch.
  const observedHash = packet.packet_hash;
  const expectedHash = packetHash(packet);
  const hashOk = observedHash === expectedHash;
  if (structurallyComplete && !hashOk) {
    addFailure(failures, "packet_hash_mismatch", "DRIFT", {
      expected: expectedHash,
      observed: observedHash
    });
  }
  checks.push({ name: "check.packet_hash", passed: hashOk, skipped: !structurallyComplete });

  // check.artifact_digest -> DRIFT. The artifact digest is recomputed over the
  // canonical sample bytes. A tampered sample changes the digest, so this is a
  // second, independent tamper signal alongside the per-measurement recompute.
  let artifactDigestOk = true;
  const samples = packet.artifact?.samples;
  if (samples !== undefined && samples !== null && packet.artifact?.digest !== undefined) {
    const recomputed = recomputeArtifactDigest(samples);
    if (packet.artifact.digest !== recomputed) {
      artifactDigestOk = false;
      addFailure(failures, "measurement_value_mismatch", "DRIFT", {
        path: "artifact.digest",
        expected: packet.artifact.digest,
        recomputed
      });
    }
  }
  checks.push({ name: "check.artifact_digest", passed: artifactDigestOk });

  // check.measurements -> the core recompute. Each measurement value is
  // recomputed from the embedded samples. A deviation above tolerance is DRIFT
  // carrying the recomputed value. A measurement whose method or sample_refs
  // point at a basis the artifact does not carry cannot be recomputed: that is
  // an UNVERIFIABLE evidence gap named by its JSON path, never a silent pass.
  // Trusting a claimed value on faith would let a phantom or tampered
  // measurement reach MATCH with zero failures.
  const perMetric = [];
  let measurementsOk = true;
  const measurements = Array.isArray(packet.measurements) ? packet.measurements : [];

  // A packet with no measurements recomputes nothing, so it must never reach
  // MATCH: an empty measurement set is an UNVERIFIABLE evidence gap (nothing was
  // checked), mirroring the research lane's empty-check floor. Without this a
  // degenerate packet with measurements: [] would fold to MATCH with zero
  // recomputes run, which is exactly the phantom pass this lane forbids.
  if (measurements.length === 0) {
    measurementsOk = false;
    addFailure(failures, "no_measurements", "UNVERIFIABLE", {
      path: "measurements",
      reason: "the packet carries no measurements, so nothing was recomputed and no claim is established"
    });
  }

  measurements.forEach((measurement, index) => {
    const metric = measurement?.metric ?? `measurements[${index}]`;
    const path = `measurements[${index}]`;

    // Per-measurement required fields. A missing one is an UNVERIFIABLE gap.
    const measMissing = [];
    for (const field of ["metric", "method", "value", "unit", "tolerance"]) {
      if (measurement?.[field] === undefined || measurement?.[field] === null) {
        measMissing.push(`${path}.${field}`);
      }
    }
    if (measMissing.length) {
      measurementsOk = false;
      structurallyComplete = false;
      for (const m of measMissing) {
        addFailure(failures, "missing_required_field", "UNVERIFIABLE", { path: m });
      }
      perMetric.push({ metric, status: "UNVERIFIABLE" });
      return;
    }

    if (!RECOMPUTE_METHODS.has(measurement.method)) {
      measurementsOk = false;
      addFailure(failures, "measurement_not_recomputable", "UNVERIFIABLE", {
        path: `${path}.method`,
        reason: `unknown recompute method ${measurement.method}`
      });
      perMetric.push({ metric, status: "UNVERIFIABLE" });
      return;
    }

    const outcome = recomputeMeasurement(measurement, samples);
    if (!outcome.ok) {
      measurementsOk = false;
      addFailure(failures, "measurement_not_recomputable", "UNVERIFIABLE", {
        path: `${path}.sample_refs`,
        reason: `measurement cannot be recomputed: ${outcome.missing}`
      });
      perMetric.push({ metric, status: "UNVERIFIABLE" });
      return;
    }

    const tolerance = measurement.tolerance;
    if (typeof tolerance !== "number" || !(tolerance > 0)) {
      measurementsOk = false;
      addFailure(failures, "state_model_violation", "DRIFT", {
        path: `${path}.tolerance`,
        observed: tolerance,
        required: "a positive number"
      });
      perMetric.push({ metric, status: "DRIFT" });
      return;
    }

    // Bound the tolerance to the metric's physical range. An oversized tolerance
    // nullifies the recompute's discriminating power, so a whole-range tolerance
    // could launder a false value into MATCH. A tolerance above its per-method
    // ceiling is a state_model_violation (DRIFT), never a silent pass.
    const ceiling = TOLERANCE_CEILINGS[measurement.method];
    if (ceiling !== undefined && tolerance > ceiling) {
      measurementsOk = false;
      addFailure(failures, "tolerance_exceeds_bound", "DRIFT", {
        path: `${path}.tolerance`,
        observed: tolerance,
        ceiling,
        method: measurement.method,
        reason:
          "the declared tolerance exceeds the metric's bounded physical range, so it can no longer discriminate a real match"
      });
      perMetric.push({ metric, status: "DRIFT" });
      return;
    }

    const claimed = measurement.value;
    const deviation = Math.abs(claimed - outcome.value);
    if (deviation > tolerance) {
      measurementsOk = false;
      addFailure(failures, "measurement_value_mismatch", "DRIFT", {
        path: `${path}.value`,
        metric,
        claimed,
        recomputed: outcome.value,
        deviation,
        tolerance
      });
      perMetric.push({ metric, status: "DRIFT" });
    } else {
      perMetric.push({ metric, status: "MATCH", deviation, recomputed: outcome.value });
    }
  });
  checks.push({ name: "check.measurements", passed: measurementsOk });

  // Derive the verdict by one fold. DRIFT dominates UNVERIFIABLE dominates MATCH.
  const hasDrift = failures.some((f) => f.verdict === "DRIFT");
  const hasUnverifiable = failures.some((f) => f.verdict === "UNVERIFIABLE");
  const derivedVerdict = hasDrift ? "DRIFT" : hasUnverifiable ? "UNVERIFIABLE" : "MATCH";

  // check.verdict_derivation: the verdict is derived from the checks alone, so a
  // canned MATCH embedded in the packet can never win. When an embedded verdict
  // disagrees with the derived one, that disagreement is itself a failure at the
  // derived severity, so an embedded MATCH over tampered materials stays DRIFT
  // and an embedded MATCH over an incomplete packet stays UNVERIFIABLE.
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
    per_metric: perMetric,
    verdict: finalVerdict
  };
}

// ---------------------------------------------------------------------------
// Export to the proof-surface visual-measurement-proof-packet/v0 shape. The
// verdict is re-derived from the packet's own materials, never copied from an
// embedded verifier block. decision_summary is derived from the overall verdict.
// read_only is carried through as true. proof-surface is never imported here.
// ---------------------------------------------------------------------------

// Strip the sha256: prefix; proof-surface requires bare 64-hex.
function bare(digest) {
  return typeof digest === "string" ? digest.replace(/^sha256:/, "") : digest;
}

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

// telos visual failure codes -> proof-surface FAILURE_CODES (closed set in
// _failure.py at proof-surface HEAD). Any unmapped code falls back to
// verification_unverifiable so no failure leaves the export unlabeled.
const FAILURE_LABEL_MAP = {
  missing_required_field: "evidence_gap",
  measurement_not_recomputable: "evidence_gap",
  no_measurements: "evidence_gap",
  read_only_not_true: "binding_failed",
  physical_calibration_overclaim: "binding_failed",
  measurement_value_mismatch: "binding_failed",
  packet_hash_mismatch: "binding_failed",
  state_model_violation: "binding_failed",
  tolerance_exceeds_bound: "binding_failed",
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

// Build the disclosed-limits list. The read-only sample-only basis and the
// approximations in the metrics are named here so nothing is silently dropped.
function buildUncertainty(packet) {
  const notes = [];
  notes.push(
    "measurements are recomputed from the artifact's embedded sRGB samples, not measured off a physical display"
  );
  notes.push(
    "no monitor, LUT, or ICC profile was read or written; the packet is read-only by construction"
  );
  const hasDeltaE = (packet.measurements ?? []).some((m) => m?.method === "delta_e_cie76");
  if (hasDeltaE) {
    notes.push(
      "delta-E is CIE76 under the D65 white point, a first-order color-difference estimate rather than a perceptual guarantee"
    );
  }
  return notes;
}

// Recompute deviation for the export from the embedded samples so the exported
// measurement carries a re-derivable deviation, not a copied one.
function exportMeasurement(measurement, samples) {
  const outcome = recomputeMeasurement(measurement, samples);
  const deviation = outcome.ok ? Math.abs(measurement.value - outcome.value) : measurement.value;
  return {
    metric: measurement.metric,
    value: measurement.value,
    unit: measurement.unit,
    target: typeof measurement.target === "number" ? measurement.target : measurement.value,
    tolerance: measurement.tolerance,
    deviation,
    method: measurement.method,
    evidence: [
      `recompute:${measurement.method}`,
      ...((measurement.sample_refs ?? []).map((ref) => `sample:${ref}`))
    ]
  };
}

export function toProofSurfaceVisualPacket(packet) {
  const embedded = packet.verifier?.verdict;
  const verification = verifyVisualPacket(packet, { embeddedVerdict: embedded });
  const verdict = verification.verdict;
  const samples = packet.artifact?.samples;

  const measurements = (packet.measurements ?? []).map((m) => exportMeasurement(m, samples));

  // per_metric from the verifier's own per-metric statuses, one per metric.
  const perMetric = verification.per_metric.map((entry) => ({
    metric: entry.metric,
    status: entry.status
  }));

  // A read-only packet never claims a physical calibration. The exported
  // boundary carries the two required booleans; a physical claim is only ever
  // exported when the verifier confirmed it is grounded (it is not, in this
  // read-only lane), so the exported claim is always false here.
  const cb = packet.calibration_boundary ?? {};
  const calibrationOverclaimed = verification.failures.some(
    (f) => f.code === "physical_calibration_overclaim"
  );
  const calibration_boundary = {
    hardware_measurement_used: cb.hardware_measurement_used === true,
    physical_calibration_claim:
      cb.physical_calibration_claim === true && !calibrationOverclaimed,
    instrument: typeof cb.instrument === "string" ? cb.instrument : null
  };

  const artifact = {
    name: packet.artifact?.name,
    sha256: bare(packet.artifact?.digest),
    kind: packet.artifact?.kind,
    width: typeof packet.artifact?.width === "number" ? packet.artifact.width : null,
    height: typeof packet.artifact?.height === "number" ? packet.artifact.height : null
  };

  const color = {
    color_space: packet.color?.color_space,
    transfer: packet.color?.transfer,
    white_point: packet.color?.white_point ?? null,
    primaries: packet.color?.primaries ?? null,
    notes: packet.color?.notes ?? null
  };

  return {
    version: "visual-measurement-proof-packet/v0",
    packet_id: packet.packet_id,
    claim: packet.claim,
    scope: packet.scope,
    artifact,
    color,
    read_only: packet.read_only === true,
    measurements,
    display_caveats: [...(packet.display_caveats ?? [])],
    calibration_boundary,
    failure_labels: mapFailureLabels(verification.failures),
    verdicts: { overall: verdict, per_metric: perMetric },
    uncertainty: buildUncertainty(packet),
    decision_summary: deriveDecisionSummary(verdict, [])
  };
}
