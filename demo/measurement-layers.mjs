import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";

import { magnitudeSpectrum } from "./render-sound/dft.mjs";

const contract = JSON.parse(
  readFileSync(new URL("./integrations/measurement-layers.json", import.meta.url), "utf8")
);

function stableStringify(value) {
  if (Array.isArray(value)) return `[${value.map(stableStringify).join(",")}]`;
  if (value && typeof value === "object") {
    return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${stableStringify(value[key])}`).join(",")}}`;
  }
  return JSON.stringify(value);
}

function hashStable(value) {
  const text = typeof value === "string" ? value : stableStringify(value);
  let hash = 2166136261;
  for (let i = 0; i < text.length; i++) {
    hash ^= text.charCodeAt(i);
    hash = Math.imul(hash, 16777619) >>> 0;
  }
  return `fnv1a:${hash.toString(16).padStart(8, "0")}`;
}

function numericArray(values, label) {
  const array = Array.from(values ?? []);
  if (!array.length) throw new Error(`${label}: measurement_source_missing`);
  for (const value of array) {
    if (!Number.isFinite(Number(value))) throw new Error(`${label}: measurement_source_missing`);
  }
  return array.map(Number);
}

function round(value, places = 4) {
  const scale = 10 ** places;
  return Math.round(value * scale) / scale;
}

export function measureHistogramField({ pixels, width, height, bins = 16 }) {
  const values = numericArray(pixels, "histogram");
  if (width * height !== values.length) throw new Error("histogram: pixel_dimensions_mismatch");
  const histogram = Array.from({ length: bins }, () => 0);
  let min = 255;
  let max = 0;
  let total = 0;
  for (const value of values) {
    const luminance = Math.max(0, Math.min(255, Math.round(value)));
    min = Math.min(min, luminance);
    max = Math.max(max, luminance);
    total += luminance;
    histogram[Math.min(bins - 1, Math.floor((luminance / 256) * bins))] += 1;
  }
  const measurement = {
    layer_id: "visual.histogram-field",
    total_pixels: values.length,
    bin_count: bins,
    bins: histogram,
    min_luminance: min,
    max_luminance: max,
    mean_luminance: round(total / values.length),
    contrast_ratio: round((max + 1) / (min + 1))
  };
  measurement.measurement_hash = hashStable(measurement);
  return measurement;
}

export function measureDitherField({ pixels, width, height, matrixSize = 4 }) {
  const values = numericArray(pixels, "dither");
  if (width * height !== values.length) throw new Error("dither: pixel_dimensions_mismatch");
  const unique = new Set(values.map((value) => Math.max(0, Math.min(255, Math.round(value)))));
  let transitions = 0;
  for (let y = 0; y < height; y++) {
    for (let x = 1; x < width; x++) {
      const left = values[y * width + x - 1];
      const here = values[y * width + x];
      if (Math.abs(here - left) >= 16) transitions += 1;
    }
  }
  const tiled = width % matrixSize === 0 && height % matrixSize === 0;
  const measurement = {
    layer_id: "visual.dither-spectrum-meter",
    unique_levels: unique.size,
    pattern: tiled ? "ordered-bayer-candidate" : "irregular-threshold-candidate",
    matrix_size: matrixSize,
    horizontal_transition_count: transitions,
    algorithm_candidates: ["ordered-bayer", "void-and-cluster", "blue-noise"]
  };
  measurement.measurement_hash = hashStable(measurement);
  return measurement;
}

export function measureSplatProbe({ splats, viewport = { width: 1, height: 1 } }) {
  const items = Array.isArray(splats) ? splats : [];
  if (!items.length) throw new Error("splat: measurement_source_missing");
  const xs = items.map((item) => Number(item.x));
  const ys = items.map((item) => Number(item.y));
  const zs = items.map((item) => Number(item.z ?? 0));
  const radii = items.map((item) => Math.max(0, Number(item.radius ?? 0)));
  const opacities = items.map((item) => Math.max(0, Math.min(1, Number(item.opacity ?? 1))));
  const area = Math.max(1, Number(viewport.width) * Number(viewport.height));
  const coverage = radii.reduce((sum, radius) => sum + Math.PI * radius * radius, 0) / area;
  const measurement = {
    layer_id: "spatial.splat-probe",
    splat_count: items.length,
    bounds: {
      x: [Math.min(...xs), Math.max(...xs)],
      y: [Math.min(...ys), Math.max(...ys)],
      z: [Math.min(...zs), Math.max(...zs)]
    },
    radius_mean: round(radii.reduce((sum, value) => sum + value, 0) / radii.length),
    opacity_mean: round(opacities.reduce((sum, value) => sum + value, 0) / opacities.length),
    coverage_estimate: round(coverage)
  };
  measurement.measurement_hash = hashStable(measurement);
  return measurement;
}

export function measureClusterMeter({ grid, lights, budget = {} }) {
  const columns = Math.max(1, Math.trunc(Number(grid?.columns ?? 1)));
  const rows = Math.max(1, Math.trunc(Number(grid?.rows ?? 1)));
  const maxLights = Math.max(1, Math.trunc(Number(budget.maxLightsPerCluster ?? 8)));
  const items = Array.isArray(lights) ? lights : [];
  if (!items.length) throw new Error("cluster: measurement_source_missing");
  const counts = [];
  for (let row = 0; row < rows; row++) {
    for (let column = 0; column < columns; column++) {
      const cx = (column + 0.5) / columns;
      const cy = (row + 0.5) / rows;
      let count = 0;
      for (const light of items) {
        const dx = cx - Number(light.x);
        const dy = cy - Number(light.y);
        const radius = Math.max(0, Number(light.radius ?? 0));
        if (Math.hypot(dx, dy) <= radius) count += 1;
      }
      counts.push(count);
    }
  }
  const max = Math.max(...counts);
  const histogram = {};
  for (const count of counts) histogram[count] = (histogram[count] ?? 0) + 1;
  const measurement = {
    layer_id: "lighting.cluster-meter",
    grid: { columns, rows },
    cluster_count: counts.length,
    max_lights_per_cluster: max,
    mean_lights_per_cluster: round(counts.reduce((sum, count) => sum + count, 0) / counts.length),
    over_budget_clusters: counts.filter((count) => count > maxLights).length,
    histogram
  };
  measurement.measurement_hash = hashStable(measurement);
  return measurement;
}

export function measureAudioSpectrum({ samples, bins = 32 }) {
  const values = numericArray(samples, "audio");
  const spectrum = Array.from(magnitudeSpectrum(Float64Array.from(values), bins, { window: false }));
  const ranked = spectrum
    .map((magnitude, bin) => ({ bin, magnitude: round(magnitude) }))
    .sort((a, b) => b.magnitude - a.magnitude)
    .slice(0, 5);
  const total = spectrum.reduce((sum, value) => sum + value, 0);
  const centroid = total === 0
    ? 0
    : spectrum.reduce((sum, value, bin) => sum + value * bin, 0) / total;
  const measurement = {
    layer_id: "audio.spectral-meter",
    bin_count: bins,
    dominant_bins: ranked,
    spectral_centroid_bin: round(centroid)
  };
  measurement.measurement_hash = hashStable(measurement);
  return measurement;
}

export function demoMeasurements() {
  const pixels = Uint8Array.from(Array.from({ length: 64 }, (_, index) => (index * 37 + (index % 4) * 19) % 256));
  const splats = [
    { x: -0.7, y: -0.4, z: 0, radius: 0.35, opacity: 0.72 },
    { x: 0.25, y: -0.2, z: 0.12, radius: 0.42, opacity: 0.64 },
    { x: 0.62, y: 0.5, z: -0.08, radius: 0.31, opacity: 0.86 },
    { x: -0.18, y: 0.68, z: 0.2, radius: 0.28, opacity: 0.78 }
  ];
  const samples = Float64Array.from({ length: 64 }, (_, index) => (
    Math.sin((2 * Math.PI * 5 * index) / 64) + 0.45 * Math.sin((2 * Math.PI * 11 * index) / 64)
  ));
  const measurements = [
    measureHistogramField({ pixels, width: 8, height: 8, bins: 8 }),
    measureDitherField({ pixels, width: 8, height: 8, matrixSize: 4 }),
    measureSplatProbe({ splats, viewport: { width: 4, height: 3 } }),
    measureClusterMeter({
      grid: { columns: 4, rows: 3 },
      lights: [
        { x: 0.14, y: 0.16, radius: 0.22 },
        { x: 0.34, y: 0.2, radius: 0.25 },
        { x: 0.72, y: 0.7, radius: 0.3 },
        { x: 0.82, y: 0.42, radius: 0.18 }
      ],
      budget: { maxLightsPerCluster: 4 }
    }),
    measureAudioSpectrum({ samples, bins: 32 })
  ];
  const packet = {
    schema: contract.schema,
    tool: contract.tool,
    generated_at: contract.generated_at,
    status: "MATCH",
    purpose: contract.purpose,
    layers: contract.layers.map((layer) => layer.layer_id),
    measurements,
    source_receipts: contract.source_receipts,
    privacy: contract.privacy,
    failure_codes: contract.failure_codes,
    next_actions: contract.next_actions
  };
  packet.receipt_hash = hashStable(packet);
  return packet;
}

export function summary(packet = demoMeasurements()) {
  const lines = [
    "Telos Measurement Layers",
    `schema       ${packet.schema}`,
    `tool         ${packet.tool}`,
    `layers       ${packet.layers.length}`,
    `measurements ${packet.measurements.length}`,
    `status       ${packet.status}`,
    "next         node demo/measurement-layers.mjs"
  ];
  return `${lines.join("\n")}\n`;
}

function main() {
  const packet = demoMeasurements();
  if (process.argv.includes("--summary")) {
    process.stdout.write(summary(packet));
  } else {
    process.stdout.write(`${JSON.stringify(packet, null, 2)}\n`);
  }
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  main();
}
