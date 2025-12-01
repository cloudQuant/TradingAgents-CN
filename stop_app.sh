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

# 通用方法：根据 PID 文件终止进程
kill_pid_file() {
    local pid_file=$1
    if [ -f "$pid_file" ]; then
        local pid
        pid=$(cat "$pid_file" 2>/dev/null || true)
        if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
            echo "从 PID 文件($pid_file)发现进程，PID: $pid"
            kill -9 "$pid" 2>/dev/null || true
            echo -e "${GREEN}✅ 进程 $pid 已停止${NC}"
        fi
        rm -f "$pid_file"
    fi
}

# 通用方法：通过端口终止进程
kill_by_port() {
    local port=$1
    local raw_pids=""

    if command -v lsof >/dev/null 2>&1; then
        raw_pids=$(lsof -ti:"$port" 2>/dev/null || true)
    elif command -v netstat >/dev/null 2>&1; then
        raw_pids=$(netstat -tuln 2>/dev/null | grep ":$port" | grep LISTEN | awk '{print $NF}' | cut -d'/' -f1 || true)
    elif command -v ss >/dev/null 2>&1; then
        raw_pids=$(ss -tlnp 2>/dev/null | grep ":$port" | grep LISTEN | sed -n 's/.*pid=\([0-9]*\).*/\1/p' || true)
    else
        echo -e "${YELLOW}⚠️  无法检查端口占用情况${NC}"
        return
    fi

    if [ -z "$raw_pids" ]; then
        echo -e "${GREEN}✅ 端口 $port 未运行${NC}"
        return
    fi

    echo "发现端口 $port 相关进程: $raw_pids"
    for pid in $raw_pids; do
        if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
            kill -9 "$pid" 2>/dev/null || true
        fi
    done
    echo -e "${GREEN}✅ 端口 $port 相关进程已停止${NC}"
}

# 停止前端服务（3000 端口）
echo "[1/2] 停止前端服务 (端口 3000)..."
kill_pid_file "frontend.pid"
kill_by_port 3000

# 停止后端服务（8000 端口）
echo ""
echo "[2/2] 停止后端服务 (端口 8000)..."
kill_pid_file "backend.pid"
kill_by_port 8000

echo ""
echo "========================================"
echo -e "${GREEN}✅ 所有服务已停止${NC}"
echo "========================================"
echo ""

# 删除日志文件
echo "[清理] 删除日志文件..."
log_files=("error.log" "frontend.log" "backend.log")
for log_file in "${log_files[@]}"; do
    if [ -f "$log_file" ]; then
        rm -f "$log_file"
        echo -e "${GREEN}✅ 已删除: $log_file${NC}"
    else
        echo -e "${YELLOW}⚠️  文件不存在: $log_file${NC}"
    fi
done

echo ""
echo "========================================"
echo -e "${GREEN}✅ 清理完成${NC}"
echo "========================================"
echo ""

