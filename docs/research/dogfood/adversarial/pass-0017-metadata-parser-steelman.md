# Pass 0017 Metadata Parser Steelman

Status: LOCAL_STEELMAN_WITH_FORUM_SUBMIT_GAP
Date: 2026-07-01

Forum ledger status and verification were available, but the submit path returned
the known executor JSON parse error. This is a local adversarial review.

## Review Target

- `schemas/cloud-quantum-metadata-parsers-pass-0017.json`
- `schemas/pass-0017-metadata-parser-validator-result.json`
- `packets/027-cloud-quantum-metadata-parser-hardening.md`
- `schemas/tool-receipts-pass-0017.json`

## Objection 1 - Sample Metadata Is Not Live Metadata

The pass uses synthetic sample payloads. It does not call Braket `GetDevice`,
IBM backend properties, or Azure target list in a live account.

Assessment: valid objection.

Countermeasure: keep the pass non-promotional and add live adapter receipts only
after credentials, budget, and provider access are intentionally allocated.

## Objection 2 - Provider Schemas Drift

Provider API fields can change. A hardcoded parser profile may pass local fixtures
while failing live payloads.

Assessment: valid objection.

Countermeasure: store raw provider payload hashes, parser version hashes, source
anchors, and unavailable-field verdicts. Add schema-version and unknown-field
policies in the next provider-adapter pass.

## Objection 3 - Hardware Eligibility Needs Paired Metadata

IBM backend properties alone do not prove simulator=false; the profile explicitly
needs paired backend metadata. Azure target kind also needs provider-specific
target semantics, not just a sample `target_profile`.

Assessment: valid objection.

Countermeasure: treat absent target-kind evidence as rejection for hardware
claims. Add paired backend/target metadata fixtures before any hardware claim.

## Objection 4 - Bitstring Receipts Need Cross-Framework Coverage

The register-layout receipt uses Qiskit-style bit ordering. Other frameworks,
providers, and result formats may use different conventions or expose memory slots,
classical registers, readout maps, or endian semantics differently.

Assessment: valid objection.

Countermeasure: add Qiskit, Braket, Cirq, PennyLane, and QIR layout adapters
separately. Reject normalized cross-provider counts unless a layout adapter is
declared.

## Objection 5 - Duplicate Keys And Floating-Point Policy Are Only Listed

The negative fixtures identify duplicate JSON keys and floating-point precision as
risks, but they do not yet implement strict parser behavior for them.

Assessment: valid objection.

Countermeasure: add executable duplicate-key detection and float-precision policy
fixtures in the next canonicalization hardening pass.

## Objection 6 - Post-Processing Baseline Is Too Simple

The baseline receipt covers no mitigation, no filtering, and no truncation. Real
provider and client workflows may include readout mitigation, marginalization,
shot filtering, rescaling, register selection, and result merging.

Assessment: valid objection.

Countermeasure: make `QuantumPostProcessingReceipt/v1` operation-specific, with
operation ids, input hashes, output hashes, parameters, and proof that operations
are deterministic or explicitly stochastic.

## Verdict

Pass 0017 should remain non-promotional. It is a useful parser and interpretation
receipt design, but it does not prove live provider retrieval, hardware execution,
quantum advantage, or a new scientific result.

Recommended next pass: implement strict duplicate-key detection, binary/object
storage payload profiles, float precision policy, and cross-framework register
layout adapters.
