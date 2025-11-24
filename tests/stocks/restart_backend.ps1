# 重启后端服务脚本

Write-Host "正在重启后端服务..." -ForegroundColor Green

# 查找并停止现有的 uvicorn 进程
$processes = Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -like "*uvicorn*"
}

if ($processes) {
    Write-Host "停止现有的后端进程..." -ForegroundColor Yellow
    $processes | Stop-Process -Force
    Start-Sleep -Seconds 2
}

# 切换到项目根目录
Set-Location F:\source_code\TradingAgents-CN

# 启动后端服务
Write-Host "启动后端服务..." -ForegroundColor Green
Write-Host "访问地址: http://localhost:8848" -ForegroundColor Cyan
Write-Host "API文档: http://localhost:8848/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "按 Ctrl+C 停止服务" -ForegroundColor Yellow
Write-Host ""

# 启动服务
uvicorn app.main:app --host 0.0.0.0 --port 8848 --reload
