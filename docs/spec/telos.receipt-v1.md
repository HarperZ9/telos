# telos.receipt/v1

Every action Telos takes, refuses, holds or dry-runs writes one receipt. Receipts
form a hash chain per session, the chain head is signed with a local ed25519 key,
and a single stdlib-only file verifies a session offline. Replay and dry run write
receipts in the same chain.

Code: `demo/receipts/`. Verifier: `demo/receipts/verify.mjs` (copy it anywhere and
run it with Node 20 or later). Conformance vectors: `docs/spec/vectors/`.

## Run it

```sh
telos keys init                          # once; refuses to overwrite an existing key
telos receipts path                      # where session files are written
telos receipts verify <session.jsonl>    # uses ./checkpoints.jsonl beside it when present
telos receipts verify <session.jsonl> --pubkey telos-ed25519.pub.json --json
node verify_packet.mjs <session.jsonl>   # the packaged verifier routes chains here
node verify.mjs <session.jsonl>          # the copied single file, no Telos install
```

Exit codes: 0 `MATCH`, 1 `DRIFT`, 2 `UNVERIFIABLE`.

## Files

| Path | Content |
|---|---|
| `<home>/keys/telos-ed25519.key` | private key, PKCS#8 PEM, mode 0600 on POSIX; the same key signs grants and hold decisions |
| `<home>/keys/telos-ed25519.pub` | public key, SPKI PEM (read by the broker) |
| `<home>/keys/telos-ed25519.pub.json` | `{schema: "telos.key/v1", alg, key_id, public_key, created_at}` |
| `<home>/receipts/<session>.jsonl` | receipts and signature records, one JSON object per line |
| `<home>/receipts/checkpoints.jsonl` | signed checkpoints for every session |
| `<home>/receipts/side/<seal>/<name>` | raw arguments, page text or frames for one receipt, mode 0600 |

`<home>` is `%LOCALAPPDATA%/Telos` on Windows, else `$XDG_STATE_HOME/telos`
(default `~/.local/state/telos`), the same root the broker keeps grants and holds
in. There is no `TELOS_HOME` override. `telos keys init` needs an interactive
terminal. `telos receipts verify` pins the local public key when no `--pubkey`
is given and the key exists, so a chain re-signed by another key is DRIFT, not a
self-asserted MATCH. On Windows the mode bits
are mostly ignored and the files rely on the per-user ACL of `%LOCALAPPDATA%`.

## Receipt fields

Common fields, written in this order: `schema` (`telos.receipt/v1`),
`hash_version` (3), `receipt_id`, `session_id`, `seq` (from 1), `prev_seal`,
`ts`, `tier` (`T0` to `T5`), `verb`, `tool`, `module` (`telos` or the module
name), `module_version`, `grant_id`, `scope_sha256`, `action_digest`, `status`,
`reason`, `executed`, `spawned[]`, the tier fields, `monitor`, `does_not_prove`,
`seal`.

`status` is one of `OK`, `REFUSED`, `HOLD`, `APPROVED`, `REJECTED`, `EXPIRED`,
`DRIFT`, `NEEDS_HUMAN`, `DRY_RUN`, `UNAVAILABLE`. A receipt with `REFUSED`,
`HOLD`, `APPROVED`, `REJECTED`, `EXPIRED`, `DRY_RUN` or `UNAVAILABLE` can never
carry `executed: true`; the writer refuses it and the verifier reports it.

`does_not_prove` is fixed per status by `demo/receipts/schema.mjs`. A caller
cannot supply or change it.

Tier fields (`TIER_FIELDS` in `schema.mjs`):

| Tier | Fields |
|---|---|
| T0 | `output_digest` |
| T1 | `sense`, `scope_match`, `observation_digest`, `redactions` |
| T2 | `sandbox_root`, `pre_image_digest`, `post_image_digest`, `rollback`, `verify_result` (`MATCH`, `DRIFT`, `UNVERIFIABLE`) |
| T3 | `hold_id`, `decision_seal`, `target_ref`, `target_fingerprint`, `resolution` (`ref`, `query`, `coordinate`), `pre_state_digest`, `post_condition`, `post_condition_result`, `focus_effect` |
| T4 | the T3 fields, plus `argv_digest`, `exit_code`, `stdout_digest`, `stderr_digest`, `duration_ms` |
| T5 | the T3 fields, plus `device_id`, `restore_state_digest`, `restore_verify_result`, `presence_check` |

Any tier may also carry `args_sha256`, `would_hold` (dry run), `replay_of` and
`replay_diff` (replay), and `side_files`. A field outside this vocabulary is
sealed and kept, and `unknownFields()` lists it, so a module can extend v1
without breaking a chain.

## Canonical form and seal

Canonical form: object keys sorted, separators `,` and `:` with no spaces, UTF-8,
and no floats. Numbers must be safe integers; anything else goes in a decimal
string. The writer refuses a float, `NaN` or `undefined` before sealing.

`seal = sha256(canonical(receipt with seal set to ""))`, lowercase hex.
`prev_seal` of seq 1 is 64 zeros. The 0.6.0 native-control ledger
(`hash_version` 2, spaced separators) stays verifiable through
`verify_packet.mjs`; new chains use `hash_version` 3.

## Action digest

`sha256(canonical({tier, verb, target_ref, target_fingerprint, args_sha256,
scope_sha256, grant_id}))`, missing fields as `null` (`demo/receipts/digest.mjs`).
A fingerprint object is reduced to the sha256 of its canonical form first.
Changing any one field changes the digest, so an approval for one element,
argument set, scope or grant cannot be borrowed by another.

## Signatures and checkpoints

A signature record is a line in the session file:

```json
{"schema": "telos.receipt-signature/v1", "session_id": "...", "seq": 12,
 "head_seal": "...", "key_id": "...", "public_key": "<base64url raw 32 bytes>",
 "sig": "<base64url ed25519>"}
```

The signature covers `canonical({schema, session_id, seq, head_seal, key_id})`.
`key_id` is the sha256 of the raw public key. The writer signs every head by
default; a fast observe loop may set `signEvery` up to 32, and the verifier
rejects a gap over 32 between signed heads.

A checkpoint is a line in `checkpoints.jsonl`, written every 256 receipts and at
session close:

```json
{"schema": "telos.receipt-checkpoint/v1", "session": "...", "seq": 256,
 "head_seal": "...", "key_id": "...", "public_key": "...", "signature": "..."}
```

The signature covers `canonical({schema, session, seq, head_seal, key_id})`.

## What the verifier checks

1. Every line parses and has a known schema.
2. Each receipt passes the structural checks, keeps one `session_id`, has the
   next `seq`, links `prev_seal` to the previous seal, and its seal re-derives.
3. Each signature names an existing seq whose seal equals `head_seal`, uses the
   chain's single key, and verifies.
4. Each checkpoint for this session verifies, names a seq that still exists, and
   names the seal at that seq.
5. Every receipt is covered by a later signed head.

Verdicts: `MATCH` when all five hold; `DRIFT` at the first break, with the line
and reason; `UNVERIFIABLE` for an empty file or an unsigned tail.

`key_trust` in the result is `pinned` when `--pubkey` was given and
`self-asserted` otherwise. A self-asserted `MATCH` only shows the chain is
internally consistent under the key it embeds: a chain re-signed end to end with
another key passes. Pin the key to rule that out.

## Dry run and replay

`dryRun(steps, {resolve, gate, chain})` resolves and gates each step and writes
`DRY_RUN` receipts with `executed: false`. It takes no execute function. The
result lists the holds, refusals and unresolved targets a real run would meet.

`replay(recording, hooks, {chain, trustedKey, startAt})` refuses a recording that
does not verify. For each recorded `OK` step it re-gates against current grants,
re-resolves the target by fingerprint, compares `pre_state_digest` and
`args_sha256`, raises a fresh hold for T3 and above, executes, and re-checks the
post-condition. Recorded hold ids and decision seals are never passed to the
approver. The first divergence stops replay with `DRIFT` and a `replay_diff` of
`{field, recorded, observed}`. A pending hold pauses replay; `startAt` resumes it.
Every replay receipt names the original seal in `replay_of`.

The `resolve`, `gate`, `preState`, `requestHold`, `execute` and `checkPost` hooks
are the broker's contracts. Their shapes are documented at the top of
`dry-run.mjs` and `replay.mjs`.

## Verified on this design

- The four negative controls (suffix removed after a checkpoint, edited entry,
  reordered entry, wrong-key signature) each return `DRIFT`.
  `demo/receipts/receipts-tamper.test.mjs`.
- 1,000 receipts with 1,000 head signatures and 4 checkpoints verify in about
  90 ms on the development workstation (target: under 1 s).

## What a MATCH does not show

A valid chain shows this install's key signed these heads. It does not show the
actions were wise, that the screen matched, or that the operator's account was
uncompromised. Anyone holding the key can re-sign a forged chain back to the last
external anchor. Without a checkpoint, a suffix cut exactly at a signed head is
not detectable. One writer per session file; concurrent writers are unsupported.
