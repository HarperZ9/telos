#!/usr/bin/env node
// keys.mjs - `telos keys <init|show>`. init generates the local ed25519 receipt
// key once under <telos home>/keys and never overwrites it. show prints the
// public key file. Neither command prints or returns private key material.
import { existsSync, readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { initKey, publicKeyPath, telosHome } from "./receipts/keys.mjs";

export function main(argv) {
  const [command] = argv;
  const home = telosHome();
  if (command === "init") {
    try {
      const pub = initKey({ home });
      process.stdout.write(`${JSON.stringify({ status: "CREATED", ...pub, public_key_file: publicKeyPath(home) }, null, 2)}\n`);
      return 0;
    } catch (err) {
      process.stderr.write(`REFUSED  ${err.message}\n`);
      return 1;
    }
  }
  if (command === "show") {
    const file = publicKeyPath(home);
    if (!existsSync(file)) {
      process.stderr.write("NO_KEY  run `telos keys init` first\n");
      return 1;
    }
    process.stdout.write(readFileSync(file, "utf8"));
    return 0;
  }
  process.stderr.write("usage: telos keys <init|show>\n");
  return 2;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  process.exit(main(process.argv.slice(2)));
}
