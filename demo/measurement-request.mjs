// measurement-request.mjs: parse and check a `project-telos.measurement-request/v2` request.
//
// The v2 measurement contract lets a caller hand Telos its own image as raw 8-bit RGBA, inline as base64
// or as a file under a root the server operator configured (TELOS_MEASUREMENT_ROOTS). Every refusal is a
// MeasurementError with a failure code; nothing here echoes the caller's bytes or path back.
import { readFileSync, realpathSync, statSync } from "node:fs";
import path from "node:path";

export const REQUEST_SCHEMA = "project-telos.measurement-request/v2";
export const MAX_PIXELS = 16777216;
const B64 = /^[A-Za-z0-9+/]*={0,2}$/;
const KEYS = new Set(["image", "declared", "layers", "n", "roi", "resample", "overlays", "overlays_drawn", "run_id", "frame_id"]);
const COLOUR_SPACES = new Set(["srgb", "display-p3", "rec2020", "unknown"]);
const ALPHAS = new Set(["none", "straight", "premultiplied"]);
const LAYER_IDS = ["L0", "L1", "L2", "L3"];

export class MeasurementError extends Error {
  constructor(code, detail = "") {
    super(`${code}${detail ? `: ${detail}` : ""}`);
    this.code = code;
    this.detail = detail;
  }
}

const fail = (code, detail) => { throw new MeasurementError(code, detail); };
const isInt = (v, lo, hi) => Number.isInteger(v) && v >= lo && v <= hi;

function decodeBase64(text, what) {
  if (typeof text !== "string" || text.length % 4 !== 0 || !B64.test(text)) fail("request_invalid", `${what} is not base64`);
  return new Uint8Array(Buffer.from(text, "base64"));
}

// Real path of `p` when it lies inside an allowed root, after every symlink and junction.
function sameOrInside(child, root) {
  const norm = (s) => (process.platform === "win32" ? s.toLowerCase() : s);
  const c = norm(child), r = norm(root.endsWith(path.sep) ? root : root + path.sep);
  return c === norm(root) || c.startsWith(r);
}

export function resolveAllowedPath(p, env = process.env) {
  if (typeof p !== "string" || p.length === 0) fail("path_outside_allowed_root", "empty path");
  if (/^[\\/]{2}/.test(p)) fail("path_outside_allowed_root", "UNC or device path");
  if (!path.isAbsolute(p)) fail("path_outside_allowed_root", "relative path");
  const roots = String(env.TELOS_MEASUREMENT_ROOTS || "").split(path.delimiter).filter(Boolean)
    .flatMap((r) => { try { return [realpathSync.native(r)]; } catch { return []; } });
  if (!roots.length) fail("path_outside_allowed_root", "no allowed roots configured");
  const lexical = path.resolve(p);
  if (!roots.some((r) => sameOrInside(lexical, r)) && !roots.some((r) => sameOrInside(lexical, path.resolve(r)))) {
    fail("path_outside_allowed_root", "outside every root");
  }
  let real;
  try { real = realpathSync.native(lexical); } catch { fail("image_decode_failed", "file not readable"); }
  if (!roots.some((r) => sameOrInside(real, r))) fail("path_outside_allowed_root", "link leaves the root");
  return real;
}

function readImage(image, env) {
  if (!image || typeof image !== "object") fail("request_invalid", "image missing");
  const { width, height } = image;
  if (!isInt(width, 1, MAX_PIXELS) || !isInt(height, 1, MAX_PIXELS)) fail("request_invalid", "width and height must be positive integers");
  if (width * height > MAX_PIXELS) fail("image_too_large");
  const hasRgba = "rgba" in image, hasPath = "path" in image;
  if (hasRgba === hasPath) fail("request_invalid", "give exactly one of rgba or path");
  let bytes;
  if (hasRgba) bytes = decodeBase64(image.rgba, "rgba");
  else {
    const real = resolveAllowedPath(image.path, env);
    if (statSync(real).size > MAX_PIXELS * 4) fail("image_too_large");
    bytes = new Uint8Array(readFileSync(real));
  }
  if (bytes.length !== width * height * 4) fail("pixel_dimensions_mismatch");
  return { px: bytes, w: width, h: height, decoder: "raw-rgba8", source: hasRgba ? "inline" : "path" };
}

// Un-premultiply in integers: c' = min(255, floor((c * 255 + floor(a / 2)) / a)), 0 when a = 0.
function unpremultiply(px) {
  const out = new Uint8Array(px.length);
  for (let i = 0; i < px.length; i += 4) {
    const a = px[i + 3];
    for (let k = 0; k < 3; k++) out[i + k] = a === 0 ? 0 : Math.min(255, Math.floor((px[i + k] * 255 + Math.floor(a / 2)) / a));
    out[i + 3] = a;
  }
  return out;
}

function crop(px, w, h, roi) {
  const { x, y, w: rw, h: rh } = roi;
  if (!isInt(x, 0, w - 1) || !isInt(y, 0, h - 1) || !isInt(rw, 1, w - x) || !isInt(rh, 1, h - y)) fail("request_invalid", "roi outside the image");
  const out = new Uint8Array(rw * rh * 4);
  for (let r = 0; r < rh; r++) out.set(px.subarray(((y + r) * w + x) * 4, ((y + r) * w + x + rw) * 4), r * rw * 4);
  return out;
}

// Parse a request into decoded pixels and options. Throws MeasurementError.
export function parseRequest(args, env = process.env) {
  if (!args || typeof args !== "object" || Array.isArray(args)) fail("request_invalid", "arguments must be an object");
  for (const k of Object.keys(args)) if (!KEYS.has(k)) fail("request_invalid", `unknown field ${k}`);
  const declared = { colour_space: "unknown", alpha: "straight", bit_depth: 8, ...(args.declared || {}) };
  for (const k of Object.keys(declared)) if (!["colour_space", "alpha", "bit_depth"].includes(k)) fail("request_invalid", `unknown declared field ${k}`);
  if (!COLOUR_SPACES.has(declared.colour_space)) fail("request_invalid", "colour_space");
  if (!ALPHAS.has(declared.alpha)) fail("request_invalid", "alpha");
  if (declared.bit_depth !== 8) fail("unsupported_bit_depth");
  const layers = args.layers ?? (args.overlays?.length ? LAYER_IDS : ["L0", "L1", "L2"]);
  if (!Array.isArray(layers) || !layers.length || layers.some((l) => !LAYER_IDS.includes(l))) fail("request_invalid", "layers");
  const n = args.n ?? 32;
  if (!isInt(n, 1, 64)) fail("request_invalid", "n must be an integer from 1 to 64");
  const img = readImage(args.image, env);
  let px = declared.alpha === "premultiplied" ? unpremultiply(img.px) : img.px;
  const alphaStep = declared.alpha === "premultiplied" ? "unpremultiplied-int" : declared.alpha === "straight" ? "alpha-ignored" : "none";
  let { w, h } = img;
  const overlays = (args.overlays || []).map((o, i) => {
    if (!o || typeof o.id !== "string" || !/^[A-Za-z0-9_.-]{1,32}$/.test(o.id)) fail("request_invalid", `overlay ${i} id`);
    const mask = decodeBase64(o.mask, `overlay ${i} mask`);
    if (mask.length !== w * h) fail("pixel_dimensions_mismatch", `overlay ${i} mask`);
    return { id: o.id, mask };
  });
  if (overlays.length && (args.roi || args.resample)) fail("request_invalid", "overlays cannot be combined with roi or resample in v2");
  if (args.overlays_drawn !== undefined && typeof args.overlays_drawn !== "boolean") fail("request_invalid", "overlays_drawn");
  let roi = null;
  if (args.roi) { px = crop(px, w, h, args.roi); roi = { x: args.roi.x, y: args.roi.y, w: args.roi.w, h: args.roi.h }; w = roi.w; h = roi.h; }
  let resample = null;
  if (args.resample) {
    const { long_edge: le, filter } = args.resample;
    if (filter !== "area-linear" || !isInt(le, 1, 4096)) fail("request_invalid", "resample needs filter area-linear and long_edge 1 to 4096");
    resample = { long_edge: le, filter };
  }
  const str = (v, d) => (v === undefined ? d : typeof v === "string" && v.length <= 128 ? v : fail("request_invalid", "run_id and frame_id are short strings"));
  return {
    px, w, h, decoder: img.decoder, source: img.source, declared, alphaStep, layers, n, roi, resample, overlays,
    overlaysDrawn: args.overlays_drawn === true, runId: str(args.run_id, "telos.measurement.v2"), frameId: str(args.frame_id, "frame:0"),
  };
}
