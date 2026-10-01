// Telos native-control catalog: the verb list and receipt shape, with no driver.
//
// The `telos.native.control` MCP tool runs this file. It imports no browser,
// UI Automation, device, form or network driver, so the client plugin can ship
// the catalog without the actuation code. The actuation CLI is
// `demo/native-control.mjs`; it ships in the npm package and the source
// repository, and it reuses SCHEMA, makeReceipt and HELP from this module.

import { fileURLToPath } from "node:url";
import { focusSemantics } from "./native-control/focus.mjs";

export const SCHEMA = "project-telos.native-control/v1";

// Pure: build a receipt. Clock injected for testability.
export function makeReceipt(action, target, result, { ok = true, clock } = {}) {
  const at = clock ? clock() : new Date().toISOString();
  return {
    schema: SCHEMA,
    tool: "telos.native.control",
    action,
    target,
    ok,
    result,
    ...focusSemantics(action, result),
    at,
  };
}

// Every verb the CLI dispatcher accepts, by domain. A test compares this list
// with the dispatcher's `case` labels so the catalog cannot under-report what
// the npm CLI can do.
export const HELP = Object.freeze({
  usage: "node demo/native-control.mjs <browser|app|device|learn> <verb> [args]",
  delivery:
    "The actuation CLI ships in the npm package and the source repository. The client plugin carries this catalog only and cannot drive a browser, an application or the device.",
  browser: [
    "tabs",
    "navigate",
    "eval",
    "evalfile",
    "evalframe",
    "click",
    "fill",
    "focus",
    "type",
    "input",
    "upload",
    "autofill",
    "spatialfill",
    "autofillframe",
    "spatialfillframe",
    "apifetch",
    "netcap",
    "run",
    "runverify",
    "gettext",
    "waitfor",
    "screenshot",
    "snapshot-dom",
    "snapshot-text",
    "snapshot-visual",
    "snapshot-ax",
    "click-ref",
    "fill-ref",
    "select-ref",
    "focus-ref",
    "evidence",
  ],
  app: ["windows", "tree", "snapshot-ax", "resolve", "invoke", "setvalue", "focus", "value", "select", "restore", "input", "type"],
  device: ["exec", "read", "write", "ls"],
  learn: ["plan", "record", "study", "due", "mastery", "misconceptions", "status"],
  aliases: { "browser behave": "browser input" },
});

export function helpReceipt(options = {}) {
  return makeReceipt("help", null, HELP, options);
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  process.stdout.write(`${JSON.stringify(helpReceipt(), null, 2)}\n`);
}
