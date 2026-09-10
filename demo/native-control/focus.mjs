// Driver behavior classification, not a measurement of actual OS focus.
// Browser actuation may first launch Chrome. Invocations, scripts and device
// execution can have application-defined effects, so unknown stays null.
const NO_INPUT = new Set([
  "help", "browser.tabs", "app.windows", "app.tree", "app.value",
  "device.read", "device.write", "device.ls",
]);
export function focusSemantics(action, result) {
  if (result?.foreground === true || action === "app.input" || action === "app.type") {
    return { background: false, focus_effect: "foreground_input" };
  }
  if (action === "app.focus" || action === "app.setvalue") {
    return { background: false, focus_effect: "focus_requested" };
  }
  if (NO_INPUT.has(action)) return { background: true, focus_effect: "none_requested" };
  return { background: null, focus_effect: "unknown" };
}
