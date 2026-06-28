# Display Calibration Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a read-only Telos display-calibration contract that promotes Calibrate Pro and Quanta Color into a host-neutral CLI/MCP surface.

**Architecture:** Follow the existing Telos integration pattern: JSON contract, tiny Node CLI wrapper, Telos MCP mapping, catalog/server-manifest parity, docs/status/changelog, and targeted tests. The contract is read-only and does not call monitor APIs or write calibration artifacts.

**Tech Stack:** Node ESM, JSON contracts, Telos MCP stdio runtime, built-in `node:assert/strict`, existing Telos demo test scripts.

## Global Constraints

- Do not mutate monitor settings, DDC/CI, LUTs, ICC profiles, or operating-system color state.
- Do not include purchased fonts, private assets, raw device telemetry, raw reports, or secrets.
- Keep new source files under 300 lines.
- Use `MATCH`, `DRIFT`, and `UNVERIFIABLE` vocabulary for verification boundaries.
- Use `apply_patch` for manual edits.

---

### Task 1: Display Calibration Contract Test

**Files:**
- Create: `C:/dev/public/telos/demo/display-calibration.test.mjs`
- Later create: `C:/dev/public/telos/demo/integrations/display-calibration.json`
- Later create: `C:/dev/public/telos/demo/display-calibration.mjs`

**Interfaces:**
- Consumes: no new runtime code.
- Produces: test expectations for `project-telos.display-calibration/v1` and CLI behavior.

- [ ] **Step 1: Write the failing test**

```js
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { spawnSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const contract = JSON.parse(readFileSync(new URL("./integrations/display-calibration.json", import.meta.url), "utf8"));

assert.equal(contract.schema, "project-telos.display-calibration/v1");
assert.equal(contract.tool, "telos.display.calibration");
assert.equal(contract.contract.hardware_mutation_allowed, false);
assert.ok(contract.sources.some((source) => source.id === "calibrate-pro"));
assert.ok(contract.sources.some((source) => source.id === "quanta-color"));
assert.ok(contract.display_targets.some((target) => target.id === "generic-sdr-reference"));
assert.ok(contract.patch_sets.some((patchSet) => patchSet.id === "colorchecker-24"));
assert.ok(contract.artifact_types.includes("icc-v4-profile-ref"));
assert.ok(contract.measurement_gates.some((gate) => gate.tool === "crucible.measurement_gate"));
assert.match(contract.boundary, /read-only/);

const cli = spawnSync(process.execPath, [path.join(here, "display-calibration.mjs")], {
  cwd: path.resolve(here, ".."),
  encoding: "utf8"
});
assert.equal(cli.status, 0, cli.stderr || cli.stdout);
assert.deepEqual(JSON.parse(cli.stdout), contract);
```

- [ ] **Step 2: Run test to verify it fails**

Run: `node demo/display-calibration.test.mjs`
Expected: FAIL because `demo/integrations/display-calibration.json` does not exist.

### Task 2: Minimal Contract And CLI

**Files:**
- Create: `C:/dev/public/telos/demo/integrations/display-calibration.json`
- Create: `C:/dev/public/telos/demo/display-calibration.mjs`
- Test: `C:/dev/public/telos/demo/display-calibration.test.mjs`

**Interfaces:**
- Consumes: test from Task 1.
- Produces: `telos.display.calibration` JSON payload and CLI summary.

- [ ] **Step 1: Implement the JSON contract**

Create a compact JSON contract with these required roots: `schema`, `tool`, `generated_at`, `contract`, `sources`, `display_targets`, `patch_sets`, `artifact_types`, `measurement_gates`, `privacy`, `boundary`, and `next_actions`.

- [ ] **Step 2: Implement the CLI wrapper**

Create `display-calibration.mjs` that reads the JSON contract, prints full JSON by default, and prints a compact summary when passed `--summary`.

- [ ] **Step 3: Run test to verify it passes**

Run: `node demo/display-calibration.test.mjs`
Expected: PASS.

### Task 3: MCP, Catalog, Status, And Docs

**Files:**
- Modify: `C:/dev/public/telos/demo/telos-mcp.mjs`
- Modify: `C:/dev/public/telos/demo/integrations/mcp-tool-catalog.json`
- Modify: `C:/dev/public/telos/demo/integrations/mcp-server-manifest.json`
- Modify: `C:/dev/public/telos/demo/status.mjs`
- Modify: `C:/dev/public/telos/README.md`
- Modify: `C:/dev/public/telos/demo/integrations/README.md`
- Modify: `C:/dev/public/telos/CHANGELOG.md`
- Modify tests that assert tool count or Telos MCP tool names.

**Interfaces:**
- Consumes: `demo/display-calibration.mjs`.
- Produces: `telos.display.calibration` through CLI, MCP, catalog, manifest, and docs.

- [ ] **Step 1: Add MCP mapping**

Add `telos.display.calibration` to `tools` and `toolScripts` in `demo/telos-mcp.mjs`.

- [ ] **Step 2: Add catalog and server manifest parity**

Add the tool to the Telos section of `mcp-tool-catalog.json` and `mcp-server-manifest.json`. Update expected counts from 45 to 46 and Telos tools from 17 to 18 where tests assert them.

- [ ] **Step 3: Update docs**

Document `node demo/display-calibration.mjs --summary`, the new MCP tool, the Calibrate Pro promotion lane, and the new 46-tool count.

- [ ] **Step 4: Run the targeted verification slice**

Run:

```powershell
node demo/display-calibration.test.mjs; node demo/integrations.test.mjs; node demo/telos-mcp.test.mjs; node demo/server-manifest.test.mjs; node demo/operator-scripts.test.mjs; node demo/rendering-research.test.mjs
```

Expected: all commands exit 0.

### Task 4: Final Verification And Commit

**Files:**
- All files touched above.

**Interfaces:**
- Consumes: Tasks 1-3.
- Produces: pushed commit with CI evidence.

- [ ] **Step 1: Run broader Telos verification**

Run the existing broad Telos demo slice plus `node demo/display-calibration.test.mjs`.

- [ ] **Step 2: Check staged contents**

Run `git diff --check`, `git status --short`, and a staged secret-shape scan before committing.

- [ ] **Step 3: Commit and push**

Commit with `feat: add display calibration contract`, push `main`, then watch the GitHub Actions CI run to completion.
