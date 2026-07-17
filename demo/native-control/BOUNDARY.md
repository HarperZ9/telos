# The personhood boundary

`native-control` automates work on the operator's own machine and accounts. It
holds one invariant, and the whole design follows from it:

> **Automate everything that expresses the operator's own intent, up to — never
> through — a personhood gate. Never forge the signals a third party uses to
> decide whether a human is present.**

A **personhood gate** is any point where a counterparty asks the operator to
personally prove they are human, authenticate, attest to truth, sign, or pay:

| gate | example | who must act |
|------|---------|--------------|
| `captcha` | reCAPTCHA / hCaptcha / Turnstile, "are you human" | operator |
| `login` | a password field | operator |
| `mfa` | a one-time / 2FA code | operator |
| `legal` | "I certify … under penalty", an attestation of truth | operator |
| `esign` | a typed or drawn signature | operator |
| `payment` | a card / payment field | operator (tool never moves money) |

Reaching one is **not** a wall to route around. It is the designed **handoff**:
the tool has done all the labor (find, research, fill, assemble, track) and the
operator does the one thing only they can legitimately do.

## Why this is the boundary (not "automated vs manual")

"Operator in the driver's seat" is only true if the operator is the one who
answers "are you human?" — because they are. Forging that answer (spoofing
`navigator.webdriver`, seeding fake behavior, solving a CAPTCHA, harvesting a
score token) removes the human at the exact gate that asks for one. That is the
opposite of operator-controlled. So the tool never does it on this path.

The predicate is a single question the code can check on any page:

> Does this step assert to an outside party that a human is present, when the
> truth is that automation is acting? **Yes → hand off. No → automate.**

## How it is enforced in code

- `gate.mjs` — `detect(session)` classifies the terminal gate. `classifyGate()`
  is pure and unit-tested.
- `prepare.mjs` — `prepare()` fills from the profile, detects the gate and the
  still-required fields, and **stops**. `submitted` is always `false`.
- `runner.mjs` — the `handoff` action raises `HandoffSignal`, which halts a
  workflow as `paused_for_operator` regardless of `onError`. There is **no**
  `stealth`, `warmup`, `captcha`, or `token` action in the registry.
- Outward publishes (`send`, `linkedin`, `gumroadlist`) stage unless the call
  passes `--authorize`, so "run the outreach in succession" can never mean a
  hands-off blast.
- `redteam/` — the personhood-forging code still exists, walled off, for
  red-teaming a property you **own**. Every entry point calls
  `assertOwnProperty()` and refuses on any host you have not named. It is not
  imported by the dispatcher or the runner.

## Authentication and the vault

"Use existing authentication" means: you sign in once, inside the dedicated
Telos Chrome profile (`browser.mjs resolveUserDataDir`), and the tool operates
inside that persisted session. `auth check` observes whether the live page shows
a signed-in state (it reads the page, never the cookie store or tokens);
`auth login <url>` navigates and hands you the keyboard.

`vault.mjs` is a password-manager contract, not a harvester:

- Secrets are AES-256-GCM encrypted at rest, key derived (scrypt) from
  `TELOS_VAULT_PASSPHRASE`. No passphrase, no write: it never stores plaintext.
- A credential fills **only** when the live page's origin exactly matches the
  stored host (anti-phishing). The check runs both in `vault.mjs` and again
  inside the injected page expression.
- It holds **username + password only**. It does not store or fill MFA/TOTP.
  MFA stays a handoff, the one live checkpoint that bounds what any bug or
  injected page instruction can do while acting in your session.
- `list()` and every receipt exclude the secret; the witnessed ledger carries no
  credentials by construction.

## Discovery and outreach

`scrape`/`enrich` read public pages to find targets and their public contact or
apply links. Results feed the `queue`, which `prepare`s each item (fill + gate
detection) and **stages** it for your review. Outward publishes
(`send`/`linkedin`/`gumroadlist`) require `--authorize` on the call. Nothing is
submitted or sent from discovery or the queue on its own.

## Reputation guards (the asset careless automation burns)

The tool protects the operator's own sending reputation before it does anything
outward:

- `compose` drafts a personalized message from a template + target fields and
  leaves unresolved tokens visible (never sends "Hi {{name}}").
- `send` (cold email) must pass a CAN-SPAM check: an opt-out line and the
  operator's physical address (`TELOS_SENDER_ADDRESS`), unless
  `TELOS_SKIP_COMPLIANCE` is explicitly set.
- `outreach-log.mjs` refuses to email the same recipient twice (`--resend`
  overrides) and rate-limits sends (default 20/hour, `TELOS_SEND_MAX_PER_HOUR`).
  A queue run also spaces navigations (`TELOS_QUEUE_DELAY_MS`) so it does not
  hammer a host.
- `status` shows queue counts, vault hosts (no secrets), and the send-log
  summary at a glance.

These guards stage a reason and stop rather than send, so an automation misfire
costs a message, not the account.

## What the operator still does

Solve the CAPTCHA, sign in, enter the 2FA code, check the legal box if it is
true, sign, pay, and click the final submit/post. The tool gets you to that
point with everything ready, and records a witnessed receipt of exactly what it
prepared and what it left for you.
