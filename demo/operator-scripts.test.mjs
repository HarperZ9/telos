import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));

function runJson(script, ...args) {
  const result = spawnSync(process.execPath, [path.join(here, script), ...args], {
    cwd: path.resolve(here, ".."),
    encoding: "utf8"
  });
  assert.equal(result.status, 0, result.stderr || result.stdout);
  return JSON.parse(result.stdout);
}

const status = runJson("status.mjs");
assert.equal(status.schema, "project-telos.flagship-action/v1");
assert.equal(status.tool, "telos");
assert.equal(status.command, "status");
assert.ok(status.native.commands.includes("catalog"));
assert.ok(status.native.mcp_tools.includes("telos.catalog"));
assert.equal(status.next_actions[0].tool, "index");

const doctor = runJson("doctor.mjs");
assert.equal(doctor.command, "doctor");
assert.equal(doctor.native.checks.every((check) => check.status === "MATCH"), true);
assert.equal(doctor.next_actions[0].action, "flagship-workflow");

const room = runJson("room.mjs", "--json");
assert.equal(room.command, "room");
assert.equal(room.status, "MATCH");
assert.equal(room.native.ready, 5);
assert.equal(room.native.total, 5);
assert.equal(room.native.tools.map((tool) => tool.tool).join(","), "gather,crucible,index,forum,telos");

const roomHuman = spawnSync(process.execPath, [path.join(here, "room.mjs")], {
  cwd: path.resolve(here, ".."),
  encoding: "utf8"
});
assert.equal(roomHuman.status, 0, roomHuman.stderr || roomHuman.stdout);
assert.match(roomHuman.stdout, /^Project Telos Room/);
assert.match(roomHuman.stdout, /MATCH 5\/5 flagships ready/);

const workflow = runJson("flagship-workflow.mjs");
assert.equal(workflow.command, "flagship-workflow");
assert.equal(workflow.native.index_repo_count, 1);
assert.equal(workflow.native.gather_receipts, 1);
assert.equal(workflow.native.forum_decided, "project-telos");
assert.equal(workflow.native.forum_needs_escalation, false);
assert.equal(workflow.native.crucible_match, 1);
assert.equal(workflow.native.crucible_unverifiable, 1);
assert.equal(workflow.native.telos_demo_recheck, true);

const showcaseScout = runJson("showcase.mjs", "scout", "--fixture", "--json");
assert.equal(showcaseScout.schema, "project-telos.oss-scout/v1");
assert.equal(showcaseScout.candidates[0].repository.full_name, "pandas-dev/pandas");
assert.equal(showcaseScout.candidates[0].score.priority, 70);

const catalogSummary = spawnSync(process.execPath, [path.join(here, "catalog.mjs"), "--summary"], {
  cwd: path.resolve(here, ".."),
  encoding: "utf8"
});
assert.equal(catalogSummary.status, 0, catalogSummary.stderr || catalogSummary.stdout);
assert.match(catalogSummary.stdout, /^Project Telos MCP Catalog/m);
assert.match(catalogSummary.stdout, /tools\s+24 total, 24 available/);
assert.match(catalogSummary.stdout, /forum\s+5 tools\s+forum.route, forum.ledger.summary/);
assert.match(catalogSummary.stdout, /telos\s+6 tools\s+telos.status, telos.doctor/);
assert.match(catalogSummary.stdout, /next\s+node demo\/catalog.mjs/);
assert.ok(catalogSummary.stdout.split(/\r?\n/).length <= 12, "summary stays compact");
