import { fileURLToPath } from "node:url";

import { hashStable, round } from "./measurement-utils.mjs";

const defaultTrace = [
  { step: 1, proxy_score: 0.58, quality_score: 0.82, components: { tests: 0.86, readability: 0.84, receipts: 0.76 } },
  { step: 2, proxy_score: 0.64, quality_score: 0.8, components: { tests: 0.9, readability: 0.78, receipts: 0.73 } },
  { step: 3, proxy_score: 0.72, quality_score: 0.74, components: { tests: 0.96, readability: 0.66, receipts: 0.6 } },
  { step: 4, proxy_score: 0.81, quality_score: 0.66, components: { tests: 1.0, readability: 0.52, receipts: 0.45 } },
  { step: 5, proxy_score: 0.9, quality_score: 0.57, components: { tests: 1.0, readability: 0.4, receipts: 0.33 } },
  { step: 6, proxy_score: 0.96, quality_score: 0.49, components: { tests: 1.0, readability: 0.31, receipts: 0.23 } }
];

function rows(trace) {
  if (!Array.isArray(trace) || trace.length < 2) {
    throw new Error("objective_monitor: measurement_source_missing");
  }
  return trace.map((row, index) => {
    const proxy = Number(row.proxy_score);
    const quality = Number(row.quality_score);
    if (!Number.isFinite(proxy) || !Number.isFinite(quality)) {
      throw new Error("objective_monitor: measurement_source_missing");
    }
    return {
      step: Number.isFinite(Number(row.step)) ? Number(row.step) : index + 1,
      proxy_score: proxy,
      quality_score: quality,
      components: Object.fromEntries(
        Object.entries(row.components ?? {}).map(([name, value]) => [name, Number(value)])
      )
    };
  });
}

function mean(values) {
  return values.reduce((total, value) => total + value, 0) / values.length;
}

function variance(values) {
  const avg = mean(values);
  return mean(values.map((value) => (value - avg) ** 2));
}

function slope(values) {
  if (values.length < 2) return 0;
  return (values.at(-1) - values[0]) / (values.length - 1);
}

function signal(code, metric, threshold, message, verdict = "DRIFT") {
  return { code, metric: round(metric, 4), threshold, verdict, message };
}

export function detectObjectiveSignals(trace, {
  divergenceThreshold = 0.08,
  componentDominanceThreshold = 0.62,
  ceilingThreshold = 0.9,
  improvementWindow = 3,
  varianceCollapseThreshold = 0.0005
} = {}) {
  const data = rows(trace);
  const proxy = data.map((row) => row.proxy_score);
  const quality = data.map((row) => row.quality_score);
  const signals = [];
  const proxySlope = slope(proxy);
  const qualitySlope = slope(quality);

  if (proxySlope > 0 && qualitySlope < -divergenceThreshold / data.length) {
    signals.push(signal(
      "proxy_quality_divergence",
      proxySlope - qualitySlope,
      divergenceThreshold,
      "proxy score is rising while independent quality is falling"
    ));
  }

  const last = data.at(-1);
  const components = Object.entries(last.components).filter(([, value]) => Number.isFinite(value));
  const total = components.reduce((sum, [, value]) => sum + Math.abs(value), 0);
  if (total > 0) {
    const [name, value] = components.reduce((best, item) => (
      Math.abs(item[1]) > Math.abs(best[1]) ? item : best
    ));
    const ratio = Math.abs(value) / total;
    if (ratio >= componentDominanceThreshold) {
      signals.push(signal(
        "component_dominance",
        ratio,
        componentDominanceThreshold,
        `${name} dominates the objective components`
      ));
    }
  }

  const ceilingRate = proxy.filter((value) => value >= ceilingThreshold).length / proxy.length;
  if (ceilingRate > 0) {
    signals.push(signal(
      "ceiling_saturation",
      ceilingRate,
      ceilingThreshold,
      "proxy score is saturating near the ceiling"
    ));
  }

  const bestQuality = Math.max(...quality.slice(0, -1));
  const lastImprovementIndex = quality.findLastIndex((value) => value >= bestQuality);
  const stepsSinceImprovement = data.length - 1 - lastImprovementIndex;
  if (stepsSinceImprovement >= improvementWindow) {
    signals.push(signal(
      "steps_since_improvement",
      stepsSinceImprovement,
      improvementWindow,
      "quality has not improved across the recent objective steps"
    ));
  }

  const recentQuality = quality.slice(-Math.min(quality.length, improvementWindow));
  if (recentQuality.length >= 2 && variance(recentQuality) <= varianceCollapseThreshold) {
    signals.push(signal(
      "quality_variance_collapse",
      variance(recentQuality),
      varianceCollapseThreshold,
      "quality signal has collapsed and may no longer distinguish outcomes",
      "MATCH"
    ));
  }

  return signals;
}

export function objectiveMonitorPacket({ trace = defaultTrace } = {}) {
  const signals = detectObjectiveSignals(trace);
  const packet = {
    schema: "project-telos.objective-monitor/v1",
    tool: "telos.objective.monitor",
    generated_at: "2026-06-28T00:00:00.000Z",
    purpose: "Detect rewardspy-style proxy-objective drift in agent, research, and build workflows before a happy metric masks quality loss.",
    source_inspiration: {
      repo: "AvAdiii/rewardspy",
      concept: "reward-hacking observability for proxy metrics, component dominance, ceiling saturation, and training health"
    },
    contract: {
      protocol_agnostic: true,
      raw_prompt_required: false,
      raw_tool_args_required: false,
      receipts_required: true,
      verdicts: ["MATCH", "DRIFT", "UNVERIFIABLE"],
      io_surfaces: ["cli-json", "mcp-json-rpc", "ide", "tui", "app-bridge", "proof-artifact"]
    },
    watched_fields: [
      "proxy_score",
      "quality_score",
      "components",
      "step"
    ],
    failure_codes: [
      "proxy_quality_divergence",
      "component_dominance",
      "ceiling_saturation",
      "steps_since_improvement",
      "quality_variance_collapse",
      "measurement_source_missing"
    ],
    signals,
    next_actions: [
      "forum.route objective drift alerts to the right lane",
      "crucible.assess objective-monitor claims before release",
      "telos.loop.ledger attach objective signals to unattended agent runs",
      "index.context.envelope include objective traces by reference, not raw transcripts"
    ],
    privacy: {
      raw_prompt_export_required: false,
      raw_tool_args_export_required: false,
      trace_can_use_hash_refs: true
    }
  };
  packet.receipt_hash = hashStable(packet);
  return packet;
}

export function summary(packet = objectiveMonitorPacket()) {
  const codes = packet.signals.map((item) => item.code).join(", ") || "none";
  return [
    "Telos Objective Monitor",
    `schema  ${packet.schema}`,
    `tool    ${packet.tool}`,
    `signals ${packet.signals.length}`,
    `codes   ${codes}`,
    "next    node demo/objective-monitor.mjs"
  ].join("\n") + "\n";
}

function main() {
  const packet = objectiveMonitorPacket();
  process.stdout.write(process.argv.includes("--summary") ? summary(packet) : `${JSON.stringify(packet, null, 2)}\n`);
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  main();
}
