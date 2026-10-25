@echo off
REM ============================================================================
REM  start_server.bat  -- 一键重启本地服务（先杀掉占用 5050 的旧实例，再启动）
REM
REM  为什么需要它：app.py 启动时会检查 5050 端口，若已被占用会直接
REM    [FATAL] Port 5050 is already in use. Service NOT started.
REM  并 sys.exit(1) —— 这是故意的（防止"多实例静默共存 → 改了代码看不到效果"）。
REM  所以「改了代码 → 再跑一次 python app.py」是【无效】的：新进程秒退，
REM  老进程继续对外服务，前端永远看到旧接口（例如 /api/finance/cn-report/* 一直 404）。
REM  本脚本就是那段报错里提示的 Fix。
REM
REM  用法：双击本文件；或在 cmd 里执行 start_server.bat
REM  说明：纯 ASCII 输出，避免任何控制台编码环境下乱码。
REM ============================================================================
setlocal
cd /d "%~dp0"
set PORT=5050
set PYEXE=python

echo [start_server] workdir = %CD%
echo [start_server] checking port %PORT% ...

set KILLED=0
for /f "tokens=5" %%p in ('netstat -ano ^| findstr ":%PORT%" ^| findstr "LISTENING"') do (
    echo [start_server] killing old instance PID=%%p on port %PORT%
    taskkill /F /PID %%p >nul 2>&1
    set KILLED=1
)
if "%KILLED%"=="1" (
    echo [start_server] old instance killed, waiting 1s ...
    timeout /t 1 /nobreak >nul
) else (
    echo [start_server] port %PORT% is free.
)

echo [start_server] starting %PYEXE% app.py ...
%PYEXE% app.py

echo.
echo [start_server] server exited. press any key to close.
pause >nul
endlocal
