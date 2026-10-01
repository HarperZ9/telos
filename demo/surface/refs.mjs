// Accessibility-tree element refs (DESIGN.md section 5).
//
// A ref names one element in one snapshot epoch:
//   browser  b:<epoch>:<target8>:<backendNodeId>
//   native   u:<epoch>:<hwnd>:<runtimeId joined by .>
// A ref is valid for its epoch and for REF_TTL_MS. At act time the element is
// re-resolved and its fingerprint recomputed; a mismatch refuses the act, and
// the fingerprint enters the action digest, so an approval binds one element.
// Pure functions only: no driver, no file, no clock unless passed in.
import { createHash, randomBytes } from "node:crypto";

export const REF_TTL_MS = 60_000;
export const BOX_QUANTUM = 8;
export const MAX_SNAPSHOT_NODES = 4000;

// Flywheel browser_control SECRET_FIELDS, plus the input types and autocomplete
// tokens that mark credential, one-time-code and card fields. Such fields are
// redacted in snapshots and can never be a target.
export const SECRET_MARKS = Object.freeze(["password", "passwd", "pwd", "otp", "mfa", "2fa", "cvv",
  "cvc", "card", "cardnumber", "ssn", "secret", "token", "apikey", "api_key", "private_key", "seed_phrase"]);
const SECRET_AUTOCOMPLETE = /^(current-password|new-password|one-time-code|cc-[a-z-]+)$/;

function sha256(text) {
  return createHash("sha256").update(String(text), "utf8").digest("hex");
}

// Sorted keys, compact separators: the same canonical form the receipt core uses.
export function canonical(value) {
  if (value === null || typeof value !== "object") return JSON.stringify(value);
  if (Array.isArray(value)) return `[${value.map(canonical).join(",")}]`;
  return `{${Object.keys(value).sort().map((k) => `${JSON.stringify(k)}:${canonical(value[k])}`).join(",")}}`;
}

export function newEpoch(now = Date.now(), rand = () => randomBytes(3).toString("hex")) {
  return `e${Math.floor(now).toString(36)}${rand()}`;
}

export function epochTime(epoch) {
  const m = /^e([0-9a-z]+?)([0-9a-f]{6})$/.exec(String(epoch));
  return m ? parseInt(m[1], 36) : NaN;
}

function refError(code, detail) {
  return Object.assign(new Error(`${code}: ${detail}`), { code });
}

export function formatBrowserRef({ epoch, targetId, backendNodeId }) {
  if (!Number.isSafeInteger(backendNodeId) || backendNodeId < 1) throw refError("BAD_REF", "backendNodeId");
  return `b:${epoch}:${String(targetId).slice(0, 8)}:${backendNodeId}`;
}

export function formatUiaRef({ epoch, hwnd, runtimeId }) {
  const ids = (runtimeId ?? []).map(Number);
  if (!Number.isSafeInteger(Number(hwnd)) || !ids.length || ids.some((n) => !Number.isSafeInteger(n))) {
    throw refError("BAD_REF", "hwnd or runtimeId");
  }
  return `u:${epoch}:${Number(hwnd)}:${ids.join(".")}`;
}

export function parseRef(ref) {
  const m = /^([bu]):(e[0-9a-z]+):([^:]+):([0-9.-]+)$/.exec(String(ref));
  if (!m) throw refError("BAD_REF", "not a snapshot ref");
  const [, kind, epoch, owner, id] = m;
  if (kind === "b") {
    const backendNodeId = Number(id);
    if (!Number.isSafeInteger(backendNodeId) || backendNodeId < 1) throw refError("BAD_REF", "backendNodeId");
    return { surface: "browser", epoch, target8: owner, backendNodeId };
  }
  const hwnd = Number(owner);
  const runtimeId = id.split(".").map(Number);
  if (!Number.isSafeInteger(hwnd) || runtimeId.some((n) => !Number.isSafeInteger(n))) throw refError("BAD_REF", "uia ids");
  return { surface: "native", epoch, hwnd, runtimeId };
}

// STALE_REF when the epoch is older than the TTL or unparseable.
export function checkFresh(ref, now = Date.now(), ttl = REF_TTL_MS) {
  const { epoch } = parseRef(ref);
  const born = epochTime(epoch);
  if (!Number.isFinite(born) || now - born > ttl || born - now > ttl) return { ok: false, code: "STALE_REF" };
  return { ok: true };
}

export function quantizeBox(box, q = BOX_QUANTUM) {
  if (!box) return null;
  const [x, y, w, h] = Array.isArray(box) ? box : [box.x, box.y, box.width, box.height];
  if (![x, y, w, h].every(Number.isFinite)) return null;
  return [x, y, w, h].map((n) => Math.floor(n / q) * q);
}

export function ancestorHash(path) {
  return sha256((path ?? []).map(String).join("/"));
}

export function browserFingerprint({ role, name, valueKind, frameId, ancestors, box }) {
  return sha256(canonical({ s: "b", role: role ?? null, name: name ?? null, value_kind: valueKind ?? null,
    frame: frameId ?? null, ancestors: ancestorHash(ancestors), box: quantizeBox(box) }));
}

export function uiaFingerprint({ controlType, name, automationId, className, processImage, ancestors, box }) {
  return sha256(canonical({ s: "u", type: controlType ?? null, name: name ?? null, aid: automationId ?? null,
    cls: className ?? null, proc: processImage ?? null, ancestors: ancestorHash(ancestors), box: quantizeBox(box) }));
}

export function isSecretField({ name, automationId, inputType, autocomplete, id } = {}) {
  if (String(inputType ?? "").toLowerCase() === "password") return true;
  if (SECRET_AUTOCOMPLETE.test(String(autocomplete ?? "").toLowerCase().trim())) return true;
  return [name, automationId, id].some((text) => {
    const t = String(text ?? "").toLowerCase().replace(/[-\s]/g, "");
    return t && SECRET_MARKS.some((mark) => t.includes(mark.replace(/[-\s]/g, "")));
  });
}
