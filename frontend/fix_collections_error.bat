@echo off
echo ========================================
echo 修复数据集合页面加载错误
echo ========================================
echo.

echo 1. 停止前端开发服务器（如果正在运行）
echo    请手动按 Ctrl+C 停止开发服务器
echo.

echo 2. 清理缓存和依赖
echo.
cd /d "%~dp0"

if exist "node_modules\.vite" (
    echo 删除 Vite 缓存...
    rmdir /s /q "node_modules\.vite"
    echo ✓ Vite 缓存已清理
) else (
    echo ✓ Vite 缓存目录不存在，无需清理
)

if exist "dist" (
    echo 删除构建产物...
    rmdir /s /q "dist"
    echo ✓ 构建产物已清理
) else (
    echo ✓ 构建目录不存在，无需清理
)

echo.
echo 3. 重启开发服务器
echo.
echo 请执行以下命令：
echo    npm run dev
echo.
echo 或者直接按任意键启动...
pause

npm run dev
