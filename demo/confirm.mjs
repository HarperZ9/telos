#!/usr/bin/env node
// telos confirm: the human channel for holds (DESIGN.md 1.3, 1.4).
//
//   telos confirm list                 pending holds (T0)
//   telos confirm approve <hold_id>    shows the action, asks for a typed code
//   telos confirm reject <hold_id>
//
// approve and reject need an interactive terminal; the code they ask for is
// shown only on that terminal and never reaches the model.
import { fileURLToPath } from "node:url";
import { decideHold, HoldStore } from "./broker/holds.mjs";
import { loadPrivateKey, loadPublicKey } from "./broker/keys.mjs";
import { stateDirs } from "./broker/paths.mjs";
import { ask, interactive, parseFlags, typedCode } from "./broker/tty.mjs";

function store(dirs) {
  return new HoldStore({ dir: dirs.holds, publicKey: loadPublicKey(dirs.keys) });
}

function review(hold) {
  return { hold_id: hold.hold_id, tier: hold.tier, verb: hold.verb, grant_id: hold.grant_id, session_id: hold.session_id, expires_at: hold.expires_at, ...hold.review };
}

async function decide(dirs, holdId, decision) {
  const tty = interactive();
  const s = store(dirs);
  const hold = s.get(holdId);
  if (!hold) throw new Error(`no hold ${holdId}`);
  if (tty) {
    process.stdout.write(`${JSON.stringify(review(hold), null, 2)}\n`);
    const code = typedCode();
    const typed = await ask(`Type ${code} to ${decision} this action: `);
    if (typed !== code) throw new Error("code did not match; nothing decided");
  }
  const record = decideHold(s, holdId, decision, { privateKey: loadPrivateKey(dirs.keys), publicKey: loadPublicKey(dirs.keys), isTTY: tty });
  return { hold_id: holdId, decision: record.decision, decided_at: record.decided_at };
}

export async function main(argv, dirs = stateDirs()) {
  const { rest } = parseFlags(argv);
  const [cmd, id] = rest;
  if (cmd === "list" || !cmd) return { schema: "telos.hold-list/v1", pending: store(dirs).pending().map(review) };
  if ((cmd === "approve" || cmd === "reject") && id) return decide(dirs, id, cmd);
  throw new Error("usage: telos confirm <list|approve <hold_id>|reject <hold_id>>");
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  main(process.argv.slice(2)).then(
    (r) => process.stdout.write(`${JSON.stringify(r, null, 2)}\n`),
    (err) => {
      process.stderr.write(`telos confirm: ${err.message}\n`);
      process.exitCode = 1;
    },
  );
}
