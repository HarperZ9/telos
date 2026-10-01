import {
  distance,
  hashStable,
  numericArray,
  percentile,
  pointSamples,
  round,
  turnAngleDegrees
} from "./measurement-utils.mjs";

export function measureTemporalFlicker({ frames, width, height, threshold = 8 }) {
  const frameValues = Array.isArray(frames) ? frames.map((frame) => numericArray(frame, "flicker")) : [];
  if (frameValues.length < 2) throw new Error("flicker: measurement_source_missing");
  const pixelCount = width * height;
  for (const frame of frameValues) {
    if (frame.length !== pixelCount) throw new Error("flicker: frame_dimensions_mismatch");
  }
  let totalDelta = 0;
  let maxDelta = 0;
  let aboveThreshold = 0;
  let comparisons = 0;
  for (let frameIndex = 1; frameIndex < frameValues.length; frameIndex++) {
    const previous = frameValues[frameIndex - 1];
    const current = frameValues[frameIndex];
    for (let pixelIndex = 0; pixelIndex < pixelCount; pixelIndex++) {
      const delta = Math.abs(current[pixelIndex] - previous[pixelIndex]);
      totalDelta += delta;
      maxDelta = Math.max(maxDelta, delta);
      if (delta >= threshold) aboveThreshold += 1;
      comparisons += 1;
    }
  }
  const measurement = {
    layer_id: "temporal.flicker-meter",
    frame_count: frameValues.length,
    pixel_count: pixelCount,
    threshold,
    mean_delta: round(totalDelta / comparisons),
    max_delta: round(maxDelta),
    above_threshold_transitions: aboveThreshold,
    above_threshold_ratio: round(aboveThreshold / comparisons)
  };
  measurement.measurement_hash = hashStable(measurement);
  return measurement;
}

export function measureGeometryCurvature({ samples }) {
  const points = pointSamples(samples, "geometry");
  const turns = [];
  let pathLength = 0;
  for (let index = 1; index < points.length; index++) {
    pathLength += distance(points[index - 1], points[index]);
  }
  for (let index = 1; index < points.length - 1; index++) {
    turns.push(turnAngleDegrees(points[index - 1], points[index], points[index + 1]));
  }
  const meanTurn = turns.reduce((sum, value) => sum + value, 0) / turns.length;
  const measurement = {
    layer_id: "geometry.curvature-meter",
    sample_count: points.length,
    segment_count: points.length - 1,
    path_length: round(pathLength),
    mean_turn_angle_degrees: round(meanTurn),
    max_turn_angle_degrees: round(Math.max(...turns)),
    curvature_proxy: round(pathLength === 0 ? 0 : meanTurn / pathLength)
  };
  measurement.measurement_hash = hashStable(measurement);
  return measurement;
}

export function measureInteractionTrace({ actions }) {
  const items = Array.isArray(actions) ? [...actions] : [];
  if (!items.length) throw new Error("interaction: measurement_source_missing");
  items.sort((a, b) => Number(a.timestamp_ms ?? 0) - Number(b.timestamp_ms ?? 0));
  const actorCounts = {};
  const kindCounts = {};
  let handoffCount = 0;
  let maxGap = 0;
  for (let index = 0; index < items.length; index++) {
    const action = items[index];
    const actor = String(action.actor ?? "unknown");
    const kind = String(action.kind ?? "unknown");
    actorCounts[actor] = (actorCounts[actor] ?? 0) + 1;
    kindCounts[kind] = (kindCounts[kind] ?? 0) + 1;
    if (index > 0) {
      const previous = items[index - 1];
      if (String(previous.actor ?? "unknown") !== actor) handoffCount += 1;
      const gap = Number(action.timestamp_ms ?? 0) - Number(previous.timestamp_ms ?? 0);
      if (Number.isFinite(gap)) maxGap = Math.max(maxGap, gap);
    }
  }
  const measurement = {
    layer_id: "interaction.trace-meter",
    action_count: items.length,
    actor_counts: actorCounts,
    kind_counts: kindCounts,
    handoff_count: handoffCount,
    max_gap_ms: round(maxGap)
  };
  measurement.measurement_hash = hashStable(measurement);
  return measurement;
}

export function measureUncertaintyBudget({ observations }) {
  const items = Array.isArray(observations) ? observations : [];
  if (!items.length) throw new Error("uncertainty: measurement_source_missing");
  const statusCounts = { calibrated: 0, witnessed: 0, estimated: 0, unverifiable: 0, unknown: 0 };
  for (const item of items) {
    const raw = item?.uncertainty?.status ?? item?.status ?? "unknown";
    const status = Object.hasOwn(statusCounts, raw) ? raw : "unknown";
    statusCounts[status] += 1;
  }
  const riskOrder = ["unverifiable", "unknown", "estimated", "witnessed", "calibrated"];
  const highestRisk = riskOrder.find((status) => statusCounts[status] > 0) ?? "calibrated";
  const measurement = {
    layer_id: "uncertainty.budget-meter",
    observation_count: items.length,
    status_counts: statusCounts,
    highest_risk_status: highestRisk,
    unverifiable_ratio: round(statusCounts.unverifiable / items.length),
    calibrated_ratio: round(statusCounts.calibrated / items.length)
  };
  measurement.measurement_hash = hashStable(measurement);
  return measurement;
}

export function measurePerformanceBudget({ frames, budget_ms = 16.7 }) {
  const durations = (Array.isArray(frames) ? frames : []).map((frame) => Number(
    typeof frame === "number" ? frame : frame?.frame_ms
  ));
  const values = numericArray(durations, "performance");
  const sorted = [...values].sort((a, b) => a - b);
  const mean = values.reduce((sum, value) => sum + value, 0) / values.length;
  const overBudget = values.filter((value) => value > budget_ms).length;
  const measurement = {
    layer_id: "performance.frame-budget-meter",
    frame_count: values.length,
    budget_ms,
    mean_frame_ms: round(mean),
    p95_frame_ms: round(percentile(sorted, 0.95)),
    max_frame_ms: round(sorted[sorted.length - 1]),
    over_budget_frames: overBudget,
    over_budget_ratio: round(overBudget / values.length),
    budget_utilization: round(mean / budget_ms)
  };
  measurement.measurement_hash = hashStable(measurement);
  return measurement;
}
