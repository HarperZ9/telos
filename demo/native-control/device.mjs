// Device control: read, write, list and execute on the operator's machine.
//
// Node built-ins only. 0.6.0 shelled to tools/device.ps1, whose `exec` ran
// `cmd /c <string>`: cmd searches the current directory before PATH, so a
// planted `git.bat` ran in place of an allowlisted `git`, and cmd re-parses the
// string (carets, percent expansion, quotes). 0.7.0 deletes that helper.
// `exec` now takes an argv, resolves argv[0] to an absolute path through the
// absolute PATH entries only (never the current directory), refuses batch and
// script files, and spawns with shell:false. Every call reaches here only
// through the tier gate (demo/broker), which holds exec at T4.
import { spawn } from "node:child_process";
import { accessSync, constants, readFileSync, readdirSync, statSync, writeFileSync } from "node:fs";
import path from "node:path";

const WIN_EXT = [".exe", ".com"];

// whichExecutable - absolute path of argv0, or null. An argv0 that already
// names a path is used only when absolute. Relative PATH entries and the
// current directory are skipped, so a file written into the working folder
// cannot stand in for a program on PATH.
export function whichExecutable(argv0, { env = process.env, platform = process.platform } = {}) {
  if (typeof argv0 !== "string" || !argv0 || argv0.includes("\0")) return null;
  const lib = platform === "win32" ? path.win32 : path.posix;
  const exts = platform === "win32" ? WIN_EXT : [""];
  const usable = (file) => {
    if (platform === "win32" && !WIN_EXT.includes(lib.extname(file).toLowerCase())) return false;
    try {
      if (!statSync(file).isFile()) return false;
      if (platform !== "win32") accessSync(file, constants.X_OK);
      return true;
    } catch {
      return false;
    }
  };
  if (argv0.includes("/") || argv0.includes("\\")) {
    return lib.isAbsolute(argv0) && usable(argv0) ? argv0 : null;
  }
  const pathVar = env.PATH ?? env.Path ?? env.path ?? "";
  for (const dir of pathVar.split(lib.delimiter)) {
    if (!dir || !lib.isAbsolute(dir)) continue;
    const hasExt = platform === "win32" && WIN_EXT.includes(lib.extname(argv0).toLowerCase());
    for (const ext of hasExt ? [""] : exts) {
      const file = lib.join(dir, argv0 + ext);
      if (usable(file)) return file;
    }
  }
  return null;
}

// exec - argv[0] must already be the absolute path the gate approved (the
// broker substitutes it); a bare name is resolved here the same way.
export function exec(argv, { timeoutMs = 60000, cwd = process.cwd(), maxBytes = 200000 } = {}) {
  if (!Array.isArray(argv) || argv.length === 0) return Promise.reject(new Error("exec: no argv"));
  const file = whichExecutable(String(argv[0]));
  if (!file) return Promise.reject(new Error(`exec: ${path.basename(String(argv[0]))} is not an executable on PATH`));
  return new Promise((resolve, reject) => {
    const child = spawn(file, argv.slice(1).map(String), { shell: false, windowsHide: true, timeout: timeoutMs, cwd });
    let out = "";
    let err = "";
    child.stdout.on("data", (d) => { if (out.length < maxBytes) out += d; });
    child.stderr.on("data", (d) => { if (err.length < maxBytes) err += d; });
    child.on("error", reject);
    child.on("close", (code, signal) => {
      resolve({ ok: code === 0, exit: code, signal: signal ?? null, executable: path.basename(file),
        stdout: out.slice(0, maxBytes).trim(), stderr: err.slice(0, maxBytes).trim() });
    });
  });
}

export async function read(p, maxBytes = 200000) {
  const text = readFileSync(p, "utf8");
  const truncated = text.length > maxBytes;
  const content = truncated ? text.slice(0, maxBytes) : text;
  return { ok: true, path: p, length: content.length, truncated, content };
}

export async function write(p, text) {
  if (!p) throw new Error("write: no path");
  const data = String(text ?? "");
  writeFileSync(p, data, "utf8");
  return { ok: true, path: p, bytes: Buffer.byteLength(data, "utf8") };
}

export async function ls(p = ".") {
  const entries = readdirSync(p || ".", { withFileTypes: true }).map((e) => {
    let kb = 0;
    try { kb = e.isDirectory() ? 0 : Math.round(statSync(path.join(p || ".", e.name)).size / 102.4) / 10; } catch { kb = 0; }
    return { name: e.name, type: e.isDirectory() ? "dir" : "file", kb };
  });
  return { ok: true, path: p || ".", count: entries.length, entries };
}
