// Act-by-ref for the browser (DESIGN.md 5.3). Each verb takes a backend node
// id that the caller has already re-resolved and fingerprint-checked through
// demo/surface/resolve.mjs; these functions do not decide whether to act, the
// broker does. Secret fields are refused here too, so a driver called without
// the broker still cannot type into one.
import { axNode, nodeExtras } from "./cdp.mjs";
import { ACTIONABLE_ROLES, browserNodeFacts } from "../surface/snapshot.mjs";
import { browserFingerprint } from "../surface/refs.mjs";

function refused(code, detail) {
  return Object.assign(new Error(`${code}: ${detail}`), { code });
}

// Live facts and fingerprint of one node, computed the way the snapshot did.
export async function describeRef(session, backendNodeId) {
  const { frameId, nodes, node } = await axNode(session, backendNodeId);
  if (!node) return { ok: false, code: "TARGET_NOT_FOUND" };
  const byId = new Map(nodes.map((n) => [n.nodeId, n]));
  const extra = await nodeExtras(session, backendNodeId, node.role?.value, ACTIONABLE_ROLES);
  const { facts, secret } = browserNodeFacts(node, byId, { frameId, box: extra.box, attrs: extra.attrs });
  return { ok: true, facts, secret, fingerprint: browserFingerprint(facts) };
}

async function objectFor(session, backendNodeId) {
  await session.send("DOM.enable");
  const { object } = await session.send("DOM.resolveNode", { backendNodeId });
  if (!object?.objectId) throw refused("TARGET_NOT_FOUND", "node is gone");
  return object.objectId;
}

async function callOn(session, backendNodeId, fn, args = []) {
  const objectId = await objectFor(session, backendNodeId);
  const res = await session.send("Runtime.callFunctionOn", {
    objectId, functionDeclaration: fn, arguments: args.map((value) => ({ value })), returnByValue: true
  });
  if (res.exceptionDetails) throw new Error(`page call failed: ${res.exceptionDetails.text}`);
  return res.result?.value;
}

// A real pointer press and release at the centre of the resolved box, so the
// page sees the same events a person's click produces. No OS cursor moves.
export async function clickRef(session, backendNodeId) {
  const box = await callOn(session, backendNodeId,
    "function(){this.scrollIntoView({block:'center'});const r=this.getBoundingClientRect();return [r.x,r.y,r.width,r.height];}");
  if (!Array.isArray(box) || box[2] <= 0 || box[3] <= 0) throw refused("NOT_CLICKABLE", "element has no box");
  const x = box[0] + box[2] / 2;
  const y = box[1] + box[3] / 2;
  for (const type of ["mousePressed", "mouseReleased"]) {
    await session.send("Input.dispatchMouseEvent", { type, x, y, button: "left", clickCount: 1 });
  }
  return { clicked: backendNodeId, at: [Math.round(x), Math.round(y)] };
}

export async function fillRef(session, backendNodeId, text, { secret = false } = {}) {
  if (secret) throw refused("SECRET_FIELD", "credential, one-time-code and card fields are never filled");
  const ok = await callOn(session, backendNodeId,
    "function(v){const p=this instanceof HTMLTextAreaElement?HTMLTextAreaElement.prototype:HTMLInputElement.prototype;" +
    "if(this instanceof HTMLInputElement&&this.type==='password')return 'secret';" +
    "const d=Object.getOwnPropertyDescriptor(p,'value');this.focus();" +
    "if(d&&d.set&&(this instanceof HTMLInputElement||this instanceof HTMLTextAreaElement))d.set.call(this,v);else if(this.isContentEditable)this.textContent=v;else return false;" +
    "this.dispatchEvent(new Event('input',{bubbles:true}));this.dispatchEvent(new Event('change',{bubbles:true}));return true;}",
    [String(text)]);
  if (ok === "secret") throw refused("SECRET_FIELD", "password inputs are never filled");
  if (ok !== true) throw refused("NOT_FILLABLE", "element takes no text value");
  return { filled: backendNodeId, chars: String(text).length };
}

export async function selectRef(session, backendNodeId, value) {
  const ok = await callOn(session, backendNodeId,
    "function(v){if(!(this instanceof HTMLSelectElement))return false;const o=[...this.options].find(x=>x.value===v||x.label===v);" +
    "if(!o)return 'missing';this.value=o.value;this.dispatchEvent(new Event('input',{bubbles:true}));this.dispatchEvent(new Event('change',{bubbles:true}));return true;}",
    [String(value)]);
  if (ok === "missing") throw refused("OPTION_NOT_FOUND", String(value));
  if (ok !== true) throw refused("NOT_SELECTABLE", "element is not a select");
  return { selected: backendNodeId, value: String(value) };
}

export async function focusRef(session, backendNodeId) {
  await session.send("DOM.enable");
  await session.send("DOM.focus", { backendNodeId });
  return { focused: backendNodeId };
}
