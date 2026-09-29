# Telos 0.4.3

The browser `apifetch` command again sends its positional request body and honors
`--contenttype` and `--method`. Version 0.4.2 introduced a duplicate dispatch label
that masked the original implementation. Requests without a body keep the existing
POST and JSON defaults.

Offline tests exercise argument dispatch with a fake browser session and reject
duplicate case labels. Static guards check that capabilities removed in 0.4.2 do
not return under their former module, import, dependency, command, or environment
variable names. These checks do not detect a capability renamed to evade a guard;
code and behavior review remain necessary.

This patch preserves the existing MCP surface and actuation behavior. It does not
add the unfinished input-timing or search-scrape redesign. The tests do not establish
live browser control or admission to another harness's native-control policy.
