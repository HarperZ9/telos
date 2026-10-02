// run-mutations.mjs: show that every equality check of the v2 measurement contract can fail.
// For the baseline and each mutation in mutations.json: copy demo/ and bench/ to a temporary directory,
// apply the one mutation, run demo/measurement-image.test.mjs and record which tests failed. Surviving
// mutations are reported, never dropped.
// Run: node bench/measurement-v2/run-mutations.mjs   (writes results/mutation.json when TELOS_WRITE_RESULTS=1)
import { cpSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(HERE, "..", "..");
const REG = JSON.parse(readFileSync(join(HERE, "mutations.json"), "utf8"));

function freshCopy() {
  const dir = mkdtempSync(join(tmpdir(), "telos-v2-mut-"));
  for (const t of ["demo", "bench", "package.json"]) cpSync(join(ROOT, t), join(dir, t), { recursive: true });
  return dir;
}

function run(dir) {
  const r = spawnSync(process.execPath, ["--test", "--test-reporter=tap", REG.testFile],
    { cwd: dir, encoding: "utf8", maxBuffer: 1 << 26, env: { ...process.env, TELOS_WRITE_RESULTS: "0" } });
  const failed = new Set(), passed = new Set();
  for (const line of (r.stdout || "").split(/\r?\n/)) {
    const m = line.match(/^(not ok|ok) \d+ - (.*?)(?: # (?:SKIP|TODO).*)?$/);
    if (m) (m[1] === "ok" ? passed : failed).add(m[2].trim());
  }
  return { failed, passed, exit: r.status };
}

const out = { registry: "bench/measurement-v2/mutations.json", baseline: null, mutations: [] };
{
  const dir = freshCopy();
  try {
    const r = run(dir);
    out.baseline = { passed: r.passed.size, failed: [...r.failed], allPassed: r.exit === 0 && r.failed.size === 0 };
  } finally { rmSync(dir, { recursive: true, force: true }); }
}
for (const m of REG.mutations) {
  const dir = freshCopy();
  try {
    const p = join(dir, m.file), src = readFileSync(p, "utf8");
    const n = src.split(m.find).length - 1;
    if (n !== 1) throw new Error(`${m.id}: find text occurs ${n} times in ${m.file}`);
    writeFileSync(p, src.replace(m.find, m.replace));
    const r = run(dir);
    const killed = m.kills.filter((t) => r.failed.has(t)), survived = m.kills.filter((t) => !r.failed.has(t));
    out.mutations.push({ id: m.id, fault: m.fault, killed, survived, otherFailures: [...r.failed].filter((t) => !m.kills.includes(t)) });
    console.log(`${m.id.padEnd(22)} killed ${killed.length}/${m.kills.length}${survived.length ? "  SURVIVED" : ""}`);
  } finally { rmSync(dir, { recursive: true, force: true }); }
}
const killed = new Set(out.mutations.flatMap((m) => m.killed));
out.summary = {
  equalityTests: REG.equalityTests.length,
  killedAtLeastOnce: REG.equalityTests.filter((t) => killed.has(t)).length,
  neverKilled: REG.equalityTests.filter((t) => !killed.has(t)),
  mutations: out.mutations.length,
  withSurvivors: out.mutations.filter((m) => m.survived.length).map((m) => m.id),
};
console.log(JSON.stringify({ baseline: out.baseline.allPassed, ...out.summary }, null, 1));
if (process.env.TELOS_WRITE_RESULTS === "1") writeFileSync(join(HERE, "results", "mutation.json"), JSON.stringify(out, null, 1) + "\n");
process.exitCode = out.baseline.allPassed && out.summary.neverKilled.length === 0 ? 0 : 1;
