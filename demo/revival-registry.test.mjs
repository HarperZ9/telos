import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { spawnSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const registry = JSON.parse(readFileSync(new URL("./integrations/revival-registry.json", import.meta.url), "utf8"));

assert.equal(registry.schema, "project-telos.revival-registry/v1");
assert.equal(registry.tool, "telos.revival.registry");
assert.equal(registry.contract.protocol_agnostic, true);
assert.equal(registry.contract.receipts_required, true);
assert.equal(registry.contract.raw_source_required_for_interop, false);
assert.ok(registry.promotion_standard.includes("cli-json"));
assert.ok(registry.promotion_standard.includes("mcp-adapter-or-roadmap"));
assert.ok(registry.promotion_standard.includes("privacy-boundary"));

const byId = new Map(registry.tools.map((tool) => [tool.id, tool]));
for (const id of [
  "calibrate-pro",
  "quanta-color",
  "quantalang",
  "warden-security-lineage",
  "agent-audit",
  "context-curator-lite",
  "secret-redact-io",
  "repo-proof-index",
  "release-surface-scanner",
  "gpu-trace-validator"
]) {
  assert.ok(byId.has(id), `missing revived tool ${id}`);
}

const calibrate = byId.get("calibrate-pro");
assert.equal(calibrate.promotion_lane, "display-calibration");
assert.equal(calibrate.status, "promotion-ready");
assert.ok(calibrate.flagship_hosts.includes("telos.measurement.layers"));
assert.ok(calibrate.flagship_hosts.includes("telos.creative.engine"));
assert.ok(calibrate.flagship_hosts.includes("crucible.measurement_gate"));
assert.ok(calibrate.capabilities.includes("display calibration workflows"));
assert.ok(calibrate.capabilities.includes("ICC and LUT artifact generation"));
assert.ok(calibrate.integration_targets.includes("telos.display.calibration"));
assert.ok(calibrate.provenance.receipts.some((receipt) => receipt.sha256.startsWith("04e294f1")));

const color = byId.get("quanta-color");
assert.equal(color.promotion_lane, "color-science-library");
assert.ok(color.capabilities.includes("Delta-E and perceptual difference metrics"));
assert.ok(color.flagship_hosts.includes("calibrate-pro"));

const language = byId.get("quantalang");
assert.equal(language.promotion_lane, "effects-language");
assert.ok(language.capabilities.includes("compiled shader/effects language"));
assert.ok(language.integration_targets.includes("telos.creative.kernels"));

const warden = byId.get("warden-security-lineage");
assert.equal(warden.promotion_lane, "defensive-find-and-fix");
assert.equal(warden.status, "quarantine-and-adapt");
assert.match(warden.risk_boundary, /defensive/);
assert.match(warden.risk_boundary, /authorized/);
assert.equal(warden.exposed_offensive_commands, false);
assert.ok(warden.integration_targets.includes("telos.find_fix"));

const curator = byId.get("context-curator-lite");
assert.equal(curator.promotion_lane, "context-envelope-source");
assert.equal(curator.status, "promotion-ready");
assert.ok(curator.capabilities.includes("Project Telos context-envelope export"));
assert.ok(curator.capabilities.includes("lossless-by-reference context packets"));
assert.ok(curator.flagship_hosts.includes("telos.context.envelope"));
assert.ok(curator.flagship_hosts.includes("index.context.envelope"));
assert.ok(curator.integration_targets.includes("crucible.assess"));
assert.match(curator.risk_boundary, /not a security boundary/);
assert.ok(curator.provenance.receipts.some((receipt) => receipt.sha256.startsWith("134f4b95")));

for (const tool of registry.tools) {
  assert.ok(tool.origin_paths.length > 0, `${tool.id} has origin paths`);
  assert.ok(tool.flagship_hosts.length > 0, `${tool.id} has flagship hosts`);
  assert.ok(tool.capabilities.length > 0, `${tool.id} has capabilities`);
  assert.ok(tool.integration_targets.length > 0, `${tool.id} has integration targets`);
  assert.ok(tool.next_actions.length > 0, `${tool.id} has next actions`);
  assert.ok(tool.provenance.evidence.length > 0, `${tool.id} has evidence`);
  assert.ok(tool.risk_boundary.length > 0, `${tool.id} has risk boundary`);
}

const cli = spawnSync(process.execPath, [path.join(here, "revival-registry.mjs")], {
  cwd: path.resolve(here, ".."),
  encoding: "utf8"
});
assert.equal(cli.status, 0, cli.stderr || cli.stdout);
assert.deepEqual(JSON.parse(cli.stdout), registry);

const summary = spawnSync(process.execPath, [path.join(here, "revival-registry.mjs"), "--summary"], {
  cwd: path.resolve(here, ".."),
  encoding: "utf8"
});
assert.equal(summary.status, 0, summary.stderr || summary.stdout);
assert.match(summary.stdout, /Telos Revival Registry/);
assert.match(summary.stdout, /tools\s+10/);
assert.match(summary.stdout, /display-calibration/);
assert.match(summary.stdout, /quarantine-and-adapt/);
