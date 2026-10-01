// The Telos broker: the tier gate in front of every actuation verb (DESIGN.md
// 1.1 to 1.4, 3.2). Flow: tier floor, target resolution, prechecks, grant and
// scope, then run (T0 to T2) or hold for a human decision (T3 to T5). A call
// that cannot write its receipt does not run.
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { actionDigest as receiptActionDigest, argsSha256 } from "../receipts/digest.mjs";
import { precheck, selectGrant } from "./gate.mjs";
import { loadGrants } from "./grants.mjs";
import { HoldStore } from "./holds.mjs";
import { resolveTarget } from "./resolve.mjs";
import { LADDER, tierRank, verbSpec } from "./tiers.mjs";
import { CONTROL_FLAGS, Outcome } from "./outcome.mjs";

const sha = (buf) => createHash("sha256").update(buf).digest("hex");

// One action digest for the broker, dry run and replay (receipts/digest.mjs).
export function actionDigest({ tier, verb, target, params, flags, grant }) {
  return receiptActionDigest({
    tier, verb, target_ref: target.ref ?? null, target_fingerprint: target.fingerprint ?? null,
    args_sha256: argsSha256({ params, flags }), scope_sha256: grant.scope_sha256, grant_id: grant.grant_id,
  });
}

function capturePreimage(file, dir) {
  try {
    if (!existsSync(file)) return { ok: true, exists: false, sha256: null };
    const bytes = readFileSync(file);
    const digest = sha(bytes);
    mkdirSync(dir, { recursive: true, mode: 0o700 });
    const copy = path.join(dir, digest);
    if (!existsSync(copy)) writeFileSync(copy, bytes, { mode: 0o600 });
    return { ok: true, exists: true, sha256: digest, rollback: digest };
  } catch (err) {
    return { ok: false, error: err.code ?? err.message };
  }
}

function claimSlot(dir, grant) {
  if (grant.max_actions === undefined) return true;
  const d = path.join(dir, grant.grant_id);
  mkdirSync(d, { recursive: true, mode: 0o700 });
  for (let i = 0; i < grant.max_actions; i++) {
    try {
      writeFileSync(path.join(d, String(i)), "", { flag: "wx" });
      return true;
    } catch {
      // slot taken; try the next one
    }
  }
  return false;
}

// T5 grants bind to the first session that uses them.
function bindSession(dir, grant, sessionId) {
  const file = path.join(dir, `${grant.grant_id}.session`);
  try {
    writeFileSync(file, sessionId, { flag: "wx", mode: 0o600 });
    return true;
  } catch {
    return readFileSync(file, "utf8") === sessionId;
  }
}

// T2 fields, named as telos.receipt/v1 names them (DESIGN.md 1.5).
function verifyWrite(c) {
  if (c.verb !== "device.write" || !c.preimage) return {};
  const pre = { pre_image_digest: c.preimage.sha256 ?? null, rollback: c.preimage.rollback ?? null };
  try {
    const post = sha(readFileSync(c.target.path));
    const want = sha(Buffer.from(c.params.slice(1).join(" "), "utf8"));
    return { ...pre, post_image_digest: post, verify_result: post === want ? "MATCH" : "DRIFT" };
  } catch {
    return { ...pre, verify_result: "UNVERIFIABLE" };
  }
}

function cleanRequest(req) {
  const verb = req.verb;
  const spec = verbSpec(verb);
  const params = Array.isArray(req.params) ? req.params.map(String) : [];
  const flags = Object.fromEntries(Object.entries(req.flags ?? {}).filter(([k]) => !CONTROL_FLAGS.includes(k)));
  return { verb, spec, params, flags, tier: spec?.tier ?? null, grant: null, target: {} };
}

// The broker as a class so each step stays a short method. `call` is the only
// method a tool surface reaches; the human side lives in holds.decideHold.
export class Broker {
  constructor(opts) {
    this.opts = opts;
    this.dirs = opts.dirs;
    this.publicKey = opts.publicKey;
    this.sessionId = opts.sessionId;
    this.now = opts.now ?? (() => Date.now());
    this.platform = opts.platform ?? process.platform;
    this.holds = opts.holds ?? new HoldStore({ dir: opts.dirs.holds, publicKey: opts.publicKey, now: this.now });
    this.out = new Outcome({ recorder: opts.recorder, sessionId: opts.sessionId, now: this.now });
    this.ctx = { stateRoot: opts.dirs.root, platform: this.platform, protectedProcesses: opts.protectedProcesses ?? [] };
  }

  // Observe verbs that save a file write it to an owner-only side file unless
  // the caller named a path (which the gate has already scoped).
  runParams(c) {
    const i = c.spec.writeArg;
    if (i === undefined || c.params[i]) return c.params;
    const side = path.join(this.dirs.receipts, "side");
    mkdirSync(side, { recursive: true, mode: 0o700 });
    const copy = [...c.params];
    copy[i] = path.join(side, `${c.digest ?? "t0"}-${this.now()}.png`);
    return copy;
  }

  async execute(c, extra = {}) {
    let result;
    try {
      result = await this.opts.executor(c.verb, this.runParams(c), c.flags);
    } catch (err) {
      return this.out.finish(c, "ERROR", { ...extra, executed: true, reason: "EXECUTOR_ERROR", detail: err.message });
    }
    return this.out.finish(c, "OK", { ...extra, executed: true, result, ...verifyWrite(c) });
  }

  liveGrants() {
    return loadGrants(this.dirs.grants, { publicKey: this.publicKey, now: this.now() }).live;
  }

  async prepare(req) {
    const c = cleanRequest(req);
    if (!c.spec) return this.out.refuse(c, "UNKNOWN_VERB");
    if (c.spec.tier === "T0") return { c, ready: true };
    // Nothing is resolved, probed or attached for a verb no live grant names.
    const live = this.liveGrants();
    if (!live.some((g) => g.verbs.includes(c.verb) || (g.verbs.includes("*") && c.spec.tier === "T1"))) {
      return this.out.refuse(c, c.spec.reserved ? (c.spec.presence ? "PRESENCE_UNAVAILABLE" : "RESERVED_VERB") : "NO_GRANT");
    }
    try {
      c.target = await resolveTarget(c.verb, c.params, c.flags, { drivers: this.opts.drivers, cwd: this.opts.cwd });
    } catch (err) {
      return this.out.refuse(c, "TARGET_NOT_FOUND", err.message);
    }
    if (c.target.error) return this.out.refuse(c, c.target.error);
    const pre = precheck(c.spec, c.target, c.flags, this.ctx);
    if (pre) return this.out.refuse(c, pre.reason, pre.detail);
    c.preimage = c.spec.target === "path-write" ? capturePreimage(c.target.path, this.dirs.preimages) : null;
    const sel = selectGrant(c.verb, c.spec, c.target, live, { platform: this.platform, preimage: c.preimage });
    if (sel.reason) return this.out.refuse(c, sel.reason);
    Object.assign(c, sel);
    return { c, ready: true };
  }

  gateSession(c, holdId) {
    if (c.spec.suspendDuringHold || ["screen", "clipboard"].includes(c.spec.sense)) {
      if (this.holds.openFor(this.sessionId, holdId).length) return "SUSPENDED_DURING_HOLD";
    }
    if (LADDER[c.tier].session_bound && !bindSession(this.dirs.grants, c.grant, this.sessionId)) return "SESSION_BOUND";
    return null;
  }

  openHold(c, status, reason) {
    const holdId = this.holds.newId();
    const rec = this.out.record(c, status, { hold_id: holdId, reason, executed: false });
    if (!rec) return this.out.refuse(c, "RECORDER_FAILED");
    this.holds.open({
      hold_id: holdId, digests: [c.digest], tier: c.tier, verb: c.verb, grant_id: c.grant.grant_id,
      session_id: this.sessionId, window_s: LADDER[c.tier].window_s, review: { target_ref: c.target.ref, params: c.params },
    });
    this.opts.notify?.({ hold_id: holdId, verb: c.verb, tier: c.tier, target_ref: c.target.ref });
    return this.out.result(c, status, { hold_id: holdId, reason, executed: false, receipt_seal: rec.seal });
  }

  async confirmFlow(c, holdId) {
    const out = this.out;
    if (!holdId) {
      return this.holds.isRejected(c.digest) ? out.finish(c, "REJECTED", { reason: "REJECTED_DIGEST" }) : this.openHold(c, "HOLD", "AWAITING_HUMAN");
    }
    const r = this.holds.redeem(holdId, c.digest, this.sessionId);
    const next = {
      UNKNOWN: () => out.refuse(c, "HOLD_UNKNOWN"),
      OTHER_SESSION: () => out.refuse(c, "HOLD_OTHER_SESSION"),
      CONSUMED: () => out.refuse(c, "HOLD_CONSUMED"),
      PENDING: () => out.result(c, "HOLD", { hold_id: holdId, reason: "AWAITING_HUMAN", executed: false }),
      REJECTED: () => out.finish(c, "REJECTED", { hold_id: holdId, reason: "REJECTED_BY_HUMAN" }),
      EXPIRED: () => this.openHold(c, "EXPIRED", "APPROVAL_WINDOW_CLOSED"),
      MISMATCH: () => this.openHold(c, "HOLD", "DIGEST_MISMATCH"),
    };
    if (r.code !== "OK") return next[r.code]();
    return this.dispatch(c, { hold_id: holdId, decision_seal: r.hold.decision_seal });
  }

  dispatch(c, extra = {}) {
    if (!claimSlot(this.dirs.usage, c.grant)) return this.out.refuse(c, "MAX_ACTIONS");
    if (tierRank(c.tier) >= tierRank("T2") && !this.out.record(c, "APPROVED", { ...extra, executed: false, reason: "DISPATCH" })) {
      return this.out.refuse(c, "RECORDER_FAILED");
    }
    return this.execute(c, extra);
  }

  async call(req = {}) {
    const p = await this.prepare(req);
    if (!p.ready) return p;
    const { c } = p;
    if (c.tier === "T0") return this.execute(c);
    const blocked = this.gateSession(c, req.hold_id ?? null);
    if (blocked) return this.out.refuse(c, blocked);
    c.digest = actionDigest(c);
    if (req.dry_run) return this.out.finish(c, "DRY_RUN", { executed: false, would_hold: LADDER[c.tier].confirm });
    if (!LADDER[c.tier].confirm) return this.dispatch(c);
    return this.confirmFlow(c, req.hold_id ?? null);
  }
}

export function createBroker(opts) {
  return new Broker(opts);
}
