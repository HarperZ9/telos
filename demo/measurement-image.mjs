// measurement-image.mjs: `telos.measurement.layers` v2, Telos measurement layers on a caller's image.
//
// The request (measurement-request.mjs) gives raw 8-bit RGBA. This module runs the sense-core integer
// colour path (vendor/sense-core, byte-identical with the site and the studio libraries) and returns:
//   - layers L0 to L2 (global statistics, coarse layout, perceptual field) and L3 (caller overlays);
//   - an exact OKLab mean and a luma histogram;
//   - SHA-256 receipts over canonical bytes: the input, every layer, and the whole response.
// Values computed from caller pixels carry uncertainty status `computed` with the input receipt: Telos saw
// the bytes it was handed, not where they came from. The packet verdict is UNVERIFIABLE until a caller
// names a criterion. A privacy bound caps every layer at one cell per 16 input pixels, and a final scan
// refuses any response that carries a long run of encoded data outside the permitted layer text.
import { createHash } from "node:crypto";

import { canonicalString } from "./vendor/shared-frame/canonical.js";
import { layerPacketLinear, layerL3Overlays, linearQ24FromRgba } from "./vendor/sense-core/layers-int.mjs";
import { oklabMeanExact } from "./vendor/sense-core/oklab-mean-exact.mjs";
import { resampleAreaLinear, longEdgeSize, RESAMPLE_SCHEMA } from "./vendor/sense-core/resample-int.mjs";
import { OKLAB_INT_SCHEMA } from "./vendor/sense-core/oklab-int.mjs";
import { MeasurementError, parseRequest, REQUEST_SCHEMA } from "./measurement-request.mjs";

export const RESPONSE_SCHEMA = "project-telos.measurement-layers/v2";
export const TOOL = "telos.measurement.layers";
export const FAILURE_CODES = Object.freeze([
  "request_invalid", "image_decode_failed", "image_too_large", "unsupported_bit_depth", "pixel_dimensions_mismatch",
  "path_outside_allowed_root", "privacy_cell_bound", "overlay_covers_frame", "raw_payload_leak",
]);
const LAYER_NOTES = {
  L0: ["global tone range and colour cast", "every spatial fact"],
  L1: ["where light, dark and colour masses sit, at one eighth of each side", "everything inside a cell; chroma finer than a quarter"],
  L2: ["cell-mean colour in linear light at N, chroma at half resolution (achromatic branch: L only at N/2, 8 bits)", "sub-cell variance and edge position inside a cell"],
  L3: ["caller overlays as integer pixel boxes with their area", "overlay shape inside the box"],
};

export const sha256Hex = (data) => createHash("sha256").update(data).digest("hex");
export const canonicalSha256 = (value) => sha256Hex(Buffer.from(canonicalString(value), "utf8"));

// Cells a layer emits, the unit of the privacy bound.
export function layerCells(id, { n, achromatic, overlays = 0 }) {
  const half = Math.max(1, Math.floor(n / 2));
  if (id === "L0") return 1;
  if (id === "L1") return 80;
  if (id === "L2") return achromatic ? half * half : n * n + half * half;
  return overlays;
}

// Runs that would carry pixel data: base64 or hex longer than 64 characters, or decimal lists longer than
// 64 characters. Emitted layer texts are removed before the scan; their size is bounded by cells.
const LONG_B64 = /[A-Za-z0-9+/=_-]{65,}/;
const DEC_LIST = /-?\d+(?:\.\d+)?(?:[ ,;]+-?\d+(?:\.\d+)?)+/g;
// The histogram's 16 bins are a bounded summary block and are removed the same way.
export function payloadScan(response) {
  const texts = new Set((response.layers || []).map((l) => l.text));
  const strip = (v) => (typeof v === "string" ? (texts.has(v) ? "" : v)
    : Array.isArray(v) ? v.map(strip) : v && typeof v === "object" ? Object.fromEntries(Object.entries(v).map(([k, x]) => [k, strip(x)])) : v);
  const body = { ...response };
  if (body.luma_histogram) body.luma_histogram = { ...body.luma_histogram, bins: [] };
  const flat = JSON.stringify(strip(body));
  if (LONG_B64.test(flat)) return "encoded_run";
  for (const m of flat.matchAll(DEC_LIST)) if (m[0].length > 64) return "decimal_list";
  return null;
}

function lumaHistogram(px, w, h, keep) {
  const bins = new Array(16).fill(0);
  let min = 255, max = 0, sum = 0, count = 0;
  for (let i = 0; i < w * h; i++) {
    if (keep && !keep(i)) continue;
    const o = i * 4;
    const y = Math.floor((2126 * px[o] + 7152 * px[o + 1] + 722 * px[o + 2] + 5000) / 10000);
    bins[y >> 4] += 1; min = Math.min(min, y); max = Math.max(max, y); sum += y; count += 1;
  }
  return { luma: "rec709-int8", bin_count: 16, bins, min, max, mean_milli: count ? Math.floor((2000 * sum + count) / (2 * count)) : null, pixels: count };
}

export function rejection(code, detail = "") {
  return { schema: RESPONSE_SCHEMA, tool: TOOL, status: "REJECTED", failure_code: code, ...(detail ? { detail } : {}) };
}

// Build the v2 response for a parsed request.
function measure(req) {
  const { px, w, h, overlays, overlaysDrawn } = req;
  const union = overlays.length ? (i) => overlays.some((o) => o.mask[i]) : null;
  const keep = union && overlaysDrawn ? (i) => !union(i) : null;
  if (keep) { let any = false; for (let i = 0; i < w * h && !any; i++) any = keep(i); if (!any) throw new MeasurementError("overlay_covers_frame"); }
  const colourStatus = req.declared.colour_space === "unknown" ? "unverifiable" : "declared";
  const inputBody = {
    rgba_sha256: sha256Hex(px), width: w, height: h, decoder: req.decoder, declared: req.declared,
    colour_status: colourStatus, alpha_step: req.alphaStep, roi: req.roi, resample: req.resample ? { ...req.resample, schema: RESAMPLE_SCHEMA } : null,
  };
  const input_receipt = { ...inputBody, sha256: canonicalSha256(inputBody) };
  let lin = linearQ24FromRgba(px, w, h, 4), W = w, H = h;
  if (req.resample) { [W, H] = longEdgeSize(w, h, req.resample.long_edge); lin = resampleAreaLinear(lin, w, h, W, H); }
  const bound = Math.floor((W * H) / 16);
  const warnings = [], dropped = [];
  if (colourStatus === "unverifiable") warnings.push({ code: "colour_space_unknown" });
  if (keep) warnings.push({ code: "overlay_in_pixels" });
  const probe = layerPacketLinear(lin, W, H, 1, { keep, layers: ["L0"] });
  const achromatic = probe.achromatic;
  let n = req.n;
  while (n > 1 && layerCells("L2", { n, achromatic }) > bound) n -= 1;
  if (n !== req.n) warnings.push({ code: "privacy_n_capped", requested: req.n, emitted: n });
  const emit = req.layers.filter((id) => {
    const cells = layerCells(id, { n, achromatic, overlays: overlays.length });
    if (id === "L3" && !overlays.length) return false;
    if (cells > bound) { dropped.push({ id, failure_code: "privacy_cell_bound", cells, bound }); return false; }
    return true;
  });
  const packet = layerPacketLinear(lin, W, H, n, { keep, layers: emit.filter((id) => id !== "L3") });
  const layers = emit.map((id) => {
    const text = id === "L3" ? layerL3Overlays(overlays, w, h) : packet.layers[id];
    const params = { schema: id === "L3" ? "overlay-l3/v1" : OKLAB_INT_SCHEMA, width: W, height: H,
      ...(id === "L2" ? { n, branch: achromatic ? "achromatic" : "chromatic" } : {}), ...(id === "L0" && keep ? { pixels: "outside-overlays" } : {}) };
    const cells = layerCells(id, { n, achromatic, overlays: overlays.length });
    return { id, text, cells, params, preserves: LAYER_NOTES[id][0], discards: LAYER_NOTES[id][1], measurement_sha256: canonicalSha256({ id, text, params }) };
  });
  const events = layers.map((l) => {
    const ev = {
      event_id: `${req.runId}:${l.id}`, run_id: req.runId, frame_id: req.frameId, actor: TOOL, domain: "visual", subject_ref: l.id,
      clock_domain: "none", coordinate_space: "image.pixel", value_shape: "layer-text", value_ref: l.measurement_sha256,
      uncertainty: { status: "computed", reason: "caller_pixels", input_receipt: input_receipt.sha256 },
      privacy: { raw_payload_required: false, exported_value_is_summary: true }, severity: "info",
    };
    return { ...ev, event_sha256: canonicalSha256(ev) };
  });
  let histogram = null;
  if (bound >= 16) histogram = lumaHistogram(px, w, h, keep);
  else dropped.push({ id: "luma_histogram", failure_code: "privacy_cell_bound", cells: 16, bound });
  const body = {
    schema: RESPONSE_SCHEMA, tool: TOOL, request_schema: REQUEST_SCHEMA, status: "UNVERIFIABLE", status_reason: "no_criterion_supplied",
    input_receipt, layers, dropped, oklab_mean: { basis: "decoded pixels after roi", ...oklabMeanExact(px, w, h, 4, keep) },
    luma_histogram: histogram, events, warnings, failure_code_vocabulary: FAILURE_CODES,
    canonical: "project-telos.canonical-bytes/v1",
  };
  return { ...body, receipt_sha256: canonicalSha256(body) };
}

// Entry point: a request object in, a response or a rejection out. Never throws for caller errors.
export function measureRequest(args, env = process.env) {
  let response;
  try { response = measure(parseRequest(args, env)); } catch (err) {
    if (err instanceof MeasurementError) return rejection(err.code, err.detail);
    if (/overlay_covers_frame/.test(String(err && err.message))) return rejection("overlay_covers_frame");
    throw err;
  }
  const leak = payloadScan(response);
  return leak ? rejection("raw_payload_leak", leak) : response;
}

// Re-derive a response's receipt hash from its other fields.
export function verifyMeasurementReceipt(response) {
  if (!response || typeof response.receipt_sha256 !== "string") return false;
  const body = { ...response };
  delete body.receipt_sha256;
  try { return canonicalSha256(body) === response.receipt_sha256; } catch { return false; }
}
