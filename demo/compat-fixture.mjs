import { mkdirSync, realpathSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

/** Create only a new synthetic workspace. Existing targets are never reused. */
export function createCompatibilityFixture(directory) {
  const requested = path.resolve(directory);
  const root = path.join(realpathSync(path.dirname(requested)), path.basename(requested));
  mkdirSync(root); // EEXIST also refuses a target link or a pre-existing directory.
  const repo = path.join(root, "index");
  mkdirSync(path.join(repo, ".git"), { recursive: true });
  writeFileSync(path.join(repo, "pyproject.toml"), '[project]\nname="index-fixture"\nversion="0.0.0"\n', { flag: "wx" });
  writeFileSync(path.join(repo, "sample.py"), "VALUE = 1\n", { flag: "wx" });
  return { PROJECT_TELOS_COMPAT_FIXTURE: root.replaceAll("\\", "/") };
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  if (process.argv.length !== 3) {
    process.stderr.write("Usage: node demo/compat-fixture.mjs <new-directory>\n");
    process.exitCode = 2;
  } else {
    try {
      process.stdout.write(`${JSON.stringify(createCompatibilityFixture(process.argv[2]), null, 2)}\n`);
    } catch (error) {
      process.stderr.write(`Cannot create compatibility fixture: ${error.message}\n`);
      process.exitCode = 1;
    }
  }
}
