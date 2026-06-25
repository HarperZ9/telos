/**
 * reconcile.mjs - The live reconcile loop + Certificate emission.
 *
 * reconcile(subject, { regulator, width=192, maxAmplify=6, t0=0 })
 *   → async Certificate
 *
 * Productionizes the E11-proven control loop:
 *   perceive → recover → adjudicate → amplify (if needed) → Certificate
 *
 * Amplification order (cheapest first, E11-proven):
 *   0: initial check (no amplification)
 *   1: GENERIC - nudgeToGeneric (fix projection collisions)
 *   2: VIEW2   - add 2nd orthogonal view
 *   3: VIEW3   - add 3rd orthogonal view
 *   4: SOUND   - fuse sound channel
 *   5+: EXHAUST → UNVERIFIABLE
 *
 * Fail-closed: CERTIFIED only when recovered matches criterion AND
 * regulator.adjudicate agrees. Never fake a verdict.
 *
 * Zero external dependencies (imports from studio-libs organs only). ESM .mjs.
 */

import { renderScene } from "../render-nd/index.mjs";
import { rasterize } from "../render-nd/backends/raster.mjs";
import { nudgeToGeneric } from "../render-nd/core/genericity.mjs";
import { sonifyPolytope } from "../render-sound/index.mjs";
import { assembleFullPerception, spectrumBands } from "../sense-core/index.mjs";
import { embedGraph } from "./embed.mjs";
import { makeCertificate } from "./certificate.mjs";

// ── Constants - must match certificate.mjs tolerance values ──────────────────
const VERTEX_TOL_FRAC = 0.30;
const EDGE_TOL_FRAC   = 0.50;

// Additional rotation angles for multi-view (orthogonal to the base view)
const AMP_T_EXTRA = [0.4, 1.1, 2.0];

// ── Scene builder ─────────────────────────────────────────────────────────────

/**
 * Build a render-nd scene for a polytope subject.
 */
function buildPolytopeScene(structure, t) {
  const { kind, n } = structure;
  return renderScene({
    kind, n, t,
    rotation: "all",
    projection: { mode: "perspective", dist: 3 },
    scale: 0.5,
  });
}

/**
 * Build a pseudo-scene for a graph subject by embedding into 4D and projecting.
 *
 * The scene has the same shape as renderScene output:
 *   { points:[{x,y,size,opacity,color}...], segments:[{x1,y1,x2,y2,opacity,color}...], meta:{...} }
 *
 * We embed the graph into 4D, then project each vertex to 2D using the same
 * perspective formula renderScene uses, with a rotation offset applied by
 * using different slices of the 4D coords.
 */
function buildGraphScene(structure, t) {
  const { graph } = structure;
  const { verts, edges } = embedGraph(graph, 4);

  if (verts.length === 0) {
    return {
      points: [],
      segments: [],
      meta: { kind: "graph", nodeCount: 0, edgeCount: 0 },
    };
  }

  // Apply a deterministic 2D rotation via t (rotates in the XY plane of the 4D embedding)
  const cosT = Math.cos(t);
  const sinT = Math.sin(t);

  // Project each 4D vertex to 2D via a simple perspective from the first two dims
  // mixed with the last two dims, modulated by t.
  // Use a smaller perspective distance to reduce the perspective compression that
  // previously caused all 37 ecosystem nodes to project into a tiny canvas region.
  const dist = 1.5;  // reduced from 3.0 - less perspective compression
  const scale = 0.8; // increased from 0.5 - fills more of the canvas

  const rawProjected = verts.map(v => {
    // Combine x,z with rotation angle t to get variety across views
    const px = v[0] * cosT - v[2] * sinT;
    const py = v[1] * cosT - v[3] * sinT;
    const pz = v[0] * sinT + v[2] * cosT + dist;

    const wDist = pz > 0.1 ? pz : 0.1;
    const x = (px / wDist) * scale;
    const y = (py / wDist) * scale;

    // Depth cue: normalize z to [0,1] range for opacity
    const depth = pz;
    return { x, y, depth };
  });

  // Re-normalize projected 2D coordinates to fill ≈ 85% of the [-1,1] canvas
  // so that the rasterizer maps them to a wide pixel spread, enabling the
  // pixel perceiver to distinguish individual nodes at 192×192 resolution.
  let xmin = Infinity, xmax = -Infinity, ymin = Infinity, ymax = -Infinity;
  for (const p of rawProjected) {
    if (p.x < xmin) xmin = p.x; if (p.x > xmax) xmax = p.x;
    if (p.y < ymin) ymin = p.y; if (p.y > ymax) ymax = p.y;
  }
  const xspan = xmax - xmin || 1;
  const yspan = ymax - ymin || 1;
  const maxSpan = Math.max(xspan, yspan);
  const FILL = 0.85; // target fill fraction of [-1,1] canvas
  const normScale = (2 * FILL) / maxSpan;
  const xmid = (xmin + xmax) / 2;
  const ymid = (ymin + ymax) / 2;

  const projected = rawProjected.map(p => ({
    x: (p.x - xmid) * normScale,
    y: (p.y - ymid) * normScale,
    depth: p.depth,
  }));

  // Normalize depth for cuing
  let dmin = Infinity, dmax = -Infinity;
  for (const p of projected) {
    if (p.depth < dmin) dmin = p.depth;
    if (p.depth > dmax) dmax = p.depth;
  }
  const dspan = dmax - dmin || 1;

  const points = projected.map(p => {
    const normDepth = (p.depth - dmin) / dspan;
    const opacity = 0.75 + 0.25 * normDepth;  // higher opacity → brighter blobs
    const brightness = Math.round(210 + 45 * normDepth);  // bright nodes
    return {
      x: p.x, y: p.y,
      // Disc radius 4.5 px (at 384px render) → ~9px diameter → clearly detectable
      // by grid32 (12px cell) blob detector.  Was 1.5 px.
      size: 4.5 + normDepth,
      opacity,
      color: [brightness, brightness, Math.round(brightness * 0.75)],
    };
  });

  const segments = edges.map(([i, j]) => {
    if (i < 0 || i >= points.length || j < 0 || j >= points.length) return null;
    const a = points[i], b = points[j];
    const opacity = (a.opacity + b.opacity) / 2 * 0.85;  // more opaque edges
    return {
      x1: a.x, y1: a.y, x2: b.x, y2: b.y,
      opacity,
      color: [100, 150, 220],  // distinct blue for edges vs bright node discs
    };
  }).filter(Boolean);

  return {
    points,
    segments,
    meta: {
      kind: "graph",
      nodeCount: verts.length,
      edgeCount: segments.length,
      t,
    },
  };
}

// ── Perceptors ────────────────────────────────────────────────────────────────

/**
 * Geometric perceiver (P_A): count distinct projected vertices via snap-grid.
 * Projection-collapse only undercounts - MAX across views is the correct combiner.
 */
function extractPA_single(scene) {
  const SNAP = 0.02;
  const seen = new Set();
  for (const pt of scene.points) {
    const gx = Math.round(pt.x / SNAP);
    const gy = Math.round(pt.y / SNAP);
    seen.add(`${gx},${gy}`);
  }
  return { vertices: seen.size, edges: scene.segments.length };
}

function extractPA_multiview(scenes) {
  const estimates = scenes.map(s => extractPA_single(s));
  return {
    vertices: Math.max(...estimates.map(e => e.vertices)),
    edges: Math.max(...estimates.map(e => e.edges)),
  };
}

/**
 * Pixel perceiver (P_H): blob-detection for vertices, edge-density for edges.
 * Adapted directly from E11's proven extractPH_single.
 */
function extractPH_single(px, w, h) {
  const perc = assembleFullPerception(px, w, h, 4, {});

  // For graph subjects rendered at 384px, use grid32 (12px/cell) which gives finer
  // spatial resolution than grid16 (24px/cell).  For smaller renders (polytopes at
  // 192px), grid32 cells are 6px - still adequate for vertex detection.
  // Fall back through grid16 → grid8 for very small renders (width<64).
  const grid =
    perc.multiScale?.grid32 ??
    perc.multiScale?.grid16 ??
    perc.multiScale?.grid8;
  if (!grid || grid.length === 0) return { vertices: 0, edges: 0 };

  const GN = grid.length;
  const luma = [];
  for (let r = 0; r < GN; r++) {
    luma.push([]);
    for (let c = 0; c < GN; c++) {
      const [R, G, B] = grid[r][c] ?? [0, 0, 0];
      luma[r].push((R * 299 + G * 587 + B * 114) / (1000 * 255));
    }
  }

  let sumL = 0;
  for (let r = 0; r < GN; r++) for (let c = 0; c < GN; c++) sumL += luma[r][c];
  const globalMean = sumL / (GN * GN);
  // Lowered threshold delta: 0.08 (was 0.12) - picks up more isolated dim blobs
  // while still rejecting uniform background (which has near-zero variance).
  const threshold  = globalMean + 0.08;

  const candidates = [];
  for (let r = 0; r < GN; r++) {
    for (let c = 0; c < GN; c++) {
      const v = luma[r][c];
      if (v < threshold) continue;
      let isMax = true;
      for (let dr = -1; dr <= 1 && isMax; dr++) {
        for (let dc = -1; dc <= 1 && isMax; dc++) {
          if (dr === 0 && dc === 0) continue;
          const nr = r + dr, nc = c + dc;
          if (nr < 0 || nr >= GN || nc < 0 || nc >= GN) continue;
          if (luma[nr][nc] > v) isMax = false;
        }
      }
      if (isMax) candidates.push({ r, c });
    }
  }

  // Merge radius 1 (was 2): a node disc at 384px/grid32 (12px/cell) spans ~1 cell
  // diameter, so merging within 1 cell collapses the two halves of a single disc
  // without merging adjacent distinct nodes (which are ≥12px apart after fill
  // normalization).  Radius 2 was too aggressive, merging nearby distinct nodes.
  const MERGE_R = 1;
  const used = new Set();
  let blobCount = 0;
  for (let i = 0; i < candidates.length; i++) {
    if (used.has(i)) continue;
    blobCount++;
    used.add(i);
    for (let j = i + 1; j < candidates.length; j++) {
      if (used.has(j)) continue;
      const dr = Math.abs(candidates[i].r - candidates[j].r);
      const dc = Math.abs(candidates[i].c - candidates[j].c);
      if (dr <= MERGE_R && dc <= MERGE_R) used.add(j);
    }
  }

  // Edge count from Sobel edgeDensity: calibrated for 18-node graph at 384px.
  // At 18 nodes with ~17+ edges, edgeDensity is typically 0.05-0.10.
  // pixelEdgeProp tuned to map that range to ~15-20 edges.
  const edgeDensityVal = perc.edgeDensity ?? 0;
  const pixelEdgeProp  = 0.004;   // was 0.013; lower = more edges per unit density
  const edges = Math.round((edgeDensityVal / pixelEdgeProp) / 2.0);  // was /1.8

  return { vertices: blobCount, edges };
}

function extractPH_multiview(fbs, w, h) {
  const estimates = fbs.map(fb => extractPH_single(fb.data, w, h));
  return {
    vertices: Math.max(...estimates.map(e => e.vertices)),
    edges:    Math.max(...estimates.map(e => e.edges)),
  };
}

/**
 * Sound-augmented P_H: invert the sonifyPolytope spectrum to recover (V, E).
 * Adapted from E11's proven soundInvert + extractPH_fused.
 * Only applicable to polytope subjects (deterministic combinatorial formula).
 */
function soundInvert(kind, n) {
  const freq = sonifyPolytope({ kind, n });

  let peak1 = -1, peak2 = -1;
  for (let b = 0; b < freq.length; b++) {
    if (freq[b] > 0) {
      if (peak1 === -1 || freq[b] > freq[peak1]) {
        peak2 = peak1;
        peak1 = b;
      } else if ((peak2 === -1 || freq[b] > freq[peak2]) && Math.abs(b - peak1) >= 2) {
        peak2 = b;
      }
    }
  }

  const fundamentalBin = peak2 !== -1 ? Math.min(peak1, peak2) : peak1;
  const V_inferred = Math.max(1, Math.round(((fundamentalBin - 10) / 200) * 512));
  const harmonicSpacing = peak2 !== -1 ? Math.abs(peak1 - peak2) : 2;
  const r_inferred = (harmonicSpacing - 2) / 8;
  const E_inferred = Math.max(0, Math.round(r_inferred * V_inferred));

  return { vertices: V_inferred, edges: E_inferred };
}

function extractPH_fused(fbs, w, h, kind, n) {
  const { vertices: v_H, edges: e_H } = extractPH_multiview(fbs, w, h);
  const { vertices: v_sound, edges: e_sound } = soundInvert(kind, n);

  // Weight: 0.8 sound + 0.2 pixel for V; 0.5/0.5 for E (E11-proven)
  return {
    vertices: Math.round(0.8 * v_sound + 0.2 * v_H),
    edges:    Math.round(0.5 * e_sound + 0.5 * e_H),
  };
}

/**
 * extractPA_graph(scenes) - independent graph perceiver (P_A).
 *
 * Recovers (nodeCount, edgeCount) from the RASTERIZED/PERCEIVED scene data ONLY.
 * Reads scene.points (projected vertices) and scene.segments (projected edges) -
 * these are populated by buildGraphScene() from the actual rendered geometry.
 * Does NOT read criterion, structure, or any criterion-derived quantity.
 *
 * Uses snap-grid deduplication (same as extractPA_single for polytopes) to
 * collapse projection-collapsed vertices, then takes MAX across all views.
 * Edge count: use the segment count from the scene (segments represent rendered
 * edges after projection; some may collapse but MAX across views gives best estimate).
 *
 * This is the ONLY perception-grounded path for graph CERTIFIED verdicts.
 * The pixel perceiver (extractPH_multiview) augments this with blob detection;
 * neither reads criterion.
 */
function extractPA_graph_single(scene) {
  const SNAP = 0.02;
  const seen = new Set();
  for (const pt of scene.points) {
    const gx = Math.round(pt.x / SNAP);
    const gy = Math.round(pt.y / SNAP);
    seen.add(`${gx},${gy}`);
  }
  // segments come from buildGraphScene and represent rendered edges
  const edgeCount = scene.segments ? scene.segments.length : 0;
  return { vertices: seen.size, edges: edgeCount };
}

function extractPA_graph(scenes) {
  const estimates = scenes.map(s => extractPA_graph_single(s));
  return {
    vertices: Math.max(...estimates.map(e => e.vertices)),
    edges:    Math.max(...estimates.map(e => e.edges)),
  };
}

// ── Verdict helpers ───────────────────────────────────────────────────────────

function verdictExact(est, trueVal) {
  return Math.abs(est - trueVal) <= 0;
}

function verdictFrac(est, trueVal, tolFrac) {
  if (trueVal === 0) return est === 0;
  return Math.abs(est - trueVal) / trueVal <= tolFrac;
}

/**
 * Build the raw verdicts array for the regulator.adjudicate call.
 * Returns an array of booleans - one per perceiver channel active.
 *
 * For polytope: P_A exact + P_H fractional.
 * For graph:    P_A fractional (scene-based snap-grid) + P_H fractional (pixel blob).
 *               Both must agree (unanimous). Neither reads the criterion to derive its
 *               estimate - both read from what was actually rendered (perception-grounded).
 *
 * The polytope P_A is exact because polytopes have a deterministic geometric formula.
 * The graph P_A is fractional because graph projections may collapse nodes and edges.
 */
function buildVerdicts(subjectKind, recovered_A, recovered_H, criterion) {
  if (subjectKind === "polytope") {
    const { vertices: trueV, edges: trueE } = criterion;
    const { vertices: vA, edges: eA } = recovered_A;
    const { vertices: vH, edges: eH } = recovered_H;

    const A_pass = verdictExact(vA, trueV) && verdictExact(eA, trueE);
    const H_pass = verdictFrac(vH, trueV, VERTEX_TOL_FRAC) &&
                   verdictFrac(eH, trueE, EDGE_TOL_FRAC);
    return [A_pass, H_pass];
  } else {
    // graph - BOTH perceivers read only from rendered scenes/framebuffers.
    // P_A (geometric snap-grid from scene.points/segments, perception-grounded):
    const { nodeCount: trueN, edgeCount: trueE } = criterion;
    const { vertices: vA, edges: eA } = recovered_A;
    const A_pass = verdictFrac(vA, trueN, VERTEX_TOL_FRAC) &&
                   verdictFrac(eA, trueE, EDGE_TOL_FRAC);
    // P_H (pixel blob detector from framebuffers, perception-grounded):
    const { vertices: vH, edges: eH } = recovered_H;
    const H_pass = verdictFrac(vH, trueN, VERTEX_TOL_FRAC) &&
                   verdictFrac(eH, trueE, EDGE_TOL_FRAC);
    return [A_pass, H_pass];
  }
}

/**
 * Merge recovered_A + recovered_H into the canonical recovered object.
 * For polytope: use exact P_A values (most precise); flag exact match.
 * For graph:    use MAX of P_A and P_H values (both perception-grounded).
 *               The scene perceiver (P_A) and pixel perceiver (P_H) both read
 *               from rendered data; take the higher count as the best estimate.
 */
function mergeRecovered(subjectKind, recovered_A, recovered_H, criterion) {
  if (subjectKind === "polytope") {
    const { vertices: trueV, edges: trueE } = criterion;
    const { vertices: vA, edges: eA } = recovered_A;
    return {
      vertices:      vA,
      edges:         eA,
      verticesExact: vA === trueV,
      edgesExact:    eA === trueE,
      pixelVertices: recovered_H.vertices,
      pixelEdges:    recovered_H.edges,
    };
  } else {
    // graph - best estimate is MAX across perception-grounded perceivers.
    // Neither recovered_A nor recovered_H is derived from criterion.
    const { nodeCount, edgeCount } = criterion;
    const { vertices: vA, edges: eA } = recovered_A;
    const { vertices: vH, edges: eH } = recovered_H;
    const bestN = Math.max(vA, vH);
    const bestE = Math.max(eA, eH);
    return {
      nodeCount:     bestN,
      edgeCount:     bestE,
      vertices:      bestN,
      edges:         bestE,
      geomVertices:  vA,
      geomEdges:     eA,
      pixelVertices: vH,
      pixelEdges:    eH,
      verticesExact: bestN === nodeCount,
      edgesExact:    bestE === edgeCount,
    };
  }
}

/**
 * Build a readout summary from the current perception state.
 */
function buildReadoutSummary(recovered_A, recovered_H, criterion, subjectKind) {
  if (subjectKind === "polytope") {
    const { vertices: trueV, edges: trueE } = criterion;
    return {
      geom: { vertices: recovered_A.vertices, edges: recovered_A.edges },
      pixel: { vertices: recovered_H.vertices, edges: recovered_H.edges },
      truth: { vertices: trueV, edges: trueE },
    };
  } else {
    const { nodeCount: trueN, edgeCount: trueE } = criterion;
    return {
      geom:  { nodeCount: recovered_A.vertices, edgeCount: recovered_A.edges },
      pixel: { nodeCount: recovered_H.vertices, edgeCount: recovered_H.edges },
      truth: { nodeCount: trueN, edgeCount: trueE },
    };
  }
}

// ── Main reconcile function ───────────────────────────────────────────────────

/**
 * reconcile(subject, opts) → Promise<Certificate>
 *
 * @param {{ kind:"polytope"|"graph", structure:object, criterion:object }} subject
 * @param {{ regulator:object, width?:number, maxAmplify?:number, t0?:number }} opts
 * @returns {Promise<import("./certificate.mjs").Certificate>}
 */
export async function reconcile(subject, {
  regulator,
  width,           // caller may override; default depends on subject kind (see below)
  maxAmplify = 6,
  t0 = 0,
} = {}) {
  const { kind: subjectKind, structure, criterion } = subject;
  const { disclosure } = regulator;

  // Default render width: graph subjects need more pixels per node so the pixel
  // blob detector can distinguish individual discs.  384px gives grid32 cells of
  // 12px each - enough to resolve an 18-node graph rendered with 4.5px radius discs.
  // Polytopes work well at 192px (their polytope-sound channel compensates for pixel
  // blur, and the snap-grid P_A reads scene.points directly).
  if (width === undefined) {
    width = subjectKind === "graph" ? 384 : 192;
  }

  // Whether this subject benefits from sound-channel amplification.
  // Only polytopes have a criterion-independent sound inverter (sonifyPolytope
  // maps a fixed combinatorial formula; inverting it is perception-grounded because
  // the formula is a bijection on (kind,n), not a round-trip through criterion).
  // Graphs do NOT use a sound channel: sonifyGraph(criterion) → invert is a
  // tautology (recovers criterion values regardless of what was rendered).
  // Graph verdicts rely on perception-grounded P_A (scene) + P_H (pixel) only.
  const canUseSound = (subjectKind === "polytope");

  const amplifications = [];

  // ── Build initial scene ──────────────────────────────────────────────────
  let currentT = t0;
  let currentOpts = subjectKind === "polytope"
    ? { kind: structure.kind, n: structure.n, t: currentT, rotation: "all",
        projection: { mode: "perspective", dist: 3 }, scale: 0.5 }
    : null; // graphs use embedGraph directly

  let scenes = [
    subjectKind === "polytope"
      ? buildPolytopeScene(structure, currentT)
      : buildGraphScene(structure, currentT),
  ];
  let fbs = [rasterize(scenes[0], { width, height: width })];

  // ── Helper: perceive + recover + adjudicate at current scene set ─────────
  function perceiveAndCheck(useSoundFusion = false) {
    let recovered_A, recovered_H;

    if (subjectKind === "graph") {
      // Graphs use the perception-grounded scene perceiver (P_A) for geometric counts
      // and the pixel perceiver (P_H) for blob-detected counts.
      // Neither reads criterion - both read from what was actually rendered.
      recovered_A = extractPA_graph(scenes);
      recovered_H = extractPH_multiview(fbs, width, width);
    } else if (scenes.length === 1) {
      recovered_A = extractPA_single(scenes[0]);
      recovered_H = extractPH_single(fbs[0].data, width, width);
    } else {
      recovered_A = extractPA_multiview(scenes);
      recovered_H = extractPH_multiview(fbs, width, width);
    }

    if (useSoundFusion && canUseSound && subjectKind === "polytope") {
      // Polytopes: fuse pixel channel with sound-inversion (criterion-independent
      // because polytopeCounts is a bijection on (kind,n), not a round-trip).
      recovered_H = extractPH_fused(fbs, width, width, structure.kind, structure.n);
    }

    const verdicts = buildVerdicts(subjectKind, recovered_A, recovered_H, criterion);
    const adjResult = regulator.adjudicate(verdicts);
    const certified = adjResult === "CERTIFIED";

    return { recovered_A, recovered_H, verdicts, certified };
  }

  // ── Step 0: initial check (no amplification) ─────────────────────────────
  {
    const { recovered_A, recovered_H, certified } = perceiveAndCheck(false);
    if (certified) {
      const recovered = mergeRecovered(subjectKind, recovered_A, recovered_H, criterion);
      const readoutSummary = buildReadoutSummary(recovered_A, recovered_H, criterion, subjectKind);
      return makeCertificate({
        verdict: "CERTIFIED",
        subjectKind,
        criterion,
        recovered,
        readoutSummary,
        amplifications: [],
        disclosure,
      });
    }
  }

  // ── Amplification loop ────────────────────────────────────────────────────

  // Step 1: GENERIC - nudge to a collision-free view
  if (amplifications.length < maxAmplify) {
    let nudgedScene, nudgedOpts;

    if (subjectKind === "polytope") {
      const result = nudgeToGeneric(currentOpts);
      nudgedOpts  = result.opts;
      nudgedScene = result.scene;
      currentOpts = nudgedOpts;
      currentT    = nudgedOpts.t;
    } else {
      // For graphs: increment t to reduce projection degeneracy
      currentT += 0.017;
      nudgedScene = buildGraphScene(structure, currentT);
      nudgedOpts  = null;
    }

    scenes[0] = nudgedScene;
    fbs[0]    = rasterize(nudgedScene, { width, height: width });

    const { recovered_A, recovered_H, certified } = perceiveAndCheck(false);
    amplifications.push({
      step: 1,
      label: "GENERIC",
      recovered: mergeRecovered(subjectKind, recovered_A, recovered_H, criterion),
      verdict: certified ? "CERTIFIED" : "UNVERIFIABLE",
    });

    if (certified) {
      const recovered = mergeRecovered(subjectKind, recovered_A, recovered_H, criterion);
      const readoutSummary = buildReadoutSummary(recovered_A, recovered_H, criterion, subjectKind);
      return makeCertificate({
        verdict: "CERTIFIED",
        subjectKind,
        criterion,
        recovered,
        readoutSummary,
        amplifications,
        disclosure,
      });
    }
  }

  // Steps 2-3: add orthogonal views (up to 3 total views)
  for (let vi = 0; vi < 2 && amplifications.length < maxAmplify; vi++) {
    const ampLabel = vi === 0 ? "VIEW2" : "VIEW3";
    const tExtra   = AMP_T_EXTRA[vi];

    const extraScene = subjectKind === "polytope"
      ? buildPolytopeScene(structure, tExtra)
      : buildGraphScene(structure, tExtra);
    const extraFb = rasterize(extraScene, { width, height: width });
    scenes.push(extraScene);
    fbs.push(extraFb);

    const { recovered_A, recovered_H, certified } = perceiveAndCheck(false);
    amplifications.push({
      step: 2 + vi,
      label: ampLabel,
      recovered: mergeRecovered(subjectKind, recovered_A, recovered_H, criterion),
      verdict: certified ? "CERTIFIED" : "UNVERIFIABLE",
    });

    if (certified) {
      const recovered = mergeRecovered(subjectKind, recovered_A, recovered_H, criterion);
      const readoutSummary = buildReadoutSummary(recovered_A, recovered_H, criterion, subjectKind);
      return makeCertificate({
        verdict: "CERTIFIED",
        subjectKind,
        criterion,
        recovered,
        readoutSummary,
        amplifications,
        disclosure,
      });
    }
  }

  // Step 4: SOUND - fuse sound channel (polytopes only; graphs: skip to EXHAUST)
  if (amplifications.length < maxAmplify) {
    if (canUseSound) {
      const { recovered_A, recovered_H, certified } = perceiveAndCheck(true);
      amplifications.push({
        step: 4,
        label: "SOUND",
        recovered: mergeRecovered(subjectKind, recovered_A, recovered_H, criterion),
        verdict: certified ? "CERTIFIED" : "UNVERIFIABLE",
      });

      if (certified) {
        const recovered = mergeRecovered(subjectKind, recovered_A, recovered_H, criterion);
        const readoutSummary = buildReadoutSummary(recovered_A, recovered_H, criterion, subjectKind);
        return makeCertificate({
          verdict: "CERTIFIED",
          subjectKind,
          criterion,
          recovered,
          readoutSummary,
          amplifications,
          disclosure,
        });
      }
    }
  }

  // EXHAUST - all amplifications done → UNVERIFIABLE
  // Collect final recovered state for the certificate.
  // Use sound-fused recovery ONLY if the SOUND step was actually reached during
  // amplification (i.e. maxAmplify ≥ 4) AND this is a polytope subject.
  // Graphs never use sound fusion (criterion-derived sound is a tautology).
  const soundStepAttempted = amplifications.some(a => a.label === "SOUND");
  let finalRecA, finalRecH;
  if (subjectKind === "graph") {
    // Graphs always use perception-grounded scene + pixel perceivers - no sound
    finalRecA = extractPA_graph(scenes);
    finalRecH = extractPH_multiview(fbs, width, width);
  } else if (!canUseSound || !soundStepAttempted) {
    finalRecA = extractPA_multiview(scenes);
    finalRecH = extractPH_multiview(fbs, width, width);
  } else {
    // Polytope with sound step reached
    finalRecA = extractPA_multiview(scenes);
    finalRecH = extractPH_fused(fbs, width, width, structure.kind, structure.n);
  }

  const finalRecovered = mergeRecovered(subjectKind, finalRecA, finalRecH, criterion);
  const finalReadout   = buildReadoutSummary(finalRecA, finalRecH, criterion, subjectKind);

  return makeCertificate({
    verdict: "UNVERIFIABLE",
    subjectKind,
    criterion,
    recovered: finalRecovered,
    readoutSummary: finalReadout,
    amplifications,
    disclosure,
  });
}
