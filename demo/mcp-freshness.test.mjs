import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { freshnessPacket } from "./mcp-freshness.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const packet = freshnessPacket();

assert.equal(packet.schema, "project-telos.mcp-freshness/v1");
assert.equal(packet.tool, "telos.mcp.freshness");
assert.equal(packet.validation.verdict, "MATCH");
assert.deepEqual(packet.failure_codes, [
  "stale_mcp_server",
  "tool_surface_drift",
  "version_drift",
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
  assert.ok(server.restart_hint.includes("restart"));
}

assert.equal(packet.servers.forum.expected_version, "1.12.0");
assert.equal(packet.servers.index.expected_tools.includes("index.context.envelope"), true);
assert.equal(packet.servers.telos.status_tool, "telos.status");

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
