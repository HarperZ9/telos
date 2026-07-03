import { createHash } from "node:crypto";
import { existsSync, readFileSync, readdirSync, statSync } from "node:fs";
import { spawnSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const defaultRoot = path.resolve(here, "..");
const publicRoots = [
  "",
  "docs",
  "docs/registry",
  "docs/research/official",
  "docs/research/whitepapers",
  "docs/outreach"
];
const rootDocs = new Set([
  "README.md",
  "CHANGELOG.md",
  "PRODUCT.md",
  "USAGE.md",
  "AGENTS.md",
  "AUTHORS.md",
  "CONTRIBUTING.md"
]);
const pathPrefix = "(?:\\.github|demo|docs|tools|README|CHANGELOG|PRODUCT|USAGE|AGENTS|AUTHORS|CONTRIBUTING)";
const pathExt = "(?:md|mjs|json|jsonl|yml|yaml|txt|py|ps1|html)";
const rawPathPattern = new RegExp(`(^|[^A-Za-z0-9_./-])(${pathPrefix}[A-Za-z0-9_./\\\\*-]*\\.${pathExt})`, "g");

function sha256(text) {
  return `sha256:${createHash("sha256").update(text).digest("hex")}`;
}

function slash(value) {
  return value.replace(/\\/g, "/");
}

function rel(root, filePath) {
  return slash(path.relative(root, filePath));
}

function readSurface(root, relPath) {
  const resolved = path.join(root, relPath);
  const text = readFileSync(resolved, "utf8");
  return { relPath, text, hash: sha256(text) };
}

function collectPublicSurfaces(root) {
  const surfaces = [];
  for (const relativeDir of publicRoots) {
    const absoluteDir = path.join(root, relativeDir);
    if (!existsSync(absoluteDir) || !statSync(absoluteDir).isDirectory()) {
      continue;
    }
    for (const entry of readdirSync(absoluteDir, { withFileTypes: true })) {
      if (!entry.isFile() || !entry.name.endsWith(".md")) {
        continue;
      }
      const relative = slash(path.join(relativeDir, entry.name));
      if (relativeDir === "" && !rootDocs.has(entry.name)) {
        continue;
      }
      surfaces.push(relative);
    }
  }
  return [...new Set(surfaces)].sort();
}

function normalizeRef(raw) {
  let value = raw.trim().replace(/^<|>$/g, "").replace(/\\/g, "/");
  value = value.replace(/[),.;:]+$/g, "");
  value = value.split("#")[0].split("?")[0];
  if (!value || value.startsWith("#") || value.startsWith("/") || /^[a-z]+:/i.test(value)) {
    return null;
  }
  if (value.startsWith("./")) {
    value = value.slice(2);
  }
  if (!new RegExp(`^${pathPrefix}`).test(value)) {
    return null;
  }
  if (!value.includes(".") && !value.endsWith("/")) {
    return null;
  }
  return value;
}

function extractRefs(surface) {
  const refs = [];
  const lines = surface.text.split(/\r?\n/);
  for (let index = 0; index < lines.length; index += 1) {
    const line = lines[index];
    addMarkdownRefs(refs, surface.relPath, line, index + 1);
    addInlineRefs(refs, surface.relPath, line, index + 1);
    addRawRefs(refs, surface.relPath, line, index + 1);
  }
  return dedupeRefs(refs);
}

function addRef(refs, surface, line, raw, source) {
  const normalized = normalizeRef(raw);
  if (normalized) {
    refs.push({ surface, line, path_ref: normalized, source });
  }
}

function addMarkdownRefs(refs, surface, line, lineNumber) {
  for (const match of line.matchAll(/\[[^\]]+\]\(([^)]+)\)/g)) {
    addRef(refs, surface, lineNumber, match[1], "markdown-link");
  }
}

function addInlineRefs(refs, surface, line, lineNumber) {
  for (const match of line.matchAll(/`([^`]+)`/g)) {
    addRef(refs, surface, lineNumber, match[1], "inline-code");
  }
}

function addRawRefs(refs, surface, line, lineNumber) {
  for (const match of line.matchAll(rawPathPattern)) {
    addRef(refs, surface, lineNumber, match[2], "text-path");
  }
}

function dedupeRefs(refs) {
  const seen = new Set();
  const unique = [];
  for (const ref of refs) {
    const key = `${ref.surface}:${ref.line}:${ref.path_ref}`;
    if (!seen.has(key)) {
      seen.add(key);
      unique.push(ref);
    }
  }
  return unique;
}

function gitLines(root, args) {
  const result = spawnSync("git", args, { cwd: root, encoding: "utf8" });
  if (result.status !== 0) {
    return null;
  }
  return result.stdout.split(/\r?\n/).filter(Boolean);
}

function gitSnapshot(root) {
  const tracked = gitLines(root, ["ls-files"]);
  const status = gitLines(root, ["status", "--porcelain=v1", "--untracked-files=all"]);
  if (!tracked || !status) {
    return null;
  }
  return {
    tracked: new Set(tracked.map(slash)),
    dirty: new Set(status.map((line) => slash(line.slice(3))))
  };
}

function gitState(snapshot, relPath) {
  if (!snapshot) {
    return { status: "UNVERIFIABLE", failure_code: "git_state_unavailable" };
  }
  if (!snapshot.tracked.has(relPath)) {
    return { status: "WORKING_TREE_ONLY", failure_code: "working_tree_only_reference" };
  }
  if (snapshot.dirty.has(relPath)) {
    return { status: "DIRTY", failure_code: "dirty_reference" };
  }
  return { status: "CLEAN_TRACKED" };
}

function directoryState(snapshot, relPath) {
  if (!snapshot) {
    return { status: "UNVERIFIABLE", failure_code: "git_state_unavailable" };
  }
  const prefix = relPath.endsWith("/") ? relPath : `${relPath}/`;
  const hasTrackedChildren = [...snapshot.tracked].some((trackedPath) => trackedPath.startsWith(prefix));
  if (!hasTrackedChildren) {
    return { status: "WORKING_TREE_ONLY", failure_code: "working_tree_only_reference" };
  }
  const hasDirtyChildren = [...snapshot.dirty].some((dirtyPath) => dirtyPath.startsWith(prefix));
  if (hasDirtyChildren) {
    return { status: "DIRTY_CONTAINER", failure_code: "dirty_reference" };
  }
  return { status: "CLEAN_TRACKED_CONTAINER" };
}

function classifyRef(root, snapshot, ref) {
  if (ref.path_ref.includes("*")) {
    return { ...ref, status: "GLOB_REFERENCE" };
  }
  const absolute = path.join(root, ref.path_ref);
  if (!existsSync(absolute)) {
    return { ...ref, status: "MISSING", failure_code: "missing_reference" };
  }
  if (statSync(absolute).isDirectory()) {
    return { ...ref, ...directoryState(snapshot, ref.path_ref) };
  }
  return { ...ref, ...gitState(snapshot, ref.path_ref) };
}

function failureCodes(references) {
  return [...new Set(references.map((ref) => ref.failure_code).filter(Boolean))].sort();
}

function surfaceRefs(surfaces) {
  return surfaces.map((surface) => ({
    path_ref: surface.relPath,
    hash: surface.hash,
    reference_count: surface.refs.length
  }));
}

export function scanPublicationBoundary(options = {}) {
  const root = path.resolve(options.root ?? defaultRoot);
  const surfacePaths = options.surfaces ?? collectPublicSurfaces(root);
  const snapshot = gitSnapshot(root);
  const surfaces = surfacePaths
    .filter((surface) => existsSync(path.join(root, surface)))
    .map((surface) => readSurface(root, surface));
  for (const surface of surfaces) {
    surface.refs = extractRefs(surface).map((ref) => classifyRef(root, snapshot, ref));
  }
  const references = surfaces.flatMap((surface) => surface.refs);
  const failures = failureCodes(references);
  const verdict = failures.length === 0 ? "MATCH" : "DRIFT";
  return {
    schema: "project-telos.publication-boundary-gate/v1",
    tool: "telos.publication.boundary",
    generated_at: options.generatedAt ?? new Date().toISOString(),
    aggregate: {
      verdict,
      surface_count: surfaces.length,
      reference_count: references.length,
      failing_reference_count: references.filter((ref) => ref.failure_code).length,
      glob_reference_count: references.filter((ref) => ref.status === "GLOB_REFERENCE").length,
      failure_codes: failures
    },
    surfaces: surfaceRefs(surfaces),
    references: references.map((ref) => ({
      surface: ref.surface,
      line: ref.line,
      path_ref: ref.path_ref,
      status: ref.status,
      source: ref.source,
      ...(ref.failure_code ? { failure_code: ref.failure_code } : {})
    })),
    privacy_boundary: {
      raw_docs_included: false,
      absolute_paths_included: false,
      git_diff_included: false,
      external_fetches_performed: false,
      filesystem_writes_performed: false,
      local_subprocesses_performed: true
    },
    requirements: [
      "Public-facing Markdown surfaces may reference only committed, clean, repo-tracked files.",
      "Missing, untracked, or dirty referenced artifacts block publication claims.",
      "Glob references are counted but do not prove a concrete artifact is publication-ready.",
      "The receipt includes hashes and path refs, not raw document bodies."
    ]
  };
}

function printSummary(packet) {
  const lines = [
    "Telos Publication Boundary Gate",
    `schema     ${packet.schema}`,
    `surfaces   ${packet.aggregate.surface_count}`,
    `references ${packet.aggregate.reference_count}`,
    `failures   ${packet.aggregate.failing_reference_count}`,
    `globs      ${packet.aggregate.glob_reference_count}`,
    `verdict    ${packet.aggregate.verdict}`,
    "next       node demo/publication-boundary-gate.mjs --strict --summary"
  ];
  process.stdout.write(`${lines.join("\n")}\n`);
}

function argValue(args, name) {
  const index = args.indexOf(name);
  const inline = args.find((arg) => arg.startsWith(`${name}=`));
  if (inline) {
    return inline.slice(name.length + 1);
  }
  return index === -1 ? null : args[index + 1];
}

function main() {
  const args = process.argv.slice(2);
  const packet = scanPublicationBoundary({ root: argValue(args, "--root") ?? defaultRoot });
  if (args.includes("--summary")) {
    printSummary(packet);
  } else {
    process.stdout.write(`${JSON.stringify(packet, null, 2)}\n`);
  }
  if (args.includes("--strict") && packet.aggregate.verdict !== "MATCH") {
    process.exitCode = 1;
  }
}

if (process.argv[1] && import.meta.url.endsWith(process.argv[1].replace(/\\/g, "/"))) {
  main();
}
