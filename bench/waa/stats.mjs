// Statistics the benchmark plan names (DESIGN 7.4): a Wilson 95% interval for
// each arm's success rate and an exact McNemar test on paired tasks. Pure
// functions, no dependencies.

// wilson - score interval for k successes in n trials. z defaults to 1.96.
export function wilson(k, n, z = 1.959963984540054) {
  if (!Number.isInteger(k) || !Number.isInteger(n) || n <= 0 || k < 0 || k > n) {
    throw new RangeError("wilson needs integers 0 <= k <= n, n > 0");
  }
  const p = k / n;
  const z2 = z * z;
  const denom = 1 + z2 / n;
  const centre = (p + z2 / (2 * n)) / denom;
  const half = (z * Math.sqrt((p * (1 - p)) / n + z2 / (4 * n * n))) / denom;
  return { k, n, rate: p, low: Math.max(0, centre - half), high: Math.min(1, centre + half) };
}

function logChoose(n, k) {
  let s = 0;
  for (let i = 1; i <= k; i++) s += Math.log(n - k + i) - Math.log(i);
  return s;
}

// mcnemarExact - two-sided exact p-value from the discordant pairs: b tasks
// arm A solved and arm B did not, c tasks the reverse. Binomial(b + c, 1/2).
export function mcnemarExact(b, c) {
  if (!Number.isInteger(b) || !Number.isInteger(c) || b < 0 || c < 0) throw new RangeError("counts must be non-negative integers");
  const n = b + c;
  if (n === 0) return { b, c, n, p: 1 };
  const lo = Math.min(b, c);
  let tail = 0;
  for (let i = 0; i <= lo; i++) tail += Math.exp(logChoose(n, i) - n * Math.LN2);
  return { b, c, n, p: Math.min(1, 2 * tail) };
}

// pairCounts - discordant counts from two per-task outcome maps (id -> bool),
// over the tasks both arms ran.
export function pairCounts(a, bMap) {
  let b = 0;
  let c = 0;
  let paired = 0;
  for (const [id, okA] of Object.entries(a)) {
    if (!(id in bMap)) continue;
    paired += 1;
    if (okA && !bMap[id]) b += 1;
    if (!okA && bMap[id]) c += 1;
  }
  return { b, c, paired };
}
