import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { handleRequest, tools } from "./telos-mcp.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const packet = JSON.parse(
  readFileSync(new URL("./research/rendering-pipeline-seeds.json", import.meta.url), "utf8")
);
const catalog = JSON.parse(
  readFileSync(new URL("./integrations/mcp-tool-catalog.json", import.meta.url), "utf8")
);
const manifest = JSON.parse(
  readFileSync(new URL("./integrations/mcp-server-manifest.json", import.meta.url), "utf8")
);

assert.equal(packet.schema, "project-telos.research-seed/v1");
assert.equal(packet.tool, "telos.rendering.research");
assert.equal(packet.seeds.length, 3);

const byId = new Map(packet.seeds.map((seed) => [seed.seed_id, seed]));
assert.ok(byId.has("seed-gaussian-splatting-webgpu"));
assert.ok(byId.has("seed-clustered-forward-rendering"));
assert.ok(byId.has("seed-dithering-sampling-kernels"));

for (const seed of packet.seeds) {
  assert.equal(seed.evidence_status, "MATCH");
  assert.ok(seed.source_receipts.length >= 3, `${seed.seed_id} has lawful source receipts`);
  assert.ok(seed.source_leads.every((lead) => lead.evidence_status === "UNVERIFIABLE"));
  assert.ok(seed.source_leads.every((lead) => lead.provenance_class === "operator_source_lead"));
  assert.ok(seed.design_acceptance_gates.some((gate) => /pretty|visual|beauty/i.test(gate.gate)));
  assert.ok(seed.design_acceptance_gates.some((gate) => /a11y|accessibility/i.test(`${gate.gate} ${gate.criterion}`)));
  for (const receipt of seed.source_receipts) {
    assert.equal(receipt.provenance_class, "lawful_source");
    assert.match(receipt.receipt_hash, /^sha256:[a-f0-9]{64}$/);
  }
}

assert.equal(packet.modern_rendering_candidates.length, 2);
const candidateIds = new Set(packet.modern_rendering_candidates.map((candidate) => candidate.candidate_id));
assert.ok(candidateIds.has("candidate-neural-rendering-rtx-kit"));
assert.ok(candidateIds.has("candidate-mesh-shader-pipelines"));
for (const candidate of packet.modern_rendering_candidates) {
  assert.equal(candidate.evidence_status, "MATCH");
  assert.ok(candidate.source_receipts.length >= 2);
  assert.match(candidate.adoption_boundary, /benchmark|fallback|portability|license/i);
  for (const receipt of candidate.source_receipts) {
    assert.equal(receipt.provenance_class, "lawful_source");
    assert.match(receipt.receipt_hash, /^sha256:[a-f0-9]{64}$/);
  }
}

assert.equal(packet.execution_substrate_leads.length, 3);
assert.ok(packet.execution_substrate_leads.every((lead) => lead.evidence_status === "UNVERIFIABLE"));
assert.ok(packet.execution_substrate_leads.every((lead) => lead.provenance_class === "operator_source_lead"));
assert.ok(packet.execution_substrate_leads.every((lead) => /GPU|Render|render|provider|farm/i.test(lead.notes)));

assert.ok(
  byId.get("seed-gaussian-splatting-webgpu").claims.some((claim) => /SuperSplat/.test(claim.claim))
);
assert.ok(
  byId.get("seed-clustered-forward-rendering").claims.some((claim) => /WebGPU\/WGSL/.test(claim.claim))
);
assert.ok(
  byId.get("seed-dithering-sampling-kernels").claims.some((claim) => /Void-and-cluster|blue-noise/i.test(claim.claim))
);

const run = spawnSync(process.execPath, [path.join(here, "rendering-research.mjs")], {
  cwd: path.resolve(here, ".."),
  encoding: "utf8"
});
assert.equal(run.status, 0, run.stderr || run.stdout);
assert.deepEqual(JSON.parse(run.stdout), packet);

const catalogTool = catalog.tools.find((tool) => tool.name === "telos.rendering.research");
assert.ok(catalogTool, "catalog exposes telos.rendering.research");
assert.equal(catalogTool.flagship, "telos");
assert.deepEqual(catalogTool.cli, ["node", "demo/rendering-research.mjs"]);
assert.equal(catalogTool.mcp.tool, "telos.rendering.research");

assert.ok(tools.some((tool) => tool.name === "telos.rendering.research"));
assert.ok(tools.some((tool) => tool.name === "telos.rendering.capabilities"));
assert.ok(tools.some((tool) => tool.name === "telos.measurement.layers"));
assert.ok(manifest.servers.telos.expected_tools.includes("telos.rendering.research"));
assert.ok(manifest.servers.telos.expected_tools.includes("telos.rendering.capabilities"));
assert.ok(manifest.servers.telos.expected_tools.includes("telos.measurement.layers"));

const mcp = handleRequest({
  jsonrpc: "2.0",
  id: 42,
  method: "tools/call",
  params: { name: "telos.rendering.research", arguments: {} }
});
assert.equal(mcp.result.structuredContent.tool, "telos.rendering.research");
assert.equal(mcp.result.structuredContent.seeds.length, 3);

const status = spawnSync(process.execPath, [path.join(here, "status.mjs")], {
  cwd: path.resolve(here, ".."),
  encoding: "utf8"
});
assert.equal(status.status, 0, status.stderr || status.stdout);
const statusPayload = JSON.parse(status.stdout);
assert.ok(statusPayload.native.mcp_tools.includes("telos.rendering.research"));
assert.ok(statusPayload.native.mcp_tools.includes("telos.rendering.capabilities"));
assert.ok(statusPayload.native.mcp_tools.includes("telos.measurement.layers"));
assert.ok(statusPayload.native.mcp_tools.includes("telos.creative.engine"));
assert.ok(statusPayload.native.mcp_tools.includes("telos.creative.kernels"));
assert.ok(statusPayload.native.mcp_tools.includes("telos.display.calibration"));
assert.ok(statusPayload.native.mcp_tools.includes("telos.objective.monitor"));
assert.match(statusPayload.native.current_status, /47-tool/);

const catalogSummary = spawnSync(process.execPath, [path.join(here, "catalog.mjs"), "--summary"], {
  cwd: path.resolve(here, ".."),
  encoding: "utf8"
});
assert.equal(catalogSummary.status, 0, catalogSummary.stderr || catalogSummary.stdout);
assert.match(catalogSummary.stdout, /tools\s+47 total, 47 available/);
assert.match(catalogSummary.stdout, /telos\s+19 tools/);

const manifestSummary = spawnSync(process.execPath, [path.join(here, "server-manifest.mjs"), "--summary"], {
  cwd: path.resolve(here, ".."),
  encoding: "utf8"
});
assert.equal(manifestSummary.status, 0, manifestSummary.stderr || manifestSummary.stdout);
assert.match(manifestSummary.stdout, /tools\s+47 expected/);
