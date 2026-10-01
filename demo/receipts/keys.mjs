// keys.mjs - the local Telos ed25519 signing key (DESIGN 4.2). Node's built-in
// crypto only, so Telos keeps zero runtime dependencies. The private key stays in
// this module: loadSigner returns a sign() closure and public fields, never the
// key object or its bytes, so it cannot reach a receipt, a tool result or a log.
// It is a Telos key, separate from any Flywheel receipt-signing key.
//
// File modes: directories 0700 and the private key 0600 on POSIX. On Windows the
// mode bits are mostly ignored; the key relies on the per-user ACL that
// %LOCALAPPDATA% inherits. Telos spawns no icacls call to tighten it.
import { createPrivateKey, createPublicKey, generateKeyPairSync, sign as edSign } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { keyIdOf } from "./verify.mjs";

export const KEY_SCHEMA = "telos.key/v1";
const PRIVATE_FILE = "telos-ed25519.pem";
const PUBLIC_FILE = "telos-ed25519.pub.json";

// telosHome - TELOS_HOME, else %LOCALAPPDATA%/Telos on Windows, else
// $XDG_STATE_HOME/telos (default ~/.local/state/telos).
export function telosHome(env = process.env, platform = process.platform) {
  if (env.TELOS_HOME) return path.resolve(env.TELOS_HOME);
  if (platform === "win32") {
    return path.join(env.LOCALAPPDATA || path.join(os.homedir(), "AppData", "Local"), "Telos");
  }
  return path.join(env.XDG_STATE_HOME || path.join(os.homedir(), ".local", "state"), "telos");
}

export function ensureDir(dir) {
  mkdirSync(dir, { recursive: true, mode: 0o700 });
  return dir;
}

export function keysDir(home = telosHome()) {
  return path.join(home, "keys");
}

export function publicKeyPath(home = telosHome()) {
  return path.join(keysDir(home), PUBLIC_FILE);
}

function rawPublic(publicKey) {
  return publicKey.export({ format: "jwk" }).x;
}

// initKey - generate a key once. Refuses to overwrite: replacing the key would
// orphan every chain it signed. Returns public fields only.
export function initKey({ home = telosHome(), now = () => new Date() } = {}) {
  const dir = ensureDir(keysDir(home));
  const privPath = path.join(dir, PRIVATE_FILE);
  if (existsSync(privPath)) throw new Error(`a Telos key already exists at ${privPath}; it is never overwritten`);
  const { privateKey, publicKey } = generateKeyPairSync("ed25519");
  const public_key = rawPublic(publicKey);
  const pub = { schema: KEY_SCHEMA, alg: "ed25519", key_id: keyIdOf(public_key), public_key, created_at: now().toISOString() };
  writeFileSync(privPath, privateKey.export({ format: "pem", type: "pkcs8" }), { mode: 0o600, flag: "wx" });
  writeFileSync(path.join(dir, PUBLIC_FILE), `${JSON.stringify(pub, null, 2)}\n`, { mode: 0o644, flag: "wx" });
  return pub;
}

export function hasKey(home = telosHome()) {
  return existsSync(path.join(keysDir(home), PRIVATE_FILE));
}

// loadSigner - load the key and return { key_id, public_key, sign(text) }.
// Fails closed if the private and public files disagree.
export function loadSigner({ home = telosHome() } = {}) {
  const dir = keysDir(home);
  const privateKey = createPrivateKey(readFileSync(path.join(dir, PRIVATE_FILE), "utf8"));
  const public_key = rawPublic(createPublicKey(privateKey));
  const pub = JSON.parse(readFileSync(path.join(dir, PUBLIC_FILE), "utf8"));
  if (pub.public_key !== public_key || pub.key_id !== keyIdOf(public_key)) {
    throw new Error("Telos key files disagree: the public key file does not match the private key");
  }
  const signer = {
    key_id: pub.key_id,
    public_key,
    sign: (text) => edSign(null, Buffer.from(text, "utf8"), privateKey).toString("base64url")
  };
  return Object.freeze(signer);
}

// signerFromKeyObject - test and embedding seam for an in-memory key.
export function signerFromKeyObject(privateKey) {
  const public_key = rawPublic(createPublicKey(privateKey));
  return Object.freeze({
    key_id: keyIdOf(public_key),
    public_key,
    sign: (text) => edSign(null, Buffer.from(text, "utf8"), privateKey).toString("base64url")
  });
}

export function ephemeralSigner() {
  return signerFromKeyObject(generateKeyPairSync("ed25519").privateKey);
}
