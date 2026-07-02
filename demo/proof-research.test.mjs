import assert from "node:assert/strict";
import { readFileSync, readdirSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import {
  assembleResearchPacket,
  verifyResearchPacket,
  toProofSurfaceResearchPacket,
  canonicalBytes,
  packetHash,
  digestBytes,
  stableStringify
} from "./proof-research.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const conventions = JSON.parse(
  readFileSync(path.join(here, "integrations", "research-proof-packet-conventions.json"), "utf8")
);

// The proof-surface research-claim-proof-packet/v0 root field list, frozen here
// as a fixture so the export shape is asserted without importing proof-surface
// at runtime. Verified against proof-surface HEAD 8757032
// research_claim/packet.py ROOT_FIELDS.
const PROOF_SURFACE_ROOT_FIELDS = [
  "attempts",
  "checks",
  "claim",
  "decision_summary",
  "declared_branches",
  "evidence_classes",
  "failure_labels",
  "formal",
  "packet_id",
  "promotion",
  "scope",
  "sources",
  "statement",
  "uncertainty",
  "verdicts",
  "version",
  "witness_tier"
];

// proof-surface research_claim CHECK_STATUSES, OVERALL_VERDICTS, PROMOTIONS,
// frozen so a taxonomy drift is caught here rather than at export time.
const PROOF_SURFACE_CHECK_STATUSES = new Set(["pass", "fail", "unverifiable"]);
const PROOF_SURFACE_OVERALL_VERDICTS = new Set(["MATCH", "DRIFT", "UNVERIFIABLE"]);
const PROOF_SURFACE_PROMOTIONS = new Set([
  "SOURCE_LEAD",
  "HYPOTHESIS",
  "IDENTITY",
  "PROBE_MATCH",
  "CRUCIBLE_MATCH",
  "UNVERIFIABLE",
  "LAW_CANDIDATE",
  "REFUTED"
]);
const PROOF_SURFACE_FAILURE_CODES = new Set([
  "binding_failed",
  "unjoinable_action",
  "verification_unverifiable",
  "stale_criterion",
  "authority_gap",
  "evidence_gap",
  "duplicate_idempotency_key",
  "external_request_id_missing",
  "failed_route"
]);

function clone(value) {
  return JSON.parse(JSON.stringify(value));
}

// ---------------------------------------------------------------------------
// 1. Determinism and byte stability.
// ---------------------------------------------------------------------------
{
  const a = assembleResearchPacket({ demo: true });
  const b = assembleResearchPacket({ demo: true });
  assert.equal(canonicalBytes(a), canonicalBytes(b), "canonical bytes are stable");
  assert.equal(a.packet_hash, b.packet_hash, "packet_hash is stable");
  assert.equal(
    JSON.stringify(a.source_refs),
    JSON.stringify(b.source_refs),
    "source refs (with recomputed digests) are byte-identical"
  );
  const canon = canonicalBytes(a);
  assert.ok(!/\d{4}-\d{2}-\d{2}T/.test(canon), "hash scope carries no wall-clock timestamp");
  assert.ok(!canon.includes("assembled_at"), "hash scope excludes wall_clock");
  assert.ok(!canon.includes("packet_hash"), "hash scope excludes packet_hash");
  assert.match(a.packet_hash, /^sha256:[a-f0-9]{64}$/, "packet_hash is a prefixed 64-hex digest");

  // The assembler resolved the "recompute" placeholders into real digests.
  for (const ref of a.source_refs) {
    assert.match(ref.content_hash, /^sha256:[a-f0-9]{64}$/, "source content_hash is a real digest");
    assert.equal(ref.content_hash, digestBytes(ref.body), "content_hash recomputes from the body");
  }
  assert.equal(
    a.negative_fixture.content_hash,
    digestBytes(a.negative_fixture.body),
    "negative fixture content_hash recomputes from its body"
  );
  assert.equal(a.verdicts.overall, "MATCH", "the clean demo packet folds to MATCH");
}

// ---------------------------------------------------------------------------
// 2. Clean packet verifies as MATCH; re-check is MATCH.
// ---------------------------------------------------------------------------
{
  const packet = assembleResearchPacket({ demo: true });
  const result = verifyResearchPacket(packet);
  assert.equal(result.verdict, "MATCH", "clean demo packet verifies as MATCH");
  assert.equal(result.failures.length, 0, "clean demo packet has no failures");
  // A truthful embedded MATCH still passes; only the derived verdict decides.
  const recheck = verifyResearchPacket(packet, { embeddedVerdict: packet.verdicts.overall });
  assert.equal(recheck.verdict, "MATCH", "re-check with truthful embedded MATCH stays MATCH");
  // Every named check ran and passed.
  for (const check of result.checks) {
    assert.ok(check.passed || check.skipped, `${check.name} passed or was skipped`);
  }
}

// ---------------------------------------------------------------------------
// 3. Tamper a source body -> DRIFT with the expected-vs-recomputed delta.
// ---------------------------------------------------------------------------
{
  const packet = assembleResearchPacket({ demo: true });
  const tampered = clone(packet);
  tampered.source_refs[0].body = "tampered source body";
  const result = verifyResearchPacket(tampered);
  assert.equal(result.verdict, "DRIFT", "tampered source body verifies as DRIFT");
  const codes = result.failures.map((f) => f.code);
  assert.ok(codes.includes("source_digest_mismatch"), "reports source_digest_mismatch");
  assert.ok(codes.includes("packet_hash_mismatch"), "tamper also breaks the packet hash");
  const digestFail = result.failures.find((f) => f.code === "source_digest_mismatch");
  assert.equal(digestFail.path, "source_refs[0].content_hash", "names the tampered source path");
  assert.equal(digestFail.expected, packet.source_refs[0].content_hash, "carries the claimed digest");
  assert.equal(
    digestFail.recomputed,
    digestBytes("tampered source body"),
    "carries the recomputed digest over the tampered body"
  );
  assert.notEqual(digestFail.expected, digestFail.recomputed, "the delta is a real mismatch");
}

// ---------------------------------------------------------------------------
// 3b. Tamper the negative fixture body -> DRIFT naming the fixture digest.
// ---------------------------------------------------------------------------
{
  const packet = assembleResearchPacket({ demo: true });
  const tampered = clone(packet);
  tampered.negative_fixture.body = "a different control variant";
  const result = verifyResearchPacket(tampered);
  assert.equal(result.verdict, "DRIFT", "tampered negative fixture body is DRIFT");
  const fail = result.failures.find((f) => f.code === "negative_fixture_digest_mismatch");
  assert.ok(fail, "reports negative_fixture_digest_mismatch");
  assert.equal(fail.path, "negative_fixture.content_hash", "names the fixture digest path");
  assert.equal(fail.recomputed, digestBytes("a different control variant"), "recomputes the fixture digest");
}

// ---------------------------------------------------------------------------
// 4. Missing negative fixture -> UNVERIFIABLE, naming the missing item.
// ---------------------------------------------------------------------------
{
  const packet = assembleResearchPacket({ demo: true });
  const noNeg = clone(packet);
  delete noNeg.negative_fixture;
  const result = verifyResearchPacket(noNeg);
  assert.equal(result.verdict, "UNVERIFIABLE", "missing negative fixture is UNVERIFIABLE");
  assert.ok(!result.failures.some((f) => f.verdict === "DRIFT"), "no DRIFT masks the missing fixture");
  const missing = result.failures.filter((f) => f.code === "missing_required_field").map((f) => f.path);
  assert.ok(missing.includes("negative_fixture.id"), "names negative_fixture.id");
  assert.ok(missing.includes("negative_fixture.body"), "names negative_fixture.body");
  assert.ok(missing.includes("negative_fixture.control_outcome"), "names the missing control outcome");

  // Dropping only the control outcome is likewise UNVERIFIABLE, named.
  const noOutcome = clone(packet);
  delete noOutcome.negative_fixture.control_outcome;
  const r2 = verifyResearchPacket(noOutcome);
  assert.equal(r2.verdict, "UNVERIFIABLE", "missing control outcome is UNVERIFIABLE");
  const named = r2.failures.filter((f) => f.code === "missing_required_field").map((f) => f.path);
  assert.ok(named.includes("negative_fixture.control_outcome"), "names the missing control outcome path");
}

// ---------------------------------------------------------------------------
// 4b. A recorded not-survived control -> DRIFT (the check does not discriminate).
// ---------------------------------------------------------------------------
{
  const packet = assembleResearchPacket({ demo: true });
  const notSurvived = clone(packet);
  notSurvived.negative_fixture.control_outcome = "not_survived";
  const result = verifyResearchPacket(notSurvived);
  assert.equal(result.verdict, "DRIFT", "a not-survived control is DRIFT");
  const fail = result.failures.find((f) => f.code === "negative_control_not_survived");
  assert.ok(fail, "reports negative_control_not_survived");
  assert.equal(fail.path, "negative_fixture.control_outcome", "names the control outcome path");
}

// ---------------------------------------------------------------------------
// 5. Check that names an undeclared source ref -> UNVERIFIABLE named.
// ---------------------------------------------------------------------------
{
  // Mutate the fixture before assembly so the packet hash is computed over the
  // bad ref: the evidence gap is then the sole failure, not masked by a
  // derivative hash mismatch.
  const fixture = clone(conventions.conformance_fixture.happy_path);
  fixture.checks[0].source_ref_ids = ["src_that_does_not_exist"];
  const badRef = assembleResearchPacket(fixture);
  const result = verifyResearchPacket(badRef);
  assert.equal(result.verdict, "UNVERIFIABLE", "unresolvable check source ref is UNVERIFIABLE");
  const fail = result.failures.find((f) => f.code === "evidence_ref_unresolvable");
  assert.ok(fail, "reports evidence_ref_unresolvable");
  assert.equal(fail.ref, "src_that_does_not_exist", "carries the unresolvable ref id");
  assert.equal(fail.path, "checks[0].source_ref_ids", "names the check whose ref is unresolvable");
}

// ---------------------------------------------------------------------------
// 6. Promotion honesty: PROMOTED_DISCOVERY is never assertable in one packet.
// ---------------------------------------------------------------------------
{
  const packet = assembleResearchPacket({ demo: true });
  const promoted = clone(packet);
  promoted.promotion = "PROMOTED_DISCOVERY";
  const result = verifyResearchPacket(promoted);
  assert.equal(result.verdict, "DRIFT", "asserting PROMOTED_DISCOVERY in one packet is DRIFT");
  const fail = result.failures.find((f) => f.code === "promotion_not_assertable_in_single_packet");
  assert.ok(fail, "reports promotion_not_assertable_in_single_packet");
  assert.equal(fail.observed, "PROMOTED_DISCOVERY", "names the offending rung");

  // The exporter never emits a reproduction-gated rung either.
  const exported = toProofSurfaceResearchPacket(promoted);
  assert.notEqual(exported.promotion, "PROMOTED_DISCOVERY", "export never emits PROMOTED_DISCOVERY");
  assert.ok(PROOF_SURFACE_PROMOTIONS.has(exported.promotion), "export promotion is a known rung");
}

// ---------------------------------------------------------------------------
// 7. Canned-verdict impossibility.
// ---------------------------------------------------------------------------
{
  const packet = assembleResearchPacket({ demo: true });
  const tampered = clone(packet);
  tampered.source_refs[0].body = "silently tampered";
  const result = verifyResearchPacket(tampered, { embeddedVerdict: "MATCH" });
  assert.equal(result.verdict, "DRIFT", "canned MATCH over tampered materials is DRIFT");
  const derivationFail = result.failures.find((f) => f.code === "embedded_verdict_not_derived");
  assert.ok(derivationFail, "reports embedded_verdict_not_derived");
  assert.equal(derivationFail.embedded, "MATCH", "records the dishonest embedded verdict");
  assert.equal(derivationFail.derived, "DRIFT", "records the derived verdict");

  // There is no code path that returns a literal MATCH: the verdict is folded
  // from the checks alone. A clean packet with a truthful embedded MATCH passes,
  // a tampered packet with an embedded MATCH is DRIFT.
  const clean = verifyResearchPacket(packet, { embeddedVerdict: "MATCH" });
  assert.equal(clean.verdict, "MATCH", "truthful embedded MATCH over clean materials passes");

  // Recorded overall that disagrees with the fold of the check statuses is
  // check_status_not_derivable.
  const mislabeled = clone(packet);
  mislabeled.verdicts.overall = "DRIFT"; // no check failed, so the fold is MATCH
  const r2 = verifyResearchPacket(mislabeled);
  const mismatch = r2.failures.find((f) => f.code === "check_status_not_derivable");
  assert.ok(mismatch, "reports check_status_not_derivable when overall disagrees with the fold");
  assert.equal(mismatch.recomputed, "MATCH", "recomputes the folded overall");
  assert.equal(mismatch.recorded, "DRIFT", "records the mislabeled overall");
}

// ---------------------------------------------------------------------------
// 8. State-model violation on an attempt result -> DRIFT.
// ---------------------------------------------------------------------------
{
  const packet = assembleResearchPacket({ demo: true });
  const badAttempt = clone(packet);
  badAttempt.attempts[0].result = "definitely_true";
  const result = verifyResearchPacket(badAttempt);
  assert.equal(result.verdict, "DRIFT", "attempt result outside the taxonomy is DRIFT");
  const fail = result.failures.find(
    (f) => f.code === "state_model_violation" && f.path === "attempts[0].result"
  );
  assert.ok(fail, "reports state_model_violation on the attempt result");
  assert.equal(fail.observed, "definitely_true", "names the offending value");
  assert.ok(Array.isArray(fail.allowed), "carries the allowed set");
}

// ---------------------------------------------------------------------------
// 9. Every declared conformance negative case produces its declared code.
// ---------------------------------------------------------------------------
{
  const happy = conventions.conformance_fixture.happy_path;
  const cases = {
    tampered_source_body: (p) => {
      p.source_refs[0].body = "conformance tamper";
    },
    missing_negative_fixture: (p) => {
      delete p.negative_fixture;
    },
    negative_fixture_no_control_outcome: (p) => {
      delete p.negative_fixture.control_outcome;
    },
    negative_fixture_not_survived: (p) => {
      p.negative_fixture.control_outcome = "not_survived";
    },
    check_unresolvable_source_ref: (p) => {
      p.checks[0].source_ref_ids = ["not_a_declared_source"];
    },
    promoted_discovery_asserted: (p) => {
      p.promotion = "PROMOTED_DISCOVERY";
    }
  };
  for (const [name, mutate] of Object.entries(cases)) {
    const spec = conventions.conformance_fixture[name];
    assert.ok(spec, `conformance fixture declares ${name}`);
    // Mutate the fixture before assembly so the packet hash is computed over the
    // mutated materials. Deleting a required field or setting a bad value then
    // yields exactly the target failure, not a derivative packet-hash mismatch.
    // The two tamper cases (tampered_source_body, embedded_canned_match) are the
    // exception: they mutate a body after the hash is pinned, so the digest delta
    // is the whole point and is covered by the dedicated tamper assertions above.
    const fixture = clone(happy);
    if (name === "tampered_source_body") {
      // Assemble first (pins the hash to the original body), then tamper.
      const packet = assembleResearchPacket(fixture);
      mutate(packet);
      const result = verifyResearchPacket(packet);
      assert.equal(result.verdict, spec.expected_verdict, `${name} verdict is ${spec.expected_verdict}`);
      assert.ok(
        result.failures.map((f) => f.code).includes(spec.expected_failure_code),
        `${name} reports ${spec.expected_failure_code}`
      );
      continue;
    }
    mutate(fixture);
    const packet = assembleResearchPacket(fixture);
    const result = verifyResearchPacket(packet, { embeddedVerdict: undefined });
    assert.equal(result.verdict, spec.expected_verdict, `${name} verdict is ${spec.expected_verdict}`);
    const codes = result.failures.map((f) => f.code);
    assert.ok(
      codes.includes(spec.expected_failure_code),
      `${name} reports ${spec.expected_failure_code}; got ${JSON.stringify(codes)}`
    );
  }
  // The embedded-canned-match conformance case.
  const canned = conventions.conformance_fixture.embedded_canned_match;
  const cannedPacket = assembleResearchPacket(clone(happy));
  cannedPacket.source_refs[0].body = "conformance canned tamper";
  const cannedResult = verifyResearchPacket(cannedPacket, { embeddedVerdict: "MATCH" });
  assert.equal(cannedResult.verdict, canned.expected_verdict, "embedded_canned_match is DRIFT");
  assert.ok(
    cannedResult.failures.some((f) => f.code === canned.expected_failure_code),
    "embedded_canned_match reports embedded_verdict_not_derived"
  );
}

// ---------------------------------------------------------------------------
// 10. proof-surface research_claim shape conformance (frozen field list).
// ---------------------------------------------------------------------------
{
  const packet = assembleResearchPacket({ demo: true });
  const exported = toProofSurfaceResearchPacket(packet);
  assert.deepEqual(
    Object.keys(exported).sort(),
    [...PROOF_SURFACE_ROOT_FIELDS].sort(),
    "export keys equal the frozen proof-surface root field list"
  );
  assert.equal(exported.version, "research-claim-proof-packet/v0");
  assert.equal(exported.verdicts.overall, "MATCH");
  assert.ok(PROOF_SURFACE_PROMOTIONS.has(exported.promotion), "promotion is a known rung");
  assert.notEqual(exported.promotion, "PROMOTED_DISCOVERY", "PROMOTED_DISCOVERY is never emitted");
  assert.notEqual(exported.promotion, "LAW_CANDIDATE", "LAW_CANDIDATE is never emitted");

  // Every source sha256 is bare 64-hex or null.
  const hexRe = /^[0-9a-f]{64}$/;
  for (const source of exported.sources) {
    assert.ok(source.sha256 === null || hexRe.test(source.sha256), "source sha256 is bare 64-hex or null");
  }

  // Checks and per-check verdicts align 1:1 (proof-surface _validate_consistency).
  const checkNames = exported.checks.map((c) => c.checker);
  const perCheckNames = exported.verdicts.per_check.map((v) => v.checker);
  assert.deepEqual(
    [...checkNames].sort(),
    [...perCheckNames].sort(),
    "every check has exactly one matching per_check verdict"
  );
  assert.equal(new Set(checkNames).size, checkNames.length, "no duplicate checker names");
  for (const check of exported.checks) {
    assert.ok(PROOF_SURFACE_CHECK_STATUSES.has(check.status), `check status ${check.status} is valid`);
    assert.ok(Array.isArray(check.evidence), "check carries an evidence array");
  }
  for (const v of exported.verdicts.per_check) {
    assert.ok(PROOF_SURFACE_OVERALL_VERDICTS.has(v.status), `per_check status ${v.status} is valid`);
  }

  // The negative fixture is surfaced as a check with a survived outcome.
  const negCheck = exported.checks.find((c) => c.checker.startsWith("negative_fixture:"));
  assert.ok(negCheck, "the negative fixture is surfaced as a check");
  assert.equal(negCheck.status, "pass", "a survived control is a passing check");

  // decision_summary derives from the overall verdict, not from any attempt.
  assert.equal(exported.decision_summary.decision, "approve", "MATCH derives approve");
  assert.equal(exported.decision_summary.confidence, "high", "MATCH derives high confidence");
  assert.ok(Array.isArray(exported.decision_summary.missing_evidence), "missing_evidence is an array");

  // failure_labels are a subset of the proof-surface closed set.
  assert.ok(Array.isArray(exported.failure_labels), "failure_labels is an array");
  for (const label of exported.failure_labels) {
    assert.ok(PROOF_SURFACE_FAILURE_CODES.has(label), `failure label ${label} is a known code`);
  }

  // The optional family fields are null (absent) on a clean run, or valid.
  assert.equal(exported.formal, null, "formal is null on the demo packet");
  assert.equal(exported.declared_branches, null, "declared_branches is null on the demo packet");
  assert.equal(exported.witness_tier, null, "witness_tier is null on the demo packet");
  assert.ok(
    exported.evidence_classes === null || Array.isArray(exported.evidence_classes),
    "evidence_classes is null or an array"
  );

  // A DRIFT export derives a block decision, and no positive promotion survives.
  const tampered = clone(packet);
  tampered.source_refs[0].body = "export tamper";
  tampered.verdicts.overall = "MATCH";
  const driftExport = toProofSurfaceResearchPacket(tampered);
  assert.equal(driftExport.verdicts.overall, "DRIFT", "tampered export overall is DRIFT");
  assert.equal(driftExport.decision_summary.decision, "block", "DRIFT derives block");
  assert.equal(driftExport.promotion, "UNVERIFIABLE", "a DRIFT run emits no positive promotion");
  assert.ok(driftExport.failure_labels.includes("binding_failed"), "DRIFT export labels the binding failure");

  // An UNVERIFIABLE export derives escalate and carries missing evidence.
  const unv = clone(packet);
  delete unv.negative_fixture;
  const unvExport = toProofSurfaceResearchPacket(unv);
  assert.equal(unvExport.verdicts.overall, "UNVERIFIABLE", "missing-fixture export overall is UNVERIFIABLE");
  assert.equal(unvExport.decision_summary.decision, "escalate", "UNVERIFIABLE derives escalate");
  assert.ok(unvExport.decision_summary.missing_evidence.length >= 1, "escalation names missing evidence");
  assert.ok(unvExport.failure_labels.includes("evidence_gap"), "UNVERIFIABLE export labels the evidence gap");
}

// ---------------------------------------------------------------------------
// 11. No secrets, no raw external payloads beyond the embedded source bodies.
// ---------------------------------------------------------------------------
{
  const packet = assembleResearchPacket({ demo: true });
  const text = JSON.stringify(packet);
  assert.ok(!/[A-Za-z0-9_-]*(?:SECRET|PASSWORD|APIKEY|TOKEN)[A-Za-z0-9_-]*=/.test(text), "no secret assignments");
  assert.ok(!/-----BEGIN [A-Z ]+PRIVATE KEY-----/.test(text), "no private key blocks");
  assert.ok(!/\bsk-[A-Za-z0-9]{20,}\b/.test(text), "no api-key-shaped tokens");
  for (const ref of packet.source_refs) {
    assert.match(ref.content_hash, /^sha256:[a-f0-9]{64}$/, "source carries a content hash");
    assert.ok(ref.ref, "source carries a provenance ref");
  }
}

// ---------------------------------------------------------------------------
// 12. Canonical serialization is sorted-key and whitespace-free.
// ---------------------------------------------------------------------------
{
  assert.equal(stableStringify({ b: 1, a: 2 }), '{"a":2,"b":1}');
  assert.equal(stableStringify([3, 1, 2]), "[3,1,2]");
  assert.equal(
    digestBytes("abc"),
    "sha256:ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
  );
  assert.equal(packetHash({ z: 1 }), "sha256:" + packetHash({ z: 1 }).slice(7));
}

// ---------------------------------------------------------------------------
// 13. Em-dash and en-dash scan over the research lane's new files.
// ---------------------------------------------------------------------------
{
  const laneFiles = readdirSync(here)
    .filter((name) => /^proof-research(\.test)?\.mjs$/.test(name))
    .map((name) => path.join(here, name));
  laneFiles.push(path.join(here, "integrations", "research-proof-packet-conventions.json"));
  // Match by code point so this scanner does not itself contain the characters
  // it forbids (U+2014 em-dash, U+2013 en-dash).
  const emDash = String.fromCharCode(0x2014);
  const enDash = String.fromCharCode(0x2013);
  for (const file of laneFiles) {
    const bytes = readFileSync(file, "utf8");
    assert.ok(!bytes.includes(emDash), `${path.basename(file)} contains no em-dash`);
    assert.ok(!bytes.includes(enDash), `${path.basename(file)} contains no en-dash`);
  }
}

process.stdout.write("proof-research.test.mjs: all assertions passed\n");
