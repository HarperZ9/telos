import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { handleRequest, tools } from "./telos-mcp.mjs";

function request(method, params = undefined) {
  return { jsonrpc: "2.0", id: 1, method, ...(params ? { params } : {}) };
}

assert.equal(
  handleRequest({ jsonrpc: "2.0", method: "notifications/initialized" }),
  null
);

const init = handleRequest(request("initialize"));
assert.equal(init.result.protocolVersion, "2025-06-18");
assert.equal(init.result.serverInfo.name, "project-telos-telos");

const listed = handleRequest(request("tools/list"));
const names = new Set(listed.result.tools.map((tool) => tool.name));
for (const name of ["telos.status", "telos.doctor", "telos.room", "telos.workflow"]) {
  assert.ok(names.has(name), `missing ${name}`);
}

for (const tool of tools) {
  assert.equal(tool.inputSchema.type, "object");
  assert.equal(tool.inputSchema.additionalProperties, false);
}

const status = handleRequest(request("tools/call", { name: "telos.status", arguments: {} }));
assert.equal(status.result.structuredContent.schema, "project-telos.flagship-action/v1");
assert.equal(status.result.structuredContent.tool, "telos");
assert.equal(status.result.structuredContent.command, "status");
assert.match(status.result.content[0].text, /"command": "status"/);

const badTool = handleRequest(request("tools/call", { name: "telos.missing", arguments: {} }));
assert.equal(badTool.error.code, -32000);
assert.match(badTool.error.message, /unknown tool/);

const serverPath = fileURLToPath(new URL("./telos-mcp.mjs", import.meta.url));
const stdio = spawnSync(process.execPath, [serverPath], {
  input: JSON.stringify({ jsonrpc: "2.0", id: 7, method: "tools/list" }) + "\n",
  encoding: "utf8"
});
assert.equal(stdio.status, 0, stdio.stderr || stdio.stdout);
const stdioResponse = JSON.parse(stdio.stdout.trim());
assert.equal(stdioResponse.id, 7);
assert.ok(stdioResponse.result.tools.some((tool) => tool.name === "telos.workflow"));