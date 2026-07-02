"""Validate pass 0035 theorem-specific proof packet receipts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "theorem-specific-proof-packets-pass-0035.json"
FIXTURE_PATH = ROOT / "fixtures" / "theorem-specific-proof-packets-pass-0035.json"
SOURCE_PATH = ROOT / "schemas" / "lean-replay-verification-pass-0034.json"
RESULT_PATH = ROOT / "schemas" / "pass-0035-theorem-packets-validator-result.json"


EXPECTED_THEOREMS = [
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
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def check_seal(value: dict) -> bool:
    copy = dict(value)
    seal = copy.pop("seal", None)
    return seal == sha256_obj(copy)


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def main() -> None:
    errors: list[str] = []
    contract = load_json(SCHEMA_PATH)
    fixture = load_json(FIXTURE_PATH)
    source = load_json(SOURCE_PATH)

    require(isinstance(contract, dict), errors, "contract not object")
    require(isinstance(fixture, dict), errors, "fixture not object")

    rows = contract.get("theorems", []) if isinstance(contract, dict) else []
    if isinstance(contract, dict):
        require(contract.get("schema") == "TheoremSpecificProofPacketSet/v1", errors, "schema mismatch")
        require(contract.get("status") == "THEOREM_SPECIFIC_REPLAY_MATCH", errors, "status mismatch")
        require(check_seal(contract), errors, "contract seal mismatch")
        require(contract.get("source_replay_binding", {}).get("sha256") == sha256_file(SOURCE_PATH), errors, "source sha mismatch")
        require(contract.get("source_replay_binding", {}).get("seal") == source.get("seal"), errors, "source seal mismatch")
        require([row.get("theorem") for row in rows] == EXPECTED_THEOREMS, errors, "theorem ordering/count mismatch")
        require(contract.get("verifier_measurements", {}).get("all_exit_zero") is True, errors, "all_exit_zero mismatch")
        require(contract.get("verifier_measurements", {}).get("all_result_pass") is True, errors, "all_result_pass mismatch")
        require(contract.get("verifier_measurements", {}).get("theorem_count") == 10, errors, "measurement theorem count mismatch")
        require(contract.get("verifier_measurements", {}).get("packet_count") == 10, errors, "packet count mismatch")
        require(contract.get("verifier_measurements", {}).get("transcript_count") == 10, errors, "transcript count mismatch")

        for row in rows:
            theorem = row.get("theorem")
            require(row.get("exit_code") == 0, errors, f"{theorem} exit not zero")
            require(row.get("result_pass") is True, errors, f"{theorem} result not PASS")
            require(row.get("axiom_set") == ["propext", "Classical.choice", "Quot.sound"], errors, f"{theorem} axiom set mismatch")
            require(row.get("statement_discharge_status") == "PASS", errors, f"{theorem} discharge gate mismatch")
            require(row.get("statement_solution_status") == "PASS", errors, f"{theorem} solution gate mismatch")
            require(row.get("lake_build_status") == "PASS", errors, f"{theorem} lake build mismatch")
            require(row.get("banned_keywords_status") == "PASS", errors, f"{theorem} banned keyword mismatch")
            require(row.get("frozen_sha_pins_status") == "PASS", errors, f"{theorem} frozen pin mismatch")
            for key in ("frozen_statement", "solution_decl", "discharge_gate", "proof_decl"):
                require(bool(row.get("source_refs", {}).get(key)), errors, f"{theorem} missing {key}")
            packet_path = ROOT / row.get("packet_path", "")
            transcript_path = ROOT / row.get("transcript_ref", "")
            require(packet_path.exists(), errors, f"{theorem} packet missing")
            require(transcript_path.exists(), errors, f"{theorem} transcript missing")
            if transcript_path.exists():
                require(sha256_file(transcript_path) == row.get("transcript_sha256"), errors, f"{theorem} transcript sha mismatch")
                text = transcript_path.read_text(encoding="utf-8")
                require("=== RESULT: PASS" in text, errors, f"{theorem} transcript lacks PASS")
                require(f"Target: {theorem}" in text, errors, f"{theorem} transcript target mismatch")

        fixture_ref = contract.get("theorem_fixture", {})
        require(fixture_ref.get("sha256") == sha256_file(FIXTURE_PATH), errors, "fixture sha mismatch")
        require(fixture_ref.get("seal") == fixture.get("seal"), errors, "fixture seal reference mismatch")

        negatives = contract.get("negative_fixtures", [])
        require(len(negatives) == 10, errors, "negative fixture count mismatch")
        for row in negatives:
            require(row.get("expected_validator_status") == "REJECT", errors, f"negative {row.get('id')} not REJECT")
        require(contract.get("current_promoted_natural_laws") == [], errors, "natural law promoted")

    if isinstance(fixture, dict):
        require(fixture.get("schema") == "TheoremSpecificProofPacketFixture/v1", errors, "fixture schema mismatch")
        require(check_seal(fixture), errors, "fixture seal mismatch")
        require(fixture.get("theorem_count") == 10, errors, "fixture theorem count mismatch")

    result = {
        "checks": [
            {
                "artifact": "TheoremSpecificProofPacketSet",
                "errors": errors,
                "packet_count": contract.get("verifier_measurements", {}).get("packet_count") if isinstance(contract, dict) else None,
                "path": str(SCHEMA_PATH.relative_to(ROOT)),
                "status": "MATCH" if not errors else "DRIFT",
                "theorem_count": len(rows),
                "transcript_count": contract.get("verifier_measurements", {}).get("transcript_count") if isinstance(contract, dict) else None
            }
        ],
        "drift": 1 if errors else 0,
        "match": 0 if errors else 1,
        "pass": "0035",
        "schema": "Pass0035TheoremPacketValidatorRun/v1",
        "status": "MATCH" if not errors else "DRIFT"
    }
    write_json(RESULT_PATH, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
