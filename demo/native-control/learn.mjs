// learn integration: the accountable learning engine (tutor / spaced repetition /
// mastery gate) as a first-class witnessed action of the automation runner. A
// workflow can study an objective, record an attempt, and check mastery -- each
// step chained into the ledger, so a study + certification-prep run is itself a
// witnessed artifact. learn stays its own public flagship; this is the bridge.
//
// Shells to the learn CLI (node src/cli.mjs). Override the path with LEARN_CLI.
// learn uses exit code as a SIGNAL (e.g. mastery "not yet" exits non-zero), so
// run() returns the verdict text on stdout regardless of exit code.

import { spawnSync } from "node:child_process";

export const LEARN_CLI = process.env.LEARN_CLI || "C:/dev/public/learn/src/cli.mjs";

export function run(args, { timeoutMs = 45000 } = {}) {
  const r = spawnSync("node", [LEARN_CLI, ...args.map(String)], {
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
