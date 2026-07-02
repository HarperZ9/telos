import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { scanCompatibilitySurface } from "./compatibility-doctor.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));

const failureCodes = [
  "stale_mcp_server",
  "tool_surface_drift",
  "version_drift",
  "behavior_probe_drift",
  "launch_profile_unresolved",
  "freshness_probe_unavailable"
];

const goodCatalog = {
  schema: "project-telos.mcp-tool-catalog/v1",
  action_schema: "project-telos.flagship-action/v1",
  transports: ["stdio", "streamable-http"],
  tools: [
    {
      name: "gather.status",
      flagship: "gather",
      description: "Emit Gather readiness.",
      cli: ["gather", "status", "--json"],
      mcp: { status: "available", server: "gather", method: "tools/call", tool: "gather.status" },
      next_actions: ["index.map"]
    },
    {
      name: "telos.catalog",
      flagship: "telos",
      description: "Emit Telos catalog.",
      cli: ["node", "demo/catalog.mjs"],
      mcp: { status: "available", server: "telos", method: "tools/call", tool: "telos.catalog" },
      next_actions: ["telos.server.manifest"]
    }
  ]
};

const goodManifest = {
  schema: "project-telos.mcp-server-manifest/v1",
  transports: ["stdio"],
  profiles: ["source_checkout", "package"],
  hosts: {
    codex: { config_key: "mcp_servers", format: "toml" },
    claude: { container_key: "mcpServers", format: "json" },
    openai_agents: { transport: "stdio" },
    openai_apps: { transport: "mcp" }
  },
  sources: [
    { name: "MCP", url: "https://modelcontextprotocol.io/specification/2025-06-18" }
  ],
  servers: {
    gather: {
      expected_tools: ["gather.status"],
      freshness: {
        status_tool: "gather.status",
        expected_version: "1.5.0",
        expected_current_status: "ready",
        failure_codes: failureCodes
      },
      profiles: {
        source_checkout: { command: "python", args: ["-m", "gather.cli", "mcp"] },
        package: { command: "gather", args: ["mcp"] }
      }
    },
    telos: {
      expected_tools: ["telos.catalog"],
      freshness: {
        status_tool: "telos.status",
        expected_version: "0.1.0",
        expected_current_status: "ready",
        failure_codes: failureCodes
      },
      profiles: {
        source_checkout: { command: "node", args: ["${PROJECT_TELOS_PUBLIC}/telos/demo/telos-mcp.mjs"] },
        package: { command: "telos", args: ["mcp"] }
      }
    }
  }
};

const badCatalog = {
  schema: "wrong",
  transports: ["stdio"],
  tools: [
    {
      name: "gather.status",
      flagship: "gather",
      description: "No CLI and unavailable MCP.",
      cli: [],
      mcp: { status: "missing", server: "gather", method: "tools/call", tool: "gather.status" },
      next_actions: []
    }
  ]
};

const badManifest = {
  schema: "wrong",
  workspace_placeholder: "C:\\Users\\Example\\secret",
  transports: [],
  profiles: ["package"],
  hosts: {
    codex: { config_key: "mcp_servers" }
  },
  sources: [
    { name: "bad", url: "http://example.test/insecure" }
  ],
  servers: {
    gather: {
      expected_tools: ["gather.status", "gather.missing"],
      freshness: {
        status_tool: "",
        failure_codes: ["stale_mcp_server"]
      },
      profiles: {}
    }
  }
};

const tempRoot = mkdtempSync(path.join(tmpdir(), "telos-compatibility-doctor-"));
try {
  const goodCatalogPath = path.join(tempRoot, "good-catalog.json");
  const goodManifestPath = path.join(tempRoot, "good-manifest.json");
  const badCatalogPath = path.join(tempRoot, "bad-catalog.json");
  const badManifestPath = path.join(tempRoot, "bad-manifest.json");
  writeFileSync(goodCatalogPath, JSON.stringify(goodCatalog, null, 2), "utf8");
  writeFileSync(goodManifestPath, JSON.stringify(goodManifest, null, 2), "utf8");
  writeFileSync(badCatalogPath, JSON.stringify(badCatalog, null, 2), "utf8");
  writeFileSync(badManifestPath, JSON.stringify(badManifest, null, 2), "utf8");

  const match = scanCompatibilitySurface({
    catalogPath: goodCatalogPath,
    manifestPath: goodManifestPath,
    generatedAt: "2026-06-29T00:00:00.000Z"
  });
  assert.equal(match.schema, "project-telos.compatibility-doctor/v1");
  assert.equal(match.tool, "telos.compatibility.doctor");
  assert.equal(match.generated_at, "2026-06-29T00:00:00.000Z");
  assert.equal(match.aggregate.check_count, 14);
  assert.equal(match.aggregate.verdict, "MATCH");
  assert.deepEqual(match.aggregate.failure_codes, []);
  assert.equal(match.metrics.tool_count, 2);
  assert.equal(match.metrics.server_count, 2);
  assert.equal(match.signals.expected_tools_join_catalog, true);
  assert.equal(match.signals.host_exports_present, true);
  assert.equal(match.privacy_boundary.raw_catalog_included, false);
  assert.equal(match.privacy_boundary.raw_manifest_included, false);
  assert.equal(JSON.stringify(match).includes(tempRoot), false, "scanner must not leak absolute temp path");
  assert.equal(JSON.stringify(match).includes("Emit Gather readiness"), false, "scanner must not include raw catalog body");

  const drift = scanCompatibilitySurface({
    catalogPath: badCatalogPath,
    manifestPath: badManifestPath,
    generatedAt: "2026-06-29T00:00:01.000Z"
  });
  assert.equal(drift.aggregate.verdict, "DRIFT");
  assert.deepEqual(drift.aggregate.failure_codes, [
    "catalog_schema_invalid",
    "manifest_schema_invalid",
    "streamable_http_transport_missing",
    "manifest_stdio_transport_missing",
    "host_export_missing",
    "source_checkout_profile_missing",
    "expected_tool_unjoinable",
    "cli_fallback_missing",
    "mcp_unavailable",
    "freshness_status_tool_missing",
    "freshness_failure_codes_incomplete",
    "source_url_not_https",
    "private_path_leak",
    "package_profile_missing"
  ]);

  const missing = scanCompatibilitySurface({
    catalogPath: path.join(tempRoot, "missing-catalog.json"),
    manifestPath: goodManifestPath,
    generatedAt: "2026-06-29T00:00:02.000Z"
  });
  assert.equal(missing.aggregate.verdict, "UNVERIFIABLE");
  assert.deepEqual(missing.aggregate.failure_codes, ["compatibility_surface_unjoinable"]);

  const cli = spawnSync(process.execPath, [
    path.join(here, "compatibility-doctor.mjs"),
    "--catalog",
    goodCatalogPath,
    "--manifest",
    goodManifestPath
  ], {
    cwd: path.resolve(here, ".."),
    encoding: "utf8"
  });
  assert.equal(cli.status, 0, cli.stderr || cli.stdout);
  assert.equal(JSON.parse(cli.stdout).aggregate.verdict, "MATCH");

  const summary = spawnSync(process.execPath, [
    path.join(here, "compatibility-doctor.mjs"),
    "--catalog",
    goodCatalogPath,
    "--manifest",
    goodManifestPath,
    "--summary"
  ], {
    cwd: path.resolve(here, ".."),
    encoding: "utf8"
  });
  assert.equal(summary.status, 0, summary.stderr || summary.stdout);
  assert.match(summary.stdout, /Telos Compatibility Doctor/);
  assert.match(summary.stdout, /checks\s+14/);
  assert.match(summary.stdout, /verdict\s+MATCH/);

  const real = scanCompatibilitySurface({ generatedAt: "2026-06-29T00:00:03.000Z" });
  assert.equal(real.aggregate.verdict, "MATCH");
  assert.equal(real.metrics.server_count, 5);
  assert.equal(real.metrics.tool_count, 69);
} finally {
  rmSync(tempRoot, { recursive: true, force: true });
}
