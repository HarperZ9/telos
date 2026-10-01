import { writeFileSync } from "node:fs";

const fixture = {
  robot: {
    model: "differential_drive_planar_fixture",
    wheel_base_m: 0.5,
    robot_radius_m: 0.08,
    max_wheel_speed_mps: 0.6,
    max_angular_speed_rad_s: 1.1,
    max_latency_s: 0.1
  },
  environment: {
    workspace_m: { min_x: -0.2, max_x: 2.0, min_y: -0.4, max_y: 0.8 },
    obstacles: [{ id: "bench_fixture", x_m: 0.72, y_m: 0.44, radius_m: 0.1 }]
  },
  tolerances: {
    mean_path_error_m: 0.025,
    max_path_error_m: 0.04,
    terminal_position_error_m: 0.04,
    terminal_heading_error_rad: 0.05,
    min_obstacle_clearance_m: 0.08
  },
  commands: [
    { dt_s: 1, left_mps: 0.42, right_mps: 0.42 },
    { dt_s: 1, left_mps: 0.24, right_mps: 0.48 },
    { dt_s: 1, left_mps: 0.46, right_mps: 0.46 },
    { dt_s: 1, left_mps: 0.44, right_mps: 0.2 }
  ],
  observation_offsets: [
    { x_m: 0, y_m: 0, heading_rad: 0 },
    { x_m: 0.006, y_m: -0.003, heading_rad: 0.004 },
    { x_m: 0.011, y_m: 0.005, heading_rad: 0.007 },
    { x_m: 0.016, y_m: 0.009, heading_rad: 0.01 },
    { x_m: 0.018, y_m: 0.012, heading_rad: 0.011 }
  ],
  observed_latency_s: 0.04
};

function round(value) {
  return Number(value.toFixed(6));
}

function pose(x = 0, y = 0, heading = 0) {
  return { x_m: round(x), y_m: round(y), heading_rad: round(heading) };
}

function step(current, command, robot = fixture.robot) {
  const v = (command.left_mps + command.right_mps) / 2;
  const omega = (command.right_mps - command.left_mps) / robot.wheel_base_m;
  const headingMid = current.heading_rad + (omega * command.dt_s) / 2;
  return pose(
    current.x_m + v * Math.cos(headingMid) * command.dt_s,
    current.y_m + v * Math.sin(headingMid) * command.dt_s,
    current.heading_rad + omega * command.dt_s
  );
}

function simulate(commands, robot = fixture.robot) {
  const trace = [pose()];
  for (const command of commands) trace.push(step(trace.at(-1), command, robot));
  return trace;
}

function observedTrace(predicted) {
  return predicted.map((entry, index) => pose(
    entry.x_m + fixture.observation_offsets[index].x_m,
    entry.y_m + fixture.observation_offsets[index].y_m,
    entry.heading_rad + fixture.observation_offsets[index].heading_rad
  ));
}

function distance(a, b) {
  return Math.hypot(a.x_m - b.x_m, a.y_m - b.y_m);
}

function headingError(a, b) {
  return Math.abs(Math.atan2(Math.sin(a.heading_rad - b.heading_rad), Math.cos(a.heading_rad - b.heading_rad)));
}

function pathMetrics(predicted, observed) {
  const errors = predicted.map((entry, index) => distance(entry, observed[index]));
  const terminalPredicted = predicted.at(-1);
  const terminalObserved = observed.at(-1);
  return {
    mean_path_error_m: round(errors.reduce((sum, item) => sum + item, 0) / errors.length),
    max_path_error_m: round(Math.max(...errors)),
    terminal_position_error_m: round(distance(terminalPredicted, terminalObserved)),
    terminal_heading_error_rad: round(headingError(terminalPredicted, terminalObserved))
  };
}

function minObstacleClearance(trace, environment = fixture.environment, robot = fixture.robot) {
  let minClearance = Infinity;
  for (const point of trace) {
    for (const obstacle of environment.obstacles) {
      const center = { x_m: obstacle.x_m, y_m: obstacle.y_m };
      const clearance = distance(point, center) - obstacle.radius_m - robot.robot_radius_m;
      minClearance = Math.min(minClearance, clearance);
    }
  }
  return round(minClearance);
}

function commandEnvelope(commands, robot = fixture.robot) {
  const speeds = commands.flatMap((command) => [Math.abs(command.left_mps), Math.abs(command.right_mps)]);
  const angular = commands.map((command) => Math.abs((command.right_mps - command.left_mps) / robot.wheel_base_m));
  return {
    max_wheel_speed_mps: round(Math.max(...speeds)),
    max_angular_speed_rad_s: round(Math.max(...angular)),
    wheel_speed_ok: Math.max(...speeds) <= robot.max_wheel_speed_mps,
    angular_speed_ok: Math.max(...angular) <= robot.max_angular_speed_rad_s
  };
}

function workspaceOk(trace, environment = fixture.environment) {
  const { min_x, max_x, min_y, max_y } = environment.workspace_m;
  return trace.every((point) => (
    point.x_m >= min_x && point.x_m <= max_x && point.y_m >= min_y && point.y_m <= max_y
  ));
}

function verdict(metrics, predicted, commands, latency = fixture.observed_latency_s, environment = fixture.environment) {
  const envelope = commandEnvelope(commands);
  const clearance = minObstacleClearance(predicted, environment);
  const tolerances = fixture.tolerances;
  const checks = {
    trajectory_match:
      metrics.mean_path_error_m <= tolerances.mean_path_error_m &&
      metrics.max_path_error_m <= tolerances.max_path_error_m &&
      metrics.terminal_position_error_m <= tolerances.terminal_position_error_m &&
      metrics.terminal_heading_error_rad <= tolerances.terminal_heading_error_rad,
    safety_envelope_match:
      envelope.wheel_speed_ok &&
      envelope.angular_speed_ok &&
      workspaceOk(predicted, environment) &&
      clearance >= tolerances.min_obstacle_clearance_m,
    latency_match: latency <= fixture.robot.max_latency_s,
    unit_contract_match: commands.every((command) => command.dt_s > 0 && Number.isFinite(command.left_mps) && Number.isFinite(command.right_mps))
  };
  return {
    checks,
    envelope,
    min_obstacle_clearance_m: clearance,
    verdict: Object.values(checks).every(Boolean) ? "MATCH" : "DRIFT"
  };
}

function variantPacket(id, commands, robot = fixture.robot, environment = fixture.environment, latency = fixture.observed_latency_s) {
  const predicted = simulate(commands, robot);
  const observed = observedTrace(simulate(fixture.commands));
  const metrics = pathMetrics(predicted, observed);
  const result = verdict(metrics, predicted, commands, latency, environment);
  return {
    id,
    verdict: result.verdict,
    metrics,
    failed_checks: Object.entries(result.checks).filter(([, ok]) => !ok).map(([name]) => name)
  };
}

function buildPacket() {
  const predicted = simulate(fixture.commands);
  const observed = observedTrace(predicted);
  const metrics = pathMetrics(predicted, observed);
  const result = verdict(metrics, predicted, fixture.commands);
  const inflatedEnvironment = {
    ...fixture.environment,
    obstacles: [{ id: "bench_fixture", x_m: 0.72, y_m: 0.44, radius_m: 0.28 }]
  };
  const negativeControls = [
    variantPacket("wrong_wheel_base", fixture.commands, { ...fixture.robot, wheel_base_m: 0.32 }),
    variantPacket("swapped_wheels", fixture.commands.map((command) => ({
      dt_s: command.dt_s,
      left_mps: command.right_mps,
      right_mps: command.left_mps
    }))),
    variantPacket("centimeters_treated_as_meters", fixture.commands.map((command) => ({
      dt_s: command.dt_s,
      left_mps: command.left_mps * 100,
      right_mps: command.right_mps * 100
    }))),
    variantPacket("unsafe_clearance", fixture.commands, fixture.robot, inflatedEnvironment),
    variantPacket("latency_over_limit", fixture.commands, fixture.robot, fixture.environment, 0.18)
  ];
  const match = result.verdict === "MATCH" && negativeControls.every((control) => control.verdict === "DRIFT");
  return {
    schema: "project-telos.embodied-sim2real/proof-packet-fixture/v1",
    generated_at: "2026-07-02T00:00:00.000Z",
    result: match ? "EMBODIED_SIM2REAL_FIXTURE_MATCH" : "EMBODIED_SIM2REAL_FIXTURE_DRIFT",
    fixture: {
      robot: fixture.robot,
      environment: fixture.environment,
      tolerances: fixture.tolerances,
      commands: fixture.commands
    },
    traces: { predicted, observed },
    metrics: {
      ...metrics,
      min_obstacle_clearance_m: result.min_obstacle_clearance_m,
      command_envelope: result.envelope,
      observed_latency_s: fixture.observed_latency_s
    },
    checks: {
      ...result.checks,
      negative_controls: negativeControls
    },
    claim_card: {
      claim: "In the deterministic planar robotics fixture, the observed trace matches the differential-drive prediction within tolerance, stays inside the declared safety envelope, preserves units and latency limits, and rejects configured negative controls.",
      verdict: match ? "MATCH" : "DRIFT",
      scope: "One local differential-drive sim-to-real fixture only; not a real robot safety claim, not a medical robotics claim, and not a foundation-model benchmark.",
      falsification: "The trajectory exceeds tolerance, the safety envelope fails, latency exceeds limit, units are ill-posed, or any negative control is accepted as MATCH."
    },
    toolchain_implications: [
      "Gather owns robotics, embodied AI, surgical robotics, soft robotics, benchmark, and safety source receipts.",
      "Index should package robot morphology, command logs, sensor traces, environment state, and source refs.",
      "Forum should route embodied claims through robotics, safety, domain, and verification lanes.",
      "BuildLang/buildc should become the typed runtime for units, kinematics, dynamics, traces, and tolerance proofs.",
      "Crucible should reject sim-to-real claims without units, tolerances, safety envelopes, trace comparisons, and negative controls.",
      "Learn should turn fixtures into exercises about units, kinematics, latency, clearance, and overclaim boundaries."
    ],
    non_claims: [
      "This fixture does not prove real-world robot safety.",
      "This fixture does not validate a vision-language-action model.",
      "This fixture does not make a surgical or medical recommendation.",
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
    "Project Telos Embodied Sim-to-Real Proof Packet",
    `result      ${packet.result}`,
    `mean_error  ${packet.metrics.mean_path_error_m} m`,
    `clearance   ${packet.metrics.min_obstacle_clearance_m} m`,
    `negative    ${packet.checks.negative_controls.length}`,
    `verdict     ${packet.claim_card.verdict}`
  ].join("\n") + "\n");
} else {
  process.stdout.write(`${JSON.stringify(packet, null, 2)}\n`);
}
