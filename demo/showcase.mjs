import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { buildReadinessPacket } from "./showcase/record.mjs";
import { scoutFixture, scoutLive, renderScoutTable } from "./showcase/scout.mjs";

function has(flag) {
  return process.argv.includes(flag);
}

function valueAfter(flag, fallback = undefined) {
  const index = process.argv.indexOf(flag);
  return index === -1 ? fallback : process.argv[index + 1];
}

function writeOutput(payload) {
  const out = valueAfter("--out");
  if (!out) {
    return;
  }
  mkdirSync(out, { recursive: true });
  writeFileSync(path.join(out, "scout.json"), `${JSON.stringify(payload, null, 2)}\n`);
}

function main() {
  const command = process.argv[2];
  if (!["scout", "record"].includes(command)) {
    process.stderr.write("usage: node demo/showcase.mjs scout|record [--json]\n");
    return 2;
  }

  const now = new Date(valueAfter("--now", new Date().toISOString()));

  if (command === "record") {
    const candidatePath = valueAfter("--candidate");
    const evidencePath = valueAfter("--evidence");
    if (!candidatePath || !evidencePath) {
      process.stderr.write("record requires --candidate FILE --evidence FILE\n");
      return 2;
    }
    const packet = buildReadinessPacket({
      candidate: JSON.parse(readFileSync(candidatePath, "utf8")),
      evidence: JSON.parse(readFileSync(evidencePath, "utf8")),
      now
    });
    if (has("--json")) {
      process.stdout.write(`${JSON.stringify(packet, null, 2)}\n`);
    } else {
      process.stdout.write(`${packet.pr_ready ? "PR-ready" : "Not PR-ready"}: ${packet.operator_next_action}\n`);
    }
    return 0;
  }

  const payload = has("--fixture")
    ? scoutFixture({ now })
    : scoutLive({ query: valueAfter("--query"), limit: Number(valueAfter("--limit", "5")), now });
  writeOutput(payload);
  if (has("--json")) {
    process.stdout.write(`${JSON.stringify(payload, null, 2)}\n`);
  } else {
    process.stdout.write(renderScoutTable(payload));
  }
  return 0;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  process.exitCode = main();
}