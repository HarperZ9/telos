import { readFileSync } from "node:fs";

const manifest = JSON.parse(
  readFileSync(new URL("./integrations/mcp-server-manifest.json", import.meta.url), "utf8")
);

function selectedProfile(server, profile) {
  const value = server.profiles[profile];
  if (!value) {
    throw new Error(`unknown server profile ${profile}`);
  }
  return value;
}

function totalTools() {
  return Object.values(manifest.servers)
    .reduce((sum, server) => sum + server.expected_tools.length, 0);
}

function totalAuxiliaryTools() {
  return Object.values(manifest.servers)
    .reduce((sum, server) => sum + (server.auxiliary_tools ?? []).length, 0);
}

function freshnessProbeCount() {
  return Object.values(manifest.servers)
    .filter((server) => server.freshness?.status_tool).length;
}

export function summary() {
  const lines = [
    "Project Telos MCP Server Manifest",
    `servers  ${Object.keys(manifest.servers).length}`,
    `tools    ${totalTools()} expected`,
    `auxiliary ${totalAuxiliaryTools()} compatible`,
    `freshness ${freshnessProbeCount()} probes`,
    `profile  source_checkout`,
    `host     Codex TOML, Claude JSON, OpenAI Agents stdio`
  ];
  for (const [name, server] of Object.entries(manifest.servers)) {
    const auxiliary = (server.auxiliary_tools ?? []).length;
    const suffix = auxiliary ? ` + ${auxiliary} auxiliary` : "";
    lines.push(`${name.padEnd(9)} ${server.expected_tools.length} tools${suffix}`);
  }
  lines.push("next     node demo/server-manifest.mjs --codex");
  return `${lines.join("\n")}\n`;
}

export function codexToml(profile = "source_checkout") {
  const blocks = [];
  for (const [name, server] of Object.entries(manifest.servers)) {
    const config = selectedProfile(server, profile);
    blocks.push(`[mcp_servers.${name}]`);
    blocks.push(`command = ${tomlString(config.command)}`);
    blocks.push(`args = ${tomlArray(config.args ?? [])}`);
    if (config.cwd) {
      blocks.push(`cwd = ${tomlString(config.cwd)}`);
    }
    if (config.env) {
      blocks.push("");
      blocks.push(`[mcp_servers.${name}.env]`);
      for (const [key, value] of Object.entries(config.env)) {
        blocks.push(`${key} = ${tomlString(value)}`);
      }
    }
    blocks.push("");
  }
  return blocks.join("\n").trimEnd() + "\n";
}

export function claudeJson(profile = "source_checkout") {
  const mcpServers = {};
  for (const [name, server] of Object.entries(manifest.servers)) {
    const config = selectedProfile(server, profile);
    mcpServers[name] = {
      type: "stdio",
      command: config.command,
      args: config.args ?? []
    };
    if (config.cwd) {
      mcpServers[name].cwd = config.cwd;
    }
    if (config.env) {
      mcpServers[name].env = config.env;
    }
  }
  return `${JSON.stringify({ mcpServers }, null, 2)}\n`;
}

function tomlString(value) {
  return JSON.stringify(value);
}

function tomlArray(values) {
  return `[${values.map(tomlString).join(", ")}]`;
}

function profileFromArgs(args) {
  const index = args.indexOf("--profile");
  const inline = args.find((arg) => arg.startsWith("--profile="));
  if (inline) {
    return inline.slice("--profile=".length);
  }
  if (index !== -1) {
    return args[index + 1] ?? "source_checkout";
  }
  return "source_checkout";
}

function main() {
  const args = process.argv.slice(2);
  const profile = profileFromArgs(args);
  if (args.includes("--summary")) {
    process.stdout.write(summary());
  } else if (args.includes("--codex")) {
    process.stdout.write(codexToml(profile));
  } else if (args.includes("--claude-json")) {
    process.stdout.write(claudeJson(profile));
  } else {
    process.stdout.write(`${JSON.stringify(manifest, null, 2)}\n`);
  }
}

if (process.argv[1] && import.meta.url.endsWith(process.argv[1].replace(/\\/g, "/"))) {
  main();
}
