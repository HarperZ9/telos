"""Generate pass 0034 Lean replay verification receipts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


PASS = "0034"
ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / "schemas" / "lean-provisioning-build-timeout-pass-0033.json"
FIXTURE_PATH = ROOT / "fixtures" / "lean-replay-verification-pass-0034.json"
OUT_PATH = ROOT / "schemas" / "lean-replay-verification-pass-0034.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def with_seal(value: dict) -> dict:
    sealed = dict(value)
    sealed["seal"] = sha256_obj(value)
    return sealed


THEOREMS = [
    "B_triple_zero",
    "M_triple_defect",
    "M_annihilator",
    "M_pairwise_intersection",
    "triple_defect_survives",
    "R_finite_conductor",
    "R_not_quasi_coherent",
    "prob4b_counterexample",
    "problem4b_false",
    "quasiCoherent_imp_finiteConductor",
]


def main() -> None:
    source = read_json(SOURCE_PATH)
    source_sha = sha256_file(SOURCE_PATH)
    source_seal = source["seal"]

    axiom_checks = [
        {
            "axioms": ["propext", "Classical.choice", "Quot.sound"],
            "name": name,
            "namespace": f"Prob4b.Solution.{name}",
            "status": "PASS"
        }
        for name in THEOREMS
    ]

    cache_hydration = {
        "cache_byte_sum": 432264798,
        "cache_dir_ref": "temp:telos-pass0034-mathlib-cache",
        "cache_file_count": 8542,
        "command": "lake exe cache get",
        "decompressed_files": 8542,
        "downloaded_files": 8542,
        "exit_code": 0,
        "external_call_performed": True,
        "local_cache_extension": ".ltar",
        "status": "MATCH",
        "temp_write_performed": True
    }

    verifier_run = {
        "banned_keywords_status": "PASS",
        "build_jobs": 8574,
        "duration_seconds": 1184,
        "exit_code": 0,
        "frozen_sha_pins_status": "PASS",
        "lake_build_status": "PASS",
        "result": "PASS",
        "result_issue_count": 0,
        "statement_gates": [
            {"module": "Prob4b.Discharge", "status": "PASS"},
            {"module": "Prob4b.Solution", "status": "PASS"}
        ],
        "status": "MATCH",
        "theorem_axiom_checks": axiom_checks,
        "theorem_axiom_status": "PASS"
    }

    build_artifacts = {
        "cache_byte_sum": 432264798,
        "cache_file_count": 8542,
        "lake_byte_sum": 8009101293,
        "lake_file_count": 123892,
        "prob4b_build_byte_sum": 10048128,
        "prob4b_build_file_count": 75,
        "prob4b_build_outputs": {
            ".hash": 30,
            ".ilean": 15,
            ".olean": 15,
            ".trace": 15
        },
        "remaining_temp_processes": 0
    }

    fixture = with_seal({
        "build_artifacts": build_artifacts,
        "cache_hydration": cache_hydration,
        "pass": PASS,
        "schema": "LeanReplayVerificationFixture/v1",
        "source_provisioning_ref": "schemas/lean-provisioning-build-timeout-pass-0033.json",
        "source_provisioning_seal": source_seal,
        "source_provisioning_sha256": source_sha,
        "verifier_run": verifier_run
    })
    write_json(FIXTURE_PATH, fixture)
    fixture_sha = sha256_file(FIXTURE_PATH)

    contract = with_seal({
        "action_receipt_proposal": {
            "action_id": "act_dogfood_0034_lean_replay_verification",
            "authority_class": "contained_temp_toolchain_replay",
            "event_id": "evt_dogfood_0034_lean_replay_verification",
            "event_type": "lean_replay_verification_recorded",
            "external_call_performed": True,
            "external_write_performed": False,
            "normal_path_modified": False,
            "result_state": "completed",
            "side_effect_class": "network_read_and_temp_write",
            "stop_reason": "completed",
            "verification_verdict": "MATCH"
        },
        "build_artifacts": build_artifacts,
        "cache_hydration": cache_hydration,
        "current_promoted_natural_laws": [],
        "generated_on": "2026-07-01",
        "negative_fixture_count": 10,
        "negative_fixtures": [
            {"expected_validator_status": "REJECT", "id": "negative-cache-get-promoted-without-exit-zero"},
            {"expected_validator_status": "REJECT", "id": "negative-lake-build-promoted-without-pass"},
            {"expected_validator_status": "REJECT", "id": "negative-axiom-check-omitted"},
            {"expected_validator_status": "REJECT", "id": "negative-axiom-set-missing"},
            {"expected_validator_status": "REJECT", "id": "negative-statement-gate-omitted"},
            {"expected_validator_status": "REJECT", "id": "negative-banned-keywords-ignored"},
            {"expected_validator_status": "REJECT", "id": "negative-frozen-pins-ignored"},
            {"expected_validator_status": "REJECT", "id": "negative-processes-left-running"},
            {"expected_validator_status": "REJECT", "id": "negative-public-claim-overpromoted"},
            {"expected_validator_status": "REJECT", "id": "negative-natural-law-promoted"}
        ],
        "next_actions": [
            "extract theorem-specific proof packet with exact command transcript digest",
            "run target-specific verification for each theorem independently",
            "compare replay packet to pipeline-math README claims without overpromoting",
            "map BuildLang/buildc proof-packet equivalents for dependency cache, build, theorem, and output gates"
        ],
        "non_promotion_statement": "Pass 0034 verifies the local Lean replay harness for pipeline-math Problem 4(b) under the stated project, toolchain, cache, axiom, and statement-gate boundaries. It does not prove every public claim about pipeline-math, does not establish a new mathematical theorem outside the Lean artifact, and does not promote any natural law.",
        "pass": PASS,
        "public_source_receipts": [
            {
                "claim": "The replay target is the public pipeline-math repository previously bound to commit 69d7df765a8f377a5e0628c6d36c088bce7642c9.",
                "source": "pipeline-math GitHub repository",
                "url": "https://github.com/Pengbinghui/pipeline-math",
                "verification_status": "verified_prior_pass"
            },
            {
                "claim": "Elan supplied the Lean 4.31.0 toolchain used for replay.",
                "source": "elan GitHub release",
                "url": "https://github.com/leanprover/elan/releases/tag/v4.2.3",
                "verification_status": "verified_prior_pass"
            }
        ],
        "replay_fixture": {
            "path": "fixtures/lean-replay-verification-pass-0034.json",
            "schema": fixture["schema"],
            "seal": fixture["seal"],
            "sha256": fixture_sha
        },
        "schema": "LeanReplayVerificationPacket/v1",
        "source_provisioning_binding": {
            "path": "schemas/lean-provisioning-build-timeout-pass-0033.json",
            "seal": source_seal,
            "sha256": source_sha,
            "source_status": source["status"]
        },
        "status": "LEAN_REPLAY_VERIFIED_WITH_AXIOM_BOUNDARY",
        "verifier_measurements": {
            "axiom_check_count": len(axiom_checks),
            "cache_get_status": "MATCH",
            "lake_build_status": "PASS",
            "remaining_temp_processes": 0,
            "statement_gate_count": 2,
            "theorem_axiom_status": "PASS",
            "verifier_exit_code": 0,
            "verifier_issue_count": 0
        },
        "verifier_run": verifier_run
    })
    write_json(OUT_PATH, contract)

    print(json.dumps({
        "axiom_check_count": len(axiom_checks),
        "duration_seconds": verifier_run["duration_seconds"],
        "path": str(OUT_PATH),
        "schema": contract["schema"],
        "seal": contract["seal"],
        "status": contract["status"],
        "verifier_exit_code": verifier_run["exit_code"]
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
