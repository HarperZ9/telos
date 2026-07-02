# Embodied Sim-to-Real Proof Packets for Robotics

Official local copy for publication packaging.
Author: Zain Dana Harper
Date: 2026-07-02
Status: working draft, not archive-submitted

## Official Status

`EMBODIED_SIM2REAL_FIXTURE_MATCH` applies to the deterministic local
differential-drive fixture.

`SOURCE_LEAD` applies to the arXiv metadata rows in the source ledger.

`HYPOTHESIS` applies to the larger embodied robotics, medical robotics,
AI4Robotics, and sim-to-real proof-packet product opportunity.

`NOT_REPLAYED` applies to real robot safety, surgical robotics, soft-robot
physics, VLA/foundation-model benchmark results, and BuildLang/buildc-native
execution.

## Publishable Claim

Project Telos now has a replayable embodied-systems preflight that binds:

- source-ledger receipts,
- robot morphology and unit declarations,
- command logs,
- predicted and observed traces,
- tolerances,
- safety envelope checks,
- latency checks,
- negative controls,
- Crucible measurement receipts, and
- Learn prooflesson export.

The fixture proves only the local contract. It is not a real robot result.

## Verified Artifacts

- Source ledger:
  `demo/research/embodied-sim2real-source-receipts.json`
- Fixture CLI:
  `demo/embodied-sim2real-proof-packet.mjs`
- Fixture test:
  `demo/embodied-sim2real-proof-packet.test.mjs`
- Fixture output:
  `docs/outreach/receipts/twenty-ninth-wave/embodied-sim2real-proof-packet-2026-07-02.json`
- Outreach note:
  `docs/outreach/TWENTY-NINTH-WAVE-EMBODIED-SIM2REAL-PREFLIGHT-2026-07-02.md`
- Working paper:
  `docs/research/whitepapers/EMBODIED-SIM2REAL-PROOF-PACKETS-FOR-ROBOTICS-2026-07-02.md`
- Crucible run:
  `docs/outreach/receipts/twenty-ninth-wave-embodied-sim2real-run-2026-07-02.json`
- Crucible run SHA-256:
  `b1f5bd65975c9a454ca9593c3b9310b9b7683ece8711ecbbcbdc789cff1f9704`
- Crucible report:
  `docs/outreach/receipts/twenty-ninth-wave-embodied-sim2real-report-2026-07-02.md`
- Crucible report SHA-256:
  `195c5b908d4597e38ee98dbf963d71aca564ac79fb7293f17b9a65b113d4fe2e`
- Learn packet:
  `docs/outreach/receipts/twenty-ninth-wave/embodied-sim2real.learn-packet.json`
- Learn packet SHA-256:
  `8aff40700c303e548136718be44d263f53890e51c3c8ca85ef9a567a0153a20e`
- Learn prooflesson receipt:
  `docs/outreach/receipts/twenty-ninth-wave/learn-embodied-sim2real/tutor/twenty-ninth-wave-embodied-sim2real.prooflesson.json`
- Learn prooflesson SHA-256:
  `5c54b90445982a59866aa74172ac25cb530e67569ab2e6da001613d5891344f1`
- Learn reverify witness SHA-256:
  `258663c0dd0d647de661602ceaeb00771a1a750a478ddb562bf21c0af71c7d6a`

## Fixture Result

The local fixture declares:

- Robot model: `differential_drive_planar_fixture`
- Wheel base: `0.5 m`
- Robot radius: `0.08 m`
- Max wheel speed: `0.6 m/s`
- Max angular speed: `1.1 rad/s`
- Max latency: `0.1 s`
- Mean path error tolerance: `0.025 m`
- Max path error tolerance: `0.04 m`
- Terminal position tolerance: `0.04 m`
- Terminal heading tolerance: `0.05 rad`
- Minimum obstacle clearance: `0.08 m`

The replayed nominal result is:

`EMBODIED_SIM2REAL_FIXTURE_MATCH`

The following negative controls are rejected:

- wrong wheel base,
- swapped wheels,
- centimeters treated as meters,
- unsafe clearance, and
- latency over limit.

## Publication Boundary

The publication can say:

> Project Telos turned an embodied robotics source-intake lane into a
> replayable sim-to-real preflight. The preflight demonstrates how an embodied
> proof packet can carry units, commands, traces, tolerances, safety envelope,
> latency, negative controls, and verification receipts before an embodied claim
> is promoted.

The publication must also say:

> This is a deterministic local fixture. It does not prove real robot safety,
> validate foundation-model robotic control, make a medical or surgical
> recommendation, or prove BuildLang/buildc robotics-runtime execution.

## Promotion Checklist

- [x] Source ledger is metadata-only.
- [x] Fixture declares robot morphology and units.
- [x] Fixture declares command logs.
- [x] Fixture emits predicted and observed traces.
- [x] Fixture checks trajectory tolerances.
- [x] Fixture checks command, latency, workspace, and obstacle-clearance bounds.
- [x] Fixture rejects five negative controls.
- [x] Local test replays the fixture.
- [x] Crucible run and report hashes patched after final run.
- [x] Learn packet and prooflesson hashes patched after final run.
- [ ] BuildLang/buildc typed-unit version exists.
- [ ] Manipulation/task benchmark fixture exists.
- [ ] Soft-robotics deformation fixture exists.
- [ ] Surgical/medical non-claim gate exists.

## Next Submission Gate

Do not submit this as an empirical robotics result. The stronger next paper
should be a methods paper: proof-carrying embodied AI claims for robotics, with
typed units, real/synthetic traces, safety envelopes, negative controls, and
BuildLang/buildc runtime receipts.
