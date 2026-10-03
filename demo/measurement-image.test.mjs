// measurement-image.test.mjs: telos.measurement.layers v2, the measurement contract for a caller's image.
// Checks (a) to (e) of the contract, the paired sensitivity checks for every equality check, the status
// rule and layer identity. Tests named "eq:" are equality checks; bench/measurement-v2/mutations.json
// pairs each with a mutation that must make it fail (bench/measurement-v2/run-mutations.mjs).
// Run: node --test demo/measurement-image.test.mjs  (Python 3 with numpy for the two Python checks)
import { test } from "node:test";
import assert from "node:assert/strict";
import { execFileSync, spawnSync } from "node:child_process";
import { mkdirSync, mkdtempSync, rmSync, symlinkSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { measureRequest, verifyMeasurementReceipt, payloadScan } from "./measurement-image.mjs";
import { layerPacket } from "./vendor/sense-core/layers-int.mjs";
import { handleRequest } from "./telos-mcp.mjs";
import { b64, noise, request, seededImages, solid, xorshift32 } from "../bench/measurement-v2/fixtures.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const BENCH = path.join(here, "..", "bench", "measurement-v2");
const results = {};
const py = (args, input) => execFileSync("python", args, { cwd: BENCH, encoding: "utf8", maxBuffer: 1 << 28, input });
const ok = (r) => { assert.notEqual(r.status, "REJECTED", JSON.stringify(r).slice(0, 300)); return r; };

test("mv2.a eq: a constant image fills one histogram bin and oklab_mean is within 1e-6 of float OKLab", () => {
  const next = xorshift32(20261002);
  const colours = [[200, 120, 40]];
  for (let i = 0; i < 200; i++) colours.push([next() & 255, next() & 255, next() & 255]);
  const dir = mkdtempSync(path.join(tmpdir(), "telos-v2-"));
  try {
    writeFileSync(path.join(dir, "c.json"), JSON.stringify(colours));
    const ref = JSON.parse(py(["float_oklab.py", path.join(dir, "c.json")]));
    let worst = 0, oneBin = 0;
    colours.forEach((c, k) => {
      const r = ok(measureRequest(request({ w: 64, h: 64, px: solid(64, 64, c) })));
      if (r.luma_histogram.bins.filter((v) => v > 0).length === 1 && r.luma_histogram.bins.includes(4096)) oneBin++;
      ["L", "a", "b"].forEach((ch, j) => { worst = Math.max(worst, Math.abs(Number(r.oklab_mean[ch]) - ref[k][j])); });
    });
    results.a = { colours: colours.length, oneBin, worstAbsError: worst };
    assert.equal(oneBin, colours.length);
    assert.ok(worst <= 1e-6, `worst ${worst}`);
  } finally { rmSync(dir, { recursive: true, force: true }); }
});

test("mv2.b: an rgba length mismatch and a mask size mismatch return pixel_dimensions_mismatch", () => {
  const px = solid(8, 8, [1, 2, 3]);
  assert.equal(measureRequest({ image: { rgba: b64(px.subarray(4)), width: 8, height: 8 } }).failure_code, "pixel_dimensions_mismatch");
  assert.equal(measureRequest({ image: { rgba: b64(px), width: 8, height: 8 }, overlays: [{ id: "o", mask: b64(new Uint8Array(63)) }] }).failure_code, "pixel_dimensions_mismatch");
  assert.equal(measureRequest({ image: { rgba: b64(px), width: 4096, height: 4097 } }).failure_code, "image_too_large");
});

test("mv2.c: outside, UNC, relative and junction-escape paths are refused; a file inside the root is read", () => {
  const base = mkdtempSync(path.join(tmpdir(), "telos-v2-root-"));
  try {
    const root = path.join(base, "root"), outside = path.join(base, "outside");
    mkdirSync(root); mkdirSync(outside);
    const px = solid(4, 4, [9, 9, 9]);
    writeFileSync(path.join(root, "in.rgba"), px); writeFileSync(path.join(outside, "out.rgba"), px);
    symlinkSync(outside, path.join(root, "link"), "junction");
    const env = { TELOS_MEASUREMENT_ROOTS: root };
    const call = (p) => measureRequest({ image: { path: p, width: 4, height: 4 }, layers: ["L0"] }, env);
    const codes = {
      outside: call(path.join(outside, "out.rgba")).failure_code,
      unc: call("\\\\server\\share\\x.rgba").failure_code,
      relative: call("in.rgba").failure_code,
      junction: call(path.join(root, "link", "out.rgba")).failure_code,
      noRoots: measureRequest({ image: { path: path.join(root, "in.rgba"), width: 4, height: 4 } }, {}).failure_code,
    };
    results.c = codes;
    for (const [k, v] of Object.entries(codes)) assert.equal(v, "path_outside_allowed_root", k);
    const inside = ok(call(path.join(root, "in.rgba")));
    assert.equal(inside.input_receipt.rgba_sha256, measureRequest(request({ w: 4, h: 4, px }), {}).input_receipt.rgba_sha256);
  } finally { rmSync(base, { recursive: true, force: true }); }
});

test("mv2.d eq: two runs in one process and in two processes give one receipt_sha256", () => {
  const img = [...seededImages(1, 40, 60)][0];
  const a = ok(measureRequest(request(img))), b = ok(measureRequest(request(img)));
  const cli = () => JSON.parse(spawnSync(process.execPath, [path.join(here, "measurement-layers.mjs"), "--request", "-"],
    { input: JSON.stringify(request(img)), encoding: "utf8", maxBuffer: 1 << 26 }).stdout).receipt_sha256;
  const c = cli(), d = cli();
  results.d = { inProcess: [a.receipt_sha256, b.receipt_sha256], processes: [c, d], node: process.version, platform: process.platform,
    otherNodeMajor: "not run (no second Node major on this machine)", linux: "not run (no Node on the Linux runtime here)" };
  assert.equal(a.receipt_sha256, b.receipt_sha256);
  assert.equal(c, d);
  assert.equal(a.receipt_sha256, c);
});

test("mv2.d eq: Python re-derives input_receipt.sha256 and receipt_sha256 on 100 seeded responses", () => {
  const responses = [...seededImages(100, 4, 80, 777)].map((img) => ok(measureRequest(request(img, { declared: { colour_space: "srgb" } }))));
  const dir = mkdtempSync(path.join(tmpdir(), "telos-v2-py-"));
  try {
    writeFileSync(path.join(dir, "r.json"), JSON.stringify(responses));
    py(["rederive.py", path.join(dir, "r.json"), path.join(dir, "o.json")]);
    const out = JSON.parse(execFileSync("python", ["-c", "import sys;print(open(sys.argv[1]).read())", path.join(dir, "o.json")], { encoding: "utf8" }));
    const agree = out.filter((o, i) => o.input_sha256 === responses[i].input_receipt.sha256 && o.receipt_sha256 === responses[i].receipt_sha256).length;
    results.pythonRederive = { agree, of: responses.length };
    assert.equal(agree, responses.length);
  } finally { rmSync(dir, { recursive: true, force: true }); }
});

// A clause fixed before the code also asked that the same edit change "the changed layer's
// measurement_sha256". As written it fails: a one-code change to one pixel moves no cell across a bin, so no
// layer text changes and no layer hash may change. The count is recorded (results.onePixel.layerHashChanged)
// and the clause is reported as failed. The post hoc check below tests a one-step change to a quantised value.
test("mv2.sens: one code value in one pixel changes the input receipt and the response receipt (20 of 20)", () => {
  let changed = 0, layerHashChanged = 0;
  for (const img of seededImages(20, 24, 64, 4242)) {
    const before = ok(measureRequest(request(img)));
    const px = Uint8Array.from(img.px); const i = (img.w * img.h >> 1) * 4; px[i] = px[i] === 255 ? 254 : px[i] + 1;
    const after = ok(measureRequest(request({ ...img, px })));
    if (before.layers.some((l, k) => l.measurement_sha256 !== after.layers[k]?.measurement_sha256)) layerHashChanged++;
    if (before.input_receipt.sha256 !== after.input_receipt.sha256 && before.receipt_sha256 !== after.receipt_sha256) changed++;
  }
  results.onePixel = { changed, of: 20, layerHashChanged, layerClause: "failed as written: no layer text changed, so no layer hash may change" };
  assert.equal(changed, 20);
});

test("mv2.sens (post hoc) eq: a layer hash changes exactly when its text changes, on 20 one-bin edits", () => {
  let moved = 0, heldWhenSame = 0;
  for (const img of seededImages(20, 64, 96, 515)) {
    const before = ok(measureRequest(request(img)));
    const paint = (v) => {
      const px = Uint8Array.from(img.px);
      for (let y = 0; y < Math.floor(img.h / 8); y++) for (let x = 0; x < Math.floor(img.w / 8); x++) {
        const i = (y * img.w + x) * 4; px[i] = v; px[i + 1] = v; px[i + 2] = v;
      }
      return ok(measureRequest(request({ ...img, px })));
    };
    let after = paint(255);
    if (after.layers[1].text === before.layers[1].text) after = paint(0);
    for (let k = 0; k < before.layers.length; k++) {
      const same = before.layers[k].text === after.layers[k].text;
      if (!same && before.layers[k].measurement_sha256 !== after.layers[k].measurement_sha256) moved++;
      if (same && before.layers[k].measurement_sha256 === after.layers[k].measurement_sha256) heldWhenSame++;
    }
    const l1 = after.layers.find((l) => l.id === "L1");
    if (before.layers.find((l) => l.id === "L1").text === l1.text) assert.fail("the corner edit did not move an L1 bin");
  }
  results.oneBin = { layerHashMovedWithText: moved, layerHashHeldWithText: heldWhenSame };
  assert.ok(moved >= 20);
});

test("mv2.sens: one declared field changes both receipt hashes; 20 single-field edits each fail verification", () => {
  const img = [...seededImages(1, 64, 64, 99)][0];
  const r = ok(measureRequest(request(img, { declared: { colour_space: "srgb" } })));
  const p3 = ok(measureRequest(request(img, { declared: { colour_space: "display-p3" } })));
  assert.notEqual(r.input_receipt.sha256, p3.input_receipt.sha256);
  assert.notEqual(r.receipt_sha256, p3.receipt_sha256);
  assert.equal(verifyMeasurementReceipt(r), true);
  const edits = [
    (x) => { x.status = "MATCH"; }, (x) => { x.status_reason = ""; }, (x) => { x.input_receipt.width += 1; },
    (x) => { x.layers[0].text += " "; }, (x) => { x.layers[1].cells += 1; }, (x) => { x.dropped.push({ id: "L9" }); },
    (x) => { x.oklab_mean.L = "0.000000000"; }, (x) => { x.luma_histogram.min += 1; }, (x) => { x.events[0].frame_id = "frame:1"; },
    (x) => { x.warnings.push({ code: "x" }); }, (x) => { x.tool = "telos.other"; }, (x) => { x.schema += "x"; },
    (x) => { x.request_schema = ""; }, (x) => { x.canonical = "none"; }, (x) => { x.failure_code_vocabulary.pop(); },
    (x) => { x.layers[0].measurement_sha256 = "0".repeat(64); }, (x) => { x.events[0].uncertainty.status = "witnessed"; },
    (x) => { x.input_receipt.colour_status = "unverifiable"; }, (x) => { x.luma_histogram.bins[0] += 1; }, (x) => { x.layers[2].params.n += 1; },
  ];
  const failed = edits.filter((e) => { const x = structuredClone(r); e(x); return !verifyMeasurementReceipt(x); }).length;
  results.edits = { failed, of: edits.length };
  assert.equal(failed, 20);
});

test("mv2.e eq: no encoded run outside permitted blocks on 100 seeded images and a 64 x 64 noise image", () => {
  const imgs = [...seededImages(100, 1, 96, 31337), { w: 64, h: 64, px: noise(64, 64, xorshift32(5)) }];
  const bad = imgs.map((img) => measureRequest(request(img))).filter((r) => r.status === "REJECTED" || payloadScan(r) !== null);
  results.e = { images: imgs.length, flagged: bad.length };
  assert.equal(bad.length, 0);
});

test("mv2.e: a 32 x 32 input at n = 32 emits at most 64 cells per layer (L1 dropped, L2 at N = 7)", () => {
  const r = ok(measureRequest(request({ w: 32, h: 32, px: noise(32, 32, xorshift32(11)) }, { n: 32 })));
  results.small = { layers: r.layers.map((l) => [l.id, l.cells]), dropped: r.dropped.map((d) => d.id) };
  assert.ok(r.layers.every((l) => l.cells <= 64));
  assert.deepEqual(r.layers.map((l) => l.id), ["L0", "L2"]);
  assert.equal(r.layers[1].params.n, 7);
  assert.ok(r.dropped.some((d) => d.id === "L1" && d.failure_code === "privacy_cell_bound"));
});

test("mv2.e: an injected 65-character hex run is refused with raw_payload_leak", () => {
  const img = [...seededImages(1, 64, 64, 8)][0];
  assert.equal(measureRequest(request(img, { run_id: "a".repeat(65) })).failure_code, "raw_payload_leak");
  assert.equal(measureRequest(request(img, { run_id: Array.from({ length: 30 }, (_, i) => i).join(",") })).failure_code, "raw_payload_leak");
  assert.notEqual(measureRequest(request(img, { run_id: "a".repeat(64) })).status, "REJECTED");
});

test("mv2.status eq: caller pixels carry computed with the input receipt, never witnessed; the verdict is UNVERIFIABLE", () => {
  const img = [...seededImages(1, 50, 70, 3)][0];
  const r = ok(measureRequest(request(img)));
  assert.equal(r.status, "UNVERIFIABLE");
  assert.ok(r.events.length >= 3);
  for (const e of r.events) assert.deepEqual(e.uncertainty, { status: "computed", reason: "caller_pixels", input_receipt: r.input_receipt.sha256 });
  assert.equal(JSON.stringify(r).includes("witnessed"), false);
});

test("mv2.identity eq: v2 layer text equals sense-core layerPacket on 50 seeded images", () => {
  let same = 0;
  for (const img of seededImages(50, 144, 200, 2026)) {
    const r = ok(measureRequest(request(img)));
    const want = layerPacket(img.px, img.w, img.h, 4, 32).text;
    if (r.layers.map((l) => l.text).join("\n") + "\n" === want) same++;
  }
  results.identity = { same, of: 50 };
  assert.equal(same, 50);
});

test("mv2.overlays: drawn overlays leave L0, an overlay is listed in L3, a full mask is refused", () => {
  const w = 40, h = 30, px = solid(w, h, [90, 90, 90]), mask = new Uint8Array(w * h);
  for (let x = 5; x < 15; x++) { mask[5 * w + x] = 1; const i = (5 * w + x) * 4; px[i] = 255; px[i + 1] = 0; px[i + 2] = 0; }
  const r = ok(measureRequest({ image: { rgba: b64(px), width: w, height: h }, overlays: [{ id: "ring", mask: b64(mask) }], overlays_drawn: true }));
  assert.match(r.layers[0].text, /achromatic:1/);
  assert.equal(r.layers.at(-1).text.split("\n")[1], "region id:ring bbox:5,5,14,5 area:8 overlay:true");
  assert.equal(measureRequest({ image: { rgba: b64(px), width: w, height: h }, overlays: [{ id: "all", mask: b64(new Uint8Array(w * h).fill(1)) }], overlays_drawn: true }).failure_code, "overlay_covers_frame");
});

test("mv2.mcp: tools/call with arguments returns v2; without arguments the v1 demo packet", () => {
  const img = [...seededImages(1, 30, 30, 1)][0];
  const v2 = handleRequest({ jsonrpc: "2.0", id: 1, method: "tools/call", params: { name: "telos.measurement.layers", arguments: request(img) } });
  assert.equal(v2.result.structuredContent.schema, "project-telos.measurement-layers/v2");
  const v1 = handleRequest({ jsonrpc: "2.0", id: 2, method: "tools/call", params: { name: "telos.measurement.layers", arguments: {} } });
  assert.equal(v1.result.structuredContent.schema, "project-telos.measurement-layers/v1");
});

test("mv2 results file", () => {
  if (process.env.TELOS_WRITE_RESULTS !== "1") return;
  // SHA-256 of the rule texts fixed before this code was written (kept in the site repository's test tree).
  const out = { result: "measurement-v2", rule_text_sha256: [
    "7c13f35793a05da63f4199edffa3fb08ce60b2ecf6135d4294a6146f81efde52",
    "75cbd7d12857b3d9143c4cd14169731388f33be5e495093943b6d29fdd2061eb",
    "31831aaec61385d29f47180b52cd785eb8a107c001653f30e3ce3ca7690978be",
    "a3db4b310e3a24ec0a3c40124b88dbef0dba713d334c4fe8303f02f6b350d121"], node: process.version, ...results };
  writeFileSync(path.join(BENCH, "results", "measurement-v2.json"), JSON.stringify(out, null, 1) + "\n");
});
