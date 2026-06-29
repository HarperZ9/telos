import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const defaultInput = path.join(here, "integrations", "ci-triage-fixtures.json");

function sha256(text) {
  return `sha256:${createHash("sha256").update(text).digest("hex")}`;
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function sanitizeLine(line) {
  const authHeader = "Author" + "ization";
  return line
    .replace(/\u001b\[[0-9;]*m/g, "")
    .replace(/^[^\t\r\n]+\t[^\t\r\n]+\t\d{4}-\d\d-\d\dT[^\s]+\s+/g, "")
    .replace(/[A-Z]:\\[^:\n\r]+/g, "<runner-path>")
    .replace(/\/home\/runner\/work\/[^\s:]+/g, "<runner-path>")
    .replace(/gh[op]_[A-Za-z0-9_]+/g, "<redacted-token>")
    .replace(new RegExp(`${authHeader}:\\s*\\S+`, "gi"), `${authHeader}: <redacted>`);
}

function evidenceExcerpt(text) {
  const interesting = [
    /test cases:/i,
    /Status: FAILURE/i,
    /Write-Error:/i,
    /cargo fmt --check/i,
    /Diff in /i,
    /Process completed with exit code/i,
    /Node 20 is being deprecated/i,
    /Node\.js 20 is deprecated/i
  ];
  return text
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter((line) => interesting.some((pattern) => pattern.test(line)))
    .slice(0, 8)
    .map(sanitizeLine)
    .join("\n");
}

function actionRefs(text) {
  return unique([...text.matchAll(/[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+@v?\d+/g)].map((match) => match[0]));
}

function failureCodes(text) {
  const codes = [];
  if (/cargo fmt --check/i.test(text) && /Diff in /i.test(text) && /exit code 1/i.test(text)) {
    codes.push("rust_format_failure");
  }
  if (/\[doctest\]\s+test cases:.*\|\s*[1-9]\d*\s+failed/i.test(text)) {
    codes.push("test_gate_failed");
  }
  if (codes.length === 0 && /##\[error\].*exit code 1/i.test(text)) {
    codes.push("ci_step_failed");
  }
  return codes;
}

function warningCodes(text) {
  const codes = [];
  if (/Node 20 is being deprecated/i.test(text)) {
    codes.push("node_runtime_migration_warning");
  }
  if (/Node\.js 20 is deprecated.*forced to run on Node\.js 24/i.test(text)) {
    codes.push("javascript_action_node20_forced_node24");
  }
  return codes;
}

function remediationKind(failures, warnings) {
  if (failures.includes("rust_format_failure")) return "format_source";
  if (failures.includes("test_gate_failed")) return "fix_failing_tests";
  if (failures.length > 0) return "inspect_failed_step";
  if (warnings.length > 0) return "workflow_runtime_migration";
  return "none";
}

function routesFor(failures, warnings) {
  const routes = [];
  if (failures.includes("rust_format_failure")) routes.push("local.format", "ci.rerun");
  if (failures.includes("test_gate_failed")) routes.push("crucible.assess", "local.test.slice");
  if (failures.includes("ci_step_failed")) routes.push("ci.logs.inspect", "forum.route");
  if (warnings.length > 0) routes.push("telos.ci.doctor", "telos.compatibility.doctor");
  return unique(routes);
}

export function classifyLogText(logText, metadata = {}) {
  const failures = failureCodes(logText);
  const warnings = warningCodes(logText);
  const blocking = failures.length > 0;
  return {
    id: metadata.id ?? `${metadata.repo ?? "unknown"}#${metadata.run_id ?? "unknown"}`,
    repo: metadata.repo ?? "unknown",
    workflow: metadata.workflow ?? "unknown",
    run_id: metadata.run_id ?? null,
    run_url: metadata.run_url ?? null,
    log_hash: sha256(logText),
    evidence_excerpt: evidenceExcerpt(logText),
    blocking_failure: blocking,
    verdict: blocking ? "DRIFT" : "MATCH",
    failure_codes: failures,
    warning_codes: warnings,
    action_refs: actionRefs(logText),
    remediation_kind: remediationKind(failures, warnings),
    route_to: routesFor(failures, warnings)
  };
}

function assembleTriagePacket(cases, options = {}) {
  const failureCodes = unique(cases.flatMap((item) => item.failure_codes));
  const warningCodes = unique(cases.flatMap((item) => item.warning_codes));
  const blockingCount = cases.filter((item) => item.blocking_failure).length;
  const runtimeWarningCount = cases.filter((item) => item.warning_codes.length > 0).length;
  const runtimeVerdict = runtimeWarningCount > 0 ? "DRIFT" : "MATCH";
  const resultVerdict = blockingCount > 0 ? "DRIFT" : "MATCH";
  return {
    schema: "project-telos.ci-triage/v1",
    tool: "telos.ci.triage",
    generated_at: options.generatedAt ?? new Date().toISOString(),
    purpose: "Separate fatal GitHub Actions gate failures from Node runtime migration warnings before routing remediation.",
    aggregate: {
      case_count: cases.length,
      blocking_failure_count: blockingCount,
      runtime_warning_count: runtimeWarningCount,
      ci_result_verdict: resultVerdict,
      runtime_migration_verdict: runtimeVerdict,
      verdict: blockingCount > 0 || runtimeWarningCount > 0 ? "DRIFT" : "MATCH",
      failure_codes: failureCodes,
      warning_codes: warningCodes
    },
    privacy_boundary: {
      raw_logs_included: false,
      redacted_evidence_excerpts_included: true,
      tokens_or_secrets_included: false,
      absolute_private_paths_included: false,
      github_writes_performed: false,
      workflow_mutation_performed: false
    },
    failure_code_contract: [
      { code: "test_gate_failed", meaning: "A test runner reported failed tests; route to focused reproduction and Crucible assessment." },
      { code: "rust_format_failure", meaning: "Rust formatting gate failed; run cargo fmt and re-run the lint slice." },
      { code: "ci_step_failed", meaning: "A step exited non-zero without a more specific classifier; inspect logs before patching." },
      { code: "node_runtime_migration_warning", meaning: "GitHub warned that Node 20 actions are being migrated; not a fatal CI failure." },
      { code: "javascript_action_node20_forced_node24", meaning: "An action targets Node 20 and was forced onto Node 24; update action majors when possible." }
    ],
    cases
  };
}

export function buildTriagePacket(options = {}) {
  const cases = (options.cases ?? []).map((item) => classifyLogText(item.log_text ?? "", item));
  return assembleTriagePacket(cases, options);
}

export function parseGithubRunRef(value) {
  const match = /^([A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+)[#:](\d+)$/.exec(value ?? "");
  if (!match) {
    throw new Error("Expected --gh-run value like owner/repo#123456789 or owner/repo:123456789.");
  }
  return { repo: match[1], runId: match[2] };
}

function runGh(args) {
  return execFileSync("gh", args, {
    encoding: "utf8",
    maxBuffer: 16 * 1024 * 1024
  });
}

export function caseFromGithubRun(ref, gh = runGh) {
  const { repo, runId } = parseGithubRunRef(ref);
  const metadata = JSON.parse(gh([
    "run",
    "view",
    runId,
    "--repo",
    repo,
    "--json",
    "databaseId,workflowName,url,conclusion,status,headSha"
  ]));
  const logText = gh(["run", "view", runId, "--repo", repo, "--log"]);
  return {
    ...classifyLogText(logText, {
      repo,
      run_id: runId,
      run_url: metadata.url,
      workflow: metadata.workflowName
    }),
    github_status: metadata.status,
    github_conclusion: metadata.conclusion,
    head_sha: metadata.headSha
  };
}

export function summary(value) {
  return [
    "Telos CI Triage",
    `schema       ${value.schema}`,
    `tool         ${value.tool}`,
    `cases        ${value.aggregate.case_count}`,
    `blocking     ${value.aggregate.blocking_failure_count}`,
    `runtime      ${value.aggregate.runtime_migration_verdict}`,
    `result       ${value.aggregate.ci_result_verdict}`,
    `verdict      ${value.aggregate.verdict}`,
    "next         node demo/ci-triage.mjs"
  ].join("\n") + "\n";
}

function optionValue(args, name) {
  const index = args.indexOf(name);
  const inline = args.find((arg) => arg.startsWith(`${name}=`));
  if (inline) return inline.slice(name.length + 1);
  return index === -1 ? null : args[index + 1];
}

function main() {
  const args = process.argv.slice(2);
  const ghRun = optionValue(args, "--gh-run");
  const packet = ghRun
    ? assembleTriagePacket([caseFromGithubRun(ghRun)])
    : buildTriagePacket((() => {
      const inputPath = optionValue(args, "--input") ?? defaultInput;
      const input = JSON.parse(readFileSync(inputPath, "utf8"));
      return { ...input, generatedAt: input.generated_at };
    })());
  process.stdout.write(args.includes("--summary") ? summary(packet) : `${JSON.stringify(packet, null, 2)}\n`);
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  main();
}
