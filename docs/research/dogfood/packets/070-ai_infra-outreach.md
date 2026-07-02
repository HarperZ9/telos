# Action-receipt layer for agent tracing and replay

Buyer: `ai_infra`

Status: `draft_ready_not_sent`

## Draft

We are testing whether AI infrastructure teams need a proof layer that connects traces, workspace state, tool authority, verification verdicts, and durable receipts.

Pilot ask: Evaluate one agent workflow where existing traces are converted into action receipts with replay and negative-verdict handling.

Demo anchor: Agent observability-to-action-receipt proof packet.

Discovery question: When evaluating a Project Telos proof-packet workflow, how would your team answer this objection: We already have tracing and LLM observability.

Boundary: this is a hypothesis-only market probe. It does not claim market proof, scientific truth, production readiness, or unique capability.

## Evidence Intake Fields

- `buyer_role`: Named buyer role and authority path
- `budget_path`: Budget owner, procurement path, or explicit no-budget signal
- `workflow_pain`: Current workflow pain stated by the buyer
- `incumbent_stack`: Existing tools, platforms, observability, notebooks, or lab systems
- `proof_gap`: What evidence current tools fail to bind
- `acceptance_criterion`: Concrete demo condition that would justify a pilot
- `negative_disqualifier`: One result that should stop the pilot
- `trace_boundary`: Where tracing ends and action authority evidence is missing

## Acceptance Criteria

- Buyer names one workflow where a proof packet would be reviewed by a real stakeholder.
- Buyer identifies a source, action, verification, or replay gap in the current workflow.
- Buyer names a concrete artifact that would move the conversation from interest to pilot.
- Pilot candidate can ingest traces or agent logs and produce durable action receipts.

## Negative Disqualifiers

- Buyer only wants a generic chatbot, dashboard, or prose report.
- Buyer cannot name any evidence artifact that current tools fail to provide.
- Buyer expects unsupported claims of scientific discovery, market dominance, or production certification.
- Agent workflow has no accessible traces, logs, tool calls, or state receipts.

## Follow-up Schedule

- day 0: Send draft proof-packet pilot note and request a 25-minute evidence-fit call.
- day 3: Ask for one current workflow artifact or incumbent-tool screenshot equivalent.
- day 10: Close loop with a go/no-go proof-demo acceptance criterion.
