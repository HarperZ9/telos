// Outward-publish authorization. An irreversible outward action (email send,
// social post, product listing) requires explicit per-call operator
// authorization: the verb runs only when the call passes `--authorize`.
// Otherwise it STAGES -- it reports what it would publish and stops -- so
// "run the outreach in succession" can never become a hands-off blast. The
// operator stays the one who authorizes each outward action. See BOUNDARY.md.

export const OUTWARD_VERBS = new Set(["send", "linkedin", "gumroadlist"]);

export function isOutward(verb) {
  return OUTWARD_VERBS.has(verb);
}

// Build the "staged, not sent" receipt for an unauthorized outward verb.
export function stagedOutward(verb, params, flags) {
  const text = (params.join(" ") || flags.text || flags.body || flags.description || "").slice(0, 400);
  return {
    staged: true,
    authorized: false,
    verb,
    would: { to: flags.to || null, subject: flags.subject || null, text },
    next_action: "Review the content above, then re-run with --authorize to publish. This tool does not send outward on its own.",
  };
}
