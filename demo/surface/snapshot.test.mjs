import test from "node:test";
import assert from "node:assert/strict";
import { buildBrowserSnapshot, buildUiaSnapshot } from "./snapshot.mjs";
import { newEpoch, parseRef } from "./refs.mjs";

const epoch = newEpoch(2_000_000_000_000, () => "cccccc");

function axNode(nodeId, backend, role, name, extra = {}) {
  return { nodeId, backendDOMNodeId: backend, role: { value: role }, name: { value: name },
    parentId: extra.parentId, properties: extra.properties ?? [], value: extra.value, ignored: extra.ignored };
}

test("a browser snapshot outlines actionable nodes with refs and fingerprints", () => {
  const axNodes = [
    axNode(1, 101, "RootWebArea", "doc"),
    axNode(2, 102, "button", "Save", { parentId: 1 }),
    axNode(3, 103, "textbox", "Search", { parentId: 1, value: { value: "hi", type: "string" } }),
    axNode(4, 104, "generic", "", { parentId: 1, ignored: true })
  ];
  const boxes = new Map([[102, [10, 10, 40, 20]]]);
  const snap = buildBrowserSnapshot({ epoch, targetId: "tab12345", frameId: "F", axNodes, boxes });
  assert.equal(snap.count, 3);
  const button = snap.nodes.find((n) => n.name === "Save");
  assert.equal(parseRef(button.ref).backendNodeId, 102);
  assert.match(button.fingerprint, /^[a-f0-9]{64}$/);
  assert.equal(snap.nodes.find((n) => n.name === "Search").value, "hi");
});

test("a password textbox is listed secret with no value and cannot be targeted later", () => {
  const axNodes = [
    axNode(1, 1, "RootWebArea", "doc"),
    axNode(2, 2, "textbox", "Password", { parentId: 1, value: { value: "hunter2", type: "string" }, properties: [{ name: "protected", value: { value: true } }] })
  ];
  const attrs = new Map([[2, { type: "password" }]]);
  const snap = buildBrowserSnapshot({ epoch, targetId: "t", frameId: "F", axNodes, attrs });
  const field = snap.nodes.find((n) => n.name === "Password");
  assert.equal(field.secret, true);
  assert.equal(field.value, undefined);
});

test("the snapshot honours the node budget and reports truncation", () => {
  const axNodes = Array.from({ length: 10 }, (_, i) => axNode(i + 1, i + 1, "button", `b${i}`, { parentId: 0 }));
  const snap = buildBrowserSnapshot({ epoch, targetId: "t", frameId: "F", axNodes, maxNodes: 4 });
  assert.equal(snap.count, 4);
  assert.equal(snap.truncated, true);
});

test("a uia snapshot carries runtimeId refs and marks password fields", () => {
  const elements = [
    { runtimeId: [42, 7], type: "ControlType.Button", name: "OK", automationId: "ok", className: "B", rect: [0, 0, 8, 8], path: ["ControlType.Window"] },
    { runtimeId: [42, 9], type: "ControlType.Edit", name: "Secret entry", automationId: "pw", isPassword: true, rect: [0, 20, 8, 8], path: ["ControlType.Window"] }
  ];
  const snap = buildUiaSnapshot({ epoch, hwnd: 555, processImage: "app", elements });
  assert.equal(snap.count, 2);
  assert.equal(parseRef(snap.nodes[0].ref).runtimeId.join("."), "42.7");
  assert.equal(snap.nodes[1].secret, true);
});
