import { magnitudeSpectrum } from "./render-sound/dft.mjs";
import { hashStable, numericArray, round } from "./measurement-utils.mjs";

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
      if (Math.abs(values[y * width + x] - values[y * width + x - 1]) >= 16) transitions += 1;
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
    coverage_estimate: round(radii.reduce((sum, radius) => sum + Math.PI * radius * radius, 0) / area)
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
        if (Math.hypot(cx - Number(light.x), cy - Number(light.y)) <= Math.max(0, Number(light.radius ?? 0))) {
          count += 1;
        }
      }
      counts.push(count);
    }
  }
  const histogram = {};
  for (const count of counts) histogram[count] = (histogram[count] ?? 0) + 1;
  const measurement = {
    layer_id: "lighting.cluster-meter",
    grid: { columns, rows },
    cluster_count: counts.length,
    max_lights_per_cluster: Math.max(...counts),
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
  const centroid = total === 0 ? 0 : spectrum.reduce((sum, value, bin) => sum + value * bin, 0) / total;
  const measurement = {
    layer_id: "audio.spectral-meter",
    bin_count: bins,
    dominant_bins: ranked,
    spectral_centroid_bin: round(centroid)
  };
  measurement.measurement_hash = hashStable(measurement);
  return measurement;
}
