# Telos native app control via Windows UI Automation.
#
# Acts on controls through UIA patterns (InvokePattern, ValuePattern, SetFocus),
# which dispatch into the target process WITHOUT moving the mouse or keyboard.
# JSON in via args, JSON out on stdout. Verbs:
#   windows
#   tree <windowMatch> [maxElements]
#   invoke <windowMatch> <elementMatch>
#   setvalue <windowMatch> <elementMatch> <text>
#   focus <windowMatch>

$ErrorActionPreference = "Stop"

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
try {
  Add-Type -AssemblyName UIAutomationClient
  Add-Type -AssemblyName UIAutomationTypes
} catch {
  Write-Output (@{ ok = $false; error = "UIAutomation assemblies unavailable: $($_.Exception.Message)" } | ConvertTo-Json -Compress)
  exit 0
}

$AE = [System.Windows.Automation.AutomationElement]
$Scope = [System.Windows.Automation.TreeScope]
$CTns = [System.Windows.Automation.ControlType]

function Out-Json($obj) { Write-Output ($obj | ConvertTo-Json -Depth 6 -Compress) }

function Get-TopWindows {
  $root = $AE::RootElement
  $cond = New-Object System.Windows.Automation.PropertyCondition($AE::ControlTypeProperty, $CTns::Window)
  return $root.FindAll($Scope::Children, $cond)
}

function Find-Window($match) {
  foreach ($w in Get-TopWindows) {
    $n = $w.Current.Name
    if ($n -and ($n -eq $match)) { return $w }
  }
  foreach ($w in Get-TopWindows) {
    $n = $w.Current.Name
    if ($n -and ($n.ToLower().Contains($match.ToLower()))) { return $w }
  }
  return $null
}

function Find-Element($window, $match) {
  $cond = New-Object System.Windows.Automation.PropertyCondition($AE::NameProperty, $match)
  $hit = $window.FindFirst($Scope::Descendants, $cond)
  if ($hit) { return $hit }
  $all = $window.FindAll($Scope::Descendants, [System.Windows.Automation.Condition]::TrueCondition)
  foreach ($e in $all) {
    $n = $e.Current.Name; $a = $e.Current.AutomationId
    if (($n -and $n.ToLower().Contains($match.ToLower())) -or ($a -and $a -eq $match)) { return $e }
  }
  return $null
}

$verb = if ($args.Count -ge 1) { $args[0] } else { "" }

switch ($verb) {
  "windows" {
    $list = @()
    foreach ($w in Get-TopWindows) {
      if ($w.Current.Name) { $list += @{ name = $w.Current.Name; class = $w.Current.ClassName } }
    }
    Out-Json @{ ok = $true; windows = $list }
  }
  "tree" {
    $win = Find-Window $args[1]
    if (-not $win) { Out-Json @{ ok = $false; error = "window not found: $($args[1])" }; break }
    $max = if ($args.Count -ge 3) { [int]$args[2] } else { 300 }
    $all = $win.FindAll($Scope::Descendants, [System.Windows.Automation.Condition]::TrueCondition)
    $els = @(); $count = 0
    foreach ($e in $all) {
      if ($count -ge $max) { break }
      $n = $e.Current.Name; $a = $e.Current.AutomationId
      if ($n -or $a) {
        $els += @{ name = $n; type = $e.Current.ControlType.ProgrammaticName; automationId = $a }
        $count++
      }
    }
    Out-Json @{ ok = $true; window = $win.Current.Name; count = $count; elements = $els }
  }
  "invoke" {
    $win = Find-Window $args[1]
    if (-not $win) { Out-Json @{ ok = $false; error = "window not found: $($args[1])" }; break }
    $el = Find-Element $win $args[2]
    if (-not $el) { Out-Json @{ ok = $false; error = "element not found: $($args[2])" }; break }
    $pattern = $null
    if ($el.TryGetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern, [ref]$pattern)) {
      $pattern.Invoke()
      Out-Json @{ ok = $true; invoked = $el.Current.Name }
    } else {
      Out-Json @{ ok = $false; error = "element has no InvokePattern: $($args[2])" }
    }
  }
  "setvalue" {
    $win = Find-Window $args[1]
    if (-not $win) { Out-Json @{ ok = $false; error = "window not found: $($args[1])" }; break }
    $el = Find-Element $win $args[2]
    if (-not $el) { Out-Json @{ ok = $false; error = "element not found: $($args[2])" }; break }
    $pattern = $null
    if ($el.TryGetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern, [ref]$pattern)) {
      $el.SetFocus()
      $pattern.SetValue($args[3])
      Out-Json @{ ok = $true; set = $el.Current.Name }
    } else {
      Out-Json @{ ok = $false; error = "element has no ValuePattern: $($args[2])" }
    }
  }
  "focus" {
    $win = Find-Window $args[1]
    if (-not $win) { Out-Json @{ ok = $false; error = "window not found: $($args[1])" }; break }
    $win.SetFocus()
    Out-Json @{ ok = $true; focused = $win.Current.Name }
  }
  "value" {
    $win = Find-Window $args[1]
    if (-not $win) { Out-Json @{ ok = $false; error = "window not found: $($args[1])" }; break }
    $el = Find-Element $win $args[2]
    if (-not $el) { Out-Json @{ ok = $false; error = "element not found: $($args[2])" }; break }
    $pattern = $null
    $v = $null
    if ($el.TryGetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern, [ref]$pattern)) {
      $v = $pattern.Current.Value
    }
    Out-Json @{ ok = $true; name = $el.Current.Name; type = $el.Current.ControlType.ProgrammaticName; value = $v }
  }
  "input" {
    # FOREGROUND key synthesis: sends SendKeys to the currently focused element.
    # Caller is responsible for focusing the target window/element first (verb:
    # 'focus') and for SendKeys escaping (+ ^ % ~ ( ) { } -> wrap each in {}).
    # This is the no-CDP path that reaches controls UIA patterns cannot actuate.
    Add-Type -AssemblyName System.Windows.Forms -ErrorAction SilentlyContinue
    $keys = if ($args.Count -ge 2) { $args[1] } else { "" }
    if (-not $keys) { Out-Json @{ ok = $false; error = "input: no keys" }; break }
    [System.Windows.Forms.SendKeys]::SendWait($keys)
    Out-Json @{ ok = $true; sent = $keys; foreground = $true }
  }
  "type" {
    # FOREGROUND arbitrary-text input: auto-escapes SendKeys special chars so any
    # literal text reaches the focused element. Focus the target first.
    Add-Type -AssemblyName System.Windows.Forms -ErrorAction SilentlyContinue
    $text = if ($args.Count -ge 2) { $args[1] } else { "" }
    $esc = ""
    foreach ($ch in $text.ToCharArray()) {
      if ($ch -match '[+%^~(){}]') { $esc += "{$ch}" } else { $esc += $ch }
    }
    [System.Windows.Forms.SendKeys]::SendWait($esc)
    Out-Json @{ ok = $true; chars = $text.Length; foreground = $true }
  }
  default {
    Out-Json @{ ok = $false; error = "unknown verb: $verb"; verbs = @("windows", "tree", "invoke", "setvalue", "focus", "value", "input", "type") }
  }
}
