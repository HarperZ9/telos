import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";

import {
  measureAudioSpectrum,
  measureClusterMeter,
  measureDitherField,
  measureHistogramField,
  measureSplatProbe
} from "./measurement-basic-meters.mjs";
import {
  measureGeometryCurvature,
  measureInteractionTrace,
  measurePerformanceBudget,
  measureTemporalFlicker,
  measureUncertaintyBudget
} from "./measurement-engine-meters.mjs";
import { hashStable } from "./measurement-utils.mjs";

export {
  measureAudioSpectrum,
  measureClusterMeter,
  measureDitherField,
  measureGeometryCurvature,
  measureHistogramField,
  measureInteractionTrace,
  measurePerformanceBudget,
  measureSplatProbe,
  measureTemporalFlicker,
  measureUncertaintyBudget
};

const contract = JSON.parse(
  readFileSync(new URL("./integrations/measurement-layers.json", import.meta.url), "utf8")
);

const busDefaults = {
  "visual.histogram-field": ["visual", "image.pixel", { luminance: "0..255", count: "pixels" }, "histogram"],
  "visual.dither-spectrum-meter": ["sampling", "image.pixel", { level: "0..255", count: "pixels" }, "operator-summary"],
  "spatial.splat-probe": ["splat", "scene.normalized", { position: "scene-unit", opacity: "0..1", coverage: "viewport-ratio" }, "field-summary"],
  "lighting.cluster-meter": ["lighting", "view.cluster-grid", { count: "lights" }, "cluster-histogram"],
  "audio.spectral-meter": ["audio", "frequency.bin", { magnitude: "relative", bin: "fft-bin" }, "spectrum-summary"],
  "temporal.flicker-meter": ["temporal", "frame.sequence", { delta: "luminance", count: "transitions", time: "frame-index" }, "temporal-summary"],
  "geometry.curvature-meter": ["geometry", "sample.curve", { angle: "degrees", distance: "scene-unit" }, "curvature-summary"],
  "interaction.trace-meter": ["interaction", "event.sequence", { count: "events", time: "ms" }, "actor-transition-summary"],
  "uncertainty.budget-meter": ["uncertainty", "observation.set", { count: "observations", ratio: "0..1" }, "risk-summary"],
  "performance.frame-budget-meter": ["performance", "frame.sequence", { duration: "ms", ratio: "0..1" }, "frame-budget-summary"]
};

export function makeMeasurementEvent(measurement, {
  runId = "demo.measurement-layers",
  frameId = "frame:0",
  actor = "telos.measurement.layers",
  timestamp = contract.generated_at,
  clockDomain = "demo.logical"
} = {}) {
  const layer = busDefaults[measurement.layer_id];
  if (!layer) throw new Error(`measurement_bus: unknown_layer ${measurement.layer_id}`);
  const [domain, coordinateSpace, units, valueShape] = layer;
  const event = {
    event_id: `${runId}:${measurement.layer_id}`,
    run_id: runId,
    frame_id: frameId,
    actor,
    domain,
    subject_ref: measurement.layer_id,
    timestamp,
    clock_domain: clockDomain,
    coordinate_space: coordinateSpace,
    units,
    value_shape: valueShape,
    value: measurement,
    uncertainty: { status: "estimated", reason: "demo_fixture_without_external_calibration" },
    provenance: {
      measurement_hash: measurement.measurement_hash,
      source: "demo/measurement-layers.mjs",
      generated_by: "deterministic-demo-fixture"
    },
    privacy: { raw_payload_required: false, exported_value_is_summary: true },
    severity: "info"
  };
  event.event_hash = hashStable(event);
  return event;
}

function demoInputs() {
  const pixels = Uint8Array.from(Array.from({ length: 64 }, (_, index) => (index * 37 + (index % 4) * 19) % 256));
  const samples = Float64Array.from({ length: 64 }, (_, index) => (
    Math.sin((2 * Math.PI * 5 * index) / 64) + 0.45 * Math.sin((2 * Math.PI * 11 * index) / 64)
  ));
  return {
    pixels,
    samples,
    temporalFrames: [
      Array.from(pixels),
      Array.from(pixels, (value, index) => (value + (index % 7) * 3) % 256),
      Array.from(pixels, (value, index) => (value + (index % 5) * 8) % 256)
    ],
    splats: [
      { x: -0.7, y: -0.4, z: 0, radius: 0.35, opacity: 0.72 },
      { x: 0.25, y: -0.2, z: 0.12, radius: 0.42, opacity: 0.64 },
      { x: 0.62, y: 0.5, z: -0.08, radius: 0.31, opacity: 0.86 },
      { x: -0.18, y: 0.68, z: 0.2, radius: 0.28, opacity: 0.78 }
    ],
    curveSamples: Array.from({ length: 9 }, (_, index) => ({
      x: index / 2,
      y: Math.sin(index / 2),
      z: Math.cos(index / 3) * 0.25
    })),
    interactionActions: [
      { actor: "human", kind: "seed", timestamp_ms: 0 },
      { actor: "model", kind: "proposal", timestamp_ms: 38 },
      { actor: "tool", kind: "render", timestamp_ms: 72 },
      { actor: "meter", kind: "measure", timestamp_ms: 89 },
      { actor: "human", kind: "select", timestamp_ms: 140 },
      { actor: "model", kind: "refine", timestamp_ms: 190 }
    ]
  };
}

export function demoMeasurements() {
  const input = demoInputs();
  const measurements = [
    measureHistogramField({ pixels: input.pixels, width: 8, height: 8, bins: 8 }),
    measureDitherField({ pixels: input.pixels, width: 8, height: 8, matrixSize: 4 }),
    measureSplatProbe({ splats: input.splats, viewport: { width: 4, height: 3 } }),
    measureClusterMeter({ grid: { columns: 4, rows: 3 }, lights: demoLights(), budget: { maxLightsPerCluster: 4 } }),
    measureAudioSpectrum({ samples: input.samples, bins: 32 }),
    measureTemporalFlicker({ frames: input.temporalFrames, width: 8, height: 8, threshold: 18 }),
    measureGeometryCurvature({ samples: input.curveSamples }),
    measureInteractionTrace({ actions: input.interactionActions }),
    measureUncertaintyBudget({ observations: demoObservations() }),
    measurePerformanceBudget({ frames: demoFrameBudget(), budget_ms: 16.7 })
  ];
  const packet = {
    schema: contract.schema,
    tool: contract.tool,
    generated_at: contract.generated_at,
    status: "MATCH",
    purpose: contract.purpose,
    measurement_bus: contract.measurement_bus,
    layers: contract.layers.map((layer) => layer.layer_id),
    measurements,
    events: measurements.map((measurement) => makeMeasurementEvent(measurement)),
    source_receipts: contract.source_receipts,
    privacy: contract.privacy,
    failure_codes: contract.failure_codes,
    next_actions: contract.next_actions
  };
  packet.receipt_hash = hashStable(packet);
  return packet;
}

function demoLights() {
  return [
    { x: 0.14, y: 0.16, radius: 0.22 },
    { x: 0.34, y: 0.2, radius: 0.25 },
    { x: 0.72, y: 0.7, radius: 0.3 },
    { x: 0.82, y: 0.42, radius: 0.18 }
  ];
}

function demoObservations() {
  return ["estimated", "witnessed", "calibrated", "unverifiable"]
    .map((status) => ({ uncertainty: { status } }));
}

function demoFrameBudget() {
  return [11.8, 15.6, 18.9, 13.4, 22.1, 12.3].map((frame_ms) => ({ frame_ms }));
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
  process.stdout.write(process.argv.includes("--summary") ? summary(packet) : `${JSON.stringify(packet, null, 2)}\n`);
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  main();
}
