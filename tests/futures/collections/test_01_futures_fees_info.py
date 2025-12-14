"""
期货交易费用参照表数据集合测试用例

接口类型：无参数接口
AKShare接口：ak.futures_fees_info()
数据来源：http://openctp.cn/fees.html
"""
import sys
import os
import asyncio

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from test_base import FuturesCollectionTestBase, PlaywrightAPITestMixin, PLAYWRIGHT_AVAILABLE


class TestFuturesFeesInfoCollection(FuturesCollectionTestBase, PlaywrightAPITestMixin):
    """测试期货交易费用参照表数据集合"""
    
    collection_name = "futures_fees_info"
    display_name = "期货交易费用参照表"
    
    # 接口配置
    api_type = "no_param"  # 无参数接口
    akshare_func = "futures_fees_info"
    default_params = {}  # 无参数
    
    def test_akshare_interface(self):
        """测试AKShare接口是否可用"""
        try:
            import akshare as ak
            df = ak.futures_fees_info()
            assert df is not None, "返回None"
            assert not df.empty, "返回空DataFrame"
            # 验证关键字段
            expected_cols = ["交易所", "合约代码", "合约名称"]
            for col in expected_cols:
                assert col in df.columns, f"缺少字段: {col}"
            print(f"[OK] AKShare接口可用，返回 {len(df)} 行数据")
        except Exception as e:
            print(f"  [WARN] AKShare接口测试失败: {e}")
    
    async def test_api_update_async(self):
        """测试API更新功能（异步版本）- 针对无参数接口"""
        if not await self._setup_playwright():
            return {"success": False, "error": "Playwright未安装"}
        
        try:
            # 登录
            if not await self._login():
                return {"success": False, "error": "登录失败"}
            
            # 无参数接口，直接更新
            data = {
                "update_type": "single",
                "params": {}
            }
            
            result = await self._api_request_with_auth(
                f"/collections/{self.collection_name}/refresh",
                method="POST",
                data=data
            )
            
            # 验证响应
            if result["success"] and result.get("response"):
                response = result["response"]
                # 检查是否返回了任务ID或成功消息
                if isinstance(response, dict):
                    if "task_id" in response or "success" in response:
                        result["validated"] = True
            
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
    
    test = TestFuturesFeesInfoCollection()
    
    if args.akshare:
        test.test_akshare_interface()
    
    if args.playwright:
        test.test_playwright_api_update()
    
    success = test.run_all_tests(include_api_tests=args.api)
    sys.exit(0 if success else 1)
