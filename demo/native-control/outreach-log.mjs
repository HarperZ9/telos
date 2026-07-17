// Outreach send-log: protects the operator's sender reputation (the asset that
// gets burned by careless automation). Records each authorized send locally and
// enforces two guards before another send:
//
//   - dedup: refuse to email the same recipient twice (override: --resend).
//   - rate limit: refuse more than N sends per rolling window (default 20/hour;
//     env TELOS_SEND_MAX_PER_HOUR). Waiting is the point -- it keeps a queue run
//     from looking like a blast.
//
// The log is local, gitignored, and holds the operator's own outreach history
// (recipient + subject + timestamp). It carries no credentials.

import { readFileSync, writeFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname } from "node:path";

export function logPath(env = process.env) {
  if (env.TELOS_SENDLOG_PATH) return env.TELOS_SENDLOG_PATH;
  const base = env.LOCALAPPDATA || env.HOME || ".";
  return `${base}/Telos/outreach-log.json`;
}

export function normalizeEmail(e) {
  return String(e || "").trim().toLowerCase();
}

export function load(path = logPath()) {
  if (!existsSync(path)) return { sends: [] };
  try { return JSON.parse(readFileSync(path, "utf8")); } catch { return { sends: [] }; }
}

export function save(state, path = logPath()) {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, JSON.stringify(state, null, 2) + "\n", "utf8");
  return { saved: true, count: state.sends.length };
}

// Pure: has this recipient already been contacted?
export function alreadySent(state, to) {
  const t = normalizeEmail(to);
  return (state.sends || []).some((s) => normalizeEmail(s.to) === t);
}

// Pure: count sends within the rolling window ending at nowMs.
export function countWithin(state, nowMs, windowMs) {
  return (state.sends || []).filter((s) => {
    const t = Date.parse(s.at);
    return Number.isFinite(t) && nowMs - t < windowMs;
  }).length;
}

export function rateConfig(env = process.env) {
  const max = Number(env.TELOS_SEND_MAX_PER_HOUR) || 20;
  return { max, windowMs: 3600_000 };
}

// Pure: decide whether a send is allowed. Returns {allow, reason}.
export function checkSend(state, to, { nowMs, resend = false, rate = rateConfig() } = {}) {
  if (!resend && alreadySent(state, to)) {
    const prev = state.sends.find((s) => normalizeEmail(s.to) === normalizeEmail(to));
    return { allow: false, reason: `already contacted ${normalizeEmail(to)} on ${prev?.at || "?"} (use --resend to override)` };
  }
  const recent = countWithin(state, nowMs, rate.windowMs);
  if (recent >= rate.max) {
    return { allow: false, reason: `rate limit: ${recent}/${rate.max} sends in the last hour; wait before sending more (raise TELOS_SEND_MAX_PER_HOUR to change)` };
  }
  return { allow: true, reason: `${recent + 1}/${rate.max} this hour` };
}

// Append a send record. `at` injected for testability; defaults to now.
export function record({ to, subject, at }, path = logPath()) {
  const state = load(path);
  state.sends.push({ to: normalizeEmail(to), subject: subject || "", at: at || new Date().toISOString() });
  save(state, path);
  return { recorded: normalizeEmail(to), total: state.sends.length };
}

// Summary for the status verb (no full recipient list dumped by default).
export function summary(path = logPath()) {
  const state = load(path);
  const sends = state.sends || [];
  const last = sends[sends.length - 1];
  return { total: sends.length, lastAt: last?.at || null, lastTo: last?.to || null };
}
