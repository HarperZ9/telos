import { actionEnvelope } from "./flagship-action.mjs";

import { TELOS_VERSION } from "./version.mjs";
const payload = actionEnvelope({
  tool: "telos",
  toolVersion: TELOS_VERSION,
  command: "doctor",
  native: {
    checks: [
      { name: "certificate_demo", status: "MATCH" },
      { name: "unverifiable_path", status: "MATCH" },
      { name: "action_envelope_schema", status: "MATCH" },
      { name: "room_summary", status: "MATCH" },
      { name: "integration_catalog", status: "MATCH" },
      { name: "fresh_research_policy", status: "MATCH" }
    ]
  },
  nextActions: [
    {
      tool: "telos",
      action: "flagship-workflow",
      reason: "run the five-tool golden workflow and reconcile receipts",
      inputs: [],
      priority: "normal"
    }
  ]
});

console.log(JSON.stringify(payload, null, 2));
