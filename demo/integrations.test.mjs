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
  "telos.research.seed",
  "telos.rendering.research",
  "telos.rendering.capabilities",
  "telos.creative.engine"
]) {
  assert.ok(names.has(name), `missing ${name}`);
}

for (const tool of catalog.tools) {
  assert.match(tool.name, /^(gather|index|forum|crucible|telos)\.[a-z.]+$/);
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
