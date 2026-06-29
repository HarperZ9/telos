import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";

const doctor = JSON.parse(
  readFileSync(new URL("./integrations/ci-doctor.json", import.meta.url), "utf8")
);

export function summary(value = doctor) {
  const aggregate = value.aggregate;
  const lines = [
    "Telos CI Doctor",
    `schema       ${value.schema}`,
    `tool         ${value.tool}`,
    `flagships    ${aggregate.flagship_count}`,
    `workflows    ${aggregate.workflow_count}`,
    `latest CI    ${aggregate.latest_ci_failures === 0 ? "MATCH" : "DRIFT"}`,
    `node24       ${aggregate.node24_compatibility}`,
    `verdict      ${aggregate.verdict}`,
    "next         node demo/ci-doctor.mjs"
  ];
  return `${lines.join("\n")}\n`;
}

function main() {
  if (process.argv.includes("--summary")) {
    process.stdout.write(summary());
  } else {
    process.stdout.write(`${JSON.stringify(doctor, null, 2)}\n`);
  }
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  main();
}
