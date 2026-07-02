"""Validate pass 0030 theorem replay preflight receipts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "theorem-replay-preflight-pass-0030.json"
FIXTURE_PATH = ROOT / "fixtures" / "pipeline-math-problem4b-preflight-pass-0030.json"
SOURCE_PACKET_PATH = ROOT / "schemas" / "research-claim-packet-pass-0029.json"
RESULT_PATH = ROOT / "schemas" / "pass-0030-theorem-replay-preflight-validator-result.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    data = load_json(SCHEMA_PATH)
    fixture = load_json(FIXTURE_PATH)
    source_packet = load_json(SOURCE_PACKET_PATH)
    errors: list[str] = []

    require(data.get("schema") == "TheoremReplayPreflightPacket/v1", errors, "wrong schema")
    require(data.get("pass") == "0030", errors, "wrong pass")
    require(data.get("status") == "THEOREM_REPLAY_PREFLIGHT_MATCH_WITH_TOOLCHAIN_GAP", errors, "wrong status")
    require(data.get("seal") == sha256_obj({key: value for key, value in data.items() if key != "seal"}), errors, "seal mismatch")

    binding = data.get("source_packet_binding", {})
    require(binding.get("path") == "schemas/research-claim-packet-pass-0029.json", errors, "wrong source packet path")
    require(binding.get("sha256") == sha256_file(SOURCE_PACKET_PATH), errors, "source packet sha mismatch")
    require(binding.get("seal") == source_packet.get("seal"), errors, "source packet seal mismatch")
    require(binding.get("schema") == "ResearchClaimPacket/v1", errors, "source packet schema mismatch")

    preflight_ref = data.get("preflight_fixture", {})
    require(preflight_ref.get("path") == "fixtures/pipeline-math-problem4b-preflight-pass-0030.json", errors, "wrong fixture path")
    require(preflight_ref.get("sha256") == sha256_file(FIXTURE_PATH), errors, "fixture sha mismatch")
    require(preflight_ref.get("seal") == fixture.get("seal"), errors, "fixture seal mismatch")
    require(fixture.get("seal") == sha256_obj({key: value for key, value in fixture.items() if key != "seal"}), errors, "fixture self seal mismatch")

    repo = data.get("repo_receipt", {})
    require(repo.get("url") == "https://github.com/Pengbinghui/pipeline-math.git", errors, "repo URL mismatch")
    require(repo.get("commit") == "69d7df765a8f377a5e0628c6d36c088bce7642c9", errors, "repo commit mismatch")
    require(repo.get("lean_file_count") == 66, errors, "lean file count mismatch")
    require(repo.get("formalization_project_count") == 4, errors, "project count mismatch")
    require(len(repo.get("formalization_projects", [])) == 4, errors, "project list count mismatch")
    require("lean/problem-4b-formalization" in repo.get("formalization_projects", []), errors, "problem 4b project missing")

    project = data.get("selected_project", {})
    theorem_names = project.get("theorem_names", [])
    require(project.get("path") == "lean/problem-4b-formalization", errors, "selected project path mismatch")
    require(project.get("lean_toolchain") == "leanprover/lean4:v4.31.0", errors, "lean toolchain mismatch")
    require(project.get("theorem_count") == len(theorem_names), errors, "theorem count field mismatch")
    require(len(theorem_names) == 10, errors, "wrong theorem count")
    require("problem4b_false" in theorem_names, errors, "problem4b_false theorem missing")
    require("quasiCoherent_imp_finiteConductor" in theorem_names, errors, "quasiCoherent theorem missing")

    pins = data.get("frozen_pin_receipt", {})
    require(pins.get("pin_matches_git_blob_bytes") is True, errors, "pin should match git blob bytes")
    require(pins.get("pin_matches_windows_worktree_bytes") is False, errors, "pin should not match CRLF worktree bytes")
    line = pins.get("line_ending_probe", {})
    require(line.get("git_index") == "lf", errors, "git index eol mismatch")
    require(line.get("working_tree") == "crlf", errors, "working tree eol mismatch")
    require(line.get("eol_drift") is True, errors, "eol drift not detected")
    pinned = pins.get("pinned_git_blob_hashes", {})
    blobs = pins.get("git_blob_hashes", {})
    worktree = pins.get("working_tree_hashes", {})
    require(pinned.get("Prob4b/Defs.lean") == blobs.get("Prob4b/Defs.lean"), errors, "Defs pin/blob mismatch")
    require(pinned.get("Prob4b/Theorems.lean") == blobs.get("Prob4b/Theorems.lean"), errors, "Theorems pin/blob mismatch")
    require(worktree.get("Prob4b/Defs.lean") != blobs.get("Prob4b/Defs.lean"), errors, "Defs worktree drift missing")
    require(worktree.get("Prob4b/Theorems.lean") != blobs.get("Prob4b/Theorems.lean"), errors, "Theorems worktree drift missing")

    toolchain = data.get("toolchain_receipt", {})
    require(toolchain.get("git") == "MATCH", errors, "git unavailable")
    require(toolchain.get("python") == "MATCH", errors, "python unavailable")
    require(toolchain.get("bash") == "UNAVAILABLE", errors, "bash status mismatch")
    require(toolchain.get("lake") == "UNAVAILABLE", errors, "lake status mismatch")
    require(toolchain.get("lean") == "UNAVAILABLE", errors, "lean status mismatch")
    require(toolchain.get("verify_script_attempt_status") == "UNVERIFIABLE_TOOL_UNAVAILABLE", errors, "verify status mismatch")
    require(toolchain.get("verify_script_missing_command") == "bash", errors, "missing command mismatch")
    require(toolchain.get("lean_replay_status") == "UNVERIFIABLE_TOOL_UNAVAILABLE", errors, "lean replay status mismatch")
    require(toolchain.get("replay_promotion_allowed") is False, errors, "replay promotion allowed")

    proposal = data.get("action_receipt_proposal", {})
    require(proposal.get("schema") == "ActionReceiptTheoremReplayPreflight/v1", errors, "proposal schema mismatch")
    require(proposal.get("event_type") == "theorem_replay_preflight_created", errors, "proposal event type mismatch")
    require(proposal.get("external_write_performed") is False, errors, "external write performed")
    require(proposal.get("toolchain_install_performed") is False, errors, "toolchain install performed")
    require(proposal.get("replay_promotion_allowed") is False, errors, "proposal replay promotion allowed")
    require(proposal.get("verification", {}).get("verdict") == "MATCH", errors, "proposal verification mismatch")

    measures = data.get("verifier_measurements", {})
    require(measures.get("formalization_project_count") == 4, errors, "measurement project count mismatch")
    require(measures.get("lean_file_count") == 66, errors, "measurement lean file count mismatch")
    require(measures.get("selected_theorem_count") == 10, errors, "measurement theorem count mismatch")
    commands = measures.get("required_commands_available", {})
    require(commands.get("git") is True and commands.get("python") is True, errors, "available command mismatch")
    require(commands.get("bash") is False and commands.get("lake") is False and commands.get("lean") is False, errors, "missing command mismatch")
    require(measures.get("pin_matches_git_blob_bytes") is True, errors, "measurement git blob pin mismatch")
    require(measures.get("pin_matches_windows_worktree_bytes") is False, errors, "measurement worktree pin mismatch")
    require(measures.get("line_ending_drift_detected") is True, errors, "measurement line-ending drift mismatch")
    require(measures.get("lean_replay_status") == "UNVERIFIABLE_TOOL_UNAVAILABLE", errors, "measurement replay status mismatch")
    require(measures.get("replay_success_promoted") is False, errors, "replay success promoted")
    require(measures.get("measurement_status") == "MATCH", errors, "measurement status mismatch")

    negatives = data.get("negative_fixtures", [])
    require(data.get("negative_fixture_count") == len(negatives), errors, "negative count mismatch")
    require(len(negatives) >= 10, errors, "expected at least ten negatives")
    require(all(item.get("expected_validator_status") == "REJECT" for item in negatives), errors, "negative not rejected")
    required_negative_ids = {
        "negative-lean-replay-promoted-without-lean",
        "negative-lake-build-promoted-without-lake",
        "negative-verify-script-promoted-without-bash",
        "negative-frozen-pin-worktree-mismatch-ignored",
        "negative-git-commit-missing",
        "negative-theorem-names-missing",
        "negative-toolchain-pin-missing",
        "negative-source-packet-link-missing",
        "negative-axiom-check-promoted",
        "negative-natural-law-promoted",
    }
    require(required_negative_ids == {item.get("fixture_id") for item in negatives}, errors, "negative id set mismatch")

    market = data.get("market_implication", {})
    require(market.get("uniqueness_status") == "hypothesis", errors, "uniqueness treated as fact")
    require(data.get("current_promoted_natural_laws") == [], errors, "natural law promoted")
    require("does not run Lean" in data.get("non_promotion_statement", ""), errors, "missing Lean non-promotion boundary")

    result = {
        "schema": "Pass0030TheoremReplayPreflightValidatorRun/v1",
        "pass": "0030",
        "status": "MATCH" if not errors else "DRIFT",
        "match": 1 if not errors else 0,
        "drift": 0 if not errors else 1,
        "checks": [
            {
                "artifact": "TheoremReplayPreflightPacket",
                "path": str(SCHEMA_PATH.relative_to(ROOT)),
                "status": "MATCH" if not errors else "DRIFT",
                "repo_commit": repo.get("commit"),
                "formalization_project_count": repo.get("formalization_project_count"),
                "lean_file_count": repo.get("lean_file_count"),
                "selected_theorem_count": len(theorem_names),
                "line_ending_drift_detected": line.get("eol_drift"),
                "pin_matches_git_blob_bytes": pins.get("pin_matches_git_blob_bytes"),
                "pin_matches_windows_worktree_bytes": pins.get("pin_matches_windows_worktree_bytes"),
                "lean_replay_status": toolchain.get("lean_replay_status"),
                "missing_commands": [name for name in ("bash", "lake", "lean") if toolchain.get(name) == "UNAVAILABLE"],
                "negative_fixture_count": len(negatives),
                "errors": errors,
            }
        ],
    }
    write_json(RESULT_PATH, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
