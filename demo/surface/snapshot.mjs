// Snapshot outlines (DESIGN.md 5.1): raw accessibility trees in, a compact
// ref outline out. Pure: the drivers fetch, this file shapes. Each outline node
// carries ref, role, name, a value (redacted for secret fields), state flags,
// and the fingerprint the act-time check recomputes. Secret fields are listed
// with `secret: true` and no value so the model knows they exist and that
// Telos will not target them.
import {
  MAX_SNAPSHOT_NODES, browserFingerprint, formatBrowserRef, formatUiaRef, isSecretField, uiaFingerprint
} from "./refs.mjs";

// Roles whose box enters the fingerprint. Both the snapshot and the act-time
// resolver apply the same rule, so a fingerprint never compares a box to null.
export const ACTIONABLE_ROLES = new Set(["button", "link", "textbox", "searchbox", "combobox", "checkbox",
  "radio", "menuitem", "menuitemcheckbox", "menuitemradio", "tab", "option", "slider", "switch",
  "spinbutton", "listbox", "treeitem"]);

const prop = (node, name) => (node.properties ?? []).find((p) => p.name === name)?.value?.value;

function valueKind(node) {
  const v = node.value?.type;
  return v ? String(v) : null;
}

// Non-ignored ancestor roles, root first. The same walk runs at act time over
// Accessibility.getPartialAXTree with fetchRelatives.
export function browserAncestors(nodeId, byId) {
  const out = [];
  let cur = byId.get(byId.get(nodeId)?.parentId);
  while (cur) {
    if (!cur.ignored) out.unshift(cur.role?.value ?? "");
    cur = byId.get(cur.parentId);
  }
  return out;
}

export function browserNodeFacts(node, byId, { frameId, box, attrs }) {
  const role = node.role?.value ?? "";
  const name = node.name?.value ?? "";
  const facts = { role, name, valueKind: valueKind(node), frameId, ancestors: browserAncestors(node.nodeId, byId),
    box: ACTIONABLE_ROLES.has(role) ? box ?? null : null };
  const secret = isSecretField({ name, inputType: attrs?.type, autocomplete: attrs?.autocomplete, id: attrs?.id })
    || (role === "textbox" && prop(node, "protected") === true);
  return { facts, secret };
}

// axNodes: Accessibility.getFullAXTree nodes. boxes / attrs: maps from
// backendDOMNodeId to a box [x,y,w,h] and to {type, autocomplete, id}.
export function buildBrowserSnapshot({ epoch, targetId, frameId, axNodes, boxes = new Map(), attrs = new Map(),
  maxNodes = MAX_SNAPSHOT_NODES }) {
  const byId = new Map(axNodes.map((n) => [n.nodeId, n]));
  const nodes = [];
  let truncated = false;
  for (const node of axNodes) {
    if (node.ignored || !node.backendDOMNodeId) continue;
    if (nodes.length >= maxNodes) { truncated = true; break; }
    const id = node.backendDOMNodeId;
    const { facts, secret } = browserNodeFacts(node, byId, { frameId, box: boxes.get(id), attrs: attrs.get(id) });
    nodes.push({
      ref: formatBrowserRef({ epoch, targetId, backendNodeId: id }),
      role: facts.role, name: facts.name,
      ...(secret ? { secret: true } : node.value?.value !== undefined ? { value: String(node.value.value) } : {}),
      ...(prop(node, "focused") ? { focused: true } : {}),
      ...(prop(node, "disabled") ? { disabled: true } : {}),
      fingerprint: browserFingerprint(facts)
    });
  }
  return { epoch, surface: "browser", count: nodes.length, truncated, nodes };
}

// elements: uia.ps1 `tree` records with runtimeId, type, name, automationId,
// className, rect and path (ancestor control types, window first).
export function uiaNodeFacts(el, processImage) {
  return { controlType: el.type ?? null, name: el.name ?? null, automationId: el.automationId ?? null,
    className: el.className ?? null, processImage, ancestors: el.path ?? [], box: el.rect ?? null };
}

export function buildUiaSnapshot({ epoch, hwnd, processImage, elements, truncated = false, settlesAbsence }) {
  const nodes = [];
  for (const el of elements) {
    if (!Array.isArray(el.runtimeId) || !el.runtimeId.length) continue;
    const facts = uiaNodeFacts(el, processImage);
    const secret = isSecretField({ name: el.name, automationId: el.automationId }) || el.isPassword === true;
    nodes.push({
      ref: formatUiaRef({ epoch, hwnd, runtimeId: el.runtimeId }),
      role: el.type, name: el.name ?? "", ...(el.automationId ? { automationId: el.automationId } : {}),
      ...(secret ? { secret: true } : {}),
      fingerprint: uiaFingerprint(facts)
    });
  }
  return { epoch, surface: "native", count: nodes.length, truncated, settlesAbsence: settlesAbsence ?? null, nodes };
}
