// Background native-app control via Windows UI Automation.
//
// Shells to tools/uia.ps1 (built-in PowerShell, no external dependency). UIA
// patterns act on the control inside the target process, so the mouse and
// keyboard are never moved.

import { spawn } from "node:child_process";
import { existsSync } from "node:fs";
import { fileURLToPath } from "node:url";

export function uiaScriptPath() {
  return fileURLToPath(new URL("../../tools/uia.ps1", import.meta.url));
}

// Build the PowerShell argv for a verb. Pure + unit-testable.
export function uiaArgs(scriptPath, verb, params = []) {
  return [
    "-NoProfile",
    "-NonInteractive",
    "-ExecutionPolicy",
    "Bypass",
    "-File",
    scriptPath,
    verb,
    ...params.map((p) => String(p)),
  ];
}

// Parse a single JSON line from the helper. Throws on malformed output, surfaces
// helper-reported errors. Pure + unit-testable.
export function parseUiaOutput(stdout) {
  const line = String(stdout || "").trim().split(/\r?\n/).filter(Boolean).pop();
  if (!line) throw new Error("uia helper produced no output");
  let parsed;
  try {
    parsed = JSON.parse(line);
  } catch {
    throw new Error(`uia helper output not JSON: ${line.slice(0, 200)}`);
  }
  if (parsed.ok === false) throw new Error(`uia: ${parsed.error}`);
  return parsed;
}

function run(verb, params = [], { powershell = "powershell.exe", timeoutMs = 20000 } = {}) {
  const script = uiaScriptPath();
  if (!existsSync(script)) {
    return Promise.reject(new Error(`uia helper missing: ${script}`));
  }
  return new Promise((resolve, reject) => {
    const child = spawn(powershell, uiaArgs(script, verb, params), {
      timeout: timeoutMs,
      windowsHide: true,
    });
    let out = "";
    let err = "";
    child.stdout.on("data", (d) => (out += d));
    child.stderr.on("data", (d) => (err += d));
    child.on("error", reject);
    child.on("close", (code) => {
      if (code !== 0 && !out.trim()) {
        reject(new Error(`uia helper exited ${code}: ${err.slice(0, 200)}`));
        return;
      }
      try {
        resolve(parseUiaOutput(out));
      } catch (e) {
        reject(e);
      }
    });
  });
}

export const windows = (opts) => run("windows", [], opts);
export const tree = (windowMatch, max, opts) =>
  run("tree", max ? [windowMatch, max] : [windowMatch], opts);
export const invoke = (windowMatch, elementMatch, opts) =>
  run("invoke", [windowMatch, elementMatch], opts);
export const setValue = (windowMatch, elementMatch, text, opts) =>
  run("setvalue", [windowMatch, elementMatch, text], opts);
export const focus = (windowMatch, opts) => run("focus", [windowMatch], opts);
