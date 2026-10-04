// The five flagship heroes moved to the shared art direction on 4 October 2026:
// each repository now carries docs/art/hero-dark.svg and hero-light.svg, a social
// preview, marks and lockups, with a superstack.receipt/1 for every PNG in
// docs/art/receipts.json. tools/render_flagship_heroes.py stays as the record of
// the previous render. This check reads whichever sibling checkouts are present.
import assert from "node:assert/strict";
import { existsSync, readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const publicRoot = path.resolve(here, "..", "..");
const flagships = ["telos", "gather", "crucible", "index", "forum"];

let checked = 0;
for (const name of flagships) {
  const root = path.join(publicRoot, name);
  if (!existsSync(path.join(root, "README.md"))) continue;
  for (const rel of ["docs/art/hero-dark.svg", "docs/art/hero-light.svg", "docs/art/social.png", "docs/brand/mark-512.png"]) {
    assert.ok(existsSync(path.join(root, rel)), `${name}: ${rel} is missing`);
  }
  const book = JSON.parse(readFileSync(path.join(root, "docs/art/receipts.json"), "utf8"));
  const receipts = Object.values(book.receipts);
  assert.ok(receipts.length > 0, `${name}: no receipts`);
  for (const r of receipts) {
    assert.equal(r.schema, "superstack.receipt/1");
    assert.equal(r.seed, name);
    assert.ok(r.does_not_prove.length > 0);
  }
  const readme = readFileSync(path.join(root, "README.md"), "utf8");
  assert.match(readme, /docs\/art\/hero-(dark|light)\.svg/, `${name}: README does not show the hero`);
  checked += 1;
}
assert.ok(existsSync(path.join(here, "..", "docs/art/hero-dark.svg")), "telos hero is missing");
console.log(`checked ${checked} flagship checkout(s)`);
