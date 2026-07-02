# Thirtieth Wave: Quantum Error-Correction Preflight

Date: 2026-07-02
Verdict: `QEC_STABILIZER_FIXTURE_MATCH`

## What Changed

This pass promotes the quantum-computing lane into a replayable local preflight.
It does not claim surface-code decoding, hardware-level quantum error
correction, fault-tolerant computation, quantum advantage, cryptographic
security, or BuildLang/buildc-native quantum execution. It proves only that
Project Telos can carry a bounded QEC claim with source receipts, a declared
code, supported error model, stabilizers, syndrome table, correction table,
logical recovery checks, and negative controls.

The concrete artifact is a deterministic 3-qubit bit-flip repetition-code
fixture. It corrects no-error and single Pauli-X errors for logical `0` and
logical `1`. It rejects or marks unverifiable: double-X error, phase error,
missing stabilizer measurement, wrong syndrome map, and non-codeword input.

## Captured Source Leads

The source ledger stays metadata-only:

- `2605.17156v2`: Sparse Mamba decoder for surface-code syndromes.
- `2512.07737v2`: real-time neural decoder for topological quantum codes.
- `2207.05942v2`: syndrome decoding by quantum approximate optimization.
- `2102.01984v1`: belief propagation for data-syndrome codes.
- `2409.01440v3`: almost-linear decoder for quantum LDPC codes.
- `quant-ph/0602157v1`: error-correcting code foundations.
- `1810.01029v1`: 3-qubit quantum error-correction simulation.
- `2412.07841v3`: atom-loss resilient QEC.
- `2605.19854v1`: superconducting cat-qubit computation.
- `1509.02004v2`: fault-tolerant high-level quantum circuits.
- `1908.03903v3`: quantum algorithm verification source lead.
- `2602.11092v2`: photonic and hybrid quantum machine learning discovery.

These rows are source leads and requirements pressure, not proof that the local
fixture solves surface-code decoding, hardware QEC, or fault-tolerant quantum
computation.

## Receipts

- Source ledger:
  `demo/research/quantum-error-correction-source-receipts.json`
- Fixture CLI:
  `demo/quantum-error-correction-proof-packet.mjs`
- Fixture test:
  `demo/quantum-error-correction-proof-packet.test.mjs`
- Fixture output:
  `docs/outreach/receipts/thirtieth-wave/quantum-error-correction-proof-packet-2026-07-02.json`
- Crucible thesis:
  `docs/outreach/receipts/thirtieth-wave-quantum-error-correction-thesis-2026-07-02.json`
- Crucible measurements:
  `docs/outreach/receipts/thirtieth-wave-quantum-error-correction-measurements-2026-07-02.json`
- Crucible run:
  `docs/outreach/receipts/thirtieth-wave-quantum-error-correction-run-2026-07-02.json`
- Crucible report:
  `docs/outreach/receipts/thirtieth-wave-quantum-error-correction-report-2026-07-02.md`
- Learn packet:
  `docs/outreach/receipts/thirtieth-wave/quantum-error-correction.learn-packet.json`
- Learn prooflesson:
  `docs/outreach/receipts/thirtieth-wave/learn-quantum-error-correction/tutor/thirtieth-wave-quantum-error-correction.prooflesson.json`
- Learn reverify witness SHA-256:
  `3093cea9b0746b052dba844a6745cdba1d11ae836be5468503af41f93c4702f3`

## Claim Boundary

Allowed:

- "The local fixture emits `QEC_STABILIZER_FIXTURE_MATCH`."
- "The fixture corrects no-error and single Pauli-X errors for both logical
  basis states."
- "The five configured negative controls are rejected or marked
  `UNVERIFIABLE`."
- "The source ledger records arXiv metadata rows and digest seals as source
  leads."

Blocked:

- "Project Telos implemented a surface-code decoder."
- "Project Telos proved hardware-level quantum error correction."
- "Project Telos established fault-tolerant quantum computation."
- "Project Telos validated quantum advantage or resource estimates."
- "The fixture already runs natively through BuildLang/buildc."

## Megatool Integration

The QEC proof packet connects the existing megatool stack:

1. Gather captures QEC, decoder, compiler, hardware, and resource-estimation
   source receipts.
2. Index packages circuit specs, code distance, stabilizers, logical operators,
   decoder configs, and source refs.
3. Forum routes claims through physics, formal methods, compiler, hardware, and
   verification lanes.
4. Crucible rejects quantum claims without supported error model, code distance,
   syndrome table, decoder verdicts, and negative controls.
5. Learn turns passing and failing packets into lessons about stabilizers,
   syndromes, logical errors, unsupported error models, and overclaim
   boundaries.
6. BuildLang/buildc becomes the typed runtime for Pauli operators, stabilizer
   groups, circuits, syndromes, decoders, and resource estimates.
7. Telos binds sources, circuit/state specs, decoder outputs, verification
   verdicts, and learning receipts into one packet.

## Next Tooling Target

The next iteration should promote one of these fixtures:

- A BuildLang/buildc typed Pauli/stabilizer runtime for the same 3-qubit code.
- A small surface-code syndrome fixture with declared lattice, defects, and
  decoder table.
- A Clifford-circuit equivalence checker over a tiny gate set.
- A resource-estimation packet that refuses advantage claims without classical
  baseline and hardware assumptions.

The strongest public demo is the BuildLang/buildc Pauli/stabilizer replay
because it turns the language/runtime ambition into typed quantum primitives
without overclaiming hardware QEC.

## Tool Results

Crucible returned `MATCH 3 / DRIFT 0 / UNVERIFIABLE 0` for the bounded QEC
preflight claims. Learn generated and reverified the prooflesson as `VERIFIED`,
with witnessed SHA-256
`3093cea9b0746b052dba844a6745cdba1d11ae836be5468503af41f93c4702f3`.
