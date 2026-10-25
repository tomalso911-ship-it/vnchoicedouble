$p = Get-CimInstance Win32_Process -Filter "Name='python.exe'"
foreach ($proc in $p) {
    if ($proc.CommandLine -like '*_fin_build_trilingual*') {
        Write-Host ("Killing migration PID " + $proc.ProcessId)
        Stop-Process -Id $proc.ProcessId -Force
    }
}
Write-Host "done"
