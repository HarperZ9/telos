// Receipt bodies and tool results for the broker. Field names follow
// telos.receipt/v1 (DESIGN.md 4.1); the recorder seals and chains them.

// Flags the broker consumes itself; they never reach a driver or the digest.
export const CONTROL_FLAGS = Object.freeze(["hold", "dry-run"]);

const DOES_NOT_PROVE = Object.freeze({
  OK: "The action was dispatched and the named post-condition was checked. It does not show the task succeeded or that the target system recorded the effect.",
  REFUSED: "Nothing was dispatched. It does not show the action would have been harmful.",
  HOLD: "Nothing was dispatched. A hold records that a human decision is required; it is not an approval.",
  EXPIRED: "Nothing was dispatched. The approval window closed and a new hold was raised.",
  REJECTED: "Nothing was dispatched. A human rejected this exact action digest.",
  APPROVED: "A redeemed human decision covered this action digest. It does not show the action ran or succeeded.",
  DRY_RUN: "Nothing was dispatched. Tier, scope and digest were computed against the target as resolved at that moment.",
  ERROR: "The driver was called and raised an error. The target may be partly changed.",
});

export class Outcome {
  constructor({ recorder, sessionId, now }) {
    this.recorder = recorder;
    this.sessionId = sessionId;
    this.now = now;
  }

  body(c, status, extra = {}) {
    const { result, ...fields } = extra;
    return {
      schema: "telos.receipt/v1",
      session_id: this.sessionId,
      ts: new Date(this.now()).toISOString(),
      tier: c.tier,
      verb: c.verb ?? null,
      tool: "telos.native.control",
      module: "telos",
      grant_id: c.grant?.grant_id ?? null,
      scope_sha256: c.grant?.scope_sha256 ?? null,
      action_digest: c.digest ?? null,
      target_ref: c.target?.ref ?? null,
      target_fingerprint: c.target?.fingerprint ?? null,
      resolution: c.target?.resolution ?? null,
      status,
      executed: false,
      ...fields,
      does_not_prove: DOES_NOT_PROVE[status] ?? null,
    };
  }

  // Returns { seal, seq } or null when the recorder fails.
  record(c, status, extra = {}) {
    try {
      return this.recorder.append(this.body(c, status, extra));
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
