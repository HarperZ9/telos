#!/usr/bin/env node
// telos reach: the agent-native crawler and reader CLI. Node built-ins only.
//
//   telos reach doctor [--json]
//   telos reach menu [--tier T1] [--memory FILE]
//   telos reach fetch <url>
//   telos reach site <url> [--depth 1] [--budget 10]
//   telos reach reddit listing <subreddit> [--sort hot] [--limit 25] [--time day]
//   telos reach reddit comments <post-id> [--depth 3] [--limit 100]
//   telos reach x oembed <post-url>
//   telos reach x post <id> | x search <query> [--max 10] | x user <name> [--max 10]
//   telos reach api <channel> <op> [key=value ...]
//
// Common flags: --receipt FILE appends the receipt as JSON lines; --memory FILE
// records what was read for the action menu; --request - reads parameters as
// JSON from stdin (the MCP server uses this).
import { readFileSync, realpathSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { formatDoctor } from "./reach/doctor.mjs";
import { runReach } from "./reach/run.mjs";

const NUMERIC = new Set(["depth", "budget", "page_budget", "limit", "max"]);

/** Split argv into positionals and --flags. */
export function parseArgs(argv) {
  const positional = [];
  const flags = {};
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (!arg.startsWith("--")) {
      positional.push(arg);
      continue;
    }
    const key = arg.slice(2).replace(/-/g, "_");
    const next = argv[i + 1];
    if (next === undefined || next.startsWith("--")) flags[key] = true;
    else {
      flags[key] = NUMERIC.has(key) ? Number(next) : next;
      i += 1;
    }
  }
  return { positional, flags };
}

const X_OPS = { post: ["post", "id"], search: ["search_recent", "query"], user: ["user_posts", "username"] };

/** Map CLI words to a reach command and parameters. */
export function toCommand(positional, flags) {
  const [first, second, ...rest] = positional;
  const pick = ({ json, receipt, memory, request, ...other }) => other;
  const base = pick(flags);
  if (first === "reddit" && second === "listing") return ["reddit-listing", { ...base, subreddit: rest[0] }];
  if (first === "reddit" && second === "comments") return ["reddit-comments", { ...base, post_id: rest[0] }];
  if (first === "x" && second === "oembed") return ["x-oembed", { ...base, url: rest[0] }];
  if (first === "x" && X_OPS[second]) return ["x-api", { ...base, op: X_OPS[second][0], [X_OPS[second][1]]: rest.join(" ") }];
  if (first === "api") {
    const [op, ...pairs] = rest;
    const params = Object.fromEntries(pairs.map((kv) => kv.split("=")).map(([k, ...v]) => [k, v.join("=")]));
    return ["api", { channel: second, op, params: { ...params, ...base } }];
  }
  if (first === "fetch" || first === "site") return [first, { ...base, url: second }];
  if (first === "menu") return ["menu", { tier: flags.tier, memory: flags.memory }];
  return [first, base];
}

function readRequest() {
  const text = readFileSync(0, "utf8").trim();
  return text ? JSON.parse(text) : {};
}

export async function main(argv) {
  const { positional, flags } = parseArgs(argv);
  let [command, params] = toCommand(positional, flags);
  if (flags.request === "-") params = { ...params, ...readRequest() };
  if (!command) {
    process.stderr.write("usage: telos reach <doctor|menu|fetch|site|reddit|x|api> ...\n");
    return 2;
  }
  try {
    const out = await runReach(command, params, { receiptFile: flags.receipt, memoryFile: flags.memory });
    const human = command === "doctor" && !flags.json && !flags.request;
    process.stdout.write(`${human ? formatDoctor(out) : JSON.stringify(out, null, 2)}\n`);
    return 0;
  } catch (err) {
    process.stderr.write(`${JSON.stringify({ error: err instanceof Error ? err.message : String(err), command })}\n`);
    return 1;
  }
}

function samePath(a, b) {
  const canonical = (value) => {
    let resolved = path.resolve(value);
    try {
      resolved = realpathSync(resolved);
    } catch {
      // keep the resolved path when realpath is unavailable
    }
    return process.platform === "win32" ? resolved.toLowerCase() : resolved;
  };
  return canonical(a) === canonical(b);
}

if (process.argv[1] && samePath(process.argv[1], fileURLToPath(import.meta.url))) {
  main(process.argv.slice(2)).then((code) => {
    process.exitCode = code;
  });
}
