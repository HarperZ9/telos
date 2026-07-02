# Packet 001: Agent Action Receipts

Status: `HYPOTHESIS` plus local substrate `MATCH`

## Question

Can Telos turn AI agent observability into durable action accountability without replacing existing observability stacks?

## Source Anchors

- OpenTelemetry AI agent observability: https://opentelemetry.io/blog/2025/ai-agent-observability/
- OpenTelemetry GenAI agentic systems semantic-conventions issue: https://github.com/open-telemetry/semantic-conventions-genai/issues/35
- Telos action receipt local MCP output: `project-telos.action-receipt/v1`
- Telos admission telemetry local MCP output: `project-telos.admission-telemetry/v1`

## Working Thesis

Traces explain runtime behavior; action receipts justify material actions. A trace span is necessary evidence, but not sufficient for post-hoc accountability when an agent writes files, calls APIs, spends money, changes state, or triggers human-visible workflows.

Confidence: moderate. The local Telos contract supports the distinction. Market adoption remains unproven.

## Proof Packet Shape

Minimum packet:

- `action_intent_id`
- proposed action and args hash
- admission decision
- policy/criterion reference
- execution reference
- side-effect class
- idempotency key
- redacted before/after references
- trace/span join fields
- Crucible verdict
- compensation or rollback pointer

## Adversarial Steelman

Objection: OpenTelemetry and agent observability standards may already capture enough action semantics.

Response: treat this as a falsifier. If an OTel-compatible span can preserve admission, authority, side effects, idempotency, compensation, and verifier verdicts in a durable export that survives trace retention and redaction, Telos should become a schema/profile adapter rather than a separate action layer.

## Next Proof Attempt

Create a trace fixture with one side-effecting tool call and emit:

1. raw trace packet;
2. Telos action receipt;
3. diff of fields available in trace only, receipt only, and both;
4. Crucible verdict over join integrity.

