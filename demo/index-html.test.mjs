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
assert.match(html, /<caption>The room view summarizes/);
assert.match(html, /node demo\/room\.mjs --json/);
assert.match(html, /node demo\/flagship-workflow\.mjs/);
assert.match(html, /All five flagships expose native tools/);
assert.match(html, /@media\(prefers-reduced-motion:reduce\)/);
assert.match(html, /aria-label="Current room state is MATCH"/);

for (const tool of ["Gather", "Crucible", "Index", "Forum", "Telos"]) {
  assert.match(html, new RegExp(`<th scope="row">${tool}</th>`));
}

assert.equal(/background-clip:\s*text/.test(html), false);
assert.equal(/repeating-linear-gradient/.test(html), false);
assert.ok(contrast("#0b0c0e", "#f4f3ef") >= 4.5);
assert.ok(contrast("#4c515a", "#f4f3ef") >= 4.5);
