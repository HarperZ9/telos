// Review-and-authorize queue for outreach and applications. Add targets (by hand
// or from scrape), then `run` walks them: each item is prepared (navigate +
// fill + gate detection) and STAGED for the operator to review and authorize.
// Nothing is submitted or sent from the queue. Storage is a plain JSON file and
// never holds secrets. See BOUNDARY.md.
//
//   queue add --url=.. [--kind=apply|contact]
//   queue list
//   queue run [limit]     -> prepare each pending item, stage for review
//   queue remove --id=..

import { readFileSync, writeFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname } from "node:path";
import * as browser from "./browser.mjs";
import * as prepare from "./prepare.mjs";

export function queuePath(env = process.env) {
  if (env.TELOS_QUEUE_PATH) return env.TELOS_QUEUE_PATH;
  const base = env.LOCALAPPDATA || env.HOME || ".";
  return `${base}/Telos/queue.json`;
}

export function load(path = queuePath()) {
  if (!existsSync(path)) return { items: [] };
  try { return JSON.parse(readFileSync(path, "utf8")); } catch { return { items: [] }; }
}

export function save(state, path = queuePath()) {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, JSON.stringify(state, null, 2) + "\n", "utf8");
  return { saved: true, count: state.items.length };
}

// Pure: append items, de-duplicating by url. idFor injects the id (kept pure /
// deterministic for testing rather than depending on a clock).
export function addItems(state, items, idFor = (url, i) => `q${i}_${normalize(url)}`) {
  const seen = new Set(state.items.map((it) => it.url));
  let n = state.items.length;
  for (const raw of items) {
    const url = typeof raw === "string" ? raw : raw.url;
    if (!url || seen.has(url)) continue;
    seen.add(url);
    state.items.push({ id: idFor(url, n), url, kind: (raw && raw.kind) || "apply", status: "pending" });
    n++;
  }
  return state;
}

function normalize(url) {
  return String(url).replace(/^https?:\/\//, "").replace(/[^a-z0-9]+/gi, "-").slice(0, 40);
}

export function add(items, path = queuePath()) {
  const state = addItems(load(path), Array.isArray(items) ? items : [items]);
  save(state, path);
  return { added: state.items.filter((i) => i.status === "pending").length, total: state.items.length };
}

export function list(path = queuePath()) {
  return load(path).items;
}

export function remove(id, path = queuePath()) {
  const state = load(path);
  const before = state.items.length;
  state.items = state.items.filter((it) => it.id !== id);
  save(state, path);
  return { id, removed: before !== state.items.length };
}

// Prepare each pending item and stage it. Never submits; prepare() stops at the
// personhood gate, and the item's status records what the operator must do.
export async function run(session, { path = queuePath(), limit = 5 } = {}) {
  const state = load(path);
  const pending = state.items.filter((it) => it.status === "pending").slice(0, limit);
  const staged = [];
  const politenessMs = Number(process.env.TELOS_QUEUE_DELAY_MS) || 1500;
  let first = true;
  for (const item of pending) {
    try {
      if (!first) await new Promise((r) => setTimeout(r, politenessMs)); // don't hammer hosts
      first = false;
      await browser.navigate(session, item.url);
      const res = await prepare.prepare(session, {});
      item.status = "staged";
      item.disposition = res.disposition;
      item.gate = res.gate?.gate || "none";
      staged.push({ id: item.id, url: item.url, disposition: res.disposition, gate: item.gate, next_action: res.next_action });
    } catch (err) {
      item.status = "error";
      item.error = err.message;
      staged.push({ id: item.id, url: item.url, error: err.message });
    }
  }
  save(state, path);
  return { ran: pending.length, staged, note: "Review each staged item; authorize submission yourself." };
}
