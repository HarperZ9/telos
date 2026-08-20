// High-level background browser control built on the CDP client.
//
// Verbs interact with the page through `Runtime.evaluate` and CDP's `Input`
// domain, both of which dispatch synthetic events into the renderer. The
// operating system pointer and keyboard are never used, so the operator can
// keep working on their machine while these run.

import { spawn } from "node:child_process";
import { existsSync } from "node:fs";
import {
  CdpSession,
  DEFAULT_PORT,
  debuggerVersion,
  listTargets,
  pickPageTarget,
} from "./cdp.mjs";

// ---- Pure builders (unit-testable, injection-safe via JSON.stringify) ----

export function getTextExpression(selector) {
  return `(()=>{const el=document.querySelector(${JSON.stringify(
    selector,
  )});return el?(el.innerText??el.textContent??""):null;})()`;
}

export function clickExpression(selector) {
  return `(()=>{const el=document.querySelector(${JSON.stringify(
    selector,
  )});if(!el)return false;el.scrollIntoView({block:"center"});el.click();return true;})()`;
}

export function setValueExpression(selector, text) {
  const sel = JSON.stringify(selector);
  const val = JSON.stringify(text);
  return `(()=>{const el=document.querySelector(${sel});if(!el)return false;const proto=el instanceof HTMLTextAreaElement?HTMLTextAreaElement.prototype:HTMLInputElement.prototype;const setter=Object.getOwnPropertyDescriptor(proto,"value");if(setter&&setter.set&&(el instanceof HTMLInputElement||el instanceof HTMLTextAreaElement)){setter.set.call(el,${val});}else{el.focus();el.textContent=${val};}el.dispatchEvent(new Event("input",{bubbles:true}));el.dispatchEvent(new Event("change",{bubbles:true}));return true;})()`;
}

export function focusExpression(selector) {
  return `(()=>{const el=document.querySelector(${JSON.stringify(
    selector,
  )});if(!el)return false;el.focus();el.scrollIntoView({block:"center"});return document.activeElement===el;})()`;
}

export function existsExpression(selector) {
  return `!!document.querySelector(${JSON.stringify(selector)})`;
}

export function domSnapshotExpression() {
  return '(()=>document.documentElement ? document.documentElement.outerHTML : "")()';
}

export function textSnapshotExpression(limit = 20000) {
  return `(()=>((document.body&&document.body.innerText)||"").slice(0,${Number(limit)}))()`;
}

// Build the argv that launches Chrome with the remote-debugging port on a
// DEDICATED Telos automation profile. Chrome 136+ deliberately ignores
// --remote-debugging-port on the default profile (anti-malware), so a separate
// --user-data-dir is required. A dedicated profile also keeps the operator's
// main browser and cursor entirely theirs while Telos drives this instance.
export function ensureChromeArgs(port, userDataDir) {
  const args = [
    `--remote-debugging-port=${port}`,
    "--no-first-run",
    "--no-default-browser-check",
  ];
  if (userDataDir) args.push(`--user-data-dir=${userDataDir}`);
  return args;
}

export function resolveChromePath(env = process.env) {
  const candidates = [
    env.TELOS_CHROME_PATH,
    `${env.ProgramFiles || "C:/Program Files"}/Google/Chrome/Application/chrome.exe`,
    `${env["ProgramFiles(x86)"] || "C:/Program Files (x86)"}/Google/Chrome/Application/chrome.exe`,
    `${env.LOCALAPPDATA || ""}/Google/Chrome/Application/chrome.exe`,
  ].filter(Boolean);
  return candidates.find((p) => existsSync(p)) || null;
}

// The dedicated Telos automation profile. Never the OS default Chrome profile
// (which cannot be debugged). Override with TELOS_CHROME_PROFILE. The operator
// signs into the sites they want Telos to act on once in this profile.
export function resolveUserDataDir(env = process.env) {
  if (env.TELOS_CHROME_PROFILE) return env.TELOS_CHROME_PROFILE;
  if (env.LOCALAPPDATA) return `${env.LOCALAPPDATA}/Telos/chrome-profile`;
  return null;
}

// ---- Launcher + connection ----

export async function ensureChrome({
  port = DEFAULT_PORT,
  env = process.env,
  wait = 800,
} = {}) {
  const existing = await debuggerVersion(port);
  if (existing) return { launched: false, version: existing };
  const chrome = resolveChromePath(env);
  if (!chrome) throw new Error("Chrome executable not found; set TELOS_CHROME_PATH");
  const args = ensureChromeArgs(port, resolveUserDataDir(env));
  const child = spawn(chrome, args, { detached: true, stdio: "ignore" });
  child.unref();
  // Poll for the endpoint to come up.
  const deadline = Date.now() + 15000;
  for (;;) {
    await new Promise((r) => setTimeout(r, wait));
    const v = await debuggerVersion(port);
    if (v) return { launched: true, version: v, pid: child.pid };
    if (Date.now() > deadline) throw new Error("Chrome debug endpoint did not come up");
  }
}

export async function attach({ port = DEFAULT_PORT, match } = {}) {
  const targets = await listTargets(port);
  const target = pickPageTarget(targets, { match });
  if (!target) throw new Error("No inspectable page target found");
  const session = await CdpSession.connect(target.webSocketDebuggerUrl);
  await session.send("Runtime.enable");
  await session.send("Page.enable");
  return { session, target };
}

// ---- Verbs (return plain results; caller wraps in a receipt) ----

async function evaluate(session, expression, { awaitPromise = false } = {}) {
  const res = await session.send("Runtime.evaluate", {
    expression,
    returnByValue: true,
    awaitPromise,
  });
  if (res.exceptionDetails) {
    throw new Error(`page eval failed: ${res.exceptionDetails.text}`);
  }
  return res.result?.value;
}

export async function tabs(port = DEFAULT_PORT) {
  const targets = await listTargets(port);
  return targets
    .filter((t) => t.type === "page")
    .map((t) => ({ id: t.id, title: t.title, url: t.url }));
}

export async function navigate(session, url) {
  await session.send("Page.navigate", { url });
  return { url };
}

export async function evalJs(session, expression) {
  return evaluate(session, expression, { awaitPromise: true });
}

export async function pageState(session) {
  const [url, title, text, html] = await Promise.all([
    evaluate(session, "location.href"),
    evaluate(session, "document.title"),
    evaluate(session, textSnapshotExpression()),
    evaluate(session, domSnapshotExpression()),
  ]);
  return { url: url || "", title: title || "", text: text || "", html: html || "" };
}

export async function getText(session, selector) {
  return evaluate(session, getTextExpression(selector));
}

export async function click(session, selector) {
  const ok = await evaluate(session, clickExpression(selector));
  if (!ok) throw new Error(`click target not found: ${selector}`);
  return { clicked: selector };
}

export async function setValue(session, selector, text) {
  const ok = await evaluate(session, setValueExpression(selector, text));
  if (!ok) throw new Error(`value target not found: ${selector}`);
  return { set: selector };
}

// Type into the currently focused element using synthetic key input. Works for
// rich/contenteditable editors where setting .value does not.
export async function insertText(session, text) {
  await session.send("Input.insertText", { text });
  return { inserted: text.length };
}

// Fill a react-select / combobox: focus its text input, type the value as
// TRUSTED input so the widget filters, then press Enter to take the highlighted
// option -- all in one session. A synthetic el.click cannot do this because the
// menu blurs shut between separate CDP attaches, and react-select ignores
// untrusted events. `selector` is the control (or its input).
export async function reactSelect(session, selector, value) {
  const focusExpr = `(() => {
    const ctrl = document.querySelector(${JSON.stringify(selector)});
    if (!ctrl) return "no-control";
    ctrl.scrollIntoView({ block: "center" });
    const input = ctrl.matches("input") ? ctrl : ctrl.querySelector("input");
    if (!input) return "no-input";
    input.focus();
    return document.activeElement === input ? "ok" : "not-focused";
  })()`;
  const focused = await evaluate(session, focusExpr);
  if (focused !== "ok") throw new Error(`react-select ${selector}: ${focused}`);
  // react-select v5 ignores programmatic value/input events; it only filters on
  // real trusted key events. Type each character as a dispatched key so its menu
  // opens and narrows to the match, then Enter takes the highlighted option.
  for (const ch of value) {
    await session.send("Input.dispatchKeyEvent", { type: "keyDown", text: ch, key: ch, unmodifiedText: ch });
    await session.send("Input.dispatchKeyEvent", { type: "keyUp", key: ch });
    await new Promise((r) => setTimeout(r, 45));
  }
  await new Promise((r) => setTimeout(r, 500));
  for (const type of ["keyDown", "keyUp"]) {
    await session.send("Input.dispatchKeyEvent", {
      type, key: "Enter", code: "Enter",
      windowsVirtualKeyCode: 13, nativeVirtualKeyCode: 13,
    });
  }
  await new Promise((r) => setTimeout(r, 400));
  const shown = await evaluate(session, `(() => {
    const ctrl = document.querySelector(${JSON.stringify(selector)});
    const v = ctrl && ctrl.querySelector(".select__single-value");
    return v ? v.textContent : "";
  })()`);
  return { selector, value, shown };
}

// Put text into a React-controlled input/textarea: clear it, focus it, and use
// CDP's TRUSTED Input.insertText so React registers the change and clears its
// required-field validation. Setting .value directly (even via the native
// setter) does not clear aria-invalid on Greenhouse's forms; insertText does.
export async function insertInto(session, selector, text) {
  const ready = await evaluate(session, `(() => {
    const e = document.querySelector(${JSON.stringify(selector)});
    if (!e) return "no-el";
    const proto = e.tagName === "TEXTAREA" ? window.HTMLTextAreaElement.prototype : window.HTMLInputElement.prototype;
    const setter = Object.getOwnPropertyDescriptor(proto, "value").set;
    e.focus();
    setter.call(e, "");
    if (e._valueTracker) e._valueTracker.setValue("x");
    e.dispatchEvent(new Event("input", { bubbles: true }));
    e.focus();
    return document.activeElement === e ? "ok" : "not-focused";
  })()`);
  if (ready !== "ok") throw new Error(`insertInto ${selector}: ${ready}`);
  // Trusted per-character keystrokes: React's controlled inputs only clear their
  // required-field validation on real key events, not on .value or insertText.
  for (const ch of text.replace(/\r?\n/g, " ")) {
    await session.send("Input.dispatchKeyEvent", { type: "keyDown", text: ch, key: ch, unmodifiedText: ch });
    await session.send("Input.dispatchKeyEvent", { type: "keyUp", key: ch });
    await new Promise((r) => setTimeout(r, 8));
  }
  await new Promise((r) => setTimeout(r, 200));
  const invalid = await evaluate(session, `(() => {
    const e = document.querySelector(${JSON.stringify(selector)});
    return e ? { len: (e.value || "").length, invalid: e.getAttribute("aria-invalid") } : null;
  })()`);
  return { selector, ...invalid };
}

// Open a react-select menu (ArrowDown, trusted) and read its option texts, so a
// caller can pick the exact label instead of guessing.
export async function reactOptions(session, selector) {
  const ok = await evaluate(session, `(() => {
    const c = document.querySelector(${JSON.stringify(selector)});
    if (!c) return false;
    const i = c.matches("input") ? c : c.querySelector("input");
    if (!i) return false;
    c.scrollIntoView({ block: "center" });
    i.focus();
    return document.activeElement === i;
  })()`);
  if (!ok) throw new Error(`reactOptions: ${selector} not focusable`);
  for (const type of ["keyDown", "keyUp"]) {
    await session.send("Input.dispatchKeyEvent", { type, key: "ArrowDown", code: "ArrowDown", windowsVirtualKeyCode: 40, nativeVirtualKeyCode: 40 });
  }
  await new Promise((r) => setTimeout(r, 450));
  const options = await evaluate(session, `JSON.stringify([...document.querySelectorAll(".select__option")].map((o) => o.textContent.trim()).slice(0, 40))`);
  return { options: JSON.parse(options || "[]") };
}

export async function waitFor(session, selector, timeoutMs = 8000) {
  const deadline = Date.now() + timeoutMs;
  for (;;) {
    if (await evaluate(session, existsExpression(selector))) return { found: selector };
    if (Date.now() > deadline) throw new Error(`waitFor timed out: ${selector}`);
    await new Promise((r) => setTimeout(r, 200));
  }
}

export async function screenshot(session) {
  const res = await session.send("Page.captureScreenshot", { format: "png" });
  return res.data; // base64 png
}

// Set a local file onto an <input type="file"> via CDP DOM.setFileInputFiles.
// CDP accepts a host filesystem path; Chrome reads and uploads it. This is the
// native path for resume/portfolio uploads that page-JS cannot perform (file
// inputs are security-restricted from programmatic .value assignment).
export async function uploadFile(session, selector, filePath) {
  await session.send("DOM.enable");
  const doc = await session.send("DOM.getDocument", { depth: 0 });
  const rootId = doc.root.nodeId;
  const q = await session.send("DOM.querySelector", { nodeId: rootId, selector });
  if (!q || !q.nodeId) throw new Error(`upload: file input not found: ${selector}`);
  const desc = await session.send("DOM.describeNode", { nodeId: q.nodeId });
  const backendNodeId = desc.node.backendNodeId;
  if (!backendNodeId) throw new Error(`upload: no backendNodeId for: ${selector}`);
  await session.send("DOM.setFileInputFiles", {
    files: [filePath],
    backendNodeId,
  });
  return { uploaded: filePath, selector };
}

// Evaluate inside a specific (often cross-origin) iframe. Greenhouse/Lever/
// Workday render their application forms in cross-origin iframes the main-frame
// eval cannot reach. Resolves the frame by URL substring, creates an isolated
// world in it (DOM-visible, page-JS-isolated), and evaluates there.
export async function evalInFrame(session, frameUrlMatch, expression) {
  const tree = await session.send("Page.getFrameTree");
  const frames = [];
  (function walk(f) { frames.push(f.frame); (f.childFrames || []).forEach(walk); })(tree.frameTree);
  let target = frames.find((f) => f.url && f.url.includes(frameUrlMatch));
  if (!target) target = frames.find((f) => f.url && f !== frames[0]); // first non-main
  if (!target) throw new Error(`evalInFrame: no frame matching "${frameUrlMatch}" (saw ${frames.map(f => f.url).join(", ")})`);
  const iso = await session.send("Page.createIsolatedWorld", { frameId: target.id });
  const res = await session.send("Runtime.evaluate", {
    expression,
    contextId: iso.executionContextId,
    returnByValue: true,
    awaitPromise: false,
  });
  if (res.exceptionDetails) throw new Error(`frame eval failed: ${res.exceptionDetails.text}`);
  return { frame: target.url, value: res.result?.value };
}

// Upload into a specific iframe (file input lives inside the cross-origin form).
export async function uploadInFrame(session, frameUrlMatch, selector, filePath) {
  const tree = await session.send("Page.getFrameTree");
  const frames = [];
  (function walk(f) { frames.push(f.frame); (f.childFrames || []).forEach(walk); })(tree.frameTree);
  let target = frames.find((f) => f.url && f.url.includes(frameUrlMatch));
  if (!target) target = frames.find((f) => f.url && f !== frames[0]);
  if (!target) throw new Error(`uploadInFrame: no frame matching "${frameUrlMatch}"`);
  await session.send("DOM.enable");
  // Resolve the file input within the frame's document via the frame's root node.
  const root = await session.send("DOM.getFrameOwner", { frameId: target.id }).catch(() => null);
  // Use the isolated-world eval path: locate the input, then set files via its backendNodeId.
  const iso = await session.send("Page.createIsolatedWorld", { frameId: target.id });
  const locate = await session.send("Runtime.evaluate", {
    expression: `(()=>{const el=document.querySelector(${JSON.stringify(selector)});if(!el)return null;const r=el.getBoundingClientRect();return el.outerHTML.slice(0,80);})()`,
    contextId: iso.executionContextId, returnByValue: true,
  });
  if (!locate.result?.value) throw new Error(`uploadInFrame: file input not found in frame: ${selector}`);
  return { frame: target.url, found: locate.result.value };
}
