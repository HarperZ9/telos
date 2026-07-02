# Project Telos Fourth-Wave Measurement Gate Demo

Date: 2026-07-02

Purpose: package two things the third-wave demo still needed: a Crucible measurement-gate result over a supported Telos measurement subset, and a Learn negative fixture proving forged proof-packet verdicts are rejected.

## Verified Results

| Segment | Evidence | Boundary |
| --- | --- | --- |
| Crucible positive gate | `crucible measurement-gate docs\outreach\receipts\fourth-wave-measurement-gate-packet.json --criteria docs\outreach\receipts\fourth-wave-measurement-gate-criteria.json --json` returned `verification_verdict: MATCH`, `decision_outcome: allow`, and summary `MATCH: 5`. | Current Crucible gate verifies five Telos layer types: histogram, dither, splat, cluster, and audio spectrum. |
| Crucible negative gate | The same packet with `fourth-wave-measurement-gate-negative-criteria.json` returned `verification_verdict: UNVERIFIABLE`, `decision_outcome: block`, and failure code `pixel_dimensions_mismatch`. | This proves criteria can fail closed; it does not prove all possible bad packets are caught. |
| Learn negative prooflesson | `learn tutor prooflesson forged --packet fourth-wave-forged-proof-packet.json` exited `1`, rejected `VERIFIED_SUPREME`, and wrote no receipt. | Negative fixture only. It proves illegal verdict enums are rejected at the prooflesson boundary. |
| Telos broader measurement bus | `node demo\measurement-layers.mjs --summary` still reports 10 layers and 10 measurements. | The broader bus has five current Crucible-gated layers and five future gate-expansion layers. Do not claim all ten are currently accepted by `crucible measurement-gate`. |

## Artifact Map

| Artifact | Role |
| --- | --- |
| `docs/outreach/receipts/fourth-wave-measurement-gate-packet.json` | UTF-8 Telos measurement packet filtered to the five Crucible-supported layer types. |
| `docs/outreach/receipts/fourth-wave-measurement-gate-criteria.json` | Positive criteria for the supported gate. |
| `docs/outreach/receipts/fourth-wave-measurement-gate-result.json` | Positive gate result: `MATCH`, `allow`, 5 matched rows. |
| `docs/outreach/receipts/fourth-wave-measurement-gate-negative-criteria.json` | Negative criterion requiring the wrong histogram pixel total. |
| `docs/outreach/receipts/fourth-wave-measurement-gate-negative-result.json` | Negative gate result: `UNVERIFIABLE`, `block`, `pixel_dimensions_mismatch`. |
| `docs/outreach/receipts/fourth-wave-forged-proof-packet.json` | Learn negative fixture with illegal verdict enum. |
| `docs/outreach/receipts/fourth-wave-negative-prooflesson-result.json` | Recorded rejection result for the forged proof packet. |

## Re-run Commands

From `C:\dev\public\telos`:

```powershell
crucible measurement-gate docs\outreach\receipts\fourth-wave-measurement-gate-packet.json --criteria docs\outreach\receipts\fourth-wave-measurement-gate-criteria.json --json
crucible measurement-gate docs\outreach\receipts\fourth-wave-measurement-gate-packet.json --criteria docs\outreach\receipts\fourth-wave-measurement-gate-negative-criteria.json --json
node demo\measurement-layers.mjs --summary
```

From any temp directory:

```powershell
node C:\dev\public\learn\src\cli.mjs tutor prooflesson forged --packet C:\dev\public\telos\docs\outreach\receipts\fourth-wave-forged-proof-packet.json
```

Expected negative prooflesson result:

- exit code `1`;
- rejection mentions illegal verdict enum;
- no `tutor\forged.prooflesson.json` file.

## Public Post Angle

> A proof stack needs negative fixtures. This pass shows both sides: a five-layer Telos measurement packet passes Crucible's current gate, a bad criterion blocks, and Learn refuses a forged verdict enum instead of turning it into a lesson.

## Do Not Post

- "Crucible gates all 10 Telos measurement layers today."
- "This proves physical display calibration."
- "The negative fixtures prove all malicious packets are impossible."
- "Learn accepts arbitrary proof-packet verdicts."
