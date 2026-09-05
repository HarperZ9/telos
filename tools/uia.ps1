# Telos native app control via Windows UI Automation.
#
# Most verbs act through UIA patterns (InvokePattern, ValuePattern, SetFocus),
# which dispatch into the target process WITHOUT moving the mouse or keyboard.
# Two verbs do not: 'input' and 'type' synthesise keystrokes into whatever
# window currently holds focus, and they are marked FOREGROUND below and in
# their responses.
#
# JSON in via args, JSON out on stdout, always exit 0. Every answer carries an
# 'ok' field; a failure carries 'error'. Verbs:
#   windows
#   tree <windowMatch> [maxElements]
#   invoke <windowMatch> <elementMatch>
#   setvalue <windowMatch> <elementMatch> <text>
#   focus <windowMatch>
#   value <windowMatch> <elementMatch>
#   input <keys>                        FOREGROUND key synthesis
#   type <text>                         FOREGROUND key synthesis
#   selftest
#
# A <match> resolves exact name first, then exact AutomationId, then a unique
# case-insensitive substring. A match landing on more than one candidate is
# refused as ambiguous at EVERY rung and lists what it matched, because
# returning whichever element the tree walk reached first is an arbitrary answer
# the caller cannot tell from a correct one. Duplicate exact names are not
# hypothetical: two top-level windows on this machine share the name of the
# executable that owns them.
#
# 'tree' says whether its listing settles a question of absence. A walk stopped
# at maxElements is 'truncated'. A walk that completed and found no named
# element at all is 'opaque', because a window whose content sits behind a
# provider boundary reads here exactly like an empty window: Windows 11 File
# Explorer answers one anonymous Pane and nothing under it. 'settlesAbsence' is
# false for either, and a caller must not read a name missing from such a
# listing as a control that is not there.

$ErrorActionPreference = "Stop"

# One list, used by the unknown-verb answer and checked against the header
# comment above by demo/uia-script.test.mjs. A second hand-typed copy is
# how the header drifted to five verbs while the file implemented eight.
$VERBS = @("windows", "tree", "invoke", "setvalue", "focus", "value", "input", "type", "selftest")

# Total argv length each verb needs, including the verb itself. Checked before
# dispatch so a missing argument answers in JSON: without it $args[1] is $null,
# .ToLower() on it throws, and the caller parsing stdout gets a PowerShell stack
# trace where the contract promises an object.
$ARITY = @{ windows = 1; tree = 2; invoke = 3; setvalue = 4; focus = 2; value = 3; input = 2; type = 2; selftest = 1 }

# stdout carries JSON, so the stream has to be UTF-8 whatever the console
# codepage is. Without this the host writes control names in the codepage, a
# name outside it is replaced or dropped, and the caller JSON.parse fails on
# bytes that are no longer valid UTF-8. Guarded, because a redirected or
# absent console can refuse the assignment and that must not take the helper
# down: the worst case is the old behaviour, not a crash.
try {
  $utf8 = New-Object System.Text.UTF8Encoding $false
  [Console]::OutputEncoding = $utf8
  $OutputEncoding = $utf8
} catch { }

function Out-Json($obj) { Write-Output ($obj | ConvertTo-Json -Depth 6 -Compress) }

# Choose one candidate for a match string. Pure: plain records in, a decision
# out, no UIA and no process state, so 'selftest' exercises it anywhere.
# Each record is @{ index = <int>; name = <string>; automationId = <string> }.
function Select-Candidate($candidates, $match) {
  if ($null -eq $match -or "$match" -eq "") { return @{ status = "invalid"; reason = "empty match" } }
  $named = @($candidates | Where-Object { $_.name -eq $match })
  if ($named.Count -eq 1) { return @{ status = "ok"; index = $named[0].index; how = "name-exact" } }
  if ($named.Count -gt 1) { return (New-Ambiguity $named "name-exact") }
  $ided = @($candidates | Where-Object { $_.automationId -and $_.automationId -eq $match })
  if ($ided.Count -eq 1) { return @{ status = "ok"; index = $ided[0].index; how = "automationid-exact" } }
  if ($ided.Count -gt 1) { return (New-Ambiguity $ided "automationid-exact") }
  $needle = "$match".ToLowerInvariant()
  $sub = @($candidates | Where-Object { $_.name -and $_.name.ToLowerInvariant().Contains($needle) })
  if ($sub.Count -eq 1) { return @{ status = "ok"; index = $sub[0].index; how = "name-substring-unique" } }
  if ($sub.Count -gt 1) { return (New-Ambiguity $sub "name-substring") }
  return @{ status = "none" }
}

# Whether a 'tree' listing settles a question of absence. Pure, so 'selftest'
# gates it on any machine: this is the bit a caller leans on to turn 'the name
# is not in the listing' into 'the control is not in the window', and the
# expensive mistake is reading a walk that saw nothing as a window holding
# nothing.
function Test-SettlesAbsence($named, $truncated) {
  return ((-not $truncated) -and ($named -gt 0))
}

# What could narrow this match, read off the candidates rather than assumed from
# the rung. 'use an AutomationId' is useless advice for two windows that have
# none, and this refusal is the only place a caller learns what it can do next.
function Get-Hint($hits, $how) {
  if ($how -eq "name-substring") { return "use an exact name or AutomationId" }
  $same = if ($how -eq "name-exact") { "names" } else { "AutomationIds" }
  $try = if ($how -eq "name-exact") { "automationId" } else { "name" }
  $distinct = @($hits | ForEach-Object { $_.$try } | Where-Object { $_ } | Select-Object -Unique)
  if ($distinct.Count -eq $hits.Count) {
    $label = if ($try -eq "name") { "names" } else { "AutomationIds" }
    return "the $same are identical; match one of the $label listed instead"
  }
  return "nothing in this listing tells these apart; narrow by another route"
}

# One refusal shape for all three rungs. Candidates carry the AutomationId where
# there is one: for a duplicate exact name the name is what the caller already
# supplied, so repeating it back says nothing about how to narrow the match.
function New-Ambiguity($hits, $how) {
  return @{ status = "ambiguous"; how = $how; matches = $hits.Count
            hint = (Get-Hint $hits $how)
            candidates = @($hits | Select-Object -First 10 | ForEach-Object {
              if ($_.automationId) { "$($_.name) [$($_.automationId)]" } else { "$($_.name)" } }) }
}

# Turn a Select-Candidate refusal into the JSON error body for a subject.
function Deny-Body($decision, $subject, $match) {
  switch ($decision.status) {
    "invalid"   { return @{ ok = $false; error = "$subject match is empty" } }
    "ambiguous" { return @{ ok = $false; error = "$subject match is ambiguous: $match"
                            matched = $decision.matches; candidates = $decision.candidates
                            rung = $decision.how; hint = $decision.hint } }
    default     { return @{ ok = $false; error = "$subject not found: $match" } }
  }
}

try {
  Add-Type -AssemblyName UIAutomationClient
  Add-Type -AssemblyName UIAutomationTypes
} catch {
  Out-Json @{ ok = $false; error = "UIAutomation assemblies unavailable: $($_.Exception.Message)" }
  exit 0
}

$AE = [System.Windows.Automation.AutomationElement]
$Scope = [System.Windows.Automation.TreeScope]
$CTns = [System.Windows.Automation.ControlType]
$TrueCond = [System.Windows.Automation.Condition]::TrueCondition

function Get-TopWindows {
  $root = $AE::RootElement
  $cond = New-Object System.Windows.Automation.PropertyCondition($AE::ControlTypeProperty, $CTns::Window)
  return $root.FindAll($Scope::Children, $cond)
}

# Read a UIA collection into the plain records Select-Candidate consumes. One
# Name and AutomationId fetch per element, which is the cost a walking rung pays.
function Get-Records($collection) {
  $out = @()
  for ($i = 0; $i -lt $collection.Count; $i++) {
    $out += @{ index = $i; name = $collection[$i].Current.Name
               automationId = $collection[$i].Current.AutomationId }
  }
  return ,$out
}

# Resolve a top-level window. Returns @{ element = <el> } or a decision to deny.
function Find-Window($match) {
  $all = Get-TopWindows
  $d = Select-Candidate (Get-Records $all) $match
  if ($d.status -eq "ok") { return @{ element = $all[$d.index]; how = $d.how } }
  return @{ deny = $d }
}

# Resolve an element inside a window. The two exact rungs are answered by a UIA
# property search, so the common case never fetches a name per element; the
# substring rung pays for a full walk, which is why it is last. Each exact rung
# takes every hit rather than the first, because FindFirst on a name two
# controls share returns one of them and reports nothing about the other.
function Find-Element($window, $match) {
  if ($null -eq $match -or "$match" -eq "") { return @{ deny = @{ status = "invalid" } } }
  foreach ($rung in @(@{ prop = $AE::NameProperty; how = "name-exact" },
                      @{ prop = $AE::AutomationIdProperty; how = "automationid-exact" })) {
    $hits = $window.FindAll($Scope::Descendants,
      (New-Object System.Windows.Automation.PropertyCondition($rung.prop, $match)))
    if ($hits.Count -eq 1) { return @{ element = $hits[0]; how = $rung.how } }
    if ($hits.Count -gt 1) { return @{ deny = (New-Ambiguity (Get-Records $hits) $rung.how) } }
  }
  $all = $window.FindAll($Scope::Descendants, $TrueCond)
  $d = Select-Candidate (Get-Records $all) $match
  if ($d.status -eq "ok") { return @{ element = $all[$d.index]; how = $d.how } }
  return @{ deny = $d }
}

# Resolve window then element, carrying back which subject failed. It must not
# emit: Write-Output inside a function joins that function's return value, so
# an Out-Json here would be swallowed by the caller's assignment instead of
# reaching stdout. Only script scope writes the answer.
function Resolve-Target($windowMatch, $elementMatch) {
  $w = Find-Window $windowMatch
  if ($w.deny) { return @{ deny = $w.deny; subject = "window"; match = $windowMatch } }
  $e = Find-Element $w.element $elementMatch
  if ($e.deny) { return @{ deny = $e.deny; subject = "element"; match = $elementMatch } }
  return @{ window = $w.element; element = $e.element; how = $e.how }
}

$verb = if ($args.Count -ge 1) { $args[0] } else { "" }

if ($ARITY.ContainsKey($verb) -and $args.Count -lt $ARITY[$verb]) {
  Out-Json @{ ok = $false; error = "$verb needs $($ARITY[$verb] - 1) argument(s), got $($args.Count - 1)" }
  exit 0
}

# Everything the verbs touch is a live UIA provider in another process, and
# $ErrorActionPreference = "Stop" turns any exception one of them raises into a
# terminating error: a window closing mid-walk, a provider refusing access, a
# pattern call throwing. Unhandled, that leaves stdout empty and the process at
# exit 1, which is the one outcome the header promises never happens. Only the
# argument cast in 'tree' was ever observed doing it, and the guard there is
# specific for a specific reason; this is the net under the rest of the file.
try {
  switch ($verb) {
    "windows" {
      $list = @()
      foreach ($w in Get-TopWindows) {
        if ($w.Current.Name) { $list += @{ name = $w.Current.Name; class = $w.Current.ClassName } }
      }
      Out-Json @{ ok = $true; windows = $list }
    }
    "tree" {
      # The arity table catches a MISSING argument. A malformed one reached the
      # cast, which throws under $ErrorActionPreference = "Stop" and leaves stdout
      # empty with exit 1, breaking the contract this file opens with. A negative
      # ceiling was worse than a crash: it answered ok with an empty listing.
      #
      # Read before the window is resolved, so an unusable argument is named as
      # what it is. Resolving first answers 'window not found' for a caller whose
      # real mistake was the ceiling, and that reading depends on which windows
      # happen to be open.
      $max = 300
      if ($args.Count -ge 3) {
        $parsed = 0
        if (-not [int]::TryParse("$($args[2])", [ref]$parsed) -or $parsed -lt 1) {
          Out-Json @{ ok = $false; error = "tree maxElements must be a positive integer: $($args[2])" }
          break
        }
        $max = $parsed
      }
      $w = Find-Window $args[1]
      if ($w.deny) { Out-Json (Deny-Body $w.deny "window" $args[1]); break }
      $all = $w.element.FindAll($Scope::Descendants, $TrueCond)
      $els = @(); $count = 0; $truncated = $false
      foreach ($e in $all) {
        if ($count -ge $max) { $truncated = $true; break }
        $n = $e.Current.Name; $a = $e.Current.AutomationId
        if ($n -or $a) {
          $els += @{ name = $n; type = $e.Current.ControlType.ProgrammaticName; automationId = $a }
          $count++
        }
      }
      # 'descendants' counts every element in the subtree, named or not, so it is
      # an upper bound on a complete listing rather than the exact number held
      # back. It is free here because the collection is already in hand, and it
      # is what tells a caller that count=300 is a ceiling and not a total.
      #
      # 'opaque' is the other way this listing fails to settle absence, and it is
      # the quiet one: the walk finished, nothing was cut, and no element carried
      # a name. Read alone, count=0 with truncated=false says the window holds no
      # such control. It equally says the walk could not see in. 'settlesAbsence'
      # collapses both into the one bit a caller needs before treating a name it
      # cannot find as a control that is not there.
      Out-Json @{ ok = $true; window = $w.element.Current.Name; count = $count
                  descendants = $all.Count; truncated = $truncated; opaque = ($count -eq 0)
                  settlesAbsence = (Test-SettlesAbsence $count $truncated)
                  max = $max; elements = $els }
    }
    "invoke" {
      $t = Resolve-Target $args[1] $args[2]
      if ($t.deny) { Out-Json (Deny-Body $t.deny $t.subject $t.match); break }
      $pattern = $null
      if ($t.element.TryGetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern, [ref]$pattern)) {
        $pattern.Invoke()
        Out-Json @{ ok = $true; invoked = $t.element.Current.Name; matched = $t.how }
      } else {
        Out-Json @{ ok = $false; error = "element has no InvokePattern: $($args[2])" }
      }
    }
    "setvalue" {
      $t = Resolve-Target $args[1] $args[2]
      if ($t.deny) { Out-Json (Deny-Body $t.deny $t.subject $t.match); break }
      $pattern = $null
      if ($t.element.TryGetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern, [ref]$pattern)) {
        $t.element.SetFocus()
        $pattern.SetValue($args[3])
        Out-Json @{ ok = $true; set = $t.element.Current.Name; matched = $t.how }
      } else {
        Out-Json @{ ok = $false; error = "element has no ValuePattern: $($args[2])" }
      }
    }
    "focus" {
      $w = Find-Window $args[1]
      if ($w.deny) { Out-Json (Deny-Body $w.deny "window" $args[1]); break }
      $w.element.SetFocus()
      Out-Json @{ ok = $true; focused = $w.element.Current.Name; matched = $w.how }
    }
    "value" {
      $t = Resolve-Target $args[1] $args[2]
      if ($t.deny) { Out-Json (Deny-Body $t.deny $t.subject $t.match); break }
      $pattern = $null
      $v = $null
      if ($t.element.TryGetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern, [ref]$pattern)) {
        $v = $pattern.Current.Value
      }
      Out-Json @{ ok = $true; name = $t.element.Current.Name; matched = $t.how
                  type = $t.element.Current.ControlType.ProgrammaticName; value = $v }
    }
    "input" {
      # FOREGROUND key synthesis: SendKeys goes to whatever window holds focus
      # right now, not to a window this call names. UIA patterns cannot actuate
      # every control, and this is the no-CDP path for the ones they cannot.
      # Caller focuses the target first (verb 'focus') and escapes SendKeys
      # specials (+ ^ % ~ ( ) { } -> wrap each in {}).
      Add-Type -AssemblyName System.Windows.Forms -ErrorAction SilentlyContinue
      $keys = $args[1]
      if (-not $keys) { Out-Json @{ ok = $false; error = "input: no keys" }; break }
      [System.Windows.Forms.SendKeys]::SendWait($keys)
      Out-Json @{ ok = $true; sent = $keys; foreground = $true }
    }
    "type" {
      # FOREGROUND arbitrary-text input, same focus caveat as 'input'. Escapes
      # SendKeys specials so literal text arrives literally. SendKeys carries no
      # general Unicode path, so characters outside the active keyboard layout
      # are not guaranteed to arrive: use 'setvalue' where a ValuePattern exists.
      Add-Type -AssemblyName System.Windows.Forms -ErrorAction SilentlyContinue
      $text = $args[1]
      $esc = ""
      foreach ($ch in "$text".ToCharArray()) {
        if ($ch -match '[+%^~(){}]') { $esc += "{$ch}" } else { $esc += $ch }
      }
      [System.Windows.Forms.SendKeys]::SendWait($esc)
      Out-Json @{ ok = $true; chars = "$text".Length; foreground = $true }
    }
    "selftest" {
      # Falsifiable, offline, no window required: drives Select-Candidate over
      # synthetic records. Case 2 is the regression for the defect this file
      # carried, where a substring matching several controls returned whichever
      # one the walk reached first and the caller could not tell.
      $c = @(
        @{ index = 0; name = "Save"; automationId = "btnSave" },
        @{ index = 1; name = "Save As..."; automationId = "btnSaveAs" },
        @{ index = 2; name = "Cancel"; automationId = "btnCancel" },
        @{ index = 3; name = $null; automationId = "idOnly" }
      )
      # Duplicates on the EXACT rungs, which the substring cases above cannot
      # reach. Two top-level windows sharing an executable name is the observed
      # instance; the shared AutomationId is the same defect one rung down.
      $dup = @(
        @{ index = 0; name = "tor.exe"; automationId = $null },
        @{ index = 1; name = "tor.exe"; automationId = $null },
        @{ index = 2; name = "First"; automationId = "shared" },
        @{ index = 3; name = "Second"; automationId = "shared" },
        @{ index = 4; name = "Open"; automationId = "openTop" },
        @{ index = 5; name = "Open"; automationId = "openBottom" }
      )
      $cases = @(
        @{ case = "exact name beats a longer substring match"; got = (Select-Candidate $c "Save"); want = "ok"; how = "name-exact"; index = 0 },
        @{ case = "substring matching two controls is refused"; got = (Select-Candidate $c "Sav"); want = "ambiguous" },
        @{ case = "substring matching one control resolves"; got = (Select-Candidate $c "ance"); want = "ok"; how = "name-substring-unique"; index = 2 },
        @{ case = "AutomationId resolves when no name matches"; got = (Select-Candidate $c "idOnly"); want = "ok"; how = "automationid-exact"; index = 3 },
        @{ case = "no match reports none"; got = (Select-Candidate $c "nothing here"); want = "none" },
        @{ case = "empty match is invalid, not a null crash"; got = (Select-Candidate $c ""); want = "invalid" },
        @{ case = "null match is invalid, not a null crash"; got = (Select-Candidate $c $null); want = "invalid" },
        @{ case = "two candidates with one exact name is refused"; got = (Select-Candidate $dup "tor.exe"); want = "ambiguous"; how = "name-exact" },
        @{ case = "two candidates with one exact AutomationId is refused"; got = (Select-Candidate $dup "shared"); want = "ambiguous"; how = "automationid-exact" },
        @{ case = "duplicate names with distinct ids point at the ids"; got = (Select-Candidate $dup "Open"); want = "ambiguous"; hint = "the names are identical; match one of the AutomationIds listed instead" },
        @{ case = "duplicate ids with distinct names point at the names"; got = (Select-Candidate $dup "shared"); want = "ambiguous"; hint = "the AutomationIds are identical; match one of the names listed instead" },
        @{ case = "candidates nothing tells apart are not sent after a field they lack"; got = (Select-Candidate $dup "tor.exe"); want = "ambiguous"; hint = "nothing in this listing tells these apart; narrow by another route" }
      )
      # Both clauses of the absence bit, driven directly. The second is the one
      # that shipped wrong: a walk that completed and saw nothing named read as
      # a window holding nothing, which is how an unreadable window answers a
      # question it never saw.
      $absence = @(
        @{ case = "a whole listing with names settles absence"; got = (Test-SettlesAbsence 12 $false); want = $true },
        @{ case = "a clipped listing does not settle absence"; got = (Test-SettlesAbsence 12 $true); want = $false },
        @{ case = "a whole listing with nothing named does not settle absence"; got = (Test-SettlesAbsence 0 $false); want = $false }
      )
      $results = @(); $failed = 0
      foreach ($k in $cases) {
        $ok = $k.got.status -eq $k.want
        if ($ok -and $k.ContainsKey("how")) { $ok = $k.got.how -eq $k.how }
        if ($ok -and $k.ContainsKey("index")) { $ok = $k.got.index -eq $k.index }
        if ($ok -and $k.ContainsKey("hint")) { $ok = $k.got.hint -eq $k.hint }
        if (-not $ok) { $failed++ }
        $results += @{ case = $k.case; pass = $ok; status = $k.got.status; how = $k.got.how }
      }
      foreach ($k in $absence) {
        $ok = ($k.got -eq $k.want)
        if (-not $ok) { $failed++ }
        $results += @{ case = $k.case; pass = $ok; status = "$($k.got)"; how = "settles-absence" }
      }
      Out-Json @{ ok = ($failed -eq 0); cases = $results.Count; failed = $failed; results = $results }
    }
    default {
      Out-Json @{ ok = $false; error = "unknown verb: $verb"; verbs = $VERBS }
    }
  }
} catch {
  Out-Json @{ ok = $false; error = "$verb failed: $($_.Exception.Message)"
              verb = $verb; exception = $_.Exception.GetType().Name }
}

exit 0
