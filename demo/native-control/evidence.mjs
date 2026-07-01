import { createHash } from "node:crypto";

export const BROWSER_EVIDENCE_SCHEMA = "project-telos.browser-evidence/v1";

export const MODES = new Set([
  "work-actuate",
  "research-capture",
  "credential-logistics",
  "credential-assess",
  "lab-assess",
  "creative-capture",
]);

export const VERDICTS = new Set(["MATCH", "DRIFT", "UNVERIFIABLE"]);

export function sha256Hex(value) {
  return createHash("sha256").update(value).digest("hex");
}

export function digestRef(kind, value) {
  return `${kind}:sha256:${sha256Hex(value)}`;
}

export function makeUnavailableSummary(kind, reason) {
  const failure_code = kind === "network" ? "network_capture_unavailable" : "console_capture_unavailable";
  return { kind, verdict: "UNVERIFIABLE", failure_code, reason };
}

function snapshot(input) {
  const text = input.text ?? "";
  return {
    url: input.url ?? "",
    url_digest: digestRef("url", input.url ?? ""),
    title: input.title ?? "",
    dom_snapshot_ref: input.domArtifactRef ?? null,
    text_digest: digestRef("text", text),
    screenshot_ref: input.screenshotRef ?? null,
  };
}

export function makeBrowserEvidencePacket(input) {
  const verification = input.verification ?? { verdict: "UNVERIFIABLE", ref: null };
  return {
    schema: BROWSER_EVIDENCE_SCHEMA,
    tool: "telos.browser.evidence",
    mode: input.mode,
    session_ref: input.sessionRef ?? null,
    target_ref: digestRef("url", input.after?.url ?? input.before?.url ?? ""),
    action_receipt_ref: input.actionReceiptRef ?? null,
    action: {
      kind: input.action?.kind ?? "browser.unknown",
      selector: input.action?.selector ?? null,
      args_hash: input.action?.argsHash ?? digestRef("args", ""),
    },
    before: snapshot(input.before ?? {}),
    after: snapshot(input.after ?? {}),
    network_summary: input.networkSummary ?? makeUnavailableSummary("network", "collector-not-attached"),
    console_summary: input.consoleSummary ?? makeUnavailableSummary("console", "collector-not-attached"),
    artifact_hashes: input.artifactHashes ?? [],
    redaction_status: input.redactionStatus ?? "redacted",
    side_effect: input.sideEffect ?? { class: "read", external_write: false, reversible: true },
    verification,
    created_at: input.clock ? input.clock() : new Date().toISOString(),
  };
}

export function validateBrowserEvidencePacket(packet) {
  const failures = [];
  if (!packet || typeof packet !== "object") return { ok: false, failures: ["not_an_object"] };
  if (packet.schema !== BROWSER_EVIDENCE_SCHEMA) failures.push("schema_mismatch");
  if (!MODES.has(packet.mode)) failures.push("mode_invalid");
  if (!packet.action || typeof packet.action !== "object") failures.push("missing_action");
  if (!packet.before || typeof packet.before !== "object") failures.push("missing_before");
  if (!packet.after || typeof packet.after !== "object") failures.push("missing_after");
  if (!packet.verification || !VERDICTS.has(packet.verification.verdict)) failures.push("missing_verification");
  if (!Array.isArray(packet.artifact_hashes)) failures.push("artifact_hashes_not_array");
  return { ok: failures.length === 0, failures };
}
