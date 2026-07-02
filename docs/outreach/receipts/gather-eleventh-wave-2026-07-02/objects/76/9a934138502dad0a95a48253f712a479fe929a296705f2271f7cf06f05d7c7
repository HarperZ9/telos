# Packet 017: Formal Identity - Odd Sum Square

Date: 2026-07-01

Status: `IDENTITY` plus bounded `PROBE_MATCH`.

Claim:

```text
For every natural number n >= 0:
sum_{k=1..n}(2k - 1) = n^2
```

## Proof

Base case, `n = 0`:

The left side is the empty sum, which is `0`. The right side is `0^2 = 0`. The identity holds.

Induction step:

Assume the identity holds for some `n >= 0`:

```text
sum_{k=1..n}(2k - 1) = n^2
```

Then for `n + 1`:

```text
sum_{k=1..n+1}(2k - 1)
= sum_{k=1..n}(2k - 1) + (2(n + 1) - 1)
= n^2 + 2n + 1
= (n + 1)^2
```

So the identity holds for `n + 1`. By induction, it holds for all natural `n >= 0`.

## Computational Witness

An incremental Python probe checked every `n` from `0` through `100000`.

Result:

- failures: `0`;
- sample `n=10`: `100`;
- sample `n=100000`: `10000000000`;
- seal: `e9293c7bb2fd8d0b4bbcf9ff547f4f50f90c3b0d008fe261a3c7bd338a779d5f`.

The first naive repeated-summation probe timed out. That failure is recorded as a measurement-design lesson: bounded witnesses should use the structure of the identity rather than quadratic recomputation.

## Proof-Packet Role

This is not a new theorem or natural law. It is a deliberately simple formal identity used to test whether the Telos proof-packet spine can carry:

- a precise claim;
- a human-checkable proof;
- a bounded computational witness;
- an action event normalized from an OpenTelemetry-style fixture;
- positive and negative validator outcomes;
- Crucible verdicts.

## Promotion

Promotion state: `IDENTITY`.

No `PROMOTED_LAW` status is assigned.
