// Scope matching for grants, plus the targets no grant can reach. Every
// function here is pure and fails closed: a malformed input never matches.
import { lstatSync, realpathSync } from "node:fs";
import path from "node:path";
import { NAMED_ONLY_SENSES, SECRET_MARKS } from "./tiers.mjs";

// realTarget - the path the operating system will act on: the deepest existing
// ancestor through realpath (symlinks, junctions, 8.3 short names and legacy
// profile junctions such as "Local Settings" all resolve), plus the segments
// that do not exist yet. A link that exists but points nowhere returns null,
// because a write through it would land wherever the link is later pointed.
// Lexical paths alone let a link inside a granted folder reach the Telos key.
export function realTarget(p) {
  if (typeof p !== "string" || !p) return null;
  const abs = path.resolve(p);
  const rest = [];
  let cur = abs;
  for (;;) {
    let st = null;
    try { st = lstatSync(cur); } catch { st = null; }
    if (st) {
      let real;
      try { real = realpathSync.native(cur); } catch { return null; }
      return rest.length ? path.join(real, ...rest.reverse()) : real;
    }
    const parent = path.dirname(cur);
    if (parent === cur) return abs;
    rest.push(path.basename(cur));
    cur = parent;
  }
}

// realRoots - grant roots and the state root through the same resolution, so
// a root that is itself a link (macOS /tmp, a junctioned drive) still matches.
export function realRoots(roots = []) {
  return roots.map((r) => (typeof r === "string" && r ? realTarget(r) ?? r : r));
}

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

// Characters that give a shell string a second command or a redirect. 0.7.0
// spawns exec with shell:false, so none reaches a shell; the refusal stays as a
// second wall in case a future driver reintroduces one.
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
  return Boolean(stateRoot) && pathInside(target, [stateRoot, ...realRoots([stateRoot])], platform);
}
