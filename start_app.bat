@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
set NO_PAUSE=0
if /i "%~1"=="--no-pause" set NO_PAUSE=1
echo ========================================
echo 云子量化 启动脚本
echo ========================================
echo.

REM 获取脚本所在目录
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM 检查并释放 3000/8000 端口
echo [1/4] 检查并释放端口占用情况...
call :kill_by_port 3000 前端
call :kill_by_port 8000 后端

REM 等待端口释放
timeout /t 2 /nobreak >nul
call :check_port_free 3000
call :check_port_free 8000

REM 启动后端服务
echo.
echo [2/4] 启动后端服务 (python -m app)...
start /B "" python -m app > backend.log 2>&1
if !errorlevel! equ 0 (
    echo ✅ 后端服务已在后台启动
) else (
    echo ⚠️  后端服务启动中，请查看 backend.log 确认状态
)

REM 等待后端启动
echo 等待后端服务启动...
timeout /t 5 /nobreak >nul

REM 启动前端服务
echo.
echo [3/4] 启动前端服务 (npm run dev)...
cd /d "%SCRIPT_DIR%\frontend"
start /B "" cmd /c "npm run dev > ..\frontend.log 2>&1"
echo ✅ 前端服务已在后台启动
echo ⚠️  如果启动失败，请查看 frontend.log 确认状态

REM 返回原目录
cd /d "%SCRIPT_DIR%"

echo.
echo [4/4] 启动完成！
echo ========================================
echo ✅ 后端服务: http://localhost:8000
echo ✅ 前端服务: http://localhost:3000
echo ✅ API 文档: http://localhost:8000/docs
echo ========================================
echo.
echo 📝 日志文件:
echo    - 后端日志: backend.log
echo    - 前端日志: frontend.log
echo.
echo 💡 提示: 关闭此窗口不会停止服务，如需停止服务请运行 stop_app.bat
echo.
if %NO_PAUSE%==0 pause

exit /b 0

:kill_by_port
set PORT=%~1
set SERVICE=%~2
set FOUND=0
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :%PORT% ^| findstr LISTENING') do (
    set PID=%%a
    echo 发现%SERVICE%端口 %PORT% 被进程占用，PID: %%a
    taskkill /F /PID %%a >nul 2>&1
    if !errorlevel! equ 0 (
        echo ✅ 已关闭 PID %%a
    ) else (
        echo ⚠️  关闭 PID %%a 失败，可能进程已不存在
    )
    set FOUND=1
)
if !FOUND! equ 0 (
    echo ✅ %SERVICE%端口 %PORT% 未被占用
)
exit /b 0

:check_port_free
set PORT=%~1
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :%PORT% ^| findstr LISTENING') do (
    echo ⚠️  端口 %PORT% 仍被占用，PID: %%a
    exit /b 0
)
echo ✅ 端口 %PORT% 已释放
exit /b 0

