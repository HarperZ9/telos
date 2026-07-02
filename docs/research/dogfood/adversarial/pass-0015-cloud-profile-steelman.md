# Pass 0015 Cloud Profile Steelman

Date: 2026-07-01

Status: `UNVERIFIABLE` for Forum submit; `MATCH` for local adversarial analysis.

## Forum Tool Receipt

Forum status and ledger verification are reachable:

```json
{
  "status": {
    "entries": 6,
    "checkpoint": "253900c51d9c6444119aac10be5730f2d00bfc13894c5bec9ebde8e2634b9c6b"
  },
  "verify": {
    "chain": true,
    "deep": true
  }
}
```

Forum submit still fails:

```json
{
  "error": "the configured executor did not return valid JSON; point the daemon at a real model executor (could not parse JSON from output: Extra data: line 2 column 1 (char 98))"
}
```

This pass does not claim a witnessed Forum adversarial answer.

## Steelman Objections

### Objection 1: Calibration References Are Provider-Specific

The profile currently requires calibration or device/backend/target properties references, but each provider exposes this differently. A generic string field can become a compliance checkbox rather than a real link to device state.

Required hardening:

- define provider-specific calibration reference types;
- include retrieval timestamp;
- include hash of the properties payload when available;
- mark calibration unavailable as `UNVERIFIABLE`, not `MATCH`.

### Objection 2: Payload Hashes Need Canonicalization

The profile requires a result payload hash, but provider result objects may include nondeterministic ordering, metadata, timestamps, or SDK-specific wrappers.

Required hardening:

- define canonical JSON serialization for result payloads;
- hash raw provider payload and normalized result separately;
- record normalization lossiness.

### Objection 3: Simulator Identity Is Still Easy To Hide

Cloud providers expose both QPUs and simulators. A provider cloud job id alone does not prove QPU hardware.

Required hardening:

- require `device_kind` or equivalent backend kind;
- require simulator/QPU branch mapping;
- reject hardware claims when backend kind is simulator, even if provider is cloud.

### Objection 4: Azure Resource Estimator Needs A Separate Profile Family

Azure Quantum includes resource estimation as a valuable workflow, but it is structurally different from execution jobs. The current pass includes a separation rule; the next pass should create a first-class `CloudQuantumResourceEstimateReceiptProfile/v1`.

Required hardening:

- define resource-estimator fields separately;
- include physical/logical estimate outputs and assumptions;
- explicitly prohibit execution and hardware-result claims from estimate-only receipts.

### Objection 5: Sample Receipts Could Be Mistaken For Executed Receipts

The sample receipts are shape-only, but they use realistic-looking provider fields. Future reports must render the shape-only status visibly.

Required hardening:

- report sample receipts under a separate "fixture" heading;
- keep `hardware_claim_allowed=false`;
- reject any sample receipt with `SHAPE_ONLY_NOT_EXECUTED` when cited as evidence.

## Verdict

Pass 0015 is a useful provider-profile layer, but production readiness requires provider-specific canonicalizers, calibration payload references, simulator/QPU backend mapping, and a separate Azure resource-estimator profile family.

