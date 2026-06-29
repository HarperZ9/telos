import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const telosRoot = path.resolve(here, "..");
const publicRoot = path.resolve(telosRoot, "..");
const manifest = JSON.parse(
  readFileSync(new URL("./integrations/mcp-server-manifest.json", import.meta.url), "utf8")
);

function expand(value) {
  return value.replaceAll("${PROJECT_TELOS_PUBLIC}", publicRoot.replaceAll("\\", "/"));
}

function launchToolsList(serverName, server) {
  const profile = server.profiles.source_checkout;
  const env = { ...process.env };
  for (const [key, value] of Object.entries(profile.env ?? {})) {
    env[key] = expand(value);
  }
  const request = `${JSON.stringify({ jsonrpc: "2.0", id: 1, method: "tools/list" })}\n`;
  const result = spawnSync(profile.command, profile.args.map(expand), {
    cwd: expand(profile.cwd),
    env,
    input: request,
    encoding: "utf8",
    timeout: 10_000
  });

  assert.equal(result.status, 0, `${serverName} launch failed: ${result.stderr || result.stdout}`);
  const response = JSON.parse(result.stdout);
  assert.equal(response.jsonrpc, "2.0");
  assert.equal(response.id, 1);
  assert.ok(Array.isArray(response.result.tools), `${serverName} did not return tools/list tools`);
  return response.result.tools.map((tool) => tool.name).sort();
}

for (const [serverName, server] of Object.entries(manifest.servers)) {
  const actual = launchToolsList(serverName, server);
  const expected = new Set(server.expected_tools);
  const auxiliary = new Set(server.auxiliary_tools ?? []);
  const missing = server.expected_tools.filter((tool) => !actual.includes(tool)).sort();
  const extras = actual.filter((tool) => !expected.has(tool)).sort();
  const undeclaredExtras = extras.filter((tool) => !auxiliary.has(tool)).sort();

  assert.deepEqual(missing, [], `${serverName} source_checkout profile misses expected MCP tools`);
  assert.deepEqual(
    undeclaredExtras,
    [],
    `${serverName} source_checkout profile exposes undeclared extra MCP tools`
  );
}
