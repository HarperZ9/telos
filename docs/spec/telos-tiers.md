# Telos permission tiers, grants and holds

Every native-control verb runs through one gate. The gate checks the verb's tier,
a live signed grant, the grant's scope against the target as resolved at call
time, and for T3 and above a human decision on the exact action. This page is
the contract for `telos.grant/v1`, `telos.hold/v1` and the broker call.

## Tiers

| Tier | Name | Grant expiry ceiling | Confirmation |
|---|---|---|---|
| T0 | Catalog | none needed | none |
| T1 | Observe | 8 h | none per call; the grant is the consent |
| T2 | Reversible act | 4 h | none inside a sandbox root with a captured pre-image |
| T3 | Consequential act | 1 h | per action, 120 s window; a grant may set `batch` up to 10 |
| T4 | Execute and configure | 15 min | per action, 60 s window, no batching |
| T5 | Hardware | 15 min, one session | per action, 60 s window |

`demo/broker/tiers.mjs` maps every dispatcher verb to its floor. A test fails
when a verb has none. Context can only raise a floor:

- coordinates instead of a selector or ref: T3;
- a write outside every sandbox root: T3;
- a sandbox write whose pre-image cannot be captured: T3.

Refused under any grant: password, OTP and card fields; Telos state (keys,
grants, holds, receipts); terminal windows and the approval window; shell
metacharacters in `device exec`; flags that claim approval or irreversibility
(`--approve`, `--confirm`, `--yes`, `--force`, `--irreversible` and the rest);
reserved hardware verbs. The `screen` and `clipboard` senses are never implied
by a wildcard.

## Grants

Grants live in `%LOCALAPPDATA%/Telos/grants/` on Windows and
`$XDG_STATE_HOME/telos/grants/` elsewhere. `telos grant issue` writes them and
refuses without an interactive terminal. Each grant is signed with the local
ed25519 key from `telos keys init`; an edited, renamed or foreign-key grant fails
to load. A grant cannot list a verb above its own tier, use `*` above T1, run
past its tier's ceiling, or batch outside T3. T3 and above need `max_actions`.
`telos grant revoke <id>` appends a revocation; any revocation line counts.

```json
{
  "schema": "telos.grant/v1",
  "grant_id": "g_<32 hex>",
  "tier": "T3",
  "verbs": ["browser.click", "browser.fill"],
  "scope": {"origins": ["https://example.test"], "windows": [], "paths": [],
            "sandbox_roots": [], "exec_allow": [], "devices": [], "senses": []},
  "max_actions": 50,
  "batch": 1,
  "issued_at": "2026-10-01T18:00:00.000Z",
  "expires_at": "2026-10-01T19:00:00.000Z",
  "owner_ref": "owner_local",
  "scope_sha256": "<sha256 of the canonical scope>",
  "signature": {"alg": "ed25519", "key_id": "<sha256 of raw public key>", "sig": "<base64>"}
}
```

Scope entries: `windows` items are `{title}` or `{title_contains}`, optionally
with `class` or `process`. `exec_allow` items are token arrays where `*` matches
one token and a trailing `**` matches the rest. T5 synthetic input needs the
device id `input:synthetic`. A T5 grant binds to the first session that uses it.

## Holds

A T3, T4 or T5 call never runs on first arrival. The broker computes the action
digest (sha256 of the canonical form of tier, verb, target ref and fingerprint,
argument digest, scope digest and grant id), writes a hold receipt, and returns
`HOLD` with a `hold_id`. The `hold_id` is not an approval: it carries nothing
the model can use alone.

A human runs `telos confirm approve <hold_id>` at a terminal, reads the action,
and types a code shown only there. The decision is signed with the Telos key.
The model then re-issues the identical call with the `hold_id`
(`--hold=<id>` on the CLI). It runs only when:

- the decision verifies, names this hold and this digest;
- the re-resolved call produces the same digest;
- the approval window is open;
- the hold belongs to the calling session;
- no earlier call redeemed it.

Redemption claims an exclusive-create marker, so two processes cannot both
redeem. A changed argument or target gives a new hold. A rejection is durable
for its digest. Silence is never yes. While a session has an open hold, its
synthetic input and the `screen` and `clipboard` senses are suspended.

## Broker call

```js
broker.call({ verb, params, flags, hold_id, dry_run })
// -> { status, verb, tier, executed, reason, action_digest, hold_id,
//      grant_id, target_ref, receipt_seal, result }
```

`status` is one of `OK`, `REFUSED`, `HOLD`, `EXPIRED`, `REJECTED`, `DRY_RUN`,
`ERROR`. A call whose hold or dispatch receipt cannot be written does not run.

## What this does not establish

- A process running as the operator can call the drivers directly or forge
  state with the operator's key. The gate bounds a model acting through Telos.
- Target resolution reads the page origin and window list before the action;
  the page can change in between. Element refs with act-time fingerprints are a
  separate step.
- The grant `batch` field is validated, but this version raises one hold per
  action; grouped review of a batch is not built yet.
- Key files get POSIX mode 0600. On Windows they rely on the per-user
  `%LOCALAPPDATA%` ACL; no explicit ACL is set.
