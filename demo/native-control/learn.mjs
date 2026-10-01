// learn integration: the accountable learning engine (tutor / spaced repetition /
// mastery gate) as a first-class witnessed action of the automation runner. A
// workflow can study an objective, record an attempt, and check mastery -- each
// step chained into the ledger, so a study + certification-prep run is itself a
// witnessed artifact. learn stays its own public flagship; this is the bridge.
//
// Shells to the learn CLI. Resolution order: LEARN_CLI (a path to learn's
// src/cli.mjs), then the `learn` bin of an installed @harperz9/learn package
// found through PATH. There is no default path: when neither resolves, every
// action answers UNAVAILABLE with the install command. learn uses exit code as
// a SIGNAL (e.g. mastery "not yet" exits non-zero), so run() returns the
// verdict text on stdout regardless of exit code.

import { spawnSync } from "node:child_process";
import { existsSync } from "node:fs";
import path from "node:path";

export const LEARN_INSTALL = "npm install -g @harperz9/learn";

// Global npm installs put the package beside the PATH shim on Windows
// (<prefix>/node_modules) and under <prefix>/lib/node_modules elsewhere.
export function resolveLearnCli(env = process.env, exists = existsSync) {
  if (env.LEARN_CLI && env.LEARN_CLI.trim()) return { cli: env.LEARN_CLI.trim(), source: "LEARN_CLI" };
  const rel = path.join("node_modules", "@harperz9", "learn", "src", "cli.mjs");
  const dirs = String(env.PATH || env.Path || "").split(path.delimiter).filter(Boolean);
  for (const dir of dirs) {
    for (const candidate of [path.join(dir, rel), path.join(dir, "..", "lib", rel)]) {
      if (exists(candidate)) return { cli: candidate, source: "PATH" };
    }
  }
  return { cli: null, source: null };
}

export function run(args, { timeoutMs = 45000, env = process.env } = {}) {
  const { cli } = resolveLearnCli(env);
  if (!cli) {
    return { ok: false, status: "UNAVAILABLE", out: "", err: `learn is not installed; run: ${LEARN_INSTALL}`, exit: null };
  }
  const r = spawnSync(process.execPath, [cli, ...args.map(String)], {
    encoding: "utf-8", timeout: timeoutMs, windowsHide: true, maxBuffer: 1 << 20,
  });
  const out = String(r.stdout || "").trim();
  const err = String(r.stderr || "").trim();
  return { ok: out.length > 0, out, err: err.slice(0, 400), exit: r.status };
}

const nowIso = (s) => s.now || new Date().toISOString();

// Map runner step -> learn CLI argv. step fields: session, topic, objectives,
// objective, prompt, answer, correct, grade, now, useFsrs, desiredRetention.
export const actions = {
  plan: (s) => run(["tutor", "plan", s.session, "--topic", s.topic || "", "--objectives", s.objectives || ""].concat(s.enableFsrs ? ["--enableFsrs"] : [])),
  record: (s) => run(["tutor", "record", s.session, "--objective", s.objective, "--prompt", s.prompt || "", "--answer", s.answer || "", "--correct", String(!!s.correct), "--now", nowIso(s)].concat(s.grade != null ? ["--grade", String(s.grade)] : [])),
  study: (s) => run(["tutor", "study", s.session, "--now", nowIso(s)].concat(s.useFsrs ? ["--useFsrs"] : []).concat(s.desiredRetention != null ? ["--desiredRetention", String(s.desiredRetention)] : [])),
  due: (s) => run(["tutor", "due", s.session, "--now", nowIso(s)].concat(s.useFsrs ? ["--useFsrs"] : [])),
  mastery: (s) => run(["tutor", "mastery", s.session]),
  misconceptions: (s) => run(["tutor", "misconceptions", s.session]),
  status: () => run(["status"]),
};
