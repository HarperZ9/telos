# Spec: Telos Native Background Control

## Objective
Give Telos its own native, zero-external-dependency capability to control the
browser and native desktop apps in the **background**, by delivering synthetic
events into the target process rather than driving the operating system mouse
and keyboard. The operator must be able to keep using their physical cursor and
device while Telos works.

## Why
Off-the-shelf actuators fail the background requirement: OS input injection
(SendInput, computer-use, Windows-MCP) hijacks the physical cursor/keyboard, and
the Claude-in-Chrome MCP blocks whole domains (e.g. reddit.com). Telos already
frames the engine as the model's native cockpit (perceive / act / verify with
receipts); this adds the missing actuation layer on the same accountable spine.

## Requirements
- [ ] Browser control via the Chrome DevTools Protocol (CDP) over Node's built-in
      `WebSocket`/`fetch` (Node 25), no third-party packages.
- [ ] App control via Windows UI Automation through built-in PowerShell
      (`System.Windows.Automation`), no third-party packages.
- [ ] Every action is a synthetic event into the target; the OS cursor/keyboard
      is never moved. This is the defining, tested property.
- [ ] Exposed as a host-neutral Telos CLI plus an MCP/catalog tool.
- [ ] Each action emits a Telos receipt (action, target, result, verdict).
- [ ] Contract tests (`node --test`) for the pure logic; integration smokes that
      skip cleanly when no debug Chrome / target app is present.
- [ ] Files kept under 300 lines; functions focused.

## Technical Approach
A new `demo/native-control/` module tree, a `demo/native-control.mjs` CLI, a
`tools/uia.ps1` helper, and MCP/catalog/manifest/status/docs/CI wiring.

### Browser driver (CDP)
- `demo/native-control/cdp.mjs` — discover tabs via `http://127.0.0.1:9222/json`,
  attach to a tab's `webSocketDebuggerUrl` with the built-in `WebSocket`, send
  commands by incrementing id and await the matching response; surface events.
- `demo/native-control/browser.mjs` — high-level verbs built on `Runtime.evaluate`
  (primary, robust), `Input.*` (synthetic), and `Page.*`:
  `tabs`, `navigate(url)`, `eval(js)`, `click(selector)`, `type(selector,text)`,
  `getText(selector)`, `waitFor(selector,timeoutMs)`, `screenshot(path)`.
- `ensureChrome()` — probe `:9222/json/version`; if absent, relaunch Chrome with
  `--remote-debugging-port=9222 --restore-last-session` on the operator's
  existing `User Data` profile so logins persist and tabs restore. Chrome path
  and profile are resolved from the environment, never hardcoded as secrets.

### App driver (Win32 UI Automation)
- `tools/uia.ps1` — a read/act PowerShell helper using `System.Windows.Automation`:
  `windows` (top-level windows), `tree <window>` (element names/types/automationIds),
  `invoke <window> <name>` (InvokePattern), `setvalue <window> <name> <text>`
  (ValuePattern), `focus <window>`. JSON in, JSON out. UIA patterns act on the
  control directly, without moving the cursor.
- `demo/native-control/app.mjs` — Node wrapper that shells to `uia.ps1`, parses
  JSON, and returns structured results.

### Surface
- `demo/native-control.mjs` — `node demo/native-control.mjs <browser|app> <verb> [args]`,
  wraps each call in a receipt.
- `telos-mcp.mjs` + `mcp-tool-catalog.json` + `mcp-server-manifest.json` — MCP
  exposure; `status.mjs`, README, CURRENT-STATE — presentation; `ci.yml` — coverage.

## Files to Modify / Create
- `demo/native-control/cdp.mjs`, `browser.mjs`, `app.mjs` (new)
- `demo/native-control.mjs` (new CLI)
- `tools/uia.ps1` (new)
- `demo/native-control.test.mjs` (new contract + gated integration tests)
- `demo/telos-mcp.mjs`, `demo/integrations/mcp-tool-catalog.json`,
  `demo/integrations/mcp-server-manifest.json`, `demo/status.mjs`, `README.md`,
  `docs/CURRENT-STATE.md`, `.github/workflows/ci.yml` (wiring)

## Success Criteria
- [ ] `node demo/native-control.mjs browser tabs` lists open tabs (after ensureChrome).
- [ ] Driving a tab (navigate + eval + getText) succeeds with the physical cursor
      untouched (operator can move the mouse during the run).
- [ ] `node demo/native-control.mjs app windows` lists native windows; `invoke`/
      `setvalue` act on a control (verified against Notepad) without cursor motion.
- [ ] `node --test demo/native-control.test.mjs` passes; integration smokes skip
      cleanly when no debug Chrome / app is present.
- [ ] MCP/catalog/manifest/status/docs/CI updated; `git diff --check` clean; no
      credential material staged.

## Non-Goals (YAGNI)
- No headless/standalone browser management beyond attach + one relaunch helper.
- No cross-platform app control (Windows UIA only for v1).
- No recording/replay macros yet; single discrete actions with receipts.

## Verification Evidence
- `node --test demo/native-control.test.mjs` => 17/17 pass (CDP correlation, target
  selection, injection-safe expression builders, launcher args, CLI parsing,
  receipts, UIA arg/parse, the help-receipt CLI smoke, a live CDP browser smoke,
  and a live UIA `windows` smoke).
- Live browser proof: `ensureChrome()` launched a dedicated Telos automation Chrome
  on :9222; `node demo/native-control.mjs browser navigate https://example.com/`
  then `... browser gettext "h1"` returned "Example Domain" with no OS cursor or
  keyboard used.
- Live app proof: the UIA helper listed top-level windows via PowerShell
  (`InvokePattern`/`ValuePattern`), background, no cursor motion.
- Full Telos suite: 45/45 demo test files pass after wiring the read-only
  `telos.native.control` MCP discovery tool into the catalog, manifest, status,
  CURRENT-STATE, and CI.

## Security Finding (shaped the design)
Chrome 136+ ignores `--remote-debugging-port` on the default profile, and Chrome
127+ app-bound cookie encryption resists copying login cookies elsewhere. Both
are deliberate anti-malware guardrails. Telos therefore drives a DEDICATED
automation profile (its own debug port); the operator signs into the sites Telos
should act on once in that profile. Actuation stays on the local CLI; the MCP
tool exposes only the read-only capability catalog.

## Status: IMPLEMENTED
