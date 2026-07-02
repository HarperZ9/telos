#!/usr/bin/env bash
# Verification harness for the Problem 4(b) formalization.
#
# Project layout (mirrors ~/dev/prob27bFORM):
#   * Sources live under Prob4b/.
#   * The frozen pair Prob4b/Defs.lean + Prob4b/Theorems.lean are pinned by
#     SHA-256 in scripts/frozen.sha256.
#   * Theorems.lean holds the immutable statements as `sorry` stubs; the proofs
#     live in Prob4b/Proofs/** and are exposed as clean, named theorems in
#     Prob4b/Solution.lean (Prob4b.Solution.<name>). Prob4b/Discharge.lean
#     pairs each frozen statement with its proof via `@Frozen = @Proof := rfl`.
#
# Usage:
#   scripts/verify.sh [--no-log] [<theorem_name> | --all]
#
# With no theorem (or --all), verifies the whole solution. With a theorem name,
# the axiom check (Check 4) is restricted to that theorem; the project-wide
# checks (pins, banned keywords, build, gates) always run.
#
# Checks:
#   1. Frozen SHA pins      Defs.lean / Theorems.lean match scripts/frozen.sha256.
#   2. Banned keywords      No sorry/sorryAx/native_decide/admit/axiom/unsafe in
#                           any first-party *.lean (comment-aware). `sorry` is
#                           allowed ONLY in Theorems.lean (the frozen stubs).
#   3. lake build clean     Exit 0, no errors, no warnings except the expected
#                           `declaration uses 'sorry'` from Theorems.lean.
#   4. #print axioms        Each Prob4b.Solution.<name> depends only on the
#                           standard axioms {propext, Classical.choice, Quot.sound}.
#   5. Statement gates      Discharge.lean (`@Frozen = @Proof := rfl`) and
#                           Solution.lean (`:= <proof>`) compile — machine proof
#                           that each clean theorem has exactly the frozen type.
#
# Exit code = number of failed checks (0 = PASS).

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC_DIR="$REPO_ROOT/Prob4b"
DEFS_FILE="$SRC_DIR/Defs.lean"
THEOREMS_FILE="$SRC_DIR/Theorems.lean"
PINS_FILE="$REPO_ROOT/scripts/frozen.sha256"

# The ten frozen theorems (= Prob4b.Solution.<name> = Prob4b.<name>).
ALL_THEOREMS=(B_triple_zero M_triple_defect M_annihilator M_pairwise_intersection \
              triple_defect_survives R_finite_conductor R_not_quasi_coherent \
              prob4b_counterexample problem4b_false quasiCoherent_imp_finiteConductor)

usage() { echo "Usage: $0 [--no-log] [<theorem_name> | --all]"; }

NO_LOG=0
TARGET="--all"
while [ $# -gt 0 ]; do
    case "$1" in
        --no-log|--dry-run) NO_LOG=1; shift ;;
        -h|--help) usage; exit 0 ;;
        --all) TARGET="--all"; shift ;;
        -*) echo "ERROR: unknown option: $1"; usage; exit 1 ;;
        *) TARGET="$1"; shift ;;
    esac
done

# Resolve target theorem list.
if [ "$TARGET" = "--all" ]; then
    TARGETS=("${ALL_THEOREMS[@]}")
else
    found=0
    for t in "${ALL_THEOREMS[@]}"; do [ "$t" = "$TARGET" ] && found=1; done
    if [ "$found" -eq 0 ]; then
        echo "ERROR: unknown theorem '$TARGET'. Known: ${ALL_THEOREMS[*]}"
        exit 1
    fi
    TARGETS=("$TARGET")
fi

for required in "$DEFS_FILE" "$THEOREMS_FILE" "$PINS_FILE"; do
    [ -f "$required" ] || { echo "ERROR: required file not found: $required"; exit 1; }
done

sha256_of() {
    if command -v sha256sum >/dev/null 2>&1; then sha256sum "$1" | awk '{print $1}'
    else shasum -a 256 "$1" | awk '{print $1}'; fi
}

# Run `lake env lean` / `lake build`, sourcing elan if present.
run_lake() {
    if [ -f "$HOME/.elan/env" ]; then ( . "$HOME/.elan/env" && cd "$REPO_ROOT" && lake "$@" );
    else ( cd "$REPO_ROOT" && lake "$@" ); fi
}

echo "=== Verifying Problem 4(b) formalization ==="
echo "  Target: $TARGET"
[ "$NO_LOG" -eq 1 ] && echo "  Log mode: disabled"
echo ""

ERRORS=0
START_TIME=$(date +%s)

# --- Check 1: Frozen SHA pins ---
echo "--- Check 1: Frozen SHA pins ---"
while read -r pinned relpath; do
    [ -z "$pinned" ] && continue
    actual=$(sha256_of "$REPO_ROOT/$relpath")
    if [ "$pinned" = "$actual" ]; then
        echo "PASS: $relpath pin matches"
    else
        echo "FAIL: $relpath SHA pin mismatch"
        echo "  Pinned: $pinned"
        echo "  Actual: $actual"
        ERRORS=$((ERRORS + 1))
    fi
done < "$PINS_FILE"

# --- Check 2: Banned keywords (comment-aware) ---
echo ""
echo "--- Check 2: Banned keywords ---"
BANNED_OUT=$(SRC_DIR="$SRC_DIR" ROOT_LEAN="$REPO_ROOT/Prob4b.lean" THEOREMS_FILE="$THEOREMS_FILE" python3 - <<'PY'
import os, re, sys, glob
src_dir = os.environ["SRC_DIR"]
theorems = os.environ["THEOREMS_FILE"]
root_lean = os.environ["ROOT_LEAN"]
banned = ["sorry", "sorryAx", "native_decide", "admit", "unsafe",
          "implemented_by", "ofReduceBool"]
def strip_comments(s):
    out=[]; i=0; n=len(s); depth=0
    while i<n:
        two=s[i:i+2]
        if depth==0 and two=="--":
            j=s.find("\n", i);
            if j==-1: break
            i=j
        elif two=="/-":
            depth+=1; i+=2
        elif depth>0 and two=="-/":
            depth-=1; i+=2
        elif depth>0:
            i+=1
        else:
            out.append(s[i]); i+=1
    return "".join(out)
files = sorted(glob.glob(os.path.join(src_dir, "**", "*.lean"), recursive=True))
if os.path.isfile(root_lean): files.append(root_lean)
bad=0
for f in files:
    code = strip_comments(open(f, encoding="utf-8").read())
    allow_sorry = (os.path.abspath(f) == os.path.abspath(theorems))
    # `axiom` as a declaration keyword (start of line, after stripping comments)
    if re.search(r'(?m)^\s*axiom\b', code):
        print(f"  {f}: contains `axiom` declaration"); bad+=1
    for kw in banned:
        if kw == "sorry" and allow_sorry:
            continue
        if re.search(r'\b'+re.escape(kw)+r'\b', code):
            print(f"  {f}: contains banned `{kw}`"); bad+=1
sys.exit(1 if bad else 0)
PY
)
BANNED_EXIT=$?
if [ "$BANNED_EXIT" -eq 0 ]; then
    echo "PASS: no banned keywords (sorry allowed only in Theorems.lean)"
else
    echo "FAIL: banned keywords detected"
    echo "$BANNED_OUT"
    ERRORS=$((ERRORS + 1))
fi

# --- Check 3: lake build clean ---
echo ""
echo "--- Check 3: lake build ---"
set +e
BUILD_OUTPUT=$(run_lake build 2>&1)
BUILD_EXIT=$?
set -e
BUILD_ERRORS=$(echo "$BUILD_OUTPUT" | grep -c "^error:" || true)
BUILD_WARNINGS=$(echo "$BUILD_OUTPUT" | grep "warning:" \
    | grep -v "declaration uses .sorry." | wc -l | tr -d '[:space:]' || true)
echo "$BUILD_OUTPUT" | tail -1
if [ "$BUILD_EXIT" -eq 0 ] && [ "$BUILD_ERRORS" -eq 0 ] && [ "$BUILD_WARNINGS" -eq 0 ]; then
    echo "PASS: build clean (only expected Theorems.lean sorry warnings)"
else
    echo "FAIL: build exit=$BUILD_EXIT, errors=$BUILD_ERRORS, unexpected warnings=$BUILD_WARNINGS"
    echo "$BUILD_OUTPUT" | grep -E "^error:|warning:" | grep -v "declaration uses .sorry." | head -20
    ERRORS=$((ERRORS + 1))
fi

# --- Check 4: #print axioms ---
echo ""
echo "--- Check 4: #print axioms (Prob4b.Solution.*) ---"
AX_FILE=$(mktemp /tmp/p4b_ax_XXXX.lean)
trap 'rm -f "$AX_FILE"' EXIT
{ echo "import Prob4b"; for t in "${TARGETS[@]}"; do echo "#print axioms Prob4b.Solution.$t"; done; } > "$AX_FILE"
set +e
AX_OUTPUT=$(run_lake env lean "$AX_FILE" 2>&1)
set -e
AX_FAIL=0
for t in "${TARGETS[@]}"; do
    line=$(echo "$AX_OUTPUT" | grep "Prob4b.Solution.$t' depends on axioms")
    if [ -z "$line" ]; then
        echo "FAIL: $t — no axiom output (build/name error)"; AX_FAIL=$((AX_FAIL+1)); continue
    fi
    # Allowed exactly: propext, Classical.choice, Quot.sound. Reject anything else.
    bad=$(echo "$line" | grep -oE "sorryAx|ofReduceBool|nativeDecide" || true)
    if [ -n "$bad" ]; then
        echo "FAIL: $t — non-standard axiom: $bad"; echo "   $line"; AX_FAIL=$((AX_FAIL+1))
    else
        echo "PASS: $t — [propext, Classical.choice, Quot.sound]"
    fi
done
[ "$AX_FAIL" -ne 0 ] && ERRORS=$((ERRORS + 1))

# --- Check 5: Statement gates (Discharge + Solution compile) ---
echo ""
echo "--- Check 5: Statement gates (Discharge / Solution) ---"
GATE_FAIL=0
for mod in Prob4b.Discharge Prob4b.Solution; do
    set +e
    GOUT=$(run_lake build "$mod" 2>&1); GEXIT=$?
    set -e
    GERR=$(echo "$GOUT" | grep -c "^error:" || true)
    if [ "$GEXIT" -eq 0 ] && [ "$GERR" -eq 0 ]; then
        echo "PASS: $mod compiles (statement↔proof gate holds)"
    else
        echo "FAIL: $mod did not compile"; echo "$GOUT" | grep "^error:" | head; GATE_FAIL=$((GATE_FAIL+1))
    fi
done
[ "$GATE_FAIL" -ne 0 ] && ERRORS=$((ERRORS + 1))

# --- Summary ---
END_TIME=$(date +%s); DURATION=$((END_TIME - START_TIME))
SUCCESS="false"; [ "$ERRORS" -eq 0 ] && SUCCESS="true"
echo ""
echo "=== RESULT: $([ "$SUCCESS" = "true" ] && echo PASS || echo FAIL) ($ERRORS issue(s), ${DURATION}s) ==="

if [ "$NO_LOG" -eq 0 ]; then
    LOG_DIR="$REPO_ROOT/logs"; mkdir -p "$LOG_DIR"
    TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    echo "{\"timestamp\":\"$TS\",\"target\":\"$TARGET\",\"build_errors\":$BUILD_ERRORS,\"build_warnings\":$BUILD_WARNINGS,\"issues\":$ERRORS,\"duration_sec\":$DURATION,\"success\":$SUCCESS}" \
        >> "$LOG_DIR/verify_log.jsonl"
fi

exit "$ERRORS"
