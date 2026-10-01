#!/usr/bin/env node
// receipts.mjs - `telos receipts <verify|head|path>`. verify runs the offline
// verifier in demo/receipts/verify.mjs (stdlib only). When a checkpoints.jsonl
// sits next to the session file and no --checkpoints flag is given, it is used,
// so a removed suffix after a checkpoint is caught by default. The local public
// key is pinned by default when it exists.
import { existsSync, readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { receiptsDir } from "./receipts/chain.mjs";
import { publicKeyPath, telosHome } from "./receipts/keys.mjs";
import { cliMain, verifyChain } from "./receipts/verify.mjs";

function usage() {
  process.stderr.write([
    "usage: telos receipts <command>",
    "",
    "  verify <session.jsonl> [--checkpoints f] [--pubkey f] [--json]   offline chain verification",
    "  head <session.jsonl>                                              last seq, head seal and key",
    "  path                                                              where receipts are written",
    ""
  ].join("\n"));
  return 2;
}

// positional - the first argument that is neither a flag nor a flag's value.
function positional(args) {
  for (let i = 0; i < args.length; i += 1) {
    if (args[i] === "--checkpoints" || args[i] === "--pubkey") i += 1;
    else if (!args[i].startsWith("--")) return args[i];
  }
  return null;
}

export function main(argv) {
  const [command, ...rest] = argv;
  if (command === "verify") {
    const target = positional(rest);
    if (target && !rest.includes("--checkpoints")) {
      const sibling = path.join(path.dirname(target), "checkpoints.jsonl");
      if (existsSync(sibling)) rest.push("--checkpoints", sibling);
    }
    // Pin the local key by default. Without a pin the verifier can only report
    // a self-asserted MATCH, which a chain re-signed by any key also earns.
    const local = publicKeyPath(telosHome());
    if (!rest.includes("--pubkey") && existsSync(local)) rest.push("--pubkey", local);
    return cliMain(rest);
  }
  if (command === "head" && rest[0]) {
    const v = verifyChain(readFileSync(rest[0], "utf8"));
    const head = { verdict: v.verdict, session_id: v.session_id ?? null, seq: v.count ?? 0,
      head_seal: v.head_seal ?? null, signed_through: v.signed_through ?? 0, key_id: v.key_id ?? null };
    process.stdout.write(`${JSON.stringify(head, null, 2)}\n`);
    return v.verdict === "MATCH" ? 0 : v.verdict === "DRIFT" ? 1 : 2;
  }
  if (command === "path") {
    process.stdout.write(`${receiptsDir(telosHome())}\n`);
    return 0;
  }
  return usage();
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  process.exit(main(process.argv.slice(2)));
}
