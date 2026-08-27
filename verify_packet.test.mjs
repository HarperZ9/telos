// End-to-end test for the vendored zero-import verifier verify_packet.mjs.
// It produces a REAL proof packet from the shipped proof CLI, then drives the
// vendored verifier as a stranger would: subprocess in, exit code out. The
// packetHash path (proof packet) and the chainValue path (native-control
// ledger) are each checked clean, tampered, and unreadable.
import { spawnSync } from "node:child_process";
import { mkdtempSync, writeFileSync, readFileSync } from "node:fs";
import path from "node:path";
import os from "node:os";
import { fileURLToPath } from "node:url";
import { Ledger } from "./demo/native-control/ledger.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const verifier = path.join(here, "verify_packet.mjs");
const proofCli = path.join(here, "demo", "proof.mjs");

let pass = 0;
let fail = 0;
const ok = (name, cond) => {
  if (cond) {
    pass++;
  } else {
    fail++;
    console.log("FAIL", name);
  }
};

function run(target) {
  return spawnSync(process.execPath, [verifier, target], { encoding: "utf8" });
}

const dir = mkdtempSync(path.join(os.tmpdir(), "verify-packet-test-"));

// A real proof packet, sealed by the shipped assembler (packetHash lane).
const build = spawnSync(process.execPath, [proofCli, "agent-action", "--demo", "--out", dir], {
  encoding: "utf8"
});
ok("proof CLI produced a packet", build.status === 0);
const packetPath = path.join(dir, "packet.json");

const clean = run(packetPath);
ok("clean packet exits 0 (MATCH)", clean.status === 0);

// Tamper one hashed content byte: the recomputed packetHash must no longer
// match the recorded one.
const packet = JSON.parse(readFileSync(packetPath, "utf8"));
packet.objective.claim = `${packet.objective.claim}X`;
const tamperedPath = path.join(dir, "packet.tampered.json");
writeFileSync(tamperedPath, JSON.stringify(packet, null, 2), "utf8");
const tampered = run(tamperedPath);
ok("tampered packet exits 1 (DRIFT)", tampered.status === 1);

// Missing artifact is UNVERIFIABLE, not a false clean pass.
const missing = run(path.join(dir, "does-not-exist.json"));
ok("missing packet exits 2 (UNVERIFIABLE)", missing.status === 2);

// A native-control ledger export, sealed by the chainValue hash chain.
const led = new Ledger({ runId: "run_verify_test", name: "verify-test" });
led.append("s1", { action: "navigate", target: "https://x", ok: true, result: { url: "https://x" } });
led.append("s2", { action: "fill", target: "#email", ok: true, result: { set: "#email" } });
const ledgerExport = led.export();
const ledgerPath = path.join(dir, "ledger.json");
writeFileSync(ledgerPath, `${JSON.stringify(ledgerExport, null, 2)}\n`, "utf8");
const cleanLedger = run(ledgerPath);
ok("clean ledger exits 0 (MATCH)", cleanLedger.status === 0);

const badLedger = JSON.parse(JSON.stringify(ledgerExport));
badLedger.entries[0].result.url = "https://EVIL";
const badLedgerPath = path.join(dir, "ledger.tampered.json");
writeFileSync(badLedgerPath, `${JSON.stringify(badLedger, null, 2)}\n`, "utf8");
const tamperedLedger = run(badLedgerPath);
ok("tampered ledger exits 1 (DRIFT)", tamperedLedger.status === 1);

console.log(`\npass ${pass} / fail ${fail}`);
process.exit(fail ? 1 : 0);
