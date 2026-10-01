// Canonical JSON for digests and signatures: sorted keys, compact separators,
// UTF-8, no floats. This is the Flywheel record form that DESIGN.md section 4.1
// names for telos.receipt/v1. A non-integer number, NaN, Infinity, a function or
// undefined inside an array throws, so two callers can never hash the same
// value two ways.
import { createHash } from "node:crypto";

function encode(value) {
  if (value === null) return "null";
  if (typeof value === "string" || typeof value === "boolean") return JSON.stringify(value);
  if (typeof value === "number") {
    if (!Number.isSafeInteger(value)) throw new TypeError(`canonical form refuses non-integer number ${value}`);
    return String(value);
  }
  if (Array.isArray(value)) return `[${value.map(encode).join(",")}]`;
  if (typeof value === "object") {
    const keys = Object.keys(value).filter((k) => value[k] !== undefined).sort();
    return `{${keys.map((k) => `${JSON.stringify(k)}:${encode(value[k])}`).join(",")}}`;
  }
  throw new TypeError(`canonical form refuses ${typeof value}`);
}

export function canonical(value) {
  return encode(value);
}

export function sha256Hex(input) {
  return createHash("sha256").update(input).digest("hex");
}

export function digestOf(value) {
  return sha256Hex(canonical(value));
}
