// Input pacing in native-control/behave.mjs. Every wait is a fixed, documented
// delay whose only job is to let the target page process the previous event.
// Nothing about the timing is random.
//
// The tests drive the public workflow actions (behave.type, behave.select,
// behave.click) with a fake CDP session. No browser starts. Every timer delay
// is recorded and resolved at once, and every call to Math.random is counted.
import test from "node:test";
import assert from "node:assert/strict";
import { runWorkflow } from "./native-control/runner.mjs";
import * as behave from "./native-control/behave.mjs";

function fakeSession() {
  return {
    async send(method) {
      if (method === "Runtime.evaluate") return { result: { value: { url: "about:blank", host: "" } } };
      return {};
    },
  };
}

async function recordTimers(fn) {
  const delays = [];
  let draws = 0;
  const realTimeout = globalThis.setTimeout;
  const realRandom = Math.random;
  globalThis.setTimeout = (cb, ms, ...args) => {
    delays.push(ms);
    return realTimeout(cb, 0, ...args);
  };
  Math.random = () => {
    draws += 1;
    return realRandom();
  };
  try {
    const result = await fn();
    return { result, delays, draws };
  } finally {
    globalThis.setTimeout = realTimeout;
    Math.random = realRandom;
  }
}

const workflow = {
  name: "input-timing",
  profile: {},
  steps: [
    { id: "type", act: "behave.type", text: "abc" },
    { id: "select", act: "behave.select", selector: "#country", option: "Canada" },
    { id: "click", act: "behave.click", x: 10, y: 20 },
  ],
};

test("workflow input actions draw no random numbers and repeat the same waits", async () => {
  const first = await recordTimers(() => runWorkflow(workflow, { session: fakeSession() }));
  const second = await recordTimers(() => runWorkflow(workflow, { session: fakeSession() }));
  assert.equal(first.result.summary.failed, 0, JSON.stringify(first.result.ledger));
  assert.equal(first.draws + second.draws, 0, "input pacing drew a random number");
  assert.deepEqual(first.delays, second.delays);
  const typed = first.delays.slice(0, 3);
  assert.equal(new Set(typed).size, 1, `per-character waits differ: ${typed}`);
});

test("the waits are the documented constants", async () => {
  const delays = behave.INPUT_DELAYS_MS;
  assert.ok(Object.isFrozen(delays), "INPUT_DELAYS_MS must be frozen");
  for (const [name, ms] of Object.entries(delays)) {
    assert.ok(Number.isInteger(ms) && ms > 0, `${name} is not a positive integer`);
  }
  const run = await recordTimers(() => runWorkflow(workflow, { session: fakeSession() }));
  const expected = [delays.character, delays.character, delays.character, delays.popupOpen];
  assert.deepEqual(run.delays.slice(0, 4), expected);
});

test("key-event typing waits the documented keystroke delay per character", async () => {
  const sent = [];
  const session = { async send(method, params) { sent.push({ method, params }); return {}; } };
  const run = await recordTimers(() => behave.typeKeys(session, "hi"));
  assert.deepEqual(run.result, { typed: 2 });
  assert.equal(run.draws, 0);
  assert.deepEqual(run.delays, [behave.INPUT_DELAYS_MS.keystroke, behave.INPUT_DELAYS_MS.keystroke]);
  assert.equal(sent.filter((s) => s.method === "Input.dispatchKeyEvent").length, 6);
});

test("no exported input function is named for looking like a person", () => {
  const names = Object.keys(behave);
  assert.deepEqual(names.filter((name) => /^human/i.test(name)), []);
  for (const want of ["clickAt", "typeText", "typeKeys", "scroll", "selectpick", "INPUT_DELAYS_MS"]) {
    assert.ok(names.includes(want), `behave.mjs should export ${want}`);
  }
});
