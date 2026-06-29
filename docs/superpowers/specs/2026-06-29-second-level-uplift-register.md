# Spec: Second-Level Uplift Register Refresh

## Objective
Refresh the Project Telos second-level flagship queue from the current `C:/dev` workspace map so older, adjacent, forked, and local-only tools continue to move toward the five flagship architecture with evidence, privacy boundaries, and first adapter actions.

## Requirements
- [x] Use current Index evidence for the workspace substrate instead of stale repository counts.
- [x] Add public-safe candidates that clearly feed the five flagships: accountability substrate, accountable surface, telemetry kernels, signal kernels, and reward proxy observability.
- [x] Keep private/local-only details represented as lane families, not raw private paths or payloads.
- [x] Preserve the queue contract: public candidates need a README receipt, flagship hosts, value, risk boundary, and first action.
- [x] Update tests and docs so the queue is executable and visible through Telos.

## Technical Approach
Update `demo/integrations/second-level-flagship-queue.json` and its tests. Keep this as a public-safe metadata registry rather than importing code. Use README SHA256 receipts for each new public candidate and leave any private viability detail outside git.

## Files to Modify
- `C:\dev\public\telos\demo\integrations\second-level-flagship-queue.json` - refresh evidence and add public-safe candidates.
- `C:\dev\public\telos\demo\second-level-flagship-queue.test.mjs` - assert new queue entries and updated public count.
- `C:\dev\public\telos\docs\QUALITY-TOOL-REVIVAL.md` - document the refreshed queue lanes.
- `C:\dev\public\telos\docs\superpowers\specs\2026-06-29-second-level-uplift-register.md` - record status and verification.

## Success Criteria
- [x] `node --test demo\second-level-flagship-queue.test.mjs` passes.
- [x] `node demo\second-level-flagship-queue.mjs --summary` reports the updated public candidate count.
- [x] `node --test demo\operator-scripts.test.mjs demo\project-current-state-docs.test.mjs` passes.
- [x] Git diff checks pass and changed content contains no credential material.

## Blockers
None identified.

## Verification Evidence
- Index MCP map over `C:\dev` reported 123 repositories: 113 public-class, 10 local-class, 93 dirty, root SHA256 prefix `99e773d965f606c9`.
- `node demo\second-level-flagship-queue.mjs --summary` reports `public          15` and `private_tranche 5`.
- Fail-fast local CI-equivalent Telos run completed all contract tests listed in `.github/workflows/ci.yml`, plus the new `mcp-freshness`, `project-current-state-docs`, and `second-level-flagship-queue` tests, then ran catalog, server manifest, room, and workflow smoke commands.
- `git diff --check` passed. The changed-content credential scan only matched benign documentation terms such as `secret-redact-io`, `credentials`, and `credential collection`; no credential values or key material were present.

## Status: IMPLEMENTED
