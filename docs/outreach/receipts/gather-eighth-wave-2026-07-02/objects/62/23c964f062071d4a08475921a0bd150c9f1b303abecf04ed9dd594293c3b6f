# Packet 136: Source-Lead Demotion Gate

Date: 2026-07-01

Status: `SOURCE_LEAD_DEMOTION_GATE_MATCH`

Purpose: make the pass 0125 video-source boundary executable. Video metadata,
transcript hashes, and keyword signals may route experiments, but they cannot
promote a claim to fact or law without independent artifacts.

```text
source_leads = 4
fixtures = 7
accepted = 3
rejected = 4
compose_status = MATCH
test_status = MATCH
validator_status = MATCH
```

## Source Summary

| Video | Status | Dominant signal | Raw transcript in packet |
| --- | --- | --- | --- |
| HbKzqvey5PA | SOURCE_LEAD_ONLY | quantum_physics | False |
| 4MQbd5wTlI8 | SOURCE_LEAD_ONLY | formal_math | False |
| EdVG5qNm2rY | SOURCE_LEAD_ONLY | counterexample | False |
| nYwid6Q5HXk | SOURCE_LEAD_ONLY | agent_loop | False |

## Gate Fixtures

| Fixture | Requested status | Gate status | Failures |
| --- | --- | --- | --- |
| source_lead_only_ok | SOURCE_LEAD_ONLY | ACCEPTED |  |
| hypothesis_routing_ok | HYPOTHESIS | ACCEPTED |  |
| independent_probe_ok | PROBE_MATCH | ACCEPTED |  |
| video_only_fact_rejected | VERIFIED_FACT | REJECTED | missing_independent_evidence,video_only_promotion |
| video_law_rejected | PROMOTED_LAW | REJECTED | law_promotion_forbidden,missing_independent_evidence,video_only_promotion |
| raw_transcript_rejected | HYPOTHESIS | REJECTED | raw_transcript_included |
| keyword_count_as_proof_rejected | CRUCIBLE_MATCH | REJECTED | keyword_count_not_proof,missing_independent_evidence,video_only_promotion |

## Policy

- Source leads may remain `SOURCE_LEAD_ONLY` or `HYPOTHESIS`.
- Fact-like statuses require independent non-video evidence.
- `PROMOTED_LAW` is rejected by this gate.
- Raw transcript packet exports are rejected.
- Keyword signal counts are routing data, not proof.

## Boundary

Pass 0126 is a demotion and rejection gate. It does not validate video claims, expose raw transcripts, declare market fit, or promote a natural law.
