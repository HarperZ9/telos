import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

const packet = JSON.parse(
  readFileSync(new URL("./research/operator-source-leads.json", import.meta.url), "utf8")
);

assert.equal(packet.schema, "project-telos.operator-source-leads/v1");
assert.ok(Array.isArray(packet.leads));
assert.equal(packet.leads.length, 4);
assert.ok(packet.next_actions.some((action) => action.startsWith("gather.browser:")));

const byId = new Map(packet.leads.map((lead) => [lead.lead_id, lead]));

const reddit = byId.get("lead-reddit-gamechanging-websites");
assert.equal(reddit.evidence_status, "UNVERIFIABLE");
assert.equal(reddit.provenance_class, "operator_source_lead");
assert.equal(reddit.gather_receipt.chars, 0);
assert.equal(reddit.gather_receipt.verified, true);
assert.match(reddit.gather_receipt.digest_seal, /^[a-f0-9]{64}$/);
assert.match(reddit.promotion_rule, /independent source/);

for (const id of [
  "lead-vast-ai-gpu-provider",
  "lead-hostkey-rendering-gpu-server",
  "lead-irender-gpu-cloud-rendering"
]) {
  const lead = byId.get(id);
  assert.ok(lead.url.startsWith("https://"));
  assert.equal(lead.evidence_status, "UNVERIFIABLE");
  assert.equal(lead.provenance_class, "operator_source_lead");
  assert.match(lead.promotion_rule, /provider|infrastructure|render-farm|rendering-technique/);
}
