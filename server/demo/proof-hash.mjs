import { createHash } from "node:crypto";

// Canonical, sorted-key, whitespace-free serialization. Same pattern as
// context-pack.mjs so digests are re-derivable on any machine.
export function stableStringify(value) {
  if (Array.isArray(value)) {
    return `[${value.map(stableStringify).join(",")}]`;
  }
  if (value && typeof value === "object") {
    return `{${Object.keys(value)
      .sort()
      .map((key) => `${JSON.stringify(key)}:${stableStringify(value[key])}`)
      .join(",")}}`;
  }
  return JSON.stringify(value);
}

export function sha256Prefixed(value) {
  return `sha256:${createHash("sha256").update(value).digest("hex")}`;
}

// Digest over raw artifact bytes (a string), matching EMET's raw-byte model.
export function digestBytes(text) {
  return sha256Prefixed(Buffer.from(String(text), "utf8"));
}

// The hash scope is every field except these result and wall-clock fields.
const UNHASHED_FIELDS = new Set(["packet_hash", "verifier", "witness", "wall_clock", "witness_coverage"]);

export function hashScope(packet) {
  const scope = {};
  for (const key of Object.keys(packet)) {
    if (!UNHASHED_FIELDS.has(key)) {
      scope[key] = packet[key];
    }
  }
  return scope;
}

export function canonicalBytes(packet) {
  return stableStringify(hashScope(packet));
}

export function packetHash(packet) {
  return sha256Prefixed(Buffer.from(canonicalBytes(packet), "utf8"));
}
