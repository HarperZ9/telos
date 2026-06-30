import { readFileSync } from "node:fs";

const packet = JSON.parse(
  readFileSync(new URL("./integrations/learning-forge-labs.json", import.meta.url), "utf8")
);

function labIdFromArgs(args) {
  const inline = args.find((arg) => arg.startsWith("--lab="));
  if (inline) {
    return inline.slice("--lab=".length);
  }
  const index = args.indexOf("--lab");
  return index === -1 ? null : args[index + 1] ?? null;
}

function summary() {
  const lines = [
    "Project Telos Learning Forge Labs",
    `labs     ${packet.labs.length}`,
    `verdict  ${packet.validation.verdict}`,
    `source   ${packet.source_receipts.operator_packet.sha256.slice(0, 12)}`,
    "next     node demo/learning-forge-labs.mjs --lab tiny-autoregressive-predictor"
  ];
  return `${lines.join("\n")}\n`;
}

const args = process.argv.slice(2);
const labId = labIdFromArgs(args);

if (args.includes("--summary")) {
  process.stdout.write(summary());
} else if (labId) {
  const lab = packet.labs.find((entry) => entry.id === labId);
  if (!lab) {
    process.stderr.write(`unknown learning forge lab: ${labId}\n`);
    process.exit(2);
  }
  process.stdout.write(`${JSON.stringify(lab, null, 2)}\n`);
} else {
  process.stdout.write(`${JSON.stringify(packet, null, 2)}\n`);
}
