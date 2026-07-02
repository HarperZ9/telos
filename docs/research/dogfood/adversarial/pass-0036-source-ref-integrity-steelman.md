# Pass 0036 Steelman: Source-Ref Integrity

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

## Thesis Under Pressure

Pass 0036 claims that the pass 0035 theorem source refs resolve to actual Lean
source lines at the frozen `pipeline-math` commit and are bound to file/blob
hashes.

## Strongest Objections

1. The pass checks declaration headers, not full proof bodies.

Correct. This pass upgrades line refs to source-integrity receipts. It is not an
independent proof audit.

2. The source checkout is local temp state.

Correct. The commit, Git blob ids, file SHA-256 values, and line/context hashes
make the receipt replayable, but the next product step should fetch or archive
source blobs from the commit without relying on a temp directory.

3. Git blob ids are not SHA-256 object ids in this repository.

Correct. The packet records Git blob ids and separate SHA-256 hashes of blob
bytes/worktree bytes.

4. Matching line headers does not validate statement equivalence.

Correct. It proves the refs point at the expected symbols. Statement-body
equivalence remains a future AST/elaboration-level verifier.

5. The checkout inherits global `core.autocrlf=true`.

Correct. The pass records observed `git ls-files --eol` output and requires
`w/lf` for checked files rather than assuming config intent.

## Verdict

Strong evidence for source-ref integrity. Still bounded to declaration-line
binding, not full semantic proof review.
