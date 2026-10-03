// The reach doctor: which channels work for this user right now. It reads
// environment variable names and nothing else. It makes no network call,
// writes no file and starts no process, so it is safe to run anywhere.
import { userAgent } from "./identity.mjs";
import { CHANNELS, CHECKED_ON, NO_ROUTE } from "./channels.mjs";
import { traceProvider } from "./receipt.mjs";

export const DOCTOR_SCHEMA = "telos.reach-doctor/v1";

const present = (env, name) => typeof env[name] === "string" && env[name].trim() !== "";

/** Status of one channel from the environment alone. */
export function channelStatus(channel, env = process.env) {
  const missing = channel.env.filter((name) => !present(env, name));
  const auth = Object.fromEntries([...channel.env, ...channel.optionalEnv].map((name) => [name, present(env, name) ? "set" : "unset"]));
  let status;
  if (channel.id === "x-session") status = "user-present only";
  else if (missing.length) status = "needs credentials";
  else status = "ready";
  return {
    id: channel.id,
    name: channel.name,
    status,
    missing,
    auth,
    route: channel.route,
    tool: channel.tool,
    cost: channel.cost,
    covers: channel.covers,
    leaves_out: channel.leaves_out,
  };
}

/** The full doctor report. Pure: same env in, same report out. */
export function reachDoctor(env = process.env) {
  const channels = CHANNELS.map((channel) => channelStatus(channel, env));
  const ready = channels.filter((c) => c.status === "ready").map((c) => c.id);
  return {
    schema: DOCTOR_SCHEMA,
    checked_on: CHECKED_ON,
    side_effects: "none: reads environment variable names only; no network, no file writes, no processes",
    user_agent: userAgent(env),
    summary: { ready: ready.length, total: channels.length, ready_ids: ready },
    channels,
    no_permitted_route: NO_ROUTE,
    trace: traceProvider(env),
  };
}

/** One line per channel for a terminal. */
export function formatDoctor(report) {
  const width = Math.max(...report.channels.map((c) => c.id.length));
  const lines = report.channels.map((c) => `${c.id.padEnd(width)}  ${c.status.padEnd(18)}  ${c.missing.length ? `set ${c.missing.join(", ")}` : c.cost}`);
  return [`reach doctor  ${report.summary.ready}/${report.summary.total} channels ready`, ...lines, "", report.trace.line].join("\n");
}
