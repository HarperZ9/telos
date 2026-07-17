// Draft composer for outreach. Fills a template from target fields (from scrape/
// enrich or supplied by the operator) plus the operator's signature, and checks
// commercial-email compliance BEFORE anything can be authorized to send. This is
// the friction the outreach use-case actually hits: writing personalized,
// compliant messages. It drafts; the operator reviews and authorizes.
//
// Templates use {{token}} placeholders. Unresolved tokens are reported in
// `missing` and left visible in the text (never silently blanked) so the
// operator never sends "Hi {{name}}".

// Pure: render a template against a merged field dict. Returns {text, missing}.
export function render(template, fields = {}) {
  const missing = [];
  const text = String(template || "").replace(/\{\{\s*([\w.]+)\s*\}\}/g, (_, key) => {
    const v = fields[key];
    if (v == null || v === "") { missing.push(key); return `{{${key}}}`; }
    return String(v);
  });
  return { text, missing: [...new Set(missing)] };
}

// Pure: CAN-SPAM style check for commercial outreach. Requires an unsubscribe/
// opt-out cue and the sender's physical postal address in the body. Job
// applications are not commercial email; this gate is for `send` (cold email).
export function complianceCheck(body, { senderAddress } = {}) {
  const text = String(body || "");
  const missing = [];
  const hasOptOut = /unsubscribe|opt[\s-]?out|reply\s+.*stop|no longer wish to receive/i.test(text);
  if (!hasOptOut) missing.push("opt-out / unsubscribe line");
  const addr = String(senderAddress || process.env.TELOS_SENDER_ADDRESS || "").trim();
  if (!addr) missing.push("configured sender address (TELOS_SENDER_ADDRESS)");
  else if (!text.includes(addr)) missing.push("physical mailing address in the body");
  return { compliant: missing.length === 0, missing };
}

// Compose a draft: render, then attach compliance status. Never sends.
export function draft({ template, target = {}, sender = {} } = {}) {
  const fields = {
    ...target,
    sender_name: sender.name || "",
    sender_address: sender.address || process.env.TELOS_SENDER_ADDRESS || "",
    unsubscribe: sender.unsubscribe || "",
  };
  const { text, missing } = render(template, fields);
  const compliance = complianceCheck(text, { senderAddress: fields.sender_address });
  return {
    text,
    missing,
    compliance,
    ready: missing.length === 0 && compliance.compliant,
    note: missing.length || !compliance.compliant
      ? "Fill missing fields and satisfy compliance before authorizing a send."
      : "Draft complete and compliant; review, then send with --authorize.",
  };
}
