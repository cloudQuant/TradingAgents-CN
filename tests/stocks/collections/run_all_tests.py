#!/usr/bin/env python
"""
运行所有股票数据集合测试

使用方法:
    # 运行所有测试（不含集成测试）
    python run_all_tests.py
    
    # 运行包含集成测试（需要网络）
    python run_all_tests.py --integration
    
    # 运行特定集合的测试
    python run_all_tests.py --collection stock_zh_a_spot_em
    
    # 详细输出
    python run_all_tests.py -v
"""
import subprocess
import sys
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="运行股票数据集合测试")
    parser.add_argument("--integration", "-i", action="store_true", 
                        help="运行集成测试（需要网络连接）")
    parser.add_argument("--collection", "-c", type=str, 
                        help="只运行特定集合的测试")
    parser.add_argument("--verbose", "-v", action="store_true", 
                        help="详细输出")
    parser.add_argument("--coverage", action="store_true", 
                        help="生成覆盖率报告")
    args = parser.parse_args()
    
    # 构建pytest命令
    cmd = ["python", "-m", "pytest"]
    
    # 测试目录
    test_dir = Path(__file__).parent
    
    if args.collection:
        # 运行特定集合的测试
        test_file = test_dir / f"*{args.collection}*.py"
        cmd.append(str(test_file))
    else:
        cmd.append(str(test_dir))
    
    # 排除集成测试（除非明确指定）
    if not args.integration:
        cmd.extend(["-m", "not integration"])
    
    # 详细输出
    if args.verbose:
        cmd.append("-v")
    else:
        cmd.append("-q")
    
    # 覆盖率
    if args.coverage:
        cmd.extend(["--cov=app.services.data_sources.stocks", 
                    "--cov-report=html:coverage_stocks"])
    
    # 其他选项
    cmd.extend([
        "--tb=short",  # 简短的错误追踪
        "-x",  # 遇到第一个错误就停止
        "--ignore=test_base.py",  # 忽略基类文件
    ])
    
    print(f"运行命令: {' '.join(cmd)}")
    print("-" * 60)
    
    # 运行测试
    result = subprocess.run(cmd, cwd=test_dir.parent.parent.parent)
    
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
