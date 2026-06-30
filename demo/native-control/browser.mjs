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
