/**
 * dft.mjs - zero-dependency DFT for render-sound.
 *
 * Promoted from C:/dev/scratch/viable-viz-sim/E10-waveform/dft.mjs
 * after E10 confirmed zero-leakage at N=512 (bin-aligned) regime.
 *
 * Self-test cases (originally from prototype, inline as comments below each function):
 *
 *   TEST 1: single sine at bin k peaks at bin k
 *   TEST 2: sum of two sines - top-2 bins match both frequencies
 *   TEST 3: DC signal (all-ones) peaks at bin 0
 *   TEST 4: Hann window preserves peak bin for a bin-aligned sine
 *   TEST 5: non-bin-aligned sine - dominant peak lands on the nearest integer bin
 *
 * Exports:
 *   dft(samples)                   → { re, im, mag }       (O(N²), safe for N ≤ 2048)
 *   hannWindow(N)                  → Float64Array[N]
 *   magnitudeSpectrum(samples, bins, opts?)  → Float64Array[bins]
 *   selfTest()                     → boolean (true = all pass)
 */

// ── Core DFT ──────────────────────────────────────────────────────────────────

/**
 * dft(samples) → { re: Float64Array, im: Float64Array, mag: Float64Array }
 *
 * Full N-point DFT of real-valued `samples`. Returns all N complex coefficients
 * and their magnitudes.  O(N²) - intentional; sufficient for N ≤ 2048.
 *
 * Self-test note: for a pure sine at integer bin k (N samples, exactly k cycles),
 * mag[k] = N/2 and mag[N-k] = N/2; all other bins are zero (exact, no leakage).
 */
export function dft(samples) {
  const N = samples.length;
  const re  = new Float64Array(N);
  const im  = new Float64Array(N);
  const mag = new Float64Array(N);

  const TWO_PI_OVER_N = (2 * Math.PI) / N;

  for (let k = 0; k < N; k++) {
    let sumRe = 0, sumIm = 0;
    for (let n = 0; n < N; n++) {
      const angle = TWO_PI_OVER_N * k * n;
      sumRe += samples[n] * Math.cos(angle);
      sumIm -= samples[n] * Math.sin(angle);
    }
    re[k]  = sumRe;
    im[k]  = sumIm;
    mag[k] = Math.sqrt(sumRe * sumRe + sumIm * sumIm);
  }

  return { re, im, mag };
}

// ── Hann window ───────────────────────────────────────────────────────────────

/**
 * hannWindow(N) → Float64Array[N]
 *
 * w[n] = 0.5 * (1 − cos(2πn/(N−1)))
 *
 * Reduces spectral leakage for non-bin-aligned sinusoids. Not needed when
 * all frequencies are integer multiples of SR/N (the N=512 aligned regime).
 */
export function hannWindow(N) {
  const w = new Float64Array(N);
  for (let n = 0; n < N; n++) {
    w[n] = 0.5 * (1 - Math.cos((2 * Math.PI * n) / (N - 1)));
  }
  return w;
}

// ── Magnitude spectrum ────────────────────────────────────────────────────────

/**
 * magnitudeSpectrum(samples, bins?, opts?) → Float64Array[bins]
 *
 * Returns the positive-frequency half of the DFT magnitude, NOT normalised to
 * 0-255 (use raw float magnitudes so callers can apply their own scale or
 * compare numerically).  `bins` defaults to floor(N/2).
 *
 * @param {number[]|Float32Array|Float64Array} samples  Real-valued signal.
 * @param {number}  [bins]   Output bin count (≤ N/2).  Defaults to N/2.
 * @param {object}  [opts]
 *   @param {boolean} opts.window  Apply Hann window before DFT (default false).
 *
 * Relationship to render-sound bin scale:
 *   When N = 2 * FFT_BINS (= 512 with FFT_BINS=256), magnitudeSpectrum returns
 *   exactly FFT_BINS bins and the bin resolution SR/N = (SR/2)/FFT_BINS matches
 *   the render-sound scale - zero leakage for all waveSonify partials.
 *
 * Self-test notes (prototype tests 1-5 verified at N=64):
 *   - Single sine at bin k  → mag[k] = N/2 (dominant peak at bin k)
 *   - Two sines at k1, k2   → two distinct peaks
 *   - DC (all-ones)         → dominant peak at bin 0
 *   - Hann + bin-aligned    → peak bin unchanged
 *   - Non-aligned sine      → peak at nearest integer bin (leakage spreads but doesn't flip the peak)
 */
export function magnitudeSpectrum(samples, bins, opts = {}) {
  const N = samples.length;
  const outBins = bins != null ? bins : Math.floor(N / 2);

  let windowed = samples;
  if (opts.window) {
    const w = hannWindow(N);
    const buf = new Float64Array(N);
    for (let i = 0; i < N; i++) buf[i] = samples[i] * w[i];
    windowed = buf;
  }

  const { mag } = dft(windowed);

  const half = Math.min(outBins, Math.floor(N / 2));
  const out = new Float64Array(outBins); // extra slots stay 0
  for (let k = 0; k < half; k++) out[k] = mag[k];

  return out;
}

// ── Self-test (importable + standalone) ──────────────────────────────────────

/**
 * selfTest() → boolean
 *
 * Runs the 5 prototype self-tests inline.  Returns true if all pass.
 * Can also be called standalone: node dft.mjs
 */
export function selfTest() {
  const N = 64;

  // TEST 1: single sine at bin f1 peaks at bin f1
  const f1 = 8;
  const sine1 = new Float64Array(N);
  for (let i = 0; i < N; i++) sine1[i] = Math.sin(2 * Math.PI * f1 * i / N);
  const ms1 = magnitudeSpectrum(sine1, N / 2);
  let peakBin1 = 0;
  for (let k = 1; k < N / 2; k++) if (ms1[k] > ms1[peakBin1]) peakBin1 = k;
  const pass1 = peakBin1 === f1;

  // TEST 2: sum of sines at f2a and f2b - top-2 bins match both
  const f2a = 4, f2b = 12;
  const sine2 = new Float64Array(N);
  for (let i = 0; i < N; i++) {
    sine2[i] = 0.6 * Math.sin(2 * Math.PI * f2a * i / N) +
               0.4 * Math.sin(2 * Math.PI * f2b * i / N);
  }
  const ms2 = magnitudeSpectrum(sine2, N / 2);
  const top2 = Array.from({ length: N / 2 }, (_, k) => [k, ms2[k]])
    .sort((a, b) => b[1] - a[1]).slice(0, 2).map(x => x[0]).sort((a, b) => a - b);
  const pass2 = top2[0] === f2a && top2[1] === f2b;

  // TEST 3: DC at bin 0
  const dc = new Float64Array(N).fill(1.0);
  const msDC = magnitudeSpectrum(dc, N / 2);
  let peakDC = 0;
  for (let k = 1; k < N / 2; k++) if (msDC[k] > msDC[peakDC]) peakDC = k;
  const pass3 = peakDC === 0;

  // TEST 4: Hann window preserves peak bin for bin-aligned sine
  const sine4 = new Float64Array(N);
  for (let i = 0; i < N; i++) sine4[i] = Math.sin(2 * Math.PI * f1 * i / N);
  const ms4 = magnitudeSpectrum(sine4, N / 2, { window: true });
  let peakBin4 = 0;
  for (let k = 1; k < N / 2; k++) if (ms4[k] > ms4[peakBin4]) peakBin4 = k;
  const pass4 = peakBin4 === f1;

  // TEST 5: non-bin-aligned sine - dominant peak at nearest integer bin
  const fNonAligned = 5.5;
  const sineNA = new Float64Array(N);
  for (let i = 0; i < N; i++) sineNA[i] = Math.sin(2 * Math.PI * fNonAligned * i / N);
  const msNA = magnitudeSpectrum(sineNA, N / 2);
  let peakNA = 0;
  for (let k = 1; k < N / 2; k++) if (msNA[k] > msNA[peakNA]) peakNA = k;
  const pass5 = peakNA === Math.round(fNonAligned) || peakNA === Math.floor(fNonAligned);

  return pass1 && pass2 && pass3 && pass4 && pass5;
}

// Standalone runner
if (import.meta.url === (
  typeof process !== "undefined" && process.argv[1]
    ? new URL("file://" + process.argv[1].replace(/\\/g, "/")).href
    : null
)) {
  const ok = selfTest();
  console.log(ok ? "dft.mjs: ALL PASS" : "dft.mjs: SOME FAIL");
  process.exit(ok ? 0 : 1);
}
