// Outreach verb handler. Owns the discovery + publish + queue + vault surface so
// the main dispatcher stays lean. Outward publishes (send/linkedin/gumroadlist)
// stage unless the call passes --authorize; discovery and queue never publish.
// The operator authorizes each outward action. See BOUNDARY.md.

import { readFileSync } from "node:fs";
import * as scrape from "./scrape.mjs";
import * as share from "./share.mjs";
import * as vault from "./vault.mjs";
import * as queue from "./queue.mjs";
import * as compose from "./compose.mjs";
import * as sendlog from "./outreach-log.mjs";
import { guardedSend } from "./guarded-send.mjs";
import { OUTWARD_VERBS, stagedOutward } from "./outward.mjs";

export const NOT_HANDLED = Symbol("not-handled");

const VERBS = new Set([
  "targets", "scrape", "enrich", "send", "linkedin",
  "gumroadlogin", "gumroadlist", "vault", "queue", "compose", "status",
]);

export function handles(verb) {
  return VERBS.has(verb);
}

export async function handle(verb, { session, params, flags }) {
  if (!VERBS.has(verb)) return NOT_HANDLED;
  // Outward publishes stage unless the operator authorizes this call.
  if (OUTWARD_VERBS.has(verb) && flags.authorize == null) return stagedOutward(verb, params, flags);
  switch (verb) {
    case "targets":
    case "scrape":
      return scrape.targets(session, { query: flags.query, limit: params[0] ? Number(params[0]) : 12 });
    case "enrich":
      return scrape.enrich(session, { url: params[0] || flags.url });
    case "compose":
      return handleCompose(params, flags);
    case "status":
      return handleStatus();
    case "send":
      return handleSend(session, params, flags);
    case "linkedin":
      return share.linkedinPost(session, { text: params.join(" ") || flags.text });
    case "gumroadlogin":
      return share.gumroadLoginGoogle(session);
    case "gumroadlist":
      return share.gumroadList(session, { name: flags.name, description: flags.description, price: flags.price, file: flags.file });
    case "vault":
      return handleVault(params, flags);
    case "queue":
      return handleQueue(session, params, flags);
    default:
      return NOT_HANDLED;
  }
}

// Cold email routes through the single guarded path (guarded-send.mjs) so the
// reputation guards cannot be skipped by a second call site.
function handleSend(session, params, flags) {
  return guardedSend(session, {
    to: flags.to, subject: flags.subject, body: params.join(" ") || flags.body || "",
    resend: flags.resend != null,
  });
}

// Draft a personalized message from a template + target fields; never sends.
function handleCompose(params, flags) {
  const template = flags.templatefile ? readFileSync(flags.templatefile, "utf8") : (flags.template || params.join(" "));
  return compose.draft({
    template,
    target: { name: flags.name, company: flags.company, role: flags.role, url: flags.url, email: flags.to },
    sender: { name: flags.sender, address: flags.address },
  });
}

// One-glance state: queue, vault hosts (no secrets), and send-log summary.
function handleStatus() {
  const items = queue.list();
  const byStatus = items.reduce((m, it) => ((m[it.status] = (m[it.status] || 0) + 1), m), {});
  let vaultHosts = null;
  try { vaultHosts = vault.list().map((v) => v.host); } catch (err) { vaultHosts = { locked: err.message }; }
  return { queue: { total: items.length, byStatus }, vaultHosts, sends: sendlog.summary() };
}

// vault set|list|remove. The secret for `set` comes from env TELOS_VAULT_SECRET,
// never argv (argv leaks to the process list and shell history).
function handleVault(params, flags) {
  const sub = params[0];
  if (sub === "set") return vault.setEntry({ host: flags.host, username: flags.user, password: process.env.TELOS_VAULT_SECRET });
  if (sub === "list") return vault.list();
  if (sub === "remove") return vault.remove(flags.host);
  throw new Error(`unknown vault verb: ${sub} (set|list|remove)`);
}

// queue add|list|run|remove. `run` prepares each item and stages it; it never submits.
function handleQueue(session, params, flags) {
  const sub = params[0];
  if (sub === "add") return queue.add({ url: flags.url, kind: flags.kind });
  if (sub === "list") return queue.list();
  if (sub === "run") return queue.run(session, { limit: params[1] ? Number(params[1]) : 5 });
  if (sub === "remove") return queue.remove(flags.id);
  throw new Error(`unknown queue verb: ${sub} (add|list|run|remove)`);
}
