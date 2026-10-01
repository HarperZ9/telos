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

// An explicit URL/title substring must select one page. Without a match the
// raw CLI retains first-page selection; that compatibility is not authorization.
export function pickPageTarget(targets, { match } = {}) {
  if (match !== undefined && (typeof match !== "string" || !match.trim())) {
    throw Object.assign(new Error("Explicit browser target match is invalid"), { code: "TARGET_INVALID" });
  }
  const pages = (targets || []).filter(
    (t) => t.type === "page" && t.webSocketDebuggerUrl,
  );
  if (match !== undefined) {
    const hits = pages.filter(
      (t) => (t.url || "").includes(match) || (t.title || "").includes(match),
    );
    if (hits.length !== 1) {
      const code = hits.length ? "TARGET_AMBIGUOUS" : "TARGET_NOT_FOUND";
      throw Object.assign(new Error(hits.length
        ? "Explicit browser target match is ambiguous" : "Explicit browser target match was not found"), { code });
    }
    return hits[0];
  }
  return pages[0] ?? null;
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

// ---- Accessibility tree reads (DESIGN.md section 5) ----
// Read-only CDP calls. The ref and fingerprint logic lives in demo/surface;
// these return raw nodes plus the boxes and input attributes it needs.

function boxOf(model) {
  const q = model?.border;
  if (!Array.isArray(q) || q.length < 8) return null;
  const xs = [q[0], q[2], q[4], q[6]];
  const ys = [q[1], q[3], q[5], q[7]];
  const x = Math.min(...xs);
  const y = Math.min(...ys);
  return [x, y, Math.max(...xs) - x, Math.max(...ys) - y];
}

const ATTR_ROLES = new Set(["textbox", "searchbox", "combobox", "spinbutton"]);

// Box (for actionable roles) and type/autocomplete/id (for text inputs) of one
// backend node. A node with no layout box answers null, never a guess.
export async function nodeExtras(session, backendNodeId, role, actionableRoles) {
  const out = { box: null, attrs: null };
  if (actionableRoles.has(role)) {
    try {
      out.box = boxOf((await session.send("DOM.getBoxModel", { backendNodeId })).model);
    } catch {
      out.box = null;
    }
  }
  if (ATTR_ROLES.has(role)) {
    try {
      const a = (await session.send("DOM.describeNode", { backendNodeId })).node.attributes ?? [];
      const map = {};
      for (let i = 0; i + 1 < a.length; i += 2) map[a[i]] = a[i + 1];
      out.attrs = { type: map.type ?? null, autocomplete: map.autocomplete ?? null, id: map.id ?? null };
    } catch {
      out.attrs = null;
    }
  }
  return out;
}

export async function axSnapshot(session, { actionableRoles, maxNodes = 4000 } = {}) {
  await session.send("Accessibility.enable");
  await session.send("DOM.enable");
  const { nodes } = await session.send("Accessibility.getFullAXTree");
  const frameId = (await session.send("Page.getFrameTree")).frameTree.frame.id;
  const boxes = new Map();
  const attrs = new Map();
  let seen = 0;
  for (const n of nodes) {
    if (n.ignored || !n.backendDOMNodeId) continue;
    if (++seen > maxNodes) break;
    const extra = await nodeExtras(session, n.backendDOMNodeId, n.role?.value, actionableRoles ?? new Set());
    if (extra.box) boxes.set(n.backendDOMNodeId, extra.box);
    if (extra.attrs) attrs.set(n.backendDOMNodeId, extra.attrs);
  }
  return { frameId, nodes, boxes, attrs };
}

// The node and its ancestors for act-time re-resolution.
export async function axNode(session, backendNodeId) {
  await session.send("Accessibility.enable");
  const { nodes } = await session.send("Accessibility.getPartialAXTree", { backendNodeId, fetchRelatives: true });
  const frameId = (await session.send("Page.getFrameTree")).frameTree.frame.id;
  const node = nodes.find((n) => n.backendDOMNodeId === backendNodeId && !n.ignored) ?? null;
  return { frameId, nodes, node };
}
