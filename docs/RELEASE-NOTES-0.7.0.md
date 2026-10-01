# Telos 0.7.0

Telos 0.7.0 puts every native-control action behind a permission tier, signs a
receipt for every gated call, and lets the model act on accessibility-tree refs.
A model can observe what the operator grants, act where the operator grants, and
take a consequential step only after a person approves that exact step at a
terminal.

## Upgrade note

The CLI is default-deny. After upgrading, every native-control verb above T0 is
refused until the operator, at an interactive terminal:

```
telos keys init
telos grant issue --tier=T1 --verbs=* --senses=page_text,accessibility_tree --origins=https://example.com --ttl=3600
```

A T3, T4 or T5 call returns `HOLD` with a hold id. Approve it with
`telos confirm approve <hold_id>` and re-run the call with `--hold=<hold_id>`.

## Tiers

| Tier | Covers | Confirmation |
|---|---|---|
| T0 | catalog, verify a ledger | none |
| T1 | observe: tabs, page text, accessibility trees, file reads in scope | none, grant needed |
| T2 | reversible writes inside a sandbox root, with a pre-image and rollback | none, grant needed |
| T3 | clicks, fills, navigation, UIA invoke and set value | a human decision per action |
| T4 | eval, workflows, exec of an allowlisted argv | a human decision per action |
| T5 | synthetic OS input; hardware verbs stay reserved | a human decision per action, session-bound grant |

## Receipts

Each gated call appends a `telos.receipt/v1` entry to a hash-chained session
file under the Telos state directory, with ed25519 head signatures and signed
checkpoints. `telos receipts verify <session.jsonl>` checks a chain offline and
pins the local key by default. `verify.mjs` runs as one copied file.

## Removed

- Password filling and consent auto-ticking in the form filler.
- The Greenhouse adapter and workflow `adapter.*` actions.
- `tools/profile-mine.py` and `tools/device.ps1`.

## Limits

- The gate limits a model acting through Telos. It does not limit other code
  running as the operator, which can read the key or call the drivers directly.
- Target checks happen before the driver call. A symlink swapped, a file edited
  or a page navigated between the check and the act is not caught.
- The Windows key relies on the per-user ACL of `%LOCALAPPDATA%`.
- No live browser, UI Automation or device action ran in the release tests;
  drivers were fakes behind the gate.
- The WindowsAgentArena harness is a dry run. No success rate is claimed.
