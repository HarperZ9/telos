// Interim receipt recorder for the tier gate. The broker needs one thing from a
// recorder: append(body) returns { seal, seq } or throws, and a throw stops the
// action (fail closed). The receipt-core slice (DESIGN.md 4.1, 4.2) supplies the
// signed telos.receipt/v1 chain with the same method; until it merges this one
// seals each body with sha256 over the canonical form and chains prev_seal.
import { appendFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
import path from "node:path";
import { digestOf } from "./canonical.mjs";

const GENESIS = "0".repeat(64);

export class JsonlRecorder {
  constructor(file) {
    this.file = file;
    mkdirSync(path.dirname(file), { recursive: true, mode: 0o700 });
    this.seq = 0;
    this.prev = GENESIS;
    if (existsSync(file)) {
      const lines = readFileSync(file, "utf8").split("\n").filter(Boolean);
      if (lines.length) {
        const last = JSON.parse(lines[lines.length - 1]);
        this.seq = last.seq;
        this.prev = last.seal;
      }
    }
  }

  append(body) {
    const entry = { ...body, seq: this.seq + 1, prev_seal: this.prev, seal: "" };
    entry.seal = digestOf({ ...entry, seal: "" });
    appendFileSync(this.file, `${JSON.stringify(entry)}\n`, { mode: 0o600 });
    this.seq = entry.seq;
    this.prev = entry.seal;
    return { seal: entry.seal, seq: entry.seq };
  }
}

export class MemoryRecorder {
  constructor() {
    this.entries = [];
  }

  append(body) {
    const prev = this.entries.at(-1)?.seal ?? GENESIS;
    const entry = { ...body, seq: this.entries.length + 1, prev_seal: prev, seal: "" };
    entry.seal = digestOf({ ...entry, seal: "" });
    this.entries.push(entry);
    return { seal: entry.seal, seq: entry.seq };
  }
}
