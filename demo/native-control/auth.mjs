// Authentication surface. The operator establishes auth ONCE, by signing in
// inside the dedicated Telos profile (see browser.mjs resolveUserDataDir); the
// tool then operates inside those persisted sessions. This module never reads
// the cookie store or decrypts tokens. It OBSERVES the live page to report
// whether you are signed in, and it drives the login as a handoff: navigate to
// the sign-in page, then give you the keyboard. Session persistence does the
// rest. This is "use existing authentication" without a harvest step, and it
// still stops at MFA/captcha like every other personhood gate. See BOUNDARY.md.

import * as browser from "./browser.mjs";
import * as gate from "./gate.mjs";
import * as vault from "./vault.mjs";

// Pure: an in-page expression that reports auth signals on the current page.
export function authCheckExpression() {
  return `(() => {
    const q = (s) => document.querySelectorAll(s).length;
    const text = ((document.body && document.body.innerText) || "").toLowerCase();
    const loginForm = q('input[type=password]') > 0;
    const account = q('[aria-label*="account" i],[data-testid*="account" i],[class*="avatar" i],a[href*="logout" i],a[href*="signout" i],button[aria-label*="profile" i]') > 0
      || /(sign out|log out|my account|your profile)/.test(text);
    return { host: location.host, url: location.href, loginForm, account };
  })()`;
}

// Pure: classify auth state from the scan. Unknown is an honest answer -- the
// tool does not guess a session is valid from the absence of a login form.
export function classifyAuth(scan = {}) {
  if (scan.loginForm) return { authed: false, reason: "login-form-present" };
  if (scan.account) return { authed: true, reason: "account-affordance-present" };
  return { authed: "unknown", reason: "no-decisive-signal" };
}

// Report whether the current page shows a signed-in session.
export async function check(session) {
  const res = await session.send("Runtime.evaluate", { expression: authCheckExpression(), returnByValue: true });
  const scan = res.result?.value || {};
  return { ...classifyAuth(scan), host: scan.host, url: scan.url };
}

// Drive a one-time login as a handoff. Navigate to url (if given); if the page
// is a login/MFA gate or not clearly authed, hand the keyboard to the operator.
// The tool never types credentials here -- the operator signs in, and the
// session persists in the dedicated profile for later reuse.
export async function login(session, url, { useVault = true } = {}) {
  if (url) await browser.navigate(session, url);
  const st0 = await check(session);
  // Host-scoped credential fill from the vault (if unlocked and not already in).
  // Fills username + password only; MFA still hands off below.
  let vaultFill = null;
  if (useVault && st0.authed !== true && process.env.TELOS_VAULT_PASSPHRASE) {
    try { vaultFill = await vault.fillLogin(session); }
    catch (err) { vaultFill = { filled: false, reason: err.message }; }
  }
  const verdict = await gate.detect(session);
  const st = await check(session);
  if (st.authed === true && verdict.gate !== "login" && verdict.gate !== "mfa") {
    return { alreadyAuthed: true, host: st.host, url: st.url, vault: vaultFill };
  }
  await gate.banner(session, {
    gate: verdict.gate === "none" ? "login" : verdict.gate,
    action: vaultFill?.filled
      ? "Credentials filled from your vault. Review, complete MFA if prompted, and sign in."
      : "Sign in here once. Your session persists in the Telos profile; the tool reuses it after.",
  });
  return {
    handoff: true,
    gate: verdict.gate,
    host: st.host,
    vault: vaultFill,
    next_action: vaultFill?.filled
      ? "Review the filled login, complete any MFA yourself, and submit."
      : "Operator signs in; the session persists in the dedicated profile for later reuse.",
  };
}
