import { createHash } from "node:crypto";
import { existsSync, readFileSync, statSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const defaultRoot = path.resolve(here, "..", "..");
const defaultFlagships = ["gather", "crucible", "index", "forum", "telos"];

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function sha256(text) {
  return `sha256:${createHash("sha256").update(text).digest("hex")}`;
}

function readText(root, id, relativePath) {
  const fullPath = path.join(root, id, relativePath);
  if (!existsSync(fullPath) || !statSync(fullPath).isFile()) {
    return null;
  }
  const text = readFileSync(fullPath, "utf8");
  return { relative_path: relativePath.replace(/\\/g, "/"), hash: sha256(text), text };
}

function fileExists(root, id, relativePath) {
  const fullPath = path.join(root, id, relativePath);
  return existsSync(fullPath) && statSync(fullPath).isFile();
}

function readmeSignals(text) {
  return {
    hero_image: /docs\/brand\/[^)\s"']*hero\.png|<img\b/i.test(text),
    project_telos_nav: /Project Telos/i.test(text)
      && /github\.com\/HarperZ9\/gather/i.test(text)
      && /github\.com\/HarperZ9\/crucible/i.test(text)
      && /github\.com\/HarperZ9\/index/i.test(text)
      && /github\.com\/HarperZ9\/forum/i.test(text)
      && /github\.com\/HarperZ9\/telos/i.test(text),
    ci_badge: /actions\/workflows\/ci\.ya?ml\/badge\.svg/i.test(text),
    version_badge: /badge\/version-|version:/i.test(text),
    license_badge: /badge\/license-|license:/i.test(text),
    operator_surface: /operator surface/i.test(text),
    current_status: /current floor|current status/i.test(text),
    cli_mcp_terms: /\bCLI\b/i.test(text) && /\bMCP\b/i.test(text)
  };
}

function changelogSignals(text) {
  return {
    unreleased_section: /^##\s+Unreleased\b/im.test(text),
    presentation_housekeeping: /presentation|operator-surface|operator surface/i.test(text),
    mcp_surface: /\bMCP\b/i.test(text)
  };
}

function signalFailures(signals, mapping) {
  return Object.entries(mapping)
    .filter(([key]) => !signals[key])
    .map(([, code]) => code);
}

function analyzeFlagship(root, id) {
  const repoRoot = path.join(root, id);
  if (!existsSync(repoRoot) || !statSync(repoRoot).isDirectory()) {
    return {
      id,
      repo: { present: false },
      files: {
        readme: { present: false },
        changelog: { present: false },
        brand: { assets: [] }
      },
      presentation: {
        verdict: "UNVERIFIABLE",
        failure_codes: ["flagship_repo_unjoinable"]
      }
    };
  }

  const readme = readText(root, id, "README.md");
  const changelog = readText(root, id, "CHANGELOG.md");
  const brandRelative = [
    `docs/brand/${id}-hero.png`,
    `docs/brand/${id}-hero.svg`,
    `docs/brand/${id}-mark.svg`,
    "docs/brand/README.md"
  ];
  const brandAssets = brandRelative.map((relativePath) => ({
    relative_path: relativePath,
    present: fileExists(root, id, relativePath)
  }));

  const failures = [];
  const readmePacket = readme
    ? {
        present: true,
        relative_path: readme.relative_path,
        hash: readme.hash,
        signals: readmeSignals(readme.text)
      }
    : { present: false };
  if (!readme) {
    failures.push("readme_missing");
  } else {
    failures.push(...signalFailures(readmePacket.signals, {
      project_telos_nav: "project_telos_nav_missing",
      hero_image: "readme_hero_missing",
      ci_badge: "ci_badge_missing",
      version_badge: "version_badge_missing",
      license_badge: "license_badge_missing",
      operator_surface: "operator_surface_missing",
      current_status: "current_status_missing",
      cli_mcp_terms: "cli_mcp_terms_missing"
    }));
  }

  const changelogPacket = changelog
    ? {
        present: true,
        relative_path: changelog.relative_path,
        hash: changelog.hash,
        signals: changelogSignals(changelog.text)
      }
    : { present: false };
  if (!changelog) {
    failures.push("changelog_missing");
  } else {
    failures.push(...signalFailures(changelogPacket.signals, {
      unreleased_section: "changelog_freshness_missing",
      presentation_housekeeping: "changelog_freshness_missing",
      mcp_surface: "changelog_freshness_missing"
    }));
  }

  if (brandAssets.some((asset) => !asset.present)) {
    failures.push("brand_artifact_missing");
  }

  const failureCodes = unique(failures);
  return {
    id,
    repo: { present: true },
    files: {
      readme: readmePacket,
      changelog: changelogPacket,
      brand: { assets: brandAssets }
    },
    presentation: {
      verdict: failureCodes.length === 0 ? "MATCH" : "DRIFT",
      failure_codes: failureCodes
    }
  };
}

function aggregateVerdict(verdicts) {
  if (verdicts.some((verdict) => verdict === "DRIFT")) {
    return "DRIFT";
  }
  if (verdicts.every((verdict) => verdict === "MATCH")) {
    return "MATCH";
  }
  return "UNVERIFIABLE";
}

export function scanPresentationSurfaces(root = defaultRoot, options = {}) {
  const flagships = options.flagships ?? defaultFlagships;
  const scanned = flagships.map((id) => analyzeFlagship(root, id));
  const verdicts = scanned.map((flagship) => flagship.presentation.verdict);
  const failureCodes = unique(scanned.flatMap((flagship) => flagship.presentation.failure_codes));
  return {
    schema: "project-telos.presentation-doctor/v1",
    tool: "telos.presentation.doctor",
    generated_at: options.generatedAt ?? new Date().toISOString(),
    aggregate: {
      flagship_count: scanned.length,
      readme_count: scanned.filter((flagship) => flagship.files.readme.present).length,
      changelog_count: scanned.filter((flagship) => flagship.files.changelog.present).length,
      brand_asset_count: scanned.reduce(
        (count, flagship) => count + flagship.files.brand.assets.filter((asset) => asset.present).length,
        0
      ),
      verdict: aggregateVerdict(verdicts),
      failure_codes: failureCodes
    },
    privacy_boundary: {
      absolute_paths_included: false,
      raw_document_bodies_included: false,
      private_paths_included: false,
      github_queries_performed: false,
      filesystem_writes_performed: false
    },
    requirements: [
      "README.md with shared Project Telos navigation, hero art, CI/version/license badges, operator surface, current status, and CLI/MCP terms",
      "CHANGELOG.md with an Unreleased section and current presentation/operator/MCP notes",
      "docs/brand hero PNG, hero SVG, mark SVG, and brand README present for each flagship"
    ],
    flagships: scanned
  };
}

export function summary(value = scanPresentationSurfaces()) {
  const lines = [
    "Telos Presentation Doctor",
    `schema       ${value.schema}`,
    `tool         ${value.tool}`,
    `flagships    ${value.aggregate.flagship_count}`,
    `readmes      ${value.aggregate.readme_count}`,
    `changelogs   ${value.aggregate.changelog_count}`,
    `brand assets ${value.aggregate.brand_asset_count}`,
    `verdict      ${value.aggregate.verdict}`,
    "next         node demo/presentation-doctor.mjs"
  ];
  return `${lines.join("\n")}\n`;
}

function optionValue(args, name) {
  const index = args.indexOf(name);
  const inline = args.find((arg) => arg.startsWith(`${name}=`));
  if (inline) {
    return inline.slice(name.length + 1);
  }
  if (index !== -1) {
    return args[index + 1];
  }
  return null;
}

function main() {
  const args = process.argv.slice(2);
  const root = optionValue(args, "--scan-root") ?? defaultRoot;
  const flagshipsArg = optionValue(args, "--flagships");
  const flagships = flagshipsArg
    ? flagshipsArg.split(",").map((item) => item.trim()).filter(Boolean)
    : undefined;
  const packet = scanPresentationSurfaces(root, { flagships });
  if (args.includes("--summary")) {
    process.stdout.write(summary(packet));
  } else {
    process.stdout.write(`${JSON.stringify(packet, null, 2)}\n`);
  }
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  main();
}
