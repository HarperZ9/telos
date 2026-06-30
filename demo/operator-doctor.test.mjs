import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { scanOperatorSurface } from "./operator-doctor.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));

const doctors = [
  "ci-doctor",
  "presentation-doctor",
  "accessibility-doctor",
  "performance-doctor",
  "compatibility-doctor",
  "operator-doctor"
];

const goodStatus = {
  native: {
    commands: ["run", "catalog", "server-manifest", ...doctors],
    statuses: ["MATCH", "DRIFT", "UNVERIFIABLE", "ERROR"],
    mcp_tools: ["telos.status", "telos.operator.doctor"]
  },
  next_actions: [
    { tool: "index", action: "map" },
    { tool: "gather", action: "docs" }
  ]
};

const goodCatalog = {
  tools: [
    { name: "gather.status", flagship: "gather", cli: ["gather", "status"], mcp: { status: "available" } },
    { name: "telos.status", flagship: "telos", cli: ["node", "demo/status.mjs"], mcp: { status: "available" } },
    { name: "telos.operator.doctor", flagship: "telos", cli: ["node", "demo/operator-doctor.mjs"], mcp: { status: "available" } }
  ]
};

const goodManifest = {
  servers: {
    gather: { expected_tools: ["gather.status"] },
    telos: { expected_tools: ["telos.status", "telos.operator.doctor"] }
  }
};

const goodReadme = `# Project Telos

## Try it

Zero dependencies.

\`\`\`bash
node demo/run.mjs
node demo/catalog.mjs --summary
node demo/server-manifest.mjs --summary
node demo/ci-doctor.mjs --summary
node demo/presentation-doctor.mjs --summary
node demo/accessibility-doctor.mjs --summary
node demo/performance-doctor.mjs --summary
node demo/compatibility-doctor.mjs --summary
node demo/operator-doctor.mjs --summary
\`\`\`

Use \`npm start\` or \`node demo/telos-mcp.mjs\` to run the Telos stdio MCP server.
Use \`node demo/catalog.mjs --summary\` for CLI and MCP operator maps.
Use \`node demo/server-manifest.mjs --summary\` for Codex, Claude, OpenAI Agents, plugins, IDE, TUI, and app hosts.
Use each doctor command to produce MATCH, DRIFT, or UNVERIFIABLE receipts.
`;

const goodCurrentState = `# Project Telos Current State

Telos catalog now presents 3 available tools.
The CI doctor lane is native.
The presentation doctor lane is native.
The accessibility doctor lane is native.
The performance doctor lane is native.
The compatibility doctor lane is native.
The operator doctor lane is native.
`;

const goodCi = `
run: |
  node demo/ci-doctor.test.mjs
  node demo/presentation-doctor.test.mjs
  node demo/accessibility-doctor.test.mjs
  node demo/performance-doctor.test.mjs
  node demo/compatibility-doctor.test.mjs
  node demo/operator-doctor.test.mjs
`;

const badReadme = "# Project Telos\nNo useful operating instructions.";
const badCurrentState = "# Project Telos Current State\nTelos catalog now presents 99 available tools.";
const badCi = "run: |\n  node demo/ci-doctor.test.mjs\n";
const badStatus = {
  native: {
    commands: [],
    statuses: ["MATCH"],
    mcp_tools: ["telos.missing"]
  },
  next_actions: []
};
const badCatalog = {
  tools: [
    { name: "telos.status", flagship: "telos", cli: [], mcp: { status: "missing" } }
  ]
};
const badManifest = {
  servers: {
    telos: { expected_tools: ["telos.status", "telos.missing"] }
  }
};

const tempRoot = mkdtempSync(path.join(tmpdir(), "telos-operator-doctor-"));
try {
  const paths = {};
  function write(name, body) {
    const filePath = path.join(tempRoot, name);
    writeFileSync(filePath, typeof body === "string" ? body : JSON.stringify(body, null, 2), "utf8");
    paths[name] = filePath;
  }
  write("README-good.md", goodReadme);
  write("CURRENT-good.md", goodCurrentState);
  write("ci-good.yml", goodCi);
  write("catalog-good.json", goodCatalog);
  write("manifest-good.json", goodManifest);
  write("status-good.json", goodStatus);
  write("README-bad.md", badReadme);
  write("CURRENT-bad.md", badCurrentState);
  write("ci-bad.yml", badCi);
  write("catalog-bad.json", badCatalog);
  write("manifest-bad.json", badManifest);
  write("status-bad.json", badStatus);

  const match = scanOperatorSurface({
    readmePath: paths["README-good.md"],
    currentStatePath: paths["CURRENT-good.md"],
    ciPath: paths["ci-good.yml"],
    catalogPath: paths["catalog-good.json"],
    manifestPath: paths["manifest-good.json"],
    statusPath: paths["status-good.json"],
    generatedAt: "2026-06-29T00:00:00.000Z"
  });
  assert.equal(match.schema, "project-telos.operator-doctor/v1");
  assert.equal(match.tool, "telos.operator.doctor");
  assert.equal(match.generated_at, "2026-06-29T00:00:00.000Z");
  assert.equal(match.aggregate.check_count, 14);
  assert.equal(match.aggregate.verdict, "MATCH");
  assert.deepEqual(match.aggregate.failure_codes, []);
  assert.equal(match.metrics.tool_count, 3);
  assert.equal(match.metrics.telos_tool_count, 2);
  assert.equal(match.metrics.doctor_lane_count, 6);
  assert.equal(match.signals.status_catalog_tool_parity, true);
  assert.equal(match.privacy_boundary.raw_docs_included, false);
  assert.equal(match.privacy_boundary.absolute_paths_included, false);
  assert.equal(JSON.stringify(match).includes(tempRoot), false, "scanner must not leak absolute temp path");
  assert.equal(JSON.stringify(match).includes("Zero dependencies"), false, "scanner must not include raw README body");

  const drift = scanOperatorSurface({
    readmePath: paths["README-bad.md"],
    currentStatePath: paths["CURRENT-bad.md"],
    ciPath: paths["ci-bad.yml"],
    catalogPath: paths["catalog-bad.json"],
    manifestPath: paths["manifest-bad.json"],
    statusPath: paths["status-bad.json"],
    generatedAt: "2026-06-29T00:00:01.000Z"
  });
  assert.equal(drift.aggregate.verdict, "DRIFT");
  assert.deepEqual(drift.aggregate.failure_codes, [
    "readme_try_it_missing",
    "readme_zero_dependency_missing",
    "readme_mcp_launch_missing",
    "readme_doctor_lane_missing",
    "readme_summary_command_missing",
    "status_command_surface_missing",
    "status_catalog_tool_drift",
    "status_taxonomy_incomplete",
    "catalog_manifest_count_drift",
    "ci_doctor_coverage_missing",
    "current_state_tool_count_stale",
    "current_state_doctor_lane_missing",
    "host_surface_language_missing",
    "next_action_guidance_missing"
  ]);

  const missing = scanOperatorSurface({
    readmePath: path.join(tempRoot, "missing.md"),
    currentStatePath: paths["CURRENT-good.md"],
    ciPath: paths["ci-good.yml"],
    catalogPath: paths["catalog-good.json"],
    manifestPath: paths["manifest-good.json"],
    statusPath: paths["status-good.json"],
    generatedAt: "2026-06-29T00:00:02.000Z"
  });
  assert.equal(missing.aggregate.verdict, "UNVERIFIABLE");
  assert.deepEqual(missing.aggregate.failure_codes, ["operator_surface_unjoinable"]);

  const cli = spawnSync(process.execPath, [
    path.join(here, "operator-doctor.mjs"),
    "--readme",
    paths["README-good.md"],
    "--current-state",
    paths["CURRENT-good.md"],
    "--ci",
    paths["ci-good.yml"],
    "--catalog",
    paths["catalog-good.json"],
    "--manifest",
    paths["manifest-good.json"],
    "--status",
    paths["status-good.json"]
  ], {
    cwd: path.resolve(here, ".."),
    encoding: "utf8"
  });
  assert.equal(cli.status, 0, cli.stderr || cli.stdout);
  assert.equal(JSON.parse(cli.stdout).aggregate.verdict, "MATCH");

  const summary = spawnSync(process.execPath, [
    path.join(here, "operator-doctor.mjs"),
    "--readme",
    paths["README-good.md"],
    "--current-state",
    paths["CURRENT-good.md"],
    "--ci",
    paths["ci-good.yml"],
    "--catalog",
    paths["catalog-good.json"],
    "--manifest",
    paths["manifest-good.json"],
    "--status",
    paths["status-good.json"],
    "--summary"
  ], {
    cwd: path.resolve(here, ".."),
    encoding: "utf8"
  });
  assert.equal(summary.status, 0, summary.stderr || summary.stdout);
  assert.match(summary.stdout, /Telos Operator Doctor/);
  assert.match(summary.stdout, /checks\s+14/);
  assert.match(summary.stdout, /verdict\s+MATCH/);
} finally {
  rmSync(tempRoot, { recursive: true, force: true });
}
