(function attachTelosModelAdapter(root) {
  // Model-in-the-loop live generation for the Telos Studio showcase surface.
  //
  // This module ships the SHIPPABLE SLICE of standout feature 1 in
  // docs/PROJECT-TELOS-FEATURE-LEADERSHIP-2026-07-02.md: a person (or an
  // upstream agent) types a natural-language intent, a MODEL edits the scene
  // parameters, an Arena-style two-proposal pick renders both, and the WITNESS
  // step certifies the kept proposal into the existing scene receipt.
  //
  // The accountability layer is the floor: this feature RIDES ON the existing
  // scene-spec / scene-receipt substrate in effects-protocol.js. It does not
  // replace receipts. Every kept proposal joins a real MATCH/DRIFT receipt with
  // the intent recorded as an auditable, hashed edit trail.
  //
  // Live-model wiring is a spec (see docs/STUDIO-MODEL-IN-THE-LOOP.md). What is
  // shipped here is: (1) a model-adapter contract, (2) a deterministic offline
  // model stub that needs no network and no live model, (3) the Arena pick, and
  // (4) the witness-into-receipt step. The offline stub is deterministic so the
  // whole surface is headless-testable in Node.

  // Resolve the scene substrate lazily. In the browser, effects-protocol.js is a
  // classic <script> loaded before this file, so the global is already set. In
  // Node ESM, the CLI and the tests `await import("./effects-protocol.js")`
  // first, which sets the same global. Resolving lazily means this file attaches
  // in any load order and fails with a clear message only if the substrate is
  // genuinely absent at call time.
  function getProtocol() {
    const protocol = root.TelosEffectsProtocol;
    if (!protocol) {
      throw new Error("model-adapter: effects_protocol_required (import effects-protocol.js first)");
    }
    return protocol;
  }

  function createSceneSpec(options) {
    return getProtocol().createSceneSpec(options);
  }
  function createSceneReceipt(spec, runtime) {
    return getProtocol().createSceneReceipt(spec, runtime);
  }
  function hashStable(value) {
    return getProtocol().hashStable(value);
  }
  function stableStringify(value) {
    return getProtocol().stableStringify(value);
  }

  // ---- Strand parameter surface -------------------------------------------
  //
  // The scene-spec already carries seed / layers / intensity / density / frame.
  // Model intents like "tile at 5-fold" or "warmer palette" or "slower loop"
  // need a richer, named, sampleable parameter block. We add a `strand` block
  // with explicit bounds so an edit is always clamped and deterministic. The
  // browser renderer consumes these as documented in the spec; the contract and
  // bounds are the part that is shipped and tested here.

  const STRAND_PARAMS = [
    { key: "symmetry", label: "Symmetry fold", min: 1, max: 12, step: 1, default: 1, integer: true },
    { key: "palette_warmth", label: "Palette warmth", min: -1, max: 1, step: 0.05, default: 0 },
    { key: "loop_speed", label: "Loop speed", min: 0.1, max: 4, step: 0.05, default: 1 },
    { key: "contrast", label: "Contrast", min: 0, max: 1, step: 0.05, default: 0.5 }
  ];

  const STRAND_BY_KEY = new Map(STRAND_PARAMS.map((param) => [param.key, param]));

  function defaultStrand() {
    const strand = {};
    for (const param of STRAND_PARAMS) strand[param.key] = param.default;
    return strand;
  }

  function clampStrandValue(key, value) {
    const param = STRAND_BY_KEY.get(key);
    if (!param) return value;
    let number = Number(value);
    if (!Number.isFinite(number)) return param.default;
    number = Math.max(param.min, Math.min(param.max, number));
    if (param.integer) return Math.round(number);
    // Round to the parameter step so the edit is stable and reproducible.
    const rounded = Math.round(number / param.step) * param.step;
    // Guard against float dust so hashes stay stable across platforms.
    return Number(rounded.toFixed(6));
  }

  function normalizeStrand(input = {}) {
    const strand = defaultStrand();
    for (const param of STRAND_PARAMS) {
      if (input[param.key] !== undefined) {
        strand[param.key] = clampStrandValue(param.key, input[param.key]);
      }
    }
    return strand;
  }

  // ---- Intent parsing (the deterministic offline "model") -----------------
  //
  // A real model would read the intent and emit an edit. The offline stub is a
  // deterministic rule-based reader: the SAME intent string always produces the
  // SAME edit. This is what makes the surface headless-testable and lets a
  // receipt be re-derived. It is honestly labelled a stub, not a language model.

  const NUMBER_WORDS = {
    one: 1, two: 2, three: 3, four: 4, five: 5, six: 6,
    seven: 7, eight: 8, nine: 9, ten: 10, eleven: 11, twelve: 12
  };

  function extractFold(text) {
    // "5-fold", "5 fold", "five-fold", "fivefold", "at 5"
    const digit = text.match(/(\d+)\s*-?\s*fold/);
    if (digit) return Number(digit[1]);
    for (const [word, value] of Object.entries(NUMBER_WORDS)) {
      if (text.includes(`${word}-fold`) || text.includes(`${word}fold`) || text.includes(`${word} fold`)) {
        return value;
      }
    }
    const tileAt = text.match(/tile\s+(?:it\s+)?at\s+(\d+)/);
    if (tileAt) return Number(tileAt[1]);
    return null;
  }

  // Each rule reads the lowercased intent and, if it matches, returns a partial
  // edit. Rules are applied in listed order; later rules can layer on earlier
  // ones. Every rule is pure and deterministic.
  const INTENT_RULES = [
    {
      id: "symmetry.fold",
      test: (text) => extractFold(text) !== null,
      apply: (text, edit) => {
        edit.strand.symmetry = extractFold(text);
        edit.notes.push(`symmetry->${edit.strand.symmetry}-fold`);
      }
    },
    {
      id: "palette.warmer",
      test: (text) => /\b(warm(er|th)?|hot|amber|orange|sunset|golden)\b/.test(text),
      apply: (text, edit) => {
        const magnitude = /much|very|way|far/.test(text) ? 0.6 : 0.35;
        edit.strand.palette_warmth = clampStrandValue("palette_warmth", edit.strand.palette_warmth + magnitude);
        edit.notes.push(`palette_warmth+${magnitude}`);
      }
    },
    {
      id: "palette.cooler",
      test: (text) => /\b(cool(er)?|cold|blue|teal|ice|icy|winter)\b/.test(text),
      apply: (text, edit) => {
        const magnitude = /much|very|way|far/.test(text) ? 0.6 : 0.35;
        edit.strand.palette_warmth = clampStrandValue("palette_warmth", edit.strand.palette_warmth - magnitude);
        edit.notes.push(`palette_warmth-${magnitude}`);
      }
    },
    {
      id: "loop.slower",
      test: (text) => /\b(slow(er)?|calm(er)?|gentle|gentler|relax\w*|lazy)\b/.test(text),
      apply: (text, edit) => {
        const factor = /much|very|way|far/.test(text) ? 0.5 : 0.7;
        edit.strand.loop_speed = clampStrandValue("loop_speed", edit.strand.loop_speed * factor);
        edit.notes.push(`loop_speed*${factor}`);
      }
    },
    {
      id: "loop.faster",
      test: (text) => /\b(fast(er)?|quick(er)?|rapid|energetic|frantic)\b/.test(text),
      apply: (text, edit) => {
        const factor = /much|very|way|far/.test(text) ? 2 : 1.4;
        edit.strand.loop_speed = clampStrandValue("loop_speed", edit.strand.loop_speed * factor);
        edit.notes.push(`loop_speed*${factor}`);
      }
    },
    {
      id: "contrast.higher",
      test: (text) => /(high|more|bold|punch|crisp|sharp).{0,12}contrast|contrast.{0,12}(up|high|more)/.test(text),
      apply: (text, edit) => {
        edit.strand.contrast = clampStrandValue("contrast", edit.strand.contrast + 0.25);
        edit.notes.push("contrast+0.25");
      }
    },
    {
      id: "contrast.lower",
      test: (text) => /(low|less|soft|flat|muted).{0,12}contrast|contrast.{0,12}(down|low|less)/.test(text),
      apply: (text, edit) => {
        edit.strand.contrast = clampStrandValue("contrast", edit.strand.contrast - 0.25);
        edit.notes.push("contrast-0.25");
      }
    },
    {
      id: "density.denser",
      test: (text) => /\b(dense(r)?|busy|busier|packed|more detail|intricate)\b/.test(text),
      apply: (text, edit) => {
        edit.density = clamp01(edit.density + 0.2);
        edit.notes.push("density+0.2");
      }
    },
    {
      id: "density.sparser",
      test: (text) => /\b(spars(e|er)|clean(er)?|minimal|less detail|breathing room)\b/.test(text),
      apply: (text, edit) => {
        edit.density = clamp01(edit.density - 0.2);
        edit.notes.push("density-0.2");
      }
    },
    {
      id: "intensity.stronger",
      test: (text) => /\b(strong(er)?|intense|intenser|brighter|louder|bolder)\b/.test(text),
      apply: (text, edit) => {
        edit.intensity = clamp01(edit.intensity + 0.15);
        edit.notes.push("intensity+0.15");
      }
    },
    {
      id: "intensity.softer",
      test: (text) => /\b(soft(er)?|dimmer|quieter|subtle(r)?)\b/.test(text),
      apply: (text, edit) => {
        edit.intensity = clamp01(edit.intensity - 0.15);
        edit.notes.push("intensity-0.15");
      }
    }
  ];

  function clamp01(value) {
    const number = Number(value);
    if (!Number.isFinite(number)) return 0;
    return Number(Math.max(0, Math.min(1, number)).toFixed(6));
  }

  // Apply the rule set to a base scene, producing an edit descriptor. Pure and
  // deterministic: (intent, base) fully determine the output.
  function readIntent(intent, base) {
    const text = String(intent || "").toLowerCase().trim();
    const edit = {
      intensity: base.intensity,
      density: base.density,
      strand: normalizeStrand(base.strand),
      notes: [],
      matched_rules: []
    };
    for (const rule of INTENT_RULES) {
      if (rule.test(text)) {
        rule.apply(text, edit);
        edit.matched_rules.push(rule.id);
      }
    }
    edit.strand = normalizeStrand(edit.strand);
    return edit;
  }

  // ---- The adapter contract -----------------------------------------------
  //
  // Any model backend (the offline stub here, or a live model later) must
  // satisfy this contract: propose(intent, base) -> { edit } where edit carries
  // intensity, density, strand, and a notes/matched_rules trail. The Studio
  // calls the adapter through this one seam, so swapping the offline stub for a
  // live model is a spec-level change, not a rewrite.

  const ADAPTER_CONTRACT = {
    protocol: "project-telos.model-adapter/v1",
    seam: "propose(intent, baseScene) -> proposal",
    determinism_required_for: "offline",
    live_model: "specified, not shipped (see docs/STUDIO-MODEL-IN-THE-LOOP.md)",
    required_proposal_fields: [
      "adapter",
      "variant",
      "intent",
      "intent_hash",
      "scene_spec",
      "edit_delta",
      "matched_rules"
    ],
    parameter_surface: STRAND_PARAMS.map((param) => ({
      key: param.key,
      label: param.label,
      min: param.min,
      max: param.max,
      integer: Boolean(param.integer)
    })),
    accountability: "Kept proposals are witnessed into project-telos.scene-receipt/v1."
  };

  // The offline stub adapter. Two variants ("a" and "b") give the Arena its two
  // distinct proposals from ONE intent: variant "b" reads the intent against a
  // slightly reframed base (a seed nudge plus a light second reading) so the two
  // proposals differ while both honestly answer the same intent.
  function createOfflineAdapter(options = {}) {
    const id = String(options.id || "telos-offline-stub");
    return {
      id,
      kind: "offline-deterministic-stub",
      contract: ADAPTER_CONTRACT.protocol,
      propose(intent, baseScene, variant = "a") {
        return proposeEdit({ adapter: id, intent, baseScene, variant });
      }
    };
  }

  function normalizeBaseScene(baseScene = {}) {
    return {
      mode: baseScene.mode || "all",
      seed: Number.isInteger(baseScene.seed) ? baseScene.seed : 5505,
      layers: Array.isArray(baseScene.layers) ? baseScene.layers : undefined,
      intensity: Number.isFinite(baseScene.intensity) ? baseScene.intensity : 0.82,
      density: Number.isFinite(baseScene.density) ? baseScene.density : 0.64,
      frame: Number.isInteger(baseScene.frame) ? baseScene.frame : 0,
      strand: normalizeStrand(baseScene.strand)
    };
  }

  // Build one proposal: read the intent, apply the edit onto a scene-spec, and
  // fold the strand block into the spec so the whole thing is hashed as one
  // artifact. Variant "b" perturbs the seed and applies a second, lighter pass
  // so the two Arena proposals are genuinely different specs.
  function proposeEdit({ adapter, intent, baseScene, variant = "a" }) {
    const base = normalizeBaseScene(baseScene);
    const isB = String(variant) === "b";

    const edit = readIntent(intent, base);

    let seed = base.seed;
    if (isB) {
      // Variant B: a deterministic seed nudge derived from the intent, plus a
      // second lighter reading, so it explores an adjacent point in the space.
      seed = deriveVariantSeed(base.seed, intent);
      const second = readIntent(intent, { ...base, strand: edit.strand });
      // Blend: keep B slightly more restrained on loop_speed so it is distinct.
      edit.strand = normalizeStrand({
        ...second.strand,
        loop_speed: clampStrandValue(
          "loop_speed",
          (edit.strand.loop_speed + base.strand.loop_speed) / 2
        )
      });
    }

    const spec = createSceneSpec({
      mode: base.mode,
      layers: base.layers,
      seed,
      intensity: edit.intensity,
      density: edit.density,
      frame: base.frame,
      host: "telos-studio-model-loop",
      source: adapter
    });

    // Fold the strand parameter block and its intent provenance into the spec,
    // then re-hash so spec_hash covers the strand edit too.
    spec.strand = edit.strand;
    spec.model_edit = {
      adapter,
      variant: String(variant),
      matched_rules: edit.matched_rules,
      notes: edit.notes
    };
    spec.spec_hash = hashStable({ ...spec, spec_hash: undefined });

    const intent_hash = hashStable(String(intent || "").toLowerCase().trim());

    return {
      protocol: "project-telos.model-proposal/v1",
      adapter,
      variant: String(variant),
      intent: String(intent || ""),
      intent_hash,
      scene_spec: spec,
      edit_delta: strandDelta(base, edit),
      matched_rules: edit.matched_rules,
      notes: edit.notes
    };
  }

  function deriveVariantSeed(seed, intent) {
    const token = hashStable(`variant-b:${String(intent || "")}:${seed}`);
    const numeric = Number.parseInt(token.replace("fnv1a:", ""), 16);
    // Keep it a positive 31-bit integer, distinct from the base seed.
    const nudged = (seed + 1 + (numeric % 9973)) >>> 0;
    return nudged === seed ? seed + 1 : nudged;
  }

  function strandDelta(base, edit) {
    const delta = {
      intensity: Number((edit.intensity - base.intensity).toFixed(6)),
      density: Number((edit.density - base.density).toFixed(6)),
      strand: {}
    };
    for (const param of STRAND_PARAMS) {
      delta.strand[param.key] = Number(
        (edit.strand[param.key] - base.strand[param.key]).toFixed(6)
      );
    }
    return delta;
  }

  // ---- Arena: two proposals, one pick, one witness ------------------------
  //
  // The Arena runs the adapter twice (variant a and b) for a single intent,
  // giving two proposals that render side by side. The user picks one; the
  // WITNESS step certifies the kept proposal into a scene-receipt so "the model
  // made this" always arrives with "and here is the check it passed."

  function runArena(adapter, intent, baseScene = {}) {
    const proposalA = adapter.propose(intent, baseScene, "a");
    const proposalB = adapter.propose(intent, baseScene, "b");
    const arena_id = `telos-arena-${hashStable({
      a: proposalA.scene_spec.spec_hash,
      b: proposalB.scene_spec.spec_hash,
      intent: proposalA.intent_hash
    }).slice(6, 18)}`;
    return {
      protocol: "project-telos.model-arena/v1",
      arena_id,
      intent: String(intent || ""),
      intent_hash: proposalA.intent_hash,
      proposals: [proposalA, proposalB],
      differ: proposalA.scene_spec.spec_hash !== proposalB.scene_spec.spec_hash
    };
  }

  // Witness the kept proposal into the existing scene-receipt substrate. The
  // criterion the model did NOT author: the kept spec must be internally
  // consistent (strand within declared bounds, spec_hash covers the edit). If
  // the strand ever falls out of bounds or the hash does not recompute, the
  // verdict is DRIFT, not MATCH. This is the accountability floor the feature
  // rides on.
  function witnessPick(arena, keptVariant, runtime = {}) {
    const kept = arena.proposals.find((proposal) => proposal.variant === String(keptVariant));
    if (!kept) throw new Error("model-adapter: kept_variant_not_found");
    const rejected = arena.proposals.find((proposal) => proposal.variant !== String(keptVariant));

    const verdict = evaluateProposal(kept);

    const receipt = createSceneReceipt(kept.scene_spec, {
      verification_verdict: verdict,
      verdict,
      decision_outcome: verdict === "MATCH" ? "allow" : "hold",
      criterion_ref: "project-telos.model-adapter/v1#bounded-model-edit",
      evidence_ref: `receipt://model-arena/${arena.arena_id}/${kept.variant}`,
      result_ref: "canvas://effect-canvas",
      frame: kept.scene_spec.frame,
      reduced_motion: Boolean(runtime.reduced_motion),
      render_ms: Math.max(0, Math.trunc(Number(runtime.render_ms) || 0)),
      evaluated_at: String(runtime.evaluated_at || "runtime"),
      previous_receipt_hash: runtime.previous_receipt_hash || null
    });

    // Attach the model-in-the-loop provenance to the receipt as an auditable,
    // hashed edit trail, then re-hash so receipt_hash covers it.
    receipt.model_loop = {
      protocol: "project-telos.model-adapter/v1",
      adapter: kept.adapter,
      intent: kept.intent,
      intent_hash: kept.intent_hash,
      kept_variant: kept.variant,
      rejected_variant: rejected ? rejected.variant : null,
      arena_id: arena.arena_id,
      matched_rules: kept.matched_rules,
      edit_delta: kept.edit_delta,
      strand: kept.scene_spec.strand
    };
    receipt.receipt_hash = hashStable({ ...receipt, receipt_hash: undefined });

    return receipt;
  }

  // The criterion the model did not author. Returns MATCH / DRIFT / UNVERIFIABLE.
  function evaluateProposal(proposal) {
    const spec = proposal && proposal.scene_spec;
    if (!spec || !spec.strand) return "UNVERIFIABLE";
    // Strand must be within declared bounds.
    for (const param of STRAND_PARAMS) {
      const value = spec.strand[param.key];
      if (!Number.isFinite(value) || value < param.min || value > param.max) {
        return "DRIFT";
      }
      if (param.integer && !Number.isInteger(value)) return "DRIFT";
    }
    // spec_hash must recompute over the current spec (edit included).
    const recomputed = hashStable({ ...spec, spec_hash: undefined });
    if (recomputed !== spec.spec_hash) return "DRIFT";
    return "MATCH";
  }

  // ---- Summary (CLI) ------------------------------------------------------

  function summary(intent = "make the field tile at 5-fold, warmer palette, slower loop") {
    const adapter = createOfflineAdapter();
    const arena = runArena(adapter, intent, {});
    const receipt = witnessPick(arena, "a");
    const lines = [
      "Telos Studio Model-in-the-Loop (offline stub)",
      `intent    ${intent}`,
      `adapter   ${adapter.id} (${adapter.kind})`,
      `arena     ${arena.arena_id} differ=${arena.differ}`,
      `variant a ${describeStrand(arena.proposals[0].scene_spec.strand)}`,
      `variant b ${describeStrand(arena.proposals[1].scene_spec.strand)}`,
      `kept      a -> verdict ${receipt.verdict}`,
      `receipt   ${receipt.receipt_hash}`,
      "next      node demo/model-adapter.js --json"
    ];
    return `${lines.join("\n")}\n`;
  }

  function describeStrand(strand) {
    return `fold=${strand.symmetry} warmth=${strand.palette_warmth} loop=${strand.loop_speed} contrast=${strand.contrast}`;
  }

  const api = {
    ADAPTER_CONTRACT,
    STRAND_PARAMS,
    createOfflineAdapter,
    defaultStrand,
    normalizeStrand,
    clampStrandValue,
    readIntent,
    runArena,
    witnessPick,
    evaluateProposal,
    summary,
    stableStringify
  };

  root.TelosModelAdapter = api;
  if (typeof module !== "undefined" && module.exports) module.exports = api;
})(typeof globalThis !== "undefined" ? globalThis : window);
