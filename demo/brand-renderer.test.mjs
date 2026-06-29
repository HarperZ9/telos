import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(here, "..");
const publicRoot = path.resolve(repo, "..");

const result = spawnSync(
  "python",
  [
    path.join(repo, "tools", "render_flagship_heroes.py"),
    "--check-existing",
    "--public-root",
    publicRoot,
    "--json"
  ],
  { cwd: repo, encoding: "utf8" }
);

assert.equal(result.status, 0, result.stderr || result.stdout);

const receipt = JSON.parse(result.stdout);
assert.equal(receipt.schema, "project-telos.brand-render/v2");
assert.equal(receipt.mode, "check-existing");
assert.equal(receipt.source_contract, "telos.rendering.research");
assert.equal(receipt.dimensions.width, 1600);
assert.equal(receipt.dimensions.height, 640);
assert.equal(receipt.outputs.length, 5);
assert.equal(receipt.font_inputs.every((font) => font.committed === false), true);
assert.match(receipt.provenance_boundary, /font files remain local/);
assert.ok(receipt.design_gates.includes("three-second headline and product-role read"));
assert.ok(receipt.design_gates.includes("solid text field with no high-frequency texture under copy"));
assert.ok(receipt.design_gates.includes("contained engine viewport for procedural rendering material"));

const byTool = new Map(receipt.outputs.map((output) => [output.tool, output]));
for (const tool of ["gather", "crucible", "index", "forum", "telos"]) {
  const output = byTool.get(tool);
  assert.equal(output.width, 1600, `${tool} hero width`);
  assert.equal(output.height, 640, `${tool} hero height`);
  assert.match(output.sha256, /^[a-f0-9]{64}$/);
  assert.ok(output.image.endsWith(`${tool}-hero.png`));
  assert.ok(output.readme.endsWith("README.md"));
}
