// Declarative workflow runner for native-control. A workflow is a JSON list of
// steps; each step's `act` resolves against a registry of action handlers that
// wrap the engine verbs. Every step's result chains into a witnessed Ledger, so
// a multi-step run (apply to a job, walk an auth flow, scrape + verify) is one
// re-checkable artifact. Per-site behavior lives in pluggable adapters under
// adapters/ (e.g. greenhouse), reached via `act: "adapter.<name>"`.
//
//   browser run <workflow.json> [--out=ledger.json]
//     workflow: { name?, adapter?, profile?, steps:[{id,act,...}], onError? }
//     onError: "halt" (default) | "record-continue"

import { readFileSync, writeFileSync } from "node:fs";
import * as browser from "./browser.mjs";
import * as forms from "./forms.mjs";
import * as behave from "./behave.mjs";
import * as network from "./network.mjs";
import * as learn from "./learn.mjs";
import * as gate from "./gate.mjs";
import * as prepare from "./prepare.mjs";
import { guardedSend } from "./guarded-send.mjs";
import { Ledger } from "./ledger.mjs";

// A step reaching a personhood gate raises this so the loop records it as a
// designed handoff (paused_for_operator) rather than an error.
export class HandoffSignal extends Error {
  constructor(verdict) {
    super(`HANDOFF: personhood gate '${verdict.gate}' -- ${verdict.action}`);
    this.name = "HandoffSignal";
    this.verdict = verdict;
  }
}

// Registry: act-name -> async (ctx, step) => result. ctx = { session, profile, adapter }.
// Note: no stealth / warmup / captcha / token actions exist here. Personhood-
// forging is not reachable from a workflow; see gate.mjs + BOUNDARY.md.
export function defaultRegistry() {
  const R = new Map();
  const num = (v, d) => (v == null ? d : Number(v));
  R.set("navigate", (c, s) => browser.navigate(c.session, s.url));
  R.set("upload", (c, s) => browser.uploadFile(c.session, s.selector || 'input[type=file]', s.file));
  R.set("click", (c, s) => browser.click(c.session, s.selector));
  R.set("fill", (c, s) => browser.setValue(c.session, s.selector, s.value));
  R.set("waitfor", (c, s) => browser.waitFor(c.session, s.selector, num(s.timeoutMs, 8000)));
  R.set("eval", (c, s) => browser.evalJs(c.session, s.expression));
  R.set("evalfile", (c, s) => browser.evalJs(c.session, readFileSync(s.file, "utf-8")));
  R.set("snapshot", async (c) => ({ state: await browser.pageState(c.session) }));
  R.set("autofill", (c) => forms.fill(c.session, c.profile));
  R.set("spatialfill", (c) => forms.spatialFill(c.session, c.profile));
  R.set("prepare", (c, s) => prepare.prepare(c.session, { profile: c.profile, adapter: c.adapter, spatial: !!s.spatial }));
  // gate: detect the terminal personhood gate (report, do not act on it).
  R.set("gate", (c) => gate.detect(c.session));
  // handoff: stop the run for the operator when a personhood gate is present.
  R.set("handoff", async (c) => {
    const v = await gate.detect(c.session);
    if (v.personhood) { await gate.banner(c.session, { gate: v.gate, action: v.action }); throw new HandoffSignal(v); }
    return { gate: "none", personhood: false };
  });
  R.set("behave.click", (c, s) => behave.humanClick(c.session, num(s.x), num(s.y)));
  R.set("behave.type", (c, s) => behave.humanType(c.session, s.text));
  R.set("behave.select", (c, s) => behave.selectpick(c.session, s.selector, s.option));
  R.set("apifetch", (c, s) => network.apiFetch(c.session, { url: s.url, body: s.body, method: s.method || "POST", headers: s.headers, contentType: s.contentType }));
  R.set("netcap", (c, s) => network.capture(c.session, { durationMs: s.durationMs || 3000, urlFilter: s.urlFilter || "" }));
  // learn (accountable learning engine) -- no browser session needed; shells to CLI.
  for (const [name, fn] of Object.entries(learn.actions)) R.set(`learn.${name}`, (c, s) => fn(s));
  // Routes through the guarded path: CAN-SPAM compliance + dedup + rate limit
  // apply to workflow sends exactly as to the `send` verb (no bypass).
  R.set("contact.send", (c, s) => guardedSend(c.session, { to: s.to, subject: s.subject, body: s.body, resend: s.resend === true }));
  return R;
}

// Static allowlist of adapters. A workflow's `adapter` field is DATA; resolving
// it by string interpolation into import() let a workflow JSON path-traverse to
// any module (e.g. "../redteam/evade"), which reached the walled-off forging
// code. Only known adapters load now.
const ADAPTERS = {
  greenhouse: () => import("./adapters/greenhouse.mjs"),
  base: () => import("./adapters/base.mjs"),
};

export async function loadAdapter(name) {
  if (!name) return null;
  const load = ADAPTERS[name];
  if (!load) throw new Error(`unknown adapter: ${name} (allowed: ${Object.keys(ADAPTERS).join(", ")})`);
  const mod = await load();
  return mod.default || mod;
}

// Pure: does this workflow act cross a submit gate? Used to force a personhood
// check before any submit, so the invariant is enforced in code, not left to
// each workflow author to remember a preceding `handoff` step.
export function isSubmitAct(act) {
  return act === "submit" || /\.submit$/.test(String(act || ""));
}

// Outward publishes that must not fire from a workflow without explicit
// authorization (step.authorize or workflow.authorize).
export const OUTWARD_ACTS = new Set(["contact.send"]);

export async function runWorkflow(workflow, { session, registry = defaultRegistry() } = {}) {
  const ledger = new Ledger({ name: workflow.name || "native-control-run" });
  const profile = workflow.profile && workflow.profile !== "default"
    ? (typeof workflow.profile === "string" ? JSON.parse(workflow.profile) : workflow.profile)
    : forms.defaultProfile();
  const adapter = await loadAdapter(workflow.adapter);
  const ctx = { session, profile, adapter };
  const onError = workflow.onError || "halt";
  const summary = { ran: 0, ok: 0, failed: 0, paused: 0 };
  let handoff = null;

  for (const step of workflow.steps || []) {
    const id = step.id || `${step.act}#${summary.ran}`;
    summary.ran++;
    try {
      // Outward publishes need explicit authorization even inside a workflow.
      if (OUTWARD_ACTS.has(step.act) && step.authorize !== true && workflow.authorize !== true) {
        ledger.append(id, { action: step.act, target: step.to || null, ok: true, result: { staged: true, next_action: "set step.authorize=true (or workflow.authorize) to publish" } });
        summary.ok++;
        continue;
      }
      // Never step through a personhood gate to submit. This is enforced here,
      // not left to the workflow author to precede submit with a handoff step.
      if (isSubmitAct(step.act)) {
        const v = await gate.detect(ctx.session);
        if (v.personhood) { await gate.banner(ctx.session, { gate: v.gate, action: v.action }); throw new HandoffSignal(v); }
      }
      let handler = registry.get(step.act);
      // adapter actions: "adapter.foo" -> adapter.foo(ctx, step)
      if (!handler && step.act.startsWith("adapter.") && adapter && typeof adapter[step.act.slice(8)] === "function") {
        handler = (c, st) => adapter[st.act.slice(8)](c, st);
      }
      if (!handler) throw new Error(`unknown action: ${step.act}`);
      const result = await handler(ctx, step);
      const entry = { action: step.act, target: step.url || step.selector || step.file || step.option || null, ok: true, result };
      ledger.append(id, entry);
      summary.ok++;
      if (step.expect && JSON.stringify(result).indexOf(step.expect) === -1) {
        throw new Error(`expect failed: "${step.expect}" not in result`);
      }
    } catch (err) {
      // A personhood gate is a designed handoff to the operator, not a failure.
      // It always halts the run regardless of onError -- the tool does not step
      // past the gate, ever.
      if (err instanceof HandoffSignal) {
        handoff = err.verdict;
        ledger.append(id, { action: step.act, target: err.verdict.gate, ok: true, paused_for_operator: true, result: err.verdict });
        summary.paused++;
        break;
      }
      const entry = { action: step.act, target: step.url || step.selector || step.file || null, ok: false, result: { error: err.message } };
      ledger.append(id, entry);
      summary.failed++;
      if (onError !== "record-continue") break;
    }
  }
  return { summary, handoff, ledger: ledger.export() };
}

// CLI entry shape: browser run <workflow.json> [--out=ledger.json]
export async function runFromPath(workflowPath, { session, out } = {}) {
  const workflow = JSON.parse(readFileSync(workflowPath, "utf-8"));
  const { summary, ledger } = await runWorkflow(workflow, { session });
  if (out) writeFileSync(out, JSON.stringify(ledger, null, 2) + "\n", "utf-8");
  return { summary, ledgerPath: out || null, ledger };
}
