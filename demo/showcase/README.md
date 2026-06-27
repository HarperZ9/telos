# OSS Proof Showcase

The OSS Proof Showcase is a Telos lane for finding public bug candidates,
capturing evidence, and producing local PR-readiness packets. It does not open
PRs or post upstream comments by itself.

## Fixture Scout

```powershell
node demo\showcase.mjs scout --fixture
node demo\showcase.mjs scout --fixture --json
```

The fixture is modeled after `pandas-dev/pandas#66050` and keeps default tests
offline and deterministic.

## Live Scout

```powershell
node demo\showcase.mjs scout --query "repo:pandas-dev/pandas is:issue is:open label:Bug pd.array masked array" --limit 5 --json
```

The live scout requires the GitHub CLI. It records failures as unverifiable
candidate capture rather than guessing.

## PR-Readiness Packet

```powershell
node demo\showcase.mjs record --candidate demo\showcase\fixtures\pandas-66050.json --evidence path\to\evidence.json --json
```

The packet becomes PR-ready only when reproduction, patch summary, passing test
evidence, and a `MATCH` Crucible verdict are present.

Every packet includes a `not_verified` section for skipped tests, files not
inspected, assumptions, and unobserved state. Later retry, refund, dispute,
maintainer feedback, or re-run events append to `follow_up_events`; they do not
rewrite the original evidence.