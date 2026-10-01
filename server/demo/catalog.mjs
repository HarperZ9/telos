import { readFileSync } from "node:fs";

const catalog = JSON.parse(
  readFileSync(new URL("./integrations/mcp-tool-catalog.json", import.meta.url), "utf8")
);

function countsByStatus(tools) {
  const counts = {};
  for (const tool of tools) {
    const status = tool.mcp.status;
    counts[status] = (counts[status] ?? 0) + 1;
  }
  return counts;
}

function toolsByFlagship(tools) {
  const grouped = new Map();
  for (const tool of tools) {
    const existing = grouped.get(tool.flagship) ?? [];
    existing.push(tool.name);
    grouped.set(tool.flagship, existing);
  }
  return grouped;
}

function compactToolList(names) {
  const visible = names.slice(0, 2).join(", ");
  const remaining = names.length - 2;
  return remaining > 0 ? `${visible}, +${remaining} more` : visible;
}

function summary(catalog) {
  const counts = countsByStatus(catalog.tools);
  const lines = [
    "Project Telos MCP Catalog",
    `tools    ${catalog.tools.length} total, ${counts.available ?? 0} available`,
    `transport ${catalog.transports.join(", ")}`
  ];
  for (const [flagship, names] of toolsByFlagship(catalog.tools)) {
    lines.push(`${flagship.padEnd(9)} ${names.length} tools ${compactToolList(names)}`);
  }
  lines.push("next     node demo/catalog.mjs");
  return `${lines.join("\n")}\n`;
}

if (process.argv.includes("--summary")) {
  process.stdout.write(summary(catalog));
} else {
  process.stdout.write(`${JSON.stringify(catalog, null, 2)}\n`);
}
