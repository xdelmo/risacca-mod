param([string]$Name, [int]$Count, [int]$Cols = 3, [string]$Out)
Add-Type -AssemblyName System.Drawing
$t = $PSScriptRoot
$w = 512; $h = 304
$rows = [math]::Ceiling($Count / $Cols)
$m = New-Object System.Drawing.Bitmap ($w * $Cols), ($h * $rows)
$g = [System.Drawing.Graphics]::FromImage($m)
for ($i = 0; $i -lt $Count; $i++) {
  $s = [System.Drawing.Image]::FromFile("$t\$Name-$($i+1).png")
  $g.DrawImage($s, ($i % $Cols) * $w, [math]::Floor($i / $Cols) * $h, $w, $h)
  $s.Dispose()
}
$m.Save("$t\$Out", [System.Drawing.Imaging.ImageFormat]::Png)
"foglio: $Out"
