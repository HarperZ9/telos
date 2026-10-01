import test from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { lookupRef, saveEpoch, surfaceDir } from "./epochs.mjs";
import { buildBrowserSnapshot } from "./snapshot.mjs";
import { REF_TTL_MS, newEpoch } from "./refs.mjs";

function snap(now) {
  const epoch = newEpoch(now, () => "dddddd");
  const axNodes = [
    { nodeId: 1, backendDOMNodeId: 1, role: { value: "RootWebArea" }, name: { value: "doc" } },
    { nodeId: 2, backendDOMNodeId: 5, role: { value: "button" }, name: { value: "Go" }, parentId: 1, properties: [] }
  ];
  return buildBrowserSnapshot({ epoch, targetId: "tab", frameId: "F", axNodes, boxes: new Map([[5, [0, 0, 8, 8]]]) });
}

test("a saved ref looks up its fingerprint, and a foreign ref is unknown", () => {
  const dir = mkdtempSync(path.join(tmpdir(), "telos-epoch-"));
  try {
    const now = 2_100_000_000_000;
    const s = snap(now);
    saveEpoch(s, { dir, target: { origin: "https://example.test" }, now });
    const ref = s.nodes.find((n) => n.name === "Go").ref;
    const hit = lookupRef(ref, { dir, now });
    assert.equal(hit.ok, true);
    assert.equal(hit.fingerprint, s.nodes.find((n) => n.name === "Go").fingerprint);
    assert.deepEqual(hit.target, { origin: "https://example.test" });
    const other = newEpoch(now, () => "eeeeee");
    assert.equal(lookupRef(`b:${other}:tab:5`, { dir, now }).code, "UNKNOWN_REF");
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("a ref past the TTL is stale even when the epoch file is present", () => {
  const dir = mkdtempSync(path.join(tmpdir(), "telos-epoch-"));
  try {
    const now = 2_100_000_000_000;
    const s = snap(now);
    saveEpoch(s, { dir, now });
    const ref = s.nodes.find((n) => n.name === "Go").ref;
    assert.equal(lookupRef(ref, { dir, now: now + REF_TTL_MS + 1 }).code, "STALE_REF");
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("the surface dir has no environment override", () => {
  const a = surfaceDir({ env: { LOCALAPPDATA: "C:/base" }, platform: "win32" });
  assert.equal(a, path.join("C:/base", "Telos", "surface", "epochs"));
  const b = surfaceDir({ env: { XDG_STATE_HOME: "/s" }, platform: "linux" });
  assert.equal(b, path.join("/s", "telos", "surface", "epochs"));
});
