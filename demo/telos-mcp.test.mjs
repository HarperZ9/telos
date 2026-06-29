import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { handleRequest, tools } from "./telos-mcp.mjs";

function request(method, params = undefined) {
  return { jsonrpc: "2.0", id: 1, method, ...(params ? { params } : {}) };
}

assert.equal(
  handleRequest({ jsonrpc: "2.0", method: "notifications/initialized" }),
  null
);

const init = handleRequest(request("initialize"));
assert.equal(init.result.protocolVersion, "2025-06-18");
assert.equal(init.result.serverInfo.name, "project-telos-telos");

const listed = handleRequest(request("tools/list"));
const names = new Set(listed.result.tools.map((tool) => tool.name));
for (const name of [
  "telos.status",
  "telos.doctor",
  "telos.room",
  "telos.workflow",
  "telos.catalog",
  "telos.server.manifest",
  "telos.admission.telemetry",
  "telos.context.envelope",
  "telos.action.receipt",
  "telos.loop.ledger",
  "telos.objective.monitor",
  "telos.research.seed",
  "telos.rendering.research",
  "telos.rendering.capabilities",
  "telos.measurement.layers",
  "telos.creative.engine",
  "telos.creative.kernels",
  "telos.revival.registry",
  "telos.display.calibration"
]) {
  assert.ok(names.has(name), `missing ${name}`);
}

for (const tool of tools) {
  assert.equal(tool.inputSchema.type, "object");
  assert.equal(tool.inputSchema.additionalProperties, false);
}

const status = handleRequest(request("tools/call", { name: "telos.status", arguments: {} }));
assert.equal(status.result.structuredContent.schema, "project-telos.flagship-action/v1");
assert.equal(status.result.structuredContent.tool, "telos");
assert.equal(status.result.structuredContent.command, "status");
assert.match(status.result.content[0].text, /"command": "status"/);

const expectedCatalog = JSON.parse(
  readFileSync(new URL("./integrations/mcp-tool-catalog.json", import.meta.url), "utf8")
);
const catalog = handleRequest(request("tools/call", { name: "telos.catalog", arguments: {} }));
assert.deepEqual(catalog.result.structuredContent, expectedCatalog);
assert.deepEqual(JSON.parse(catalog.result.content[0].text), expectedCatalog);
assert.equal(catalog.result.structuredContent.schema, "project-telos.mcp-tool-catalog/v1");
assert.ok(
  catalog.result.structuredContent.tools.some((tool) => tool.name === "telos.catalog"),
  "catalog includes telos.catalog"
);

const expectedServerManifest = JSON.parse(
  readFileSync(new URL("./integrations/mcp-server-manifest.json", import.meta.url), "utf8")
);
const serverManifest = handleRequest(request("tools/call", {
  name: "telos.server.manifest",
  arguments: {}
}));
assert.deepEqual(serverManifest.result.structuredContent, expectedServerManifest);
assert.equal(serverManifest.result.structuredContent.schema, "project-telos.mcp-server-manifest/v1");
assert.ok(serverManifest.result.structuredContent.servers.gather.expected_tools.includes("gather.docs"));

const expectedAdmissionTelemetry = JSON.parse(
  readFileSync(new URL("./integrations/admission-telemetry-conventions.json", import.meta.url), "utf8")
);
const admissionTelemetry = handleRequest(request("tools/call", {
  name: "telos.admission.telemetry",
  arguments: {}
}));
assert.deepEqual(admissionTelemetry.result.structuredContent, expectedAdmissionTelemetry);
assert.equal(admissionTelemetry.result.structuredContent.schema, "project-telos.admission-telemetry/v1");
assert.ok(admissionTelemetry.result.structuredContent.required_fields.includes("decision.outcome"));

const expectedContextEnvelope = JSON.parse(
  readFileSync(new URL("./integrations/context-envelope-conventions.json", import.meta.url), "utf8")
);
const contextEnvelope = handleRequest(request("tools/call", {
  name: "telos.context.envelope",
  arguments: {}
}));
assert.deepEqual(contextEnvelope.result.structuredContent, expectedContextEnvelope);
assert.equal(contextEnvelope.result.structuredContent.schema, "project-telos.context-envelope/v1");
assert.equal(contextEnvelope.result.structuredContent.contract.hidden_payloads_allowed, false);
assert.ok(contextEnvelope.result.structuredContent.failure_codes.includes("readability_regression"));

const expectedActionReceipt = JSON.parse(
  readFileSync(new URL("./integrations/action-receipt-conventions.json", import.meta.url), "utf8")
);
const actionReceipt = handleRequest(request("tools/call", {
  name: "telos.action.receipt",
  arguments: {}
}));
assert.deepEqual(actionReceipt.result.structuredContent, expectedActionReceipt);
assert.equal(actionReceipt.result.structuredContent.schema, "project-telos.action-receipt/v1");
assert.equal(actionReceipt.result.structuredContent.contract.append_only_compensation_required, true);
assert.ok(actionReceipt.result.structuredContent.required_fields.includes("component.config_hash"));

const expectedLoopLedger = JSON.parse(
  readFileSync(new URL("./integrations/loop-ledger-conventions.json", import.meta.url), "utf8")
);
const loopLedger = handleRequest(request("tools/call", {
  name: "telos.loop.ledger",
  arguments: {}
}));
assert.deepEqual(loopLedger.result.structuredContent, expectedLoopLedger);
assert.equal(loopLedger.result.structuredContent.schema, "project-telos.loop-ledger/v1");
assert.equal(loopLedger.result.structuredContent.contract.ledger_first_class, true);
assert.equal(loopLedger.result.structuredContent.headless_scheduled_fire.ask_user_mid_fire_status, "needs_attention");

const objectiveMonitor = handleRequest(request("tools/call", {
  name: "telos.objective.monitor",
  arguments: {}
}));
assert.equal(objectiveMonitor.result.structuredContent.schema, "project-telos.objective-monitor/v1");
assert.equal(objectiveMonitor.result.structuredContent.tool, "telos.objective.monitor");
assert.ok(objectiveMonitor.result.structuredContent.failure_codes.includes("proxy_quality_divergence"));
assert.ok(objectiveMonitor.result.structuredContent.signals.length >= 1);

const expectedResearchSeed = JSON.parse(
  readFileSync(new URL("./research/fundamental-physics-seeds.json", import.meta.url), "utf8")
);
const researchSeed = handleRequest(request("tools/call", {
  name: "telos.research.seed",
  arguments: {}
}));
assert.deepEqual(researchSeed.result.structuredContent, expectedResearchSeed);
assert.equal(researchSeed.result.structuredContent.schema, "project-telos.research-seed/v1");
assert.equal(researchSeed.result.structuredContent.seeds.length, 4);

const expectedRenderingResearch = JSON.parse(
  readFileSync(new URL("./research/rendering-pipeline-seeds.json", import.meta.url), "utf8")
);
const renderingResearch = handleRequest(request("tools/call", {
  name: "telos.rendering.research",
  arguments: {}
}));
assert.deepEqual(renderingResearch.result.structuredContent, expectedRenderingResearch);
assert.equal(renderingResearch.result.structuredContent.schema, "project-telos.research-seed/v1");
assert.equal(renderingResearch.result.structuredContent.tool, "telos.rendering.research");
assert.equal(renderingResearch.result.structuredContent.seeds.length, 3);

const expectedRenderingCapabilities = JSON.parse(
  readFileSync(new URL("./integrations/rendering-capabilities.json", import.meta.url), "utf8")
);
const renderingCapabilities = handleRequest(request("tools/call", {
  name: "telos.rendering.capabilities",
  arguments: {}
}));
assert.deepEqual(renderingCapabilities.result.structuredContent, expectedRenderingCapabilities);
assert.equal(renderingCapabilities.result.structuredContent.schema, "project-telos.rendering-capabilities/v1");
assert.equal(renderingCapabilities.result.structuredContent.renderer_profiles.length, 4);

const measurementLayers = handleRequest(request("tools/call", {
  name: "telos.measurement.layers",
  arguments: {}
}));
assert.equal(measurementLayers.result.structuredContent.schema, "project-telos.measurement-layers/v1");
assert.equal(measurementLayers.result.structuredContent.tool, "telos.measurement.layers");
assert.equal(measurementLayers.result.structuredContent.measurements.length, 10);

const expectedCreativeEngine = JSON.parse(
  readFileSync(new URL("./integrations/creative-engine-manifest.json", import.meta.url), "utf8")
);
const creativeEngine = handleRequest(request("tools/call", {
  name: "telos.creative.engine",
  arguments: {}
}));
assert.deepEqual(creativeEngine.result.structuredContent, expectedCreativeEngine);
assert.equal(creativeEngine.result.structuredContent.schema, "project-telos.creative-engine/v1");
assert.equal(creativeEngine.result.structuredContent.domains.length, 9);

const creativeKernels = handleRequest(request("tools/call", {
  name: "telos.creative.kernels",
  arguments: {}
}));
assert.equal(creativeKernels.result.structuredContent.schema, "project-telos.creative-kernels/v1");
assert.equal(creativeKernels.result.structuredContent.tool, "telos.creative.kernels");
assert.equal(creativeKernels.result.structuredContent.kernels.length, 4);

const expectedRevivalRegistry = JSON.parse(
  readFileSync(new URL("./integrations/revival-registry.json", import.meta.url), "utf8")
);
const revivalRegistry = handleRequest(request("tools/call", {
  name: "telos.revival.registry",
  arguments: {}
}));
assert.deepEqual(revivalRegistry.result.structuredContent, expectedRevivalRegistry);
assert.equal(revivalRegistry.result.structuredContent.schema, "project-telos.revival-registry/v1");
assert.ok(revivalRegistry.result.structuredContent.tools.some((tool) => tool.id === "calibrate-pro"));

const expectedDisplayCalibration = JSON.parse(
  readFileSync(new URL("./integrations/display-calibration.json", import.meta.url), "utf8")
);
const displayCalibration = handleRequest(request("tools/call", {
  name: "telos.display.calibration",
  arguments: {}
}));
assert.deepEqual(displayCalibration.result.structuredContent, expectedDisplayCalibration);
assert.equal(displayCalibration.result.structuredContent.schema, "project-telos.display-calibration/v1");
assert.equal(displayCalibration.result.structuredContent.contract.hardware_mutation_allowed, false);

const badTool = handleRequest(request("tools/call", { name: "telos.missing", arguments: {} }));
assert.equal(badTool.error.code, -32000);
assert.match(badTool.error.message, /unknown tool/);

const serverPath = fileURLToPath(new URL("./telos-mcp.mjs", import.meta.url));
const stdio = spawnSync(process.execPath, [serverPath], {
  input: JSON.stringify({ jsonrpc: "2.0", id: 7, method: "tools/list" }) + "\n",
  encoding: "utf8"
});
assert.equal(stdio.status, 0, stdio.stderr || stdio.stdout);
const stdioResponse = JSON.parse(stdio.stdout.trim());
assert.equal(stdioResponse.id, 7);
assert.ok(stdioResponse.result.tools.some((tool) => tool.name === "telos.workflow"));
assert.ok(stdioResponse.result.tools.some((tool) => tool.name === "telos.catalog"));
assert.ok(stdioResponse.result.tools.some((tool) => tool.name === "telos.server.manifest"));
assert.ok(stdioResponse.result.tools.some((tool) => tool.name === "telos.admission.telemetry"));
assert.ok(stdioResponse.result.tools.some((tool) => tool.name === "telos.context.envelope"));
assert.ok(stdioResponse.result.tools.some((tool) => tool.name === "telos.action.receipt"));
assert.ok(stdioResponse.result.tools.some((tool) => tool.name === "telos.loop.ledger"));
assert.ok(stdioResponse.result.tools.some((tool) => tool.name === "telos.objective.monitor"));
assert.ok(stdioResponse.result.tools.some((tool) => tool.name === "telos.research.seed"));
assert.ok(stdioResponse.result.tools.some((tool) => tool.name === "telos.rendering.research"));
assert.ok(stdioResponse.result.tools.some((tool) => tool.name === "telos.rendering.capabilities"));
assert.ok(stdioResponse.result.tools.some((tool) => tool.name === "telos.measurement.layers"));
assert.ok(stdioResponse.result.tools.some((tool) => tool.name === "telos.creative.engine"));
assert.ok(stdioResponse.result.tools.some((tool) => tool.name === "telos.creative.kernels"));
assert.ok(stdioResponse.result.tools.some((tool) => tool.name === "telos.revival.registry"));
assert.ok(stdioResponse.result.tools.some((tool) => tool.name === "telos.display.calibration"));
