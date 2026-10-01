// chain.mjs - persistent, hash-chained, signed telos.receipt/v1 chains (DESIGN
// 4.1, 4.2). Every append writes the sealed receipt to
// <home>/receipts/<session>.jsonl before it returns, so a receipt exists even if
// the caller crashes after the effect. Heads are signed with the local ed25519
// key every `signEvery` receipts (1 by default, at most 32 for fast observe
// loops). Checkpoints {session, seq, head_seal, signature} go to
// <home>/receipts/checkpoints.jsonl every `checkpointEvery` receipts (256) and
// at close. Raw arguments, page text and frames go to owner-only side files under
// <home>/receipts/side/<seal>/; receipts hold digests. Single writer per session:
// two processes appending to one session file is unsupported.
import { randomBytes } from "node:crypto";
import { appendFileSync, existsSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { ensureDir, hasKey, loadSigner, telosHome } from "./keys.mjs";
import { DOES_NOT_PROVE, checkBody, orderedReceipt } from "./schema.mjs";
import {
  CHECKPOINT_SCHEMA, GENESIS, HASH_VERSION, MAX_SIGNATURE_BATCH, RECEIPT_SCHEMA, SIGNATURE_SCHEMA,
  checkpointPayload, sealOf, signaturePayload, verifyChain
} from "./verify.mjs";

const SESSION_RE = /^[A-Za-z0-9][A-Za-z0-9_.-]{0,79}$/;
const SIDE_NAME_RE = /^[a-z][a-z0-9_-]{0,39}\.(json|txt|bin|png)$/;

export function receiptsDir(home = telosHome()) {
  return path.join(home, "receipts");
}

export function newSessionId(now = new Date()) {
  return `s_${now.getTime().toString(36)}_${randomBytes(4).toString("hex")}`;
}

function resolveSigner(signer, home) {
  if (signer === "auto") return hasKey(home) ? loadSigner({ home }) : null;
  return signer ?? null;
}

// resume - read an existing session file and continue its chain. An unsigned
// tail (a crash between append and sign) is accepted and signed on the next
// append; any other verifier finding refuses to extend the file.
function resume(file, signer) {
  const text = readFileSync(file, "utf8");
  const trustedKey = signer ? { key_id: signer.key_id, public_key: signer.public_key } : undefined;
  const v = verifyChain(text, { trustedKey });
  const unsignedOnly = v.verdict === "UNVERIFIABLE" && (/unsigned$/.test(v.reason) || v.count === 0);
  if (v.verdict !== "MATCH" && !unsignedOnly) {
    throw new Error(`refusing to extend ${path.basename(file)}: ${v.verdict} ${v.reason}`);
  }
  return { seq: v.count, head: v.count ? (v.head_seal ?? lastSeal(text)) : GENESIS, signedThrough: v.signed_through };
}

function lastSeal(text) {
  const lines = text.trim().split(/\r?\n/).map((l) => JSON.parse(l)).filter((r) => r.schema === RECEIPT_SCHEMA);
  return lines.at(-1).seal;
}

export class ReceiptChain {
  // open - options: home, session_id, signer ("auto" loads the local key when
  // present; null persists unsigned and the verifier reports UNVERIFIABLE),
  // signEvery (1..32), checkpointEvery (default 256), now (clock seam).
  static open(options = {}) {
    const home = options.home ?? telosHome();
    const session_id = options.session_id ?? newSessionId();
    if (!SESSION_RE.test(session_id)) throw new TypeError(`invalid session id ${session_id}`);
    const signEvery = options.signEvery ?? 1;
    if (!Number.isSafeInteger(signEvery) || signEvery < 1 || signEvery > MAX_SIGNATURE_BATCH) {
      throw new RangeError(`signEvery must be 1..${MAX_SIGNATURE_BATCH}`);
    }
    const dir = ensureDir(receiptsDir(home));
    const signer = resolveSigner(options.signer ?? "auto", home);
    const file = path.join(dir, `${session_id}.jsonl`);
    const state = existsSync(file) ? resume(file, signer) : { seq: 0, head: GENESIS, signedThrough: 0 };
    return new ReceiptChain({ home, dir, file, session_id, signer, signEvery, state,
      checkpointEvery: options.checkpointEvery ?? 256, now: options.now ?? (() => new Date()) });
  }

  constructor({ home, dir, file, session_id, signer, signEvery, state, checkpointEvery, now }) {
    Object.assign(this, { home, dir, file, session_id, signer, signEvery, checkpointEvery, now });
    this.seq = state.seq;
    this.head = state.head;
    this.signedThrough = state.signedThrough;
    this.checkpointFile = path.join(dir, "checkpoints.jsonl");
  }

  // append - seal, persist, then sign and checkpoint on schedule. `side` maps a
  // side-file name (e.g. "args.json") to raw content; side files are written
  // after the seal exists and their names are listed in the receipt digests the
  // caller already supplied, never their content.
  append(body, { side } = {}) {
    checkBody(body);
    const receipt = this.#build(body);
    receipt.seal = sealOf(receipt);
    const line = JSON.stringify(orderedReceipt(receipt));
    appendFileSync(this.file, `${line}\n`, { mode: 0o600 });
    this.seq = receipt.seq;
    this.head = receipt.seal;
    if (side) this.#writeSide(receipt.seal, side);
    if (this.signer && this.seq - this.signedThrough >= this.signEvery) this.sign();
    if (this.signer && this.seq % this.checkpointEvery === 0) this.checkpoint();
    return JSON.parse(line);
  }

  #build(body) {
    const clean = JSON.parse(JSON.stringify(body));
    return {
      schema: RECEIPT_SCHEMA, hash_version: HASH_VERSION,
      receipt_id: `r_${randomBytes(8).toString("hex")}`, session_id: this.session_id,
      seq: this.seq + 1, prev_seal: this.head, ts: this.now().toISOString(),
      tool: null, module: "telos", module_version: null, grant_id: null, scope_sha256: null,
      action_digest: null, reason: "", executed: false, spawned: [], monitor: null,
      ...clean, does_not_prove: DOES_NOT_PROVE[clean.status], seal: ""
    };
  }

  #writeSide(seal, side) {
    const dir = ensureDir(path.join(this.dir, "side", seal));
    for (const [name, content] of Object.entries(side)) {
      if (!SIDE_NAME_RE.test(name)) throw new TypeError(`invalid side file name ${name}`);
      const data = typeof content === "string" || Buffer.isBuffer(content) ? content : JSON.stringify(content);
      writeFileSync(path.join(dir, name), data, { mode: 0o600, flag: "wx" });
    }
  }

  readSide(seal, name) {
    if (!/^[0-9a-f]{64}$/.test(seal) || !SIDE_NAME_RE.test(name)) throw new TypeError("invalid side file reference");
    return readFileSync(path.join(this.dir, "side", seal, name), "utf8");
  }

  // sign - sign the current head if any receipt after the last signature exists.
  sign() {
    if (!this.signer || this.seq === 0 || this.signedThrough === this.seq) return null;
    const rec = { schema: SIGNATURE_SCHEMA, session_id: this.session_id, seq: this.seq, head_seal: this.head,
      key_id: this.signer.key_id, public_key: this.signer.public_key };
    rec.sig = this.signer.sign(signaturePayload(rec));
    appendFileSync(this.file, `${JSON.stringify(rec)}\n`, { mode: 0o600 });
    this.signedThrough = this.seq;
    return rec;
  }

  checkpoint() {
    if (!this.signer || this.seq === 0 || this.checkpointedAt === this.seq) return null;
    this.sign();
    const rec = { schema: CHECKPOINT_SCHEMA, session: this.session_id, seq: this.seq, head_seal: this.head,
      key_id: this.signer.key_id, public_key: this.signer.public_key };
    rec.signature = this.signer.sign(checkpointPayload(rec));
    appendFileSync(this.checkpointFile, `${JSON.stringify(rec)}\n`, { mode: 0o600 });
    this.checkpointedAt = this.seq;
    return rec;
  }

  close() {
    return this.checkpoint();
  }

  verify(options = {}) {
    const checkpoints = existsSync(this.checkpointFile) ? readFileSync(this.checkpointFile, "utf8") : undefined;
    const trustedKey = this.signer ? { key_id: this.signer.key_id, public_key: this.signer.public_key } : undefined;
    return verifyChain(readFileSync(this.file, "utf8"), { checkpoints, trustedKey, ...options });
  }
}
