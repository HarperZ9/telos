import { readFileSync } from "node:fs";

const convention = JSON.parse(
  readFileSync(new URL("./integrations/context-envelope-conventions.json", import.meta.url), "utf8")
);

process.stdout.write(`${JSON.stringify(convention, null, 2)}\n`);
