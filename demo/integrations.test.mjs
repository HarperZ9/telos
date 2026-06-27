import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

const catalog = JSON.parse(
  readFileSync(new URL("./integrations/mcp-tool-catalog.json", import.meta.url), "utf8")
);

assert.equal(catalog.schema, "project-telos.mcp-tool-catalog/v1");
assert.equal(catalog.action_schema, "project-telos.flagship-action/v1");
assert.ok(catalog.transports.includes("stdio"));
assert.ok(catalog.transports.includes("streamable-http"));

const names = new Set(catalog.tools.map((tool) => tool.name));
for (const name of [
  "gather.docs",
  "gather.run",
  "index.map",
  "index.context",
  "forum.route",
  "forum.ledger.summary",
  "crucible.assess",
  "crucible.recheck",
  "telos.status",
  "telos.workflow"
]) {
  assert.ok(names.has(name), `missing ${name}`);
}

const statuses = new Set();
for (const tool of catalog.tools) {
  assert.match(tool.name, /^(gather|index|forum|crucible|telos)\.[a-z.]+$/);
  assert.ok(Array.isArray(tool.cli) && tool.cli.length > 0, `${tool.name} has CLI fallback`);
  assert.equal(tool.mcp.method, "tools/call");
  statuses.add(tool.mcp.status);
}

for (const status of ["available", "cli-bridge", "planned"]) {
  assert.ok(statuses.has(status), `missing availability status ${status}`);
}
