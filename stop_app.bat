@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
echo ========================================
echo TradingAgents-CN 停止脚本
echo ========================================
echo.

REM 获取脚本所在目录
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM 停止前端服务（3000 端口）
echo [1/2] 停止前端服务 (端口 3000)...
set FRONTEND_FOUND=0
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3000 ^| findstr LISTENING') do (
    set PID=%%a
    echo 发现前端进程，PID: %%a
    taskkill /F /PID %%a >nul 2>&1
    if !errorlevel! equ 0 (
        echo ✅ 前端服务已停止
    ) else (
        echo ⚠️  停止前端服务失败
    )
    set FRONTEND_FOUND=1
    goto :frontend_stopped
)
if !FRONTEND_FOUND! equ 0 (
    echo ✅ 前端服务未运行
)
:frontend_stopped

REM 停止后端服务（8000 端口）
echo.
echo [2/2] 停止后端服务 (端口 8000)...
set BACKEND_FOUND=0
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    set PID=%%a
    echo 发现后端进程，PID: %%a
    taskkill /F /PID %%a >nul 2>&1
    if !errorlevel! equ 0 (
        echo ✅ 后端服务已停止
    ) else (
        echo ⚠️  停止后端服务失败
    )
    set BACKEND_FOUND=1
    goto :backend_stopped
)
if !BACKEND_FOUND! equ 0 (
    echo ✅ 后端服务未运行
)
:backend_stopped

echo.
echo ========================================
echo ✅ 所有服务已停止
echo ========================================
echo.
pause

