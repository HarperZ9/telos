// Telos native background control: a single CLI/MCP surface over the browser
// (CDP) and native-app (UIA) drivers, plus a full-device read/write/execute
// surface. Every action is a synthetic event into the target process, so the
// operator's physical cursor and keyboard stay free.
//
//   node demo/native-control.mjs browser <verb> [args] [--match=..] [--port=..]
//   node demo/native-control.mjs app <verb> [args]
//   node demo/native-control.mjs device <verb> [args]
//
// Three paths to a target, weakest coupling first:
//   - app (UIA): drives controls inside any desktop process via UI Automation
//     patterns (invoke/value) and, where a pattern cannot reach a control,
//     foreground key synthesis (input/type). No debug port, no CDP -- this is
//     the path that drives a normally-launched, authenticated browser.
//   - browser (CDP): the higher-fidelity path, requires a debug-enabled browser.
//   - device: OS-level execute/read/write/list -- the remote-desktop R/W/X
//     surface, for anything that is not a UI control.

import { writeFileSync, readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { DEFAULT_PORT } from "./native-control/cdp.mjs";
import * as browser from "./native-control/browser.mjs";
import * as app from "./native-control/app.mjs";
import * as device from "./native-control/device.mjs";
import * as captcha from "./native-control/captcha.mjs";
import * as forms from "./native-control/forms.mjs";
import * as behave from "./native-control/behave.mjs";

export const SCHEMA = "project-telos.native-control/v1";

// Pure: split argv into domain/verb/params and flags.
export function parseArgs(argv) {
  const flags = {};
  const rest = [];
  for (const a of argv) {
    const m = /^--([^=]+)=(.*)$/.exec(a);
    if (m) flags[m[1]] = m[2];
    else if (a === "--") continue;
    else rest.push(a);
  }
  return { domain: rest[0], verb: rest[1], params: rest.slice(2), flags };
}

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
    background: true, // no OS cursor/keyboard used
    at,
  };
}

async function runBrowser(verb, params, flags) {
  const port = flags.port ? Number(flags.port) : DEFAULT_PORT;
  if (verb === "tabs") {
    return browser.tabs(port);
  }
  await browser.ensureChrome({ port });
  const { session } = await browser.attach({ port, match: flags.match });
  try {
    switch (verb) {
      case "navigate":
        return await browser.navigate(session, params[0]);
      case "eval":
        return await browser.evalJs(session, params[0]);
      case "evalfile":
        return await browser.evalJs(session, readFileSync(params[0], "utf-8"));
      case "click":
        return await browser.click(session, params[0]);
      case "fill":
        return await browser.setValue(session, params[0], params.slice(1).join(" "));
      case "focus":
        return await browser.evalJs(session, browser.focusExpression(params[0]));
      case "type":
        return await browser.insertText(session, params.join(" "));
      case "gettext":
        return await browser.getText(session, params[0]);
      case "upload":
        return await browser.uploadFile(session, params[0], params[1]);
      case "captcha":
        return await captcha.solve(session, { prompt: flags.prompt || "" });
      case "autofill": {
        // browser autofill: injects a profile JSON (arg) or the candidate-profile-
        // derived shape, fills every field on the page (any site / auth flow).
        const profile = params[0] ? JSON.parse(params.join(" ")) : await forms.defaultProfile();
        return await forms.fill(session, profile);
      }
      case "spatialfill": {
        // browser spatialfill: label-by-rect association for obfuscated React ATS.
        const profile = params[0] ? JSON.parse(params.join(" ")) : await forms.defaultProfile();
        return await forms.spatialFill(session, profile);
      }
      case "evalframe":
        // browser evalframe <frameUrlMatch> <jsfile>: eval inside a cross-origin iframe.
        return await browser.evalInFrame(session, params[0], readFileSync(params[1], "utf-8"));
      case "autofillframe": {
        // browser autofillframe <frameUrlMatch>: generic autofill inside the iframe form.
        const profile = params[1] ? JSON.parse(params.slice(1).join(" ")) : await forms.defaultProfile();
        return await browser.evalInFrame(session, params[0], forms.fillExpression(profile));
      }
      case "spatialfillframe": {
        const profile = params[1] ? JSON.parse(params.slice(1).join(" ")) : await forms.defaultProfile();
        const r = await browser.evalInFrame(session, params[0], forms.SPATIAL_FILL_JS(JSON.stringify(profile)));
        return r.value;
      }
      case "behave": {
        const sub = params[0];
        if (sub === "stealth") return await behave.stealth(session);
        if (sub === "warmup") return await behave.warmup(session);
        if (sub === "click") return await behave.humanClick(session, Number(params[1]), Number(params[2]));
        if (sub === "type") return await behave.humanType(session, params.slice(1).join(" "));
        if (sub === "select") return await behave.selectpick(session, params[1], params.slice(2).join(" "));
        throw new Error(`unknown behave verb: ${sub} (stealth|warmup|click|type|select)`);
      }
      case "waitfor":
        return await browser.waitFor(session, params[0], params[1] ? Number(params[1]) : undefined);
      case "screenshot": {
        const data = await browser.screenshot(session);
        const path = params[0] || "telos-screenshot.png";
        writeFileSync(path, Buffer.from(data, "base64"));
        return { path, bytes: Buffer.from(data, "base64").length };
      }
      case "snapshot-dom":
        return { html: await browser.evalJs(session, browser.domSnapshotExpression()) };
      case "snapshot-text":
        return { text: await browser.evalJs(session, browser.textSnapshotExpression(params[0] ? Number(params[0]) : 20000)) };
      case "snapshot-visual": {
        const data = await browser.screenshot(session);
        const path = params[0] || "telos-screenshot.png";
        writeFileSync(path, Buffer.from(data, "base64"));
        return { path, bytes: Buffer.from(data, "base64").length };
      }
      case "evidence": {
        const before = await browser.pageState(session);
        const { makeBrowserEvidencePacket, makeUnavailableSummary, digestRef } = await import("./native-control/evidence.mjs");
        return makeBrowserEvidencePacket({
          mode: flags.mode || "research-capture",
          action: { kind: "browser.evidence", argsHash: digestRef("args", JSON.stringify(params)) },
          sessionRef: `browser-session:cdp-${port}`,
          actionReceiptRef: null,
          before,
          after: before,
          networkSummary: makeUnavailableSummary("network", "collector-not-attached"),
          consoleSummary: makeUnavailableSummary("console", "collector-not-attached"),
          verification: { verdict: "MATCH", ref: "telos:native-control-evidence" },
        });
      }
      default:
        throw new Error(`unknown browser verb: ${verb}`);
    }
  } finally {
    session.close();
  }
}

async function runApp(verb, params) {
  switch (verb) {
    case "windows":
      return app.windows();
    case "tree":
      return app.tree(params[0], params[1]);
    case "invoke":
      return app.invoke(params[0], params[1]);
    case "setvalue":
      return app.setValue(params[0], params[1], params.slice(2).join(" "));
    case "focus":
      return app.focus(params[0]);
    case "value":
      return app.value(params[0], params[1]);
    case "input":
      return app.input(params.join(" "));
    case "type":
      return app.typeText(params.join(" "));
    default:
      throw new Error(`unknown app verb: ${verb}`);
  }
}

async function runDevice(verb, params) {
  switch (verb) {
    case "exec":
      return device.exec(params.join(" "));
    case "read":
      return device.read(params[0], params[1] ? Number(params[1]) : undefined);
    case "write":
      return device.write(params[0], params.slice(1).join(" "));
    case "ls":
      return device.ls(params[0]);
    default:
      throw new Error(`unknown device verb: ${verb}`);
  }
}

export async function run(domain, verb, params, flags = {}) {
  if (domain === "browser") return runBrowser(verb, params, flags);
  if (domain === "app") return runApp(verb, params);
  if (domain === "device") return runDevice(verb, params);
  throw new Error(`unknown domain: ${domain} (expected browser|app|device)`);
}

async function main() {
  const { domain, verb, params, flags } = parseArgs(process.argv.slice(2));
  if (!domain || !verb) {
    process.stdout.write(
          `${JSON.stringify(
        makeReceipt("help", null, {
          usage: "node demo/native-control.mjs <browser|app|device> <verb> [args]",
          browser: [
            "tabs",
            "navigate",
            "eval",
            "click",
            "fill",
            "focus",
            "type",
            "gettext",
            "waitfor",
            "screenshot",
            "snapshot-dom",
            "snapshot-text",
            "snapshot-visual",
            "evidence",
          ],
          app: ["windows", "tree", "invoke", "setvalue", "focus", "value", "input", "type"],
          device: ["exec", "read", "write", "ls"],
        }),
        null,
        2,
      )}\n`,
    );
    return;
  }
  try {
    const result = await run(domain, verb, params, flags);
    process.stdout.write(`${JSON.stringify(makeReceipt(`${domain}.${verb}`, params[0] ?? null, result), null, 2)}\n`);
  } catch (err) {
    process.stdout.write(
      `${JSON.stringify(makeReceipt(`${domain}.${verb}`, params[0] ?? null, { error: err.message }, { ok: false }), null, 2)}\n`,
    );
    process.exitCode = 1;
  }
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  main();
}
