# TradingAgents-CN 启动脚本说明

## 📋 脚本文件

- `start_app.bat` - Windows 启动脚本
- `start_app.sh` - Linux/Mac 启动脚本
- `stop_app.bat` - Windows 停止脚本
- `stop_app.sh` - Linux/Mac 停止脚本

## 🚀 使用方法

### Windows 系统

1. **启动服务**
   - 双击运行 `start_app.bat`
   - 或在命令行中运行：`start_app.bat`

2. **停止服务**
   - 双击运行 `stop_app.bat`
   - 或在命令行中运行：`stop_app.bat`

### Linux/Mac 系统

1. **首次使用需要添加执行权限**
   ```bash
   chmod +x start_app.sh stop_app.sh
   ```

2. **启动服务**
   ```bash
   ./start_app.sh
   ```

3. **停止服务**
   ```bash
   ./stop_app.sh
   ```

## 🔧 脚本功能

### 启动脚本 (`start_app.bat` / `start_app.sh`)

1. **检查端口占用**
   - 检查 3000 端口是否被占用
   - 如果被占用，自动关闭占用该端口的进程

2. **启动后端服务**
   - 在项目根目录后台运行 `python -m app`
   - 日志输出到 `backend.log`

3. **启动前端服务**
   - 在 `frontend` 目录后台运行 `npm run dev`
   - 日志输出到 `frontend.log`

4. **显示服务地址**
   - 后端服务: http://localhost:8000
   - 前端服务: http://localhost:3000
   - API 文档: http://localhost:8000/docs

### 停止脚本 (`stop_app.bat` / `stop_app.sh`)

1. **停止前端服务**
   - 查找并关闭占用 3000 端口的进程

2. **停止后端服务**
   - 查找并关闭占用 8000 端口的进程

## 📝 日志文件

- `backend.log` - 后端服务日志
- `frontend.log` - 前端服务日志
- `backend.pid` - 后端进程 ID（Linux/Mac）
- `frontend.pid` - 前端进程 ID（Linux/Mac）

## ⚠️ 注意事项

1. **端口冲突**
   - 如果 3000 或 8000 端口被其他程序占用，脚本会尝试自动关闭
   - 如果无法关闭，请手动关闭占用端口的程序

2. **后台运行**
   - 服务在后台运行，关闭终端窗口不会停止服务
   - 使用停止脚本可以安全地关闭服务

3. **依赖检查**
   - 确保已安装 Python 和 Node.js
   - 确保已安装项目依赖（`pip install -r requirements.txt` 和 `npm install`）

4. **权限问题**（Linux/Mac）
   - 如果遇到权限问题，使用 `chmod +x` 添加执行权限
   - 某些系统可能需要使用 `sudo` 来关闭进程

## 🐛 故障排除

### Windows

1. **端口检查失败**
   - 手动检查端口：`netstat -ano | findstr :3000`
   - 手动关闭进程：`taskkill /F /PID <进程ID>`

2. **服务启动失败**
   - 检查 Python 是否在 PATH 中：`python --version`
   - 检查 Node.js 是否在 PATH 中：`node --version`
   - 查看日志文件：`backend.log` 和 `frontend.log`

### Linux/Mac

1. **端口检查失败**
   - 手动检查端口：`lsof -i :3000` 或 `netstat -tuln | grep :3000`
   - 手动关闭进程：`kill -9 <进程ID>`

2. **服务启动失败**
   - 检查 Python 是否在 PATH 中：`python --version` 或 `python3 --version`
   - 检查 Node.js 是否在 PATH 中：`node --version`
   - 查看日志文件：`backend.log` 和 `frontend.log`

3. **权限问题**
   - 确保脚本有执行权限：`chmod +x start_app.sh stop_app.sh`
   - 如果无法关闭进程，可能需要使用 `sudo`

