#!/usr/bin/env node
// verify.mjs - offline verifier for telos.receipt/v1 chains. Stdlib only
// (node:crypto, node:fs): copy this one file next to a receipts .jsonl and run
// `node verify.mjs session.jsonl [--checkpoints checkpoints.jsonl]
// [--pubkey telos-ed25519.pub.json] [--json]`. Exit 0 MATCH, 1 DRIFT,
// 2 UNVERIFIABLE. It re-derives every seal, checks each prev_seal link and seq,
// checks every ed25519 head signature against one key, and checks checkpoints.
// A MATCH shows the file is the chain a holder of that key signed. It does not
// show the actions were wise, that the screen matched, or that the key was not
// stolen: a key holder can re-sign a forged chain back to the last external
// anchor. Without a checkpoint, a suffix cut at a signed head is not detectable.
import { createHash, createPublicKey, verify as edVerify } from "node:crypto";
import { readFileSync, realpathSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

export const RECEIPT_SCHEMA = "telos.receipt/v1";
export const SIGNATURE_SCHEMA = "telos.receipt-signature/v1";
export const CHECKPOINT_SCHEMA = "telos.receipt-checkpoint/v1";
export const HASH_VERSION = 3;
export const GENESIS = "0".repeat(64);
export const MAX_SIGNATURE_BATCH = 32;
export const TIERS = ["T0", "T1", "T2", "T3", "T4", "T5"];
export const STATUSES = ["OK", "REFUSED", "HOLD", "APPROVED", "REJECTED", "EXPIRED",
  "DRIFT", "NEEDS_HUMAN", "DRY_RUN", "UNAVAILABLE"];
// Statuses that never carry an executed effect.
export const NON_EXECUTING = new Set(["REFUSED", "HOLD", "APPROVED", "REJECTED", "EXPIRED",
  "DRY_RUN", "UNAVAILABLE"]);
export const REQUIRED_FIELDS = ["schema", "hash_version", "receipt_id", "session_id", "seq",
  "prev_seal", "ts", "tier", "verb", "tool", "module", "module_version", "grant_id",
  "scope_sha256", "action_digest", "status", "reason", "executed", "spawned", "monitor",
  "does_not_prove", "seal"];

// canonical - sorted keys, compact separators, UTF-8, no floats. Integers must be
// safe integers; anything else is a decimal string. Throws on floats, NaN,
// undefined, functions and bigints so a receipt can never seal an ambiguous value.
// An object key whose value is undefined is dropped, as JSON.stringify drops it,
// so a value hashes the same before and after a JSON round trip.
export function canonical(value) {
  if (value === null) return "null";
  switch (typeof value) {
    case "string": return JSON.stringify(value);
    case "boolean": return value ? "true" : "false";
    case "number":
      if (!Number.isSafeInteger(value)) throw new TypeError(`canonical form forbids non-integer number ${value}`);
      return String(value);
    case "object":
      if (Array.isArray(value)) return `[${value.map(canonical).join(",")}]`;
      return `{${Object.keys(value).filter((k) => value[k] !== undefined).sort()
        .map((k) => `${JSON.stringify(k)}:${canonical(value[k])}`).join(",")}}`;
    default:
      throw new TypeError(`canonical form forbids ${typeof value}`);
  }
}

export function sha256Hex(text) {
  return createHash("sha256").update(text, "utf8").digest("hex");
}

// sealOf - sha256 over the canonical receipt with the seal field blank.
export function sealOf(receipt) {
  return sha256Hex(canonical({ ...receipt, seal: "" }));
}

export function signaturePayload({ session_id, seq, head_seal, key_id }) {
  return canonical({ schema: SIGNATURE_SCHEMA, session_id, seq, head_seal, key_id });
}

export function checkpointPayload({ session, seq, head_seal, key_id }) {
  return canonical({ schema: CHECKPOINT_SCHEMA, session, seq, head_seal, key_id });
}

export function keyIdOf(publicKeyB64url) {
  return createHash("sha256").update(Buffer.from(publicKeyB64url, "base64url")).digest("hex");
}

function publicKeyObject(publicKeyB64url) {
  return createPublicKey({ key: { kty: "OKP", crv: "Ed25519", x: publicKeyB64url }, format: "jwk" });
}

export function verifySignature(payload, sigB64url, publicKeyB64url) {
  try {
    return edVerify(null, Buffer.from(payload, "utf8"), publicKeyObject(publicKeyB64url), Buffer.from(sigB64url, "base64url"));
  } catch {
    return false;
  }
}

// validateReceipt - structural checks the seal cannot make: required fields,
// enums, types, and the rule that a non-executing status never claims an effect.
export function validateReceipt(r) {
  for (const f of REQUIRED_FIELDS) if (!(f in r)) return `missing field ${f}`;
  if (r.schema !== RECEIPT_SCHEMA) return `schema ${r.schema}`;
  if (r.hash_version !== HASH_VERSION) return `hash_version ${r.hash_version}`;
  if (!TIERS.includes(r.tier)) return `tier ${r.tier}`;
  if (!STATUSES.includes(r.status)) return `status ${r.status}`;
  if (typeof r.executed !== "boolean") return "executed is not a boolean";
  if (r.executed && NON_EXECUTING.has(r.status)) return `status ${r.status} cannot be executed`;
  if (!Array.isArray(r.spawned)) return "spawned is not an array";
  if (typeof r.does_not_prove !== "string" || !r.does_not_prove) return "does_not_prove is empty";
  if (!Number.isSafeInteger(r.seq) || r.seq < 1) return `seq ${r.seq}`;
  return null;
}

export function parseJsonl(text) {
  const out = [];
  const lines = String(text).split(/\r?\n/);
  for (let i = 0; i < lines.length; i += 1) {
    if (!lines[i].trim()) continue;
    try {
      out.push({ line: i + 1, rec: JSON.parse(lines[i]) });
    } catch {
      return { error: `line ${i + 1} is not JSON` };
    }
  }
  return { records: out };
}

const drift = (reason, extra = {}) => ({ verdict: "DRIFT", reason, ...extra });

// keyCheck - one key per chain. A pinned key wins; otherwise the first signature's
// key is used and every later signature must match it (key_trust self-asserted).
function keyCheck(rec, state) {
  if (typeof rec.public_key !== "string" || keyIdOf(rec.public_key) !== rec.key_id) {
    return "key_id is not the sha256 of the embedded public key";
  }
  if (!state.key) state.key = { key_id: rec.key_id, public_key: rec.public_key };
  if (rec.key_id !== state.key.key_id) return `signed by key ${rec.key_id.slice(0, 12)}, chain key is ${state.key.key_id.slice(0, 12)}`;
  return null;
}

function checkReceipt(rec, line, state) {
  const bad = validateReceipt(rec);
  if (bad) return drift(`line ${line}: ${bad}`, { break_at: line });
  if (state.session_id === null) state.session_id = rec.session_id;
  if (rec.session_id !== state.session_id) return drift(`line ${line}: session_id changes`, { break_at: line });
  if (rec.seq !== state.seals.length + 1) return drift(`line ${line}: seq ${rec.seq}, expected ${state.seals.length + 1}`, { break_at: line });
  const prev = state.seals.length ? state.seals[state.seals.length - 1] : GENESIS;
  if (rec.prev_seal !== prev) return drift(`line ${line}: prev_seal does not link to seq ${rec.seq - 1}`, { break_at: line });
  let derived;
  try {
    derived = sealOf(rec);
  } catch (err) {
    return drift(`line ${line}: ${err.message}`, { break_at: line });
  }
  if (derived !== rec.seal) return drift(`line ${line}: seal does not re-derive at seq ${rec.seq}`, { break_at: line });
  state.seals.push(rec.seal);
  return null;
}

function checkSignature(rec, line, state) {
  if (rec.session_id !== state.session_id) return drift(`line ${line}: signature for another session`, { break_at: line });
  if (!Number.isSafeInteger(rec.seq) || rec.seq < 1 || rec.seq > state.seals.length) {
    return drift(`line ${line}: signature names seq ${rec.seq} before it exists`, { break_at: line });
  }
  if (state.seals[rec.seq - 1] !== rec.head_seal) return drift(`line ${line}: signed head is not the seal at seq ${rec.seq}`, { break_at: line });
  const keyProblem = keyCheck(rec, state);
  if (keyProblem) return drift(`line ${line}: ${keyProblem}`, { break_at: line });
  if (!verifySignature(signaturePayload(rec), rec.sig, state.key.public_key)) {
    return drift(`line ${line}: signature does not verify for seq ${rec.seq}`, { break_at: line });
  }
  if (rec.seq - state.signedThrough > MAX_SIGNATURE_BATCH) {
    return drift(`line ${line}: signature gap of ${rec.seq - state.signedThrough} exceeds ${MAX_SIGNATURE_BATCH}`, { break_at: line });
  }
  state.signedThrough = Math.max(state.signedThrough, rec.seq);
  return null;
}

function checkCheckpoints(text, state) {
  const parsed = parseJsonl(text);
  if (parsed.error) return { result: drift(`checkpoints: ${parsed.error}`) };
  let checked = 0;
  for (const { line, rec } of parsed.records) {
    if (rec.schema !== CHECKPOINT_SCHEMA) return { result: drift(`checkpoints line ${line}: unknown schema`) };
    if (rec.session !== state.session_id) continue;
    const keyProblem = keyCheck(rec, state);
    if (keyProblem) return { result: drift(`checkpoints line ${line}: ${keyProblem}`) };
    if (!verifySignature(checkpointPayload(rec), rec.signature, state.key.public_key)) {
      return { result: drift(`checkpoints line ${line}: checkpoint signature does not verify`) };
    }
    if (rec.seq > state.seals.length) {
      return { result: drift(`suffix removed: checkpoint at seq ${rec.seq}, chain ends at seq ${state.seals.length}`) };
    }
    if (state.seals[rec.seq - 1] !== rec.head_seal) return { result: drift(`checkpoint at seq ${rec.seq} names a different head`) };
    checked += 1;
  }
  return { checked };
}

// verifyChain - verify one session file. options: checkpoints (text),
// trustedKey ({key_id, public_key}) to pin the signing key.
export function verifyChain(text, options = {}) {
  const started = Date.now();
  const parsed = parseJsonl(text);
  if (parsed.error) return drift(parsed.error);
  const state = { session_id: null, seals: [], signedThrough: 0, key: options.trustedKey ?? null };
  for (const { line, rec } of parsed.records) {
    let problem;
    if (rec?.schema === RECEIPT_SCHEMA) problem = checkReceipt(rec, line, state);
    else if (rec?.schema === SIGNATURE_SCHEMA) problem = checkSignature(rec, line, state);
    else problem = drift(`line ${line}: unknown record schema`, { break_at: line });
    if (problem) return { ...problem, count: state.seals.length };
  }
  const base = { count: state.seals.length, session_id: state.session_id, signed_through: state.signedThrough,
    key_id: state.key?.key_id ?? null, key_trust: options.trustedKey ? "pinned" : "self-asserted" };
  if (!state.seals.length) return { verdict: "UNVERIFIABLE", reason: "no receipts", ...base };
  let checkpoints = 0;
  if (options.checkpoints) {
    const cp = checkCheckpoints(options.checkpoints, state);
    if (cp.result) return { ...cp.result, ...base };
    checkpoints = cp.checked;
  }
  const elapsed_ms = Date.now() - started;
  if (state.signedThrough < state.seals.length) {
    return { verdict: "UNVERIFIABLE", reason: `${state.seals.length - state.signedThrough} receipts after seq ${state.signedThrough} are unsigned`, ...base, checkpoints, elapsed_ms };
  }
  return { verdict: "MATCH", reason: `${state.seals.length} receipts re-derive and every head is signed`, ...base, head_seal: state.seals.at(-1), checkpoints, elapsed_ms };
}

export function loadTrustedKey(file) {
  const pub = JSON.parse(readFileSync(file, "utf8"));
  if (keyIdOf(pub.public_key) !== pub.key_id) throw new Error("public key file: key_id does not match public_key");
  return { key_id: pub.key_id, public_key: pub.public_key };
}

export function cliMain(argv) {
  const args = [...argv];
  const take = (flag) => {
    const i = args.indexOf(flag);
    return i < 0 ? null : args.splice(i, 2)[1];
  };
  const json = args.includes("--json") ? (args.splice(args.indexOf("--json"), 1), true) : false;
  const cpFile = take("--checkpoints");
  const pubFile = take("--pubkey");
  const target = args[0];
  if (!target) {
    process.stderr.write("usage: verify <session.jsonl> [--checkpoints file] [--pubkey file] [--json]\n");
    return 2;
  }
  let result;
  try {
    result = verifyChain(readFileSync(target, "utf8"), {
      checkpoints: cpFile ? readFileSync(cpFile, "utf8") : undefined,
      trustedKey: pubFile ? loadTrustedKey(pubFile) : undefined
    });
  } catch (err) {
    result = { verdict: "UNVERIFIABLE", reason: `unreadable input: ${err.message}` };
  }
  process.stdout.write(json ? `${JSON.stringify(result, null, 2)}\n` : `${result.verdict}  ${result.reason}\n`);
  return result.verdict === "MATCH" ? 0 : result.verdict === "DRIFT" ? 1 : 2;
}

function isMain() {
  if (!process.argv[1]) return false;
  const real = (p) => {
    try { return realpathSync(path.resolve(p)); } catch { return path.resolve(p); }
  };
  const norm = (p) => (process.platform === "win32" ? real(p).toLowerCase() : real(p));
  return norm(process.argv[1]) === norm(fileURLToPath(import.meta.url));
}

if (isMain()) process.exit(cliMain(process.argv.slice(2)));
