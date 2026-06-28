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
  "telos.research.seed"
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

const expectedResearchSeed = JSON.parse(
  readFileSync(new URL("./research/fundamental-physics-seeds.json", import.meta.url), "utf8")
);
const researchSeed = handleRequest(request("tools/call", {
  name: "telos.research.seed",
  arguments: {}
}));
assert.deepEqual(researchSeed.result.structuredContent, expectedResearchSeed);
assert.equal(researchSeed.result.structuredContent.schema, "project-telos.research-seed/v1");
assert.equal(researchSeed.result.structuredContent.seeds.length, 2);

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
assert.ok(stdioResponse.result.tools.some((tool) => tool.name === "telos.research.seed"));
