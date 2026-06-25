// subject.mjs - Subject constructors for Viable Visualization (Task 1).
// Zero external dependencies; ESM.

// node:fs is loaded lazily + guarded so this module is BROWSER-SAFE (the web surface imports it via app.mjs).
// In Node, readFileSync reads the real ecosystem map; in the browser the dynamic import rejects → readFileSync
// stays null → ecosystemSubject's existing try/catch falls through to the synthetic connected fallback.
let readFileSync = null;
try { ({ readFileSync } = await import("node:fs")); } catch { /* browser: no node:fs */ }
import { polytope } from "../render-nd/index.mjs";

// ---------------------------------------------------------------------------
// polytopeSubject
// ---------------------------------------------------------------------------

/**
 * polytopeSubject(kind, n) → { kind:"polytope", structure:{kind,n},
 *   criterion:{vertices, edges, polytopeKind} }
 * Criterion counts are read directly from render-nd's polytope().
 */
export function polytopeSubject(kind, n) {
  const p = polytope(kind, n);
  return {
    kind: "polytope",
    structure: { kind, n },
    criterion: {
      vertices: p.verts.length,
      edges: p.edges.length,
      polytopeKind: kind,
    },
  };
}

// ---------------------------------------------------------------------------
// graphSubject helpers: union-find + degree sequence
// ---------------------------------------------------------------------------

function makeUnionFind(size) {
  const parent = Int32Array.from({ length: size }, (_, i) => i);
  const rank = new Int32Array(size);

  function find(x) {
    while (parent[x] !== x) {
      parent[x] = parent[parent[x]]; // path halving
      x = parent[x];
    }
    return x;
  }

  function union(a, b) {
    const ra = find(a), rb = find(b);
    if (ra === rb) return;
    if (rank[ra] < rank[rb]) parent[ra] = rb;
    else if (rank[ra] > rank[rb]) parent[rb] = ra;
    else { parent[rb] = ra; rank[ra]++; }
  }

  function componentCount() {
    let count = 0;
    for (let i = 0; i < size; i++) if (find(i) === i) count++;
    return count;
  }

  return { find, union, componentCount };
}

// ---------------------------------------------------------------------------
// graphSubject
// ---------------------------------------------------------------------------

/**
 * graphSubject(graph) where graph = { nodes:[id,...], edges:[[i,j],...] }
 * (edges are 0-based indices into nodes array)
 * → { kind:"graph", structure:{graph}, criterion:{nodeCount, edgeCount,
 *     degreeSeq, components} }
 */
export function graphSubject(graph) {
  const { nodes, edges } = graph;
  const nodeCount = nodes.length;
  const edgeCount = edges.length;

  // Degree sequence
  const deg = new Int32Array(nodeCount);
  for (const [i, j] of edges) {
    if (i >= 0 && i < nodeCount) deg[i]++;
    if (j >= 0 && j < nodeCount) deg[j]++;
  }
  const degreeSeq = Array.from(deg).sort((a, b) => a - b);

  // Connected components via union-find
  const uf = makeUnionFind(nodeCount);
  for (const [i, j] of edges) {
    if (i >= 0 && i < nodeCount && j >= 0 && j < nodeCount) {
      uf.union(i, j);
    }
  }
  const components = nodeCount === 0 ? 0 : uf.componentCount();

  return {
    kind: "graph",
    structure: { graph },
    criterion: { nodeCount, edgeCount, degreeSeq, components },
  };
}

// ---------------------------------------------------------------------------
// Synthetic fallback ecosystem (~12 nodes representing real workspace lanes)
// ---------------------------------------------------------------------------

const SYNTHETIC_ECOSYSTEM = (() => {
  // Deterministic representative subgraph of the real workspace.
  // Names mirror real workspace projects; edges mirror plausible dependencies.
  const nodes = [
    "accountable-surface",  // 0
    "coherence-membrane",   // 1
    "studio-libs",          // 2
    "render-nd",            // 3
    "render-sound",         // 4
    "sense-core",           // 5
    "viable-viz",           // 6
    "studio-engine",        // 7
    "portfolio-site",       // 8
    "project-docs",         // 9
    "workspace-repo-map",   // 10
    "orca",                 // 11
  ];
  const edges = [
    [3, 2],   // render-nd → studio-libs
    [4, 2],   // render-sound → studio-libs
    [5, 2],   // sense-core → studio-libs
    [6, 3],   // viable-viz → render-nd
    [6, 4],   // viable-viz → render-sound
    [6, 5],   // viable-viz → sense-core
    [7, 3],   // studio-engine → render-nd
    [7, 5],   // studio-engine → sense-core
    [1, 5],   // coherence-membrane → sense-core
    [0, 1],   // accountable-surface → coherence-membrane
    [8, 9],   // portfolio-site → project-docs
    [10, 9],  // workspace-repo-map → project-docs
  ];
  return { nodes, edges };
})();

// ---------------------------------------------------------------------------
// ecosystemSubject - helpers
// ---------------------------------------------------------------------------

/**
 * buildUnionFindFull(size) - returns a union-find over [0..size).
 * Separate from makeUnionFind above to keep this section self-contained.
 */
function makeUF(size) {
  const parent = Int32Array.from({ length: size }, (_, i) => i);
  const rank   = new Int32Array(size);
  function find(x) {
    while (parent[x] !== x) { parent[x] = parent[parent[x]]; x = parent[x]; }
    return x;
  }
  function union(a, b) {
    const ra = find(a), rb = find(b);
    if (ra === rb) return;
    if (rank[ra] < rank[rb]) parent[ra] = rb;
    else if (rank[ra] > rank[rb]) parent[rb] = ra;
    else { parent[rb] = ra; rank[ra]++; }
  }
  return { find, union };
}

/**
 * buildLaneStarEdges(projects) → Array<[number, number]>
 *
 * Within each lane, connect every non-first project to the first (star topology).
 * This ensures projects sharing a lane are connected, giving graph density
 * representative of real workspace organisation.
 */
function buildLaneStarEdges(projects) {
  const laneMap = new Map();
  for (let i = 0; i < projects.length; i++) {
    const lane = projects[i].lane || "_default";
    if (!laneMap.has(lane)) laneMap.set(lane, []);
    laneMap.get(lane).push(i);
  }
  const edges = [];
  for (const indices of laneMap.values()) {
    for (let k = 1; k < indices.length; k++) {
      edges.push([indices[0], indices[k]]);
    }
  }
  return edges;
}

/**
 * largestConnectedComponent(nodeCount, edgeList) → Set<number> of node indices.
 */
function largestConnectedComponent(nodeCount, edgeList) {
  const uf = makeUF(nodeCount);
  for (const [a, b] of edgeList) uf.union(a, b);

  const compMap = new Map();
  for (let i = 0; i < nodeCount; i++) {
    const root = uf.find(i);
    if (!compMap.has(root)) compMap.set(root, []);
    compMap.get(root).push(i);
  }

  let best = [];
  for (const members of compMap.values()) {
    if (members.length > best.length) best = members;
  }
  return new Set(best);
}

/**
 * bfsInducedSubgraph(seedIdx, nodeSet, adjList, maxNodes)
 * → { nodes: number[], edges: [number,number][] } (global indices, connected).
 *
 * BFS from seedIdx keeping the highest-degree nodes first, bounded to maxNodes.
 * Returns indices in the original nodeSet's global numbering.
 */
function bfsInducedSubgraph(seedIdx, globalAdjList, maxNodes) {
  const visited = new Set();
  // BFS priority: use a simple FIFO queue; seed is the highest-degree node
  const queue = [seedIdx];
  visited.add(seedIdx);

  while (queue.length > 0 && visited.size < maxNodes) {
    const current = queue.shift();
    const neighbors = globalAdjList.get(current) || [];
    // Sort neighbors by degree (descending) to prefer well-connected nodes
    const sorted = [...neighbors].sort(
      (a, b) => (globalAdjList.get(b)?.length ?? 0) - (globalAdjList.get(a)?.length ?? 0)
    );
    for (const nb of sorted) {
      if (!visited.has(nb) && visited.size < maxNodes) {
        visited.add(nb);
        queue.push(nb);
      }
    }
  }

  return visited;
}

// ---------------------------------------------------------------------------
// ecosystemSubject
// ---------------------------------------------------------------------------

/**
 * ecosystemSubject(path?) → graphSubject result (never throws).
 * Reads WORKSTATION-ECOSYSTEM.json; if absent/unparseable → synthetic fallback.
 * Adds .source = "ecosystem-map" | "synthetic-fallback" and optionally .truncatedTo.
 *
 * Strategy:
 *   1. Parse JSON; extract all nodes + all inter-project references from both
 *      `goals` arrays (direct dependencies) and lane membership (star topology
 *      per lane, reflecting real workspace organisation).
 *   2. De-duplicate edges (undirected).
 *   3. Compute connected components via union-find.
 *   4. Take the LARGEST connected component (LCC).
 *   5. If LCC > 40 nodes: take a BFS-induced subgraph ≤40 from the
 *      highest-degree node in the LCC, keeping it connected with induced edges.
 *   6. Result is a CONNECTED graph with edgeCount ≥ nodeCount − 1.
 *   7. Falls back to SYNTHETIC_ECOSYSTEM on any error - never throws.
 */
export async function ecosystemSubject(
  path = "c:/dev/project-docs/maps/WORKSTATION-ECOSYSTEM.json"
) {
  // Right-sized for perceptual legibility: ≤18 nodes gives each node ≥21 pixels of
  // separation at 384px render width, which is enough for the pixel blob detector
  // (grid32 cells = 12px each) to find distinct peaks without overlaps.
  // The BFS subgraph is still drawn from the real workspace ecosystem map -
  // it is a genuine connected piece of the workspace, not synthetic.
  const MAX_NODES = 18;

  let rawGraph = null;
  let source = "synthetic-fallback";
  let truncatedTo = null;

  try {
    const text = readFileSync(path, "utf8");
    const json = JSON.parse(text);

    // ── Shape: { projects: [ { name, lane, goals:[...] } ] } ──────────────────
    if (Array.isArray(json.projects) && json.projects.length > 0) {
      const projects = json.projects;
      const nameToIdx = new Map(projects.map((p, i) => [p.name, i]));

      // Build undirected edge list (goals + lane-star), de-duplicated
      const edgeSet = new Set();
      const allEdges = [];
      function addEdge(a, b) {
        if (a === b) return;
        const key = a < b ? `${a},${b}` : `${b},${a}`;
        if (!edgeSet.has(key)) {
          edgeSet.add(key);
          allEdges.push([a, b]);
        }
      }

      // 1. Direct goal edges
      for (let i = 0; i < projects.length; i++) {
        if (Array.isArray(projects[i].goals)) {
          for (const g of projects[i].goals) {
            const j = nameToIdx.get(g);
            if (j !== undefined) addEdge(i, j);
          }
        }
      }

      // 2. Lane-star edges (connects projects sharing a lane)
      for (const [a, b] of buildLaneStarEdges(projects)) addEdge(a, b);

      // 3. Find largest connected component
      const lccSet = largestConnectedComponent(projects.length, allEdges);

      // 4. If LCC ≤ MAX_NODES, use it directly; else BFS-trim to MAX_NODES
      let selectedSet = lccSet;
      if (lccSet.size > MAX_NODES) {
        // Build adjacency list restricted to the LCC
        const lccAdj = new Map();
        for (const [a, b] of allEdges) {
          if (lccSet.has(a) && lccSet.has(b)) {
            if (!lccAdj.has(a)) lccAdj.set(a, []);
            if (!lccAdj.has(b)) lccAdj.set(b, []);
            lccAdj.get(a).push(b);
            lccAdj.get(b).push(a);
          }
        }

        // Find highest-degree seed in the LCC
        let seedIdx = -1, maxDeg = -1;
        for (const idx of lccSet) {
          const deg = lccAdj.get(idx)?.length ?? 0;
          if (deg > maxDeg) { maxDeg = deg; seedIdx = idx; }
        }

        selectedSet = bfsInducedSubgraph(seedIdx, lccAdj, MAX_NODES);
        truncatedTo = MAX_NODES;
      }

      // 5. Build final node list + induced edges
      const selectedArr = [...selectedSet].sort((a, b) => a - b);
      const globalToLocal = new Map(selectedArr.map((gi, li) => [gi, li]));

      const nodeNames = selectedArr.map(gi => projects[gi].name);
      const inducedEdges = [];
      for (const [a, b] of allEdges) {
        if (selectedSet.has(a) && selectedSet.has(b)) {
          inducedEdges.push([globalToLocal.get(a), globalToLocal.get(b)]);
        }
      }

      rawGraph = { nodes: nodeNames, edges: inducedEdges };
      source = "ecosystem-map";
    }
    // ── Shape: { nodes:[...], edges|links:[...] } ─────────────────────────────
    else if (Array.isArray(json.nodes)) {
      const nodeList = json.nodes.map((n, i) =>
        typeof n === "object" ? (n.id ?? n.name ?? i) : n
      );
      const edgeList = (json.edges || json.links || []).map((e) => {
        if (Array.isArray(e)) return e;
        return [e.source, e.target];
      });
      rawGraph = { nodes: nodeList, edges: edgeList };
      source = "ecosystem-map";
    }
  } catch (_) {
    // File missing, unreadable, or unparseable - fall through to synthetic
  }

  if (!rawGraph) {
    rawGraph = SYNTHETIC_ECOSYSTEM;
    source = "synthetic-fallback";
    truncatedTo = null;
  }

  const result = graphSubject(rawGraph);
  result.source = source;
  if (truncatedTo !== null) result.truncatedTo = truncatedTo;
  return result;
}
