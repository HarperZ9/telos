export const SCHEMA = "project-telos.flagship-action/v1";
export const allowedStatuses = new Set(["MATCH", "DRIFT", "UNVERIFIABLE", "ERROR"]);

export function actionEnvelope({
  tool,
  toolVersion,
  command,
  status = "MATCH",
  inputs = [],
  outputs = [],
  receipts = [],
  native = {},
  nextActions = [],
  diagnostics = [],
  startedAt = new Date(0).toISOString(),
  finishedAt = new Date(0).toISOString()
}) {
  const envelope = {
    schema: SCHEMA,
    tool,
    tool_version: toolVersion,
    command,
    status,
    started_at: startedAt,
    finished_at: finishedAt,
    inputs,
    outputs,
    receipts,
    native,
    next_actions: nextActions,
    diagnostics
  };
  assertActionEnvelope(envelope);
  return envelope;
}

export function assertActionEnvelope(value) {
  for (const key of [
    "schema",
    "tool",
    "tool_version",
    "command",
    "status",
    "inputs",
    "outputs",
    "receipts",
    "native",
    "next_actions",
    "diagnostics"
  ]) {
    if (!(key in value)) {
      throw new Error(`missing action envelope key: ${key}`);
    }
  }
  if (value.schema !== SCHEMA) {
    throw new Error(`bad schema: ${value.schema}`);
  }
  if (!allowedStatuses.has(value.status)) {
    throw new Error(`bad status: ${value.status}`);
  }
  return true;
}
