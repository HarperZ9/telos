# Packet 056: Elan Controlled Install Plan

Date: 2026-07-01

Status: `ELAN_CONTROLLED_INSTALL_PLAN_MATCH`

Pass 0046 converts the official Windows installer script surface into a
no-execution install plan. It records the parameters and proposed guarded
command but does not install Elan.

```text
installer_script_sha256 = 1d3c66430d0e7b719b104e1dea80e395a066e96c37b886f2de4b0e9025a037fb
installer_script_executed = false
default_toolchain = leanprover/lean4:v4.31.0
no_prompt_supported = true
no_modify_path_supported = true
default_toolchain_supported = true
start_process_present = true
```

Proposed next command shape:

```powershell
powershell -ExecutionPolicy Bypass -File elan-init.ps1 -NoPrompt 1 -NoModifyPath 1 -DefaultToolchain leanprover/lean4:v4.31.0
```

The next admissible pass should run this only with an explicit install root and
then record `elan --version`, `lean --version`, `lake --version`, and `lake env
lean --version`.

Current promoted natural laws: none.
