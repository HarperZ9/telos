# Packet 058: Competitor Proof-Gap Matrix

Date: 2026-07-01

Status: `COMPETITOR_PROOF_GAP_MATRIX_MATCH`

This pass creates a 45-row source-backed market matrix across three tracks.
Gap claims are hypothesis labels unless directly verified by source text.

```text
market_row_count = 45
source_match_count = 45
research_ai4science_rows = 15
ai_infra_agent_ops_rows = 15
visual_compiler_compute_rows = 15
uniqueness_claim_status = HYPOTHESIS_ONLY
```

| Track | Tool | Buyer | Gap status |
| --- | --- | --- | --- |
| `research_ai4science` | pipeline_math | Research labs and formal math teams | `inferred` |
| `research_ai4science` | FutureHouse | AI4Science labs | `inferred` |
| `research_ai4science` | Sakana AI Scientist | AI research teams | `inferred` |
| `research_ai4science` | Microsoft Discovery | Enterprise R&D organizations | `inferred` |
| `research_ai4science` | NVIDIA BioNeMo | Bio/pharma AI teams | `inferred` |
| `research_ai4science` | Elicit | Researchers and analysts | `inferred` |
| `research_ai4science` | Consensus | Researchers and evidence consumers | `inferred` |
| `research_ai4science` | Semantic Scholar API | Literature graph builders | `inferred` |
| `research_ai4science` | OpenAlex | Bibliometrics and research graph teams | `verified` |
| `research_ai4science` | Benchling | Biotech R&D teams | `inferred` |
| `research_ai4science` | Nextflow | Bioinformatics and data workflow teams | `inferred` |
| `research_ai4science` | Snakemake | Computational biology teams | `inferred` |
| `research_ai4science` | LeanDojo | Formal methods and theorem proving teams | `inferred` |
| `research_ai4science` | DeepMind AlphaProof | Mathematical AI teams | `inferred` |
| `research_ai4science` | Jupyter | Scientific computing teams | `inferred` |
| `ai_infra_agent_ops` | LangSmith | AI application teams | `inferred` |
| `ai_infra_agent_ops` | Langfuse | LLM product teams | `inferred` |
| `ai_infra_agent_ops` | Arize Phoenix | AI engineering teams | `inferred` |
| `ai_infra_agent_ops` | Braintrust | AI product teams | `inferred` |
| `ai_infra_agent_ops` | OpenTelemetry | Platform engineering teams | `verified` |
| `ai_infra_agent_ops` | MLflow | ML platform teams | `inferred` |
| `ai_infra_agent_ops` | Weights & Biases | ML teams | `inferred` |
| `ai_infra_agent_ops` | DVC | ML/data teams | `inferred` |
| `ai_infra_agent_ops` | LlamaIndex | RAG and agent builders | `inferred` |
| `ai_infra_agent_ops` | LangGraph | Agent application teams | `inferred` |
| `ai_infra_agent_ops` | Humanloop | AI product teams | `inferred` |
| `ai_infra_agent_ops` | Helicone | LLM application teams | `inferred` |
| `ai_infra_agent_ops` | promptfoo | AI safety/eval teams | `inferred` |
| `ai_infra_agent_ops` | OpenLLMetry | AI observability teams | `inferred` |
| `ai_infra_agent_ops` | Evidently | ML monitoring teams | `inferred` |
| `visual_compiler_compute` | Julia | Scientific computing teams | `inferred` |
| `visual_compiler_compute` | Mojo | AI/performance engineers | `inferred` |
| `visual_compiler_compute` | OpenXLA | ML compiler teams | `inferred` |
| `visual_compiler_compute` | Chapel | HPC teams | `inferred` |
| `visual_compiler_compute` | MLIR | Compiler infrastructure teams | `inferred` |
| `visual_compiler_compute` | Triton | GPU kernel teams | `inferred` |
| `visual_compiler_compute` | ACES | Color pipeline teams | `inferred` |
| `visual_compiler_compute` | OpenColorIO | VFX/color pipeline teams | `inferred` |
| `visual_compiler_compute` | Calman | Display calibration teams | `inferred` |
| `visual_compiler_compute` | ColourSpace | Display calibration teams | `inferred` |
| `visual_compiler_compute` | DaVinci Resolve Color | Colorists and post teams | `inferred` |
| `visual_compiler_compute` | ParaView | Scientific visualization teams | `inferred` |
| `visual_compiler_compute` | VTK | Visualization developers | `inferred` |
| `visual_compiler_compute` | CUDA | GPU computing teams | `inferred` |
| `visual_compiler_compute` | OpenFOAM | Engineering simulation teams | `inferred` |

Primary 30-day push: publish the agent-action proof packet demo first,
then use it as the execution substrate for pipeline-math++ and BuildLang/color demos.

Current promoted natural laws: none.
