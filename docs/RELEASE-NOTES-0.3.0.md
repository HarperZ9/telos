# Project Telos 0.3.0

This release changes native-control receipt verification and corrects browser
packet privacy labels. It follows the pre-1.0 minor-version compatibility policy;
consumers need to account for the two changes below before upgrading writers.

## Ledger compatibility

New native-control ledgers export `hash_version: 2` under the existing
`project-telos.native-control-ledger/v1` schema identifier. The hash binds
session metadata and entry fields, including action, target, and outcome.
Both the library and the standalone verifier support this format.

Upgrade readers before writers. Version 0.2.0 readers reject version 2 ledgers.
Version 0.3.0 readers retain support for legacy receipts with
`integrity_scope: legacy-step-and-result-only`; legacy metadata does not gain
integrity protection merely because a newer reader accepted the receipt.
New receipt success reports `entry-and-session-metadata`.

Hashes are unsigned. A trusted external checkpoint is needed to detect a fully
rewritten chain or a removed suffix. A consistent chain does not establish
execution success, authorship, completeness, semantic truth, or safety.

## Browser packet compatibility and privacy

Browser packets now report `redaction_status: unredacted`. The builder rejects
unsupported redaction assertions, and the validator rejects a forged `redacted`
label. Consumers that expected the old literal must update their handling.

URLs, titles, selectors, artifact references, and supplied summaries can retain
source context. Snapshot text is hashed rather than exported as raw DOM/body;
hashing is not encryption or a complete privacy transformation. Keep packets in
private operator storage. This release does not provide a public-safe sanitizer.

## Install and package boundary

The GitHub release provides `project-telos-mcp-0.3.0.tgz`,
`project-telos-demo-v0.3.0.zip`, and `SHA256SUMS.txt`. Both archives share the
reviewed npm package file set and include the native helper scripts. Local
font-input render receipts remain excluded. The standalone `verify_packet.mjs`
is now included in both archives for offline receipt checks with
`node verify_packet.mjs path/to/receipt.json` from the extracted package root.
Sibling flagship servers are separate source checkouts, not bundled servers.

```bash
npm install -g ./project-telos-mcp-0.3.0.tgz
telos catalog --summary
```

The native Telos MCP surface remains 41 tools. Node 20 or newer is required;
CI uses Node 24. npm registry publication is a separate operator action.

## Verification boundary

CI and release gates include synthetic metadata mutations, legacy-receipt
compatibility, browser privacy assertions, packaging negative controls, and
source-checkout MCP launch checks. These checks do not measure live browser or
Windows control, focus behavior, provider conformance, or execution safety.
