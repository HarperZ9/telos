(function attachTelosEffectsProtocol(root) {
  const EFFECT_LAYERS = [
    { id: "retro", name: "Retro CGI", family: "cgi", claim: "Wireframes, horizon grids, shaded primitives, and measurement-friendly depth." },
    { id: "glitch", name: "Glitch", family: "corruption", claim: "Scanline offsets, channel splits, and deliberate corruption with readable state." },
    { id: "generative", name: "Generative", family: "procedural", claim: "Seeded particle fields and graph traces for repeatable variation." },
    { id: "plotter", name: "Plotter", family: "vector", claim: "Pen-plotter paths, hatch lines, and vector-like trace discipline." },
    { id: "pixelsort", name: "Pixel sort", family: "raster", claim: "Luminance-ranked row fragments that expose algorithmic image transforms." },
    { id: "poster", name: "Poster", family: "print", claim: "Typographic blocks and print-system composition for flagship presentation." },
    { id: "fractal", name: "Fractal", family: "recursive", claim: "Branching recursion and orbital geometry for sensitivity-map demos." },
    { id: "splat", name: "Gaussian splat", family: "radiance", claim: "Transparent ellipses that stand in for web-native splat fields." },
    { id: "clustered", name: "Clustered lights", family: "lighting", claim: "Forward-style screen clusters showing light bins and overlay visibility." },
    { id: "crt", name: "CRT scanlines", family: "display", claim: "Phosphor scanlines, vignette, and refresh artifacts with reduced-motion fallback." },
    { id: "chromatic", name: "Chromatic split", family: "optics", claim: "Channel-separated offsets for lens and signal stress tests." },
    { id: "dither", name: "Dither", family: "raster", claim: "Ordered threshold texture for low-bit export previews." },
    { id: "contour", name: "Contour map", family: "measurement", claim: "Iso-line fields for scientific overlays and scalar maps." },
    { id: "voronoi", name: "Voronoi cells", family: "partition", claim: "Nearest-seed regions for segmentation and route-field sketches." },
    { id: "ascii", name: "ASCII raster", family: "terminal", claim: "Glyph-based rasterization for TUI and log-friendly previews." },
    { id: "vector", name: "Vector field", family: "flow", claim: "Directional arrows for flow, gradient, and sensitivity overlays." },
    { id: "feedback", name: "Feedback trails", family: "temporal", claim: "Frame-to-frame echo paths for history and action-loop memory." },
    { id: "halftone", name: "Halftone press", family: "print", claim: "Dot-gain texture, screen tone, and poster-print tactility without hiding the receipt." },
    { id: "layout", name: "Editorial grid", family: "presentation", claim: "Crop marks, modular columns, hierarchy rails, and critique-friendly spacing checks." }
  ];

  const EFFECT_PRESETS = [
    { id: "all", name: "All layers", layers: EFFECT_LAYERS.map((layer) => layer.id), claim: "Full Telos Studio composition for presentation and stress testing." },
    { id: "scientific", name: "Scientific overlay", layers: ["clustered", "contour", "vector", "splat", "fractal"], claim: "Measurement overlays, flow probes, and radiance-style spatial evidence." },
    { id: "poster", name: "Poster system", layers: ["poster", "plotter", "dither", "chromatic"], claim: "Print-forward composition for README, GitHub, and launch assets." },
    { id: "flagship", name: "Flagship poster", layers: ["poster", "layout", "halftone", "plotter", "dither", "chromatic"], claim: "Five-tool presentation system with strong type hierarchy, replayable receipt data, and gallery-ready art direction." },
    { id: "terminal", name: "Terminal signal", layers: ["ascii", "crt", "dither", "glitch"], claim: "TUI-friendly preview language with fallback-readable artifacts." },
    { id: "radiance", name: "Radiance field", layers: ["splat", "clustered", "voronoi", "feedback", "chromatic"], claim: "Gaussian-splat and clustered-forward inspired scene diagnostics." },
    { id: "diagnostic", name: "Diagnostic stress", layers: ["retro", "contour", "vector", "pixelsort", "glitch", "crt"], claim: "Bias, drift, sensitivity, and render-path stress surface." }
  ];

  const RENDERER_PROFILES = [
    { id: "webgpu-splat-clustered", fallback: "webgl2-cluster-preview", claim: "WebGPU profile for splat fields, clustered lighting, and measured overlays." },
    { id: "webgl2-cluster-preview", fallback: "canvas2d-receipt-renderer", claim: "WebGL2 profile for clustered-light previews and geometry overlays." },
    { id: "canvas2d-receipt-renderer", fallback: "static-artifact-receipt", claim: "Canvas profile for live raster effects, receipt export, and broad browser fallback." },
    { id: "static-artifact-receipt", fallback: null, claim: "Static profile for CI, TUI, screen-reader, README, and JSON replay surfaces." }
  ];

  const layerIds = new Set(EFFECT_LAYERS.map((layer) => layer.id));
  const rendererProfileIds = new Set(RENDERER_PROFILES.map((profile) => profile.id));

  function stableStringify(value) {
    if (Array.isArray(value)) return `[${value.map(stableStringify).join(",")}]`;
    if (value && typeof value === "object") {
      return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${stableStringify(value[key])}`).join(",")}}`;
    }
    return JSON.stringify(value);
  }

  function hashStable(value) {
    const text = typeof value === "string" ? value : stableStringify(value);
    let hash = 2166136261;
    for (let i = 0; i < text.length; i++) {
      hash ^= text.charCodeAt(i);
      hash = Math.imul(hash, 16777619) >>> 0;
    }
    return `fnv1a:${hash.toString(16).padStart(8, "0")}`;
  }

  function clamp01(value, fallback) {
    const number = Number(value);
    if (!Number.isFinite(number)) return fallback;
    return Math.max(0, Math.min(1, number));
  }

  function normalizeLayerList(layers) {
    const source = Array.isArray(layers) ? layers : [];
    const normalized = [];
    for (const layer of source) {
      if (layerIds.has(layer) && !normalized.includes(layer)) normalized.push(layer);
    }
    return normalized.length ? normalized : EFFECT_LAYERS.map((layer) => layer.id);
  }

  function layersForMode(mode) {
    const preset = EFFECT_PRESETS.find((item) => item.id === mode);
    if (preset) return preset.layers;
    if (layerIds.has(mode)) return [mode];
    return EFFECT_PRESETS[0].layers;
  }

  function normalizeRendererProfile(profile) {
    const value = String(profile || "canvas2d-receipt-renderer");
    return rendererProfileIds.has(value) ? value : "canvas2d-receipt-renderer";
  }

  function rendererFallbackChain(profile) {
    const chain = [];
    let current = normalizeRendererProfile(profile);
    while (current && !chain.includes(current)) {
      chain.push(current);
      current = RENDERER_PROFILES.find((item) => item.id === current)?.fallback;
    }
    return chain;
  }

  function createSceneSpec(options = {}) {
    const mode = String(options.mode || "all");
    const layers = normalizeLayerList(options.layers || layersForMode(mode));
    const seed = Number.isInteger(options.seed) ? options.seed : Math.trunc(Number(options.seed) || 5505);
    const intensity = clamp01(options.intensity, 0.82);
    const density = clamp01(options.density, 0.64);
    const frame = Math.max(0, Math.trunc(Number(options.frame) || 0));
    const rendererProfile = normalizeRendererProfile(options.renderer_profile || options.rendererProfile);
    const args = { density, frame, intensity, layers, mode, seed };
    const args_hash = hashStable(args);
    const scene_id = `telos-scene-${hashStable({ layers, mode, seed }).slice(6, 18)}`;
    const action_intent_id = `telos-action-${hashStable({ args_hash, scene_id }).slice(6, 18)}`;
    const spec = {
      protocol: "project-telos.scene-spec/v1",
      scene_id,
      action_intent_id,
      mode,
      seed,
      layers,
      intensity,
      density,
      frame,
      args_hash,
      io: {
        host: String(options.host || "browser"),
        source: String(options.source || "telos-studio"),
        protocol_agnostic: true,
        embeddable: true,
        transports: ["html-canvas", "cli-json", "mcp-json-rpc", "app-bridge"]
      },
      privacy: {
        raw_payload_exported: false,
        evidence_boundary: "hashes verdicts timestamps redacted refs"
      },
      provenance: {
        engine: "project-telos.effects-engine/v1",
        layer_catalog: "project-telos.effects-catalog/v1",
        generated_at: String(options.generated_at || "runtime")
      },
      renderer: {
        capability_contract: "project-telos.rendering-capabilities/v1",
        selected_profile: rendererProfile,
        fallback_chain: rendererFallbackChain(rendererProfile),
        raw_gpu_trace_required: false,
        reduced_motion_supported: true
      },
      verification: {
        criterion_ref: "telos-effects-protocol/v1#renderable-scene",
        required_fields: ["action_intent_id", "args_hash", "spec_hash", "layers", "seed"],
        verdicts: ["MATCH", "DRIFT", "UNVERIFIABLE"]
      }
    };
    spec.spec_hash = hashStable(spec);
    return spec;
  }

  function createSceneReceipt(spec, runtime = {}) {
    const verification_verdict = String(runtime.verification_verdict || runtime.verdict || "MATCH");
    const frame = Math.max(0, Math.trunc(Number(runtime.frame ?? spec.frame) || 0));
    const receipt = {
      protocol: "project-telos.scene-receipt/v1",
      scene_id: spec.scene_id,
      action_intent_id: spec.action_intent_id,
      mode: spec.mode,
      layers: spec.layers,
      frame,
      args_hash: spec.args_hash,
      spec_hash: spec.spec_hash,
      decision_outcome: String(runtime.decision_outcome || "allow"),
      verification_verdict,
      verdict: verification_verdict,
      criterion_ref: String(runtime.criterion_ref || spec.verification?.criterion_ref || "telos-effects-protocol/v1#renderable-scene"),
      evidence_ref: String(runtime.evidence_ref || `receipt://scene/${spec.scene_id}/${spec.spec_hash.slice(6)}`),
      result_ref: String(runtime.result_ref || "canvas://effect-canvas"),
      result_hash: String(runtime.result_hash || hashStable({ frame, layers: spec.layers, scene_id: spec.scene_id })),
      render_ms: Math.max(0, Math.trunc(Number(runtime.render_ms) || 0)),
      reduced_motion: Boolean(runtime.reduced_motion),
      raw_payload_exported: false,
      evaluated_at: String(runtime.evaluated_at || "runtime"),
      previous_receipt_hash: runtime.previous_receipt_hash || null
    };
    receipt.receipt_hash = hashStable(receipt);
    return receipt;
  }

  function createReceiptChain(spec, previousReceipt, runtime = {}) {
    return createSceneReceipt(spec, {
      ...runtime,
      previous_receipt_hash: previousReceipt?.receipt_hash || null
    });
  }

  function encodeBase64Url(text) {
    if (typeof Buffer !== "undefined") return Buffer.from(text, "utf8").toString("base64url");
    const binary = encodeURIComponent(text).replace(/%([0-9A-F]{2})/g, (_, hex) => String.fromCharCode(Number.parseInt(hex, 16)));
    return btoa(binary).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/g, "");
  }

  function decodeBase64Url(token) {
    const normalized = String(token).replace(/-/g, "+").replace(/_/g, "/");
    const padded = normalized.padEnd(Math.ceil(normalized.length / 4) * 4, "=");
    if (typeof Buffer !== "undefined") return Buffer.from(padded, "base64").toString("utf8");
    const binary = atob(padded);
    return decodeURIComponent([...binary].map((char) => `%${char.charCodeAt(0).toString(16).padStart(2, "0")}`).join(""));
  }

  function encodeSceneSpec(spec) {
    return encodeBase64Url(stableStringify(spec));
  }

  function decodeSceneSpec(token) {
    return JSON.parse(decodeBase64Url(token));
  }

  const api = {
    EFFECT_LAYERS,
    EFFECT_PRESETS,
    RENDERER_PROFILES,
    createReceiptChain,
    createSceneReceipt,
    createSceneSpec,
    decodeSceneSpec,
    encodeSceneSpec,
    hashStable,
    normalizeLayerList,
    normalizeRendererProfile,
    rendererFallbackChain,
    stableStringify
  };

  root.TelosEffectsProtocol = api;
  if (typeof module !== "undefined" && module.exports) module.exports = api;
})(typeof globalThis !== "undefined" ? globalThis : window);
