# Packet 055: Lean Toolchain Acquisition Sources

Date: 2026-07-01

Status: `LEAN_TOOLCHAIN_ACQUISITION_SOURCES_MATCH`

Pass 0045 records official source anchors for unblocking Lean/Lake replay on
Windows. It fetches the installer script for hashing only and does not execute
it.

## Acquisition Sources

```text
source_count = 4
source_match_count = 4
windows_installer_script_fetched = true
windows_installer_script_executed = false
previous_preflight_status = LEAN_LAKE_EXECUTABLE_PREFLIGHT_BLOCKED
expected_project_toolchain = leanprover/lean4:v4.31.0
```

## Product Reading

The replay path now has an acquisition source packet: official Lean install
docs, official Elan toolchain behavior docs, the Elan README, and the Windows
installer script hash. The next step can either install into a controlled local
toolchain home or keep this as a blocked preflight.

## Non-Promotion Boundary

Pass 0045 does not install Elan, run Lean, run `lake build`, compile
dependencies, validate every public `pipeline-math` claim, or promote any
natural law.

Current promoted natural laws: none.
