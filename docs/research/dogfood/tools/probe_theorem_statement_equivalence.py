"""Generate pass 0037 theorem statement-signature equivalence receipts."""

from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path


PASS = "0037"
PROJECT_SUBDIR = "lean/problem-4b-formalization"
ROOT = Path(__file__).resolve().parents[1]
SOURCE_REF_PACKET = ROOT / "schemas" / "theorem-source-ref-integrity-pass-0036.json"
FIXTURE_PATH = ROOT / "fixtures" / "theorem-statement-equivalence-pass-0037.json"
OUT_PATH = ROOT / "schemas" / "theorem-statement-equivalence-pass-0037.json"
PACKET_PATH = ROOT / "packets" / "047-theorem-statement-equivalence.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0037-statement-equivalence-steelman.md"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def read_json(path: Path) -> object:
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


def extract_signature(repo: Path, git_path: str, line_no: int) -> dict:
    path = repo / git_path
    lines = path.read_text(encoding="utf-8").splitlines()
    parts: list[str] = []
    end_line = line_no
    for idx in range(line_no - 1, len(lines)):
        line = lines[idx].rstrip()
        end_line = idx + 1
        if ":=" in line:
            before = line.split(":=", 1)[0].rstrip()
            if before:
                parts.append(before)
            break
        parts.append(line)
    signature_text = "\n".join(parts).strip()
    return {
        "canonical_signature": canonical_signature(signature_text),
        "signature_sha256": sha256_text(signature_text),
        "signature_span": [line_no, end_line],
        "signature_text": signature_text,
    }


def canonical_signature(signature_text: str) -> str:
    one_line = re.sub(r"\s+", " ", signature_text).strip()
    match = re.match(r"^(theorem|lemma)\s+\S+\s*(.*)$", one_line)
    if match:
        return match.group(2).strip()
    return one_line


def check_discharge(line_text: str, theorem: str) -> bool:
    stripped = re.sub(r"\s+", " ", line_text).strip()
    return f"@{theorem} = @{theorem}_proof" in stripped and stripped.endswith(":= rfl")


def row_map(source_ref_packet: dict) -> dict[tuple[str, str], dict]:
    return {
        (row["theorem"], row["ref_kind"]): row
        for row in source_ref_packet["source_ref_checks"]
    }


def build_checks(repo: Path, source_ref_packet: dict) -> list[dict]:
    rows = row_map(source_ref_packet)
    theorem_names = []
    for row in source_ref_packet["source_ref_checks"]:
        theorem = row["theorem"]
        if theorem not in theorem_names:
            theorem_names.append(theorem)

    checks = []
    for theorem in theorem_names:
        frozen_ref = rows[(theorem, "frozen_statement")]
        solution_ref = rows[(theorem, "solution_decl")]
        proof_ref = rows[(theorem, "proof_decl")]
        discharge_ref = rows[(theorem, "discharge_gate")]
        frozen_sig = extract_signature(repo, frozen_ref["git_path"], frozen_ref["line_no"])
        solution_sig = extract_signature(repo, solution_ref["git_path"], solution_ref["line_no"])
        proof_sig = extract_signature(repo, proof_ref["git_path"], proof_ref["line_no"])
        discharge_ok = check_discharge(discharge_ref["line_text"], theorem)
        frozen_solution_match = frozen_sig["canonical_signature"] == solution_sig["canonical_signature"]
        frozen_proof_match = frozen_sig["canonical_signature"] == proof_sig["canonical_signature"]
        checks.append({
            "discharge_gate_ref": discharge_ref["ref"],
            "discharge_gate_status": "MATCH" if discharge_ok else "DRIFT",
            "frozen_proof_status": "MATCH" if frozen_proof_match else "DRIFT",
            "frozen_ref": frozen_ref["ref"],
            "frozen_signature": frozen_sig,
            "frozen_solution_status": "MATCH" if frozen_solution_match else "DRIFT",
            "proof_ref": proof_ref["ref"],
            "proof_signature": proof_sig,
            "solution_ref": solution_ref["ref"],
            "solution_signature": solution_sig,
            "status": "MATCH" if frozen_solution_match and frozen_proof_match and discharge_ok else "DRIFT",
            "theorem": theorem,
        })
    return checks


def render_packet(contract: dict) -> str:
    table = "\n".join(
        f"| `{row['theorem']}` | `{row['frozen_solution_status']}` | `{row['frozen_proof_status']}` | `{row['discharge_gate_status']}` | `{row['status']}` |"
        for row in contract["statement_checks"]
    )
    return f"""# Packet 047: Theorem Statement Equivalence

Date: 2026-07-01

Status: `{contract['status']}`

Pass 0037 compares declaration signatures for each theorem across the frozen
statement, the solution restatement, and the proof theorem header, then checks
the discharge equality gate.

## Source Binding

```text
source = schemas/theorem-source-ref-integrity-pass-0036.json
source_sha256 = {contract['source_ref_integrity_binding']['sha256']}
source_seal = {contract['source_ref_integrity_binding']['seal']}
theorem_count = {contract['verifier_measurements']['theorem_count']}
statement_check_count = {contract['verifier_measurements']['statement_check_count']}
```

## Statement Checks

| Theorem | Frozen vs solution | Frozen vs proof | Discharge gate | Overall |
| --- | --- | --- | --- | --- |
{table}

## Product Reading

This is the next source-integrity layer after line refs: a proof packet should
show that the headline theorem, solution namespace theorem, and proof theorem
carry the same normalized declaration signature before trusting a replay as a
per-claim receipt.

## Non-Promotion Boundary

Pass 0037 checks declaration-signature equivalence and discharge gate shape. It
does not re-run Lean, prove semantic equivalence by elaboration, prove an
axiom-free result, validate every public `pipeline-math` claim, or promote any
natural law.

Current promoted natural laws: none.
"""


def render_steelman() -> str:
    return """# Pass 0037 Steelman: Statement Equivalence

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

## Thesis Under Pressure

Pass 0037 claims that frozen theorem declarations, solution declarations, proof
declaration headers, and discharge equality gates match at the normalized
source-signature level.

## Strongest Objections

1. This is still text normalization, not Lean elaboration.

Correct. It catches obvious drift between declarations but does not replace the
Lean kernel, theorem replay, or an AST/elaboration equivalence checker.

2. Whitespace normalization can hide formatting differences.

Correct. That is intentional for signature comparison, but the packet keeps raw
signature text hashes and spans for stricter review.

3. It only checks theorem declaration signatures, not proof bodies.

Correct. Proof-body review belongs to a later AST or elaboration pass.

4. The discharge gate is checked as source text.

Correct. It must still be compiled by the replay harness to become a theorem
kernel fact. This pass only verifies the gate source has the expected equality
shape.

## Verdict

Useful protection against statement drift. Not a substitute for compiled Lean
replay or semantic proof review.
"""


def main() -> None:
    repo = source_root()
    if not repo.exists():
        raise SystemExit(f"missing source checkout: {repo}")
    source_ref_packet = read_json(SOURCE_REF_PACKET)
    source_sha = sha256_file(SOURCE_REF_PACKET)
    checks = build_checks(repo, source_ref_packet)
    all_match = all(row["status"] == "MATCH" for row in checks)

    fixture = with_seal({
        "generated_on": "2026-07-01",
        "pass": PASS,
        "schema": "TheoremStatementEquivalenceFixture/v1",
        "source_ref_integrity_sha256": source_sha,
        "statement_checks": checks,
    })
    write_json(FIXTURE_PATH, fixture)
    fixture_sha = sha256_file(FIXTURE_PATH)

    contract = with_seal({
        "action_receipt_proposal": {
            "action_id": "act_dogfood_0037_statement_equivalence",
            "authority_class": "read_only_source_signature_verification",
            "event_id": "evt_dogfood_0037_statement_equivalence",
            "event_type": "theorem_statement_equivalence_verified",
            "external_call_performed": False,
            "external_write_performed": False,
            "normal_path_modified": False,
            "result_state": "completed",
            "side_effect_class": "local_read_and_repo_artifact_write",
            "stop_reason": "completed",
            "verification_verdict": "MATCH" if all_match else "DRIFT",
        },
        "current_promoted_natural_laws": [],
        "generated_on": "2026-07-01",
        "negative_fixture_count": 8,
        "negative_fixtures": [
            {"expected_validator_status": "REJECT", "id": "negative-frozen-solution-signature-drift"},
            {"expected_validator_status": "REJECT", "id": "negative-frozen-proof-signature-drift"},
            {"expected_validator_status": "REJECT", "id": "negative-discharge-gate-drift"},
            {"expected_validator_status": "REJECT", "id": "negative-signature-span-missing"},
            {"expected_validator_status": "REJECT", "id": "negative-signature-hash-missing"},
            {"expected_validator_status": "REJECT", "id": "negative-source-ref-binding-missing"},
            {"expected_validator_status": "REJECT", "id": "negative-public-claim-overpromoted"},
            {"expected_validator_status": "REJECT", "id": "negative-natural-law-promoted"}
        ],
        "non_promotion_statement": "Pass 0037 checks declaration-signature equivalence and discharge gate shape. It does not re-run Lean, prove semantic equivalence by elaboration, prove an axiom-free result, validate every public pipeline-math claim, or promote any natural law.",
        "pass": PASS,
        "schema": "TheoremStatementEquivalenceSet/v1",
        "source_ref_integrity_binding": {
            "path": "schemas/theorem-source-ref-integrity-pass-0036.json",
            "seal": source_ref_packet["seal"],
            "sha256": source_sha,
            "source_status": source_ref_packet["status"],
        },
        "statement_checks": checks,
        "statement_equivalence_fixture": {
            "path": "fixtures/theorem-statement-equivalence-pass-0037.json",
            "schema": fixture["schema"],
            "seal": fixture["seal"],
            "sha256": fixture_sha,
        },
        "status": "STATEMENT_EQUIVALENCE_MATCH" if all_match else "STATEMENT_EQUIVALENCE_DRIFT",
        "verifier_measurements": {
            "all_discharge_gates_match": all(row["discharge_gate_status"] == "MATCH" for row in checks),
            "all_frozen_proof_match": all(row["frozen_proof_status"] == "MATCH" for row in checks),
            "all_frozen_solution_match": all(row["frozen_solution_status"] == "MATCH" for row in checks),
            "all_statement_checks_match": all_match,
            "statement_check_count": len(checks),
            "theorem_count": len(checks),
        },
    })
    write_json(OUT_PATH, contract)
    write_text(PACKET_PATH, render_packet(contract))
    write_text(STEELMAN_PATH, render_steelman())

    print(json.dumps({
        "path": str(OUT_PATH),
        "schema": contract["schema"],
        "seal": contract["seal"],
        "statement_check_count": len(checks),
        "status": contract["status"],
        "theorem_count": len(checks),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
