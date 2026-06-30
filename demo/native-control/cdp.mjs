// Native Chrome DevTools Protocol client.
//
// Uses Node's built-in `fetch` and `WebSocket` (Node 25), with zero external
// dependencies. Every interaction is delivered into the browser process over
// the protocol, so the operating system cursor and keyboard are never moved:
// the operator keeps using their physical device while Telos drives the page.

export const DEFAULT_PORT = 9222;

// Probe the debugger endpoint. Returns the version object, or null when no
// debug-enabled Chrome is listening (used to decide whether to relaunch).
export async function debuggerVersion(port = DEFAULT_PORT, fetchImpl = fetch) {
  try {
    const res = await fetchImpl(`http://127.0.0.1:${port}/json/version`, {
      signal: AbortSignal.timeout(1500),
    });
    if (!res.ok) return null;
    return await res.json();
  } catch {
    return null;
  }
}

// List all inspectable targets (tabs, workers, ...).
export async function listTargets(port = DEFAULT_PORT, fetchImpl = fetch) {
  const res = await fetchImpl(`http://127.0.0.1:${port}/json`);
  if (!res.ok) throw new Error(`CDP target list failed: HTTP ${res.status}`);
  return res.json();
}

// Choose a page target, optionally preferring one whose url/title contains
// `match`. Returns null when no inspectable page exists.
export function pickPageTarget(targets, { match } = {}) {
  const pages = (targets || []).filter(
    (t) => t.type === "page" && t.webSocketDebuggerUrl,
  );
  if (!pages.length) return null;
  if (match) {
    const hit = pages.find(
      (t) => (t.url || "").includes(match) || (t.title || "").includes(match),
    );
    if (hit) return hit;
  }
  return pages[0];
}

// A single CDP connection. Correlates outgoing command ids to their responses
// so callers can `await session.send(...)`. The socket is injected so the
// correlation logic is unit-testable without a live browser.
export class CdpSession {
  constructor(socket) {
    this.socket = socket;
    this.id = 0;
    this.pending = new Map();
    this.events = new Map();
    this.socket.onmessage = (event) => this._onMessage(event);
  }

  static async connect(wsUrl, socketFactory = (u) => new WebSocket(u)) {
    const socket = socketFactory(wsUrl);
    await new Promise((resolve, reject) => {
      socket.onopen = () => resolve();
      socket.onerror = (e) =>
        reject(new Error(`CDP socket error: ${e?.message || "open failed"}`));
    });
    return new CdpSession(socket);
  }

  _onMessage(event) {
    let msg;
    try {
      msg = JSON.parse(typeof event === "string" ? event : event.data);
    } catch {
      return;
    }
    if (msg.id && this.pending.has(msg.id)) {
      const { resolve, reject } = this.pending.get(msg.id);
      this.pending.delete(msg.id);
      if (msg.error) reject(new Error(`CDP ${msg.error.code}: ${msg.error.message}`));
      else resolve(msg.result);
      return;
    }
    if (msg.method) {
      const handler = this.events.get(msg.method);
      if (handler) handler(msg.params);
    }
  }

  on(method, handler) {
    this.events.set(method, handler);
  }

  send(method, params = {}, { timeoutMs = 15000 } = {}) {
    const id = ++this.id;
    const payload = JSON.stringify({ id, method, params });
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        if (this.pending.has(id)) {
          this.pending.delete(id);
          reject(new Error(`CDP timeout after ${timeoutMs}ms: ${method}`));
        }
      }, timeoutMs);
      this.pending.set(id, {
        resolve: (r) => {
          clearTimeout(timer);
          resolve(r);
        },
        reject: (e) => {
          clearTimeout(timer);
          reject(e);
        },
      });
      try {
        this.socket.send(payload);
      } catch (err) {
        this.pending.delete(id);
        clearTimeout(timer);
        reject(err);
      }
    });
  }

  close() {
    try {
      this.socket.close();
    } catch {
      // already closed
    }
  }
}
