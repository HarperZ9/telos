// Telos native background control: a single CLI/MCP surface over the browser
// (CDP) and native-app (UIA) drivers, plus a full-device read/write/execute
// surface. UIA focus/input verbs can affect the operator's foreground window;
// receipts classify known focus behavior and retain unknowns.
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
import { SCHEMA, makeReceipt, helpReceipt } from "./native-control-catalog.mjs";
import * as browser from "./native-control/browser.mjs";
import * as app from "./native-control/app.mjs";
import * as device from "./native-control/device.mjs";
import * as forms from "./native-control/forms.mjs";
import * as input from "./native-control/input.mjs";
import * as runner from "./native-control/runner.mjs";
import { Ledger } from "./native-control/ledger.mjs";
import * as network from "./native-control/network.mjs";
import * as learn from "./native-control/learn.mjs";
import { defaultBroker } from "./broker/index.mjs";
import { actByRef } from "./native-control/act-ref.mjs";

export { actByRef };

// The catalog module owns the receipt shape so the MCP tool can return the
// catalog without loading any driver.
export { SCHEMA, makeReceipt };

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

// Default connection: start the dedicated debug browser if needed, then attach.
async function connectBrowser({ port, match }) {
  await browser.ensureChrome({ port });
  return browser.attach({ port, match });
}

async function runBrowser(verb, params, flags, { connect = connectBrowser } = {}) {
  const port = flags.port ? Number(flags.port) : DEFAULT_PORT;
  if (verb === "tabs") {
    return browser.tabs(port);
  }
  const { session } = await connect({ port, match: flags.match });
  try {
    switch (verb) {
      case "navigate":
        return await browser.navigate(session, params[0]);
      case "snapshot-ax": {
        // Read-only accessibility outline with element refs (DESIGN.md 5.1).
        const { newEpoch } = await import("./surface/refs.mjs");
        const { ACTIONABLE_ROLES, buildBrowserSnapshot } = await import("./surface/snapshot.mjs");
        const { saveEpoch } = await import("./surface/epochs.mjs");
        const raw = await browser.axSnapshot(session, { actionableRoles: ACTIONABLE_ROLES, maxNodes: flags.max ? Number(flags.max) : undefined });
        const target = await browser.pageState(session);
        const snapshot = buildBrowserSnapshot({ epoch: newEpoch(), targetId: flags.match ?? "page", frameId: raw.frameId,
          axNodes: raw.nodes, boxes: raw.boxes, attrs: raw.attrs });
        saveEpoch(snapshot, { target: { origin: new URL(target.url || "about:blank").origin } });
        return snapshot;
      }
      case "click-ref":
      case "fill-ref":
      case "select-ref":
      case "focus-ref":
        return await actByRef(session, verb, params);
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
      case "input":
      case "behave": {
        // `behave` is the pre-0.6.0 name for the same fixed-pace input verbs.
        const sub = params[0];
        if (sub === "click") return await input.pointerClick(session, Number(params[1]), Number(params[2]));
        if (sub === "type") return await input.typeText(session, params.slice(1).join(" "), { pauseMs: flags.pause });
        if (sub === "keys") return await input.typeKeys(session, params.slice(1).join(" "), { pauseMs: flags.pause });
        if (sub === "select") return await input.selectOption(session, params[1], params.slice(2).join(" "), { pauseMs: flags.pause });
        throw new Error(`unknown input verb: ${sub} (click|type|keys|select)`);
      }
      case "run":
        // browser run <workflow.json> [--out=ledger.json]: declarative witnessed run.
        return await runner.runFromPath(params[0], { session, out: flags.out });
      case "runverify":
        return Ledger.verify(JSON.parse(readFileSync(params[0], "utf-8")));
      case "apifetch": {
        const body = params.slice(1).join(" ");
        return await network.apiFetch(session, { url: params[0], body: body ? body : null, method: flags.method || "POST", contentType: flags.contenttype || "application/json" });
      }
      case "netcap":
        return await network.capture(session, {
          durationMs: params[0] ? Number(params[0]) : 3000,
          urlFilter: params[1] || "",
        });
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
    case "snapshot-ax": {
      const { newEpoch } = await import("./surface/refs.mjs");
      const { buildUiaSnapshot } = await import("./surface/snapshot.mjs");
      const { saveEpoch } = await import("./surface/epochs.mjs");
      const t = await app.tree(params[0], params[1]);
      const snapshot = buildUiaSnapshot({ epoch: newEpoch(), hwnd: t.hwnd, processImage: t.process,
        elements: t.elements ?? [], truncated: t.truncated, settlesAbsence: t.settlesAbsence });
      saveEpoch(snapshot, { target: { hwnd: t.hwnd, window: t.window } });
      return snapshot;
    }
    case "resolve":
      return app.resolve(params[0], params[1]);
    case "invoke":
      return app.invoke(params[0], params[1]);
    case "setvalue":
      return app.setValue(params[0], params[1], params.slice(2).join(" "));
    case "focus":
      return app.focus(params[0]);
    case "value":
      return app.value(params[0], params[1]);
    case "select":
      return app.select(params[0], params[1]);
    case "restore":
      return app.restore(params[0]);
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
      return device.exec(params);
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

// `options.connect` replaces the browser connection (tests pass a fake session).
export async function run(domain, verb, params, flags = {}, options = {}) {
  if (domain === "browser") return runBrowser(verb, params, flags, options);
  if (domain === "app") return runApp(verb, params);
  if (domain === "device") return runDevice(verb, params);
  if (domain === "learn") {
    // learn <action> --session=.. --topic=.. ... (no browser session; shells to CLI)
    const fn = learn.actions[verb];
    if (!fn) throw new Error(`unknown learn action: ${verb} (${Object.keys(learn.actions).join("|")})`);
    return fn(flags);
  }
  throw new Error(`unknown domain: ${domain} (expected browser|app|device|learn)`);
}

// The CLI reaches the drivers only through the tier gate (DESIGN.md 1.1 to
// 1.4). `--hold=<id>` re-issues a held call after a human approved it with
// `telos confirm`; `--dry-run=1` resolves and receipts without acting.
export async function gatedRun(domain, verb, params, flags = {}, { broker } = {}) {
  const port = flags.port ? Number(flags.port) : DEFAULT_PORT;
  const gate = broker ?? defaultBroker({
    executor: (v, p, f) => run(domain, v.slice(domain.length + 1), p, f),
    browser,
    app,
    port,
    notify: (h) => process.stderr.write(`telos: ${h.verb} (${h.tier}) is held as ${h.hold_id}. Approve it at an interactive terminal with \`telos confirm approve ${h.hold_id}\`, then re-run with --hold=${h.hold_id}.\n`),
  });
  return gate.call({ verb: `${domain}.${verb}`, params, flags, hold_id: flags.hold, dry_run: flags["dry-run"] === "1" });
}

async function main() {
  const { domain, verb, params, flags } = parseArgs(process.argv.slice(2));
  if (!domain || !verb) {
    process.stdout.write(`${JSON.stringify(helpReceipt(), null, 2)}\n`);
    return;
  }
  try {
    const result = await gatedRun(domain, verb, params, flags);
    const ok = result.status === "OK" || result.status === "DRY_RUN";
    process.stdout.write(`${JSON.stringify(makeReceipt(`${domain}.${verb}`, params[0] ?? null, result, { ok }), null, 2)}\n`);
    if (!ok) process.exitCode = result.status === "HOLD" || result.status === "EXPIRED" ? 2 : 1;
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
