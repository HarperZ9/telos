# Dogfood Pass 0005 Ledger

Date: 2026-07-01

Status: `CRUCIBLE_MATCH`.

Crucible assessment:

- thesis id: `d51b7984f1d1e194`;
- claims: `7`;
- match: `7`;
- drift: `0`;
- unverifiable: `0`;
- thesis seal: `d51b7984f1d1e194761fea93b1d2e9563c81f6ffa4b7c73539af1eadfffe6935`;
- verdict seal: `37bf743a3c043d82f711c091b7f8a969c9cbaaad7da4b6e76c4253fbc37d6252`;
- measurement seal: `7e3003111f8c843b99a72259a405cb450c1d5a7ac6fb49d14c13b82418bdcf3c`;
- assessment seal: `39cd8c3bb74519e94eb8d916917035dbd9d98176ead08121fc18dc36f56629c7`;
- integrity: `seals_ok=True`, `thesis_ok=True`, `verdicts_rederive=True`.

Pass theme: turn the adversarial pass into adoption architecture. The product assumption for this pass is that Telos should import and bind evidence from incumbent systems rather than attempt to replace every workflow tool.

No uniqueness claim in this pass is treated as fact. The claim is narrower: incumbent tools already hold valuable fragments of evidence, and the Telos wedge is hypothesized to be cross-layer binding plus verification.

## Tool Receipts

| Surface | Result | Evidence |
| --- | --- | --- |
| Gather web config attempt 1 | `CONFIG_DRIFT` | rejected because config needed a non-empty `jobs` list. |
| Gather web config attempt 2 | `CONFIG_DRIFT` | rejected because each job needed `source` and `target`. |
| Gather web config attempt 3 | `CONFIG_DRIFT` | rejected because raw URL was treated as an unknown `source`. |
| Gather doctor | `MATCH` | zero-dependency core, JSON receipts, and offline docs intake returned `MATCH`; tool version `1.5.0`. |
| Gather docs, scoped | `MATCH` | kept `1`, dropped `22`, seal `5141418c6e49f466ad7b616471f185f21ab9d49ae337e4c575f6dc4c592a71ca`. |
| Gather docs, unscoped | `MATCH` | kept `23`, dropped `0`, seal `8afe8c29d704aff1ca6255e81704722bb5a347c9bed237e9ecca34facdeb09a3`. |
| Index map on Telos | `MATCH` | branch `main`, head `cbbf82c`, repo count `1`, dirty count `0`, untracked count `7`, tool version `2.8.0`. |
| Forum route check | `ESCALATE` | no decided lane; confidence `0.17297297297297298`; top candidate `ci-cd` score `0.2`, `project-telos` score `0.02702702702702703`. |
| Forum verify | `MATCH` | chain `true`, deep `true`. |
| Forum ledger summary | `MATCH` | entries `1`, requests `1`, answers `0`, model calls `0`, checkpoint `0d88da42deb02a0891e910298c244b66a3654ed5ea9863e585a897c6beb0f806`, verified `true`. |
| Telos room | `MATCH` | five tools ready out of five, twenty checks passed out of twenty, sixty-five protocol surfaces available. |

## Source Refresh

Direct official source reads were used for current external claims because the Gather web config path needs repair.

| Source | Relevant evidence fragment | Adapter implication |
| --- | --- | --- |
| OpenTelemetry traces | Traces provide context, correlation, hierarchy, spans, status, events, links, and exporters. | Import traces as causality evidence, not as the final proof packet. |
| LangSmith Observability | LangSmith positions itself around LLM traces, production metrics, integrations, automations, evaluations, and feedback. | Treat LangSmith traces/evals as upstream evidence when buyers already use it. |
| Langfuse Observability | Langfuse traces prompts, responses, token use, latency, tools, retrieval steps, sessions, environments, cost, and metadata. | Import LLM-specific trace fields and bind them to authority and verification records. |
| MLflow Tracking | MLflow logs parameters, code versions, metrics, output files, runs, artifacts, models, datasets, and remote tracking components. | Import run/model/dataset evidence, then add authority, source, and verification packets around it. |
| W&B Artifacts | W&B Artifacts track and version data as run inputs and outputs, including datasets and model checkpoints. | Import artifact lineage as model/data evidence. |
| DVC data/model versioning | DVC captures data/model versions in Git commits, tracks code/data/model history, and supports reproducibility and audit review. | Import DVC metadata as data lineage and reproducibility evidence. |
| Nextflow reports | Nextflow offers execution logs, HTML reports, timelines, trace files, and workflow DAGs for pipeline runs. | Import workflow run/task evidence for scientific and bioinformatics packets. |
| Snakemake reports | Snakemake can generate self-contained reports with runtime statistics, provenance information, workflow topology, and annotated results. | Import workflow reports as research-experiment evidence. |
| OpenLineage | OpenLineage defines an extensible job/run/dataset lineage model with facets and integrations. | Use as a lineage interchange layer for data workflows. |
| SLSA Provenance | SLSA provenance includes build definitions, run details, builders, dependencies, and external/internal parameters. | Map BuildLang/buildc and CI receipts to known supply-chain provenance patterns. |
| in-toto | in-toto records what steps were performed, by whom, and in what order to secure software supply-chain integrity. | Reuse supply-chain step attestation concepts for tool-action receipts. |

## Strategic Read

The proof-packet product should be adapter-first:

1. `TraceImporter`: OpenTelemetry, Langfuse, LangSmith.
2. `ExperimentImporter`: MLflow, W&B, DVC.
3. `WorkflowImporter`: Nextflow, Snakemake, OpenLineage.
4. `SupplyChainImporter`: SLSA, in-toto, Git/CI.
5. `InternalReceiptImporter`: Index, Gather, Forum, Crucible, Telos, BuildLang/buildc, Build Color, Calibrate Pro.

The market promise is not "we trace better than every trace product." The promise is "we bind traces, source lineage, authority, workspace state, verification verdicts, runtime/build receipts, and buyer-facing decisions into one packet with explicit failure labels."

## Artifacts

| Artifact | Role |
| --- | --- |
| `schemas/proof-packet-adapters-pass-0005.json` | Prioritized adapter list and missing binding layer for each incumbent evidence system. |
| `schemas/buyer-objections-pass-0005.json` | Buyer objection matrix with required demo evidence. |
| `schemas/validator-contracts-pass-0005.json` | Validator contract set for schema and minimum proof packet quality gates. |
| `crucible/pass-0005-thesis.json` | Falsifiable claims for this pass. |
| `crucible/pass-0005-measurements.json` | Measurements for this pass. |
| `crucible/pass-0005-report.md` | Crucible assessment report. |
| `crucible/pass-0005-run.json` | Crucible run record. |

## 30-Day Product Adjustment

Primary push remains `AgentActionProofPacket`, but the first implementation should ship with three adapter stubs:

1. OpenTelemetry span import.
2. Langfuse/LangSmith-style LLM trace import.
3. Git/CI/SLSA-style source/build receipt import.

The next public demo should show the same agent action as:

- a raw trace;
- a trace plus artifact/run receipt;
- a Telos proof packet with authority, workspace state, verification, and replay summary.

## Natural-Law Promotion

Current promoted natural laws: none.

## Next-Pass Queue

1. Convert validator contracts into executable schema validators.
2. Create a minimal `ProofPacket/v1` example JSON with all required fields.
3. Build an import-normalization table from OpenTelemetry spans to Telos action events.
4. Add one concrete Build Color/Calibrate measurement receipt into the same packet shape.
5. Repair the Gather web config adapter and document the accepted config schema.
