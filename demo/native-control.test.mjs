import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

import {
  CdpSession,
  pickPageTarget,
  debuggerVersion,
} from "./native-control/cdp.mjs";
import {
  getTextExpression,
  clickExpression,
  setValueExpression,
  focusExpression,
  existsExpression,
  domSnapshotExpression,
  textSnapshotExpression,
  ensureChromeArgs,
  resolveChromePath,
  resolveUserDataDir,
  attach,
  navigate,
  getText,
  waitFor,
} from "./native-control/browser.mjs";
import { uiaArgs, parseUiaOutput, uiaScriptPath, windows } from "./native-control/app.mjs";
import { parseArgs, makeReceipt, SCHEMA } from "./native-control.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));

// ---- CDP correlation (no live browser) ----

function fakeSocket() {
  return { sent: [], send(s) { this.sent.push(s); }, close() { this.closed = true; }, onmessage: null };
}

test("CdpSession resolves a command with the matching response id", async () => {
  const sock = fakeSocket();
  const session = new CdpSession(sock);
  const p = session.send("Runtime.evaluate", { expression: "1+1" });
  const { id, method } = JSON.parse(sock.sent[0]);
  assert.equal(method, "Runtime.evaluate");
  sock.onmessage(JSON.stringify({ id, result: { value: 2 } }));
  assert.deepEqual(await p, { value: 2 });
});

test("CdpSession rejects on a protocol error", async () => {
  const sock = fakeSocket();
  const session = new CdpSession(sock);
  const p = session.send("Bad.method");
  const { id } = JSON.parse(sock.sent[0]);
  sock.onmessage(JSON.stringify({ id, error: { code: -32601, message: "not found" } }));
  await assert.rejects(p, /not found/);
});

test("CdpSession ignores unmatched ids and dispatches events", async () => {
  const sock = fakeSocket();
  const session = new CdpSession(sock);
  let seen = null;
  session.on("Page.loadEventFired", (params) => { seen = params; });
  sock.onmessage(JSON.stringify({ id: 999, result: { stray: true } })); // unmatched, must not throw
  sock.onmessage(JSON.stringify({ method: "Page.loadEventFired", params: { ok: 1 } }));
  assert.deepEqual(seen, { ok: 1 });
});

test("CdpSession times out when no response arrives", async () => {
  const sock = fakeSocket();
  const session = new CdpSession(sock);
  await assert.rejects(session.send("Runtime.evaluate", {}, { timeoutMs: 40 }), /timeout/);
});

// ---- target selection ----

test("pickPageTarget prefers a url/title match, falls back to first page", () => {
  const targets = [
    { type: "page", url: "https://a.com", webSocketDebuggerUrl: "ws://1" },
    { type: "page", url: "https://reddit.com/r/x", webSocketDebuggerUrl: "ws://2" },
    { type: "background_page", url: "x", webSocketDebuggerUrl: "ws://3" },
  ];
  assert.equal(pickPageTarget(targets, { match: "reddit" }).webSocketDebuggerUrl, "ws://2");
  assert.equal(pickPageTarget(targets).webSocketDebuggerUrl, "ws://1");
  assert.equal(pickPageTarget([]), null);
});

// ---- expression builders: injection-safe ----

test("expression builders embed selectors/text via JSON.stringify (injection-safe)", () => {
  const nasty = 'a"]; doEvil(); //';
  for (const expr of [getTextExpression(nasty), clickExpression(nasty), focusExpression(nasty), existsExpression(nasty)]) {
    assert.ok(expr.includes(JSON.stringify(nasty)), "selector must be JSON-escaped");
    assert.ok(!expr.includes('doEvil(); //"]'), "raw injection must not appear unescaped");
  }
  const sv = setValueExpression("#in", '"><script>x</script>');
  assert.ok(sv.includes(JSON.stringify("#in")));
  assert.ok(sv.includes(JSON.stringify('"><script>x</script>')));
});

test("getTextExpression and existsExpression query the given selector", () => {
  assert.match(getTextExpression("#title"), /querySelector\("#title"\)/);
  assert.equal(existsExpression(".foo"), '!!document.querySelector(".foo")');
});

test("snapshot expressions collect bounded page state without secrets by design", () => {
  assert.match(domSnapshotExpression(), /document\.documentElement\.outerHTML/);
  assert.match(textSnapshotExpression(123), /slice\(0,123\)/);
  assert.match(textSnapshotExpression(), /innerText/);
});

// ---- launcher args + env resolution ----

test("ensureChromeArgs carries the debug port + a dedicated profile (never the default)", () => {
  const args = ensureChromeArgs(9222, "C:/Telos/chrome-profile");
  assert.ok(args.includes("--remote-debugging-port=9222"));
  assert.ok(args.includes("--no-first-run"));
  assert.ok(args.includes("--no-default-browser-check"));
  assert.ok(args.includes("--user-data-dir=C:/Telos/chrome-profile"));
  // Chrome 136+ ignores the debug port on the default profile, so this must be a
  // dedicated dir, not the OS default Chrome "User Data".
});

test("resolveChromePath honors the env override; resolveUserDataDir uses a dedicated Telos profile", () => {
  assert.equal(resolveChromePath({ TELOS_CHROME_PATH: process.execPath }), process.execPath);
  assert.equal(resolveUserDataDir({ TELOS_CHROME_PROFILE: "X" }), "X");
  assert.equal(resolveUserDataDir({ LOCALAPPDATA: "C:/L" }), "C:/L/Telos/chrome-profile");
  assert.ok(!resolveUserDataDir({ LOCALAPPDATA: "C:/L" }).includes("Google/Chrome/User Data"));
  assert.equal(resolveUserDataDir({}), null);
});

// ---- CLI parsing + receipts ----

test("parseArgs splits domain/verb/params and --flags", () => {
  const a = parseArgs(["browser", "navigate", "https://x.com", "--match=reddit", "--port=9333"]);
  assert.equal(a.domain, "browser");
  assert.equal(a.verb, "navigate");
  assert.deepEqual(a.params, ["https://x.com"]);
  assert.deepEqual(a.flags, { match: "reddit", port: "9333" });
});

test("makeReceipt has the contract shape and marks background-true", () => {
  const r = makeReceipt("browser.click", "#go", { clicked: "#go" }, { clock: () => "T0" });
  assert.equal(r.schema, SCHEMA);
  assert.equal(r.tool, "telos.native.control");
  assert.equal(r.action, "browser.click");
  assert.equal(r.target, "#go");
  assert.equal(r.ok, true);
  assert.equal(r.background, true);
  assert.equal(r.at, "T0");
  assert.deepEqual(r.result, { clicked: "#go" });
  assert.equal(makeReceipt("x", null, { error: "e" }, { ok: false, clock: () => "T" }).ok, false);
});

// ---- UIA arg building + output parsing (no live app) ----

test("uiaArgs builds a safe PowerShell invocation", () => {
  const args = uiaArgs("C:/t/uia.ps1", "invoke", ["Untitled - Notepad", "Save"]);
  assert.deepEqual(args, [
    "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-File",
    "C:/t/uia.ps1", "invoke", "Untitled - Notepad", "Save",
  ]);
});

test("parseUiaOutput returns the last JSON line and surfaces helper errors", () => {
  assert.deepEqual(parseUiaOutput('noise\n{"ok":true,"windows":[]}\n'), { ok: true, windows: [] });
  assert.throws(() => parseUiaOutput('{"ok":false,"error":"window not found"}'), /window not found/);
  assert.throws(() => parseUiaOutput("not json at all"), /not JSON/);
  assert.throws(() => parseUiaOutput("   "), /no output/);
});

test("uiaScriptPath points at tools/uia.ps1", () => {
  assert.match(uiaScriptPath().replaceAll("\\", "/"), /tools\/uia\.ps1$/);
});

// ---- CLI smoke: help receipt ----

test("CLI prints a help receipt when no verb is given", () => {
  const cli = spawnSync(process.execPath, [path.join(here, "native-control.mjs")], { encoding: "utf8" });
  assert.equal(cli.status, 0, cli.stderr);
  const receipt = JSON.parse(cli.stdout);
  assert.equal(receipt.schema, SCHEMA);
  assert.ok(receipt.result.browser.includes("navigate"));
});

test("CLI help advertises browser evidence verbs", () => {
  const cli = spawnSync(process.execPath, [path.join(here, "native-control.mjs")], { encoding: "utf8" });
  assert.equal(cli.status, 0, cli.stderr);
  const receipt = JSON.parse(cli.stdout);
  assert.ok(receipt.result.browser.includes("snapshot-dom"));
  assert.ok(receipt.result.browser.includes("snapshot-text"));
  assert.ok(receipt.result.browser.includes("snapshot-visual"));
  assert.ok(receipt.result.browser.includes("evidence"));
});

// ---- gated integration: real Chrome via CDP (skips when no debug endpoint) ----

const chromeVersion = await debuggerVersion();

test("browser: drives a real tab via CDP without OS input", { skip: chromeVersion ? false : "no debug Chrome on :9222" }, async () => {
  const { session } = await attach({});
  try {
    await navigate(session, "data:text/html,<p id=tc>telos-ok</p>");
    await waitFor(session, "#tc", 5000);
    assert.equal(await getText(session, "#tc"), "telos-ok");
  } finally {
    session.close();
  }
});

// ---- gated integration: UIA helper responds (skips off-Windows) ----

test("app: UIA helper lists windows", { skip: process.platform === "win32" ? false : "windows-only" }, async () => {
  const res = await windows({ timeoutMs: 25000 });
  assert.equal(res.ok, true);
  assert.ok(Array.isArray(res.windows));
});
