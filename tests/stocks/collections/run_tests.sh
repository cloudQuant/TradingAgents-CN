#!/bin/bash
# 股票数据集合测试运行脚本

# 设置颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "========================================"
echo "股票数据集合测试运行器"
echo "========================================"

# 检查环境变量
if [ -z "$API_AUTH_TOKEN" ]; then
    echo -e "${YELLOW}警告: API_AUTH_TOKEN 未设置${NC}"
    echo "大部分测试将被跳过"
    echo ""
    echo "设置方法:"
    echo "  export API_AUTH_TOKEN=your_token"
    echo "  export API_BASE_URL=http://localhost:8848"
    echo ""
fi

# 检查 Python 环境
PYTHON_CMD=""
if command -v /Users/yunjinqi/opt/anaconda3/bin/python &> /dev/null; then
    PYTHON_CMD="/Users/yunjinqi/opt/anaconda3/bin/python"
elif command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo -e "${RED}错误: 未找到 Python${NC}"
    exit 1
fi

echo "使用 Python: $PYTHON_CMD"
echo ""

# 运行快速状态检查
echo "1. 检查测试覆盖状态..."
$PYTHON_CMD quick_status.py
echo ""

# 运行测试
echo "2. 运行测试..."
case "$1" in
    "all")
        echo "运行所有测试..."
        $PYTHON_CMD -m pytest -v --tb=short
        ;;
    "quick")
        echo "运行快速测试（只测试前10个集合）..."
        $PYTHON_CMD -m pytest 007_*.py 008_*.py 009_*.py 010_*.py 011_*.py -v --tb=short
        ;;
    "coverage")
        echo "运行覆盖率测试..."
        $PYTHON_CMD -m pytest test_collections_requirements_coverage.py -v -s
        ;;
    *)
        echo "用法: $0 [all|quick|coverage]"
        echo "  all      - 运行所有测试"
        echo "  quick    - 运行快速测试"
        echo "  coverage - 运行覆盖率测试"
        ;;
esac
