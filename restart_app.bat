@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

echo ========================================
echo TradingAgents-CN 重启脚本
echo ========================================
echo.

REM 获取脚本所在目录
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

set STOP_SCRIPT=%SCRIPT_DIR%stop_app.bat
set START_SCRIPT=%SCRIPT_DIR%start_app.bat

if not exist "%STOP_SCRIPT%" (
    echo ❌ 未找到 stop_app.bat: %STOP_SCRIPT%
    exit /b 1
)

if not exist "%START_SCRIPT%" (
    echo ❌ 未找到 start_app.bat: %START_SCRIPT%
    exit /b 1
)

REM 1) 停止服务
echo [1/3] 停止服务...
call "%STOP_SCRIPT%" --no-pause

REM 2) 清空日志
echo.
echo [2/3] 清空日志...
(
  echo.
) > "%SCRIPT_DIR%error.log"
echo ✅ 已清空: error.log
(
  echo.
) > "%SCRIPT_DIR%frontend.log"
echo ✅ 已清空: frontend.log
(
  echo.
) > "%SCRIPT_DIR%backend.log"
echo ✅ 已清空: backend.log

REM 3) 启动服务
echo.
echo [3/3] 启动服务...
call "%START_SCRIPT%" --no-pause

echo.
echo ========================================
echo ✅ 重启完成
echo ========================================
echo.

pause
