import { actionEnvelope } from "./flagship-action.mjs";

const payload = actionEnvelope({
  tool: "telos",
  toolVersion: "demo",
  command: "status",
  native: {
    role: "shared-room-reconciliation",
    commands: ["room", "status", "doctor", "run", "flagship-workflow"],
    statuses: ["MATCH", "DRIFT", "UNVERIFIABLE", "ERROR"]
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
