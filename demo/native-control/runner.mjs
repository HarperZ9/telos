// Declarative workflow runner for native-control. A workflow is a JSON list of
// steps; each step's `act` resolves against a registry of action handlers that
// wrap the engine verbs. Every step's result chains into a witnessed Ledger, so
// a multi-step run (fill a form, check a result, verify the ledger) is one
// re-checkable artifact. 0.7.0 removed per-site adapters (the Greenhouse
// apply-and-submit adapter and the base submit): a workflow that names an
// adapter or an `adapter.*` act is refused before any step runs.
//
//   browser run <workflow.json> [--out=ledger.json]
//     workflow: { name?, profile?, steps:[{id,act,...}], onError? }
//     onError: "halt" (default) | "record-continue"

import { readFileSync, writeFileSync } from "node:fs";
import * as browser from "./browser.mjs";
import * as forms from "./forms.mjs";
import * as input from "./input.mjs";
import * as network from "./network.mjs";
import * as learn from "./learn.mjs";
import { Ledger } from "./ledger.mjs";

// Registry: act-name -> async (ctx, step) => result. ctx = { session, profile }.
function defaultRegistry() {
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
  // `behave.*` are the pre-0.6.0 names for the same fixed-pace input actions.
  for (const prefix of ["input", "behave"]) {
    R.set(`${prefix}.click`, (c, s) => input.pointerClick(c.session, num(s.x), num(s.y)));
    R.set(`${prefix}.type`, (c, s) => input.typeText(c.session, s.text, { pauseMs: s.pauseMs }));
    R.set(`${prefix}.keys`, (c, s) => input.typeKeys(c.session, s.text, { pauseMs: s.pauseMs }));
    R.set(`${prefix}.select`, (c, s) => input.selectOption(c.session, s.selector, s.option, { pauseMs: s.pauseMs }));
  }
  R.set("apifetch", (c, s) => network.apiFetch(c.session, { url: s.url, body: s.body, method: s.method || "POST", headers: s.headers, contentType: s.contentType }));
  R.set("netcap", (c, s) => network.capture(c.session, { durationMs: s.durationMs || 3000, urlFilter: s.urlFilter || "" }));
  // learn (accountable learning engine) -- no browser session needed; shells to CLI.
  for (const [name, fn] of Object.entries(learn.actions)) R.set(`learn.${name}`, (c, s) => fn(s));
  return R;
}

// Refuse removed features before the first step, so a workflow never runs half
// of its steps and then stops at a submit adapter.
function refuseRemoved(workflow) {
  if (workflow.adapter) throw new Error("workflow adapters were removed in 0.7.0");
  const step = (workflow.steps || []).find((s) => typeof s.act === "string" && s.act.startsWith("adapter."));
  if (step) throw new Error(`adapter actions were removed in 0.7.0: ${step.act}`);
}

export async function runWorkflow(workflow, { session, registry = defaultRegistry() } = {}) {
  const ledger = new Ledger({ name: workflow.name || "native-control-run" });
  const profile = workflow.profile && workflow.profile !== "default"
    ? (typeof workflow.profile === "string" ? JSON.parse(workflow.profile) : workflow.profile)
    : forms.defaultProfile();
  refuseRemoved(workflow);
  const ctx = { session, profile };
  const onError = workflow.onError || "halt";
  const summary = { ran: 0, ok: 0, failed: 0 };

  for (const step of workflow.steps || []) {
    const id = step.id || `${step.act}#${summary.ran}`;
    summary.ran++;
    try {
      const handler = registry.get(step.act);
      if (!handler) throw new Error(`unknown action: ${step.act}`);
      const result = await handler(ctx, step);
      const entry = { action: step.act, target: step.url || step.selector || step.file || step.option || null, ok: true, result };
      ledger.append(id, entry);
      summary.ok++;
      if (step.expect && JSON.stringify(result).indexOf(step.expect) === -1) {
        throw new Error(`expect failed: "${step.expect}" not in result`);
      }
    } catch (err) {
      const entry = { action: step.act, target: step.url || step.selector || step.file || null, ok: false, result: { error: err.message } };
      ledger.append(id, entry);
      summary.failed++;
      if (onError !== "record-continue") break;
    }
  }
  return { summary, ledger: ledger.export() };
}

// CLI entry shape: browser run <workflow.json> [--out=ledger.json]
export async function runFromPath(workflowPath, { session, out } = {}) {
  const workflow = JSON.parse(readFileSync(workflowPath, "utf-8"));
  const { summary, ledger } = await runWorkflow(workflow, { session });
  if (out) writeFileSync(out, JSON.stringify(ledger, null, 2) + "\n", "utf-8");
  return { summary, ledgerPath: out || null, ledger };
}
