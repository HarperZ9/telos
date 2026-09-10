// Native-control ledger integrity, not execution truth or authorization.
// hash_version 2 binds session identity and every entry field except the derived
// chain/chain_ok fields. Missing hash_version denotes the legacy step/result
// calculation. Retained targets and results can contain private data.
// These are unsigned hashes: a trusted external checkpoint is needed to detect
// a rewritten chain or a removed suffix. Verification cannot establish success.

import { createHash } from "node:crypto";

export function canonicalJson(value) {
  // Stable emet-pinned form: recursively sorted keys, ", " and ": " separators,
  // UTF-8. Built directly (JSON.stringify's separators are not configurable to
  // this form) so a chain re-derives identically in any runtime.
  const seen = new WeakSet();
  const ser = (v) => {
    if (v === null || typeof v === "undefined") return "null";
    if (typeof v === "string") return JSON.stringify(v);
    if (typeof v === "number" || typeof v === "boolean") return String(v);
    if (typeof v === "bigint") return v.toString();
    if (typeof v !== "object") return JSON.stringify(v);
    if (seen.has(v)) return "null"; // cycle break
    seen.add(v);
    if (Array.isArray(v)) return "[" + v.map(ser).join(", ") + "]";
    const keys = Object.keys(v).sort();
    return "{" + keys.map((k) => JSON.stringify(k) + ": " + ser(v[k])).join(", ") + "}";
  };
  return ser(value);
}

export function chainValue(prev, stepId, result) {
  return createHash("sha256").update(prev + String(stepId) + canonicalJson(result), "utf8").digest("hex");
}

const SCHEMA = "project-telos.native-control-ledger/v1";
const GENESIS = "0".repeat(64);

function entryChain(prev, entry, ledger) {
  if ((ledger.hash_version ?? 1) === 1) return chainValue(prev, entry.step, entry.result);
  const { chain, chain_ok, ...fields } = entry;
  const payload = {
    schema: SCHEMA, hash_version: 2, runId: ledger.runId, name: ledger.name, entry: fields,
  };
  return createHash("sha256").update(prev + canonicalJson(payload), "utf8").digest("hex");
}

export class Ledger {
  constructor({ runId, name } = {}) {
    this.runId = runId || `run_${Date.now().toString(36)}_${Math.random().toString(36).slice(2, 8)}`;
    this.name = name || "native-control-session";
    this.hash_version = 2;
    this.prev = GENESIS;
    this.entries = [];
  }

  append(stepId, entry) {
    // Hash the JSON wire values and detach caller-owned objects before storing.
    // This also avoids alias/cycle ambiguities in the legacy serializer.
    const rec = JSON.parse(JSON.stringify({ ...entry, step: stepId }));
    delete rec.chain;
    delete rec.chain_ok;
    const chain = entryChain(this.prev, rec, this);
    rec.chain = chain;
    this.entries.push(rec);
    this.prev = chain;
    return rec;
  }

  export() {
    let p = GENESIS;
    const entries = this.entries.map((e) => {
      const check = entryChain(p, e, this);
      p = e.chain;
      return { ...e, chain_ok: check === e.chain };
    });
    return {
      schema: SCHEMA,
      hash_version: this.hash_version,
      runId: this.runId,
      name: this.name,
      genesis: GENESIS,
      entries,
      integrity: entries.every((e) => e.chain_ok) ? "INTACT" : "BROKEN",
      integrity_scope: "entry-and-session-metadata",
      count: entries.length,
    };
  }

  static verify(exported) {
    if (!exported || exported.genesis !== GENESIS) return { ok: false, reason: "bad-genesis" };
    if (exported.schema !== SCHEMA) return { ok: false, reason: "unknown-schema" };
    const version = exported.hash_version ?? 1;
    if (version !== 1 && version !== 2) return { ok: false, reason: "unknown-hash-version" };
    if (!Array.isArray(exported.entries) || exported.entries.some((e) => !e || typeof e !== "object" || Array.isArray(e))) {
      return { ok: false, reason: "bad-entries" };
    }
    let p = exported.genesis;
    for (const e of exported.entries) {
      if (entryChain(p, e, exported) !== e.chain) return { ok: false, reason: "chain-broken", step: e.step };
      if (e.prev !== undefined && e.prev !== p) return { ok: false, reason: "linkage", step: e.step };
      p = e.chain;
    }
    return {
      ok: true, count: exported.entries.length,
      integrity_scope: version === 2 ? "entry-and-session-metadata" : "legacy-step-and-result-only",
    };
  }
}
