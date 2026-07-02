# Project Telos Flagship Operator Spine - Design Spec

Date: 2026-06-27
Status: draft for operator review
Home: `C:\dev\public\telos`
Scope: `gather`, `crucible`, `index`, `forum`, `telos`

## Objective

Make the five public flagships feel like one coherent operator surface without collapsing them into one repo or one transport.

The target is an action-to-action workflow:

1. Every tool can run alone.
2. Every tool emits a stable machine-readable receipt when asked.
3. Every meaningful action carries enough provenance for the next tool to continue without the operator re-explaining the context.
4. Every claim, map, route, digest, certificate, and handoff can be rechecked or honestly marked `UNVERIFIABLE`.
5. The whole loop improves AI workflows natively, with provenance as a first-class product feature rather than a reporting afterthought.

This spec starts the update by defining the shared contract and implementation sequence. It intentionally comes before code changes so the next pass has a tight target.

## Current Evidence

These facts were verified in the local workspace during the planning pass.

- `gather` is a zero-dependency Python CLI package named `gather-engine` at version `1.5.0`. Its CLI exposes `parse`, `video`, `web`, `feed`, `docs`, `arxiv`, `pdf`, `api`, `browser`, `ocr`, `transcribe`, `run`, and `corpus`.
- `crucible` is a zero-dependency Python CLI package named `crucible-bench` at version `1.1.0`. Its CLI exposes `register`, `export`, `assess`, `steelman`, `measure`, `run`, `refine`, `registry`, `verdicts`, `recheck`, `review`, `report`, `batch`, and `drift`.
- `index` is a zero-dependency Python CLI package named `index-graph`. Its CLI exposes `map`, `graph`, `context`, `viz`, `atlas`, `internals`, `check`, `snapshot`, `drift`, `router`, `verify`, and `mcp`.
- `forum` is a zero-dependency Python CLI package named `forum-engine` at version `1.12.0`. Its CLI exposes `route`, `submit`, `serve`, `mcp`, `ledger`, and `bench`.
- `telos` currently has a runnable zero-dependency demo via `node demo/run.mjs`, which emits an expected certified path and an expected unverifiable path.
- Full local test baselines were green for `gather` (`166 passed`), `crucible` (`212 passed, 1 skipped`), and `forum` (`250 passed, 2 skipped`).
- `index` has one known stale test failure: `tests/test_viz_theme.py::test_theme_has_dark_serious_palette` still expects the pre-Telos dark palette while current `theme.py`, brand assets, and `tests/test_atlas_html.py` use the newer Telos palette.
- `gather docs` on `C:\dev\project-docs\outreach\dispatch-ready\2026-06-26-1627\flagship-dogfood-loop.md` produced a document receipt with source SHA-256 `943480010451d8e311be64b25a2acbbb8d310809a15427a6e9666ecfea30aa88` and digest seal `74b019bb6e836b077778909b921ccad6b18d4ad975ff936a5cd19b6f90e9ff41`.
- `forum route` on a cross-flagship product-work request returned low confidence and escalation, which is useful product evidence: Forum should recognize Project Telos action classes and fail into a clearer next action.
- The recent `flagship-dogfood-loop.md` already names the intended rhythm: `index` maps, `forum` routes, `gather` intakes, `crucible` verifies, and `telos` demonstrates receipts.

## Imported Principles

The current design inherits these principles from `C:\dev\project-docs`.

- From `VISION.md`: one operation, the reconcile, turns artifacts into witnessed forms, checks them against a criterion they did not author, carries proof, and says `UNVERIFIABLE` when proof is not available.
- From `TELOS-NORTH-STAR.md`: Telos is the shared accountable room and the productization factory; the factory should prove itself by productizing the corpus through its own tools.
- From `SPRINT-2026-06-24-wrapup-and-next.md`: the flagships are peers, each standalone and compatible. Telos is the engine substrate, not a rank above the others.
- From `RESEARCH-TO-TOOL-2026-06-23.md`: research only counts when it feeds back into a tool, a test, a receipt, or an explicit honest bound.
- From `2026-06-20-the-reconcile-universal-spine.md`: verdict logic must not launder confidence into truth. Fail closed. Never create a false verified state.
- From the publish/outreach packets: action artifacts should be concrete, reviewable, approval-ready, and separated by role: target corpus, checklist, public copy, receipts, and operator next actions.

## Product Shape

The Operator Spine is not a sixth flagship. It is the shared protocol, UX grammar, and test harness that lets the five flagships compose naturally.

The spine has three layers.

1. Tool-local layer: each repo keeps its own identity, CLI, docs, tests, and release cadence.
2. Shared contract layer: each tool emits a compatible action receipt and accepts compatible upstream receipts where that is meaningful.
3. Telos room layer: Telos presents the action stream as the shared surface where operator and model can perceive, act, verify, and continue.

No repo should import sibling internals to appear integrated. Integration happens through public JSON contracts, local files, stdin/stdout, HTTP, MCP, or future native bridge messages.

## Tool Roles

`gather` is perception and intake.

- Normalize local docs, web pages, feeds, PDFs, APIs, browser captures, OCR, and transcripts into receipts.
- Emit digest seals and source hashes that downstream tools can cite.
- Produce a "next intake" hint when a source is incomplete, stale, duplicated, or out of scope.

`index` is structure and context.

- Map workspace, repo, module, and dependency shape.
- Emit graph receipts, snapshots, drift reports, and salience hints.
- Supply context packs that tell a model what matters without relying on memory.

`forum` is orchestration and routing.

- Classify the action, choose the next work surface, track budget, and write a ledger.
- Escalate clearly when no confident route exists.
- Treat low confidence as a useful action state, not a vague failure.

`crucible` is verification and pressure.

- Turn claims into falsifiable theses.
- Assess, steelman, measure, report, and recheck.
- Mark unsupported claims as `UNVERIFIABLE`, not weakly persuasive.

`telos` is reconciliation and shared room.

- Bind the action stream into a witnessed surface.
- Demonstrate certified and unverifiable paths.
- Own the cross-flagship contract, golden workflow, and native application bridge.

## Shared Action Contract

Every flagship should support a stable JSON action envelope for machine use. Human output can stay crafted, but `--json` must stay parseable, quiet, and schema-versioned.

Required envelope:

```json
{
  "schema": "project-telos.flagship-action/v1",
  "tool": "index",
  "tool_version": "2.8.0",
  "command": "map",
  "status": "MATCH",
  "started_at": "2026-06-27T00:00:00Z",
  "finished_at": "2026-06-27T00:00:01Z",
  "inputs": [],
  "outputs": [],
  "receipts": [],
  "native": {},
  "next_actions": [],
  "diagnostics": []
}
```

Allowed `status` values for the shared layer:

- `MATCH`: action succeeded and evidence matches the criterion.
- `DRIFT`: action succeeded but evidence differs from the expected baseline.
- `UNVERIFIABLE`: action could not establish the claim, state, or proof.
- `ERROR`: the tool failed before producing a meaningful verdict.

Native verdicts remain preserved under `native.status` when a tool uses a richer local vocabulary such as `CERTIFIED`, `REFUTED`, or route confidence.

Required receipt fields when a receipt exists:

```json
{
  "kind": "document",
  "ref": "C:\\dev\\project-docs\\...",
  "method": "file-read",
  "sha256": "943480010451d8e311be64b25a2acbbb8d310809a15427a6e9666ecfea30aa88",
  "seal": "74b019bb6e836b077778909b921ccad6b18d4ad975ff936a5cd19b6f90e9ff41",
  "derived_from": []
}
```

Required `next_actions` fields:

```json
{
  "tool": "crucible",
  "action": "assess",
  "reason": "public claim needs falsifiable verification before publish",
  "inputs": ["receipt:74b019bb6e836b077778909b921ccad6b18d4ad975ff936a5cd19b6f90e9ff41"],
  "priority": "normal"
}
```

## Action-To-Action Workflow

The golden workflow for flagship development should become:

1. `index map` generates the workspace or repo map.
2. `gather docs` ingests the relevant roadmap, spec, issue, source packet, or external research.
3. `forum route` chooses the next action class and records escalation when confidence is low.
4. `crucible assess` checks the claims that will be repeated in docs, release copy, demos, or public packets.
5. `telos` reconciles the action chain into a certificate-style report and shared room event.

Each step emits `next_actions`, so the operator can continue from the last receipt instead of reconstructing the workflow from memory.

The first golden workflow fixture should be this exact update path:

- map the five repos,
- gather the dogfood-loop and north-star docs,
- route the flagship improvement request,
- assess the design spec's falsifiable claims,
- produce a Telos receipt for the resulting spec.

## UX Requirements

Command line UX:

- Each tool gets `doctor`, `status`, and `demo` commands or exact equivalents.
- Every command that can emit JSON supports `--json`.
- JSON mode never prints progress bars, color codes, banners, or mixed human prose.
- Human mode prints the verdict first, then evidence, then next action.
- Errors name the failed input, the failed criterion, and a next recovery action.

Surface UX:

- Demos and generated HTML must be keyboard reachable, screen-reader labeled, and usable without color as the only signal.
- Long-running work should show phase, current artifact, elapsed time, and a resumable receipt path.
- Low confidence and `UNVERIFIABLE` should feel like honest system states, not broken UX.
- Generated pages must avoid text overlap, preserve focus states, and expose action history.

Operator UX:

- Every action should answer: what happened, what evidence backs it, what changed, what can be rechecked, and what should happen next.
- The operator should never have to remember which tool comes next for a routine five-flagship loop.
- The model should receive minimized, receipt-backed context instead of raw workspace sprawl.

## Performance And Efficiency Requirements

- Keep zero-dependency cores where they already exist.
- Use bounded parallel IO for independent scans.
- Cache only with visible invalidation, source hashes, and drift checks.
- Avoid re-reading unchanged corpora when a receipt seal already proves the same input.
- Keep targeted test slices under roughly 10 seconds where possible.
- Do not widen to full suites unless a shared base, protocol contract, or cross-tool workflow changed.
- Prefer streaming or JSONL for large action histories.

## Compatibility Requirements

- Contracts must work over CLI files, stdout, stdin, HTTP, MCP, and future WebView2 bridge messages.
- Paths must normalize across Windows and POSIX without erasing the original reference.
- Offline local workflows must remain first-class.
- Unknown schema versions must fail into `UNVERIFIABLE` or `ERROR` with a clear diagnostic.
- Public JSON must not include secrets, `.env` values, tokens, or private client data.

## Accessibility Requirements

- Every interactive control in demos has a label, focus state, and keyboard path.
- Status is conveyed by text and structure, not color alone.
- Motion can be paused or reduced in visual demos.
- Tables and ledgers expose headings and row identity.
- CLI output has a concise plain-text fallback for terminals without color.

## Implementation Phases

Phase 0: design and baseline.

- Commit this spec in Telos.
- Record the current test and dogfood evidence.
- Treat the stale `index` palette test as the first known repair.

Phase 1: per-tool operator commands.

- Add or normalize `doctor`, `status`, and `demo` across the five tools.
- Add schema-versioned JSON envelopes where missing.
- Add conformance tests for quiet JSON mode.

Phase 2: action receipt adapters.

- Add a lightweight `project-telos.flagship-action/v1` emitter in each repo.
- Preserve native tool payloads under `native`.
- Emit `next_actions` for common continuations.

Phase 3: golden dogfood workflow.

- Build a fixture that runs index -> gather -> forum -> crucible -> telos on a small local packet.
- Save receipts, seals, verdicts, and a final report.
- Make the workflow runnable from each flagship and from Telos.

Phase 4: UX hardening.

- Add accessibility checks for demo HTML and generated reports.
- Add performance budgets for workspace scans, digest generation, routing, and assessment.
- Replace vague low-confidence states with explicit operator choices.

Phase 5: Telos room integration.

- Render the action stream in the Telos shared room.
- Let the operator inspect receipts, replay checks, and continue the next action.
- Keep the native bridge transport-agnostic by speaking the same action contract.

## Initial Backlog

1. Fix `index` `tests/test_viz_theme.py` to match the Telos UI kit palette already used by implementation and adjacent tests.
2. Add a small shared schema fixture to Telos for `project-telos.flagship-action/v1`.
3. Add `doctor/status/demo` parity audit for all five repos.
4. Add a `forum` route fixture for Project Telos cross-flagship work so low confidence becomes a named action class.
5. Add `gather` run config for recurring public and project-doc intake.
6. Add `crucible` thesis pack for repeated public claims about the five tools.
7. Add a Telos golden workflow demo that consumes receipts from all four peer tools.
8. Add accessibility checks for all existing demo HTML.
9. Split oversized implementation files only when touching them for behavior, beginning with CLI or demo files that block the operator-spine work.

## Success Criteria

- Each flagship still works standalone.
- Each flagship emits a compatible JSON action envelope for at least one primary command.
- The golden workflow runs locally without network.
- The workflow produces at least one gather receipt, one index map receipt, one forum route or escalation receipt, one crucible assessment, and one Telos reconciliation report.
- The stale `index` palette test is repaired and targeted tests are green for changed behavior.
- Demo and report surfaces pass keyboard and label checks.
- Unknown, stale, or unsupported evidence is reported as `UNVERIFIABLE`, `DRIFT`, or `ERROR`; never as success.
- No new dependency is added without a written reason.

## Non-Goals

- Do not merge the five tools into one package.
- Do not require a single transport such as MCP or HTTP.
- Do not hide each tool's native vocabulary.
- Do not build a large dashboard before the action contract exists.
- Do not claim end-to-end verification where the tool only produced routing, confidence, or convenience output.

## Review Gate

This spec is ready for operator review when:

- It accurately reflects the recent project-docs design principles.
- It gives each flagship a clear role in the larger body of work.
- It defines a small enough first contract to implement without architectural drift.
- It makes dogfooding part of the action loop rather than a separate report.

After review, the next artifact should be an implementation plan with repo-by-repo steps, targeted tests, and commit boundaries.
