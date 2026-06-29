# Forward-Facing Repository Inventory

Snapshot date: 2026-06-29

This inventory tracks the public/developer presentation rollout for HarperZ9 repositories. It uses GitHub repository metadata, local Git remotes under `C:/dev`, and the Telos presentation audit tool.

## Current Counts

- Owned public repositories on GitHub: 47.
- Public forks on GitHub: 11.
- Active private repositories on GitHub: 25.
- Owned public repositories with a local clone found under `C:/dev`: 46 of 47.
- Missing local clone from the scanned tree: `.github`.
- Exact local presentation audit: 46 owned-public repositories audited, 5 `MATCH`, 41 `DRIFT`.

## Completed Public Flagship Set

These now pass the public/developer presentation audit and have merged presentation updates with green main CI.

- `gather`
- `crucible`
- `index`
- `forum`
- `telos`

## Standard

Apply [PRESENTATION-STANDARD.md](PRESENTATION-STANDARD.md) to every forward-facing repository.

Each repository needs two layers:

- Public layer: plain first-screen description, why it matters, quickstart, and non-cryptic visual hierarchy.
- Developer layer: install/setup, runnable command, verification command, integration surfaces, status, license, and provenance/receipt behavior where relevant.

Visual direction uses `r/design`, `r/design_critiques`, and `r/posterdesign` as non-evidentiary critique lanes for hierarchy, poster readability, focal control, typography, and effect restraint.

## Rollout Batches

Batch 1: product front doors and high-visibility engines.

- `HarperZ9`
- `HarperZ9.github.io`
- `studio-engine`
- `reconcile`
- `calibrate-pro`
- `quantalang`
- `quanta-color`
- `raw`

Batch 2: AI workflow, provenance, and release-safety utilities.

- `accountable-engine`
- `accountable-surface`
- `agent-audit`
- `agent-hook-pack`
- `agent-routing-kit`
- `proof-surface`
- `proof-surface-report`
- `provenance-sensorium`
- `model-provenance-validator`
- `secret-redact-io`
- `repo-proof-index`
- `release-surface-scanner`
- `public-surface-sweeper`

Batch 3: Quanta ecosystem.

- `quanta-ecosystem`
- `quanta-engine`
- `quanta-finance`
- `quanta-oracle`
- `quanta-ui`
- `quanta-universe`
- `quantalang-vscode`
- `quantalang-tmLanguage`

Batch 4: research, kernels, and validation libraries.

- `emet`
- `faithful-transpile`
- `senses-and-sensibility`
- `witnessing-spine`
- `coherence-membrane`
- `context-curator-lite`
- `gpu-trace-validator`
- `signal-kernels`
- `anomaly-kernels`

Batch 5: smaller public utilities and templates.

- `workflow-harness-lite`
- `wol-pi`
- `consulting-template-kit`

## Fork Policy

Public forks are forward-facing, but they should not receive Harper/Telos product branding by default. Treat them as upstream-contribution surfaces: clean patches, bug fixes, issue reproductions, and narrow README notes only when the fork has a Harper-specific purpose.

