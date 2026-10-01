#!/usr/bin/env node
// telos keys: the local ed25519 key that signs grants and hold decisions.
//
//   telos keys id      print the key id (sha256 of the raw public key), or null
//   telos keys init    create the key pair; needs an interactive terminal
import { fileURLToPath } from "node:url";
import { initKeys, keyId, loadPublicKey } from "./broker/keys.mjs";
import { stateDirs } from "./broker/paths.mjs";
import { interactive } from "./broker/tty.mjs";

export function main(argv, dirs = stateDirs()) {
  const [cmd] = argv;
  if (cmd === "init") return initKeys(dirs.keys, { isTTY: interactive() });
  if (cmd === "id" || !cmd) {
    const pub = loadPublicKey(dirs.keys);
    return { key_id: pub ? keyId(pub) : null };
  }
  throw new Error("usage: telos keys <id|init>");
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  try {
    process.stdout.write(`${JSON.stringify(main(process.argv.slice(2)), null, 2)}\n`);
  } catch (err) {
    process.stderr.write(`telos keys: ${err.message}\n`);
    process.exitCode = 1;
  }
}
