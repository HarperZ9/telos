import { spawnSync } from "node:child_process";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { actionEnvelope } from "./flagship-action.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const telosRoot = path.resolve(here, "..");
const publicRoot = path.resolve(telosRoot, "..");

function py(repo, moduleName, args) {
  const repoRoot = path.join(publicRoot, repo);
  const sourcePath = path.join(repoRoot, "src");
  const code = [
    "import importlib, json, sys",
    "sys.path.insert(0, sys.argv[1])",
    "cli_args = json.loads(sys.argv[2])",
    "module_name = sys.argv[3]",
    "cli = importlib.import_module(module_name + '.cli')",
    "raise SystemExit(cli.main(cli_args))"
  ].join("; ");
  const result = spawnSync(
    "python",
    ["-c", code, sourcePath, JSON.stringify(args), moduleName],
    { cwd: repoRoot, encoding: "utf8" }
  );
  if (result.status !== 0) {
    throw new Error(`${repo} ${args.join(" ")} failed: ${result.stderr || result.stdout}`);
  }
  return result.stdout;
}

function jsonFrom(label, stdout) {
  const text = stdout.trim();
  if (!text) {
    throw new Error(`${label} returned no JSON`);
  }
  return JSON.parse(text);
}

const specPath = path.join(
  telosRoot,
  "docs",
  "superpowers",
  "specs",
  "2026-06-27-flagship-operator-spine-design.md"
);
const tmp = mkdtempSync(path.join(tmpdir(), "telos-flagship-workflow-"));
const thesis = path.join(tmp, "thesis.json");
const measurements = path.join(tmp, "measurements.json");

try {
  writeFileSync(
    thesis,
    JSON.stringify(
      {
        title: "Operator spine smoke claims",
        claims: [
          {
            text: "the operator spine spec exists",
            falsification: "the spec file is missing"
          },
          {
            text: "the golden workflow is already persisted in a registry",
            falsification: "no registry receipt exists"
          }
        ]
      },
      null,
      2
    )
  );

  writeFileSync(
    measurements,
    JSON.stringify(
      {
        measurements: [
          {
            claim: "the operator spine spec exists",
            deviation: 0.0,
            tolerance: 0.1,
            method: "file-exists",
            evidence: [specPath]
          }
        ]
      },
      null,
      2
    )
  );

  const indexMap = jsonFrom("index.map", py("index", "index_graph", ["map", "--root", telosRoot, "--json"]));
  const gatherDocs = jsonFrom("gather.docs", py("gather", "gather", ["docs", specPath, "--json"]));
  const forumRoute = jsonFrom(
    "forum.route",
    py("forum", "forum", ["route", "improve Project Telos flagship gather crucible index forum provenance workflow"])
  );
  const crucibleAssess = jsonFrom(
    "crucible.assess",
    py("crucible", "crucible", ["assess", thesis, "--measurements", measurements, "--json"])
  );

  const demo = spawnSync("node", ["demo/run.mjs"], { cwd: telosRoot, encoding: "utf8" });
  if (demo.status !== 0) {
    throw new Error(`telos demo failed: ${demo.stderr || demo.stdout}`);
  }

  const payload = actionEnvelope({
    tool: "telos",
    toolVersion: "0.1.0",
    command: "flagship-workflow",
    native: {
      index_repo_count: indexMap.repo_count ?? indexMap.repositories?.length ?? 0,
      index_dirty_count: indexMap.dirty_count ?? 0,
      gather_receipts: gatherDocs.digest?.receipts?.length ?? 0,
      forum_decided: forumRoute.decided,
      forum_needs_escalation: forumRoute.needs_escalation,
      crucible_match: crucibleAssess.assessment?.match ?? 0,
      crucible_drift: crucibleAssess.assessment?.drift ?? 0,
      crucible_unverifiable: crucibleAssess.assessment?.unverifiable ?? 0,
      telos_demo_recheck: demo.stdout.includes("recheck=true")
    },
    receipts: gatherDocs.digest?.receipts ?? [],
    nextActions: [
      {
        tool: "crucible",
        action: "recheck",
        reason: "replay the workflow assessment after it is persisted to a registry",
        inputs: [],
        priority: "normal"
      },
      {
        tool: "telos",
        action: "workbench",
        reason: "render this same envelope in an IDE, CLI, TUI, or app harness",
        inputs: [],
        priority: "low"
      }
    ]
  });

  console.log(JSON.stringify(payload, null, 2));
} finally {
  rmSync(tmp, { recursive: true, force: true });
}
