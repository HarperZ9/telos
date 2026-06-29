import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";

const queue = JSON.parse(
  readFileSync(new URL("./integrations/second-level-flagship-queue.json", import.meta.url), "utf8")
);

function countsBy(items, field) {
  const counts = new Map();
  for (const item of items) {
    const key = item[field] ?? "unknown";
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  return [...counts.entries()].map(([key, count]) => `${key}=${count}`).join(", ");
}

export function summary(value = queue) {
  const lines = [
    "Telos Second-Level Flagship Queue",
    `schema          ${value.schema}`,
    `tool            ${value.tool}`,
    `public          ${value.public_candidates.length}`,
    `private_tranche ${value.private_local_tranches.length}`,
    `lanes           ${countsBy(value.public_candidates, "lane")}`,
    `hosts           ${[...new Set(value.public_candidates.flatMap((candidate) => candidate.host_flagships))].length}`,
    "next            node demo/second-level-flagship-queue.mjs"
  ];
  return `${lines.join("\n")}\n`;
}

function main() {
  if (process.argv.includes("--summary")) {
    process.stdout.write(summary());
  } else {
    process.stdout.write(`${JSON.stringify(queue, null, 2)}\n`);
  }
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  main();
}
