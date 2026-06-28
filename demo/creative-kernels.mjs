import { fileURLToPath } from "node:url";

export { bayerMatrix, orderedDither, pixelSortRows } from "./creative-kernel-raster.mjs";
export { clusterLightBins, harmonographPath } from "./creative-kernel-geometry.mjs";
export { stableReceiptHash } from "./creative-kernel-utils.mjs";

const GENERATED_AT = "2026-06-28T00:00:00.000Z";

export function buildCreativeKernelPacket() {
  return {
    schema: "project-telos.creative-kernels/v1",
    tool: "telos.creative.kernels",
    generated_at: GENERATED_AT,
    status: "MATCH",
    purpose: "Deterministic creative kernels for Telos effects, sensors, and host-neutral engine work.",
    kernels: [
      kernel("raster.ordered-dither", "orderedDither", "visual.dither-spectrum-meter"),
      kernel("raster.pixel-sort-rows", "pixelSortRows", "visual.pixel-sort-meter"),
      kernel("plotter.harmonograph-path", "harmonographPath", "plotter.harmonograph-path"),
      kernel("lighting.cluster-light-bins", "clusterLightBins", "lighting.cluster-meter")
    ],
    source_receipts: [
      {
        title: "Project Telos creative kernels",
        url: "demo/creative-kernels.mjs",
        source_kind: "local-source",
        provenance_class: "lawful_source",
        receipt_hash: "sha256:7d96f11e87f176a18d671a6b0d78fe8107b91bf9fca96a089da97849dcfb95bd"
      },
      {
        title: "Void-and-cluster method for dither array generation",
        url: "https://doi.org/10.1117/12.59015",
        source_kind: "publication-record",
        provenance_class: "lawful_source",
        receipt_hash: "sha256:2977c8a06de0ee51f56ec8e7c4e0a07ba9df1fb0a3ca27622fd6700e3c8027ae"
      },
      {
        title: "Clustered Deferred and Forward Shading",
        url: "https://diglib.eg.org/items/6342d4d6-5220-4376-a5c6-a153058f4a3c",
        source_kind: "open-publication-record",
        provenance_class: "lawful_source",
        receipt_hash: "sha256:88df9920005119dda0876d67b563c57a7b90b5d238c1ada8ca187f2a5494e1a4"
      }
    ],
    privacy: {
      raw_assets_required_for_interop: false,
      exported_fields: ["kernel", "measurement", "receipt_hash", "bounds", "runs", "bins"]
    },
    next_actions: ["wire-browser-effects-engine", "add-blue-noise-kernel", "add-audio-reactive-kernel"]
  };
}

function kernel(id, fn, measurementLayer) {
  return {
    id,
    function: fn,
    measurement_layer: measurementLayer,
    source: "demo/creative-kernels.mjs"
  };
}

export function summary(packet = buildCreativeKernelPacket()) {
  const lines = [
    "Telos Creative Kernels",
    `schema  ${packet.schema}`,
    `tool    ${packet.tool}`,
    `kernels ${packet.kernels.length}`,
    `status  ${packet.status}`,
    "next    node demo/creative-kernels.mjs"
  ];
  return `${lines.join("\n")}\n`;
}

function main() {
  if (process.argv.includes("--summary")) {
    process.stdout.write(summary());
  } else {
    process.stdout.write(`${JSON.stringify(buildCreativeKernelPacket(), null, 2)}\n`);
  }
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  main();
}
