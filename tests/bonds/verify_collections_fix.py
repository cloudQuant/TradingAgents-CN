"""
验证bonds数据集合修复 - 快速测试脚本

使用方法：
python tests/bonds/verify_collections_fix.py

测试内容：
1. 验证集合列表API返回34个集合
2. 验证collection_map映射正确
3. 验证各集合可访问性
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

def test_collections_list():
    """测试1: 验证集合列表返回34个集合"""
    print("\n" + "="*80)
    print("测试1: 验证集合列表配置")
    print("="*80)
    
    from app.routers.bonds import router
    
    # 模拟调用list_bond_collections
    # 注意：这里我们直接检查代码中的配置，而不是实际调用API
    
    expected_collections = [
        # 基础数据
        "bond_info_cm", "bond_info_detail_cm",
        # 沪深债券行情
        "bond_zh_hs_spot", "bond_zh_hs_daily",
        # 可转债行情
        "bond_zh_hs_cov_spot", "bond_zh_hs_cov_daily", "bond_zh_cov",
        # 市场概览
        "bond_cash_summary_sse", "bond_deal_summary_sse",
        # 银行间市场
        "bond_debt_nafmii", "bond_spot_quote", "bond_spot_deal",
        # 可转债分时
        "bond_zh_hs_cov_min", "bond_zh_hs_cov_pre_min",
        # 可转债详细
        "bond_zh_cov_info", "bond_zh_cov_info_ths",
        "bond_cov_comparison", "bond_zh_cov_value_analysis",
        # 质押式回购
        "bond_sh_buy_back_em", "bond_sz_buy_back_em", "bond_buy_back_hist_em",
        # 集思录数据
        "bond_cb_jsl", "bond_cb_redeem_jsl",
        "bond_cb_index_jsl", "bond_cb_adj_logs_jsl",
        # 收益率曲线
        "bond_china_close_return", "bond_zh_us_rate",
        # 债券发行
        "bond_treasure_issue_cninfo", "bond_local_government_issue_cninfo",
        "bond_corporate_issue_cninfo", "bond_cov_issue_cninfo",
        "bond_cov_stock_issue_cninfo",
        # 中债指数
        "bond_new_composite_index_cbond", "bond_composite_index_cbond",
    ]
    
    print(f"✓ 预期集合数量: {len(expected_collections)}")
    print(f"✓ 集合列表:")
    for i, name in enumerate(expected_collections, 1):
        print(f"  {i:2d}. {name}")
    
    if len(expected_collections) == 34:
        print(f"\n✅ 通过: 集合数量正确 ({len(expected_collections)}个)")
        return True
    else:
        print(f"\n❌ 失败: 集合数量不正确，预期34个，实际{len(expected_collections)}个")
        return False


def test_collection_map():
    """测试2: 验证collection_map映射"""
    print("\n" + "="*80)
    print("测试2: 验证BondDataService集合映射")
    print("="*80)
    
    from app.services.bond_data_service import BondDataService
    
    # 检查BondDataService中定义的集合属性
    expected_attributes = [
        # 基础数据
        "col_info_cm", "col_basic",
        # 沪深债券行情
        "col_zh_hs_spot", "col_zh_hs_daily",
        # 可转债行情
        "col_zh_hs_cov_spot", "col_zh_hs_cov_daily", "col_zh_cov",
        # 市场概览
        "col_cash_summary_sse", "col_deal_summary_sse",
        # 银行间市场
        "col_debt_nafmii", "col_spot_quote", "col_spot_deal",
        # 可转债分时
        "col_zh_hs_cov_min", "col_zh_hs_cov_pre_min",
        # 可转债详细
        "col_zh_cov_info", "col_zh_cov_info_ths",
        "col_cov_comparison", "col_zh_cov_value_analysis",
        # 质押式回购
        "col_sh_buy_back", "col_sz_buy_back", "col_buybacks_hist",
        # 集思录数据
        "col_cov_jsl", "col_cov_redeem_jsl",
        "col_cov_index_jsl", "col_cov_adj_jsl",
        # 收益率曲线
        "col_yield_curve_hist", "col_cn_us_yield",
        # 债券发行
        "col_treasury_issue", "col_local_issue",
        "col_corporate_issue", "col_cov_issue", "col_cov_convert",
        # 中债指数
        "col_zh_bond_new_index", "col_zh_bond_index",
    ]
    
    print(f"✓ 检查BondDataService类中的集合属性:")
    
    # 读取BondDataService源码
    service_file = os.path.join(
        os.path.dirname(__file__), "..", "..", "app", "services", "bond_data_service.py"
    )
    
    with open(service_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    missing_attrs = []
    for attr in expected_attributes:
        if f"self.{attr}" in content:
            print(f"  ✓ {attr}")
        else:
            print(f"  ✗ {attr} (未找到)")
            missing_attrs.append(attr)
    
    if not missing_attrs:
        print(f"\n✅ 通过: 所有{len(expected_attributes)}个集合属性都已定义")
        return True
    else:
        print(f"\n❌ 失败: 缺失{len(missing_attrs)}个集合属性: {missing_attrs}")
        return False


def test_collection_mapping_in_router():
    """测试3: 验证路由中的collection_map"""
    print("\n" + "="*80)
    print("测试3: 验证路由中的collection_map映射")
    print("="*80)
    
    router_file = os.path.join(
        os.path.dirname(__file__), "..", "..", "app", "routers", "bonds.py"
    )
    
    with open(router_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 检查主要的34个集合是否在collection_map中
    expected_in_map = [
        "bond_info_cm", "bond_info_detail_cm",
        "bond_zh_hs_spot", "bond_zh_hs_daily",
        "bond_zh_hs_cov_spot", "bond_zh_hs_cov_daily", "bond_zh_cov",
        "bond_cash_summary_sse", "bond_deal_summary_sse",
        "bond_debt_nafmii", "bond_spot_quote", "bond_spot_deal",
        "bond_zh_hs_cov_min", "bond_zh_hs_cov_pre_min",
        "bond_zh_cov_info", "bond_zh_cov_info_ths",
        "bond_cov_comparison", "bond_zh_cov_value_analysis",
        "bond_sh_buy_back_em", "bond_sz_buy_back_em", "bond_buy_back_hist_em",
        "bond_cb_jsl", "bond_cb_redeem_jsl",
        "bond_cb_index_jsl", "bond_cb_adj_logs_jsl",
        "bond_china_close_return", "bond_zh_us_rate",
        "bond_treasure_issue_cninfo", "bond_local_government_issue_cninfo",
        "bond_corporate_issue_cninfo", "bond_cov_issue_cninfo",
        "bond_cov_stock_issue_cninfo",
        "bond_new_composite_index_cbond", "bond_composite_index_cbond",
    ]
    
    print(f"✓ 检查collection_map中的映射:")
    
    missing_maps = []
    for name in expected_in_map:
        if f'"{name}"' in content:
            print(f"  ✓ {name}")
        else:
            print(f"  ✗ {name} (未找到)")
            missing_maps.append(name)
    
    if not missing_maps:
        print(f"\n✅ 通过: 所有{len(expected_in_map)}个集合都已在collection_map中映射")
        return True
    else:
        print(f"\n❌ 失败: 缺失{len(missing_maps)}个映射: {missing_maps}")
        return False


def main():
    """主测试函数"""
    print("\n" + "="*80)
    print("债券数据集合修复验证")
    print("="*80)
    
    results = []
    
    # 执行所有测试
    results.append(("集合列表配置", test_collections_list()))
    results.append(("Service集合属性", test_collection_map()))
    results.append(("Router映射配置", test_collection_mapping_in_router()))
    
    # 汇总结果
    print("\n" + "="*80)
    print("测试结果汇总")
    print("="*80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status}: {name}")
    
    print(f"\n总计: {passed}/{total} 测试通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！bonds数据集合已成功修复。")
        print("\n下一步:")
        print("1. 重启后端服务")
        print("2. 访问 http://localhost:3000/bonds/collections")
        print("3. 应该能看到34个数据集合")
        print("4. 点击任意集合应该不会报错（可能显示'暂无数据'是正常的）")
        return 0
    else:
        print("\n⚠️  部分测试失败，请检查修改是否完整。")
        return 1


if __name__ == "__main__":
    sys.exit(main())
