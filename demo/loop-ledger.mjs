import { readFileSync } from "node:fs";

const convention = JSON.parse(
  readFileSync(new URL("./integrations/loop-ledger-conventions.json", import.meta.url), "utf8")
);

process.stdout.write(`${JSON.stringify(convention, null, 2)}\n`);
