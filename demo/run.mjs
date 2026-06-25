/**
 * run.mjs - the reconcile -> Certificate loop, end to end, on one concrete subject.
 *
 * What this file does, in plain terms:
 *
 *   1. Takes a 4-dimensional cube (a "tesseract"). We know its true vertex and
 *      edge counts up front -- 16 vertices, 32 edges. That known truth is the
 *      CRITERION. It is supplied by the subject, not invented by the loop.
 *
 *   2. Renders the cube and PERCEIVES it two independent ways:
 *        - a geometric reader that counts distinct projected vertices, and
 *        - a pixel reader that finds bright blobs in the rasterized image.
 *      Neither reader is allowed to look at the criterion. Each recovers its own
 *      estimate of (vertices, edges) from what was actually drawn.
 *
 *   3. CHECKS both recovered estimates against the criterion. The regulator only
 *      says CERTIFIED when every channel agrees AND every channel matches the
 *      criterion (unanimity). If a view is degenerate, the loop AMPLIFIES --
 *      nudges the rotation, adds orthogonal views, fuses a sound channel -- and
 *      tries again, cheapest fix first.
 *
 *   4. Emits a Certificate carrying its own evidence. The Certificate can
 *      recheck() itself: it re-derives the verdict from the stored criterion +
 *      recovered values, with no access to the live run. Trust the re-derivation,
 *      not the loop's say-so.
 *
 * Two runs below:
 *   RUN A -- a normal render. Expected: CERTIFIED, and recheck() == true.
 *   RUN B -- a deliberately broken render (8x8 pixels, far too few to resolve 16
 *            vertices). The geometric channel still reads the scene correctly, but
 *            the pixel channel cannot, so the two disagree. Expected: UNVERIFIABLE.
 *            The loop does NOT fall back to the channel that happens to be right
 *            and fake a pass. When it cannot verify, it says so.
 *
 * Zero external dependencies. Node >= 18. Run: node demo/run.mjs
 */

import { polytopeSubject } from "./viable-viz/subject.mjs";
import { groundedRegulator } from "./viable-viz/regulator.mjs";
import { reconcile } from "./viable-viz/reconcile.mjs";

// ── small printing helpers (no deps) ──────────────────────────────────────────

const RULE = "-".repeat(70);
const HEAVY = "=".repeat(70);

function heading(title) {
  console.log("");
  console.log(HEAVY);
  console.log(" " + title);
  console.log(HEAVY);
}

/**
 * Print the witnessed amplification steps the loop recorded.
 * Each step is the loop trying a cheaper-first fix and re-checking.
 */
function printWitnessedSteps(certificate) {
  console.log("  witnessed steps (perceive -> check -> amplify if needed):");
  if (certificate.amplifications.length === 0) {
    console.log("    [0] INITIAL  -> certified on the first check, no amplification needed");
    return;
  }
  console.log("    [0] INITIAL  -> not unanimous yet, begin amplification");
  for (const amp of certificate.amplifications) {
    const rec = certificate.subjectKind === "polytope"
      ? `vertices=${amp.recovered.vertices} edges=${amp.recovered.edges}` +
        ` (pixel: v=${amp.recovered.pixelVertices} e=${amp.recovered.pixelEdges})`
      : JSON.stringify(amp.recovered);
    console.log(`    [${amp.step}] ${String(amp.label).padEnd(8)} -> ${amp.verdict.padEnd(13)} ${rec}`);
  }
}

/**
 * Print the final Certificate, including the independent recheck().
 */
function printCertificate(certificate) {
  const c = certificate;
  console.log(RULE);
  console.log("  CERTIFICATE");
  console.log(RULE);
  console.log(`    subject        : ${c.subjectKind} (4-D cube / tesseract)`);
  console.log(`    criterion      : ${JSON.stringify(c.criterion)}    <- the external truth the loop did not author`);
  console.log(`    recovered      : vertices=${c.recovered.vertices} edges=${c.recovered.edges}` +
              `  (geometric channel, exact match: ${c.recovered.verticesExact && c.recovered.edgesExact})`);
  console.log(`    pixel readout  : vertices=${c.recovered.pixelVertices} edges=${c.recovered.pixelEdges}` +
              `  (independent pixel channel)`);
  console.log("");
  console.log(`    VERDICT        : ${c.verdict}`);
  console.log(`    recheck()      : ${c.recheck()}   <- verdict re-derived from stored evidence alone`);
  console.log(RULE);
  console.log("  regulator disclosure (verbatim):");
  console.log("    " + c.disclosure);
}

// ── RUN A: a normal render -> expect CERTIFIED ────────────────────────────────

async function runCertified() {
  heading("RUN A  -  honest render of a 4-D cube  ->  expect CERTIFIED");

  // The subject carries the criterion. polytope('cube', 4) has 16 vertices, 32 edges;
  // those counts come straight from the geometry, not from the loop.
  const subject = polytopeSubject("cube", 4);

  // Grounded regulator: no model in the loop. It adjudicates by unanimity and is
  // fail-closed -- CERTIFIED only when every channel agrees and matches.
  const regulator = groundedRegulator(subject.criterion);

  // 192px is enough resolution for the pixel channel to resolve 16 vertices.
  const certificate = await reconcile(subject, { regulator, width: 192, maxAmplify: 6 });

  printWitnessedSteps(certificate);
  console.log("");
  printCertificate(certificate);

  return certificate;
}

// ── RUN B: a broken render -> expect UNVERIFIABLE (the honest floor) ───────────

async function runUnverifiable() {
  heading("RUN B  -  variety-deficient render (8x8 px)  ->  expect UNVERIFIABLE");

  // Same true subject, same criterion -- nothing about the truth changed.
  const subject = polytopeSubject("cube", 4);
  const regulator = groundedRegulator(subject.criterion);

  // 8x8 pixels is far too coarse to resolve 16 distinct vertices. The geometric
  // channel (which reads the scene's projected points) still recovers the right
  // counts, but the pixel channel cannot -- it over-counts noise. The two channels
  // disagree, so unanimity fails. After exhausting every amplification, the loop
  // returns UNVERIFIABLE. It refuses to lean on the one channel that happens to be
  // right and report a pass it cannot stand behind.
  const certificate = await reconcile(subject, { regulator, width: 8, maxAmplify: 6 });

  printWitnessedSteps(certificate);
  console.log("");
  printCertificate(certificate);

  return certificate;
}

// ── main ──────────────────────────────────────────────────────────────────────

async function main() {
  console.log("");
  console.log("  reconcile -> Certificate  : perceive -> check vs a criterion you did not");
  console.log("  author -> emit MATCH (CERTIFIED) / DRIFT / UNVERIFIABLE -- never \"trusted\".");
  console.log("");
  console.log("  LEGEND");
  console.log("    criterion    the external truth (here: a 4-D cube's true 16 vertices, 32 edges)");
  console.log("    recovered    what perception read back from the actual render (criterion-blind)");
  console.log("    CERTIFIED    every channel agreed AND matched the criterion (fail-closed)");
  console.log("    UNVERIFIABLE could not verify -- reported honestly, NOT a fabricated pass");
  console.log("    recheck()    re-derives the verdict from stored evidence only; trust this, not the run");

  const certA = await runCertified();
  const certB = await runUnverifiable();

  // ── summary + exit-code contract ───────────────────────────────────────────
  heading("SUMMARY");
  console.log(`  RUN A (honest render)  : ${certA.verdict}      recheck=${certA.recheck()}`);
  console.log(`  RUN B (broken render)  : ${certB.verdict}   recheck=${certB.recheck()}`);
  console.log("");

  const aOk = certA.verdict === "CERTIFIED"   && certA.recheck() === true;
  const bOk = certB.verdict === "UNVERIFIABLE" && certB.recheck() === true;

  if (aOk && bOk) {
    console.log("  Both outcomes are as expected: a real pass certifies and re-checks; a render");
    console.log("  that cannot be verified returns UNVERIFIABLE instead of a confident guess.");
    console.log(HEAVY);
    process.exit(0);
  } else {
    console.log("  UNEXPECTED: the demo did not produce both a CERTIFIED and an UNVERIFIABLE.");
    console.log(`    RUN A ok=${aOk}  RUN B ok=${bOk}`);
    console.log(HEAVY);
    process.exit(1);
  }
}

main().catch((err) => {
  console.error("demo crashed:", err && err.stack ? err.stack : err);
  process.exit(2);
});
