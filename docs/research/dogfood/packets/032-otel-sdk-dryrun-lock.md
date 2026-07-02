# OpenTelemetry SDK Dry-Run Lock Packet

Pass: `0022`

Date: 2026-07-01

Status: `OTEL_SDK_DRYRUN_LOCK_MATCH`

This packet advances pass 0021 without mutating the shared environment. Because
`opentelemetry-sdk` is not installed locally, pass 0022 uses pip's dry-run
report mode to resolve a version-aligned SDK plan and capture wheel hashes.

No package was installed. `opentelemetry.sdk` remains unavailable after the
dry-run.

## Generated Receipt

Artifact:

```text
schemas/otel-sdk-dryrun-lock-pass-0022.json
```

Seal:

```text
678d201ea634eeea2786f0c4effb22d4e38528a80d7cb05c9abe18b446ba3f3c
```

Validator:

```text
schema = Pass0022OTelSdkDryRunLockValidatorRun/v1
status = MATCH
resolved_install_count = 2
negative_fixture_count = 5
invalid_distribution_warning_count = 3
post_dryrun_sdk_available = false
```

## Dry-Run Command

```text
python -m pip install --disable-pip-version-check --dry-run --report - opentelemetry-sdk==1.41.0
```

The command returned `0` and emitted a pip report. The report hash is:

```text
b472706e86eb81537066b709b4d2bd8df831bc1cafb196cb3e3e169f5b4bead2
```

## Resolved Wheels

| Package | Version | Requested | SHA-256 |
| --- | --- | --- | --- |
| `opentelemetry-sdk` | `1.41.0` | `true` | `a596f5687964a3e0d7f8edfdcf5b79cbca9c93c7025ebf5fb00f398a9443b0bd` |
| `opentelemetry-semantic-conventions` | `0.62b0` | `false` | `0ddac1ce59eaf1a827d9987ab60d9315fb27aea23304144242d1fcad9e16b489` |

The SDK requires:

```text
opentelemetry-api==1.41.0
opentelemetry-semantic-conventions==0.62b0
typing-extensions>=4.5.0
```

Local `opentelemetry-api==1.41.0` was already satisfied before this pass.

## Post Dry-Run Audit

| Field | Value |
| --- | --- |
| Distribution | `opentelemetry-sdk` |
| Module | `opentelemetry.sdk` |
| `find_spec_available` | `false` |
| Install performed | `false` |
| Expected status | `NOT_INSTALLED_AFTER_DRY_RUN` |

## Environment Warnings

The dry-run observed three pip warnings for invalid distributions:

```text
~
~arden-shell
~~rden-shell
```

These warnings do not block the dry-run, but they are now evidence that the
shared Python environment should be cleaned before any real install is promoted.

## Negative Fixtures

| Fixture | Expected Result |
| --- | --- |
| `negative-dryrun-treated-as-install` | `REJECT` |
| `negative-wheel-without-hash` | `REJECT` |
| `negative-unmatched-api-sdk-version` | `REJECT` |
| `negative-ignore-invalid-distribution-warnings` | `REJECT` |
| `negative-recording-span-without-sdk-import` | `REJECT` |

## Next Proof Step

The next pass should create an isolated environment or a throwaway venv, install
only the two resolved wheels plus already-satisfied dependencies, and then run a
real `OpenTelemetryRecordingSpanFixture/v1` with an in-memory exporter.

That fixture must record:

- tracer provider;
- resource attributes;
- span name;
- trace id and span id;
- span attributes;
- exporter sink hash;
- action-receipt mapping;
- non-promotion boundary.

## Non-Promotion

Pass 0022 performs pip dry-run resolution only. It does not install
`opentelemetry-sdk`, import `opentelemetry.sdk`, create recording spans, modify
the environment, or promote trace evidence.
