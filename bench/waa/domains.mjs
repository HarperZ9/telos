// WindowsAgentArena domains and the Telos benchmark grant scope for each.
//
// Domain keys and task counts are the keys of WAA's
// evaluation_examples_windows/test_all.json, read from
// github.com/microsoft/WindowsAgentArena on 2026-10-01 (154 tasks, 12 domains).
// The window patterns are the Windows process images and title fragments of
// the stock apps. They have not been checked inside the WAA guest image, so
// each carries verified: false until a dry run against the guest confirms it.
export const WAA_SOURCE = Object.freeze({
  repo: "github.com/microsoft/WindowsAgentArena",
  file: "src/win-arena-container/client/evaluation_examples_windows/test_all.json",
  read_on: "2026-10-01",
  total_tasks: 154,
});

const app = (process, title_contains, count) => Object.freeze({ surface: "native", windows: [{ process, title_contains }], count, verified: false });
const web = (process, count) => Object.freeze({ surface: "browser", process, origins_from_task: true, count, verified: false });

export const DOMAINS = Object.freeze({
  file_explorer: app("explorer", "File Explorer", 19),
  libreoffice_calc: app("soffice.bin", "LibreOffice Calc", 24),
  libreoffice_writer: app("soffice.bin", "LibreOffice Writer", 19),
  vs_code: app("code", "Visual Studio Code", 24),
  vlc: app("vlc", "VLC media player", 21),
  chrome: web("chrome", 17),
  msedge: web("msedge", 13),
  settings: app("systemsettings", "Settings", 5),
  clock: app("time", "Clock", 4),
  microsoft_paint: app("mspaint", "Paint", 3),
  windows_calc: app("calculatorapp", "Calculator", 3),
  notepad: app("notepad", "Notepad", 2),
});

// Verbs the benchmark grant lists. T1 observe and T3 act-by-ref; no T4 exec,
// no T5 synthetic input or hardware. Settings tasks that need a T4 config
// verb are reported as out of grant, not widened silently.
export const NATIVE_VERBS = Object.freeze(["app.windows", "app.tree", "app.snapshot-ax", "app.resolve", "app.value", "app.invoke", "app.setvalue", "app.select", "app.focus"]);
export const BROWSER_VERBS = Object.freeze(["browser.tabs", "browser.snapshot-ax", "browser.snapshot-text", "browser.click-ref", "browser.fill-ref", "browser.select-ref", "browser.focus-ref", "browser.navigate"]);

// benchmarkGrantSpec - the grant a run would ask the operator to issue for one
// domain. Browser origins come from each task's config, so the spec names none
// until a task supplies them; a browser domain with no origins grants nothing.
export function benchmarkGrantSpec(domain, { origins = [] } = {}) {
  const d = DOMAINS[domain];
  if (!d) return null;
  if (d.surface === "browser") {
    return { tier: "T3", verbs: [...BROWSER_VERBS], scope: { origins, senses: ["browser_tabs", "page_dom", "page_text"] }, max_actions: 60 };
  }
  return { tier: "T3", verbs: [...NATIVE_VERBS], scope: { windows: d.windows, senses: ["windows", "accessibility_tree"] }, max_actions: 60 };
}
