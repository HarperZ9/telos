// Receipt recorders for the broker. The broker needs one thing from a
// recorder: append(body) returns { seal, seq } or throws, and a throw stops the
// action (fail closed).
//
// ChainRecorder is the production recorder: the signed, hash-chained
// telos.receipt/v1 chain in demo/receipts/chain.mjs, keyed by the same local
// key that signs grants. MemoryRecorder is the unit-test recorder; it applies
// the same writer checks, so a body that the chain would refuse fails the
// broker tests too.
import { ReceiptChain } from "../receipts/chain.mjs";
import { checkBody } from "../receipts/schema.mjs";
import { GENESIS, sealOf } from "../receipts/verify.mjs";

export class ChainRecorder {
  constructor({ home, sessionId, signer = "auto" }) {
    this.home = home;
    this.sessionId = sessionId;
    this.signer = signer;
    this.chain = null;
  }

  // Opened on first append, so a call that writes no receipt never opens it.
  append(body) {
    this.chain ??= ReceiptChain.open({ home: this.home, session_id: this.sessionId, signer: this.signer });
    return this.chain.append(body);
  }

  close() {
    return this.chain?.close() ?? null;
  }
}

export class MemoryRecorder {
  constructor() {
    this.entries = [];
  }

  append(body) {
    checkBody(body);
    const prev = this.entries.at(-1)?.seal ?? GENESIS;
    const entry = { ...JSON.parse(JSON.stringify(body)), seq: this.entries.length + 1, prev_seal: prev, seal: "" };
    entry.seal = sealOf(entry);
    this.entries.push(entry);
    return { seal: entry.seal, seq: entry.seq };
  }
}
