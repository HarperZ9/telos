import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { spawnSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const manifest = JSON.parse(readFileSync(new URL("./integrations/creative-engine-manifest.json", import.meta.url), "utf8"));

assert.equal(manifest.schema, "project-telos.creative-engine/v1");
assert.equal(manifest.tool, "telos.creative.engine");
assert.equal(manifest.contract.protocol_agnostic, true);
assert.equal(manifest.contract.receipts_required, true);
assert.equal(manifest.contract.raw_assets_required_for_interop, false);
assert.equal(manifest.research_receipts.math_educator_video_leads, "demo/research/youtube-math-educator-receipts.json");
assert.equal(manifest.research_receipts.rendering_pipeline, "demo/research/rendering-pipeline-seeds.json");
assert.ok(manifest.research_receipts.creative_kernel_sources.includes("https://arxiv.org/abs/2402.16447"));
assert.match(manifest.research_receipts.mission, /mathematicians/);
assert.ok(manifest.research_receipts.representative_leads.includes("https://www.youtube.com/@InigoQuilez"));

for (const domain of [
  "generative_art",
  "retro_cgi",
  "raster_fx",
  "sound",
  "film_media",
  "typography",
  "math_physics",
  "node_graph",
  "verification"
]) {
  assert.ok(manifest.domains.some((item) => item.id === domain), `missing domain ${domain}`);
}

for (const technique of [
  "dither.ordered-bayer",
  "pixel-sort.luminance-runs",
  "halftone.press-screen",
  "audio.additive-web-audio",
  "font.generative-glyph-lab",
  "touchdesigner.node-graph-compatible",
  "physics.particle-field",
  "cgi.clustered-forward-lighting",
  "renderer.capability-probe",
  "sensor.measurement-layers",
  "kernel.deterministic-creative-core"
]) {
  assert.ok(manifest.techniques.some((item) => item.id === technique), `missing technique ${technique}`);
}

for (const library of [
  "raster_print_core",
  "cgi_render_core",
  "math_physics_core",
  "sound_media_core",
  "typography_design_core"
]) {
  assert.ok(manifest.effect_libraries.some((item) => item.id === library), `missing effect library ${library}`);
}
assert.ok(
  manifest.effect_libraries
    .find((item) => item.id === "raster_print_core")
    .next.includes("void-and-cluster matrix generator")
);
assert.ok(
  manifest.live_modules.some((item) => item.path === "demo/creative-kernels.mjs"),
  "missing creative kernels live module"
);

assert.equal(manifest.rendering_capabilities.tool, "telos.rendering.capabilities");
assert.equal(manifest.rendering_capabilities.contract, "project-telos.rendering-capabilities/v1");
assert.ok(manifest.rendering_capabilities.profiles.includes("webgpu-splat-clustered"));
assert.match(manifest.rendering_capabilities.boundary, /separate from verification/);

assert.equal(manifest.measurement_layers.tool, "telos.measurement.layers");
assert.equal(manifest.measurement_layers.contract, "project-telos.measurement-layers/v1");
assert.ok(manifest.measurement_layers.layers.includes("visual.dither-spectrum-meter"));
assert.match(manifest.measurement_layers.boundary, /Crucible still owns verdicts/);

assert.equal(manifest.sensor_measurement_layers.length, 5);
for (const sensor of [
  "visual.histogram-field",
  "visual.dither-spectrum-meter",
  "spatial.splat-probe",
  "lighting.cluster-meter",
  "audio.spectral-meter"
]) {
  assert.ok(manifest.sensor_measurement_layers.some((item) => item.id === sensor), `missing sensor ${sensor}`);
}
assert.ok(
  manifest.sensor_measurement_layers
    .find((item) => item.id === "lighting.cluster-meter")
    .outputs.includes("overlay legibility verdict")
);

for (const revived of [
  "demo/render-nd",
  "demo/render-sound",
  "demo/sense-core",
  "demo/viable-viz",
  "../studio-engine/studio_engine/organs/raster.py",
  "../studio-engine/studio_engine/organs/sonify.py",
  "../studio-engine/studio_engine/organs/flowfield.py",
  "../studio-engine/studio_engine/organs/harmonograph.py",
  "../studio-engine/studio_engine/strand/webaudio.py",
  "../studio-engine/showcase/media.js",
  "../studio-libs/render-sound/index.mjs"
]) {
  assert.ok(manifest.revival_candidates.some((item) => item.path === revived), `missing revival candidate ${revived}`);
}

const cli = spawnSync(process.execPath, [path.join(here, "creative-engine.mjs")], {
  cwd: path.resolve(here, ".."),
  encoding: "utf8"
});
assert.equal(cli.status, 0, cli.stderr || cli.stdout);
assert.deepEqual(JSON.parse(cli.stdout), manifest);

const summary = spawnSync(process.execPath, [path.join(here, "creative-engine.mjs"), "--summary"], {
  cwd: path.resolve(here, ".."),
  encoding: "utf8"
});
assert.equal(summary.status, 0, summary.stderr || summary.stdout);
assert.match(summary.stdout, /Telos Creative Engine/);
assert.match(summary.stdout, /domains\s+9/);
assert.match(summary.stdout, /techniques\s+11/);
assert.match(summary.stdout, /revival\s+11/);
