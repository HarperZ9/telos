# Dogfood Pass 0026 Ledger

Date: 2026-07-01

Status: `CRUCIBLE_MATCH`.

Crucible assessment:

- thesis id: `d18deb6fe05de89d`;
- claims: `10`;
- match: `10`;
- drift: `0`;
- unverifiable: `0`;
- thesis seal: `d18deb6fe05de89db557ab515d22b39714c4632c3509dde05ca5d893e3e6a848`;
- verdict seal: `7260547a3c273952344cdbc49800037b8a00ddad1a6317e23b5205500fec699b`;
- measurement seal: `ae5993895bd40c93b3b3a3b7a122b622da574326fb3c0d3eb09cf2a2b4045b11`;
- assessment seal: `102711eda237255d21962eed118000101dab319b991714a7b20113c8fdf64c2a`;
- integrity: `seals_ok=True`, `thesis_ok=True`, `verdicts_rederive=True`.

Registry stats after pass 0026:

- theses: `23`;
- claims: `196`;
- unique claims: `196`;
- assessments: `23`;
- latest assessments: `23`;
- invalid latest assessments: `0`;
- verdicts: `MATCH=196`, `DRIFT=0`, `UNVERIFIABLE=0`.

Pass theme: bind action-receipt evidence to redacted before/after artifact refs
and a digest-only synthetic raw payload reference, then scan all model-facing
pass artifacts for raw-payload leakage.

No production DLP, cryptographic secrecy, external vault integration, live Telos
runtime integration, external write safety, buyer adoption signal, theorem proof,
scientific discovery, biological result, material result, medical result,
finance result, safety result, or natural law is promoted in this pass.

## Primary Receipt

Receipt schema:

```text
RedactionBoundaryFixtureSet/v1
```

Receipt seal:

```text
adcdfc1abcdb59427573760f4779182da9f9fde18553c633af5b08fc57f1816c
```

Validator result:

```text
status = MATCH
match = 1
drift = 0
redacted_ref_count = 2
negative_fixture_count = 8
scan_target_count = 8
raw_payload_leak_count = 0
```

## Source Binding

Source receipt:

```text
path = schemas/action-receipt-persistence-replay-pass-0025.json
sha256 = 03832d00e62c33828cbb5c6d351a10e47e5f61ac185f318044829910bdd0f293
seal = 7203957ec04350756af9cdb2d244760ebbc2c00bbc3fcc048acd7c9ff2a1a177
ledger_head_hash = 6d194872068da0e9c74d95478cca7e4f2c5a447da9a82a73be3ce9b5aa44f371
```

## Redaction Boundary

Synthetic raw payload reference:

```text
storage_boundary = TEMP_PRIVATE_NOT_COMMITTED
raw_payload_sha256 = 8c53911bf4e3763486de4c3dd43a0e1a8a587f3b172e08c322202d1b3fd66ca4
length = 85
value_in_receipts = false
value_in_model_facing_artifacts = false
```

Redacted refs:

```text
before_ref = fixtures/redacted-before-pass-0026.json
before_sha256 = 32ba5ef8fcc63fb0e7bb2f3d9a84d272693971dcc524f27021fe4ad29d6dc231
after_ref = fixtures/redacted-after-pass-0026.json
after_sha256 = e697e1ecd32c15eec3032b001596cae71021b08808db9d597bbb4a08c6bf8c9f
contains_raw_payload = false
contains_digest_ref = true
```

Action receipt redaction object:

```text
schema = ActionReceiptRedactionRef/v1
redacted_before_ref = artifact:fixtures/redacted-before-pass-0026.json
redacted_after_ref = artifact:fixtures/redacted-after-pass-0026.json
raw_payload_required_for_model = false
verification_verdict = MATCH
```

## Leak Scan

Scan targets:

```text
schemas/redaction-boundary-pass-0026.json
fixtures/redacted-before-pass-0026.json
fixtures/redacted-after-pass-0026.json
packets/036-redaction-boundary.md
adversarial/pass-0026-redaction-boundary-steelman.md
schemas/tool-receipts-pass-0026.json
crucible/pass-0026-thesis.json
crucible/pass-0026-measurements.json
```

Negative fixtures:

```text
negative-raw-payload-in-packet
negative-raw-payload-in-receipt
negative-redacted-ref-missing-digest
negative-digest-mismatch
negative-before-ref-missing
negative-after-ref-missing
negative-raw-path-committed
negative-leak-scan-target-missing
```

All negative fixtures expect validator status `REJECT`.

## Tool Substrate Receipt

Pass 0026 refreshed the tool surfaces:

| Tool | Status | Note |
| --- | --- | --- |
| Index | `MATCH` | Version 2.8.0; status and doctor available. |
| Gather | `MATCH` | Version 1.5.0; packet 036 read verified. |
| Telos | `MATCH` | Operator doctor 14/14; action receipt and loop ledger surfaced. |
| Forum | `MATCH_WITH_SUBMIT_GAP` | Status and ledger verification work; submit is `UNVERIFIABLE` because no model executor is configured. |
| Crucible | `MATCH` | Version 1.1.0; pass 0026 assessment matched. |

Gather docs receipt for packet 036:

```text
sha256=39af9c048ffb9f65128e820bd76d8ed4f836e35a6bfe73d283ab4ffe962af0c8
seal=e389dcba07e1383397e99bb58dd423884e441f274274e9e8a5d994ea5faafad3
chars=3857
```

Forum submit attempt:

```text
status=UNVERIFIABLE
error=submit needs a model executor
```

## Artifacts

| Artifact | Role |
| --- | --- |
| `tools/probe_redaction_boundary.py` | Synthetic redaction-boundary fixture generator. |
| `tools/validate_pass_0026_redaction_boundary.py` | Validator for source binding, digest refs, redacted refs, leak scan coverage, and negative fixtures. |
| `fixtures/redacted-before-pass-0026.json` | Redacted before-state fixture. |
| `fixtures/redacted-after-pass-0026.json` | Redacted after-state fixture. |
| `packets/036-redaction-boundary.md` | Human-readable redaction-boundary packet. |
| `adversarial/pass-0026-redaction-boundary-steelman.md` | Forum failure receipt plus local pass 0026 steelman. |
| `schemas/redaction-boundary-pass-0026.json` | `RedactionBoundaryFixtureSet/v1` artifact. |
| `schemas/pass-0026-redaction-boundary-validator-result.json` | Validator receipt for pass 0026. |
| `schemas/tool-receipts-pass-0026.json` | Compact Index, Gather, Telos, Forum, and Crucible receipts. |
| `crucible/pass-0026-thesis.json` | Falsifiable claims for the twenty-sixth pass. |
| `crucible/pass-0026-measurements.json` | Measurements/evidence for the twenty-sixth pass. |
| `crucible/pass-0026-report.md` | Crucible assessment report. |
| `crucible/pass-0026-run.json` | Crucible run record. |

## Primary Next Push

Build a fresh-context replay fixture that consumes only redacted artifact refs
and digest references from pass 0026.

The next proof should include:

- copy or replay redacted before/after refs into a new temp bundle;
- explicitly avoid requiring the synthetic raw payload value;
- recompute artifact hashes and verify digest continuity;
- reject any replay path that needs raw payload material;
- compare replay output against pass 0026 action receipt redaction refs;
- preserve the non-promotion boundary.

## Natural-Law Promotion

Current promoted natural laws: none.
