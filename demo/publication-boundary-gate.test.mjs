import assert from "node:assert/strict";
import { execFileSync, spawnSync } from "node:child_process";
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { scanPublicationBoundary } from "./publication-boundary-gate.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));

function git(root, args) {
  execFileSync("git", args, { cwd: root, stdio: "ignore" });
}

function write(root, relative, body) {
  const target = path.join(root, relative);
  mkdirSync(path.dirname(target), { recursive: true });
  writeFileSync(target, body, "utf8");
}

function setupRepo() {
  const root = mkdtempSync(path.join(tmpdir(), "telos-publication-gate-"));
  git(root, ["init"]);
  git(root, ["config", "user.email", "test@example.invalid"]);
  git(root, ["config", "user.name", "Telos Test"]);
  write(root, "README.md", [
    "# Fixture",
    "",
    "Use [`demo/ready.mjs`](demo/ready.mjs).",
    "Read `docs/ready.md`.",
    "Glob family `docs/research/official/*.md` stays counted, not promoted."
  ].join("\n"));
  write(root, "CHANGELOG.md", "# Changelog\n");
  write(root, "demo/ready.mjs", "console.log('ready');\n");
  write(root, "docs/ready.md", "# Ready\n");
  write(root, "docs/research/official/packet.md", "# Packet\n");
  git(root, ["add", "."]);
  git(root, ["commit", "-m", "fixture"]);
  return root;
}

function withRepo(callback) {
  const root = setupRepo();
  try {
    callback(root);
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
}

withRepo((root) => {
  const packet = scanPublicationBoundary({
    root,
    surfaces: ["README.md"],
    generatedAt: "2026-07-02T00:00:00.000Z"
  });
  assert.equal(packet.schema, "project-telos.publication-boundary-gate/v1");
  assert.equal(packet.tool, "telos.publication.boundary");
  assert.equal(packet.aggregate.verdict, "MATCH");
  assert.equal(packet.aggregate.surface_count, 1);
  assert.equal(packet.aggregate.reference_count, 3);
  assert.equal(packet.aggregate.glob_reference_count, 1);
  assert.deepEqual(packet.aggregate.failure_codes, []);
  assert.equal(packet.privacy_boundary.raw_docs_included, false);
  assert.equal(JSON.stringify(packet).includes("# Fixture"), false);
  assert.equal(JSON.stringify(packet).includes(root), false);
});

withRepo((root) => {
  write(root, "README.md", "New public claim links `demo/untracked.mjs`.\n");
  write(root, "demo/untracked.mjs", "console.log('new');\n");
  const packet = scanPublicationBoundary({ root, surfaces: ["README.md"] });
  assert.equal(packet.aggregate.verdict, "DRIFT");
  assert.deepEqual(packet.aggregate.failure_codes, ["working_tree_only_reference"]);
  assert.ok(packet.references.some((ref) => ref.path_ref === "demo/untracked.mjs"));
});

withRepo((root) => {
  write(root, "demo/ready.mjs", "console.log('dirty');\n");
  const packet = scanPublicationBoundary({ root, surfaces: ["README.md"] });
  assert.equal(packet.aggregate.verdict, "DRIFT");
  assert.deepEqual(packet.aggregate.failure_codes, ["dirty_reference"]);
});

withRepo((root) => {
  write(root, "README.md", "Missing public claim links [missing](docs/missing.md).\n");
  const packet = scanPublicationBoundary({ root, surfaces: ["README.md"] });
  assert.equal(packet.aggregate.verdict, "DRIFT");
  assert.deepEqual(packet.aggregate.failure_codes, ["missing_reference"]);
  assert.ok(packet.references.some((ref) => ref.path_ref === "docs/missing.md"));
});

withRepo((root) => {
  const json = spawnSync(process.execPath, [
    path.join(here, "publication-boundary-gate.mjs"),
    "--root",
    root
  ], { encoding: "utf8" });
  assert.equal(json.status, 0, json.stderr || json.stdout);
  assert.equal(JSON.parse(json.stdout).aggregate.verdict, "MATCH");

  const summary = spawnSync(process.execPath, [
    path.join(here, "publication-boundary-gate.mjs"),
    "--root",
    root,
    "--strict",
    "--summary"
  ], { encoding: "utf8" });
  assert.equal(summary.status, 0, summary.stderr || summary.stdout);
  assert.match(summary.stdout, /Telos Publication Boundary Gate/);
  assert.match(summary.stdout, /verdict\s+MATCH/);
});
