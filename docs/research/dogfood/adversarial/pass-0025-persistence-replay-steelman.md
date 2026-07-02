# Pass 0025 Adversarial Steelman

Date: 2026-07-01

Subject: append-only JSONL persistence and replay for Telos action receipt
events.

## Steelman Objections

1. JSONL is not a production persistence system.

The pass proves local append-only file replay, not database durability,
concurrent writers, locking, crash recovery, replication, or retention policy.

Required countermeasure: add a storage adapter contract with fsync semantics,
concurrent append tests, and crash-replay fixtures before claiming production
runtime durability.

2. Hash chains are not signatures.

The ledger catches local tampering if the verifier has the expected head hash,
but it does not prove identity, non-repudiation, timestamp authority, or
external anchoring.

Required countermeasure: add signing and anchoring adapters over canonical
ledger lines after the storage interface stabilizes.

3. The compensation event is a no-op fixture.

The appended compensation demonstrates non-mutation, but it does not reverse a
real external action or prove user-visible remediation.

Required countermeasure: later external-action simulators need before/after
refs, reversal actions, and proof that the original event remains immutable.

4. Replay still trusts the local source fixture.

The replay binds back to pass 0024 by digest, but both artifacts live in the
same local corpus. This is enough for dogfood, not for independent audit.

Required countermeasure: export a minimal proof bundle and verify it from a
fresh directory with only ledger, source digest, validator, and public contract
excerpt.

5. Canonical JSON is necessary but insufficient.

Rejecting duplicate keys, non-finite JSON, and non-canonical lines prevents
some ambiguity, but does not address schema migration, semantic version drift,
or replay across languages.

Required countermeasure: add schema-version migration fixtures and a second
implementation verifier in another runtime.

6. Fresh context is simulated by file replay, not a separate agent process.

The pass replays from disk, but the same local Python process controls
generation and validation.

Required countermeasure: use a separate process with only a ledger path and
expected source digest, then compare outputs.

7. The market claim is still a hypothesis.

Durable replay is a strong proof-packet primitive, but this pass does not prove
buyer urgency, pricing, procurement fit, or competitor gaps.

Required countermeasure: connect this demo to the market matrix and test buyer
language against AI infrastructure teams using existing observability tools.

## Pass 0025 Boundary

The strongest claim pass 0025 can make is:

```text
A local append-only JSONL ledger can persist pass 0024 Telos-style action
receipt events, replay them from disk, preserve original event hashes, append a
compensation event without mutation, and reject structural replay hazards.
```

The pass must not claim production database durability, distributed consensus,
cryptographic signing, external anchoring, live runtime integration, external
write safety, scientific discovery, theorem proof, or natural-law promotion.

## Next Adversarial Tests

1. Crash during append and prove partial-line rejection.
2. Concurrent append collision and prove sequence/hash rejection.
3. Export bundle to a fresh temp directory and replay without repo context.
4. Sign canonical ledger lines and reject altered signatures.
5. Anchor the ledger head in a separate immutable artifact.
6. Redact a sensitive payload and prove no raw payload enters packet text.
7. Run replay in another implementation language.
8. Add schema migration and reject silent version drift.

Current promoted natural laws: none.
