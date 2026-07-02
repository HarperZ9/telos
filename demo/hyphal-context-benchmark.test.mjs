import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { buildHyphalBenchmark } from "./hyphal-context-benchmark.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const packet = buildHyphalBenchmark();

assert.equal(packet.schema, "project-telos.hyphal-context-benchmark/v1");
assert.equal(packet.benchmark_id, "twenty-second-wave-hyphal-context-benchmark");
assert.equal(packet.comparison.result, "HYPHAL_CONTEXT_FIXTURE_MATCH");
assert.equal(packet.routes.full_context.verdict, "MATCH");
assert.equal(packet.routes.hyphal_context.verdict, "MATCH");
assert.match(packet.receipt_hash, /^sha256:[a-f0-9]{64}$/);

assert.equal(packet.routes.full_context.candidate_source_count, 10);
assert.equal(packet.routes.full_context.delivered_source_bodies, 10);
assert.equal(packet.routes.hyphal_context.gradient_envelope_count, 10);
assert.equal(packet.routes.hyphal_context.rehydrated_card_count, 6);
assert.ok(packet.comparison.hyphal_context_tokens < packet.comparison.full_context_tokens);
assert.ok(packet.comparison.token_savings_ratio >= 0.5);
assert.equal(packet.comparison.evidence_recall_delta, 0);
assert.equal(packet.comparison.guardrail_delta, 0);

const required = new Set(packet.required_evidence_classes);
for (const route of [packet.routes.full_context, packet.routes.hyphal_context]) {
  const recovered = new Set(route.evidence_classes_recovered);
  for (const evidenceClass of required) {
    assert.ok(recovered.has(evidenceClass), `${route.route_id} missed ${evidenceClass}`);
  }
  assert.deepEqual(route.guardrails_blocked, [
    "biological_nervous_system_equivalence",
    "universal_intentional_common_mycorrhizal_network_messaging",
    "benchmarked_hyphal_context_protocol_claim"
  ]);
}

function scanNoRawBodies(value, pathSoFar = "$") {
  if (!value || typeof value !== "object") return;
  if (Array.isArray(value)) {
    value.forEach((item, index) => scanNoRawBodies(item, `${pathSoFar}[${index}]`));
    return;
  }
  for (const [key, child] of Object.entries(value)) {
    assert.notEqual(key, "raw_source_body", `${pathSoFar}.${key} leaks a raw source body`);
    assert.notEqual(key, "raw_context", `${pathSoFar}.${key} leaks raw context`);
    scanNoRawBodies(child, `${pathSoFar}.${key}`);
  }
}
scanNoRawBodies(packet);

const run = spawnSync(process.execPath, [path.join(here, "hyphal-context-benchmark.mjs")], {
  cwd: path.resolve(here, ".."),
  encoding: "utf8"
});
assert.equal(run.status, 0, run.stderr || run.stdout);
assert.deepEqual(JSON.parse(run.stdout), packet);

const frozenReceipt = JSON.parse(
  readFileSync(
    path.join(here, "..", "docs", "outreach", "receipts", "twenty-second-wave", "hyphal-context-benchmark-2026-07-02.json"),
    "utf8"
  )
);
assert.deepEqual(frozenReceipt, packet);
