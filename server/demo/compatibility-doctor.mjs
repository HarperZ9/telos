import { createHash } from "node:crypto";
import { existsSync, readFileSync, statSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const defaultCatalog = path.join(here, "integrations", "mcp-tool-catalog.json");
const defaultManifest = path.join(here, "integrations", "mcp-server-manifest.json");

const requiredFreshnessCodes = [
  "stale_mcp_server",
  "tool_surface_drift",
  "version_drift",
  "behavior_probe_drift",
  "launch_profile_unresolved",
  "freshness_probe_unavailable"
];

function sha256(text) {
  return `sha256:${createHash("sha256").update(text).digest("hex")}`;
}

function relativeLabel(filePath) {
  const relative = path.relative(path.resolve(here, ".."), filePath).replace(/\\/g, "/");
  return relative.startsWith("..") ? path.basename(filePath) : relative;
}

function readJsonSurface(filePath) {
  const resolved = path.resolve(filePath);
  if (!existsSync(resolved) || !statSync(resolved).isFile()) {
    return { resolved, present: false };
  }
  const text = readFileSync(resolved, "utf8");
  return { resolved, present: true, text, value: JSON.parse(text), hash: sha256(text) };
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function toolNames(catalog) {
  return new Set((catalog.tools ?? []).map((tool) => tool.name));
}

function expectedToolNames(manifest) {
  return new Set(Object.values(manifest.servers ?? {}).flatMap((server) => server.expected_tools ?? []));
}

function everyTool(catalog, predicate) {
  const tools = catalog.tools ?? [];
  return tools.length > 0 && tools.every(predicate);
}

function everyServer(manifest, predicate) {
  const servers = Object.values(manifest.servers ?? {});
  return servers.length > 0 && servers.every(predicate);
}

function hostsPresent(manifest) {
  const hosts = manifest.hosts ?? {};
  return Boolean(
    hosts.codex?.config_key === "mcp_servers"
      && hosts.claude?.container_key === "mcpServers"
      && hosts.openai_agents?.transport === "stdio"
      && hosts.openai_apps?.transport
  );
}

function expectedToolsJoin(catalog, manifest) {
  const catalogNames = toolNames(catalog);
  const expectedNames = expectedToolNames(manifest);
  if (catalogNames.size === 0 || expectedNames.size === 0 || catalogNames.size !== expectedNames.size) {
    return false;
  }
  return [...expectedNames].every((name) => catalogNames.has(name));
}

function freshnessCodesComplete(manifest) {
  return everyServer(manifest, (server) => {
    const codes = new Set(server.freshness?.failure_codes ?? []);
    return requiredFreshnessCodes.every((code) => codes.has(code));
  });
}

function sourceUrlsHttps(manifest) {
  const sources = manifest.sources ?? [];
  return sources.length > 0 && sources.every((source) => /^https:\/\//i.test(source.url ?? ""));
}

function privatePathAbsent(...texts) {
  const joined = texts.join("\n");
  return !/(?:[A-Z]:\\Users\\|\/Users\/|\/home\/|AppData|\.env\b|secret|private[_-]?key)/i.test(joined);
}

function signalsFor(catalog, manifest, catalogText, manifestText) {
  const tools = catalog.tools ?? [];
  const servers = Object.values(manifest.servers ?? {});
  return {
    catalog_schema: catalog.schema === "project-telos.mcp-tool-catalog/v1",
    manifest_schema: manifest.schema === "project-telos.mcp-server-manifest/v1",
    streamable_http_transport: (catalog.transports ?? []).includes("streamable-http"),
    manifest_stdio_transport: (manifest.transports ?? []).includes("stdio"),
    host_exports_present: hostsPresent(manifest),
    source_checkout_profiles: everyServer(manifest, (server) => Boolean(server.profiles?.source_checkout)),
    expected_tools_join_catalog: expectedToolsJoin(catalog, manifest),
    cli_fallbacks: everyTool(catalog, (tool) => Array.isArray(tool.cli) && tool.cli.length > 0),
    mcp_available: everyTool(catalog, (tool) => tool.mcp?.status === "available" && tool.mcp?.method === "tools/call"),
    freshness_status_tools: everyServer(manifest, (server) => Boolean(server.freshness?.status_tool)),
    freshness_failure_codes: freshnessCodesComplete(manifest),
    source_urls_https: sourceUrlsHttps(manifest),
    private_path_absent: privatePathAbsent(catalogText, manifestText),
    package_profiles: servers.length > 0 && servers.every((server) => Boolean(server.profiles?.package))
  };
}

function metricsFor(catalog, manifest) {
  const tools = catalog.tools ?? [];
  const servers = Object.values(manifest.servers ?? {});
  return {
    tool_count: tools.length,
    server_count: servers.length,
    expected_tool_count: [...expectedToolNames(manifest)].length,
    available_mcp_tools: tools.filter((tool) => tool.mcp?.status === "available").length,
    host_count: Object.keys(manifest.hosts ?? {}).length,
    source_count: (manifest.sources ?? []).length
  };
}

function signalFailures(signals) {
  const mapping = {
    catalog_schema: "catalog_schema_invalid",
    manifest_schema: "manifest_schema_invalid",
    streamable_http_transport: "streamable_http_transport_missing",
    manifest_stdio_transport: "manifest_stdio_transport_missing",
    host_exports_present: "host_export_missing",
    source_checkout_profiles: "source_checkout_profile_missing",
    expected_tools_join_catalog: "expected_tool_unjoinable",
    cli_fallbacks: "cli_fallback_missing",
    mcp_available: "mcp_unavailable",
    freshness_status_tools: "freshness_status_tool_missing",
    freshness_failure_codes: "freshness_failure_codes_incomplete",
    source_urls_https: "source_url_not_https",
    private_path_absent: "private_path_leak",
    package_profiles: "package_profile_missing"
  };
  return Object.entries(mapping)
    .filter(([key]) => !signals[key])
    .map(([, code]) => code);
}

export function scanCompatibilitySurface(options = {}) {
  const catalogPath = options.catalogPath ?? defaultCatalog;
  const manifestPath = options.manifestPath ?? defaultManifest;
  const catalog = readJsonSurface(catalogPath);
  const manifest = readJsonSurface(manifestPath);
  const surfaces = {
    catalog: surfaceRef(catalog),
    manifest: surfaceRef(manifest)
  };
  if (!catalog.present || !manifest.present) {
    return {
      schema: "project-telos.compatibility-doctor/v1",
      tool: "telos.compatibility.doctor",
      generated_at: options.generatedAt ?? new Date().toISOString(),
      surfaces,
      aggregate: {
        check_count: 14,
        passed_count: 0,
        verdict: "UNVERIFIABLE",
        failure_codes: ["compatibility_surface_unjoinable"]
      },
      privacy_boundary: privacyBoundary(),
      metrics: {},
      signals: {},
      requirements: requirements()
    };
  }

  const signals = signalsFor(catalog.value, manifest.value, catalog.text, manifest.text);
  const failures = unique(signalFailures(signals));
  return {
    schema: "project-telos.compatibility-doctor/v1",
    tool: "telos.compatibility.doctor",
    generated_at: options.generatedAt ?? new Date().toISOString(),
    surfaces,
    aggregate: {
      check_count: Object.keys(signals).length,
      passed_count: Object.values(signals).filter(Boolean).length,
      verdict: failures.length === 0 ? "MATCH" : "DRIFT",
      failure_codes: failures
    },
    privacy_boundary: privacyBoundary(),
    metrics: metricsFor(catalog.value, manifest.value),
    signals,
    requirements: requirements()
  };
}

function surfaceRef(surface) {
  return {
    kind: "json",
    present: surface.present,
    path_ref: relativeLabel(surface.resolved),
    ...(surface.hash ? { hash: surface.hash } : {})
  };
}

function privacyBoundary() {
  return {
    raw_catalog_included: false,
    raw_manifest_included: false,
    absolute_paths_included: false,
    external_fetches_performed: false,
    filesystem_writes_performed: false,
    browser_automation_required: false
  };
}

function requirements() {
  return [
    "Catalog and server manifest use current Project Telos schemas and host-neutral transports",
    "Manifest exports cover Codex, Claude, OpenAI Agents, OpenAI Apps, source checkouts, and packages",
    "Expected tools join exactly to catalog tools with CLI fallbacks and available MCP tools",
    "Freshness probes, HTTPS protocol sources, and private-path hygiene remain explicit"
  ];
}

export function summary(value = scanCompatibilitySurface()) {
  const lines = [
    "Telos Compatibility Doctor",
    `schema       ${value.schema}`,
    `tool         ${value.tool}`,
    `tools        ${value.metrics.tool_count ?? 0}`,
    `servers      ${value.metrics.server_count ?? 0}`,
    `checks       ${value.aggregate.check_count}`,
    `passed       ${value.aggregate.passed_count}`,
    `verdict      ${value.aggregate.verdict}`,
    "next         node demo/compatibility-doctor.mjs"
  ];
  return `${lines.join("\n")}\n`;
}

function optionValue(args, name) {
  const index = args.indexOf(name);
  const inline = args.find((arg) => arg.startsWith(`${name}=`));
  if (inline) {
    return inline.slice(name.length + 1);
  }
  if (index !== -1) {
    return args[index + 1];
  }
  return null;
}

function main() {
  const args = process.argv.slice(2);
  const packet = scanCompatibilitySurface({
    catalogPath: optionValue(args, "--catalog") ?? defaultCatalog,
    manifestPath: optionValue(args, "--manifest") ?? defaultManifest
  });
  if (args.includes("--summary")) {
    process.stdout.write(summary(packet));
  } else {
    process.stdout.write(`${JSON.stringify(packet, null, 2)}\n`);
  }
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  main();
}
