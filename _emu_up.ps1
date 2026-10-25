$ErrorActionPreference = 'Continue'
$log = 'c:\vnchoicedouble\_emu_up.log'
function L($m) { $t = Get-Date -Format 'HH:mm:ss'; Add-Content -Path $log -Value "$t  $m" -Encoding UTF8 }
if (Test-Path $log) { Remove-Item $log -Force }
L 'start'

$emu = Join-Path $env:LOCALAPPDATA 'Android\Sdk\emulator\emulator.exe'
$adb = Join-Path $env:LOCALAPPDATA 'Android\Sdk\platform-tools\adb.exe'

# 1) 启动（必须 Start-Process，否则阻塞 PowerShell；且不能用管道接住 stdout）
if (-not (Get-Process -Name 'qemu-system-x86_64' -ErrorAction SilentlyContinue)) {
  Start-Process -FilePath $emu -ArgumentList '-avd','test35','-no-snapshot-load'
  L 'emulator start requested'
} else { L 'emulator already running' }

for ($i = 0; $i -lt 60; $i++) {
  $out = (& $adb devices) -join ' '
  if ($out -match 'device\s*$' -or $out -like '*emulator-*device*') { break }
  Start-Sleep -Seconds 2
}
L 'device online'

for ($i = 0; $i -lt 120; $i++) {
  $b = (& $adb shell getprop sys.boot_completed 2>$null) -join ''
  if ($b -match '1') { break }
  Start-Sleep -Seconds 2
}
L ("boot=" + ((& $adb shell getprop sys.boot_completed) -join ''))

& $adb shell cmd connectivity airplane-mode disable | Out-Null
& $adb shell svc wifi enable | Out-Null
& $adb shell settings put system accelerometer_rotation 1 | Out-Null   # 自动转屏
& $adb shell settings put system user_rotation 0 | Out-Null
Start-Sleep -Seconds 6
L ("airplane=" + ((& $adb shell settings get global airplane_mode_on) -join '') + " size=" + ((& $adb shell wm size) -join ''))

$ins = & $adb install -r 'c:\vnchoicedouble\android-app\android\app\build\outputs\apk\debug\app-debug.apk' 2>&1
L ('install: ' + (($ins | Select-Object -Last 1) -join ''))

& $adb shell am start -n com.choicelats.pm/.MainActivity | Out-Null
Start-Sleep -Seconds 14
& $adb shell screencap -p /sdcard/emu_dash.png | Out-Null
& $adb pull /sdcard/emu_dash.png 'c:\vnchoicedouble\_emu_dash.png' | Out-Null
L 'screenshot saved'

$center = powershell -ExecutionPolicy Bypass -File 'c:\vnchoicedouble\_emu_portrait.ps1' 2>&1
foreach ($l in $center) { L $l }
L 'done'
