import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { evaluateObservedServer } from "./mcp-freshness.mjs";
import { createCompatibilityFixture } from "./compat-fixture.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const workspace = path.resolve(here, "../..");
const manifest = JSON.parse(readFileSync(path.join(here, "integrations/mcp-server-manifest.json")));
const server = manifest.servers.index;
const probe = server.freshness.behavior_probes[0];
assert.equal(probe.arguments.root, "${PROJECT_TELOS_COMPAT_FIXTURE}");
assert.equal(probe.arguments.bounded_output, true);
const temporary = mkdtempSync(path.join(tmpdir(), "telos-compat-"));
const fixture = path.join(temporary, "workspace");
const repo = path.join(fixture, "index");
assert.equal(createCompatibilityFixture(fixture).PROJECT_TELOS_COMPAT_FIXTURE,
  fixture.replaceAll("\\", "/"));
assert.throws(() => createCompatibilityFixture(fixture), { code: "EEXIST" });
const expand = (value) => value.replaceAll("${PROJECT_TELOS_PUBLIC}", workspace.replaceAll("\\", "/"))
  .replaceAll("${PROJECT_TELOS_COMPAT_FIXTURE}", fixture.replaceAll("\\", "/"))
  .replaceAll("${PROJECT_TELOS_PRIVATE_LINE}", fixture.replaceAll("\\", "/"));
const profile = server.profiles.source_checkout;
const env = Object.fromEntries(Object.entries(process.env).filter(([key]) =>
  ["PATH", "SYSTEMROOT", "WINDIR", "COMSPEC", "PATHEXT"].includes(key.toUpperCase())));
Object.assign(env, { HOME: temporary, USERPROFILE: temporary, TEMP: temporary, TMP: temporary });
for (const [key, value] of Object.entries(profile.env ?? {})) env[key] = expand(value);

function call(requests) {
  const result = spawnSync(profile.command, profile.args.map(expand), {
    cwd: expand(profile.cwd), env, encoding: "utf8", timeout: 30000, maxBuffer: 4 * 1024 * 1024,
    input: requests.map((request) => `${JSON.stringify(request)}\n`).join("")
  });
  assert.equal(result.status, 0, result.stderr);
  return result.stdout.trim().split(/\r?\n/).map((line) => JSON.parse(line));
}
const request = (id, name, args) => ({ jsonrpc: "2.0", id, method: "tools/call",
  params: { name, arguments: args } });
const unpack = (message) => {
  assert.notEqual(message.result.isError, true);
  return JSON.parse(message.result.content[0].text);
};
try {
  const requests = [{ jsonrpc: "2.0", id: 1, method: "initialize", params: {} },
    { jsonrpc: "2.0", id: 2, method: "tools/list" }, request(3, "index.status", {})];
  for (const [i, item] of server.freshness.behavior_probes.entries())
    requests.push(request(i + 4, item.tool, JSON.parse(expand(JSON.stringify(item.arguments)))));
  const responses = call(requests);
  const observed = { initialize: responses[0], tools_list: responses[1],
    status_payload: unpack(responses[2]), behavior_probes: {} };
  server.freshness.behavior_probes.forEach((item, i) => {
    observed.behavior_probes[item.id] = unpack(responses[i + 3]);
  });
  const envelope = observed.behavior_probes[probe.id];
  assert.deepEqual(envelope.failure_codes, []);
  assert.deepEqual(envelope.omitted, []);
  assert.equal(evaluateObservedServer("index", observed).verdict, "MATCH");
  assert.ok(Math.ceil(Buffer.byteLength(JSON.stringify(responses[3])) / 4) <= probe.arguments.budget);

  // A real large-workspace budget failure must never satisfy the positive probe.
  const large = unpack(call([request(1, probe.tool,
    { root: workspace, budget: 700, focus: "index", hops: 0 })])[0]);
  assert.equal(large.verification_verdict, "UNVERIFIABLE");
  assert.ok(large.failure_codes.includes("budget_overflow"));
  const overflowing = structuredClone(observed);
  overflowing.behavior_probes[probe.id] = large;
  assert.equal(evaluateObservedServer("index", overflowing).verdict, "DRIFT");

  // Re-derive freshness against the changed source, rather than trusting a receipt.
  const saved = path.join(temporary, "envelope.json");
  writeFileSync(saved, JSON.stringify(envelope));
  const recheck = () => {
    const verify = spawnSync(profile.command, ["-c", [
    "import json,sys; from pathlib import Path",
    "from index_graph.graph.build import build_graph",
    "from index_graph.context.envelope import verify_envelope_freshness",
    "print(json.dumps(verify_envelope_freshness(json.loads(Path(sys.argv[1]).read_text()),build_graph({'index':Path(sys.argv[2])}))))"
  ].join(";"), saved, repo], { cwd: expand(profile.cwd), env, encoding: "utf8", timeout: 10000 });
    assert.equal(verify.status, 0, verify.stderr);
    return JSON.parse(verify.stdout);
  };
  assert.equal(recheck().verdict, "MATCH");
  writeFileSync(path.join(repo, "sample.py"), "VALUE = 2\n");
  const stale = recheck();
  assert.equal(stale.verdict, "DRIFT");
  assert.deepEqual(stale.drifted_repos, ["index"]);
  console.log(JSON.stringify({ fixture: "one synthetic index repo", budget: probe.arguments.budget,
    responseApproxTokens: Math.ceil(Buffer.byteLength(JSON.stringify(responses[3])) / 4),
    positive: "MATCH", unchangedSource: "MATCH", changedSource: stale.verdict,
    realWorkspace700: large.verification_verdict, realWorkspace700Accepted: false }));
} finally {
  assert.equal(path.dirname(path.resolve(temporary)), path.resolve(tmpdir()));
  assert.ok(path.basename(temporary).startsWith("telos-compat-"));
  rmSync(temporary, { recursive: true, force: true });
}
