#!/usr/bin/env node
// verify_packet.mjs -- standalone integrity verifier for a Project Telos sealed
// artifact. Imports only the Node standard library (node:crypto, node:fs) and
// nothing from the telos package, so a stranger with one artifact re-derives its
// seal offline: `node verify_packet.mjs artifact.json`. A proof packet is sealed
// by packetHash over its canonical bytes; a native-control ledger export by the
// chainValue chain. This file re-reads the artifact, recomputes the seal from its
// own bytes, and compares. Exit 0 MATCH, 1 DRIFT, 2 UNVERIFIABLE (missing,
// unreadable, or a schema not re-derivable here). Honest null: a packet
// ledger_ref anchors an external chain the packet does not embed, kept UNVERIFIABLE.
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";

// packetHash lane: compact sorted-key serialization, mirroring proof-hash.mjs.
function stableStringify(value) {
  if (Array.isArray(value)) return `[${value.map(stableStringify).join(",")}]`;
  if (value && typeof value === "object") {
    const body = Object.keys(value).sort().map((k) => `${JSON.stringify(k)}:${stableStringify(value[k])}`);
    return `{${body.join(",")}}`;
  }
  return JSON.stringify(value);
}

const UNHASHED = new Set(["packet_hash", "verifier", "witness", "wall_clock", "witness_coverage"]);

function packetHash(packet) {
  const scope = {};
  for (const key of Object.keys(packet)) if (!UNHASHED.has(key)) scope[key] = packet[key];
  return `sha256:${createHash("sha256").update(Buffer.from(stableStringify(scope), "utf8")).digest("hex")}`;
}

// chainValue lane: spaced sorted-key serialization, mirroring ledger.mjs.
function canonicalJson(value) {
  if (value === null || typeof value === "undefined") return "null";
  if (typeof value === "string") return JSON.stringify(value);
  if (typeof value === "number" || typeof value === "boolean") return String(value);
  if (typeof value === "bigint") return value.toString();
  if (typeof value !== "object") return JSON.stringify(value);
  if (Array.isArray(value)) return `[${value.map(canonicalJson).join(", ")}]`;
  const body = Object.keys(value).sort().map((k) => `${JSON.stringify(k)}: ${canonicalJson(value[k])}`);
  return `{${body.join(", ")}}`;
}

const GENESIS = "0".repeat(64);

function chainValue(prev, stepId, result) {
  return createHash("sha256").update(prev + String(stepId) + canonicalJson(result), "utf8").digest("hex");
}

const PROOF_SCHEMAS = new Set([
  "project-telos.proof-packet/v1",
  "project-telos.research-proof-packet/v1",
  "project-telos.visual-proof-packet/v1",
  "project-telos.build-proof-packet/v1"
]);

function verifyProofPacket(packet) {
  const recorded = packet.packet_hash;
  if (typeof recorded !== "string") {
    return ["UNVERIFIABLE", "proof packet carries no packet_hash to re-derive"];
  }
  const derived = packetHash(packet);
  if (derived !== recorded) {
    return ["DRIFT", `packet_hash recorded ${recorded} but recomputes to ${derived}`];
  }
  return ["MATCH", `packet_hash re-derives over the packet canonical bytes: ${derived}`];
}

function verifyLedger(ledger) {
  if (ledger.genesis !== GENESIS) {
    return ["UNVERIFIABLE", "ledger genesis is not the 64-zero anchor"];
  }
  const entries = Array.isArray(ledger.entries) ? ledger.entries : [];
  let prev = GENESIS;
  for (const entry of entries) {
    if (chainValue(prev, entry.step, entry.result) !== entry.chain) {
      return ["DRIFT", `chainValue does not re-derive at step ${entry.step}`];
    }
    if (entry.prev !== undefined && entry.prev !== prev) {
      return ["DRIFT", `chain linkage broken at step ${entry.step}`];
    }
    prev = entry.chain;
  }
  return ["MATCH", `chainValue re-derives across ${entries.length} ledger entries`];
}

function verify(artifact) {
  const schema = artifact.schema;
  if (schema === "project-telos.native-control-ledger/v1") {
    return verifyLedger(artifact);
  }
  if (PROOF_SCHEMAS.has(schema) || schema === undefined) {
    return verifyProofPacket(artifact);
  }
  return ["UNVERIFIABLE", `no standalone re-derivation for schema ${schema}`];
}

function main(argv) {
  const target = argv[0];
  if (!target) {
    process.stderr.write("usage: node verify_packet.mjs <artifact.json>\n");
    return 2;
  }
  let artifact;
  try {
    artifact = JSON.parse(readFileSync(target, "utf8"));
  } catch (err) {
    process.stdout.write(`UNVERIFIABLE  artifact unreadable: ${err.message}\n`);
    return 2;
  }
  const [verdict, detail] = verify(artifact);
  process.stdout.write(`${verdict}  ${detail}\n`);
  return verdict === "MATCH" ? 0 : verdict === "DRIFT" ? 1 : 2;
}

process.exit(main(process.argv.slice(2)));
