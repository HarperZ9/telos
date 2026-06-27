import { readFileSync } from "node:fs";

const catalog = JSON.parse(
  readFileSync(new URL("./integrations/mcp-tool-catalog.json", import.meta.url), "utf8")
);

process.stdout.write(`${JSON.stringify(catalog, null, 2)}\n`);
