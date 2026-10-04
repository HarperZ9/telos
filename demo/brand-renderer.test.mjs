// Telos's README art, checked against its own receipts.
//
// Until 4 October 2026 this test re-checked the five flagship hero PNGs in the
// sibling checkouts. CI checks each sibling out at the release its manifest pins
// (demo/integrations/mcp-server-manifest.json), and README art is a docs change
// that lands on a sibling's main between releases, so a cross-repository art
// check here tested a combination that never ships together. Each sibling now
// tests its own art. This test holds Telos's: every file exists, every PNG
// matches the hash its receipt records, and every receipt names the Telos seed
// and says what it does not prove.
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { existsSync, readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const repo = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const art = path.join(repo, "docs", "art");
const sha256 = (file) => createHash("sha256").update(readFileSync(file)).digest("hex");

for (const rel of ["docs/art/hero-dark.svg", "docs/art/hero-light.svg", "docs/art/social.png",
  "docs/brand/mark-16.png", "docs/brand/mark-32.png", "docs/brand/mark-512.png", "docs/brand/mark-tile.svg"]) {
  assert.ok(existsSync(path.join(repo, rel)), `${rel} is missing`);
}

const book = JSON.parse(readFileSync(path.join(art, "receipts.json"), "utf8"));
assert.equal(book.schema, "harperz9.repo-art.receipts/1");
const entries = Object.entries(book.receipts);
assert.ok(entries.length >= 10, `expected a receipt per rendered PNG, found ${entries.length}`);

const shipped = {
  "social-dark.png": "docs/art/social.png",
  "mark-micro-tile-16.png": "docs/brand/mark-16.png",
  "mark-micro-tile-32.png": "docs/brand/mark-32.png",
  "mark-full-tile-64.png": "docs/brand/mark-64.png",
  "mark-full-tile-512.png": "docs/brand/mark-512.png",
};
let matched = 0;
for (const [name, receipt] of entries) {
  assert.equal(receipt.schema, "superstack.receipt/1", name);
  assert.equal(receipt.seed, "telos", `${name}: seed`);
  assert.equal(receipt.seed_rule, "xmur3-mulberry32/1", `${name}: seed rule`);
  assert.match(receipt.content_sha256, /^[0-9a-f]{64}$/, `${name}: content hash`);
  assert.ok(receipt.does_not_prove.length > 0, `${name}: does_not_prove`);
  if (shipped[name]) {
    assert.equal(sha256(path.join(repo, shipped[name])), receipt.outputs[name],
      `${shipped[name]} does not match the PNG its receipt records`);
    matched += 1;
  }
}
assert.equal(matched, Object.keys(shipped).length, "every shipped PNG has a receipt");

const readme = readFileSync(path.join(repo, "README.md"), "utf8");
assert.match(readme, /<source media="\(prefers-color-scheme: dark\)" srcset="docs\/art\/hero-dark\.svg">/);
assert.match(readme, /<img src="docs\/art\/hero-light\.svg" alt="telos: [^"]{40,}"/);
for (const svg of ["hero-dark.svg", "hero-light.svg"]) {
  const text = readFileSync(path.join(art, svg), "utf8");
  assert.match(text, /<title>[^<]+<\/title><desc>[^<]+<\/desc>/, `${svg}: title and description`);
  assert.doesNotMatch(text, /font-family/, `${svg}: text must be outlined, not set in a font`);
}
console.log(`telos art: ${entries.length} receipts, ${matched} shipped PNGs matched`);
