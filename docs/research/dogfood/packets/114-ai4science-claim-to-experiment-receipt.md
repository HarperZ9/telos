# Packet 114: AI4Science Claim-to-Experiment Receipt

Date: 2026-07-01

Status: `AI4SCIENCE_CLAIM_TO_EXPERIMENT_RECEIPT_MATCH`

Purpose: convert AI4Science market and whitepaper sources into a minimum
claim-to-experiment receipt. This pass maps agentic discovery, biomolecular
models, workflow engines, and lab-record systems into proof fields without
promoting any biological or drug-discovery claim.

```text
source_count = 11
official_or_primary_count = 11
youtube_ai4science_video_count = 1
minimum_packet_fields = 11
compose_status = MATCH
test_status = MATCH
```

## Source-To-Receipt Map

| Source | Kind | Gap Status | First Required Receipts |
| --- | --- | --- | --- |
| FutureHouse | official | inferred | source_claim, agent_action_receipt, reviewer_objections |
| FutureHouse Platform | official | inferred | agent_action_receipt, workflow_runtime_receipt |
| Sakana AI Scientist | official | inferred | model_or_agent_actions, experiment_or_simulation_protocol, reviewer_objections |
| Sakana AI Scientist paper | primary_paper | inferred | source_claim, measurement_receipt, promotion_verdict |
| Microsoft Discovery blog | official | inferred | hypothesis_receipt, validation_loop_receipt, iteration_receipt |
| Microsoft Discovery product | official | inferred | enterprise_context_receipt, human_review_receipt |
| NVIDIA BioNeMo | official_docs | inferred | model_checkpoint_receipt, training_or_inference_receipt |
| AlphaFold 3 Nature | primary_paper | inferred | primary_paper_receipt, prediction_measurement_receipt, experimental_validation_boundary |
| Nextflow | official | inferred | workflow_runtime_receipt, container_or_environment_receipt |
| Snakemake | official_docs | inferred | workflow_runtime_receipt, reproducibility_receipt |
| Benchling | official | inferred | lab_record_receipt, sample_or_entity_lineage_receipt |

## Promotion Gates

- Reject unmeasured discovery claims: `True`.
- Require reproduction status: `True`.
- Require human review: `True`.

## Next Experiments

| Experiment | Acceptance | Status |
| --- | --- | --- |
| `source_claim_to_unverified_protocol` | one biological claim has source receipt, protocol placeholder is explicit, promotion verdict remains UNVERIFIABLE | READY_NEXT |
| `workflow_runtime_bridge` | Nextflow/Snakemake analog fields map to Telos receipts, environment and output hashes are required | READY_AFTER_SCHEMA |
| `negative_result_and_review_lane` | failed experiment is first-class, reviewer objections block promotion, human review is required | READY_AFTER_MINIMUM_PACKET |

Boundary: this pass is a receipt schema and market/research map. It does not
prove a biological result, drug efficacy, benchmark superiority, or a natural
law.
