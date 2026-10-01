// Terminal helpers for the human-only commands (`telos grant`, `telos confirm`,
// `telos keys`). Both stdin and stdout must be a TTY: an agent's shell pipes
// both, so these commands refuse there before asking anything.
import { randomInt } from "node:crypto";
import { createInterface } from "node:readline/promises";

export function interactive(stdin = process.stdin, stdout = process.stdout) {
  return stdin.isTTY === true && stdout.isTTY === true;
}

export async function ask(question) {
  const rl = createInterface({ input: process.stdin, output: process.stdout });
  try {
    return (await rl.question(question)).trim();
  } finally {
    rl.close();
  }
}

// A short code shown only on this terminal and typed back, so a decision needs
// someone reading this screen.
const ALPHABET = "ABCDEFGHJKMNPQRSTUVWXYZ23456789";
export function typedCode(length = 6) {
  let out = "";
  for (let i = 0; i < length; i++) out += ALPHABET[randomInt(ALPHABET.length)];
  return out;
}

export function parseFlags(argv) {
  const flags = {};
  const rest = [];
  for (const a of argv) {
    const m = /^--([^=]+)=(.*)$/.exec(a);
    if (m) flags[m[1]] = m[2];
    else rest.push(a);
  }
  return { rest, flags };
}

export const list = (v) => (v ? v.split(",").map((s) => s.trim()).filter(Boolean) : []);
