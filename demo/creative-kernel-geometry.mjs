import { assertPositiveInteger, numericArray, objectArray, stableReceiptHash } from "./creative-kernel-utils.mjs";

export function harmonographPath({ samples = 256, x, y }) {
  assertPositiveInteger(samples, "harmonograph.samples");
  const xSpec = { frequency: 2, phase: 0, amplitude: 1, damping: 0.01, ...x };
  const ySpec = { frequency: 3, phase: Math.PI / 2, amplitude: 1, damping: 0.01, ...y };
  const points = [];

  for (let index = 0; index < samples; index += 1) {
    const t = samples === 1 ? 0 : (index / (samples - 1)) * Math.PI * 2;
    const px = xSpec.amplitude * Math.sin(xSpec.frequency * t + xSpec.phase) * Math.exp(-xSpec.damping * index);
    const py = ySpec.amplitude * Math.sin(ySpec.frequency * t + ySpec.phase) * Math.exp(-ySpec.damping * index);
    points.push({ x: Number(px.toFixed(6)), y: Number(py.toFixed(6)) });
  }

  const bounds = {
    x: [Math.min(...points.map((point) => point.x)), Math.max(...points.map((point) => point.x))],
    y: [Math.min(...points.map((point) => point.y)), Math.max(...points.map((point) => point.y))]
  };
  const measurement = {
    layer_id: "plotter.harmonograph-path",
    samples,
    bounds,
    measurement_hash: stableReceiptHash({ kernel: "harmonographPath", samples, xSpec, ySpec, bounds })
  };
  return {
    kernel: "plotter.harmonograph-path",
    points,
    bounds,
    measurement,
    receipt_hash: stableReceiptHash({ measurement, points })
  };
}

export function clusterLightBins({ grid, lights, budget = {} }) {
  const columns = grid?.columns ?? 1;
  const rows = grid?.rows ?? 1;
  const slices = grid?.slices ?? 1;
  assertPositiveInteger(columns, "cluster.columns");
  assertPositiveInteger(rows, "cluster.rows");
  assertPositiveInteger(slices, "cluster.slices");
  const maxLightsPerCluster = budget.maxLightsPerCluster ?? Infinity;
  const lightValues = objectArray(lights ?? [], "lights").map((light) => ({
    x: Math.max(0, Math.min(1, light.x ?? 0)),
    y: Math.max(0, Math.min(1, light.y ?? 0)),
    z: Math.max(0, Math.min(1, light.z ?? 0.5)),
    radius: Math.max(0, light.radius ?? 0)
  }));
  const bins = [];

  for (let z = 0; z < slices; z += 1) {
    for (let y = 0; y < rows; y += 1) {
      for (let x = 0; x < columns; x += 1) {
        bins.push({ x, y, z, count: countLights({ x, y, z, columns, rows, slices }, lightValues) });
      }
    }
  }

  const maxLights = Math.max(...bins.map((bin) => bin.count), 0);
  const overBudget = Number.isFinite(maxLightsPerCluster)
    ? bins.filter((bin) => bin.count > maxLightsPerCluster).length
    : 0;
  const measurement = {
    layer_id: "lighting.cluster-meter",
    grid: { columns, rows, slices },
    light_count: lightValues.length,
    cluster_count: bins.length,
    max_lights_per_cluster: maxLights,
    over_budget_clusters: overBudget,
    measurement_hash: stableReceiptHash({ kernel: "clusterLightBins", grid: { columns, rows, slices }, bins })
  };
  return {
    kernel: "lighting.cluster-light-bins",
    bins,
    cluster_count: bins.length,
    max_lights_per_cluster: maxLights,
    over_budget_clusters: overBudget,
    measurement,
    receipt_hash: stableReceiptHash({ measurement, bins })
  };
}

function countLights(cell, lights) {
  const center = {
    x: (cell.x + 0.5) / cell.columns,
    y: (cell.y + 0.5) / cell.rows,
    z: (cell.z + 0.5) / cell.slices
  };
  const halfDiagonal = Math.hypot(1 / cell.columns, 1 / cell.rows, 1 / cell.slices) / 2;
  numericArray([center.x, center.y, center.z], "cluster.center");
  return lights.filter((light) => (
    Math.hypot(light.x - center.x, light.y - center.y, light.z - center.z) <= light.radius + halfDiagonal
  )).length;
}
