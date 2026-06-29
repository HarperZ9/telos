import { createHash } from "node:crypto";
import { existsSync, readFileSync, statSync } from "node:fs";
import { spawnSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "..");

const defaults = {
  readmePath: path.join(root, "README.md"),
  currentStatePath: path.join(root, "docs", "CURRENT-STATE.md"),
  ciPath: path.join(root, ".github", "workflows", "ci.yml"),
  catalogPath: path.join(here, "integrations", "mcp-tool-catalog.json"),
  manifestPath: path.join(here, "integrations", "mcp-server-manifest.json")
};

const doctorCommands = [
  "ci-doctor",
  "presentation-doctor",
  "accessibility-doctor",
  "performance-doctor",
  "compatibility-doctor",
  "operator-doctor"
];

function sha256(text) {
  return `sha256:${createHash("sha256").update(text).digest("hex")}`;
}

function relativeLabel(filePath) {
  const relative = path.relative(root, filePath).replace(/\\/g, "/");
  return relative.startsWith("..") ? path.basename(filePath) : relative;
}

function readText(filePath) {
  const resolved = path.resolve(filePath);
  if (!existsSync(resolved) || !statSync(resolved).isFile()) {
    return { resolved, present: false, text: "" };
  }
  const text = readFileSync(resolved, "utf8");
  return { resolved, present: true, text, hash: sha256(text) };
}

function readJson(filePath) {
  const surface = readText(filePath);
  return { ...surface, value: surface.present ? JSON.parse(surface.text) : null };
}

function readStatus(statusPath) {
  if (statusPath) {
    return { surface: readJson(statusPath), subprocess: false };
  }
  const result = spawnSync(process.execPath, [path.join(here, "status.mjs")], {
    cwd: root,
    encoding: "utf8"
  });
  if (result.status !== 0) {
    return {
      surface: { resolved: path.join(here, "status.mjs"), present: false, text: "" },
      subprocess: true
    };
  }
  const text = result.stdout;
  return {
    surface: {
      resolved: path.join(here, "status.mjs"),
      present: true,
      text,
      value: JSON.parse(text),
      hash: sha256(text)
    },
    subprocess: true
  };
}

function setEqual(left, right) {
  return left.size === right.size && [...left].every((value) => right.has(value));
}

function telosToolNames(catalog) {
  return new Set((catalog.tools ?? [])
    .filter((tool) => tool.flagship === "telos")
    .map((tool) => tool.name));
}

function expectedToolCount(manifest) {
  return Object.values(manifest.servers ?? {})
    .reduce((sum, server) => sum + (server.expected_tools ?? []).length, 0);
}

function commandText(command) {
  return `node demo/${command}.mjs`;
}

function signalsFor({ readme, currentState, ci, catalog, manifest, status }) {
  const readmeText = readme.text;
  const currentText = currentState.text;
  const ciText = ci.text;
  const statusNative = status.value?.native ?? {};
  const statusCommands = new Set(statusNative.commands ?? []);
  const statusTools = new Set(statusNative.mcp_tools ?? []);
  const catalogTelosTools = telosToolNames(catalog.value ?? {});
  const toolCount = (catalog.value?.tools ?? []).length;
  return {
    readme_try_it: /## Try it/i.test(readmeText),
    readme_zero_dependency: /Zero dependencies/i.test(readmeText),
    readme_mcp_launch: /npm start/i.test(readmeText) && /node demo\/telos-mcp\.mjs/i.test(readmeText),
    readme_doctor_lanes: doctorCommands.every((command) => readmeText.includes(commandText(command))),
    readme_summary_commands: ["catalog", "server-manifest"].every((command) =>
      readmeText.includes(`${commandText(command)} --summary`)
    ),
    status_command_surface: ["run", "catalog", "server-manifest", ...doctorCommands]
      .every((command) => statusCommands.has(command)),
    status_catalog_tool_parity: setEqual(statusTools, catalogTelosTools),
    status_taxonomy: ["MATCH", "DRIFT", "UNVERIFIABLE", "ERROR"]
      .every((state) => (statusNative.statuses ?? []).includes(state)),
    catalog_manifest_count: toolCount === expectedToolCount(manifest.value ?? {}),
    ci_doctor_coverage: doctorCommands.every((command) => ciText.includes(`node demo/${command}.test.mjs`)),
    current_state_tool_count: new RegExp(`${toolCount}\\s+available tools`, "i").test(currentText),
    current_state_doctor_lanes: doctorCommands.every((command) =>
      new RegExp(command.replace("-", " "), "i").test(currentText)
    ),
    host_surface_language: ["CLI", "MCP", "IDE", "TUI", "app"].every((term) =>
      new RegExp(term, "i").test(readmeText)
    ),
    next_action_guidance: (status.value?.next_actions ?? []).some((action) => action.tool === "index")
      && (status.value?.next_actions ?? []).some((action) => action.tool === "gather")
  };
}

function metricsFor({ catalog, manifest, status }) {
  const tools = catalog.value?.tools ?? [];
  return {
    tool_count: tools.length,
    telos_tool_count: [...telosToolNames(catalog.value ?? {})].length,
    expected_tool_count: expectedToolCount(manifest.value ?? {}),
    command_count: status.value?.native?.commands?.length ?? 0,
    doctor_lane_count: doctorCommands.length,
    status_mcp_tool_count: status.value?.native?.mcp_tools?.length ?? 0
  };
}

function signalFailures(signals) {
  const mapping = {
    readme_try_it: "readme_try_it_missing",
    readme_zero_dependency: "readme_zero_dependency_missing",
    readme_mcp_launch: "readme_mcp_launch_missing",
    readme_doctor_lanes: "readme_doctor_lane_missing",
    readme_summary_commands: "readme_summary_command_missing",
    status_command_surface: "status_command_surface_missing",
    status_catalog_tool_parity: "status_catalog_tool_drift",
    status_taxonomy: "status_taxonomy_incomplete",
    catalog_manifest_count: "catalog_manifest_count_drift",
    ci_doctor_coverage: "ci_doctor_coverage_missing",
    current_state_tool_count: "current_state_tool_count_stale",
    current_state_doctor_lanes: "current_state_doctor_lane_missing",
    host_surface_language: "host_surface_language_missing",
    next_action_guidance: "next_action_guidance_missing"
  };
  return Object.entries(mapping)
    .filter(([key]) => !signals[key])
    .map(([, code]) => code);
}

export function scanOperatorSurface(options = {}) {
  const readme = readText(options.readmePath ?? defaults.readmePath);
  const currentState = readText(options.currentStatePath ?? defaults.currentStatePath);
  const ci = readText(options.ciPath ?? defaults.ciPath);
  const catalog = readJson(options.catalogPath ?? defaults.catalogPath);
  const manifest = readJson(options.manifestPath ?? defaults.manifestPath);
  const { surface: status, subprocess } = readStatus(options.statusPath);
  const surfaces = { readme, current_state: currentState, ci, catalog, manifest, status };
  if (Object.values(surfaces).some((surface) => !surface.present)) {
    return packet(options, surfaces, subprocess, {}, {}, ["operator_surface_unjoinable"], "UNVERIFIABLE");
  }
  const signals = signalsFor({ readme, currentState, ci, catalog, manifest, status });
  const failures = signalFailures(signals);
  return packet(
    options,
    surfaces,
    subprocess,
    metricsFor({ catalog, manifest, status }),
    signals,
    failures,
    failures.length === 0 ? "MATCH" : "DRIFT"
  );
}

function packet(options, surfaces, subprocess, metrics, signals, failures, verdict) {
  return {
    schema: "project-telos.operator-doctor/v1",
    tool: "telos.operator.doctor",
    generated_at: options.generatedAt ?? new Date().toISOString(),
    surfaces: Object.fromEntries(Object.entries(surfaces).map(([key, surface]) => [key, surfaceRef(surface)])),
    aggregate: {
      check_count: 14,
      passed_count: Object.values(signals).filter(Boolean).length,
      verdict,
      failure_codes: failures
    },
    privacy_boundary: privacyBoundary(subprocess),
    metrics,
    signals,
    requirements: requirements()
  };
}

function surfaceRef(surface) {
  return {
    kind: surface.value ? "json" : "text",
    present: surface.present,
    path_ref: relativeLabel(surface.resolved),
    ...(surface.hash ? { hash: surface.hash } : {})
  };
}

function privacyBoundary(subprocess) {
  return {
    raw_docs_included: false,
    raw_status_included: false,
    raw_catalog_included: false,
    raw_manifest_included: false,
    absolute_paths_included: false,
    external_fetches_performed: false,
    filesystem_writes_performed: false,
    local_subprocesses_performed: subprocess
  };
}

function requirements() {
  return [
    "README quick start exposes zero-dependency setup, summary commands, MCP launch, and doctor lanes",
    "Status, catalog, and manifest agree on the Telos command and MCP tool surface",
    "CI covers the native doctor lanes that protect presentation, accessibility, performance, compatibility, and operator discoverability",
    "Current-state docs and host language remain synchronized with the operator surface"
  ];
}

export function summary(value = scanOperatorSurface()) {
  return [
    "Telos Operator Doctor",
    `schema       ${value.schema}`,
    `tool         ${value.tool}`,
    `tools        ${value.metrics.tool_count ?? 0}`,
    `commands     ${value.metrics.command_count ?? 0}`,
    `checks       ${value.aggregate.check_count}`,
    `passed       ${value.aggregate.passed_count}`,
    `verdict      ${value.aggregate.verdict}`,
    "next         node demo/operator-doctor.mjs"
  ].join("\n") + "\n";
}

function optionValue(args, name) {
  const index = args.indexOf(name);
  const inline = args.find((arg) => arg.startsWith(`${name}=`));
  if (inline) return inline.slice(name.length + 1);
  return index === -1 ? null : args[index + 1];
}

function main() {
  const args = process.argv.slice(2);
  const packet = scanOperatorSurface({
    readmePath: optionValue(args, "--readme") ?? defaults.readmePath,
    currentStatePath: optionValue(args, "--current-state") ?? defaults.currentStatePath,
    ciPath: optionValue(args, "--ci") ?? defaults.ciPath,
    catalogPath: optionValue(args, "--catalog") ?? defaults.catalogPath,
    manifestPath: optionValue(args, "--manifest") ?? defaults.manifestPath,
    statusPath: optionValue(args, "--status") ?? null
  });
  process.stdout.write(args.includes("--summary") ? summary(packet) : `${JSON.stringify(packet, null, 2)}\n`);
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  main();
}
