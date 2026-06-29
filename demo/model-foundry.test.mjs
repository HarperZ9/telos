import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

import {
  buildModelFoundryPacket,
  evaluateDaemonCycle,
  validateModelFoundryPacket
} from "./model-foundry.mjs";
import { handleRequest, tools } from "./telos-mcp.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));

const packet = buildModelFoundryPacket();

assert.equal(packet.schema, "project-telos.model-foundry/v1");
assert.equal(packet.tool, "telos.model.foundry");
assert.equal(packet.validation.verdict, "MATCH");
assert.equal(packet.contract.frontier_pretraining_claimed, false);
assert.equal(packet.contract.self_modification_requires_crucible_match, true);
assert.equal(packet.contract.blind_self_training_allowed, false);
assert.equal(packet.daemon.mode, "bounded-self-improvement");
assert.equal(packet.daemon.cycle.length, 7);
assert.deepEqual(packet.verdicts, ["MATCH", "DRIFT", "UNVERIFIABLE"]);
assert.ok(packet.model_layers.some((layer) => layer.id === "frontier-orchestration"));
assert.ok(packet.model_layers.some((layer) => layer.id === "local-open-weight-runtime"));
assert.ok(packet.model_layers.some((layer) => layer.id === "post-training-lab"));
assert.ok(packet.flagship_bindings.gather.includes("fresh public/primary source intake"));
assert.ok(packet.flagship_bindings.index.includes("lossless-by-reference context envelopes"));
assert.ok(packet.flagship_bindings.crucible.includes("promotion gates for eval, safety, and regression"));
assert.ok(packet.failure_codes.includes("eval_regression"));
assert.ok(packet.failure_codes.includes("unverified_capability_claim"));
assert.ok(packet.failure_codes.includes("context_budget_exceeded"));
assert.ok(packet.receipt_hash.startsWith("fnv1a:"));

for (const source of packet.current_sources) {
  assert.match(source.receipt_hash, /^fnv1a:[0-9a-f]+$/);
  assert.equal(source.provenance, "public-official-or-primary-source");
}

const blocked = evaluateDaemonCycle({
  ...packet.daemon.example_cycle,
  crucible_verdict: "DRIFT"
});
assert.equal(blocked.decision_outcome, "block");
assert.equal(blocked.verification_verdict, "DRIFT");
assert.equal(blocked.failure_code, "eval_regression");

const allowed = evaluateDaemonCycle({
  ...packet.daemon.example_cycle,
  crucible_verdict: "MATCH",
  objective_signals: []
});
assert.equal(allowed.decision_outcome, "allow");
assert.equal(allowed.verification_verdict, "MATCH");
assert.equal(allowed.failure_code, null);

const unverifiable = validateModelFoundryPacket({
  ...packet,
  current_sources: []
});
assert.equal(unverifiable.verdict, "UNVERIFIABLE");
assert.equal(unverifiable.failure_code, "source_receipt_missing");

const cli = spawnSync(process.execPath, [path.join(here, "model-foundry.mjs")], {
  cwd: path.resolve(here, ".."),
  encoding: "utf8"
});
assert.equal(cli.status, 0, cli.stderr || cli.stdout);
assert.deepEqual(JSON.parse(cli.stdout), packet);

const summary = spawnSync(process.execPath, [path.join(here, "model-foundry.mjs"), "--summary"], {
  cwd: path.resolve(here, ".."),
  encoding: "utf8"
});
assert.equal(summary.status, 0, summary.stderr || summary.stdout);
assert.match(summary.stdout, /Telos Model Foundry/);
assert.match(summary.stdout, /bounded-self-improvement/);

const mcp = handleRequest({
  jsonrpc: "2.0",
  id: 56,
  method: "tools/call",
  params: { name: "telos.model.foundry", arguments: {} }
});
assert.equal(mcp.result.structuredContent.schema, "project-telos.model-foundry/v1");
assert.equal(mcp.result.structuredContent.validation.verdict, "MATCH");

assert.ok(tools.some((tool) => tool.name === "telos.model.foundry"));
