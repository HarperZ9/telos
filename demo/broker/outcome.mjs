// Receipt bodies and tool results for the broker. Bodies are telos.receipt/v1
// caller fields (DESIGN.md 4.1): the chain (demo/receipts/chain.mjs) adds
// schema, session, seq, links, does_not_prove and the seal, and refuses a body
// that breaks the contract, which stops the call (fail closed).
import { DOES_NOT_PROVE } from "../receipts/schema.mjs";

// Flags the broker consumes itself; they never reach a driver or the digest.
export const CONTROL_FLAGS = Object.freeze(["hold", "dry-run"]);

export class Outcome {
  constructor({ recorder, sessionId, now }) {
    this.recorder = recorder;
    this.sessionId = sessionId;
    this.now = now;
  }

  // An unknown verb has no tier floor; its refusal is recorded at T5, the
  // highest tier, so a reader never sees it as a low-risk call.
  body(c, status, extra = {}) {
    const { result, ...fields } = extra;
    const body = {
      ts: new Date(this.now()).toISOString(),
      tier: c.tier ?? "T5",
      verb: c.verb ? String(c.verb) : "unknown",
      tool: "telos.native.control",
      module: "telos",
      grant_id: c.grant?.grant_id ?? null,
      scope_sha256: c.grant?.scope_sha256 ?? null,
      action_digest: c.digest ?? null,
      target_ref: c.target?.ref ?? null,
      target_fingerprint: c.target?.fingerprint ?? null,
      status,
      executed: false,
      reason: "",
      ...fields,
    };
    if (c.target?.resolution) body.resolution = c.target.resolution;
    return body;
  }

  // Returns { seal, seq } or null when the recorder fails.
  record(c, status, extra = {}) {
    try {
      const r = this.recorder.append(this.body(c, status, extra));
      return { seal: r.seal, seq: r.seq };
    } catch {
      return null;
    }
  }

  result(c, status, extra = {}) {
    return {
      status,
      verb: c.verb ?? null,
      tier: c.tier,
      executed: false,
      action_digest: c.digest ?? null,
      grant_id: c.grant?.grant_id ?? null,
      target_ref: c.target?.ref ?? null,
      does_not_prove: DOES_NOT_PROVE[status] ?? null,
      ...extra,
    };
  }

  finish(c, status, extra = {}) {
    const rec = this.record(c, status, extra);
    return this.result(c, status, { ...extra, receipt_seal: rec?.seal ?? null, ...(rec ? {} : { recorder_error: true }) });
  }

  refuse(c, reason, detail) {
    return this.finish(c, "REFUSED", { reason, ...(detail ? { detail } : {}) });
  }
}
