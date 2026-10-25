# 把模拟器固定为竖屏，并按 1080x2400 比例把窗口调到最大可见尺寸并居中
$ErrorActionPreference = 'Continue'
Add-Type -AssemblyName System.Windows.Forms
Add-Type @'
using System;
using System.Runtime.InteropServices;
public class WinMove {
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr hWnd, out RECT lpRect);
  [DllImport("user32.dll")] public static extern bool SetWindowPos(IntPtr hWnd, IntPtr hAfter, int X, int Y, int cx, int cy, uint flags);
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
  [StructLayout(LayoutKind.Sequential)] public struct RECT { public int Left; public int Top; public int Right; public int Bottom; }
}
'@
$adb = Join-Path $env:LOCALAPPDATA 'Android\Sdk\platform-tools\adb.exe'

# 1) 强制竖屏
& $adb shell settings put system accelerometer_rotation 0
& $adb shell settings put system user_rotation 0
Start-Sleep -Seconds 3
Write-Output ('size=' + (& $adb shell wm size) + ' rot=' + (& $adb shell settings get system user_rotation))

# 2) 找窗口
$proc = $null
for ($i = 0; $i -lt 20; $i++) {
  $proc = Get-Process | Where-Object { ($_.MainWindowTitle -like '*Android Emulator*') -and $_.MainWindowHandle -ne 0 } | Select-Object -First 1
  if ($proc) { break }
  Start-Sleep -Seconds 1
}
if (-not $proc) { Write-Output 'WINDOW_NOT_FOUND'; exit 1 }
$h = $proc.MainWindowHandle

# 3) 目标尺寸：按设备比例(1080:2400)尽量占满可用高度(留 12px)
$wa = [System.Windows.Forms.Screen]::PrimaryScreen.WorkingArea
$hMax = $wa.Height - 12
$hT = $hMax
$wT = [int]($hT * 1080 / 2400)
if ($wT -gt ($wa.Width - 40)) { $t = ($wa.Width - 40) / $wT; $wT = [int]($wT * $t); $hT = [int]($hT * $t) }

[WinMove]::SetWindowPos($h, [IntPtr]::Zero, 0, 0, $wT, $hT, 0x0004) | Out-Null   # 改大小
Start-Sleep -Milliseconds 800
$x = [int](($wa.Width - $wT) / 2); if ($x -lt 0) { $x = 0 }
$y = [int](($wa.Height - $hT) / 2); if ($y -lt 0) { $y = 0 }
[WinMove]::SetWindowPos($h, [IntPtr]::Zero, $x, $y, 0, 0, 0x0001) | Out-Null    # 居中
[WinMove]::SetForegroundWindow($h) | Out-Null

$r = New-Object WinMove+RECT
[WinMove]::GetWindowRect($h, [ref]$r) | Out-Null
Write-Output ('title=' + $proc.MainWindowTitle)
Write-Output ('win=' + ($r.Right - $r.Left) + 'x' + ($r.Bottom - $r.Top) + " screen=" + $wa.Width + 'x' + $wa.Height)
Write-Output ('pos=' + $r.Left + ',' + $r.Top)
