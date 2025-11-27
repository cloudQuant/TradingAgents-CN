@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
echo ========================================
echo TradingAgents-CN 启动脚本
echo ========================================
echo.

REM 获取脚本所在目录
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM 检查 3000 端口是否被占用
echo [1/4] 检查 3000 端口占用情况...
set PORT_FOUND=0
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3000 ^| findstr LISTENING') do (
    set PID=%%a
    echo 发现端口 3000 被进程占用，PID: %%a
    echo 正在关闭进程...
    taskkill /F /PID %%a >nul 2>&1
    if !errorlevel! equ 0 (
        echo ✅ 进程已关闭
    ) else (
        echo ⚠️  关闭进程失败，可能进程已不存在
    )
    set PORT_FOUND=1
    goto :port_found
)

if !PORT_FOUND! equ 0 (
    echo ✅ 端口 3000 未被占用
)
:port_found

REM 等待端口释放
timeout /t 2 /nobreak >nul

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
pause

