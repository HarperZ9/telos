import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { detectObjectiveSignals, objectiveMonitorPacket } from "./objective-monitor.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));

const trace = [
  { step: 1, proxy_score: 0.62, quality_score: 0.81, components: { tests: 0.9, readability: 0.82, receipts: 0.72 } },
  { step: 2, proxy_score: 0.67, quality_score: 0.8, components: { tests: 0.92, readability: 0.78, receipts: 0.71 } },
  { step: 3, proxy_score: 0.73, quality_score: 0.76, components: { tests: 0.97, readability: 0.68, receipts: 0.63 } },
  { step: 4, proxy_score: 0.81, quality_score: 0.68, components: { tests: 1.0, readability: 0.55, receipts: 0.49 } },
  { step: 5, proxy_score: 0.88, quality_score: 0.59, components: { tests: 1.0, readability: 0.43, receipts: 0.36 } },
  { step: 6, proxy_score: 0.94, quality_score: 0.51, components: { tests: 1.0, readability: 0.34, receipts: 0.25 } }
];

const signals = detectObjectiveSignals(trace);
const codes = new Set(signals.map((signal) => signal.code));

assert.ok(codes.has("proxy_quality_divergence"));
assert.ok(codes.has("component_dominance"));
assert.ok(codes.has("ceiling_saturation"));
assert.ok(codes.has("steps_since_improvement"));
assert.ok(signals.every((signal) => signal.verdict === "DRIFT" || signal.verdict === "MATCH"));

const packet = objectiveMonitorPacket({ trace });
assert.equal(packet.schema, "project-telos.objective-monitor/v1");
assert.equal(packet.tool, "telos.objective.monitor");
assert.equal(packet.contract.raw_prompt_required, false);
assert.equal(packet.contract.raw_tool_args_required, false);
assert.equal(packet.source_inspiration.repo, "AvAdiii/rewardspy");
assert.ok(packet.failure_codes.includes("proxy_quality_divergence"));
assert.ok(packet.failure_codes.includes("component_dominance"));
assert.ok(packet.failure_codes.includes("ceiling_saturation"));
assert.ok(packet.failure_codes.includes("steps_since_improvement"));
assert.ok(packet.signals.length >= 4);
assert.ok(packet.receipt_hash.startsWith("fnv1a:"));

const cli = spawnSync(process.execPath, [path.join(here, "objective-monitor.mjs")], {
  cwd: path.resolve(here, ".."),
  encoding: "utf8"
});
assert.equal(cli.status, 0, cli.stderr || cli.stdout);
assert.deepEqual(JSON.parse(cli.stdout), objectiveMonitorPacket());

const summary = spawnSync(process.execPath, [path.join(here, "objective-monitor.mjs"), "--summary"], {
  cwd: path.resolve(here, ".."),
  encoding: "utf8"
});
assert.equal(summary.status, 0, summary.stderr || summary.stdout);
assert.match(summary.stdout, /Telos Objective Monitor/);
assert.match(summary.stdout, /signals\s+[0-9]+/);
assert.match(summary.stdout, /proxy_quality_divergence/);
