"""Generate pass 0046 controlled Elan install-plan receipts without executing."""
from __future__ import annotations

import hashlib
import json
import urllib.request
from pathlib import Path


PASS = "0046"
ROOT = Path(__file__).resolve().parents[1]
PREVIOUS_PACKET = ROOT / "schemas" / "lean-toolchain-acquisition-sources-pass-0045.json"
OUT_PATH = ROOT / "schemas" / "elan-controlled-install-plan-pass-0046.json"
FIXTURE_PATH = ROOT / "fixtures" / "elan-controlled-install-plan-pass-0046.json"
PACKET_PATH = ROOT / "packets" / "056-elan-controlled-install-plan.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0046-elan-controlled-install-plan-steelman.md"
INSTALLER_URL = "https://elan.lean-lang.org/elan-init.ps1"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def sha256_obj(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def write_json(path: Path, value: object) -> None:
    write_text(path, json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def with_seal(value: dict) -> dict:
    sealed = dict(value)
    sealed["seal"] = sha256_obj(value)
    return sealed


def fetch_installer() -> tuple[bytes, str]:
    request = urllib.request.Request(INSTALLER_URL, headers={"User-Agent": "telos-dogfood/0046"})
    with urllib.request.urlopen(request, timeout=30) as response:
        body = response.read()
    return body, body.decode("utf-8", errors="replace")


def extract_markers(text: str) -> dict:
    markers = [
        "NoPrompt",
        "NoModifyPath",
        "DefaultToolchain",
        "ElanRoot",
        "ElanVersion",
        "--no-modify-path",
        "--default-toolchain",
        "Start-Process",
        "Invoke-WebRequest",
    ]
    rows: dict[str, list[int]] = {}
    lines = text.splitlines()
    for marker in markers:
        rows[marker] = [index for index, line in enumerate(lines, 1) if marker.lower() in line.lower()]
    return rows


def render_packet(contract: dict) -> str:
    m = contract["verifier_measurements"]
    return f"""# Packet 056: Elan Controlled Install Plan

Date: 2026-07-01

Status: `{contract['status']}`

Pass 0046 converts the official Windows installer script surface into a
no-execution install plan. It records the parameters and proposed guarded
command but does not install Elan.

```text
installer_script_sha256 = {m['installer_script_sha256']}
installer_script_executed = false
default_toolchain = {m['default_toolchain']}
no_prompt_supported = {str(m['no_prompt_supported']).lower()}
no_modify_path_supported = {str(m['no_modify_path_supported']).lower()}
default_toolchain_supported = {str(m['default_toolchain_supported']).lower()}
start_process_present = {str(m['start_process_present']).lower()}
```

Proposed next command shape:

```powershell
{contract['proposed_command_shape']}
```

The next admissible pass should run this only with an explicit install root and
then record `elan --version`, `lean --version`, `lake --version`, and `lake env
lean --version`.

Current promoted natural laws: none.
"""


def render_steelman() -> str:
    return """# Pass 0046 Steelman: Elan Controlled Install Plan

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

This pass does not prove installation safety or build success. It only proves
that the fetched script exposes no-prompt, no-PATH-modification, and explicit
default-toolchain controls and records a proposed guarded command shape.
"""


def main() -> None:
    previous = read_json(PREVIOUS_PACKET)
    previous_sha = sha256_file(PREVIOUS_PACKET)
    body, text = fetch_installer()
    markers = extract_markers(text)
    installer_sha = sha256_bytes(body)
    default_toolchain = previous["expected_project_toolchain"]
    proposed = (
        "powershell -ExecutionPolicy Bypass -File elan-init.ps1 "
        f"-NoPrompt 1 -NoModifyPath 1 -DefaultToolchain {default_toolchain}"
    )
    fixture = with_seal({
        "generated_on": "2026-07-01",
        "installer_sha256": installer_sha,
        "markers": markers,
        "pass": PASS,
        "schema": "ElanControlledInstallPlanFixture/v1",
    })
    write_json(FIXTURE_PATH, fixture)
    fixture_sha = sha256_file(FIXTURE_PATH)
    measurements = {
        "default_toolchain": default_toolchain,
        "default_toolchain_supported": bool(markers["DefaultToolchain"] and markers["--default-toolchain"]),
        "elan_root_supported": bool(markers["ElanRoot"]),
        "elan_version_supported": bool(markers["ElanVersion"]),
        "installer_script_executed": False,
        "installer_script_sha256": installer_sha,
        "invoke_web_request_present": bool(markers["Invoke-WebRequest"]),
        "no_modify_path_supported": bool(markers["NoModifyPath"] and markers["--no-modify-path"]),
        "no_prompt_supported": bool(markers["NoPrompt"]),
        "start_process_present": bool(markers["Start-Process"]),
    }
    all_supported = all([
        measurements["default_toolchain_supported"],
        measurements["no_modify_path_supported"],
        measurements["no_prompt_supported"],
        measurements["start_process_present"],
    ])
    contract = with_seal({
        "action_receipt_proposal": {
            "action_id": "act_dogfood_0046_elan_controlled_install_plan",
            "authority_class": "read_only_install_plan",
            "event_id": "evt_dogfood_0046_elan_controlled_install_plan",
            "event_type": "elan_controlled_install_plan_verified",
            "external_call_performed": True,
            "external_write_performed": False,
            "installer_script_executed": False,
            "normal_path_modified": False,
            "verification_verdict": "MATCH" if all_supported else "DRIFT",
        },
        "acquisition_source_binding": {
            "path": "schemas/lean-toolchain-acquisition-sources-pass-0045.json",
            "seal": previous["seal"],
            "sha256": previous_sha,
            "source_status": previous["status"],
        },
        "current_promoted_natural_laws": [],
        "elan_controlled_install_fixture": {
            "path": "fixtures/elan-controlled-install-plan-pass-0046.json",
            "schema": fixture["schema"],
            "seal": fixture["seal"],
            "sha256": fixture_sha,
        },
        "generated_on": "2026-07-01",
        "non_promotion_statement": "Pass 0046 records an install plan only. It does not execute elan-init.ps1, install Elan, run Lean, run lake build, compile dependencies, validate every public pipeline-math claim, or promote any natural law.",
        "pass": PASS,
        "proposed_command_shape": proposed,
        "schema": "ElanControlledInstallPlanSet/v1",
        "status": "ELAN_CONTROLLED_INSTALL_PLAN_MATCH" if all_supported else "ELAN_CONTROLLED_INSTALL_PLAN_DRIFT",
        "verifier_measurements": measurements,
    })
    write_json(OUT_PATH, contract)
    write_text(PACKET_PATH, render_packet(contract))
    write_text(STEELMAN_PATH, render_steelman())
    print(json.dumps({
        "path": str(OUT_PATH),
        "schema": contract["schema"],
        "seal": contract["seal"],
        "status": contract["status"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
