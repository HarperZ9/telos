// The local Telos ed25519 key. Grants and hold decisions are signed with it, so
// a grant or decision file written by hand, or by a process without the key,
// fails to load. Node's built-in crypto only, so Telos keeps zero runtime
// dependencies. The receipts slice signs chain heads with the same key; the
// file names below are the shared contract (DESIGN.md 4.2).
import { createPrivateKey, createPublicKey, generateKeyPairSync, sign, verify } from "node:crypto";
import { existsSync, readFileSync } from "node:fs";
import path from "node:path";
import { initKey, PRIVATE_FILE, PUBLIC_PEM_FILE } from "../receipts/keys.mjs";
import { sha256Hex } from "./canonical.mjs";

export const PRIVATE_KEY_FILE = PRIVATE_FILE;
export const PUBLIC_KEY_FILE = PUBLIC_PEM_FILE;

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

// initKeys - `dir` is <state root>/keys. The receipt key module writes the
// files, so the broker and the receipt chain share one key.
export function initKeys(dir, { isTTY } = {}) {
  requireTty(isTTY, "telos keys init");
  if (path.basename(dir) !== "keys") throw new Error("initKeys expects the <state root>/keys directory");
  const { key_id } = initKey({ home: path.dirname(dir) });
  return { key_id };
}

export function loadPublicKey(dir) {
  const file = path.join(dir, PUBLIC_KEY_FILE);
  return existsSync(file) ? createPublicKey(readFileSync(file)) : null;
}

export function loadPrivateKey(dir) {
  const file = path.join(dir, PRIVATE_KEY_FILE);
  return existsSync(file) ? createPrivateKey(readFileSync(file)) : null;
}
