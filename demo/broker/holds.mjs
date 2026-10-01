// Holds and confirmation (DESIGN.md 1.3). A hold is server-side state keyed by
// action digest. The model receives a hold_id, never an approval code. Only a
// human at a terminal can sign a decision; redemption is single-use per digest,
// enforced with an exclusive-create marker so two processes cannot both redeem.
import { randomBytes } from "node:crypto";
import { existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { canonical } from "./canonical.mjs";
import { keyId, requireTty, signText, verifyText } from "./keys.mjs";

const HOLD_ID = /^h_[0-9a-f]{32}$/;
const DIGEST = /^[0-9a-f]{64}$/;

const holdFile = (dir, id) => path.join(dir, `${id}.json`);
const decisionFile = (dir, id) => path.join(dir, `${id}.decision.json`);
const redeemedFile = (dir, id, digest) => path.join(dir, `${id}.${digest}.redeemed`);
const rejectedFile = (dir, digest) => path.join(dir, "rejected", digest);

function readJson(file) {
  try {
    return JSON.parse(readFileSync(file, "utf8"));
  } catch {
    return null;
  }
}

const decisionBody = (d) => ({ hold_id: d.hold_id, digests: d.digests, decision: d.decision, decided_at: d.decided_at, window_s: d.window_s, channel: d.channel });

export class HoldStore {
  constructor({ dir, publicKey, now = () => Date.now(), idGen } = {}) {
    this.dir = dir;
    this.publicKey = publicKey;
    this.now = now;
    this.idGen = idGen ?? (() => `h_${randomBytes(16).toString("hex")}`);
    mkdirSync(path.join(dir, "rejected"), { recursive: true, mode: 0o700 });
  }

  newId() {
    return this.idGen();
  }

  open({ hold_id, digests, tier, verb, grant_id, session_id, window_s, review }) {
    if (!digests.every((d) => DIGEST.test(d))) throw new Error("hold digests must be sha256 hex");
    const created = this.now();
    const hold = {
      schema: "telos.hold/v1", hold_id, digests, tier, verb, grant_id, session_id, window_s,
      created_at: new Date(created).toISOString(), expires_at: new Date(created + window_s * 1000).toISOString(),
      review,
    };
    writeFileSync(holdFile(this.dir, hold_id), `${JSON.stringify(hold, null, 2)}\n`, { flag: "wx", mode: 0o600 });
    return hold;
  }

  // A decision counts only when its signature verifies and it names the hold's digests.
  decision(hold) {
    const d = readJson(decisionFile(this.dir, hold.hold_id));
    if (!d || !this.publicKey || d.hold_id !== hold.hold_id) return null;
    if (d.key_id !== keyId(this.publicKey)) return null;
    if (!verifyText(this.publicKey, canonical(decisionBody(d)), d.sig)) return null;
    if (canonical(d.digests) !== canonical(hold.digests)) return null;
    return d;
  }

  get(holdId) {
    if (!HOLD_ID.test(String(holdId))) return null;
    const hold = readJson(holdFile(this.dir, holdId));
    if (!hold) return null;
    const d = this.decision(hold);
    const now = this.now();
    let status = "PENDING";
    if (d?.decision === "reject") status = "REJECTED";
    else if (d?.decision === "approve") {
      const done = hold.digests.every((dg) => existsSync(redeemedFile(this.dir, holdId, dg)));
      status = done ? "CONSUMED" : now > Date.parse(d.decided_at) + d.window_s * 1000 ? "EXPIRED" : "APPROVED";
    } else if (now > Date.parse(hold.expires_at)) status = "EXPIRED";
    return { ...hold, status, decision_seal: d ? d.sig : null };
  }

  // Codes: OK, UNKNOWN, OTHER_SESSION, PENDING, REJECTED, EXPIRED, CONSUMED, MISMATCH.
  redeem(holdId, digest, sessionId) {
    const hold = this.get(holdId);
    if (!hold) return { code: "UNKNOWN" };
    if (hold.session_id !== sessionId) return { code: "OTHER_SESSION", hold };
    if (!hold.digests.includes(digest)) return { code: "MISMATCH", hold };
    if (hold.status !== "APPROVED") return { code: hold.status, hold };
    try {
      writeFileSync(redeemedFile(this.dir, holdId, digest), new Date(this.now()).toISOString(), { flag: "wx", mode: 0o600 });
    } catch {
      return { code: "CONSUMED", hold };
    }
    return { code: "OK", hold };
  }

  isRejected(digest) {
    return DIGEST.test(digest) && existsSync(rejectedFile(this.dir, digest));
  }

  // Holds of this session that are still waiting on a human or on redemption.
  openFor(sessionId, exceptId = null) {
    const out = [];
    for (const name of readdirSync(this.dir).filter((n) => /^h_[0-9a-f]{32}\.json$/.test(n))) {
      const id = name.slice(0, -5);
      if (id === exceptId) continue;
      const hold = this.get(id);
      if (hold && hold.session_id === sessionId && (hold.status === "PENDING" || hold.status === "APPROVED")) out.push(hold);
    }
    return out;
  }

  pending() {
    return readdirSync(this.dir)
      .filter((n) => /^h_[0-9a-f]{32}\.json$/.test(n))
      .map((n) => this.get(n.slice(0, -5)))
      .filter((h) => h && h.status === "PENDING");
  }
}

// The human side. Needs a terminal and the private key; the broker never calls it.
export function decideHold(store, holdId, decision, { privateKey, publicKey, isTTY, channel = "tty" } = {}) {
  requireTty(isTTY, "telos confirm");
  if (decision !== "approve" && decision !== "reject") throw new Error("decision must be approve or reject");
  const hold = store.get(holdId);
  if (!hold) throw new Error(`no hold ${holdId}`);
  if (hold.status !== "PENDING") throw new Error(`hold ${holdId} is ${hold.status}, not PENDING`);
  const body = decisionBody({ hold_id: holdId, digests: hold.digests, decision, decided_at: new Date(store.now()).toISOString(), window_s: hold.window_s, channel });
  const record = { ...body, key_id: keyId(publicKey), sig: signText(privateKey, canonical(body)) };
  writeFileSync(decisionFile(store.dir, holdId), `${JSON.stringify(record, null, 2)}\n`, { flag: "wx", mode: 0o600 });
  if (decision === "reject") for (const dg of hold.digests) writeFileSync(rejectedFile(store.dir, dg), holdId, { mode: 0o600 });
  return record;
}
