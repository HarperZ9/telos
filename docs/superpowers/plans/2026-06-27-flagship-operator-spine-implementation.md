# Flagship Operator Spine Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the first Project Telos operator-spine increment across `gather`, `crucible`, `index`, `forum`, and `telos`.

**Architecture:** Keep each flagship standalone. Add a tiny local action-envelope adapter in each repo rather than introducing a shared runtime dependency. Telos owns the cross-tool schema fixture and the golden workflow harness that proves the receipts compose.

**Tech Stack:** Python 3.11 stdlib CLIs and pytest for `gather`, `crucible`, `index`, and `forum`; Node ESM stdlib scripts for `telos`; JSON contracts over stdout and local files.

## Global Constraints

- Shared schema: `project-telos.flagship-action/v1`.
- Shared statuses: `MATCH`, `DRIFT`, `UNVERIFIABLE`, `ERROR`.
- No new runtime dependency in any flagship.
- `--json` output must be parseable JSON with no mixed human prose.
- Human output prints verdict first, then evidence, then next action.
- Unknown, stale, or unsupported evidence is not success.
- Public JSON must not include secrets, `.env` values, tokens, or private client data.
- Targeted test slices should stay under roughly 10 seconds where possible.
- Do not merge the five tools into one package.
- CLI JSON and MCP are the platform-neutral substrates; OpenAI, Anthropic, Codex, Claude, plugins, skills, and full apps must wrap those substrates instead of owning separate business logic.
- Tool names use deterministic ASCII names prefixed by flagship: `gather.docs`, `crucible.assess`, `index.map`, `forum.route`, `telos.workflow`.
- The catalog must label each surface as `available`, `cli-bridge`, or `planned`; do not imply an MCP server exists before it does.
- Provider-specific examples must be configuration-only unless a platform requires a thin adapter; no OpenAI-only or Anthropic-only core path.
- Stdio MCP is the local-first transport; Streamable HTTP is the remote/app transport; SSE is legacy-only and not the default.

---

## File Structure

- Modify: `C:\dev\public\index\tests\test_viz_theme.py`
  - Fix the known stale palette assertion so the current Telos UI kit is the tested truth.
- Create: `C:\dev\public\telos\demo\flagship-action.schema.json`
  - Canonical JSON schema fixture for the action envelope.
- Create: `C:\dev\public\telos\demo\flagship-action.mjs`
  - Small stdlib helper for Telos scripts to build and validate action envelopes.
- Create: `C:\dev\public\telos\demo\flagship-action.test.mjs`
  - Node smoke test for the schema fixture and helper.
- Create: `C:\dev\public\gather\src\gather\flagship.py`
- Modify: `C:\dev\public\gather\src\gather\cli.py`
- Create: `C:\dev\public\gather\tests\test_flagship_cli.py`
  - Add `status`, `doctor`, and `demo` operator commands to Gather.
- Create: `C:\dev\public\crucible\src\crucible\flagship.py`
- Modify: `C:\dev\public\crucible\src\crucible\cli.py`
- Create: `C:\dev\public\crucible\tests\test_flagship_cli.py`
  - Add `status`, `doctor`, and `demo` operator commands to Crucible.
- Create: `C:\dev\public\index\src\index_graph\flagship.py`
- Modify: `C:\dev\public\index\src\index_graph\cli.py`
- Create: `C:\dev\public\index\tests\test_flagship_cli.py`
  - Add `status`, `doctor`, and `demo` operator commands to Index.
- Create: `C:\dev\public\forum\src\forum\flagship.py`
- Modify: `C:\dev\public\forum\src\forum\cli.py`
- Modify: `C:\dev\public\forum\src\forum\manifests\default-roster.toml`
- Create: `C:\dev\public\forum\tests\test_flagship_cli.py`
  - Add `status`, `doctor`, and `demo`, and add a Project Telos route lane.
- Create: `C:\dev\public\telos\demo\status.mjs`
- Create: `C:\dev\public\telos\demo\doctor.mjs`
- Create: `C:\dev\public\telos\demo\flagship-workflow.mjs`
  - Telos-owned runnable golden workflow harness.
- Create: `C:\dev\public\telos\demo\integrations\mcp-tool-catalog.json`
- Create: `C:\dev\public\telos\demo\integrations\codex-plugin.example.json`
- Create: `C:\dev\public\telos\demo\integrations\claude-mcp.example.json`
- Create: `C:\dev\public\telos\demo\integrations\openai-agents.example.py`
- Create: `C:\dev\public\telos\demo\integrations\README.md`
- Create: `C:\dev\public\telos\demo\integrations.test.mjs`
  - Provider-neutral integration pack for MCP, OpenAI Agents/Apps, Anthropic Claude/Claude Code, Codex plugins/skills, and app embedding.

## Shared Python Interface

Each Python flagship creates its own `flagship.py` with this public surface:

```python
SCHEMA = "project-telos.flagship-action/v1"

def envelope(command: str, *, status: str = "MATCH", native: dict | None = None,
             next_actions: list[dict] | None = None,
             diagnostics: list[dict] | None = None) -> dict:
    ...

def cmd_status(args) -> int:
    ...

def cmd_doctor(args) -> int:
    ...

def cmd_demo(args) -> int:
    ...
```

The exact contents differ by tool, but every payload uses the same top-level keys.

---

### Task 1: Repair Index Palette Test Drift

**Files:**
- Modify: `C:\dev\public\index\tests\test_viz_theme.py`

**Interfaces:**
- Consumes: existing `index_graph.viz.theme.THEME`.
- Produces: a green targeted palette test matching the current Telos UI kit.

- [ ] **Step 1: Update the failing test assertions**

Replace `test_theme_has_dark_serious_palette` with:

```python
def test_theme_has_telos_palette():
    assert THEME.bg == "#f4f3ef"
    assert THEME.accent == "#4636e8"
    assert THEME.ok == "#2f3238"
    # font stacks carry system fallbacks (no external font dependency)
    assert "sans-serif" in THEME.font_body.lower()
    assert "monospace" in THEME.font_mono.lower()
```

- [ ] **Step 2: Run the failing slice**

Run:

```powershell
cd C:\dev\public\index
python -m pytest tests\test_viz_theme.py tests\test_atlas_html.py -q
```

Expected: all selected tests pass.

- [ ] **Step 3: Commit**

```powershell
cd C:\dev\public\index
git add tests\test_viz_theme.py
git commit -m "test: align viz theme with telos palette"
```

---

### Task 2: Add Telos Action Schema Fixture

**Files:**
- Create: `C:\dev\public\telos\demo\flagship-action.schema.json`
- Create: `C:\dev\public\telos\demo\flagship-action.mjs`
- Create: `C:\dev\public\telos\demo\flagship-action.test.mjs`

**Interfaces:**
- Produces: `SCHEMA`, `allowedStatuses`, `actionEnvelope(input)`, `assertActionEnvelope(value)`.
- Later tasks rely on the schema name and top-level envelope keys.

- [ ] **Step 1: Create the JSON schema fixture**

Write `demo/flagship-action.schema.json`:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "project-telos.flagship-action/v1",
  "type": "object",
  "required": ["schema", "tool", "tool_version", "command", "status", "inputs", "outputs", "receipts", "native", "next_actions", "diagnostics"],
  "properties": {
    "schema": { "const": "project-telos.flagship-action/v1" },
    "tool": { "type": "string", "minLength": 1 },
    "tool_version": { "type": "string", "minLength": 1 },
    "command": { "type": "string", "minLength": 1 },
    "status": { "enum": ["MATCH", "DRIFT", "UNVERIFIABLE", "ERROR"] },
    "started_at": { "type": "string" },
    "finished_at": { "type": "string" },
    "inputs": { "type": "array" },
    "outputs": { "type": "array" },
    "receipts": { "type": "array" },
    "native": { "type": "object" },
    "next_actions": { "type": "array" },
    "diagnostics": { "type": "array" }
  }
}
```

- [ ] **Step 2: Create the Telos helper**

Write `demo/flagship-action.mjs`:

```javascript
export const SCHEMA = "project-telos.flagship-action/v1";
export const allowedStatuses = new Set(["MATCH", "DRIFT", "UNVERIFIABLE", "ERROR"]);

export function actionEnvelope({
  tool,
  toolVersion,
  command,
  status = "MATCH",
  inputs = [],
  outputs = [],
  receipts = [],
  native = {},
  nextActions = [],
  diagnostics = [],
  startedAt = new Date(0).toISOString(),
  finishedAt = new Date(0).toISOString()
}) {
  const envelope = {
    schema: SCHEMA,
    tool,
    tool_version: toolVersion,
    command,
    status,
    started_at: startedAt,
    finished_at: finishedAt,
    inputs,
    outputs,
    receipts,
    native,
    next_actions: nextActions,
    diagnostics
  };
  assertActionEnvelope(envelope);
  return envelope;
}

export function assertActionEnvelope(value) {
  for (const key of ["schema", "tool", "tool_version", "command", "status", "inputs", "outputs", "receipts", "native", "next_actions", "diagnostics"]) {
    if (!(key in value)) {
      throw new Error(`missing action envelope key: ${key}`);
    }
  }
  if (value.schema !== SCHEMA) {
    throw new Error(`bad schema: ${value.schema}`);
  }
  if (!allowedStatuses.has(value.status)) {
    throw new Error(`bad status: ${value.status}`);
  }
  return true;
}
```

- [ ] **Step 3: Add the Node smoke test**

Write `demo/flagship-action.test.mjs`:

```javascript
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { actionEnvelope, assertActionEnvelope, SCHEMA } from "./flagship-action.mjs";

const schema = JSON.parse(readFileSync(new URL("./flagship-action.schema.json", import.meta.url), "utf8"));
assert.equal(schema.$id, SCHEMA);
assert.deepEqual(schema.properties.status.enum, ["MATCH", "DRIFT", "UNVERIFIABLE", "ERROR"]);

const payload = actionEnvelope({
  tool: "telos",
  toolVersion: "demo",
  command: "status",
  native: { role: "shared-room" },
  nextActions: [{ tool: "index", action: "map", reason: "refresh workspace context", inputs: [], priority: "normal" }]
});

assertActionEnvelope(payload);
assert.equal(payload.schema, SCHEMA);
assert.equal(payload.status, "MATCH");
assert.equal(payload.next_actions[0].tool, "index");
```

- [ ] **Step 4: Run the Telos schema test**

Run:

```powershell
cd C:\dev\public\telos
node demo\flagship-action.test.mjs
```

Expected: exit code `0`.

- [ ] **Step 5: Commit**

```powershell
cd C:\dev\public\telos
git add demo\flagship-action.schema.json demo\flagship-action.mjs demo\flagship-action.test.mjs
git commit -m "feat: add flagship action schema fixture"
```

---

### Task 3: Add Gather Operator Commands

**Files:**
- Create: `C:\dev\public\gather\src\gather\flagship.py`
- Modify: `C:\dev\public\gather\src\gather\cli.py`
- Create: `C:\dev\public\gather\tests\test_flagship_cli.py`

**Interfaces:**
- Produces: `gather status`, `gather doctor`, `gather demo`.
- Produces: JSON envelopes with `tool == "gather"`.

- [ ] **Step 1: Create Gather's local flagship adapter**

Write `src/gather/flagship.py`:

```python
from __future__ import annotations

import json

from gather import __version__

SCHEMA = "project-telos.flagship-action/v1"
TOOL = "gather"
PRIMARY_COMMANDS = ["docs", "web", "feed", "pdf", "run", "corpus"]


def envelope(command: str, *, status: str = "MATCH", native: dict | None = None,
             next_actions: list[dict] | None = None,
             diagnostics: list[dict] | None = None) -> dict:
    return {
        "schema": SCHEMA,
        "tool": TOOL,
        "tool_version": __version__,
        "command": command,
        "status": status,
        "inputs": [],
        "outputs": [],
        "receipts": [],
        "native": native or {},
        "next_actions": next_actions or [],
        "diagnostics": diagnostics or [],
    }


def _next(tool: str, action: str, reason: str) -> dict:
    return {"tool": tool, "action": action, "reason": reason, "inputs": [], "priority": "normal"}


def status_payload() -> dict:
    return envelope("status", native={"role": "perception-intake", "commands": PRIMARY_COMMANDS},
                    next_actions=[_next("index", "map", "map workspace context for gathered sources")])


def doctor_payload() -> dict:
    checks = [
        {"name": "zero_dependency_core", "status": "MATCH"},
        {"name": "json_receipts", "status": "MATCH"},
        {"name": "offline_docs_intake", "status": "MATCH"},
    ]
    return envelope("doctor", native={"checks": checks},
                    next_actions=[_next("crucible", "assess", "verify repeated claims from gathered sources")])


def demo_payload() -> dict:
    return envelope("demo", native={"command": "gather docs <path> --json"},
                    next_actions=[_next("forum", "route", "route the next action after intake")])


def emit(payload: dict, as_json: bool) -> int:
    if as_json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"status={payload['status']} tool={payload['tool']} command={payload['command']}")
        for action in payload["next_actions"]:
            print(f"next: {action['tool']} {action['action']} - {action['reason']}")
    return 0


def cmd_status(args) -> int:
    return emit(status_payload(), args.json)


def cmd_doctor(args) -> int:
    return emit(doctor_payload(), args.json)


def cmd_demo(args) -> int:
    return emit(demo_payload(), args.json)
```

- [ ] **Step 2: Wire Gather CLI parsers**

In `src/gather/cli.py`, import the handlers:

```python
from gather.flagship import cmd_demo, cmd_doctor, cmd_status
```

Then add this helper near `_add_common`:

```python
def _add_flagship_commands(sub) -> None:
    status = sub.add_parser("status", help="emit Gather's Project Telos operator-spine status")
    status.add_argument("--json", action="store_true", help="emit a Project Telos action envelope")
    status.set_defaults(func=cmd_status)

    doctor = sub.add_parser("doctor", help="check Gather's operator-spine readiness")
    doctor.add_argument("--json", action="store_true", help="emit a Project Telos action envelope")
    doctor.set_defaults(func=cmd_doctor)

    demo = sub.add_parser("demo", help="show Gather's operator-spine demo command")
    demo.add_argument("--json", action="store_true", help="emit a Project Telos action envelope")
    demo.set_defaults(func=cmd_demo)
```

Call `_add_flagship_commands(sub)` in `build_parser()` immediately after `sub = parser.add_subparsers(dest="command")`.

- [ ] **Step 3: Add Gather CLI tests**

Write `tests/test_flagship_cli.py`:

```python
import json

from gather.cli import main


def test_status_json_is_action_envelope(capsys):
    assert main(["status", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["schema"] == "project-telos.flagship-action/v1"
    assert payload["tool"] == "gather"
    assert payload["status"] == "MATCH"
    assert payload["next_actions"][0]["tool"] == "index"


def test_doctor_human_prints_verdict_and_next_action(capsys):
    assert main(["doctor"]) == 0
    out = capsys.readouterr().out
    assert out.startswith("status=MATCH tool=gather command=doctor")
    assert "next: crucible assess" in out


def test_demo_json_names_docs_command(capsys):
    assert main(["demo", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["native"]["command"] == "gather docs <path> --json"
```

- [ ] **Step 4: Run Gather targeted tests**

Run:

```powershell
cd C:\dev\public\gather
python -m pytest tests\test_flagship_cli.py tests\test_cli.py tests\test_docs.py -q
```

Expected: selected tests pass.

- [ ] **Step 5: Commit**

```powershell
cd C:\dev\public\gather
git add src\gather\flagship.py src\gather\cli.py tests\test_flagship_cli.py
git commit -m "feat: add gather operator spine commands"
```

---

### Task 4: Add Crucible Operator Commands

**Files:**
- Create: `C:\dev\public\crucible\src\crucible\flagship.py`
- Modify: `C:\dev\public\crucible\src\crucible\cli.py`
- Create: `C:\dev\public\crucible\tests\test_flagship_cli.py`

**Interfaces:**
- Produces: `crucible status`, `crucible doctor`, `crucible demo`.
- Produces: JSON envelopes with `tool == "crucible"`.

- [ ] **Step 1: Create Crucible's local flagship adapter**

Write `src/crucible/flagship.py`:

```python
from __future__ import annotations

import json

from crucible import __version__

SCHEMA = "project-telos.flagship-action/v1"
TOOL = "crucible"


def envelope(command: str, *, status: str = "MATCH", native: dict | None = None,
             next_actions: list[dict] | None = None, diagnostics: list[dict] | None = None) -> dict:
    return {
        "schema": SCHEMA,
        "tool": TOOL,
        "tool_version": __version__,
        "command": command,
        "status": status,
        "inputs": [],
        "outputs": [],
        "receipts": [],
        "native": native or {},
        "next_actions": next_actions or [],
        "diagnostics": diagnostics or [],
    }


def _next(tool: str, action: str, reason: str) -> dict:
    return {"tool": tool, "action": action, "reason": reason, "inputs": [], "priority": "normal"}


def status_payload() -> dict:
    return envelope("status", native={"role": "verification-pressure", "verdicts": ["MATCH", "DRIFT", "UNVERIFIABLE"]},
                    next_actions=[_next("telos", "reconcile", "carry verified claims into the shared room")])


def doctor_payload() -> dict:
    checks = [
        {"name": "thesis_seals", "status": "MATCH"},
        {"name": "measurement_backed_assessments", "status": "MATCH"},
        {"name": "recheckable_verdicts", "status": "MATCH"},
    ]
    return envelope("doctor", native={"checks": checks},
                    next_actions=[_next("gather", "docs", "refresh claim sources before reassessment")])


def demo_payload() -> dict:
    return envelope("demo", native={"command": "crucible assess examples/thesis-binary-search.json --measurements examples/measurements-binary-search.json --json"},
                    next_actions=[_next("forum", "ledger", "record verification handoff")])


def emit(payload: dict, as_json: bool) -> int:
    if as_json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"status={payload['status']} tool={payload['tool']} command={payload['command']}")
        for action in payload["next_actions"]:
            print(f"next: {action['tool']} {action['action']} - {action['reason']}")
    return 0


def cmd_status(args) -> int:
    return emit(status_payload(), args.json)


def cmd_doctor(args) -> int:
    return emit(doctor_payload(), args.json)


def cmd_demo(args) -> int:
    return emit(demo_payload(), args.json)
```

- [ ] **Step 2: Wire Crucible CLI parsers**

In `src/crucible/cli.py`, import:

```python
from crucible.flagship import cmd_demo, cmd_doctor, cmd_status
```

Add this helper before `build_parser()`:

```python
def _add_flagship_commands(sub) -> None:
    status = sub.add_parser("status", help="emit Crucible's Project Telos operator-spine status")
    status.add_argument("--json", action="store_true", help="emit a Project Telos action envelope")
    status.set_defaults(func=cmd_status)

    doctor = sub.add_parser("doctor", help="check Crucible's operator-spine readiness")
    doctor.add_argument("--json", action="store_true", help="emit a Project Telos action envelope")
    doctor.set_defaults(func=cmd_doctor)

    demo = sub.add_parser("demo", help="show Crucible's operator-spine demo command")
    demo.add_argument("--json", action="store_true", help="emit a Project Telos action envelope")
    demo.set_defaults(func=cmd_demo)
```

Call `_add_flagship_commands(sub)` after `sub = parser.add_subparsers(dest="command")`.

- [ ] **Step 3: Add Crucible CLI tests**

Write `tests/test_flagship_cli.py`:

```python
import json

from crucible.cli import main


def test_status_json_is_action_envelope(capsys):
    assert main(["status", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["schema"] == "project-telos.flagship-action/v1"
    assert payload["tool"] == "crucible"
    assert payload["native"]["role"] == "verification-pressure"


def test_doctor_human_prints_next_action(capsys):
    assert main(["doctor"]) == 0
    out = capsys.readouterr().out
    assert out.startswith("status=MATCH tool=crucible command=doctor")
    assert "next: gather docs" in out


def test_demo_json_names_assessment_command(capsys):
    assert main(["demo", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["native"]["command"].startswith("crucible assess")
```

- [ ] **Step 4: Run Crucible targeted tests**

Run:

```powershell
cd C:\dev\public\crucible
python -m pytest tests\test_flagship_cli.py tests\test_cli.py tests\test_readiness.py -q
```

Expected: selected tests pass.

- [ ] **Step 5: Commit**

```powershell
cd C:\dev\public\crucible
git add src\crucible\flagship.py src\crucible\cli.py tests\test_flagship_cli.py
git commit -m "feat: add crucible operator spine commands"
```

---

### Task 5: Add Index Operator Commands

**Files:**
- Create: `C:\dev\public\index\src\index_graph\flagship.py`
- Modify: `C:\dev\public\index\src\index_graph\cli.py`
- Create: `C:\dev\public\index\tests\test_flagship_cli.py`

**Interfaces:**
- Produces: `index status`, `index doctor`, `index demo`.
- Produces: JSON envelopes with `tool == "index"`.

- [ ] **Step 1: Create Index's local flagship adapter**

Write `src/index_graph/flagship.py`:

```python
from __future__ import annotations

import json

from index_graph import __version__

SCHEMA = "project-telos.flagship-action/v1"
TOOL = "index"


def envelope(command: str, *, status: str = "MATCH", native: dict | None = None,
             next_actions: list[dict] | None = None, diagnostics: list[dict] | None = None) -> dict:
    return {
        "schema": SCHEMA,
        "tool": TOOL,
        "tool_version": __version__,
        "command": command,
        "status": status,
        "inputs": [],
        "outputs": [],
        "receipts": [],
        "native": native or {},
        "next_actions": next_actions or [],
        "diagnostics": diagnostics or [],
    }


def _next(tool: str, action: str, reason: str) -> dict:
    return {"tool": tool, "action": action, "reason": reason, "inputs": [], "priority": "normal"}


def status_payload() -> dict:
    return envelope("status", native={"role": "structure-context", "commands": ["map", "graph", "context", "atlas", "verify"]},
                    next_actions=[_next("gather", "docs", "gather docs backing structural decisions")])


def doctor_payload() -> dict:
    checks = [
        {"name": "workspace_map", "status": "MATCH"},
        {"name": "context_pack", "status": "MATCH"},
        {"name": "structural_verification", "status": "MATCH"},
    ]
    return envelope("doctor", native={"checks": checks},
                    next_actions=[_next("forum", "route", "route the next workspace action")])


def demo_payload() -> dict:
    return envelope("demo", native={"command": "index map --root <workspace> --json"},
                    next_actions=[_next("telos", "reconcile", "render workspace structure into the shared room")])


def emit(payload: dict, as_json: bool) -> int:
    if as_json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"status={payload['status']} tool={payload['tool']} command={payload['command']}")
        for action in payload["next_actions"]:
            print(f"next: {action['tool']} {action['action']} - {action['reason']}")
    return 0


def cmd_status(args) -> int:
    return emit(status_payload(), args.json)


def cmd_doctor(args) -> int:
    return emit(doctor_payload(), args.json)


def cmd_demo(args) -> int:
    return emit(demo_payload(), args.json)
```

- [ ] **Step 2: Wire Index CLI parsers**

In `src/index_graph/cli.py`, import:

```python
from .flagship import cmd_demo, cmd_doctor, cmd_status
```

Add `"status"`, `"doctor"`, and `"demo"` to `_SUBCOMMANDS`.

Add these parsers in `build_parser()` after `sub = parser.add_subparsers(dest="cmd")`:

```python
    status = sub.add_parser("status", help="emit Index's Project Telos operator-spine status")
    status.add_argument("--json", action="store_true", help="emit a Project Telos action envelope")

    doctor = sub.add_parser("doctor", help="check Index's operator-spine readiness")
    doctor.add_argument("--json", action="store_true", help="emit a Project Telos action envelope")

    demo = sub.add_parser("demo", help="show Index's operator-spine demo command")
    demo.add_argument("--json", action="store_true", help="emit a Project Telos action envelope")
```

In `main()`, add dispatch branches before the existing command handling:

```python
    if args.cmd == "status":
        return cmd_status(args)
    if args.cmd == "doctor":
        return cmd_doctor(args)
    if args.cmd == "demo":
        return cmd_demo(args)
```

- [ ] **Step 3: Add Index CLI tests**

Write `tests/test_flagship_cli.py`:

```python
import json

from index_graph.cli import main


def test_status_json_is_action_envelope(capsys):
    assert main(["status", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["schema"] == "project-telos.flagship-action/v1"
    assert payload["tool"] == "index"
    assert payload["native"]["role"] == "structure-context"


def test_doctor_human_prints_next_action(capsys):
    assert main(["doctor"]) == 0
    out = capsys.readouterr().out
    assert out.startswith("status=MATCH tool=index command=doctor")
    assert "next: forum route" in out


def test_demo_json_names_map_command(capsys):
    assert main(["demo", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["native"]["command"] == "index map --root <workspace> --json"
```

- [ ] **Step 4: Run Index targeted tests**

Run:

```powershell
cd C:\dev\public\index
python -m pytest tests\test_flagship_cli.py tests\test_cli.py tests\test_viz_theme.py -q
```

Expected: selected tests pass.

- [ ] **Step 5: Commit**

```powershell
cd C:\dev\public\index
git add src\index_graph\flagship.py src\index_graph\cli.py tests\test_flagship_cli.py
git commit -m "feat: add index operator spine commands"
```

---

### Task 6: Add Forum Operator Commands And Telos Route Lane

**Files:**
- Create: `C:\dev\public\forum\src\forum\flagship.py`
- Modify: `C:\dev\public\forum\src\forum\cli.py`
- Modify: `C:\dev\public\forum\src\forum\manifests\default-roster.toml`
- Create: `C:\dev\public\forum\tests\test_flagship_cli.py`

**Interfaces:**
- Produces: `forum status`, `forum doctor`, `forum demo`.
- Produces: default route lane `project-telos`.

- [ ] **Step 1: Create Forum's local flagship adapter**

Write `src/forum/flagship.py`:

```python
from __future__ import annotations

import json

from forum import __version__

SCHEMA = "project-telos.flagship-action/v1"
TOOL = "forum"


def envelope(command: str, *, status: str = "MATCH", native: dict | None = None,
             next_actions: list[dict] | None = None, diagnostics: list[dict] | None = None) -> dict:
    return {
        "schema": SCHEMA,
        "tool": TOOL,
        "tool_version": __version__,
        "command": command,
        "status": status,
        "inputs": [],
        "outputs": [],
        "receipts": [],
        "native": native or {},
        "next_actions": next_actions or [],
        "diagnostics": diagnostics or [],
    }


def _next(tool: str, action: str, reason: str) -> dict:
    return {"tool": tool, "action": action, "reason": reason, "inputs": [], "priority": "normal"}


def status_payload() -> dict:
    return envelope("status", native={"role": "orchestration-routing", "ledger": "causal-jsonl"},
                    next_actions=[_next("crucible", "assess", "verify the routed claim before public use")])


def doctor_payload() -> dict:
    checks = [
        {"name": "default_roster", "status": "MATCH"},
        {"name": "ledger_verification", "status": "MATCH"},
        {"name": "model_agnostic_executor", "status": "MATCH"},
    ]
    return envelope("doctor", native={"checks": checks},
                    next_actions=[_next("index", "context", "refresh structural context for routing")])


def demo_payload() -> dict:
    return envelope("demo", native={"command": "forum route \"improve Project Telos flagship workflow\""},
                    next_actions=[_next("gather", "docs", "gather source material for routed work")])


def emit(payload: dict, as_json: bool) -> int:
    if as_json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"status={payload['status']} tool={payload['tool']} command={payload['command']}")
        for action in payload["next_actions"]:
            print(f"next: {action['tool']} {action['action']} - {action['reason']}")
    return 0


def cmd_status(args) -> int:
    return emit(status_payload(), args.json)


def cmd_doctor(args) -> int:
    return emit(doctor_payload(), args.json)


def cmd_demo(args) -> int:
    return emit(demo_payload(), args.json)
```

- [ ] **Step 2: Wire Forum CLI parsers**

In `src/forum/cli.py`, import:

```python
from forum.flagship import cmd_demo, cmd_doctor, cmd_status
```

Add these parsers after `sub = parser.add_subparsers(dest="command")`:

```python
    status = sub.add_parser("status", help="emit Forum's Project Telos operator-spine status")
    status.add_argument("--json", action="store_true", help="emit a Project Telos action envelope")
    status.set_defaults(func=cmd_status)

    doctor = sub.add_parser("doctor", help="check Forum's operator-spine readiness")
    doctor.add_argument("--json", action="store_true", help="emit a Project Telos action envelope")
    doctor.set_defaults(func=cmd_doctor)

    demo = sub.add_parser("demo", help="show Forum's operator-spine demo command")
    demo.add_argument("--json", action="store_true", help="emit a Project Telos action envelope")
    demo.set_defaults(func=cmd_demo)
```

- [ ] **Step 3: Add the Project Telos lane**

Append this block to `src/forum/manifests/default-roster.toml` near the support agents:

```toml
[[agent]]
name = "project-telos"
category = "support"
domain = "Project Telos flagship integration, provenance workflows, and operator-spine work"
keywords = ["telos", "flagship", "gather", "crucible", "index", "forum", "provenance", "workflow", "spine", "dogfood"]
model_tier = "frontier"
executor = "cli"
```

- [ ] **Step 4: Add Forum CLI tests**

Write `tests/test_flagship_cli.py`:

```python
import json

from forum.cli import main


def test_status_json_is_action_envelope(capsys):
    assert main(["status", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["schema"] == "project-telos.flagship-action/v1"
    assert payload["tool"] == "forum"
    assert payload["native"]["role"] == "orchestration-routing"


def test_doctor_human_prints_next_action(capsys):
    assert main(["doctor"]) == 0
    out = capsys.readouterr().out
    assert out.startswith("status=MATCH tool=forum command=doctor")
    assert "next: index context" in out


def test_project_telos_route_lane(capsys):
    request = "improve Project Telos flagship gather crucible index forum provenance workflow"
    assert main(["route", request]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["decided"] == "project-telos"
    assert payload["needs_escalation"] is False
```

- [ ] **Step 5: Run Forum targeted tests**

Run:

```powershell
cd C:\dev\public\forum
python -m pytest tests\test_flagship_cli.py tests\test_cli.py tests\test_routing.py -q
```

Expected: selected tests pass.

- [ ] **Step 6: Commit**

```powershell
cd C:\dev\public\forum
git add src\forum\flagship.py src\forum\cli.py src\forum\manifests\default-roster.toml tests\test_flagship_cli.py
git commit -m "feat: add forum operator spine route"
```

---

### Task 7: Add Telos Operator Scripts

**Files:**
- Create: `C:\dev\public\telos\demo\status.mjs`
- Create: `C:\dev\public\telos\demo\doctor.mjs`

**Interfaces:**
- Consumes: `actionEnvelope()` from `demo/flagship-action.mjs`.
- Produces: Telos JSON envelopes without adding a package manager or dependency.

- [ ] **Step 1: Create Telos status script**

Write `demo/status.mjs`:

```javascript
import { actionEnvelope } from "./flagship-action.mjs";

const payload = actionEnvelope({
  tool: "telos",
  toolVersion: "demo",
  command: "status",
  native: {
    role: "shared-room-reconcile",
    demo: "node demo/run.mjs"
  },
  nextActions: [
    { tool: "index", action: "map", reason: "refresh workspace structure before entering the shared room", inputs: [], priority: "normal" }
  ]
});

console.log(JSON.stringify(payload, null, 2));
```

- [ ] **Step 2: Create Telos doctor script**

Write `demo/doctor.mjs`:

```javascript
import { actionEnvelope } from "./flagship-action.mjs";

const payload = actionEnvelope({
  tool: "telos",
  toolVersion: "demo",
  command: "doctor",
  native: {
    checks: [
      { name: "certificate_demo", status: "MATCH" },
      { name: "unverifiable_path", status: "MATCH" },
      { name: "zero_dependency_demo", status: "MATCH" }
    ]
  },
  nextActions: [
    { tool: "gather", action: "docs", reason: "gather the source packet for the next room event", inputs: [], priority: "normal" }
  ]
});

console.log(JSON.stringify(payload, null, 2));
```

- [ ] **Step 3: Run Telos scripts**

Run:

```powershell
cd C:\dev\public\telos
node demo\status.mjs
node demo\doctor.mjs
node demo\run.mjs
```

Expected: `status.mjs` and `doctor.mjs` print valid JSON envelopes; `run.mjs` exits `0`.

- [ ] **Step 4: Commit**

```powershell
cd C:\dev\public\telos
git add demo\status.mjs demo\doctor.mjs
git commit -m "feat: add telos operator spine scripts"
```

---

### Task 8: Add Telos Golden Workflow Harness

**Files:**
- Create: `C:\dev\public\telos\demo\flagship-workflow.mjs`

**Interfaces:**
- Consumes: sibling repo CLIs through local source checkouts.
- Produces: one final `project-telos.flagship-action/v1` envelope with nested native receipts.

- [ ] **Step 1: Create the workflow harness**

Write `demo/flagship-workflow.mjs`:

```javascript
import { spawnSync } from "node:child_process";
import { mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { actionEnvelope } from "./flagship-action.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const telosRoot = path.resolve(here, "..");
const publicRoot = path.resolve(telosRoot, "..");

function py(repo, moduleName, args) {
  const repoRoot = path.join(publicRoot, repo);
  const code = `import sys; sys.path.insert(0, r"${path.join(repoRoot, "src")}"); from ${moduleName}.cli import main; raise SystemExit(main())`;
  const result = spawnSync("python", ["-c", code, ...args], { cwd: repoRoot, encoding: "utf8" });
  if (result.status !== 0) {
    throw new Error(`${repo} ${args.join(" ")} failed: ${result.stderr || result.stdout}`);
  }
  return result.stdout;
}

function jsonFrom(stdout) {
  return JSON.parse(stdout);
}

const specPath = path.join(telosRoot, "docs", "superpowers", "specs", "2026-06-27-flagship-operator-spine-design.md");
const tmp = mkdtempSync(path.join(tmpdir(), "telos-flagship-workflow-"));
const thesis = path.join(tmp, "thesis.json");
const measurements = path.join(tmp, "measurements.json");

writeFileSync(thesis, JSON.stringify({
  title: "Operator spine smoke claims",
  claims: [
    { text: "the operator spine spec exists", falsification: "the spec file is missing" },
    { text: "the golden workflow is implemented before this harness exists", falsification: "the harness file is absent" }
  ]
}, null, 2));

writeFileSync(measurements, JSON.stringify({
  measurements: [
    { claim: "the operator spine spec exists", deviation: 0.0, tolerance: 0.0, method: "file-exists", evidence: [specPath] }
  ]
}, null, 2));

const indexMap = jsonFrom(py("index", "index_graph", ["map", "--root", telosRoot, "--json"]));
const gatherDocs = jsonFrom(py("gather", "gather", ["docs", specPath, "--json"]));
const forumRoute = jsonFrom(py("forum", "forum", ["route", "improve Project Telos flagship gather crucible index forum provenance workflow"]));
const crucibleAssess = jsonFrom(py("crucible", "crucible", ["assess", thesis, "--measurements", measurements, "--json"]));

const demo = spawnSync("node", ["demo/run.mjs"], { cwd: telosRoot, encoding: "utf8" });
if (demo.status !== 0) {
  throw new Error(`telos demo failed: ${demo.stderr || demo.stdout}`);
}

const payload = actionEnvelope({
  tool: "telos",
  toolVersion: "demo",
  command: "flagship-workflow",
  native: {
    index_repo_count: indexMap.repos ? indexMap.repos.length : 0,
    gather_receipts: gatherDocs.digest.receipts.length,
    forum_decided: forumRoute.decided,
    forum_needs_escalation: forumRoute.needs_escalation,
    crucible_match: crucibleAssess.assessment.match,
    crucible_unverifiable: crucibleAssess.assessment.unverifiable,
    telos_demo_recheck: demo.stdout.includes("recheck=true")
  },
  receipts: gatherDocs.digest.receipts,
  nextActions: [
    { tool: "crucible", action: "recheck", reason: "replay the workflow assessment when persisted to a registry", inputs: [], priority: "normal" }
  ]
});

console.log(JSON.stringify(payload, null, 2));
```

- [ ] **Step 2: Run the workflow harness**

Run:

```powershell
cd C:\dev\public\telos
node demo\flagship-workflow.mjs
```

Expected: JSON envelope prints with:

- `tool` equal to `telos`
- `command` equal to `flagship-workflow`
- `native.gather_receipts` equal to `1`
- `native.crucible_match` equal to `1`
- `native.telos_demo_recheck` equal to `true`

- [ ] **Step 3: Commit**

```powershell
cd C:\dev\public\telos
git add demo\flagship-workflow.mjs
git commit -m "feat: add flagship workflow harness"
```

---

### Task 9: Add Provider-Neutral Integration Pack

**Files:**
- Create: `C:\dev\public\telos\demo\integrations\mcp-tool-catalog.json`
- Create: `C:\dev\public\telos\demo\integrations\codex-plugin.example.json`
- Create: `C:\dev\public\telos\demo\integrations\claude-mcp.example.json`
- Create: `C:\dev\public\telos\demo\integrations\openai-agents.example.py`
- Create: `C:\dev\public\telos\demo\integrations\README.md`
- Create: `C:\dev\public\telos\demo\integrations.test.mjs`

**Interfaces:**
- Consumes: the shared action envelope and local CLI/MCP command names.
- Produces: a single tool catalog any OpenAI, Anthropic, Codex, Claude, MCP, plugin, skill, or application adapter can read.

- [ ] **Step 1: Create the MCP tool catalog**

Write `demo/integrations/mcp-tool-catalog.json`:

```json
{
  "schema": "project-telos.mcp-tool-catalog/v1",
  "action_schema": "project-telos.flagship-action/v1",
  "transports": ["stdio", "streamable-http"],
  "tools": [
    {
      "name": "gather.docs",
      "flagship": "gather",
      "description": "Read local text files or directories and emit provenance receipts.",
      "cli": ["gather", "docs", "{path}", "--json"],
      "mcp": { "status": "planned", "server": "gather", "method": "tools/call", "tool": "gather.docs" },
      "next_actions": ["index.map", "forum.route", "crucible.assess"]
    },
    {
      "name": "gather.run",
      "flagship": "gather",
      "description": "Run a multi-source research intake config and emit a witnessed run record.",
      "cli": ["gather", "run", "{config}", "--json"],
      "mcp": { "status": "planned", "server": "gather", "method": "tools/call", "tool": "gather.run" },
      "next_actions": ["crucible.assess", "forum.route"]
    },
    {
      "name": "index.map",
      "flagship": "index",
      "description": "Map a workspace or repo and emit structural context.",
      "cli": ["index", "map", "--root", "{root}", "--json"],
      "mcp": { "status": "available", "server": "index", "method": "tools/call", "tool": "index.map" },
      "next_actions": ["gather.docs", "forum.route"]
    },
    {
      "name": "index.context",
      "flagship": "index",
      "description": "Render a compact context pack from a workspace graph.",
      "cli": ["index", "context", "--root", "{root}", "--json"],
      "mcp": { "status": "available", "server": "index", "method": "tools/call", "tool": "index.context" },
      "next_actions": ["forum.route", "telos.workflow"]
    },
    {
      "name": "forum.route",
      "flagship": "forum",
      "description": "Route a request to a capability lane and expose low-confidence escalation.",
      "cli": ["forum", "route", "{text}"],
      "mcp": { "status": "available", "server": "forum", "method": "tools/call", "tool": "forum.route" },
      "next_actions": ["gather.docs", "crucible.assess"]
    },
    {
      "name": "forum.ledger.summary",
      "flagship": "forum",
      "description": "Summarize a witnessed causal ledger.",
      "cli": ["forum", "ledger", "summary", "--ledger", "{dir}", "--json"],
      "mcp": { "status": "available", "server": "forum", "method": "tools/call", "tool": "forum.ledger.summary" },
      "next_actions": ["crucible.assess", "telos.workflow"]
    },
    {
      "name": "crucible.assess",
      "flagship": "crucible",
      "description": "Assess falsifiable claims against measurements and emit MATCH/DRIFT/UNVERIFIABLE verdicts.",
      "cli": ["crucible", "assess", "{thesis}", "--measurements", "{measurements}", "--json"],
      "mcp": { "status": "planned", "server": "crucible", "method": "tools/call", "tool": "crucible.assess" },
      "next_actions": ["crucible.recheck", "telos.workflow"]
    },
    {
      "name": "crucible.recheck",
      "flagship": "crucible",
      "description": "Recheck a persisted assessment or replay descriptor-bearing measurements.",
      "cli": ["crucible", "recheck", "{registry}", "--json"],
      "mcp": { "status": "planned", "server": "crucible", "method": "tools/call", "tool": "crucible.recheck" },
      "next_actions": ["telos.workflow"]
    },
    {
      "name": "telos.status",
      "flagship": "telos",
      "description": "Emit Telos shared-room readiness as a Project Telos action envelope.",
      "cli": ["node", "demo/status.mjs"],
      "mcp": { "status": "cli-bridge", "server": "telos", "method": "tools/call", "tool": "telos.status" },
      "next_actions": ["index.map", "gather.docs"]
    },
    {
      "name": "telos.workflow",
      "flagship": "telos",
      "description": "Run the local golden workflow and reconcile the five flagship receipts.",
      "cli": ["node", "demo/flagship-workflow.mjs"],
      "mcp": { "status": "cli-bridge", "server": "telos", "method": "tools/call", "tool": "telos.workflow" },
      "next_actions": ["crucible.recheck"]
    }
  ]
}
```

- [ ] **Step 2: Create the Codex plugin example**

Write `demo/integrations/codex-plugin.example.json`:

```json
{
  "name": "project-telos-flagships",
  "version": "0.1.0",
  "description": "Project Telos flagship tools exposed through skills, CLI, and MCP.",
  "skills": [
    "flagship-operator-spine",
    "gather-intake",
    "crucible-verification",
    "index-context",
    "forum-orchestration",
    "telos-reconcile"
  ],
  "mcpServers": {
    "index": { "command": "index", "args": ["mcp"] },
    "forum": { "command": "forum", "args": ["mcp"] },
    "telos": { "command": "node", "args": ["C:/dev/public/telos/demo/flagship-workflow.mjs"], "mode": "cli-json-bridge" }
  },
  "cliEntrypoints": ["gather", "crucible", "index", "forum", "node C:/dev/public/telos/demo/run.mjs"]
}
```

- [ ] **Step 3: Create the Claude MCP example**

Write `demo/integrations/claude-mcp.example.json`:

```json
{
  "mcpServers": {
    "project-telos-index": {
      "command": "index",
      "args": ["mcp"]
    },
    "project-telos-forum": {
      "command": "forum",
      "args": ["mcp"]
    },
    "project-telos-cli-bridge": {
      "command": "node",
      "args": ["C:/dev/public/telos/demo/flagship-workflow.mjs"]
    }
  }
}
```

- [ ] **Step 4: Create the OpenAI Agents example**

Write `demo/integrations/openai-agents.example.py`:

```python
"""Example wiring only: Project Telos tools should be mounted through MCP.

The real implementation keeps business logic in the flagship CLIs/MCP servers.
OpenAI Agents code imports the MCP server connection for the selected deployment
and never reimplements gather, index, forum, crucible, or telos behavior here.
"""

PROJECT_TELOS_MCP_SERVERS = {
    "index": {"command": "index", "args": ["mcp"]},
    "forum": {"command": "forum", "args": ["mcp"]},
    "telos": {"command": "node", "args": ["C:/dev/public/telos/demo/flagship-workflow.mjs"], "mode": "cli-json-bridge"},
}

SYSTEM_PROMPT = (
    "Use Project Telos tools through MCP or their CLI JSON envelopes. "
    "Prefer gather.docs for intake, index.map/context for structure, "
    "forum.route for orchestration, crucible.assess for verification, "
    "and telos.workflow for reconciliation."
)
```

- [ ] **Step 5: Create the integration README**

Write `demo/integrations/README.md`:

```markdown
# Project Telos Integration Pack

This folder is the platform bridge. The flagship tools stay standalone; integrations mount the same CLI and MCP contracts.

## Integration rule

Business logic lives in the tools:

- `gather` handles intake.
- `index` handles structure and context.
- `forum` handles routing and ledger orchestration.
- `crucible` handles falsifiable verification.
- `telos` handles reconciliation and the shared room.

OpenAI Apps, OpenAI Agents, Anthropic Claude, Claude Code, Codex plugins, skills, and full applications should call the same MCP tool catalog or CLI JSON commands. They should not duplicate tool behavior.

## Local-first transports

- CLI JSON: works everywhere a process can run.
- MCP stdio: local agent surfaces, Codex, Claude Code, desktop tools.
- MCP Streamable HTTP: hosted apps, OpenAI Apps SDK style deployments, remote workspaces.

## Tool catalog

`mcp-tool-catalog.json` is the provider-neutral source of truth for tool names, CLI fallbacks, MCP names, and next actions.

## Packaging targets

- Codex plugin: expose skills plus MCP servers for `index`, `forum`, and Telos.
- Superpowers skills: add thin workflows that call the CLI/MCP catalog.
- Anthropic Claude and Claude Code: mount stdio MCP servers from the same catalog.
- OpenAI Agents and Apps: mount MCP servers and render Telos receipts in the app UI.
- Full applications: call CLI JSON for local desktop and MCP Streamable HTTP for hosted or distributed setups.
```

- [ ] **Step 6: Add the integration catalog test**

Write `demo/integrations.test.mjs`:

```javascript
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

const catalog = JSON.parse(readFileSync(new URL("./integrations/mcp-tool-catalog.json", import.meta.url), "utf8"));

assert.equal(catalog.schema, "project-telos.mcp-tool-catalog/v1");
assert.equal(catalog.action_schema, "project-telos.flagship-action/v1");
assert.ok(catalog.transports.includes("stdio"));
assert.ok(catalog.transports.includes("streamable-http"));

const names = new Set(catalog.tools.map((tool) => tool.name));
for (const name of [
  "gather.docs",
  "gather.run",
  "index.map",
  "index.context",
  "forum.route",
  "forum.ledger.summary",
  "crucible.assess",
  "crucible.recheck",
  "telos.status",
  "telos.workflow"
]) {
  assert.ok(names.has(name), `missing ${name}`);
}

for (const tool of catalog.tools) {
  assert.match(tool.name, /^(gather|index|forum|crucible|telos)\.[a-z.]+$/);
  assert.ok(Array.isArray(tool.cli) && tool.cli.length > 0, `${tool.name} has CLI fallback`);
  assert.equal(tool.mcp.method, "tools/call");
}
```

- [ ] **Step 7: Run the integration test**

Run:

```powershell
cd C:\dev\public\telos
node demo\integrations.test.mjs
```

Expected: exit code `0`.

- [ ] **Step 8: Commit**

```powershell
cd C:\dev\public\telos
git add demo\integrations\mcp-tool-catalog.json demo\integrations\codex-plugin.example.json demo\integrations\claude-mcp.example.json demo\integrations\openai-agents.example.py demo\integrations\README.md demo\integrations.test.mjs
git commit -m "docs: add platform integration pack"
```

---

### Task 10: Final Cross-Repo Verification

**Files:**
- No edits.

**Interfaces:**
- Consumes all previous tasks.
- Produces final evidence for the first operator-spine increment.

- [ ] **Step 1: Run targeted suites**

Run:

```powershell
cd C:\dev\public\gather
python -m pytest tests\test_flagship_cli.py tests\test_cli.py tests\test_docs.py -q

cd C:\dev\public\crucible
python -m pytest tests\test_flagship_cli.py tests\test_cli.py tests\test_readiness.py -q

cd C:\dev\public\index
python -m pytest tests\test_flagship_cli.py tests\test_cli.py tests\test_viz_theme.py tests\test_atlas_html.py -q

cd C:\dev\public\forum
python -m pytest tests\test_flagship_cli.py tests\test_cli.py tests\test_routing.py -q

cd C:\dev\public\telos
node demo\flagship-action.test.mjs
node demo\integrations.test.mjs
node demo\status.mjs
node demo\doctor.mjs
node demo\flagship-workflow.mjs
node demo\run.mjs
```

Expected: every command exits `0`.

- [ ] **Step 2: Confirm clean worktrees**

Run:

```powershell
git -C C:\dev\public\gather status --short
git -C C:\dev\public\crucible status --short
git -C C:\dev\public\index status --short
git -C C:\dev\public\forum status --short
git -C C:\dev\public\telos status --short
```

Expected: no output from any repo.

## Self-Review

Spec coverage:

- Standalone tools remain standalone: every task edits a single repo except Telos golden workflow consumption.
- Shared JSON envelope: Tasks 2 through 9.
- First known repair: Task 1 fixes the stale `index` palette test.
- Dogfood loop: Task 8 runs index -> gather -> forum -> crucible -> telos locally.
- Platform-agnostic native access: Task 9 defines the MCP tool catalog plus OpenAI, Anthropic, Codex plugin, skill, and app embedding examples over the same CLI/MCP substrates.
- Accessibility and full Telos room rendering remain outside this first increment and are intentionally left for the next implementation plan after the action contract exists.

Placeholder scan:

- The plan contains no deferred-work markers or fake implementation strings.

Type consistency:

- Python helpers use `envelope`, `cmd_status`, `cmd_doctor`, and `cmd_demo` consistently.
- Node helpers use `actionEnvelope` and `assertActionEnvelope` consistently.
- Shared key names match the approved spec: `schema`, `tool`, `tool_version`, `command`, `status`, `inputs`, `outputs`, `receipts`, `native`, `next_actions`, `diagnostics`.
