// CLI for the Telos Studio model-in-the-loop offline stub.
//
//   node demo/model-adapter-cli.mjs                       # summary for the sample intent
//   node demo/model-adapter-cli.mjs "warmer palette, 7-fold, slower loop"
//   node demo/model-adapter-cli.mjs --json "faster, cooler"
//
// The scene substrate is a classic browser script; importing it here sets the
// TelosEffectsProtocol global that model-adapter.js reads. We import both as
// side effects, then read the attached globals.
import { fileURLToPath } from "node:url";

await import("./effects-protocol.js");
await import("./model-adapter.js");

const api = globalThis.TelosModelAdapter;

function run(argv) {
  const wantJson = argv.includes("--json");
  const args = argv.filter((arg) => arg !== "--json" && arg !== "--summary");
  const intent = args.join(" ") || "make the field tile at 5-fold, warmer palette, slower loop";

  if (wantJson) {
    const adapter = api.createOfflineAdapter();
    const arena = api.runArena(adapter, intent, {});
    const receipt = api.witnessPick(arena, "a");
    return `${JSON.stringify({ arena, receipt }, null, 2)}\n`;
  }
  return api.summary(intent);
}

if (fileURLToPath(import.meta.url) === process.argv[1]) {
  process.stdout.write(run(process.argv.slice(2)));
}

export { run };
