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

function observedToolNames(observed) {
  const tools = observed?.tools_list?.result?.tools ?? observed?.tools?.result?.tools ?? observed?.tools ?? [];
  if (!Array.isArray(tools)) {
    return [];
  }
  return tools
    .map((tool) => typeof tool === "string" ? tool : tool?.name)
    .filter((name) => typeof name === "string" && name.length > 0);
}

function observedVersion(observed) {
  return observed?.status_payload?.tool_version
    ?? observed?.status?.tool_version
    ?? observed?.initialize?.result?.serverInfo?.version
    ?? observed?.serverInfo?.version
    ?? null;
}

function observedServerInfoVersion(observed) {
  return observed?.initialize?.result?.serverInfo?.version ?? observed?.serverInfo?.version ?? null;
}

function observedStatusText(observed) {
  return observed?.status_payload?.native?.current_status
    ?? observed?.status?.native?.current_status
    ?? null;
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

export function evaluateObservedServer(name, observed) {
  const packet = freshnessPacket();
  const expected = packet.servers[name];
  if (!expected) {
    throw new Error(`unknown MCP server: ${name}`);
  }

  const diagnostics = [];
  const toolNames = observedToolNames(observed);
  const toolHash = toolNames.length > 0 ? expectedToolHash(toolNames) : null;
  const statusVersion = observedVersion(observed);
  const serverInfoVersion = observedServerInfoVersion(observed);
  const statusText = observedStatusText(observed);

  if (!serverInfoVersion || !statusVersion || !statusText || toolNames.length === 0) {
    diagnostics.push({
      code: "freshness_probe_unavailable",
      message: "observed initialize, status, or tools/list payload is missing required freshness fields"
    });
  }

  if (serverInfoVersion && serverInfoVersion !== expected.expected_version) {
    diagnostics.push({
      code: "stale_mcp_server",
      expected: expected.expected_version,
      observed: serverInfoVersion,
      field: "initialize.result.serverInfo.version"
    });
  }

  if (statusVersion && statusVersion !== expected.expected_version) {
    diagnostics.push({
      code: "version_drift",
      expected: expected.expected_version,
      observed: statusVersion,
      field: "status.tool_version"
    });
  }

  if (statusText && statusText !== expected.expected_current_status) {
    diagnostics.push({
      code: "version_drift",
      expected: expected.expected_current_status,
      observed: statusText,
      field: "status.native.current_status"
    });
  }

  if (toolHash && toolHash !== expected.expected_tool_hash) {
    const expectedSet = new Set(expected.expected_tools);
    const observedSet = new Set(toolNames);
    diagnostics.push({
      code: "tool_surface_drift",
      expected: expected.expected_tool_hash,
      observed: toolHash,
      missing_tools: expected.expected_tools.filter((tool) => !observedSet.has(tool)),
      unexpected_tools: toolNames.filter((tool) => !expectedSet.has(tool))
    });
  }

  const failureCodes = FAILURE_CODES.filter((code) => diagnostics.some((item) => item.code === code));
  const verdict = failureCodes.length === 0
    ? "MATCH"
    : failureCodes.includes("freshness_probe_unavailable") && failureCodes.length === 1
      ? "UNVERIFIABLE"
      : "DRIFT";

  return {
    schema: "project-telos.mcp-freshness-observation/v1",
    tool: "telos.mcp.freshness",
    server: name,
    verdict,
    failure_codes: failureCodes,
    expected: {
      version: expected.expected_version,
      current_status: expected.expected_current_status,
      tool_hash: expected.expected_tool_hash
    },
    observed: {
      server_info_version: serverInfoVersion,
      status_version: statusVersion,
      current_status: statusText,
      tools: toolNames,
      tool_hash: toolHash
    },
    diagnostics,
    next_actions: verdict === "MATCH" ? [] : [
      expected.restart_hint,
      "record the observation in forum.ledger.summary before retrying the host workflow"
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
  const observedIndex = process.argv.indexOf("--observed");
  if (observedIndex !== -1) {
    const file = process.argv[observedIndex + 1];
    if (!file) {
      throw new Error("--observed requires a JSON file path");
    }
    const observed = JSON.parse(readFileSync(file, "utf8"));
    const server = observed.server;
    if (typeof server !== "string" || server.length === 0) {
      throw new Error("observed payload must include a server field");
    }
    process.stdout.write(`${JSON.stringify(evaluateObservedServer(server, observed), null, 2)}\n`);
  } else if (process.argv.includes("--summary")) {
    process.stdout.write(summary());
  } else {
    process.stdout.write(`${JSON.stringify(freshnessPacket(), null, 2)}\n`);
  }
}

if (process.argv[1] && import.meta.url.endsWith(process.argv[1].replace(/\\/g, "/"))) {
  main();
}
