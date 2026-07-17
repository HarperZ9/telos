// The ONE path outbound email may take. Both the `send` verb (outreach.mjs) and
// the workflow `contact.send` action (runner.mjs) route through here, so the
// reputation guards cannot be bypassed by reaching gmailSend from a second call
// site. Order: CAN-SPAM compliance -> dedup + rate limit -> send -> record
// (only on a confirmed send). Blocks stage a reason and never send or record.

import * as contact from "./contact.mjs";
import * as compose from "./compose.mjs";
import * as sendlog from "./outreach-log.mjs";

// nowMs and sendFn injected for testability; default to wall clock + gmailSend.
export async function guardedSend(session, { to, subject, body, resend = false, skipCompliance = process.env.TELOS_SKIP_COMPLIANCE != null, nowMs, sendFn = contact.gmailSend } = {}) {
  const at = nowMs == null ? Date.now() : nowMs;
  if (!to) return { blocked: true, verb: "send", reason: "no recipient" };

  if (!skipCompliance) {
    const c = compose.complianceCheck(body || "", {});
    if (!c.compliant) {
      return { blocked: true, verb: "send", reason: "non-compliant commercial email", missing: c.missing, hint: "add an opt-out line + set TELOS_SENDER_ADDRESS, or set TELOS_SKIP_COMPLIANCE=1 to override" };
    }
  }

  const chk = sendlog.checkSend(sendlog.load(), to, { nowMs: at, resend });
  if (!chk.allow) return { blocked: true, verb: "send", reason: chk.reason };

  const result = await sendFn(session, { to, subject, body });

  // Record only a CONFIRMED send. gmailSend can return sent:false on a UI
  // failure without throwing; recording that would wrongly block a real retry.
  const confirmed = result?.confirm?.sent === true && result?.confirm?.stillCompose !== true;
  if (!confirmed) {
    return { ...result, sent: false, recorded: false, reason: "send could not be confirmed; not recorded (retry without --resend)" };
  }
  sendlog.record({ to, subject });
  return { ...result, sent: true, recorded: true, sendlog: chk.reason };
}
