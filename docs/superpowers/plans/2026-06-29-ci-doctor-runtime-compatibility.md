# CI Doctor Runtime Compatibility Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a native Telos CI doctor that surfaces GitHub Actions runtime/action compatibility and latest flagship CI state as a receipt-backed CLI/MCP contract.

**Architecture:** Follow existing Telos integration shape: one JSON register, one small CLI wrapper, one MCP tool, catalog/manifest/status wiring, focused tests, and docs. The register is read-only and privacy-safe; it stores workflow filenames and public CI metadata, not logs, tokens, secrets, or raw private paths.

**Tech Stack:** Node.js ESM scripts, JSON integration packets, GitHub CLI evidence, existing Telos contract tests.

## Global Constraints

- ASCII-only edits unless an existing file requires otherwise.
- Read-only tool: no workflow mutation, no GitHub API writes, no external side effects.
- No raw logs, tokens, secrets, credentials, or private paths in the public register.
- Node 24 compatibility is modeled as a receipt, not as a deployment gate.

---

### Task 1: Contract And CLI Test

**Files:**
- Create: `demo/ci-doctor.test.mjs`

**Interfaces:**
- Consumes: `demo/integrations/ci-doctor.json`, `demo/ci-doctor.mjs`
- Produces: assertions for `project-telos.ci-doctor/v1`, summary output, and privacy boundaries.

- [ ] **Step 1: Write the failing test**

Create `demo/ci-doctor.test.mjs` with assertions that the register has schema `project-telos.ci-doctor/v1`, tool `telos.ci.doctor`, five flagships, nine workflows, latest CI verdict `MATCH`, Node 24 migration verdict `MATCH`, and no forbidden private or secret strings.

- [ ] **Step 2: Run test to verify it fails**

Run: `node demo/ci-doctor.test.mjs`
Expected: FAIL because `demo/integrations/ci-doctor.json` and `demo/ci-doctor.mjs` do not exist yet.

### Task 2: Register And CLI

**Files:**
- Create: `demo/integrations/ci-doctor.json`
- Create: `demo/ci-doctor.mjs`

**Interfaces:**
- Produces: `summary(value)` and default JSON output.

- [ ] **Step 1: Add the JSON register**

Create `demo/integrations/ci-doctor.json` with aggregate counts, flagship run evidence, workflow scan evidence, action baseline tags, compatibility checks, failure classes, privacy boundary, and next actions.

- [ ] **Step 2: Add the CLI wrapper**

Create `demo/ci-doctor.mjs` that reads the JSON packet and supports `--summary` with compact lines for schema, tool, flagships, workflows, latest CI, Node 24, verdict, and next command.

- [ ] **Step 3: Run the focused test**

Run: `node demo/ci-doctor.test.mjs`
Expected: PASS.

### Task 3: MCP And Catalog Wiring

**Files:**
- Modify: `demo/telos-mcp.mjs`
- Modify: `demo/telos-mcp.test.mjs`
- Modify: `demo/integrations/mcp-tool-catalog.json`
- Modify: `demo/integrations/mcp-server-manifest.json`
- Modify: `demo/status.mjs`
- Modify: `demo/integrations.test.mjs`
- Modify: `demo/operator-scripts.test.mjs`
- Modify: `demo/rendering-research.test.mjs`
- Modify: `demo/server-manifest.test.mjs`

**Interfaces:**
- Consumes: `demo/ci-doctor.mjs`
- Produces: `telos.ci.doctor` MCP tool and 54-tool/26-Telos-tool status.

- [ ] **Step 1: Wire the tool**

Add `telos.ci.doctor` to Telos MCP tools, tool scripts, catalog, manifest expected tools, and status command lists.

- [ ] **Step 2: Update focused tests**

Update counts from 53 to 54 and Telos count from 25 to 26 where the tests assert catalog, manifest, or status summaries.

- [ ] **Step 3: Run focused tests**

Run: `node demo/ci-doctor.test.mjs && node demo/telos-mcp.test.mjs && node demo/integrations.test.mjs && node demo/operator-scripts.test.mjs && node demo/rendering-research.test.mjs && node demo/server-manifest.test.mjs`
Expected: PASS.

### Task 4: Docs And CI Workflow

**Files:**
- Modify: `.github/workflows/ci.yml`
- Modify: `README.md`
- Modify: `docs/CURRENT-STATE.md`
- Modify: `demo/integrations/README.md`
- Modify: `demo/project-current-state-docs.test.mjs`

**Interfaces:**
- Consumes: `telos.ci.doctor`
- Produces: documented command/MCP surface and CI coverage.

- [ ] **Step 1: Add docs**

Document `node demo/ci-doctor.mjs --summary`, `telos.ci.doctor`, current five-flagship CI status, and Node 24 compatibility evidence.

- [ ] **Step 2: Add the CI test**

Add `node demo/ci-doctor.test.mjs` to `.github/workflows/ci.yml`.

- [ ] **Step 3: Run docs and workflow-equivalent tests**

Run the focused tests plus the local workflow-equivalent Telos test slice.
Expected: PASS.
