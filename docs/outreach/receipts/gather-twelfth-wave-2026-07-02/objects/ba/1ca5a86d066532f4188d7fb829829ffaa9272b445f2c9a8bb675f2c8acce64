# Dogfood Pass 0024 Ledger

Date: 2026-07-01

Status: `CRUCIBLE_MATCH`.

Crucible assessment:

- thesis id: `b6b32758c2889b1c`;
- claims: `10`;
- match: `10`;
- drift: `0`;
- unverifiable: `0`;
- thesis seal: `b6b32758c2889b1cda2248dee527509c306df993a3444b16a98978b31b57ddb1`;
- verdict seal: `cab97bef341a19101155a6dee268f1a65d78b87be2b4e44f154b6fd5beac1892`;
- measurement seal: `5f053d42e59f58a01ed127aa003966924030a8da7582ea2152d35182d7f81748`;
- assessment seal: `ba2a2d3ad4bf80360d34d2b6b5de979f3261d8b111a0f481518c5edc4bf2d1b2`;
- integrity: `seals_ok=True`, `thesis_ok=True`, `verdicts_rederive=True`.

Registry stats after pass 0024:

- theses: `21`;
- claims: `176`;
- unique claims: `176`;
- assessments: `21`;
- latest assessments: `21`;
- invalid latest assessments: `0`;
- verdicts: `MATCH=176`, `DRIFT=0`, `UNVERIFIABLE=0`.

Pass theme: convert the pass 0023 OpenTelemetry recording-span fixture into a
durable local Telos action-receipt fixture chain. The span remains evidence, not
the receipt. The receipt is the append-only action claim that binds source
digests, action intent, policy, execution refs, trace/span refs, verification,
and event-chain hashes.

No live Telos runtime persistence, external write safety, cloud trace export,
buyer adoption signal, theorem proof, scientific discovery, biological result,
material result, medical result, finance result, safety result, or natural law
is promoted in this pass.

## Primary Receipt

Receipt schema:

```text
TelosActionReceiptFixtureSet/v1
```

Receipt seal:

```text
58ed4ced91f18cbab776729f49f728d47013542cfc2448865bbdb8dccd1228e3
```

Chain head:

```text
0617602eed957e0bc6c2e4a21548528f6defc542c4468433bde85df76cb51b3a
```

Validator result:

```text
status = MATCH
match = 1
drift = 0
event_count = 4
negative_fixture_count = 9
receipt_is_trace_span = false
trace_id_hex = aaa76491660d7a56086f69d1be94debe
span_id_hex = 1424d4ca9a6c5b58
```

## Upstream Binding

Source artifacts:

| Artifact | Role | SHA-256 |
| --- | --- | --- |
| `schemas/otel-recording-span-venv-pass-0023.json` | upstream span receipt | `fc7beb76d616fd7823f0fe9a9cc879c92d00e5d7963a1e9228be89ae60486b1d` |
| `schemas/pass-0023-otel-recording-span-venv-validator-result.json` | upstream validator receipt | `cf08afa51e45e70c6f9b66f9b43f976400a3d004f71e392ebe43e78ae797eddc` |
| `packets/033-otel-recording-span-venv.md` | upstream human packet | `945054a1aed15ecffcfd46427b97dd268056a05d08997906a99faab29eed5b05` |

OpenTelemetry continuity:

```text
trace_id_hex = aaa76491660d7a56086f69d1be94debe
span_id_hex = 1424d4ca9a6c5b58
span_ref = otel:trace/aaa76491660d7a56086f69d1be94debe/span/1424d4ca9a6c5b58
exporter_sink_hash = f2e9f33d12e261457731f6eedbe62c3c6d04d574c2c8274870da4eee0c2c2fc0
fixture_hash = b1f3b6cd1c5b81d1784b29f5f9e11dd9ab1c2849f7510de94926dca07d5e2a25
```

Telos contract digest:

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

## Tool Substrate Receipt

Pass 0024 refreshed the tool surfaces:

| Tool | Status | Note |
| --- | --- | --- |
| Index | `MATCH` | Version 2.8.0; status and doctor available. |
| Gather | `MATCH` | Version 1.5.0; packet 034 read verified. |
| Telos | `MATCH` | Operator doctor 14/14; action receipt and loop ledger surfaced. |
| Forum | `MATCH_WITH_SUBMIT_GAP` | Status and ledger verification work; submit is `UNVERIFIABLE` because no model executor is configured. |
| Crucible | `MATCH` | Version 1.1.0; pass 0024 assessment matched. |

Gather docs receipt for packet 034:

```text
sha256=2c5f373c9e7b3a70ad2e204060c159981a80c318d4ae22a1163f7d5b4cb47974
seal=e5f577d4667fb98aea9d6428c4c30a5663b6c96008331b145b14b6d5ef18968e
chars=7262
```

Forum submit attempt:

```text
status=UNVERIFIABLE
error=submit needs a model executor
```

## Artifacts

| Artifact | Role |
| --- | --- |
| `tools/probe_telos_action_receipt_fixture.py` | Deterministic Telos action receipt fixture generator. |
| `tools/validate_pass_0024_telos_action_receipt_fixture.py` | Validator for source hashes, contract digest, span continuity, event hashes, chain hashes, policy/verdict/material fields, and negative fixtures. |
| `packets/034-telos-action-receipt-fixture.md` | Human-readable Telos action receipt fixture packet. |
| `adversarial/pass-0024-action-receipt-steelman.md` | Forum failure receipt plus local pass 0024 steelman. |
| `schemas/telos-action-receipt-fixture-pass-0024.json` | `TelosActionReceiptFixtureSet/v1` artifact. |
| `schemas/pass-0024-telos-action-receipt-fixture-validator-result.json` | Validator receipt for pass 0024. |
| `schemas/tool-receipts-pass-0024.json` | Compact Index, Gather, Telos, Forum, and Crucible receipts. |
| `crucible/pass-0024-thesis.json` | Falsifiable claims for the twenty-fourth pass. |
| `crucible/pass-0024-measurements.json` | Measurements/evidence for the twenty-fourth pass. |
| `crucible/pass-0024-report.md` | Crucible assessment report. |
| `crucible/pass-0024-run.json` | Crucible run record. |

## Primary Next Push

Build an append-only persistence adapter fixture for `TelosActionReceiptEvent/v1`.

The next proof should include:

- JSONL append of each event;
- replay from fresh context;
- lookup by `action_id`, `action_intent_id`, `event_id`, and
  `idempotency_key`;
- rejection of mutation to any previous event;
- append-only correction or compensation event;
- strict JSON duplicate-key and non-finite rejection;
- replay seal over the whole ledger.

## Natural-Law Promotion

Current promoted natural laws: none.
