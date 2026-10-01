// Snapshot epochs on disk. Each MCP tool call runs in its own child process,
// so the fingerprints a snapshot hands out must outlive the call that made
// them. An epoch file maps ref -> fingerprint and is owner-only. The epoch
// store is a freshness record, never an authorization: the act-time check
// recomputes the live fingerprint and compares it to this one.
//
// The root matches the broker's state root (no environment override, so a
// process cannot point Telos at a directory it controls). Tests pass `dir`.
import { mkdirSync, readFileSync, readdirSync, rmSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { REF_TTL_MS, checkFresh, epochTime, parseRef } from "./refs.mjs";

export function surfaceDir({ env = process.env, platform = process.platform, home = os.homedir() } = {}) {
  const base = platform === "win32"
    ? path.join(env.LOCALAPPDATA || path.join(home, "AppData", "Local"), "Telos")
    : path.join(env.XDG_STATE_HOME || path.join(home, ".local", "state"), "telos");
  return path.join(base, "surface", "epochs");
}

const EPOCH_RE = /^e[0-9a-z]+$/;

export function saveEpoch(snapshot, { dir = surfaceDir(), target = null, now = Date.now() } = {}) {
  if (!EPOCH_RE.test(snapshot.epoch)) throw new TypeError("bad epoch");
  mkdirSync(dir, { recursive: true, mode: 0o700 });
  const refs = Object.fromEntries(snapshot.nodes.map((n) => [n.ref, { fingerprint: n.fingerprint, secret: Boolean(n.secret) }]));
  const body = { schema: "telos.surface-epoch/v1", epoch: snapshot.epoch, surface: snapshot.surface, target, created_ms: now, refs };
  writeFileSync(path.join(dir, `${snapshot.epoch}.json`), JSON.stringify(body), { mode: 0o600 });
  pruneEpochs({ dir, now });
  return body;
}

export function pruneEpochs({ dir = surfaceDir(), now = Date.now(), ttl = REF_TTL_MS } = {}) {
  let names = [];
  try { names = readdirSync(dir); } catch { return 0; }
  let removed = 0;
  for (const name of names) {
    const epoch = name.replace(/\.json$/, "");
    if (EPOCH_RE.test(epoch) && now - epochTime(epoch) > 10 * ttl) {
      rmSync(path.join(dir, name), { force: true });
      removed += 1;
    }
  }
  return removed;
}

// Look a ref up. Answers { ok, fingerprint, secret, target } or a code:
// BAD_REF, STALE_REF (older than the TTL), UNKNOWN_REF (no such epoch or ref).
export function lookupRef(ref, { dir = surfaceDir(), now = Date.now() } = {}) {
  let parsed;
  try { parsed = parseRef(ref); } catch (err) { return { ok: false, code: err.code ?? "BAD_REF" }; }
  const fresh = checkFresh(ref, now);
  if (!fresh.ok) return { ok: false, code: fresh.code };
  let body;
  try {
    body = JSON.parse(readFileSync(path.join(dir, `${parsed.epoch}.json`), "utf8"));
  } catch {
    return { ok: false, code: "UNKNOWN_REF" };
  }
  const hit = body.refs?.[ref];
  if (!hit) return { ok: false, code: "UNKNOWN_REF" };
  return { ok: true, parsed, fingerprint: hit.fingerprint, secret: hit.secret, target: body.target };
}
