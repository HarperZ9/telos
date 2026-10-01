// Act-time ref resolution (DESIGN.md 5, "Resolution at act time"). Given a ref
// the model supplied, re-read the live element, recompute its fingerprint and
// compare it to the one the snapshot recorded in the epoch store. The result
// feeds the action digest, so a human approves a specific element and a
// re-rendered page with a different element at the same id cannot borrow the
// approval.
//
// Fallback order (5.2): a ref is primary; an accessible-name query resolves to
// a ref and is recorded as resolution "query"; coordinates raise the tier to a
// T3 floor and are recorded as "coordinate". This module handles ref and query;
// the coordinate path is the broker's, which sets the floor.
import { describeRef } from "../native-control/browser-ref.mjs";
import { lookupRef } from "./epochs.mjs";
import { uiaFingerprint } from "./refs.mjs";
import { uiaNodeFacts } from "./snapshot.mjs";

function fail(code, detail) {
  return { ok: false, code, reason: detail ?? code };
}

// Resolve a browser ref. `attach` returns a CDP session for the ref's target.
export async function resolveBrowserRef(ref, { attach, dir, now = Date.now() }) {
  const known = lookupRef(ref, { dir, now });
  if (!known.ok) return fail(known.code);
  const { backendNodeId } = known.parsed;
  const { session } = await attach(known.parsed.target8);
  try {
    const live = await describeRef(session, backendNodeId);
    if (!live.ok) return fail(live.code ?? "TARGET_NOT_FOUND");
    if (live.secret) return fail("SECRET_FIELD", "target is a credential, one-time-code or card field");
    if (live.fingerprint !== known.fingerprint) {
      return { ok: false, code: "FINGERPRINT_MISMATCH", reason: "the element at this ref changed since the snapshot",
        recorded: known.fingerprint, observed: live.fingerprint };
    }
    return { ok: true, resolution: "ref", surface: "browser", target_ref: ref, backendNodeId,
      target_fingerprint: live.fingerprint, secret: false, target: known.target };
  } finally {
    session.close();
  }
}

// Resolve a native ref. `resolveUia(hwnd, ridMatch)` runs uia.ps1 `resolve`.
export async function resolveUiaRef(ref, { resolveUia, dir, now = Date.now() }) {
  const known = lookupRef(ref, { dir, now });
  if (!known.ok) return fail(known.code);
  const { hwnd, runtimeId } = known.parsed;
  let live;
  try {
    live = await resolveUia(hwnd, `rid:${runtimeId.join(".")}`);
  } catch (err) {
    return fail("TARGET_NOT_FOUND", err.message);
  }
  if (!live?.ok) return fail("TARGET_NOT_FOUND");
  if (live.element?.isPassword) return fail("SECRET_FIELD", "target is a protected field");
  const fingerprint = uiaFingerprint(uiaNodeFacts(live.element, live.process));
  if (fingerprint !== known.fingerprint) {
    return { ok: false, code: "FINGERPRINT_MISMATCH", reason: "the element at this ref changed since the snapshot",
      recorded: known.fingerprint, observed: fingerprint };
  }
  return { ok: true, resolution: "ref", surface: "native", target_ref: ref, hwnd, runtimeId,
    target_fingerprint: fingerprint, secret: false, target: known.target };
}

export async function resolveRef(ref, hooks) {
  const surface = String(ref).startsWith("b:") ? "browser" : String(ref).startsWith("u:") ? "native" : null;
  if (surface === "browser") return resolveBrowserRef(ref, hooks);
  if (surface === "native") return resolveUiaRef(ref, hooks);
  return fail("BAD_REF", "ref names neither a browser nor a native surface");
}
