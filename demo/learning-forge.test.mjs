import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { handleRequest, tools } from "./telos-mcp.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const packet = JSON.parse(
  readFileSync(new URL("./research/learning-forge-seed.json", import.meta.url), "utf8")
);
const catalog = JSON.parse(
  readFileSync(new URL("./integrations/mcp-tool-catalog.json", import.meta.url), "utf8")
);

function request(method, params = undefined) {
  return { jsonrpc: "2.0", id: 1, method, ...(params ? { params } : {}) };
}

assert.equal(packet.schema, "project-telos.learning-forge/youtube-research-seed/v1");
assert.equal(packet.tool, "telos.learning.forge");
assert.equal(packet.validation.verdict, "MATCH");
assert.equal(packet.source_boundary.raw_transcripts_stored, false);
assert.equal(packet.source_boundary.raw_video_stored, false);
assert.equal(packet.source_boundary.youtube_claims_promoted, false);
assert.equal(packet.source_boundary.shadow_full_text_allowed_as_provenance, false);

assert.ok(packet.youtube_seed_corpus.inputs.length >= 10);
assert.ok(packet.youtube_seed_corpus.inputs.includes("https://www.youtube.com/@MachineLearningStreetTalk"));
assert.ok(packet.youtube_seed_corpus.inputs.includes("https://www.youtube.com/watch?v=5pieVHmlbyk&t=668s"));
assert.ok(packet.youtube_seed_corpus.inputs.includes("https://www.youtube.com/@lobais/videos"));
assert.equal(packet.youtube_seed_corpus.receipt_state, "UNVERIFIABLE_UNTIL_GATHER_TRANSCRIPT");

for (const source of packet.current_source_receipts) {
  assert.match(source.receipt_hash, /^sha256:[a-f0-9]{64}$/);
  assert.match(source.resolved_at, /^2026-06-30T/);
  assert.equal(source.provenance_class, "lawful_source");
  assert.ok(source.url.startsWith("https://"));
}

const sourceIds = new Set(packet.current_source_receipts.map((source) => source.id));
for (const id of [
  "source-neurips-2026-education-track",
  "source-neurips-2026-reproducibility-track",
  "source-neurips-2026-evaluations-datasets-track",
  "source-ibm-planning-era-language-models",
  "source-deepseek-r1-arxiv",
  "source-swe-skills-bench-arxiv"
]) {
  assert.ok(sourceIds.has(id), `missing current source receipt ${id}`);
}

const moduleIds = new Set(packet.learning_modules.map((module) => module.id));
for (const id of [
  "programming-as-evidence",
  "reasoning-test-time-compute",
  "agents-tools-mcp-receipts",
  "coding-agents-repo-work",
  "evaluation-reproducibility",
  "interpretability-faithfulness",
  "efficient-alternative-compute",
  "ai-for-science-measurement"
]) {
  assert.ok(moduleIds.has(id), `missing learning module ${id}`);
}

for (const module of packet.learning_modules) {
  assert.ok(module.source_receipt_ids.length > 0, `${module.id} has sources`);
  assert.ok(module.failure_case, `${module.id} has a failure case`);
  assert.ok(module.crucible_gate, `${module.id} has a crucible gate`);
}

for (const role of ["gather", "index", "forum", "crucible", "telos"]) {
  assert.ok(packet.flagship_roles[role].length > 0, `missing role ${role}`);
}

assert.ok(packet.claim_cards.some((claim) => claim.verdict === "UNVERIFIABLE"));
assert.ok(packet.claim_cards.some((claim) => claim.verdict === "MATCH"));
assert.ok(packet.next_actions.some((action) => action.owner === "gather" && action.action === "capture_youtube_metadata"));
assert.ok(packet.next_actions.some((action) => action.owner === "crucible" && action.action === "build_negative_corpus"));

assert.ok(catalog.tools.some((tool) => tool.name === "telos.learning.forge"));
assert.ok(tools.some((tool) => tool.name === "telos.learning.forge"));

const mcpResult = handleRequest(request("tools/call", {
  name: "telos.learning.forge",
  arguments: {}
}));
assert.deepEqual(mcpResult.result.structuredContent, packet);

const run = spawnSync(process.execPath, [path.join(here, "learning-forge.mjs")], {
  cwd: path.resolve(here, ".."),
  encoding: "utf8"
});
assert.equal(run.status, 0, run.stderr || run.stdout);
assert.deepEqual(JSON.parse(run.stdout), packet);
