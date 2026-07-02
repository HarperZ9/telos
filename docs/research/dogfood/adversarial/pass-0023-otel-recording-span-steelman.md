# Pass 0023 Adversarial Steelman

Forum submit status: `UNVERIFIABLE`.

Forum submit attempt:

```text
forum submit "Dogfood pass 0023 adversarial review for isolated OpenTelemetry recording-span venv packet and Telos action-receipt bridge sketch" --max-model-calls 1 --max-seconds 30 --json
```

Observed error:

```text
submit needs a model executor. Forum is model-agnostic: pass --cmd "<model cli>" (any command, local models need no account), --chat-url <openai-compatible url> (e.g. a local Ollama server), or --api (Anthropic).
```

Forum ledger summary remained empty for the default ledger path:

```text
entries = 0
checkpoint = 0000000000000000000000000000000000000000000000000000000000000000
verified = true
```

Forum ledger verification:

```text
chain = true
deep = true
```

## Local Steelman

The strongest objection is that pass 0023 still proves a trace fixture, not the
market-facing product. A finished OpenTelemetry span can show that a runtime
observed a local event. It does not by itself prove who authorized the action,
what source state was in scope, whether policy admitted the action, whether the
action had external side effects, whether the result was verified, whether the
receipt survives trace retention, or whether compensation records are
append-only.

The temporary virtual environment also reduces blast radius but does not prove
production installation, deployment reproducibility, or cross-language parity.
The span identifiers are intentionally nonzero but not deterministic. The
fixture hash and exporter sink hash are useful evidence, but they are not a
cryptographic signature, an external anchor, or an independent review.

The action-receipt bridge is correctly labeled as a sketch. Treating it as a
runtime Telos action receipt would be an overclaim. The next pass must bind a
trace id and span id into a durable action receipt object with action intent,
command digest, source digest, policy/admission status, verification verdict,
and append-only event hash.

## Market Steelman

Competitors in agent observability and ML operations can reasonably say that
this is a tiny fixture compared with production trace collection, dashboards,
evals, prompt/version tracking, alerting, and managed retention. The Telos wedge
is not stronger because it has a span. It becomes stronger only if traces are
treated as one evidence stream inside a broader proof packet that joins:

- source provenance;
- workspace state;
- operator intent;
- policy admission;
- tool execution;
- trace evidence;
- verification verdicts;
- durable action receipts;
- append-only compensation.

Until that bridge is executable, the market gap remains a hypothesis.

## Required Next Refutation

Pass 0024 should create `TelosActionReceiptFixture/v1` and reject any packet
that:

- has a trace id but no action intent id;
- has a span id but no command digest;
- has a command digest but no source digest;
- has a completed action but no verification verdict;
- has a compensation event that mutates the original event;
- collapses a proposed action and completed action into one record;
- treats the trace span itself as the durable receipt.

Current promoted natural laws: none.
