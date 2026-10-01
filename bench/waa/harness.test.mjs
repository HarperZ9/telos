// The WindowsAgentArena skeleton: dry run only, zero executed actions, every
// receipt chain verifies, out-of-scope and above-grant probes are refused, and
// --live stops instead of acting on the host.
import test from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { dryRun, loadTasks, main } from "./harness.mjs";
import { benchmarkGrantSpec, DOMAINS, WAA_SOURCE } from "./domains.mjs";
import { mcnemarExact, pairCounts, wilson } from "./stats.mjs";

test("the domain table matches the upstream task counts read on the source date", () => {
  assert.equal(Object.keys(DOMAINS).length, 12);
  assert.equal(Object.values(DOMAINS).reduce((a, d) => a + d.count, 0), WAA_SOURCE.total_tasks);
  assert.ok(Object.values(DOMAINS).every((d) => d.verified === false), "window patterns stay unverified until checked in the guest");
});

test("the benchmark grant stops at T3: no exec, no synthetic input, no hardware", () => {
  for (const domain of Object.keys(DOMAINS)) {
    const spec = benchmarkGrantSpec(domain, { origins: ["https://a.invalid"] });
    assert.equal(spec.tier, "T3");
    assert.ok(!spec.verbs.some((v) => /^(device\.|hardware\.|sense\.)|app\.(input|type)$|browser\.(eval|run)/.test(v)), domain);
  }
  assert.deepEqual(benchmarkGrantSpec("chrome").scope.origins, [], "a browser domain grants no origin until a task names one");
  assert.equal(benchmarkGrantSpec("not_a_domain"), null);
});

test("a dry run executes nothing, verifies every chain and refuses the out-of-scope probes", async () => {
  const r = await dryRun();
  assert.equal(r.mode, "DRY_RUN");
  assert.equal(r.executed_actions, 0);
  assert.equal(r.chains_verified, true);
  assert.equal(r.episodes_planned, 154 * 3 * 3 + 30 * 3, "1,386 Windows episodes plus 90 for the browser subset");
  for (const d of r.domains) {
    const byVerb = d.calls.map((c) => `${c.verb}:${c.status}:${c.reason ?? ""}`);
    if (d.surface === "browser") {
      assert.ok(byVerb.includes("browser.navigate:REFUSED:OUT_OF_SCOPE"), d.domain);
      assert.ok(byVerb.includes("browser.eval:REFUSED:NO_GRANT"), d.domain);
    } else {
      assert.ok(byVerb.includes("app.invoke:REFUSED:PROTECTED_TARGET"), `${d.domain}: a terminal is never a T3 target`);
      assert.ok(byVerb.includes("device.exec:REFUSED:NO_GRANT"), d.domain);
    }
    assert.ok(d.approver.every((a) => a.decision === "approve"), "only in-scope would-hold calls reach the approver");
  }
});

test("task files: unknown domains are reported, upstream counts are checked", () => {
  const dir = mkdtempSync(path.join(os.tmpdir(), "telos-waa-"));
  const f = path.join(dir, "t.json");
  writeFileSync(f, JSON.stringify({ notepad: ["a"], made_up: ["b"] }));
  const t = loadTasks(f);
  assert.deepEqual(t.unknown, ["made_up"]);
  assert.equal(t.matches_upstream_counts, false);
  assert.equal(t.synthetic, false);
});

test("--live is refused", async () => {
  const write = process.stdout.write;
  let out = "";
  process.stdout.write = (s) => { out += s; return true; };
  try {
    assert.equal(await main(["--live"]), 2);
  } finally {
    process.stdout.write = write;
  }
  assert.equal(JSON.parse(out).status, "LIVE_REFUSED");
});

test("Wilson interval and exact McNemar match hand-computed values", () => {
  const w = wilson(50, 100);
  assert.ok(Math.abs(w.low - 0.4038) < 1e-3 && Math.abs(w.high - 0.5962) < 1e-3);
  const z = wilson(0, 10);
  assert.equal(z.low, 0);
  assert.ok(Math.abs(z.high - 0.2775) < 1e-3);
  assert.ok(Math.abs(mcnemarExact(1, 9).p - 0.021484375) < 1e-9, "2 * P(X <= 1), X ~ Bin(10, 1/2) = 22/1024");
  assert.equal(mcnemarExact(0, 0).p, 1);
  assert.deepEqual(pairCounts({ a: true, b: false, c: true }, { a: false, b: true, c: true, d: true }), { b: 1, c: 1, paired: 3 });
  assert.throws(() => wilson(5, 3), RangeError);
});
