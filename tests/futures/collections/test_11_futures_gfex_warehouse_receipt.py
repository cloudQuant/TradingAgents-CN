"""
仓单日报-广州期货交易所数据集合测试用例
"""
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from test_base import FuturesCollectionTestBase, PlaywrightAPITestMixin, PLAYWRIGHT_AVAILABLE


class TestFuturesGfexWarehouseReceiptCollection(FuturesCollectionTestBase, PlaywrightAPITestMixin):
    """测试仓单日报-广州期货交易所数据集合
    
    接口类型：date_param
    AKShare接口：ak.futures_gfex_warehouse_receipt()
    """
    collection_name = "futures_gfex_warehouse_receipt"
    display_name = "仓单日报-广州期货交易所"
    
    # 接口配置
    api_type = "date_param"
    akshare_func = "futures_gfex_warehouse_receipt"
    default_params = {'date': '20241213'}
    
    def test_akshare_interface(self):
        """测试AKShare接口是否可用"""
        try:
            import akshare as ak
            result = ak.futures_gfex_warehouse_receipt(date="20241213")
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

    async def test_api_update_async(self):
        """测试API更新功能（异步版本）"""
        if not await self._setup_playwright():
            return {"success": False, "error": "Playwright未安装"}
        
        try:
            # 登录
            if not await self._login():
                return {"success": False, "error": "登录失败"}
            
            # 构建请求数据
            data = {
                "update_type": "single",
                "params": {'date': '20241213'}
            }
            
            result = await self._api_request_with_auth(
                f"/collections/{self.collection_name}/refresh",
                method="POST",
                data=data
            )
            
            return result
            
        finally:
            await self._teardown_playwright()



if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--api", action="store_true", help="包含API功能测试")
    parser.add_argument("--akshare", action="store_true", help="测试AKShare接口")
    parser.add_argument("--playwright", action="store_true", help="运行Playwright自动化测试")
    args = parser.parse_args()
    
    test = TestFuturesGfexWarehouseReceiptCollection()
    
    if args.akshare:
        test.test_akshare_interface()
    
    if args.playwright:
        test.test_playwright_api_update()
    
    success = test.run_all_tests(include_api_tests=args.api)
    sys.exit(0 if success else 1)
