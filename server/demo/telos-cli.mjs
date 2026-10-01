// telos-cli.mjs - the telos engine's CLI surface. `render <specPath>` is the seam the `learn`
// flagship wires to (see learn/src/interop/telos.mjs: LEARN_TELOS_CMD -> "... render <specPath>").
// Zero external dependencies (node builtins only). Fail-closed: any error yields verdict
// "UNVERIFIABLE" rather than a thrown exception or a partial/ambiguous result.
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { renderScene } from "./render-nd/index.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));

const CAPABILITIES = JSON.parse(
  readFileSync(path.join(here, "integrations", "rendering-capabilities.json"), "utf8")
);

const SCHEMA = "learn.telos.scene-request/v1";

// The render-nd polytope kinds this engine can reuse directly (demo/render-nd/core/polytopes.mjs).
const POLYTOPE_KINDS = new Set(["cube", "simplex", "orthoplex", "24cell"]);

function sha256hex(input) {
  return createHash("sha256").update(input).digest("hex");
}

// selectProfile - walk the fallback chain declared in rendering-capabilities.json and report which
// profile is actually reachable in this host. A Node CLI has no navigator.gpu / WebGL2 / canvas
// context, so the only host signal it can honestly claim is "file_artifact" -> static-artifact-receipt.
// The full chain is still reported (unselected entries included) so learn gets provenance for why.
function selectProfile() {
  const fallback_chain = CAPABILITIES.selection_order.slice();
  const selected_profile = "static-artifact-receipt";
  if (!fallback_chain.includes(selected_profile)) fallback_chain.push(selected_profile);
  return { selected_profile, fallback_chain };
}

// validateSceneRequest - structural check against learn.telos.scene-request/v1. Returns
// { ok: true, request } or { ok: false, reason }. Never throws.
function validateSceneRequest(request) {
  if (!request || typeof request !== "object") return { ok: false, reason: "scene request is not an object" };
  if (request.schema !== SCHEMA) return { ok: false, reason: `unexpected schema (want ${SCHEMA})` };
  if (!request.concept || typeof request.concept !== "object") return { ok: false, reason: "missing concept" };
  if (typeof request.concept.kind !== "string" || !request.concept.kind) return { ok: false, reason: "missing concept.kind" };
  if (!request.spec || typeof request.spec !== "object") return { ok: false, reason: "missing spec" };
  if (typeof request.requestHash !== "string" || !request.requestHash.startsWith("sha256:")) {
    return { ok: false, reason: "missing or malformed requestHash" };
  }
  return { ok: true, request };
}

function svgDocument(width, height, body) {
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${width} ${height}" width="${width}" height="${height}">` +
    `<rect x="0" y="0" width="${width}" height="${height}" fill="#0a0c10"/>${body}</svg>\n`;
}

// polytopeToSvg - reuse render-nd's renderScene() (geometry + projection) and emit its segments
// as a simple SVG line drawing. Normalized [-1,1] scene space -> pixel space (y flipped).
function polytopeToSvg(concept, params, width = 512, height = 512) {
  const scene = renderScene({
    kind: concept.kind,
    n: params.n,
    t: params.t,
    rotation: params.rotation,
    projection: params.projection,
    scale: params.scale
  });
  const toPx = (x, y) => [((x + 1) / 2) * (width - 1), (1 - (y + 1) / 2) * (height - 1)];
  const lines = scene.segments.map((s) => {
    const [x1, y1] = toPx(s.x1, s.y1);
    const [x2, y2] = toPx(s.x2, s.y2);
    const [r, g, b] = s.color;
    return `<line x1="${x1.toFixed(2)}" y1="${y1.toFixed(2)}" x2="${x2.toFixed(2)}" y2="${y2.toFixed(2)}" ` +
      `stroke="rgb(${r},${g},${b})" stroke-opacity="${s.opacity.toFixed(3)}" stroke-width="1.5"/>`;
  });
  return { svg: svgDocument(width, height, lines.join("")), meta: scene.meta };
}

// sampleFunctionPlot - the ~30-line math.* primitive. Samples spec.params into a polyline SVG.
// params: { fn: "sin"|"cos"|"linear"|"quadratic", xmin, xmax, samples, omega, zeta, amplitude, ... }.
// Unknown/absent params fall back to a damped-oscillator-friendly default so a bare {omega, zeta}
// concept (learn's physics.ode example) still renders something meaningful.
function sampleFunctionPlot(params = {}, width = 512, height = 200) {
  const xmin = params.xmin ?? 0;
  const xmax = params.xmax ?? (params.omega ? (4 * Math.PI) / Math.max(params.omega, 1e-6) : 10);
  const samples = Math.max(2, Math.min(2000, Math.floor(params.samples ?? 200)));
  const omega = params.omega ?? 1;
  const zeta = params.zeta ?? 0;
  const amplitude = params.amplitude ?? 1;
  const fn = params.fn ?? (params.omega !== undefined ? "damped" : "linear");

  const evaluate = (x) => {
    if (fn === "sin") return amplitude * Math.sin(omega * x);
    if (fn === "cos") return amplitude * Math.cos(omega * x);
    if (fn === "quadratic") return amplitude * x * x;
    if (fn === "damped") return amplitude * Math.exp(-zeta * omega * x) * Math.cos(omega * x);
    return amplitude * x; // linear default
  };

  const ys = [];
  for (let i = 0; i < samples; i += 1) {
    const x = xmin + ((xmax - xmin) * i) / (samples - 1);
    ys.push({ x, y: evaluate(x) });
  }
  let ymin = Infinity, ymax = -Infinity;
  for (const p of ys) { if (p.y < ymin) ymin = p.y; if (p.y > ymax) ymax = p.y; }
  if (!Number.isFinite(ymin) || !Number.isFinite(ymax) || ymin === ymax) { ymin -= 1; ymax += 1; }

  const pad = 12;
  const toPx = (x, y) => {
    const px = pad + ((x - xmin) / (xmax - xmin)) * (width - 2 * pad);
    const py = height - pad - ((y - ymin) / (ymax - ymin)) * (height - 2 * pad);
    return [px, py];
  };
  const pts = ys.map((p) => toPx(p.x, p.y).map((v) => v.toFixed(2)).join(",")).join(" ");
  const polyline = `<polyline points="${pts}" fill="none" stroke="#5ec8f8" stroke-width="2"/>`;
  return { svg: svgDocument(width, height, polyline), meta: { fn, samples, xmin, xmax, ymin, ymax } };
}

// artifactPathFor - a sibling path of specPath, e.g. "runs/scene-request.json" -> "runs/scene-request.svg".
function artifactPathFor(specPath) {
  const dir = path.dirname(specPath);
  const base = path.basename(specPath, path.extname(specPath));
  return path.join(dir, `${base}.svg`);
}

// renderFromSpec - the testable core. Reads+validates the scene request at specPath, selects a
// renderer profile, produces a real SVG artifact, hashes both request and artifact, and returns
// the exact 7-key render-result shape learn's telosRender() expects. Never throws.
export function renderFromSpec(specPath) {
  const { selected_profile, fallback_chain } = selectProfile();
  const base = { selected_profile, fallback_chain, scene_spec_hash: null, result_hash: null,
    verdict: "UNVERIFIABLE", evidence_refs: [specPath], artifactRef: null };
  try {
    const raw = readFileSync(specPath, "utf8");
    const parsed = JSON.parse(raw);
    const validated = validateSceneRequest(parsed);
    if (!validated.ok) return { ...base, reason: validated.reason };
    const request = validated.request;

    const scene_spec_hash = "sha256:" + sha256hex(JSON.stringify({ concept: request.concept, spec: request.spec }));

    const params = request.spec.params ?? {};
    const isPolytope = POLYTOPE_KINDS.has(request.concept.kind);
    const { svg } = isPolytope ? polytopeToSvg(request.concept, params) : sampleFunctionPlot(params);

    const artifactRef = artifactPathFor(specPath);
    writeFileSync(artifactRef, svg, "utf8");
    const result_hash = "sha256:" + sha256hex(readFileSync(artifactRef));

    return { selected_profile, fallback_chain, scene_spec_hash, result_hash, verdict: "MATCH",
      evidence_refs: [specPath], artifactRef };
  } catch (err) {
    return { ...base, reason: String(err && err.message ? err.message : err) };
  }
}

function usage() {
  process.stderr.write("usage: node demo/telos-cli.mjs render <specPath>\n");
}

// main - thin argv wrapper. `render <specPath>` prints the render-result JSON on stdout.
// Any other subcommand, or a missing specPath, prints usage to stderr and exits non-zero.
export function main(argv) {
  const [cmd, specPath] = argv;
  if (cmd !== "render" || !specPath) { usage(); return 1; }
  const result = renderFromSpec(specPath);
  process.stdout.write(`${JSON.stringify(result)}\n`);
  return 0;
}

const invokedDirectly = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (invokedDirectly) {
  process.exit(main(process.argv.slice(2)));
}
