import test from "node:test";
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import {
  BROWSER_EVIDENCE_SCHEMA,
  sha256Hex,
  digestRef,
  makeBrowserEvidencePacket,
  makeUnavailableSummary,
  validateBrowserEvidencePacket,
} from "./native-control/evidence.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));

test("sha256Hex and digestRef produce stable sha256 refs", () => {
  assert.equal(
    sha256Hex("telos"),
    "c987adc38cb5536554f70a5d0db6900a59d4d4a32e84ba48f75b3301a939c6ae",
  );
  assert.equal(
    digestRef("url", "https://example.com"),
    "url:sha256:100680ad546ce6a577f42f52df33b4cfdca756859e664b8d7de329b150d09ce9",
  );
});

test("makeUnavailableSummary fails closed for missing collectors", () => {
  const summary = makeUnavailableSummary("network", "collector-not-attached");
  assert.equal(summary.kind, "network");
  assert.equal(summary.verdict, "UNVERIFIABLE");
  assert.equal(summary.failure_code, "network_capture_unavailable");
  assert.equal(summary.reason, "collector-not-attached");
});

test("makeBrowserEvidencePacket builds the v1 packet without raw DOM", () => {
  const packet = makeBrowserEvidencePacket({
    mode: "research-capture",
    action: { kind: "browser.navigate", argsHash: digestRef("args", "nav") },
    sessionRef: "browser-session:test",
    actionReceiptRef: "receipt:test",
    before: {
      url: "https://example.com",
      title: "Before",
      text: "before text",
      domArtifactRef: "artifact:before-dom",
      screenshotRef: "artifact:before-png",
    },
    after: {
      url: "https://example.com/after",
      title: "After",
      text: "after text",
      domArtifactRef: "artifact:after-dom",
      screenshotRef: "artifact:after-png",
    },
    artifactHashes: [{ ref: "artifact:after-dom", hash: digestRef("sha256", "dom") }],
    networkSummary: makeUnavailableSummary("network", "collector-not-attached"),
    consoleSummary: makeUnavailableSummary("console", "collector-not-attached"),
    sideEffect: { class: "read", external_write: false, reversible: true },
    verification: { verdict: "MATCH", ref: "crucible:packet-shape" },
    clock: () => "2026-07-01T00:00:00.000Z",
  });

  assert.equal(packet.schema, BROWSER_EVIDENCE_SCHEMA);
  assert.equal(packet.mode, "research-capture");
  assert.equal(packet.before.url_digest, digestRef("url", "https://example.com"));
  assert.equal(packet.after.text_digest, digestRef("text", "after text"));
  assert.equal(packet.network_summary.verdict, "UNVERIFIABLE");
  assert.equal(packet.console_summary.failure_code, "console_capture_unavailable");
  assert.equal(Object.hasOwn(packet.after, "raw_dom"), false);
  assert.deepEqual(validateBrowserEvidencePacket(packet), { ok: true, failures: [] });
});

test("validateBrowserEvidencePacket reports typed failures", () => {
  const result = validateBrowserEvidencePacket({ schema: BROWSER_EVIDENCE_SCHEMA, mode: "work-actuate" });
  assert.equal(result.ok, false);
  assert.ok(result.failures.includes("missing_action"));
  assert.ok(result.failures.includes("missing_after"));
  assert.ok(result.failures.includes("missing_verification"));
});

test("browser-evidence CLI emits the fixture contract", () => {
  const cli = spawnSync(process.execPath, [path.join(here, "browser-evidence.mjs"), "--fixture"], {
    cwd: path.resolve(here, ".."),
    encoding: "utf8",
  });
  assert.equal(cli.status, 0, cli.stderr || cli.stdout);
  const packet = JSON.parse(cli.stdout);
  assert.equal(packet.schema, BROWSER_EVIDENCE_SCHEMA);
  assert.equal(packet.tool, "telos.browser.evidence");
  assert.equal(packet.mode, "research-capture");
  assert.equal(validateBrowserEvidencePacket(packet).ok, true);
});

test("browser evidence smoke receipt names pipeline consumers", () => {
  const smoke = JSON.parse(readFileSync(path.join(here, "research", "browser-evidence-smoke.json"), "utf8"));

  assert.equal(smoke.schema, "project-telos.browser-evidence-smoke/v1");
  assert.equal(smoke.source_packet, "demo/integrations/browser-evidence.json");
  assert.equal(smoke.verdict, "MATCH");
  assert.ok(smoke.pipeline_consumers.includes("gather.browser-evidence"));
  assert.ok(smoke.pipeline_consumers.includes("index.browser_evidence_refs"));
  assert.ok(smoke.pipeline_consumers.includes("forum.project-telos-route"));
  assert.ok(smoke.pipeline_consumers.includes("crucible.verify_browser_evidence"));
  assert.ok(smoke.pipeline_consumers.includes("learn.evidenceRef"));
  assert.ok(smoke.pipeline_consumers.includes("emet.anchor-recipe"));
  assert.ok(smoke.pipeline_consumers.includes("buildlang.editor-fixture"));
  assert.equal(smoke.council_route.local_first, true);
  assert.ok(smoke.council_route.route_surfaces.includes("index.context-envelope"));
  assert.ok(smoke.council_route.route_surfaces.includes("forum.project-telos-route"));
  assert.equal(smoke.overhead_metrics.default_model_payload, "refs-only");
  assert.ok(smoke.overhead_metrics.tracked.includes("council_calls"));
  assert.ok(smoke.overhead_metrics.tracked.includes("tokens_spent"));
});
