// Telos permission tiers (DESIGN.md section 1.1). Every verb the native-control
// dispatcher accepts has a tier floor here, and a test fails when a dispatcher
// `case` label has none. Context can raise a floor; nothing lowers it.
export const TIERS = Object.freeze(["T0", "T1", "T2", "T3", "T4", "T5"]);

export function tierRank(tier) {
  const i = TIERS.indexOf(tier);
  if (i < 0) throw new RangeError(`unknown tier ${tier}`);
  return i;
}

export const maxTier = (a, b) => (tierRank(a) >= tierRank(b) ? a : b);

// Grant expiry ceiling, approval window and batching per tier.
export const LADDER = Object.freeze({
  T0: { name: "Catalog", ceiling_s: 0, window_s: 0, confirm: false, batch_max: 1 },
  T1: { name: "Observe", ceiling_s: 8 * 3600, window_s: 0, confirm: false, batch_max: 1 },
  T2: { name: "Reversible act", ceiling_s: 4 * 3600, window_s: 0, confirm: false, batch_max: 1 },
  T3: { name: "Consequential act", ceiling_s: 3600, window_s: 120, confirm: true, batch_max: 10 },
  T4: { name: "Execute and configure", ceiling_s: 900, window_s: 60, confirm: true, batch_max: 1 },
  T5: { name: "Hardware", ceiling_s: 900, window_s: 60, confirm: true, batch_max: 1, session_bound: true },
});

// Senses a T1 wildcard never implies.
export const NAMED_ONLY_SENSES = Object.freeze(["screen", "clipboard"]);

// Field marks a target may not name (Flywheel browser_control SECRET_FIELDS).
export const SECRET_MARKS = Object.freeze([
  "password", "passwd", "pwd", "otp", "mfa", "2fa", "cvv", "cvc", "card", "cardnumber",
  "ssn", "secret", "token", "apikey", "api_key", "private_key", "seed_phrase",
]);

// target kinds: none | origin | navigate | window | path-read | path-write |
// argv | foreground | device. `arg` is the positional index the resolver reads.
// A kind the gate does not know is out of scope (fail closed).
const v = (tier, target, extra = {}) => Object.freeze({ tier, target, ...extra });

export const VERBS = Object.freeze({
  "browser.tabs": v("T1", "none", { sense: "browser_tabs" }),
  "browser.gettext": v("T1", "origin", { sense: "page_text", selectorArg: 0 }),
  "browser.waitfor": v("T1", "origin", { sense: "page_text", selectorArg: 0 }),
  "browser.snapshot-dom": v("T1", "origin", { sense: "page_dom" }),
  "browser.snapshot-text": v("T1", "origin", { sense: "page_text" }),
  "browser.screenshot": v("T1", "origin", { sense: "page_screenshot", writeArg: 0 }),
  "browser.snapshot-visual": v("T1", "origin", { sense: "page_screenshot", writeArg: 0 }),
  "browser.evidence": v("T1", "origin", { sense: "page_state" }),
  "browser.snapshot-ax": v("T1", "origin", { sense: "page_dom" }),
  // Act-by-ref (DESIGN.md 5.3). params[refArg] is a snapshot ref; the resolver
  // re-reads the element and binds its live fingerprint into the action digest.
  "browser.click-ref": v("T3", "origin", { refArg: 0 }),
  "browser.fill-ref": v("T3", "origin", { refArg: 0 }),
  "browser.select-ref": v("T3", "origin", { refArg: 0 }),
  "browser.focus-ref": v("T3", "origin", { refArg: 0 }),
  "browser.runverify": v("T0", "none"),
  "browser.navigate": v("T3", "navigate", { urlArg: 0 }),
  "browser.click": v("T3", "origin", { selectorArg: 0 }),
  "browser.fill": v("T3", "origin", { selectorArg: 0 }),
  "browser.focus": v("T3", "origin", { selectorArg: 0 }),
  "browser.type": v("T3", "origin"),
  "browser.input": v("T3", "origin", { selectorArg: 1 }),
  "browser.behave": v("T3", "origin", { selectorArg: 1 }),
  "browser.upload": v("T3", "origin", { selectorArg: 0, readArg: 1 }),
  "browser.autofill": v("T3", "origin"),
  "browser.spatialfill": v("T3", "origin"),
  "browser.autofillframe": v("T3", "origin"),
  "browser.spatialfillframe": v("T3", "origin"),
  "browser.apifetch": v("T3", "origin", { urlArg: 0, sameOrigin: true }),
  "browser.netcap": v("T3", "origin"),
  "browser.eval": v("T4", "origin"),
  "browser.evalfile": v("T4", "origin", { readArg: 0 }),
  "browser.evalframe": v("T4", "origin", { readArg: 1 }),
  "browser.run": v("T4", "origin"),
  "app.windows": v("T1", "none", { sense: "windows" }),
  "app.tree": v("T1", "window", { sense: "accessibility_tree" }),
  "app.value": v("T1", "window", { sense: "accessibility_tree", selectorArg: 1 }),
  "app.snapshot-ax": v("T1", "window", { sense: "accessibility_tree" }),
  "app.resolve": v("T1", "window", { sense: "accessibility_tree", selectorArg: 1 }),
  "app.invoke": v("T3", "window", { selectorArg: 1 }),
  "app.setvalue": v("T3", "window", { selectorArg: 1 }),
  "app.select": v("T3", "window", { selectorArg: 1 }),
  "app.focus": v("T3", "window"),
  "app.restore": v("T3", "window"),
  "app.input": v("T5", "foreground", { device: "input:synthetic", suspendDuringHold: true }),
  "app.type": v("T5", "foreground", { device: "input:synthetic", suspendDuringHold: true }),
  "device.ls": v("T1", "path-read", { sense: "directory_list", pathArg: 0 }),
  "device.read": v("T1", "path-read", { sense: "file_read", pathArg: 0 }),
  "device.write": v("T2", "path-write", { pathArg: 0 }),
  "device.exec": v("T4", "argv"),
  "learn.status": v("T1", "none", { sense: "learn" }),
  "learn.due": v("T1", "none", { sense: "learn" }),
  "learn.mastery": v("T1", "none", { sense: "learn" }),
  "learn.misconceptions": v("T1", "none", { sense: "learn" }),
  "learn.plan": v("T3", "none"),
  "learn.record": v("T3", "none"),
  "learn.study": v("T3", "none"),
  // Reserved: listed so the ladder is complete; refused until a module and,
  // where marked, a presence check exist.
  "sense.screen": v("T1", "none", { sense: "screen", reserved: true }),
  "sense.clipboard": v("T1", "none", { sense: "clipboard", reserved: true }),
  "sense.microphone": v("T5", "device", { reserved: true }),
  "sense.camera": v("T5", "device", { reserved: true }),
  "hardware.ddc.write": v("T5", "device", { reserved: true }),
  "hardware.gamma.apply": v("T5", "device", { reserved: true }),
  "hardware.usb.io": v("T5", "device", { reserved: true }),
  "hardware.device.enable": v("T5", "device", { reserved: true }),
  "hardware.device.disable": v("T5", "device", { reserved: true, presence: true }),
  "hardware.power.sleep": v("T5", "device", { reserved: true, presence: true }),
  "hardware.power.restart": v("T5", "device", { reserved: true, presence: true }),
  "hardware.power.shutdown": v("T5", "device", { reserved: true, presence: true }),
});

export function verbSpec(verb) {
  return Object.hasOwn(VERBS, verb) ? VERBS[verb] : null;
}

// Promotion only. `ctx` comes from the resolver and the broker's own checks.
export function effectiveTier(verb, ctx = {}) {
  const spec = verbSpec(verb);
  if (!spec) return null;
  let tier = spec.tier;
  if (ctx.resolution === "coordinate") tier = maxTier(tier, "T3");
  if (ctx.writesOutsideSandbox) tier = maxTier(tier, "T3");
  if (ctx.writesInSandbox) tier = maxTier(tier, "T2");
  if (ctx.preimageFailed) tier = maxTier(tier, "T3");
  return tier;
}
