import { spawnSync } from "node:child_process";
import { existsSync, mkdtempSync, writeFileSync, rmSync, statSync } from "node:fs";
import path from "node:path";
import os from "node:os";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const telosRoot = path.resolve(here, "..");

// The exact, contract-frozen unavailability record. Never a fabricated verdict.
export const WITNESS_UNAVAILABLE = Object.freeze({
  status: "unavailable",
  verdict: "UNVERIFIABLE",
  reason: "no emet implementation reachable"
});

// Lookup order: env override, sibling checkout, then the known pubscan impl.
// Only a path that exists and is a file is a reachable implementation.
// TELOS_EMET_DISABLE_FALLBACKS restricts resolution to TELOS_EMET_CLI only, so
// a test can force the honest unavailable path deterministically in any
// environment (including a developer machine that has the pubscan impl).
export function resolveEmet() {
  const fallbacksDisabled = process.env.TELOS_EMET_DISABLE_FALLBACKS === "1";
  const candidates = fallbacksDisabled
    ? [process.env.TELOS_EMET_CLI]
    : [
        process.env.TELOS_EMET_CLI,
        path.join(telosRoot, "..", "emet", "impl", "js", "emet.js"),
        "c:/dev/public/pubscan/emet/impl/js/emet.js"
      ];
  for (const candidate of candidates) {
    if (!candidate) continue;
    try {
      if (existsSync(candidate) && statSync(candidate).isFile()) {
        return candidate;
      }
    } catch {
      // unreadable candidate is not reachable
    }
  }
  return null;
}

// Map EMET coherence verdicts to witness verdicts.
function mapVerdict(emetVerdict) {
  if (emetVerdict === "COHERENT") return "MATCH";
  if (emetVerdict === "VIEW_DIFFERS_FROM_SOURCE") return "DRIFT";
  return "UNVERIFIABLE";
}

// Run the EMET coherence witness over source and view byte strings.
// Returns a recorded envelope, or the exact unavailability record when no
// implementation is reachable. Never fabricates a verdict.
export function runWitness(sourceBytes, viewBytes) {
  const emet = resolveEmet();
  if (!emet) {
    return { ...WITNESS_UNAVAILABLE };
  }
  let dir;
  try {
    dir = mkdtempSync(path.join(os.tmpdir(), "telos-proof-witness-"));
    const sourcePath = path.join(dir, "source.bytes");
    const viewPath = path.join(dir, "view.bytes");
    writeFileSync(sourcePath, sourceBytes, "utf8");
    writeFileSync(viewPath, viewBytes, "utf8");
    const result = spawnSync(process.execPath, [emet, "coherence", "--json", sourcePath, viewPath], {
      encoding: "utf8"
    });
    if (result.status === 64) {
      return {
        status: "witnessed",
        verdict: "UNVERIFIABLE",
        exit_code: 64,
        reason: (result.stderr || result.stdout || "emet usage error").trim().slice(0, 200)
      };
    }
    let envelope;
    try {
      envelope = JSON.parse((result.stdout || "").trim());
    } catch {
      return {
        status: "witnessed",
        verdict: "UNVERIFIABLE",
        exit_code: result.status,
        reason: (result.stderr || "emet produced no parseable JSON").trim().slice(0, 200)
      };
    }
    // subject is deliberately omitted: EMET reports the temp source path, which
    // is a per-run implementation artifact, not evidence. Recording it would
    // make the witnessed packet nondeterministic and break the MCP parity gate.
    const record = {
      status: "witnessed",
      verdict: mapVerdict(envelope.verdict),
      emet_version: envelope.emet_version,
      spec_version: envelope.spec_version,
      exit_code: envelope.exit_code,
      emet_verdict: envelope.verdict,
      subject: "packet.canonical"
    };
    if (envelope.reason !== undefined) {
      record.reason = envelope.reason;
    }
    return record;
  } catch (err) {
    return {
      status: "witnessed",
      verdict: "UNVERIFIABLE",
      reason: `witness spawn failed: ${err instanceof Error ? err.message : String(err)}`.slice(0, 200)
    };
  } finally {
    if (dir) {
      rmSync(dir, { recursive: true, force: true });
    }
  }
}
