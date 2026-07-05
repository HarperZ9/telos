// Witnessed session ledger for native-control runs. Each step's result chains
// into a tamper-evident log (emet/forum-style: chain = SHA-256(prev + stepId +
// canonical_json(result))), so an entire automation session -- apply to N jobs,
// a multi-step auth flow, a scrape -- is itself a witnessed, re-checkable
// artifact. This is telos's accountability thesis applied to its own actuation.
//
//   canonicalJson : keys sorted, ", " / ": " separators, UTF-8 (emet-pinned form)
//   chainValue    : sha256(prev + stepId + canonicalJson(result)), genesis = 64 zeros
//
// A ledger EXPORT is a list of {step, action, target, ok, result, chain}; verify
// re-derives the chain and rejects any edited step or ordering. It is a FACT of
// what ran, never authority -- and it never carries secrets (action results are
// the engine's own receipts, which exclude credentials by construction).

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

export class Ledger {
  constructor({ runId, name } = {}) {
    this.runId = runId || `run_${Date.now().toString(36)}_${Math.random().toString(36).slice(2, 8)}`;
    this.name = name || "native-control-session";
    this.prev = "0".repeat(64);
    this.entries = [];
  }

  append(stepId, entry) {
    const chain = chainValue(this.prev, stepId, entry.result);
    const rec = { step: stepId, ...entry, chain };
    this.entries.push(rec);
    this.prev = chain;
    return rec;
  }

  export() {
    // genesis prev + ordered entries; the chain itself is the integrity proof.
    let p = "0".repeat(64);
    const entries = this.entries.map((e) => {
      const check = chainValue(p, e.step, e.result);
      p = e.chain;
      return { ...e, chain_ok: check === e.chain };
    });
    return {
      schema: "project-telos.native-control-ledger/v1",
      runId: this.runId,
      name: this.name,
      genesis: "0".repeat(64),
      entries,
      integrity: entries.every((e) => e.chain_ok) ? "INTACT" : "BROKEN",
      count: entries.length,
    };
  }

  static verify(exported) {
    if (!exported || exported.genesis !== "0".repeat(64)) return { ok: false, reason: "bad-genesis" };
    let p = exported.genesis;
    for (const e of exported.entries) {
      if (chainValue(p, e.step, e.result) !== e.chain) return { ok: false, reason: "chain-broken", step: e.step };
      if (e.prev !== undefined && e.prev !== p) return { ok: false, reason: "linkage", step: e.step };
      p = e.chain;
    }
    return { ok: true, count: exported.entries.length };
  }
}
