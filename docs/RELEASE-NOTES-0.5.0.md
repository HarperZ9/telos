# Telos 0.5.0 candidate

Telos now builds scoped client packages alongside the main distribution. Windows
x64 ZIP and Claude Desktop MCPB artifacts include a pinned Node runtime and its
license. Advanced source ZIP packages retain an explicit Node prerequisite.

The plugin contains the Telos workbench skill and MCP entrypoint. It does not
install sibling tools, configure client accounts or add a model. Native control,
network and write permissions retain their existing boundaries.

Release packaging requires matching source and plugin versions, a clean exact-tag
checkout, runtime and payload checksums, real local stdio validation and exact-byte
rerun comparison. Client installation and marketplace review remain separate gates.
