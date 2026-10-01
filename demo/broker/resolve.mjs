// Target resolution for the tier gate. This slice resolves the targets the
// 0.6.0 drivers take (page origin, window title, file path, command string).
// The element-ref slice (DESIGN.md section 5) replaces `ref` and `fingerprint`
// with snapshot-epoch refs; the broker only reads the fields named here.
import path from "node:path";
import { digestOf } from "./canonical.mjs";
import { namesSecretField, originOf, SHELL_METACHARS } from "./scope.mjs";
import { verbSpec } from "./tiers.mjs";

function pickWindow(windows, match) {
  if (typeof match !== "string" || !match) return { error: "TARGET_NOT_FOUND" };
  const m = match.toLowerCase();
  const exact = windows.filter((w) => String(w.title).toLowerCase() === m);
  const hits = exact.length ? exact : windows.filter((w) => String(w.title).toLowerCase().includes(m));
  if (hits.length === 0) return { error: "TARGET_NOT_FOUND" };
  if (hits.length > 1) return { error: "AMBIGUOUS_TARGET" };
  return { window: hits[0] };
}

async function resolveKind(spec, params, flags, { drivers, cwd }) {
  const at = (i) => (i === undefined ? undefined : params[i]);
  switch (spec.target) {
    case "origin": {
      const url = await drivers.pageUrl(flags);
      const origin = originOf(url);
      if (!origin) return { error: "TARGET_NOT_FOUND" };
      const out = { origin, url };
      if (spec.sameOrigin && originOf(at(spec.urlArg)) !== origin) out.crossOrigin = true;
      return out;
    }
    case "navigate": {
      const origin = originOf(at(spec.urlArg));
      return origin ? { origin, url: at(spec.urlArg) } : { error: "TARGET_NOT_FOUND" };
    }
    case "window":
      return pickWindow(await drivers.listWindows(), at(0));
    case "path-read":
    case "path-write":
      return { path: path.resolve(cwd, at(spec.pathArg) ?? ".") };
    case "argv": {
      const command = params.join(" ").trim();
      return { command, argv: command ? command.split(/\s+/) : [], shellMeta: SHELL_METACHARS.test(command) };
    }
    case "foreground":
    case "device":
      return { device: spec.device ?? null };
    default:
      return {};
  }
}

function resolutionOf(verb, params) {
  if ((verb === "browser.input" || verb === "browser.behave") && params[0] === "click") return "coordinate";
  return verbSpec(verb).selectorArg !== undefined ? "selector" : "none";
}

export async function resolveTarget(verb, params = [], flags = {}, { drivers, cwd = process.cwd() } = {}) {
  const spec = verbSpec(verb);
  const base = await resolveKind(spec, params, flags, { drivers, cwd });
  if (base.error) return base;
  const selector = spec.selectorArg !== undefined ? params[spec.selectorArg] ?? null : null;
  const target = {
    kind: spec.target,
    ...base,
    selector,
    secret: namesSecretField(selector),
    resolution: resolutionOf(verb, params),
    readPath: spec.readArg !== undefined && params[spec.readArg] ? path.resolve(cwd, params[spec.readArg]) : null,
    writePath: spec.writeArg !== undefined && params[spec.writeArg] ? path.resolve(cwd, params[spec.writeArg]) : null,
  };
  const where = target.origin ?? target.window?.title ?? target.path ?? target.argv?.[0] ?? target.device ?? "-";
  target.ref = `${spec.target}:${where}${selector ? `#${selector}` : ""}`;
  target.fingerprint = digestOf({ kind: target.kind, origin: target.origin ?? null, window: target.window ?? null, path: target.path ?? null, selector, resolution: target.resolution });
  return target;
}

// Live drivers for the CLI. Each is read-only: it attaches to an existing debug
// browser (never launches one) or lists top-level windows.
export function liveDrivers({ browser, app, port }) {
  return {
    async pageUrl(flags) {
      const { session, target } = await browser.attach({ port: flags.port ? Number(flags.port) : port, match: flags.match });
      session.close();
      return target.url;
    },
    async listWindows() {
      const r = await app.windows();
      return (r.windows ?? []).map((w) => ({ title: w.name, class: w.class, process: w.process ?? null }));
    },
  };
}
