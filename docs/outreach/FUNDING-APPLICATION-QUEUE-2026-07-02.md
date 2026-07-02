# Project Telos Funding Application Queue

Date: 2026-07-02

Purpose: prepare funding and grant outreach for Project Telos without submitting forms or transmitting applications before final operator confirmation.

## Current Tool Evidence To Reuse

- Telos catalog reports 70 available tools across Gather, Index, Forum, Crucible, and Telos.
- Gather status reports `1.5.0` and `MATCH`.
- Index status reports `2.8.0` and `MATCH`.
- Forum doctor reports `1.12.0` and `MATCH`.
- Current public positioning: proof-native AI workbench; local-first source intake, workspace context, routing, action receipts, and `MATCH` / `DRIFT` / `UNVERIFIABLE` verification.
- Current repo license: `FSL-1.1-ALv2` / fair-source. This may block strict FOSS grant programs unless the application targets permissively licensed subcomponents or the license posture changes.

## Opportunity Matrix

| Opportunity | URL | Current status | Fit | Next action |
| --- | --- | --- | --- | --- |
| OpenAI Cybersecurity Grant / Trusted Access for Cyber | https://openai.com/form/cybersecurity-grant-program/ and https://openai.com/index/trusted-access-for-cyber/ | Official application remains live; OpenAI says the program evolved toward Trusted Access for Cyber and $10M in API credits for cyber defense. | Strong if strictly defensive: verified OSS fixes, duplicate filtering, CI triage, maintainer-friendly proof packets, and security remediation workflows. | Use existing draft `outputs/project-telos-openai-cybersecurity-grant-draft-2026-07-02.md`; final form needs applicant/contact/budget fields. |
| OpenAI / Trail of Bits Patch the Planet | https://openai.com/index/patch-the-planet/ and https://trailofbits.com/patch-the-planet/ | Active maintainer participation path; selected maintainers receive support, including ChatGPT Pro and conditional Codex security access. | Strong partnership/outreach path if framed as maintainer-side receipt tooling for validation, patch evidence, and duplicate filtering. | Prepare maintainer-facing note. Do not claim official partnership. |
| NLnet | https://nlnet.nl/propose/ | Next deadline shown as August 1, 2026 12:00 CEST; temporary intake limited to NGI TALER and NGI Fediversity. | Weak immediate fit unless we frame a Fediversity/hosting-stack adapter. Stronger fit when regular open calls reopen after summer. | Hold immediate submission. Prepare future open-call proposal and only submit if scope matches. |
| NLnet CodeSupply | https://nlnet.nl/codesupply/ and https://nlnet.nl/codesupply/guideforapplicants/ | First call says coming soon; guide says the program runs 2026-06-01 through 2029-05-30 and has EUR 400,000 for auxiliary projects. | Strong for supply-chain metadata, package-origin receipts, SBOM/AIBOM-style provenance, and source-federation adapters. | Keep CodeSupply draft parked until the call opens. |
| Alpha-Omega | https://alpha-omega.dev/ and https://openssf.org/community/alpha-omega/ | OpenSSF/LF security initiative focused on sustainable security improvements for critical open source projects and ecosystems. | Moderate to strong if attached to a critical OSS project/ecosystem rather than only Telos itself. | Use existing draft `outputs/project-telos-alpha-omega-grant-draft-2026-07-02.md`; pick recipient/project/amount before submit. |
| Cline Open Source Grant | https://cline.bot/blog/5m-installs-1m-open-source-grant-program and https://cline.bot/oss-grant | Rolling credit grants for developer tools, AI infrastructure, and agentic systems; application redirects to a Google Form. | Strong for Telos as a solo/small-team developer-tool and agentic-systems workbench. Credits only, not cash. | Prepare short application; submit only after operator confirms contact fields and whether Cline credits are useful. |
| Google DeepMind / Schmidt Sciences Multi-Agent AI Safety | https://deepmind.google/blog/investing-in-multi-agent-ai-safety-research/ and https://schmidtsciences.smapply.io/prog/scaling_ai_safety_for_a_multi_agent_world/ | Current call due August 8, 2026; Tier 1 up to $300k, Tier 2 $300k-$1M, 1-2 year projects. | Strong thematic fit for Telos as multi-agent action receipts, side-effect gates, tool-surface drift, and replayable verification; weaker if no research partner/institutional host. | Prepare a research-facing LOI; identify whether to apply as individual researcher, team, nonprofit, or collaboration. |
| grantmaking.ai AI Safety Launch Round | https://www.grantmaking.ai/ | Current $1M launch round; site says $5k-$50k grants focused on existential AI safety, with application timing language showing July 2026 deadlines. | Moderate if scoped to agent safety infrastructure: action receipts, tool-call drift, permission gates, and replayable audits. Weak if framed as generic dev tooling. | Prepare small-grant application; clarify deadline and cause-area fit before submitting. |
| Survival and Flourishing Fund | https://survivalandflourishing.fund/ | 2026 grant round announced; SFF says it has organized about $152M in philanthropic gifts/grants and estimates $20M-$40M across 2026 rounds/tracks. | Possible for long-term AI safety and governance infrastructure, but requires stronger existential-risk framing than normal Telos outreach. | Prepare only if the operator wants a long-term-risk framing and can support nonprofit/project identity details. |
| FLOSS/fund | https://floss.fund/ and https://dir.floss.fund/submit | Ongoing public directory/application via hosted `funding.json`; up to $100,000/year per FAQ. | Good mechanism, but license and usage maturity are risks. Telos fair-source is not clearly FLOSS. | Prepare `funding.json` draft; do not submit until public contact, license, and hosted URL are resolved. |
| Mozilla Builders | https://builders.mozilla.org/programs/ | Program page describes open-source AI accelerator with up to $100,000 non-dilutive funding and 12-week curriculum; visible page still carries 2024 dates. | Strong thematic fit for local AI, developer tooling, agent reliability, and open-source AI infrastructure. | Watch for next cohort; prepare concise accelerator application narrative now. |
| Mozilla MOSS | https://www.mozilla.org/en-US/moss/ | Not active. Mozilla's MOSS page says applications are closed and the program is on indefinite hiatus. | Historical fit only; do not treat as a current submission path. | Park. Route Mozilla work toward current Builders/Foundation opportunities only after verifying an open call. |
| GitHub Accelerator | https://github.com/open-source/accelerator | Current page is 2024 AI accelerator archive/sign-up; no current 2026 application form found in this pass. | Strong strategic fit if reopened: open AI, security, sustainability, visibility, and community. | Sign up for updates / monitor; prepare application copy and metrics. |
| GitHub Fund | https://github.com/open-source/fund | Investment/contact path, not a grant. | Possible only if Project Telos is positioned as an open-source developer-tool company. | Lower priority unless operator wants venture path. |
| a16z Open Source AI Grants | https://a16z.com/announcing-our-latest-open-source-ai-grants/ | Program page is older but relevant: grants for open-source AI stack builders. | Potential fit if applications remain accepted through private/contact path. | Prepare short inquiry, not a full application, unless current intake is verified. |

## Priority Order

1. OpenAI Cybersecurity Grant / Trusted Access for Cyber: highest-readiness active application path, strictly defensive framing.
2. Patch the Planet: strong maintainer/outreach path around AI-assisted security findings becoming real patches and tests.
3. Alpha-Omega: strong if tied to critical OSS maintainer support and measurable security-quality outcomes.
4. Cline Open Source Grant: strong, lower-friction credit path for developer-tool/agentic-systems work.
5. Google DeepMind / Schmidt multi-agent AI safety: strong if a research application or collaborator path is viable before August 8, 2026.
6. grantmaking.ai: moderate, fast small-grant path if framed as AI safety infrastructure rather than generic tooling.
7. NLnet CodeSupply: strong supply-chain/provenance fit, but wait until the call opens and license scope is FOSS.
8. Mozilla Builders: strong thematic fit if a current cohort opens.
9. FLOSS/fund: useful public funding directory path after license/contact/manifest issues are resolved.
10. SFF: possible only with a stronger long-term-risk/nonprofit framing.
11. GitHub Accelerator: high-visibility target; monitor for next opening.
12. NLnet general open calls: hold until regular open calls reopen or a specific Fediversity/Taler subproject exists.
13. MOSS: parked because applications are closed on indefinite hiatus.
14. a16z Open Source AI Grants: inquiry only until current intake is verified.

## Core Funding Narrative

Project Telos is a local-first, proof-native AI workbench for consequential agent work. It connects five standalone flagship tools:

- Gather: source intake and provenance receipts.
- Index: workspace maps and context envelopes.
- Forum: routing, ledgers, and operator-readable handoffs.
- Crucible: falsifiable claim checks with `MATCH`, `DRIFT`, and `UNVERIFIABLE` verdicts.
- Telos: shared MCP/catalog/action-receipt surface for host integration, browser evidence, model-foundry lanes, Learning Forge labs, and OSS proof packets.

The immediate funding goal is not generic runway. It is a bounded 8- to 12-week public hardening push:

- Stabilize the 70-tool MCP catalog and host freshness checks.
- Package browser evidence and action receipts for real developer workflows.
- Turn OSS issue intake into reproducible patch packets with tests and verifier results.
- Publish short demos and docs that make source provenance, selected context, actions, and blocked claims visible.
- Bring early users from AI agents, scientific computing, quant/dev tooling, and open-source maintainer workflows into feedback loops.

## Draft: Mozilla Builders / Open-Source AI Accelerator

Short application summary:

> Project Telos is a local-first AI workbench that makes agent work inspectable. Instead of treating an agent answer as the product, Telos records the source intake, workspace context, route, proposed action, execution evidence, and verification state. The current source checkout exposes a 70-tool MCP/catalog surface across Gather, Index, Forum, Crucible, and Telos, with `MATCH`/`DRIFT`/`UNVERIFIABLE` receipts for host freshness, CI triage, browser evidence, action receipts, and OSS proof packets.

Problem:

> AI coding and research agents are moving faster than the evidence around them. Developers can get code, summaries, and browser actions quickly, but often cannot reconstruct what sources were read, which files were selected, which commands ran, or which claims remained unverified. That is especially harmful for scientific workflows, open-source maintenance, quant/dev tooling, and regulated-adjacent review.

12-week plan:

1. Weeks 1-2: package the MCP freshness and action-receipt demos into a one-command local install path.
2. Weeks 3-4: ship browser-evidence packets for long browser workflows with redacted state digests and side-effect classes.
3. Weeks 5-6: convert one live OSS bug into a complete reproduction -> patch -> tests -> verifier packet.
4. Weeks 7-8: publish short docs/videos for local AI agents, MCP hosts, and maintainer review workflows.
5. Weeks 9-10: onboard 10-20 technical users and collect missing receipt fields.
6. Weeks 11-12: harden docs, public examples, and contribution lanes based on feedback.

Funding ask:

> $75,000-$100,000 non-dilutive support for focused engineering, documentation, public demo packaging, and user feedback loops.

## Draft: OpenAI Cybersecurity Grant / Trusted Access

Status: current output draft exists at `outputs/project-telos-openai-cybersecurity-grant-draft-2026-07-02.md`.

Short framing:

> Project Telos would use defensive AI access to reduce maintainer burden from machine-speed vulnerability reports and low-quality AI patches. The project would package each finding/fix as a re-checkable proof packet: source intake, duplicate scan, reproduction, patch, tests, CI triage, verifier verdict, and explicit remaining uncertainty.

Best evidence to attach:

- Existing public bugfix PRs with green checks or maintainer approval.
- OSS Proof Showcase receipts showing live issue intake blocked until reproduction/test/verifier evidence exists.
- CI triage and action-receipt docs showing defensive, maintainer-friendly workflow.

Do not include offensive exploitation, exploit development, credential acquisition, or vulnerability hype. Keep all examples in good-faith defensive find-and-fix lanes.

## Draft: Patch the Planet Maintainer Note

Target:

> Maintainership path through OpenAI / Trail of Bits Patch the Planet or direct maintainer outreach.

Body:

> Project Telos can help with the maintenance side of AI-assisted security work: duplicate filtering, reproduction evidence, patch/test receipts, and explicit `UNVERIFIABLE` states before a finding reaches maintainers. The useful contribution is not another stream of generated reports; it is a package that shows what was read, what was reproduced, what changed, which checks ran, and what remains uncertain.

## Draft: Alpha-Omega

Status: current output draft exists at `outputs/project-telos-alpha-omega-grant-draft-2026-07-02.md`.

Short framing:

> Use Project Telos as a maintainer-support workflow for critical OSS security quality: triage AI-generated findings, reject duplicates, reproduce real issues, package patches/tests, and publish monthly public reports with evidence fields maintainers can audit.

Missing fields before form submission:

- Specific target project/ecosystem.
- Amount and duration.
- Applicant identity/contact.
- License answer.
- Public reporting cadence.

## Draft: Cline Open Source Grant

Status: short credit-grant application prepared in `docs/outreach/NINETEENTH-WAVE-FUNDING-SUBMISSION-PACKETS-2026-07-02.md`.

Short framing:

> Project Telos is a local-first AI agent workbench for making agentic software work inspectable: source intake, workspace maps, routing ledgers, action receipts, MCP freshness checks, and `MATCH`/`DRIFT`/`UNVERIFIABLE` verification. A Cline OSS grant would support a focused public demo path for developers using agentic coding tools who need evidence, replay, and verifier packets around the work.

Blockers before submit:

- Operator contact email/name.
- Decide whether Cline credits are useful for the current Telos workflow.
- Confirm whether the fair-source umbrella license is acceptable for this program.

## Draft: Multi-Agent AI Safety Research Call

Status: research-facing LOI prepared in `docs/outreach/NINETEENTH-WAVE-FUNDING-SUBMISSION-PACKETS-2026-07-02.md`.

Short framing:

> Project Telos can be framed as multi-agent safety infrastructure: agents propose actions, deterministic tools execute bounded tasks, side effects are classified, policy/approval decisions are recorded, and replayable receipts preserve what happened. The research question is how to make multi-agent workflows safer by moving critical state, tool admission, and evidence into inspectable control planes rather than hidden prompt context.

Blockers before submit:

- Applicant identity and team/institution/collaboration shape.
- Decide Tier 1 vs Tier 2; Tier 1 is more realistic for Telos without a formal research consortium.
- Add bibliography and evaluation plan if applying.

## Draft: grantmaking.ai / SFF AI Safety Funding

Status: possible small-grant and long-term-risk paths, not ready for submission.

Short framing:

> Project Telos reduces AI-agent accident risk by requiring action receipts, permission gates, tool-surface freshness checks, side-effect classes, and replayable audit packets before consequential agent work is trusted. The small-grant ask would harden this into public examples for real agent workflows and publish negative cases where the system blocks or labels claims `UNVERIFIABLE`.

Blockers before submit:

- Confirm exact cause-area framing.
- Confirm applicant identity and public profile.
- Clarify deadline language for grantmaking.ai.
- Decide whether SFF's larger long-term-risk process is appropriate.

## Draft: NLnet CodeSupply

Status: parked until call opens.

Short framing:

> Project Telos would implement receipt-backed package and source-federation adapters for software supply-chain metadata. The work would focus on package-origin evidence, repository/source joins, metadata drift, and machine-readable verification packets that can route through CLI and MCP hosts.

Possible deliverables:

1. Package-origin receipt schema.
2. Source registry federation adapter.
3. SBOM/AIBOM-adjacent provenance demo.
4. MCP host integration for supply-chain source checks.
5. Crucible verification packet for metadata drift.

## Draft: FLOSS/fund Directory / funding.json

Status: draft only. See `docs/outreach/DRAFT-FUNDING-JSON-2026-07-02.json`.

Blockers before submit:

- Replace placeholder public contact email.
- Decide whether Telos umbrella fair-source license is acceptable. If not, apply with a permissively licensed component or publish a clearly FOSS subset first.
- Host the manifest at a stable URL, ideally in-repo as `funding.json`.
- Add `.well-known/funding-manifest-urls` only if the manifest references URLs on another hostname.

Suggested ask:

> $100,000 one-time support for Project Telos public hardening: MCP host freshness, action receipts, browser evidence, OSS proof packets, and maintainer-facing documentation.

## Draft: NLnet Future Open Call

Current status: hold for regular call unless a Fediversity/Taler-shaped subproject is created.

Proposal name:

> Project Telos: Re-checkable AI Agent Workflows for Open Internet Tooling

Abstract:

> Project Telos is a local-first workbench that gives AI-assisted software and research workflows a re-checkable evidence trail. It connects source intake, workspace context selection, task routing, action receipts, and falsifiable verification into CLI and MCP tools that can run locally. The project outcome is a hardened open workflow where developers and maintainers can see what an agent read, what it changed, which checks ran, and which claims remained `UNVERIFIABLE`.

Requested support:

> EUR 50,000-75,000 for a bounded public hardening effort: source-federation receipts, MCP freshness probes, action-receipt schemas, browser evidence packets, OSS maintainer proof packets, documentation, and interoperability testing.

Technical challenges:

> The hard problem is preserving enough evidence for review without leaking raw private data or forcing every host into one platform. The work must keep receipts portable across CLI, MCP, IDE, TUI, and app surfaces; distinguish `MATCH`, `DRIFT`, and `UNVERIFIABLE`; and make missing evidence actionable instead of hiding it behind a fluent model answer.

Ecosystem engagement:

> Publish examples for MCP host authors, local AI agent users, scientific/research tooling developers, and open-source maintainers. Continue upstream PRs that show the workflow on real public bugs and directory listings. Gather feedback from Reddit, YouTube, GitHub, and developer communities where people already discuss agent reliability, reproducibility, and long browser workflows.

## Parked: MOSS Champion Pitch

Subject:

> Seeking Mozillian champion for local-first AI workflow receipt tooling

Body:

> I am building Project Telos, a local-first AI workbench for recording what agent workflows read, selected, changed, and verified. The current source checkout exposes a 70-tool MCP/catalog surface across source intake, workspace mapping, routing, verification, action receipts, browser evidence, and OSS proof packets. The project is relevant to open-source AI because it makes local agent work more inspectable and less dependent on opaque hosted workflow state.
>
> I am looking for a Mozillian champion before considering a MOSS Foundational Technology application. The bounded project goal would be to harden browser-evidence packets, MCP freshness checks, and maintainer-facing action receipts so local AI tools can preserve provenance without sending raw private payloads to a central service.

Current status: do not send as an active MOSS application pitch. Mozilla's public MOSS page says applications are closed and the program is on indefinite hiatus. Keep this language only as a relationship/champion note if a future Mozilla open-source funding path reopens.

## Draft: a16z Open Source AI Grants Inquiry

Subject:

> Open-source AI tooling grant inquiry: proof-native agent workbench

Body:

> I am building Project Telos, a local-first workbench for AI agent provenance and verification. It packages source intake, workspace context, routing, action receipts, browser evidence, and verifier verdicts into a 70-tool MCP/catalog surface across Gather, Index, Forum, Crucible, and Telos. The near-term goal is to harden developer-facing demos and real OSS bugfix packets so agent workflows become inspectable, replayable, and maintainer-friendly.
>
> If the open-source AI grant program is still accepting projects or referrals, I would like to share a concise proposal and current receipts.

## Do Not Submit Yet

- Do not submit any grant form, application, public directory listing, or funding manifest without final operator confirmation.
- Do not send personal contact details until the exact destination and data are confirmed.
- Do not claim Telos is fully FLOSS while the umbrella repo is `FSL-1.1-ALv2`.
- Do not claim user adoption or production deployments unless current evidence exists.
