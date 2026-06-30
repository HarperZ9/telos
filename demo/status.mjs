import { actionEnvelope } from "./flagship-action.mjs";

const payload = actionEnvelope({
  tool: "telos",
  toolVersion: "0.1.0",
  command: "status",
  native: {
    role: "shared-room-reconciliation",
    commands: ["room", "status", "doctor", "catalog", "server-manifest", "run", "flagship-workflow", "model-foundry", "mcp-freshness", "ci-doctor", "ci-triage", "presentation-doctor", "accessibility-doctor", "performance-doctor", "compatibility-doctor", "operator-doctor", "revival-registry", "second-level-flagship-queue", "workstation-substrate", "display-calibration"],
    statuses: ["MATCH", "DRIFT", "UNVERIFIABLE", "ERROR"],
    mcp_tools: [
      "telos.status",
      "telos.doctor",
      "telos.room",
      "telos.catalog",
      "telos.workflow",
      "telos.server.manifest",
      "telos.mcp.freshness",
      "telos.ci.doctor",
      "telos.ci.triage",
      "telos.presentation.doctor",
      "telos.accessibility.doctor",
      "telos.performance.doctor",
      "telos.compatibility.doctor",
      "telos.operator.doctor",
      "telos.admission.telemetry",
      "telos.context.envelope",
      "telos.context.pack",
      "telos.action.receipt",
      "telos.loop.ledger",
      "telos.objective.monitor",
      "telos.model.foundry",
      "telos.research.seed",
      "telos.research.thermodynamic",
      "telos.rendering.research",
      "telos.rendering.capabilities",
      "telos.measurement.layers",
      "telos.creative.engine",
      "telos.creative.kernels",
      "telos.revival.registry",
      "telos.second_level.queue",
      "telos.workstation.substrate",
      "telos.display.calibration",
      "telos.native.control"
    ],
    current_status: "0.1.0 source registry package with 61-tool five-flagship catalog, CI doctor, CI triage, presentation doctor, accessibility doctor, performance doctor, compatibility doctor, operator doctor, context envelopes, context packs, action receipts, loop ledger, objective monitoring, model foundry, MCP freshness, research seeds, transcript-backed thermodynamic research, rendering research, rendering capabilities, measurement layers, creative engine, creative kernels, revival registry, second-level queue, workstation substrate, display calibration, native background control of browser and apps, and native Telos MCP surface"
  },
  nextActions: [
    {
      tool: "index",
      action: "map",
      reason: "refresh workspace structure before reconciliation",
      inputs: [],
      priority: "normal"
    },
    {
      tool: "gather",
      action: "docs",
      reason: "attach source receipts for the next witnessed room event",
      inputs: [],
      priority: "normal"
    }
  ]
});

console.log(JSON.stringify(payload, null, 2));
