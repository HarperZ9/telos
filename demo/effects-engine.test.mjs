import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

const html = readFileSync(new URL("./index.html", import.meta.url), "utf8");
const engine = readFileSync(new URL("./effects-engine.js", import.meta.url), "utf8");

const layers = [
  ["retro", "Retro CGI"],
  ["glitch", "Glitch"],
  ["generative", "Generative"],
  ["plotter", "Plotter"],
  ["pixelsort", "Pixel sort"],
  ["poster", "Poster"],
  ["fractal", "Fractal"],
  ["splat", "Gaussian splat"],
  ["clustered", "Clustered lights"],
  ["crt", "CRT scanlines"],
  ["chromatic", "Chromatic split"],
  ["dither", "Dither"],
  ["contour", "Contour map"],
  ["voronoi", "Voronoi cells"],
  ["ascii", "ASCII raster"],
  ["vector", "Vector field"],
  ["feedback", "Feedback trails"]
];

assert.match(engine, /window\.TelosEffects = TelosEffects/);
assert.match(engine, /project-telos\.effects-engine\/v1/);
assert.match(html, /<script src="effects-engine\.js"><\/script>/);
assert.equal(/<script>\s*\(\(\) =>/.test(html), false, "engine should not be inlined in HTML");

for (const [id, label] of layers) {
  assert.match(engine, new RegExp(`id: "${id}"`), `engine missing ${id}`);
  assert.match(engine, new RegExp(`name: "${label}"`), `engine missing ${label}`);
  assert.match(html, new RegExp(`data-effect="${id}"`), `HTML missing button for ${id}`);
  assert.match(html, new RegExp(label), `HTML missing visible label ${label}`);
}

for (const id of ["effect-intensity", "effect-density", "effect-freeze", "effect-step", "effect-reroll"]) {
  assert.match(html, new RegExp(`id="${id}"`), `missing control ${id}`);
  assert.match(engine, new RegExp(id), `engine does not bind ${id}`);
}

for (const required of [
  "makeRng",
  "drawRetroCgi",
  "drawGenerative",
  "drawPlotter",
  "drawFractal",
  "drawSplat",
  "drawClustered",
  "drawCrt",
  "drawDither",
  "drawContour",
  "drawVoronoi",
  "drawAscii",
  "drawVectorField",
  "drawFeedback",
  "applyGlitch",
  "applyChromaticSplit",
  "applyPixelSort",
  "requestAnimationFrame",
  "matchMedia(\"(prefers-reduced-motion: reduce)\")"
]) {
  assert.match(engine, new RegExp(required.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")), `missing ${required}`);
}

for (const receiptField of [
  "mode=",
  "seed=",
  "layers=",
  "intensity=",
  "density=",
  "frame=",
  "status=MATCH",
  "fallback=canvas+text",
  "reduced_motion="
]) {
  assert.match(engine, new RegExp(receiptField.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")), `receipt missing ${receiptField}`);
}

assert.equal(/import\s/.test(engine), false, "engine should stay dependency-free for file:// demo use");
assert.equal(/fetch\(/.test(engine), false, "engine should not require network data");