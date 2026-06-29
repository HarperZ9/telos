import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { evaluateObservedServer, freshnessPacket } from "./mcp-freshness.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const packet = freshnessPacket();

assert.equal(packet.schema, "project-telos.mcp-freshness/v1");
assert.equal(packet.tool, "telos.mcp.freshness");
assert.equal(packet.validation.verdict, "MATCH");
assert.deepEqual(packet.failure_codes, [
  "stale_mcp_server",
  "tool_surface_drift",
  "version_drift",
  "behavior_probe_drift",
  "launch_profile_unresolved",
  "freshness_probe_unavailable"
]);

assert.deepEqual(Object.keys(packet.servers).sort(), [
  "crucible",
  "forum",
  "gather",
  "index",
  "telos"
]);

for (const [name, server] of Object.entries(packet.servers)) {
  assert.equal(server.flagship, name);
  assert.match(server.expected_tool_hash, /^sha256:[a-f0-9]{64}$/);
  assert.ok(server.expected_tools.length >= 1);
  assert.ok(server.status_tool.endsWith(".status"));
  assert.ok(server.expected_version);
  assert.ok(server.expected_current_status);
  assert.ok(server.probe_contract.observed_server_info_required);
  assert.ok(server.probe_contract.observed_tools_list_required);
  assert.ok(server.probe_contract.observed_status_payload_required);
  assert.ok(Array.isArray(server.behavior_probes));
  assert.ok(server.restart_hint.includes("restart"));
}

assert.equal(packet.servers.forum.expected_version, "1.12.0");
assert.equal(packet.servers.forum.behavior_probes.length, 1);
assert.deepEqual(packet.servers.forum.behavior_probes[0].expected_subset, {
  decided: "project-telos",
  needs_escalation: false
});
assert.equal(packet.servers.index.expected_tools.includes("index.context.envelope"), true);
assert.equal(packet.servers.index.expected_current_status, (
  "2.8.0 workspace atlas, certificates, freshness, benchmarking, "
  + "selection-aware context envelopes, and MCP parity"
));
assert.equal(packet.servers.index.behavior_probes.length, 1);
assert.deepEqual(packet.servers.index.behavior_probes[0].expected_subset, {
  schema: "project-telos.context-envelope/v1",
  tool: "index.context.envelope",
  verification_verdict: "MATCH",
  selection: {
    mode: "focused",
    retained_names: ["index"]
  },
  freshness: {
    schema: "index.context-envelope-freshness/v1"
  }
});
assert.equal(packet.servers.telos.status_tool, "telos.status");

const observedForumMatch = {
  server: "forum",
  initialize: { result: { serverInfo: { name: "forum", version: "1.12.0" } } },
  tools_list: {
    result: {
      tools: packet.servers.forum.expected_tools.map((name) => ({ name }))
    }
  },
  status_payload: {
    tool_version: "1.12.0",
    native: {
      current_status: packet.servers.forum.expected_current_status
    }
  },
  behavior_probes: {
    "forum-broad-telos-route": {
      result: {
        decided: "project-telos",
        needs_escalation: false
      }
    }
  }
};

const match = evaluateObservedServer("forum", observedForumMatch);
assert.equal(match.schema, "project-telos.mcp-freshness-observation/v1");
assert.equal(match.server, "forum");
assert.equal(match.verdict, "MATCH");
assert.deepEqual(match.failure_codes, []);
assert.equal(match.observed.tool_hash, packet.servers.forum.expected_tool_hash);
assert.equal(match.observed.behavior_probes["forum-broad-telos-route"].verdict, "MATCH");

const behaviorDriftForum = structuredClone(observedForumMatch);
behaviorDriftForum.behavior_probes["forum-broad-telos-route"].result = {
  decided: null,
  needs_escalation: true
};
const behaviorDrift = evaluateObservedServer("forum", behaviorDriftForum);
assert.equal(behaviorDrift.verdict, "DRIFT");
assert.deepEqual(behaviorDrift.failure_codes, ["behavior_probe_drift"]);
assert.ok(behaviorDrift.diagnostics.some((item) => item.code === "behavior_probe_drift"));

const observedIndexMatch = {
  server: "index",
  initialize: { result: { serverInfo: { name: "index-graph", version: "2.8.0" } } },
  tools_list: {
    result: {
      tools: packet.servers.index.expected_tools.map((name) => ({ name }))
    }
  },
  status_payload: {
    tool_version: "2.8.0",
    native: {
      current_status: packet.servers.index.expected_current_status
    }
  },
  behavior_probes: {
    "index-context-envelope-selection-freshness": {
      result: {
        schema: "project-telos.context-envelope/v1",
        tool: "index.context.envelope",
        verification_verdict: "MATCH",
        selection: {
          mode: "focused",
          retained_names: ["index"]
        },
        freshness: {
          schema: "index.context-envelope-freshness/v1"
        }
      }
    }
  }
};

const indexMatch = evaluateObservedServer("index", observedIndexMatch);
assert.equal(indexMatch.verdict, "MATCH");
assert.deepEqual(indexMatch.failure_codes, []);
assert.equal(
  indexMatch.observed.behavior_probes["index-context-envelope-selection-freshness"].verdict,
  "MATCH"
);

const staleIndexBehavior = structuredClone(observedIndexMatch);
delete staleIndexBehavior.behavior_probes["index-context-envelope-selection-freshness"].result.selection;
const staleIndex = evaluateObservedServer("index", staleIndexBehavior);
assert.equal(staleIndex.verdict, "DRIFT");
assert.deepEqual(staleIndex.failure_codes, ["behavior_probe_drift"]);

const staleForum = structuredClone(observedForumMatch);
staleForum.initialize.result.serverInfo.version = "1.11.0";
staleForum.status_payload.tool_version = "1.11.0";
staleForum.status_payload.native.current_status = "1.11.0 delivery ladder without model-foundry daemon routing";
staleForum.tools_list.result.tools = staleForum.tools_list.result.tools
  .filter((tool) => tool.name !== "forum.prose.humanize");

const stale = evaluateObservedServer("forum", staleForum);
assert.equal(stale.verdict, "DRIFT");
assert.deepEqual(stale.failure_codes, [
  "stale_mcp_server",
  "tool_surface_drift",
  "version_drift"
]);
assert.ok(stale.diagnostics.some((item) => item.code === "tool_surface_drift"));
assert.ok(stale.diagnostics.some((item) => item.code === "version_drift"));

const unavailable = evaluateObservedServer("forum", { server: "forum" });
assert.equal(unavailable.verdict, "UNVERIFIABLE");
assert.deepEqual(unavailable.failure_codes, ["freshness_probe_unavailable"]);

const observedPath = path.join(tmpdir(), `telos-mcp-observed-${process.pid}.json`);
writeFileSync(observedPath, JSON.stringify(observedForumMatch), "utf8");
const observedCli = spawnSync(process.execPath, [
  path.join(here, "mcp-freshness.mjs"),
  "--observed",
  observedPath
], {
  cwd: path.resolve(here, ".."),
  encoding: "utf8"
});
assert.equal(observedCli.status, 0, observedCli.stderr || observedCli.stdout);
assert.equal(JSON.parse(observedCli.stdout).verdict, "MATCH");

const cli = spawnSync(process.execPath, [path.join(here, "mcp-freshness.mjs")], {
  cwd: path.resolve(here, ".."),
  encoding: "utf8"
});
assert.equal(cli.status, 0, cli.stderr || cli.stdout);
assert.deepEqual(JSON.parse(cli.stdout), packet);

const summary = spawnSync(process.execPath, [path.join(here, "mcp-freshness.mjs"), "--summary"], {
  cwd: path.resolve(here, ".."),
  encoding: "utf8"
});
assert.equal(summary.status, 0, summary.stderr || summary.stdout);
assert.match(summary.stdout, /^Project Telos MCP Freshness/m);
assert.match(summary.stdout, /servers\s+5/);
assert.match(summary.stdout, /failure stale_mcp_server/);
