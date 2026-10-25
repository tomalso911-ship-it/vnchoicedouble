# 把安卓模拟器窗口缩放 fitscreen 并移到屏幕正中间
$ErrorActionPreference = 'Continue'
Add-Type -AssemblyName System.Windows.Forms
Add-Type @'
using System;
using System.Runtime.InteropServices;
public class WinMove {
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr hWnd, out RECT lpRect);
  [DllImport("user32.dll")] public static extern bool SetWindowPos(IntPtr hWnd, IntPtr hWndAfter, int X, int Y, int cx, int cy, uint flags);
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
  [StructLayout(LayoutKind.Sequential)] public struct RECT { public int Left; public int Top; public int Right; public int Bottom; }
}
'@
$proc = Get-Process | Where-Object { ($_.MainWindowTitle -like '*Android Emulator*') -and $_.MainWindowHandle -ne 0 } | Select-Object -First 1
if (-not $proc) { Write-Output 'EMULATOR_WINDOW_NOT_FOUND'; exit 1 }
$h = $proc.MainWindowHandle
$r = New-Object WinMove+RECT
[WinMove]::GetWindowRect($h, [ref]$r) | Out-Null
$w = $r.Right - $r.Left
$ht = $r.Bottom - $r.Top
$wa = [System.Windows.Forms.Screen]::PrimaryScreen.WorkingArea

# 先按可用高度(留 16px)等比缩放（Android 12+ 模拟器窗口可自由改大小）
$maxH = $wa.Height - 16
if ($ht -gt $maxH) {
  $scale = $maxH / $ht
  $w = [int]($w * $scale)
  $ht = [int]($ht * $scale)
  [WinMove]::SetWindowPos($h, [IntPtr]::Zero, 0, 0, $w, $ht, 0x0004) | Out-Null   # SWP_NOZORDER：只改大小
  Start-Sleep -Milliseconds 600
}
$x = [int](($wa.Width - $w) / 2); if ($x -lt 0) { $x = 0 }
$y = [int](($wa.Height - $ht) / 2); if ($y -lt 0) { $y = 0 }
[WinMove]::SetWindowPos($h, [IntPtr]::Zero, $x, $y, 0, 0, 0x0001) | Out-Null      # SWP_NOSIZE：只移动
[WinMove]::SetForegroundWindow($h) | Out-Null

$r2 = New-Object WinMove+RECT
[WinMove]::GetWindowRect($h, [ref]$r2) | Out-Null
Write-Output ("title=" + $proc.MainWindowTitle)
Write-Output ("win=" + ($r2.Right - $r2.Left) + 'x' + ($r2.Bottom - $r2.Top) + " screen=" + $wa.Width + 'x' + $wa.Height)
Write-Output ("pos=" + $r2.Left + ',' + $r2.Top)
