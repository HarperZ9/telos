// Shared setup for the broker tests: a throwaway state root, a real ed25519
// key, a fixed clock, fake drivers and a recording executor. No browser,
// window or device is touched.
import test from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { createBroker } from "./dispatch.mjs";
import { issueGrant, saveGrant } from "./grants.mjs";
import { decideHold, HoldStore } from "./holds.mjs";
import { generateKeys } from "./keys.mjs";
import { stateDirs } from "./paths.mjs";
import { MemoryRecorder } from "./recorder.mjs";

export const T0 = Date.parse("2026-10-01T18:00:00Z");

export function makeEnv({ windows, pageUrl = "https://example.test/form" } = {}) {
  const root = mkdtempSync(path.join(os.tmpdir(), "telos-broker-"));
  const dirs = stateDirs(path.join(root, "state"));
  const { privateKey, publicKey } = generateKeys();
  const clock = { t: T0 };
  const now = () => clock.t;
  const calls = [];
  const recorder = new MemoryRecorder();
  const drivers = {
    pageUrl: async () => pageUrl,
    listWindows: async () => windows ?? [{ title: "Untitled - Notepad", class: "Notepad", process: "notepad" }],
    which: (name) => (/^[a-z]+$/.test(name) ? path.join(root, "bin", name) : null),
  };
  const env = {
    root, dirs, privateKey, publicKey, clock, now, calls, recorder, drivers,
    sandbox: path.join(root, "sandbox"),
    executor: async (verb, params, flags) => {
      calls.push({ verb, params, flags });
      return { ok: true };
    },
    grant(spec) {
      const g = issueGrant(spec, { privateKey, publicKey, now: now(), isTTY: true });
      saveGrant(dirs.grants, g);
      return g;
    },
    broker(extra = {}) {
      return createBroker({ dirs, publicKey, executor: env.executor, recorder, sessionId: "s1", drivers, now, cwd: root, ...extra });
    },
    decide(holdId, decision = "approve") {
      const store = new HoldStore({ dir: dirs.holds, publicKey, now });
      return decideHold(store, holdId, decision, { privateKey, publicKey, isTTY: true });
    },
  };
  return env;
}

export const t3Grant = (env, extra = {}) =>
  env.grant({ tier: "T3", verbs: ["browser.click", "browser.fill", "browser.navigate"], scope: { origins: ["https://example.test"] }, max_actions: 10, ...extra });

test("the harness builds a broker that refuses with no grant", async () => {
  const env = makeEnv();
  const r = await env.broker().call({ verb: "browser.snapshot-text", params: [] });
  assert.equal(r.status, "REFUSED");
  assert.equal(r.reason, "NO_GRANT");
  assert.equal(env.calls.length, 0);
});
