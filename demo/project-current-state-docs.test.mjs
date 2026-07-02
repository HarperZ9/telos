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
const connectionMap = readDoc("docs/PROJECT-CONNECTION-MAP.md");
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
  "telos.model.foundry",
  "telos.mcp.freshness",
  "telos.ci.doctor",
  "telos.ci.triage",
  "telos.presentation.doctor",
  "telos.accessibility.doctor",
  "telos.performance.doctor",
  "telos.compatibility.doctor",
  "telos.operator.doctor",
  "telos.research.thermodynamic",
  "Thermodynamic AI Chip",
  "second-level flagship queue",
  "second-level-flagship-queue",
  "workstation substrate register",
  "telos.workstation.substrate"
]) {
  assert.match(currentState, new RegExp(term.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "i"));
}

for (const term of [
  "Project Telos Connection Map",
  "HarperZ9 repository",
  "constellation",
  "public non-forks",
  "private active repos",
  "raw-native",
  "studio-libs",
  "forum-archive",
  "seed bank",
  "Gather senses",
  "Index remembers",
  "Forum routes",
  "Crucible verifies",
  "action_intent_id",
  "action_receipt",
  "context_envelope",
  "verdict_certificate",
  "MCP gives the port",
  "OpenTelemetry gives the spans",
  "Telos gives the durable receipt",
  "Hyphal Context Protocol",
  "promotion record",
  "Lane Record Shape",
  "UNVERIFIABLE"
]) {
  assert.match(connectionMap, new RegExp(term.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "i"));
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
  "raw-native",
  "studio-libs",
  "forum-archive",
  "studio-engine",
  "reconcile",
  "promotion-ready",
  "quarantine-and-adapt",
  "defensive",
  "creative",
  "machine learning",
  "science",
  "Second-Level Flagship Queue",
  "workstation substrate register",
  "reconcile",
  "model-provenance-validator"
]) {
  assert.match(revival, new RegExp(term.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "i"));
}

assert.match(currentState, /2026-06-28T17:29:42-07:00/);
assert.match(currentState, /repo_count[^0-9]+52/i);
assert.match(currentState, /root_sha256_prefix[^a-f0-9]+92ef331e0850ccf6/i);
assert.match(currentState, /Telos repo[^.\n]+2894b72/i);
assert.match(currentState, /70 available tools/i);
assert.match(currentState, /telos\.learning\.forge/i);
assert.match(currentState, /telos\.learning\.labs/i);
assert.match(currentState, /CI doctor/i);
assert.match(currentState, /CI triage/i);
assert.match(currentState, /--gh-run owner\/repo#run_id/i);
assert.match(currentState, /presentation doctor/i);
assert.match(currentState, /accessibility doctor/i);
assert.match(currentState, /performance doctor/i);
assert.match(currentState, /compatibility doctor/i);
assert.match(currentState, /operator doctor/i);
assert.match(currentState, /five latest flagship CI runs/i);
assert.match(currentState, /Node 24/i);
assert.match(currentState, /PROJECT-CONNECTION-MAP\.md/i);
assert.match(currentState, /77 visible HarperZ9 repos/i);
assert.match(currentState, /raw-native/i);
assert.match(currentState, /15 public-safe candidates/i);
assert.match(currentState, /331 repositories/i);
assert.match(currentState, /163 public-class repos/i);
assert.match(currentState, /168 local-class repos/i);
assert.match(currentState, /8 public-safe lane families/i);
