# CI Doctor Runtime Compatibility Spec

Status: IMPLEMENTED

## Purpose

Add a native Telos CI doctor surface that turns GitHub Actions runner/runtime drift into a first-class receipt instead of a manual changelog chase.

## Evidence

- Index map of the public development root generated at `2026-06-29T01:02:24-07:00`: 52 repositories, 48 public-class, 4 local-class, dirty count 0, root prefix `92ef331e0850ccf6`.
- Forum route for the CI doctor request: `project-telos`, confidence `0.6`, `needs_escalation: false`, with `ci-cd` as a secondary candidate.
- Five flagship workflow scan: 9 workflow files across Gather, Crucible, Index, Forum, and Telos.
- Latest flagship CI runs inspected through `gh run list`: all five latest `CI` runs are completed with `success`.
- Current action release tags queried through `gh api`: `actions/checkout@v7.0.0`, `actions/setup-node@v6.4.0`, `actions/setup-python@v6.3.0`, `actions/upload-artifact@v7.0.1`, `actions/download-artifact@v8.0.1`.
- GitHub Actions Node 20 deprecation changelog confirms the native migration path: `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24=true` for early Node 24 testing, Node 24 default beginning `2026-06-16`, and `ACTIONS_ALLOW_USE_UNSECURE_NODE_VERSION=true` only as a temporary Node 20 opt-out.

## Requirements

- [x] Create `project-telos.ci-doctor/v1` as a privacy-safe JSON register.
- [x] Expose the register as `node demo/ci-doctor.mjs` and `node demo/ci-doctor.mjs --summary`.
- [x] Expose the same register through `telos.ci.doctor`.
- [x] Record latest CI status for the five flagships without raw logs, tokens, or private paths.
- [x] Record workflow compatibility checks for Node 24 migration: latest action majors, `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24`, Node 24 where a Node setup step exists, and known third-party release action status.
- [x] Route follow-up failure classes to Index, Forum, Crucible, and Telos.
- [x] Update the catalog, manifest, status, README, integration README, current-state docs, and CI workflow tests.

## Success Criteria

- [x] `node demo/ci-doctor.mjs --summary` prints a compact status with 5 flagships, 9 workflows, verdict `MATCH`, and next command.
- [x] `node demo/ci-doctor.test.mjs` proves schema, counts, CI status, compatibility checks, privacy boundaries, and leak guards.
- [x] `demo/telos-mcp.test.mjs` proves `telos.ci.doctor` returns the same JSON as the CLI payload.
- [x] Existing catalog, manifest, status, docs, and freshness tests reflect the new 54-tool/26-Telos-tool surface.

## Verification

- `node demo/ci-doctor.test.mjs` passed after the red test failed on the missing register.
- The follow-up scanner red test failed on the missing `scanLocalWorkflows` export, then passed after implementing local workflow scanning.
- A matrix-version regression test caught YAML matrix values being parsed as `[` and `${{`; the scanner now ignores expressions and extracts concrete quoted array values.
- `node demo/ci-doctor.mjs --scan-root .. --summary` returns `project-telos.ci-doctor-workflow-observation/v1` with local workflow counts and Node 24 compatibility status without GitHub writes or raw workflow bodies.
- Negative scanner fixtures assert distinct `node_runtime_drift`, `action_major_drift`, and `workflow_evidence_unjoinable` codes, including aggregate `failure_codes`.
- Focused surface tests passed: `demo/telos-mcp.test.mjs`, `demo/integrations.test.mjs`, `demo/operator-scripts.test.mjs`, `demo/rendering-research.test.mjs`, `demo/server-manifest.test.mjs`, and `demo/project-current-state-docs.test.mjs`.
- `node demo/catalog.mjs --summary` reports 54 total and 54 available tools, with 26 Telos tools.
- `node demo/server-manifest.mjs --summary` reports 54 expected tools, with 26 Telos tools.
