import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(here, "..");

const result = spawnSync(
  "python",
  [path.join(repo, "tools", "check_repo_art.py"), "--json"],
  { cwd: repo, encoding: "utf8" }
);

assert.equal(result.status, 0, result.stderr || result.stdout);

const receipt = JSON.parse(result.stdout);
assert.equal(receipt.schema, "project-telos.repo-art/v1");
assert.equal(receipt.mode, "check");
assert.equal(receipt.passed, true);

// Name the gates rather than counting them, so a check that quietly disappears
// from the registry fails here instead of passing as a smaller green run.
const REQUIRED = [
  "spec.present",
  "art.matches_spec",
  "art.render_is_deterministic",
  "art.identity_per_repository",
  "art.seed_is_recorded",
  "art.no_local_paths_or_em_dashes",
  "art.spec_words_reach_the_drawing",
  "art.note_survives_the_wrapper",
  "art.return_edge_stays_on_its_row",
  "art.every_illustration_is_shown",
  "art.tagline_stays_inside_its_rule",
  "art.outcome_fits_its_box"
];
const byName = new Map(receipt.checks.map((check) => [check.name, check]));
for (const name of REQUIRED) {
  const check = byName.get(name);
  assert.ok(check, `gate ${name} is missing from the receipt`);
  assert.equal(check.passed, true, `${name}: ${check.failures.join("; ")}`);
  assert.deepEqual(check.failures, [], name);
}

assert.deepEqual(receipt.specs, ["docs/art/telos.art.json"]);

const files = receipt.outputs.map((output) => output.file);
assert.deepEqual(files, ["docs/art/proof-lane.svg", "docs/art/telos-header.svg"]);
for (const output of receipt.outputs) {
  assert.match(output.sha256, /^[a-f0-9]{64}$/, output.file);
  assert.ok(output.bytes > 0, `${output.file} is empty`);
  assert.equal(output.spec, "docs/art/telos.art.json");
}

// A gate that cannot fail is not a gate. Point the outcome-box check at a
// throwaway spec whose note is far too wide for its box, and it must say so.
const canFail = spawnSync(
  "python",
  [
    "-c",
    [
      "import sys, json, tempfile, pathlib",
      "sys.path.insert(0, 'tools')",
      "import check_repo_art as gate",
      "d = pathlib.Path(tempfile.mkdtemp())",
      "box = {'label': 'L', 'note': 'ok', 'tone': 'none'}",
      "wide = {'label': 'L', 'note': 'n' * 80, 'tone': 'none'}",
      "spec = {'header': {'name': 'x', 'role': 'x', 'tagline': 'y', 'words': []},",
      "        'flows': [{'outcomes': [wide, box, box]}]}",
      "(d / 'bad.art.json').write_text(json.dumps(spec), encoding='utf-8')",
      "gate.ART = d",
      "print(len(gate.check_outcome_fits_its_box([])))"
    ].join("\n")
  ],
  { cwd: repo, encoding: "utf8" }
);
assert.equal(canFail.status, 0, canFail.stderr || canFail.stdout);
assert.equal(Number(canFail.stdout.trim()), 1, "the outcome-box gate cannot fail");

console.log(`repo-art: ${REQUIRED.length} gates, ${receipt.outputs.length} files`);
