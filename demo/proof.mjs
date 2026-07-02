import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { assemblePacket, verifyPacket, canonicalBytes, stableStringify } from "./proof-core.mjs";
import { runWitness } from "./proof-witness.mjs";
import { toProofSurfacePacket } from "./proof-export.mjs";
import {
  assembleResearchPacket,
  verifyResearchPacket,
  toProofSurfaceResearchPacket
} from "./proof-research.mjs";
import {
  assembleVisualPacket,
  verifyVisualPacket,
  toProofSurfaceVisualPacket
} from "./proof-visual.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));

export { assemblePacket, verifyPacket, toProofSurfacePacket, stableStringify };

// Schema ids for the three lanes. verify and export dispatch on the packet's own
// schema field so a research packet is never checked by the agent-action verifier
// and vice versa.
const AGENT_ACTION_SCHEMA = "project-telos.proof-packet/v1";
const RESEARCH_SCHEMA = "project-telos.research-proof-packet/v1";
const VISUAL_SCHEMA = "project-telos.visual-proof-packet/v1";

function loadConventions() {
  return JSON.parse(readFileSync(path.join(here, "integrations", "proof-packet-conventions.json"), "utf8"));
}

function loadResearchConventions() {
  return JSON.parse(
    readFileSync(path.join(here, "integrations", "research-proof-packet-conventions.json"), "utf8")
  );
}

function loadVisualConventions() {
  return JSON.parse(
    readFileSync(path.join(here, "integrations", "visual-proof-packet-conventions.json"), "utf8")
  );
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

// Resolve a fixture for the research/visual subcommands: --demo pulls the frozen
// happy-path conformance fixture, --fixture <path> loads a fixture file. Returns
// { fixture } on success or { usage } with the usage string on a bad invocation.
function resolveFixtureArgs(args, lane, loadHappy) {
  const fixtureIndex = args.indexOf("--fixture");
  if (args.includes("--demo")) {
    return { fixture: loadHappy() };
  }
  if (fixtureIndex >= 0 && args[fixtureIndex + 1] && !args[fixtureIndex + 1].startsWith("--")) {
    return { fixture: JSON.parse(readFileSync(args[fixtureIndex + 1], "utf8")) };
  }
  return { usage: `usage: proof ${lane} --demo|--fixture <path> [--out <dir>] [--json]\n` };
}

function summarizeLane(packet, verifier, paths) {
  const lines = [];
  lines.push(`packet_id     ${packet.packet_id}`);
  lines.push(`packet_hash   ${packet.packet_hash}`);
  lines.push(`verdict       ${verifier.verdict}`);
  for (const f of verifier.failures ?? []) {
    lines.push(`  ${f.code} (${f.verdict}) ${f.path ?? f.name ?? f.ref ?? ""}`.trimEnd());
  }
  if (paths) {
    lines.push(`packet        ${paths.packetPath}`);
    lines.push(`canonical     ${paths.canonicalPath}`);
  }
  return lines.join("\n");
}

// Research lane: assemble -> verify (no Emet witness stage; the research verifier
// recomputes source and negative-fixture digests from embedded bodies). The
// emitted packet carries the verifier block so a piped verify re-derives it.
function runResearch(args) {
  const json = args.includes("--json");
  const outIndex = args.indexOf("--out");
  const outDir = outIndex >= 0 ? args[outIndex + 1] : null;
  const resolved = resolveFixtureArgs(args, "research", () => loadResearchConventions().conformance_fixture.happy_path);
  if (resolved.usage) {
    process.stderr.write(resolved.usage);
    return 2;
  }
  const assembled = assembleResearchPacket(resolved.fixture);
  const verifier = verifyResearchPacket(assembled, { embeddedVerdict: assembled.verdicts?.overall });
  const packet = { ...assembled, verifier };
  let paths = null;
  if (outDir) {
    paths = writeOut(outDir, packet);
  }
  if (json) {
    process.stdout.write(`${JSON.stringify(packet, null, 2)}\n`);
  } else {
    process.stdout.write(`${summarizeLane(packet, verifier, paths)}\n`);
  }
  return exitCodeFor(verifier.verdict);
}

// Visual lane: assemble -> verify (no Emet witness stage; the visual verifier
// recomputes each measurement from the artifact's embedded sRGB samples).
function runVisual(args) {
  const json = args.includes("--json");
  const outIndex = args.indexOf("--out");
  const outDir = outIndex >= 0 ? args[outIndex + 1] : null;
  const resolved = resolveFixtureArgs(args, "visual", () => loadVisualConventions().conformance_fixture.happy_path);
  if (resolved.usage) {
    process.stderr.write(resolved.usage);
    return 2;
  }
  const assembled = assembleVisualPacket(resolved.fixture);
  const verifier = verifyVisualPacket(assembled, { embeddedVerdict: assembled.verifier?.verdict });
  const packet = { ...assembled, verifier };
  let paths = null;
  if (outDir) {
    paths = writeOut(outDir, packet);
  }
  if (json) {
    process.stdout.write(`${JSON.stringify(packet, null, 2)}\n`);
  } else {
    process.stdout.write(`${summarizeLane(packet, verifier, paths)}\n`);
  }
  return exitCodeFor(verifier.verdict);
}

function readPacketArg(arg) {
  if (arg === "-") {
    return JSON.parse(readFileSync(0, "utf8"));
  }
  return JSON.parse(readFileSync(arg, "utf8"));
}

// Re-check an agent-action packet: re-run the verifier over its own materials
// and the Emet witness over its canonical bytes.
function verifyAgentAction(input, json) {
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

// Re-check a research or visual packet. Neither lane has an Emet witness stage;
// each verifier recomputes its load-bearing digests and measurements from the
// packet's own embedded materials. Any embedded verdict is checked against the
// freshly derived one, so a canned MATCH over tampered materials fails.
function verifyLane(input, json, verifyFn, schemaLabel) {
  const embedded = input.verifier?.verdict ?? input.verdicts?.overall;
  const verifier = verifyFn(input, { embeddedVerdict: embedded });
  const report = {
    schema: schemaLabel,
    packet_id: input.packet_id,
    verdict: verifier.verdict,
    checks: verifier.checks,
    failures: verifier.failures
  };
  if (verifier.per_metric) {
    report.per_metric = verifier.per_metric;
  }
  if (json) {
    process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
  } else {
    const lines = [`verdict       ${verifier.verdict}`];
    for (const f of verifier.failures) {
      lines.push(`  ${f.code} (${f.verdict}) ${f.path ?? f.name ?? f.ref ?? ""}`.trimEnd());
    }
    process.stdout.write(`${lines.join("\n")}\n`);
  }
  return exitCodeFor(verifier.verdict);
}

function runVerify(args) {
  const json = args.includes("--json");
  const target = args.find((a) => a !== "--json" && a !== "verify");
  if (!target) {
    process.stderr.write("usage: proof verify <packet.json|-> [--json]\n");
    return 2;
  }
  const input = readPacketArg(target);
  // Dispatch by the packet's own schema id so each lane is re-checked by its own
  // verifier. An unknown schema is an error, never a silent pass.
  if (input.schema === RESEARCH_SCHEMA) {
    return verifyLane(input, json, verifyResearchPacket, "project-telos.research-proof-packet-verification/v1");
  }
  if (input.schema === VISUAL_SCHEMA) {
    return verifyLane(input, json, verifyVisualPacket, "project-telos.visual-proof-packet-verification/v1");
  }
  if (input.schema === AGENT_ACTION_SCHEMA || input.schema === undefined) {
    return verifyAgentAction(input, json);
  }
  process.stderr.write(`unknown packet schema for verify: ${input.schema}\n`);
  return 2;
}

function runExport(args) {
  const target = args.find((a) => a !== "--json" && a !== "export");
  if (!target) {
    process.stderr.write("usage: proof export <packet.json|-> [--json]\n");
    return 2;
  }
  const input = readPacketArg(target);
  // Dispatch by schema id: each lane exports to its own proof-surface shape.
  let exported;
  if (input.schema === RESEARCH_SCHEMA) {
    exported = toProofSurfaceResearchPacket(input);
  } else if (input.schema === VISUAL_SCHEMA) {
    exported = toProofSurfaceVisualPacket(input);
  } else if (input.schema === AGENT_ACTION_SCHEMA || input.schema === undefined) {
    exported = toProofSurfacePacket(input);
  } else {
    process.stderr.write(`unknown packet schema for export: ${input.schema}\n`);
    return 2;
  }
  process.stdout.write(`${JSON.stringify(exported, null, 2)}\n`);
  return 0;
}

function main() {
  const [subcommand, ...args] = process.argv.slice(2);
  let code;
  if (subcommand === "agent-action") {
    code = runAgentAction(args);
  } else if (subcommand === "research") {
    code = runResearch(args);
  } else if (subcommand === "visual") {
    code = runVisual(args);
  } else if (subcommand === "verify") {
    code = runVerify(args);
  } else if (subcommand === "export") {
    code = runExport(args);
  } else {
    process.stderr.write(
      "usage: proof <agent-action|research|visual --demo|--fixture <path> | verify <packet.json|-> | export <packet.json|->> [--out <dir>] [--json]\n"
    );
    code = 2;
  }
  process.exit(code);
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main();
}
