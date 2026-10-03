// fixtures.mjs: seeded images for the telos.measurement.layers v2 checks (xorshift32, seed 20261002).
export function xorshift32(seed) {
  let x = seed >>> 0;
  return function next() {
    x ^= x << 13; x >>>= 0;
    x ^= x >>> 17;
    x ^= x << 5; x >>>= 0;
    return x;
  };
}

export const randInt = (next, lo, hi) => lo + (next() % (hi - lo + 1));

// Opaque RGBA of one colour.
export function solid(w, h, [r, g, b]) {
  const px = new Uint8Array(w * h * 4);
  for (let i = 0; i < w * h; i++) { px[i * 4] = r; px[i * 4 + 1] = g; px[i * 4 + 2] = b; px[i * 4 + 3] = 255; }
  return px;
}

// Opaque seeded noise.
export function noise(w, h, next) {
  const px = new Uint8Array(w * h * 4);
  for (let i = 0; i < w * h; i++) { px[i * 4] = next() & 255; px[i * 4 + 1] = next() & 255; px[i * 4 + 2] = next() & 255; px[i * 4 + 3] = 255; }
  return px;
}

// Seeded images: noise, blocks or ramps, sides in [lo, hi].
export function* seededImages(count, lo, hi, seed = 20261002) {
  const next = xorshift32(seed);
  for (let k = 0; k < count; k++) {
    const w = randInt(next, lo, hi), h = randInt(next, lo, hi), kind = next() % 3;
    let px;
    if (kind === 0) px = noise(w, h, next);
    else {
      px = solid(w, h, [next() & 255, next() & 255, next() & 255]);
      const c = [next() & 255, next() & 255, next() & 255];
      for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
        const inside = kind === 1 ? (x > w / 3 && y > h / 4) : x * 3 > w * ((y % 7) + 1) / 7;
        if (inside) { const i = (y * w + x) * 4; px[i] = c[0]; px[i + 1] = c[1]; px[i + 2] = c[2]; }
      }
    }
    yield { name: `img-${String(k).padStart(3, "0")}`, w, h, px };
  }
}

export const b64 = (px) => Buffer.from(px).toString("base64");
export const request = (img, extra = {}) => ({ image: { rgba: b64(img.px), width: img.w, height: img.h }, ...extra });
