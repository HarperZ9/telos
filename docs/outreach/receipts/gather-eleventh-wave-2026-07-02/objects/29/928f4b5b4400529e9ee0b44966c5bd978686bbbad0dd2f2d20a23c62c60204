# Dogfood Pass 0027 Ledger

Date: 2026-07-01

Status: `CRUCIBLE_MATCH`.

Crucible assessment:

- thesis id: `fb386943251381ab`;
- claims: `10`;
- match: `10`;
- drift: `0`;
- unverifiable: `0`;
- thesis seal: `fb386943251381aba18e034d90394f8289545dde740a57ff3258edb69d6ef452`;
- verdict seal: `2e5f718b2867b243dc88c8ec109db72acdeabed63f4e6633aebe6a0387189bff`;
- measurement seal: `cedeb7a50dab8d52a8f052972b516914ba7f0999e0b7539d6376133624680b82`;
- assessment seal: `c41b7c91645213cc4049ce5d940686ee90432d02c366ab7bbed3adab7617cc4f`;
- integrity: `seals_ok=True`, `thesis_ok=True`, `verdicts_rederive=True`.

Registry stats after pass 0027:

- theses: `24`;
- claims: `206`;
- unique claims: `206`;
- assessments: `24`;
- latest assessments: `24`;
- invalid latest assessments: `0`;
- verdicts: `MATCH=206`, `DRIFT=0`, `UNVERIFIABLE=0`.

Pass theme: replay pass 0026 redacted before/after refs from a fresh temp
bundle using only redacted artifact refs, SHA-256 values, and digest strings.

No production DLP, cryptographic secrecy, external vault integration, live Telos
runtime integration, external write safety, buyer adoption signal, theorem proof,
scientific discovery, biological result, material result, medical result,
finance result, safety result, or natural law is promoted in this pass.

## Primary Receipt

Receipt schema:

```text
RedactedRefReplaySet/v1
```

Receipt seal:

```text
da9d1c939bcc56eb33711537ab6cd491f8e9e70c91920d3e6a42572b8d985576
```

Validator result:

```text
status = MATCH
match = 1
drift = 0
source_sha256 = cb4233fcdafb0c35fb7b87ac78dcbc6f7dbec980614049d1fd63f08595757e80
manifest_sha256 = 47181c707049aea7573282b30cce175f51de014845ca5dd26bd1c933dd208fa3
redacted_ref_count = 2
negative_fixture_count = 9
scan_target_count = 9
sentinel_prefix_leak_count = 0
raw_payload_value_used = false
```

## Source Binding

Source receipt:

```text
path = schemas/redaction-boundary-pass-0026.json
sha256 = cb4233fcdafb0c35fb7b87ac78dcbc6f7dbec980614049d1fd63f08595757e80
schema = RedactionBoundaryFixtureSet/v1
seal = adcdfc1abcdb59427573760f4779182da9f9fde18553c633af5b08fc57f1816c
redacted_ref_count = 2
```

## Replay Contract

Replay contract:

```text
schema = RedactedRefReplayContract/v1
action_id = act_dogfood_0024_001
event_id = evt_dogfood_0026_redaction_boundary
raw_payload_value_used = false
raw_payload_material_available_to_replay = false
fresh_replay_verdict = MATCH
redacted_ref_count = 2
contract_hash = 4498487ca72ca41e69ebb1fb84a9d2991855ee4537c2b24c77198d2ebc2335f9
```

Redacted refs:

```text
before_source = fixtures/redacted-before-pass-0026.json
before_source_sha256 = 32ba5ef8fcc63fb0e7bb2f3d9a84d272693971dcc524f27021fe4ad29d6dc231
before_bundle_sha256 = 32ba5ef8fcc63fb0e7bb2f3d9a84d272693971dcc524f27021fe4ad29d6dc231
after_source = fixtures/redacted-after-pass-0026.json
after_source_sha256 = e697e1ecd32c15eec3032b001596cae71021b08808db9d597bbb4a08c6bf8c9f
after_bundle_sha256 = e697e1ecd32c15eec3032b001596cae71021b08808db9d597bbb4a08c6bf8c9f
contains_digest_ref = true
contains_unredacted_sentinel_prefix = false
source_bundle_sha_match = true
```

## Fresh Bundle

Fresh replay manifest:

```text
manifest = fixtures/redacted-ref-replay-manifest-pass-0027.json
manifest_sha256 = 47181c707049aea7573282b30cce175f51de014845ca5dd26bd1c933dd208fa3
manifest_seal = 2eb54dfc3b6974d35396c2ef597e3eec2ccb1269a88f678ceea976ad34a5f739
bundle_storage_boundary = TEMP_PRIVATE_NOT_COMMITTED
bundle_under_repo = false
file_count = 3
bundle_index_hash = 5b7ee765157d297dd17db5f61a7057c1a6a2c315bb03484346cd7d118bbdb32e
```

Raw material policy:

```text
raw_payload_value_used = false
raw_payload_material_available_to_replay = false
raw_payload_value_required = false
digest_ref_required = true
redacted_refs_required = true
scanner_token_hash = 96ec1bf4fc72002389e059a1a237017de7f9b7953a2505121bcdf106f0671ece
scanner_token_allowed_in_model_facing_artifacts = false
```

## Leak Scan

Scan targets:

```text
schemas/redacted-ref-replay-pass-0027.json
fixtures/redacted-ref-replay-manifest-pass-0027.json
fixtures/redacted-before-pass-0026.json
fixtures/redacted-after-pass-0026.json
packets/037-redacted-ref-replay.md
adversarial/pass-0027-redacted-ref-replay-steelman.md
schemas/tool-receipts-pass-0027.json
crucible/pass-0027-thesis.json
crucible/pass-0027-measurements.json
```

Negative fixtures:

```text
negative-raw-payload-value-required
negative-missing-before-ref
negative-missing-after-ref
negative-before-sha-drift
negative-after-sha-drift
negative-digest-mismatch
negative-temp-bundle-under-repo
negative-unredacted-sentinel-present
negative-source-seal-drift
```

All negative fixtures expect validator status `REJECT`.

## Tool Substrate Receipt

Pass 0027 refreshed the tool surfaces:

| Tool | Status | Note |
| --- | --- | --- |
| Index | `MATCH` | Version 2.8.0; status and doctor available. |
| Gather | `MATCH` | Version 1.5.0; packet 037 read verified. |
| Telos | `MATCH` | Operator doctor 14/14; catalog, action receipt, and loop ledger surfaced. |
| Forum | `MATCH_WITH_SUBMIT_GAP` | Status and ledger verification work; submit is `UNVERIFIABLE` because no model executor is configured. |
| Crucible | `MATCH` | Version 1.1.0; pass 0027 assessment matched. |

Gather docs receipt for packet 037:

```text
sha256=bcac13a4ae6d870fcd11ffbea4da24f35a6cdb3826c4dc802f9c6d1b1bb98d3d
seal=e8d3cb959419e51b9e1b30c9dffc81ffd4feee8107110ad608cd77cd202b680b
chars=5078
```

Forum submit attempt:

```text
status=UNVERIFIABLE
error=submit needs a model executor
```

## Artifacts

| Artifact | Role |
| --- | --- |
| `tools/probe_redacted_ref_replay.py` | Fresh-context redacted-ref replay fixture generator. |
| `tools/validate_pass_0027_redacted_ref_replay.py` | Validator for source binding, replay contract, manifest, raw material policy, scan targets, and negative fixtures. |
| `fixtures/redacted-ref-replay-manifest-pass-0027.json` | Durable manifest for the temp replay bundle. |
| `packets/037-redacted-ref-replay.md` | Human-readable redacted-ref replay packet. |
| `adversarial/pass-0027-redacted-ref-replay-steelman.md` | Forum failure receipt plus local pass 0027 steelman. |
| `schemas/redacted-ref-replay-pass-0027.json` | `RedactedRefReplaySet/v1` artifact. |
| `schemas/pass-0027-redacted-ref-replay-validator-result.json` | Validator receipt for pass 0027. |
| `schemas/tool-receipts-pass-0027.json` | Compact Index, Gather, Telos, Forum, and Crucible receipts. |
| `crucible/pass-0027-thesis.json` | Falsifiable claims for the twenty-seventh pass. |
| `crucible/pass-0027-measurements.json` | Measurements/evidence for the twenty-seventh pass. |
| `crucible/pass-0027-report.md` | Crucible assessment report. |
| `crucible/pass-0027-run.json` | Crucible run record. |

## Primary Next Push

Connect redacted replay to a browser/source evidence receipt.

The next proof should include:

- source URL or local file evidence digest;
- redacted browser/source evidence snapshot;
- action receipt event that references source evidence;
- replay from redacted refs plus source digest;
- validator rejection for source-digest drift, evidence omission, and raw source
  leakage;
- preserved non-promotion boundary.

## Natural-Law Promotion

Current promoted natural laws: none.
