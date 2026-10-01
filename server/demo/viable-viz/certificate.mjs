/**
 * certificate.mjs - The witnessed Certificate for the Viable Visualization reconcile loop.
 *
 * makeCertificate({ verdict, subjectKind, criterion, recovered, readoutSummary,
 *                   amplifications, disclosure })
 *   → Certificate
 *
 * Certificate.recheck() re-derives the verdict from the stored criterion + recovered
 * independently of the live run. Trust nothing; re-derive.
 *
 * Zero external dependencies. ESM .mjs.
 */

// ── Verdict re-derivation logic ───────────────────────────────────────────────

/**
 * Tolerance fractions for the grounded recheck path.
 * These must match the thresholds used during the live reconcile loop.
 */
const VERTEX_TOL_FRAC = 0.30;
const EDGE_TOL_FRAC   = 0.50;

/**
 * recheckPolytope(criterion, recovered)
 *
 * criterion: { vertices, edges, polytopeKind }
 * recovered: { vertices, edges, verticesExact, edgesExact,
 *              pixelVertices?, pixelEdges? }
 *
 * Re-derives whether the recovered invariant matches the criterion using the
 * same DUAL-CHANNEL logic as the live loop:
 *   - Geometric channel (P_A): exact match - vertices/edges fields
 *   - Pixel channel (P_H):     fractional tolerance - pixelVertices/pixelEdges fields
 *
 * The live loop requires BOTH P_A AND P_H to pass for CERTIFIED.
 * This recheck mirrors that exactly: if either channel fails, verdict is UNVERIFIABLE.
 *
 * If pixelVertices/pixelEdges are absent, falls back to the stored vertices/edges
 * for both channels (compatible with simple recovered objects).
 *
 * Returns true iff the stored verdict is consistent with re-derivation.
 */
function recheckPolytope(criterion, recovered, verdict) {
  const { vertices: trueV, edges: trueE } = criterion;

  // P_A path (geometric exact): use the primary recovered values
  const recV = recovered.vertices;
  const recE = recovered.edges;
  const geomVpass = Math.abs(recV - trueV) === 0;
  const geomEpass = Math.abs(recE - trueE) === 0;
  const geomCert  = geomVpass && geomEpass;

  // P_H path (pixel fractional): use pixelVertices/pixelEdges if present,
  // else fall back to the primary values (for single-channel recovered objects)
  const pixV = recovered.pixelVertices !== undefined ? recovered.pixelVertices : recV;
  const pixE = recovered.pixelEdges    !== undefined ? recovered.pixelEdges    : recE;
  const pixVpass = trueV === 0 ? pixV === 0 : Math.abs(pixV - trueV) / trueV <= VERTEX_TOL_FRAC;
  const pixEpass = trueE === 0 ? pixE === 0 : Math.abs(pixE - trueE) / trueE <= EDGE_TOL_FRAC;
  const pixCert  = pixVpass && pixEpass;

  // CERTIFIED requires BOTH channels - mirrors the live loop's adjudication
  const rederived = (geomCert && pixCert) ? "CERTIFIED" : "UNVERIFIABLE";
  return rederived === verdict;
}

/**
 * recheckGraph(criterion, recovered, verdict)
 *
 * criterion: { nodeCount, edgeCount, degreeSeq, components }
 * recovered: { nodeCount, edgeCount, geomVertices?, geomEdges?, pixelVertices?, pixelEdges? }
 *
 * Re-derives whether the recovered invariant is consistent with the criterion.
 * Mirrors the DUAL-CHANNEL adjudication of the live loop:
 *   - Geometric perceiver (P_A): geomVertices/geomEdges vs criterion (fractional tolerance)
 *   - Pixel perceiver (P_H):     pixelVertices/pixelEdges vs criterion (fractional tolerance)
 *
 * CERTIFIED requires BOTH channels to pass (unanimity gate).
 * If only one channel's values are available (no geom/pixel split in recovered),
 * falls back to checking the merged nodeCount/edgeCount against tolerance.
 */
function recheckGraph(criterion, recovered, verdict) {
  const { nodeCount: trueN, edgeCount: trueE } = criterion;

  let rederived;

  if (recovered.geomVertices !== undefined && recovered.pixelVertices !== undefined) {
    // Dual-channel recheck (mirrors the live loop's buildVerdicts for graphs)
    const { geomVertices: vA, geomEdges: eA, pixelVertices: vH, pixelEdges: eH } = recovered;
    const A_nPass = trueN === 0 ? vA === 0 : Math.abs(vA - trueN) / trueN <= VERTEX_TOL_FRAC;
    const A_ePass = trueE === 0 ? eA === 0 : Math.abs(eA - trueE) / trueE <= EDGE_TOL_FRAC;
    const A_pass  = A_nPass && A_ePass;

    const H_nPass = trueN === 0 ? vH === 0 : Math.abs(vH - trueN) / trueN <= VERTEX_TOL_FRAC;
    const H_ePass = trueE === 0 ? eH === 0 : Math.abs(eH - trueE) / trueE <= EDGE_TOL_FRAC;
    const H_pass  = H_nPass && H_ePass;

    rederived = (A_pass && H_pass) ? "CERTIFIED" : "UNVERIFIABLE";
  } else {
    // Legacy / single-channel fallback
    const { nodeCount: recN, edgeCount: recE } = recovered;
    const nPass = trueN === 0 ? recN === 0 : Math.abs(recN - trueN) / trueN <= VERTEX_TOL_FRAC;
    const ePass = trueE === 0 ? recE === 0 : Math.abs(recE - trueE) / trueE <= EDGE_TOL_FRAC;
    rederived = (nPass && ePass) ? "CERTIFIED" : "UNVERIFIABLE";
  }

  return rederived === verdict;
}

// ── Certificate factory ───────────────────────────────────────────────────────

/**
 * makeCertificate({ verdict, subjectKind, criterion, recovered,
 *                   readoutSummary, amplifications, disclosure })
 *
 * @param {object} opts
 * @param {"CERTIFIED"|"UNVERIFIABLE"} opts.verdict
 * @param {"polytope"|"graph"} opts.subjectKind
 * @param {object} opts.criterion    - the external criterion from the subject
 * @param {object} opts.recovered    - the recovered invariant from perception
 * @param {object} [opts.readoutSummary]  - summary of the final perception readout
 * @param {Array}  [opts.amplifications]  - array of { step, label, recovered, verdict }
 * @param {string} [opts.disclosure]      - disclosure string from the regulator
 *
 * @returns {Certificate}
 */
export function makeCertificate({
  verdict,
  subjectKind,
  criterion,
  recovered,
  readoutSummary = null,
  amplifications = [],
  disclosure = "",
}) {
  if (verdict !== "CERTIFIED" && verdict !== "UNVERIFIABLE") {
    throw new Error(`makeCertificate: verdict must be "CERTIFIED" or "UNVERIFIABLE", got: ${verdict}`);
  }

  /**
   * recheck() - re-derive the verdict from the stored criterion + recovered.
   *
   * Independent of the live run. Re-compares recovered-vs-criterion using the
   * same tolerance logic and confirms the stored verdict is consistent.
   *
   * Returns true  if re-derivation agrees with the stored verdict.
   * Returns false if re-derivation disagrees (indicates a loop inconsistency).
   */
  function recheck() {
    try {
      if (subjectKind === "polytope") {
        return recheckPolytope(criterion, recovered, verdict);
      } else if (subjectKind === "graph") {
        return recheckGraph(criterion, recovered, verdict);
      } else {
        // Unknown subject kind - conservative: confirm only if UNVERIFIABLE
        return verdict === "UNVERIFIABLE";
      }
    } catch (_) {
      // Any error in re-derivation → recheck fails (fail-closed)
      return false;
    }
  }

  return {
    verdict,
    subjectKind,
    criterion,
    recovered,
    readoutSummary,
    amplifications,
    disclosure,
    recheck,
  };
}
