import assert from "node:assert/strict";
import { mkdtempSync, readFileSync, writeFileSync } from "node:fs";

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

import { spawnSync } from "node:child_process";
import os from "node:os";
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

import { buildReadinessPacket, isPrReady } from "./showcase/record.mjs";

const matchingEvidence = {
  clone: { commit: "abc1234", root: "external/pandas" },
  reproduction: { command: "python -m pytest pandas/tests/arrays/test_masked.py -q", status: "failed-before-patch" },
  patch: {
    summary: "Preserve NumPy masked-array mask in pd.array conversion.",
    files_changed: ["pandas/core/construction.py"]
  },
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
const recordDir = mkdtempSync(path.join(os.tmpdir(), "telos-showcase-record-"));
const evidencePath = path.join(recordDir, "evidence.json");
writeFileSync(evidencePath, `${JSON.stringify(matchingEvidence, null, 2)}\n`);
const cliRecord = spawnSync(
  process.execPath,
  [
    path.join(here, "showcase.mjs"),
    "record",
    "--candidate",
    path.join(here, "showcase", "fixtures", "pandas-66050.json"),
    "--evidence",
    evidencePath,
    "--now",
    "2026-06-27T12:30:00Z",
    "--json"
  ],
  { cwd: path.resolve(here, ".."), encoding: "utf8" }
);
assert.equal(cliRecord.status, 0, cliRecord.stderr || cliRecord.stdout);
const cliRecordPayload = JSON.parse(cliRecord.stdout);
assert.equal(cliRecordPayload.schema, "project-telos.oss-pr-readiness/v1");
assert.equal(cliRecordPayload.pr_ready, true);
assert.equal(cliRecordPayload.operator_next_action, "open-pr");