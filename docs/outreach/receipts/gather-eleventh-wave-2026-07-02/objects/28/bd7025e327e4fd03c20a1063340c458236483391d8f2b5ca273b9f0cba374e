# Pass 0018 Strict Adapter Steelman

Status: LOCAL_STEELMAN_WITH_FORUM_SUBMIT_GAP
Date: 2026-07-01

Forum ledger status and verification were available, but the submit path returned
the known executor JSON parse error. This is a local adversarial review.

## Review Target

- `schemas/quantum-strict-canonicalization-adapters-pass-0018.json`
- `schemas/pass-0018-strict-canonicalization-adapter-validator-result.json`
- `packets/028-quantum-strict-canonicalization-adapters.md`
- `schemas/tool-receipts-pass-0018.json`

## Objection 1 - Adapter Profiles Are Not Executable Parsers

The adapters are receipt profiles, not executable framework parsers. They cannot
yet prove that Qiskit, Braket, Cirq, PennyLane, or QIR results are interpreted
correctly on live outputs.

Assessment: valid objection.

Countermeasure: implement executable adapter tests with real framework output
fixtures and reject claims when adapter version and parser hash are absent.

## Objection 2 - Framework Semantics Are Contextual

Bit order can depend on measurement keys, qubit order, wire order, register maps,
fold functions, result helpers, and output formats. A one-line policy is not a
complete semantics model.

Assessment: valid objection.

Countermeasure: require adapter-specific receipt fields and bind them to raw
result hashes. Treat missing fields as rejection, not warning.

## Objection 3 - Duplicate-Key Detection Needs Real Parser Hooks

The pass records a duplicate-key fixture and validator expectation, but it does
not yet enforce duplicate detection across every JSON ingestion path.

Assessment: valid objection.

Countermeasure: add a shared strict JSON loader used by every proof-packet parser.

## Objection 4 - Floating-Point Policy Needs Type-Level Enforcement

The pass requires a precision policy, but it does not yet enforce decimal-string,
IEEE double, interval, arbitrary precision, or unit-specific constraints at the
schema level.

Assessment: valid objection.

Countermeasure: introduce `NumericPrecisionReceipt/v1` with numeric class, source
precision, rounding mode, unit, tolerance, and output representation.

## Objection 5 - Object Storage Requires Retrieval Receipts

A content hash helps, but object storage evidence also needs retrieval command,
provider, bucket/container, version/generation, permissions context, timestamp,
and optional signature.

Assessment: valid objection.

Countermeasure: define `ObjectStorageEvidenceReceipt/v1` with locator, immutable
content hash, version/generation, retrieval timestamp, and access boundary.

## Verdict

Pass 0018 should remain non-promotional. It hardens policy and adapter shape, but
does not execute real framework adapter tests, run a cloud quantum job, or prove a
hardware result.

Recommended next pass: implement strict JSON loader fixtures, numeric precision
receipts, object-storage evidence receipts, and one executable framework output
fixture per adapter.
