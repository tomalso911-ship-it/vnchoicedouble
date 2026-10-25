# 启动安卓模拟器并把窗口移到屏幕正中间
# 用法：powershell -ExecutionPolicy Bypass -File _center_emulator.ps1
$ErrorActionPreference = 'Continue'
$emu = Join-Path $env:LOCALAPPDATA 'Android\Sdk\emulator\emulator.exe'
$adb = Join-Path $env:LOCALAPPDATA 'Android\Sdk\platform-tools\adb.exe'
$avd = 'test35'

Write-Output "AVD=$avd"

if (-not (Get-Process -Name 'qemu-system-x86_64' -ErrorAction SilentlyContinue)) {
  Write-Output 'emulator not running -> starting'
  Start-Process -FilePath $emu -ArgumentList '-avd', $avd, '-no-snapshot-load'
  Start-Sleep -Seconds 5
}

& $adb wait-for-device
for ($i = 0; $i -lt 120; $i++) {
  $boot = (& $adb shell getprop sys.boot_completed 2>$null)
  if ($boot -match '1') { break }
  Start-Sleep -Seconds 2
}
Write-Output ('boot_completed=' + (& $adb shell getprop sys.boot_completed))
try { & $adb shell cmd connectivity airplane-mode disable | Out-Null } catch {}
Start-Sleep -Seconds 4

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

$maxWait = 30
$proc = $null
for ($i = 0; $i -lt $maxWait; $i++) {
  $proc = Get-Process | Where-Object {
    ($_.MainWindowTitle -like "*$avd*" -or $_.MainWindowTitle -like '*Android Emulator*') -and $_.MainWindowHandle -ne 0
  } | Select-Object -First 1
  if ($proc) { break }
  Start-Sleep -Seconds 1
}

if (-not $proc) { Write-Output 'WARN: emulator window not found'; exit 0 }

$h = $proc.MainWindowHandle
$r = New-Object WinMove+RECT
[WinMove]::GetWindowRect($h, [ref]$r) | Out-Null
$w = $r.Right - $r.Left
$ht = $r.Bottom - $r.Top
$wa = [System.Windows.Forms.Screen]::PrimaryScreen.WorkingArea
$x = [int](($wa.Width - $w) / 2)
$y = [int](($wa.Height - $ht) / 2)
if ($x -lt 0) { $x = 0 }
if ($y -lt 0) { $y = 0 }

# SWP_NOSIZE=0x0001 不改变大小，只移动
[WinMove]::SetWindowPos($h, [IntPtr]::Zero, $x, $y, 0, 0, 0x0001) | Out-Null
[WinMove]::SetForegroundWindow($h) | Out-Null

Write-Output ("title=" + $proc.MainWindowTitle)
Write-Output ("winSize=" + $w + 'x' + $ht)
Write-Output ("screen=" + $wa.Width + 'x' + $wa.Height)
Write-Output ("movedTo=" + $x + ',' + $y)
