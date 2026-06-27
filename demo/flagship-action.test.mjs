import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { actionEnvelope, assertActionEnvelope, SCHEMA } from "./flagship-action.mjs";

const schema = JSON.parse(
  readFileSync(new URL("./flagship-action.schema.json", import.meta.url), "utf8")
);
assert.equal(schema.$id, SCHEMA);
assert.deepEqual(schema.properties.status.enum, ["MATCH", "DRIFT", "UNVERIFIABLE", "ERROR"]);

const payload = actionEnvelope({
  tool: "telos",
  toolVersion: "demo",
  command: "status",
  native: { role: "shared-room" },
  nextActions: [
    {
      tool: "index",
      action: "map",
      reason: "refresh workspace context",
      inputs: [],
      priority: "normal"
    }
  ]
});

assertActionEnvelope(payload);
assert.equal(payload.schema, SCHEMA);
assert.equal(payload.status, "MATCH");
assert.equal(payload.next_actions[0].tool, "index");
