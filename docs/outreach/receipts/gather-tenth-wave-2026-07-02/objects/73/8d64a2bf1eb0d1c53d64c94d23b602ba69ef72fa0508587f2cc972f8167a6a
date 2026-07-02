# Packet 010: Post-Quantum Cryptography Migration Receipts

Status: `HYPOTHESIS` plus `PROBE_MATCH`

## Market Context

Post-quantum cryptography is no longer only research planning. NIST finalized FIPS 203, FIPS 204, and FIPS 205 in 2024 and encouraged system administrators to begin transition planning. The migration surface is large: codebases, TLS stacks, certificates, SSH, package signing, firmware signing, archives, and long-lived encrypted records.

Source URLs:

- https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards
- https://csrc.nist.gov/projects/post-quantum-cryptography

## Telos Wedge

Hypothesis: the unmet need is not another PQC algorithm implementation. The sharper product is a `PqcMigrationReceipt`:

- inventory of cryptographic use sites;
- source paths and dependency versions;
- algorithm classification: RSA/ECC/DH/classical symmetric/PQC/hybrid/unknown;
- standard target: ML-KEM, ML-DSA, SLH-DSA, or future backup;
- migration action record;
- tests and interoperability evidence;
- exception ledger;
- reviewer signoff or domain-validator verdict.

This could be sold as regulated migration proof: "what changed, why, where, and how it was checked."

## Local Probe

The pass ran a deterministic toy RSA round trip:

- `n=3233`;
- public exponent `17`;
- message `65`;
- ciphertext `2790`;
- decrypted output `65`;
- result matched original message.

Classification: `PROBE_MATCH`.

Boundary: this is not PQC. It is only a receipt template for cryptographic inventory and deterministic verification.

## Internal Integration

| Internal tool | Role |
| --- | --- |
| Index | Map cryptographic API usage across repos and dependency manifests. |
| Gather | Intake NIST standards, implementation docs, library guidance, and vendor migration notes. |
| Forum | Escalate crypto changes to compiler/security/domain validators. |
| Crucible | Check bounded claims: standard reference present, test vectors pass, inventory count unchanged after patch. |
| Telos action receipts | Record approval, source paths, tests, and migration artifacts. |
| BuildLang/buildc | Future typed receipt checker for allowed algorithms and policy profiles. |

## Gaps

| Gap | Label | Note |
| --- | --- | --- |
| No repo-wide crypto inventory was run in pass 0002. | `verified` | This packet only defines the receipt shape. |
| No PQC library was installed or tested. | `verified` | The pass did not run ML-KEM, ML-DSA, or SLH-DSA vectors. |
| NIST standard targets are official, but local migration mapping is missing. | `verified` | Source-backed standards exist; internal action still needed. |
| PQC policy schema compatibility with BuildLang is a hypothesis. | `unverified` | No BuildLang policy checker was invoked. |

## Demo Candidate

Create `pqc-inventory-demo`:

1. Run Index over one repo.
2. Detect crypto APIs and certificate/signature tools.
3. Emit `PqcMigrationReceipt` with `unknown` labels where classification fails.
4. Run a small standard test-vector suite if a PQC library is present.
5. Crucible checks count consistency and test-vector result.

## Market Read

Buyers: security teams, regulated enterprises, government contractors, financial institutions, infrastructure vendors.

Primary wedge: migration evidence, not cryptographic novelty. The budget signal is strong because standards are official and transition pressure is external.
