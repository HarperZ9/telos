# Pass 0026 Adversarial Steelman

Date: 2026-07-01

Subject: redaction-boundary fixture for action receipt proof packets.

## Steelman Objections

1. This is not production DLP.

The pass proves a local fixture and scan. It does not provide enterprise data
classification, policy engines, secret stores, retention rules, or endpoint
controls.

Required countermeasure: add policy-class fixtures and test multiple payload
classes before claiming operational DLP.

2. The raw payload is a fixture, not a real secret.

The payload is synthetic and deterministic. This is correct for a public-safe
test, but it does not prove safety for real credentials, PII, PHI, or regulated
client data.

Required countermeasure: keep using synthetic payloads for public artifacts, but
add private-only operator tests for real data classes inside secure local
tooling.

3. Digest refs can leak correlation.

Even when raw text is absent, a digest can still identify a known payload if the
payload has low entropy or appears in a dictionary.

Required countermeasure: add salted or keyed digest adapter fixtures for
low-entropy payload classes.

4. The scan target list can be incomplete.

The validator only scans declared targets. If a future packet writes raw payload
to an unlisted file, this pass would not catch it.

Required countermeasure: add recursive leak scans over the pass artifact set and
explicit allowlists for private temp paths.

5. Redacted refs are still local files.

The pass does not prove object storage, signed refs, access control, retention,
or immutable audit trails.

Required countermeasure: combine redaction with the pass 0025 append-only ledger
and later signing/anchoring adapters.

6. The raw temp file may persist.

Temp-private does not mean deleted. This pass avoids repo commit risk, but does
not prove lifecycle management.

Required countermeasure: add destruction and post-delete digest receipts, or a
private vault adapter with lifecycle policy.

## Pass 0026 Boundary

The strongest claim pass 0026 can make is:

```text
A local fixture can keep a synthetic raw payload out of model-facing artifacts,
carry only digest-bound redacted refs, and scan declared pass files for leaks.
```

The pass must not claim production DLP, cryptographic secrecy, external vault
integration, live runtime integration, scientific discovery, theorem proof, or
natural-law promotion.

## Next Adversarial Tests

1. Recursive scan over the whole pass artifact directory.
2. Salted digest fixture for low-entropy payloads.
3. Delete raw temp file and prove post-delete absence.
4. Replay from a fresh directory with only digest refs.
5. Add redaction schema migration tests.
6. Add policy classes for PII, PHI, credentials, and proprietary source text.
7. Verify no raw payload appears in generated Crucible reports.

Current promoted natural laws: none.
