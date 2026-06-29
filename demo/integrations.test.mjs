import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

const catalog = JSON.parse(
  readFileSync(new URL("./integrations/mcp-tool-catalog.json", import.meta.url), "utf8")
);
const science = JSON.parse(
  readFileSync(new URL("./integrations/science-research-adapters.json", import.meta.url), "utf8")
);
const admissionTelemetry = JSON.parse(
  readFileSync(new URL("./integrations/admission-telemetry-conventions.json", import.meta.url), "utf8")
);

assert.equal(catalog.schema, "project-telos.mcp-tool-catalog/v1");
assert.equal(catalog.action_schema, "project-telos.flagship-action/v1");
assert.ok(catalog.transports.includes("stdio"));
assert.ok(catalog.transports.includes("streamable-http"));

const names = new Set(catalog.tools.map((tool) => tool.name));
for (const name of [
  "gather.status",
  "gather.doctor",
  "gather.docs",
  "gather.arxiv",
  "gather.run",
  "index.map",
  "index.context",
  "index.context.envelope",
  "index.status",
  "index.doctor",
  "forum.route",
  "forum.ledger.summary",
  "forum.prose.humanize",
  "forum.status",
  "forum.doctor",
  "crucible.status",
  "crucible.doctor",
  "crucible.assess",
  "crucible.recheck",
  "crucible.run",
  "crucible.measurement_gate",
  "crucible.review",
  "crucible.report",
  "crucible.batch",
  "crucible.registry",
  "crucible.drift",
  "crucible.refine",
  "crucible.verdicts",
  "telos.status",
  "telos.doctor",
  "telos.room",
  "telos.workflow",
  "telos.catalog",
  "telos.server.manifest",
  "telos.mcp.freshness",
  "telos.ci.doctor",
  "telos.presentation.doctor",
  "telos.accessibility.doctor",
  "telos.performance.doctor",
  "telos.admission.telemetry",
  "telos.context.envelope",
  "telos.context.pack",
  "telos.action.receipt",
  "telos.loop.ledger",
  "telos.research.seed",
  "telos.research.thermodynamic",
  "telos.rendering.research",
  "telos.rendering.capabilities",
  "telos.measurement.layers",
  "telos.creative.engine",
  "telos.creative.kernels",
  "telos.revival.registry",
  "telos.second_level.queue",
  "telos.workstation.substrate",
  "telos.display.calibration"
]) {
  assert.ok(names.has(name), `missing ${name}`);
}

for (const tool of catalog.tools) {
  assert.match(tool.name, /^(gather|index|forum|crucible|telos)\.[a-z._]+$/);
  assert.ok(Array.isArray(tool.cli) && tool.cli.length > 0, `${tool.name} has CLI fallback`);
  assert.equal(tool.mcp.method, "tools/call");
  assert.equal(tool.mcp.status, "available", `${tool.name} is native MCP available`);
}

const byName = new Map(catalog.tools.map((tool) => [tool.name, tool]));
assert.deepEqual(byName.get("crucible.recheck").cli, [
  "crucible",
  "recheck",
  "{dir}",
  "--index",
  "{index}",
  "--pack",
  "{pack}",
  "--json"
]);

assert.deepEqual(byName.get("crucible.measurement_gate").cli, [
  "crucible",
  "measurement-gate",
  "{packet}",
  "--criteria",
  "{criteria}",
  "--json"
]);

assert.deepEqual(byName.get("index.context.envelope").cli, [
  "index",
  "context-envelope",
  "--root",
  "{root}",
  "--budget",
  "{budget}",
  "--json"
]);

assert.deepEqual(byName.get("telos.creative.kernels").cli, [
  "node",
  "demo/creative-kernels.mjs"
]);

assert.deepEqual(byName.get("telos.revival.registry").cli, [
  "node",
  "demo/revival-registry.mjs"
]);

assert.deepEqual(byName.get("telos.workstation.substrate").cli, [
  "node",
  "demo/workstation-substrate.mjs"
]);

assert.deepEqual(byName.get("telos.display.calibration").cli, [
  "node",
  "demo/display-calibration.mjs"
]);

assert.deepEqual(byName.get("telos.mcp.freshness").cli, [
  "node",
  "demo/mcp-freshness.mjs"
]);

assert.deepEqual(byName.get("telos.ci.doctor").cli, [
  "node",
  "demo/ci-doctor.mjs"
]);

assert.deepEqual(byName.get("telos.presentation.doctor").cli, [
  "node",
  "demo/presentation-doctor.mjs"
]);

assert.deepEqual(byName.get("telos.accessibility.doctor").cli, [
  "node",
  "demo/accessibility-doctor.mjs"
]);

assert.deepEqual(byName.get("telos.performance.doctor").cli, [
  "node",
  "demo/performance-doctor.mjs"
]);

assert.deepEqual(byName.get("telos.context.pack").cli, [
  "node",
  "demo/context-pack.mjs"
]);

assert.deepEqual(byName.get("telos.research.thermodynamic").cli, [
  "node",
  "demo/thermodynamic-ai-chip-receipt.mjs"
]);

assert.equal(science.schema, "project-telos.science-research-adapters/v1");
assert.equal(science.freshness_policy.current_source_required, true);
assert.equal(science.legal_access_policy.lawful_full_text_required, true);
assert.equal(science.legal_access_policy.illicit_access_sources_allowed, false);
assert.equal(science.legal_access_policy.source_leads_allowed, true);
assert.equal(science.legal_access_policy.source_lead_status, "non_evidentiary");
assert.ok(science.legal_access_policy.blocked_sources.includes("sci-hub"));
assert.ok(science.legal_access_policy.source_lead_fields.includes("lawful_resolution_attempts"));
assert.match(science.legal_access_policy.source_lead_policy, /excluded from provenance/);

assert.equal(admissionTelemetry.schema, "project-telos.admission-telemetry/v1");
assert.ok(admissionTelemetry.required_fields.includes("verification.verdict"));

const adapterNames = new Set(science.adapters.map((adapter) => adapter.name));
for (const name of [
  "preprint.arxiv",
  "preprint.biorxiv",
  "preprint.medrxiv",
  "literature.pubmed",
  "literature.europepmc",
  "literature.openalex",
  "literature.crossref",
  "literature.semantic-scholar",
  "trials.clinicaltrials",
  "structure.alphafold-db",
  "structure.alphafold3",
  "medical.midjourney-medical",
  "oa.unpaywall",
  "oa.core",
  "oa.doaj",
  "oa.pubmed-central"
]) {
  assert.ok(adapterNames.has(name), `missing science adapter ${name}`);
}

for (const adapter of science.adapters) {
  assert.ok(adapter.primary_source.startsWith("https://"), `${adapter.name} has primary source`);
  assert.ok(adapter.status.length > 0, `${adapter.name} has status`);
}
