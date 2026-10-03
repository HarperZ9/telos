// run-mutations.mjs: show that each reach behaviour test fails when the code it
// guards is broken. For each entry in mutations.json: copy demo/ and
// package.json to a temporary directory, apply the one mutation, run the named
// test file, and expect a failure. Survivors are reported and exit non-zero.
// Run: node bench/reach/run-mutations.mjs
import { cpSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(HERE, "..", "..");
const { mutations } = JSON.parse(readFileSync(join(HERE, "mutations.json"), "utf8"));

function freshCopy() {
  const dir = mkdtempSync(join(tmpdir(), "telos-reach-mut-"));
  for (const item of ["demo", "package.json"]) cpSync(join(ROOT, item), join(dir, item), { recursive: true });
  return dir;
}

const runTest = (dir, file) => spawnSync(process.execPath, ["--test", file], { cwd: dir, encoding: "utf8" }).status;

const results = [];
for (const m of mutations) {
  const dir = freshCopy();
  try {
    const target = join(dir, m.file);
    const source = readFileSync(target, "utf8");
    if (!source.includes(m.find)) throw new Error(`mutation anchor not found in ${m.file}: ${m.find}`);
    const baseline = runTest(dir, m.test);
    writeFileSync(target, source.replace(m.find, m.replace));
    const mutated = runTest(dir, m.test);
    results.push({ file: m.file, find: m.find, baseline_passed: baseline === 0, killed: mutated !== 0 });
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
}
const survivors = results.filter((r) => !r.killed || !r.baseline_passed);
for (const r of results) console.log(`${r.killed ? "killed  " : "SURVIVED"} ${r.file} :: ${r.find.slice(0, 60)}`);
console.log(`${results.length - survivors.length}/${results.length} mutations killed with a passing baseline`);
process.exitCode = survivors.length ? 1 : 0;
