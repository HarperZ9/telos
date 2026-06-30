import { scoutLive, renderScoutTable } from "./showcase/scout.mjs";

const payload = scoutLive({
  query: "repo:pandas-dev/pandas is:issue is:open label:Bug pd.array masked array",
  limit: 5
});

if (payload.status === "UNVERIFIABLE") {
  process.stderr.write(`${JSON.stringify(payload.diagnostics || [], null, 2)}\n`);
  process.exitCode = 2;
} else {
  process.stdout.write(renderScoutTable(payload));
}