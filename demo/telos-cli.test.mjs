import { test } from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, rmSync, writeFileSync, existsSync, readFileSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { tmpdir } from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createHash } from "node:crypto";

import { renderFromSpec } from "./telos-cli.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const cliPath = path.join(here, "telos-cli.mjs");

function writeSceneRequest(dir, overrides = {}) {
  const request = {
    schema: "learn.telos.scene-request/v1",
    concept: { title: "Damped harmonic oscillator", kind: "physics.ode" },
    spec: { lane: "math_physics", params: { omega: 2.0, zeta: 0.1 }, notes: "" },
    requestHash: "sha256:" + "a".repeat(64),
    ...overrides
  };
  const specPath = path.join(dir, "scene-request.json");
  writeFileSync(specPath, JSON.stringify(request, null, 2));
  return specPath;
}

const SEVEN_KEYS = ["selected_profile", "fallback_chain", "scene_spec_hash", "result_hash", "verdict", "evidence_refs", "artifactRef"];

test("renderFromSpec produces the 7-key render-result shape with MATCH on a valid math scene request", () => {
  const dir = mkdtempSync(path.join(tmpdir(), "telos-cli-"));
  try {
    const specPath = writeSceneRequest(dir);
    const result = renderFromSpec(specPath);

    for (const key of SEVEN_KEYS) assert.ok(key in result, `missing key ${key}`);
    assert.equal(Object.keys(result).filter((k) => SEVEN_KEYS.includes(k)).length, SEVEN_KEYS.length);

    assert.equal(result.verdict, "MATCH");
    assert.match(result.scene_spec_hash, /^sha256:[0-9a-f]{64}$/);
    assert.match(result.result_hash, /^sha256:[0-9a-f]{64}$/);
    assert.equal(result.selected_profile, "static-artifact-receipt");
    assert.ok(Array.isArray(result.fallback_chain) && result.fallback_chain.includes("static-artifact-receipt"));
    assert.deepEqual(result.evidence_refs, [specPath]);
    assert.ok(existsSync(result.artifactRef), "artifact file was not written");
    const svg = readFileSync(result.artifactRef, "utf8");
    assert.match(svg, /^<svg /);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("renderFromSpec reports the full fallback_chain for provenance even though only the static profile is reachable", () => {
  const dir = mkdtempSync(path.join(tmpdir(), "telos-cli-"));
  try {
    const specPath = writeSceneRequest(dir);
    const result = renderFromSpec(specPath);
    assert.ok(result.fallback_chain.length >= 4);
    assert.equal(result.fallback_chain[result.fallback_chain.length - 1], "static-artifact-receipt");
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("renderFromSpec reuses render-nd for a known polytope concept.kind and still emits a valid SVG", () => {
  const dir = mkdtempSync(path.join(tmpdir(), "telos-cli-"));
  try {
    const specPath = writeSceneRequest(dir, {
      concept: { title: "Tesseract", kind: "cube" },
      spec: { lane: "math_physics", params: { n: 4, t: 0.25 }, notes: "" }
    });
    const result = renderFromSpec(specPath);
    assert.equal(result.verdict, "MATCH");
    const svg = readFileSync(result.artifactRef, "utf8");
    assert.match(svg, /<line /);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("renderFromSpec computes scene_spec_hash as sha256 of the canonical {concept, spec} JSON (matches learn's requestHash derivation)", () => {
  const dir = mkdtempSync(path.join(tmpdir(), "telos-cli-"));
  try {
    const concept = { title: "y = sin(x)", kind: "math.function-plot" };
    const spec = { lane: "math_physics", params: { fn: "sin", omega: 1 }, notes: "" };
    const specPath = writeSceneRequest(dir, { concept, spec });
    const result = renderFromSpec(specPath);

    const expected = "sha256:" + createHash("sha256").update(JSON.stringify({ concept, spec })).digest("hex");
    assert.equal(result.scene_spec_hash, expected);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("renderFromSpec fails closed (UNVERIFIABLE) on a missing spec file, never throws", () => {
  const dir = mkdtempSync(path.join(tmpdir(), "telos-cli-"));
  try {
    const missing = path.join(dir, "does-not-exist.json");
    const result = renderFromSpec(missing);
    for (const key of SEVEN_KEYS) assert.ok(key in result, `missing key ${key}`);
    assert.equal(result.verdict, "UNVERIFIABLE");
    assert.equal(result.scene_spec_hash, null);
    assert.equal(result.result_hash, null);
    assert.equal(result.artifactRef, null);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("renderFromSpec fails closed (UNVERIFIABLE) on the wrong schema", () => {
  const dir = mkdtempSync(path.join(tmpdir(), "telos-cli-"));
  try {
    const specPath = writeSceneRequest(dir, { schema: "some.other.schema/v1" });
    const result = renderFromSpec(specPath);
    assert.equal(result.verdict, "UNVERIFIABLE");
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("renderFromSpec fails closed (UNVERIFIABLE) on malformed JSON", () => {
  const dir = mkdtempSync(path.join(tmpdir(), "telos-cli-"));
  try {
    const specPath = path.join(dir, "scene-request.json");
    writeFileSync(specPath, "{ not: valid json");
    const result = renderFromSpec(specPath);
    assert.equal(result.verdict, "UNVERIFIABLE");
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("main() prints usage to stderr and returns non-zero for an unknown subcommand", () => {
  const res = spawnSync(process.execPath, [cliPath, "bogus"], { encoding: "utf8" });
  assert.notEqual(res.status, 0);
  assert.match(res.stderr, /usage: node demo\/telos-cli\.mjs render <specPath>/);
});

test("main() prints usage to stderr and returns non-zero when specPath is missing", () => {
  const res = spawnSync(process.execPath, [cliPath, "render"], { encoding: "utf8" });
  assert.notEqual(res.status, 0);
  assert.match(res.stderr, /usage:/);
});

test("CLI end-to-end: `node demo/telos-cli.mjs render <specPath>` prints the 7-key JSON with MATCH", () => {
  const dir = mkdtempSync(path.join(tmpdir(), "telos-cli-"));
  try {
    const specPath = writeSceneRequest(dir);
    const res = spawnSync(process.execPath, [cliPath, "render", specPath], { encoding: "utf8" });
    assert.equal(res.status, 0);
    const out = JSON.parse(res.stdout);
    for (const key of SEVEN_KEYS) assert.ok(key in out, `missing key ${key}`);
    assert.equal(out.verdict, "MATCH");
    assert.match(out.scene_spec_hash, /^sha256:[0-9a-f]{64}$/);
    assert.match(out.result_hash, /^sha256:[0-9a-f]{64}$/);
    assert.ok(existsSync(out.artifactRef));
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});
