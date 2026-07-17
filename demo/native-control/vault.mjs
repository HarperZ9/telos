// Local credential vault. A password-manager contract, not a harvester:
//
// - The operator populates it. Secrets are AES-256-GCM encrypted at rest with a
//   key derived (scrypt) from TELOS_VAULT_PASSPHRASE. With no passphrase it
//   refuses; it never writes plaintext credentials.
// - A credential is stored per host and filled ONLY when the live page's origin
//   matches that host. Your real password is never typed into a lookalike form
//   (the anti-phishing rule every password manager enforces).
// - It stores and fills username + password only. It does NOT hold MFA/TOTP
//   secrets and never fills a second factor. MFA stays an operator handoff: the
//   one live checkpoint that bounds what any bug or injected instruction can do.
// - list() and receipts never expose secrets. See BOUNDARY.md.
//
//   vault set --host=.. --user=..   (secret from env TELOS_VAULT_SECRET, not argv)
//   vault list
//   vault remove --host=..

import { readFileSync, writeFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname } from "node:path";
import { randomBytes, scryptSync, createCipheriv, createDecipheriv } from "node:crypto";

export function vaultPath(env = process.env) {
  if (env.TELOS_VAULT_PATH) return env.TELOS_VAULT_PATH;
  const base = env.LOCALAPPDATA || env.HOME || ".";
  return `${base}/Telos/vault.enc`;
}

export function normalizeHost(h) {
  return String(h || "").toLowerCase().replace(/^https?:\/\//, "").replace(/\/.*$/, "").replace(/:\d+$/, "");
}

// Strict, exact origin match (no subdomain widening) -- a credential for
// accounts.example.com must not fill on example.com.
export function originMatches(pageHost, entryHost) {
  const a = normalizeHost(pageHost);
  return a !== "" && a === normalizeHost(entryHost);
}

// ---- encryption (pure) ----

export function encryptBlob(obj, passphrase) {
  if (!passphrase) throw new Error("VAULT_LOCKED: set TELOS_VAULT_PASSPHRASE");
  const salt = randomBytes(16), iv = randomBytes(12);
  const key = scryptSync(String(passphrase), salt, 32);
  const c = createCipheriv("aes-256-gcm", key, iv);
  const enc = Buffer.concat([c.update(JSON.stringify(obj), "utf8"), c.final()]);
  return Buffer.concat([salt, iv, c.getAuthTag(), enc]).toString("base64");
}

export function decryptBlob(blob, passphrase) {
  if (!passphrase) throw new Error("VAULT_LOCKED: set TELOS_VAULT_PASSPHRASE");
  const b = Buffer.from(String(blob), "base64");
  const salt = b.subarray(0, 16), iv = b.subarray(16, 28), tag = b.subarray(28, 44), enc = b.subarray(44);
  const key = scryptSync(String(passphrase), salt, 32);
  const d = createDecipheriv("aes-256-gcm", key, iv);
  d.setAuthTag(tag);
  return JSON.parse(Buffer.concat([d.update(enc), d.final()]).toString("utf8"));
}

// ---- store I/O ----

export function load({ path = vaultPath(), passphrase = process.env.TELOS_VAULT_PASSPHRASE } = {}) {
  if (!existsSync(path)) return {};
  return decryptBlob(readFileSync(path, "utf8"), passphrase);
}

export function save(store, { path = vaultPath(), passphrase = process.env.TELOS_VAULT_PASSPHRASE } = {}) {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, encryptBlob(store, passphrase), "utf8");
  return { saved: true, hosts: Object.keys(store).length };
}

export function setEntry({ host, username, password }, opts = {}) {
  const h = normalizeHost(host);
  if (!h || !password) throw new Error("vault set needs --host and a secret (env TELOS_VAULT_SECRET)");
  const store = load(opts);
  store[h] = { username: username || "", password };
  save(store, opts);
  return { host: h, username: username || "", stored: true }; // no secret in the receipt
}

export function list(opts = {}) {
  const store = load(opts);
  return Object.entries(store).map(([host, e]) => ({ host, username: e.username || "" }));
}

export function remove(host, opts = {}) {
  const store = load(opts);
  const h = normalizeHost(host);
  const had = !!store[h];
  delete store[h];
  save(store, opts);
  return { host: h, removed: had };
}

// Internal: fetch a full entry (with secret) for the fill path only.
function getEntry(host, opts = {}) {
  const store = load(opts);
  return store[normalizeHost(host)] || null;
}

// In-page fill expression. Re-checks the origin inside the page as a second
// guard, and only fills username + password (never a second factor).
export function fillLoginExpression(username, password, host) {
  return `(() => {
    if (location.host.toLowerCase().replace(/:\\d+$/,'') !== ${JSON.stringify(normalizeHost(host))}) {
      return { filled: false, reason: 'host-mismatch', host: location.host };
    }
    const set = (el, v) => {
      const d = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value');
      if (d && d.set) d.set.call(el, v);
      el.dispatchEvent(new Event('input', { bubbles: true }));
      el.dispatchEvent(new Event('change', { bubbles: true }));
    };
    const pw = document.querySelector('input[type=password]');
    if (!pw) return { filled: false, reason: 'no-login-form' };
    const user = document.querySelector('input[autocomplete=username],input[type=email],input[name=session_key],input[type=text][name*="user" i],input[type=text][name*="email" i]') || document.querySelector('input[type=text]');
    const fields = [];
    if (user && ${JSON.stringify(username || "")}) { set(user, ${JSON.stringify(username || "")}); fields.push('username'); }
    set(pw, ${JSON.stringify(password)}); fields.push('password');
    return { filled: true, fields, host: location.host };
  })()`;
}

// Fill the current page's login from the vault, host-scoped. Returns a
// secret-free receipt. Does not submit and does not touch MFA.
export async function fillLogin(session, opts = {}) {
  const hostRes = await session.send("Runtime.evaluate", { expression: "location.host", returnByValue: true });
  const host = normalizeHost(hostRes.result?.value);
  if (!host) return { filled: false, reason: "no-page-host" };
  const entry = getEntry(host, opts);
  if (!entry) return { filled: false, reason: "no-vault-entry-for-host", host };
  const res = await session.send("Runtime.evaluate", {
    expression: fillLoginExpression(entry.username, entry.password, host),
    returnByValue: true,
  });
  const out = res.result?.value || { filled: false, reason: "eval-failed" };
  return { host, filled: !!out.filled, reason: out.reason, fields: out.fields }; // never the secret
}
