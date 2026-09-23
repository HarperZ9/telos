// The version has to say the same thing everywhere a caller can read it.
//
// Before version.mjs it was typed out in eight places. Exactly one of them was
// guarded: telos-mcp.test.mjs reads package.json and asserts serverInfo.version
// against it. The four action-envelope sites had no check at all, so a release
// could bump package.json and leave every receipt reporting the previous
// version with the whole suite still green. The server-manifest freshness
// expectation for Telos itself was a ninth literal in a JSON fixture, which is
// the one place a constant cannot reach, so it is asserted here instead.
//
// The name is here for the same reason. It read "project-telos-telos" from June
// 2026 until the first npm publish, and only one assertion ever referred to it.
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));

import { handleRequest } from "./telos-mcp.mjs";
import { TELOS_PACKAGE, TELOS_SERVER_NAME, TELOS_VERSION } from "./version.mjs";

const manifest = JSON.parse(
  readFileSync(new URL("../package.json", import.meta.url), "utf8")
);

// Guards the guard. If version.mjs ever resolved to undefined, every equality
// below would compare undefined to undefined and pass while proving nothing.
assert.match(TELOS_VERSION, /^\d+\.\d+\.\d+$/);
assert.equal(TELOS_VERSION, manifest.version);
assert.equal(TELOS_PACKAGE, manifest.name);

// What a client is told on connect.
const init = handleRequest({
  jsonrpc: "2.0",
  id: 1,
  method: "initialize",
  params: {}
});
assert.equal(init.result.serverInfo.version, manifest.version);
assert.equal(init.result.serverInfo.name, TELOS_SERVER_NAME);
assert.equal(TELOS_SERVER_NAME, "telos");

// Every sibling lane reports its short name, so a doubled or prefixed name is
// the failure to catch here.
assert.ok(
  !TELOS_SERVER_NAME.includes("telos-telos"),
  "the server name doubled its own word again"
);

// The action envelopes. These are the sites that had no guard.
//
// They run as subprocesses because status.mjs, doctor.mjs and room.mjs export
// nothing: each builds a payload and console.logs it. An earlier draft of this
// file imported them and read `mod.default ?? mod.payload`, which is undefined,
// so the check skipped every envelope and passed while asserting nothing. That
// is the failure this file exists to catch, so it is worth naming here.
for (const [label, argv] of [
  ["status", ["status.mjs"]],
  ["doctor", ["doctor.mjs"]],
  ["room", ["room.mjs", "--json"]]
]) {
  const run = spawnSync(
    process.execPath,
    [path.join(here, argv[0]), ...argv.slice(1)],
    { encoding: "utf8", cwd: path.resolve(here, "..") }
  );
  assert.equal(run.status, 0, `${label} exited ${run.status}: ${run.stderr?.slice(0, 200)}`);
  const payload = JSON.parse(run.stdout);
  assert.equal(
    payload.tool_version,
    manifest.version,
    `${label} envelope reports ${payload.tool_version}, package.json says ${manifest.version}`
  );
}

// The freshness expectation Telos holds for itself. A stale one makes
// telos.mcp.freshness report DRIFT against the very server producing it.
const serverManifest = JSON.parse(
  readFileSync(
    new URL("./integrations/mcp-server-manifest.json", import.meta.url),
    "utf8"
  )
);
assert.equal(
  serverManifest.servers.telos.freshness.expected_version,
  manifest.version,
  "the server manifest expects a different Telos version than package.json declares"
);

// The README version badge. It is a literal in prose, so nothing else can hold
// it in step, and a badge that lies about the release is the first thing a
// reader sees.
const readme = readFileSync(new URL("../README.md", import.meta.url), "utf8");
const badge = readme.match(/badge\/version-(\d+\.\d+\.\d+)-/);
assert.ok(badge, "README no longer carries a version badge in the expected shape");
assert.equal(
  badge[1],
  manifest.version,
  `README badge says ${badge[1]}, package.json says ${manifest.version}`
);

// Every server's status line should name the version it claims to describe.
// This caught gather, index and forum sitting three releases behind.
for (const [name, server] of Object.entries(serverManifest.servers)) {
  const { expected_version: version, expected_current_status: status } =
    server.freshness;
  assert.match(version, /^\d+\.\d+\.\d+$/, `${name} expected_version is not a release number`);
  assert.ok(
    status.startsWith(version),
    `${name} status line starts "${status.slice(0, 24)}" but expects ${version}`
  );
}
