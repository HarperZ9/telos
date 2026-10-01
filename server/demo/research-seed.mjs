import { readFileSync } from "node:fs";

const packet = JSON.parse(
  readFileSync(new URL("./research/fundamental-physics-seeds.json", import.meta.url), "utf8")
);

process.stdout.write(`${JSON.stringify(packet, null, 2)}\n`);
