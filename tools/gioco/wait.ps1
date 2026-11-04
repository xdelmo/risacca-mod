param([int]$Seconds = 45)
Add-Type @"
using System; using System.Runtime.InteropServices;
public class FW { [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow(); }
"@
$p = Get-Process isaac-ng | Select-Object -First 1
$end = (Get-Date).AddSeconds($Seconds)
while ((Get-Date) -lt $end) {
  if ([FW]::GetForegroundWindow() -eq $p.MainWindowHandle) { Start-Sleep -Seconds 2; "focus ok"; exit 0 }
  Start-Sleep -Milliseconds 300
}
"focus non arrivato"; exit 3
