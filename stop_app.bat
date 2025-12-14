@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
set NO_PAUSE=0
if /i "%~1"=="--no-pause" set NO_PAUSE=1
echo ========================================
echo 云子量化 停止脚本
echo ========================================
echo.

REM 获取脚本所在目录
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM 停止前端服务（3000 端口）
echo [1/2] 停止前端服务 (端口 3000)...
call :kill_by_port 3000 前端

REM 停止后端服务（8000 端口）
echo.
echo [2/2] 停止后端服务 (端口 8000)...
call :kill_by_port 8000 后端

echo.
echo ========================================
echo ✅ 所有服务已停止
echo ========================================
echo.
if %NO_PAUSE%==0 pause

exit /b 0

:kill_by_port
set PORT=%~1
set SERVICE=%~2
set FOUND=0
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :%PORT% ^| findstr LISTENING') do (
    set PID=%%a
    echo 发现%SERVICE%进程，PID: %%a
    taskkill /F /PID %%a >nul 2>&1
    if !errorlevel! equ 0 (
        echo ✅ %SERVICE%进程已停止
    ) else (
        echo ⚠️  停止%SERVICE%进程失败
    )
    set FOUND=1
)
if !FOUND! equ 0 (
    echo ✅ %SERVICE%服务未运行
)
exit /b 0

