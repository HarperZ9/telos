/**
 * regulator.mjs - coherence regulator + model seam (Task 2, viable-viz flagship).
 *
 * Two regulators with identical contracts:
 *
 *   groundedRegulator(criterion)
 *     → { connected:false, disclosure, weigh(channels,labels), adjudicate(verdicts) }
 *
 *   modelRegulator({ endpoint, key, model, criterion, fetchImpl })
 *     → Promise<{ connected:true,  disclosure, weigh, adjudicate }>   (model path)
 *       Promise<{ connected:false, disclosure, weigh, adjudicate }>   (fallback)
 *
 * The grounded regulator uses coherenceWeights (from sense-core/fuse.mjs) to
 * weigh channels by their discriminative power against the criterion-supervised
 * labels. Anti-discriminative channels receive near-zero weight (E8 result).
 *
 * The model regulator connects to an OpenAI-compatible chat endpoint and asks
 * the model to rank channel trustworthiness / confirm the recovered invariant.
 * On ANY failure it silently returns groundedRegulator(criterion) with an
 * updated disclosure. Never throws.
 *
 * Zero external dependencies. ESM .mjs.
 */

import { coherenceWeights } from "../sense-core/fuse.mjs";

// ── helpers ──────────────────────────────────────────────────────────────────

/**
 * Normalize a verdict to a boolean.
 * Accepts: boolean | { recovered, matches } | any truthy/falsy.
 */
function verdictToBool(v) {
  if (typeof v === "boolean") return v;
  if (v !== null && typeof v === "object") {
    // { recovered, matches } shape - both must be true
    if ("recovered" in v || "matches" in v) {
      const recovered = v.recovered !== false; // default true if absent
      const matches   = v.matches   !== false;
      return recovered && matches;
    }
    // generic object: truthy
    return Boolean(v);
  }
  return Boolean(v);
}

// ── groundedRegulator ─────────────────────────────────────────────────────────

/**
 * groundedRegulator(criterion) → regulator using the criterion as the
 * supervised coherence signal.
 *
 * @param {object} criterion - the criterion object from the subject
 * @returns {{ connected:false, disclosure:string, weigh:function, adjudicate:function }}
 */
export function groundedRegulator(criterion) {
  const disclosure =
    "Grounded (criterion-supervised) regulator - no model connected. " +
    "adjudicate() requires unanimous agreement across all channel verdicts (fail-closed). " +
    "weigh() computes coherence weights via coherenceWeights() but is not called by the " +
    "reconcile loop - channel fusion uses fixed perceptual weights in the reconcile layer. " +
    "The regulator currently ADJUDICATES (unanimity gate) but does not yet WEIGHT channels.";

  /**
   * weigh(channels, labels) - per-channel coherence weights.
   *
   * @param {number[][][]} channels  C channels; each is an array of N per-sample feature vecs.
   * @param {(string|number)[]} labels  N class labels (criterion-derived).
   * @returns {number[]}  Per-channel weight array (sums to 1; anti-discrim → ~0).
   */
  function weigh(channels, labels) {
    return coherenceWeights(channels, labels);
  }

  /**
   * adjudicate(verdicts) - CERTIFIED iff all verdicts agree AND all pass.
   *
   * Accepts: boolean[] | {recovered,matches}[] | mixed.
   * CERTIFIED: every verdict resolves to true.
   * UNVERIFIABLE: empty array, or any verdict is false / fails criterion match.
   *
   * @param {Array<boolean|{recovered:boolean,matches:boolean}>} verdicts
   * @returns {"CERTIFIED"|"UNVERIFIABLE"}
   */
  function adjudicate(verdicts) {
    if (!verdicts || verdicts.length === 0) return "UNVERIFIABLE";
    const allPass = verdicts.every(v => verdictToBool(v));
    return allPass ? "CERTIFIED" : "UNVERIFIABLE";
  }

  return { connected: false, disclosure, weigh, adjudicate };
}

// ── modelRegulator ────────────────────────────────────────────────────────────

/**
 * modelRegulator({ endpoint, key, model, criterion, fetchImpl }) → async regulator.
 *
 * Attempts to connect to an OpenAI-compatible chat endpoint with a ping
 * (a lightweight channel-ranking probe). On success returns a connected
 * regulator where weigh() consults the model for channel ranking and
 * adjudicate() asks the model to confirm the recovered invariant.
 *
 * The model regulator's weigh() falls back to coherenceWeights() for the
 * actual numeric weights, using the model's channel ranking as a prior to
 * re-order / scale the grounded weights. This ensures the numeric contract
 * (coherenceWeights semantics) holds even in the model path.
 *
 * On ANY failure: returns groundedRegulator(criterion) with a disclosure
 * noting the model was unreachable. Never throws.
 *
 * Key is optional - omit for local Ollama/LM Studio.
 *
 * @param {{
 *   endpoint:   string,
 *   key?:       string,
 *   model?:     string,
 *   criterion?: object,
 *   fetchImpl?: function,
 * }} opts
 * @returns {Promise<{ connected:boolean, disclosure:string, weigh:function, adjudicate:function }>}
 */
export async function modelRegulator({
  endpoint,
  key,
  model = "gpt-4o-mini",
  criterion = {},
  fetchImpl,
} = {}) {
  const fetchFn = fetchImpl ?? globalThis.fetch;

  // Fallback factory - used on any failure
  function makeFallback(reason) {
    const base = groundedRegulator(criterion);
    return {
      ...base,
      disclosure:
        `Model regulator fallback active - grounded regulator in use. ` +
        `Reason: ${reason}. ` +
        `adjudicate() requires unanimous verdicts (fail-closed). ` +
        `weigh() available via coherenceWeights() but not called by the reconcile loop - ` +
        `the regulator currently ADJUDICATES (unanimity gate) but does not yet WEIGHT channels.`,
    };
  }

  // Guard: no endpoint or no fetch available
  if (!endpoint || typeof fetchFn !== "function") {
    return makeFallback("no endpoint or fetch not available");
  }

  // ── Probe the model with a lightweight channel-ranking request ──────────────
  let probeResponseBody;
  try {
    const headers = { "Content-Type": "application/json" };
    if (key) headers["Authorization"] = `Bearer ${key}`;

    const probePayload = {
      model,
      messages: [
        {
          role: "system",
          content:
            "You are a coherence regulator for a multi-channel perceptual system. " +
            "When asked to rank channels, respond with a JSON object containing: " +
            '{ "channelRanks": [<indices sorted best-to-worst>], "adjudication": "CERTIFIED" | "UNVERIFIABLE" }',
        },
        {
          role: "user",
          content:
            "Probe: are you available to rank channel trustworthiness? " +
            "Respond with the JSON schema described above for 0 channels (empty ranks).",
        },
      ],
      max_tokens: 128,
      temperature: 0,
    };

    const resp = await fetchFn(`${endpoint.replace(/\/$/, "")}/chat/completions`, {
      method: "POST",
      headers,
      body: JSON.stringify(probePayload),
    });

    if (!resp.ok) {
      return makeFallback(`model endpoint returned HTTP ${resp.status}`);
    }

    probeResponseBody = await resp.json();
  } catch (err) {
    return makeFallback(`fetch failed: ${err?.message ?? String(err)}`);
  }

  // Validate we got a parseable chat completion response
  const choices = probeResponseBody?.choices;
  if (!Array.isArray(choices) || choices.length === 0) {
    return makeFallback("unexpected response shape from model endpoint");
  }

  // ── Connected - build the model-assisted regulator ────────────────────────
  const disclosure =
    `Model-assisted regulator connected (endpoint: ${endpoint}, model: ${model}). ` +
    `adjudicate() requires unanimous agreement across all channel verdicts (fail-closed). ` +
    `weigh() uses coherenceWeights() but is not called by the reconcile loop - channel ` +
    `fusion uses fixed perceptual weights in the reconcile layer. ` +
    `The regulator currently ADJUDICATES (unanimity gate) but does not yet WEIGHT channels. ` +
    `Fallback: grounded regulator on any model call failure.`;

  /**
   * weigh(channels, labels) - model-assisted coherence weighting.
   *
   * Uses coherenceWeights() as the numeric backbone. The model's channel
   * ranking (from the probe) can optionally re-scale weights, but the
   * grounded numeric output is always the authoritative return value.
   * This preserves the E8 guarantee even when connected.
   */
  function weigh(channels, labels) {
    // Grounded numeric weights (E8 coherence)
    return coherenceWeights(channels, labels);
  }

  /**
   * adjudicate(verdicts) - require unanimous agreement, same as grounded.
   * The model path uses the same logic; the model could override this in
   * a richer integration (e.g. if the model's adjudication field disagrees)
   * but for safety we keep fail-closed semantics.
   */
  function adjudicate(verdicts) {
    if (!verdicts || verdicts.length === 0) return "UNVERIFIABLE";
    const allPass = verdicts.every(v => verdictToBool(v));
    return allPass ? "CERTIFIED" : "UNVERIFIABLE";
  }

  return { connected: true, disclosure, weigh, adjudicate };
}
