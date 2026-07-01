# Telos Browser Evidence Kernel - Design Spec

Date: 2026-07-01
Status: draft for operator review
Home: `C:\dev\public\telos`
Scope: `gather`, `index`, `telos`, `forum`, `crucible`, `learn`, `buildlang`, `emet`

## Objective

Integrate the best useful parts of `vibheksoni/stealth-browser-mcp` into the Project Telos pipeline natively, with a stronger contract than a standalone browser MCP server.

The target is fluid browser automation for real work, research, extraction, tutoring support, scientific and creative workflows, and repeatable verification. Browser actions should be easy to launch and inspect, while every meaningful actuation leaves a durable evidence packet that the rest of the pipeline can route, index, verify, and witness.

This is not a direct port. Telos should import the good engineering ideas: CDP-backed sessions, DOM extraction, screenshots, element/style capture, network summaries, file-backed large artifacts, and MCP-friendly command shape. Telos should replace anti-bot framing, arbitrary dynamic hooks, and unbounded CDP execution with typed workflows, action receipts, local artifact refs, and `MATCH` / `DRIFT` / `UNVERIFIABLE` verification.

## Current Evidence

These facts were verified in the local workspace during the planning pass.

- `telos` is on branch `feat/learn-render` and already exposes `telos.native.control` in the MCP catalog.
- `demo/native-control.mjs` is the current Telos native control surface for browser CDP and Windows UI Automation.
- `demo/native-control/browser.mjs` launches or attaches to a dedicated Telos Chrome automation profile, never the operator's default profile, and uses synthetic renderer events rather than the OS cursor or keyboard.
- `demo/integrations/action-receipt-conventions.json` defines `project-telos.action-receipt/v1` with proposed/admitted/executed state separation, side-effect classes, typed stop reasons, append-only persistence, and verification verdicts.
- `learn` already has `src/actuation/native-driver.mjs`, which imports Telos native control lazily through `LEARN_NATIVE_CONTROL`.
- `learn` currently keeps credential `assess` steps hard-human while allowing `witnessed-auto` submission for operator-authorized logistics.
- `gather` already has a `browser` adapter, but it shells out to a headless browser and records only `browser-extract`.
- `index` already emits `project-telos.context-envelope/v1` packets with evidence refs and freshness roots.
- `forum` already uses a replayable, hash-chained ledger and emits `project-telos.action-receipt/v1` submit receipts.
- `crucible` already consumes Telos witnessed artifacts, Gather digests, and Index verification records through measurement interfaces.
- `emet` exists at `C:\dev\public\pubscan\emet` as a Python package named `emet` with byte-level `anchor`, `verify`, `coherence`, `corroborate`, `audit`, and `selftest` commands.
- The local public BuildLang surfaces found in this workspace are editor-facing repos: `buildlang-tmLanguage` and `buildlang-vscode`. The compiler repository is referenced by those repos but was not found as `C:\dev\public\buildlang`.
- The upstream `stealth-browser-mcp` clone at `C:\tmp\stealth-browser-mcp` was fetched current at commit `d96a9c6`, and its README currently advertises anti-bot bypass, CDP extraction, network interception, dynamic hooks, and modular MCP tools.

## Design Position

Telos owns the browser substrate. Other tools consume evidence packets and action receipts; they do not each grow their own browser control stack.

The core product shape is a Telos Browser Evidence Kernel layered on top of `telos.native.control`. It turns a browser action from "I clicked something" into "this typed action was admitted, executed in a dedicated automation profile, observed before and after, stored with artifact hashes, and made available to Gather, Index, Forum, Crucible, Learn, BuildLang, and Emet."

This keeps browser automation general-purpose. It is not only a learning tool. The same substrate must support `work-actuate` workflows where Telos completes authorized work end-to-end, and `research-capture` workflows where Telos gathers source state without writing externally.

`learn` remains a special consumer because human credential provenance matters. Learn may use the browser kernel for study, tutoring aids, course navigation, source capture, and witnessed logistical submission. Credential `assess` remains human-only unless a later spec explicitly changes that model. General work automation belongs in the Telos `work-actuate` lane, not by weakening Learn's credential boundary.

## Core Packet

Add `project-telos.browser-evidence/v1`.

Minimum packet shape:

```json
{
  "schema": "project-telos.browser-evidence/v1",
  "tool": "telos.browser.evidence",
  "mode": "work-actuate",
  "session_ref": "browser-session:...",
  "target_ref": "url-digest:sha256:...",
  "action_receipt_ref": "receipt:...",
  "action": {
    "kind": "browser.navigate",
    "selector": null,
    "args_hash": "sha256:..."
  },
  "before": {
    "url": "https://example.com",
    "url_digest": "sha256:...",
    "title": "Example",
    "dom_snapshot_ref": "artifact:...",
    "text_digest": "sha256:...",
    "screenshot_ref": "artifact:..."
  },
  "after": {
    "url": "https://example.com/done",
    "url_digest": "sha256:...",
    "title": "Done",
    "dom_snapshot_ref": "artifact:...",
    "text_digest": "sha256:...",
    "screenshot_ref": "artifact:..."
  },
  "network_summary_ref": "artifact:...",
  "console_summary_ref": "artifact:...",
  "artifact_hashes": [],
  "redaction_status": "redacted",
  "side_effect": {
    "class": "read",
    "external_write": false,
    "reversible": true
  },
  "verification": {
    "verdict": "MATCH",
    "ref": "crucible:..."
  },
  "created_at": "2026-07-01T00:00:00Z"
}
```

Required `mode` values:

- `work-actuate`: authorized automation for ordinary work tasks, including form fill, submission, site operation, and workflow completion.
- `research-capture`: read-only browsing, source intake, screenshots, DOM/text extraction, and network observation.
- `credential-logistics`: learning or credential workflow navigation, capture, completion checks, or operator-authorized non-assessment submission.
- `credential-assess`: human assessment state. Telos may witness or halt; Learn does not auto-answer or auto-complete this mode.
- `lab-assess`: owned benchmarks, internal evals, synthetic labs, or tool tests where automated answers and submissions are allowed.
- `creative-capture`: element/style/media capture for rendering, design, BuildLang examples, or creative-engine work.

## Browser Verbs

The first kernel layer should extend the existing browser verbs instead of replacing them.

Initial verbs:

- `browser.session.start`
- `browser.session.close`
- `browser.navigate`
- `browser.action.click`
- `browser.action.type`
- `browser.action.fill`
- `browser.action.focus`
- `browser.wait_for`
- `browser.snapshot.dom`
- `browser.snapshot.visual`
- `browser.snapshot.text`
- `browser.element.extract`
- `browser.network.summary`
- `browser.console.summary`
- `browser.workflow.run`
- `browser.receipt.export`

The first implementation slice may make `network.summary` and `console.summary` explicit `UNVERIFIABLE` placeholders if no event collector has been attached yet. That is better than silently omitting them or implying a capture that did not happen.

## Artifact Storage

Browser evidence can become large. The kernel should write artifacts locally and return refs plus hashes.

Artifact classes:

- DOM snapshot JSON or HTML.
- Visible text snapshot.
- Screenshot PNG.
- Element extraction JSON: selector, bounding box, attributes, computed style subset, inner text digest, and asset refs.
- Network summary JSON: URL digests, methods, status codes, resource types, timing, and redaction status.
- Console summary JSON: level, message digest, source location when available.
- Workflow run JSON: ordered browser evidence packet refs.

Artifact refs must not require raw private payloads to cross the model boundary. Hosts can show refs, hashes, verdicts, and summaries; local tools can re-open full artifacts when authorized.

## Upstream Feature Triage

Carry forward:

- CDP browser operation.
- Dedicated browser profiles.
- Fast text insertion and synthetic input.
- Screenshot capture.
- DOM and element extraction.
- CSS/style extraction for build and creative workflows.
- Network observation and response metadata summaries.
- Large-response-to-file pattern.
- MCP-friendly small verbs and modular capability discovery.
- Allowlisted local file upload patterns, after a separate upload policy spec.

Do not carry forward as native defaults:

- Anti-bot or bypass framing.
- Arbitrary AI-written dynamic Python hooks.
- Unbounded generic CDP command execution exposed to hosts.
- Raw cookie dumping as a routine model-facing capability.
- Response-body capture without redaction and artifact policy.
- Claims that a browser action is safe or verified without an action receipt and evidence refs.

If request blocking, redirecting, or response mocking is needed, it should be lab-only, declarative, fixture-backed, and separately marked as `lab-assess` or `synthetic-capture`.

## Pipeline Responsibilities

### Telos

Telos provides the kernel, CLI/MCP catalog entries, action receipts, and artifact refs.

Telos should add:

- `telos.browser.evidence` for packet shape and fixture output.
- `telos.browser.workflow` for ordered browser automation with receipts.
- `telos.native.control` catalog updates that advertise the evidence layer.
- Tests proving browser evidence packets preserve mode, side-effect class, artifact hashes, redaction status, and verification verdict.

### Gather

Gather consumes browser evidence as a richer browser source.

The existing `browser-extract` method should remain valid. A Telos-backed source can emit the same `Item` text plus metadata containing `browser_evidence_ref`, `dom_snapshot_ref`, `screenshot_ref`, and `network_summary_ref`.

Gather does not decide whether a page claim is true. It records how content was obtained and feeds receipts downstream.

### Index

Index includes browser evidence refs in context envelopes.

The context envelope should keep raw DOM and screenshots out of the model packet by default, but retain source refs, hashes, selection summaries, and artifact handles that a later local run can expand.

### Forum

Forum routes browser workflows as first-class tasks.

The router should distinguish read-only capture, work actuation, learning logistics, lab evals, and creative capture. The ledger records browser evidence refs as task results or upstream context, so a later run can resume without reconstructing browser state from prose.

### Crucible

Crucible verifies claims over browser evidence.

The first adapter should treat a browser evidence packet like a Telos witnessed artifact: malformed packet is `UNVERIFIABLE`, missing artifact is `UNVERIFIABLE`, hash mismatch is `DRIFT`, and a matching artifact hash with expected mode/side-effect class is `MATCH` for the evidence-integrity claim. Crucible still needs a specific measurement to verify semantic claims about the web page.

### Learn

Learn uses the kernel without becoming the kernel.

Allowed default uses:

- Source capture for study.
- Retrieval practice from captured material.
- Tutor receipts linking source snapshots to practice prompts.
- Course navigation and capture.
- `witnessed-auto` submission for non-assessment logistics.
- Telos visualization aid receipts.

Default boundary:

- Credential `assess` remains a hard human gate.
- Learn does not auto-fill or auto-answer human credential assessment.
- General work automation uses Telos `work-actuate`, not Learn's credential runner.

### BuildLang

BuildLang's local public surface is editor support today, so the first integration is a consumer/export target.

Browser evidence can generate:

- `.bld` examples that describe browser workflows as typed effects.
- Syntax-highlighted fixtures for `buildlang-tmLanguage` and `buildlang-vscode`.
- Future compiler-facing workflow specs when the language runtime is available locally.

The first spec should avoid claiming compiler integration until the compiler repository is present and inspected.

### Emet

Emet acts as an external witness, not a browser controller.

Emet can:

- Anchor exported evidence bundles.
- Verify exported evidence files against anchors.
- Corroborate artifact read paths where available.
- Audit its own witness log.

Emet should not mutate browser artifacts, decide browser policy, or replace Telos action receipts.

## Data Flow

Read-only capture:

1. Forum routes request to `research-capture`.
2. Telos starts or attaches to the dedicated browser profile.
3. Telos navigates and captures DOM/text/screenshot/network summary.
4. Telos emits browser evidence packet and action receipt.
5. Gather imports text and provenance with evidence refs.
6. Index includes evidence refs in a context envelope.
7. Crucible verifies evidence integrity or semantic claims as separate measurements.
8. Emet optionally anchors the exported bundle.

Work actuation:

1. Forum routes request to `work-actuate`.
2. Telos records proposed action, policy decision, and side-effect class.
3. Telos captures before state.
4. Telos performs action.
5. Telos captures after state.
6. Telos emits action receipt plus browser evidence packet.
7. Forum ledger records completion, failure, or required compensation.
8. Crucible can check the receipt and evidence packet.

Learn credential logistics:

1. Learn runner classifies step.
2. `assess` halts for the operator.
3. Non-assessment browser steps call Telos native control.
4. Telos evidence refs enrich Learn's ledger.
5. Learn receipt separates automated logistics, human assessment, and aid visualizations.

## Error Handling

All failures should be typed.

Required failure codes:

- `browser_unavailable`
- `debug_endpoint_unavailable`
- `target_not_found`
- `navigation_failed`
- `selector_not_found`
- `action_denied`
- `artifact_write_failed`
- `artifact_hash_mismatch`
- `network_capture_unavailable`
- `console_capture_unavailable`
- `redaction_required`
- `mode_policy_conflict`
- `credential_assess_halt`
- `verification_unverifiable`

Failure handling rules:

- A missing capture is `UNVERIFIABLE`, not success.
- A hash mismatch is `DRIFT`.
- A denied action records an action receipt with `result.state = failed` or `cancelled`.
- External writes require before/after refs.
- Compensation is append-only; no receipt is rewritten.
- Raw secrets, cookies, tokens, `.env` values, and private payloads must not appear in model-facing summaries.

## Testing Strategy

Telos first slice:

- Unit-test pure packet builders.
- Unit-test hash/ref generation.
- Unit-test receipt mode and side-effect classification.
- Unit-test `native-control` help/catalog includes new evidence verbs.
- Keep live browser tests optional and skipped unless a debug browser is available.

Cross-tool adapter tests:

- Gather fixture imports a browser evidence packet and preserves `browser-extract` plus evidence refs.
- Index fixture includes browser evidence refs without raw DOM leakage.
- Forum fixture routes browser automation prompts into `research-capture`, `work-actuate`, `credential-logistics`, or `creative-capture`.
- Crucible fixture verifies packet integrity: `MATCH`, `DRIFT`, and `UNVERIFIABLE`.
- Learn fixture proves `assess` still halts and browser logistics can carry evidence refs.
- Emet fixture anchors and verifies an exported browser evidence bundle.
- BuildLang fixture uses browser evidence to generate an editor-support `.bld` example only.

## Implementation Phases

Phase 0: design and review.

- Commit this spec.
- Confirm operator review.
- Write an implementation plan with repo-by-repo tasks and tests.

Phase 1: Telos packet and CLI foundation.

- Add browser evidence packet builder.
- Add artifact hashing helpers.
- Extend `native-control` with DOM/text/screenshot evidence exports.
- Add `browser.receipt.export`.
- Update catalog and MCP tests.

Phase 2: Gather and Learn consumers.

- Add Telos-backed Gather browser source.
- Enrich Learn `NativeDriver.capture` and runner ledger entries with evidence refs.
- Preserve Learn's human assessment boundary.

Phase 3: Index, Forum, and Crucible.

- Add context-envelope support for browser evidence refs.
- Add Forum route labels and ledger examples for browser workflows.
- Add Crucible browser evidence integrity measurement.

Phase 4: BuildLang and Emet.

- Add BuildLang browser workflow example generation for editor fixtures.
- Add Emet export/anchor recipe for evidence bundles.

Phase 5: polish and live smoke.

- Add an operator-run browser smoke using a harmless local or public page.
- Verify artifacts render and hashes re-check.
- Add docs that explain how to use browser automation for work without confusing it with Learn credential assessment.

## Success Criteria

- Telos emits `project-telos.browser-evidence/v1` packets with artifact refs and hashes.
- Browser evidence packets join to `project-telos.action-receipt/v1`.
- At least one read-only browser capture path works without raw DOM in model-facing summaries.
- At least one work-actuation receipt records before/after evidence refs.
- Gather can ingest Telos browser evidence as source provenance.
- Index can preserve browser evidence refs in context envelopes.
- Forum can route browser automation workflows by mode.
- Crucible can verify browser evidence packet integrity.
- Learn still halts credential `assess` steps by default.
- Emet can anchor or verify exported evidence artifacts.
- BuildLang integration is limited to verified local editor-support surfaces until the compiler repo is present.
- Upstream `stealth-browser-mcp` useful concepts are represented natively without importing bypass framing or arbitrary hook execution.

## Non-Goals

- Do not build a separate browser stack per flagship.
- Do not port the upstream project wholesale.
- Do not expose arbitrary CDP command execution as a default host-facing tool.
- Do not expose raw cookies, tokens, or local secrets.
- Do not claim semantic truth from a browser capture alone.
- Do not weaken Learn's human credential assessment boundary in this spec.
- Do not claim BuildLang compiler integration until the compiler repo is available and inspected.

## Review Gate

This spec is ready for operator review when it does four things clearly:

- Names Telos as the browser evidence owner.
- Separates general work automation from Learn credential assessment.
- Gives every named tool a concrete role in the pipeline.
- Defines a small enough first slice to implement and verify without broad, speculative rewrites.

After review, the next artifact should be an implementation plan with exact files, tests, and commit boundaries.
