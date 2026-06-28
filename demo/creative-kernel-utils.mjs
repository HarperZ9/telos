export function stableStringify(value) {
  if (Array.isArray(value)) return `[${value.map(stableStringify).join(",")}]`;
  if (value && typeof value === "object") {
    return `{${Object.keys(value)
      .sort()
      .map((key) => `${JSON.stringify(key)}:${stableStringify(value[key])}`)
      .join(",")}}`;
  }
  return JSON.stringify(value);
}

export function stableReceiptHash(value) {
  const text = stableStringify(value);
  let hash = 0x811c9dc5;
  for (let index = 0; index < text.length; index += 1) {
    hash ^= text.charCodeAt(index);
    hash = Math.imul(hash, 0x01000193) >>> 0;
  }
  return `fnv1a:${hash.toString(16).padStart(8, "0")}`;
}

export function assertPositiveInteger(value, label) {
  if (!Number.isInteger(value) || value <= 0) {
    throw new Error(`${label}: positive_integer_required`);
  }
}

export function isPowerOfTwo(value) {
  return Number.isInteger(value) && value > 0 && (value & (value - 1)) === 0;
}

export function numericArray(values, label) {
  const array = Array.from(values ?? []);
  if (!array.length) throw new Error(`${label}: source_missing`);
  for (const value of array) {
    if (!Number.isFinite(value)) throw new Error(`${label}: finite_numbers_required`);
  }
  return array;
}

export function objectArray(values, label) {
  const array = Array.from(values ?? []);
  if (!array.length) throw new Error(`${label}: source_missing`);
  for (const value of array) {
    if (!value || typeof value !== "object") throw new Error(`${label}: object_records_required`);
  }
  return array;
}

export function validatePixels({ pixels, width, height }) {
  assertPositiveInteger(width, "pixels.width");
  assertPositiveInteger(height, "pixels.height");
  const values = numericArray(pixels, "pixels");
  if (values.length !== width * height) throw new Error("pixels: dimensions_mismatch");
  return values.map((value) => Math.max(0, Math.min(255, Math.round(value))));
}
