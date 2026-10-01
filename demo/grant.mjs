#!/usr/bin/env node
// telos grant: the only writer of permission grants (DESIGN.md 1.2).
//
//   telos grant status                         list live and rejected grants (T0)
//   telos grant issue --tier=T3 --verbs=browser.click,browser.fill
//         [--origins=https://a.test] [--windows=Title,Other] [--paths=..]
//         [--sandbox=..] [--exec="git status;git log **"] [--devices=..]
//         [--senses=..] [--ttl=seconds] [--max-actions=n] [--batch=n]
//   telos grant revoke <grant_id>
//
// issue and revoke need an interactive terminal and a typed confirmation.
import { fileURLToPath } from "node:url";
import { issueGrant, loadGrants, revokeGrant, saveGrant } from "./broker/grants.mjs";
import { loadPrivateKey, loadPublicKey } from "./broker/keys.mjs";
import { stateDirs } from "./broker/paths.mjs";
import { ask, interactive, list, parseFlags } from "./broker/tty.mjs";

const int = (v) => (v === undefined ? undefined : Number.parseInt(v, 10));

export function specFromFlags(flags) {
  return {
    tier: flags.tier,
    verbs: list(flags.verbs),
    scope: {
      origins: list(flags.origins),
      windows: list(flags.windows).map((title) => ({ title_contains: title })),
      paths: list(flags.paths),
      sandbox_roots: list(flags.sandbox),
      exec_allow: (flags.exec ?? "").split(";").map((s) => s.trim()).filter(Boolean).map((s) => s.split(/\s+/)),
      devices: list(flags.devices),
      senses: list(flags.senses),
    },
    ttl_s: int(flags.ttl),
    max_actions: int(flags["max-actions"]),
    batch: int(flags.batch),
  };
}

function status(dirs) {
  const publicKey = loadPublicKey(dirs.keys);
  const { live, rejected } = loadGrants(dirs.grants, { publicKey });
  const brief = (g) => ({ grant_id: g.grant_id, tier: g.tier, verbs: g.verbs, scope: g.scope, expires_at: g.expires_at, max_actions: g.max_actions ?? null });
  return { schema: "telos.grant-status/v1", key_present: Boolean(publicKey), live: live.map(brief), rejected };
}

async function issue(dirs, flags) {
  const tty = interactive();
  const privateKey = loadPrivateKey(dirs.keys);
  const publicKey = loadPublicKey(dirs.keys);
  if (!privateKey || !publicKey) throw new Error("no Telos key; run `telos keys init` at a terminal first");
  const spec = specFromFlags(flags);
  if (tty) {
    process.stdout.write(`${JSON.stringify(spec, null, 2)}\n`);
    const typed = await ask(`Type the tier (${spec.tier}) to sign this grant: `);
    if (typed !== spec.tier) throw new Error("not confirmed; no grant written");
  }
  const grant = issueGrant(spec, { privateKey, publicKey, isTTY: tty });
  saveGrant(dirs.grants, grant);
  return { grant_id: grant.grant_id, tier: grant.tier, expires_at: grant.expires_at };
}

async function revoke(dirs, id) {
  const tty = interactive();
  if (tty && (await ask(`Type the grant id to revoke ${id}: `)) !== id) throw new Error("not confirmed");
  revokeGrant(dirs.grants, id, { isTTY: tty });
  return { revoked: id };
}

export async function main(argv, dirs = stateDirs()) {
  const { rest, flags } = parseFlags(argv);
  const [cmd, arg] = rest;
  if (cmd === "status" || !cmd) return status(dirs);
  if (cmd === "issue") return issue(dirs, flags);
  if (cmd === "revoke" && arg) return revoke(dirs, arg);
  throw new Error("usage: telos grant <status|issue|revoke <id>>");
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  main(process.argv.slice(2)).then(
    (r) => process.stdout.write(`${JSON.stringify(r, null, 2)}\n`),
    (err) => {
      process.stderr.write(`telos grant: ${err.message}\n`);
      process.exitCode = 1;
    },
  );
}
