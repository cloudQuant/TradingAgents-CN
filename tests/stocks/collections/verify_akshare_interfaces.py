"""
验证 AKShare 接口是否可用

快速测试几个关键接口，确保数据能够正常获取
"""
import sys

def main():
    """主函数"""
    print("=" * 60)
    print("AKShare 接口验证")
    print("=" * 60)
    
    try:
        import akshare as ak
        print(f"\n✓ akshare 已安装，版本: {ak.__version__}")
    except ImportError:
        print("\n✗ akshare 未安装")
        print("  请运行: pip install akshare")
        return 1
    
    # 测试几个关键接口
    test_cases = [
        ("stock_zh_a_spot_em", {}, "沪深京A股实时行情"),
        ("stock_sse_summary", {}, "上证交易所总貌"),
        ("stock_szse_summary", {"date": "20231229"}, "深证交易所总貌"),
    ]
    
    print("\n测试关键接口:")
    print("-" * 60)
    
    success = 0
    for func_name, params, desc in test_cases:
        print(f"\n测试 {desc} ({func_name})...", end=" ")
        try:
            func = getattr(ak, func_name)
            df = func(**params) if params else func()
            if df is not None and len(df) > 0:
                print(f"✓ 获取到 {len(df)} 条数据")
                success += 1
            else:
                print("✗ 返回空数据")
        except Exception as e:
            print(f"✗ 错误: {str(e)[:50]}")
    
    print("\n" + "=" * 60)
    print(f"测试结果: {success}/{len(test_cases)} 通过")
    
    return 0 if success == len(test_cases) else 1

if __name__ == "__main__":
    sys.exit(main())
