// Every MCP tool states its title and read/write hints. The Anthropic Software
// Directory Policy requires readOnlyHint, destructiveHint and title on every
// tool a listed server exposes.
import test from "node:test";
import assert from "node:assert/strict";
import { handleRequest, toolTitles, tools } from "./telos-mcp.mjs";

const HINTS = ["readOnlyHint", "destructiveHint", "idempotentHint", "openWorldHint"];

test("every listed tool carries a title and boolean hints", () => {
  const listed = handleRequest({ jsonrpc: "2.0", id: 1, method: "tools/list" }).result.tools;
  assert.deepEqual(new Set(listed.map((t) => t.name)), new Set(Object.keys(toolTitles)));
  for (const tool of listed) {
    const notes = tool.annotations;
    assert.ok(notes.title && tool.title === notes.title, tool.name);
    for (const key of HINTS) assert.equal(typeof notes[key], "boolean", `${tool.name} ${key}`);
    assert.ok(tool.name.length <= 64);
  }
});

test("no tool on this server claims to write or reach a network", () => {
  for (const tool of tools) {
    assert.equal(tool.annotations.readOnlyHint, true, tool.name);
    assert.equal(tool.annotations.destructiveHint, false, tool.name);
    assert.equal(tool.annotations.openWorldHint, false, tool.name);
  }
});
