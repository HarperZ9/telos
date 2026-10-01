// Where Telos keeps operator state. There is deliberately no environment
// override: a process that could point Telos at a directory it controls could
// bring its own grants. Tests pass directories explicitly.
import os from "node:os";
import path from "node:path";

export function stateRoot({ env = process.env, platform = process.platform, home = os.homedir() } = {}) {
  if (platform === "win32") {
    const base = env.LOCALAPPDATA || path.join(home, "AppData", "Local");
    return path.join(base, "Telos");
  }
  const base = env.XDG_STATE_HOME || path.join(home, ".local", "state");
  return path.join(base, "telos");
}

export function stateDirs(root = stateRoot()) {
  return {
    root,
    grants: path.join(root, "grants"),
    keys: path.join(root, "keys"),
    holds: path.join(root, "holds"),
    receipts: path.join(root, "receipts"),
    preimages: path.join(root, "preimages"),
    usage: path.join(root, "usage"),
  };
}
