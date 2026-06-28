import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync, statSync } from "node:fs";
import { dirname, isAbsolute, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const demoRoot = dirname(fileURLToPath(import.meta.url));
const packRoot = resolve(demoRoot, "integrations", "smallharness-dogfood-pack");
const packPath = resolve(packRoot, "pack.json");
const pack = readJson(packPath);

const executableKeys = new Set([
  "command",
  "commands",
  "exec",
  "executable",
  "hook",
  "hooks",
  "postRun",
  "preRun",
  "script",
  "scripts",
  "setup",
  "shell",
  "teardown"
]);

assert.equal(pack.schema, "project-telos.smallharness-fixture-pack/v0");
assert.equal(pack.packId, "project-telos.receipt-boundary-dogfood");
assert.equal(pack.builtInFixtureCompatibility, "unchanged");
assert.equal(pack.routingOnly, true);
assert.equal(pack.noExecutableHooks, true);
assertNoExecutableFields(pack, "pack");

const workspaceRoot = resolveUnder(packRoot, pack.workspaceRoot, "workspaceRoot");
assert.equal(statSync(workspaceRoot).isDirectory(), true);

for (const entry of pack.fixtures) {
  const fixturePath = resolveUnder(packRoot, entry.path, `${entry.id}.fixture`);
  const fixture = readJson(fixturePath);
  const receiptPath = resolveUnder(packRoot, entry.receipt, `${entry.id}.receipt`);
  const receipt = readJson(receiptPath);

  assert.equal(fixture.id, entry.id);
  assertNoExecutableFields(fixture, `${entry.id}.fixture`);
  assertMinimalReceipt({ entry, fixture, fixturePath, receipt });

  if (fixture.expectedFailureCode === "path_escape_denied") {
    assert.throws(
      () => resolveUnder(packRoot, fixture.workspace, `${entry.id}.workspace`),
      /escapes pack root/
    );
    assert.equal(receipt.decisionOutcome, "block");
    continue;
  }

  const fixtureWorkspace = resolveUnder(packRoot, fixture.workspace, `${entry.id}.workspace`);
  assertUnder(workspaceRoot, fixtureWorkspace, `${entry.id}.workspaceRoot`);
  assert.equal(statSync(fixtureWorkspace).isDirectory(), true);
}

function assertMinimalReceipt({ entry, fixture, fixturePath, receipt }) {
  assert.equal(receipt.schema, "smallharness.minimal-run-receipt/v0");
  assert.equal(receipt.fixtureId, entry.id);
  assert.equal(receipt.packId, pack.packId);
  assert.equal(receipt.packVersion, pack.packVersion);
  assert.equal(receipt.fixtureFileHash, sha256File(fixturePath));
  assert.equal(typeof receipt.backendModelLabel, "string");
  assert.ok(receipt.backendModelLabel.length > 0);
  assert.deepEqual(
    receipt.checks.map((check) => check.id),
    fixture.checks.map((check) => check.id)
  );

  for (const check of receipt.checks) {
    assert.ok(["pass", "fail", "blocked"].includes(check.outcome));
    assert.equal(typeof check.type, "string");
    assert.ok(check.type.length > 0);
  }

  assert.ok(Array.isArray(receipt.observedToolCallNames));
  assertRootRelativeRef(receipt.transcriptPath, `${entry.id}.transcriptPath`);
  assertRootRelativeRef(receipt.evalJsonPath, `${entry.id}.evalJsonPath`);

  for (const omitted of [
    "workspaceHash",
    "diffArtifactRefs",
    "stdoutArtifactRefs",
    "stderrArtifactRefs",
    "artifactIndex"
  ]) {
    assert.ok(receipt.notCapturedYet.includes(omitted), `receipt must name omitted field ${omitted}`);
  }
}

function assertNoExecutableFields(value, location) {
  if (Array.isArray(value)) {
    value.forEach((item, index) => assertNoExecutableFields(item, `${location}[${index}]`));
    return;
  }

  if (!value || typeof value !== "object") {
    return;
  }

  for (const [key, child] of Object.entries(value)) {
    assert.equal(executableKeys.has(key), false, `${location}.${key} must stay data-only`);
    assertNoExecutableFields(child, `${location}.${key}`);
  }
}

function assertRootRelativeRef(value, label) {
  assert.equal(typeof value, "string", `${label} must be a path string`);
  assert.equal(isAbsolute(value), false, `${label} must be relative`);
  resolveUnder(packRoot, value, label);
}

function assertUnder(root, candidate, label) {
  const rel = relative(root, candidate);
  assert.equal(rel === "" || (!rel.startsWith("..") && !isAbsolute(rel)), true, `${label} escaped root`);
}

function readJson(path) {
  return JSON.parse(readFileSync(path, "utf8"));
}

function resolveUnder(root, path, label) {
  const absolute = resolve(root, path);
  const rel = relative(root, absolute);
  if (rel === "" || (!rel.startsWith("..") && !isAbsolute(rel))) {
    return absolute;
  }

  const error = new Error(`${label} escapes pack root: ${path}`);
  error.code = "path_escape_denied";
  throw error;
}

function sha256File(path) {
  return `sha256:${createHash("sha256").update(readFileSync(path)).digest("hex")}`;
}
