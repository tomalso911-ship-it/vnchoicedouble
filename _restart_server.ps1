$ErrorActionPreference = 'Continue'
$root = 'c:\vnchoicedouble'
$out = Join-Path $root '_srv_out.log'
$err = Join-Path $root '_srv_err.log'
$log = Join-Path $root '_restart_out.txt'
Remove-Item $log -ErrorAction SilentlyContinue

function W($m) { $m | Tee-Object -FilePath $log -Append | Out-Null; Write-Host $m }
function PidsOn5050 {
    $res = @()
    foreach ($l in (netstat -ano | Select-String ':5050' | Select-String 'LISTENING')) {
        $parts = ($l.ToString().Trim() -split '\s+')
        $res += $parts[-1]
    }
    return ($res | Select-Object -Unique)
}

W ("=== restart at " + (Get-Date).ToString('yyyy-MM-dd HH:mm:ss'))
W ("app.py mtime = " + (Get-Item (Join-Path $root 'app.py')).LastWriteTime)

Copy-Item $out ($out + '.before_restart') -Force -ErrorAction SilentlyContinue
Copy-Item $err ($err + '.before_restart') -Force -ErrorAction SilentlyContinue

$old = PidsOn5050
W ("占用 5050 的 PID = " + ($old -join ', '))
foreach ($p in $old) {
    $ci = Get-CimInstance Win32_Process -Filter "ProcessId=$p" -ErrorAction SilentlyContinue
    W ("   杀掉 PID $p : " + $ci.CommandLine)
    Stop-Process -Id $p -Force -ErrorAction SilentlyContinue
}
Start-Sleep -Seconds 8

$after = PidsOn5050
if ($after.Count -gt 0) {
    W ("端口已被别的进程重新占上（可能是看门狗），PID = " + ($after -join ', ') + " → 不再自己启动")
} else {
    W "端口 5050 空闲，启动新实例 ..."
    $py = 'C:\Users\tomal\AppData\Local\Python\bin\python.exe'
    if (-not (Test-Path $py)) { $py = 'python' }
    Start-Process -FilePath $py -ArgumentList '-u', 'app.py' -WorkingDirectory $root `
        -RedirectStandardOutput $out -RedirectStandardError $err -WindowStyle Hidden
    Start-Sleep -Seconds 14
}

$now = PidsOn5050
$nowTxt = '无'
if ($now.Count -gt 0) { $nowTxt = ($now -join ', ') }
W ("现在监听 5050 的 PID = " + $nowTxt)
foreach ($p in (Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Where-Object { $_.CommandLine -like '*app.py*' })) {
    W ("   python PID " + $p.ProcessId + " 启动于 " + $p.CreationDate + "  cmd=" + $p.CommandLine)
}
W "=== 新 _srv_out.log 开头 ==="
if (Test-Path $out) { Get-Content $out -TotalCount 10 | ForEach-Object { W ("   " + $_) } }
W "=== 新 _srv_err.log 开头 ==="
if (Test-Path $err) { Get-Content $err -TotalCount 10 | ForEach-Object { W ("   " + $_) } }
W "done"
