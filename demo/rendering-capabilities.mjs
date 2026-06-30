import { readFileSync } from "node:fs";

const capabilities = JSON.parse(
  readFileSync(new URL("./integrations/rendering-capabilities.json", import.meta.url), "utf8")
);

function summary(value = capabilities) {
  const lines = [
    "Telos Rendering Capabilities",
    `schema     ${value.schema}`,
    `tool       ${value.tool}`,
    `profiles   ${value.renderer_profiles.length}`,
    `order      ${value.selection_order.join(" -> ")}`,
    `failures   ${value.failure_codes.length}`,
    "next       node demo/rendering-capabilities.mjs"
  ];
  return `${lines.join("\n")}\n`;
}

if (process.argv.includes("--summary")) {
  process.stdout.write(summary());
} else {
  process.stdout.write(`${JSON.stringify(capabilities, null, 2)}\n`);
}
