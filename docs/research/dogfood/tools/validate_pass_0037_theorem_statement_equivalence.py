"""Validate pass 0037 theorem statement-signature equivalence receipts."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "theorem-statement-equivalence-pass-0037.json"
FIXTURE_PATH = ROOT / "fixtures" / "theorem-statement-equivalence-pass-0037.json"
SOURCE_REF_PACKET = ROOT / "schemas" / "theorem-source-ref-integrity-pass-0036.json"
RESULT_PATH = ROOT / "schemas" / "pass-0037-theorem-statement-equivalence-validator-result.json"


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


def source_root() -> Path:
    configured = os.environ.get("PIPELINE_MATH_SOURCE_ROOT")
    if configured:
        return Path(configured)
    return Path(os.environ.get("TEMP", "")) / "pipeline-math-pass0032-lf"


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def main() -> None:
    errors: list[str] = []
    contract = load_json(SCHEMA_PATH)
    fixture = load_json(FIXTURE_PATH)
    source_ref_packet = load_json(SOURCE_REF_PACKET)
    repo = source_root()

    require(isinstance(contract, dict), errors, "contract not object")
    require(isinstance(fixture, dict), errors, "fixture not object")
    if isinstance(contract, dict):
        require(contract.get("schema") == "TheoremStatementEquivalenceSet/v1", errors, "schema mismatch")
        require(contract.get("status") == "STATEMENT_EQUIVALENCE_MATCH", errors, "status mismatch")
        require(check_seal(contract), errors, "contract seal mismatch")
        require(contract.get("source_ref_integrity_binding", {}).get("sha256") == sha256_file(SOURCE_REF_PACKET), errors, "source ref packet sha mismatch")
        require(contract.get("source_ref_integrity_binding", {}).get("seal") == source_ref_packet.get("seal"), errors, "source ref packet seal mismatch")
        require(contract.get("statement_equivalence_fixture", {}).get("sha256") == sha256_file(FIXTURE_PATH), errors, "fixture sha mismatch")
        require(contract.get("statement_equivalence_fixture", {}).get("seal") == fixture.get("seal"), errors, "fixture seal reference mismatch")

        rows = contract.get("statement_checks", [])
        measurements = contract.get("verifier_measurements", {})
        require(repo.exists(), errors, f"source repo missing: {repo}")
        require(len(rows) == 10, errors, "statement check count mismatch")
        require(measurements.get("theorem_count") == 10, errors, "measurement theorem count mismatch")
        require(measurements.get("statement_check_count") == 10, errors, "measurement statement count mismatch")
        require(measurements.get("all_statement_checks_match") is True, errors, "all_statement_checks_match false")
        require(measurements.get("all_frozen_solution_match") is True, errors, "all_frozen_solution_match false")
        require(measurements.get("all_frozen_proof_match") is True, errors, "all_frozen_proof_match false")
        require(measurements.get("all_discharge_gates_match") is True, errors, "all_discharge_gates_match false")

        for row in rows:
            theorem = row.get("theorem")
            require(row.get("status") == "MATCH", errors, f"{theorem} status drift")
            require(row.get("frozen_solution_status") == "MATCH", errors, f"{theorem} frozen solution drift")
            require(row.get("frozen_proof_status") == "MATCH", errors, f"{theorem} frozen proof drift")
            require(row.get("discharge_gate_status") == "MATCH", errors, f"{theorem} discharge gate drift")
            for key in ("frozen_signature", "solution_signature", "proof_signature"):
                sig = row.get(key, {})
                require(bool(sig.get("signature_text")), errors, f"{theorem} {key} text missing")
                require(bool(sig.get("canonical_signature")), errors, f"{theorem} {key} canonical missing")
                require(bool(sig.get("signature_sha256")), errors, f"{theorem} {key} sha missing")
                require(bool(sig.get("signature_span")), errors, f"{theorem} {key} span missing")
            require(row.get("frozen_signature", {}).get("canonical_signature") == row.get("solution_signature", {}).get("canonical_signature"), errors, f"{theorem} frozen/solution canonical mismatch")
            require(row.get("frozen_signature", {}).get("canonical_signature") == row.get("proof_signature", {}).get("canonical_signature"), errors, f"{theorem} frozen/proof canonical mismatch")

        negatives = contract.get("negative_fixtures", [])
        require(len(negatives) == 8, errors, "negative fixture count mismatch")
        for row in negatives:
            require(row.get("expected_validator_status") == "REJECT", errors, f"negative {row.get('id')} not REJECT")
        require(contract.get("current_promoted_natural_laws") == [], errors, "natural law promoted")

    if isinstance(fixture, dict):
        require(fixture.get("schema") == "TheoremStatementEquivalenceFixture/v1", errors, "fixture schema mismatch")
        require(check_seal(fixture), errors, "fixture seal mismatch")

    result = {
        "checks": [
            {
                "artifact": "TheoremStatementEquivalenceSet",
                "errors": errors,
                "path": str(SCHEMA_PATH.relative_to(ROOT)),
                "statement_check_count": contract.get("verifier_measurements", {}).get("statement_check_count") if isinstance(contract, dict) else None,
                "status": "MATCH" if not errors else "DRIFT",
                "theorem_count": contract.get("verifier_measurements", {}).get("theorem_count") if isinstance(contract, dict) else None,
            }
        ],
        "drift": 1 if errors else 0,
        "match": 0 if errors else 1,
        "pass": "0037",
        "schema": "Pass0037TheoremStatementEquivalenceValidatorRun/v1",
        "status": "MATCH" if not errors else "DRIFT"
    }
    write_json(RESULT_PATH, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
