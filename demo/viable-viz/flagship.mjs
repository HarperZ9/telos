/**
 * flagship.mjs - Orchestration + headless witnessed run (Task 4, viable-viz flagship).
 *
 * runFlagship(subject, { regulator, onStep, width, maxAmplify })
 *   → async { certificate, witnessLog }
 *
 * CLI (when run directly):
 *   node viable-viz/flagship.mjs [--subject ecosystem|polytope:kind:n]
 *                                [--endpoint <url>] [--key <key>] [--model <name>]
 *                                [--width <px>] [--maxAmplify <n>]
 *
 * Honest disclosure (verbatim per Global Constraints):
 *   "Structural, bilateral, reconciled perception with honest UNVERIFIABLE on variety
 *    deficit. The live-model arm requires a connected model; this is the smallest
 *    viable instance, not the complete simulator."
 *
 * Zero external dependencies. ESM .mjs.
 */

import { reconcile } from "./reconcile.mjs";
import { groundedRegulator, modelRegulator } from "./regulator.mjs";
import { polytopeSubject, ecosystemSubject } from "./subject.mjs";

// ── Disclosure (verbatim) ─────────────────────────────────────────────────────

export const DISCLOSURE =
  "Structural, bilateral, reconciled perception with honest UNVERIFIABLE on variety " +
  "deficit. The live-model arm requires a connected model; this is the smallest " +
  "viable instance, not the complete simulator.";

// ── runFlagship ───────────────────────────────────────────────────────────────

/**
 * runFlagship(subject, opts) → async { certificate, witnessLog }
 *
 * Orchestrates: build regulator (if not provided) → run reconcile, threading
 * the onStep callback for each witnessed step. Collects steps into witnessLog.
 *
 * @param {{ kind:string, structure:object, criterion:object }} subject
 * @param {{
 *   regulator?:  object,    // pre-built regulator; if absent, groundedRegulator is built
 *   onStep?:     function,  // (step) called for each witnessed step
 *   width?:      number,    // render width in pixels (default 192)
 *   maxAmplify?: number,    // max amplification steps (default 6)
 * }} opts
 * @returns {Promise<{ certificate: object, witnessLog: object[] }>}
 */
export async function runFlagship(subject, {
  regulator: regulatorArg,
  onStep,
  width = 192,
  maxAmplify = 6,
} = {}) {
  // Build regulator if not provided
  const regulator = regulatorArg ?? groundedRegulator(subject.criterion);

  const witnessLog = [];

  // Emit a step to both the callback and the witnessLog
  function emitStep(step) {
    witnessLog.push(step);
    if (typeof onStep === "function") {
      onStep(step);
    }
  }

  // Step: START
  emitStep({
    event: "START",
    subjectKind: subject.kind,
    criterion: subject.criterion,
    regulatorConnected: regulator.connected,
    width,
    maxAmplify,
    ts: Date.now(),
  });

  // Run the reconcile loop
  const certificate = await reconcile(subject, { regulator, width, maxAmplify });

  // Step: each amplification recorded by the reconcile loop
  for (const amp of certificate.amplifications) {
    emitStep({
      event: "AMPLIFY",
      step: amp.step,
      label: amp.label,
      verdict: amp.verdict,
      recovered: amp.recovered,
      ts: Date.now(),
    });
  }

  // Step: CERTIFICATE - the final witnessed result
  emitStep({
    event: "CERTIFICATE",
    verdict: certificate.verdict,
    subjectKind: certificate.subjectKind,
    recovered: certificate.recovered,
    amplificationsUsed: certificate.amplifications.length,
    recheck: certificate.recheck(),
    disclosure: certificate.disclosure,
    ts: Date.now(),
  });

  return { certificate, witnessLog };
}

// ── CLI entry ─────────────────────────────────────────────────────────────────

/**
 * parseArgs - minimal argv parser (no external deps).
 * Returns a map of --key → value (or true for flags without a value).
 */
function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    const tok = argv[i];
    if (tok.startsWith("--")) {
      const key = tok.slice(2);
      const next = argv[i + 1];
      if (next !== undefined && !next.startsWith("--")) {
        args[key] = next;
        i++;
      } else {
        args[key] = true;
      }
    }
  }
  return args;
}

/**
 * buildSubject - parse the --subject flag into a subject object.
 * Formats:
 *   "ecosystem"            → ecosystemSubject()
 *   "polytope:kind:n"      → polytopeSubject(kind, n)
 *   "polytope:simplex:4"   → polytopeSubject("simplex", 4)
 */
async function buildSubject(subjectArg) {
  if (!subjectArg || subjectArg === "ecosystem") {
    return ecosystemSubject();
  }
  if (typeof subjectArg === "string" && subjectArg.startsWith("polytope:")) {
    const parts = subjectArg.split(":");
    // polytope:kind:n
    const kind = parts[1] ?? "cube";
    const n    = parseInt(parts[2] ?? "4", 10);
    if (isNaN(n) || n < 2) {
      throw new Error(`Invalid polytope dimension: ${parts[2]} - must be an integer >= 2`);
    }
    return polytopeSubject(kind, n);
  }
  throw new Error(
    `Unknown --subject value: "${subjectArg}". ` +
    `Valid values: "ecosystem" (default) or "polytope:kind:n" (e.g. "polytope:cube:4").`
  );
}

/**
 * printHeader - print the run header.
 */
function printHeader(subjectKind, criterion, regulatorConnected, width, maxAmplify) {
  console.log("═══════════════════════════════════════════════════════════════");
  console.log(" Viable Visualization - Flagship Headless Run");
  console.log("═══════════════════════════════════════════════════════════════");
  console.log(`  Subject kind  : ${subjectKind}`);
  console.log(`  Criterion     : ${JSON.stringify(criterion)}`);
  console.log(`  Regulator     : ${regulatorConnected ? "model-connected" : "grounded (criterion-supervised)"}`);
  console.log(`  Width         : ${width}px`);
  console.log(`  Max amplify   : ${maxAmplify}`);
  console.log("───────────────────────────────────────────────────────────────");
}

/**
 * printStep - print a single witness step concisely.
 */
function printStep(step) {
  switch (step.event) {
    case "START":
      console.log(`[START]  subject=${step.subjectKind}  regulator=${step.regulatorConnected ? "model" : "grounded"}  width=${step.width}`);
      break;
    case "AMPLIFY":
      console.log(`[AMP ${step.step}] ${step.label.padEnd(8)}  verdict=${step.verdict}  recovered=${JSON.stringify(step.recovered)}`);
      break;
    case "CERTIFICATE":
      console.log(`[CERT]   verdict=${step.verdict}  amplificationsUsed=${step.amplificationsUsed}  recheck=${step.recheck}`);
      break;
    default:
      console.log(`[${step.event}] ${JSON.stringify(step)}`);
  }
}

/**
 * printCertificate - print the full Certificate section.
 */
function printCertificate(certificate) {
  console.log("───────────────────────────────────────────────────────────────");
  console.log(" Certificate");
  console.log("───────────────────────────────────────────────────────────────");
  console.log(`  Verdict              : ${certificate.verdict}`);
  console.log(`  Subject kind         : ${certificate.subjectKind}`);
  console.log(`  Criterion            : ${JSON.stringify(certificate.criterion)}`);
  console.log(`  Recovered            : ${JSON.stringify(certificate.recovered)}`);
  console.log(`  Amplifications used  : ${certificate.amplifications.length}`);
  if (certificate.amplifications.length > 0) {
    for (const amp of certificate.amplifications) {
      console.log(`    [${amp.step}] ${amp.label.padEnd(8)} → ${amp.verdict}  recovered=${JSON.stringify(amp.recovered)}`);
    }
  }
  console.log(`  recheck()            : ${certificate.recheck()}`);
  console.log("───────────────────────────────────────────────────────────────");
  console.log(" Regulator disclosure");
  console.log("───────────────────────────────────────────────────────────────");
  console.log(`  ${certificate.disclosure}`);
  console.log("───────────────────────────────────────────────────────────────");
  console.log(" Flagship disclosure");
  console.log("───────────────────────────────────────────────────────────────");
  console.log(`  ${DISCLOSURE}`);
  console.log("═══════════════════════════════════════════════════════════════");
}

// ── Main CLI ──────────────────────────────────────────────────────────────────

if (process.argv[1] && (
  process.argv[1].endsWith("flagship.mjs") ||
  process.argv[1].endsWith("flagship.mjs".replace(/\//g, "\\"))
)) {
  (async () => {
    const args = parseArgs(process.argv.slice(2));

    // Parse options
    const subjectArg  = typeof args.subject  === "string" ? args.subject  : "ecosystem";
    const endpointArg = typeof args.endpoint === "string" ? args.endpoint : null;
    const keyArg      = typeof args.key      === "string" ? args.key      : undefined;
    const modelArg    = typeof args.model    === "string" ? args.model    : undefined;
    const widthArg    = typeof args.width    === "string" ? parseInt(args.width, 10) : 192;
    const maxAmpArg   = typeof args.maxAmplify === "string" ? parseInt(args.maxAmplify, 10) : 6;

    // Build subject
    let subject;
    try {
      subject = await buildSubject(subjectArg);
    } catch (err) {
      console.error(`Error building subject: ${err.message}`);
      process.exit(1);
    }

    // Build regulator
    let regulator;
    if (endpointArg) {
      regulator = await modelRegulator({
        endpoint: endpointArg,
        key: keyArg,
        model: modelArg,
        criterion: subject.criterion,
      });
    } else {
      regulator = groundedRegulator(subject.criterion);
    }

    // Print header
    printHeader(
      subject.kind,
      subject.criterion,
      regulator.connected,
      widthArg,
      maxAmpArg,
    );

    // Run flagship with live step printing
    let result;
    try {
      result = await runFlagship(subject, {
        regulator,
        onStep: printStep,
        width: widthArg,
        maxAmplify: maxAmpArg,
      });
    } catch (err) {
      console.error(`Flagship run error: ${err.message}`);
      if (err.stack) console.error(err.stack);
      process.exit(1);
    }

    // Print full certificate
    printCertificate(result.certificate);

    // Exit 0 on both CERTIFIED and UNVERIFIABLE (both are honest outcomes)
    // Exit nonzero only on actual crash (handled above)
    process.exit(0);
  })();
}
