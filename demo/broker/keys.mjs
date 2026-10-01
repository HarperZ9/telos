// The local Telos ed25519 key. Grants and hold decisions are signed with it, so
// a grant or decision file written by hand, or by a process without the key,
// fails to load. Node's built-in crypto only, so Telos keeps zero runtime
// dependencies. The receipts slice signs chain heads with the same key; the
// file names below are the shared contract (DESIGN.md 4.2).
import { createPrivateKey, createPublicKey, generateKeyPairSync, sign, verify } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { sha256Hex } from "./canonical.mjs";

export const PRIVATE_KEY_FILE = "telos-ed25519.key";
export const PUBLIC_KEY_FILE = "telos-ed25519.pub";

export function generateKeys() {
  return generateKeyPairSync("ed25519");
}

// key_id is the sha256 of the raw 32-byte public key.
export function keyId(publicKey) {
  const der = publicKey.export({ type: "spki", format: "der" });
  return sha256Hex(der.subarray(der.length - 32));
}

export function signText(privateKey, text) {
  return sign(null, Buffer.from(text, "utf8"), privateKey).toString("base64");
}

export function verifyText(publicKey, text, sigB64) {
  if (typeof sigB64 !== "string" || !sigB64) return false;
  try {
    return verify(null, Buffer.from(text, "utf8"), publicKey, Buffer.from(sigB64, "base64"));
  } catch {
    return false;
  }
}

export function requireTty(isTTY, what) {
  if (isTTY !== true) {
    const err = new Error(`${what} needs an interactive terminal; an agent's shell has none`);
    err.code = "NEEDS_TTY";
    throw err;
  }
}

export function initKeys(dir, { isTTY } = {}) {
  requireTty(isTTY, "telos keys init");
  const priv = path.join(dir, PRIVATE_KEY_FILE);
  if (existsSync(priv)) throw new Error(`a Telos key already exists in ${dir}`);
  mkdirSync(dir, { recursive: true, mode: 0o700 });
  const { privateKey, publicKey } = generateKeys();
  writeFileSync(priv, privateKey.export({ type: "pkcs8", format: "pem" }), { mode: 0o600, flag: "wx" });
  writeFileSync(path.join(dir, PUBLIC_KEY_FILE), publicKey.export({ type: "spki", format: "pem" }), { mode: 0o644, flag: "wx" });
  return { key_id: keyId(publicKey) };
}

export function loadPublicKey(dir) {
  const file = path.join(dir, PUBLIC_KEY_FILE);
  return existsSync(file) ? createPublicKey(readFileSync(file)) : null;
}

export function loadPrivateKey(dir) {
  const file = path.join(dir, PRIVATE_KEY_FILE);
  return existsSync(file) ? createPrivateKey(readFileSync(file)) : null;
}
