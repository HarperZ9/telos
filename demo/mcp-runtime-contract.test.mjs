import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const telosRoot = path.resolve(here, "..");
const publicRoot = path.resolve(telosRoot, "..");
const catalog = JSON.parse(
  readFileSync(path.join(here, "integrations", "mcp-tool-catalog.json"), "utf8")
);

const serverSources = {
  gather: {
    repo: "gather",
    code: `
import json, sys
sys.path.insert(0, sys.argv[1])
from gather.mcp import handle_request
resp = handle_request({"jsonrpc":"2.0","id":1,"method":"tools/list"})
print(json.dumps([tool["name"] for tool in resp["result"]["tools"]]))
`
  },
  crucible: {
    repo: "crucible",
    code: `
import json, sys
sys.path.insert(0, sys.argv[1])
from crucible.mcp import handle_request
resp = handle_request({"jsonrpc":"2.0","id":1,"method":"tools/list"})
print(json.dumps([tool["name"] for tool in resp["result"]["tools"]]))
`
  },
  index: {
    repo: "index",
    code: `
import json, sys
sys.path.insert(0, sys.argv[1])
from index_graph.mcp import handle_request
resp = handle_request({"jsonrpc":"2.0","id":1,"method":"tools/list"})
print(json.dumps([tool["name"] for tool in resp["result"]["tools"]]))
`
  },
  forum: {
    repo: "forum",
    code: `
import asyncio, json, sys, tempfile
sys.path.insert(0, sys.argv[1])
from forum.daemon import build_orchestrator
from forum.mcp_surface import McpSurface
async def main():
    with tempfile.TemporaryDirectory() as tmp:
        surface = McpSurface(build_orchestrator(tmp))
        resp = await surface.handle({"jsonrpc":"2.0","id":1,"method":"tools/list"})
        print(json.dumps([tool["name"] for tool in resp["result"]["tools"]]))
asyncio.run(main())
`
  }
};

function listRuntimeTools(server) {
  if (server === "telos") {
    const code = `
import { handleRequest } from "./demo/telos-mcp.mjs";
const resp = handleRequest({"jsonrpc":"2.0","id":1,"method":"tools/list"});
console.log(JSON.stringify(resp.result.tools.map((tool) => tool.name)));
`.trim();
    const result = spawnSync(process.execPath, ["--input-type=module", "-e", code], {
      cwd: telosRoot,
      encoding: "utf8"
    });
    assert.equal(result.status, 0, result.stderr || result.stdout);
    return new Set(JSON.parse(result.stdout));
  }
  const spec = serverSources[server];
  assert.ok(spec, `no runtime probe for ${server}`);
  const repoRoot = path.join(publicRoot, spec.repo);
  const result = spawnSync("python", ["-c", spec.code, path.join(repoRoot, "src")], {
    cwd: repoRoot,
    encoding: "utf8"
  });
  assert.equal(result.status, 0, result.stderr || result.stdout);
  return new Set(JSON.parse(result.stdout));
}

function callGatherRunInline() {
  const spec = serverSources.gather;
  const repoRoot = path.join(publicRoot, spec.repo);
  const target = path.join(telosRoot, "README.md");
  const code = `
import json, sys
sys.path.insert(0, sys.argv[1])
from gather.mcp import handle_request
resp = handle_request({
    "jsonrpc": "2.0",
    "id": 7,
    "method": "tools/call",
    "params": {
        "name": "gather.run",
        "arguments": {
            "config": {
                "jobs": [{"source": "docs", "target": sys.argv[2]}],
                "scope": ["Project Telos"],
                "store": None
            }
        }
    }
})
print(json.dumps(resp))
`;
  const result = spawnSync("python", ["-c", code, path.join(repoRoot, "src"), target], {
    cwd: repoRoot,
    encoding: "utf8"
  });
  assert.equal(result.status, 0, result.stderr || result.stdout);
  const response = JSON.parse(result.stdout);
  assert.equal(response.result.isError, false);
  return JSON.parse(response.result.content[0].text);
}

const expectedByServer = new Map();
for (const tool of catalog.tools) {
  if (tool.mcp.status !== "available") {
    continue;
  }
  const names = expectedByServer.get(tool.mcp.server) ?? [];
  names.push(tool.mcp.tool);
  expectedByServer.set(tool.mcp.server, names);
}

for (const [server, expectedNames] of expectedByServer) {
  const runtimeNames = listRuntimeTools(server);
  for (const name of expectedNames) {
    assert.ok(runtimeNames.has(name), `${server} runtime exposes ${name}`);
  }
}

const gatherRun = callGatherRunInline();
assert.equal(gatherRun.targets.length, 1);
assert.equal(gatherRun.targets[0][0], "docs");
assert.match(gatherRun.targets[0][1].replace(/\\/g, "/"), /\/telos\/README\.md$/);
assert.equal(gatherRun.scope.join(","), "Project Telos");
assert.equal(gatherRun.kept, 1);
assert.equal(gatherRun.stored, null);
assert.match(gatherRun.digest_seal, /^[a-f0-9]{64}$/);
assert.match(gatherRun.seal, /^[a-f0-9]{64}$/);
