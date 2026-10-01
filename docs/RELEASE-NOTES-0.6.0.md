# Telos 0.6.0

Telos 0.6.0 narrows the native-control drivers to actions a person directs and
can check. An audit of the 0.5.0 package found code in categories Telos does not
support. 0.6.0 removes that code, and new tests fail if it comes back.

## Removed

- The search scraper. It sent a hard-coded browser User-Agent and ran requests
  through a signed-in browser session to get past bot blocks.
- The email, LinkedIn and Gumroad verbs (`send`, `targets`, `linkedin`,
  `gumroadlogin`, `gumroadlist`, workflow action `contact.send`). They sent
  mail, posted and signed in to consumer services through a carried session
  with no confirmation step. None of them was documented.
- Randomized keystroke timing. Input helpers now pause a fixed 20 ms between
  keys by default (`--pause=<ms>` to change it), which rich editors need to
  settle. The helpers are renamed `pointerClick`, `typeText`, `typeKeys` and
  `selectOption`; the `behave` verb and `behave.*` workflow actions still work.
- The built-in form profile. It held one person's location, demographic,
  disability, veteran and work-eligibility answers and ticked consent and
  arbitration boxes by default. Forms now fill only from a profile the caller
  passes or the file named by `TELOS_FORM_PROFILE`. Consent boxes need
  `"consent": true`. Unanswered questions are reported, never guessed.

## Changed

- `browser netcap` replaces credential, cookie, session, CSRF and key header
  values with `[redacted]` and reports request bodies by size only.

## Unchanged

The MCP server, its 41 `telos.*` tools and the five-flagship manifest are the
same as 0.5.0. `telos.native.control` over MCP still returns the driver catalog
only and performs no action. The client plugin carries the same workbench skill
and entrypoint, and it adds no model, account or hosted service.

## Upgrade notes

- A workflow that relied on the default profile must now pass a profile or set
  `TELOS_FORM_PROFILE`. A profile file that cannot be read is an error.
- A workflow that relied on consent boxes being ticked must set
  `"consent": true` in its profile.
- Scripts that called the removed verbs fail with `unknown browser verb`.

## Limits

The guards check names and patterns in the shipped driver files. A capability
renamed to something innocuous would pass them, so code review still owns the
boundary. Password fields are still filled when a caller supplies
`credentials.password` in the profile, and `device exec` still runs any command
the caller gives on the local machine. Both are CLI-only and not reachable
through MCP.
