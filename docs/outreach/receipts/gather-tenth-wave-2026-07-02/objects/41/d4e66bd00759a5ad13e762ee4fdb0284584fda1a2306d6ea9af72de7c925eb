# Pass 0016 Canonicalization Steelman

Status: LOCAL_STEELMAN_WITH_FORUM_SUBMIT_GAP
Date: 2026-07-01

Forum ledger status and verification were available, but the Forum submit path
returned an executor JSON parse error. This packet records a local adversarial
review until that tool path can be repaired.

## Review Target

Artifacts reviewed:

- `schemas/cloud-quantum-canonicalization-pass-0016.json`
- `schemas/pass-0016-cloud-quantum-canonicalization-validator-result.json`
- `packets/026-cloud-quantum-result-canonicalization.md`
- `schemas/tool-receipts-pass-0016.json`

## Objection 1 - Canonical JSON Is Not Enough

Canonical JSON protects a subset of result payloads. Cloud providers may return
binary artifacts, compressed outputs, links to object storage, timestamps,
floating-point values, NaN-like strings, histograms, arrays with semantic ordering,
or provider-specific metadata.

Assessment: valid objection.

Countermeasure:

- Keep `raw_payload_hash` mandatory.
- Keep `canonicalization_policy_hash` mandatory.
- Label every transformation with a lossiness term.
- Add future fixtures for binary payloads, arrays, floating-point precision,
  duplicate JSON keys, and object-storage references.

## Objection 2 - Normalized Counts Can Hide Provider Context

Normalizing result counts into a common `{bitstring: count}` map can hide result
type, endian convention, classical register layout, readout mitigation, simulator
mode, and post-processing assumptions.

Assessment: valid objection.

Countermeasure:

- Treat normalized counts as a comparison aid, not a forensic receipt.
- Require raw payload retention.
- Add a `register_layout_receipt` and `post_processing_receipt` in a later pass.
- Reject normalized-only claims for provenance.

## Objection 3 - Calibration References Are Not Calibration Evidence

The pass defines calibration-reference profiles, but does not fetch live provider
properties, device characteristics, backend calibration timestamps, or target
metadata.

Assessment: valid objection.

Countermeasure:

- Mark pass 0016 as profile-only.
- Require `retrieval_timestamp` and payload hash in the profile.
- Mark calibration-dependent claims `UNVERIFIABLE` when metadata is unavailable.
- Add provider adapter fixtures only after live retrieval is implemented.

## Objection 4 - Backend Kind Rules Need Provider-Specific Parsers

The current backend-kind mapping is a policy scaffold. It is not yet an executable
adapter for Braket, IBM Runtime, or Azure target metadata.

Assessment: valid objection.

Countermeasure:

- Add parser-specific validators for `GetDevice`, IBM backend properties, and
  Azure target metadata.
- Treat missing backend-kind evidence as a rejection for hardware claims.
- Keep simulator and QPU branches separate in all downstream packets.

## Objection 5 - Resource Estimates Are Tempting To Overpromote

Azure-style resource estimates can sound like execution evidence because they
return concrete numbers such as physical qubits and runtime.

Assessment: valid objection.

Countermeasure:

- `CloudQuantumResourceEstimateReceiptProfile/v1` sets
  `execution_claim_allowed=false` and `hardware_claim_allowed=false`.
- Estimator receipts must state model assumptions and uncertainty.
- Estimator receipts cannot satisfy cloud task receipt requirements.

## Objection 6 - No Market Proof Yet

This pass improves receipt mechanics, but does not prove buyer demand or
differentiation in the quantum tooling market.

Assessment: valid objection.

Countermeasure:

- Feed this profile into the market matrix as a proof-layer feature.
- Compare against quantum cloud provider dashboards, PennyLane, Qiskit, Cirq,
  cloud resource estimators, and workflow tooling in a future market pass.
- Show a public demo with one simulator-only packet first, then a live cloud
  hardware packet when credentials and budget are intentionally allocated.

## Verdict

Pass 0016 should remain non-promotional. It is a useful receipt-profile hardening
step, not evidence of a cloud quantum run, a hardware result, quantum advantage, a
theorem proof, or a natural law.

Recommended next pass: implement parser-level profile fixtures for provider
metadata and add duplicate-key, binary-payload, floating-point, and register-layout
negative fixtures.
