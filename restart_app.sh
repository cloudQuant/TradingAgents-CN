#!/bin/bash

# 云子量化 重启脚本

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "========================================"
echo "云子量化 重启脚本"
echo "========================================"
echo ""

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

STOP_SCRIPT="$SCRIPT_DIR/stop_app.sh"
START_SCRIPT="$SCRIPT_DIR/start_app.sh"

if [ ! -f "$STOP_SCRIPT" ]; then
    echo -e "${RED}❌ 未找到 stop_app.sh: $STOP_SCRIPT${NC}"
    exit 1
fi

if [ ! -f "$START_SCRIPT" ]; then
    echo -e "${RED}❌ 未找到 start_app.sh: $START_SCRIPT${NC}"
    exit 1
fi

# 1) 停止服务
echo "[1/3] 停止服务..."
bash "$STOP_SCRIPT"

# 2) 清空日志
echo ""
echo "[2/3] 清空日志..."
log_files=("error.log" "frontend.log" "backend.log")
for log_file in "${log_files[@]}"; do
    : > "$SCRIPT_DIR/$log_file"
    echo -e "${GREEN}✅ 已清空: $log_file${NC}"
done

# 3) 启动服务
echo ""
echo "[3/3] 启动服务..."
bash "$START_SCRIPT"
