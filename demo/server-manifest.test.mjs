import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const manifest = JSON.parse(
  readFileSync(new URL("./integrations/mcp-server-manifest.json", import.meta.url), "utf8")
);
const catalog = JSON.parse(
  readFileSync(new URL("./integrations/mcp-tool-catalog.json", import.meta.url), "utf8")
);

assert.equal(manifest.schema, "project-telos.mcp-server-manifest/v1");
assert.deepEqual(Object.keys(manifest.servers).sort(), [
  "crucible",
  "forum",
  "gather",
  "index",
  "telos"
]);
assert.equal(manifest.hosts.codex.config_key, "mcp_servers");
assert.equal(manifest.hosts.claude.container_key, "mcpServers");
assert.equal(manifest.hosts.openai_agents.transport, "stdio");
assert.ok(manifest.sources.every((source) => source.url.startsWith("https://")));

const expectedByServer = new Map();
for (const tool of catalog.tools) {
  const names = expectedByServer.get(tool.mcp.server) ?? [];
  names.push(tool.mcp.tool);
  expectedByServer.set(tool.mcp.server, names);
}
for (const [server, expected] of expectedByServer) {
  assert.deepEqual(
    manifest.servers[server].expected_tools.slice().sort(),
    expected.slice().sort(),
    `${server} server manifest mirrors catalog tools`
  );
}

function runManifest(...args) {
  return spawnSync(process.execPath, [path.join(here, "server-manifest.mjs"), ...args], {
    cwd: path.resolve(here, ".."),
    encoding: "utf8"
  });
}

const json = runManifest();
assert.equal(json.status, 0, json.stderr || json.stdout);
assert.deepEqual(JSON.parse(json.stdout), manifest);

const summary = runManifest("--summary");
assert.equal(summary.status, 0, summary.stderr || summary.stdout);
assert.match(summary.stdout, /^Project Telos MCP Server Manifest/m);
assert.match(summary.stdout, /servers\s+5/);
assert.match(summary.stdout, /tools\s+25 expected/);
assert.match(summary.stdout, /gather\s+5 tools/);

const codex = runManifest("--codex");
assert.equal(codex.status, 0, codex.stderr || codex.stdout);
assert.match(codex.stdout, /\[mcp_servers\.gather\]/);
assert.match(codex.stdout, /PYTHONPATH/);

const claude = runManifest("--claude-json");
assert.equal(claude.status, 0, claude.stderr || claude.stdout);
const claudeConfig = JSON.parse(claude.stdout);
assert.equal(claudeConfig.mcpServers.gather.type, "stdio");
assert.deepEqual(claudeConfig.mcpServers.telos.args.slice(-1), [
  "${PROJECT_TELOS_PUBLIC}/telos/demo/telos-mcp.mjs"
]);
