# Native control: targets, focus and evidence

The CLI contains real browser, Windows UI Automation and device drivers. The
`telos.native.control` MCP tool returns their catalog only; it accepts no action
arguments and does not perform an action.

## Target selection

An explicit `--match=...` is a case-sensitive substring of a page URL or title.
Exactly one inspectable page must match. Missing, ambiguous, empty or whitespace-
only matches fail before the CDP socket connects. The selection helper exposes
`TARGET_NOT_FOUND`, `TARGET_AMBIGUOUS` and `TARGET_INVALID` error codes. Error
messages do not echo page titles, URLs or the requested match.

When match is omitted, the raw CLI retains its first-inspectable-page behavior.
This compatibility is not scoped-target authorization. An integrated agent driver
must bind an exact observed target and revalidate it before acting; a substring
alone is not a durable identity or an origin policy.

## Receipt focus fields

`project-telos.native-control/v1` retains its existing fields. `background` is now
`true`, `false` or `null`, accompanied by `focus_effect`. Consumers must preserve
null rather than treat it as proof of safe background operation.

| focus_effect | background | Meaning |
| --- | --- | --- |
| none_requested | true | The known helper path does not request OS focus or keyboard input. Applies to help, browser.tabs, app.windows/tree/value and device.read/write/ls. |
| focus_requested | false | app.focus/setvalue include a UIA SetFocus call. |
| foreground_input | false | app.input/type use foreground input, or the helper explicitly reports foreground input. |
| unknown | null | Browser actuation can start Chrome; app.invoke, device.exec, scripts, workflows and unrecognized actions have effects this classification cannot establish. |

These fields classify implementation behavior, including failed requests. They
do not measure actual OS focus, assert completion, grant permission, or prove
absence of application side effects. A file write can have `none_requested` and
still change data. A result claiming `background: true` cannot upgrade an unknown
action. Foreground input is not tied atomically to a previously observed window.

## Package and validation boundary

The package includes the existing `tools/uia.ps1` and `tools/device.ps1` helpers
at the paths used by the app/device drivers. PowerShell and Windows UI Automation
are still host prerequisites. Package-layout checks do not establish an installed
runtime or universal control of native applications.

Run the bounded offline controls with:

```sh
node --test demo/native-control-contract.test.mjs demo/native-control-package.test.mjs
```

They use synthetic targets, a fake fetch/socket and npm pack dry-run with scripts
disabled. They never inspect or drive host apps. The older native-control test
module includes live debug-browser and Windows-window probes, so running that
whole module is a separate runtime action, not an offline substitute.

## Ledger integrity

New `project-telos.native-control-ledger/v1` exports add `hash_version: 2`.
The versioned hash binds `runId`, `name` and every entry field, including `step`,
`action`, `target`, `ok` and `result`. Only the derived `chain` and `chain_ok`
entry fields are excluded. Input values are snapshotted as JSON at append time.
Version 2 uses SHA-256 over the previous chain value followed by the existing
spaced, sorted-key canonical JSON of `{schema, hash_version, runId, name, entry}`.
The schema remains v1; the hash version selects the calculation.

The library and standalone `verify_packet.mjs` still read legacy exports with
an absent or explicit `hash_version: 1`. Those verify only the ordered step IDs
and results, and report `legacy-step-and-result-only`: action, target, outcome
flags and session metadata are unbound. Older verifiers cannot verify new version
2 chains and must be updated. Unknown hash versions fail verification.

`INTACT`, `ok: true` and standalone `MATCH` describe hash consistency only.
Export summaries (`count`, `integrity`, `integrity_scope`) and `chain_ok` are
derived displays, not authenticated statements. These unsigned chains do not
prove who produced the data, that it is true, that an action ran, or that the task
succeeded. A trusted external checkpoint is needed to detect a rewritten chain
or removed suffix. An empty ledger witnesses no actions.

## Browser evidence privacy

The existing v1 builder preserves source URLs, titles, selectors, artifact refs
and supplied network/console summaries. It hashes snapshot text and omits the
snapshot DOM/body, but it does not sanitize retained context or referenced
artifacts. Digests are not encryption or an anonymity guarantee.

Packets therefore default to `redaction_status: "unredacted"`. Explicit
`redactionStatus: "redacted"` requests throw; the validator reports
`redaction_unverified` for packets with that unsupported assertion. Legacy
packets carrying that assertion must be reviewed and labeled for their actual
retained data, not treated as certified redaction. The fixture CLI and MCP tool
return a synthetic, unredacted example; the raw browser CLI captures real source
context when the operator invokes it.

Keep captures and ledger exports in private operator-controlled storage. No
privacy transform or public-safe export is implemented by these helpers. The
caller still controls any file destination and sharing decision; useful source
context is retained. Shape validation does not establish semantic truth, safe
publication or privacy of arbitrary summary fields and referenced artifacts.

Run the synthetic integrity and privacy controls with:

```sh
node --test demo/native-control-ledger.test.mjs demo/browser-evidence.test.mjs
node ledger.test.mjs
node verify_packet.test.mjs
```

These controls never read a live browser, host window, profile or credential.
