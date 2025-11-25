"""
简化版验证脚本 - 不导入复杂模块，只检查源码文件

使用方法：
python tests/bonds/verify_collections_simple.py
"""

import os
import re

def check_bonds_router():
    """检查bonds.py路由配置"""
    print("\n" + "="*70)
    print("检查 app/routers/bonds.py")
    print("="*70)
    
    router_file = "f:/source_code/TradingAgents-CN/app/routers/bonds.py"
    
    if not os.path.exists(router_file):
        print(f"[错误] 文件不存在: {router_file}")
        return False
    
    with open(router_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 检查1: list_bond_collections中的集合数量
    collections_pattern = r'"name":\s*"(bond_[^"]+)"'
    collections = re.findall(collections_pattern, content)
    collections = list(set(collections))  # 去重
    
    print(f"\n1. 集合列表配置:")
    print(f"   找到 {len(collections)} 个集合配置")
    
    if len(collections) >= 34:
        print(f"   [通过] 集合数量 >= 34")
    else:
        print(f"   [失败] 集合数量 < 34，只有 {len(collections)} 个")
        return False
    
    # 检查2: collection_map映射数量
    # 统计 collection_map 中的映射数量
    map_count = content.count('svc.col_')
    
    print(f"\n2. collection_map映射:")
    print(f"   找到 {map_count} 个集合映射 (svc.col_)")
    
    if map_count >= 34:
        print(f"   [通过] 映射数量 >= 34")
    else:
        print(f"   [失败] 映射数量 < 34")
        return False
    
    # 检查3: 关键集合是否映射
    key_collections = [
        "bond_info_cm",
        "bond_zh_hs_spot", 
        "bond_cb_jsl",
        "bond_composite_index_cbond"
    ]
    
    print(f"\n3. 检查关键集合映射:")
    all_mapped = True
    for col in key_collections:
        if f'"{col}"' in content:
            print(f"   [通过] {col}")
        else:
            print(f"   [失败] {col} 未找到")
            all_mapped = False
    
    return all_mapped


def check_bond_service():
    """检查BondDataService"""
    print("\n" + "="*70)
    print("检查 app/services/bond_data_service.py")
    print("="*70)
    
    service_file = "f:/source_code/TradingAgents-CN/app/services/bond_data_service.py"
    
    if not os.path.exists(service_file):
        print(f"[错误] 文件不存在: {service_file}")
        return False
    
    with open(service_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 统计集合属性定义
    col_attrs = re.findall(r'self\.(col_\w+)\s*=', content)
    col_attrs = list(set(col_attrs))
    
    print(f"\n集合属性数量:")
    print(f"   找到 {len(col_attrs)} 个集合属性定义")
    
    if len(col_attrs) >= 34:
        print(f"   [通过] 属性数量 >= 34")
        return True
    else:
        print(f"   [失败] 属性数量 < 34")
        return False


def main():
    """主函数"""
    print("="*70)
    print("bonds数据集合修复验证 - 简化版")
    print("="*70)
    
    results = []
    
    # 执行检查
    results.append(("bonds.py路由配置", check_bonds_router()))
    results.append(("BondDataService", check_bond_service()))
    
    # 总结
    print("\n" + "="*70)
    print("验证结果总结")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "[通过]" if result else "[失败]"
        print(f"{status} {name}")
    
    print(f"\n总计: {passed}/{total} 检查通过")
    
    if passed == total:
        print("\n[成功] 所有检查通过！")
        print("\n下一步操作:")
        print("1. 重启后端服务: python -m uvicorn app.main:app --reload")
        print("2. 访问: http://localhost:3000/bonds/collections")
        print("3. 应该能看到34个数据集合")
        print("4. 点击集合可以访问（可能显示'暂无数据'是正常的）")
        return 0
    else:
        print("\n[警告] 部分检查未通过")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
