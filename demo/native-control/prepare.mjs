// Prepare-and-handoff pipeline: the operator-in-the-driver's-seat path.
//
// prepare() does all the labor that expresses the operator's own intent -- fill
// the form from the candidate profile, find what is still required, detect the
// terminal gate -- and then STOPS. It never submits, and it never crosses a
// personhood gate (CAPTCHA / login / MFA / legal attestation / signature /
// payment). It hands back a witnessed receipt describing exactly what is ready
// and what only the operator can do next.
//
//   node demo/native-control.mjs browser prepare [--spatial] [--profile=path]
//
// Contrast with the quarantined redteam/ path, which forges personhood signals
// and is restricted to properties the operator owns. See BOUNDARY.md.

import * as forms from "./forms.mjs";
import * as gate from "./gate.mjs";

// Pure: list required-but-empty visible fields, so the operator knows what still
// needs them (a custom question, an unmapped answer) before they submit.
export function requiredEmptyExpression() {
  return `(() => {
    const out = [];
    const visible = (el) => { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
    for (const el of document.querySelectorAll('input,textarea,select')) {
      const t = (el.getAttribute('type') || '').toLowerCase();
      if (['hidden','submit','button','image','password'].includes(t)) continue;
      const req = el.required || el.getAttribute('aria-required') === 'true';
      const empty = el.type === 'checkbox' || el.type === 'radio' ? false : !((el.value || '') + '').trim();
      if (req && empty && visible(el)) {
        const lbl = ((el.closest('label') || {}).innerText || el.getAttribute('aria-label') || el.name || el.id || '').trim();
        out.push((lbl || '(unlabeled)').slice(0, 60));
      }
    }
    return out.slice(0, 20);
  })()`;
}

// Pure: decide the disposition from the fill report + gate + missing list.
// Never returns anything that implies the tool will cross the gate.
export function disposition(fillLog = {}, verdict = {}, missing = []) {
  if (verdict.personhood) {
    return { disposition: "operator-gated", next_action: verdict.action || gate.operatorAction(verdict.gate) };
  }
  if (fillLog && fillLog.login) {
    return { disposition: "operator-gated", next_action: gate.operatorAction("login") };
  }
  if ((missing || []).length) {
    return { disposition: "needs-operator-input", next_action: `Answer ${missing.length} required field(s), then review and submit.` };
  }
  return { disposition: "ready-to-review", next_action: gate.operatorAction("none") };
}

// Fill the page from the profile (adapter-aware), then detect the gate and the
// still-required fields. Returns a handoff receipt. Never submits.
export async function prepare(session, { profile, adapter = null, spatial = false, showBanner = true } = {}) {
  const p = profile || forms.defaultProfile();

  let fillLog;
  if (adapter && typeof adapter.fill === "function") {
    fillLog = await adapter.fill({ session, profile: p });
  } else if (spatial) {
    fillLog = await forms.spatialFill(session, p);
  } else {
    fillLog = await forms.fill(session, p);
  }

  const verdict = await gate.detect(session);

  const missRes = await session.send("Runtime.evaluate", {
    expression: requiredEmptyExpression(),
    returnByValue: true,
  });
  const missing = missRes.result?.value || [];

  const filledCount = Array.isArray(fillLog?.filled) ? fillLog.filled.length : 0;
  const disp = disposition(fillLog, verdict, missing);

  if (showBanner) {
    await gate.banner(session, { gate: verdict.gate, filled: filledCount, missing, action: disp.next_action });
  }

  return {
    prepared: true,
    submitted: false, // invariant: prepare never submits
    fill: fillLog,
    gate: { gate: verdict.gate, personhood: verdict.personhood, reasons: verdict.reasons },
    missing_required: missing,
    ...disp,
    url: verdict.scan?.url || null,
  };
}
