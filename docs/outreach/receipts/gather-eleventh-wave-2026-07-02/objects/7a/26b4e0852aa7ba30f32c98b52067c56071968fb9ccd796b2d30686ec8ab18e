# OSS Proof Showcase Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Telos-hosted OSS Proof Showcase lane that scores current open-source bug candidates, creates local PR-readiness packets, and demonstrates the five-flagship provenance loop without auto-opening public PRs.

**Architecture:** Keep the first slice zero-dependency and fixture-first. Telos owns the JSON contracts and command surface; generated run output stays under `demo/showcase/runs/` and out of git. Live GitHub scouting is a separate smoke path after deterministic unit tests prove the candidate and packet contracts.

**Tech Stack:** Node >= 18 ESM modules, `node:assert/strict`, `node:child_process`, `node:fs`, `node:path`, `node:url`, existing Telos action envelope helpers, GitHub CLI for optional live smoke.

## Global Constraints

- This lane is a showcase, not an auto-PR bot.
- Public communication, PR creation, and maintainer communication stay operator-gated.
- The workflow is IO protocol agnostic: CLI JSON first, MCP callable where available, file receipts as the durable interchange format.
- The first implementation must be small enough to verify locally, then extensible to more repositories and languages.
- External candidates live in isolated checkout folders outside the five flagship repos.
- Generated run output belongs under `demo/showcase/runs/<run-id>/` and stays uncommitted unless intentionally curated as a synthetic or redacted example.
- Default unit tests must not require live GitHub.
- Missing reproduction or missing test evidence blocks PR-readiness.
- No provider-specific adapter owns the workflow logic.
- Public-facing human copy must be plain enough that a non-Telos reader can understand the workflow without agent/provenance jargon.
- Receipt semantics should align with existing standards where possible: in-toto-style attestations for what happened, SBOM/AIBOM-style material inventories for compliance, and C2PA-style content authenticity for media workflows.
- Evidence updates such as refund, retry, dispute, re-run, or maintainer feedback are append-only follow-up events; do not mutate the original receipt into a stronger trust class.
- Every operator packet should expose not-verified evidence: skipped tests, files not inspected, assumptions used, and state the tools could not observe.

---

## File Structure

- Create `demo/showcase/schema.mjs`: schema constants, candidate/packet assertions, and reusable redaction checks.
- Create `demo/showcase/scoring.mjs`: deterministic candidate scoring and reason generation.
- Create `demo/showcase/standards.mjs`: standards vocabulary mapping for in-toto, SBOM/AIBOM, C2PA, and local observed receipts.
- Create `demo/showcase/scout.mjs`: fixture and live scout helpers.
- Create `demo/showcase/record.mjs`: PR-readiness packet builder and packet assertions.
- Create `demo/showcase/fixtures/pandas-66050.json`: static fixture modeled after the live pandas issue.
- Create `demo/showcase.mjs`: CLI dispatcher for `scout` and `record`.
- Create `demo/showcase.test.mjs`: fixture-backed unit and CLI smoke tests.
- Create `demo/showcase/README.md`: operator-facing workflow notes.
- Modify `demo/telos-mcp.mjs`: add a read-only `telos.showcase.scout` MCP tool after CLI behavior is stable.
- Modify `demo/integrations/mcp-tool-catalog.json`: document `telos.showcase.scout`.
- Modify `demo/integrations.test.mjs` and `demo/telos-mcp.test.mjs`: verify the catalog and MCP runtime include the new tool.
- Modify `demo/README.md` and root `README.md`: mention the showcase lane.
- Modify `.gitignore`: ignore `demo/showcase/runs/`.

---

### Task 1: Candidate Schema And Scoring

**Files:**
- Create: `demo/showcase/schema.mjs`
- Create: `demo/showcase/scoring.mjs`
- Create: `demo/showcase/standards.mjs`
- Create: `demo/showcase/fixtures/pandas-66050.json`
- Create: `demo/showcase.test.mjs`

**Interfaces:**
- Produces: `OSS_CANDIDATE_SCHEMA`, `OSS_PACKET_SCHEMA`, `assertCandidate(candidate)`, `assertNoSensitivePaths(value)`, `standardRefsFor(kind) -> string[]`, `scoreCandidate(candidate, now) -> { patchability, showcase_value, risk, priority, reasons }`.
- Consumes: no previous task.

- [ ] **Step 1: Write the failing scoring tests**

Add this initial content to `demo/showcase.test.mjs`:

```js
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

import { assertCandidate, assertNoSensitivePaths, OSS_CANDIDATE_SCHEMA } from "./showcase/schema.mjs";
import { scoreCandidate } from "./showcase/scoring.mjs";
import { standardRefsFor } from "./showcase/standards.mjs";

const pandasCandidate = JSON.parse(
  readFileSync(new URL("./showcase/fixtures/pandas-66050.json", import.meta.url), "utf8")
);

assert.equal(pandasCandidate.schema, OSS_CANDIDATE_SCHEMA);
assert.equal(assertCandidate(pandasCandidate), true);

const scored = scoreCandidate(pandasCandidate, new Date("2026-06-27T12:00:00Z"));
assert.equal(scored.patchability, 60);
assert.equal(scored.showcase_value, 10);
assert.equal(scored.risk, 0);
assert.equal(scored.priority, 70);
assert.ok(scored.reasons.includes("has reproduction"));
assert.ok(scored.reasons.includes("has expected behavior"));
assert.ok(scored.reasons.includes("updated within 14 days"));
assert.ok(scored.reasons.includes("repository has over 100k stars"));
assert.deepEqual(standardRefsFor("attestation"), ["in-toto"]);
assert.deepEqual(standardRefsFor("content-authenticity"), ["C2PA"]);

assert.throws(
  () => assertNoSensitivePaths({ path: "C:\\Users\\Zain\\secret.txt" }),
  /sensitive local path/
);
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `node demo\showcase.test.mjs`

Expected: FAIL with a module-not-found error for `demo/showcase/schema.mjs`.

- [ ] **Step 3: Create the pandas fixture**

Create `demo/showcase/fixtures/pandas-66050.json`:

```json
{
  "schema": "project-telos.oss-candidate/v1",
  "captured_at": "2026-06-27T07:05:00Z",
  "repository": {
    "full_name": "pandas-dev/pandas",
    "url": "https://github.com/pandas-dev/pandas",
    "stars": 491000,
    "language": "Python",
    "open_issues": 3500
  },
  "issue": {
    "number": 66050,
    "url": "https://github.com/pandas-dev/pandas/issues/66050",
    "title": "BUG: pd.array() silently drops missing values when converting NumPy masked arrays",
    "labels": ["Bug", "Needs Triage"],
    "comments_count": 0,
    "updated_at": "2026-06-27T06:58:11Z"
  },
  "signals": {
    "has_reproduction": true,
    "has_expected_behavior": true,
    "maintainer_invited_pr": false,
    "likely_docs_only": false,
    "requires_gpu_or_large_model": false,
    "security_sensitive": false,
    "ambiguous_expected_behavior": false
  },
  "standards": {
    "attestation": ["in-toto"],
    "inventory": ["SBOM", "AIBOM"],
    "content_authenticity": ["C2PA"],
    "observation_class": "client_observed"
  },
  "score": {
    "patchability": 0,
    "showcase_value": 0,
    "risk": 0,
    "priority": 0,
    "reasons": []
  },
  "next_actions": []
}
```

- [ ] **Step 4: Create schema helpers**

Create `demo/showcase/schema.mjs`:

```js
export const OSS_CANDIDATE_SCHEMA = "project-telos.oss-candidate/v1";
export const OSS_PACKET_SCHEMA = "project-telos.oss-pr-readiness/v1";

export function assertCandidate(candidate) {
  if (candidate?.schema !== OSS_CANDIDATE_SCHEMA) {
    throw new Error(`bad candidate schema: ${candidate?.schema}`);
  }
  for (const key of ["repository", "issue", "signals", "score", "next_actions"]) {
    if (!(key in candidate)) {
      throw new Error(`missing candidate key: ${key}`);
    }
  }
  for (const key of ["full_name", "url", "stars", "language", "open_issues"]) {
    if (!(key in candidate.repository)) {
      throw new Error(`missing repository key: ${key}`);
    }
  }
  for (const key of ["number", "url", "title", "labels", "comments_count", "updated_at"]) {
    if (!(key in candidate.issue)) {
      throw new Error(`missing issue key: ${key}`);
    }
  }
  return true;
}

export function assertPacket(packet) {
  if (packet?.schema !== OSS_PACKET_SCHEMA) {
    throw new Error(`bad packet schema: ${packet?.schema}`);
  }
  for (const key of ["candidate", "evidence", "verdict", "operator_next_action", "pr_ready"]) {
    if (!(key in packet)) {
      throw new Error(`missing packet key: ${key}`);
    }
  }
  assertNoSensitivePaths(packet);
  return true;
}

export function assertNoSensitivePaths(value) {
  const text = JSON.stringify(value);
  if (/C:\\\\Users\\\\[^"\\]+/i.test(text)) {
    throw new Error("sensitive local path detected");
  }
  if (/\.env(?:\.|["\\/\s]|$)/i.test(text)) {
    throw new Error("environment file reference detected");
  }
  if (/(api[_-]?key|access[_-]?token|password)\s*[:=]\s*[^"'\s]{8,}/i.test(text)) {
    throw new Error("token-like field detected");
  }
  return true;
}
```

- [ ] **Step 5: Create standards helper**

Create `demo/showcase/standards.mjs`:

```js
const refs = new Map([
  ["attestation", ["in-toto"]],
  ["inventory", ["SBOM", "AIBOM"]],
  ["content-authenticity", ["C2PA"]],
  ["client-observed", ["Project Telos client_observed receipt"]]
]);

export function standardRefsFor(kind) {
  return refs.get(kind) || [];
}
```

- [ ] **Step 6: Create scoring helpers**

Create `demo/showcase/scoring.mjs`:

```js
import { assertCandidate } from "./schema.mjs";

const DAY_MS = 24 * 60 * 60 * 1000;

export function scoreCandidate(candidate, now = new Date()) {
  assertCandidate(candidate);
  const reasons = [];
  let patchability = 0;
  let showcaseValue = 0;
  let risk = 0;

  if (candidate.signals.has_reproduction) {
    patchability += 30;
    reasons.push("has reproduction");
  }
  if (candidate.signals.has_expected_behavior) {
    patchability += 20;
    reasons.push("has expected behavior");
  }
  const updatedAt = new Date(candidate.issue.updated_at);
  if (!Number.isNaN(updatedAt.valueOf()) && now - updatedAt <= 14 * DAY_MS) {
    patchability += 10;
    reasons.push("updated within 14 days");
  }
  if (candidate.signals.maintainer_invited_pr) {
    showcaseValue += 25;
    reasons.push("maintainer invited PR");
  }
  if (candidate.repository.stars >= 100000) {
    showcaseValue += 10;
    reasons.push("repository has over 100k stars");
  }
  if (candidate.signals.requires_gpu_or_large_model) {
    risk += 35;
    reasons.push("requires GPU or large model");
  }
  if (candidate.signals.security_sensitive) {
    risk += 40;
    reasons.push("security sensitive");
  }
  if (candidate.signals.ambiguous_expected_behavior) {
    risk += 25;
    reasons.push("ambiguous expected behavior");
  }

  const priority = candidate.signals.has_reproduction
    ? Math.max(0, patchability + showcaseValue - risk)
    : 0;

  return {
    patchability,
    showcase_value: showcaseValue,
    risk,
    priority,
    reasons
  };
}

export function attachScore(candidate, now = new Date()) {
  return {
    ...candidate,
    score: scoreCandidate(candidate, now)
  };
}
```

- [ ] **Step 7: Run the test to verify it passes**

Run: `node demo\showcase.test.mjs`

Expected: PASS with no output.

- [ ] **Step 8: Commit**

```bash
git add demo/showcase/schema.mjs demo/showcase/scoring.mjs demo/showcase/standards.mjs demo/showcase/fixtures/pandas-66050.json demo/showcase.test.mjs
git commit -m "feat(showcase): add oss candidate schema and scoring"
```

---

### Task 2: Fixture-First Scout CLI

**Files:**
- Create: `demo/showcase/scout.mjs`
- Create: `demo/showcase.mjs`
- Modify: `demo/showcase.test.mjs`
- Modify: `.gitignore`

**Interfaces:**
- Consumes: `attachScore(candidate, now)`, `assertCandidate(candidate)`.
- Produces: `scoutFixture({ now }) -> payload`, `scoutLive({ query, limit, run }) -> payload`, `renderScoutTable(payload) -> string`, CLI `node demo/showcase.mjs scout --fixture --json`.

- [ ] **Step 1: Add failing scout tests**

Append to `demo/showcase.test.mjs`:

```js
import { spawnSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { scoutFixture, renderScoutTable } from "./showcase/scout.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const fixtureScout = scoutFixture({ now: new Date("2026-06-27T12:00:00Z") });
assert.equal(fixtureScout.schema, "project-telos.oss-scout/v1");
assert.equal(fixtureScout.candidates.length, 1);
assert.equal(fixtureScout.candidates[0].score.priority, 70);
assert.match(renderScoutTable(fixtureScout), /pandas-dev\/pandas#66050/);

const cliScout = spawnSync(process.execPath, [path.join(here, "showcase.mjs"), "scout", "--fixture", "--json"], {
  cwd: path.resolve(here, ".."),
  encoding: "utf8"
});
assert.equal(cliScout.status, 0, cliScout.stderr || cliScout.stdout);
const cliScoutPayload = JSON.parse(cliScout.stdout);
assert.equal(cliScoutPayload.schema, "project-telos.oss-scout/v1");
assert.equal(cliScoutPayload.candidates[0].issue.number, 66050);

const cliScoutHuman = spawnSync(process.execPath, [path.join(here, "showcase.mjs"), "scout", "--fixture"], {
  cwd: path.resolve(here, ".."),
  encoding: "utf8"
});
assert.equal(cliScoutHuman.status, 0, cliScoutHuman.stderr || cliScoutHuman.stdout);
assert.match(cliScoutHuman.stdout, /^OSS Proof Showcase Candidates/);
```

- [ ] **Step 2: Run test to verify it fails**

Run: `node demo\showcase.test.mjs`

Expected: FAIL with a module-not-found error for `demo/showcase/scout.mjs`.

- [ ] **Step 3: Create scout helper**

Create `demo/showcase/scout.mjs`:

```js
import { readFileSync } from "node:fs";
import { spawnSync } from "node:child_process";

import { attachScore } from "./scoring.mjs";
import { assertCandidate } from "./schema.mjs";

const fixtureUrl = new URL("./fixtures/pandas-66050.json", import.meta.url);

export function scoutFixture({ now = new Date() } = {}) {
  const candidate = attachScore(JSON.parse(readFileSync(fixtureUrl, "utf8")), now);
  return {
    schema: "project-telos.oss-scout/v1",
    captured_at: now.toISOString(),
    source: {
      kind: "fixture",
      query: "pandas-dev/pandas#66050"
    },
    candidates: [candidate]
  };
}

export function scoutLive({ query, limit = 5, now = new Date(), run = spawnSync } = {}) {
  const searchQuery = query || 'repo:pandas-dev/pandas is:issue is:open label:Bug pd.array masked array';
  const result = run("gh", [
    "search",
    "issues",
    searchQuery,
    "--limit",
    String(limit),
    "--json",
    "title,number,url,updatedAt,labels,commentsCount,repository"
  ], { encoding: "utf8" });
  if (result.status !== 0) {
    return {
      schema: "project-telos.oss-scout/v1",
      captured_at: now.toISOString(),
      status: "UNVERIFIABLE",
      source: { kind: "github", query: searchQuery },
      candidates: [],
      diagnostics: [{ message: result.stderr || result.stdout || "gh search failed" }]
    };
  }
  const rows = JSON.parse(result.stdout);
  const candidates = rows.map((row) => attachScore(candidateFromIssue(row, now), now));
  return {
    schema: "project-telos.oss-scout/v1",
    captured_at: now.toISOString(),
    status: "MATCH",
    source: { kind: "github", query: searchQuery },
    candidates
  };
}

export function candidateFromIssue(row, now = new Date()) {
  const fullName = row.repository?.nameWithOwner || "unknown/unknown";
  const labels = (row.labels || []).map((label) => label.name || label);
  const candidate = {
    schema: "project-telos.oss-candidate/v1",
    captured_at: now.toISOString(),
    repository: {
      full_name: fullName,
      url: `https://github.com/${fullName}`,
      stars: 0,
      language: "unknown",
      open_issues: 0
    },
    issue: {
      number: row.number,
      url: row.url,
      title: row.title,
      labels,
      comments_count: row.commentsCount ?? 0,
      updated_at: row.updatedAt
    },
    signals: inferSignals(row),
    score: {
      patchability: 0,
      showcase_value: 0,
      risk: 0,
      priority: 0,
      reasons: []
    },
    next_actions: []
  };
  assertCandidate(candidate);
  return candidate;
}

function inferSignals(row) {
  const text = `${row.title || ""}\n${row.body || ""}`.toLowerCase();
  return {
    has_reproduction: /repro|reproduction|steps to reproduce|example/.test(text),
    has_expected_behavior: /expected/.test(text),
    maintainer_invited_pr: /sure thing|pr welcome|pull request welcome/.test(text),
    likely_docs_only: /doc|readme|typo/.test(text),
    requires_gpu_or_large_model: /gpu|cuda|large model|oom/.test(text),
    security_sensitive: /security|cve|credential|token/.test(text),
    ambiguous_expected_behavior: !/expected/.test(text)
  };
}

export function renderScoutTable(payload) {
  const lines = ["OSS Proof Showcase Candidates", "priority  repo#issue  title"];
  for (const candidate of payload.candidates) {
    lines.push(
      `${String(candidate.score.priority).padStart(8)}  ${candidate.repository.full_name}#${candidate.issue.number}  ${candidate.issue.title}`
    );
  }
  return `${lines.join("\n")}\n`;
}
```

- [ ] **Step 4: Create CLI dispatcher**

Create `demo/showcase.mjs`:

```js
import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import { scoutFixture, scoutLive, renderScoutTable } from "./showcase/scout.mjs";

function has(flag) {
  return process.argv.includes(flag);
}

function valueAfter(flag, fallback = undefined) {
  const index = process.argv.indexOf(flag);
  return index === -1 ? fallback : process.argv[index + 1];
}

function writeOutput(payload) {
  const out = valueAfter("--out");
  if (!out) {
    return;
  }
  mkdirSync(out, { recursive: true });
  writeFileSync(path.join(out, "scout.json"), `${JSON.stringify(payload, null, 2)}\n`);
}

function main() {
  const command = process.argv[2];
  if (command !== "scout") {
    process.stderr.write("usage: node demo/showcase.mjs scout [--fixture] [--json] [--out DIR]\n");
    return 2;
  }
  const now = new Date(valueAfter("--now", new Date().toISOString()));
  const payload = has("--fixture")
    ? scoutFixture({ now })
    : scoutLive({ query: valueAfter("--query"), limit: Number(valueAfter("--limit", "5")), now });
  writeOutput(payload);
  if (has("--json")) {
    process.stdout.write(`${JSON.stringify(payload, null, 2)}\n`);
  } else {
    process.stdout.write(renderScoutTable(payload));
  }
  return 0;
}

if (import.meta.url === `file://${process.argv[1].replace(/\\/g, "/")}`) {
  process.exitCode = main();
}
```

- [ ] **Step 5: Ignore generated runs**

Append this line to `.gitignore`:

```gitignore
demo/showcase/runs/
```

- [ ] **Step 6: Run test to verify it passes**

Run: `node demo\showcase.test.mjs`

Expected: PASS with no output.

- [ ] **Step 8: Commit**

```bash
git add .gitignore demo/showcase/scout.mjs demo/showcase.mjs demo/showcase.test.mjs
git commit -m "feat(showcase): add fixture scout cli"
```

---

### Task 3: PR-Readiness Packet Builder

**Files:**
- Create: `demo/showcase/record.mjs`
- Modify: `demo/showcase.mjs`
- Modify: `demo/showcase.test.mjs`

**Interfaces:**
- Consumes: `assertPacket(packet)`, fixture candidate.
- Produces: `buildReadinessPacket({ candidate, evidence, now }) -> packet`, `isPrReady(packet) -> boolean`, CLI `node demo/showcase.mjs record --candidate FILE --evidence FILE --json`.

- [ ] **Step 1: Add failing record tests**

Append to `demo/showcase.test.mjs`:

```js
import { buildReadinessPacket, isPrReady } from "./showcase/record.mjs";

const matchingEvidence = {
  clone: { commit: "abc1234", root: "external/pandas" },
  reproduction: { command: "python -m pytest pandas/tests/arrays/test_masked.py -q", status: "failed-before-patch" },
  patch: { summary: "Preserve NumPy masked-array mask in pd.array conversion.", files_changed: ["pandas/core/construction.py"] },
  tests: [{ command: "python -m pytest pandas/tests/arrays/test_masked.py -q", status: "passed" }],
  crucible: { verdict: "MATCH", detail: "before failure and after pass observed" },
  not_verified: {
    files_not_inspected: ["pandas/_libs/**/*.pyx"],
    tests_skipped: ["full pandas test suite"],
    assumptions: ["issue reproduction remains valid on main"],
    unobserved_state: ["upstream maintainer intent"]
  },
  follow_up_events: [
    { kind: "maintainer-feedback", status: "pending", appended_at: "2026-06-27T12:30:00Z" }
  ],
  risk_notes: ["untriaged upstream issue"]
};

const readyPacket = buildReadinessPacket({
  candidate: pandasCandidate,
  evidence: matchingEvidence,
  now: new Date("2026-06-27T12:30:00Z")
});
assert.equal(readyPacket.schema, "project-telos.oss-pr-readiness/v1");
assert.equal(isPrReady(readyPacket), true);
assert.equal(readyPacket.operator_next_action, "open-pr");
assert.match(readyPacket.public_pr_draft.title, /pandas-dev\/pandas#66050/);

const blockedPacket = buildReadinessPacket({
  candidate: pandasCandidate,
  evidence: { ...matchingEvidence, tests: [] },
  now: new Date("2026-06-27T12:30:00Z")
});
assert.equal(isPrReady(blockedPacket), false);
assert.equal(blockedPacket.operator_next_action, "revise");
assert.ok(blockedPacket.blockers.includes("missing passing test evidence"));
```

- [ ] **Step 2: Run test to verify it fails**

Run: `node demo\showcase.test.mjs`

Expected: FAIL with a module-not-found error for `demo/showcase/record.mjs`.

- [ ] **Step 3: Create record helper**

Create `demo/showcase/record.mjs`:

```js
import { assertCandidate, assertPacket, OSS_PACKET_SCHEMA } from "./schema.mjs";

export function buildReadinessPacket({ candidate, evidence, now = new Date() }) {
  assertCandidate(candidate);
  const blockers = blockersForEvidence(evidence);
  const prReady = blockers.length === 0;
  const packet = {
    schema: OSS_PACKET_SCHEMA,
    captured_at: now.toISOString(),
    candidate: {
      repository: candidate.repository.full_name,
      issue: candidate.issue.number,
      issue_url: candidate.issue.url,
      candidate_schema: candidate.schema
    },
    evidence,
    verdict: evidence.crucible?.verdict || "UNVERIFIABLE",
    blockers,
    pr_ready: prReady,
    operator_next_action: prReady ? "open-pr" : "revise",
    public_pr_draft: prReady ? prDraft(candidate, evidence) : null
  };
  assertPacket(packet);
  return packet;
}

export function isPrReady(packet) {
  assertPacket(packet);
  return packet.pr_ready === true && packet.operator_next_action === "open-pr";
}

function blockersForEvidence(evidence = {}) {
  const blockers = [];
  if (!evidence.reproduction?.command) {
    blockers.push("missing reproduction command");
  }
  if (!Array.isArray(evidence.tests) || !evidence.tests.some((test) => test.status === "passed")) {
    blockers.push("missing passing test evidence");
  }
  if (evidence.crucible?.verdict !== "MATCH") {
    blockers.push("crucible verdict is not MATCH");
  }
  if (!evidence.patch?.summary) {
    blockers.push("missing patch summary");
  }
  return blockers;
}

function prDraft(candidate, evidence) {
  return {
    title: `Fix ${candidate.repository.full_name}#${candidate.issue.number}: ${candidate.issue.title}`,
    body: [
      "## Summary",
      evidence.patch.summary,
      "",
      "## Evidence",
      `- Reproduction: ${evidence.reproduction.command}`,
      ...evidence.tests.map((test) => `- Test: ${test.command} -> ${test.status}`),
      `- Crucible: ${evidence.crucible.verdict}`,
      "",
      "## Provenance",
      `Candidate: ${candidate.issue.url}`,
      "",
      "## Not verified",
      ...(evidence.not_verified?.tests_skipped || []).map((item) => `- Skipped test scope: ${item}`),
      ...(evidence.not_verified?.assumptions || []).map((item) => `- Assumption: ${item}`),
      "Generated by Project Telos OSS Proof Showcase. Public submission remains operator-gated."
    ].join("\n")
  };
}
```

- [ ] **Step 4: Extend CLI dispatcher**

Add these imports to `demo/showcase.mjs`:

```js
import { readFileSync } from "node:fs";
import { buildReadinessPacket } from "./showcase/record.mjs";
```

Replace the usage branch in `main()` with:

```js
  if (!["scout", "record"].includes(command)) {
    process.stderr.write("usage: node demo/showcase.mjs scout|record [--json]\n");
    return 2;
  }
```

Add this branch before the scout branch:

```js
  if (command === "record") {
    const candidatePath = valueAfter("--candidate");
    const evidencePath = valueAfter("--evidence");
    if (!candidatePath || !evidencePath) {
      process.stderr.write("record requires --candidate FILE --evidence FILE\n");
      return 2;
    }
    const packet = buildReadinessPacket({
      candidate: JSON.parse(readFileSync(candidatePath, "utf8")),
      evidence: JSON.parse(readFileSync(evidencePath, "utf8")),
      now
    });
    if (has("--json")) {
      process.stdout.write(`${JSON.stringify(packet, null, 2)}\n`);
    } else {
      process.stdout.write(`${packet.pr_ready ? "PR-ready" : "Not PR-ready"}: ${packet.operator_next_action}\n`);
    }
    return 0;
  }
```

- [ ] **Step 5: Run test to verify it passes**

Run: `node demo\showcase.test.mjs`

Expected: PASS with no output.

- [ ] **Step 6: Commit**

```bash
git add demo/showcase/record.mjs demo/showcase.mjs demo/showcase.test.mjs
git commit -m "feat(showcase): add pr readiness packets"
```

---

### Task 4: Operator Docs And Command Smoke

**Files:**
- Create: `demo/showcase/README.md`
- Modify: `demo/README.md`
- Modify: `README.md`
- Modify: `demo/operator-scripts.test.mjs`

**Interfaces:**
- Consumes: `node demo/showcase.mjs scout --fixture --json`.
- Produces: documented CLI workflow and operator script smoke coverage.

- [ ] **Step 1: Add failing operator smoke assertions**

Append to `demo/operator-scripts.test.mjs`:

```js
const showcaseScout = runJson("showcase.mjs", "scout", "--fixture", "--json");
assert.equal(showcaseScout.schema, "project-telos.oss-scout/v1");
assert.equal(showcaseScout.candidates[0].repository.full_name, "pandas-dev/pandas");
assert.equal(showcaseScout.candidates[0].score.priority, 70);
```

- [ ] **Step 2: Run test to verify it passes after prior tasks**

Run: `node demo\operator-scripts.test.mjs`

Expected: PASS with no output.

- [ ] **Step 3: Create operator docs**

Create `demo/showcase/README.md`:

```markdown
# OSS Proof Showcase

The OSS Proof Showcase is a Telos lane for finding public bug candidates,
capturing evidence, and producing local PR-readiness packets. It does not open
PRs or post upstream comments by itself.

## Fixture Scout

```powershell
node demo\showcase.mjs scout --fixture
node demo\showcase.mjs scout --fixture --json
```

The fixture is modeled after `pandas-dev/pandas#66050` and keeps default tests
offline and deterministic.

## Live Scout

```powershell
node demo\showcase.mjs scout --query "repo:pandas-dev/pandas is:issue is:open label:Bug pd.array masked array" --limit 5 --json
```

The live scout requires the GitHub CLI. It records failures as unverifiable
candidate capture rather than guessing.

## PR-Readiness Packet

```powershell
node demo\showcase.mjs record --candidate demo\showcase\fixtures\pandas-66050.json --evidence path\to\evidence.json --json
```

The packet becomes PR-ready only when reproduction, patch summary, passing test
evidence, and a `MATCH` Crucible verdict are present.

Every packet includes a `not_verified` section for skipped tests, files not
inspected, assumptions, and unobserved state. Later retry, refund, dispute,
maintainer feedback, or re-run events append to `follow_up_events`; they do not
rewrite the original evidence.
```

- [ ] **Step 4: Update demo README**

Add this paragraph to `demo/README.md` after the operator-spine script list:

```markdown
`showcase.mjs` starts the OSS Proof Showcase lane. It can rank a fixture-backed
candidate offline and, when the GitHub CLI is available, scout live public
issues without making public changes.
```

- [ ] **Step 5: Update root README current status**

Add this sentence under the root README current status block:

```markdown
- **Proof lane:** `node demo/showcase.mjs scout --fixture` starts the OSS Proof Showcase, a local-first path from public issue evidence to PR-readiness packets.
```

- [ ] **Step 6: Run documentation smoke**

Run: `node demo\operator-scripts.test.mjs`

Expected: PASS with no output.

- [ ] **Step 8: Commit**

```bash
git add README.md demo/README.md demo/operator-scripts.test.mjs demo/showcase/README.md
git commit -m "docs(showcase): document oss proof lane"
```

---

### Task 5: MCP Catalog Read-Only Scout Surface

**Files:**
- Modify: `demo/telos-mcp.mjs`
- Modify: `demo/telos-mcp.test.mjs`
- Modify: `demo/integrations/mcp-tool-catalog.json`
- Modify: `demo/integrations.test.mjs`
- Modify: `demo/mcp-runtime-contract.test.mjs`

**Interfaces:**
- Consumes: CLI `node demo/showcase.mjs scout --fixture --json`.
- Produces: MCP tool `telos.showcase.scout` and catalog entry.

- [ ] **Step 1: Add failing MCP test assertions**

In `demo/telos-mcp.test.mjs`, add `telos.showcase.scout` to the expected tool names and add a `tools/call` assertion:

```js
assert.ok(toolNames.has("telos.showcase.scout"));

const showcase = handleRequest({
  jsonrpc: "2.0",
  id: 8,
  method: "tools/call",
  params: { name: "telos.showcase.scout", arguments: {} }
});
assert.equal(showcase.result.structuredContent.schema, "project-telos.oss-scout/v1");
assert.equal(showcase.result.structuredContent.candidates[0].issue.number, 66050);
```

- [ ] **Step 2: Run test to verify it fails**

Run: `node demo\telos-mcp.test.mjs`

Expected: FAIL because `telos.showcase.scout` is not listed.

- [ ] **Step 3: Add MCP tool**

In `demo/telos-mcp.mjs`, add this tool object to `tools`:

```js
  {
    name: "telos.showcase.scout",
    description: "Return the fixture-backed OSS Proof Showcase scout results as structured content.",
    inputSchema: emptyInputSchema
  }
```

Add this entry to `toolScripts`:

```js
  ["telos.showcase.scout", ["showcase.mjs", "scout", "--fixture", "--json"]]
```

- [ ] **Step 4: Update catalog**

Add this object to `demo/integrations/mcp-tool-catalog.json` under `tools`:

```json
{
  "name": "telos.showcase.scout",
  "flagship": "telos",
  "description": "Return fixture-backed OSS Proof Showcase candidate rankings.",
  "cli": ["node", "demo/showcase.mjs", "scout", "--fixture", "--json"],
  "mcp": {
    "status": "available",
    "server": "telos",
    "method": "tools/call",
    "tool": "telos.showcase.scout"
  },
  "next_actions": ["gather.docs", "index.map", "crucible.assess"]
}
```

- [ ] **Step 5: Update integration tests**

In `demo/integrations.test.mjs`, add `telos.showcase.scout` to the expected names list.

Run: `node demo\integrations.test.mjs`

Expected: PASS with no output.

- [ ] **Step 6: Run MCP contract tests**

Run:

```bash
node demo\telos-mcp.test.mjs
node demo\mcp-runtime-contract.test.mjs
```

Expected: both PASS with no output.

- [ ] **Step 8: Commit**

```bash
git add demo/telos-mcp.mjs demo/telos-mcp.test.mjs demo/integrations/mcp-tool-catalog.json demo/integrations.test.mjs demo/mcp-runtime-contract.test.mjs
git commit -m "feat(showcase): expose scout over telos mcp"
```

---

### Task 6: Live GitHub Smoke And Final Verification

**Files:**
- Create: `demo/showcase-live-smoke.mjs`
- Modify: `demo/showcase/README.md`
- Modify: `CHANGELOG.md`

**Interfaces:**
- Consumes: `scoutLive({ query, limit })`.
- Produces: optional live smoke command and changelog entry.

- [ ] **Step 1: Add live smoke script**

Create `demo/showcase-live-smoke.mjs`:

```js
import { scoutLive, renderScoutTable } from "./showcase/scout.mjs";

const payload = scoutLive({
  query: 'repo:pandas-dev/pandas is:issue is:open label:Bug pd.array masked array',
  limit: 5
});

if (payload.status === "UNVERIFIABLE") {
  process.stderr.write(`${JSON.stringify(payload.diagnostics || [], null, 2)}\n`);
  process.exitCode = 2;
} else {
  process.stdout.write(renderScoutTable(payload));
}
```

- [ ] **Step 2: Document live smoke**

Add this paragraph to `demo/showcase/README.md`:

```markdown
## Live Smoke

`node demo/showcase-live-smoke.mjs` queries GitHub for the current pandas
candidate family. It is not part of the default unit test slice because it
requires network access and GitHub CLI authentication.
```

- [ ] **Step 3: Update changelog**

Add this entry at the top of `CHANGELOG.md` under `## Unreleased`:

```markdown
- OSS Proof Showcase: adds a fixture-first candidate scout, PR-readiness packet
  contract, read-only Telos MCP scout tool, and an optional live GitHub smoke
  command for high-star public issue discovery.
- Feedback integration: adds plain-language operator copy, standards vocabulary
  for in-toto/SBOM/AIBOM/C2PA alignment, append-only follow-up events, and
  `not_verified` packet fields for skipped checks and unobserved state.
```

- [ ] **Step 4: Run default verification**

Run:

```bash
node demo\showcase.test.mjs
node demo\operator-scripts.test.mjs
node demo\integrations.test.mjs
node demo\telos-mcp.test.mjs
node demo\mcp-runtime-contract.test.mjs
```

Expected: all PASS with no output.

- [ ] **Step 5: Run optional live smoke**

Run: `node demo\showcase-live-smoke.mjs`

Expected with network and `gh` available: exit 0 and a table headed `OSS Proof Showcase Candidates`.

Expected without network or `gh`: exit 2 with diagnostics; this does not fail the default test slice.

- [ ] **Step 6: Run housekeeping checks**

Run:

```bash
git diff --check
rg -n "(T[B]D|T[O]DO|implement\s+later|fill\s+in\s+details|place\s*holder)" demo docs README.md CHANGELOG.md
```

Expected: `git diff --check` exits 0, and `rg` finds no open marker text outside historical docs.

- [ ] **Step 8: Commit**

```bash
git add CHANGELOG.md demo/showcase-live-smoke.mjs demo/showcase/README.md
git commit -m "chore(showcase): add live scout smoke"
```

---

## Self-Review Checklist

- Spec coverage: Tasks 1 through 6 cover candidate schema, deterministic scoring, scout, record packet, blocked readiness, docs, MCP compatibility, generated-output hygiene, live smoke separation, operator-gated public PR behavior, standards vocabulary, append-only follow-up events, and not-verified packet fields.
- Type consistency: `project-telos.oss-candidate/v1`, `project-telos.oss-scout/v1`, and `project-telos.oss-pr-readiness/v1` are used consistently.
- Test coverage: default tests are offline; live GitHub is explicitly separated.
- Security posture: generated runs are ignored, token-like fields and local home paths are rejected, and public PR submission is not automated.
