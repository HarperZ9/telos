# Packet 015: Epidemiology and Public-Health Modeling Receipts

Status: `HYPOTHESIS` plus `PROBE_MATCH`

## Market Context

A 2025 Nature Communications scoping review describes opportunities and challenges in integrating AI with mechanistic epidemiological modeling. It frames integrated models as potentially useful for complex transmission settings while emphasizing interdisciplinary collaboration and the need to handle uncertainty, realism, and evolving epidemiological situations.

Source URL: https://www.nature.com/articles/s41467-024-55461-x

## Telos Wedge

Hypothesis: public-health modeling needs `EpiClaimPacket` receipts:

- disease/model scope;
- data source, date range, and population;
- mechanistic assumptions;
- AI model or parameter-fitting method;
- uncertainty interval;
- intervention assumptions;
- validation set;
- ethical and policy-use label;
- reviewer verdict.

The product should keep a hard wall between model exploration and policy/medical advice.

## Local Probe

The pass ran a deterministic SIR Euler integration:

- `beta=0.31`;
- `gamma=0.08`;
- `dt=0.05`;
- `steps=2000`;
- initial population `1000.0`;
- final population `1000.0000000000003`;
- max population error `9.094947017729282e-13`;
- peak infected `393.3871661096931`.

Classification: `PROBE_MATCH`.

Boundary: this is a conservation check for a toy model, not epidemiological evidence.

## Internal Integration

| Internal tool | Role |
| --- | --- |
| Gather | Intake public-health papers, datasets, and model guidance. |
| Index | Bind notebooks, source data, model configs, and output reports. |
| Forum | Escalate to deep research and public-health/domain validators. |
| Crucible | Check conservation, parameter consistency, no future leakage, and benchmark metrics. |
| Telos | Keep action receipts and policy-use labels. |
| BuildLang/buildc | Future deterministic model kernels and policy labels. |

## Gaps

| Gap | Label | Note |
| --- | --- | --- |
| No real outbreak dataset was used. | `verified` | Only a toy SIR conservation probe was run. |
| No public-health recommendation was made. | `verified` | The packet is explicitly non-advisory. |
| Data privacy and ethics review are absent. | `verified` | Required before real health data workflows. |
| BuildLang epidemiology kernels are future work. | `unverified` | No `.bld` epi module was inspected. |

## Demo Candidate

Create `epi-conservation-demo`:

1. Load a simple public synthetic SIR dataset.
2. Fit or simulate baseline parameters.
3. Emit `EpiClaimPacket` with assumptions and conservation checks.
4. Crucible checks population conservation and output reproducibility.
5. Label all results `toy` or `research-only`.

## Market Read

Buyers: public-health researchers, epidemiology labs, civic analytics teams, policy modeling groups.

Primary wedge: accountable modeling records. The product must be careful: public trust depends on conservative claim labels and review gates.
