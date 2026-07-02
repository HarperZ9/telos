"""Generate pass 0045 source receipts for Lean/Elan toolchain acquisition."""
from __future__ import annotations

import hashlib
import json
import urllib.request
from pathlib import Path


PASS = "0045"
ROOT = Path(__file__).resolve().parents[1]
PREVIOUS_PACKET = ROOT / "schemas" / "lean-lake-executable-preflight-pass-0044.json"
FIXTURE_PATH = ROOT / "fixtures" / "lean-toolchain-acquisition-sources-pass-0045.json"
OUT_PATH = ROOT / "schemas" / "lean-toolchain-acquisition-sources-pass-0045.json"
PACKET_PATH = ROOT / "packets" / "055-lean-toolchain-acquisition-sources.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0045-lean-toolchain-acquisition-sources-steelman.md"
SOURCES = [
    {
        "id": "lean_manual_install",
        "url": "https://lean-lang.org/install/manual/",
        "must_contain": ["elan-init.ps1", "powershell -ExecutionPolicy Bypass", "lake build"],
    },
    {
        "id": "lean_elan_toolchains",
        "url": "https://lean-lang.org/doc/reference/latest/Build-Tools-and-Distribution/Managing-Toolchains-with-Elan/",
        "must_contain": ["lean-toolchain", "leanprover/lean4", "toolchain file"],
    },
    {
        "id": "elan_readme",
        "url": "https://raw.githubusercontent.com/leanprover/elan/master/README.md",
        "must_contain": ["lean", "lake", "elan-init.ps1"],
    },
    {
        "id": "elan_windows_installer_script",
        "url": "https://elan.lean-lang.org/elan-init.ps1",
        "must_contain": ["elan-init", "NoModifyPath", "DefaultToolchain"],
    },
]


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


def fetch_source(source: dict) -> dict:
    request = urllib.request.Request(source["url"], headers={"User-Agent": "telos-dogfood/0045"})
    with urllib.request.urlopen(request, timeout=30) as response:
        body = response.read()
        text = body.decode("utf-8", errors="replace")
        contains = {needle: needle in text for needle in source["must_contain"]}
        return {
            "bytes": len(body),
            "contains": contains,
            "id": source["id"],
            "sha256": sha256_bytes(body),
            "status": "MATCH" if response.status == 200 and all(contains.values()) else "DRIFT",
            "status_code": response.status,
            "url": source["url"],
        }


def render_packet(contract: dict) -> str:
    m = contract["verifier_measurements"]
    return f"""# Packet 055: Lean Toolchain Acquisition Sources

Date: 2026-07-01

Status: `{contract['status']}`

Pass 0045 records official source anchors for unblocking Lean/Lake replay on
Windows. It fetches the installer script for hashing only and does not execute
it.

## Acquisition Sources

```text
source_count = {m['source_count']}
source_match_count = {m['source_match_count']}
windows_installer_script_fetched = {str(m['windows_installer_script_fetched']).lower()}
windows_installer_script_executed = false
previous_preflight_status = {contract['executable_preflight_binding']['source_status']}
expected_project_toolchain = {contract['expected_project_toolchain']}
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
"""


def render_steelman() -> str:
    return """# Pass 0045 Steelman: Lean Toolchain Acquisition Sources

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

This pass proves source availability and installer-script identity only. It does
not prove a future install will succeed, that the fetched script is safe to run,
or that a later `lake build` will pass. The stronger follow-up is a controlled
install receipt with executable paths, versions, and rollback notes.
"""


def main() -> None:
    previous = read_json(PREVIOUS_PACKET)
    previous_sha = sha256_file(PREVIOUS_PACKET)
    fetches = [fetch_source(source) for source in SOURCES]
    fixture = with_seal({
        "fetches": fetches,
        "generated_on": "2026-07-01",
        "pass": PASS,
        "schema": "LeanToolchainAcquisitionSourcesFixture/v1",
    })
    write_json(FIXTURE_PATH, fixture)
    fixture_sha = sha256_file(FIXTURE_PATH)
    all_match = all(row["status"] == "MATCH" for row in fetches)
    installer = next(row for row in fetches if row["id"] == "elan_windows_installer_script")
    contract = with_seal({
        "action_receipt_proposal": {
            "action_id": "act_dogfood_0045_lean_toolchain_acquisition_sources",
            "authority_class": "read_only_external_source_fetch",
            "event_id": "evt_dogfood_0045_lean_toolchain_acquisition_sources",
            "event_type": "lean_toolchain_acquisition_sources_verified",
            "external_call_performed": True,
            "external_write_performed": False,
            "installer_script_executed": False,
            "normal_path_modified": False,
            "result_state": "completed" if all_match else "source_drift",
            "verification_verdict": "MATCH" if all_match else "DRIFT",
        },
        "current_promoted_natural_laws": [],
        "executable_preflight_binding": {
            "path": "schemas/lean-lake-executable-preflight-pass-0044.json",
            "seal": previous["seal"],
            "sha256": previous_sha,
            "source_status": previous["status"],
        },
        "expected_project_toolchain": previous["verifier_measurements"]["expected_toolchain"],
        "generated_on": "2026-07-01",
        "non_promotion_statement": "Pass 0045 fetches official acquisition sources only. It does not install Elan, run Lean, run lake build, compile dependencies, validate every public pipeline-math claim, or promote any natural law.",
        "pass": PASS,
        "schema": "LeanToolchainAcquisitionSourcesSet/v1",
        "source_receipts": fetches,
        "status": "LEAN_TOOLCHAIN_ACQUISITION_SOURCES_MATCH" if all_match else "LEAN_TOOLCHAIN_ACQUISITION_SOURCES_DRIFT",
        "toolchain_acquisition_fixture": {
            "path": "fixtures/lean-toolchain-acquisition-sources-pass-0045.json",
            "schema": fixture["schema"],
            "seal": fixture["seal"],
            "sha256": fixture_sha,
        },
        "verifier_measurements": {
            "installer_script_sha256": installer["sha256"],
            "source_count": len(fetches),
            "source_match_count": sum(1 for row in fetches if row["status"] == "MATCH"),
            "windows_installer_script_executed": False,
            "windows_installer_script_fetched": installer["status_code"] == 200,
        },
    })
    write_json(OUT_PATH, contract)
    write_text(PACKET_PATH, render_packet(contract))
    write_text(STEELMAN_PATH, render_steelman())
    print(json.dumps({
        "path": str(OUT_PATH),
        "schema": contract["schema"],
        "seal": contract["seal"],
        "status": contract["status"],
        "source_match_count": contract["verifier_measurements"]["source_match_count"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
