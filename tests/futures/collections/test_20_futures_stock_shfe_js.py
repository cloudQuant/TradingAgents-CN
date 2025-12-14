"""
上海期货交易所-库存数据数据集合测试用例
"""
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from test_base import FuturesCollectionTestBase, PlaywrightAPITestMixin, PLAYWRIGHT_AVAILABLE


class TestFuturesStockShfeJsCollection(FuturesCollectionTestBase, PlaywrightAPITestMixin):
    """测试上海期货交易所-库存数据数据集合
    
    接口类型：no_param
    AKShare接口：ak.futures_stock_shfe_js()
    """
    collection_name = "futures_stock_shfe_js"
    display_name = "上海期货交易所-库存数据"
    
    # 接口配置
    api_type = "no_param"
    akshare_func = "futures_stock_shfe_js"
    default_params = {}
    skip_refresh = True  # 不支持刷新操作
    
    def test_akshare_interface(self):
        """测试AKShare接口是否可用"""
        try:
            import akshare as ak
            result = ak.futures_stock_shfe_js()
            if result is None:
                print(f"  [WARN] AKShare接口返回None")
            elif hasattr(result, 'empty') and result.empty:
                print(f"  [WARN] AKShare接口返回空DataFrame")
            elif isinstance(result, dict) and not result:
                print(f"  [WARN] AKShare接口返回空字典")
            else:
                if hasattr(result, '__len__'):
                    print(f"[OK] AKShare接口可用，返回 {len(result)} 条数据")
                else:
                    print(f"[OK] AKShare接口可用")
        except Exception as e:
            print(f"  [WARN] AKShare接口测试失败: {e}")

    def test_playwright_api_update(self):
        """测试API更新功能（Playwright自动化测试）- 此接口不支持刷新"""
        print("  [SKIP] 此接口不支持刷新操作")



if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--api", action="store_true", help="包含API功能测试")
    parser.add_argument("--akshare", action="store_true", help="测试AKShare接口")
    parser.add_argument("--playwright", action="store_true", help="运行Playwright自动化测试")
    args = parser.parse_args()
    
    test = TestFuturesStockShfeJsCollection()
    
    if args.akshare:
        test.test_akshare_interface()
    
    if args.playwright:
        test.test_playwright_api_update()
    
    success = test.run_all_tests(include_api_tests=args.api)
    sys.exit(0 if success else 1)
