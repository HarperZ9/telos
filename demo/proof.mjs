import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { assemblePacket, verifyPacket, canonicalBytes, stableStringify } from "./proof-core.mjs";
import { runWitness } from "./proof-witness.mjs";
import { toProofSurfacePacket } from "./proof-export.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));

export { assemblePacket, verifyPacket, toProofSurfacePacket, stableStringify };

function loadConventions() {
  return JSON.parse(readFileSync(path.join(here, "integrations", "proof-packet-conventions.json"), "utf8"));
}

// Attach the verifier result and witness stage to an assembled packet. The
// witness runs over the packet's own canonical bytes as source and its
// re-derived canonical bytes as view (identical by construction on a clean
// packet, so a reachable EMET reports COHERENT).
function verifyAndWitness(packet, embeddedVerdict) {
  const verifier = verifyPacket(packet, { embeddedVerdict });
  const canonical = canonicalBytes(packet);
  const witness = runWitness(canonical, canonical);
  const withResults = { ...packet, packet_hash: packet.packet_hash, verifier };
  withResults.witness = witness;
  withResults.witness_coverage = witness.status === "unavailable" ? "not_witnessed" : "witnessed";
  // A reachable witness that reports DRIFT lowers the overall verdict; an
  // unavailable optional witness is disclosed coverage loss, not counterevidence.
  if (witness.status === "witnessed" && witness.verdict === "DRIFT") {
    withResults.verifier = { ...verifier, verdict: "DRIFT", witness_lowered: true };
  }
  return withResults;
}

function exitCodeFor(verdict) {
  if (verdict === "MATCH") return 0;
  if (verdict === "DRIFT") return 1;
  return 2;
}

function writeOut(dir, packet) {
  mkdirSync(dir, { recursive: true });
  const packetPath = path.join(dir, "packet.json");
  const canonicalPath = path.join(dir, "packet.canonical.json");
  writeFileSync(packetPath, `${JSON.stringify(packet, null, 2)}\n`, "utf8");
  writeFileSync(canonicalPath, canonicalBytes(packet), "utf8");
  return { packetPath, canonicalPath };
}

function summarize(packet, paths) {
  const lines = [];
  lines.push(`packet_id     ${packet.packet_id}`);
  lines.push(`packet_hash   ${packet.packet_hash}`);
  lines.push(`verdict       ${packet.verifier?.verdict}`);
  lines.push(`witness       ${packet.witness?.status} / ${packet.witness?.verdict}`);
  const failures = packet.verifier?.failures ?? [];
  if (failures.length) {
    lines.push("failures");
    for (const f of failures) {
      lines.push(`  ${f.code} (${f.verdict})`);
    }
  }
  if (paths) {
    lines.push(`packet        ${paths.packetPath}`);
    lines.push(`canonical     ${paths.canonicalPath}`);
  }
  return lines.join("\n");
}

function runAgentAction(args) {
  const json = args.includes("--json");
  const outIndex = args.indexOf("--out");
  const outDir = outIndex >= 0 ? args[outIndex + 1] : null;
  const fixtureIndex = args.indexOf("--fixture");
  let fixture;
  if (args.includes("--demo")) {
    fixture = loadConventions().conformance_fixture.happy_path;
  } else if (fixtureIndex >= 0 && args[fixtureIndex + 1] && !args[fixtureIndex + 1].startsWith("--")) {
    fixture = JSON.parse(readFileSync(args[fixtureIndex + 1], "utf8"));
  } else {
    process.stderr.write("usage: proof agent-action --demo|--fixture <path> [--out <dir>] [--json]\n");
    return 2;
  }
  const assembled = assemblePacket(fixture);
  const packet = verifyAndWitness(assembled, undefined);
  let paths = null;
  if (outDir) {
    paths = writeOut(outDir, packet);
  }
  if (json) {
    process.stdout.write(`${JSON.stringify(packet, null, 2)}\n`);
  } else {
    process.stdout.write(`${summarize(packet, paths)}\n`);
  }
  return exitCodeFor(packet.verifier?.verdict);
}

function readPacketArg(arg) {
  if (arg === "-") {
    return JSON.parse(readFileSync(0, "utf8"));
  }
  return JSON.parse(readFileSync(arg, "utf8"));
}

function runVerify(args) {
  const json = args.includes("--json");
  const target = args.find((a) => a !== "--json" && a !== "verify");
  if (!target) {
    process.stderr.write("usage: proof verify <packet.json|-> [--json]\n");
    return 2;
  }
  const input = readPacketArg(target);
  // Replay: re-run the verifier over the packet's own materials. Any embedded
  // verifier.verdict is checked against the freshly derived one, so a canned
  // MATCH over tampered materials fails.
  const embedded = input.verifier?.verdict;
  const verifier = verifyPacket(input, { embeddedVerdict: embedded });
  const canonical = canonicalBytes(input);
  const witness = runWitness(canonical, canonical);
  let overall = verifier.verdict;
  if (witness.status === "witnessed" && witness.verdict === "DRIFT") {
    overall = "DRIFT";
  }
  const report = {
    schema: "project-telos.proof-packet-verification/v1",
    packet_id: input.packet_id,
    verdict: overall,
    checks: verifier.checks,
    failures: verifier.failures,
    witness,
    witness_coverage: witness.status === "unavailable" ? "not_witnessed" : "witnessed"
  };
  if (json) {
    process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
  } else {
    const lines = [`verdict       ${overall}`, `witness       ${witness.status} / ${witness.verdict}`];
    for (const f of verifier.failures) {
      lines.push(`  ${f.code} (${f.verdict}) ${f.path ?? f.name ?? ""}`.trimEnd());
    }
    process.stdout.write(`${lines.join("\n")}\n`);
  }
  return exitCodeFor(overall);
}

function runExport(args) {
  const json = args.includes("--json");
  const target = args.find((a) => a !== "--json" && a !== "export");
  if (!target) {
    process.stderr.write("usage: proof export <packet.json|-> [--json]\n");
    return 2;
  }
  const input = readPacketArg(target);
  const exported = toProofSurfacePacket(input);
  process.stdout.write(`${JSON.stringify(exported, null, json ? 2 : 2)}\n`);
  return 0;
}

function main() {
  const [subcommand, ...args] = process.argv.slice(2);
  let code;
  if (subcommand === "agent-action") {
    code = runAgentAction(args);
  } else if (subcommand === "verify") {
    code = runVerify(args);
  } else if (subcommand === "export") {
    code = runExport(args);
  } else {
    process.stderr.write(
      "usage: proof <agent-action --demo|--fixture <path> | verify <packet.json|-> | export <packet.json|->> [--out <dir>] [--json]\n"
    );
    code = 2;
  }
  process.exit(code);
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main();
}
