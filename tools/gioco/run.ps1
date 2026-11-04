# Uso: run.ps1 -Name x -Commands 'cmd1','cmd2' -Keys 57 -Shots 3 -EveryMs 700
# Esegue i comandi in console, chiude con Esc, preme i tasti (scancode) e scatta una serie di screenshot.
param([string]$Name = "t", [string[]]$Commands = @(), [int[]]$Keys = @(), [int]$HoldMs = 80, [int]$Shots = 3, [int]$EveryMs = 700, [int]$FirstMs = 150, [switch]$Freeze, [switch]$Thaw)
$t = $PSScriptRoot
if (-not ("K3" -as [type])) { Add-Type @"
using System;
using System.Runtime.InteropServices;
public class K3 {
  [StructLayout(LayoutKind.Sequential)] public struct KI { public ushort vk, scan; public uint flags, time; public IntPtr extra; }
  [StructLayout(LayoutKind.Explicit, Size=40)] public struct INPUT { [FieldOffset(0)] public uint type; [FieldOffset(8)] public KI ki; }
  [DllImport("user32.dll")] public static extern uint SendInput(uint n, INPUT[] i, int s);
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  public static void Send(ushort scan, uint flags) {
    var i = new INPUT[1]; i[0].type = 1; i[0].ki.scan = scan; i[0].ki.flags = flags;
    SendInput(1, i, Marshal.SizeOf(typeof(INPUT)));
  }
  public static void Hold(ushort s, int ms) { Send(s, 8); System.Threading.Thread.Sleep(ms); Send(s, 8 | 2); System.Threading.Thread.Sleep(60); }
  public static void Text(string t) { foreach (char c in t) { Send(c, 4); Send(c, 4 | 2); System.Threading.Thread.Sleep(25); } }
}
"@ }
$p = Get-Process isaac-ng | Select-Object -First 1
[K3]::SetForegroundWindow($p.MainWindowHandle) | Out-Null
Start-Sleep -Milliseconds 200
function Focus-OK { if ([K3]::GetForegroundWindow() -ne $p.MainWindowHandle) { "FERMO: il gioco non e' in primo piano"; exit 2 } }
if ($Thaw) { Focus-OK; [K3]::Hold(0x01, 60); Start-Sleep -Milliseconds 700 }
foreach ($c in $Commands) {
  Focus-OK
  [K3]::Hold(0x29, 60); Start-Sleep -Milliseconds 200
  Focus-OK
  [K3]::Text($c); Start-Sleep -Milliseconds 80
  [K3]::Hold(0x1C, 60); Start-Sleep -Milliseconds 150
  [K3]::Hold(0x01, 60); Start-Sleep -Milliseconds 700
  "inviato: $c"
}
foreach ($k in $Keys) { Focus-OK; [K3]::Hold([uint16]$k, $HoldMs) }
Start-Sleep -Milliseconds $FirstMs
for ($i = 1; $i -le $Shots; $i++) {
  & "$t\shot.ps1" -Out "$t\$Name-$i.png" | Out-Null
  if ($i -lt $Shots) { Start-Sleep -Milliseconds $EveryMs }
}
if ($Freeze) { Focus-OK; [K3]::Hold(0x29, 60) }  # console aperta = gioco fermo tra un turno e l'altro
"screenshot: $Name-1..$Shots"
