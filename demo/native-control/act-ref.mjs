// Act-by-ref for the CLI dispatcher (DESIGN.md 5.3).
import * as browser from "./browser.mjs";

// Act-by-ref: params[0] is a snapshot ref (b:<epoch>:<target>:<node>), never
// a raw node id. The element is re-resolved at act time against the
// fingerprint the snapshot recorded; a changed, stale, unknown or secret
// element refuses here even if a caller reached the driver without the broker.
export async function actByRef(session, verb, params, { resolve } = {}) {
  const resolveBrowserRef = resolve ?? (await import("../surface/resolve.mjs")).resolveBrowserRef;
  const borrowed = { session: { send: (...a) => session.send(...a), close() {} } };
  const live = await resolveBrowserRef(params[0], { attach: async () => borrowed });
  if (!live.ok) throw Object.assign(new Error(`${live.code}: ${live.reason ?? live.code}`), { code: live.code });
  const id = live.backendNodeId;
  const text = params.slice(1).join(" ");
  if (verb === "click-ref") return browser.clickRef(session, id);
  if (verb === "fill-ref") return browser.fillRef(session, id, text, { secret: live.secret === true });
  if (verb === "select-ref") return browser.selectRef(session, id, text);
  return browser.focusRef(session, id);
}
