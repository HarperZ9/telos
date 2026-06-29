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
    description: "Use when a host needs current Telos workbench readiness and next actions. Read-only, zero-auth, no external side effects. Returns a JSON action envelope.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.doctor",
    description: "Use before demos, listings, or agent runs to check local Telos operator-spine health. Read-only, zero-auth, no external side effects. Returns JSON check results.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.room",
    description: "Use when an agent needs the current five-flagship room summary before routing work. Read-only, zero-auth, no external side effects. Returns a JSON action envelope.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.workflow",
    description: "Use when validating the local five-flagship golden workflow from source checkouts. Read-only, zero-auth, no external side effects beyond local subprocess reads. Returns JSON receipts and verdict counts.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.catalog",
    description: "Use when a host needs the provider-neutral catalog of Project Telos MCP tools and next actions. Read-only, zero-auth, no external side effects. Returns a JSON catalog.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.server.manifest",
    description: "Use when configuring MCP clients for gather, index, forum, crucible, and telos source checkouts. Read-only, zero-auth, no external side effects. Returns a JSON server manifest.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.mcp.freshness",
    description: "Use when a host must compare loaded MCP servers against expected versions, tools, and probes. Read-only, zero-auth, no external side effects. Returns JSON MATCH, DRIFT, or UNVERIFIABLE freshness receipts.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.ci.doctor",
    description: "Use when a host needs GitHub Actions runtime, action-major, and latest five-flagship CI compatibility receipts. Read-only, zero-auth, no external side effects. Returns a JSON CI doctor register.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.presentation.doctor",
    description: "Use when a host needs five-flagship README, changelog, and brand-asset presentation parity receipts. Read-only, zero-auth, no external side effects. Returns JSON MATCH, DRIFT, or UNVERIFIABLE presentation receipts.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.accessibility.doctor",
    description: "Use when a host needs static HTML accessibility, reduced-motion, keyboard, and canvas-fallback receipts for Telos Studio surfaces. Read-only, zero-auth, no external side effects. Returns JSON MATCH, DRIFT, or UNVERIFIABLE accessibility receipts.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.performance.doctor",
    description: "Use when a host needs static Studio performance, efficiency, asset-budget, and embedding receipts. Read-only, zero-auth, no external side effects. Returns JSON MATCH, DRIFT, or UNVERIFIABLE performance receipts.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.compatibility.doctor",
    description: "Use when a host needs CLI, MCP, protocol, manifest, and integration compatibility receipts. Read-only, zero-auth, no external side effects. Returns JSON MATCH, DRIFT, or UNVERIFIABLE compatibility receipts.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.admission.telemetry",
    description: "Use when designing trace fields that keep action admission separate from verification verdicts. Read-only, zero-auth, no external side effects. Returns a JSON telemetry convention.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.context.envelope",
    description: "Use when large-workspace context needs readable source refs, budgets, and receipt chains. Read-only, zero-auth, no external side effects. Returns a JSON context-envelope convention.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.context.pack",
    description: "Use when preparing a bounded handoff packet for large-codebase agent work. Read-only, zero-auth, no external side effects. Returns a validated JSON context pack with hashes and verdicts.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.action.receipt",
    description: "Use when modeling proposed action, admission, execution, review, and compensation records. Read-only, zero-auth, no external side effects. Returns a JSON action-receipt interface.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.loop.ledger",
    description: "Use when an agent loop needs durable state across fresh contexts and bounded scheduled runs. Read-only, zero-auth, no external side effects. Returns a JSON loop-ledger convention.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.objective.monitor",
    description: "Use when checking whether proxy metrics are drifting away from real agent or build objectives. Read-only, zero-auth, no external side effects. Returns JSON objective-monitor signals.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.model.foundry",
    description: "Use when planning model-foundry work across hosted, local, open-weight, post-training, and verifier gates. Read-only, zero-auth, no external side effects. Returns a JSON model-foundry contract.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.research.seed",
    description: "Use when terse research notes need source-backed seed packets before synthesis. Read-only, zero-auth, no external side effects. Returns JSON research seeds with provenance status.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.research.thermodynamic",
    description: "Use when exploring thermodynamic or stochastic AI-chip research through public transcript evidence. Read-only, zero-auth, no external side effects. Returns a JSON research receipt with verification labels.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.rendering.research",
    description: "Use when collecting rendering leads for clustered-forward, Gaussian splatting, creative coding, and graphics demos. Read-only, zero-auth, no external side effects. Returns JSON research seeds.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.rendering.capabilities",
    description: "Use when a host must choose WebGPU, WebGL, canvas, or static rendering fallbacks for Studio surfaces. Read-only, zero-auth, no external side effects. Returns a JSON renderer capability contract.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.measurement.layers",
    description: "Use when visual, splat, lighting, dither, audio, uncertainty, or frame-budget evidence needs meters. Read-only, zero-auth, no external side effects. Returns JSON measurement layers.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.creative.engine",
    description: "Use when presenting the Telos Creative Engine across generative art, sound, typography, media, CGI, math, and physics lanes. Read-only, zero-auth, no external side effects. Returns a JSON creative-engine manifest.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.creative.kernels",
    description: "Use when deterministic creative primitives are needed for dithering, pixel sorting, plotter paths, or clustered-light bins. Read-only, zero-auth, no external side effects. Returns JSON creative kernels.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.revival.registry",
    description: "Use when deciding which older, siloed, or frozen local tools should be promoted into flagship lanes. Read-only, zero-auth, no external side effects. Returns a JSON revival registry.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.second_level.queue",
    description: "Use when assessing public-safe second-level flagship candidates before registry promotion. Read-only, zero-auth, no external side effects. Returns a JSON second-level flagship queue.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.workstation.substrate",
    description: "Use when a host needs public-safe aggregate intake for local workstation repositories and private/local lane families. Read-only, zero-auth, no external side effects. Returns a JSON workstation substrate register.",
    inputSchema: emptyInputSchema
  },
  {
    name: "telos.display.calibration",
    description: "Use when display, color, ICC/LUT, artifact refs, or measurement gates need a non-mutating calibration contract. Read-only, zero-auth, no external side effects. Returns a JSON display-calibration contract.",
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
  ["telos.mcp.freshness", ["mcp-freshness.mjs"]],
  ["telos.ci.doctor", ["ci-doctor.mjs"]],
  ["telos.presentation.doctor", ["presentation-doctor.mjs"]],
  ["telos.accessibility.doctor", ["accessibility-doctor.mjs"]],
  ["telos.performance.doctor", ["performance-doctor.mjs"]],
  ["telos.compatibility.doctor", ["compatibility-doctor.mjs"]],
  ["telos.admission.telemetry", ["admission-telemetry.mjs"]],
  ["telos.context.envelope", ["context-envelope.mjs"]],
  ["telos.context.pack", ["context-pack.mjs"]],
  ["telos.action.receipt", ["action-receipt.mjs"]],
  ["telos.loop.ledger", ["loop-ledger.mjs"]],
  ["telos.objective.monitor", ["objective-monitor.mjs"]],
  ["telos.model.foundry", ["model-foundry.mjs"]],
  ["telos.research.seed", ["research-seed.mjs"]],
  ["telos.research.thermodynamic", ["thermodynamic-ai-chip-receipt.mjs"]],
  ["telos.rendering.research", ["rendering-research.mjs"]],
  ["telos.rendering.capabilities", ["rendering-capabilities.mjs"]],
  ["telos.measurement.layers", ["measurement-layers.mjs"]],
  ["telos.creative.engine", ["creative-engine.mjs"]],
  ["telos.creative.kernels", ["creative-kernels.mjs"]],
  ["telos.revival.registry", ["revival-registry.mjs"]],
  ["telos.second_level.queue", ["second-level-flagship-queue.mjs"]],
  ["telos.workstation.substrate", ["workstation-substrate.mjs"]],
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
        serverInfo: { name: "project-telos-telos", version: "0.1.0" }
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
