import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { handleRequest, tools } from "./telos-mcp.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const packet = JSON.parse(
  readFileSync(new URL("./integrations/learning-forge-labs.json", import.meta.url), "utf8")
);
const catalog = JSON.parse(
  readFileSync(new URL("./integrations/mcp-tool-catalog.json", import.meta.url), "utf8")
);

function request(method, params = undefined) {
  return { jsonrpc: "2.0", id: 1, method, ...(params ? { params } : {}) };
}

assert.equal(packet.schema, "project-telos.learning-forge/labs/v1");
assert.equal(packet.tool, "telos.learning.labs");
assert.equal(packet.validation.verdict, "MATCH");
assert.equal(packet.source_receipts.operator_packet.sha256, "a022fa3b8ea3d277b97bc058444a7757c90e92b81f06bd90f233d8f2ed66ac48");
assert.equal(packet.source_receipts.operator_packet.digest_seal, "bc983de187794519b6ab83c9d4c851e458791d9911eecf8b1445551e038f2856");
assert.equal(packet.source_boundary.raw_transcripts_stored, false);
assert.equal(packet.source_boundary.video_specific_claims_promoted, false);

const labIds = new Set(packet.labs.map((lab) => lab.id));
for (const id of [
  "tiny-autoregressive-predictor",
  "accuracy-per-token-verifier",
  "mcp-action-receipt-agent",
  "coding-agent-contamination",
  "explanation-is-not-proof",
  "spec-representation-lab",
  "stochastic-compute-lab"
]) {
  assert.ok(labIds.has(id), `missing lab ${id}`);
}

for (const lab of packet.labs) {
  assert.ok(lab.source_refs.length > 0, `${lab.id} has source refs`);
  assert.ok(lab.failure_cases.length > 0, `${lab.id} has failure cases`);
  assert.ok(lab.runnable_surface.command.length > 0, `${lab.id} has runnable command`);
  assert.ok(lab.measurement_gate.metrics.length > 0, `${lab.id} has metrics`);
  assert.ok(lab.expected_artifacts.length > 0, `${lab.id} has artifacts`);
  assert.equal(lab.verdict, "UNVERIFIABLE_UNTIL_RUN");

  const flow = lab.flagship_flow.map((step) => step.owner);
  assert.deepEqual(flow, ["gather", "index", "forum", "crucible", "telos"]);
}

assert.ok(packet.next_actions.some((action) => action.owner === "telos" && action.action === "implement_first_lab"));
assert.ok(packet.next_actions.some((action) => action.owner === "crucible" && action.action === "write_lab_gate_fixtures"));

assert.ok(catalog.tools.some((tool) => tool.name === "telos.learning.labs"));
assert.ok(tools.some((tool) => tool.name === "telos.learning.labs"));

const mcpResult = handleRequest(request("tools/call", {
  name: "telos.learning.labs",
  arguments: {}
}));
assert.deepEqual(mcpResult.result.structuredContent, packet);

const run = spawnSync(process.execPath, [path.join(here, "learning-forge-labs.mjs")], {
  cwd: path.resolve(here, ".."),
  encoding: "utf8"
});
assert.equal(run.status, 0, run.stderr || run.stdout);
assert.deepEqual(JSON.parse(run.stdout), packet);
