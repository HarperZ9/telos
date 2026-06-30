import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

const html = readFileSync(new URL("./index.html", import.meta.url), "utf8");

function contrast(hexA, hexB) {
  function srgb(hex) {
    const n = Number.parseInt(hex.slice(1), 16);
    return [(n >> 16) & 255, (n >> 8) & 255, n & 255].map((value) => {
      const channel = value / 255;
      return channel <= 0.03928 ? channel / 12.92 : ((channel + 0.055) / 1.055) ** 2.4;
    });
  }
  function luminance(hex) {
    const [r, g, b] = srgb(hex);
    return 0.2126 * r + 0.7152 * g + 0.0722 * b;
  }
  const lighter = Math.max(luminance(hexA), luminance(hexB));
  const darker = Math.min(luminance(hexA), luminance(hexB));
  return (lighter + 0.05) / (darker + 0.05);
}

assert.match(html, /<a class="skip" href="#main">Skip to content<\/a>/);
assert.match(html, /<table class="matrix">/);
assert.match(html, /rel="icon" href="data:image\/svg\+xml/);
assert.match(html, /<caption>The room view summarizes/);
assert.match(html, /node demo\/room\.mjs --json/);
assert.match(html, /node demo\/flagship-workflow\.mjs/);
assert.match(html, /All five flagships expose native tools/);
assert.match(html, /@media\(prefers-reduced-motion:reduce\)/);
assert.match(html, /aria-label="Current room state is MATCH"/);
assert.match(html, /id="studio"/);
assert.match(html, /<canvas id="effect-canvas"/);
assert.match(html, /Your browser can still use the text controls and scene receipt/);
assert.match(html, /data-effect="all"/);
assert.match(html, /Scene receipt/);
assert.match(html, /<script src="effects-engine\.js"><\/script>/);
assert.match(html, /id="effect-intensity"/);
assert.match(html, /id="effect-density"/);
assert.match(html, /id="effect-freeze"/);
assert.match(html, /\.studio-grid\{[^}]*align-items:start/);
assert.match(html, /\.effect-list\{[^}]*max-height:18rem/);
assert.match(html, /id="effect-protocol-output"/);
assert.match(html, /renderer=canvas2d-receipt-renderer/);
assert.match(html, /fallback_chain=canvas2d-receipt-renderer&gt;static-artifact-receipt/);
assert.match(html, /Renderer path/);
assert.match(html, /node demo\/rendering-capabilities\.mjs --summary/);
assert.match(html, /id="effect-copy-receipt"/);
assert.match(html, /id="effect-export-scene"/);
assert.match(html, /id="effect-replay-scene"/);
assert.match(html, /data-preset="scientific"/);
assert.match(html, /data-preset="radiance"/);
assert.match(html, /data-preset="flagship"/);
assert.match(html, /id="engine"/);
assert.match(html, /Telos Creative Engine modules/);
assert.match(html, /node demo\/creative-engine\.mjs/);
assert.match(html, /audio-reactive visual layers/);
assert.match(html, /Gaussian splat fields/);
assert.match(html, /sensors, measurement overlays/);
assert.match(html, /mathematicians, physicists, and educators/);
assert.match(html, /id="flagships"/);
assert.match(html, /Flagship poster wall/);
assert.match(html, /data-art="gather"/);
assert.match(html, /data-art="crucible"/);
assert.match(html, /<script src="effects-protocol\.js"><\/script>/);

for (const effect of [
  "Retro CGI",
  "Glitch",
  "Generative",
  "Plotter",
  "Pixel sort",
  "Poster",
  "Fractal",
  "Gaussian splat",
  "Clustered lights",
  "CRT scanlines",
  "Chromatic split",
  "Dither",
  "Contour map",
  "Voronoi cells",
  "ASCII raster",
  "Vector field",
  "Feedback trails"
]) {
  assert.match(html, new RegExp(effect));
}

for (const tool of ["gather", "crucible", "index", "forum", "telos"]) {
  assert.match(html, new RegExp(`<th scope="row">${tool}</th>`));
}

assert.equal(/background-clip:\s*text/.test(html), false);
assert.equal(/repeating-linear-gradient/.test(html), false);
assert.ok(contrast("#0b0c0e", "#f4f3ef") >= 4.5);
assert.ok(contrast("#4c515a", "#f4f3ef") >= 4.5);
