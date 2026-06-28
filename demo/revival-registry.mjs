import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";

const registry = JSON.parse(
  readFileSync(new URL("./integrations/revival-registry.json", import.meta.url), "utf8")
);

function countsBy(items, field) {
  const counts = new Map();
  for (const item of items) {
    counts.set(item[field], (counts.get(item[field]) ?? 0) + 1);
  }
  return [...counts.entries()].map(([key, count]) => `${key}=${count}`).join(", ");
}

export function summary(value = registry) {
  const lines = [
    "Telos Revival Registry",
    `schema    ${value.schema}`,
    `tool      ${value.tool}`,
    `tools     ${value.tools.length}`,
    `lanes     ${countsBy(value.tools, "promotion_lane")}`,
    `status    ${countsBy(value.tools, "status")}`,
    `surface   ${value.contract.io_surfaces.join(", ")}`,
    "next      node demo/revival-registry.mjs"
  ];
  return `${lines.join("\n")}\n`;
}

function main() {
  if (process.argv.includes("--summary")) {
    process.stdout.write(summary());
  } else {
    process.stdout.write(`${JSON.stringify(registry, null, 2)}\n`);
  }
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  main();
}
