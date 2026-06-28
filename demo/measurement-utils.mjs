export function stableStringify(value) {
  if (Array.isArray(value)) return `[${value.map(stableStringify).join(",")}]`;
  if (value && typeof value === "object") {
    const entries = Object.keys(value)
      .sort()
      .map((key) => `${JSON.stringify(key)}:${stableStringify(value[key])}`);
    return `{${entries.join(",")}}`;
  }
  return JSON.stringify(value);
}

export function hashStable(value) {
  const text = typeof value === "string" ? value : stableStringify(value);
  let hash = 2166136261;
  for (let i = 0; i < text.length; i++) {
    hash ^= text.charCodeAt(i);
    hash = Math.imul(hash, 16777619) >>> 0;
  }
  return `fnv1a:${hash.toString(16).padStart(8, "0")}`;
}

export function numericArray(values, label) {
  const array = Array.from(values ?? []);
  if (!array.length) throw new Error(`${label}: measurement_source_missing`);
  for (const value of array) {
    if (!Number.isFinite(Number(value))) throw new Error(`${label}: measurement_source_missing`);
  }
  return array.map(Number);
}

export function round(value, places = 4) {
  const scale = 10 ** places;
  return Math.round(value * scale) / scale;
}

export function pointSamples(values, label) {
  const samples = Array.isArray(values) ? values : [];
  if (samples.length < 3) throw new Error(`${label}: measurement_source_missing`);
  return samples.map((sample) => {
    const point = { x: Number(sample.x), y: Number(sample.y), z: Number(sample.z ?? 0) };
    if (!Number.isFinite(point.x) || !Number.isFinite(point.y) || !Number.isFinite(point.z)) {
      throw new Error(`${label}: measurement_source_missing`);
    }
    return point;
  });
}

export function distance(a, b) {
  return Math.hypot(a.x - b.x, a.y - b.y, a.z - b.z);
}

export function turnAngleDegrees(a, b, c) {
  const left = { x: a.x - b.x, y: a.y - b.y, z: a.z - b.z };
  const right = { x: c.x - b.x, y: c.y - b.y, z: c.z - b.z };
  const leftMag = Math.hypot(left.x, left.y, left.z);
  const rightMag = Math.hypot(right.x, right.y, right.z);
  if (leftMag === 0 || rightMag === 0) return 0;
  const dot = left.x * right.x + left.y * right.y + left.z * right.z;
  const cosine = Math.max(-1, Math.min(1, dot / (leftMag * rightMag)));
  return (Math.PI - Math.acos(cosine)) * (180 / Math.PI);
}

export function percentile(sorted, ratio) {
  if (!sorted.length) return 0;
  const index = Math.max(0, Math.min(sorted.length - 1, Math.ceil(sorted.length * ratio) - 1));
  return sorted[index];
}
