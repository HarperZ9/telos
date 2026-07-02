# Project Telos Market Recon - 2026-07-01

This is a first-pass category and competitor scan for Project Telos. It is evidence-first:
measured local facts, source-backed market observations, and hypotheses are separated.

## Local Receipts

- Index status: `MATCH`; version `2.8.0`; role `structure-context`; source: `mcp__index.index_status`.
- Index doctor: `MATCH`; workspace map, context pack, structural verification, and MCP map probe passed; source: `mcp__index.index_doctor`.
- Forum status: `MATCH`; version `1.12.0`; role `orchestration-routing`; source: `mcp__forum.forum_status`.
- Forum doctor: `MATCH`; default roster, ledger verification, model-agnostic executor, and Project Telos route passed; source: `mcp__forum.forum_doctor`.
- Forum planner: unavailable; two calls failed with invalid JSON parse from executor.
- Gather status: `MATCH`; version `1.5.0`; role `perception-intake`; source: `mcp__gather.gather_status`.
- Gather doctor: `MATCH`; zero-dependency core, JSON receipts, and offline docs intake passed; source: `mcp__gather.gather_doctor`.
- Crucible status: `MATCH`; version `1.1.0`; role `verification-pressure`; source: `mcp__crucible.crucible_status`.
- Telos catalog: 65 available tools across five flagships; source: `mcp__telos.telos_catalog`.
- Telos compatibility doctor: `MATCH`; 14/14 checks passed, 65 available MCP tools, 5 servers, 4 host families; source: `mcp__telos.telos_compatibility_doctor`.
- Telos room: `MATCH`; 5/5 flagships ready, 20/20 checks passed, 65 protocol tools; source: `mcp__telos.telos_room`.
- Telos operator doctor: `MATCH`; 14/14 checks passed; source: `mcp__telos.telos_operator_doctor`.
- Telos CI doctor: `MATCH`; 5 latest flagship CI runs successful, 9 workflow files, Node 24 compatibility `MATCH`; generated 2026-06-29; source: `mcp__telos.telos_ci_doctor`.
- Telos golden workflow: `MATCH`; local command `node demo/flagship-workflow.mjs`; native summary included `forum_decided=project-telos`, `crucible_match=1`, `crucible_unverifiable=1`, `telos_demo_recheck=true`.
- Gather market intake 1: 7/7 kept; digest seal `d899b22e9b0c28f084a11bd1a04b1ce1a369ce7c46a7e3f6ded525245c042066`.
- Gather market intake 2: 7/7 kept; digest seal `e90cf05ded86f6c55edc7602c6002532cbc00fd3819242a6c703d27842973521`.
- Gather market intake 3: 5/5 kept after removing blocked pages; digest seal `3861f358bc57ccda749cde025601910323e034fed8fa7ed51af6d175790e2b52`.
- Crucible recon assessment: 2 `MATCH`, 0 `DRIFT`, 1 `UNVERIFIABLE`; broad uniqueness claim intentionally remains unmeasured until deeper competitor audit. Files: `C:\dev\tmp\telos-market-recon-thesis.json`, `C:\dev\tmp\telos-market-recon-measurements.json`.

## Local Scope

- `C:\dev\public`: public Project Telos workspace. Project scanner found 19,218 files. Metrics scan over selected source/doc/config extensions found 6,288 files and 1,342,993 lines.
- `C:\dev\opsec`: private-line/opsec workspace. Project scanner found 36,507 files with CI and tests. Metrics scan over selected source/doc/config extensions found 20,059 files and 2,444,542 lines.
- `C:\dev\public\telos\docs\CURRENT-STATE.md` reports the larger workstation substrate as 331 repositories, 163 public-class repos, 168 local-class repos, and 8 public-safe lane families.

## Category Map

| Category | Representative projects/tools | Market need already served | Telos overlap | Telos wedge |
|---|---|---|---|---|
| Agent orchestration frameworks | LangGraph, OpenAI Agents SDK, Microsoft AutoGen, CrewAI | Build multi-agent workflows, handoffs, persistence, hosted/local tools | Forum, Telos Model Foundry | Durable local ledger plus context envelopes, admission/action receipts, and Crucible verdicts across the whole run |
| LLM observability and evals | LangSmith, Arize Phoenix, Langfuse, W&B Weave, Braintrust, Humanloop | Trace, evaluate, debug, monitor LLM apps | Crucible, Telos operator/CI/performance doctors | Verdicts are measurement-derived and fail-closed; receipts join source, context, action, and later recheck |
| Browser automation and RPA | Playwright MCP, Browser Use, Browserbase Stagehand, UiPath | Let agents operate web apps or automate business workflows | Telos native control, browser evidence packets, Gather/Index/Crucible adapters | Browser actions become typed evidence packets with redaction, side-effect class, artifact refs, hashes, and later verification |
| Research assistants and source work | Elicit, NotebookLM, Perplexity, scite | Source-grounded search, paper review, citation-backed answers | Gather, Learning Forge | Gather separates direct source text, derived text, method, hash, and provenance before synthesis; Learning Forge turns research leads into executable labs |
| Codebase context and repo maps | Sourcegraph Cody, Cursor indexing, Aider repo-map, Greptile | Let agents understand large repos, retrieve relevant files, review code | Index, Context Curator Lite revival | Index emits source-ref expansion handles, freshness roots, omission failure codes, and context envelopes for later reruns |
| AI governance/risk management | NIST AI RMF, IBM watsonx.governance, Credo AI | Govern, monitor, document, and manage AI risk | Telos action receipts, operator doctor, Crucible, Forum | Telos targets operational receipts for each action, not only governance dashboards or policy docs |
| Creative AI and visual workflows | ComfyUI, Hugging Face Diffusers, TouchDesigner, Runway | Generate images/video/audio and build visual node workflows | Telos Creative Engine, measurement layers, creative kernels | Creative outputs carry scene specs, replay handles, measurement packets, and MATCH/DRIFT/UNVERIFIABLE gates |

## Market Observations

1. Agent frameworks are converging on durable execution, handoffs, and tool orchestration. LangGraph documents persistence/thread checkpoints, OpenAI Agents SDK exposes agents, handoffs, guardrails, sessions, tools, and tracing, AutoGen describes a multi-agent framework, and CrewAI positions itself as an agentic automation platform.

2. Observability/eval platforms are mature but mostly sit around model/app behavior. LangSmith, Phoenix, Langfuse, W&B Weave, and Braintrust all cover tracing/evals/observability patterns. Telos should not compete as "another tracing dashboard"; it should compete as the receipt spine that makes traces, source refs, action records, and verification verdicts joinable.

3. Browser automation is now a crowded agent substrate, but the trust boundary is weak in many products. Browser Use and Stagehand focus on making browser operation easier for agents; Playwright MCP makes browser control available through MCP; UiPath is moving RPA toward agentic automation. Telos' distinct entry point is not control alone; it is browser evidence packets with redaction, side-effect class, artifacts, and Crucible rechecks.

4. Research tools generally optimize answer quality and citation workflow. Elicit targets systematic review workflows; NotebookLM organizes user-provided sources; Perplexity and scite provide citation/source-backed answers. Gather's differentiated need is pre-synthesis provenance: method, ref, hash, derivation, and source/derived boundaries before an agent compresses the material.

5. Codebase context products are strong at retrieval/indexing, but many stop before replayable context contracts. Cursor describes codebase indexing, Aider has repo maps, Sourcegraph Cody focuses on codebase-aware assistance, and Greptile targets AI code review. Index's opportunity is audit-grade context envelopes: budgeted, freshness-rooted, omission-aware, and expandable by reference.

6. AI governance platforms serve enterprise oversight, but many are dashboard/process layers. NIST AI RMF supplies the governance vocabulary; IBM and Credo AI sell governance/risk platforms. Telos can meet a narrower but under-served operational need: every agent action carries intent, admission, execution evidence, review, compensation/idempotency metadata, and a verification state.

7. Creative tools are abundant, but measured creative workflows are not. ComfyUI and Diffusers provide generation workflows; TouchDesigner and Runway serve creative/interactive media. Telos' angle is "creative work you can measure and replay": rendering capability contracts, sensor layers, deterministic kernels, artifact hashes, and Crucible gates.

## Highest-Value Unmet Needs

1. End-to-end receipt chain for agent work.
   - Existing markets solve slices: orchestration, retrieval, tracing, browser control, research, or governance.
   - The gap is joining source intake, workspace memory, route/ledger state, action admission, execution evidence, and measurement verdicts into one local, re-checkable workflow.

2. Fail-closed verification as a product primitive.
   - Most tools expose scores, traces, citations, or human review queues.
   - Crucible's `MATCH` / `DRIFT` / `UNVERIFIABLE` posture is sharper: if no measurement exists, the claim does not get upgraded by fluent prose.

3. Privacy-preserving large-workspace context.
   - Large-context products tend to fetch/index aggressively.
   - Telos can sell the opposite: minimized model packets with hashes, expansion handles, source refs, omission codes, and local-only raw payloads.

4. Browser evidence for agentic work.
   - Browser-control tools answer "can the agent click/type/navigate?"
   - Telos should answer "what was admitted, what happened, what artifact proves it, what side effects existed, and can a later verifier re-check it?"

5. Research-to-lab conversion.
   - Research assistants help find and summarize.
   - Telos can convert leads into source receipts, concept modules, failure cases, executable labs, and Crucible gates.

6. Measured creative engine.
   - Creative AI tools generate artifacts.
   - Telos can own "creative artifacts with meters": pixel, dither, splat, light, waveform, renderer-capability, and replay evidence.

## Claim Boundaries

- High confidence: The local Telos room currently reports 5/5 ready flagships and 65 protocol tools. Source: `mcp__telos.telos_room`, verified by Crucible as `MATCH`.
- High confidence: The initial market scan covers at least seven adjacent categories with current public examples. Source: Gather market intakes and web research, verified by Crucible as `MATCH`.
- Moderate confidence: Telos is differentiated by an end-to-end local receipt spine spanning source, context, route, action, browser evidence, and measurement verdicts. This is strongly supported by local docs and no direct counterexample found in this pass.
- Unknown: Whether no competitor or internal enterprise platform combines all six layers. Crucible marked this `UNVERIFIABLE`; proving it requires a deeper competitor-by-competitor feature audit.

## Source Seeds

- Project Telos local docs: `C:\dev\public\telos\README.md`, `C:\dev\public\telos\docs\CURRENT-STATE.md`, `C:\dev\public\telos\docs\PROJECT-CONNECTION-MAP.md`.
- Gather README: `C:\dev\public\gather\README.md`.
- Index README: `C:\dev\public\index\README.md`.
- Forum README: `C:\dev\public\forum\README.md`.
- Crucible README: `C:\dev\public\crucible\README.md`.
- Model Context Protocol spec: <https://modelcontextprotocol.io/specification/2025-06-18>
- LangGraph persistence: <https://docs.langchain.com/oss/python/langgraph/persistence>
- LangSmith evaluation: <https://docs.langchain.com/langsmith/evaluation>
- OpenAI Agents SDK: <https://openai.github.io/openai-agents-python/>
- AutoGen docs: <https://microsoft.github.io/autogen/stable//index.html>
- CrewAI docs: <https://docs.crewai.com/>
- Arize Phoenix docs: <https://arize.com/docs/phoenix>
- Langfuse docs: <https://langfuse.com/docs>
- W&B Weave docs: <https://docs.wandb.ai/weave>
- Braintrust docs: <https://www.braintrust.dev/docs>
- Browser Use docs: <https://docs.browser-use.com/open-source/introduction>
- Stagehand docs: <https://docs.stagehand.dev/v3/first-steps/introduction>
- Playwright MCP: <https://github.com/microsoft/playwright-mcp>
- UiPath: <https://www.uipath.com/>
- Elicit systematic review: <https://elicit.com/solutions/systematic-review>
- NotebookLM: <https://notebooklm.google/>
- scite: <https://scite.ai/>
- Aider repo map: <https://aider.chat/docs/repomap.html>
- Cursor secure codebase indexing: <https://cursor.com/blog/secure-codebase-indexing>
- Greptile: <https://www.greptile.com/>
- Sourcegraph Cody: <https://sourcegraph.com/cody>
- NIST AI RMF: <https://airc.nist.gov/airmf-resources/airmf/5-sec-core/>
- IBM watsonx.governance: <https://www.ibm.com/products/watsonx-governance>
- Credo AI: <https://www.credo.ai/>
- ComfyUI: <https://github.com/comfy-org/comfyui>
- Hugging Face Diffusers: <https://huggingface.co/docs/diffusers/en/index>
- TouchDesigner: <https://derivative.ca/>
- Runway: <https://runwayml.com/>

## Next Recon Pass

1. Build a feature matrix with one row per competitor and columns for: source provenance, workspace context, orchestration ledger, action admission, browser evidence, measurement verdicts, evals, governance, local-first/privacy, MCP/CLI/SDK support, and target buyer.
2. Score each row as `present`, `partial`, `absent`, or `unverified`; use Crucible to keep the "full-stack uniqueness" claim `UNVERIFIABLE` until every key row is checked.
3. Identify buyer wedges separately: AI engineering teams, regulated enterprise agent workflows, research labs/newsrooms, codebase diligence/onboarding, browser-work automation, and creative technical artists.
4. Convert the strongest three wedges into landing-page language and demo scripts backed by local receipts.
