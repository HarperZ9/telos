import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

import {
  buildDemoContextPack,
  estimateTokens,
  validateContextPack
} from "./context-pack.mjs";
import { handleRequest, tools } from "./telos-mcp.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));

const pack = buildDemoContextPack();

assert.equal(pack.schema, "project-telos.context-pack/v1");
assert.equal(pack.tool, "telos.context.pack");
assert.equal(pack.validation.verdict, "MATCH");
assert.equal(pack.validation.failure_code, null);
assert.equal(pack.context_budget.lossless_by_ref, true);
assert.equal(pack.context_budget.hidden_payloads_used, false);
assert.ok(pack.context_budget.estimated_packet_tokens <= pack.context_budget.target_packet_tokens);
assert.match(pack.context_pack_hash, /^sha256:[a-f0-9]{64}$/);

for (const ref of pack.source_refs) {
  assert.match(ref.content_hash, /^sha256:[a-f0-9]{64}$/);
  assert.ok(ref.expansion_command.length > 0);
}

for (const claim of pack.summary.claims) {
  assert.ok(claim.source_ref_ids.length > 0);
}

assert.equal(pack.context_load.claims_usefulness, false);
assert.equal(pack.context_load.raw_payload_required, false);
assert.equal(pack.context_relevance.raw_payload_required, false);

const relevanceIds = new Set(pack.context_relevance.input_refs.map((ref) => ref.input_id));
for (const input of pack.context_load.loaded_inputs) {
  assert.ok(relevanceIds.has(input.input_id), `missing relevance join for ${input.input_id}`);
  assert.equal("raw_context" in input, false);
}

assert.equal(estimateTokens("abcd efgh ijkl mnop"), 5);

const lossy = validateContextPack({
  ...pack,
  summary: { claims: [{ text: "Unanchored claim", source_ref_ids: [] }] }
});
assert.equal(lossy.verdict, "UNVERIFIABLE");
assert.equal(lossy.failure_code, "lossy_summary");

const rawLeak = validateContextPack({
  ...pack,
  context_load: {
    ...pack.context_load,
    loaded_inputs: [
      ...pack.context_load.loaded_inputs,
      {
        input_id: "ctx_in_raw",
        source_hash: "sha256:1000000000000000000000000000000000000000000000000000000000000999",
        delivered_hash: "sha256:2000000000000000000000000000000000000000000000000000000000000999",
        rank: 99,
        role: "bad_fixture",
        bucket: "raw",
        delivery_status: "delivered",
        raw_context: "must not cross the packet boundary"
      }
    ]
  }
});
assert.equal(rawLeak.verdict, "UNVERIFIABLE");
assert.equal(rawLeak.failure_code, "raw_context_leak");

const budgetExceeded = validateContextPack({
  ...pack,
  context_budget: { ...pack.context_budget, target_packet_tokens: 4 }
});
assert.equal(budgetExceeded.verdict, "DRIFT");
assert.equal(budgetExceeded.failure_code, "budget_exceeded");

const run = spawnSync(process.execPath, [path.join(here, "context-pack.mjs")], {
  cwd: path.resolve(here, ".."),
  encoding: "utf8"
});
assert.equal(run.status, 0, run.stderr || run.stdout);
assert.deepEqual(JSON.parse(run.stdout), pack);

const mcp = handleRequest({
  jsonrpc: "2.0",
  id: 49,
  method: "tools/call",
  params: { name: "telos.context.pack", arguments: {} }
});
assert.equal(mcp.result.structuredContent.schema, "project-telos.context-pack/v1");
assert.equal(mcp.result.structuredContent.validation.verdict, "MATCH");

assert.ok(tools.some((tool) => tool.name === "telos.context.pack"));
