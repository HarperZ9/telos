#!/usr/bin/env node
// Drive the stdio MCP server out of an installed copy of this package.
//
// The release workflow runs this after installing the packed tarball into a
// clean project. A package can pack cleanly, install cleanly, and still fail at
// launch because a file the server imports was left out of the `files`
// allowlist in package.json. Nothing else in the release pipeline would see
// that: `npm pack` is happy, `npm install` is happy, and the failure arrives
// when a host first starts the server.
//
// It lives here rather than in a heredoc inside release.yml for two reasons. A
// forty-line script embedded in YAML is hard to read and harder to run by hand,
// and tools/test_release_artifacts.py asserts that ci.yml and release.yml run
// the same `node ...` contract commands, which an extra inline `node - <<EOF`
// would break for a publish-only step.
//
// Usage: node tools/probe-installed-mcp.mjs <install-dir>
// Exits non-zero with the reason on any failure.
import { spawnSync } from "node:child_process";
import { createRequire } from "node:module";
import path from "node:path";
import process from "node:process";

const PACKAGE = "project-telos-mcp";

function fail(message) {
  console.error(`probe failed: ${message}`);
  process.exit(1);
}

const installDir = path.resolve(process.argv[2] ?? process.cwd());
const require = createRequire(path.join(installDir, "noop.cjs"));

let declared;
let entry;
try {
  declared = require(`${PACKAGE}/package.json`).version;
  entry = require.resolve(`${PACKAGE}/demo/telos-mcp.mjs`);
} catch (error) {
  fail(`${PACKAGE} is not installed under ${installDir}: ${error.message}`);
}

const request = (id, method, params = {}) =>
  JSON.stringify({ jsonrpc: "2.0", id, method, params });

const input = [
  request(1, "initialize", {
    protocolVersion: "2024-11-05",
    capabilities: {},
    clientInfo: { name: "release-gate", version: "1" }
  }),
  request(2, "tools/list"),
  request(3, "tools/call", { name: "telos.status", arguments: {} })
].join("\n") + "\n";

const run = spawnSync(process.execPath, [entry], {
  input,
  encoding: "utf8",
  timeout: 240000,
  cwd: installDir
});

const lines = (run.stdout ?? "")
  .split("\n")
  .filter((line) => line.trim().startsWith("{"));

if (lines.length === 0) {
  fail(
    `the server produced no JSON on stdout. exit=${run.status} `
    + `stderr=${(run.stderr ?? "").slice(0, 1500)}`
  );
}

let info = null;
let tools = null;
let status = null;
for (const line of lines) {
  const result = JSON.parse(line).result ?? {};
  if (result.serverInfo) info = result.serverInfo;
  if (result.tools) tools = result.tools;
  if (result.structuredContent) status = result.structuredContent;
}

if (!info) fail("initialize returned no serverInfo");
if (!tools || tools.length === 0) fail("tools/list returned no tools");
if (info.version !== declared) {
  fail(`serverInfo reports ${info.version}, the installed package.json says ${declared}`);
}
if (status && status.tool_version !== declared) {
  fail(`telos.status reports ${status.tool_version}, the installed package.json says ${declared}`);
}

console.log(
  `installed MCP ok: ${info.name} ${info.version}, ${tools.length} tools`
  + (status ? `, telos.status ${status.status}` : "")
);
