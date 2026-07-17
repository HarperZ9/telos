// Personhood-gate detector. The honest inverse of a CAPTCHA solver: instead of
// forging the signals a counterparty uses to decide "is a human present," this
// module RECOGNIZES the point where a third party asks the operator to attest,
// authenticate, sign, pay, or prove humanity -- and stops there, so the operator
// crosses the gate personally. That single seam is the tool's whole boundary:
//
//   automate everything that expresses the operator's own intent on the
//   operator's own machine/account, up to (never through) a personhood gate.
//
// A "personhood gate" is any of:
//   captcha  -- reCAPTCHA / hCaptcha / Turnstile (literally "are you human")
//   login    -- a password field (authenticate as the account owner)
//   mfa      -- an OTP / 2FA code entry
//   legal    -- a checkbox/field attesting truth "under penalty", "I certify"
//   esign    -- a typed/drawn signature field
//   payment  -- a card / payment field (authorize money -- never automated)
//
// Reaching a personhood gate is not a failure to route around. It is the
// designed handoff. See BOUNDARY.md.

// Pure: a JS expression that scans the current document and returns a raw
// signal object. Evaluated in-page via CDP Runtime.evaluate (returnByValue).
export function detectGateExpression() {
  return `(() => {
    const q = (sel) => Array.from(document.querySelectorAll(sel));
    const visible = (el) => { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
    const text = ((document.body && document.body.innerText) || "").toLowerCase();

    const captchaIframes = q('iframe[src*="recaptcha"],iframe[src*="hcaptcha"],iframe[src*="challenges.cloudflare.com"],iframe[src*="turnstile"],iframe[title*="reCAPTCHA"],iframe[title*="hCaptcha"]')
      .map((e) => ({ src: e.src || "", title: e.title || "" }));
    const hasCaptchaWidget = captchaIframes.length > 0
      || q('.g-recaptcha,.h-captcha,[data-sitekey],#g-recaptcha,[class*="turnstile"]').length > 0
      || /are you (a )?human|verify you are human|i'?m not a robot|complete the captcha|security check|unusual traffic/.test(text);

    const passwords = q('input[type=password]').filter(visible).length;
    const otp = q('input[autocomplete="one-time-code"],input[name*="otp" i],input[name*="mfa" i],input[name*="2fa" i],input[aria-label*="verification code" i]').filter(visible).length;

    // Legal attestation: an unchecked checkbox / control whose surrounding text
    // asserts truth under penalty. Distinct from routine consent (terms/EEO),
    // which forms.fill may check; attestation of TRUTH is the operator's to make.
    const attestations = q('input[type=checkbox],[role=checkbox]').map((el) => {
      const lbl = ((el.closest('label') || {}).innerText || el.getAttribute('aria-label') || '').toLowerCase();
      const near = (el.closest('div,fieldset,li,section') || {}).innerText || '';
      const blob = (lbl + ' ' + near).toLowerCase();
      const isAttest = /under penalty|i certify|i attest|i declare|to the best of my knowledge|true and (complete|accurate)|electronically sign|e-?signature/.test(blob);
      return isAttest ? { checked: !!el.checked, hint: blob.slice(0, 80) } : null;
    }).filter(Boolean);

    const esign = q('input[name*="signature" i],input[aria-label*="signature" i],canvas[class*="sign" i],[class*="signature-pad" i]').filter(visible).length;
    const payment = q('input[autocomplete*="cc-number"],input[name*="card" i][name*="number" i],iframe[src*="stripe"],iframe[src*="checkout"],[class*="card-number" i]').filter(visible).length;

    return {
      url: location.href,
      host: location.host,
      hasCaptchaWidget, captchaIframes,
      passwords, otp,
      attestations,
      esign, payment,
    };
  })()`;
}

// Pure: classify a raw scan into a single gate. Ordered by precedence: the
// hardest personhood assertion wins. Returns { gate, personhood, reasons }.
export function classifyGate(scan = {}) {
  const reasons = [];
  const s = scan || {};
  if (s.hasCaptchaWidget) reasons.push("captcha-widget");
  if (s.passwords) reasons.push(`password-field(${s.passwords})`);
  if (s.otp) reasons.push(`otp-field(${s.otp})`);
  const openAttest = (s.attestations || []).filter((a) => a && a.checked === false);
  if (openAttest.length) reasons.push(`legal-attestation(${openAttest.length})`);
  if (s.esign) reasons.push(`signature-field(${s.esign})`);
  if (s.payment) reasons.push(`payment-field(${s.payment})`);

  let gate = "none";
  if (s.payment) gate = "payment";
  else if (s.esign) gate = "esign";
  else if (openAttest.length) gate = "legal";
  else if (s.hasCaptchaWidget) gate = "captcha";
  else if (s.otp) gate = "mfa";
  else if (s.passwords) gate = "login";

  return { gate, personhood: gate !== "none", reasons };
}

// Human-readable instruction for the operator at each gate class.
export function operatorAction(gate) {
  switch (gate) {
    case "captcha": return "Solve the CAPTCHA / human-check yourself, then submit.";
    case "login": return "Sign in with your own credentials, then continue.";
    case "mfa": return "Enter your one-time / 2FA code, then continue.";
    case "legal": return "Read and check the legal attestation yourself if it is true, then submit.";
    case "esign": return "Sign personally, then submit.";
    case "payment": return "Authorize any payment yourself. This tool never moves money.";
    default: return "Review the prepared fields and submit when satisfied.";
  }
}

// Run the scan in-page and classify. Session is a CDP session.
export async function detect(session) {
  const res = await session.send("Runtime.evaluate", {
    expression: detectGateExpression(),
    returnByValue: true,
  });
  if (res.exceptionDetails) throw new Error(`gate detect failed: ${res.exceptionDetails.text}`);
  const scan = res.result?.value || {};
  const verdict = classifyGate(scan);
  return { ...verdict, action: operatorAction(verdict.gate), scan };
}

// Inject an operator-facing handoff banner: honest, visible, addressed to the
// human at the keyboard (not a forged signal to the site). Summarizes what was
// prepared and what the operator must personally do.
export async function banner(session, { gate = "none", filled = 0, missing = [], action } = {}) {
  const msg = action || operatorAction(gate);
  const payload = JSON.stringify({ gate, filled, missing: missing.slice(0, 8), msg });
  const expr = `(() => {
    const d = ${payload};
    let el = document.getElementById('telos-handoff-banner');
    if (!el) { el = document.createElement('div'); el.id = 'telos-handoff-banner'; document.documentElement.appendChild(el); }
    el.setAttribute('style', 'position:fixed;z-index:2147483647;left:0;right:0;top:0;padding:10px 16px;font:600 13px system-ui,sans-serif;color:#0b0b0c;background:#ffd34e;box-shadow:0 2px 8px rgba(0,0,0,.25)');
    el.textContent = 'TELOS handoff — ' + d.msg + '  (' + d.filled + ' fields prepared' + (d.missing.length ? ', ' + d.missing.length + ' need you' : '') + ')';
    return true;
  })()`;
  try {
    await session.send("Runtime.evaluate", { expression: expr, returnByValue: true });
    return { banner: true, gate };
  } catch (err) {
    // A banner is a convenience, not a correctness requirement. Report, do not throw.
    return { banner: false, gate, error: err.message };
  }
}
