import { spawnSync } from "node:child_process";
import readline from "node:readline";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const telosRoot = path.resolve(here, "..");

const protocolVersion = "2025-06-18";
const emptyInputSchema = {
  type: "object",
  properties: {},
  additionalProperties: false
};

export const tools = [
  {
    name: "telos.status",
    description: "Emit Telos shared-room readiness as a Project Telos action envelope.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.doctor",
    description: "Check Telos operator-spine readiness.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.room",
    description: "Summarize the five-flagship operator room as a Project Telos action envelope.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.workflow",
    description: "Run the local golden workflow and reconcile the five flagship receipts.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.catalog",
    description: "Return the provider-neutral Project Telos MCP tool catalog.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.server.manifest",
    description: "Return the provider-neutral MCP server launch manifest for all five flagships.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.admission.telemetry",
    description: "Return the admission decision and verification verdict telemetry convention.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.context.envelope",
    description: "Return the large-workspace context envelope convention for readable, receipt-chained agent work.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.context.pack",
    description: "Return a runnable, budgeted, receipt-backed context packet with validation for large-codebase agent handoffs.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.action.receipt",
    description: "Return the enterprise action receipt interface and append-only persistence convention.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.loop.ledger",
    description: "Return the durable loop-state ledger and bounded headless scheduled-run convention.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.objective.monitor",
    description: "Return rewardspy-style proxy-objective drift signals for agent and build workflow health.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.research.seed",
    description: "Return receipt-backed research seeds resolved from terse operator notes.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.research.thermodynamic",
    description: "Return the verified transcript-backed thermodynamic AI chip research packet.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.rendering.research",
    description: "Return receipt-backed clustered-forward and Gaussian-splatting research seeds for Telos rendering surfaces.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.rendering.capabilities",
    description: "Return the host-neutral renderer capability, fallback, privacy, and verification-gate contract for Telos Studio surfaces.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.measurement.layers",
    description: "Return runnable Telos sensor and measurement layers for visual, splat, lighting, dither, and audio evidence.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.creative.engine",
    description: "Return the Telos Creative Engine manifest for generative art, sound, typography, media, CGI, math/physics, revived local organs, and receipt-backed creative work.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.creative.kernels",
    description: "Return deterministic Telos creative kernels for dithering, pixel sorting, plotter paths, clustered light bins, and receipt-backed effects.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.revival.registry",
    description: "Return the promotion registry for older, siloed, and frozen local tools being pulled into flagship status.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.display.calibration",
    description: "Return the read-only display-calibration contract for Calibrate Pro, Quanta Color, artifact refs, and measurement gates.",
    inputSchema: emptyInputSchema
  }
];

const toolScripts = new Map([
  ["telos.status", ["status.mjs"]],
  ["telos.doctor", ["doctor.mjs"]],
  ["telos.room", ["room.mjs", "--json"]],
  ["telos.workflow", ["flagship-workflow.mjs"]],
  ["telos.catalog", ["catalog.mjs"]],
  ["telos.server.manifest", ["server-manifest.mjs"]],
  ["telos.admission.telemetry", ["admission-telemetry.mjs"]],
  ["telos.context.envelope", ["context-envelope.mjs"]],
  ["telos.context.pack", ["context-pack.mjs"]],
  ["telos.action.receipt", ["action-receipt.mjs"]],
  ["telos.loop.ledger", ["loop-ledger.mjs"]],
  ["telos.objective.monitor", ["objective-monitor.mjs"]],
  ["telos.research.seed", ["research-seed.mjs"]],
  ["telos.research.thermodynamic", ["thermodynamic-ai-chip-receipt.mjs"]],
  ["telos.rendering.research", ["rendering-research.mjs"]],
  ["telos.rendering.capabilities", ["rendering-capabilities.mjs"]],
  ["telos.measurement.layers", ["measurement-layers.mjs"]],
  ["telos.creative.engine", ["creative-engine.mjs"]],
  ["telos.creative.kernels", ["creative-kernels.mjs"]],
  ["telos.revival.registry", ["revival-registry.mjs"]],
  ["telos.display.calibration", ["display-calibration.mjs"]]
]);

function runTool(name) {
  const args = toolScripts.get(name);
  if (!args) {
    throw new Error(`unknown tool: ${name}`);
  }
  const [script, ...scriptArgs] = args;
  const result = spawnSync(process.execPath, [path.join(here, script), ...scriptArgs], {
    cwd: telosRoot,
    encoding: "utf8"
  });
  if (result.status !== 0) {
    throw new Error(result.stderr || result.stdout || `${name} failed`);
  }
  const text = result.stdout.trim();
  const structuredContent = JSON.parse(text);
  return {
    content: [{ type: "text", text }],
    structuredContent
  };
}

function result(id, value) {
  return { jsonrpc: "2.0", id, result: value };
}

function error(id, code, message) {
  return { jsonrpc: "2.0", id, error: { code, message } };
}

export function handleRequest(request) {
  const id = request.id;
  if (id === undefined && request.method?.startsWith("notifications/")) {
    return null;
  }
  try {
    if (request.method === "initialize") {
      return result(id, {
        protocolVersion,
        capabilities: { tools: {} },
        serverInfo: { name: "project-telos-telos", version: "demo" }
      });
    }
    if (request.method === "ping") {
      return result(id, {});
    }
    if (request.method === "tools/list") {
      return result(id, { tools });
    }
    if (request.method === "tools/call") {
      const name = request.params?.name;
      if (typeof name !== "string") {
        return error(id, -32602, "tools/call requires params.name");
      }
      return result(id, runTool(name));
    }
    return error(id, -32601, `method not found: ${request.method}`);
  } catch (err) {
    return error(id, -32000, err instanceof Error ? err.message : String(err));
  }
}

function main() {
  const rl = readline.createInterface({ input: process.stdin });
  rl.on("line", (line) => {
    const text = line.trim();
    if (!text) {
      return;
    }
    let response;
    try {
      response = handleRequest(JSON.parse(text));
    } catch (err) {
      response = error(null, -32700, err instanceof Error ? err.message : String(err));
    }
    if (response) {
      process.stdout.write(`${JSON.stringify(response)}\n`);
    }
  });
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main();
}
