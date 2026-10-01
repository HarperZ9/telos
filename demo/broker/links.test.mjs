// Links inside a granted folder. Scope used to compare lexical paths, so a
// symlink or Windows junction inside a granted folder reached anything it
// pointed at, the Telos key included (Windows ships such junctions in every
// profile: "Local Settings" points at AppData\Local). Each test plants a link
// and checks the gate judges the location the operating system will act on.
import test from "node:test";
import assert from "node:assert/strict";
import { mkdirSync, symlinkSync, writeFileSync } from "node:fs";
import path from "node:path";
import { makeEnv } from "./harness.test.mjs";
import { realTarget } from "./scope.mjs";

const dirLink = (target, link) => symlinkSync(target, link, process.platform === "win32" ? "junction" : "dir");

function linkedEnv() {
  const env = makeEnv();
  const granted = path.join(env.root, "granted");
  mkdirSync(granted, { recursive: true });
  mkdirSync(env.dirs.keys, { recursive: true });
  writeFileSync(path.join(env.dirs.keys, "telos-ed25519.key"), "not a real key");
  return { env, granted };
}

test("a link inside a granted folder cannot reach the Telos state directory", async () => {
  const { env, granted } = linkedEnv();
  dirLink(env.dirs.root, path.join(granted, "state-link"));
  env.grant({ tier: "T1", verbs: ["device.read"], scope: { paths: [granted], senses: ["file_read"] } });
  const r = await env.broker().call({ verb: "device.read", params: [path.join(granted, "state-link", "keys", "telos-ed25519.key")] });
  assert.equal(r.status, "REFUSED");
  assert.equal(r.reason, "PROTECTED_TARGET");
  assert.equal(env.calls.length, 0);
});

test("a link inside a granted folder cannot read outside the grant", async () => {
  const { env, granted } = linkedEnv();
  const outside = path.join(env.root, "outside");
  mkdirSync(outside);
  writeFileSync(path.join(outside, "secret.txt"), "x");
  dirLink(outside, path.join(granted, "out-link"));
  env.grant({ tier: "T1", verbs: ["device.read"], scope: { paths: [granted], senses: ["file_read"] } });
  const r = await env.broker().call({ verb: "device.read", params: [path.join(granted, "out-link", "secret.txt")] });
  assert.equal(r.status, "REFUSED");
  assert.equal(r.reason, "OUT_OF_SCOPE");
  assert.equal(env.calls.length, 0);
});

test("a write through a sandbox link to outside the sandbox is not a T2 sandbox write", async () => {
  const { env } = linkedEnv();
  const outside = path.join(env.root, "outside");
  mkdirSync(outside);
  mkdirSync(env.sandbox, { recursive: true });
  dirLink(outside, path.join(env.sandbox, "escape"));
  env.grant({ tier: "T2", verbs: ["device.write"], scope: { sandbox_roots: [env.sandbox] } });
  const r = await env.broker().call({ verb: "device.write", params: [path.join(env.sandbox, "escape", "new.txt"), "x"] });
  assert.equal(r.status, "REFUSED");
  assert.equal(r.reason, "TIER_ABOVE_GRANT", "outside the sandbox the write promotes to T3, above the T2 grant");
  assert.equal(env.calls.length, 0);
});

test("a granted root that is itself a link still matches its own contents", async () => {
  const { env } = linkedEnv();
  const real = path.join(env.root, "real-sandbox");
  mkdirSync(real);
  dirLink(real, env.sandbox);
  env.grant({ tier: "T2", verbs: ["device.write"], scope: { sandbox_roots: [env.sandbox] } });
  const r = await env.broker().call({ verb: "device.write", params: [path.join(env.sandbox, "a.txt"), "x"] });
  assert.equal(r.status, "OK", JSON.stringify(r));
});

test("realTarget resolves links and keeps segments that do not exist yet", () => {
  const { env, granted } = linkedEnv();
  dirLink(env.dirs.root, path.join(granted, "l"));
  const got = realTarget(path.join(granted, "l", "keys", "missing", "file.txt"));
  assert.equal(got.toLowerCase(), path.join(realTarget(env.dirs.root), "keys", "missing", "file.txt").toLowerCase());
});
