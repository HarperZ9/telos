# Dogfood Pass 0045 Ledger

Date: 2026-07-01

Status: `CRUCIBLE_MATCH`.

Crucible assessment:

- thesis id: `b00abd379c004c9f`;
- claims: `8`;
- match: `8`;
- drift: `0`;
- unverifiable: `0`;
- thesis seal: `b00abd379c004c9fee8d78286fe32541229416b67946bab2dc4daa8cac63cde3`;
- verdict seal: `7eb739c6f6f2c145d57270e3ffec78c2eb12606027932e8ac95d322dd04d3e21`;
- measurement seal: `709e2993e27742b6aa51a7ac7e5f65df90be8073aecc7dbfb4c0087c96cef719`;
- assessment seal: `b725a6e1fcd081bd1a8a720082cdd3a8d4b6c89eea5eb4dc2bc421aab77c6113`;
- integrity: `seals_ok=True`, `thesis_ok=True`, `verdicts_rederive=True`.

Pass theme: official Lean/Elan acquisition sources. The pass fetches and hashes
four source anchors, including the Windows `elan-init.ps1` installer script, but
does not execute any installer or modify PATH.

## Primary Receipt

```text
path = schemas/lean-toolchain-acquisition-sources-pass-0045.json
schema = LeanToolchainAcquisitionSourcesSet/v1
status = LEAN_TOOLCHAIN_ACQUISITION_SOURCES_MATCH
sha256 = 924ef19e25fbaf101001b0cc9caf25d929f13fcb034f2aa6bcc4720101c56117
seal = b31f2684d77de7f83ef71ec4b4ef1230d8b265c36758736d03cffade4149868e
source_count = 4
source_match_count = 4
```

Source receipts:

```text
lean_manual_install = MATCH http=200 sha256=a452aecbbaad48706bd5a63443e13d49af8aef314ed2e9b0d46cbf5231d1a723
lean_elan_toolchains = MATCH http=200 sha256=fb7052c9a665a1e685ec930895eb92bb7111ccea519de43a482597b4f6d167f6
elan_readme = MATCH http=200 sha256=6778277cc096b30fbd7132ac420a85184a39a7f5b2b863b1841efee13de84d44
elan_windows_installer_script = MATCH http=200 sha256=1d3c66430d0e7b719b104e1dea80e395a066e96c37b886f2de4b0e9025a037fb
```

Installer boundary:

```text
windows_installer_script_fetched = true
windows_installer_script_executed = false
expected_project_toolchain = leanprover/lean4:v4.31.0
```

Source binding:

```text
path = schemas/lean-lake-executable-preflight-pass-0044.json
sha256 = d98513f50b384ed38e4d52d6379916bc6b43dacc318571e0299ecd1d3dcc055f
seal = 7139ea2e8ed154dcb5069fd5d5433fec85103b88d9bf309450dfd1193a6de607
status = LEAN_LAKE_EXECUTABLE_PREFLIGHT_BLOCKED
```

## Artifacts

| Artifact | Role |
| --- | --- |
| `tools/probe_lean_toolchain_acquisition_sources.py` | Official Lean/Elan acquisition-source fetch generator. |
| `tools/validate_pass_0045_lean_toolchain_acquisition_sources.py` | Validator for pass 0045 source receipts, pass 0044 binding, installer non-execution, and non-promotion controls. |
| `fixtures/lean-toolchain-acquisition-sources-pass-0045.json` | Lean/Elan acquisition source fixture. |
| `packets/055-lean-toolchain-acquisition-sources.md` | Human-readable acquisition source packet. |
| `adversarial/pass-0045-lean-toolchain-acquisition-sources-steelman.md` | Local pass 0045 steelman. |
| `schemas/lean-toolchain-acquisition-sources-pass-0045.json` | `LeanToolchainAcquisitionSourcesSet/v1` artifact. |
| `schemas/pass-0045-lean-toolchain-acquisition-sources-validator-result.json` | Validator receipt for pass 0045. |
| `schemas/tool-receipts-pass-0045.json` | Compact Index, Gather, Shell, Telos, Forum, and Crucible receipts. |
| `crucible/pass-0045-thesis.json` | Falsifiable claims for the forty-fifth pass. |
| `crucible/pass-0045-measurements.json` | Measurements/evidence for the forty-fifth pass. |
| `crucible/pass-0045-report.md` | Crucible report for the forty-fifth pass. |
| `crucible/pass-0045-run.json` | Crucible run record for the forty-fifth pass. |

## Primary Next Push

Create a controlled local Elan install plan that can install into an explicit
toolchain home and produce rollback, PATH, version, and `lake env lean --version`
receipts.

## Natural-Law Promotion

Current promoted natural laws: none.
