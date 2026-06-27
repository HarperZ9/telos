import { actionEnvelope } from "./flagship-action.mjs";

const payload = actionEnvelope({
  tool: "telos",
  toolVersion: "demo",
  command: "status",
  native: {
    role: "shared-room-reconciliation",
    commands: ["room", "status", "doctor", "catalog", "run", "flagship-workflow"],
    statuses: ["MATCH", "DRIFT", "UNVERIFIABLE", "ERROR"],
    mcp_tools: [
      "telos.status",
      "telos.doctor",
      "telos.room",
      "telos.catalog",
      "telos.workflow",
      "telos.server.manifest",
      "telos.admission.telemetry",
      "telos.context.envelope",
      "telos.action.receipt"
    ],
    current_status: "source demo with 27-tool five-flagship catalog, context envelopes, action receipts, and native Telos MCP surface"
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
