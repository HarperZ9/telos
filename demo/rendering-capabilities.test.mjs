import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { handleRequest, tools } from "./telos-mcp.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const capabilities = JSON.parse(
  readFileSync(new URL("./integrations/rendering-capabilities.json", import.meta.url), "utf8")
);
const catalog = JSON.parse(
  readFileSync(new URL("./integrations/mcp-tool-catalog.json", import.meta.url), "utf8")
);
const manifest = JSON.parse(
  readFileSync(new URL("./integrations/mcp-server-manifest.json", import.meta.url), "utf8")
);

assert.equal(capabilities.schema, "project-telos.rendering-capabilities/v1");
assert.equal(capabilities.tool, "telos.rendering.capabilities");
assert.deepEqual(capabilities.selection_order, [
  "webgpu-splat-clustered",
  "webgl2-cluster-preview",
  "canvas2d-receipt-renderer",
  "static-artifact-receipt"
]);

const profiles = new Map(capabilities.renderer_profiles.map((profile) => [profile.profile_id, profile]));
for (const profileId of capabilities.selection_order) {
  assert.ok(profiles.has(profileId), `missing profile ${profileId}`);
}

const webgpu = profiles.get("webgpu-splat-clustered");
assert.equal(webgpu.fallback_profile, "webgl2-cluster-preview");
assert.ok(webgpu.supports.includes("3d-gaussian-splatting"));
assert.ok(webgpu.supports.includes("clustered-forward-lighting"));
assert.ok(webgpu.source_receipts.length >= 5);
assert.ok(webgpu.acceptance_gates.some((gate) => /benchmark/i.test(gate.gate)));
assert.ok(webgpu.acceptance_gates.some((gate) => /a11y/i.test(gate.gate)));
assert.ok(webgpu.acceptance_gates.some((gate) => /asset_provenance/i.test(gate.gate)));

for (const profile of capabilities.renderer_profiles) {
  assert.equal(profile.evidence_status, "MATCH");
  assert.match(profile.unavailable_failure_code, /^renderer_/);
  assert.ok(profile.acceptance_gates.length >= 2);
  for (const receipt of profile.source_receipts) {
    assert.equal(receipt.provenance_class, "lawful_source");
    assert.match(receipt.receipt_hash, /^sha256:[a-f0-9]{64}$/);
  }
}

for (const code of [
  "renderer_webgpu_unavailable",
  "benchmark_missing",
  "asset_provenance_missing",
  "missing_a11y_fallback",
  "missing_receipt",
  "unsupported_host"
]) {
  assert.ok(capabilities.failure_codes.includes(code), `missing failure code ${code}`);
}

assert.equal(capabilities.privacy_boundary.raw_assets_required_for_interop, false);
assert.ok(capabilities.privacy_boundary.required_export_fields.includes("selected_profile"));
assert.ok(capabilities.privacy_boundary.required_export_fields.includes("verification_verdict"));

const cli = spawnSync(process.execPath, [path.join(here, "rendering-capabilities.mjs")], {
  cwd: path.resolve(here, ".."),
  encoding: "utf8"
});
assert.equal(cli.status, 0, cli.stderr || cli.stdout);
assert.deepEqual(JSON.parse(cli.stdout), capabilities);

const summary = spawnSync(process.execPath, [path.join(here, "rendering-capabilities.mjs"), "--summary"], {
  cwd: path.resolve(here, ".."),
  encoding: "utf8"
});
assert.equal(summary.status, 0, summary.stderr || summary.stdout);
assert.match(summary.stdout, /Telos Rendering Capabilities/);
assert.match(summary.stdout, /profiles\s+4/);
assert.match(summary.stdout, /webgpu-splat-clustered -> webgl2-cluster-preview/);

assert.ok(tools.some((tool) => tool.name === "telos.rendering.capabilities"));
const mcp = handleRequest({
  jsonrpc: "2.0",
  id: 92,
  method: "tools/call",
  params: { name: "telos.rendering.capabilities", arguments: {} }
});
assert.equal(mcp.result.structuredContent.tool, "telos.rendering.capabilities");
assert.equal(mcp.result.structuredContent.renderer_profiles.length, 4);

const catalogTool = catalog.tools.find((tool) => tool.name === "telos.rendering.capabilities");
assert.ok(catalogTool, "catalog exposes telos.rendering.capabilities");
assert.deepEqual(catalogTool.cli, ["node", "demo/rendering-capabilities.mjs"]);
assert.equal(catalogTool.mcp.tool, "telos.rendering.capabilities");
assert.ok(manifest.servers.telos.expected_tools.includes("telos.rendering.capabilities"));
