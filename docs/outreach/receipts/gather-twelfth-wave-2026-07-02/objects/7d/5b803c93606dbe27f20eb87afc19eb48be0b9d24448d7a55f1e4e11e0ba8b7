# Packet 014: Finance and Systemic-Risk Receipts

Status: `HYPOTHESIS` plus `PROBE_MATCH`

## Market Context

The Bank of England describes AI as beneficial for financial services while also raising systemic-risk channels: common weaknesses in widely used models, correlated market behavior, operational dependence on a small number of AI service providers, and changing cyber threats. It also explicitly discusses agentic AI as systems that can take autonomous action using tools and feedback.

Source URL: https://www.bankofengland.co.uk/financial-stability-in-focus/2025/april-2025

## Telos Wedge

Hypothesis: finance needs `ModelRiskActionPacket` receipts:

- model, prompt, data, and version;
- market data provenance and freshness;
- decision/action boundary;
- risk metric assumptions;
- stress scenario;
- human approval;
- tool/action log;
- provider dependency;
- validation verdict and exception record.

The wedge is strongest where AI systems influence trades, underwriting, pricing, capital allocation, or risk reports.

## Local Probe

The pass ran a two-asset one-day 95 percent parametric VaR calculation:

- weights: `0.6`, `0.4`;
- annualized vols: `0.20`, `0.35`;
- correlation: `0.25`;
- portfolio value: `$1,000,000`;
- daily portfolio sigma: `0.012971274735120223`;
- one-day 95 percent VaR: `$21335.848294246498`.

Classification: `PROBE_MATCH`.

Boundary: this is a receipt-format probe, not a trading or investment recommendation.

## Internal Integration

| Internal tool | Role |
| --- | --- |
| Build Engine | Existing paper-first prediction and feedback loop surface. |
| Build Finance | Internal financial primitive target named by Build Ecosystem. |
| Build Oracle | Forecasting and anomaly-detection target named by Build Ecosystem. |
| Telos | Action receipts for model/tool decisions. |
| Crucible | Risk metric and stress-test verification. |
| Index | Portfolio/model/code context map. |
| Gather | Regulatory, policy, market, and model-risk source intake. |

## Gaps

| Gap | Label | Note |
| --- | --- | --- |
| No live broker action was run. | `verified` | Build Engine README states paper mode is default and live mode is gated. |
| No real portfolio or market feed was used. | `verified` | Probe used synthetic parameters. |
| Regulated finance claims need model-risk review. | `verified` | Forum escalated finance. |
| Build Finance was not inspected in this pass. | `unverified` | Future pass should inspect package surfaces. |

## Demo Candidate

Create `model-risk-receipt-demo`:

1. Run a paper-only forecast or VaR calculation.
2. Emit `ModelRiskActionPacket` with data digest and assumptions.
3. Crucible checks formula, sign, covariance, and no live action.
4. Add stress scenario and reviewer note.
5. Label as `research` or `paper-only`.

## Market Read

Buyers: banks, insurers, asset managers, fintech risk teams, audit teams, regulators.

Primary wedge: evidence-grade AI model-risk reporting for agentic workflows. Avoid any positioning as financial advice or automated trading alpha.
