import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import {
  demoMeasurements,
  makeMeasurementEvent,
  measureAudioSpectrum,
  measureClusterMeter,
  measureDitherField,
  measureHistogramField,
  measureSplatProbe
} from "./measurement-layers.mjs";
import { handleRequest, tools } from "./telos-mcp.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const contract = JSON.parse(
  readFileSync(new URL("./integrations/measurement-layers.json", import.meta.url), "utf8")
);
const catalog = JSON.parse(
  readFileSync(new URL("./integrations/mcp-tool-catalog.json", import.meta.url), "utf8")
);
const manifest = JSON.parse(
  readFileSync(new URL("./integrations/mcp-server-manifest.json", import.meta.url), "utf8")
);

assert.equal(contract.schema, "project-telos.measurement-layers/v1");
assert.equal(contract.tool, "telos.measurement.layers");
assert.equal(contract.measurement_bus.schema, "project-telos.measurement-bus/v1");
assert.ok(contract.measurement_bus.event_fields.includes("event_id"));
assert.ok(contract.measurement_bus.event_fields.includes("coordinate_space"));
assert.ok(contract.measurement_bus.sensor_lanes.render.includes("lighting.cluster-meter"));
assert.ok(contract.measurement_bus.sensor_lanes.creative.includes("visual.dither-spectrum-meter"));
assert.ok(contract.measurement_bus.sensor_lanes.scientific.includes("audio.spectral-meter"));

const layerIds = new Set(contract.layers.map((layer) => layer.layer_id));
for (const id of [
  "visual.histogram-field",
  "visual.dither-spectrum-meter",
  "spatial.splat-probe",
  "lighting.cluster-meter",
  "audio.spectral-meter"
]) {
  assert.ok(layerIds.has(id), `missing measurement layer ${id}`);
}

for (const layer of contract.layers) {
  assert.equal(layer.evidence_status, "MATCH");
  assert.ok(layer.outputs.length > 0, `${layer.layer_id} exposes outputs`);
  assert.ok(layer.failure_codes.length > 0, `${layer.layer_id} exposes failure codes`);
}

const pixels = Uint8Array.from([
  0, 32, 64, 96,
  128, 160, 192, 224,
  16, 48, 80, 112,
  144, 176, 208, 240
]);
const histogram = measureHistogramField({ pixels, width: 4, height: 4, bins: 8 });
assert.equal(histogram.total_pixels, 16);
assert.equal(histogram.bin_count, 8);
assert.equal(histogram.bins.reduce((sum, count) => sum + count, 0), 16);
assert.equal(histogram.min_luminance, 0);
assert.equal(histogram.max_luminance, 240);
assert.ok(histogram.contrast_ratio > 1);
assert.match(histogram.measurement_hash, /^fnv1a:/);

const dither = measureDitherField({ pixels, width: 4, height: 4, matrixSize: 4 });
assert.equal(dither.pattern, "ordered-bayer-candidate");
assert.equal(dither.unique_levels, 16);
assert.ok(dither.algorithm_candidates.includes("ordered-bayer"));
assert.ok(dither.algorithm_candidates.includes("blue-noise"));
assert.match(dither.measurement_hash, /^fnv1a:/);

const splat = measureSplatProbe({
  splats: [
    { x: -1, y: -1, z: 0, radius: 0.4, opacity: 0.7 },
    { x: 1, y: -1, z: 0.2, radius: 0.5, opacity: 0.6 },
    { x: 0.5, y: 1, z: -0.1, radius: 0.3, opacity: 0.9 }
  ],
  viewport: { width: 4, height: 3 }
});
assert.equal(splat.splat_count, 3);
assert.deepEqual(splat.bounds.x, [-1, 1]);
assert.ok(splat.coverage_estimate > 0);
assert.ok(splat.opacity_mean > 0.7);

const cluster = measureClusterMeter({
  grid: { columns: 4, rows: 3 },
  lights: [
    { x: 0.1, y: 0.1, radius: 0.25 },
    { x: 0.35, y: 0.2, radius: 0.25 },
    { x: 0.8, y: 0.8, radius: 0.2 }
  ],
  budget: { maxLightsPerCluster: 3 }
});
assert.equal(cluster.cluster_count, 12);
assert.ok(cluster.max_lights_per_cluster >= 1);
assert.equal(cluster.over_budget_clusters, 0);

const samples = Float64Array.from({ length: 32 }, (_, index) => (
  Math.sin((2 * Math.PI * 3 * index) / 32) + 0.5 * Math.sin((2 * Math.PI * 7 * index) / 32)
));
const audio = measureAudioSpectrum({ samples, bins: 16 });
assert.equal(audio.bin_count, 16);
assert.equal(audio.dominant_bins[0].bin, 3);
assert.ok(audio.dominant_bins.some((bin) => bin.bin === 7));
assert.match(audio.measurement_hash, /^fnv1a:/);

const packet = demoMeasurements();
assert.equal(packet.schema, "project-telos.measurement-layers/v1");
assert.equal(packet.tool, "telos.measurement.layers");
assert.equal(packet.status, "MATCH");
assert.equal(packet.measurements.length, 5);
assert.equal(packet.measurement_bus.schema, "project-telos.measurement-bus/v1");
assert.equal(packet.events.length, packet.measurements.length);
assert.deepEqual(
  packet.events.map((event) => event.subject_ref),
  packet.measurements.map((measurement) => measurement.layer_id)
);
const histogramEvent = makeMeasurementEvent(histogram, { runId: "test.run", frameId: "frame:histogram" });
assert.equal(histogramEvent.event_id, "test.run:visual.histogram-field");
assert.equal(histogramEvent.frame_id, "frame:histogram");
assert.equal(histogramEvent.coordinate_space, "image.pixel");
assert.equal(histogramEvent.units.luminance, "0..255");
assert.equal(histogramEvent.privacy.raw_payload_required, false);
assert.equal(histogramEvent.provenance.measurement_hash, histogram.measurement_hash);
assert.match(histogramEvent.event_hash, /^fnv1a:/);
assert.throws(
  () => makeMeasurementEvent({ layer_id: "unknown.layer", measurement_hash: "fnv1a:00000000" }),
  /measurement_bus: unknown_layer unknown\.layer/
);
assert.equal(packet.privacy.raw_payload_required, false);
assert.ok(packet.failure_codes.includes("measurement_source_missing"));

const cli = spawnSync(process.execPath, [path.join(here, "measurement-layers.mjs")], {
  cwd: path.resolve(here, ".."),
  encoding: "utf8"
});
assert.equal(cli.status, 0, cli.stderr || cli.stdout);
assert.deepEqual(JSON.parse(cli.stdout), packet);

const summary = spawnSync(process.execPath, [path.join(here, "measurement-layers.mjs"), "--summary"], {
  cwd: path.resolve(here, ".."),
  encoding: "utf8"
});
assert.equal(summary.status, 0, summary.stderr || summary.stdout);
assert.match(summary.stdout, /Telos Measurement Layers/);
assert.match(summary.stdout, /layers\s+5/);
assert.match(summary.stdout, /measurements\s+5/);

assert.ok(tools.some((tool) => tool.name === "telos.measurement.layers"));
const mcp = handleRequest({
  jsonrpc: "2.0",
  id: 108,
  method: "tools/call",
  params: { name: "telos.measurement.layers", arguments: {} }
});
assert.equal(mcp.result.structuredContent.tool, "telos.measurement.layers");
assert.equal(mcp.result.structuredContent.measurements.length, 5);
assert.equal(mcp.result.structuredContent.events.length, 5);
assert.equal(mcp.result.structuredContent.measurement_bus.schema, "project-telos.measurement-bus/v1");

const catalogTool = catalog.tools.find((tool) => tool.name === "telos.measurement.layers");
assert.ok(catalogTool, "catalog exposes telos.measurement.layers");
assert.deepEqual(catalogTool.cli, ["node", "demo/measurement-layers.mjs"]);
assert.equal(catalogTool.mcp.tool, "telos.measurement.layers");
assert.ok(manifest.servers.telos.expected_tools.includes("telos.measurement.layers"));
