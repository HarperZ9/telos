// Pack dry-run only; no installation, helper execution or host observation.
import test from "node:test";
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

test("package includes exact native helpers beside their existing drivers", () => {
  const root = fileURLToPath(new URL("../", import.meta.url));
  const cmd = process.platform === "win32" ? "cmd.exe" : "npm";
  const args = process.platform === "win32"
    ? ["/d", "/s", "/c", "npm pack --dry-run --ignore-scripts --json"]
    : ["pack", "--dry-run", "--ignore-scripts", "--json"];
  const out = spawnSync(cmd, args, { cwd: root, encoding: "utf8", timeout: 60000, windowsHide: true });
  assert.equal(out.status, 0, out.stderr);
  const files = JSON.parse(out.stdout)[0].files.map(x => x.path);
  assert.deepEqual(files.filter(x => x.startsWith("tools/")).sort(),
    ["tools/device.ps1", "tools/uia.ps1"]);
  for (const name of ["app", "device"]) assert.ok(files.includes(`demo/native-control/${name}.mjs`));
  assert.ok(files.includes("docs/native-control-contract.md"));
});
