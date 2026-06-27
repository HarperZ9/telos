import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { actionEnvelope } from "./flagship-action.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const telosRoot = path.resolve(here, "..");
const publicRoot = path.resolve(telosRoot, "..");
const asJson = process.argv.includes("--json");

const pythonTools = {
  gather: { repo: "gather", module: "gather" },
  crucible: { repo: "crucible", module: "crucible" },
  index: { repo: "index", module: "index_graph" },
  forum: { repo: "forum", module: "forum" }
};

function py(tool, args) {
  const spec = pythonTools[tool];
  const repoRoot = path.join(publicRoot, spec.repo);
  const sourcePath = path.join(repoRoot, "src");
  const code = [
    "import importlib, json, sys",
    "sys.path.insert(0, sys.argv[1])",
    "cli_args = json.loads(sys.argv[2])",
    "module_name = sys.argv[3]",
    "cli = importlib.import_module(module_name + '.cli')",
    "raise SystemExit(cli.main(cli_args))"
  ].join("; ");
  const result = spawnSync(
    "python",
    ["-c", code, sourcePath, JSON.stringify(args), spec.module],
    { cwd: repoRoot, encoding: "utf8" }
  );
  if (result.status !== 0) {
    throw new Error(`${tool} ${args.join(" ")} failed: ${result.stderr || result.stdout}`);
  }
  return JSON.parse(result.stdout);
}

function nodeJson(script) {
  const result = spawnSync(process.execPath, [path.join(here, script)], {
    cwd: telosRoot,
    encoding: "utf8"
  });
  if (result.status !== 0) {
    throw new Error(`${script} failed: ${result.stderr || result.stdout}`);
  }
  return JSON.parse(result.stdout);
}

function catalogSummary() {
  const catalog = JSON.parse(
    readFileSync(path.join(here, "integrations", "mcp-tool-catalog.json"), "utf8")
  );
  const counts = {};
  for (const tool of catalog.tools) {
    const status = tool.mcp.status;
    counts[status] = (counts[status] ?? 0) + 1;
  }
  return { counts, tools: catalog.tools.length };
}

function collectRoom() {
  const status = {
    gather: py("gather", ["status", "--json"]),
    crucible: py("crucible", ["status", "--json"]),
    index: py("index", ["status", "--json"]),
    forum: py("forum", ["status", "--json"]),
    telos: nodeJson("status.mjs")
  };
  const doctor = {
    gather: py("gather", ["doctor", "--json"]),
    crucible: py("crucible", ["doctor", "--json"]),
    index: py("index", ["doctor", "--json"]),
    forum: py("forum", ["doctor", "--json"]),
    telos: nodeJson("doctor.mjs")
  };
  const tools = Object.keys(status).map((name) => {
    const checks = doctor[name].native.checks ?? [];
    const passed = checks.filter((check) => check.status === "MATCH").length;
    return {
      tool: name,
      status: status[name].status,
      role: status[name].native.role,
      checks_passed: passed,
      checks_total: checks.length,
      next_actions: status[name].next_actions.map((action) => `${action.tool}.${action.action}`)
    };
  });
  const ready = tools.filter((tool) => tool.status === "MATCH").length;
  const checksPassed = tools.reduce((total, tool) => total + tool.checks_passed, 0);
  const checksTotal = tools.reduce((total, tool) => total + tool.checks_total, 0);
  return { ready, total: tools.length, checksPassed, checksTotal, tools, catalog: catalogSummary() };
}

function roomEnvelope(room) {
  return actionEnvelope({
    tool: "telos",
    toolVersion: "demo",
    command: "room",
    status: room.ready === room.total && room.checksPassed === room.checksTotal ? "MATCH" : "DRIFT",
    native: {
      ready: room.ready,
      total: room.total,
      checks_passed: room.checksPassed,
      checks_total: room.checksTotal,
      protocol_surfaces: room.catalog,
      tools: room.tools
    },
    nextActions: [
      {
        tool: "telos",
        action: "flagship-workflow",
        reason: "run the five-tool golden workflow when the room is ready",
        inputs: [],
        priority: "normal"
      }
    ]
  });
}

function printHuman(payload) {
  const native = payload.native;
  console.log("Project Telos Room");
  console.log(`${payload.status} ${native.ready}/${native.total} flagships ready`);
  console.log(`${native.checks_passed}/${native.checks_total} doctor checks passing`);
  console.log("");
  for (const tool of native.tools) {
    const checks = `${tool.checks_passed}/${tool.checks_total}`;
    const next = tool.next_actions.slice(0, 2).join(", ");
    console.log(`${tool.tool.padEnd(9)} ${tool.status.padEnd(12)} checks ${checks.padEnd(5)} role ${tool.role}`);
    console.log(`          next ${next}`);
  }
  console.log("");
  const surfaces = native.protocol_surfaces.counts;
  console.log(
    `protocols  available=${surfaces.available ?? 0} planned=${surfaces.planned ?? 0} ` +
    `cli-bridge=${surfaces["cli-bridge"] ?? 0}`
  );
  console.log("next      node demo/flagship-workflow.mjs");
}

const payload = roomEnvelope(collectRoom());
if (asJson) {
  console.log(JSON.stringify(payload, null, 2));
} else {
  printHuman(payload);
}
