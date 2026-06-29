import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { scanPerformanceSurface } from "./performance-doctor.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));

const goodHtml = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Fast Telos fixture</title>
<style>
@font-face{font-family:Telos;src:url("https://harperz9.github.io/system/fonts/telos.woff2") format("woff2");font-display:swap}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
main{display:grid}
</style>
</head>
<body>
<main>
<canvas width="960" height="540">Fallback.</canvas>
<img src="hero.png" width="1200" height="630" loading="lazy" alt="Hero">
<video controls width="640" height="360"></video>
</main>
<script src="effects-protocol.js"></script>
<script src="effects-engine.js"></script>
</body>
</html>`;

const oversizedStyle = "x".repeat(65000);
const badHtml = `<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Slow fixture</title>
<link rel="stylesheet" href="https://cdn.example.test/slow.css">
<style>
@font-face{font-family:A;src:url("https://cdn.example.test/a.woff2")}
@font-face{font-family:B;src:url("https://fonts.example.test/b.woff2")}
@font-face{font-family:C;src:url("https://fonts.example.test/c.woff2")}
${oversizedStyle}
</style>
<script src="https://cdn.example.test/app.js"></script>
<script src="one.js"></script>
<script src="two.js"></script>
<script src="three.js"></script>
<script src="four.js"></script>
<script src="five.js"></script>
</head>
<body>
<main>
<canvas></canvas>
<img src="hero.png" alt="Hero">
<video autoplay src="film.mp4"></video>
<button onclick="run()">Run</button>
</main>
</body>
</html>`;

const tempRoot = mkdtempSync(path.join(tmpdir(), "telos-performance-doctor-"));
try {
  const goodPath = path.join(tempRoot, "good.html");
  const badPath = path.join(tempRoot, "bad.html");
  writeFileSync(goodPath, goodHtml, "utf8");
  writeFileSync(badPath, badHtml, "utf8");

  const match = scanPerformanceSurface(goodPath, {
    generatedAt: "2026-06-29T00:00:00.000Z"
  });
  assert.equal(match.schema, "project-telos.performance-doctor/v1");
  assert.equal(match.tool, "telos.performance.doctor");
  assert.equal(match.generated_at, "2026-06-29T00:00:00.000Z");
  assert.equal(match.surface.kind, "html");
  assert.equal(match.surface.present, true);
  assert.match(match.surface.hash, /^sha256:[a-f0-9]{64}$/);
  assert.equal(match.aggregate.check_count, 14);
  assert.equal(match.aggregate.verdict, "MATCH");
  assert.deepEqual(match.aggregate.failure_codes, []);
  assert.equal(match.privacy_boundary.raw_html_included, false);
  assert.equal(match.privacy_boundary.absolute_paths_included, false);
  assert.equal(match.privacy_boundary.browser_automation_required, false);
  assert.equal(match.metrics.script_tags, 2);
  assert.equal(match.signals.head_blocking_script_absent, true);
  assert.equal(match.signals.external_scripts_absent, true);
  assert.equal(match.signals.font_display_swap, true);
  assert.equal(match.signals.canvas_dimensions, true);
  assert.equal(match.signals.reduced_motion_media, true);
  assert.equal(JSON.stringify(match).includes(tempRoot), false, "scanner must not leak absolute temp path");
  assert.equal(JSON.stringify(match).includes("Fallback"), false, "scanner must not include HTML body");

  const drift = scanPerformanceSurface(badPath, {
    generatedAt: "2026-06-29T00:00:01.000Z"
  });
  assert.equal(drift.aggregate.verdict, "DRIFT");
  assert.deepEqual(drift.aggregate.failure_codes, [
    "html_byte_budget_exceeded",
    "inline_style_budget_exceeded",
    "script_count_budget_exceeded",
    "head_blocking_script_present",
    "external_script_present",
    "external_stylesheet_present",
    "external_host_unapproved",
    "font_display_swap_missing",
    "external_font_budget_exceeded",
    "canvas_dimensions_missing",
    "media_dimensions_missing",
    "inline_event_handler_present",
    "reduced_motion_missing",
    "autoplay_media_present"
  ]);

  const missing = scanPerformanceSurface(path.join(tempRoot, "missing.html"), {
    generatedAt: "2026-06-29T00:00:02.000Z"
  });
  assert.equal(missing.aggregate.verdict, "UNVERIFIABLE");
  assert.deepEqual(missing.aggregate.failure_codes, ["html_surface_unjoinable"]);

  const cli = spawnSync(process.execPath, [
    path.join(here, "performance-doctor.mjs"),
    "--html",
    goodPath
  ], {
    cwd: path.resolve(here, ".."),
    encoding: "utf8"
  });
  assert.equal(cli.status, 0, cli.stderr || cli.stdout);
  assert.equal(JSON.parse(cli.stdout).aggregate.verdict, "MATCH");

  const summary = spawnSync(process.execPath, [
    path.join(here, "performance-doctor.mjs"),
    "--html",
    goodPath,
    "--summary"
  ], {
    cwd: path.resolve(here, ".."),
    encoding: "utf8"
  });
  assert.equal(summary.status, 0, summary.stderr || summary.stdout);
  assert.match(summary.stdout, /Telos Performance Doctor/);
  assert.match(summary.stdout, /checks\s+14/);
  assert.match(summary.stdout, /verdict\s+MATCH/);
} finally {
  rmSync(tempRoot, { recursive: true, force: true });
}
