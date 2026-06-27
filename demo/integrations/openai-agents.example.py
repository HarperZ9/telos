"""Example wiring only: Project Telos tools should be mounted through MCP.

The real implementation keeps business logic in the flagship CLIs/MCP servers.
OpenAI Agents code imports the MCP server connection for the selected deployment
and never reimplements gather, index, forum, crucible, or telos behavior here.
"""

PROJECT_TELOS_MCP_SERVERS = {
    "index": {"command": "index", "args": ["mcp"]},
    "forum": {"command": "forum", "args": ["mcp"]},
    "telos": {
        "command": "node",
        "args": ["C:/dev/public/telos/demo/flagship-workflow.mjs"],
        "mode": "cli-json-bridge",
    },
}

SYSTEM_PROMPT = (
    "Use Project Telos tools through MCP or their CLI JSON envelopes. "
    "Prefer gather.docs for intake, index.map/context for structure, "
    "forum.route for orchestration, crucible.assess for verification, "
    "and telos.workflow for reconciliation."
)
