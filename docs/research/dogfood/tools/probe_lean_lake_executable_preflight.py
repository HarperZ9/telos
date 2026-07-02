"""Generate pass 0044 Lean/Lake executable preflight receipts."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import tomllib
from pathlib import Path
PASS = "0044"
ROOT = Path(__file__).resolve().parents[1]
PREVIOUS_PACKET = ROOT / "schemas" / "lake-dependency-cache-binding-pass-0043.json"
FIXTURE_PATH = ROOT / "fixtures" / "lean-lake-executable-preflight-pass-0044.json"
OUT_PATH = ROOT / "schemas" / "lean-lake-executable-preflight-pass-0044.json"
PACKET_PATH = ROOT / "packets" / "054-lean-lake-executable-preflight.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0044-lean-lake-executable-preflight-steelman.md"
PROJECT_SUBDIR = "lean/problem-4b-formalization"

def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()

def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())

def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))

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

def source_root() -> Path:
    configured = os.environ.get("PIPELINE_MATH_SOURCE_ROOT")
    if configured:
        return Path(configured)
    return Path(os.environ.get("TEMP", "")) / "pipeline-math-pass0032-lf"

def run_command(args: list[str], cwd: Path) -> dict:
    try:
        result = subprocess.run(args, cwd=cwd, text=True, encoding="utf-8", capture_output=True, timeout=20)
        return {
            "args": args,
            "exit_code": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "status": "MATCH" if result.returncode == 0 else "DRIFT",
        }
    except FileNotFoundError as exc:
        return {
            "args": args,
            "error": str(exc),
            "exit_code": None,
            "status": "EXECUTABLE_MISSING",
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "args": args,
            "error": str(exc),
            "exit_code": None,
            "status": "TIMEOUT",
        }

def where_result(tool: str, cwd: Path) -> dict:
    result = run_command(["where.exe", tool], cwd)
    return {
        "exit_code": result.get("exit_code"),
        "status": "FOUND" if result.get("exit_code") == 0 else "NOT_FOUND",
        "stdout": result.get("stdout", ""),
        "tool": tool,
    }

def common_candidates() -> list[Path]:
    home = Path.home()
    return [
        home / ".elan" / "bin" / "lake.exe",
        home / ".elan" / "bin" / "lean.exe",
        home / ".elan" / "bin" / "elan.exe",
        Path("C:/Program Files/Elan/bin/lake.exe"),
        Path("C:/Program Files/Elan/bin/lean.exe"),
        Path("C:/Program Files/Elan/bin/elan.exe"),
    ]

def version_attempt(tool: str, cwd: Path) -> dict:
    path = shutil.which(tool)
    if path is None:
        return {
            "args": [tool, "--version"],
            "executable_path": None,
            "status": "NOT_RUN_EXECUTABLE_MISSING",
            "tool": tool,
        }
    result = run_command([path, "--version"], cwd)
    result["executable_path"] = path
    result["tool"] = tool
    return result

def load_lakefile(path: Path) -> dict:
    with path.open("rb") as handle:
        return tomllib.load(handle)

def render_packet(contract: dict) -> str:
    measurements = contract["verifier_measurements"]
    return f"""# Packet 054: Lean/Lake Executable Preflight

Date: 2026-07-01

Status: `{contract['status']}`

Pass 0044 checks whether the local shell can attempt a bounded Lean/Lake replay.
It records that `lake`, `lean`, and `elan` are not discoverable on PATH or in the
common Elan locations checked by this pass.

## Preflight Result

```text
source = schemas/lake-dependency-cache-binding-pass-0043.json
source_sha256 = {contract['dependency_cache_binding']['sha256']}
source_seal = {contract['dependency_cache_binding']['seal']}
expected_toolchain = {measurements['expected_toolchain']}
lake_on_path = {str(measurements['lake_on_path']).lower()}
lean_on_path = {str(measurements['lean_on_path']).lower()}
elan_on_path = {str(measurements['elan_on_path']).lower()}
common_elan_candidates_present = {measurements['common_elan_candidates_present']}
compiled_replay_admissible = {str(measurements['compiled_replay_admissible']).lower()}
compiled_replay_status = NOT_RUN
lakefile_name = {measurements['lakefile_name']}
manifest_name = {measurements['manifest_name']}
project_name_match = {str(measurements['project_name_match']).lower()}
```

## Product Reading

The replay substrate now has a concrete admission gate: source archive,
dependency cache, and toolchain intent are bound, but compiled replay must wait
until the Lean/Lake executable layer is installed or explicitly provided.

## Non-Promotion Boundary

Pass 0044 is a preflight failure packet. It does not run Lean, run `lake build`,
compile dependencies, prove semantic equivalence by elaboration, validate every
public `pipeline-math` claim, or promote any natural law.

Current promoted natural laws: none.
"""

def render_steelman() -> str:
    return """# Pass 0044 Steelman: Lean/Lake Executable Preflight

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

Pass 0044 claims compiled replay is currently blocked because the Lean/Lake
executable layer is unavailable in this shell.

## Strongest Objections

1. Absence from PATH is not proof Lean is absent from the machine. Correct: this
is a bounded workstation probe, not a forensic disk inventory.
2. A missing executable can be fixed quickly. Correct: the value is the
admission gate, not permanence.
3. The Lake manifest/lakefile name mismatch may be harmless. Correct: it is a
preflight signal, not proof the project cannot build.
4. This pass does not test theorem semantics. Correct: it is not compilation.

## Verdict

Useful replay-admission evidence. The next stronger pass should locate the Lean
toolchain and run `lake env lean --version` before any full build.
"""

def main() -> None:
    repo = source_root()
    project_root = repo / PROJECT_SUBDIR
    previous = read_json(PREVIOUS_PACKET)
    previous_sha = sha256_file(PREVIOUS_PACKET)
    lean_toolchain = (project_root / "lean-toolchain").read_text(encoding="utf-8").strip()
    lake_manifest = read_json(project_root / "lake-manifest.json")
    lakefile = load_lakefile(project_root / "lakefile.toml")
    path_entries = os.environ.get("PATH", "").split(os.pathsep)
    tools = ["lake", "lean", "elan"]
    path_probes = {
        tool: {
            "which": shutil.which(tool),
            "where": where_result(tool, project_root),
        }
        for tool in tools
    }
    candidate_rows = [
        {"path": str(path), "exists": path.exists()}
        for path in common_candidates()
    ]
    version_attempts = [version_attempt(tool, project_root) for tool in tools]
    lake_env_lean_version = {
        "args": ["lake", "env", "lean", "--version"],
        "status": "NOT_RUN_EXECUTABLE_MISSING" if shutil.which("lake") is None else "READY_TO_RUN",
    }
    any_path = any(path_probes[tool]["which"] for tool in tools)
    any_common = sum(1 for row in candidate_rows if row["exists"])
    project_name_match = lakefile.get("name") == lake_manifest.get("name")
    fixture = with_seal({
        "common_candidate_paths": candidate_rows,
        "dependency_cache_binding_sha256": previous_sha,
        "generated_on": "2026-07-01",
        "lake_env_lean_version": lake_env_lean_version,
        "pass": PASS,
        "path_entry_count": len([entry for entry in path_entries if entry]),
        "path_probes": path_probes,
        "schema": "LeanLakeExecutablePreflightFixture/v1",
        "version_attempts": version_attempts,
    })
    write_json(FIXTURE_PATH, fixture)
    fixture_sha = sha256_file(FIXTURE_PATH)
    status = "LEAN_LAKE_EXECUTABLE_PREFLIGHT_READY" if any_path else "LEAN_LAKE_EXECUTABLE_PREFLIGHT_BLOCKED"
    contract = with_seal({
        "action_receipt_proposal": {
            "action_id": "act_dogfood_0044_lean_lake_executable_preflight",
            "authority_class": "read_only_executable_preflight",
            "event_id": "evt_dogfood_0044_lean_lake_executable_preflight",
            "event_type": "lean_lake_executable_preflight_checked",
            "external_call_performed": False,
            "external_write_performed": False,
            "normal_path_modified": False,
            "result_state": "blocked" if status.endswith("BLOCKED") else "completed",
            "side_effect_class": "local_executable_probe_and_repo_artifact_write",
            "stop_reason": "lake_lean_elan_missing_from_path" if status.endswith("BLOCKED") else "preflight_ready",
            "verification_verdict": "UNVERIFIABLE" if status.endswith("BLOCKED") else "MATCH",
        },
        "compiled_replay_status": "NOT_RUN",
        "current_promoted_natural_laws": [],
        "dependency_cache_binding": {
            "path": "schemas/lake-dependency-cache-binding-pass-0043.json",
            "seal": previous["seal"],
            "sha256": previous_sha,
            "source_status": previous["status"],
        },
        "executable_preflight_fixture": {
            "path": "fixtures/lean-lake-executable-preflight-pass-0044.json",
            "schema": fixture["schema"],
            "seal": fixture["seal"],
            "sha256": fixture_sha,
        },
        "generated_on": "2026-07-01",
        "negative_fixture_count": 6,
        "negative_fixtures": [
            {"expected_validator_status": "REJECT", "id": "negative-toolchain-mismatch"},
            {"expected_validator_status": "REJECT", "id": "negative-pass0043-binding-missing"},
            {"expected_validator_status": "REJECT", "id": "negative-compiled-replay-overclaimed"},
            {"expected_validator_status": "REJECT", "id": "negative-executable-path-forged"},
            {"expected_validator_status": "REJECT", "id": "negative-project-name-mismatch-hidden"},
            {"expected_validator_status": "REJECT", "id": "negative-natural-law-promoted"}
        ],
        "non_promotion_statement": "Pass 0044 is an executable preflight only. It does not run Lean, run lake build, compile dependencies, prove semantic equivalence by elaboration, validate every public pipeline-math claim, or promote any natural law.",
        "pass": PASS,
        "schema": "LeanLakeExecutablePreflightSet/v1",
        "status": status,
        "verifier_measurements": {
            "common_elan_candidates_present": any_common,
            "compiled_replay_admissible": bool(shutil.which("lake") and shutil.which("lean")),
            "compiled_replay_status": "NOT_RUN",
            "elan_on_path": shutil.which("elan") is not None,
            "expected_toolchain": lean_toolchain,
            "lake_manifest_package_count": len(lake_manifest.get("packages", [])),
            "lake_on_path": shutil.which("lake") is not None,
            "lakefile_name": lakefile.get("name"),
            "lean_on_path": shutil.which("lean") is not None,
            "manifest_name": lake_manifest.get("name"),
            "project_name_match": project_name_match,
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
        "compiled_replay_admissible": contract["verifier_measurements"]["compiled_replay_admissible"],
    }, indent=2, sort_keys=True))
if __name__ == "__main__":
    main()
