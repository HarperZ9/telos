// Device control: full-device read/write/execute (remote-desktop class).
//
// Shells to tools/device.ps1 (built-in PowerShell, no external dependency).
// This is the OS-level R/W/X surface that makes the engine a peer of a remote
// desktop: run a process, read/write files, list a directory -- each action
// receipt-wrapped by the dispatcher. JSON in via args, JSON out on stdout.

import { spawn } from "node:child_process";
import { existsSync } from "node:fs";
import { fileURLToPath } from "node:url";

export function deviceScriptPath() {
  return fileURLToPath(new URL("../../tools/device.ps1", import.meta.url));
}

export function deviceArgs(scriptPath, verb, params = []) {
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

export function parseDeviceOutput(stdout) {
  const line = String(stdout || "").trim().split(/\r?\n/).filter(Boolean).pop();
  if (!line) throw new Error("device helper produced no output");
  let parsed;
  try {
    parsed = JSON.parse(line);
  } catch {
    throw new Error(`device helper output not JSON: ${line.slice(0, 200)}`);
  }
  if (parsed.ok === false) throw new Error(`device: ${parsed.error}`);
  return parsed;
}

function run(verb, params = [], { powershell = "powershell.exe", timeoutMs = 60000 } = {}) {
  const script = deviceScriptPath();
  if (!existsSync(script)) {
    return Promise.reject(new Error(`device helper missing: ${script}`));
  }
  return new Promise((resolve, reject) => {
    const child = spawn(powershell, deviceArgs(script, verb, params), {
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
        reject(new Error(`device helper exited ${code}: ${err.slice(0, 200)}`));
        return;
      }
      try {
        resolve(parseDeviceOutput(out));
      } catch (e) {
        reject(e);
      }
    });
  });
}

export const exec = (command, opts) => run("exec", [command], opts);
export const read = (path, maxBytes, opts) =>
  run("read", maxBytes != null ? [path, maxBytes] : [path], opts);
export const write = (path, text, opts) => run("write", [path, text], opts);
export const ls = (path, opts) => run("ls", [path || "."], opts);
