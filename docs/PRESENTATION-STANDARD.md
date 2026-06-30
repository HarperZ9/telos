# Forward-Facing Repository Presentation Standard

Project Telos repositories must be understandable to two audiences without making either one decode internal language.

## Public Layer

The first screen of a README or GitHub page must answer four questions in plain language.

- What is this?
- Who is it for?
- What problem does it solve?
- What can I try in under five minutes?

Required public elements:

- A readable hero or product mark when the repository is a product, flagship, demo, site, or visual tool.
- A one-line description using ordinary product language.
- A short "Why it matters" section.
- A "Try it" or "Quickstart" section with a runnable path.
- No architecture-only terms in the first screen unless they are defined immediately.

## Developer Layer

The developer section must make the repository operable without private context.

Required developer elements:

- Install or local setup instructions.
- One runnable command.
- Test or verification command.
- Integration surface: CLI, library, MCP, plugin, app, IDE, TUI, browser, or file protocol.
- Current status with version, runtime, dependency, CI, and known limits.
- License and contribution boundary.
- Receipt, provenance, or audit behavior when the repository produces claims, artifacts, or actions.

## Visual Layer

Presentation should be public-readable first and internally expressive second.

- Typography must remain legible at GitHub README width.
- Effects must sit behind contained visual material, not behind essential text.
- Use color as support, never as the only status signal.
- Static PNG/SVG fallbacks are required for GitHub and low-capability hosts.
- Purchased fonts may be used to render exported artwork, but font files stay local and are not committed.
- `r/design`, `r/design_critiques`, and `r/posterdesign` are presentation reference lanes, not evidence sources.

## Repository Classes

- Flagship: full hero, public layer, developer layer, docs, CI/status, receipt/provenance story.
- Product/library: concise hero or mark, public layer, install/test/integration docs.
- Research paper/spec: clear abstract, claim boundaries, citations/provenance, reproduction path.
- Utility: no decorative hero required, but it still needs a plain description, quickstart, and verification command.
- Fork: do not apply Telos branding by default. Use the fork for upstream-quality patches unless the fork has a Harper-specific purpose.
