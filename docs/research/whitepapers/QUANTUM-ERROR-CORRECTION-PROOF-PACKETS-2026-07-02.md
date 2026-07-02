# Quantum Error-Correction Proof Packets

Author: Zain Dana Harper
Date: 2026-07-02
Status: working paper, not archive-submitted

## Abstract

Quantum-computing claims are difficult to trust without explicit error models,
code definitions, circuit specifications, decoder outputs, resource estimates,
and negative controls. This working paper proposes Project Telos proof-carrying
quantum-computing packets. The current contribution is intentionally small: a
deterministic 3-qubit bit-flip stabilizer fixture that emits
`QEC_STABILIZER_FIXTURE_MATCH` when no-error and single Pauli-X errors are
corrected for both logical basis states, and when double-error, phase-error,
missing-syndrome, wrong-map, and non-codeword controls are rejected or marked
unverifiable. The fixture is not a surface-code decoder, hardware QEC result,
fault-tolerant computation result, quantum-advantage result, or
BuildLang/buildc-native result. It is a preflight contract for what stronger
quantum claims must contain before public promotion.

## Problem

Quantum claims collapse many hidden assumptions: Hilbert space, gate set, error
model, noise model, code distance, syndrome extraction, decoder, logical
operator, resource estimate, hardware assumption, and classical baseline. A
model or paper summary can sound correct while silently omitting the assumption
that makes the result meaningful.

Project Telos should treat quantum research like other high-stakes research:
source receipts first, typed artifacts second, verifier gates third, and public
claims only after replay.

## Source Intake Boundary

The source ledger for this pass is
`demo/research/quantum-error-correction-source-receipts.json`. It contains arXiv
metadata rows and Gather digest seals from searches over QEC, surface-code
decoders, data-syndrome decoding, fault-tolerant compilation, quantum algorithm
verification, and resource-estimation-adjacent work.

The ledger is not a full-paper corpus. It stores source leads and requirements
pressure. It does not promote paper claims, reproduce external experiments, or
quote full text.

## Fixture

The local fixture is implemented in
`demo/quantum-error-correction-proof-packet.mjs`. It defines:

- logical states `000` and `111`,
- stabilizers `Z0Z1` and `Z1Z2`,
- syndrome bits `q0_xor_q1` and `q1_xor_q2`,
- a correction table for no-error and single-X errors, and
- unsupported error models.

The expected result is:

```json
{
  "result": "QEC_STABILIZER_FIXTURE_MATCH",
  "claim_card": {
    "verdict": "MATCH"
  }
}
```

## Negative Controls

The preflight rejects or marks unverifiable:

- double-X error, because it exceeds the fixture code distance,
- phase error, because the bit-flip fixture does not measure phase syndrome,
- missing stabilizer measurement,
- wrong syndrome map for the middle qubit, and
- non-codeword input.

These controls matter because quantum proof packets must fail visibly. A packet
that accepts an unsupported error model or hidden syndrome omission should not
be allowed to support any quantum-computing claim.

## Product Shape

The QEC workbench should be a megatool formed by existing Telos flagships:

| Layer | Responsibility |
| --- | --- |
| Gather | Capture QEC, decoder, compiler, hardware, benchmark, and resource-estimation source receipts. |
| Index | Package circuit specs, stabilizer tables, code distance, logical operators, decoder configs, and source refs. |
| Forum | Route claims through physics, formal methods, compiler, hardware, and verification lanes. |
| Crucible | Turn falsifiable quantum claims plus measurements into `MATCH`, `DRIFT`, or `UNVERIFIABLE`. |
| Learn | Convert packets and failures into exercises about stabilizers, syndromes, logical errors, unsupported error models, and overclaim boundaries. |
| BuildLang/buildc | Provide typed Pauli operators, stabilizer groups, circuit IR, decoders, and resource-estimation receipts. |
| Telos | Bind source, circuit/code state, decoder output, verdict, and learning receipts into one packet. |

This should become a family of products:

- QEC Claim Preflight for papers and research notes.
- Decoder Benchmark Card Auditor for neural, LDPC, and surface-code decoders.
- Fault-Tolerant Compiler Receipt for circuit rewrites and resource estimates.
- Quantum Advantage Non-Claim Gate for baseline and hardware assumptions.
- BuildLang Quantum Runtime for typed Pauli/stabilizer/circuit artifacts.

## Public Demo Recommendation

The top public demo should be:

1. A BuildLang/buildc typed Pauli/stabilizer runtime for this 3-qubit fixture.
2. A tiny surface-code syndrome fixture with declared lattice and decoder table.
3. A Clifford-circuit equivalence checker over a tiny gate set.
4. A resource-estimation packet that refuses quantum-advantage language without
   task definition, classical baseline, hardware assumptions, and verifier
   receipts.

The wedge is not another quantum simulator. The wedge is claim accountability:
source to code to error model to syndrome to decoder to verdict to lesson.

## Claim Boundary

This paper claims:

- Project Telos has a replayable QEC stabilizer-code preflight fixture.
- The preflight can carry code definitions, supported error model, syndrome
  table, correction table, negative controls, and non-claims.
- The workbench architecture is a plausible next product shape for
  proof-carrying quantum-computing research.

This paper does not claim:

- surface-code decoding,
- hardware-level QEC,
- fault-tolerant quantum computing,
- quantum advantage,
- cryptographic security,
- full paper digestion,
- BuildLang/buildc-native quantum runtime, or
- deployment readiness.
