// Synthetic controls only: importing this file never probes a browser or UIA.
import test from "node:test";
import assert from "node:assert/strict";
import { pickPageTarget } from "./native-control/cdp.mjs";
import { makeReceipt } from "./native-control.mjs";
import { attach } from "./native-control/browser.mjs";

const page = (id, title = id) => ({ id, type: "page", title,
  url: `https://fixture.invalid/${id}`, webSocketDebuggerUrl: `ws://fixture/${id}` });

test("explicit target must exist uniquely; omission alone keeps first-page compatibility", () => {
  const first = page("one"), second = page("two");
  assert.equal(pickPageTarget([first, second]), first);
  assert.equal(pickPageTarget([]), null);
  assert.equal(pickPageTarget([first, second], { match: "two" }), second);
  for (const targets of [[first], []]) {
    assert.throws(() => pickPageTarget(targets, { match: "missing" }),
      { code: "TARGET_NOT_FOUND" });
  }
  assert.throws(() => pickPageTarget([first, second], { match: "fixture.invalid" }),
    { code: "TARGET_AMBIGUOUS" });
  assert.throws(() => pickPageTarget([page("one", "same"), page("two", "same")], { match: "same" }),
    { code: "TARGET_AMBIGUOUS" });
});

test("invalid explicit matches cannot become omitted selection", () => {
  for (const match of ["", "   ", null, 0, false, {}]) {
    assert.throws(() => pickPageTarget([page("one")], { match }), { code: "TARGET_INVALID" });
  }
  assert.equal(pickPageTarget([page("one")], { match: undefined }).id, "one");
});

test("attach rejects invalid selection before opening a CDP socket", async () => {
  const oldFetch = globalThis.fetch, oldSocket = globalThis.WebSocket;
  let connections = 0;
  globalThis.fetch = async () => ({ ok: true, json: async () => [page("one"), page("two")] });
  globalThis.WebSocket = class { constructor() { connections++; throw new Error("unexpected connection"); } };
  try {
    await assert.rejects(attach({ match: "missing" }), { code: "TARGET_NOT_FOUND" });
    await assert.rejects(attach({ match: "fixture.invalid" }), { code: "TARGET_AMBIGUOUS" });
    await assert.rejects(attach({ match: "" }), { code: "TARGET_INVALID" });
    assert.equal(connections, 0);
  } finally {
    globalThis.fetch = oldFetch; globalThis.WebSocket = oldSocket;
  }
});

test("receipt distinguishes focus, foreground input and unknown side effects", () => {
  for (const action of ["app.focus", "app.setvalue"]) {
    const r = makeReceipt(action, "fixture", {});
    assert.equal(r.background, false); assert.equal(r.focus_effect, "focus_requested");
  }
  for (const action of ["app.input", "app.type"]) {
    const r = makeReceipt(action, "fixture", {});
    assert.equal(r.background, false); assert.equal(r.focus_effect, "foreground_input");
  }
  for (const action of ["app.invoke", "browser.click", "browser.eval", "browser.run", "device.exec", "unknown"]) {
    const r = makeReceipt(action, "fixture", { background: true });
    assert.equal(r.background, null); assert.equal(r.focus_effect, "unknown");
  }
});

test("catalog and read paths classify implementation without claiming observed focus", () => {
  for (const action of ["help", "browser.tabs", "app.windows", "app.tree", "app.value", "device.read", "device.write", "device.ls"]) {
    const r = makeReceipt(action, "fixture", {}, { clock: () => "T0" });
    assert.equal(r.background, true); assert.equal(r.focus_effect, "none_requested");
    assert.equal(r.at, "T0"); assert.equal(r.schema, "project-telos.native-control/v1");
  }
  const r = makeReceipt("app.tree", "fixture", { foreground: true }, { ok: false });
  assert.equal(r.background, false); assert.equal(r.focus_effect, "foreground_input");
  assert.equal(r.ok, false);
});
