import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "..");

function readDoc(relativePath) {
  return readFileSync(path.join(root, relativePath), "utf8");
}

const currentState = readDoc("docs/CURRENT-STATE.md");
const revival = readDoc("docs/QUALITY-TOOL-REVIVAL.md");

for (const term of [
  "Gather",
  "Index",
  "Forum",
  "Crucible",
  "Telos",
  "five flagship",
  "moving target",
  "Index and Forum",
  "MATCH",
  "DRIFT",
  "UNVERIFIABLE",
  "MCP",
  "CLI",
  "IDE",
  "TUI",
  "application",
  "studio-engine",
  "reconcile",
  "telos.context.pack",
  "telos.research.thermodynamic",
  "Thermodynamic AI Chip"
]) {
  assert.match(currentState, new RegExp(term.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "i"));
}

for (const term of [
  "quality-tool boundary",
  "calibrate-pro",
  "quanta-color",
  "quantalang",
  "warden-security-lineage",
  "agent-audit",
  "context-curator-lite",
  "secret-redact-io",
  "repo-proof-index",
  "release-surface-scanner",
  "gpu-trace-validator",
  "studio-engine",
  "reconcile",
  "promotion-ready",
  "quarantine-and-adapt",
  "defensive",
  "creative",
  "machine learning",
  "science"
]) {
  assert.match(revival, new RegExp(term.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "i"));
}

assert.match(currentState, /2026-06-28T17:29:42-07:00/);
assert.match(currentState, /repo_count[^0-9]+52/i);
assert.match(currentState, /root_sha256_prefix[^a-f0-9]+92ef331e0850ccf6/i);
assert.match(currentState, /Telos repo[^.\n]+469ce55/i);
assert.match(currentState, /49 available tools/i);
