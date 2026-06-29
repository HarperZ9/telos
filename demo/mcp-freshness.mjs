import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";

const manifest = JSON.parse(
  readFileSync(new URL("./integrations/mcp-server-manifest.json", import.meta.url), "utf8")
);

export const FAILURE_CODES = [
  "stale_mcp_server",
  "tool_surface_drift",
  "version_drift",
  "launch_profile_unresolved",
  "freshness_probe_unavailable"
];

function sha256(value) {
  return `sha256:${createHash("sha256").update(value).digest("hex")}`;
}

function expectedToolHash(tools) {
  return sha256(JSON.stringify([...tools].sort()));
}

function serverPacket(name, server) {
  return {
    flagship: server.flagship,
    status_tool: server.freshness.status_tool,
    expected_version: server.freshness.expected_version,
    expected_current_status: server.freshness.expected_current_status,
    expected_tools: server.expected_tools,
    expected_tool_hash: expectedToolHash(server.expected_tools),
    probe_contract: {
      observed_server_info_required: true,
      observed_tools_list_required: true,
      observed_status_payload_required: true,
      compare_server_info_version_to: "expected_version",
      compare_status_tool_version_to: "expected_version",
      compare_tools_list_hash_to: "expected_tool_hash"
    },
    failure_codes: server.freshness.failure_codes,
    restart_hint: `restart ${name} MCP server from telos.server.manifest source_checkout profile when observed values drift`
  };
}

export function freshnessPacket() {
  const servers = {};
  for (const [name, server] of Object.entries(manifest.servers)) {
    servers[name] = serverPacket(name, server);
  }
  return {
    schema: "project-telos.mcp-freshness/v1",
    tool: "telos.mcp.freshness",
    verified_on: manifest.verified_on,
    purpose: "Detect stale host-loaded MCP servers by comparing observed tool/version state to Telos manifest expectations.",
    failure_codes: FAILURE_CODES,
    servers,
    validation: {
      verdict: "MATCH",
      checks: [
        "each server declares a status tool",
        "each server declares an expected version and current status string",
        "each server exposes a deterministic expected tool hash",
        "hosts can distinguish stale server, tool-surface drift, version drift, and unresolved launch profiles"
      ]
    },
    next_actions: [
      "telos.server.manifest: restart stale servers from the source_checkout launch profile.",
      "forum.ledger.summary: record stale-server refresh as an operator-room event.",
      "crucible.assess: classify unresolved or drifting probes before trusting tool output."
    ]
  };
}

export function summary() {
  const packet = freshnessPacket();
  const lines = [
    "Project Telos MCP Freshness",
    `servers  ${Object.keys(packet.servers).length}`,
    `failure ${packet.failure_codes[0]}`,
    "compare  serverInfo.version, status.tool_version, tools/list hash"
  ];
  for (const [name, server] of Object.entries(packet.servers)) {
    lines.push(`${name.padEnd(9)} ${server.expected_version.padEnd(8)} ${server.expected_tools.length} tools`);
  }
  lines.push("next     node demo/mcp-freshness.mjs");
  return `${lines.join("\n")}\n`;
}

function main() {
  if (process.argv.includes("--summary")) {
    process.stdout.write(summary());
  } else {
    process.stdout.write(`${JSON.stringify(freshnessPacket(), null, 2)}\n`);
  }
}

if (process.argv[1] && import.meta.url.endsWith(process.argv[1].replace(/\\/g, "/"))) {
  main();
}
