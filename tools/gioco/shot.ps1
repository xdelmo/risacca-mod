param([string]$Out = "$PSScriptRoot\shot.png")
Add-Type -AssemblyName System.Drawing
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class W {
  [StructLayout(LayoutKind.Sequential)] public struct RECT { public int L, T, R, B; }
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
}
"@
[W]::SetProcessDPIAware() | Out-Null
$p = Get-Process isaac-ng -ErrorAction SilentlyContinue | Select-Object -First 1
if (-not $p) { "gioco: processo isaac-ng non trovato"; Get-Process | Where-Object { $_.MainWindowTitle -match 'Isaac' } | ForEach-Object { "candidato: $($_.ProcessName) '$($_.MainWindowTitle)'" }; exit 1 }
$r = New-Object W+RECT
[W]::GetWindowRect($p.MainWindowHandle, [ref]$r) | Out-Null
$w = $r.R - $r.L; $h = $r.B - $r.T
"finestra: '$($p.MainWindowTitle)' ${w}x${h} a $($r.L),$($r.T); in primo piano: $([W]::GetForegroundWindow() -eq $p.MainWindowHandle)"
$b = New-Object System.Drawing.Bitmap $w, $h
$g = [System.Drawing.Graphics]::FromImage($b)
$g.CopyFromScreen($r.L, $r.T, 0, 0, $b.Size)
$b.Save($Out, [System.Drawing.Imaging.ImageFormat]::Png)
"salvato: $Out"
