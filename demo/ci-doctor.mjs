import { existsSync, readdirSync, readFileSync, statSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const doctor = JSON.parse(
  readFileSync(new URL("./integrations/ci-doctor.json", import.meta.url), "utf8")
);

const defaultFlagships = ["gather", "crucible", "index", "forum", "telos"];

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function workflowFiles(root, flagship) {
  const workflowRoot = path.join(root, flagship, ".github", "workflows");
  if (!existsSync(workflowRoot) || !statSync(workflowRoot).isDirectory()) {
    return [];
  }
  return readdirSync(workflowRoot, { withFileTypes: true })
    .filter((entry) => entry.isFile() && /\.(ya?ml)$/i.test(entry.name))
    .map((entry) => {
      const relativePath = `.github/workflows/${entry.name}`;
      return {
        relativePath,
        text: readFileSync(path.join(workflowRoot, entry.name), "utf8")
      };
    })
    .sort((a, b) => a.relativePath.localeCompare(b.relativePath));
}

function extractUses(text) {
  const found = [];
  const pattern = /uses:\s*["']?([^@\s"']+)@([^#\s"']+)/g;
  for (const match of text.matchAll(pattern)) {
    found.push({ action: match[1], ref: match[2] });
  }
  return found;
}

function firstMajor(uses, action) {
  const found = uses.find((entry) => entry.action === action);
  if (!found) {
    return null;
  }
  const major = found.ref.match(/^v?\d+/)?.[0] ?? found.ref;
  return major.startsWith("v") ? major : `v${major}`;
}

function extractScalar(texts, key) {
  const pattern = new RegExp(`^\\s*${key}:\\s*(.+?)\\s*$`);
  const values = [];
  for (const text of texts) {
    for (const line of text.split(/\r?\n/)) {
      const match = line.match(pattern);
      if (!match) {
        continue;
      }
      const raw = match[1].split("#")[0].trim();
      if (!raw || raw.includes("${{")) {
        continue;
      }
      if (raw.startsWith("[") && raw.endsWith("]")) {
        const arrayValues = [...raw.matchAll(/["']([^"']+)["']/g)].map((item) => item[1]);
        values.push(...arrayValues);
        continue;
      }
      values.push(raw.replace(/^["']|["']$/g, ""));
    }
  }
  return unique(values.filter((value) => /^\d+(?:\.\d+)*$/.test(value)));
}

function analyzeCompatibility(files) {
  if (files.length === 0) {
    return {
      force_node24_flag: false,
      checkout_major: null,
      setup_python_major: null,
      setup_node_major: null,
      node_version: null,
      python_versions: [],
      artifact_actions: [],
      verdict: "UNVERIFIABLE",
      failure_codes: ["workflow_evidence_unjoinable"]
    };
  }

  const texts = files.map((file) => file.text);
  const uses = texts.flatMap(extractUses);
  const artifactActions = uses
    .filter((entry) => entry.action === "actions/upload-artifact" || entry.action === "actions/download-artifact")
    .map((entry) => `${entry.action}@${firstMajor([entry], entry.action)}`);
  const nodeVersions = extractScalar(texts, "node-version");
  const pythonVersions = extractScalar(texts, "python-version");
  const forceNode24 = files.length > 0 && texts.every((text) => text.includes("FORCE_JAVASCRIPT_ACTIONS_TO_NODE24"));
  const setupNodeMajor = firstMajor(uses, "actions/setup-node");
  const setupPythonMajor = firstMajor(uses, "actions/setup-python");
  const checkoutMajor = firstMajor(uses, "actions/checkout");
  const problems = [];

  if (!forceNode24) {
    problems.push("node_runtime_drift");
  }
  if (checkoutMajor && checkoutMajor !== "v7") {
    problems.push("action_major_drift");
  }
  if (setupNodeMajor && (setupNodeMajor !== "v6" || !nodeVersions.includes("24"))) {
    problems.push("node_runtime_drift");
  }
  if (setupPythonMajor && setupPythonMajor !== "v6") {
    problems.push("action_major_drift");
  }
  for (const action of artifactActions) {
    const major = action.match(/@(.+)$/)?.[1];
    if (major && Number(major.replace(/^v/, "")) < 7) {
      problems.push("action_major_drift");
    }
  }

  return {
    force_node24_flag: forceNode24,
    checkout_major: checkoutMajor,
    setup_python_major: setupPythonMajor,
    setup_node_major: setupNodeMajor,
    node_version: nodeVersions[0] ?? null,
    python_versions: pythonVersions,
    artifact_actions: unique(artifactActions),
    verdict: problems.length === 0 ? "MATCH" : "DRIFT",
    failure_codes: unique(problems)
  };
}

export function scanLocalWorkflows(root, options = {}) {
  const flagships = options.flagships ?? defaultFlagships;
  const scanned = flagships.map((id) => {
    const files = workflowFiles(root, id);
    return {
      id,
      workflow_files: files.map((file) => file.relativePath),
      compatibility: analyzeCompatibility(files)
    };
  });
  const workflowCount = scanned.reduce((count, flagship) => count + flagship.workflow_files.length, 0);
  const verdicts = scanned.map((flagship) => flagship.compatibility.verdict);
  const failureCodes = unique(scanned.flatMap((flagship) => flagship.compatibility.failure_codes));
  const node24 = verdicts.every((verdict) => verdict === "MATCH")
    ? "MATCH"
    : verdicts.some((verdict) => verdict === "DRIFT")
      ? "DRIFT"
      : "UNVERIFIABLE";

  return {
    schema: "project-telos.ci-doctor-workflow-observation/v1",
    tool: "telos.ci.doctor",
    generated_at: options.generatedAt ?? new Date().toISOString(),
    aggregate: {
      flagship_count: scanned.length,
      workflow_count: workflowCount,
      node24_compatibility: node24,
      verdict: node24,
      failure_codes: failureCodes
    },
    privacy_boundary: {
      absolute_paths_included: false,
      workflow_bodies_included: false,
      github_queries_performed: false,
      filesystem_writes_performed: false
    },
    flagships: scanned
  };
}

export function summary(value = doctor) {
  const aggregate = value.aggregate;
  const latestCi = "latest_ci_failures" in aggregate
    ? aggregate.latest_ci_failures === 0 ? "MATCH" : "DRIFT"
    : "UNVERIFIABLE";
  const lines = [
    "Telos CI Doctor",
    `schema       ${value.schema}`,
    `tool         ${value.tool}`,
    `flagships    ${aggregate.flagship_count}`,
    `workflows    ${aggregate.workflow_count}`,
    `latest CI    ${latestCi}`,
    `node24       ${aggregate.node24_compatibility}`,
    `verdict      ${aggregate.verdict}`,
    "next         node demo/ci-doctor.mjs"
  ];
  return `${lines.join("\n")}\n`;
}

function main() {
  const scanRootIndex = process.argv.indexOf("--scan-root");
  if (scanRootIndex >= 0) {
    const root = process.argv[scanRootIndex + 1];
    if (!root) {
      throw new Error("--scan-root requires a path");
    }
    const packet = scanLocalWorkflows(root);
    if (process.argv.includes("--summary")) {
      process.stdout.write(summary(packet));
    } else {
      process.stdout.write(`${JSON.stringify(packet, null, 2)}\n`);
    }
    return;
  }
  if (process.argv.includes("--summary")) {
    process.stdout.write(summary());
  } else {
    process.stdout.write(`${JSON.stringify(doctor, null, 2)}\n`);
  }
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  main();
}
