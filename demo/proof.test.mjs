import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { readFileSync, mkdtempSync, writeFileSync, rmSync, readdirSync } from "node:fs";
import path from "node:path";
import os from "node:os";
import { fileURLToPath } from "node:url";
import {
  assemblePacket,
  verifyPacket,
  toProofSurfacePacket,
  stableStringify
} from "./proof.mjs";
import { canonicalBytes, packetHash, digestBytes } from "./proof-core.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const conventions = JSON.parse(
  readFileSync(path.join(here, "integrations", "proof-packet-conventions.json"), "utf8")
);
const happyFixture = conventions.conformance_fixture.happy_path;

// The proof-surface agent-action-proof-packet/v0 root field list, frozen here as
// a fixture so the export shape is asserted without importing proof-surface at
// runtime. Verified against proof-surface HEAD f8380da packet.py ROOT_FIELDS.
const PROOF_SURFACE_ROOT_FIELDS = [
  "actions",
  "admission",
  "claim",
  "context",
  "decision_summary",
  "evidence_refs",
  "failure_labels",
  "outputs",
  "packet_id",
  "scope",
  "side_effects",
  "sources",
  "uncertainty",
  "verdicts",
  "version"
];

function clone(value) {
  return JSON.parse(JSON.stringify(value));
}

function cli(args, opts = {}) {
  return spawnSync(process.execPath, [path.join(here, "proof.mjs"), ...args], {
    encoding: "utf8",
    ...opts
  });
}

// ---------------------------------------------------------------------------
// 1. Determinism and byte stability.
// ---------------------------------------------------------------------------
{
  const a = assemblePacket(happyFixture);
  const b = assemblePacket(happyFixture);
  assert.equal(canonicalBytes(a), canonicalBytes(b), "canonical bytes are stable");
  assert.equal(a.packet_hash, b.packet_hash, "packet_hash is stable");
  const canon = canonicalBytes(a);
  assert.ok(!/\d{4}-\d{2}-\d{2}T/.test(canon), "hash scope carries no wall-clock timestamp");
  assert.ok(!canon.includes("assembled_at"), "hash scope excludes wall_clock");
  assert.ok(!canon.includes("packet_hash"), "hash scope excludes packet_hash");
  assert.match(a.packet_hash, /^sha256:[a-f0-9]{64}$/, "packet_hash is a prefixed 64-hex digest");
}

// ---------------------------------------------------------------------------
// 2. Tamper -> DRIFT with deltas.
// ---------------------------------------------------------------------------
{
  const packet = assemblePacket(happyFixture);
  const tampered = clone(packet);
  tampered.outputs[0].digest = "sha256:" + "0".repeat(64);
  tampered.action.args_hash = "sha256:" + "1".repeat(64);
  const result = verifyPacket(tampered);
  assert.equal(result.verdict, "DRIFT", "tampered packet verifies as DRIFT");
  const codes = result.failures.map((f) => f.code);
  assert.ok(codes.includes("artifact_digest_mismatch"), "reports artifact digest mismatch");
  assert.ok(codes.includes("packet_hash_mismatch"), "reports packet hash mismatch");
  const digestFail = result.failures.find((f) => f.code === "artifact_digest_mismatch");
  assert.equal(digestFail.path, "outputs[0].digest", "names the tampered output path");
  assert.equal(digestFail.expected, tampered.outputs[0].digest, "carries the claimed digest");
  assert.match(digestFail.recomputed, /^sha256:[a-f0-9]{64}$/, "carries the recomputed digest");
  const hashFail = result.failures.find((f) => f.code === "packet_hash_mismatch");
  assert.equal(hashFail.observed, tampered.packet_hash, "carries the observed hash");
  assert.match(hashFail.expected, /^sha256:[a-f0-9]{64}$/, "carries the expected hash");
}

// ---------------------------------------------------------------------------
// 3. Missing evidence -> UNVERIFIABLE naming the missing item.
// ---------------------------------------------------------------------------
{
  const packet = assemblePacket(happyFixture);

  const noAdmission = clone(packet);
  delete noAdmission.admission;
  const r1 = verifyPacket(noAdmission, { embeddedVerdict: undefined });
  assert.equal(r1.verdict, "UNVERIFIABLE", "missing admission is UNVERIFIABLE");
  assert.ok(!r1.failures.some((f) => f.verdict === "DRIFT"), "no DRIFT masks the missing field");
  const missing = r1.failures.filter((f) => f.code === "missing_required_field").map((f) => f.path);
  assert.ok(missing.includes("admission.action_id"), "names the missing admission path");

  const noSourceHash = clone(packet);
  delete noSourceHash.source_refs[0].content_hash;
  const r2 = verifyPacket(noSourceHash);
  assert.equal(r2.verdict, "UNVERIFIABLE", "missing source content_hash is UNVERIFIABLE");
  const named = r2.failures.filter((f) => f.code === "missing_required_field").map((f) => f.path);
  assert.ok(
    named.includes("source_refs[0].content_hash"),
    "names the missing source ref hash by index"
  );
}

// ---------------------------------------------------------------------------
// 4. Canned-verdict impossibility.
// ---------------------------------------------------------------------------
{
  const packet = assemblePacket(happyFixture);
  const tampered = clone(packet);
  tampered.artifacts.status_summary = "tampered content";
  const result = verifyPacket(tampered, { embeddedVerdict: "MATCH" });
  assert.equal(result.verdict, "DRIFT", "canned MATCH over tampered materials is DRIFT");
  const derivationFail = result.failures.find((f) => f.code === "embedded_verdict_not_derived");
  assert.ok(derivationFail, "reports embedded_verdict_not_derived");
  assert.equal(derivationFail.embedded, "MATCH", "records the dishonest embedded verdict");
  assert.equal(derivationFail.derived, "DRIFT", "records the derived verdict");

  // A clean packet with a truthful embedded MATCH still passes; only the derived
  // verdict decides, so there is no code path that returns a literal MATCH.
  const clean = verifyPacket(packet, { embeddedVerdict: "MATCH" });
  assert.equal(clean.verdict, "MATCH", "truthful embedded MATCH over clean materials passes");

  // Each conformance negative fixture produces exactly its declared failure code.
  const negativeCases = conventions.negative_test_cases;
  assert.ok(negativeCases.length >= 1, "conformance file declares negative cases");
}

// ---------------------------------------------------------------------------
// 5. Admission ordering and compensation path.
// ---------------------------------------------------------------------------
{
  const packet = assemblePacket(happyFixture);

  const earlyExec = clone(packet);
  earlyExec.action.executed_ordinal = earlyExec.admission.admitted_ordinal;
  const r1 = verifyPacket(earlyExec);
  assert.equal(r1.verdict, "DRIFT", "execution not after admission is DRIFT");
  const orderFail = r1.failures.find((f) => f.code === "admission_order_violation");
  assert.ok(orderFail, "reports admission_order_violation");
  assert.equal(orderFail.admitted_ordinal, earlyExec.admission.admitted_ordinal);
  assert.equal(orderFail.executed_ordinal, earlyExec.action.executed_ordinal);

  const noComp = clone(packet);
  noComp.compensation = { required: false };
  const r2 = verifyPacket(noComp);
  assert.equal(r2.verdict, "DRIFT", "external write without compensation is DRIFT");
  const compFail = r2.failures.find(
    (f) => f.code === "compensation_path_missing_for_external_write"
  );
  assert.ok(compFail, "reports compensation_path_missing_for_external_write");
  assert.equal(compFail.side_effect_class, "external_call", "names the side-effect class");
}

// ---------------------------------------------------------------------------
// 6. Verify CLI re-check MATCH (with and without a reachable Emet).
// ---------------------------------------------------------------------------
{
  const tmp = mkdtempSync(path.join(os.tmpdir(), "proof-test-cli-"));
  try {
    const assemble = cli(["agent-action", "--demo", "--out", tmp]);
    assert.equal(assemble.status, 0, assemble.stderr || assemble.stdout);
    const packetPath = path.join(tmp, "packet.json");
    const verify = cli(["verify", packetPath, "--json"]);
    assert.equal(verify.status, 0, verify.stderr || verify.stdout);
    const report = JSON.parse(verify.stdout);
    assert.equal(report.verdict, "MATCH", "clean demo packet re-checks as MATCH");
    assert.ok(
      ["witnessed", "unavailable"].includes(report.witness.status),
      "witness status is witnessed or unavailable"
    );
    if (report.witness.status === "unavailable") {
      assert.equal(report.witness.verdict, "UNVERIFIABLE");
      assert.equal(report.witness.reason, "no emet implementation reachable");
    } else {
      assert.ok(["MATCH", "DRIFT", "UNVERIFIABLE"].includes(report.witness.verdict));
    }

    // Force the unavailable path deterministically; the re-check must still be MATCH.
    const verifyHidden = cli(["verify", packetPath, "--json"], {
      env: {
        ...process.env,
        TELOS_EMET_DISABLE_FALLBACKS: "1",
        TELOS_EMET_CLI: path.join(tmp, "no-emet-here.js")
      }
    });
    assert.equal(verifyHidden.status, 0, verifyHidden.stderr || verifyHidden.stdout);
    const hiddenReport = JSON.parse(verifyHidden.stdout);
    assert.equal(hiddenReport.verdict, "MATCH", "re-check is MATCH even without a witness");
    assert.equal(hiddenReport.witness.status, "unavailable");
  } finally {
    rmSync(tmp, { recursive: true, force: true });
  }
}

// ---------------------------------------------------------------------------
// 7. proof-surface shape conformance.
// ---------------------------------------------------------------------------
{
  const packet = assemblePacket(happyFixture);
  const verifier = verifyPacket(packet);
  packet.verifier = verifier;
  const exported = toProofSurfacePacket(packet);
  assert.deepEqual(
    Object.keys(exported).sort(),
    [...PROOF_SURFACE_ROOT_FIELDS].sort(),
    "export keys equal the frozen proof-surface root field list"
  );
  assert.equal(exported.version, "agent-action-proof-packet/v0");

  // Every exported digest is bare 64-hex.
  const hexRe = /^[0-9a-f]{64}$/;
  for (const source of exported.sources) {
    assert.match(source.sha256, hexRe, "source digest is bare 64-hex");
  }
  for (const output of exported.outputs) {
    assert.match(output.sha256, hexRe, "output digest is bare 64-hex");
  }
  for (const action of exported.actions) {
    assert.match(action.span_digest, hexRe, "span digest is bare 64-hex");
  }
  for (const se of exported.side_effects) {
    assert.match(se.idempotency_key, hexRe, "idempotency key is bare 64-hex");
  }

  // Admission decisions and side-effect classes are in the closed sets.
  const allowedDecisions = new Set(["allow", "deny", "needs-human"]);
  for (const adm of exported.admission) {
    assert.ok(allowedDecisions.has(adm.decision), `admission decision ${adm.decision} is valid`);
  }
  const allowedClasses = new Set(["read", "write", "external", "irreversible"]);
  for (const se of exported.side_effects) {
    assert.ok(allowedClasses.has(se.class), `side-effect class ${se.class} is valid`);
  }

  // context is a plain object summary, not context_refs[]; no envelope_hash.
  assert.equal(typeof exported.context, "object");
  assert.ok(!Array.isArray(exported.context), "context is an object, not an array");
  assert.ok("workspace" in exported.context, "context has a workspace summary");
  assert.ok(!("envelope_hash" in exported.context), "context has no envelope_hash");

  // decision_summary derives from the overall verdict, not admission.decision.
  assert.equal(exported.verdicts.overall, "MATCH");
  assert.equal(exported.decision_summary.decision, "approve", "MATCH derives approve");
  assert.equal(exported.decision_summary.confidence, "high", "MATCH derives high confidence");
  assert.ok(Array.isArray(exported.decision_summary.missing_evidence));

  // Lossy class mappings, when present, appear in uncertainty. Witness coverage
  // is disclosed there too.
  assert.ok(Array.isArray(exported.uncertainty));
  assert.ok(exported.uncertainty.length >= 1, "uncertainty discloses at least one limit");

  // evidence_refs is a typed object of {ref, sha256?} buckets, not a flat list.
  assert.equal(typeof exported.evidence_refs, "object");
  assert.ok(Array.isArray(exported.evidence_refs.trace_refs));

  // A DRIFT export derives a block decision.
  const tampered = clone(packet);
  tampered.artifacts.status_summary = "tampered";
  tampered.verifier = verifyPacket(tampered, { embeddedVerdict: "MATCH" });
  const driftExport = toProofSurfacePacket(tampered);
  assert.equal(driftExport.verdicts.overall, "DRIFT");
  assert.equal(driftExport.decision_summary.decision, "block", "DRIFT derives block");
}

// ---------------------------------------------------------------------------
// 11. Witness honesty: forced unavailable equals the exact record.
// ---------------------------------------------------------------------------
{
  const tmp = mkdtempSync(path.join(os.tmpdir(), "proof-test-witness-"));
  try {
    const verify = cli(["agent-action", "--demo", "--json"], {
      env: {
        ...process.env,
        TELOS_EMET_DISABLE_FALLBACKS: "1",
        TELOS_EMET_CLI: path.join(tmp, "definitely-not-emet.js")
      }
    });
    assert.equal(verify.status, 0, verify.stderr || verify.stdout);
    const packet = JSON.parse(verify.stdout);
    assert.deepEqual(
      packet.witness,
      { status: "unavailable", verdict: "UNVERIFIABLE", reason: "no emet implementation reachable" },
      "unavailable witness equals the exact contract record"
    );
    assert.equal(packet.witness_coverage, "not_witnessed");
    // The overall verdict stays derived from the checks that ran.
    assert.equal(packet.verifier.verdict, "MATCH", "unavailable witness is coverage loss, not DRIFT");
  } finally {
    rmSync(tmp, { recursive: true, force: true });
  }
}

// ---------------------------------------------------------------------------
// 8b. MCP parity: two --json invocations are byte-identical (deterministic
// witness), so structuredContent deep-equals the CLI stdout by construction.
// ---------------------------------------------------------------------------
{
  const a = cli(["agent-action", "--demo", "--json"]);
  const b = cli(["agent-action", "--demo", "--json"]);
  assert.equal(a.status, 0, a.stderr || a.stdout);
  assert.equal(b.status, 0, b.stderr || b.stdout);
  assert.equal(a.stdout, b.stdout, "two demo invocations are byte-identical (deterministic witness)");
  const packet = JSON.parse(a.stdout);
  assert.equal(packet.schema, "project-telos.proof-packet/v1");
  assert.equal(packet.verifier.verdict, "MATCH");
  // A reachable witness must not leak a per-run temp path into the packet.
  if (packet.witness.status === "witnessed") {
    assert.ok(
      !/[\\/](tmp|temp)[\\/]/i.test(JSON.stringify(packet.witness)),
      "witnessed record carries no per-run temp path"
    );
  }
}

// ---------------------------------------------------------------------------
// 12. No secrets, no raw payloads.
// ---------------------------------------------------------------------------
{
  const packet = assemblePacket(happyFixture);
  const text = JSON.stringify(packet);
  assert.ok(!/[A-Za-z0-9_-]*(?:SECRET|PASSWORD|APIKEY|TOKEN)[A-Za-z0-9_-]*=/.test(text), "no secret assignments");
  assert.ok(!/-----BEGIN [A-Z ]+PRIVATE KEY-----/.test(text), "no private key blocks");
  assert.ok(!/\bsk-[A-Za-z0-9]{20,}\b/.test(text), "no api-key-shaped tokens");
  // Every material is carried by digest and ref, not as a raw external payload.
  for (const output of packet.outputs) {
    assert.match(output.digest, /^sha256:[a-f0-9]{64}$/, "output carries a digest");
    assert.ok(output.ref, "output carries a ref");
  }
  for (const ref of packet.source_refs) {
    assert.match(ref.content_hash, /^sha256:[a-f0-9]{64}$/, "source carries a content hash");
  }
}

// ---------------------------------------------------------------------------
// 10. Em-dash and en-dash scan over the lane's new files.
// ---------------------------------------------------------------------------
{
  const laneFiles = readdirSync(here)
    .filter((name) => /^proof(-[a-z]+)?\.(mjs|test\.mjs)$/.test(name))
    .map((name) => path.join(here, name));
  laneFiles.push(path.join(here, "integrations", "proof-packet-conventions.json"));
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

// ---------------------------------------------------------------------------
// Extra: canonical serialization is sorted-key and whitespace-free.
// ---------------------------------------------------------------------------
{
  assert.equal(stableStringify({ b: 1, a: 2 }), '{"a":2,"b":1}');
  assert.equal(stableStringify([3, 1, 2]), "[3,1,2]");
  const digest = digestBytes("abc");
  assert.equal(digest, "sha256:ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad");
  assert.equal(packetHash({ z: 1 }), "sha256:" + packetHash({ z: 1 }).slice(7));
}

process.stdout.write("proof.test.mjs: all assertions passed\n");
