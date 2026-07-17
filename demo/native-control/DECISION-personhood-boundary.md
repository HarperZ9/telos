# Decision record: the personhood boundary

**Decision:** Build the automation tool to operate up to a personhood gate and
hand off there. Do NOT ship detection-evasion, CAPTCHA-solving, credential/
cookie harvesting, or unattended "authenticate in my place" capability on the
operator-facing path. Wall the forging code in `redteam/` for owned-host testing
only.

**Status:** Active. **Owner:** repo maintainer. **Last review:** this change.

## Context / problem

The tool automates outreach and job-application work from the operator's real,
high-reputation accounts. Earlier iterations built a stealth/fingerprint spoof,
a GPU CAPTCHA solver, a reCAPTCHA score-token harvest, and staged auto-submit
"waves." The platforms (Reddit, reCAPTCHA on ATS forms) actively blocked the
automated sessions. The pull was to escalate the arms race.

## Alternatives considered

1. **Full evasion + auth-in-your-place (rejected).** Forge personhood signals,
   solve CAPTCHAs, harvest cookies/tokens, treat tool-launch as blanket
   downstream auth. Rejected: it transmits false signals to third parties (a
   fact about *their* systems, not governed by "my machine"); it is a
   depreciating arms-race asset (negative reuse horizon); and it maximizes
   recursive debt (any input-handling bug becomes full-identity compromise, as
   the adversarial review's workflow-JSON path-traversal finding demonstrated).
2. **Personhood-gate handoff (chosen).** Automate everything that expresses the
   operator's own intent on their own machine/accounts, stop at any point a
   third party asks the operator to prove humanity, authenticate, attest, sign,
   or pay. The operator is present (it is their tool run), so the handoff costs
   seconds.
3. **Delete the forging code entirely (partial).** Rejected in favor of walling
   it in `redteam/` behind `assertOwnProperty()` for legitimately testing the
   operator's own properties; deleting it loses the defensive knowledge.

## Reasoning

Authorization is a fact about the operator's side of the wire. A CAPTCHA/MFA/
login gate is the counterparty asking "is a human present, now, for this." The
operator's authorization cannot answer that question because it is not the
question asked. "Personal use / my machine" governs what the operator does with
their own things; it does not govern what is transmitted to someone else's
system. If the operator is genuinely present and executing, the handoff is near
zero cost; the handoff is only heavy under unattended operation, which the
personal-use framing explicitly disclaims.

## Assumptions

- The operator's data for form-fill lives in a profile they curate
  (`candidate-profile.json`), which is more accurate than scraping history.
- Auth is established once by the operator in the dedicated Telos Chrome profile
  and persists there; the tool reuses it without a harvest step.

## Enforced in code (not just convention)

- `gate.mjs` classifies personhood gates; `prepare.mjs` never submits.
- `runner.mjs` forces a gate check before any `submit` act and halts on a gate
  (`HandoffSignal`), independent of workflow-author discipline.
- `runner.mjs` loads adapters from a static allowlist (no path traversal to
  `redteam/`); outward acts require explicit authorization.
- `redteam/guard.mjs` refuses forging on any host not named as owned.
- `native-control-boundary.test.mjs` asserts no evasion action is reachable.

## Review / retirement trigger

Revisit if: a platform offers a sanctioned automation API (route there instead);
a new outward/auth verb is added (extend the gate + tests); or the boundary
tests ever fail (the invariant regressed). Retirement of this record only if the
tool itself is retired.
