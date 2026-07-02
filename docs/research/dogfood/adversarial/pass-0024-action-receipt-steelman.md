# Pass 0024 Adversarial Steelman

Date: 2026-07-01

Subject: durable Telos action receipt fixture and OpenTelemetry span evidence
boundary.

## Forum Receipt

Forum status:

```text
status = MATCH
tool_version = 1.12.0
role = orchestration-routing
```

Forum ledger:

```text
entries = 0
verified = true
chain = true
deep = true
```

Forum submit attempt:

```text
status = UNVERIFIABLE
error = submit needs a model executor. Forum is model-agnostic: pass --cmd "<model cli>" (any command, local models need no account), --chat-url <openai-compatible url> (e.g. a local Ollama server), or --api (Anthropic).
```

No model-backed Forum adversarial answer was produced. The following steelman
is local reasoning over the pass 0024 artifacts and must not be reported as a
Forum model verdict.

## Steelman Objections

1. The fixture is not a runtime Telos persistence layer.

The pass creates a deterministic JSON artifact and validates it. It does not
prove that a Telos host can admit, persist, retrieve, sign, anchor, compensate,
or render receipts during live tool execution.

Required countermeasure: pass 0025 should write events to an append-only JSONL
ledger and replay them from disk with mutation rejection.

2. The receipt chain is hash-bound but not independently anchored.

Event hashes, chain hashes, source digests, and the fixture seal catch local
drift, but they are not a signature, timestamp authority, transparency log, or
external notarization.

Required countermeasure: later passes need signing and anchoring adapters that
operate over canonical event bytes without changing the portable receipt
interface.

3. The single OpenTelemetry span is synthetic and in-memory.

The upstream pass proves local OTel SDK behavior in a temporary venv. It does
not prove distributed tracing, cloud collector export, trace retention, or
multi-service joins.

Required countermeasure: add exporter adapter fixtures only after local receipt
persistence is stable. Do not promote cloud trace claims before a live collector
receipt exists.

4. Proposal, admission, execution, and verification are generated together.

The fixture proves shape and hash binding, not temporal independence. A real
runtime must ensure admission occurs before execution and verification occurs
after execution.

Required countermeasure: persistence fixture should include monotonic append
order, created-at ordering checks, and rejection of collapsed proposed/completed
events.

5. Every event carries `MATCH`, which may overstate early stages.

In a real runtime, a proposed event might be unverified until execution or
review finishes. This fixture uses `MATCH` to validate the chain after the fact.

Required countermeasure: a later state-machine pass should distinguish
admission-policy match from execution-result match and review verdict match.

6. The modeled action is only a local fixture write.

Local file writes are useful for dogfood, but they do not prove handling of
email, purchase, deployment, database write, pull request, or other external
actions.

Required countermeasure: keep local writes as the first wedge, then add external
action simulators with redacted before/after refs, idempotency keys, and
compensation events.

7. The market wedge is not independently proven.

The fixture supports the hypothesis that Telos can sit above tracing and eval
tools as a durable action proof packet. It does not prove buyer urgency,
willingness to pay, adoption friction, or competitor inability.

Required countermeasure: combine this proof demo with a buyer interview script,
comparison matrix row updates, and a public demo that shows an existing OTel
trace being converted into a Telos receipt chain.

8. Redaction is represented by refs, not exercised.

The receipt uses redacted before/after references, but there is no raw payload,
redaction transform, or leak test.

Required countermeasure: add a redaction fixture that proves raw payloads stay
outside the model boundary while digest references remain verifiable.

## Pass 0024 Boundary

The strongest claim pass 0024 can make is:

```text
A deterministic local fixture can bind pass 0023 OTel span evidence into a
Telos-style append-only action receipt chain with digest references,
policy/verdict fields, receipt-is-not-span separation, and negative fixtures.
```

The pass must not claim live runtime integration, external action safety,
market adoption, theorem proof, scientific discovery, or natural-law promotion.

## Next Adversarial Tests

1. Mutate one earlier event and prove replay rejects the chain.
2. Reuse the same idempotency key for a different action and prove rejection.
3. Remove `policy.ref` from the completed event and prove rejection.
4. Remove `verification.verdict` from the completed event and prove rejection.
5. Set `trace.receipt_is_trace_span=true` and prove rejection.
6. Append a compensation event and prove the original event remains unchanged.
7. Serialize through a strict JSON loader with duplicate-key and non-finite
   rejection.
8. Run from fresh context using only ledger state and source artifact hashes.

Current promoted natural laws: none.
