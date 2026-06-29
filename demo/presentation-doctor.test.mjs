import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { scanPresentationSurfaces } from "./presentation-doctor.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));

function writeRepo(root, id, options = {}) {
  const repo = path.join(root, id);
  const brand = path.join(repo, "docs", "brand");
  mkdirSync(brand, { recursive: true });
  if (options.readme !== false) {
    writeFileSync(path.join(repo, "README.md"), options.readme ?? `
<p align="center">
  <img src="docs/brand/${id}-hero.png" alt="${id}, a Project Telos flagship">
</p>
<!-- Project mark: docs/brand/${id}-mark.svg -->

# ${id}

[Project Telos](https://harperz9.github.io) | [gather](https://github.com/HarperZ9/gather) | [crucible](https://github.com/HarperZ9/crucible) | [index](https://github.com/HarperZ9/index) | [forum](https://github.com/HarperZ9/forum) | [telos](https://github.com/HarperZ9/telos)

[![CI](https://github.com/HarperZ9/${id}/actions/workflows/ci.yml/badge.svg)](https://github.com/HarperZ9/${id}/actions/workflows/ci.yml)
![version: 1.0](https://img.shields.io/badge/version-1.0-informational.svg)
![license: fair-source](https://img.shields.io/badge/license-fair--source-blue.svg)

- **Operator surface:** \`${id} status --json\`, \`${id} doctor --json\`, and \`${id} mcp\` expose CLI and MCP surfaces.
- **Current floor:** source checkout with Project Telos action receipts.
`, "utf8");
  }
  if (options.changelog !== false) {
    writeFileSync(path.join(repo, "CHANGELOG.md"), options.changelog ?? `
# Changelog

## Unreleased

- Presentation and operator-surface housekeeping for Project Telos parity.
- Operator surface: README, status payload, and MCP catalog stay aligned.
`, "utf8");
  }
  for (const name of [`${id}-hero.png`, `${id}-hero.svg`, `${id}-mark.svg`, "README.md"]) {
    if (!(options.missingBrand ?? []).includes(name)) {
      writeFileSync(path.join(brand, name), `fixture ${name}`, "utf8");
    }
  }
}

const tempRoot = mkdtempSync(path.join(tmpdir(), "telos-presentation-doctor-"));
try {
  writeRepo(tempRoot, "gather");
  writeRepo(tempRoot, "telos");

  const match = scanPresentationSurfaces(tempRoot, {
    flagships: ["gather", "telos"],
    generatedAt: "2026-06-29T00:00:00.000Z"
  });
  assert.equal(match.schema, "project-telos.presentation-doctor/v1");
  assert.equal(match.tool, "telos.presentation.doctor");
  assert.equal(match.generated_at, "2026-06-29T00:00:00.000Z");
  assert.equal(match.aggregate.flagship_count, 2);
  assert.equal(match.aggregate.readme_count, 2);
  assert.equal(match.aggregate.changelog_count, 2);
  assert.equal(match.aggregate.brand_asset_count, 8);
  assert.equal(match.aggregate.verdict, "MATCH");
  assert.deepEqual(match.aggregate.failure_codes, []);
  assert.equal(match.privacy_boundary.absolute_paths_included, false);
  assert.equal(match.privacy_boundary.raw_document_bodies_included, false);
  assert.equal(match.privacy_boundary.private_paths_included, false);

  const gather = match.flagships.find((flagship) => flagship.id === "gather");
  assert.equal(gather.presentation.verdict, "MATCH");
  assert.match(gather.files.readme.hash, /^sha256:[a-f0-9]{64}$/);
  assert.equal(gather.files.readme.signals.hero_image, true);
  assert.equal(gather.files.readme.signals.project_telos_nav, true);
  assert.equal(gather.files.readme.signals.operator_surface, true);
  assert.equal(gather.files.changelog.signals.unreleased_section, true);
  assert.equal(gather.files.brand.assets.length, 4);

  const serialized = JSON.stringify(match);
  assert.equal(serialized.includes(tempRoot), false, "scanner must not leak absolute temp root");
  assert.equal(serialized.includes("Operator surface:"), false, "scanner must not include README body");

  writeRepo(tempRoot, "crucible", {
    readme: "# Crucible\n\nNo shared product surface yet.\n",
    changelog: "# Changelog\n\nNo unreleased notes.\n",
    missingBrand: ["crucible-hero.png", "crucible-mark.svg"]
  });

  const negative = scanPresentationSurfaces(tempRoot, {
    flagships: ["crucible", "missing-repo"],
    generatedAt: "2026-06-29T00:00:01.000Z"
  });
  assert.equal(negative.aggregate.verdict, "DRIFT");
  assert.deepEqual(negative.aggregate.failure_codes, [
    "project_telos_nav_missing",
    "readme_hero_missing",
    "ci_badge_missing",
    "version_badge_missing",
    "license_badge_missing",
    "operator_surface_missing",
    "current_status_missing",
    "cli_mcp_terms_missing",
    "changelog_freshness_missing",
    "brand_artifact_missing",
    "flagship_repo_unjoinable"
  ]);

  const byFlagship = new Map(negative.flagships.map((flagship) => [flagship.id, flagship]));
  assert.equal(byFlagship.get("crucible").presentation.verdict, "DRIFT");
  assert.ok(byFlagship.get("crucible").presentation.failure_codes.includes("brand_artifact_missing"));
  assert.equal(byFlagship.get("missing-repo").presentation.verdict, "UNVERIFIABLE");
  assert.deepEqual(byFlagship.get("missing-repo").presentation.failure_codes, [
    "flagship_repo_unjoinable"
  ]);

  const cli = spawnSync(process.execPath, [
    path.join(here, "presentation-doctor.mjs"),
    "--scan-root",
    tempRoot,
    "--flagships",
    "gather,telos"
  ], {
    cwd: path.resolve(here, ".."),
    encoding: "utf8"
  });
  assert.equal(cli.status, 0, cli.stderr || cli.stdout);
  assert.equal(JSON.parse(cli.stdout).aggregate.verdict, "MATCH");

  const summary = spawnSync(process.execPath, [
    path.join(here, "presentation-doctor.mjs"),
    "--scan-root",
    tempRoot,
    "--flagships",
    "gather,telos",
    "--summary"
  ], {
    cwd: path.resolve(here, ".."),
    encoding: "utf8"
  });
  assert.equal(summary.status, 0, summary.stderr || summary.stdout);
  assert.match(summary.stdout, /Telos Presentation Doctor/);
  assert.match(summary.stdout, /flagships\s+2/);
  assert.match(summary.stdout, /brand assets\s+8/);
  assert.match(summary.stdout, /verdict\s+MATCH/);

  // A configurable nav roster lets a sixth flagship (or any uplift target) be graded
  // against its own Project Telos family instead of the hardcoded original five.
  writeRepo(tempRoot, "quantalang", {
    readme: `
<p align="center"><img src="docs/brand/quantalang-hero.png" alt="quantalang, a Project Telos flagship"></p>

# quantalang

[Project Telos](https://harperz9.github.io) | [telos](https://github.com/HarperZ9/telos) | [quantalang](https://github.com/HarperZ9/quantalang)

[![CI](https://github.com/HarperZ9/quantalang/actions/workflows/ci.yml/badge.svg)](https://github.com/HarperZ9/quantalang/actions/workflows/ci.yml)
![version: 1.0](https://img.shields.io/badge/version-1.0-informational.svg)
![license: fair-source](https://img.shields.io/badge/license-fair--source-blue.svg)

- **Operator surface:** \`quantalang status --json\` and \`quantalang mcp\` expose CLI and MCP surfaces.
- **Current floor:** source checkout with Project Telos action receipts.
`
  });

  const customRoster = scanPresentationSurfaces(tempRoot, {
    flagships: ["quantalang"],
    navRoster: ["telos", "quantalang"],
    generatedAt: "2026-06-29T00:00:02.000Z"
  });
  const qCustom = customRoster.flagships.find((flagship) => flagship.id === "quantalang");
  assert.equal(
    qCustom.files.readme.signals.project_telos_nav,
    true,
    "custom navRoster should satisfy project_telos_nav when the README links the rostered repos"
  );
  assert.equal(
    qCustom.presentation.verdict,
    "MATCH",
    "quantalang fixture graded against its own roster should reach MATCH"
  );

  const defaultRoster = scanPresentationSurfaces(tempRoot, {
    flagships: ["quantalang"],
    generatedAt: "2026-06-29T00:00:03.000Z"
  });
  const qDefault = defaultRoster.flagships.find((flagship) => flagship.id === "quantalang");
  assert.equal(
    qDefault.files.readme.signals.project_telos_nav,
    false,
    "default roster still requires the original five flagship links (behavior preserved)"
  );

  const rosterCli = spawnSync(process.execPath, [
    path.join(here, "presentation-doctor.mjs"),
    "--scan-root",
    tempRoot,
    "--flagships",
    "quantalang",
    "--nav-roster",
    "telos,quantalang"
  ], {
    cwd: path.resolve(here, ".."),
    encoding: "utf8"
  });
  assert.equal(rosterCli.status, 0, rosterCli.stderr || rosterCli.stdout);
  assert.equal(JSON.parse(rosterCli.stdout).aggregate.verdict, "MATCH");

  // An umbrella tool (under the operator's umbrella but not Telos-bound) is graded
  // against its own nav label and surface terms, so a standalone compiler need not
  // claim Project Telos or expose an MCP server it does not have.
  writeRepo(tempRoot, "quantac", {
    readme: `
<p align="center"><img src="docs/brand/quantac-hero.png" alt="QuantaLang, the Effects Language"></p>

# quantac

[Quanta ecosystem](https://github.com/HarperZ9/quanta-universe) | [quantalang](https://github.com/HarperZ9/quantalang) | [quanta-universe](https://github.com/HarperZ9/quanta-universe)

[![CI](https://github.com/HarperZ9/quantac/actions/workflows/ci.yml/badge.svg)](https://github.com/HarperZ9/quantac/actions/workflows/ci.yml)
![version: 1.0](https://img.shields.io/badge/version-1.0-informational.svg)
![license: fair-source](https://img.shields.io/badge/license-fair--source-blue.svg)

- **Operator surface:** the \`quantac\` CLI builds .quanta to C, with a bundled LSP server for editors.
- **Current status:** source checkout, C backend production-grade.
`,
    changelog: `
# Changelog

## Unreleased

- Presentation pass: hero, brand assets, and Quanta ecosystem navigation.
- Operator surface documented across the CLI and the bundled LSP server.
`
  });

  const umbrella = scanPresentationSurfaces(tempRoot, {
    flagships: ["quantac"],
    navLabel: "Quanta ecosystem",
    navRoster: ["quantalang", "quanta-universe"],
    surfaceTerms: ["CLI", "LSP"],
    generatedAt: "2026-06-29T00:00:04.000Z"
  });
  const quantac = umbrella.flagships.find((flagship) => flagship.id === "quantac");
  assert.equal(
    quantac.files.readme.signals.project_telos_nav,
    true,
    "a custom nav label should anchor the family nav for an umbrella tool"
  );
  assert.equal(
    quantac.files.readme.signals.cli_mcp_terms,
    true,
    "custom surface terms (CLI + LSP) should satisfy the surface signal without requiring MCP"
  );
  assert.equal(
    quantac.presentation.verdict,
    "MATCH",
    "umbrella tool graded against its own label and terms should reach MATCH"
  );

  const umbrellaCli = spawnSync(process.execPath, [
    path.join(here, "presentation-doctor.mjs"),
    "--scan-root", tempRoot,
    "--flagships", "quantac",
    "--nav-label", "Quanta ecosystem",
    "--nav-roster", "quantalang,quanta-universe",
    "--surface-terms", "CLI,LSP"
  ], { cwd: path.resolve(here, ".."), encoding: "utf8" });
  assert.equal(umbrellaCli.status, 0, umbrellaCli.stderr || umbrellaCli.stdout);
  assert.equal(JSON.parse(umbrellaCli.stdout).aggregate.verdict, "MATCH");
} finally {
  rmSync(tempRoot, { recursive: true, force: true });
}
