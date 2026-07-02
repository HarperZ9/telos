import { writeFileSync } from "node:fs";

const graph = {
  nodes: [
    "exercise",
    "health_outcome",
    "age",
    "baseline_health",
    "biomarker",
    "encouragement"
  ],
  treatment: "exercise",
  outcome: "health_outcome",
  edges: [
    ["age", "exercise"],
    ["age", "health_outcome"],
    ["baseline_health", "exercise"],
    ["baseline_health", "health_outcome"],
    ["encouragement", "exercise"],
    ["exercise", "health_outcome"],
    ["exercise", "biomarker"],
    ["health_outcome", "biomarker"]
  ],
  observed: ["age", "baseline_health", "biomarker", "encouragement"]
};

function hasEdge(from, to) {
  return graph.edges.some(([source, target]) => source === from && target === to);
}

function children(node) {
  return graph.edges.filter(([source]) => source === node).map(([, target]) => target);
}

function parents(node) {
  return graph.edges.filter(([, target]) => target === node).map(([source]) => source);
}

function descendants(node, seen = new Set()) {
  for (const child of children(node)) {
    if (!seen.has(child)) {
      seen.add(child);
      descendants(child, seen);
    }
  }
  return seen;
}

function topologicalOrder() {
  const incoming = new Map(graph.nodes.map((node) => [node, parents(node).length]));
  const queue = graph.nodes.filter((node) => incoming.get(node) === 0);
  const order = [];
  while (queue.length) {
    const node = queue.shift();
    order.push(node);
    for (const child of children(node)) {
      incoming.set(child, incoming.get(child) - 1);
      if (incoming.get(child) === 0) queue.push(child);
    }
  }
  return order;
}

function undirectedNeighbors(node) {
  const neighbors = new Set();
  for (const [source, target] of graph.edges) {
    if (source === node) neighbors.add(target);
    if (target === node) neighbors.add(source);
  }
  return [...neighbors];
}

function allSimplePaths(start, end, path = [start], paths = []) {
  if (start === end) {
    paths.push([...path]);
    return paths;
  }
  for (const next of undirectedNeighbors(start)) {
    if (path.includes(next)) continue;
    path.push(next);
    allSimplePaths(next, end, path, paths);
    path.pop();
  }
  return paths;
}

function isCollider(prev, current, next) {
  return hasEdge(prev, current) && hasEdge(next, current);
}

function hasConditionedDescendant(node, conditioned, descendantMap) {
  for (const descendant of descendantMap.get(node) ?? []) {
    if (conditioned.has(descendant)) return true;
  }
  return false;
}

function pathActive(path, conditioned, descendantMap) {
  for (let index = 1; index < path.length - 1; index += 1) {
    const prev = path[index - 1];
    const current = path[index];
    const next = path[index + 1];
    if (isCollider(prev, current, next)) {
      if (!conditioned.has(current) && !hasConditionedDescendant(current, conditioned, descendantMap)) {
        return false;
      }
    } else if (conditioned.has(current)) {
      return false;
    }
  }
  return true;
}

function combinations(items) {
  const output = [[]];
  for (const item of items) {
    for (const combo of [...output]) output.push([...combo, item]);
  }
  return output;
}

function isSubset(a, b) {
  return a.every((item) => b.includes(item));
}

function evaluateAdjustmentSet(adjustment) {
  const conditioned = new Set(adjustment);
  const descendantMap = new Map(graph.nodes.map((node) => [node, descendants(node)]));
  const treatmentDescendants = descendantMap.get(graph.treatment);
  const descendantViolations = adjustment.filter((node) => treatmentDescendants.has(node));
  const allPaths = allSimplePaths(graph.treatment, graph.outcome);
  const backdoorPaths = allPaths.filter((path) => hasEdge(path[1], path[0]));
  const activeBackdoorPaths = backdoorPaths.filter((path) => pathActive(path, conditioned, descendantMap));
  return {
    adjustment,
    valid: descendantViolations.length === 0 && activeBackdoorPaths.length === 0,
    descendant_violations: descendantViolations,
    active_backdoor_paths: activeBackdoorPaths
  };
}

function minimalAdjustmentSets() {
  const evaluated = combinations(graph.observed).map(evaluateAdjustmentSet);
  const valid = evaluated.filter((entry) => entry.valid).map((entry) => entry.adjustment);
  return valid.filter((candidate) => !valid.some((other) => (
    other.length < candidate.length && isSubset(other, candidate)
  )));
}

function buildPacket() {
  const dagOrder = topologicalOrder();
  const minimalSets = minimalAdjustmentSets();
  const negatives = [
    evaluateAdjustmentSet([]),
    evaluateAdjustmentSet(["age"]),
    evaluateAdjustmentSet(["baseline_health"]),
    evaluateAdjustmentSet(["encouragement"]),
    evaluateAdjustmentSet(["biomarker"])
  ];
  const expectedMinimal = [["age", "baseline_health"]];
  const result = JSON.stringify(minimalSets) === JSON.stringify(expectedMinimal)
    && dagOrder.length === graph.nodes.length
    && negatives.every((entry) => !entry.valid)
    ? "CAUSAL_DAG_FIXTURE_MATCH"
    : "CAUSAL_DAG_FIXTURE_DRIFT";

  return {
    schema: "project-telos.causal-workbench/proof-packet-fixture/v1",
    generated_at: "2026-07-02T00:00:00.000Z",
    result,
    graph,
    checks: {
      dag_acyclic: dagOrder.length === graph.nodes.length,
      topological_order: dagOrder,
      treatment_descendants: [...descendants(graph.treatment)],
      backdoor_paths: allSimplePaths(graph.treatment, graph.outcome)
        .filter((path) => hasEdge(path[1], path[0])),
      minimal_adjustment_sets: minimalSets,
      negative_controls: negatives
    },
    claim_card: {
      claim: "In the toy DAG, estimating the effect of exercise on health_outcome requires adjusting for age and baseline_health; encouragement alone, age alone, baseline_health alone, or biomarker adjustment does not satisfy the fixture gate.",
      verdict: result === "CAUSAL_DAG_FIXTURE_MATCH" ? "MATCH" : "DRIFT",
      scope: "One deterministic DAG fixture only; not a general causal discovery result and not a real medical claim.",
      falsification: "The graph is cyclic, the minimal adjustment set is not exactly [age, baseline_health], or any negative control is accepted as valid."
    },
    toolchain_implications: [
      "Gather owns source receipts for causal papers, lectures, datasets, and benchmark cards.",
      "Index should package variables, graph assumptions, and candidate evidence without hiding the graph.",
      "Forum should route causal claims to statistician, domain, and verification lanes.",
      "BuildLang/buildc should become the typed graph and adjustment-check runtime.",
      "Crucible should reject any causal claim without graph assumptions, adjustment rationale, negative controls, and a replayable check.",
      "Learn should convert the fixture into exercises about adjustment, colliders, descendants, and overclaim boundaries."
    ],
    non_claims: [
      "This fixture does not prove causal discovery capability.",
      "This fixture does not validate LLM causal reasoning.",
      "This fixture does not make a medical recommendation.",
      "This fixture is not yet a BuildLang/buildc-native receipt."
    ]
  };
}

function argValue(args, name) {
  const inline = args.find((arg) => arg.startsWith(`${name}=`));
  if (inline) return inline.slice(name.length + 1);
  const index = args.indexOf(name);
  return index === -1 ? null : args[index + 1] ?? null;
}

const packet = buildPacket();
const args = process.argv.slice(2);
const outPath = argValue(args, "--out");
if (outPath) writeFileSync(outPath, `${JSON.stringify(packet, null, 2)}\n`);

if (args.includes("--summary")) {
  process.stdout.write([
    "Project Telos Causal Workbench Proof Packet",
    `result    ${packet.result}`,
    `minimal   ${packet.checks.minimal_adjustment_sets.map((set) => set.join("+")).join(", ")}`,
    `negative  ${packet.checks.negative_controls.length}`,
    `verdict   ${packet.claim_card.verdict}`
  ].join("\n") + "\n");
} else {
  process.stdout.write(`${JSON.stringify(packet, null, 2)}\n`);
}
