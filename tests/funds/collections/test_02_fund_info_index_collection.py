"""指数型基金基本信息数据集合测试用例
测试指数型基金基本信息集合的路由、服务和前端配置是否正确实现
"""
import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))


class TestIndexFundInfoCollection:
    """测试指数型基金基本信息数据集合"""

    def test_fund_collections_list_includes_fund_info_index_em(self):
        """测试基金集合列表中包含 fund_info_index_em（指数型基金基本信息）"""
        router_path = os.path.join(
            os.path.dirname(__file__),
            '..', '..', '..', 'app', 'routers', 'funds.py'
        )
        router_path = os.path.abspath(router_path)

        assert os.path.exists(router_path), f"基金路由文件不存在: {router_path}"

        with open(router_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查是否有 fund_info_index_em 集合定义
        assert 'fund_info_index_em' in content, "路由中找不到 fund_info_index_em 集合定义"
        assert '指数型基金基本信息' in content, "路由中找不到指数型基金基本信息的展示名称"
        print("[OK] 基金路由包含 fund_info_index_em 集合")

    def test_fund_data_service_has_index_implementations(self):
        """测试基金数据服务中包含 fund_info_index_em 相关实现"""
        service_path = os.path.join(
            os.path.dirname(__file__),
            '..', '..', '..', 'app', 'services', 'fund_data_service.py'
        )
        service_path = os.path.abspath(service_path)

        assert os.path.exists(service_path), f"基金数据服务文件不存在: {service_path}"

        with open(service_path, 'r', encoding='utf-8') as f:
            content = f.read()

        assert 'fund_info_index_em' in content, "数据服务中找不到 fund_info_index_em 相关内容"
        assert 'save_fund_info_index_data' in content, "数据服务中找不到 save_fund_info_index_data 方法"
        assert 'get_fund_info_index_stats' in content, "数据服务中找不到 get_fund_info_index_stats 方法"
        print("[OK] 基金数据服务包含 fund_info_index_em 实现")

    def test_fund_refresh_service_has_index_refresh(self):
        """测试基金刷新服务中包含指数型基金刷新实现"""
        service_path = os.path.join(
            os.path.dirname(__file__),
            '..', '..', '..', 'app', 'services', 'fund_refresh_service.py'
        )
        service_path = os.path.abspath(service_path)

        assert os.path.exists(service_path), f"基金刷新服务文件不存在: {service_path}"

        with open(service_path, 'r', encoding='utf-8') as f:
            content = f.read()

        assert 'fund_info_index_em' in content, "刷新服务中找不到 fund_info_index_em 相关内容"
        assert '_refresh_fund_info_index_em' in content, "刷新服务中找不到 _refresh_fund_info_index_em 方法"
        print("[OK] 基金刷新服务包含 fund_info_index_em 刷新实现")

    def test_frontend_collection_page_supports_index_funds(self):
        """测试前端基金集合详情页中支持指数型基金基本信息集合"""
        page_path = os.path.join(
            os.path.dirname(__file__),
            '..', '..', '..', 'frontend', 'src', 'views', 'Funds', 'Collection.vue'
        )
        page_path = os.path.abspath(page_path)

        assert os.path.exists(page_path), f"前端基金集合详情页不存在: {page_path}"

        with open(page_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查页面中是否有针对 fund_info_index_em 的配置或文案
        assert 'fund_info_index_em' in content, "页面中找不到 fund_info_index_em 相关配置"
        assert '指数型基金基本信息' in content, "页面中找不到指数型基金基本信息相关文案"
        print("[OK] 前端基金集合详情页支持 fund_info_index_em 集合")


if __name__ == "__main__":
    import sys
    test = TestIndexFundInfoCollection()
    failed = 0

    print("=" * 70)
    print("指数型基金基本信息数据集合测试")
    print("=" * 70)

    tests = [
        ('test_fund_collections_list_includes_fund_info_index_em', '集合列表包含 fund_info_index_em'),
        ('test_fund_data_service_has_index_implementations', '数据服务包含 fund_info_index_em 实现'),
        ('test_fund_refresh_service_has_index_refresh', '刷新服务包含 fund_info_index_em 实现'),
        ('test_frontend_collection_page_supports_index_funds', '前端集合详情页支持 fund_info_index_em'),
    ]

    for test_method, test_name in tests:
        try:
            print(f"\n[测试] {test_name}...")
            getattr(test, test_method)()
            print("  [OK] 通过")
        except AssertionError as e:
            print(f"  [FAILED] 失败: {e}")
            failed += 1
        except Exception as e:
            print(f"  [ERROR] 错误: {e}")
            failed += 1

    print("\n" + "=" * 70)
    if failed == 0:
        print("[SUCCESS] 所有测试通过！")
        print("=" * 70)
        sys.exit(0)
    else:
        print(f"[FAILED] {failed} 个测试失败")
        print("=" * 70)
        sys.exit(1)
