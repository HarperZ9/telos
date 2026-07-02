# Spec: Proof Lane 1, Agent Action Proof Packet

Date: 2026-07-02
Status: spec ready for implementation
Home: `C:\dev\public\telos` (implementation branch `feat/proof-lane-agent-action`)
Scope: `demo/proof.mjs`, `demo/proof.test.mjs`, `demo/integrations/proof-packet-conventions.json`, `demo/telos-mcp.mjs`, count-pinned tests and docs
Premise: operator master plan roadmap (2026-07-02), Agent Action Proof Packet is delivery order 1. The market wedge is: traces explain runs; receipts justify actions.

## Objective

Ship the first proof lane: a frozen agent-action proof packet contract, a zero-dependency CLI that assembles and verifies packets, a read-only MCP tool that emits the fixture demo packet, a verifier that can actually fail, an optional Emet witness stage that is never faked, and a frozen export mapping to the proof-surface `agent-action-proof-packet/v0` contract.

The packet composes the existing Telos contracts by reference. It does not duplicate them:

- `project-telos.action-receipt/v1` supplies the action join, admission and authority model, side-effect classes, typed stop reasons, and append-only compensation.
- `project-telos.context-envelope/v1` supplies the source-ref and context-ref shapes.
- `project-telos.loop-ledger/v1` supplies the optional durable loop join.

Flow, per the roadmap: source -> context -> route -> admitted action -> verifier -> Emet witness.

## Verified Seams

Every seam below was checked against the actual code at `origin/main` commit `441e746` on 2026-07-02. Corrections to the working premise are labeled.

- Conventions pattern: `demo/integrations/action-receipt-conventions.json` top-level keys are `schema`, `verified_on`, `purpose`, `sources_checked`, `source_corrections`, `contract`, `trace_relation`, `state_model`, `external_action_kinds`, `required_fields`, `adapter_interfaces`, `conformance_fixture`, `failure_codes` (exactly 20), `negative_test_cases`. Confidence: high.
- MCP registration: `demo/telos-mcp.mjs` holds a `tools` array (37 entries today) and a `toolScripts` Map; `runTool` spawns `node demo/<script>` with `cwd` at the repo root and parses stdout as JSON into `structuredContent`. Every description must match the `telos-mcp.test.mjs` regexes: starts with `Use `, contains `Read-only`, `zero-auth`, `no external side effects`, and `Returns `. `inputSchema` is the shared empty object schema. Confidence: high.
- Correction on counts: `demo/telos-mcp.test.mjs` iterates named tools and pins no numeric count. The number 65 is the five-flagship catalog total (`demo/integrations/mcp-tool-catalog.json` has 65 tool entries). The Telos server count 37 is pinned by regex in `operator-scripts.test.mjs:101` and `rendering-research.test.mjs:133`. Adding `telos.proof` moves 65 to 66 and 37 to 38. The full pin list is in "Count Pins" below. Confidence: high.
- CI: `.github/workflows/ci.yml` checks out `gather`, `crucible`, `index`, and `forum` as siblings of `telos`, uses Node 24 and Python 3.11, runs an explicit list of test files (a new test file must be added to the list by hand), then runs `catalog.mjs --summary`, `server-manifest.mjs --summary`, `room.mjs --json`, and `flagship-workflow.mjs` as smoke. `flagship-workflow.mjs` resolves flagship checkouts at the parent directory of the Telos root and hard-fails when they are absent; verified by running it in the isolated worktree. Local CI parity from a worktree requires sibling junctions (see "CI And Local Verification"). Confidence: high.
- In-repo specs honored: `docs/superpowers/specs/2026-06-28-atp-adapter-validation.md` (digest refs instead of raw payloads, policy decision separate from verification verdict, compensation as a new event, negative cases per failure code) and `docs/superpowers/specs/2026-06-27-oss-proof-showcase-design.md` (receipts readable without hidden session state, operator-gated publication, `not_verified` style disclosure, CLI JSON first with MCP after the file contract is stable). Confidence: high.
- proof-surface conformance target: `c:/dev/public/proof-surface` main (`e14d3cb`), `src/proof_surface/agent_action/packet.py` pins `PACKET_VERSION = "agent-action-proof-packet/v0"` and `ROOT_FIELDS` of exactly 15 names: `version`, `packet_id`, `claim`, `scope`, `sources`, `context`, `actions`, `admission`, `side_effects`, `outputs`, `evidence_refs`, `failure_labels`, `verdicts`, `uncertainty`, `decision_summary`. Admission decisions are `allow`, `deny`, `needs-human`. Side-effect classes are `read`, `write`, `external`, `irreversible`. Digests are bare 64-hex (no `sha256:` prefix; `_HEX64` regex). The validators also reject authority-shaped language and forbidden authorization-suppression field names. Confidence: high.
- Emet reachability: `c:/dev/public/pubscan/emet/impl/js/emet.js` exists and runs. A sibling checkout at `../emet` does not exist today. `emet coherence --json <source> <view>` compares exact raw bytes and emits a JSON envelope with keys `command`, `emet_version` (`1.0.0`), `exit_code`, `reason`, `spec_version`, `subject`, `verdict`. Coherence verdicts are `COHERENT`, `VIEW_DIFFERS_FROM_SOURCE`, `UNVERIFIABLE`. Exit codes: 0 pass, 1 negative finding, 2 unverifiable, 3 markers, 64 usage. Confidence: high.
- Flagship gates (`docs/FLAGSHIP-STATE-GOAL.md`): CLI JSON parity with MCP stdio, typed schemas, `MATCH`/`DRIFT`/`UNVERIFIABLE` verdicts, no secrets, no unverified claims. Confidence: high.
- Canonicalization precedent: `demo/context-pack.mjs` exports `stableStringify` (sorted-key, whitespace-free serialization) and `sha256` returning `sha256:<64hex>`. The proof lane reuses this exact pattern. Confidence: high.

## Deliverables

New files:

- `demo/integrations/proof-packet-conventions.json` (frozen contract, schema `project-telos.proof-packet/v1`)
- `demo/proof.mjs` (CLI: assemble, verify, export)
- `demo/proof.test.mjs` (tests, added to CI)
- `docs/superpowers/specs/2026-07-02-proof-lane-agent-action.md` (this spec)

Modified files: `demo/telos-mcp.mjs`, `demo/telos-mcp.test.mjs`, `demo/integrations/mcp-tool-catalog.json`, `demo/integrations/mcp-server-manifest.json`, `demo/status.mjs`, `demo/operator-scripts.test.mjs`, `demo/rendering-research.test.mjs`, `demo/server-manifest.test.mjs`, `demo/compatibility-doctor.test.mjs`, `demo/project-current-state-docs.test.mjs`, `.github/workflows/ci.yml`, `README.md`, `docs/CURRENT-STATE.md`, `CHANGELOG.md`, `demo/integrations/README.md`, `demo/README.md`.

Zero runtime dependencies: Node >= 20 stdlib only (`node:crypto`, `node:fs`, `node:path`, `node:child_process`, `node:os`, `node:url`). No em-dashes or en-dashes in any new or edited text.

## Contract File: proof-packet-conventions.json

Mirrors the `action-receipt-conventions.json` layout exactly:

- `schema`: `"project-telos.proof-packet/v1"`
- `verified_on`: `"2026-07-02"`
- `purpose`: one sentence; the packet is the durable, independently re-checkable justification for one admitted agent action, joining source, context, route, admission, execution, outputs, verification, and witness by reference.
- `sources_checked`: the three joined Telos conventions (by repo path and schema id), the proof-surface `agent-action-proof-packet/v0` contract (by repo path and commit), and the Emet SPEC (by repo path). No URLs are invented; local paths are honest sources here.
- `contract`: booleans and one-line invariants: `joins_by_reference_only: true`, `raw_payloads_required: false`, `digest_references_required: true`, `admission_before_execution_required: true`, `compensation_path_required_for_external_writes: true`, `witness_never_fabricated: true`, `verdict_derived_not_asserted: true`, `canonical_hash_excludes_wall_clock: true`, `verification_required: "Every packet verdict is MATCH, DRIFT, or UNVERIFIABLE."`
- `state_model`: `verification_verdicts` (`MATCH`, `DRIFT`, `UNVERIFIABLE`); `witness_statuses` (`witnessed`, `unavailable`); `witness_verdicts` (`MATCH`, `DRIFT`, `UNVERIFIABLE`); by reference: `admission_decisions`, `side_effect_classes`, `result_states`, `typed_stop_reasons` each declared as `"see project-telos.action-receipt/v1 state_model"` plus a copied value list so the file is self-contained for hosts (copied lists are labeled `copied_from: "project-telos.action-receipt/v1"`).
- `required_fields`: the packet field list below.
- `adapter_interfaces`: `assembler` (accepts a fixture, returns a canonical packet plus `packet_hash`), `verifier` (accepts a packet, returns named check results and a derived verdict), `witness` (accepts source and view byte paths, returns the Emet envelope or an unavailability record), `exporter` (accepts a packet, returns a proof-surface v0 shaped object).
- `export_contract`: `target_schema: "agent-action-proof-packet/v0"`, `proof_surface_root_fields`: the frozen 15-name list, `digest_form: "bare-64-hex"`, plus the decision map and class map tables from "Export Mapping" below.
- `conformance_fixture`: `happy_path` (the complete demo packet materials, including inline `artifacts` so digest recomputation is self-contained) and tampered variants used by tests: `tampered_output_digest`, `missing_admission`, `missing_source_ref`, `execution_before_admission`, `external_write_without_compensation`, `embedded_canned_match`.
- `failure_codes`: the 10 codes in "Verifier Rules".
- `negative_test_cases`: one entry per failure code, named like the action-receipt convention (`name` + `failure_code`).

## Packet Schema (field by field)

The packet has a hashed materials scope and an unhashed result scope. Hash scope: every field except `packet_hash`, `verifier`, `witness`, and `wall_clock`.

| Field | Shape | Joins / value source |
| --- | --- | --- |
| `schema` | const `"project-telos.proof-packet/v1"` | this contract |
| `packet_id` | string, from fixture (demo: `prfpkt_20260702_001`) | none |
| `objective` | `{ claim, scope, success_criterion }` | roadmap minimum field "Objective"; `scope` also feeds the export `scope` |
| `source_refs[]` | `{ id, ref, content_hash }` | shape from `project-telos.context-envelope/v1` `source_refs`; refs name gather-style receipts; roadmap "Source refs" |
| `context_refs[]` | `{ envelope_id, envelope_hash }` | joins `project-telos.context-envelope/v1` by id and hash; roadmap "Context refs" |
| `route` | `{ lane, decided_by, confidence, route_ref }` | joins a forum route receipt by ref and digest; roadmap "Route" |
| `admission` | `{ action_id, decision, policy_ref, authority_ref, admitted_ordinal }` | joins `project-telos.action-receipt/v1` `authority` and `policy` blocks by `action_id`; `decision` values are the action-receipt `policy_decisions`; roadmap "Authority/admission" |
| `action` | `{ action_id, event_id, tool_id, action_kind, args_hash, executed_ordinal, idempotency_key }` | joins `project-telos.action-receipt/v1` by `action_id` and `event_id`; `action_kind` from `external_action_kinds` when external; roadmap "Tool call" |
| `side_effect` | `{ class, reversible }` | values from action-receipt `state_model.side_effect_classes`; roadmap "Side-effect class" |
| `compensation` | `{ required, ref }` | joins action-receipt `compensation_ref` and the append-only compensation contract; `required` must be true when `class` is `write`, `external_call`, or `mixed`; roadmap "Compensation path" |
| `outputs[]` | `{ name, digest, ref }` | `digest` is `sha256:<64hex>` over the named artifact bytes; roadmap "Output digest" |
| `artifacts` | `{ <name>: <string material> }` | fixture-embedded artifact bodies so `check.artifact_digests` recomputes locally with no network |
| `final_status` | `{ state, stop_reason }` | values from action-receipt `result_states` and `typed_stop_reasons`; roadmap "Final status" |
| `ledger_ref` | optional `{ entry_id, ledger_hash }` | joins `project-telos.loop-ledger/v1` |
| `packet_hash` | `sha256:<64hex>` | over `stableStringify` of the hash scope; unhashed itself |
| `verifier` | `{ checks[], failures[], verdict }` | roadmap "Verifier"; appended after hashing, outside hash scope |
| `witness` | `{ status, verdict, reason?, emet_version?, spec_version?, exit_code?, subject? }` | Emet stage record, outside hash scope |
| `wall_clock` | `{ assembled_at }` | outside hash scope; pinned from the fixture in `--demo` mode |

Ordering is modeled with integer ordinals (`admitted_ordinal`, `executed_ordinal`), not timestamps, so the admission-before-execution check is deterministic and the hash scope carries no wall-clock values.

## Canonical Form And Determinism

- Canonical bytes: `stableStringify` (reuse the `context-pack.mjs` pattern: arrays in order, object keys sorted, no whitespace) over the hash scope.
- `packet_hash = "sha256:" + sha256(canonicalBytes)`.
- Same fixture in, byte-identical canonical packet out, every time, on every machine. No `Date.now()`, no `Math.random()`, no environment-dependent values inside the hash scope.
- `--out` writes `packet.json` (full packet) and `packet.canonical.json` (canonical hash-scope bytes, the witness source).

## CLI Surface

`node demo/proof.mjs <subcommand>`; JSON output on `--json`, compact human summary otherwise; every generated path printed once.

- `node demo/proof.mjs agent-action --demo [--out <dir>] [--json]`: assemble the packet from the `happy_path` conformance fixture, run the verifier, attempt the witness stage, print the packet. Exit 0 when the derived verdict is `MATCH`, 1 on `DRIFT`, 2 on `UNVERIFIABLE` (mirrors Emet exit codes).
- `node demo/proof.mjs agent-action --fixture <path> [--out <dir>] [--json]`: same pipeline over an operator-supplied fixture file.
- `node demo/proof.mjs verify <packet.json> [--json]`: replay. Re-runs required-field validation, state-model legality, digest recomputation over the packet's own materials, admission ordering, compensation-path presence, verdict derivation, and (if reachable) the Emet witness. Prints `MATCH`, `DRIFT`, or `UNVERIFIABLE` with the failure list. Exit codes as above.
- `node demo/proof.mjs export <packet.json> [--json]`: print the `toProofSurfacePacket()` output. Not exposed over MCP.

The module exports `assemblePacket(fixture)`, `verifyPacket(packet, options)`, `toProofSurfacePacket(packet)`, and `stableStringify` for tests.

## MCP Tool: telos.proof

- Entry appended to `tools` in `demo/telos-mcp.mjs` (position: after `telos.showcase.scout`, keeping registration order stable):
  - name: `telos.proof`
  - description: `Use when a host needs the fixture-backed agent-action proof packet joining source refs, context refs, route, admission, side effects, output digests, verifier checks, and the Emet witness stage. Read-only, zero-auth, no external side effects beyond local subprocess reads. Returns a JSON agent-action proof packet.` (satisfies every description regex in `telos-mcp.test.mjs`; the subprocess disclosure follows the `telos.workflow` precedent)
  - inputSchema: the shared empty object schema.
- `toolScripts` entry: `["telos.proof", ["proof.mjs", "agent-action", "--demo", "--json"]]`. The MCP tool emits the fixture demo packet only: no arguments, no file writes, no network. The witness stage inside `--demo` is a local read-only subprocess and records `unavailable` honestly when no Emet implementation is reachable.
- Parity gate: the MCP `structuredContent` must deep-equal the CLI `--json` stdout for the same invocation (it does by construction, since `runTool` parses the same stdout; the test asserts it anyway).

## Verifier Rules (each check named, each failure typed)

The verifier is a pure function from packet to check results. The verdict is derived by one fold over the results; there is no code path that returns a literal `MATCH` without a passing check set. Tampered packets produce `DRIFT` with the actual deltas; missing evidence produces `UNVERIFIABLE` with the missing item named by JSON path.

| Check | Failure code | Verdict on failure | Failure payload |
| --- | --- | --- | --- |
| `check.required_fields` | `missing_required_field` | UNVERIFIABLE | each missing JSON path, named |
| `check.state_model` | `state_model_violation` | DRIFT | field path, observed value, allowed set |
| `check.packet_hash` | `packet_hash_mismatch` | DRIFT | expected hash, observed hash |
| `check.artifact_digests` | `artifact_digest_mismatch` | DRIFT | output name, expected digest, recomputed digest |
| `check.admission_join` | `admission_missing_for_action` | DRIFT | the `action_id` with no admission record |
| `check.admission_ordering` | `admission_order_violation` | DRIFT | `admitted_ordinal`, `executed_ordinal` |
| `check.compensation_path` | `compensation_path_missing_for_external_write` | DRIFT | side-effect class, missing `compensation.ref` path |
| `check.evidence_refs` | `evidence_ref_unresolvable` | UNVERIFIABLE | the unresolvable ref, named |
| `check.verdict_derivation` | `embedded_verdict_not_derived` | DRIFT | embedded verdict, derived verdict |
| `stage.witness` | `witness_unavailable` | UNVERIFIABLE (stage level) | reason string |

Verdict roll-up over executed checks: `DRIFT` if any check failed with a DRIFT code, else `UNVERIFIABLE` if any check failed with an UNVERIFIABLE code, else `MATCH`.

Witness roll-up: the witness stage verdict is reported in its own block. When the witness executed, `VIEW_DIFFERS_FROM_SOURCE` lowers the overall verdict to `DRIFT` and a failed spawn of a reachable implementation lowers it to `UNVERIFIABLE`. When no implementation is reachable, the stage records `{ status: "unavailable", verdict: "UNVERIFIABLE", reason: "no emet implementation reachable" }` and the packet-level field `witness_coverage: "not_witnessed"` is set; the overall verdict stays derived from the checks that ran. Rationale: an unavailable optional witness is disclosed coverage loss, not counterevidence, and fabricating a witness verdict in either direction is prohibited by contract (`witness_never_fabricated`). This also keeps `verify` deterministic in CI, where no Emet checkout exists.

## Emet Witness Stage Contract

- Lookup order: `TELOS_EMET_CLI` environment variable (path to a runnable `emet.js` or executable), then `<telosRoot>/../emet/impl/js/emet.js`, then `c:/dev/public/pubscan/emet/impl/js/emet.js`. Today only the third path exists; the first two are honest future seams.
- Invocation: `node <emet.js> coherence --json <source> <view>` where source is the stored `packet.canonical.json` bytes (or, for a bare `verify <packet.json>` with no canonical file next to it, the packet's recorded canonical form re-derived from its own hash scope and written to a temp file under `os.tmpdir()`), and view is the freshly re-derived canonical bytes at verify time, also a temp file. Temp files are removed after the check.
- Recorded envelope: `emet_version`, `spec_version`, `exit_code`, `verdict`, `subject`, and `reason` when present, copied verbatim from Emet's JSON output.
- Mapping: `COHERENT` -> witness verdict `MATCH`; `VIEW_DIFFERS_FROM_SOURCE` -> `DRIFT`; `UNVERIFIABLE` -> `UNVERIFIABLE`. Emet exit codes 0/1/2 correspond; 64 is a usage bug and fails the stage as `UNVERIFIABLE` with the stderr excerpt as reason.
- Never fake a witness: if no implementation is reachable, the stage records exactly `{ status: "unavailable", verdict: "UNVERIFIABLE", reason: "no emet implementation reachable" }`. No cached, guessed, or replayed verdicts.

## toProofSurfacePacket Mapping Table

Target: `agent-action-proof-packet/v0` at proof-surface main `e14d3cb`. The 15 root field names are frozen in `export_contract.proof_surface_root_fields` and asserted by test. proof-surface is never imported or spawned at runtime.

| proof-surface v0 root field | Telos source | Notes |
| --- | --- | --- |
| `version` | const `"agent-action-proof-packet/v0"` | |
| `packet_id` | `packet_id` | |
| `claim` | `objective.claim` | |
| `scope` | `objective.scope` | |
| `sources` | `source_refs[]` as `{ ref, sha256 }` | strip the `sha256:` prefix; proof-surface requires bare 64-hex |
| `context` | `context_refs[]` as `{ ref: envelope_id, sha256: envelope_hash }` | prefix stripped |
| `actions` | `[action]` as `{ action_id, actor, agent, model, tool, action_kind, target, cost, span_digest }` | `tool` from `tool_id`; `span_digest` from `args_hash` stripped; `cost` as `{ tokens, wall_ms }` from the fixture |
| `admission` | `[admission]` as `{ action_id, decision, reasons, authorization_ref }` | decision map below; `authorization_ref` from `authority_ref` |
| `side_effects` | `[side_effect + compensation]` as `{ action_id, class, idempotency_key, compensation: { reversible, rollback_ref }, before_digest, after_digest }` | class map below; digests stripped |
| `outputs` | `outputs[]` as `{ name, sha256 }` | prefix stripped |
| `evidence_refs` | union of `source_refs[].ref`, `context_refs[].envelope_id`, `route.route_ref`, `outputs[].ref`, `ledger_ref.entry_id` when present | |
| `failure_labels` | `verifier.failures[].code` | typed codes only, no free text |
| `verdicts` | `{ overall: verifier.verdict, per_action: [{ action_id, status }] }` | |
| `uncertainty` | disclosed limits: witness coverage when `not_witnessed`, every lossy class mapping applied, refs declared but not dereferenced | |
| `decision_summary` | derived from `route`, `admission.decision`, `final_status` | sub-shape owned by proof-surface `validate_decision_summary`; confirm during implementation with a one-time manual run of the proof-surface validator over the exported demo packet, and record that run in the PR body. Confidence on the sub-shape from reading alone: moderate |

Decision map (action-receipt `policy_decisions` -> proof-surface `ADMISSION_DECISIONS`): `allow` -> `allow`; `block` -> `deny`; `escalate` -> `needs-human`; `require_review` -> `needs-human`.

Class map (action-receipt `side_effect_classes` -> proof-surface `SIDE_EFFECT_CLASSES`): `read` -> `read`; `none` -> `read` (lossy, uncertainty note); `write` -> `write`; `external_call` -> `external`; `human_action` -> `external` (lossy, uncertainty note); `mixed` -> `external` (lossy, uncertainty note); any `write`/`external_call` with `reversible: false` -> `irreversible`.

Language guard: exported text must stay factual and avoid authority-shaped words (no trusted/approved/safe claims), because the proof-surface validators reject them.

## Test List (demo/proof.test.mjs unless noted)

1. Determinism and byte stability: assemble the demo fixture twice; canonical bytes are identical and `packet_hash` is identical; the hash scope contains no wall-clock or random values.
2. Tamper -> DRIFT with deltas: mutate one output digest and one `args_hash` in copies of the demo packet; `verifyPacket` returns `DRIFT`; `failures` contains `artifact_digest_mismatch` and `packet_hash_mismatch` with expected and observed values and the JSON path.
3. Missing evidence -> UNVERIFIABLE named: delete `admission` and, separately, one `source_refs` entry that an output claims as evidence; verdicts are `UNVERIFIABLE` (for the missing required field) and the failure names the exact missing path or ref.
4. Canned-verdict impossibility: a packet carrying an embedded `verifier.verdict: "MATCH"` over tampered materials verifies as `DRIFT`, and `check.verdict_derivation` reports `embedded_verdict_not_derived`; additionally, each conformance negative fixture produces exactly its declared `failure_code`.
5. Admission ordering: the `execution_before_admission` fixture fails with `admission_order_violation`; the `external_write_without_compensation` fixture fails with `compensation_path_missing_for_external_write`.
6. Verify CLI re-check MATCH: run `node demo/proof.mjs agent-action --demo --out <tmp>` then `node demo/proof.mjs verify <tmp>/packet.json --json`; overall verdict is `MATCH`, exit code 0, and `witness.status` is one of `witnessed` or `unavailable` with internally consistent fields (the assertion must pass both with and without a reachable Emet).
7. proof-surface shape conformance: `Object.keys(toProofSurfacePacket(demoPacket))` sorted equals the frozen 15-name root field list; every exported digest matches `^[0-9a-f]{64}$`; every admission decision is in `{allow, deny, needs-human}`; every side-effect class is in `{read, write, external, irreversible}`; lossy mappings appear in `uncertainty`.
8. MCP parity and registration (in `demo/telos-mcp.test.mjs`): `telos.proof` added to the named-tools list and the stdio assertions; a `tools/call` block asserts `structuredContent.schema === "project-telos.proof-packet/v1"`, a stable `packet_id`, a `packet_hash` matching `^sha256:[a-f0-9]{64}$`, and `verifier.verdict === "MATCH"`.
9. Tool-count pins updated: the pinned tests in "Count Pins" below all pass at their new values (they run in CI; no new test needed beyond the edits).
10. Em-dash and en-dash scan: every file added or edited by this lane contains no U+2014 and no U+2013 (read bytes, assert the scan; scope at minimum: the four new files plus every modified file in "Deliverables").
11. Witness honesty: with `TELOS_EMET_CLI` pointed at a nonexistent path and the fallback paths absent (simulated via an env override that disables fallbacks in test mode, or by pointing `TELOS_EMET_CLI` at a directory), the witness block equals the exact unavailability record; no fabricated verdict.
12. No secrets and no raw payloads: the demo packet contains no `.env` content, no token-shaped strings, and carries digests plus refs instead of raw external payloads (mirror the showcase spec's packet hygiene test).

## Count Pins (exact, verified at 441e746)

Update every pin honestly when `telos.proof` lands. Catalog total: 65 -> 66. Telos server tools: 37 -> 38.

| File:line | Current pin | New value |
| --- | --- | --- |
| `demo/compatibility-doctor.test.mjs:220` | `assert.equal(real.metrics.tool_count, 65)` | 66 |
| `demo/operator-scripts.test.mjs:56` | `/65-tool/` | `/66-tool/` |
| `demo/operator-scripts.test.mjs:100` | `/tools\s+65 total, 65 available/` | 66 / 66 |
| `demo/operator-scripts.test.mjs:101` | `/telos\s+37 tools\s+telos.status, telos.doctor/` | 38 |
| `demo/project-current-state-docs.test.mjs:120` | `/65 available tools/i` | 66 |
| `demo/rendering-research.test.mjs:125` | `/65-tool/` | `/66-tool/` |
| `demo/rendering-research.test.mjs:132` | `/tools\s+65 total, 65 available/` | 66 / 66 |
| `demo/rendering-research.test.mjs:133` | `/telos\s+37 tools/` | 38 |
| `demo/rendering-research.test.mjs:140` | `/tools\s+65 expected/` | 66 |
| `demo/server-manifest.test.mjs:68` | `/tools\s+65 expected/` | 66 |

Source-of-truth data feeding those pins (must change together, same commit):

- `demo/integrations/mcp-tool-catalog.json`: add the 66th entry for `telos.proof` under the telos flagship with `cli` (`node demo/proof.mjs agent-action --demo --json`) and `mcp` (`status: "available"`, `method: "tools/call"`); the catalog description must be byte-identical to the MCP description (`telos-mcp.test.mjs` asserts it).
- `demo/integrations/mcp-server-manifest.json`: add `telos.proof` to `servers.telos.expected_tools` (the freshness tool hash is computed from this list at runtime, so no hash constant needs editing) and update `expected_current_status` from `65-tool` to `66-tool` with the new capability named.
- `demo/status.mjs`: add `telos.proof` to `native.mcp_tools` and update `current_status`; this string must remain byte-identical to the manifest `expected_current_status` or `telos.mcp.freshness` reports DRIFT.
- `demo/telos-mcp.mjs`: `tools` array 37 -> 38 entries plus the `toolScripts` entry.
- `README.md:145`: `65 preferred tools` -> `66 preferred tools` (the auxiliary count 12 is unchanged).
- `docs/CURRENT-STATE.md:20`: `65 available tools` -> `66 available tools`, adding `telos.proof` to the named list.
- `CHANGELOG.md`: new entry at the top for the proof lane; never retro-edit the historical 65-count entries at lines 126 and 129.
- `docs/FLAGSHIP-STATE-GOAL.md:14` mentions `63 tools` inside a dated dogfood record; leave it as a historical record.

## CI And Local Verification

- Add `node demo/proof.test.mjs` to the explicit test list in `.github/workflows/ci.yml` (between `node demo/presentation-doctor.test.mjs` and `node demo/project-current-state-docs.test.mjs`, keeping the loose alphabetical order).
- Run what CI runs before every commit: the full test list, then `node demo/catalog.mjs --summary`, `node demo/server-manifest.mjs --summary`, `node demo/room.mjs --json`, `node demo/flagship-workflow.mjs`.
- Worktree caveat (verified by execution): `flagship-workflow.mjs` and `room.mjs` resolve `gather`, `crucible`, `index`, and `forum` at the parent of the Telos root and hard-fail when absent. From `c:/dev/worktrees/telos-proof`, create directory junctions first: `cmd /c mklink /J c:\dev\worktrees\gather c:\dev\public\gather` and likewise for `crucible`, `index`, `forum`. Remove the junctions after verification if desired; they contain no copies.
- CI has no Emet checkout, so the witness stage is `unavailable` there by design; every test must pass in both witness states.

## Doc And README Touchpoints

- `README.md`: add `node demo/proof.mjs` to the command surface list, `telos.proof` to the operator surface list, update the preferred-tool count, and extend the "Proof lane" bullet with one sentence: the agent-action proof packet joins source refs, context, route, admission, side effects, output digests, a verifier that can fail, and an optional Emet witness; replay with `node demo/proof.mjs verify`.
- `docs/CURRENT-STATE.md`: count and named-tool updates as above.
- `CHANGELOG.md`: one new entry describing the contract, CLI, MCP tool, verifier, witness stage, and export mapping, with the honest count change 65 -> 66.
- `demo/integrations/README.md`: one line for `proof-packet-conventions.json`.
- `demo/README.md`: usage block for `proof.mjs` subcommands.
- Commit style (from git log): short imperative subjects (`feat: ...`, `docs: ...`, `test: ...`), trailer `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`. Suggested sequence: `docs: add proof-lane agent-action spec`, `feat: add agent-action proof packet contract and CLI`, `feat: expose telos.proof through telos mcp`, `test: update tool count pins 65->66 for telos.proof`, `docs: record agent-action proof lane`.
- Push only `feat/proof-lane-agent-action`; open a PR against `main`; tagging and publishing stay with the operator.

## Out Of Scope

- Importing or spawning proof-surface at runtime (the export is shape-frozen by fixture instead).
- Live network fetches of any kind; the demo is fixture-backed.
- Signing, anchoring, or storage backends (adapter seams only, per the action-receipt precedent).
- The research, scientific-runtime, learn, and visual lanes (delivery orders 2 and later).
- Editing anything in the operator's main tree at `c:/dev/public/telos` or the PR #18 worktree at `c:/dev/worktrees/telos-ship`.

## Success Criteria

- [ ] `node demo/proof.test.mjs` fails before the contract and CLI exist, passes after.
- [ ] `node demo/proof.mjs agent-action --demo --json` and MCP `tools/call telos.proof` return deep-equal JSON.
- [ ] `node demo/proof.mjs verify` on the untouched demo packet prints `MATCH` and exits 0; on a tampered copy prints `DRIFT` with the actual deltas; on a packet with missing evidence prints `UNVERIFIABLE` naming the missing item.
- [ ] Same fixture assembles to byte-identical canonical packets across runs.
- [ ] `toProofSurfacePacket` output keys equal the frozen 15-field list; digests are bare 64-hex; one manual proof-surface validator run over the exported demo packet is recorded in the PR body.
- [ ] Every count pin in the table above passes at its new value; full CI-equivalent run is green locally before each commit.
- [ ] No em-dashes or en-dashes in any file this lane adds or edits; no secrets; no unverified claims.

## Blockers

None identified. The proof-surface `decision_summary` sub-shape is the one moderate-confidence seam; it is resolved by the one-time manual validator run during implementation.

## Status: SPEC READY
