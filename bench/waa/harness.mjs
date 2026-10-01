#!/usr/bin/env node
// WindowsAgentArena harness skeleton for Telos 0.7.0 (DESIGN section 7).
//
//   node bench/waa/harness.mjs [--tasks <WAA test_all.json>] [--seeds=3] [--out=file]
//
// Dry run only. It reads a task list, plans the episodes for the four arms,
// builds the benchmark grant each domain would need, and drives the real tier
// gate and receipt chain with fake drivers in a throwaway state root: every
// call is a dry run, the executor throws if anything reaches it, and the run
// reports zero executed actions. Nothing touches this machine's windows,
// browser, files or Telos state.
//
// `--live` is refused. A live run executes actions inside a WAA guest VM and
// needs an operator-issued benchmark grant there; this skeleton has no guest
// relay yet, so it stops with LIVE_REFUSED instead of falling back to the host.
import { generateKeyPairSync } from "node:crypto";
import { mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createBroker } from "../../demo/broker/dispatch.mjs";
import { issueGrant, saveGrant } from "../../demo/broker/grants.mjs";
import { stateDirs } from "../../demo/broker/paths.mjs";
import { ChainRecorder } from "../../demo/broker/recorder.mjs";
import { signerFromKeyObject } from "../../demo/receipts/keys.mjs";
import { scriptedApprover } from "./approver.mjs";
import { benchmarkGrantSpec, DOMAINS, WAA_SOURCE } from "./domains.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const TASK_ORIGIN = "https://waa-task.invalid";
const REF = "b:e0000000:page:7";

export const ARMS = Object.freeze([
  { id: "A", actuator: "WAA Navi agent, UIA backend", runner: "not built" },
  { id: "B", actuator: "Telos 0.7.0, refs first, benchmark grant", runner: "dry run only" },
  { id: "C", actuator: "Windows-MCP, same model", runner: "not built" },
  { id: "D", actuator: "Playwright MCP, chrome and msedge subset", runner: "not built" },
]);

export function loadTasks(file = path.join(here, "fixtures", "test_all.synthetic.json")) {
  const raw = JSON.parse(readFileSync(file, "utf8"));
  const counts = Object.fromEntries(Object.entries(raw).map(([d, ids]) => [d, Array.isArray(ids) ? ids.length : 0]));
  const total = Object.values(counts).reduce((a, b) => a + b, 0);
  const unknown = Object.keys(raw).filter((d) => !DOMAINS[d]);
  const upstream = Object.keys(DOMAINS).every((d) => counts[d] === DOMAINS[d].count) && total === WAA_SOURCE.total_tasks;
  return { raw, counts, total, unknown, matches_upstream_counts: upstream, synthetic: path.basename(file).includes("synthetic") };
}

function probes(d, title) {
  if (d.surface === "browser") {
    return [["browser.snapshot-ax", []], ["browser.click-ref", [REF]], ["browser.navigate", [`${TASK_ORIGIN}/next`]],
      ["browser.navigate", ["https://off-scope.invalid/"]], ["browser.eval", ["1"]]];
  }
  return [["app.snapshot-ax", [title]], ["app.invoke", [title, "OK"]], ["app.setvalue", [title, "Name", "x"]],
    ["app.invoke", ["Windows PowerShell", "Run"]], ["device.exec", ["cmd", "/c", "whoami"]]];
}

// One domain: issue the benchmark grant into a throwaway state root, send the
// probe calls through the real broker as dry runs, let the scripted approver
// decide the would-hold calls, and verify the receipt chain.
export async function dryRunDomain(domain) {
  const d = DOMAINS[domain];
  const root = mkdtempSync(path.join(os.tmpdir(), `telos-waa-${domain}-`));
  const dirs = stateDirs(root);
  const { privateKey, publicKey } = generateKeyPairSync("ed25519");
  const spec = benchmarkGrantSpec(domain, { origins: d.surface === "browser" ? [TASK_ORIGIN] : [] });
  // isTTY: true is the in-process seam; this grant lives in the throwaway root.
  saveGrant(dirs.grants, issueGrant(spec, { privateKey, publicKey, isTTY: true }));
  const title = `${d.windows?.[0].title_contains ?? "page"} - waa task`;
  const windows = [{ title, class: "WaaApp", process: d.windows?.[0].process ?? d.process },
    { title: "Windows PowerShell", class: "ConsoleWindowClass", process: "powershell" }];
  const drivers = {
    pageUrl: async () => `${TASK_ORIGIN}/start`,
    listWindows: async () => windows,
    resolveRef: async (ref) => ({ ok: true, surface: "browser", target_ref: ref, target_fingerprint: "f".repeat(64), target: { origin: TASK_ORIGIN } }),
    which: () => null,
  };
  const recorder = new ChainRecorder({ home: root, sessionId: `waa-${domain.replace(/_/g, "-")}`, signer: signerFromKeyObject(privateKey) });
  const executor = async () => { throw new Error("dry run: the executor must never be called"); };
  const broker = createBroker({ dirs, publicKey, executor, recorder, sessionId: recorder.sessionId, drivers });
  const approver = scriptedApprover({ grantSpec: spec, task: domain });
  const calls = [];
  for (const [verb, params] of probes(d, title)) {
    const r = await broker.call({ verb, params, flags: {}, dry_run: true });
    calls.push({ verb, status: r.status, tier: r.tier, would_hold: r.would_hold ?? false, reason: r.reason ?? null });
    if (r.status === "DRY_RUN" && r.would_hold) {
      approver.decide({ verb, tier: r.tier, target: d.surface === "browser" ? { origin: originOf(verb, params) } : { window: windows[0] } });
    }
  }
  recorder.close();
  const v = recorder.chain.verify();
  return { domain, surface: d.surface, tasks_upstream: d.count, grant: { tier: spec.tier, verbs: spec.verbs.length }, calls,
    approver: approver.log, chain: { verdict: v.verdict, receipts: v.count }, executed: calls.filter((c) => c.status === "OK" || c.status === "ERROR").length };
}

function originOf(verb, params) {
  if (verb === "browser.navigate") {
    try { return new URL(params[0]).origin; } catch { return null; }
  }
  return TASK_ORIGIN;
}

export async function dryRun({ tasksFile, seeds = 3 } = {}) {
  const tasks = loadTasks(tasksFile);
  const domains = [];
  for (const domain of Object.keys(DOMAINS)) domains.push(await dryRunDomain(domain));
  const windowsArms = ARMS.filter((a) => a.id !== "D").length;
  const browserTasks = (tasks.counts.chrome ?? 0) + (tasks.counts.msedge ?? 0);
  return {
    schema: "telos.waa-dry-run/v1",
    mode: "DRY_RUN",
    source: WAA_SOURCE,
    tasks: { file_synthetic: tasks.synthetic, counts: tasks.counts, total: tasks.total, unknown_domains: tasks.unknown, matches_upstream_counts: tasks.matches_upstream_counts },
    arms: ARMS,
    episodes_planned: tasks.total * seeds * windowsArms + browserTasks * seeds,
    seeds,
    domains,
    executed_actions: domains.reduce((a, d) => a + d.executed, 0),
    chains_verified: domains.every((d) => d.chain.verdict === "MATCH"),
    does_not_prove: "A dry run shows the plan, the grant each domain needs and that the gate and receipt chain behave on probe calls. It does not show any task can be solved, that the window patterns match the WAA guest image, or any success rate.",
  };
}

function flagValue(argv, name) {
  const eq = argv.find((a) => a.startsWith(`--${name}=`));
  if (eq) return eq.slice(name.length + 3);
  const i = argv.indexOf(`--${name}`);
  return i >= 0 ? argv[i + 1] : undefined;
}

export async function main(argv = process.argv.slice(2)) {
  if (argv.includes("--live")) {
    process.stdout.write(`${JSON.stringify({ status: "LIVE_REFUSED", reason: "live runs execute inside a WAA guest VM under an operator-issued benchmark grant; the guest relay is not built, and this harness never acts on the host" }, null, 2)}\n`);
    return 2;
  }
  const report = await dryRun({ tasksFile: flagValue(argv, "tasks"), seeds: Number(flagValue(argv, "seeds") ?? 3) });
  const text = `${JSON.stringify(report, null, 2)}\n`;
  const out = flagValue(argv, "out");
  if (out) writeFileSync(out, text);
  else process.stdout.write(text);
  return report.executed_actions === 0 && report.chains_verified ? 0 : 1;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main().then((code) => { process.exitCode = code; }, (err) => { process.stderr.write(`waa harness: ${err.stack}\n`); process.exitCode = 1; });
}
