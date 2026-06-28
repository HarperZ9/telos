import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { tools } from "./telos-mcp.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const convention = JSON.parse(
  readFileSync(new URL("./integrations/research-seed-conventions.json", import.meta.url), "utf8")
);
const packet = JSON.parse(
  readFileSync(new URL("./research/fundamental-physics-seeds.json", import.meta.url), "utf8")
);
const catalog = JSON.parse(
  readFileSync(new URL("./integrations/mcp-tool-catalog.json", import.meta.url), "utf8")
);

assert.equal(convention.schema, "project-telos.research-seed/v1");
assert.equal(convention.contract.operator_notes_are_source_leads, true);
assert.equal(convention.contract.fresh_resolution_required, true);
assert.equal(convention.contract.hidden_payloads_allowed, false);

for (const field of [
  "seed_id",
  "operator_note",
  "normalized_concepts[]",
  "source_receipts[]",
  "evidence_status",
  "claim_boundaries[]",
  "next_actions[]"
]) {
  assert.ok(convention.required_fields.includes(field), `missing required field ${field}`);
}

assert.equal(packet.schema, "project-telos.research-seed/v1");
assert.equal(packet.generated_at, "2026-06-28T00:00:00.000Z");
assert.equal(packet.tool, "telos.research.seed");
assert.equal(packet.seeds.length, 2);

const byId = new Map(packet.seeds.map((seed) => [seed.seed_id, seed]));
assert.ok(byId.has("seed-neil-turok"));
assert.ok(byId.has("seed-planck-constant"));

const turok = byId.get("seed-neil-turok");
assert.equal(turok.operator_note, "Neil Turok");
assert.ok(turok.normalized_concepts.includes("cosmology"));
assert.ok(turok.normalized_concepts.includes("quantum-gravity"));
assert.equal(turok.evidence_status, "MATCH");
assert.ok(turok.source_receipts.some((receipt) => receipt.url.includes("ph.ed.ac.uk/people/neil-turok")));
assert.ok(turok.source_receipts.some((receipt) => receipt.url.includes("perimeterinstitute.ca/people/neil-turok")));

const planck = byId.get("seed-planck-constant");
assert.equal(planck.operator_note, "Planck's Constant");
assert.ok(planck.normalized_concepts.includes("metrology"));
assert.ok(planck.normalized_concepts.includes("quantum-scale"));
assert.equal(planck.evidence_status, "MATCH");
assert.ok(planck.claims.some((claim) => claim.value === "6.62607015e-34 J s"));
assert.ok(planck.source_receipts.some((receipt) => receipt.url.includes("bipm.org")));
assert.ok(planck.source_receipts.some((receipt) => receipt.url.includes("physics.nist.gov")));

for (const seed of packet.seeds) {
  assert.match(seed.seed_id, /^seed-[a-z0-9-]+$/);
  assert.ok(seed.source_receipts.length >= 2, `${seed.seed_id} has current source receipts`);
  assert.ok(seed.claim_boundaries.length > 0, `${seed.seed_id} has claim boundaries`);
  assert.ok(seed.next_actions.length > 0, `${seed.seed_id} has next actions`);
  for (const receipt of seed.source_receipts) {
    assert.match(receipt.receipt_hash, /^sha256:[a-f0-9]{64}$/);
    assert.match(receipt.resolved_at, /^2026-06-28T/);
    assert.equal(receipt.provenance_class, "lawful_source");
  }
}

assert.ok(catalog.tools.some((tool) => tool.name === "telos.research.seed"));
assert.ok(tools.some((tool) => tool.name === "telos.research.seed"));

const run = spawnSync(process.execPath, [path.join(here, "research-seed.mjs")], {
  cwd: path.resolve(here, ".."),
  encoding: "utf8"
});
assert.equal(run.status, 0, run.stderr || run.stdout);
assert.deepEqual(JSON.parse(run.stdout), packet);
