// The one place the version is read.
//
// It used to be written out by hand in eight places: the MCP serverInfo, the
// status and doctor envelopes, two sites each in room.mjs and
// flagship-workflow.mjs, and the server-manifest freshness expectation.
//
// One of those was already guarded. telos-mcp.test.mjs reads package.json and
// asserts serverInfo.version against it, so that site could not drift. The four
// envelope sites had no such check, so a release could bump package.json and
// leave every action receipt reporting the previous version with the suite
// still green. Reading the manifest once removes the question.
//
// package.json is read rather than imported. Import attributes for JSON are
// still gated behind a flag on some supported Node versions, and npm always
// puts package.json at the root of the tarball, so this resolves the same from
// a source checkout and from an installed package. Zero dependencies, which is
// the whole point of this surface.
import { readFileSync } from "node:fs";

const manifest = JSON.parse(
  readFileSync(new URL("../package.json", import.meta.url), "utf8")
);

/** The published version, from package.json. */
export const TELOS_VERSION = manifest.version;

/** The distribution name on npm. */
export const TELOS_PACKAGE = manifest.name;

/**
 * What this server calls itself over MCP.
 *
 * Every sibling lane reports its short name (plexus, canon, chorus, mneme,
 * articulate), so this one does too. It reported "project-telos-telos" from
 * June 2026 until the first npm publish, which reads as a concatenation slip
 * rather than a choice: nothing outside the code and its own assertion ever
 * referred to it.
 */
export const TELOS_SERVER_NAME = "telos";
