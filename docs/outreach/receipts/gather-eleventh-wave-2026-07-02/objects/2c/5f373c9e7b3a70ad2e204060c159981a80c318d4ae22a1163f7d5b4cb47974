# Packet 034: Telos Action Receipt Fixture

Date: 2026-07-01

Status: `CRUCIBLE_MATCH`.

Pass 0024 turns the pass 0023 OpenTelemetry recording-span fixture into a
deterministic local Telos action-receipt chain. The key boundary is explicit:
the OTel span is evidence. It is not the durable action receipt.

This pass models the action receipt as an append-only chain with separate
proposal, admission, execution-completed, and verification-recorded events. It
binds source digests, command intent, policy admission, local execution refs,
trace/span identifiers, validator verdicts, and event-chain hashes into one
portable proof object.

This is still a bounded local proof. It does not prove live Telos runtime
persistence, external writes, cloud trace export, buyer demand, scientific
discovery, theorem proof, or any natural law.

## Receipt Summary

Primary schema:

```text
schemas/telos-action-receipt-fixture-pass-0024.json
```

Receipt seal:

```text
58ed4ced91f18cbab776729f49f728d47013542cfc2448865bbdb8dccd1228e3
```

Validator result:

```text
schema = Pass0024TelosActionReceiptFixtureValidatorRun/v1
status = MATCH
match = 1
drift = 0
event_count = 4
negative_fixture_count = 9
receipt_is_trace_span = false
```

Chain head:

```text
0617602eed957e0bc6c2e4a21548528f6defc542c4468433bde85df76cb51b3a
```

## Upstream Evidence

The fixture consumes three upstream pass 0023 artifacts:

| Artifact | Role | SHA-256 |
| --- | --- | --- |
| `schemas/otel-recording-span-venv-pass-0023.json` | upstream span receipt | `fc7beb76d616fd7823f0fe9a9cc879c92d00e5d7963a1e9228be89ae60486b1d` |
| `schemas/pass-0023-otel-recording-span-venv-validator-result.json` | upstream validator receipt | `cf08afa51e45e70c6f9b66f9b43f976400a3d004f71e392ebe43e78ae797eddc` |
| `packets/033-otel-recording-span-venv.md` | upstream human packet | `945054a1aed15ecffcfd46427b97dd268056a05d08997906a99faab29eed5b05` |

The upstream OpenTelemetry identifiers are carried through unchanged:

```text
trace_id_hex = aaa76491660d7a56086f69d1be94debe
span_id_hex = 1424d4ca9a6c5b58
span_ref = otel:trace/aaa76491660d7a56086f69d1be94debe/span/1424d4ca9a6c5b58
exporter_sink_hash = f2e9f33d12e261457731f6eedbe62c3c6d04d574c2c8274870da4eee0c2c2fc0
fixture_hash = b1f3b6cd1c5b81d1784b29f5f9e11dd9ab1c2849f7510de94926dca07d5e2a25
```

## Telos Contract Binding

The fixture includes a digest-bound excerpt of the Telos action receipt
contract:

```text
project-telos.action-receipt/v1
telos_contract_excerpt_sha256 = b2d08f56f2f8247c6661f81f25d5e84f916218ef132664f85365ce37a7ef5c5b
receipt_is_trace_span = false
links_to_trace_span = true
digest_references_required = true
append_only_compensation_required = true
proposed_completed_action_separation_required = true
exportable_outside_trace_retention = true
```

That digest is included as an input material in every event. This prevents the
fixture from silently changing the proof rules without changing the receipt
hashes.

## Action Chain

Action identifiers:

```text
action_id = act_dogfood_0024_001
action_intent_id = intent_dogfood_0024_001
idempotency_key = idem_dogfood_0024_001
external_request_id = local:dogfood-pass-0024-action-receipt-fixture
```

Event order:

| Order | Event Type | Result State | Event Hash |
| --- | --- | --- | --- |
| 1 | `action_proposed` | `proposed` | `2e48696173973a47b9dc6d7a15371b50a6d6121a942846ee609c3afae3fb2a8b` |
| 2 | `action_admitted` | `admitted` | `dfd5cbd9dfbec59ee45dff7b9622779b5ad5c094e709d457f4075e9af8be2fe6` |
| 3 | `execution_completed` | `completed` | `59121d18332e9171505259687e4f52d9a6eef576ad6b913093d34d208203e5e3` |
| 4 | `verification_recorded` | `completed` | `e499b57cd42f808bd9859221914719737c8ea0111d918314df24d02803f938bf` |

Every event carries:

- action intent and action id;
- idempotency key;
- `action.kind = file_write`;
- source and contract input material digests;
- `trace.receipt_is_trace_span = false`;
- OTel `span_ref`;
- policy decision and policy ref;
- verification verdict and verification ref;
- typed result state and stop reason;
- retry envelope;
- append-only persistence metadata;
- previous chain hash and write hash.

## What This Proves

Pass 0024 proves a local deterministic fixture can bind:

- OpenTelemetry runtime evidence from pass 0023;
- gathered source packet digest;
- validator result digest;
- Telos action receipt contract digest;
- action intent;
- action admission;
- execution completion;
- verification verdict;
- append-only event-chain hashes.

The validator recomputes source artifact hashes, contract digest, event hashes,
chain hashes, seal, OTel trace/span continuity, receipt-is-not-span boundary,
policy presence, verification presence, material digests, and negative fixture
coverage.

## What This Does Not Prove

This pass does not prove:

- a live Telos action receipt runtime adapter;
- durable database persistence;
- cryptographic signing or external anchoring;
- real external writes;
- cloud trace export;
- multi-agent safety;
- buyer adoption;
- any scientific result;
- any theorem proof;
- any natural law.

Those are promotion gates for later passes.

## Negative Fixtures

| Fixture | Failure Code | Expected Result |
| --- | --- | --- |
| `negative-trace-only-receipt` | `completed_action_collapsed_into_trace_span` | `REJECT` |
| `negative-action-without-command-digest` | `missing_material_digest` | `REJECT` |
| `negative-action-without-source-digest` | `missing_material_digest` | `REJECT` |
| `negative-completed-without-verification` | `verification_missing` | `REJECT` |
| `negative-policy-missing` | `policy_decision_unjoined` | `REJECT` |
| `negative-proposed-completed-collapsed` | `proposed_completed_action_collapsed` | `REJECT` |
| `negative-non-append-only-compensation` | `non_append_only_compensation` | `REJECT` |
| `negative-missing-idempotency-key` | `unjoinable_execution_span` | `REJECT` |
| `negative-trace-span-treated-as-receipt` | `completed_action_collapsed_into_trace_span` | `REJECT` |

## Market Implication

The market wedge remains a hypothesis, but the product shape is sharper after
this pass:

```text
OpenTelemetry span = runtime observation evidence.
Telos action receipt = durable operational claim.
Crucible = verification pressure.
Gather and Index = source and workspace context intake.
Forum = routing and ledger layer when an executor is configured.
```

This points away from building "another trace viewer" as the primary product.
The stronger wedge is an action proof packet that can sit over existing trace,
eval, workflow, and storage systems. Buyers with high-stakes agent actions need
portable receipts that survive trace retention, redact raw payloads, bind source
and authority, and carry explicit verification verdicts.

## Next Push

Pass 0025 should turn this fixture into a persistence adapter fixture:

- write one receipt event to a local append-only JSONL ledger;
- re-read it by `action_id`, `action_intent_id`, `event_id`, and
  `idempotency_key`;
- reject mutation of earlier events;
- append a correction or compensation event instead of editing history;
- prove the ledger can be replayed from a fresh context.

That is the next step from fixture to runtime product.

## Natural-Law Promotion

Current promoted natural laws: none.
