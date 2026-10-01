# Telos device control: full-device read/write/execute (remote-desktop class).
#
# The device surface complements the UIA app surface: where app drives controls
# inside a target process via UI Automation, device drives the operating system
# itself (run a process, read/write files, list a directory). JSON out on stdout.
# Verbs:
#   exec <command>            run <command> via cmd /c, return combined output + exit
#   read <path> [maxBytes]    read a file as UTF-8 text (truncated to maxBytes, default 200000)
#   write <path> <text>       write <text> to <path> (overwrite, UTF-8, no trailing newline)
#   ls <path>                 list directory entries (name/type/KB)
#
# Safety: exec runs an arbitrary command string -- it is the operator-authorized
# "execute" primitive. The receipt records exactly what ran and its exit code.

$ErrorActionPreference = "Stop"

function Out-Json($obj) { Write-Output ($obj | ConvertTo-Json -Depth 6 -Compress) }

$verb = if ($args.Count -ge 1) { $args[0] } else { "" }

switch ($verb) {
  "exec" {
    $cmd = if ($args.Count -ge 2) { $args[1] } else { "" }
    if (-not $cmd) { Out-Json @{ ok = $false; error = "exec: no command" }; break }
    $out = & cmd.exe /c $cmd 2>&1
    $exit = $LASTEXITCODE
    $text = ($out | Out-String)
    Out-Json @{ ok = ($exit -eq 0); exit = $exit; command = $cmd; stdout = $text.Trim() }
  }
  "read" {
    $p = if ($args.Count -ge 2) { $args[1] } else { "" }
    $max = if ($args.Count -ge 3) { [int]$args[2] } else { 200000 }
    if (-not (Test-Path -LiteralPath $p)) { Out-Json @{ ok = $false; error = "read: not found: $p" }; break }
    $t = Get-Content -LiteralPath $p -Raw -Encoding UTF8
    if ($null -eq $t) { $t = "" }
    $truncated = $false
    if ($t.Length -gt $max) { $t = $t.Substring(0, $max); $truncated = $true }
    Out-Json @{ ok = $true; path = $p; length = $t.Length; truncated = $truncated; content = $t }
  }
  "write" {
    $p = if ($args.Count -ge 2) { $args[1] } else { "" }
    $text = if ($args.Count -ge 3) { $args[2] } else { "" }
    if (-not $p) { Out-Json @{ ok = $false; error = "write: no path" }; break }
    Set-Content -LiteralPath $p -Value $text -Encoding UTF8 -NoNewline
    Out-Json @{ ok = $true; path = $p; bytes = ([System.Text.Encoding]::UTF8.GetByteCount($text)) }
  }
  "ls" {
    $p = if ($args.Count -ge 2) { $args[1] } else { "." }
    if (-not (Test-Path -LiteralPath $p)) { Out-Json @{ ok = $false; error = "ls: not found: $p" }; break }
    $entries = @()
    foreach ($e in (Get-ChildItem -LiteralPath $p -Force -ErrorAction SilentlyContinue)) {
      $entries += @{ name = $e.Name; type = if ($e.PSIsContainer) { "dir" } else { "file" }; kb = [math]::Round(($e.Length / 1KB), 1) }
    }
    Out-Json @{ ok = $true; path = $p; count = $entries.Count; entries = $entries }
  }
  default {
    Out-Json @{ ok = $false; error = "unknown verb: $verb"; verbs = @("exec", "read", "write", "ls") }
  }
}
