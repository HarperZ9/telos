# Dogfood Pass 0046 Ledger

Date: 2026-07-01

Status: `CRUCIBLE_MATCH`.

Crucible assessment:

- thesis id: `8f4e98bce0a0543b`;
- claims: `8`;
- match: `8`;
- drift: `0`;
- unverifiable: `0`;
- thesis seal: `8f4e98bce0a0543bd5e48212cb6147ff2919d80b24aa6bf03832d1b3562c9f83`;
- verdict seal: `332b334d34495bdbcfc609adc417ffe6d132dcf08cfeee967a8819cb12979cc6`;
- measurement seal: `0d723ba9a6aa56f73da8e71b114555609028344fb49be7dd32cd0da0d1f5b288`;
- assessment seal: `46b0fddd9d9faf7930582d54bea1bcd06715865ffb9a0c59fbccf38faa8f1b4e`.

Pass theme: controlled Elan install-plan parameters. This pass records that the
official Windows installer surface supports `NoPrompt`, `NoModifyPath`, and an
explicit `DefaultToolchain`, and proposes a no-PATH-modification command shape.

```text
schema = ElanControlledInstallPlanSet/v1
status = ELAN_CONTROLLED_INSTALL_PLAN_MATCH
sha256 = 6620e88e5ed7afe4e4706ae884ff7dd66af2692081d8a135a485dbe80b3c25d5
seal = 0e79d9f03e7029462e50fcd7785d4ff3406cdb8fcd125f9202c51f32ee1e5d57
installer_script_executed = false
proposed_command_shape = powershell -ExecutionPolicy Bypass -File elan-init.ps1 -NoPrompt 1 -NoModifyPath 1 -DefaultToolchain leanprover/lean4:v4.31.0
```

## Artifacts

| Artifact | Role |
| --- | --- |
| `tools/probe_elan_controlled_install_plan.py` | Controlled Elan install-plan generator. |
| `tools/validate_pass_0046_elan_controlled_install_plan.py` | Validator for pass 0046 installer controls, pass 0045 binding, and non-execution boundary. |
| `fixtures/elan-controlled-install-plan-pass-0046.json` | Controlled install-plan fixture. |
| `packets/056-elan-controlled-install-plan.md` | Human-readable controlled install-plan packet. |
| `adversarial/pass-0046-elan-controlled-install-plan-steelman.md` | Local pass 0046 steelman. |
| `schemas/elan-controlled-install-plan-pass-0046.json` | `ElanControlledInstallPlanSet/v1` artifact. |
| `schemas/pass-0046-elan-controlled-install-plan-validator-result.json` | Validator receipt for pass 0046. |
| `schemas/tool-receipts-pass-0046.json` | Compact Index, Gather, Shell, Forum, and Crucible receipts. |
| `crucible/pass-0046-thesis.json` | Falsifiable claims for the forty-sixth pass. |
| `crucible/pass-0046-measurements.json` | Measurements/evidence for the forty-sixth pass. |
| `crucible/pass-0046-report.md` | Crucible report for the forty-sixth pass. |
| `crucible/pass-0046-run.json` | Crucible run record for the forty-sixth pass. |

## Primary Next Push

Run a controlled local install only if the next pass can capture install root,
PATH impact, rollback state, executable paths, and `lake env lean --version`.

Current promoted natural laws: none.
