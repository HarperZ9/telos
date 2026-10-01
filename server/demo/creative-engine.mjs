import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";

const manifest = JSON.parse(
  readFileSync(new URL("./integrations/creative-engine-manifest.json", import.meta.url), "utf8")
);

export function summary(value = manifest) {
  const lines = [
    "Telos Creative Engine",
    `schema     ${value.schema}`,
    `tool       ${value.tool}`,
    `domains    ${value.domains.length}`,
    `techniques ${value.techniques.length}`,
    `revival    ${value.revival_candidates.length}`,
    `surfaces   ${value.contract.io_surfaces.join(", ")}`,
    "next       node demo/creative-engine.mjs"
  ];
  return `${lines.join("\n")}\n`;
}

function main() {
  if (process.argv.includes("--summary")) {
    process.stdout.write(summary());
  } else {
    process.stdout.write(`${JSON.stringify(manifest, null, 2)}\n`);
  }
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  main();
}