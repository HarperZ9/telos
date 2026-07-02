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
assert.ok(status.native.commands.includes("server-manifest"));
assert.ok(status.native.mcp_tools.includes("telos.catalog"));
assert.ok(status.native.mcp_tools.includes("telos.server.manifest"));
assert.ok(status.native.mcp_tools.includes("telos.mcp.freshness"));
assert.ok(status.native.mcp_tools.includes("telos.ci.doctor"));
assert.ok(status.native.mcp_tools.includes("telos.ci.triage"));
assert.ok(status.native.mcp_tools.includes("telos.presentation.doctor"));
assert.ok(status.native.mcp_tools.includes("telos.accessibility.doctor"));
assert.ok(status.native.mcp_tools.includes("telos.performance.doctor"));
assert.ok(status.native.mcp_tools.includes("telos.compatibility.doctor"));
assert.ok(status.native.mcp_tools.includes("telos.operator.doctor"));
assert.ok(status.native.mcp_tools.includes("telos.admission.telemetry"));
assert.ok(status.native.mcp_tools.includes("telos.context.envelope"));
assert.ok(status.native.mcp_tools.includes("telos.context.pack"));
assert.ok(status.native.mcp_tools.includes("telos.action.receipt"));
assert.ok(status.native.mcp_tools.includes("telos.loop.ledger"));
assert.ok(status.native.mcp_tools.includes("telos.objective.monitor"));
assert.ok(status.native.mcp_tools.includes("telos.model.foundry"));
assert.ok(status.native.mcp_tools.includes("telos.research.seed"));
assert.ok(status.native.mcp_tools.includes("telos.learning.forge"));
assert.ok(status.native.mcp_tools.includes("telos.learning.labs"));
assert.ok(status.native.mcp_tools.includes("telos.research.thermodynamic"));
assert.ok(status.native.mcp_tools.includes("telos.rendering.research"));
assert.ok(status.native.mcp_tools.includes("telos.rendering.capabilities"));
assert.ok(status.native.mcp_tools.includes("telos.measurement.layers"));
assert.ok(status.native.mcp_tools.includes("telos.creative.engine"));
assert.ok(status.native.mcp_tools.includes("telos.creative.kernels"));
assert.ok(status.native.mcp_tools.includes("telos.revival.registry"));
assert.ok(status.native.mcp_tools.includes("telos.second_level.queue"));
assert.ok(status.native.mcp_tools.includes("telos.workstation.substrate"));
assert.ok(status.native.mcp_tools.includes("telos.display.calibration"));
assert.ok(status.native.mcp_tools.includes("telos.native.control"));
assert.ok(status.native.mcp_tools.includes("telos.browser.evidence"));
assert.ok(status.native.mcp_tools.includes("telos.showcase.scout"));
assert.match(status.native.current_status, /69-tool/);
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
assert.match(catalogSummary.stdout, /tools\s+69 total, 69 available/);
assert.match(catalogSummary.stdout, /telos\s+41 tools\s+telos.status, telos.doctor/);
assert.match(catalogSummary.stdout, /next\s+node demo\/catalog.mjs/);
assert.ok(catalogSummary.stdout.split(/\r?\n/).length <= 12, "summary stays compact");
