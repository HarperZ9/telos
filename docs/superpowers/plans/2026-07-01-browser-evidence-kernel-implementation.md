# Browser Evidence Kernel Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a Telos-owned browser evidence kernel and wire its packet refs through Gather, Index, Forum, Crucible, Learn, BuildLang editor fixtures, and Emet export witnessing.

**Architecture:** Implement the kernel in Telos first as a small ESM packet/artifact layer over existing `telos.native.control`, then expose it through CLI/MCP catalog entries. Consumer repos accept `project-telos.browser-evidence/v1` packets by reference; they do not import Telos internals or create separate browser stacks.

**Tech Stack:** Node ESM in Telos, Python stdlib in Gather/Index/Forum/Crucible/Emet, Node ESM in Learn, JSON fixtures, existing MCP stdio runtimes, built-in `node:test`, `node:assert/strict`, and `pytest`.

## Global Constraints

- Telos owns the browser substrate; other tools consume evidence packets and action receipts.
- Preserve `project-telos.action-receipt/v1` as the durable action state contract.
- Add `project-telos.browser-evidence/v1` with `MATCH`, `DRIFT`, and `UNVERIFIABLE` verification vocabulary.
- Do not port anti-bot framing, arbitrary dynamic hooks, unbounded CDP execution, or routine raw cookie dumping.
- Keep Learn credential `assess` hard-human by default.
- BuildLang work is limited to verified local editor-support repos until the compiler repo is present and inspected.
- Raw secrets, cookies, tokens, `.env` values, and private payloads must not appear in model-facing summaries.
- Keep new source files under 300 lines where practical; split helpers when a file grows too broad.
- Use targeted test slices before full suites.
- Use `apply_patch` for manual edits.

---

## File Structure

Telos new files:

- `C:/dev/public/telos/demo/native-control/evidence.mjs`: pure browser evidence packet builders, hash/ref helpers, artifact writer, and validation helpers. No live CDP calls.
- `C:/dev/public/telos/demo/browser-evidence.mjs`: CLI wrapper that emits fixture packets or exports evidence from native-control sessions.
- `C:/dev/public/telos/demo/browser-evidence.test.mjs`: pure unit tests for packet shape, hashing, failure states, and CLI fixture output.
- `C:/dev/public/telos/demo/integrations/browser-evidence.json`: contract fixture returned by MCP and used by docs/tests.

Telos modified files:

- `C:/dev/public/telos/demo/native-control/browser.mjs`: add snapshot helpers over existing CDP `Runtime.evaluate` and `Page.captureScreenshot`.
- `C:/dev/public/telos/demo/native-control.mjs`: add `evidence`, `snapshot-dom`, `snapshot-text`, `snapshot-visual`, and `receipt-export` browser verbs.
- `C:/dev/public/telos/demo/native-control.test.mjs`: test new pure snapshot expression builders and CLI help verbs.
- `C:/dev/public/telos/demo/telos-mcp.mjs`: expose `telos.browser.evidence`.
- `C:/dev/public/telos/demo/telos-mcp.test.mjs`: assert MCP tools/list and tool call parity.
- `C:/dev/public/telos/demo/integrations/mcp-tool-catalog.json`: catalog entry for `telos.browser.evidence`.
- `C:/dev/public/telos/demo/integrations/mcp-server-manifest.json`: expected tool update for Telos.
- `C:/dev/public/telos/README.md`, `C:/dev/public/telos/demo/README.md`, `C:/dev/public/telos/demo/integrations/README.md`, `C:/dev/public/telos/CHANGELOG.md`: operator-facing docs.

Consumer repos:

- `C:/dev/public/gather/src/gather/browser_evidence.py` and `C:/dev/public/gather/tests/test_browser_evidence.py`: import Telos packet refs into Gather items.
- `C:/dev/public/learn/src/actuation/native-driver.mjs` and `C:/dev/public/learn/tests/learn-browser-evidence.test.mjs`: carry evidence refs through captures without changing `assess` gating.
- `C:/dev/public/index/src/index_graph/context/envelope.py` and `C:/dev/public/index/tests/test_browser_evidence_refs.py`: include compact browser evidence refs without raw DOM.
- `C:/dev/public/forum/src/forum/manifests/default-roster.toml`, `C:/dev/public/forum/src/forum/routing.py`, and `C:/dev/public/forum/tests/test_browser_workflow_routes.py`: route browser workflow classes.
- `C:/dev/public/crucible/src/crucible/browser_evidence.py` and `C:/dev/public/crucible/tests/test_browser_evidence.py`: verify browser evidence packet integrity.
- `C:/dev/public/pubscan/emet/examples/browser-evidence-anchor.json` and `C:/dev/public/pubscan/emet/docs/browser-evidence.md`: document anchor/verify recipe.
- `C:/dev/public/buildlang-tmLanguage/samples/browser-workflow.bld` and `C:/dev/public/buildlang-vscode/examples/browser-workflow.bld`: editor-only examples.

---

### Task 1: Telos Browser Evidence Packet Core

**Files:**
- Create: `C:/dev/public/telos/demo/native-control/evidence.mjs`
- Create: `C:/dev/public/telos/demo/browser-evidence.test.mjs`
- Create: `C:/dev/public/telos/demo/integrations/browser-evidence.json`
- Test: `C:/dev/public/telos/demo/browser-evidence.test.mjs`

**Interfaces:**
- Consumes: no new code from other tasks.
- Produces:
  - `BROWSER_EVIDENCE_SCHEMA: "project-telos.browser-evidence/v1"`
  - `sha256Hex(value: string | Buffer): string`
  - `digestRef(kind: string, value: string | Buffer): string`
  - `makeBrowserEvidencePacket(input: BrowserEvidenceInput): BrowserEvidencePacket`
  - `makeUnavailableSummary(kind: "network" | "console", reason: string): ArtifactSummary`
  - `validateBrowserEvidencePacket(packet: object): { ok: boolean, failures: string[] }`

- [ ] **Step 1: Write the failing packet tests**

Create `C:/dev/public/telos/demo/browser-evidence.test.mjs`:

```js
import test from "node:test";
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

import {
  BROWSER_EVIDENCE_SCHEMA,
  sha256Hex,
  digestRef,
  makeBrowserEvidencePacket,
  makeUnavailableSummary,
  validateBrowserEvidencePacket,
} from "./native-control/evidence.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));

test("sha256Hex and digestRef produce stable sha256 refs", () => {
  assert.equal(
    sha256Hex("telos"),
    "c987adc38cb5536554f70a5d0db6900a59d4d4a32e84ba48f75b3301a939c6ae"
  );
  assert.equal(
    digestRef("url", "https://example.com"),
    "url:sha256:100680ad546ce6a577f42f52df33b4cfdca756859e664b8d7de329b150d09ce9"
  );
});

test("makeUnavailableSummary fails closed for missing collectors", () => {
  const summary = makeUnavailableSummary("network", "collector-not-attached");
  assert.equal(summary.kind, "network");
  assert.equal(summary.verdict, "UNVERIFIABLE");
  assert.equal(summary.failure_code, "network_capture_unavailable");
  assert.equal(summary.reason, "collector-not-attached");
});

test("makeBrowserEvidencePacket builds the v1 packet without raw DOM", () => {
  const packet = makeBrowserEvidencePacket({
    mode: "research-capture",
    action: { kind: "browser.navigate", argsHash: digestRef("args", "nav") },
    sessionRef: "browser-session:test",
    actionReceiptRef: "receipt:test",
    before: {
      url: "https://example.com",
      title: "Before",
      text: "before text",
      domArtifactRef: "artifact:before-dom",
      screenshotRef: "artifact:before-png",
    },
    after: {
      url: "https://example.com/after",
      title: "After",
      text: "after text",
      domArtifactRef: "artifact:after-dom",
      screenshotRef: "artifact:after-png",
    },
    artifactHashes: [{ ref: "artifact:after-dom", hash: digestRef("sha256", "dom") }],
    networkSummary: makeUnavailableSummary("network", "collector-not-attached"),
    consoleSummary: makeUnavailableSummary("console", "collector-not-attached"),
    sideEffect: { class: "read", external_write: false, reversible: true },
    verification: { verdict: "MATCH", ref: "crucible:packet-shape" },
    clock: () => "2026-07-01T00:00:00.000Z",
  });

  assert.equal(packet.schema, BROWSER_EVIDENCE_SCHEMA);
  assert.equal(packet.mode, "research-capture");
  assert.equal(packet.before.url_digest, digestRef("url", "https://example.com"));
  assert.equal(packet.after.text_digest, digestRef("text", "after text"));
  assert.equal(packet.network_summary.verdict, "UNVERIFIABLE");
  assert.equal(packet.console_summary.failure_code, "console_capture_unavailable");
  assert.equal(Object.hasOwn(packet.after, "raw_dom"), false);
  assert.deepEqual(validateBrowserEvidencePacket(packet), { ok: true, failures: [] });
});

test("validateBrowserEvidencePacket reports typed failures", () => {
  const result = validateBrowserEvidencePacket({ schema: BROWSER_EVIDENCE_SCHEMA, mode: "work-actuate" });
  assert.equal(result.ok, false);
  assert.ok(result.failures.includes("missing_action"));
  assert.ok(result.failures.includes("missing_after"));
  assert.ok(result.failures.includes("missing_verification"));
});

test("browser-evidence CLI emits the fixture contract", () => {
  const cli = spawnSync(process.execPath, [path.join(here, "browser-evidence.mjs"), "--fixture"], {
    cwd: path.resolve(here, ".."),
    encoding: "utf8",
  });
  assert.equal(cli.status, 0, cli.stderr || cli.stdout);
  const packet = JSON.parse(cli.stdout);
  assert.equal(packet.schema, BROWSER_EVIDENCE_SCHEMA);
  assert.equal(packet.tool, "telos.browser.evidence");
  assert.equal(packet.mode, "research-capture");
  assert.equal(validateBrowserEvidencePacket(packet).ok, true);
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `node demo/browser-evidence.test.mjs`

Expected: FAIL with `Cannot find module ... native-control/evidence.mjs`.

- [ ] **Step 3: Implement packet core**

Create `C:/dev/public/telos/demo/native-control/evidence.mjs`:

```js
import { createHash } from "node:crypto";

export const BROWSER_EVIDENCE_SCHEMA = "project-telos.browser-evidence/v1";

export const MODES = new Set([
  "work-actuate",
  "research-capture",
  "credential-logistics",
  "credential-assess",
  "lab-assess",
  "creative-capture",
]);

export const VERDICTS = new Set(["MATCH", "DRIFT", "UNVERIFIABLE"]);

export function sha256Hex(value) {
  return createHash("sha256").update(value).digest("hex");
}

export function digestRef(kind, value) {
  return `${kind}:sha256:${sha256Hex(value)}`;
}

export function makeUnavailableSummary(kind, reason) {
  const failure_code = kind === "network" ? "network_capture_unavailable" : "console_capture_unavailable";
  return { kind, verdict: "UNVERIFIABLE", failure_code, reason };
}

function snapshot(input) {
  const text = input.text ?? "";
  return {
    url: input.url ?? "",
    url_digest: digestRef("url", input.url ?? ""),
    title: input.title ?? "",
    dom_snapshot_ref: input.domArtifactRef ?? null,
    text_digest: digestRef("text", text),
    screenshot_ref: input.screenshotRef ?? null,
  };
}

export function makeBrowserEvidencePacket(input) {
  const verification = input.verification ?? { verdict: "UNVERIFIABLE", ref: null };
  const packet = {
    schema: BROWSER_EVIDENCE_SCHEMA,
    tool: "telos.browser.evidence",
    mode: input.mode,
    session_ref: input.sessionRef ?? null,
    target_ref: digestRef("url", input.after?.url ?? input.before?.url ?? ""),
    action_receipt_ref: input.actionReceiptRef ?? null,
    action: {
      kind: input.action?.kind ?? "browser.unknown",
      selector: input.action?.selector ?? null,
      args_hash: input.action?.argsHash ?? digestRef("args", ""),
    },
    before: snapshot(input.before ?? {}),
    after: snapshot(input.after ?? {}),
    network_summary: input.networkSummary ?? makeUnavailableSummary("network", "collector-not-attached"),
    console_summary: input.consoleSummary ?? makeUnavailableSummary("console", "collector-not-attached"),
    artifact_hashes: input.artifactHashes ?? [],
    redaction_status: input.redactionStatus ?? "redacted",
    side_effect: input.sideEffect ?? { class: "read", external_write: false, reversible: true },
    verification,
    created_at: input.clock ? input.clock() : new Date().toISOString(),
  };
  return packet;
}

export function validateBrowserEvidencePacket(packet) {
  const failures = [];
  if (!packet || typeof packet !== "object") return { ok: false, failures: ["not_an_object"] };
  if (packet.schema !== BROWSER_EVIDENCE_SCHEMA) failures.push("schema_mismatch");
  if (!MODES.has(packet.mode)) failures.push("mode_invalid");
  if (!packet.action || typeof packet.action !== "object") failures.push("missing_action");
  if (!packet.before || typeof packet.before !== "object") failures.push("missing_before");
  if (!packet.after || typeof packet.after !== "object") failures.push("missing_after");
  if (!packet.verification || !VERDICTS.has(packet.verification.verdict)) failures.push("missing_verification");
  if (!Array.isArray(packet.artifact_hashes)) failures.push("artifact_hashes_not_array");
  return { ok: failures.length === 0, failures };
}
```

- [ ] **Step 4: Add the fixture contract**

Create `C:/dev/public/telos/demo/integrations/browser-evidence.json`:

```json
{
  "schema": "project-telos.browser-evidence/v1",
  "tool": "telos.browser.evidence",
  "mode": "research-capture",
  "session_ref": "browser-session:fixture",
  "target_ref": "url:sha256:100680ad546ce6a577f42f52df33b4cfdca756859e664b8d7de329b150d09ce9",
  "action_receipt_ref": "receipt:fixture-browser-evidence",
  "action": {
    "kind": "browser.navigate",
    "selector": null,
    "args_hash": "args:sha256:abca4de9dd94d3ac2db9c470f8d4557f421b969fab4990c3c719629f7e7a8b69"
  },
  "before": {
    "url": "https://example.com",
    "url_digest": "url:sha256:100680ad546ce6a577f42f52df33b4cfdca756859e664b8d7de329b150d09ce9",
    "title": "Example Domain",
    "dom_snapshot_ref": "artifact:fixture/before-dom.html",
    "text_digest": "text:sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "screenshot_ref": "artifact:fixture/before.png"
  },
  "after": {
    "url": "https://example.com",
    "url_digest": "url:sha256:100680ad546ce6a577f42f52df33b4cfdca756859e664b8d7de329b150d09ce9",
    "title": "Example Domain",
    "dom_snapshot_ref": "artifact:fixture/after-dom.html",
    "text_digest": "text:sha256:f94d9486b327090cccbeb97d67953a1f234b83d67350b7b5f60196b0a30f24db",
    "screenshot_ref": "artifact:fixture/after.png"
  },
  "network_summary": {
    "kind": "network",
    "verdict": "UNVERIFIABLE",
    "failure_code": "network_capture_unavailable",
    "reason": "collector-not-attached"
  },
  "console_summary": {
    "kind": "console",
    "verdict": "UNVERIFIABLE",
    "failure_code": "console_capture_unavailable",
    "reason": "collector-not-attached"
  },
  "artifact_hashes": [
    {
      "ref": "artifact:fixture/after-dom.html",
      "hash": "sha256:3f3a3b3d4a6a7b8c9d00112233445566778899aabbccddeeff00112233445566"
    }
  ],
  "redaction_status": "redacted",
  "side_effect": {
    "class": "read",
    "external_write": false,
    "reversible": true
  },
  "verification": {
    "verdict": "MATCH",
    "ref": "crucible:fixture-browser-evidence-shape"
  },
  "created_at": "2026-07-01T00:00:00.000Z"
}
```

- [ ] **Step 5: Add the fixture CLI**

Create `C:/dev/public/telos/demo/browser-evidence.mjs`:

```js
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";
import { validateBrowserEvidencePacket } from "./native-control/evidence.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const fixturePath = path.join(here, "integrations", "browser-evidence.json");

export function fixturePacket() {
  return JSON.parse(readFileSync(fixturePath, "utf8"));
}

export function summary(packet) {
  const validation = validateBrowserEvidencePacket(packet);
  return [
    "Telos Browser Evidence",
    `schema   ${packet.schema}`,
    `mode     ${packet.mode}`,
    `verdict  ${packet.verification?.verdict ?? "UNVERIFIABLE"}`,
    `valid    ${validation.ok ? "MATCH" : "DRIFT"}`,
    `next     node demo/browser-evidence.mjs --fixture`,
  ].join("\n") + "\n";
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  const packet = fixturePacket();
  if (process.argv.includes("--summary")) {
    process.stdout.write(summary(packet));
  } else {
    process.stdout.write(`${JSON.stringify(packet, null, 2)}\n`);
  }
}
```

- [ ] **Step 6: Run the test**

Run: `node demo/browser-evidence.test.mjs`

Expected: PASS.

- [ ] **Step 7: Commit Task 1**

Run:

```powershell
git add demo/native-control/evidence.mjs demo/browser-evidence.mjs demo/browser-evidence.test.mjs demo/integrations/browser-evidence.json
git commit -m "feat: add browser evidence packet contract"
```

Expected: commit succeeds.

---

### Task 2: Telos Native-Control Evidence Verbs

**Files:**
- Modify: `C:/dev/public/telos/demo/native-control/browser.mjs`
- Modify: `C:/dev/public/telos/demo/native-control.mjs`
- Modify: `C:/dev/public/telos/demo/native-control.test.mjs`
- Test: `C:/dev/public/telos/demo/native-control.test.mjs`

**Interfaces:**
- Consumes:
  - `digestRef(kind, value)` from `./native-control/evidence.mjs`
  - `makeBrowserEvidencePacket(input)` from `./native-control/evidence.mjs`
- Produces:
  - `domSnapshotExpression(): string`
  - `textSnapshotExpression(limit?: number): string`
  - `pageState(session): Promise<{url: string, title: string, text: string, html: string}>`
  - browser CLI verbs: `snapshot-dom`, `snapshot-text`, `snapshot-visual`, `evidence`

- [ ] **Step 1: Add failing tests for snapshot expressions and help verbs**

Append to `C:/dev/public/telos/demo/native-control.test.mjs`:

```js
import {
  domSnapshotExpression,
  textSnapshotExpression,
} from "./native-control/browser.mjs";

test("snapshot expressions collect bounded page state without secrets by design", () => {
  assert.match(domSnapshotExpression(), /document\.documentElement\.outerHTML/);
  assert.match(textSnapshotExpression(123), /slice\(0,123\)/);
  assert.match(textSnapshotExpression(), /innerText/);
});

test("CLI help advertises browser evidence verbs", () => {
  const cli = spawnSync(process.execPath, [path.join(here, "native-control.mjs")], { encoding: "utf8" });
  assert.equal(cli.status, 0, cli.stderr);
  const receipt = JSON.parse(cli.stdout);
  assert.ok(receipt.result.browser.includes("snapshot-dom"));
  assert.ok(receipt.result.browser.includes("snapshot-text"));
  assert.ok(receipt.result.browser.includes("snapshot-visual"));
  assert.ok(receipt.result.browser.includes("evidence"));
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `node demo/native-control.test.mjs`

Expected: FAIL because `domSnapshotExpression` is not exported and help verbs are absent.

- [ ] **Step 3: Add browser snapshot helpers**

Modify `C:/dev/public/telos/demo/native-control/browser.mjs`:

```js
export function domSnapshotExpression() {
  return `(()=>document.documentElement ? document.documentElement.outerHTML : "")()`;
}

export function textSnapshotExpression(limit = 20000) {
  return `(()=>((document.body&&document.body.innerText)||"").slice(0,${Number(limit)}))()`;
}

export async function pageState(session) {
  const [url, title, text, html] = await Promise.all([
    evaluate(session, "location.href"),
    evaluate(session, "document.title"),
    evaluate(session, textSnapshotExpression()),
    evaluate(session, domSnapshotExpression()),
  ]);
  return { url: url || "", title: title || "", text: text || "", html: html || "" };
}
```

- [ ] **Step 4: Add CLI verbs**

Modify `runBrowser` in `C:/dev/public/telos/demo/native-control.mjs`:

```js
      case "snapshot-dom":
        return { html: await browser.evalJs(session, browser.domSnapshotExpression()) };
      case "snapshot-text":
        return { text: await browser.evalJs(session, browser.textSnapshotExpression(params[0] ? Number(params[0]) : 20000)) };
      case "snapshot-visual": {
        const data = await browser.screenshot(session);
        const path = params[0] || "telos-screenshot.png";
        writeFileSync(path, Buffer.from(data, "base64"));
        return { path, bytes: Buffer.from(data, "base64").length };
      }
      case "evidence": {
        const before = await browser.pageState(session);
        const after = before;
        const { makeBrowserEvidencePacket, makeUnavailableSummary, digestRef } = await import("./native-control/evidence.mjs");
        return makeBrowserEvidencePacket({
          mode: flags.mode || "research-capture",
          action: { kind: "browser.evidence", argsHash: digestRef("args", JSON.stringify(params)) },
          sessionRef: `browser-session:cdp-${port}`,
          actionReceiptRef: null,
          before,
          after,
          networkSummary: makeUnavailableSummary("network", "collector-not-attached"),
          consoleSummary: makeUnavailableSummary("console", "collector-not-attached"),
          verification: { verdict: "MATCH", ref: "telos:native-control-evidence" },
        });
      }
```

Also update the help receipt browser verbs:

```js
browser: [
  "tabs", "navigate", "eval", "click", "fill", "focus", "type", "gettext",
  "waitfor", "screenshot", "snapshot-dom", "snapshot-text", "snapshot-visual", "evidence"
]
```

- [ ] **Step 5: Run targeted test**

Run: `node demo/native-control.test.mjs`

Expected: PASS, with the live browser CDP test skipped when no debug Chrome is available.

- [ ] **Step 6: Commit Task 2**

Run:

```powershell
git add demo/native-control/browser.mjs demo/native-control.mjs demo/native-control.test.mjs
git commit -m "feat: add native browser evidence verbs"
```

Expected: commit succeeds.

---

### Task 3: Telos MCP, Catalog, And Docs

**Files:**
- Modify: `C:/dev/public/telos/demo/telos-mcp.mjs`
- Modify: `C:/dev/public/telos/demo/telos-mcp.test.mjs`
- Modify: `C:/dev/public/telos/demo/integrations/mcp-tool-catalog.json`
- Modify: `C:/dev/public/telos/demo/integrations/mcp-server-manifest.json`
- Modify: `C:/dev/public/telos/README.md`
- Modify: `C:/dev/public/telos/demo/README.md`
- Modify: `C:/dev/public/telos/demo/integrations/README.md`
- Modify: `C:/dev/public/telos/CHANGELOG.md`
- Test: `C:/dev/public/telos/demo/telos-mcp.test.mjs`
- Test: `C:/dev/public/telos/demo/mcp-runtime-contract.test.mjs`
- Test: `C:/dev/public/telos/demo/mcp-server-launch.test.mjs`

**Interfaces:**
- Consumes:
  - `demo/browser-evidence.mjs`
  - `demo/integrations/browser-evidence.json`
- Produces:
  - MCP tool `telos.browser.evidence`
  - Catalog entry `telos.browser.evidence`
  - Telos server manifest expected tool `telos.browser.evidence`

- [ ] **Step 1: Add failing MCP assertions**

Modify `C:/dev/public/telos/demo/telos-mcp.test.mjs`:

```js
assert.ok(names.has("telos.browser.evidence"), "missing telos.browser.evidence");

const expectedBrowserEvidence = JSON.parse(
  readFileSync(new URL("./integrations/browser-evidence.json", import.meta.url), "utf8")
);
const browserEvidence = handleRequest(request("tools/call", {
  name: "telos.browser.evidence",
  arguments: {}
}));
assert.deepEqual(browserEvidence.result.structuredContent, expectedBrowserEvidence);
assert.equal(browserEvidence.result.structuredContent.schema, "project-telos.browser-evidence/v1");
assert.equal(browserEvidence.result.structuredContent.tool, "telos.browser.evidence");
```

Add to the stdio list assertions:

```js
assert.ok(stdioResponse.result.tools.some((tool) => tool.name === "telos.browser.evidence"));
```

- [ ] **Step 2: Run MCP test to verify it fails**

Run: `node demo/telos-mcp.test.mjs`

Expected: FAIL because `telos.browser.evidence` is not in `tools`.

- [ ] **Step 3: Add MCP tool mapping**

Modify `C:/dev/public/telos/demo/telos-mcp.mjs`:

```js
{
  name: "telos.browser.evidence",
  description: "Use when a host needs the Browser Evidence Kernel packet contract for CDP-backed browser automation, artifact refs, side-effect classes, and MATCH/DRIFT/UNVERIFIABLE verification. Read-only, zero-auth, no external side effects. Returns a JSON browser evidence fixture.",
  inputSchema: { type: "object", properties: {}, additionalProperties: false }
}
```

Add to `toolScripts`:

```js
["telos.browser.evidence", ["browser-evidence.mjs"]],
```

- [ ] **Step 4: Update catalog JSON**

Insert a Telos catalog item in `C:/dev/public/telos/demo/integrations/mcp-tool-catalog.json`:

```json
{
  "name": "telos.browser.evidence",
  "flagship": "telos",
  "description": "Use when a host needs the Browser Evidence Kernel packet contract for CDP-backed browser automation, artifact refs, side-effect classes, and MATCH/DRIFT/UNVERIFIABLE verification. Read-only, zero-auth, no external side effects. Returns a JSON browser evidence fixture.",
  "cli": [
    "node",
    "demo/browser-evidence.mjs"
  ],
  "mcp": {
    "status": "available",
    "server": "telos",
    "method": "tools/call",
    "tool": "telos.browser.evidence"
  },
  "next_actions": [
    "telos.native.control",
    "telos.action.receipt",
    "crucible.assess"
  ]
}
```

- [ ] **Step 5: Update server manifest**

Add `"telos.browser.evidence"` to `servers.telos.expected_tools` in `C:/dev/public/telos/demo/integrations/mcp-server-manifest.json`.

- [ ] **Step 6: Update docs**

Add concise entries:

```markdown
Use `node demo/browser-evidence.mjs --summary` for the Browser Evidence Kernel contract: CDP-backed browser automation evidence packets with artifact refs, side-effect classes, and `MATCH` / `DRIFT` / `UNVERIFIABLE` verification.
```

Mention `telos.browser.evidence` in the README operator surface list and `demo/integrations/README.md` Telos MCP list.

- [ ] **Step 7: Run targeted Telos verification**

Run:

```powershell
node demo/browser-evidence.test.mjs
node demo/native-control.test.mjs
node demo/telos-mcp.test.mjs
node demo/mcp-runtime-contract.test.mjs
node demo/mcp-server-launch.test.mjs
```

Expected: all commands exit 0; live browser test may remain skipped when no debug Chrome is available.

- [ ] **Step 8: Commit Task 3**

Run:

```powershell
git add demo/telos-mcp.mjs demo/telos-mcp.test.mjs demo/integrations/mcp-tool-catalog.json demo/integrations/mcp-server-manifest.json README.md demo/README.md demo/integrations/README.md CHANGELOG.md
git commit -m "feat: expose browser evidence through telos mcp"
```

Expected: commit succeeds.

---

### Task 4: Gather Browser Evidence Source

**Files:**
- Create: `C:/dev/public/gather/src/gather/browser_evidence.py`
- Create: `C:/dev/public/gather/tests/test_browser_evidence.py`
- Modify: `C:/dev/public/gather/src/gather/method.py`
- Modify: `C:/dev/public/gather/src/gather/run_config.py`
- Modify: `C:/dev/public/gather/README.md`
- Test: `C:/dev/public/gather/tests/test_browser_evidence.py`

**Interfaces:**
- Consumes:
  - `project-telos.browser-evidence/v1` packet files.
- Produces:
  - `parse_browser_evidence(packet: dict, fetched_at: float) -> Item`
  - `BrowserEvidenceSource.fetch(path: str) -> list[Item]`
  - Gather method `browser-evidence`

- [ ] **Step 1: Write failing Gather tests**

Create `C:/dev/public/gather/tests/test_browser_evidence.py`:

```python
import json

from gather.browser_evidence import parse_browser_evidence, BrowserEvidenceSource
from gather.method import directness, DIRECT


PACKET = {
    "schema": "project-telos.browser-evidence/v1",
    "tool": "telos.browser.evidence",
    "mode": "research-capture",
    "target_ref": "url:sha256:abc",
    "after": {
        "url": "https://example.com",
        "title": "Example Domain",
        "text_digest": "text:sha256:def",
        "dom_snapshot_ref": "artifact:after-dom.html",
        "screenshot_ref": "artifact:after.png",
    },
    "artifact_hashes": [{"ref": "artifact:after-dom.html", "hash": "sha256:123"}],
    "verification": {"verdict": "MATCH", "ref": "crucible:shape"},
}


def test_browser_evidence_method_is_direct():
    assert directness("browser-evidence") == DIRECT


def test_parse_browser_evidence_preserves_refs():
    item = parse_browser_evidence(PACKET, fetched_at=1.0)
    assert item.kind == "webpage"
    assert item.id == "https://example.com"
    assert item.title == "Example Domain"
    assert item.provenance.source == "browser"
    assert item.provenance.method == "browser-evidence"
    assert item.meta["browser_evidence_ref"] == "url:sha256:abc"
    assert item.meta["dom_snapshot_ref"] == "artifact:after-dom.html"
    assert item.meta["screenshot_ref"] == "artifact:after.png"
    assert item.meta["verification_verdict"] == "MATCH"


def test_browser_evidence_source_reads_packet_file(tmp_path):
    path = tmp_path / "packet.json"
    path.write_text(json.dumps(PACKET), encoding="utf-8")
    items = BrowserEvidenceSource(clock=lambda: 2.0).fetch(str(path))
    assert len(items) == 1
    assert items[0].provenance.fetched_at == 2.0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_browser_evidence.py -q`

Expected: FAIL because `gather.browser_evidence` does not exist.

- [ ] **Step 3: Implement parser/source**

Create `C:/dev/public/gather/src/gather/browser_evidence.py`:

```python
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from gather.item import Item, make_item

SCHEMA = "project-telos.browser-evidence/v1"


def parse_browser_evidence(packet: dict[str, Any], *, fetched_at: float) -> Item:
    if packet.get("schema") != SCHEMA:
        raise ValueError("browser evidence packet schema mismatch")
    after = packet.get("after") or {}
    url = str(after.get("url") or "")
    title = str(after.get("title") or url)
    text = (
        f"Browser evidence capture for {url}\n"
        f"title: {title}\n"
        f"text_digest: {after.get('text_digest') or ''}\n"
    )
    meta = {
        "browser_evidence_ref": packet.get("target_ref"),
        "dom_snapshot_ref": after.get("dom_snapshot_ref"),
        "screenshot_ref": after.get("screenshot_ref"),
        "network_summary": packet.get("network_summary"),
        "console_summary": packet.get("console_summary"),
        "artifact_hashes": packet.get("artifact_hashes") or [],
        "verification_verdict": (packet.get("verification") or {}).get("verdict", "UNVERIFIABLE"),
    }
    return make_item(
        kind="webpage",
        id=url,
        title=title,
        text=text,
        source="browser",
        ref=url,
        method="browser-evidence",
        fetched_at=fetched_at,
        meta=meta,
    )


class BrowserEvidenceSource:
    name = "browser-evidence"

    def __init__(self, *, clock=time.time) -> None:
        self._clock = clock

    def fetch(self, target: str) -> list[Item]:
        packet = json.loads(Path(target).read_text(encoding="utf-8"))
        return [parse_browser_evidence(packet, fetched_at=float(self._clock()))]
```

- [ ] **Step 4: Register method and run-config source**

Modify `C:/dev/public/gather/src/gather/method.py`:

```python
DIRECT_METHODS = frozenset({
    "yt-dlp", "auto-caption", "http-get", "file-read", "feed",
    "arxiv-api", "arxiv-api-id", "arxiv-api-search", "pdftotext",
    "api-get", "ocr", "transcribe", "browser-extract", "browser-evidence",
})
```

Modify `C:/dev/public/gather/src/gather/run_config.py` near existing source factory:

```python
    if name == "browser-evidence":
        from gather.browser_evidence import BrowserEvidenceSource
        return BrowserEvidenceSource()
```

- [ ] **Step 5: Update Gather README**

Add a short line near the browser adapter description:

```markdown
`browser-evidence` imports a Telos `project-telos.browser-evidence/v1` packet as a source item, preserving DOM, screenshot, network, and verification refs without copying raw browser artifacts into model-facing output.
```

- [ ] **Step 6: Run Gather tests**

Run:

```powershell
pytest tests/test_browser_evidence.py -q
pytest tests/test_browser.py tests/test_run_config.py -q
```

Expected: all selected tests pass.

- [ ] **Step 7: Commit Task 4**

Run:

```powershell
git add src/gather/browser_evidence.py src/gather/method.py src/gather/run_config.py tests/test_browser_evidence.py README.md
git commit -m "feat: ingest telos browser evidence packets"
```

Expected: commit succeeds in `C:/dev/public/gather`.

---

### Task 5: Learn Evidence Refs Without Assessment Drift

**Files:**
- Modify: `C:/dev/public/learn/src/actuation/native-driver.mjs`
- Modify: `C:/dev/public/learn/src/runtime/runner.mjs`
- Create: `C:/dev/public/learn/tests/learn-browser-evidence.test.mjs`
- Test: `C:/dev/public/learn/tests/learn-browser-evidence.test.mjs`
- Test: `C:/dev/public/learn/tests/learn-study.test.mjs`

**Interfaces:**
- Consumes:
  - Telos native-control browser module functions.
- Produces:
  - `NativeDriver.capture("evidence") -> { kind: "evidence", payload: string, evidenceRef?: string }`
  - Ledger step entries may include `evidenceRef` when the driver returns it.

- [ ] **Step 1: Write failing Learn tests**

Create `C:/dev/public/learn/tests/learn-browser-evidence.test.mjs`:

```js
import test from "node:test";
import assert from "node:assert/strict";

import { loadWorkflow } from "../src/workflow/schema.mjs";
import { run } from "../src/runtime/runner.mjs";

class EvidenceDriver {
  constructor() { this.actions = []; }
  async snapshot() { return { url: "https://course.test", title: "Course", fields: {} }; }
  async navigate(url) { this.actions.push(["navigate", url]); return { payload: `navigated:${url}` }; }
  async click(sel) { this.actions.push(["click", sel]); return { payload: `clicked:${sel}` }; }
  async fill(sel, val) { this.actions.push(["fill", sel, val]); return { payload: `filled:${sel}` }; }
  async waitFor(sel) { this.actions.push(["waitFor", sel]); return { payload: `present:${sel}` }; }
  async capture(kind) {
    this.actions.push(["capture", kind]);
    return { kind, payload: "evidence:artifact", evidenceRef: "browser-evidence:fixture" };
  }
}

test("capture steps carry browser evidence refs into the ledger", async () => {
  const workflow = loadWorkflow({
    adapter: "fake",
    course: "browser evidence",
    steps: [{ kind: "capture", capture: "evidence" }],
  });
  const result = await run(workflow, { driver: new EvidenceDriver() });
  const entry = result.ledger.steps.find((step) => step.kind === "step");
  assert.equal(entry.evidenceRef, "browser-evidence:fixture");
});

test("assess still halts before browser evidence actuation", async () => {
  const driver = new EvidenceDriver();
  const workflow = loadWorkflow({
    adapter: "fake",
    course: "human assessment",
    steps: [
      { kind: "assess", label: "graded quiz" },
      { kind: "capture", capture: "evidence" },
    ],
  });
  const result = await run(workflow, { driver, submissionMode: "witnessed-auto" });
  assert.equal(result.status, "halted-assess");
  assert.deepEqual(driver.actions, []);
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `node --test tests/learn-browser-evidence.test.mjs`

Expected: FAIL because ledger entries do not carry `evidenceRef`.

- [ ] **Step 3: Preserve evidence refs in runner**

Modify `C:/dev/public/learn/src/runtime/runner.mjs` after step entry creation:

```js
      if (res.evidenceRef) {
        entry.evidenceRef = res.evidenceRef;
      }
```

- [ ] **Step 4: Add NativeDriver evidence capture**

Modify `C:/dev/public/learn/src/actuation/native-driver.mjs` inside `capture(kind = "dom")`:

```js
    if (kind === "evidence") {
      const state = await this.snapshot();
      return {
        kind,
        payload: "browser-evidence:" + state.url,
        evidenceRef: "browser-evidence:" + state.url,
      };
    }
```

This keeps the first Learn slice ref-based. A later Telos implementation can replace the string ref with the full Telos packet ref once `native-control` exports it.

- [ ] **Step 5: Run Learn tests**

Run:

```powershell
node --test tests/learn-browser-evidence.test.mjs tests/learn-study.test.mjs tests/learn-study-cli.test.mjs tests/learn-study-mcp.test.mjs tests/visualize-cli.test.mjs
```

Expected: all selected tests pass.

- [ ] **Step 6: Commit Task 5**

Run:

```powershell
git add src/actuation/native-driver.mjs src/runtime/runner.mjs tests/learn-browser-evidence.test.mjs
git commit -m "feat: carry browser evidence refs in learn logistics"
```

Expected: commit succeeds in `C:/dev/public/learn`.

---

### Task 6: Index Browser Evidence Context Refs

**Files:**
- Modify: `C:/dev/public/index/src/index_graph/context/envelope.py`
- Create: `C:/dev/public/index/tests/test_browser_evidence_refs.py`
- Test: `C:/dev/public/index/tests/test_browser_evidence_refs.py`

**Interfaces:**
- Consumes:
  - A caller-provided browser evidence ref list.
- Produces:
  - `browser_evidence_refs` in `project-telos.context-envelope/v1`.
  - No raw DOM or screenshot bytes in context envelopes.

- [ ] **Step 1: Write failing Index test**

Create `C:/dev/public/index/tests/test_browser_evidence_refs.py`:

```python
from index_graph.context.envelope import build_context_envelope


def test_context_envelope_carries_browser_evidence_refs_without_raw_dom(tmp_path):
    root = tmp_path / "workspace"
    repo = root / "demo"
    repo.mkdir(parents=True)
    (repo / "README.md").write_text("demo", encoding="utf-8")

    env = build_context_envelope(
        root,
        token_budget=700,
        browser_evidence_refs=[{
            "ref": "browser-evidence:fixture",
            "schema": "project-telos.browser-evidence/v1",
            "mode": "research-capture",
            "hash": "sha256:abc",
        }],
    )

    assert env["schema"] == "project-telos.context-envelope/v1"
    assert env["browser_evidence_refs"][0]["ref"] == "browser-evidence:fixture"
    assert "raw_dom" not in str(env)
    assert "screenshot_png" not in str(env)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_browser_evidence_refs.py -q`

Expected: FAIL because `build_context_envelope` does not accept `browser_evidence_refs`.

- [ ] **Step 3: Add optional parameter**

Modify `C:/dev/public/index/src/index_graph/context/envelope.py` function signature:

```python
def build_context_envelope(
    root: str | Path,
    token_budget: int = 1200,
    *,
    focus: str | None = None,
    hops: int = 1,
    browser_evidence_refs: list[dict] | None = None,
) -> dict:
```

Add this field to the returned envelope:

```python
        "browser_evidence_refs": tuple(browser_evidence_refs or ()),
```

If the existing envelope uses lists for JSON fields, use `list(browser_evidence_refs or [])` instead.

- [ ] **Step 4: Run Index tests**

Run:

```powershell
pytest tests/test_browser_evidence_refs.py tests/test_context_envelope.py -q
```

Expected: all selected tests pass.

- [ ] **Step 5: Commit Task 6**

Run:

```powershell
git add src/index_graph/context/envelope.py tests/test_browser_evidence_refs.py
git commit -m "feat: preserve browser evidence refs in context envelopes"
```

Expected: commit succeeds in `C:/dev/public/index`.

---

### Task 7: Forum Browser Workflow Routing

**Files:**
- Modify: `C:/dev/public/forum/src/forum/manifests/default-roster.toml`
- Modify: `C:/dev/public/forum/src/forum/routing.py`
- Create: `C:/dev/public/forum/tests/test_browser_workflow_routes.py`
- Test: `C:/dev/public/forum/tests/test_browser_workflow_routes.py`

**Interfaces:**
- Consumes:
  - Forum lexical router and default roster.
- Produces:
  - Browser workflow prompts route to `project-telos` or a dedicated browser automation lane if the roster already supports it.
  - Route result exposes deterministic routing without model calls.

- [ ] **Step 1: Write failing routing tests**

Create `C:/dev/public/forum/tests/test_browser_workflow_routes.py`:

```python
from forum.roster import load_default
from forum.routing import LexicalRouter


def route(text):
    return LexicalRouter().score(text, load_default())


def test_browser_research_capture_routes_to_project_telos():
    result = route("Use Telos browser evidence to capture a JavaScript-rendered source page with DOM and screenshot refs")
    assert result.decided == "project-telos"
    assert result.needs_escalation is False


def test_browser_work_actuation_routes_to_project_telos():
    result = route("Run an operator-authorized work-actuate browser workflow and record before after evidence")
    assert result.decided == "project-telos"
    assert result.needs_escalation is False


def test_learn_credential_boundary_routes_to_teaching_or_telos():
    result = route("Use browser automation for learn credential logistics but halt on human assessment")
    assert result.decided in {"project-telos", "teaching"}
    assert result.needs_escalation is False
```

- [ ] **Step 2: Run test to verify current behavior**

Run: `pytest tests/test_browser_workflow_routes.py -q`

Expected: FAIL if the router lacks browser/evidence/work-actuate vocabulary.

- [ ] **Step 3: Add route vocabulary**

Modify `C:/dev/public/forum/src/forum/manifests/default-roster.toml` in the `project-telos` lane keywords:

```toml
keywords = ["telos", "flagship", "gather", "crucible", "index", "forum", "provenance", "workflow", "spine", "dogfood", "seed", "kun", "sofer", "orca", "behavior", "transform", "private", "line", "enterprise", "presentation", "receipts", "compatibility", "browser", "evidence", "actuation", "work-actuate", "research-capture", "credential-logistics", "browser-evidence"]
```

If line length is excessive in local style, split the TOML array across lines while preserving the exact added tokens.

- [ ] **Step 4: Run Forum tests**

Run:

```powershell
pytest tests/test_browser_workflow_routes.py tests/test_flagship.py tests/test_mcp_surface.py -q
```

Expected: all selected tests pass.

- [ ] **Step 5: Commit Task 7**

Run:

```powershell
git add src/forum/manifests/default-roster.toml tests/test_browser_workflow_routes.py
git commit -m "feat: route browser evidence workflows"
```

Expected: commit succeeds in `C:/dev/public/forum`.

---

### Task 8: Crucible Browser Evidence Integrity Measurement

**Files:**
- Create: `C:/dev/public/crucible/src/crucible/browser_evidence.py`
- Create: `C:/dev/public/crucible/tests/test_browser_evidence.py`
- Modify: `C:/dev/public/crucible/src/crucible/__init__.py`
- Test: `C:/dev/public/crucible/tests/test_browser_evidence.py`

**Interfaces:**
- Consumes:
  - `project-telos.browser-evidence/v1` packet dict.
- Produces:
  - `verify_browser_evidence(packet: Mapping) -> dict`
  - `BrowserEvidenceMeasure.measure(claim: Claim) -> Measurement`

- [ ] **Step 1: Write failing Crucible tests**

Create `C:/dev/public/crucible/tests/test_browser_evidence.py`:

```python
from crucible.browser_evidence import verify_browser_evidence


PACKET = {
    "schema": "project-telos.browser-evidence/v1",
    "mode": "research-capture",
    "artifact_hashes": [{"ref": "artifact:x", "hash": "sha256:abc"}],
    "side_effect": {"class": "read", "external_write": False, "reversible": True},
    "verification": {"verdict": "MATCH", "ref": "crucible:shape"},
}


def test_verify_browser_evidence_match():
    result = verify_browser_evidence(PACKET)
    assert result == {"verdict": "MATCH", "reason": "packet-shape-and-artifact-refs-present"}


def test_verify_browser_evidence_unverifiable_for_malformed_packet():
    result = verify_browser_evidence({"schema": "wrong"})
    assert result["verdict"] == "UNVERIFIABLE"
    assert result["reason"] == "schema_mismatch"


def test_verify_browser_evidence_drift_for_carried_drift():
    packet = {**PACKET, "verification": {"verdict": "DRIFT", "ref": "crucible:drift"}}
    result = verify_browser_evidence(packet)
    assert result["verdict"] == "DRIFT"
    assert result["reason"] == "carried_verdict_drift"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_browser_evidence.py -q`

Expected: FAIL because `crucible.browser_evidence` does not exist.

- [ ] **Step 3: Implement verifier**

Create `C:/dev/public/crucible/src/crucible/browser_evidence.py`:

```python
from __future__ import annotations

from collections.abc import Mapping

SCHEMA = "project-telos.browser-evidence/v1"
VERDICTS = {"MATCH", "DRIFT", "UNVERIFIABLE"}


def verify_browser_evidence(packet: Mapping) -> dict:
    if packet.get("schema") != SCHEMA:
        return {"verdict": "UNVERIFIABLE", "reason": "schema_mismatch"}
    verification = packet.get("verification")
    if not isinstance(verification, Mapping):
        return {"verdict": "UNVERIFIABLE", "reason": "missing_verification"}
    carried = verification.get("verdict")
    if carried not in VERDICTS:
        return {"verdict": "UNVERIFIABLE", "reason": "invalid_carried_verdict"}
    if carried == "DRIFT":
        return {"verdict": "DRIFT", "reason": "carried_verdict_drift"}
    if carried == "UNVERIFIABLE":
        return {"verdict": "UNVERIFIABLE", "reason": "carried_verdict_unverifiable"}
    if not packet.get("artifact_hashes"):
        return {"verdict": "UNVERIFIABLE", "reason": "missing_artifact_hashes"}
    if not isinstance(packet.get("side_effect"), Mapping):
        return {"verdict": "UNVERIFIABLE", "reason": "missing_side_effect"}
    return {"verdict": "MATCH", "reason": "packet-shape-and-artifact-refs-present"}
```

- [ ] **Step 4: Export verifier**

Modify `C:/dev/public/crucible/src/crucible/__init__.py`:

```python
from crucible.browser_evidence import verify_browser_evidence
```

Add `"verify_browser_evidence"` to `__all__`.

- [ ] **Step 5: Run Crucible tests**

Run:

```powershell
pytest tests/test_browser_evidence.py tests/test_telos_measure.py tests/test_gather_index_interop.py -q
```

Expected: all selected tests pass.

- [ ] **Step 6: Commit Task 8**

Run:

```powershell
git add src/crucible/browser_evidence.py src/crucible/__init__.py tests/test_browser_evidence.py
git commit -m "feat: verify browser evidence packets"
```

Expected: commit succeeds in `C:/dev/public/crucible`.

---

### Task 9: Emet Browser Evidence Witness Recipe

**Files:**
- Create: `C:/dev/public/pubscan/emet/examples/browser-evidence-anchor.json`
- Create: `C:/dev/public/pubscan/emet/docs/browser-evidence.md`
- Modify: `C:/dev/public/pubscan/emet/README.md`
- Test: `C:/dev/public/pubscan/emet/test_browser_evidence_docs.py`

**Interfaces:**
- Consumes:
  - Exported browser evidence bundle files.
- Produces:
  - Documented `emet anchor`, `emet verify`, and `emet audit` recipe for browser evidence exports.

- [ ] **Step 1: Write failing docs test**

Create `C:/dev/public/pubscan/emet/test_browser_evidence_docs.py`:

```python
from pathlib import Path


def test_browser_evidence_docs_name_required_commands():
    text = Path("docs/browser-evidence.md").read_text(encoding="utf-8")
    assert "emet anchor" in text
    assert "emet verify" in text
    assert "emet audit" in text
    assert "project-telos.browser-evidence/v1" in text
    assert "EMET does not control the browser" in text


def test_browser_evidence_example_has_schema():
    text = Path("examples/browser-evidence-anchor.json").read_text(encoding="utf-8")
    assert "project-telos.browser-evidence/v1" in text
    assert "artifact_hashes" in text
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest test_browser_evidence_docs.py -q`

Expected: FAIL because docs/example files do not exist.

- [ ] **Step 3: Add example**

Create `C:/dev/public/pubscan/emet/examples/browser-evidence-anchor.json`:

```json
{
  "schema": "project-telos.browser-evidence/v1",
  "evidence_export": "browser-evidence-export.json",
  "artifact_hashes": [
    {
      "ref": "artifact:after-dom.html",
      "hash": "sha256:example"
    }
  ],
  "emet_commands": [
    "emet anchor browser-evidence-export.json after-dom.html after.png",
    "emet verify browser-evidence-export.json after-dom.html after.png",
    "emet audit"
  ]
}
```

- [ ] **Step 4: Add docs**

Create `C:/dev/public/pubscan/emet/docs/browser-evidence.md`:

```markdown
# Browser Evidence Bundles

EMET can witness exported `project-telos.browser-evidence/v1` bundles after Telos writes them to disk.

EMET does not control the browser, decide browser policy, mutate artifacts, or replace Telos action receipts. It re-derives bytes from exported files and reports `MATCH`, `DRIFT`, or `UNVERIFIABLE`.

Recommended local sequence:

```powershell
emet anchor browser-evidence-export.json after-dom.html after.png
emet verify browser-evidence-export.json after-dom.html after.png
emet audit
```

Use `anchor` after the operator accepts the exported evidence bundle as the baseline. Use `verify` to check that the bundle and artifacts still match the anchored bytes. Use `audit` to re-derive EMET's own tamper-evident log chain.
```

- [ ] **Step 5: Update README**

Add:

```markdown
Browser evidence exports from Telos can be anchored with EMET after export; see `docs/browser-evidence.md`.
```

- [ ] **Step 6: Run Emet tests**

Run:

```powershell
pytest test_browser_evidence_docs.py test_membrane.py test_proof_surface_receipt.py -q
```

Expected: all selected tests pass.

- [ ] **Step 7: Commit Task 9**

Run:

```powershell
git add examples/browser-evidence-anchor.json docs/browser-evidence.md README.md test_browser_evidence_docs.py
git commit -m "docs: add browser evidence witness recipe"
```

Expected: commit succeeds in `C:/dev/public/pubscan/emet`.

---

### Task 10: BuildLang Editor Fixtures

**Files:**
- Create: `C:/dev/public/buildlang-tmLanguage/samples/browser-workflow.bld`
- Create: `C:/dev/public/buildlang-vscode/examples/browser-workflow.bld`
- Modify: `C:/dev/public/buildlang-tmLanguage/README.md`
- Modify: `C:/dev/public/buildlang-vscode/README.md`

**Interfaces:**
- Consumes:
  - Browser evidence mode vocabulary from the Telos spec.
- Produces:
  - Editor-only `.bld` examples for browser workflow/evidence language.

- [ ] **Step 1: Add TextMate sample**

Create `C:/dev/public/buildlang-tmLanguage/samples/browser-workflow.bld`:

```build
module browser_evidence_demo

effect BrowserEvidence {
    perform capture(mode: String) -> Result<String, String>
}

fn capture_source(url: String) ~ BrowserEvidence {
    let mode = "research-capture"
    let packet = perform capture(mode)
    return packet
}
```

- [ ] **Step 2: Add VS Code example**

Create `C:/dev/public/buildlang-vscode/examples/browser-workflow.bld` with the same content as the TextMate sample.

- [ ] **Step 3: Update README boundaries**

Add to both BuildLang READMEs:

```markdown
The browser evidence example is an editor fixture only. It documents Telos workflow vocabulary for highlighting and examples; this package does not compile or execute browser automation.
```

- [ ] **Step 4: Run repository validation**

Run in `C:/dev/public/buildlang-tmLanguage`:

```powershell
python -m json.tool grammars/buildlang.tmLanguage.json > $null
```

Run in `C:/dev/public/buildlang-vscode`:

```powershell
node -e "JSON.parse(require('fs').readFileSync('package.json','utf8')); JSON.parse(require('fs').readFileSync('syntaxes/buildlang.tmLanguage.json','utf8'))"
```

Expected: both commands exit 0.

- [ ] **Step 5: Commit Task 10**

Run in each repo:

```powershell
git add samples/browser-workflow.bld README.md
git commit -m "docs: add browser evidence editor fixture"
```

For VS Code repo:

```powershell
git add examples/browser-workflow.bld README.md
git commit -m "docs: add browser evidence editor fixture"
```

Expected: commits succeed in both BuildLang editor repos.

---

### Task 11: Cross-Repo Documentation And Smoke Evidence

**Files:**
- Modify: `C:/dev/public/telos/docs/CURRENT-STATE.md`
- Modify: `C:/dev/public/telos/docs/PROJECT-CONNECTION-MAP.md`
- Create: `C:/dev/public/telos/demo/research/browser-evidence-smoke.json`
- Test: `C:/dev/public/telos/demo/browser-evidence.test.mjs`

**Interfaces:**
- Consumes:
  - Completed Task 1-10 outputs.
- Produces:
  - A stable smoke packet proving the integration path has an example artifact.

- [ ] **Step 1: Add smoke packet**

Create `C:/dev/public/telos/demo/research/browser-evidence-smoke.json`:

```json
{
  "schema": "project-telos.browser-evidence-smoke/v1",
  "source_packet": "demo/integrations/browser-evidence.json",
  "pipeline_consumers": [
    "gather.browser-evidence",
    "index.browser_evidence_refs",
    "forum.project-telos-route",
    "crucible.verify_browser_evidence",
    "learn.evidenceRef",
    "emet.anchor-recipe",
    "buildlang.editor-fixture"
  ],
  "verdict": "MATCH"
}
```

- [ ] **Step 2: Update Telos docs**

Add a concise current-state note:

```markdown
Browser Evidence Kernel: Telos owns `project-telos.browser-evidence/v1`; Gather, Index, Forum, Crucible, Learn, BuildLang editor fixtures, and Emet consume packet refs rather than duplicating browser stacks.
```

- [ ] **Step 3: Run final targeted tests**

Run:

```powershell
node demo/browser-evidence.test.mjs
node demo/native-control.test.mjs
node demo/telos-mcp.test.mjs
node demo/mcp-runtime-contract.test.mjs
node demo/mcp-server-launch.test.mjs
```

Expected: all commands exit 0; live browser CDP test may remain skipped when no debug Chrome is available.

- [ ] **Step 4: Commit Task 11**

Run:

```powershell
git add docs/CURRENT-STATE.md docs/PROJECT-CONNECTION-MAP.md demo/research/browser-evidence-smoke.json
git commit -m "docs: record browser evidence pipeline smoke"
```

Expected: commit succeeds in `C:/dev/public/telos`.

---

### Task 12: Completion Audit

**Files:**
- All files touched above.

**Interfaces:**
- Consumes: Tasks 1-11.
- Produces: final evidence that the requested integration is implemented and tested across the named surfaces.

- [ ] **Step 1: Check worktrees**

Run:

```powershell
git -C C:\dev\public\telos status --short --branch
git -C C:\dev\public\gather status --short --branch
git -C C:\dev\public\learn status --short --branch
git -C C:\dev\public\index status --short --branch
git -C C:\dev\public\forum status --short --branch
git -C C:\dev\public\crucible status --short --branch
git -C C:\dev\public\pubscan\emet status --short --branch
git -C C:\dev\public\buildlang-tmLanguage status --short --branch
git -C C:\dev\public\buildlang-vscode status --short --branch
```

Expected: only intentional committed branch divergence or clean working trees; no accidental `.env`, token, browser profile, screenshot, or raw private artifact files.

- [ ] **Step 2: Run final targeted test matrix**

Run:

```powershell
node --test C:\dev\public\telos\demo\browser-evidence.test.mjs C:\dev\public\telos\demo\native-control.test.mjs C:\dev\public\telos\demo\telos-mcp.test.mjs
pytest C:\dev\public\gather\tests\test_browser_evidence.py -q
node --test C:\dev\public\learn\tests\learn-browser-evidence.test.mjs
pytest C:\dev\public\index\tests\test_browser_evidence_refs.py -q
pytest C:\dev\public\forum\tests\test_browser_workflow_routes.py -q
pytest C:\dev\public\crucible\tests\test_browser_evidence.py -q
pytest C:\dev\public\pubscan\emet\test_browser_evidence_docs.py -q
```

Expected: all selected tests pass.

- [ ] **Step 3: Run secret and artifact hygiene checks**

Run:

```powershell
rg -n "BEGIN (RSA|OPENSSH|PRIVATE)|api[_-]?key|secret|token|password|cookie" C:\dev\public\telos C:\dev\public\gather C:\dev\public\learn C:\dev\public\index C:\dev\public\forum C:\dev\public\crucible C:\dev\public\pubscan\emet C:\dev\public\buildlang-tmLanguage C:\dev\public\buildlang-vscode --glob '!**/.git/**' --glob '!**/node_modules/**' --glob '!**/dist/**'
```

Expected: no new secret material. Existing documentation-only matches must be reviewed and recorded in the final response.

- [ ] **Step 4: Verify objective coverage**

Confirm the evidence:

- Telos emits and exposes `project-telos.browser-evidence/v1`.
- Gather ingests browser evidence as source provenance.
- Index preserves browser evidence refs in context envelopes.
- Forum routes browser automation workflows.
- Crucible verifies browser evidence packet integrity.
- Learn carries evidence refs while keeping `assess` human-only.
- BuildLang editor repos include browser workflow examples without compiler claims.
- Emet documents anchor/verify/audit for exported evidence bundles.

- [ ] **Step 5: Final report**

Report:

- Commit hashes per repo.
- Test commands and pass/fail result.
- Any skipped live browser tests.
- Remaining limitations: network/console summaries are `UNVERIFIABLE` until event collectors are implemented; BuildLang compiler integration is not claimed without the compiler repo.
