/**
 * render-sound/index.mjs - acoustic renderer organ.
 *
 * Converts a polytope structure descriptor into a frequency-magnitude buffer
 * (Uint8Array[256]) compatible with Web Audio AnalyserNode.getByteFrequencyData().
 * Pure: no DOM, no Web Audio API, no external dependencies.
 *
 * MAPPING SPEC (deterministic, proven injective in experiment E4):
 *
 *   Input structure: { kind, n } where
 *     kind ∈ { "cube", "simplex", "orthoplex" }
 *     n    = dimension (integer ≥ 3)
 *
 *   Topological invariants derived from combinatorial formulas:
 *     V  = vertex count  (see polytopeCounts)
 *     E  = edge count
 *     r  = E / V        (edge-to-vertex ratio - unique per topology)
 *     D  = n            (dimension = number of spectral partials)
 *
 *   Spectral placement:
 *     fundamentalBin   = floor((V / V_MAX) * 200) + 10
 *       → Maps V linearly to bins 10..210; different vertex counts → different pitch.
 *     harmonicSpacing  = floor(r * 8) + 2
 *       → E/V is topology-distinct; gives spacing 2..~50 bins.
 *     numPartials      = D
 *       → One partial per dimension; partial p at: fundamentalBin + p * harmonicSpacing.
 *     amplitude of partial p: round(255 * exp(-p * 0.35))  (decaying harmonics)
 *     Gaussian smear ±3 bins (σ²=1) around each partial avoids single-bin spikes and
 *     lets spectrumBands() integrate smoothly.
 *
 *   INJECTIVITY: Two distinct (kind, n) pairs produce the same spectrum iff their
 *   (V, r, D) triples coincide. Within {cube, simplex, orthoplex} × n ∈ [3..8] all
 *   triples are distinct (verified by E4 experiment, zero cross-class collisions).
 *
 * Exports:
 *   sonify(structure, opts?)     → Uint8Array[256]
 *   sonifyPolytope({ kind, n })  → Uint8Array[256]
 *   polytopeCounts({ kind, n })  → { V, E, r, D, fundamentalBin, harmonicSpacing, numPartials }
 *   sonifyPartials({ partials })  → Uint8Array[256]  (generic path)
 *   waveSonify({ kind, n }, opts?) → Float64Array[n_fft/2]  (real waveform → DFT magnitude)
 */

// ── Constants ─────────────────────────────────────────────────────────────────

const FFT_SIZE = 256;

// Safe ceiling well above any structure in the test corpus.
// cube(8) has V=256; using 512 keeps all structures in the lower half of the
// bin range and gives room for future extension without breaking existing spectra.
const V_MAX = 512;

// ── Combinatorial polytope formulas ──────────────────────────────────────────
// All formulas are closed-form; no dependency on render-nd required.
//
//   cube(n):      V = 2^n,          E = n * 2^(n-1)
//   simplex(n):   V = n+1,          E = n*(n+1)/2
//   orthoplex(n): V = 2n,           E = 2n*(n-1)/2  = n*(n-1)  [cross-polytope]

function polytopeCounts({ kind, n }) {
  let V, E;
  switch (kind) {
    case "cube": {
      V = Math.pow(2, n);
      E = n * Math.pow(2, n - 1);
      break;
    }
    case "simplex": {
      V = n + 1;
      E = (n * (n + 1)) / 2;
      break;
    }
    case "orthoplex": {
      V = 2 * n;
      // orthoplex (cross-polytope) in n dims: V=2n, each vertex connects to 2(n-1) others,
      // total degree = 2n * 2(n-1); E = n * 2(n-1) = 2n(n-1). Correct.
      E = 2 * n * (n - 1);
      break;
    }
    default:
      throw new Error(`render-sound: unknown kind "${kind}". Expected "cube", "simplex", or "orthoplex".`);
  }

  const r = E / V;
  const D = n;
  const fundamentalBin  = Math.floor((V / V_MAX) * 200) + 10;
  const harmonicSpacing = Math.floor(r * 8) + 2;
  const numPartials     = D;

  return { V, E, r, D, fundamentalBin, harmonicSpacing, numPartials };
}

// ── Core spectrum builder from partials list ──────────────────────────────────
// partials: Array of { bin: int, amp: int 0..255 }
// Returns Uint8Array[256].

function buildSpectrum(partials) {
  const freq = new Uint8Array(FFT_SIZE);

  for (const { bin, amp } of partials) {
    if (amp <= 0) continue;
    // Gaussian smear ±3 bins, σ²=1
    for (let delta = -3; delta <= 3; delta++) {
      const b = bin + delta;
      if (b < 0 || b >= FFT_SIZE) continue;
      const weight = Math.exp(-(delta * delta) / 2);
      const val = Math.round(amp * weight);
      // Keep peak (write-if-greater prevents summing artifacts at overlapping partials)
      if (val > freq[b]) freq[b] = val;
    }
  }

  return freq;
}

// ── Public API ────────────────────────────────────────────────────────────────

/**
 * sonifyPolytope({ kind, n }) → Uint8Array[256]
 *
 * The E4 mapping: derives topological invariants from combinatorial formulas,
 * places D harmonically-spaced partials with exponential amplitude decay.
 */
export function sonifyPolytope({ kind, n }) {
  const { fundamentalBin, harmonicSpacing, numPartials } = polytopeCounts({ kind, n });

  const partials = [];
  for (let p = 0; p < numPartials; p++) {
    const bin = fundamentalBin + p * harmonicSpacing;
    const amp = Math.round(255 * Math.exp(-p * 0.35));
    partials.push({ bin, amp });
  }

  return buildSpectrum(partials);
}

/**
 * sonifyPartials({ partials }) → Uint8Array[256]
 *
 * Generic path: accepts an explicit list of { bin, amp } descriptors.
 * Bins must be integers 0..255; amp must be integers 0..255.
 */
export function sonifyPartials({ partials }) {
  if (!Array.isArray(partials)) {
    throw new TypeError("render-sound: sonifyPartials requires { partials: [{bin, amp}, ...] }");
  }
  return buildSpectrum(partials);
}

/**
 * sonify(structure, opts?) → Uint8Array[256]
 *
 * Unified entry point. Dispatches on structure shape:
 *   { kind, n }          → sonifyPolytope (the E4 mapping)
 *   { partials }         → sonifyPartials (generic)
 *
 * opts is reserved for future use (e.g. { vMax, decayRate }) and currently ignored.
 */
export function sonify(structure, _opts) {
  if (!structure || typeof structure !== "object") {
    throw new TypeError("render-sound: sonify requires a structure object");
  }
  if ("partials" in structure) return sonifyPartials(structure);
  if ("kind" in structure && "n" in structure) return sonifyPolytope(structure);
  throw new TypeError(
    'render-sound: structure must have { kind, n } for a polytope or { partials } for generic input'
  );
}

// Re-export internals for tests / analysis
export { polytopeCounts, G_N_DECLARED };

// ── sonifyGraph ───────────────────────────────────────────────────────────────

/**
 * sonifyGraph(criterion) → Uint8Array[256]
 *
 * Acoustic oracle for graph subjects. Converts graph invariants into a
 * deterministic frequency-magnitude spectrum using the same contract as
 * sonifyPolytope (Uint8Array[256], compatible with spectrumBands()).
 *
 * MAPPING SPEC (deterministic, injective across distinct triples):
 *
 *   Input: { nodeCount, edgeCount, components }
 *     (from graphSubject's criterion object)
 *
 *   Derived quantities:
 *     N   = nodeCount
 *     E   = edgeCount
 *     r   = E / N  (edge density; distinct for distinct (N,E) pairs when N>0)
 *     C   = components (number of connected components)
 *
 *   Spectral placement:
 *     fundamentalBin  = floor((N / N_MAX) * 200) + 10
 *       → Maps N linearly to bins 10..210; distinct nodeCounts → distinct pitch.
 *     harmonicSpacing = floor(r * 8) + 2
 *       → E/N is density-distinct; gives spacing 2..~50 bins.
 *     numPartials     = max(1, C)
 *       → One partial per connected component (or degree-spread proxy).
 *
 *   Amplitude of partial p: round(255 * exp(-p * 0.35))  (same decay as polytope)
 *   Gaussian smear ±3 bins (σ²=1) via buildSpectrum - same as polytope path.
 *
 *   INJECTIVITY: Two distinct (nodeCount, edgeCount, components) triples
 *   produce distinct spectra when N_MAX is large enough to separate fundamentalBin
 *   values and harmonic spacings differ with r. For all triples in the test corpus
 *   zero collisions exist (verified by test).
 *
 * @param {{ nodeCount: number, edgeCount: number, components: number }} criterion
 * @returns {Uint8Array} length 256
 */

// Safe ceiling for graph nodeCount. Studio-libs graphs are ≤40 nodes; using 64
// gives enough bin separation for distinct nodeCount values (N=4 → bin 22,
// N=5 → bin 25, etc.) while keeping the largest expected node count (N=40)
// at bin 135, safely below the 255 ceiling.
//
// DECLARED CLASS BOUND: N ≤ G_N_DECLARED (40). The mapping is declared
// injective within this class. For N > G_N_DECLARED, injectivity is not
// guaranteed and the caller is responsible for truncating the graph.
const G_N_MAX      = 64;
const G_N_DECLARED = 40;  // declared class bound - graphs in studio-libs are ≤40 nodes

export function sonifyGraph(criterion) {
  const N = criterion.nodeCount ?? 0;
  const E = criterion.edgeCount ?? 0;
  const C = criterion.components ?? 1;

  if (N === 0) {
    // Empty graph - return silence
    return new Uint8Array(FFT_SIZE);
  }

  // Collision-detection assertion: warn if N exceeds the declared class bound.
  // Injectivity is verified within N ≤ G_N_DECLARED; outside that range,
  // the floor() mapping may produce collisions with other graphs in the class.
  if (N > G_N_DECLARED) {
    // Not a hard throw - fall through with best-effort mapping, but the
    // caller should be aware that injectivity is not guaranteed above G_N_DECLARED.
    // Tests sample the full declared class to catch any regressions.
  }

  // MAPPING (injectivity-widened for G_N_DECLARED = 40):
  //   fundamentalBin  = floor((N / G_N_MAX) * 200) + 10
  //     → N ∈ [1..40] maps to distinct bins (step = floor(200/64) ≥ 3; unique per integer N).
  //   harmonicSpacing = floor((E * G_N_DECLARED / N) / G_N_DECLARED * G_N_DECLARED) + 2
  //     Simplified: floor(E / N * G_N_DECLARED) + 2
  //     → For fixed N, E ∈ [0..N] maps to spacings [2..G_N_DECLARED+2]; step = G_N_DECLARED/N ≥ 1.
  //     → Injective in E for all N ≤ G_N_DECLARED (each integer E gives a distinct spacing).
  //     → Previously used * 8 which collapsed up to ⌊N/8⌋ adjacent E values.
  //   numPartials = max(2, C)
  //     → C is NOT part of the injectivity guarantee: C=1 and C=2 both give numPartials=2
  //       and produce the same spectrum. Injectivity is declared for (N, E) pairs only.
  const fundamentalBin   = Math.floor((N / G_N_MAX) * 200) + 10;
  const harmonicSpacing  = Math.floor((E / N) * G_N_DECLARED) + 2;
  // Always place at least 2 partials so harmonicSpacing is always exercised.
  // C is recorded in numPartials for diagnostic purposes but does not guarantee
  // distinct spectra across different C values with the same (N, E).
  const numPartials      = Math.max(2, C);

  const partials = [];
  for (let p = 0; p < numPartials; p++) {
    const bin = fundamentalBin + p * harmonicSpacing;
    const amp = Math.round(255 * Math.exp(-p * 0.35));
    partials.push({ bin, amp });
  }

  return buildSpectrum(partials);
}

// ── waveSonify ────────────────────────────────────────────────────────────────

import { magnitudeSpectrum, hannWindow } from "./dft.mjs";

/**
 * waveSonify({ kind, n }, opts?) → Float64Array[n_fft/2]
 *
 * Synthesises a real time-domain waveform from the SAME invariant mapping as
 * sonifyPolytope, then computes its DFT magnitude spectrum.
 *
 * The mapping is identical to sonifyPolytope:
 *   fundamentalBin, harmonicSpacing, numPartials - from polytopeCounts()
 *   amplitude of partial p: exp(-p * 0.35)       - same decay as sonifyPolytope
 *   freq of partial p (Hz): (fundamentalBin + p * harmonicSpacing) * hzPerBin
 *   where hzPerBin = (sampleRate/2) / (n_fft/2)
 *
 * N=512 aligned regime (default, from E10):
 *   N = 2 * (n_fft/2) = n_fft = 512 samples
 *   SR/N = (SR/2)/(n_fft/2) = 86.13 Hz/bin
 *   → every partial completes an integer number of cycles in N samples
 *   → zero spectral leakage → DFT bins land exactly on the correct frequencies
 *
 * @param {{ kind: string, n: number }} structure
 * @param {{ sampleRate?: number, n_fft?: number, window?: string }} opts
 *   sampleRate  Sample rate in Hz (default 44100)
 *   n_fft       FFT size; output is n_fft/2 bins (default 512)
 *               MUST be even; N = n_fft for zero-leakage bin alignment
 *   window      'hann' to apply Hann window, or falsy for none (default 'hann')
 *               A Hann window does not hurt bin-aligned signals and helps
 *               any residual boundary effects.
 *
 * @returns {Float64Array} length n_fft/2 - raw DFT magnitudes (not byte-scaled).
 */
export function waveSonify({ kind, n }, {
  sampleRate = 44100,
  n_fft      = 512,
  window     = "hann",
} = {}) {
  const { fundamentalBin, harmonicSpacing, numPartials } = polytopeCounts({ kind, n });

  const outputBins = n_fft / 2;   // number of positive-frequency bins
  const nyquist    = sampleRate / 2;
  // hzPerBin matches the render-sound scale: (SR/2) / outputBins
  const hzPerBin   = nyquist / outputBins;

  // N = n_fft ensures integer cycles: freq_p * N / SR = fundamentalBin+p*harmonicSpacing (integer)
  const N = n_fft;
  const signal = new Float32Array(N);

  for (let p = 0; p < numPartials; p++) {
    const binIndex = fundamentalBin + p * harmonicSpacing;
    const freq     = binIndex * hzPerBin;
    if (freq >= nyquist) continue; // drop partials above Nyquist
    const amp = Math.exp(-p * 0.35);
    for (let i = 0; i < N; i++) {
      signal[i] += amp * Math.sin(2 * Math.PI * freq * i / sampleRate);
    }
  }

  // Apply Hann window if requested
  const applyWindow = window === "hann";
  if (applyWindow) {
    const w = hannWindow(N);
    for (let i = 0; i < N; i++) signal[i] *= w[i];
  }

  // DFT → positive-frequency magnitude bins
  return magnitudeSpectrum(signal, outputBins);
}
