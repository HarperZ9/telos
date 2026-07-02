# Agent Action Proof-Packet Factory Adapter Brief

Date: 2026-07-01

## Decision

Promote `AgentActionProofPacketFactory` from strategy into the first executable
factory demo. The adapter preserves incumbent trace identifiers, but requires
Telos fields that traces alone cannot prove: authority, admission, side-effect
class, privacy boundary, verifier verdict, and stop reason.

## Market Wedge

This is not a LangSmith, Langfuse, Phoenix, Braintrust, or OpenTelemetry
replacement claim. It is an import-and-bind layer for regulated and high-stakes
agent work.
