// Scope matching for grants, plus the targets no grant can reach. Every
// function here is pure and fails closed: a malformed input never matches.
import path from "node:path";
import { NAMED_ONLY_SENSES, SECRET_MARKS } from "./tiers.mjs";

export function originOf(url) {
  try {
    const u = new URL(url);
    return u.origin === "null" ? null : u.origin;
  } catch {
    return null;
  }
}

export function originAllowed(origin, origins = []) {
  return typeof origin === "string" && origins.includes(origin);
}

const norm = (p, platform) => {
  const resolved = (platform === "win32" ? path.win32 : path.posix).resolve(p);
  return platform === "win32" ? resolved.toLowerCase() : resolved;
};

export function pathInside(target, roots = [], platform = process.platform) {
  if (typeof target !== "string" || !target) return false;
  const lib = platform === "win32" ? path.win32 : path.posix;
  const t = norm(target, platform);
  return roots.some((root) => {
    if (typeof root !== "string" || !root) return false;
    const rel = lib.relative(norm(root, platform), t);
    return rel === "" || (!rel.startsWith("..") && !lib.isAbsolute(rel));
  });
}

// A window pattern is { title } (exact, case-insensitive) or { title_contains },
// optionally with { process } (image name) and { class } (UIA class name),
// both case-insensitive.
export function windowAllowed(win, patterns = []) {
  if (!win || typeof win.title !== "string") return false;
  const title = win.title.toLowerCase();
  const proc = String(win.process || "").toLowerCase();
  return patterns.some((p) => {
    if (!p || typeof p !== "object") return false;
    if (p.process && String(p.process).toLowerCase() !== proc) return false;
    if (p.class && String(p.class).toLowerCase() !== String(win.class || "").toLowerCase()) return false;
    if (typeof p.title === "string") return p.title.toLowerCase() === title;
    if (typeof p.title_contains === "string" && p.title_contains) return title.includes(p.title_contains.toLowerCase());
    return false;
  });
}

// exec_allow entries are token arrays: "*" matches one token, a trailing "**"
// matches the rest. argv0 must match exactly.
export function execAllowed(argv, allow = []) {
  if (!Array.isArray(argv) || argv.length === 0) return false;
  return allow.some((entry) => {
    if (!Array.isArray(entry) || entry.length === 0) return false;
    if (entry[0] !== argv[0]) return false;
    for (let i = 1; i < entry.length; i++) {
      if (entry[i] === "**" && i === entry.length - 1) return true;
      if (i >= argv.length) return false;
      if (entry[i] !== "*" && entry[i] !== argv[i]) return false;
    }
    return argv.length === entry.length;
  });
}

export function senseAllowed(sense, senses = []) {
  if (typeof sense !== "string") return false;
  if (senses.includes(sense)) return true;
  return senses.includes("*") && !NAMED_ONLY_SENSES.includes(sense);
}

export function deviceAllowed(id, devices = []) {
  return typeof id === "string" && devices.includes(id);
}

export function namesSecretField(text) {
  if (typeof text !== "string" || !text) return false;
  const t = text.toLowerCase();
  return SECRET_MARKS.some((mark) => t.includes(mark));
}

// Characters that give a shell string a second command or a redirect. The 0.6.0
// `device exec` runs `cmd /c <string>`, so any of these turns one allowlisted
// argv into something else.
export const SHELL_METACHARS = /[&|;<>^%!`$(){}\[\]"'\r\n\*?~]/;

// Terminal hosts: text sent into one is command execution, which is T4 `exec`
// with an argv allowlist, never a T3 UI action.
export const TERMINAL_PROCESSES = Object.freeze([
  "windowsterminal", "wt", "conhost", "cmd", "powershell", "pwsh", "openconsole",
  "mintty", "bash", "wsl", "alacritty", "wezterm-gui", "kitty",
]);

// UIA window classes of terminal hosts (Windows Terminal, classic console).
export const TERMINAL_CLASSES = Object.freeze(["cascadia_hosting_window_class", "consolewindowclass", "pseudoconsolewindow"]);

// Windows that host the human approval channel or the session's own client.
export const PROTECTED_TITLES = Object.freeze([/telos confirm/i, /telos grant/i, /flywheel.*monitor/i]);

export function protectedWindow(win, extraProcesses = []) {
  if (!win) return null;
  const proc = String(win.process || "").toLowerCase().replace(/\.exe$/, "");
  if (TERMINAL_PROCESSES.includes(proc)) return "terminal host";
  if (TERMINAL_CLASSES.includes(String(win.class || "").toLowerCase())) return "terminal host";
  if (extraProcesses.map((p) => String(p).toLowerCase().replace(/\.exe$/, "")).includes(proc)) return "session client";
  if (PROTECTED_TITLES.some((re) => re.test(String(win.title || "")))) return "approval channel";
  return null;
}

export function protectedPath(target, stateRoot, platform = process.platform) {
  return Boolean(stateRoot) && pathInside(target, [stateRoot], platform);
}
