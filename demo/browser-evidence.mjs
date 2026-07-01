import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";
import { validateBrowserEvidencePacket } from "./native-control/evidence.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const fixturePath = path.join(here, "integrations", "browser-evidence.json");

export function fixturePacket() {
  return JSON.parse(readFileSync(fixturePath, "utf8"));
}

export function summary(packet) {
  const validation = validateBrowserEvidencePacket(packet);
  return [
    "Telos Browser Evidence",
    `schema   ${packet.schema}`,
    `mode     ${packet.mode}`,
    `verdict  ${packet.verification?.verdict ?? "UNVERIFIABLE"}`,
    `valid    ${validation.ok ? "MATCH" : "DRIFT"}`,
    "next     node demo/browser-evidence.mjs --fixture",
  ].join("\n") + "\n";
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  const packet = fixturePacket();
  if (process.argv.includes("--summary")) {
    process.stdout.write(summary(packet));
  } else {
    process.stdout.write(`${JSON.stringify(packet, null, 2)}\n`);
  }
}
