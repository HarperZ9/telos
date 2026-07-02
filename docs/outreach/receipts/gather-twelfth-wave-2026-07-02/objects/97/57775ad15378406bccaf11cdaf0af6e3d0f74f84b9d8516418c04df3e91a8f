# Pass 0021 Adversarial Steelman

Date: 2026-07-01

Subject: pinned quantum framework environment plan and OpenTelemetry action
bridge.

Forum submit status: `UNVERIFIABLE`.

Forum error:

```text
the configured executor did not return valid JSON; point the daemon at a real model executor (could not parse JSON from output: Extra data: line 2 column 1 (char 98))
```

The local steelman below is not a Forum verdict. It is an internal adversarial
review because Forum submit is still unavailable.

## Strongest Objections

1. The environment is still a plan, not a resolved lock. A buyer-facing proof
   demo must show exact package versions, hashes, and reproducible install
   commands.

2. `opentelemetry-api` produced a `NonRecordingSpan`, which is useful for
   mapping semantics but not evidence of trace capture, export, or span
   attributes.

3. The package plan contains packages with different platform assumptions.
   CUDA-Q, QIR tooling, and provider SDKs may have OS, Python, compiler, wheel,
   or GPU constraints that a Windows local environment cannot satisfy without
   fallback lanes.

4. Braket and Qiskit Runtime can be imported without cloud execution, but live
   provider proof requires credential, account, backend, quota, cost, and result
   retrieval boundaries.

5. A pinned environment can become fragile if the demo relies on too many SDKs
   at once. The next pass should choose a minimum viable fixture path first.

6. BuildLang/buildc and Build Color should remain sibling runtime demos, not
   dependencies of the quantum demo.

7. Hashing the Python executable path string is not a binary provenance receipt.
   It is useful as local context only.

8. The package plans include install commands but do not yet include a generated
   constraints file, lockfile, wheel hashes, or a reproducible environment
   export.

## Countermeasures

1. Start the next pass with an environment manifest, not installation: record
   Python version, OS, pip version, desired packages, resolver command, and
   expected import checks.

2. Add `opentelemetry-sdk` as a separate fixture only after it is present in an
   isolated environment. The API-only fixture must remain non-promotional.

3. Build the first quantum framework-import fixture with the smallest dependency
   surface: either Cirq-only local simulator or Qiskit-only local circuit object.

4. Split provider SDK fixtures from cloud provider fixtures. Provider SDK import
   belongs in `FRAMEWORK_IMPORT_FIXTURE`; cloud execution belongs in
   `LIVE_PROVIDER_FIXTURE`.

5. Add platform fallback gates for CUDA-Q and QIR if Windows wheels or compiler
   dependencies block local import.

6. Promote BuildLang/buildc and Build Color through the same packet schema only
   after each has a real compiler/runtime or measurement receipt.

## Verdict

Pass 0021 is a clean planning and boundary pass. It should not be presented as
quantum framework readiness. The next proof pass should produce either a real
recording OpenTelemetry SDK fixture or a single-framework local import fixture,
but not both if that would widen the blast radius.
