# Native control: targets and focus

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
