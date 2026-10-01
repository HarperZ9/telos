import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";

const contract = JSON.parse(
  readFileSync(new URL("./integrations/display-calibration.json", import.meta.url), "utf8")
);

export function summary(value = contract) {
  const hardware = value.contract.hardware_mutation_allowed ? "mutable" : "read-only";
  const lines = [
    "Telos Display Calibration",
    `schema    ${value.schema}`,
    `tool      ${value.tool}`,
    `hardware  ${hardware}`,
    `targets   ${value.display_targets.length}`,
    `patches   ${value.patch_sets.length}`,
    `artifacts ${value.artifact_types.length}`,
    `sources   ${value.sources.map((source) => source.id).join(", ")}`,
    "next      node demo/display-calibration.mjs"
  ];
  return `${lines.join("\n")}\n`;
}

function main() {
  if (process.argv.includes("--summary")) {
    process.stdout.write(summary());
  } else {
    process.stdout.write(`${JSON.stringify(contract, null, 2)}\n`);
  }
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  main();
}
