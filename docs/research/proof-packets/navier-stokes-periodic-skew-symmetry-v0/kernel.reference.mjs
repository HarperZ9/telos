import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));

function arg(name, fallback) {
  const idx = process.argv.indexOf(name);
  return idx >= 0 && idx + 1 < process.argv.length ? process.argv[idx + 1] : fallback;
}

function numericArg(name, fallback) {
  const value = Number(arg(name, fallback));
  if (!Number.isFinite(value)) {
    throw new Error(`invalid numeric ${name}: ${arg(name, fallback)}`);
  }
  return value;
}

function sha256(path) {
  return createHash("sha256").update(readFileSync(path)).digest("hex");
}

const grid = Math.trunc(numericArg("--grid", "256"));
const nu = numericArg("--nu", "0.1");
const out = arg("--out", null);

if (grid <= 0 || grid % 2 !== 0) {
  throw new Error("--grid must be a positive even integer");
}
if (nu <= 0) {
  throw new Error("--nu must be positive");
}

const modes = [
  { kx: 1, ky: 1, amp: 0.9, phase: 0.1 },
  { kx: 2, ky: 1, amp: -0.35, phase: 0.7 },
  { kx: 1, ky: 3, amp: 0.22, phase: -0.4 },
  { kx: 3, ky: 2, amp: 0.15, phase: 1.2 },
  { kx: 4, ky: 1, amp: -0.08, phase: -0.8 }
];

const L = 2 * Math.PI;
const h = L / grid;
const cellArea = h * h;

let nonlinearTransfer = 0;
let kineticEnergy = 0;
let gradEnergy = 0;
let maxDivergence = 0;

for (let ix = 0; ix < grid; ix += 1) {
  for (let iy = 0; iy < grid; iy += 1) {
    const x = (ix + 0.5) * h;
    const y = (iy + 0.5) * h;
    let ux = 0;
    let uy = 0;
    let duxDx = 0;
    let duxDy = 0;
    let duyDx = 0;
    let duyDy = 0;

    for (const mode of modes) {
      const theta = mode.kx * x + mode.ky * y + mode.phase;
      const cosTheta = Math.cos(theta);
      const sinTheta = Math.sin(theta);
      const a = mode.amp;

      ux += a * mode.ky * cosTheta;
      uy += -a * mode.kx * cosTheta;
      duxDx += -a * mode.ky * mode.kx * sinTheta;
      duxDy += -a * mode.ky * mode.ky * sinTheta;
      duyDx += a * mode.kx * mode.kx * sinTheta;
      duyDy += a * mode.kx * mode.ky * sinTheta;
    }

    const advX = ux * duxDx + uy * duxDy;
    const advY = ux * duyDx + uy * duyDy;
    nonlinearTransfer += (ux * advX + uy * advY) * cellArea;
    kineticEnergy += 0.5 * (ux * ux + uy * uy) * cellArea;
    gradEnergy += (duxDx * duxDx + duxDy * duxDy + duyDx * duyDx + duyDy * duyDy) * cellArea;
    maxDivergence = Math.max(maxDivergence, Math.abs(duxDx + duyDy));
  }
}

const tolerances = {
  nonlinear_energy_transfer_abs: 1e-10,
  max_divergence_abs: 1e-12
};

const measurements = {
  grid,
  mode_count: modes.length,
  kinetic_energy: kineticEnergy,
  gradient_energy: gradEnergy,
  viscous_dissipation_proxy: nu * gradEnergy,
  nonlinear_energy_transfer: nonlinearTransfer,
  nonlinear_energy_transfer_abs: Math.abs(nonlinearTransfer),
  max_divergence_abs: maxDivergence
};

const verdicts = {
  bounded_skew_symmetry_probe:
    measurements.nonlinear_energy_transfer_abs <= tolerances.nonlinear_energy_transfer_abs &&
    measurements.max_divergence_abs <= tolerances.max_divergence_abs
      ? "MATCH"
      : "DRIFT",
  parent_millennium_problem: "UNVERIFIABLE"
};

const receipt = {
  schema: "project-telos.pde-skew-symmetry-run-receipt/v1",
  packet_id: "navier-stokes-periodic-skew-symmetry-v0",
  generated_at: new Date().toISOString(),
  command: process.argv.join(" "),
  parameters: { grid, nu },
  source_statement_sha256: sha256(resolve(here, "problem.statement.json")),
  derivation_sha256: sha256(resolve(here, "subclaim.skew_symmetry.md")),
  assumptions: [
    "smooth finite Fourier-mode streamfunction",
    "two-dimensional periodic domain",
    "incompressible analytic velocity field",
    "analytic derivatives evaluated on a uniform periodic grid",
    "bounded witness only"
  ],
  modes,
  measurements,
  tolerances,
  verdicts,
  boundaries: [
    "This executable receipt checks one deterministic smooth periodic finite-mode witness.",
    "This executable receipt does not prove Navier-Stokes existence and smoothness.",
    "This executable receipt does not prove global regularity or physical-fluid validity.",
    "This executable receipt does not validate arbitrary numerical discretizations."
  ]
};

if (out) {
  writeFileSync(out, JSON.stringify(receipt, null, 2) + "\n");
}

console.log(JSON.stringify({
  out,
  bounded_skew_symmetry_probe: verdicts.bounded_skew_symmetry_probe,
  parent_millennium_problem: verdicts.parent_millennium_problem,
  nonlinear_energy_transfer_abs: measurements.nonlinear_energy_transfer_abs,
  max_divergence_abs: measurements.max_divergence_abs
}, null, 2));

