#!/usr/bin/env node
// telos.mjs - the packaged `telos` command. A thin router over the existing demo
// command surface: `telos mcp` starts the stdio MCP server, `telos render <spec>`
// routes to the telos-cli render seam, and `telos <command> [args]` runs the
// matching `demo/<command>.mjs` script (status, doctor, room, catalog, and the
// rest of the registered command surface). Zero external dependencies.
import { spawnSync } from "node:child_process";
import { existsSync, realpathSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));

// Route table for names that do not map 1:1 onto demo/<name>.mjs.
const aliases = {
  mcp: "telos-mcp.mjs",
  render: "telos-cli.mjs"
};

function usage() {
  process.stderr.write(
    [
      "usage: telos <command> [args]",
      "",
      "  telos mcp                    start the stdio MCP server (demo/telos-mcp.mjs)",
      "  telos render <specPath>      render a learn.telos.scene-request/v1 spec (demo/telos-cli.mjs)",
      "  telos <command> [args]       run demo/<command>.mjs, e.g. status, doctor, room,",
      "                               catalog, server-manifest, run, mcp-freshness, ci-doctor",
      "",
      "Use `telos catalog --summary` for the full command and MCP tool map.",
      ""
    ].join("\n")
  );
}

// resolveScript - map a subcommand to a demo script path, or null. Names are
// restricted to lowercase words and hyphens so the router can never leave demo/.
function resolveScript(command) {
  if (typeof command !== "string" || !/^[a-z][a-z0-9-]*$/.test(command)) return null;
  const file = aliases[command] ?? `${command}.mjs`;
  const resolved = path.join(here, file);
  return existsSync(resolved) ? resolved : null;
}

export function main(argv) {
  const [command, ...rest] = argv;
  const script = resolveScript(command);
  if (!script) {
    usage();
    return 1;
  }
  // `render` keeps its subcommand: demo/telos-cli.mjs expects argv[0] === "render".
  const forwarded = command === "render" ? ["render", ...rest] : rest;
  const result = spawnSync(process.execPath, [script, ...forwarded], { stdio: "inherit" });
  return result.status ?? 1;
}

// Compare realpaths on both sides so the guard fires when npm installs the bin
// as a symlink and when node runs with --preserve-symlinks-main.
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
  process.exit(main(process.argv.slice(2)));
}
