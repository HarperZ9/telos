import test from "node:test";
import assert from "node:assert/strict";
import {
  REF_TTL_MS, browserFingerprint, canonical, checkFresh, epochTime, formatBrowserRef, formatUiaRef,
  isSecretField, newEpoch, parseRef, quantizeBox, uiaFingerprint
} from "./refs.mjs";

test("canonical form sorts keys and refuses nothing by shape", () => {
  assert.equal(canonical({ b: 1, a: [2, { d: 4, c: 3 }] }), '{"a":[2,{"c":3,"d":4}],"b":1}');
});

test("an epoch carries its creation time and round-trips", () => {
  const now = 1_900_000_000_000;
  const epoch = newEpoch(now, () => "abc123");
  assert.equal(epochTime(epoch), now);
  assert.equal(checkFresh(formatBrowserRef({ epoch, targetId: "T", backendNodeId: 7 }), now).ok, true);
});

test("a ref older than the TTL is stale", () => {
  const now = 1_900_000_000_000;
  const epoch = newEpoch(now - REF_TTL_MS - 1, () => "aaaaaa");
  const ref = formatBrowserRef({ epoch, targetId: "target12", backendNodeId: 3 });
  assert.equal(checkFresh(ref, now).code, "STALE_REF");
});

test("browser and uia refs format and parse", () => {
  const epoch = newEpoch(1, () => "bbbbbb");
  const b = formatBrowserRef({ epoch, targetId: "abcdefghijk", backendNodeId: 12 });
  assert.deepEqual(parseRef(b), { surface: "browser", epoch, target8: "abcdefgh", backendNodeId: 12 });
  const u = formatUiaRef({ epoch, hwnd: 999, runtimeId: [42, 7, 3] });
  assert.deepEqual(parseRef(u), { surface: "native", epoch, hwnd: 999, runtimeId: [42, 7, 3] });
  assert.throws(() => parseRef("x:1:2:3"), /BAD_REF/);
  assert.throws(() => formatBrowserRef({ epoch, targetId: "T", backendNodeId: 0 }), /BAD_REF/);
});

test("boxes quantize to the grid and a missing box is null", () => {
  assert.deepEqual(quantizeBox([13, 29, 100, 23]), [8, 24, 96, 16]);
  assert.equal(quantizeBox(null), null);
  assert.equal(quantizeBox([1, 2, NaN, 4]), null);
});

test("the fingerprint changes with each field it binds", () => {
  const base = { role: "button", name: "Save", valueKind: null, frameId: "f", ancestors: ["root", "form"], box: [8, 8, 40, 16] };
  const fp = browserFingerprint(base);
  assert.notEqual(fp, browserFingerprint({ ...base, name: "Save As" }));
  assert.notEqual(fp, browserFingerprint({ ...base, ancestors: ["root", "dialog"] }));
  assert.notEqual(fp, browserFingerprint({ ...base, box: [16, 8, 40, 16] }));
  assert.equal(fp, browserFingerprint({ ...base, box: [13, 11, 44, 23] }), "same quantized box is the same print");
});

test("uia fingerprint binds control type, ids and process", () => {
  const base = { controlType: "Button", name: "OK", automationId: "ok", className: "Btn", processImage: "app", ancestors: ["Window"], box: [0, 0, 8, 8] };
  const fp = uiaFingerprint(base);
  assert.notEqual(fp, uiaFingerprint({ ...base, processImage: "other" }));
  assert.notEqual(fp, uiaFingerprint({ ...base, automationId: "ok2" }));
});

test("secret fields are caught by type, autocomplete and name marks", () => {
  assert.equal(isSecretField({ inputType: "password" }), true);
  assert.equal(isSecretField({ autocomplete: "one-time-code" }), true);
  assert.equal(isSecretField({ name: "Card number" }), true);
  assert.equal(isSecretField({ automationId: "otp_entry" }), true);
  assert.equal(isSecretField({ name: "Search" }), false);
});
