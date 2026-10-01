// embed.mjs - Deterministic nD graph embedding (Task 1).
// Strategy: iterative force-directed with a fixed, seed-free init derived
// from node index + trigonometric placement across dims.
// Zero external dependencies; ESM.

/**
 * embedGraph(graph, dims=4) → { verts: Float64Array[], edges:[i,j][] }
 *
 * graph = { nodes:[id,...], edges:[[i,j],...] }  (edges are node-index pairs)
 * Each vert is a Float64Array(dims) in approximately [-1,1]^dims.
 * Edges are preserved exactly (same array references/values).
 * Fully deterministic - no Math.random().
 */
export function embedGraph(graph, dims = 4) {
  const { nodes, edges } = graph;
  const N = nodes.length;

  if (N === 0) {
    return { verts: [], edges: [] };
  }

  // ------------------------------------------------------------------
  // 1. Deterministic init: place node i on a regular-ish arrangement
  //    using sin/cos harmonics across each dimension.
  //    For dim d, vertex i gets: cos(2π·i/N·(d+1)) layered with offset.
  //    This spreads nodes without symmetry collapse.
  // ------------------------------------------------------------------
  const verts = Array.from({ length: N }, (_, i) => {
    const v = new Float64Array(dims);
    for (let d = 0; d < dims; d++) {
      // phase shifts to avoid degeneracy when N is small
      const angle = (2 * Math.PI * i) / Math.max(N, dims + 1) * (d + 1);
      v[d] = Math.cos(angle + d * 0.37) * 0.5;  // 0.37 ≈ irrational offset
    }
    return v;
  });

  // Single-node case: nothing to relax, just return
  if (N === 1) {
    return { verts, edges: [] };
  }

  // ------------------------------------------------------------------
  // 2. Build adjacency list for fast neighbour lookup
  // ------------------------------------------------------------------
  const adj = Array.from({ length: N }, () => []);
  for (const [i, j] of edges) {
    if (i >= 0 && i < N && j >= 0 && j < N && i !== j) {
      adj[i].push(j);
      adj[j].push(i);
    }
  }

  // ------------------------------------------------------------------
  // 3. Force-directed relaxation (fixed iterations - deterministic)
  //    Spring force: pull connected pairs toward rest length L0.
  //    Repulsion: push all pairs apart (Fruchterman-Reingold style).
  //    No Barnes-Hut - exact O(N²) repulsion, capped at N≤200 safely.
  // ------------------------------------------------------------------
  const ITERS = 60;
  const L0 = 1.0;           // desired edge length
  const K_SPRING = 0.15;    // spring constant
  const K_REPULSE = 0.08;   // repulsion constant (scaled by N)
  const repulse = K_REPULSE / Math.sqrt(N);

  // temperature schedule: linear cool from 0.3 → 0.01
  const T_START = 0.3;
  const T_END = 0.01;

  const force = Array.from({ length: N }, () => new Float64Array(dims));

  for (let iter = 0; iter < ITERS; iter++) {
    const t = T_START + (T_END - T_START) * (iter / (ITERS - 1));

    // Zero forces
    for (let i = 0; i < N; i++) force[i].fill(0);

    // Repulsion: all pairs
    for (let i = 0; i < N; i++) {
      for (let j = i + 1; j < N; j++) {
        let dist2 = 0;
        for (let d = 0; d < dims; d++) {
          const dd = verts[i][d] - verts[j][d];
          dist2 += dd * dd;
        }
        const dist = Math.sqrt(dist2) || 1e-6;
        const mag = repulse / dist;
        for (let d = 0; d < dims; d++) {
          const dd = (verts[i][d] - verts[j][d]) / dist;
          force[i][d] += dd * mag;
          force[j][d] -= dd * mag;
        }
      }
    }

    // Spring attraction: connected pairs
    for (const [i, j] of edges) {
      if (i < 0 || i >= N || j < 0 || j >= N || i === j) continue;
      let dist2 = 0;
      for (let d = 0; d < dims; d++) {
        const dd = verts[i][d] - verts[j][d];
        dist2 += dd * dd;
      }
      const dist = Math.sqrt(dist2) || 1e-6;
      const stretch = dist - L0;
      const mag = K_SPRING * stretch;
      for (let d = 0; d < dims; d++) {
        const dd = (verts[j][d] - verts[i][d]) / dist;
        force[i][d] += dd * mag;
        force[j][d] -= dd * mag;
      }
    }

    // Apply forces with temperature clamping
    for (let i = 0; i < N; i++) {
      let fmag2 = 0;
      for (let d = 0; d < dims; d++) fmag2 += force[i][d] ** 2;
      const fmag = Math.sqrt(fmag2) || 1e-12;
      const step = Math.min(fmag, t) / fmag;
      for (let d = 0; d < dims; d++) {
        verts[i][d] += force[i][d] * step;
      }
    }
  }

  // ------------------------------------------------------------------
  // 4. Normalize to approximately [-1, 1]^dims
  // ------------------------------------------------------------------
  for (let d = 0; d < dims; d++) {
    let mn = Infinity, mx = -Infinity;
    for (let i = 0; i < N; i++) {
      if (verts[i][d] < mn) mn = verts[i][d];
      if (verts[i][d] > mx) mx = verts[i][d];
    }
    const span = mx - mn || 1;
    const mid = (mn + mx) / 2;
    for (let i = 0; i < N; i++) {
      verts[i][d] = (verts[i][d] - mid) / span * 2;
    }
  }

  return { verts, edges };
}
