import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

import {
  bayerMatrix,
  buildCreativeKernelPacket,
  clusterLightBins,
  harmonographPath,
  orderedDither,
  pixelSortRows,
  stableReceiptHash
} from "./creative-kernels.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));

assert.deepEqual(bayerMatrix(2), [
  [0, 2],
  [3, 1]
]);
assert.deepEqual(bayerMatrix(4)[0], [0, 8, 2, 10]);
assert.throws(() => bayerMatrix(3), /bayer: size_must_be_power_of_two/);

const pixels = Uint8Array.from([
  0, 32, 96, 160,
  224, 192, 128, 64
]);
const dither = orderedDither({ pixels, width: 4, height: 2, matrixSize: 4, levels: 4 });
assert.equal(dither.width, 4);
assert.equal(dither.height, 2);
assert.equal(dither.levels, 4);
assert.equal(dither.output.length, pixels.length);
assert.ok(dither.output.every((value) => [0, 85, 170, 255].includes(value)));
assert.equal(dither.measurement.layer_id, "visual.dither-spectrum-meter");
assert.match(dither.receipt_hash, /^fnv1a:/);

const sorted = pixelSortRows({
  pixels: Uint8Array.from([40, 10, 200, 180, 120, 20, 240, 90]),
  width: 4,
  height: 2,
  threshold: 100
});
assert.deepEqual(Array.from(sorted.output.slice(0, 4)), [40, 10, 180, 200]);
assert.deepEqual(Array.from(sorted.output.slice(4, 8)), [20, 90, 120, 240]);
assert.equal(sorted.runs.length, 2);
assert.match(sorted.receipt_hash, /^fnv1a:/);

const harmonograph = harmonographPath({
  samples: 8,
  x: { frequency: 2, phase: 0, amplitude: 1, damping: 0.01 },
  y: { frequency: 3, phase: Math.PI / 2, amplitude: 0.5, damping: 0.02 }
});
assert.equal(harmonograph.points.length, 8);
assert.ok(harmonograph.bounds.x[0] <= harmonograph.bounds.x[1]);
assert.ok(harmonograph.bounds.y[0] <= harmonograph.bounds.y[1]);
assert.equal(harmonograph.measurement.layer_id, "plotter.harmonograph-path");

const clusters = clusterLightBins({
  grid: { columns: 2, rows: 2, slices: 2 },
  lights: [
    { x: 0.25, y: 0.25, z: 0.25, radius: 0.2 },
    { x: 0.75, y: 0.25, z: 0.75, radius: 0.3 },
    { x: 0.8, y: 0.8, z: 0.5, radius: 0.2 }
  ],
  budget: { maxLightsPerCluster: 2 }
});
assert.equal(clusters.cluster_count, 8);
assert.ok(clusters.max_lights_per_cluster >= 1);
assert.equal(clusters.measurement.layer_id, "lighting.cluster-meter");

assert.equal(stableReceiptHash({ b: 2, a: 1 }), stableReceiptHash({ a: 1, b: 2 }));

const packet = buildCreativeKernelPacket();
assert.equal(packet.schema, "project-telos.creative-kernels/v1");
assert.equal(packet.tool, "telos.creative.kernels");
assert.equal(packet.status, "MATCH");
assert.deepEqual(packet.kernels.map((kernel) => kernel.id), [
  "raster.ordered-dither",
  "raster.pixel-sort-rows",
  "plotter.harmonograph-path",
  "lighting.cluster-light-bins"
]);
assert.equal(packet.privacy.raw_assets_required_for_interop, false);
assert.ok(packet.source_receipts.every((receipt) => receipt.provenance_class === "lawful_source"));

const cli = spawnSync(process.execPath, [path.join(here, "creative-kernels.mjs")], {
  cwd: path.resolve(here, ".."),
  encoding: "utf8"
});
assert.equal(cli.status, 0, cli.stderr || cli.stdout);
assert.deepEqual(JSON.parse(cli.stdout), packet);

const summary = spawnSync(process.execPath, [path.join(here, "creative-kernels.mjs"), "--summary"], {
  cwd: path.resolve(here, ".."),
  encoding: "utf8"
});
assert.equal(summary.status, 0, summary.stderr || summary.stdout);
assert.match(summary.stdout, /Telos Creative Kernels/);
assert.match(summary.stdout, /kernels\s+4/);
