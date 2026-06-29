import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";

const convention = JSON.parse(
  readFileSync(new URL("./integrations/context-envelope-conventions.json", import.meta.url), "utf8")
);

const rawPayloadKeys = new Set([
  "raw_args",
  "raw_context",
  "raw_memory",
  "raw_prompt",
  "raw_result",
  "raw_source_body",
  "raw_tool_output",
  "transcript_text"
]);

const failurePrecedence = [
  "raw_context_leak",
  "stale_context",
  "lossy_summary",
  "missing_source_ref",
  "unexpanded_required_ref",
  "unjoinable_receipt",
  "readability_regression",
  "quality_gate_missing",
  "budget_exceeded",
  "relevance_accounting_missing",
  "missing_relevance",
  "over_selection",
  "unjoinable_relevance"
];

const driftCodes = new Set(["budget_exceeded", "over_selection", "readability_regression"]);

export function stableStringify(value) {
  if (Array.isArray(value)) {
    return `[${value.map(stableStringify).join(",")}]`;
  }
  if (value && typeof value === "object") {
    return `{${Object.keys(value)
      .sort()
      .map((key) => `${JSON.stringify(key)}:${stableStringify(value[key])}`)
      .join(",")}}`;
  }
  return JSON.stringify(value);
}

export function sha256(value) {
  return `sha256:${createHash("sha256").update(stableStringify(value)).digest("hex")}`;
}

export function estimateTokens(value) {
  const text = typeof value === "string" ? value : stableStringify(value);
  if (!text.length) return 0;
  return Math.ceil(text.length / 4);
}

function asArray(value) {
  return Array.isArray(value) ? value : [];
}

function hasSha256(value) {
  return /^sha256:[a-f0-9]{64}$/.test(String(value ?? ""));
}

function addFailure(failures, code, path, detail) {
  failures.push({ code, path, detail });
}

function scanForRawPayloads(value, failures, path = "$") {
  if (!value || typeof value !== "object") return;
  if (Array.isArray(value)) {
    value.forEach((item, index) => scanForRawPayloads(item, failures, `${path}[${index}]`));
    return;
  }
  for (const [key, child] of Object.entries(value)) {
    const childPath = `${path}.${key}`;
    if (rawPayloadKeys.has(key)) {
      addFailure(failures, "raw_context_leak", childPath, "raw payload field is not allowed");
    }
    scanForRawPayloads(child, failures, childPath);
  }
}

function expectedVerdict(failureCode) {
  if (!failureCode) return "MATCH";
  return driftCodes.has(failureCode) ? "DRIFT" : "UNVERIFIABLE";
}

function firstFailureCode(failures) {
  const codes = new Set(failures.map((failure) => failure.code));
  return failurePrecedence.find((code) => codes.has(code)) ?? failures[0]?.code ?? null;
}

export function validateContextPack(pack) {
  const failures = [];
  scanForRawPayloads(pack, failures);

  const sourceRefs = new Map();
  for (const [index, ref] of asArray(pack.source_refs).entries()) {
    if (!ref?.id || !hasSha256(ref.content_hash)) {
      addFailure(failures, "missing_source_ref", `$.source_refs[${index}]`, "source ref id and hash are required");
      continue;
    }
    if (ref.current_hash && ref.current_hash !== ref.content_hash) {
      addFailure(failures, "stale_context", `$.source_refs[${index}].current_hash`, "current hash no longer matches content hash");
    }
    if (!ref.expansion_command) {
      addFailure(failures, "unexpanded_required_ref", `$.source_refs[${index}].expansion_command`, "expansion command is required");
    }
    sourceRefs.set(ref.id, ref);
  }

  for (const [index, claim] of asArray(pack.summary?.claims).entries()) {
    const refIds = asArray(claim.source_ref_ids);
    if (!refIds.length) {
      addFailure(failures, "lossy_summary", `$.summary.claims[${index}]`, "claim has no source refs");
    }
    for (const refId of refIds) {
      if (!sourceRefs.has(refId)) {
        addFailure(failures, "missing_source_ref", `$.summary.claims[${index}].source_ref_ids`, `unknown source ref ${refId}`);
      }
    }
  }

  for (const [index, receipt] of asArray(pack.receipt_chain).entries()) {
    if (!receipt?.tool || !hasSha256(receipt.receipt_hash)) {
      addFailure(failures, "unjoinable_receipt", `$.receipt_chain[${index}]`, "receipt requires tool and sha256 hash");
    }
  }

  const gates = pack.quality_gates ?? {};
  if (!gates.readability || !gates.test_evidence) {
    addFailure(failures, "quality_gate_missing", "$.quality_gates", "readability and test evidence gates are required");
  }
  if (gates.readability === "DRIFT") {
    addFailure(failures, "readability_regression", "$.quality_gates.readability", "readability gate drifted");
  }

  const tokenEstimate = estimateTokens({
    summary: pack.summary,
    source_refs: pack.source_refs,
    context_load: pack.context_load,
    context_relevance: pack.context_relevance
  });
  const targetPacketTokens = Number(pack.context_budget?.target_packet_tokens ?? 0);
  if (!Number.isFinite(targetPacketTokens) || targetPacketTokens <= 0 || tokenEstimate > targetPacketTokens) {
    addFailure(failures, "budget_exceeded", "$.context_budget.target_packet_tokens", "packet exceeds target token budget");
  }

  const loadedInputs = asArray(pack.context_load?.loaded_inputs);
  const deliveredInputs = loadedInputs.filter((input) => input.delivery_status === "delivered");
  const deliveredById = new Map(deliveredInputs.map((input) => [input.input_id, input]));
  const relevanceRefs = asArray(pack.context_relevance?.input_refs);
  if (pack.context_load?.claims_usefulness === true && !pack.context_relevance) {
    addFailure(failures, "missing_relevance", "$.context_relevance", "usefulness claims require a relevance event");
  }
  if (relevanceRefs.length > deliveredInputs.length) {
    addFailure(failures, "over_selection", "$.context_relevance.input_refs", "relevance labels exceed delivered inputs");
  }
  for (const [index, ref] of relevanceRefs.entries()) {
    const loaded = deliveredById.get(ref.input_id);
    if (!loaded || loaded.delivered_hash !== ref.delivered_hash) {
      addFailure(failures, "unjoinable_relevance", `$.context_relevance.input_refs[${index}]`, "relevance ref does not join to delivered input");
    }
  }

  const relevanceCounts = pack.context_relevance?.counts;
  if (relevanceCounts) {
    const total =
      Number(relevanceCounts.decisive ?? 0) +
      Number(relevanceCounts.supporting ?? 0) +
      Number(relevanceCounts.unused ?? 0) +
      Number(relevanceCounts.unknown ?? 0);
    if (total !== relevanceRefs.length) {
      addFailure(failures, "relevance_accounting_missing", "$.context_relevance.counts", "relevance counts do not match refs");
    }
  }

  const failureCode = firstFailureCode(failures);
  const validation = {
    schema: "project-telos.context-pack-validation/v1",
    verdict: expectedVerdict(failureCode),
    failure_code: failureCode,
    failures,
    token_estimate: tokenEstimate,
    delivered_count: deliveredInputs.length,
    relevance_count: relevanceRefs.length
  };
  return {
    ...validation,
    receipt_hash: sha256(validation)
  };
}

export function buildDemoContextPack() {
  const fixture = convention.conformance_fixture;
  const happy = fixture.happy_path;
  const relevance = fixture.context_relevance;
  const pack = {
    schema: "project-telos.context-pack/v1",
    tool: "telos.context.pack",
    generated_at: "2026-06-28T00:00:00.000Z",
    purpose: "Runnable, budgeted, lossless-by-reference context packet for large-codebase agent handoffs.",
    envelope_contract: "project-telos.context-envelope/v1",
    workspace: happy.workspace,
    context_budget: {
      max_input_tokens: happy.context_budget.max_input_tokens,
      target_packet_tokens: happy.context_budget.target_packet_tokens,
      reserved_response_tokens: happy.context_budget.reserved_response_tokens,
      lossless_by_ref: happy.compression.lossless_by_ref,
      hidden_payloads_used: happy.compression.hidden_payloads_used
    },
    compression: happy.compression,
    source_refs: happy.source_refs,
    summary: happy.summary,
    context_load: {
      event_type: relevance.receipt_contract.load_receipt.event_type,
      decision_claim: relevance.receipt_contract.load_receipt.decisionClaim,
      claims_usefulness: relevance.receipt_contract.load_receipt.claims_usefulness,
      raw_payload_required: relevance.receipt_contract.load_receipt.raw_payload_required,
      selected_count: relevance.selection.selected_count,
      delivered_count: relevance.selection.delivered_count,
      suppressed_count: relevance.selection.suppressed_count,
      loaded_inputs: relevance.loaded_inputs,
      suppressed_inputs: relevance.suppressed_inputs
    },
    context_relevance: {
      event_type: relevance.receipt_contract.relevance_receipt.event_type,
      optional: relevance.receipt_contract.relevance_receipt.optional,
      raw_payload_required: relevance.receipt_contract.relevance_receipt.raw_payload_required,
      required_join_fields: relevance.receipt_contract.relevance_receipt.required_join_fields,
      input_refs: relevance.relevance.input_refs,
      counts: {
        decisive: relevance.relevance.decisive_count,
        supporting: relevance.relevance.supporting_count,
        unused: relevance.relevance.unused_count,
        unknown: relevance.relevance.unknown_count
      }
    },
    receipt_chain: happy.receipt_chain,
    quality_gates: happy.quality_gates,
    next_actions: [
      "index.context.envelope: replace fixture source refs with live workspace refs for the selected task.",
      "forum.ledger.summary: write one bounded action against this packet before the next fresh-context turn.",
      "crucible.assess: verify summary claims and failure codes before treating the packet as enterprise evidence."
    ]
  };
  const validation = validateContextPack(pack);
  const withValidation = {
    ...pack,
    context_budget: {
      ...pack.context_budget,
      estimated_packet_tokens: validation.token_estimate
    },
    validation
  };
  return {
    ...withValidation,
    context_pack_hash: sha256(withValidation)
  };
}

function main() {
  process.stdout.write(`${JSON.stringify(buildDemoContextPack(), null, 2)}\n`);
}

if (process.argv[1] && import.meta.url.endsWith(process.argv[1].replace(/\\/g, "/"))) {
  main();
}
