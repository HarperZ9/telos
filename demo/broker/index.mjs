// Default wiring for the broker on this workstation: operator state under
// %LOCALAPPDATA%/Telos (or $XDG_STATE_HOME/telos), the local Telos key, an
// append-only receipt file per session, and read-only live drivers for target
// resolution. With no key or no grant, everything above T0 is refused.
import path from "node:path";
import { createBroker } from "./dispatch.mjs";
import { loadPublicKey } from "./keys.mjs";
import { stateDirs } from "./paths.mjs";
import { JsonlRecorder } from "./recorder.mjs";
import { liveDrivers } from "./resolve.mjs";

export { createBroker, actionDigest } from "./dispatch.mjs";
export { VERBS, LADDER, TIERS, verbSpec, effectiveTier } from "./tiers.mjs";

export function defaultBroker({ executor, browser, app, port, sessionId, dirs = stateDirs(), notify } = {}) {
  // A hold is redeemable only by the session that raised it, so the CLI uses a
  // stable session name across the two invocations of one held action.
  const session = sessionId || process.env.TELOS_SESSION || "cli";
  return createBroker({
    dirs,
    publicKey: loadPublicKey(dirs.keys),
    executor,
    recorder: new JsonlRecorder(path.join(dirs.receipts, `broker-${session}.jsonl`)),
    sessionId: session,
    drivers: liveDrivers({ browser, app, port }),
    notify,
  });
}
