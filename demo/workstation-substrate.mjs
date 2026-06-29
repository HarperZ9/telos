import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";

const substrate = JSON.parse(
  readFileSync(new URL("./integrations/workstation-substrate.json", import.meta.url), "utf8")
);

export function summary(value = substrate) {
  const aggregate = value.aggregate;
  const lines = [
    "Telos Workstation Substrate",
    `schema       ${value.schema}`,
    `tool         ${value.tool}`,
    `roots        ${aggregate.mapped_roots}`,
    `repos        ${aggregate.repo_count}`,
    `public       ${aggregate.public_class_repos}`,
    `local        ${aggregate.local_class_repos}`,
    `dirty        ${aggregate.dirty_repos}`,
    `lanes        ${value.lane_families.length}`,
    `verdict      ${aggregate.verdict}`,
    "next         node demo/workstation-substrate.mjs"
  ];
  return `${lines.join("\n")}\n`;
}

function main() {
  if (process.argv.includes("--summary")) {
    process.stdout.write(summary());
  } else {
    process.stdout.write(`${JSON.stringify(substrate, null, 2)}\n`);
  }
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  main();
}
