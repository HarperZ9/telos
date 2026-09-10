import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { mkdtempSync, writeFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { Ledger } from "./native-control/ledger.mjs";

const verifier = fileURLToPath(new URL("../verify_packet.mjs", import.meta.url));
const clone = (value) => JSON.parse(JSON.stringify(value));

function fixture() {
  const ledger = new Ledger({ runId: "synthetic-run", name: "synthetic-task" });
  ledger.append("s1", { action: "read", target: "https://example.invalid/one", ok: true, result: { value: "one" } });
  ledger.append("s2", { action: "read", target: "https://example.invalid/two", ok: false, result: { error: "synthetic failure" } });
  return ledger.export();
}

function standalone(packet) {
  const dir = mkdtempSync(path.join(tmpdir(), "telos-ledger-boundary-"));
  try {
    const file = path.join(dir, "ledger.json");
    writeFileSync(file, JSON.stringify(packet));
    return spawnSync(process.execPath, [verifier, file], { encoding: "utf8" });
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
}

test("new ledger metadata edits fail both verifiers after a JSON round trip", () => {
  const packet = fixture();
  assert.equal(Ledger.verify(packet).ok, true);
  assert.equal(standalone(packet).status, 0);
  const mutations = [
    (p) => { p.entries[0].action = "write"; },
    (p) => { p.entries[0].target = "https://example.invalid/wrong"; },
    (p) => { p.entries[0].ok = false; },
    (p) => { p.entries[0].step = "other-step"; },
    (p) => { p.entries[0].result.value = "wrong"; },
    (p) => { p.entries[0].extra = "injected"; },
    (p) => { p.runId = "other-run"; },
    (p) => { p.name = "other-task"; },
    (p) => { delete p.hash_version; },
    (p) => { p.entries.reverse(); },
  ];
  for (const mutate of mutations) {
    const changed = clone(packet);
    mutate(changed);
    assert.equal(Ledger.verify(changed).ok, false, mutate.toString());
    assert.equal(standalone(changed).status, 1, mutate.toString());
  }
});

test("legacy result-only chains remain readable with an explicit limited scope", () => {
  // Independent known v1 wire bytes, not the implementation's hash helper.
  const chain = createHash("sha256").update("0".repeat(64) + 's1{"ok": true}').digest("hex");
  const packet = {
    schema: "project-telos.native-control-ledger/v1", genesis: "0".repeat(64),
    entries: [{ step: "s1", action: "changed outside the hash", target: "unbound", ok: false, result: { ok: true }, chain }],
  };
  const result = Ledger.verify(packet);
  assert.equal(result.ok, true);
  assert.equal(result.integrity_scope, "legacy-step-and-result-only");
  const external = standalone(packet);
  assert.equal(external.status, 0);
  assert.match(external.stdout, /legacy.*step.*result.*metadata.*not bound/i);
});

test("unknown hash versions and malformed entries cannot become an empty valid ledger", () => {
  for (const packet of [
    { ...fixture(), hash_version: 999 },
    { ...fixture(), entries: undefined },
    { ...fixture(), entries: [null] },
  ]) {
    assert.equal(Ledger.verify(packet).ok, false);
    assert.equal(standalone(packet).status, 2);
  }
});

test("new receipts snapshot JSON values so shared objects and later input edits do not drift", () => {
  const result = { nested: { text: "synthetic" } };
  result.shared = result.nested;
  const ledger = new Ledger({ runId: "synthetic" });
  ledger.append("s1", { action: "read", target: "fixture", ok: true, result });
  result.nested.text = "changed later";
  const packet = clone(ledger.export());
  assert.equal(packet.entries[0].result.nested.text, "synthetic");
  assert.equal(Ledger.verify(packet).ok, true);
  assert.equal(standalone(packet).status, 0);
});
