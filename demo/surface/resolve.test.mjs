import test from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { resolveRef, resolveUiaRef } from "./resolve.mjs";
import { saveEpoch } from "./epochs.mjs";
import { buildUiaSnapshot } from "./snapshot.mjs";
import { newEpoch, uiaFingerprint } from "./refs.mjs";
import { uiaNodeFacts } from "./snapshot.mjs";

function uiaEnv(now, { isPassword = false } = {}) {
  const dir = mkdtempSync(path.join(tmpdir(), "telos-resolve-"));
  const epoch = newEpoch(now, () => "ffffff");
  const el = { runtimeId: [42, 7], type: "ControlType.Button", name: "OK", automationId: "ok",
    className: "B", rect: [10, 10, 40, 20], path: ["ControlType.Window"], isPassword };
  const snap = buildUiaSnapshot({ epoch, hwnd: 321, processImage: "app", elements: [el] });
  saveEpoch(snap, { dir, target: { hwnd: 321 }, now });
  return { dir, ref: snap.nodes[0].ref, el };
}

// A live resolve that echoes the recorded element: fingerprints match.
function liveSame(el, process = "app") {
  return async () => ({ ok: true, hwnd: 321, process, element: el });
}

test("a matching native ref resolves and carries resolution ref", async () => {
  const now = 2_200_000_000_000;
  const { dir, ref, el } = uiaEnv(now);
  try {
    const r = await resolveUiaRef(ref, { resolveUia: liveSame(el), dir, now });
    assert.equal(r.ok, true);
    assert.equal(r.resolution, "ref");
    assert.equal(r.target_fingerprint, uiaFingerprint(uiaNodeFacts(el, "app")));
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("a changed element refuses with FINGERPRINT_MISMATCH", async () => {
  const now = 2_200_000_000_000;
  const { dir, ref, el } = uiaEnv(now);
  try {
    const moved = { ...el, name: "Cancel" };
    const r = await resolveUiaRef(ref, { resolveUia: liveSame(moved), dir, now });
    assert.equal(r.ok, false);
    assert.equal(r.code, "FINGERPRINT_MISMATCH");
    assert.notEqual(r.recorded, r.observed);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("a now-protected element refuses as a secret field", async () => {
  const now = 2_200_000_000_000;
  const { dir, ref, el } = uiaEnv(now);
  try {
    const r = await resolveUiaRef(ref, { resolveUia: liveSame({ ...el, isPassword: true }), dir, now });
    assert.equal(r.code, "SECRET_FIELD");
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("a disappeared element and an unparseable ref both refuse", async () => {
  const now = 2_200_000_000_000;
  const { dir, ref } = uiaEnv(now);
  try {
    const gone = await resolveUiaRef(ref, { resolveUia: async () => ({ ok: false }), dir, now });
    assert.equal(gone.code, "TARGET_NOT_FOUND");
    assert.equal((await resolveRef("z:1:2:3", { dir, now })).code, "BAD_REF");
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});
