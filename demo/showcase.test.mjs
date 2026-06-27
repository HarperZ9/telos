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
