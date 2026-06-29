import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { scanAccessibilitySurface } from "./accessibility-doctor.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));

const goodHtml = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Accessible Telos fixture</title>
<style>
a:focus-visible,button:focus-visible{outline:3px solid #111}
@media(max-width:840px){.grid{grid-template-columns:1fr}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{animation:none!important;transition:none!important}}
</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header aria-label="Project Telos navigation"><nav aria-label="Page sections"><a href="#main">Main</a></nav></header>
<main id="main">
<section aria-labelledby="title"><h1 id="title">Telos</h1></section>
<canvas role="img" aria-label="Receipt-backed rendering demo">Canvas fallback text.</canvas>
<button type="button" aria-pressed="false">Toggle</button>
<label for="density">Density <input id="density" type="range"></label>
<output aria-live="polite">Receipt ready</output>
<table><caption>Receipt table</caption><thead><tr><th scope="col">Tool</th></tr></thead><tbody><tr><th scope="row">telos</th></tr></tbody></table>
</main>
</body>
</html>`;

const badHtml = `<!doctype html>
<html>
<head>
<title>Bad fixture</title>
<style>.button:hover{transform:translateY(-1px)}</style>
</head>
<body>
<div class="nav"><a href="#x">X</a></div>
<canvas></canvas>
<button>Toggle</button>
<input id="density" type="range">
</body>
</html>`;

const tempRoot = mkdtempSync(path.join(tmpdir(), "telos-accessibility-doctor-"));
try {
  const goodPath = path.join(tempRoot, "good.html");
  const badPath = path.join(tempRoot, "bad.html");
  writeFileSync(goodPath, goodHtml, "utf8");
  writeFileSync(badPath, badHtml, "utf8");

  const match = scanAccessibilitySurface(goodPath, {
    generatedAt: "2026-06-29T00:00:00.000Z"
  });
  assert.equal(match.schema, "project-telos.accessibility-doctor/v1");
  assert.equal(match.tool, "telos.accessibility.doctor");
  assert.equal(match.generated_at, "2026-06-29T00:00:00.000Z");
  assert.equal(match.surface.kind, "html");
  assert.equal(match.surface.present, true);
  assert.match(match.surface.hash, /^sha256:[a-f0-9]{64}$/);
  assert.equal(match.aggregate.verdict, "MATCH");
  assert.deepEqual(match.aggregate.failure_codes, []);
  assert.equal(match.privacy_boundary.raw_html_included, false);
  assert.equal(match.privacy_boundary.absolute_paths_included, false);
  assert.equal(match.signals.reduced_motion_media, true);
  assert.equal(match.signals.focus_visible_style, true);
  assert.equal(match.signals.canvas_accessible_name, true);
  assert.equal(match.signals.canvas_fallback_text, true);
  assert.equal(match.signals.live_region, true);
  assert.equal(match.signals.form_controls_labeled, true);
  assert.equal(JSON.stringify(match).includes(tempRoot), false, "scanner must not leak absolute temp path");
  assert.equal(JSON.stringify(match).includes("Canvas fallback text"), false, "scanner must not include HTML body");

  const drift = scanAccessibilitySurface(badPath, {
    generatedAt: "2026-06-29T00:00:01.000Z"
  });
  assert.equal(drift.aggregate.verdict, "DRIFT");
  assert.deepEqual(drift.aggregate.failure_codes, [
    "html_lang_missing",
    "viewport_meta_missing",
    "skip_link_missing",
    "main_landmark_missing",
    "navigation_label_missing",
    "focus_visible_missing",
    "reduced_motion_missing",
    "responsive_media_missing",
    "canvas_accessible_name_missing",
    "canvas_fallback_missing",
    "button_type_missing",
    "interactive_state_missing",
    "form_label_missing",
    "live_region_missing"
  ]);

  const missing = scanAccessibilitySurface(path.join(tempRoot, "missing.html"), {
    generatedAt: "2026-06-29T00:00:02.000Z"
  });
  assert.equal(missing.aggregate.verdict, "UNVERIFIABLE");
  assert.deepEqual(missing.aggregate.failure_codes, ["html_surface_unjoinable"]);

  const cli = spawnSync(process.execPath, [
    path.join(here, "accessibility-doctor.mjs"),
    "--html",
    goodPath
  ], {
    cwd: path.resolve(here, ".."),
    encoding: "utf8"
  });
  assert.equal(cli.status, 0, cli.stderr || cli.stdout);
  assert.equal(JSON.parse(cli.stdout).aggregate.verdict, "MATCH");

  const summary = spawnSync(process.execPath, [
    path.join(here, "accessibility-doctor.mjs"),
    "--html",
    goodPath,
    "--summary"
  ], {
    cwd: path.resolve(here, ".."),
    encoding: "utf8"
  });
  assert.equal(summary.status, 0, summary.stderr || summary.stdout);
  assert.match(summary.stdout, /Telos Accessibility Doctor/);
  assert.match(summary.stdout, /checks\s+14/);
  assert.match(summary.stdout, /verdict\s+MATCH/);
} finally {
  rmSync(tempRoot, { recursive: true, force: true });
}
