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
import * as captcha from "./captcha.mjs";
import * as network from "./network.mjs";
import { Ledger } from "./ledger.mjs";

// Registry: act-name -> async (ctx, step) => result. ctx = { session, profile, adapter }.
function defaultRegistry() {
  const R = new Map();
  const num = (v, d) => (v == null ? d : Number(v));
  R.set("navigate", (c, s) => browser.navigate(c.session, s.url));
  R.set("stealth", (c) => behave.stealth(c.session));
  R.set("warmup", (c, s) => behave.warmup(c.session, { moves: num(s.moves, 9), totalMs: num(s.totalMs, 4200) }));
  R.set("upload", (c, s) => browser.uploadFile(c.session, s.selector || 'input[type=file]', s.file));
  R.set("click", (c, s) => browser.click(c.session, s.selector));
  R.set("fill", (c, s) => browser.setValue(c.session, s.selector, s.value));
  R.set("waitfor", (c, s) => browser.waitFor(c.session, s.selector, num(s.timeoutMs, 8000)));
  R.set("eval", (c, s) => browser.evalJs(c.session, s.expression));
  R.set("evalfile", (c, s) => browser.evalJs(c.session, readFileSync(s.file, "utf-8")));
  R.set("snapshot", async (c) => ({ state: await browser.pageState(c.session) }));
  R.set("autofill", (c) => forms.fill(c.session, c.profile));
  R.set("spatialfill", (c) => forms.spatialFill(c.session, c.profile));
  R.set("behave.click", (c, s) => behave.humanClick(c.session, num(s.x), num(s.y)));
  R.set("behave.type", (c, s) => behave.humanType(c.session, s.text));
  R.set("behave.select", (c, s) => behave.selectpick(c.session, s.selector, s.option));
  R.set("captcha", (c, s) => captcha.solve(c.session, { prompt: s.prompt || "" }));
  R.set("token", (c, s) => network.recaptchaToken(c.session, { action: s.action || "submit", siteKey: s.siteKey }));
  R.set("apifetch", (c, s) => network.apiFetch(c.session, { url: s.url, body: s.body, method: s.method || "POST", headers: s.headers, contentType: s.contentType }));
  R.set("netcap", (c, s) => network.capture(c.session, { durationMs: s.durationMs || 3000, urlFilter: s.urlFilter || "" }));
  return R;
}

async function loadAdapter(name) {
  if (!name) return null;
  const mod = await import(`./adapters/${name}.mjs`);
  return mod.default || mod;
}

export async function runWorkflow(workflow, { session, registry = defaultRegistry() } = {}) {
  const ledger = new Ledger({ name: workflow.name || "native-control-run" });
  const profile = workflow.profile && workflow.profile !== "default"
    ? (typeof workflow.profile === "string" ? JSON.parse(workflow.profile) : workflow.profile)
    : forms.defaultProfile();
  const adapter = await loadAdapter(workflow.adapter);
  const ctx = { session, profile, adapter };
  const onError = workflow.onError || "halt";
  const summary = { ran: 0, ok: 0, failed: 0 };

  for (const step of workflow.steps || []) {
    const id = step.id || `${step.act}#${summary.ran}`;
    summary.ran++;
    try {
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
