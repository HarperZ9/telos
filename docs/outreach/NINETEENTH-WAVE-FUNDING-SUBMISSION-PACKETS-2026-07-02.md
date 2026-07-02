# Nineteenth-Wave Funding Submission Packets

Date: 2026-07-02

Purpose: turn the current funding queue into field-level submission packets for the highest-fit non-GitHub opportunities. These are ready-to-review drafts, not submitted applications.

## Current Tool Evidence

- Telos room: `MATCH`, 5 of 5 flagship tools ready, 20 of 20 checks passed, 70 protocol tools available.
- Gather: `MATCH`, `1.5.0`.
- Index: `MATCH`, `2.8.0`.
- Forum: `MATCH`, `1.12.0`.
- Crucible: `MATCH`, `1.1.0`.
- Telos operator doctor: `MATCH`, 14 of 14 checks passed.

## 1. OpenAI Cybersecurity Grant / Trusted Access

Source status:

- OpenAI's Trusted Access for Cyber page frames the path around defensive cyber acceleration and $10M in API credits.
- The Cybersecurity Grant form asks for applicant fields, project title, one-sentence description, proposal, problem statement, timeline, requested funding/API credits/resources, and public sharing plans.
- The form says offensive-security projects will not be considered.

Recommended disposition: submit first after operator fields are confirmed.

### Field Map

- First name: `[OPERATOR FIELD]`
- Last name: `[OPERATOR FIELD]`
- Email: `[OPERATOR FIELD]`
- Company or university: `Project Telos` or `[OPERATOR FIELD]`
- Role/title: `[OPERATOR FIELD]`
- LinkedIn: `[OPERATOR FIELD]`
- Other people: `[OPERATOR FIELD or "None for this submission"]`
- Project title: `Maintainer-Safe AI Security Remediation Receipts`
- One descriptive sentence: `Project Telos will turn AI-assisted OSS security work into maintainer-safe proof packets with source intake, duplicate filtering, reproduction, patch/test evidence, CI triage, and explicit unverifiable-state labels.`

### Problem Statement, 200 Words Max

Open-source maintainers are receiving more AI-generated vulnerability reports, issue comments, and patch submissions. The bottleneck is no longer only discovery; it is validating whether a report is real, whether the proposed fix is scoped, whether tests prove the claim, whether CI failures are caused by the change, and whether maintainers can trust the evidence without reconstructing the entire workflow. Project Telos addresses that burden by producing maintainer-safe receipts: what sources were read, which repository context was selected, what was reproduced, what changed, which tests and checks ran, what failed, and which claims remain `UNVERIFIABLE`. The proposal is defensive-only: use AI to improve validation, false-positive filtering, CI triage, and reproducible remediation packets for public open-source software.

### Timeline

- Month 1: freeze the OSS remediation receipt schema; package existing proof packets into a maintainer-facing template; document sensitive-disclosure routing.
- Month 2: run the workflow on public, non-sensitive OSS cases; publish successful and rejected packets; improve duplicate checks and CI classification.
- Month 3: onboard maintainers or reviewers for feedback; publish docs, examples, and a final report with lessons learned and remaining gaps.

### Requested Resources

Preferred ask:

> API credits plus a small engineering grant for a 12-week defensive maintainer-support sprint.

Budget tiers:

- Credits only: run public-repo workflows, refine CI triage, publish examples.
- $25k-$50k plus credits: focused implementation, docs, case studies, and maintainer feedback loops.
- $75k-$100k plus credits: dedicated public hardening sprint with at least 10 case studies and reusable maintainer documentation.

### Public Sharing Plan

Public outputs will include the receipt schema, non-sensitive case studies, docs, examples, and final report. The project will not publish secrets, private credentials, private target data, exploit mechanics for unresolved vulnerabilities, or maintainer-private discussions. Security-sensitive findings will follow project disclosure processes.

## 2. Cline Open Source Grant

Source status:

- Cline announced a $1M Open Source Grant program.
- Grant amounts are described as $1,000-$10,000 in credits.
- The program looks for developer tools, AI infrastructure, agentic systems, and projects from solo developers or small teams.
- Application path redirects from `https://cline.bot/oss-grant` to a Google Form.

Recommended disposition: high-fit, low-friction credit application if Cline credits are useful.

### Short Application Copy

Project Telos is a local-first AI agent workbench for developers who need evidence around agentic coding work. It connects source intake, workspace maps, routing ledgers, action receipts, MCP host freshness checks, browser evidence packets, and `MATCH`/`DRIFT`/`UNVERIFIABLE` verification. The current source checkout reports 70 available protocol tools across Gather, Index, Forum, Crucible, and Telos.

The grant would help package Telos into a clearer public developer path: one-command demos, short videos/docs, Cline-compatible workflows where useful, and real proof packets showing how agentic coding work can preserve what was read, changed, tested, blocked, or left unverifiable.

Why it matters: coding agents are getting faster, but maintainers and developers still need inspectable evidence. Telos is not another autonomous-agent demo; it is the evidence layer around those agents.

### Blockers

- Confirm operator contact fields.
- Confirm whether Cline credits are useful.
- Confirm license answer and public repo links.

## 3. Google DeepMind / Schmidt Sciences Multi-Agent AI Safety

Source status:

- Call: Scaling AI Safety for a Multi-Agent World.
- Proposal due date: August 8, 2026.
- Tier 1: up to $300,000 for 1-2 years.
- Tier 2: $300,000-$1,000,000 for 1-2 years.
- Eligible applicants include individual researchers, research teams, research institutions, and collaborations.

Recommended disposition: prepare Tier 1 LOI; submit only if applicant/team framing is strong enough.

### Research-Facing Abstract

Project Telos proposes a receipt-first safety architecture for multi-agent systems. Instead of allowing agents to hold critical state in hidden prompt context, Telos separates source intake, workspace selection, task routing, action admission, side-effect classification, execution evidence, and verification into inspectable local tools. The research objective is to evaluate whether explicit action receipts, tool-surface freshness probes, replayable state/event packets, and `MATCH`/`DRIFT`/`UNVERIFIABLE` verdicts reduce failure modes in multi-agent workflows that touch software repositories, browsers, command lines, and external APIs.

### Research Questions

1. Can receipt-backed action admission reduce unintended side effects in multi-agent software workflows?
2. Can tool-surface freshness probes detect drift before agents call stale or misdescribed tools?
3. Can replayable state/event packets make multi-agent failures easier to reproduce and repair?
4. Which evidence fields are necessary for human reviewers to trust, reject, or rerun an agent handoff?

### Evaluation Plan

- Build benchmark tasks where multi-agent workflows must read sources, select context, call tools, edit code, run checks, and produce a handoff.
- Compare normal logs against Telos receipts for reproducibility, review time, side-effect classification, and failure localization.
- Include negative cases: stale MCP tools, hidden context loss, ambiguous approvals, command failure, external CI failure, and unverifiable claims.
- Publish artifacts and findings where safe.

### Blockers

- Applicant/team identity.
- Whether to apply as individual researcher, nonprofit/project, or collaboration.
- Tier selection.
- Research references and letters/collaborators if needed.

## 4. grantmaking.ai AI Safety Launch Round

Source status:

- Current site says a $1M launch round is live.
- Site states $5k-$50k grants focused on existential AI safety.
- The page has inconsistent timing language: it says applications are open until July 27, 2026 and also says apply by July 13, 2026.

Recommended disposition: prepare a small-grant profile/application; verify deadline before submission.

### Small-Grant Copy

Project Telos is AI safety infrastructure for agentic software work. It reduces accident risk by making consequential agent actions inspectable: the system records source intake, selected context, tool surfaces, proposed actions, side-effect classes, approvals, command results, verifier verdicts, and explicit `UNVERIFIABLE` states. The near-term grant would harden public examples where agents are blocked from unsafe or unsupported handoffs, detect stale tool surfaces before execution, and preserve replayable evidence for human review.

### Ask

> $25,000-$50,000 to package and evaluate action receipts, side-effect gates, tool drift probes, and replayable audit packets for multi-agent developer workflows.

### Blockers

- Confirm whether Telos should be framed under existential AI safety, AI control, agent safety engineering, or developer-tooling safety.
- Confirm public profile and contact fields.
- Resolve deadline ambiguity.

## 5. Survival and Flourishing Fund

Source status:

- SFF's 2026 grant round is announced.
- SFF estimates $20M-$40M in funding across 2026 rounds/tracks.
- SFF is broader and more long-term-risk oriented than normal developer-tool grants.

Recommended disposition: prepare only if the operator wants a long-term-risk framing.

### Candidate Framing

Project Telos is infrastructure for safer delegation to increasingly capable AI agents. As agents gain the ability to operate browsers, CLIs, repositories, workflows, and APIs, failures become harder to audit if state and approvals live only in model context or provider logs. Telos creates local, replayable evidence packets so humans and institutions can inspect what an agent read, selected, proposed, executed, and failed to verify. The SFF-relevant outcome is safer deployment and governance of multi-agent systems through practical evidence standards, not a generic productivity tool.

### Blockers

- Stronger long-term-risk theory of change.
- Applicant/project legal identity.
- Budget and duration.
- Whether to apply via S-Process, rolling application, or later round.

## Submit-Ready Boundary

Do not submit any application until the operator confirms:

- applicant/contact fields,
- project/legal identity,
- public repository URLs,
- requested amount or credits,
- license answer,
- exact final text,
- side effect: public or private submission to the named program.

