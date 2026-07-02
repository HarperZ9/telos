"""Generate pass 0030 theorem replay preflight packet receipts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


PASS = "0030"
ROOT = Path(__file__).resolve().parents[1]
SOURCE_PACKET_PATH = ROOT / "schemas" / "research-claim-packet-pass-0029.json"
FIXTURE_PATH = ROOT / "fixtures" / "pipeline-math-problem4b-preflight-pass-0030.json"
OUT_PATH = ROOT / "schemas" / "theorem-replay-preflight-pass-0030.json"


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


source_packet = read_json(SOURCE_PACKET_PATH)

theorem_names = [
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

preflight_fixture = {
    "schema": "PipelineMathProblem4bPreflightFixture/v1",
    "source_repo": {
        "url": "https://github.com/Pengbinghui/pipeline-math.git",
        "commit": "69d7df765a8f377a5e0628c6d36c088bce7642c9",
        "clone_method": "git clone --depth 1",
        "observed_on": "2026-07-01",
        "temp_ref": "temp:pipeline-math-pass0030",
        "lean_file_count": 66,
        "formalization_project_count": 4,
        "formalization_projects": [
            "lean/problem-20-formalization",
            "lean/problem-27b-form",
            "lean/problem-30c-formalization",
            "lean/problem-4b-formalization",
        ],
    },
    "selected_project": {
        "path": "lean/problem-4b-formalization",
        "reason": "Problem 4(b) includes a verification harness, frozen SHA pins, and ten named solution theorems.",
        "lean_toolchain": "leanprover/lean4:v4.31.0",
        "theorem_count": len(theorem_names),
        "theorem_names": theorem_names,
    },
    "source_hashes": {
        "lean_toolchain_sha256": "465c68148dd061230368e3cbe5d1d2973069172b48b684c928ef1a665b627832",
        "lakefile_toml_sha256": "00fef5f7a14febfb4b9e1a3473ac00f16d45b039309ed4bb5a92b13263751f5f",
        "verify_sh_sha256": "fdb7f355ae2bbc0059b29fb5c2d9a834f433da22fa4e52ee704d2f5f148f39a7",
        "frozen_sha256_file_sha256": "64eabbdb5e601149590d2bda5c1957c585d53ba2f0dd5679253af55913f10bce",
        "root_prob4b_sha256": "b549dda1f16b3bf7ce569ef5f729f4d7bf12d755cbe178056d2077bd728d9753",
        "solution_worktree_sha256": "66f6fd1422de69a4c74aab403f3c0e5585c7ae1325fc0b8af61b5260b28467b6",
        "theorems_worktree_sha256": "70356618935d908762980a8dc0aead297f8d02a1ebdb997b5caaa1bfdfaa1b2e",
    },
    "frozen_pin_check": {
        "pin_file": "lean/problem-4b-formalization/scripts/frozen.sha256",
        "pinned_git_blob_hashes": {
            "Prob4b/Defs.lean": "f596023b79726b87da05ccaf825e512bd17237f29a43df3ce31dc01c7646868a",
            "Prob4b/Theorems.lean": "cb80242d1bfd9e9b142e442dac9d0784081dabefbf7bd400dd0a27cd0e8bd3ae",
        },
        "git_blob_hashes": {
            "Prob4b/Defs.lean": "f596023b79726b87da05ccaf825e512bd17237f29a43df3ce31dc01c7646868a",
            "Prob4b/Theorems.lean": "cb80242d1bfd9e9b142e442dac9d0784081dabefbf7bd400dd0a27cd0e8bd3ae",
        },
        "working_tree_hashes": {
            "Prob4b/Defs.lean": "4d3285bae57a53a42c33311745f5afdf6990d483cf0d1a0ffd796101a8051b2d",
            "Prob4b/Theorems.lean": "70356618935d908762980a8dc0aead297f8d02a1ebdb997b5caaa1bfdfaa1b2e",
        },
        "line_ending_probe": {
            "git_index": "lf",
            "working_tree": "crlf",
            "eol_drift": True,
            "replay_requirement": "Use Git blob bytes, enforce LF checkout, or normalize before frozen SHA validation.",
        },
        "pin_matches_git_blob_bytes": True,
        "pin_matches_windows_worktree_bytes": False,
    },
    "toolchain_probe": {
        "git": "MATCH",
        "python": "MATCH",
        "bash": "UNAVAILABLE",
        "lake": "UNAVAILABLE",
        "lean": "UNAVAILABLE",
        "verify_script_attempt_status": "UNVERIFIABLE_TOOL_UNAVAILABLE",
        "verify_script_missing_command": "bash",
        "lean_replay_status": "UNVERIFIABLE_TOOL_UNAVAILABLE",
        "replay_promotion_allowed": False,
    },
    "non_claims": [
        "This preflight does not prove any Problem 4(b) theorem.",
        "This preflight does not run Lake or Lean.",
        "This preflight does not verify theorem axiom output.",
        "This preflight does not promote pipeline-math proof correctness.",
    ],
}
preflight_fixture["seal"] = sha256_obj({key: value for key, value in preflight_fixture.items() if key != "seal"})
write_json(FIXTURE_PATH, preflight_fixture)

fixture_sha = sha256_file(FIXTURE_PATH)
source_packet_sha = sha256_file(SOURCE_PACKET_PATH)

negative_fixtures = [
    {
        "fixture_id": "negative-lean-replay-promoted-without-lean",
        "failure_mode": "The packet claims Lean replay success even though lean is unavailable.",
        "expected_validator_status": "REJECT",
    },
    {
        "fixture_id": "negative-lake-build-promoted-without-lake",
        "failure_mode": "The packet claims Lake build success even though lake is unavailable.",
        "expected_validator_status": "REJECT",
    },
    {
        "fixture_id": "negative-verify-script-promoted-without-bash",
        "failure_mode": "The packet claims verify.sh success even though bash is unavailable.",
        "expected_validator_status": "REJECT",
    },
    {
        "fixture_id": "negative-frozen-pin-worktree-mismatch-ignored",
        "failure_mode": "The packet ignores CRLF working-tree hash drift when checking frozen SHA pins.",
        "expected_validator_status": "REJECT",
    },
    {
        "fixture_id": "negative-git-commit-missing",
        "failure_mode": "The source repository commit is missing from the replay receipt.",
        "expected_validator_status": "REJECT",
    },
    {
        "fixture_id": "negative-theorem-names-missing",
        "failure_mode": "The selected theorem names are missing or not counted.",
        "expected_validator_status": "REJECT",
    },
    {
        "fixture_id": "negative-toolchain-pin-missing",
        "failure_mode": "The Lean toolchain pin is missing.",
        "expected_validator_status": "REJECT",
    },
    {
        "fixture_id": "negative-source-packet-link-missing",
        "failure_mode": "The pass 0030 packet is not linked back to pass 0029.",
        "expected_validator_status": "REJECT",
    },
    {
        "fixture_id": "negative-axiom-check-promoted",
        "failure_mode": "The packet claims #print axioms success without running Lean.",
        "expected_validator_status": "REJECT",
    },
    {
        "fixture_id": "negative-natural-law-promoted",
        "failure_mode": "The packet promotes a theorem replay preflight into a natural-law or solved-theorem claim.",
        "expected_validator_status": "REJECT",
    },
]

record = {
    "schema": "TheoremReplayPreflightPacket/v1",
    "pass": PASS,
    "generated_on": "2026-07-01",
    "status": "THEOREM_REPLAY_PREFLIGHT_MATCH_WITH_TOOLCHAIN_GAP",
    "packet_title": "Pipeline-math Problem 4(b) Lean Replay Preflight",
    "source_packet_binding": {
        "path": "schemas/research-claim-packet-pass-0029.json",
        "sha256": source_packet_sha,
        "seal": source_packet["seal"],
        "schema": source_packet["schema"],
    },
    "preflight_fixture": {
        "path": "fixtures/pipeline-math-problem4b-preflight-pass-0030.json",
        "sha256": fixture_sha,
        "seal": preflight_fixture["seal"],
        "schema": preflight_fixture["schema"],
    },
    "repo_receipt": preflight_fixture["source_repo"],
    "selected_project": preflight_fixture["selected_project"],
    "frozen_pin_receipt": preflight_fixture["frozen_pin_check"],
    "toolchain_receipt": preflight_fixture["toolchain_probe"],
    "action_receipt_proposal": {
        "schema": "ActionReceiptTheoremReplayPreflight/v1",
        "action_id": "act_dogfood_0030_theorem_replay_preflight",
        "event_id": "evt_dogfood_0030_theorem_replay_preflight",
        "event_type": "theorem_replay_preflight_created",
        "authority_class": "read_only_public_repo_preflight",
        "input_refs": [
            "artifact:schemas/research-claim-packet-pass-0029.json",
            "artifact:fixtures/pipeline-math-problem4b-preflight-pass-0030.json",
        ],
        "input_digests": [
            f"sha256:{source_packet_sha}",
            f"sha256:{fixture_sha}",
        ],
        "output_ref": "artifact:schemas/theorem-replay-preflight-pass-0030.json",
        "external_write_performed": False,
        "toolchain_install_performed": False,
        "replay_promotion_allowed": False,
        "verification": {
            "verdict": "MATCH",
            "ref": "validator:pass-0030-theorem-replay-preflight",
        },
    },
    "verifier_measurements": {
        "schema": "TheoremReplayPreflightMeasurements/v1",
        "formalization_project_count": 4,
        "lean_file_count": 66,
        "selected_theorem_count": len(theorem_names),
        "required_commands_available": {
            "git": True,
            "python": True,
            "bash": False,
            "lake": False,
            "lean": False,
        },
        "pin_matches_git_blob_bytes": True,
        "pin_matches_windows_worktree_bytes": False,
        "line_ending_drift_detected": True,
        "lean_replay_status": "UNVERIFIABLE_TOOL_UNAVAILABLE",
        "replay_success_promoted": False,
        "measurement_status": "MATCH",
    },
    "negative_fixtures": negative_fixtures,
    "negative_fixture_count": len(negative_fixtures),
    "market_implication": {
        "wedge_hypothesis": "Research proof packets need theorem-level replay preflights that separate source availability, environment readiness, line-ending/hash integrity, and proof replay success.",
        "uniqueness_status": "hypothesis",
        "buyer_relevance": [
            "Math and AI4Science labs need proof artifacts that distinguish source claims from replayed formal verification.",
            "Agent-ops teams need tooling that blocks proof-success promotion when toolchains are absent.",
            "BuildLang/buildc can reuse the same preflight contract for compiler/runtime proof receipts before claiming numerical or formal correctness.",
        ],
    },
    "next_replay_requirements": [
        "Install or provision bash, elan, lake, and Lean v4.31.0 in an isolated environment.",
        "Clone with LF-preserving checkout or hash Git blob bytes for frozen pin checks.",
        "Run scripts/verify.sh --no-log --all from lean/problem-4b-formalization.",
        "Capture lake build output, #print axioms output, statement-gate output, and exit code.",
        "Bind completed replay logs through action receipts and Crucible measurements.",
    ],
    "non_promotion_statement": "Pass 0030 verifies a theorem replay preflight only. It does not run Lean, does not run Lake, does not prove any Problem 4(b) theorem, does not prove pipeline-math proof correctness, and does not promote any natural law.",
    "current_promoted_natural_laws": [],
}
record["seal"] = sha256_obj({key: value for key, value in record.items() if key != "seal"})
write_json(OUT_PATH, record)

print(
    json.dumps(
        {
            "path": str(OUT_PATH),
            "schema": record["schema"],
            "status": record["status"],
            "repo_commit": record["repo_receipt"]["commit"],
            "formalization_project_count": record["verifier_measurements"]["formalization_project_count"],
            "lean_file_count": record["verifier_measurements"]["lean_file_count"],
            "selected_theorem_count": record["verifier_measurements"]["selected_theorem_count"],
            "lean_replay_status": record["verifier_measurements"]["lean_replay_status"],
            "line_ending_drift_detected": record["verifier_measurements"]["line_ending_drift_detected"],
            "negative_fixture_count": record["negative_fixture_count"],
            "seal": record["seal"],
        },
        indent=2,
        sort_keys=True,
    )
)
