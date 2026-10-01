# Current Host Protocol Notes

Verified on 2026-06-27 from official project and platform documentation.

## MCP Baseline

Project Telos treats MCP tools as JSON-RPC methods over host-selected transports. The local baseline is stdio and newline-delimited JSON-RPC; hosted or distributed deployments should prefer Streamable HTTP. Tool discovery and execution are expressed through `tools/list` and `tools/call`.

Primary source: https://modelcontextprotocol.io/specification/2025-06-18

## OpenAI Hosts

OpenAI Agents SDK integrations should mount the flagship MCP servers and keep business logic inside the tools. OpenAI Apps SDK integrations should register MCP tools and render receipts through the app UI instead of reimplementing Gather, Crucible, Index, Forum, or Telos behavior.

Primary sources:

- https://openai.github.io/openai-agents-python/mcp/
- https://developers.openai.com/apps-sdk/build/mcp-server

## Anthropic Hosts

Anthropic and Claude Code integrations should mount the same stdio MCP servers for local workflows. Remote deployments should use the current remote MCP transport supported by the host rather than introducing provider-specific tool semantics.

Primary source: https://docs.anthropic.com/en/docs/claude-code/mcp

## Project Telos Implication

Every flagship should expose a CLI JSON path and an MCP path. Provider adapters are configuration or thin host glue; they do not own workflow logic.