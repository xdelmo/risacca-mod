# Scrive ogni testo in console SENZA Invio, fotografa i suggerimenti, cancella e chiude.
param([string[]]$Texts, [string]$Name = "peek")
$t = $PSScriptRoot
& "$t\run.ps1" -Name "_noop" -Shots 0 | Out-Null
$p = Get-Process isaac-ng | Select-Object -First 1
[K3]::SetForegroundWindow($p.MainWindowHandle) | Out-Null
Start-Sleep -Milliseconds 200
$n = 0
foreach ($x in $Texts) {
  if ([K3]::GetForegroundWindow() -ne $p.MainWindowHandle) { "FERMO: il gioco non e' in primo piano"; exit 2 }
  $n++
  [K3]::Hold(0x29, 60); Start-Sleep -Milliseconds 200
  [K3]::Text($x); Start-Sleep -Milliseconds 300
  & "$t\shot.ps1" -Out "$t\$Name-$n.png" | Out-Null
  for ($i = 0; $i -lt $x.Length; $i++) { [K3]::Hold(0x0E, 20) }
  [K3]::Hold(0x01, 60); Start-Sleep -Milliseconds 150
  "$n = $x"
}
