"""
期权模块重构验证测试
验证新的架构是否正确实现
"""

import sys
import os

# 设置输出编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))


def test_imports():
    """测试所有模块是否可以正确导入"""
    print("=" * 60)
    print("测试模块导入...")
    print("=" * 60)
    
    # 测试配置导入
    try:
        from app.config.option_update_config import (
            OPTION_UPDATE_CONFIGS,
            get_collection_config,
            get_all_collection_names
        )
        print(f"✓ option_update_config 导入成功，配置了 {len(OPTION_UPDATE_CONFIGS)} 个集合")
    except Exception as e:
        print(f"✗ option_update_config 导入失败: {e}")
        return False
    
    # 测试基础类导入
    try:
        from app.services.data_sources.options.providers.base_provider import BaseOptionProvider
        from app.services.data_sources.options.services.base_service import BaseOptionService
        print("✓ 基础类 BaseOptionProvider 和 BaseOptionService 导入成功")
    except Exception as e:
        print(f"✗ 基础类导入失败: {e}")
        return False
    
    # 测试刷新服务导入
    try:
        from app.services.option_refresh_service import OptionRefreshService
        print("✓ OptionRefreshService 导入成功")
    except Exception as e:
        print(f"✗ OptionRefreshService 导入失败: {e}")
        return False
    
    # 测试各个服务模块导入
    service_modules = [
        ("option_em_service", ["OptionCurrentEmService", "OptionLhbEmService", "OptionValueAnalysisEmService"]),
        ("option_misc_service", ["OptionContractInfoCtpService", "OptionCommInfoService", "OptionMarginService"]),
        ("option_sse_service", ["OptionCurrentDaySseService", "OptionRiskIndicatorSseService"]),
        ("option_szse_service", ["OptionCurrentDaySzseService", "OptionDailyStatsSzseService"]),
        ("option_cffex_list_sina_service", ["OptionCffexSz50ListSinaService", "OptionCffexHs300ListSinaService"]),
        ("option_cffex_sina_service", ["OptionCffexSz50SpotSinaService", "OptionCffexHs300DailySinaService"]),
        ("option_sse_sina_service", ["OptionSseListSinaService", "OptionSseGreeksSinaService"]),
        ("option_finance_service", ["OptionFinanceBoardService"]),
        ("option_commodity_sina_service", ["OptionCommodityContractSinaService", "OptionCommodityHistSinaService"]),
        ("option_exchange_service", ["OptionHistShfeService", "OptionHistDceService", "OptionCzceHistService"]),
    ]
    
    for module_name, classes in service_modules:
        try:
            module = __import__(
                f"app.services.data_sources.options.services.{module_name}",
                fromlist=classes
            )
            for cls_name in classes:
                getattr(module, cls_name)
            print(f"✓ {module_name} 导入成功 ({len(classes)} 个服务类)")
        except Exception as e:
            print(f"✗ {module_name} 导入失败: {e}")
            return False
    
    return True


def test_config_structure():
    """测试配置结构"""
    print("\n" + "=" * 60)
    print("测试配置结构...")
    print("=" * 60)
    
    from app.config.option_update_config import OPTION_UPDATE_CONFIGS, get_collection_config
    
    # 检查配置结构
    required_keys = ["display_name", "update_description", "single_update", "batch_update"]
    
    errors = []
    for name, config in OPTION_UPDATE_CONFIGS.items():
        for key in required_keys:
            if key not in config:
                errors.append(f"{name} 缺少 {key} 字段")
    
    if errors:
        for err in errors:
            print(f"✗ {err}")
        return False
    
    print(f"✓ 所有 {len(OPTION_UPDATE_CONFIGS)} 个集合配置结构正确")
    
    # 列出所有集合
    print("\n配置的集合列表:")
    for i, (name, config) in enumerate(OPTION_UPDATE_CONFIGS.items(), 1):
        single = "✓" if config["single_update"]["enabled"] else "✗"
        batch = "✓" if config["batch_update"]["enabled"] else "✗"
        print(f"  {i:2d}. {name}: {config['display_name']} (单条:{single} 批量:{batch})")
    
    return True


def test_service_mapping():
    """测试服务映射"""
    print("\n" + "=" * 60)
    print("测试服务映射...")
    print("=" * 60)
    
    from app.services.option_refresh_service import OptionRefreshService
    from app.config.option_update_config import OPTION_UPDATE_CONFIGS
    
    # 创建服务实例（不连接数据库）
    service = OptionRefreshService(db=None, task_manager=None)
    
    # 检查服务映射覆盖率
    mapped_collections = set(service._service_classes.keys())
    configured_collections = set(OPTION_UPDATE_CONFIGS.keys())
    
    missing_in_service = configured_collections - mapped_collections
    extra_in_service = mapped_collections - configured_collections
    
    if missing_in_service:
        print(f"⚠ 配置中有但服务映射中缺少: {missing_in_service}")
    
    if extra_in_service:
        print(f"⚠ 服务映射中有但配置中缺少: {extra_in_service}")
    
    covered = mapped_collections & configured_collections
    print(f"✓ 服务映射覆盖 {len(covered)}/{len(configured_collections)} 个配置集合")
    
    return True


def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("期权模块重构验证测试")
    print("=" * 60)
    
    results = []
    
    results.append(("模块导入测试", test_imports()))
    results.append(("配置结构测试", test_config_structure()))
    results.append(("服务映射测试", test_service_mapping()))
    
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "✓ 通过" if passed else "✗ 失败"
        print(f"  {name}: {status}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print("\n✓ 所有测试通过！期权模块重构验证成功。")
    else:
        print("\n✗ 部分测试失败，请检查上述错误。")
    
    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
