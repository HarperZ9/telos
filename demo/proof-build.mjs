import {
  stableStringify,
  sha256Prefixed,
  digestBytes,
  packetHash
} from "./proof-core.mjs";

// The build scientific-runtime lane. It assembles and verifies a buildc
// scientific-compute proof packet, then exports it to the proof-surface
// conservation-proof-packet/v0 shape. A source program (a buildc-compiled
// routine, identified by a SHA-256 source digest) undergoes a numerical run over
// a backend, and a claimed invariant (a conserved quantity) is recomputed from
// the run's embedded samples with stdlib math and checked within a bounded
// tolerance. A required negative fixture is a control run that must break the
// invariant. Every load-bearing claim is recomputed from embedded materials, so
// the verifier can fail: a tampered source program drifts the digest, a wrong
// invariant value drifts against the recomputed mean, an over-tolerance run
// drifts on the conservation metric, a control that does not break the invariant
// is DRIFT, an empty run is an UNVERIFIABLE gap, and an oversized author-declared
// tolerance is rejected. There is no code path that returns a literal MATCH
// without a passing check set.

const INVARIANT_METHODS = new Set(["mean_total_energy", "max_relative_energy_drift"]);
const DRIFT_METHODS = new Set(["max_relative_energy_drift"]);
const BACKEND_MATURITY = new Set(["verified", "experimental"]);
const EFFECT_CLASSES = new Set(["none", "read", "write", "external_call", "mixed"]);

// Per-method tolerance ceilings, bounded to a small fraction of each metric's
// physical range. Without a ceiling, tolerance is an author-controlled dial with
// no upper bound: a whole-range tolerance would nullify the recompute's
// discriminating power and let a value far from the recomputed truth reach MATCH.
// max_relative_energy_drift is a relative fraction on [0, 1], so a tolerance
// above 0.1 (a tenth of the range) can no longer discriminate a conserved run
// from a lossy one. mean_total_energy is bounded to a fraction of the recomputed
// energy scale: its ceiling is one hundredth of the recomputed mean energy, so it
// is computed against the samples rather than fixed, since energy is not on a
// unit range. A tolerance above its ceiling is a state_model_violation (DRIFT).
const RELATIVE_DRIFT_CEILING = 0.1;
const MEAN_ENERGY_CEILING_FRACTION = 0.01;

// Required JSON paths. A missing one is reported by its own path and lowers the
// verdict to UNVERIFIABLE.
const REQUIRED_PATHS = [
  "schema",
  "packet_id",
  "claim",
  "scope",
  "receipt.source_id",
  "receipt.source_program",
  "receipt.source_digest",
  "receipt.effect_class",
  "receipt.policy_summary",
  "receipt.backend_label",
  "receipt.backend_maturity",
  "run.constants.mass",
  "run.constants.stiffness",
  "run.samples",
  "invariant.name",
  "invariant.method",
  "invariant.value",
  "invariant.unit",
  "invariant.tolerance",
  "drift.method",
  "drift.value",
  "drift.tolerance",
  "negative_fixture.id",
  "negative_fixture.description",
  "negative_fixture.samples",
  "negative_fixture.drift_method",
  "negative_fixture.conservation_tolerance",
  "boundary_run.id",
  "boundary_run.description",
  "boundary_run.samples",
  "packet_hash"
];

function getPath(obj, path) {
  return path.split(".").reduce((node, key) => (node == null ? undefined : node[key]), obj);
}

// ---------------------------------------------------------------------------
// Invariant math. Stdlib only. A sample is [t, position, velocity].
// The total mechanical energy of a one-dimensional harmonic oscillator is
// E = 0.5 m v*v + 0.5 k x*x, a conserved quantity for the undamped case.
// ---------------------------------------------------------------------------

// A sample is a recomputable basis only when it is an array whose position and
// velocity are finite numbers. The leading time field is not load-bearing for the
// energy recompute, so it is not constrained beyond being present.
function isSample(value) {
  return (
    Array.isArray(value) &&
    value.length >= 3 &&
    typeof value[1] === "number" &&
    Number.isFinite(value[1]) &&
    typeof value[2] === "number" &&
    Number.isFinite(value[2])
  );
}

function sampleEnergy(sample, mass, stiffness) {
  const x = sample[1];
  const v = sample[2];
  return 0.5 * mass * v * v + 0.5 * stiffness * x * x;
}

// Recompute the energy series and its summary statistics from the embedded
// samples. Returns { ok: true, mean, maxRelDrift, energies } or
// { ok: false, missing } so the verifier can turn a missing basis into an
// UNVERIFIABLE gap named by its path.
function recomputeEnergyStats(samples, mass, stiffness) {
  if (!Array.isArray(samples) || samples.length === 0) {
    return { ok: false, missing: "no samples to recompute from" };
  }
  if (typeof mass !== "number" || !Number.isFinite(mass) || mass <= 0) {
    return { ok: false, missing: "mass must be a positive number" };
  }
  if (typeof stiffness !== "number" || !Number.isFinite(stiffness) || stiffness <= 0) {
    return { ok: false, missing: "stiffness must be a positive number" };
  }
  const energies = [];
  for (let i = 0; i < samples.length; i++) {
    if (!isSample(samples[i])) {
      return { ok: false, missing: `sample ${i} is not [t, position, velocity]` };
    }
    energies.push(sampleEnergy(samples[i], mass, stiffness));
  }
  const mean = energies.reduce((a, b) => a + b, 0) / energies.length;
  if (!(Math.abs(mean) > 0)) {
    // A zero-mean energy would make the relative drift undefined; treat it as a
    // basis the metric cannot be recomputed over rather than dividing by zero.
    return { ok: false, missing: "recomputed mean energy is zero, relative drift is undefined" };
  }
  const maxRelDrift = Math.max(...energies.map((e) => Math.abs(e - mean) / mean));
  return { ok: true, mean, maxRelDrift, energies };
}

// The source digest is the SHA-256 over the embedded source program text. The
// same raw-byte model as the sibling lanes, so it is re-derivable anywhere.
function recomputeSourceDigest(program) {
  return digestBytes(program);
}

// ---------------------------------------------------------------------------
// Assemble a canonical packet from fixture materials. Deterministic: no clock,
// no randomness inside the hash scope. The source digest is recomputed from the
// embedded source program so the fixture never has to hardcode it.
// ---------------------------------------------------------------------------
export function assembleBuildPacket(fixture) {
  if (!fixture) {
    throw new Error("assembleBuildPacket requires a fixture object");
  }
  const receipt = { ...fixture.receipt };
  if (receipt.source_digest === "recompute" && receipt.source_program !== undefined) {
    receipt.source_digest = recomputeSourceDigest(receipt.source_program);
  }
  const base = {
    schema: "project-telos.build-proof-packet/v1",
    packet_id: fixture.packet_id,
    claim: fixture.claim,
    scope: fixture.scope,
    receipt,
    run: fixture.run,
    invariant: fixture.invariant,
    drift: fixture.drift,
    negative_fixture: fixture.negative_fixture,
    boundary_run: fixture.boundary_run
  };
  if (fixture.context_refs) {
    base.context_refs = fixture.context_refs;
  }
  if (fixture.uncertainty) {
    base.uncertainty = fixture.uncertainty;
  }
  const packet = { ...base, packet_hash: packetHash(base) };
  packet.wall_clock = fixture.wall_clock ?? { assembled_at: "unpinned" };
  return packet;
}

// Convenience wrapper mirroring the sibling lanes' {fixture|demo} entry.
export function assembleBuild({ fixture, demo } = {}) {
  if (fixture) return assembleBuildPacket(fixture);
  if (demo) return assembleBuildPacket(demo);
  throw new Error("assembleBuild requires a fixture or demo object");
}

function addFailure(failures, code, verdict, detail) {
  failures.push({ code, verdict, ...detail });
}

// ---------------------------------------------------------------------------
// Pure verifier: packet in, named check results plus a derived verdict out.
// ---------------------------------------------------------------------------
export function verifyBuildPacket(packet, options = {}) {
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

  // check.backend_maturity and check.effect_class -> DRIFT with observed value
  // and allowed set. An honest backend label is a closed vocabulary, so a value
  // outside its set is a state_model_violation, not a silent pass.
  const stateDeltas = [];
  const maturity = packet.receipt?.backend_maturity;
  if (maturity !== undefined && !BACKEND_MATURITY.has(maturity)) {
    stateDeltas.push({
      path: "receipt.backend_maturity",
      observed: maturity,
      allowed: [...BACKEND_MATURITY]
    });
  }
  const effect = packet.receipt?.effect_class;
  if (effect !== undefined && !EFFECT_CLASSES.has(effect)) {
    stateDeltas.push({
      path: "receipt.effect_class",
      observed: effect,
      allowed: [...EFFECT_CLASSES]
    });
  }
  for (const delta of stateDeltas) {
    addFailure(failures, "state_model_violation", "DRIFT", delta);
  }
  checks.push({ name: "check.backend_label", passed: stateDeltas.length === 0 });

  // check.source_digest -> DRIFT recomputing the source digest over the embedded
  // source program. A digest that claims a value but carries no embedded program
  // cannot be recomputed: the digest is a load-bearing claim, so a missing
  // program is an UNVERIFIABLE evidence gap (named above), never a silent pass.
  let sourceDigestOk = true;
  const program = packet.receipt?.source_program;
  const claimedDigest = packet.receipt?.source_digest;
  if (program !== undefined && program !== null && claimedDigest) {
    const recomputed = recomputeSourceDigest(program);
    if (claimedDigest !== recomputed) {
      sourceDigestOk = false;
      addFailure(failures, "source_digest_mismatch", "DRIFT", {
        path: "receipt.source_digest",
        expected: claimedDigest,
        recomputed
      });
    }
  }
  checks.push({ name: "check.source_digest", passed: sourceDigestOk });

  // check.run_samples -> the empty-run floor. A run with no samples recomputes
  // nothing, so it must never reach MATCH: an empty sample series is an
  // UNVERIFIABLE evidence gap (nothing was checked), mirroring the visual lane's
  // empty-measurement floor and the research lane's empty-check floor.
  const mass = packet.run?.constants?.mass;
  const stiffness = packet.run?.constants?.stiffness;
  const samples = packet.run?.samples;
  let runSamplesOk = true;
  if (Array.isArray(samples) && samples.length === 0) {
    runSamplesOk = false;
    addFailure(failures, "no_run_samples", "UNVERIFIABLE", {
      path: "run.samples",
      reason: "the run carries no samples, so nothing was recomputed and no invariant claim is established"
    });
  }
  checks.push({ name: "check.run_samples", passed: runSamplesOk });

  // Recompute the run's energy statistics once; both the invariant and the drift
  // checks read from it. A basis that cannot be recomputed is an UNVERIFIABLE gap.
  const runStats =
    Array.isArray(samples) && samples.length > 0
      ? recomputeEnergyStats(samples, mass, stiffness)
      : { ok: false, missing: "run has no samples" };

  // check.invariant -> the core recompute. The claimed invariant value is
  // recomputed from the embedded samples. A deviation above tolerance is DRIFT
  // carrying the recomputed value. A claim whose method is unknown or whose
  // samples cannot be recomputed is an UNVERIFIABLE gap named by its JSON path,
  // never a silent pass. Trusting a claimed value on faith would let a phantom or
  // tampered invariant reach MATCH with zero failures.
  let invariantOk = true;
  let perInvariant = { metric: packet.invariant?.name ?? "invariant", status: "UNVERIFIABLE" };
  const invMethod = packet.invariant?.method;
  const invValue = packet.invariant?.value;
  const invTolerance = packet.invariant?.tolerance;
  if (structurallyComplete && runSamplesOk) {
    if (!INVARIANT_METHODS.has(invMethod)) {
      invariantOk = false;
      addFailure(failures, "invariant_not_recomputable", "UNVERIFIABLE", {
        path: "invariant.method",
        reason: `unknown invariant method ${invMethod}`
      });
    } else if (!runStats.ok) {
      invariantOk = false;
      addFailure(failures, "invariant_not_recomputable", "UNVERIFIABLE", {
        path: "run.samples",
        reason: `invariant cannot be recomputed: ${runStats.missing}`
      });
    } else if (typeof invTolerance !== "number" || !(invTolerance > 0)) {
      invariantOk = false;
      addFailure(failures, "state_model_violation", "DRIFT", {
        path: "invariant.tolerance",
        observed: invTolerance,
        required: "a positive number"
      });
      perInvariant = { metric: packet.invariant?.name ?? "invariant", status: "DRIFT" };
    } else {
      // The recomputed reference value depends on the method. mean_total_energy
      // is the mean of the energy series; max_relative_energy_drift is the
      // conservation metric.
      const recomputed =
        invMethod === "mean_total_energy" ? runStats.mean : runStats.maxRelDrift;

      // Bound the tolerance to the metric's physical range. An oversized tolerance
      // nullifies the recompute's discriminating power, so a whole-range tolerance
      // could launder a false value into MATCH. mean_total_energy is bounded to a
      // fraction of the recomputed energy scale; the relative drift metric is
      // bounded to a fraction of its [0, 1] range.
      const ceiling =
        invMethod === "mean_total_energy"
          ? Math.abs(runStats.mean) * MEAN_ENERGY_CEILING_FRACTION
          : RELATIVE_DRIFT_CEILING;
      if (invTolerance > ceiling) {
        invariantOk = false;
        addFailure(failures, "tolerance_exceeds_bound", "DRIFT", {
          path: "invariant.tolerance",
          observed: invTolerance,
          ceiling,
          method: invMethod,
          reason:
            "the declared tolerance exceeds the metric's bounded physical range, so it can no longer discriminate a real match"
        });
        perInvariant = { metric: packet.invariant?.name ?? "invariant", status: "DRIFT" };
      } else {
        const deviation = Math.abs(invValue - recomputed);
        if (deviation > invTolerance) {
          invariantOk = false;
          addFailure(failures, "invariant_value_mismatch", "DRIFT", {
            path: "invariant.value",
            metric: packet.invariant?.name ?? "invariant",
            claimed: invValue,
            recomputed,
            deviation,
            tolerance: invTolerance
          });
          perInvariant = {
            metric: packet.invariant?.name ?? "invariant",
            status: "DRIFT",
            deviation,
            recomputed
          };
        } else {
          perInvariant = {
            metric: packet.invariant?.name ?? "invariant",
            status: "MATCH",
            deviation,
            recomputed
          };
        }
      }
    }
  } else if (!structurallyComplete) {
    invariantOk = false;
  }
  checks.push({ name: "check.invariant", passed: invariantOk });

  // check.drift -> the conservation-quality recompute. The claimed conservation
  // drift is recomputed from the embedded samples and must both agree with the
  // recomputed value within the drift tolerance AND stay within the claimed
  // conservation tolerance. A recomputed drift above the claimed tolerance means
  // the run did not conserve the invariant, so the conservation claim fails.
  let driftOk = true;
  const driftMethod = packet.drift?.method;
  const driftValue = packet.drift?.value;
  const driftTolerance = packet.drift?.tolerance;
  if (structurallyComplete && runSamplesOk) {
    if (!DRIFT_METHODS.has(driftMethod)) {
      driftOk = false;
      addFailure(failures, "invariant_not_recomputable", "UNVERIFIABLE", {
        path: "drift.method",
        reason: `unknown drift method ${driftMethod}`
      });
    } else if (!runStats.ok) {
      driftOk = false;
      addFailure(failures, "invariant_not_recomputable", "UNVERIFIABLE", {
        path: "run.samples",
        reason: `drift cannot be recomputed: ${runStats.missing}`
      });
    } else if (typeof driftTolerance !== "number" || !(driftTolerance > 0)) {
      driftOk = false;
      addFailure(failures, "state_model_violation", "DRIFT", {
        path: "drift.tolerance",
        observed: driftTolerance,
        required: "a positive number"
      });
    } else if (driftTolerance > RELATIVE_DRIFT_CEILING) {
      driftOk = false;
      addFailure(failures, "tolerance_exceeds_bound", "DRIFT", {
        path: "drift.tolerance",
        observed: driftTolerance,
        ceiling: RELATIVE_DRIFT_CEILING,
        method: driftMethod,
        reason:
          "the declared drift tolerance exceeds the metric's bounded physical range, so it can no longer discriminate a conserved run from a lossy one"
      });
    } else {
      const recomputedDrift = runStats.maxRelDrift;
      // The claimed drift value must agree with the recomputed drift within the
      // drift tolerance: a tampered drift value is DRIFT.
      const valueDeviation = Math.abs(driftValue - recomputedDrift);
      if (valueDeviation > driftTolerance) {
        driftOk = false;
        addFailure(failures, "invariant_value_mismatch", "DRIFT", {
          path: "drift.value",
          metric: "max_relative_energy_drift",
          claimed: driftValue,
          recomputed: recomputedDrift,
          deviation: valueDeviation,
          tolerance: driftTolerance
        });
      }
      // The recomputed drift must itself stay within the claimed tolerance: a run
      // whose energy drifts beyond tolerance did not conserve the invariant.
      if (recomputedDrift > driftTolerance) {
        driftOk = false;
        addFailure(failures, "drift_exceeds_tolerance", "DRIFT", {
          path: "drift.value",
          recomputed: recomputedDrift,
          tolerance: driftTolerance,
          reason: "the recomputed energy drift exceeds the conservation tolerance, so the run did not conserve the invariant"
        });
      }
    }
  } else if (!structurallyComplete) {
    driftOk = false;
  }
  checks.push({ name: "check.drift", passed: driftOk });

  // check.negative_fixture -> the control the claim must survive. The control run
  // must genuinely break the invariant: its recomputed drift must exceed the
  // claimed conservation tolerance. A control whose recomputed drift stays within
  // tolerance does not break the invariant, so the check has no discriminating
  // power: that is DRIFT (negative_control_conserved), never a silent pass. A
  // control whose samples cannot be recomputed is an UNVERIFIABLE gap.
  let negativeOk = true;
  const neg = packet.negative_fixture;
  if (neg && Array.isArray(neg.samples)) {
    const negTolerance = neg.conservation_tolerance;
    if (typeof negTolerance !== "number" || !(negTolerance > 0)) {
      negativeOk = false;
      addFailure(failures, "state_model_violation", "DRIFT", {
        path: "negative_fixture.conservation_tolerance",
        observed: negTolerance,
        required: "a positive number"
      });
    } else if (!DRIFT_METHODS.has(neg.drift_method)) {
      negativeOk = false;
      addFailure(failures, "invariant_not_recomputable", "UNVERIFIABLE", {
        path: "negative_fixture.drift_method",
        reason: `unknown drift method ${neg.drift_method}`
      });
    } else {
      const negStats = recomputeEnergyStats(neg.samples, mass, stiffness);
      if (!negStats.ok) {
        negativeOk = false;
        addFailure(failures, "invariant_not_recomputable", "UNVERIFIABLE", {
          path: "negative_fixture.samples",
          reason: `negative control cannot be recomputed: ${negStats.missing}`
        });
      } else if (negStats.maxRelDrift <= negTolerance) {
        negativeOk = false;
        addFailure(failures, "negative_control_conserved", "DRIFT", {
          path: "negative_fixture.samples",
          recomputed_drift: negStats.maxRelDrift,
          conservation_tolerance: negTolerance,
          reason:
            "the control run's recomputed energy drift is within the conservation tolerance, so the control does not break the invariant and the check does not discriminate"
        });
      }
    }
  }
  checks.push({ name: "check.negative_fixture", passed: negativeOk });

  // check.packet_hash -> DRIFT with expected and observed. Only runs when the
  // packet is structurally complete; a missing required field is UNVERIFIABLE and
  // must not be masked by a derivative hash mismatch.
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

  // Derive the verdict by one fold. DRIFT dominates UNVERIFIABLE dominates MATCH.
  const hasDrift = failures.some((f) => f.verdict === "DRIFT");
  const hasUnverifiable = failures.some((f) => f.verdict === "UNVERIFIABLE");
  const derivedVerdict = hasDrift ? "DRIFT" : hasUnverifiable ? "UNVERIFIABLE" : "MATCH";

  // check.verdict_derivation: the verdict is derived from the checks alone, so a
  // canned MATCH embedded in the packet can never win. When an embedded verdict
  // disagrees with the derived one, that disagreement is itself a failure at the
  // derived severity, so an embedded MATCH over tampered materials stays DRIFT and
  // an embedded MATCH over an incomplete packet stays UNVERIFIABLE.
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
    per_invariant: perInvariant,
    verdict: finalVerdict
  };
}

// ---------------------------------------------------------------------------
// Export to the proof-surface conservation-proof-packet/v0 shape. The verdict is
// re-derived from the packet's own materials, never copied from an embedded
// verifier block. decision_summary is derived from the overall verdict.
// proof-surface is never imported here; the field list is frozen as a test
// fixture instead.
// ---------------------------------------------------------------------------

// Strip the sha256: prefix; proof-surface source sha256 is bare 64-hex.
function bare(digest) {
  if (typeof digest !== "string") return null;
  const stripped = digest.replace(/^sha256:/, "");
  return /^[0-9a-f]{64}$/.test(stripped) ? stripped : null;
}

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

// telos build failure codes -> proof-surface FAILURE_CODES (closed set in
// _failure.py at proof-surface HEAD). Any unmapped code falls back to
// verification_unverifiable so no failure leaves the export unlabeled.
const FAILURE_LABEL_MAP = {
  missing_required_field: "evidence_gap",
  no_run_samples: "evidence_gap",
  invariant_not_recomputable: "evidence_gap",
  source_digest_mismatch: "binding_failed",
  invariant_value_mismatch: "binding_failed",
  drift_exceeds_tolerance: "binding_failed",
  packet_hash_mismatch: "binding_failed",
  state_model_violation: "binding_failed",
  tolerance_exceeds_bound: "binding_failed",
  negative_control_conserved: "verification_unverifiable",
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

// Recompute the drift over a sample series for the export, so the exported
// witnesses and negative fixture carry a re-derived drift, not a copied one.
function recomputedDriftFor(samples, mass, stiffness) {
  const stats = recomputeEnergyStats(samples, mass, stiffness);
  return stats.ok ? stats.maxRelDrift : null;
}

// Build the disclosed-limits list. The finite-run, fixture-receipt, and
// no-re-execution boundaries are named so nothing is silently dropped.
function buildUncertainty(packet) {
  const declared = Array.isArray(packet.uncertainty) ? [...packet.uncertainty] : [];
  const notes = [...declared];
  notes.push(
    "the invariant is recomputed from the run's embedded samples, not re-executed from the buildc toolchain"
  );
  notes.push(
    "the backend label is a fixture-declared claim about the buildc receipt, not a live backend re-run"
  );
  return notes;
}

export function toProofSurfaceBuildPacket(packet) {
  const embedded = packet.verifier?.verdict;
  const verification = verifyBuildPacket(packet, { embeddedVerdict: embedded });
  const verdict = verification.verdict;
  const failureLabels = mapFailureLabels(verification.failures);

  const mass = packet.run?.constants?.mass;
  const stiffness = packet.run?.constants?.stiffness;

  // sources: the buildc receipt ref and its bare-hex source digest.
  const sources = [
    {
      ref: `buildc:receipt/${packet.receipt?.source_id ?? "source"}`,
      sha256: bare(packet.receipt?.source_digest)
    }
  ];

  // transformation: the numerical run with an honest backend label and domain.
  const transformation = {
    description: `numerical run of the buildc-compiled routine over the ${packet.receipt?.backend_label ?? "unlabeled backend"} (${packet.receipt?.backend_maturity ?? "unlabeled"} maturity), ${
      Array.isArray(packet.run?.samples) ? packet.run.samples.length : 0
    } samples`,
    domain: "scientific-compute"
  };

  const invariant = {
    name: packet.invariant?.name,
    declared: typeof packet.invariant?.declared === "string" ? packet.invariant.declared : null
  };

  // witnesses: one numeric witness per recompute method, each carrying the
  // recomputed drift and a positive tolerance. The claimed-value witness carries
  // the recomputed absolute deviation from the claimed invariant value; the
  // conservation witness carries the recomputed relative energy drift. Both are
  // re-derived from the embedded samples so they are never copied on faith.
  const runStats = recomputeEnergyStats(packet.run?.samples, mass, stiffness);
  const valueDrift =
    runStats.ok && typeof packet.invariant?.value === "number"
      ? Math.abs(packet.invariant.value - runStats.mean)
      : 0;
  const conservationDrift = runStats.ok ? runStats.maxRelDrift : 0;
  const witnesses = [
    {
      kind: "numeric",
      method: "recomputed absolute deviation of the claimed mean energy from the embedded-sample mean",
      drift: valueDrift,
      tolerance: typeof packet.invariant?.tolerance === "number" && packet.invariant.tolerance > 0
        ? packet.invariant.tolerance
        : 1
    },
    {
      kind: "numeric",
      method: "recomputed maximum relative energy drift over the embedded samples",
      drift: conservationDrift,
      tolerance: typeof packet.drift?.tolerance === "number" && packet.drift.tolerance > 0
        ? packet.drift.tolerance
        : 1
    }
  ];

  // negative_fixture: the control run, carrying its recomputed drift and the
  // conservation tolerance. breaks_invariant is true only when the recomputed
  // drift exceeds the tolerance, and proof-surface additionally requires the
  // drift to exceed tolerance, so the two agree by construction.
  const neg = packet.negative_fixture ?? {};
  const negDrift = recomputedDriftFor(neg.samples, mass, stiffness);
  const negTolerance =
    typeof neg.conservation_tolerance === "number" && neg.conservation_tolerance > 0
      ? neg.conservation_tolerance
      : 1;
  const negBreaks = negDrift !== null && negDrift > negTolerance;
  const negativeFixture = {
    description: neg.description ?? "control run",
    drift: negDrift !== null ? negDrift : 0,
    tolerance: negTolerance,
    breaks_invariant: negBreaks
  };

  // boundary_fixture: the boundary run shows the conservation goal HOLDING while
  // the specific claimed value FAILS. goal_holds is true when the boundary run is
  // itself conserved within the drift tolerance; condition_holds is false because
  // its mean energy differs from the happy-path claimed value.
  const bnd = packet.boundary_run;
  let boundaryFixture = null;
  if (bnd && Array.isArray(bnd.samples)) {
    const bndStats = recomputeEnergyStats(bnd.samples, mass, stiffness);
    const driftTol =
      typeof packet.drift?.tolerance === "number" && packet.drift.tolerance > 0
        ? packet.drift.tolerance
        : RELATIVE_DRIFT_CEILING;
    const goalHolds = bndStats.ok && bndStats.maxRelDrift <= driftTol;
    const claimedValue = packet.invariant?.value;
    const invTol =
      typeof packet.invariant?.tolerance === "number" && packet.invariant.tolerance > 0
        ? packet.invariant.tolerance
        : 0;
    const conditionHolds =
      bndStats.ok && typeof claimedValue === "number"
        ? Math.abs(bndStats.mean - claimedValue) <= invTol
        : false;
    boundaryFixture = {
      description: bnd.description ?? "boundary run",
      goal_holds: goalHolds,
      condition_holds: conditionHolds
    };
  }

  const exported = {
    version: "conservation-proof-packet/v0",
    packet_id: packet.packet_id,
    claim: packet.claim,
    scope: packet.scope,
    sources,
    transformation,
    invariant,
    witnesses,
    negative_fixture: negativeFixture,
    boundary_fixture: boundaryFixture,
    failure_labels: failureLabels,
    verdicts: { overall: verdict },
    uncertainty: buildUncertainty(packet),
    decision_summary: deriveDecisionSummary(
      verdict,
      verdict === "UNVERIFIABLE" ? buildUncertainty(packet) : []
    )
  };
  return exported;
}
