import { fileURLToPath } from "node:url";

import { hashStable } from "./measurement-utils.mjs";

const currentSourceLeads = [
  {
    id: "source-mcp",
    title: "Model Context Protocol",
    url: "https://modelcontextprotocol.io/docs/getting-started/intro",
    claim_scope: "provider-neutral tool and context connector layer"
  },
  {
    id: "source-openai-tools",
    title: "OpenAI API tools guide",
    url: "https://developers.openai.com/api/docs/guides/tools",
    claim_scope: "hosted frontier-model tool-use surface"
  },
  {
    id: "source-anthropic-tool-use",
    title: "Anthropic tool use overview",
    url: "https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview",
    claim_scope: "hosted frontier-model tool-use surface"
  },
  {
    id: "source-gemini-long-context",
    title: "Gemini long context",
    url: "https://ai.google.dev/gemini-api/docs/long-context",
    claim_scope: "long-context capability and retrieval/cost caveats"
  },
  {
    id: "source-hf-trl",
    title: "Hugging Face TRL",
    url: "https://huggingface.co/docs/trl/en/index",
    claim_scope: "public post-training and reinforcement-learning toolkit"
  },
  {
    id: "source-pytorch-fsdp",
    title: "PyTorch FSDP tutorial",
    url: "https://docs.pytorch.org/tutorials/intermediate/FSDP_tutorial.html",
    claim_scope: "public distributed-training primitive"
  },
  {
    id: "source-openai-evals",
    title: "OpenAI evals guide",
    url: "https://developers.openai.com/api/docs/guides/evals",
    claim_scope: "model and system evaluation as a product primitive"
  },
  {
    id: "source-nist-genai-profile",
    title: "NIST AI RMF Generative AI Profile",
    url: "https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence",
    claim_scope: "risk-management and governance reference"
  }
];

function sourceReceipt(source) {
  const withProvenance = {
    ...source,
    provenance: "public-official-or-primary-source",
    verified_on: "2026-06-29",
    claim_state: "SOURCE_LEAD"
  };
  return {
    ...withProvenance,
    receipt_hash: hashStable(withProvenance)
  };
}

export function evaluateDaemonCycle(cycle) {
  if (!cycle || cycle.crucible_verdict !== "MATCH") {
    return {
      decision_outcome: "block",
      verification_verdict: cycle?.crucible_verdict ?? "UNVERIFIABLE",
      failure_code: cycle?.crucible_verdict === "DRIFT" ? "eval_regression" : "verification_unverifiable"
    };
  }
  if ((cycle.objective_signals ?? []).some((signal) => signal.verdict === "DRIFT")) {
    return {
      decision_outcome: "require_review",
      verification_verdict: "DRIFT",
      failure_code: "objective_drift"
    };
  }
  return {
    decision_outcome: "allow",
    verification_verdict: "MATCH",
    failure_code: null
  };
}

export function validateModelFoundryPacket(packet) {
  if (!Array.isArray(packet.current_sources) || packet.current_sources.length === 0) {
    return { verdict: "UNVERIFIABLE", failure_code: "source_receipt_missing" };
  }
  if (!packet.contract || packet.contract.blind_self_training_allowed !== false) {
    return { verdict: "UNVERIFIABLE", failure_code: "unbounded_self_training" };
  }
  if (!packet.contract.self_modification_requires_crucible_match) {
    return { verdict: "UNVERIFIABLE", failure_code: "promotion_gate_missing" };
  }
  return { verdict: "MATCH", failure_code: null };
}

export function buildModelFoundryPacket() {
  const current_sources = currentSourceLeads.map(sourceReceipt);
  const packet = {
    schema: "project-telos.model-foundry/v1",
    tool: "telos.model.foundry",
    generated_at: "2026-06-29T00:00:00.000Z",
    purpose: "Define Project Telos as a model foundry: a bounded, provenance-native system for building, routing, evaluating, fine-tuning, and improving AI workflows without pretending independent infrastructure equals frontier-lab pretraining.",
    current_sources,
    contract: {
      frontier_pretraining_claimed: false,
      frontier_apis_allowed_as_components: true,
      local_open_weight_models_allowed: true,
      post_training_allowed: true,
      blind_self_training_allowed: false,
      self_modification_requires_crucible_match: true,
      promotion_requires_receipt_chain: true,
      raw_private_data_export_required: false,
      protocol_agnostic: true,
      mcp_native: true,
      io_surfaces: ["cli-json", "mcp-json-rpc", "ide", "tui", "app-bridge", "daemon"]
    },
    verdicts: ["MATCH", "DRIFT", "UNVERIFIABLE"],
    model_layers: [
      {
        id: "frontier-orchestration",
        role: "Route hard reasoning, code review, multimodal, and long-context work to hosted frontier APIs when policy, cost, and privacy permit.",
        boundary: "Use provider models as components; do not claim private frontier pretraining capability."
      },
      {
        id: "local-open-weight-runtime",
        role: "Run private, low-latency, offline, or cost-sensitive tasks on local and hosted open-weight models.",
        boundary: "Capability is measured by task receipts and evals, not model-card reputation."
      },
      {
        id: "post-training-lab",
        role: "Run SFT, LoRA/QLoRA, DPO/GRPO-style experiments, reward-model probes, and dataset distillation on feasible model sizes.",
        boundary: "Promotion requires held-out eval improvement and no regression in safety, readability, or provenance."
      },
      {
        id: "tool-use-os",
        role: "Expose Gather, Index, Forum, Crucible, Telos, shells, browsers, renderers, simulators, and research adapters through typed tools.",
        boundary: "Every tool action must join proposed action, admission, execution, result, and receipt records."
      },
      {
        id: "memory-and-context",
        role: "Compile large workspaces into lossless-by-reference context envelopes, source refs, ledgers, and replayable artifacts.",
        boundary: "Long context is a useful substrate, not a substitute for retrieval, receipts, and explicit omissions."
      },
      {
        id: "eval-and-safety",
        role: "Run task, tool-call, citation, prompt-injection, regression, and policy evals before promotion or unattended continuation.",
        boundary: "A failed or missing verifier result is UNVERIFIABLE, not success."
      }
    ],
    daemon: {
      mode: "bounded-self-improvement",
      cycle: [
        "gather fresh public or local evidence with source receipts",
        "index workspace and build lossless-by-reference context envelope",
        "forum route one bounded improvement proposal",
        "telos admit the proposed action with action_intent_id and policy decision",
        "execute one patch, experiment, eval, or research intake",
        "crucible assess outputs against tests, evals, receipts, and negative fixtures",
        "promote only MATCH results; block or require review on DRIFT or UNVERIFIABLE"
      ],
      example_cycle: {
        action_intent_id: "model-foundry-demo-cycle-001",
        proposed_action: "promote a model-routing or post-training improvement",
        source_refs: current_sources.map((source) => source.id),
        crucible_verdict: "MATCH",
        objective_signals: []
      },
      ceilings: {
        max_actions_per_cycle: 1,
        requires_context_envelope: true,
        requires_action_receipt: true,
        requires_eval_delta: true,
        requires_human_review_for_external_side_effects: true
      }
    },
    flagship_bindings: {
      gather: [
        "fresh public/primary source intake",
        "dataset provenance, license, and dedup receipts",
        "research packet harvesting without raw private payload export"
      ],
      index: [
        "lossless-by-reference context envelopes",
        "workspace, symbol, doc, and dependency maps",
        "freshness and source-ref hashes for daemon continuation"
      ],
      forum: [
        "route model, data, eval, rendering, and research lanes",
        "ledger each bounded improvement claim",
        "humanize handoffs without adding unsupported facts"
      ],
      crucible: [
        "promotion gates for eval, safety, and regression",
        "negative fixtures for changed args, missing evidence, stale criteria, and objective drift",
        "MATCH/DRIFT/UNVERIFIABLE verdicts before persistence"
      ],
      telos: [
        "model router and daemon supervisor",
        "action receipts, loop ledger, context pack, objective monitor, creative and scientific tool surfaces",
        "provider-neutral MCP and application bridge"
      ]
    },
    failure_codes: [
      "source_receipt_missing",
      "context_budget_exceeded",
      "eval_regression",
      "objective_drift",
      "promotion_gate_missing",
      "unbounded_self_training",
      "unverified_capability_claim",
      "external_side_effect_requires_review",
      "private_data_boundary_violation"
    ],
    next_actions: [
      "index.context.envelope: provide source-ref handles for the foundry daemon",
      "gather.run: maintain current official-source packets for model, tool, and eval claims",
      "forum.route: split foundry work into model runtime, post-training, eval, and creative/science lanes",
      "crucible.assess: gate every promotion on eval and receipt evidence",
      "telos.loop.ledger: store each daemon cycle as append-only loop state"
    ]
  };
  packet.validation = validateModelFoundryPacket(packet);
  packet.receipt_hash = hashStable(packet);
  return packet;
}

export function summary(packet = buildModelFoundryPacket()) {
  return [
    "Telos Model Foundry",
    `schema  ${packet.schema}`,
    `tool    ${packet.tool}`,
    `daemon  ${packet.daemon.mode}`,
    `layers  ${packet.model_layers.length}`,
    `sources ${packet.current_sources.length}`,
    `verdict ${packet.validation.verdict}`,
    "next    node demo/model-foundry.mjs"
  ].join("\n") + "\n";
}

function main() {
  const packet = buildModelFoundryPacket();
  process.stdout.write(process.argv.includes("--summary") ? summary(packet) : `${JSON.stringify(packet, null, 2)}\n`);
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  main();
}
