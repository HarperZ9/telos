# Spec: Workstation Substrate Intake

## Objective
Expose a public-safe Telos substrate intake register for the two large local workspaces so future sessions can keep assessing older, private, local-only, creative, defensive, and research tools without publishing private paths, payloads, credentials, signing material, or local runbooks.

## Requirements
- [x] Record current Index aggregate evidence for the operator development root and operator profile root.
- [x] Represent sensitive/private areas as lane families, not raw path lists or file names.
- [x] Expose the register as a host-neutral Telos CLI and MCP/catalog tool.
- [x] Connect each lane family to one or more of the five flagships and a safe first action.
- [x] Update status, manifest, README/current-state docs, and tests.

## Technical Approach
Add a JSON register under `demo/integrations/`, a small read-only `demo/workstation-substrate.mjs` command, MCP/catalog entries, manifest/status wiring, tests, and docs. The JSON should carry aggregate Index counts and root labels, but no absolute private paths or raw local artifact names.

## Files to Modify
- `C:\dev\public\telos\demo\integrations\workstation-substrate.json` - public-safe aggregate intake register.
- `C:\dev\public\telos\demo\workstation-substrate.mjs` - read-only CLI summary/JSON command.
- `C:\dev\public\telos\demo\workstation-substrate.test.mjs` - contract tests.
- `C:\dev\public\telos\demo\telos-mcp.mjs` and related tests - MCP exposure.
- `C:\dev\public\telos\demo\integrations\mcp-tool-catalog.json` and `mcp-server-manifest.json` - host catalog exposure.
- `C:\dev\public\telos\demo\status.mjs`, README, and current-state docs - presentation update.
- `C:\dev\public\telos\.github\workflows\ci.yml` - CI coverage for the new contract.

## Success Criteria
- [x] `node demo\workstation-substrate.mjs --summary` reports two mapped roots and no private path strings.
- [x] `node --test demo\workstation-substrate.test.mjs demo\telos-mcp.test.mjs demo\server-manifest.test.mjs demo\operator-scripts.test.mjs demo\project-current-state-docs.test.mjs` passes.
- [x] The fail-fast local CI-equivalent command passes.
- [x] `git diff --check` passes and staged content contains no credential material.

## Blockers
None identified.

## Verification Evidence
- Index aggregate extraction for the development root: 124 repositories, 114 public-class, 10 local-class, 93 dirty, root SHA256 prefix `99e773d965f606c9`, generated `2026-06-29T00:49:59-07:00`.
- Index aggregate extraction for the operator-profile root: 207 repositories, 49 public-class, 158 local-class, 240 dirty, root SHA256 prefix `b79886309f93e63a`, generated `2026-06-29T00:50:16-07:00`.
- `node demo\workstation-substrate.mjs --summary` reports roots `2`, repos `331`, public `163`, local `168`, dirty `333`, lanes `8`, verdict `MATCH`.
- Focused test run passed: `node --test demo\workstation-substrate.test.mjs demo\telos-mcp.test.mjs demo\server-manifest.test.mjs demo\operator-scripts.test.mjs demo\project-current-state-docs.test.mjs demo\integrations.test.mjs demo\rendering-research.test.mjs demo\mcp-freshness.test.mjs`.
- Fail-fast local CI-equivalent command passed all Telos contract tests plus catalog, server manifest, room, and flagship workflow smoke commands.
- `git diff --check` passed. The pre-stage credential-material scan matched only a forbidden-string assertion inside `demo/workstation-substrate.test.mjs`; no credential values or key material were present.

## Status: IMPLEMENTED
