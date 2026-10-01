#!/usr/bin/env node
// telos keys: the one local ed25519 key. It signs grants and hold decisions
// (broker) and receipt chain heads and checkpoints (receipts).
//
//   telos keys id      print the key id (sha256 of the raw public key), or null
//   telos keys show    print the public key record (no private material)
//   telos keys init    create the key pair once; needs an interactive terminal,
//                      so an agent's shell cannot mint the key that signs grants
import { existsSync, readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { initKeys, keyId, loadPublicKey } from "./broker/keys.mjs";
import { stateDirs } from "./broker/paths.mjs";
import { interactive } from "./broker/tty.mjs";
import { publicKeyPath } from "./receipts/keys.mjs";

export function main(argv, dirs = stateDirs(), isTTY = interactive()) {
  const [cmd] = argv;
  if (cmd === "init") {
    const { key_id } = initKeys(dirs.keys, { isTTY });
    return { status: "CREATED", key_id, public_key_file: publicKeyPath(dirs.root) };
  }
  if (cmd === "show") {
    const file = publicKeyPath(dirs.root);
    if (!existsSync(file)) throw new Error("NO_KEY  run `telos keys init` in an interactive terminal first");
    return JSON.parse(readFileSync(file, "utf8"));
  }
  if (cmd === "id" || !cmd) {
    const pub = loadPublicKey(dirs.keys);
    return { key_id: pub ? keyId(pub) : null };
  }
  throw new Error("usage: telos keys <id|show|init>");
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    process.stdout.write(`${JSON.stringify(main(process.argv.slice(2)), null, 2)}\n`);
  } catch (err) {
    process.stderr.write(`telos keys: ${err.message}\n`);
    process.exitCode = 1;
  }
}
