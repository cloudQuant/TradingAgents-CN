#!/bin/bash

# TradingAgents-CN 停止脚本

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "========================================"
echo "TradingAgents-CN 停止脚本"
echo "========================================"
echo ""

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 停止前端服务（3000 端口）
echo "[1/2] 停止前端服务 (端口 3000)..."

# 尝试从 PID 文件读取
if [ -f "frontend.pid" ]; then
    FRONTEND_PID=$(cat frontend.pid 2>/dev/null || true)
    if [ -n "$FRONTEND_PID" ] && kill -0 "$FRONTEND_PID" 2>/dev/null; then
        echo "从 PID 文件发现前端进程，PID: $FRONTEND_PID"
        kill -9 "$FRONTEND_PID" 2>/dev/null || true
        rm -f frontend.pid
        echo -e "${GREEN}✅ 前端服务已停止${NC}"
    else
        rm -f frontend.pid
    fi
fi

# 尝试通过端口查找进程
if command -v lsof >/dev/null 2>&1; then
    PID=$(lsof -ti:3000 2>/dev/null || true)
    if [ -n "$PID" ]; then
        echo "发现前端进程，PID: $PID"
        kill -9 "$PID" 2>/dev/null || true
        echo -e "${GREEN}✅ 前端服务已停止${NC}"
    else
        echo -e "${GREEN}✅ 前端服务未运行${NC}"
    fi
elif command -v netstat >/dev/null 2>&1; then
    PID=$(netstat -tuln 2>/dev/null | grep ':3000' | grep LISTEN | awk '{print $NF}' | cut -d'/' -f1 | head -1 || true)
    if [ -n "$PID" ]; then
        echo "发现前端进程，PID: $PID"
        kill -9 "$PID" 2>/dev/null || true
        echo -e "${GREEN}✅ 前端服务已停止${NC}"
    else
        echo -e "${GREEN}✅ 前端服务未运行${NC}"
    fi
elif command -v ss >/dev/null 2>&1; then
    PID=$(ss -tlnp 2>/dev/null | grep ':3000' | grep LISTEN | sed -n 's/.*pid=\([0-9]*\).*/\1/p' | head -1 || true)
    if [ -n "$PID" ]; then
        echo "发现前端进程，PID: $PID"
        kill -9 "$PID" 2>/dev/null || true
        echo -e "${GREEN}✅ 前端服务已停止${NC}"
    else
        echo -e "${GREEN}✅ 前端服务未运行${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  无法检查端口占用情况${NC}"
fi

# 停止后端服务（8000 端口）
echo ""
echo "[2/2] 停止后端服务 (端口 8000)..."

# 尝试从 PID 文件读取
if [ -f "backend.pid" ]; then
    BACKEND_PID=$(cat backend.pid 2>/dev/null || true)
    if [ -n "$BACKEND_PID" ] && kill -0 "$BACKEND_PID" 2>/dev/null; then
        echo "从 PID 文件发现后端进程，PID: $BACKEND_PID"
        kill -9 "$BACKEND_PID" 2>/dev/null || true
        rm -f backend.pid
        echo -e "${GREEN}✅ 后端服务已停止${NC}"
    else
        rm -f backend.pid
    fi
fi

# 尝试通过端口查找进程
if command -v lsof >/dev/null 2>&1; then
    PID=$(lsof -ti:8000 2>/dev/null || true)
    if [ -n "$PID" ]; then
        echo "发现后端进程，PID: $PID"
        kill -9 "$PID" 2>/dev/null || true
        echo -e "${GREEN}✅ 后端服务已停止${NC}"
    else
        echo -e "${GREEN}✅ 后端服务未运行${NC}"
    fi
elif command -v netstat >/dev/null 2>&1; then
    PID=$(netstat -tuln 2>/dev/null | grep ':8000' | grep LISTEN | awk '{print $NF}' | cut -d'/' -f1 | head -1 || true)
    if [ -n "$PID" ]; then
        echo "发现后端进程，PID: $PID"
        kill -9 "$PID" 2>/dev/null || true
        echo -e "${GREEN}✅ 后端服务已停止${NC}"
    else
        echo -e "${GREEN}✅ 后端服务未运行${NC}"
    fi
elif command -v ss >/dev/null 2>&1; then
    PID=$(ss -tlnp 2>/dev/null | grep ':8000' | grep LISTEN | sed -n 's/.*pid=\([0-9]*\).*/\1/p' | head -1 || true)
    if [ -n "$PID" ]; then
        echo "发现后端进程，PID: $PID"
        kill -9 "$PID" 2>/dev/null || true
        echo -e "${GREEN}✅ 后端服务已停止${NC}"
    else
        echo -e "${GREEN}✅ 后端服务未运行${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  无法检查端口占用情况${NC}"
fi

echo ""
echo "========================================"
echo -e "${GREEN}✅ 所有服务已停止${NC}"
echo "========================================"
echo ""

