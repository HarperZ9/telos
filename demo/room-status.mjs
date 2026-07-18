const sourceHealthy = {
  crucible: {
    statuses: new Set(["OK"]),
    checks: new Set(["OK", "available"])
  }
};

export function normalizeRoomStatus(tool, value) {
  if (value === "MATCH") {
    return "MATCH";
  }
  return sourceHealthy[tool]?.statuses.has(value) ? "MATCH" : value;
}

export function roomCheckPasses(tool, value) {
  if (value === "MATCH") {
    return true;
  }
  return sourceHealthy[tool]?.checks.has(value) ?? false;
}
