#!/bin/bash

# TradingAgents-CN 启动脚本

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "========================================"
echo "TradingAgents-CN 启动脚本"
echo "========================================"
echo ""

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 检查 3000 端口是否被占用
echo "[1/4] 检查 3000 端口占用情况..."

# 尝试使用 lsof 查找占用端口的进程
if command -v lsof >/dev/null 2>&1; then
    PID=$(lsof -ti:3000 2>/dev/null || true)
    if [ -n "$PID" ]; then
        echo -e "${YELLOW}发现端口 3000 被进程占用，PID: $PID${NC}"
        echo "正在关闭进程..."
        kill -9 "$PID" 2>/dev/null || true
        sleep 1
        # 再次检查是否已关闭
        if lsof -ti:3000 >/dev/null 2>&1; then
            echo -e "${RED}❌ 关闭进程失败${NC}"
        else
            echo -e "${GREEN}✅ 进程已关闭${NC}"
        fi
    else
        echo -e "${GREEN}✅ 端口 3000 未被占用${NC}"
    fi
# 如果没有 lsof，尝试使用 netstat (Linux)
elif command -v netstat >/dev/null 2>&1; then
    PID=$(netstat -tuln 2>/dev/null | grep ':3000' | grep LISTEN | awk '{print $NF}' | cut -d'/' -f1 | head -1 || true)
    if [ -n "$PID" ]; then
        echo -e "${YELLOW}发现端口 3000 被进程占用，PID: $PID${NC}"
        echo "正在关闭进程..."
        kill -9 "$PID" 2>/dev/null || true
        sleep 1
        echo -e "${GREEN}✅ 进程已关闭${NC}"
    else
        echo -e "${GREEN}✅ 端口 3000 未被占用${NC}"
    fi
# 如果没有 lsof 和 netstat，尝试使用 ss (Linux)
elif command -v ss >/dev/null 2>&1; then
    PID=$(ss -tlnp 2>/dev/null | grep ':3000' | grep LISTEN | sed -n 's/.*pid=\([0-9]*\).*/\1/p' | head -1 || true)
    if [ -n "$PID" ]; then
        echo -e "${YELLOW}发现端口 3000 被进程占用，PID: $PID${NC}"
        echo "正在关闭进程..."
        kill -9 "$PID" 2>/dev/null || true
        sleep 1
        echo -e "${GREEN}✅ 进程已关闭${NC}"
    else
        echo -e "${GREEN}✅ 端口 3000 未被占用${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  无法检查端口占用情况（未找到 lsof/netstat/ss 命令）${NC}"
    echo "继续执行..."
fi

# 等待端口释放
sleep 2

# 启动后端服务
echo ""
echo "[2/4] 启动后端服务 (python -m app)..."
nohup python -m app > backend.log 2>&1 &
BACKEND_PID=$!

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ 后端服务已在后台启动 (PID: $BACKEND_PID)${NC}"
    echo "$BACKEND_PID" > backend.pid
else
    echo -e "${RED}❌ 后端服务启动失败${NC}"
    exit 1
fi

# 等待后端启动
echo "等待后端服务启动..."
sleep 5

# 启动前端服务
echo ""
echo "[3/4] 启动前端服务 (npm run dev)..."
cd "$SCRIPT_DIR/frontend"
nohup npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ 前端服务已在后台启动 (PID: $FRONTEND_PID)${NC}"
    echo "$FRONTEND_PID" > ../frontend.pid
else
    echo -e "${RED}❌ 前端服务启动失败${NC}"
    exit 1
fi

# 返回原目录
cd "$SCRIPT_DIR"

echo ""
echo "[4/4] 启动完成！"
echo "========================================"
echo -e "${GREEN}✅ 后端服务: http://localhost:8000${NC}"
echo -e "${GREEN}✅ 前端服务: http://localhost:3000${NC}"
echo -e "${GREEN}✅ API 文档: http://localhost:8000/docs${NC}"
echo "========================================"
echo ""
echo "📝 日志文件:"
echo "   - 后端日志: backend.log"
echo "   - 前端日志: frontend.log"
echo ""
echo "📝 PID 文件:"
echo "   - 后端 PID: backend.pid"
echo "   - 前端 PID: frontend.pid"
echo ""
echo "💡 提示: 关闭此终端不会停止服务，如需停止服务请运行 stop_app.sh"
echo ""

