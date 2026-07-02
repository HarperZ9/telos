# Quantum Error-Correction Proof Packets

Official local copy for publication packaging.
Author: Zain Dana Harper
Date: 2026-07-02
Status: working draft, not archive-submitted

## Official Status

`QEC_STABILIZER_FIXTURE_MATCH` applies to the deterministic local 3-qubit
bit-flip stabilizer fixture.

`SOURCE_LEAD` applies to the arXiv metadata rows in the source ledger.

`HYPOTHESIS` applies to the larger quantum-computing, QEC decoder,
fault-tolerant compiler, and resource-estimation product opportunity.

`NOT_REPLAYED` applies to surface-code decoding, hardware QEC, quantum
advantage, cryptography, fault-tolerant computation, and BuildLang/buildc-native
execution.

## Publishable Claim

Project Telos now has a replayable QEC preflight that binds:

- source-ledger receipts,
- a declared stabilizer code,
- supported and unsupported error models,
- syndrome table,
- correction table,
- logical recovery checks,
- negative controls,
- Crucible measurement receipts, and
- Learn prooflesson export.

The fixture proves only the local contract. It is not a hardware or surface-code
result.

## Verified Artifacts

- Source ledger:
  `demo/research/quantum-error-correction-source-receipts.json`
- Fixture CLI:
  `demo/quantum-error-correction-proof-packet.mjs`
- Fixture test:
  `demo/quantum-error-correction-proof-packet.test.mjs`
- Fixture output:
  `docs/outreach/receipts/thirtieth-wave/quantum-error-correction-proof-packet-2026-07-02.json`
- Outreach note:
  `docs/outreach/THIRTIETH-WAVE-QUANTUM-ERROR-CORRECTION-PREFLIGHT-2026-07-02.md`
- Working paper:
  `docs/research/whitepapers/QUANTUM-ERROR-CORRECTION-PROOF-PACKETS-2026-07-02.md`
- Crucible run:
  `docs/outreach/receipts/thirtieth-wave-quantum-error-correction-run-2026-07-02.json`
- Crucible run SHA-256:
  `3d46985ec81ed6330bd38ee87f05a93814503dca286a74d2718ce02e24cca438`
- Crucible report:
  `docs/outreach/receipts/thirtieth-wave-quantum-error-correction-report-2026-07-02.md`
- Crucible report SHA-256:
  `1612e3007d41bde5f106aa2b4c99156ad0af131abf10a362315040080ee01872`
- Learn packet:
  `docs/outreach/receipts/thirtieth-wave/quantum-error-correction.learn-packet.json`
- Learn packet SHA-256:
  `09dcf1fd9ff2614cf6495fdefbe568fa9c8f0de92f8fd9ca3db43aa2a19b7170`
- Learn prooflesson receipt:
  `docs/outreach/receipts/thirtieth-wave/learn-quantum-error-correction/tutor/thirtieth-wave-quantum-error-correction.prooflesson.json`
- Learn prooflesson SHA-256:
  `201afea6e463bd0fb035a5afa591858e99ef3de5db7e32b37a6e13fe43fd1000`
- Learn reverify witness SHA-256:
  `3093cea9b0746b052dba844a6745cdba1d11ae836be5468503af41f93c4702f3`

## Fixture Result

The local fixture declares:

- Code: `three_qubit_bit_flip_repetition_code`
- Logical zero: `000`
- Logical one: `111`
- Stabilizers: `Z0Z1`, `Z1Z2`
- Syndrome bits: `q0_xor_q1`, `q1_xor_q2`
- Supported error model: one Pauli-X bit flip on at most one physical qubit

The replayed nominal result is:

`QEC_STABILIZER_FIXTURE_MATCH`

The following negative controls are rejected or marked `UNVERIFIABLE`:

- double-bit flip aliasing to a logical error,
- phase error outside the bit-flip code,
- missing stabilizer measurement,
- wrong syndrome map, and
- non-codeword input.

## Publication Boundary

The publication can say:

> Project Telos turned a quantum-computing source-intake lane into a replayable
> QEC preflight. The preflight demonstrates how a proof packet can carry a
> stabilizer code, supported error model, syndrome table, correction table,
> logical recovery checks, negative controls, and verification receipts before a
> quantum claim is promoted.

The publication must also say:

> This is a deterministic local fixture. It does not implement a surface-code
> decoder, prove hardware quantum error correction, establish fault-tolerant
> quantum computation, validate quantum advantage, or prove BuildLang/buildc
> quantum-runtime execution.

## Promotion Checklist

- [x] Source ledger is metadata-only.
- [x] Fixture declares code, logical states, stabilizers, syndrome bits, and
  correction map.
- [x] Fixture declares supported and unsupported error models.
- [x] Fixture checks no-error and single-X recovery for both logical basis
  states.
- [x] Fixture rejects or marks unverifiable five negative controls.
- [x] Local test replays the fixture.
- [x] Crucible run and report hashes patched after final run.
- [x] Learn packet and prooflesson hashes patched after final run.
- [ ] BuildLang/buildc typed Pauli/stabilizer version exists.
- [ ] Surface-code toy fixture exists.
- [ ] Clifford-circuit equivalence fixture exists.
- [ ] Resource-estimation non-claim gate exists.

## Next Submission Gate

Do not submit this as a quantum hardware or surface-code result. The stronger
next paper should be a methods paper: proof-carrying quantum-computing claims
with typed Pauli/stabilizer runtime, circuit equivalence checks, decoder
receipts, negative controls, and resource-estimation boundaries.
