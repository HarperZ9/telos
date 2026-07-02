#!/usr/bin/env node
import { createHash } from "node:crypto";
import { writeFileSync } from "node:fs";

const args = new Map();
for (let i = 2; i < process.argv.length; i += 1) {
  const arg = process.argv[i];
  if (arg.startsWith("--")) {
    const key = arg.slice(2);
    const next = process.argv[i + 1];
    if (next && !next.startsWith("--")) {
      args.set(key, next);
      i += 1;
    } else {
      args.set(key, "true");
    }
  }
}

const nu = Number(args.get("nu") ?? "0.1");
const t = Number(args.get("t") ?? "0.75");
const n = Number(args.get("grid") ?? "128");
const out = args.get("out") ?? "run.receipt.json";

if (!Number.isFinite(nu) || nu <= 0) throw new Error("nu must be positive");
if (!Number.isFinite(t) || t < 0) throw new Error("t must be non-negative");
if (!Number.isInteger(n) || n < 8 || n % 2 !== 0) throw new Error("grid must be an even integer >= 8");

const pi = Math.PI;
const twoPi = 2 * pi;
const dx = twoPi / n;
const dy = twoPi / n;
const area = dx * dy;
const amplitude = Math.exp(-2 * nu * t);

let integralUSquared = 0;
let integralGradUSquared = 0;
let maxDivergenceAbs = 0;

for (let ix = 0; ix < n; ix += 1) {
  const x = (ix + 0.5) * dx;
  const sx = Math.sin(x);
  const cx = Math.cos(x);
  for (let iy = 0; iy < n; iy += 1) {
    const y = (iy + 0.5) * dy;
    const sy = Math.sin(y);
    const cy = Math.cos(y);

    const u1 = amplitude * sx * cy;
    const u2 = -amplitude * cx * sy;

    const du1dx = amplitude * cx * cy;
    const du1dy = -amplitude * sx * sy;
    const du2dx = amplitude * sx * sy;
    const du2dy = -amplitude * cx * cy;

    const divergence = du1dx + du2dy;
    maxDivergenceAbs = Math.max(maxDivergenceAbs, Math.abs(divergence));

    integralUSquared += (u1 * u1 + u2 * u2) * area;
    integralGradUSquared += (du1dx * du1dx + du1dy * du1dy + du2dx * du2dx + du2dy * du2dy) * area;
  }
}

const energyNumeric = 0.5 * integralUSquared;
const dissipationNumeric = nu * integralGradUSquared;
const energyAnalytic = pi * pi * amplitude * amplitude;
const dissipationAnalytic = 4 * nu * pi * pi * amplitude * amplitude;
const dEnergyDtAnalytic = -4 * nu * pi * pi * amplitude * amplitude;
const residualAnalytic = dEnergyDtAnalytic + dissipationAnalytic;
const residualNumeric = dEnergyDtAnalytic + dissipationNumeric;

const source = "u=(A sin(x) cos(y), -A cos(x) sin(y)); A=exp(-2 nu t); periodic square [0,2pi]^2";
const sourceHash = createHash("sha256").update(source).digest("hex");

const receipt = {
  schema: "project-telos.pde-identity-run-receipt/v1",
  packet_id: "navier-stokes-periodic-energy-identity-v0",
  generated_at: new Date().toISOString(),
  command: process.argv.join(" "),
  parameters: { nu, t, grid: n },
  source_statement_sha256: sourceHash,
  assumptions: [
    "smooth Taylor-Green velocity field",
    "two-dimensional periodic domain",
    "incompressible analytic field",
    "positive viscosity",
    "bounded identity only"
  ],
  measurements: {
    integral_u_squared_numeric: integralUSquared,
    integral_grad_u_squared_numeric: integralGradUSquared,
    energy_numeric: energyNumeric,
    energy_analytic: energyAnalytic,
    energy_abs_error: Math.abs(energyNumeric - energyAnalytic),
    dissipation_numeric: dissipationNumeric,
    dissipation_analytic: dissipationAnalytic,
    dissipation_abs_error: Math.abs(dissipationNumeric - dissipationAnalytic),
    d_energy_dt_analytic: dEnergyDtAnalytic,
    residual_analytic: residualAnalytic,
    residual_numeric: residualNumeric,
    residual_numeric_abs: Math.abs(residualNumeric),
    max_divergence_abs: maxDivergenceAbs
  },
  tolerances: {
    energy_abs_error: 1e-10,
    dissipation_abs_error: 1e-10,
    residual_numeric_abs: 1e-10,
    max_divergence_abs: 1e-12
  },
  verdicts: {
    bounded_identity_probe: Math.abs(energyNumeric - energyAnalytic) <= 1e-10
      && Math.abs(dissipationNumeric - dissipationAnalytic) <= 1e-10
      && Math.abs(residualNumeric) <= 1e-10
      && maxDivergenceAbs <= 1e-12
      ? "MATCH"
      : "DRIFT",
    parent_millennium_problem: "UNVERIFIABLE"
  },
  boundaries: [
    "This executable receipt checks a bounded periodic identity for one smooth field.",
    "This executable receipt does not prove Navier-Stokes existence and smoothness.",
    "This executable receipt does not validate arbitrary numerical simulations or physical fluids."
  ]
};

writeFileSync(out, `${JSON.stringify(receipt, null, 2)}\n`);
console.log(JSON.stringify({
  out,
  bounded_identity_probe: receipt.verdicts.bounded_identity_probe,
  parent_millennium_problem: receipt.verdicts.parent_millennium_problem,
  residual_numeric_abs: receipt.measurements.residual_numeric_abs,
  max_divergence_abs: receipt.measurements.max_divergence_abs
}, null, 2));
