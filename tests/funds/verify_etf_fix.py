"""
验证 fund_etf_spot_em 修复：无需数据库连接
"""

import sys
import os
import io

# 设置输出编码为 UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

def verify_fields_definition():
    """验证字段定义"""
    print("\n" + "="*60)
    print("验证 1: 检查字段定义")
    print("="*60)
    
    # 读取路由文件
    router_file = os.path.join(os.path.dirname(__file__), '../../app/routers/funds.py')
    
    with open(router_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找 fund_etf_spot_em 的字段定义
    start_idx = content.find('"name": "fund_etf_spot_em"')
    if start_idx == -1:
        print("✗ 未找到 fund_etf_spot_em 定义")
        return False
    
    # 提取字段部分
    fields_start = content.find('"fields":', start_idx)
    fields_end = content.find(']', fields_start) + 1
    fields_section = content[fields_start:fields_end]
    
    # 计算字段数量（简单统计双引号中的内容）
    import re
    fields = re.findall(r'"([^"]+)"', fields_section)
    # 排除 "fields" 本身
    fields = [f for f in fields if f != 'fields']
    
    print(f"✓ 找到 {len(fields)} 个字段定义")
    
    # 验证关键字段是否存在
    key_fields = ["外盘", "内盘", "超大单净流入-净额", "现手", "买一", "卖一", "最新份额", "流通市值", "总市值"]
    missing = [f for f in key_fields if f not in fields]
    
    if missing:
        print(f"✗ 缺少以下关键字段: {', '.join(missing)}")
        return False
    else:
        print(f"✓ 所有关键新增字段都已定义")
    
    # 显示前10个和后10个字段
    print(f"\n前10个字段: {', '.join(fields[:10])}")
    print(f"后10个字段: {', '.join(fields[-10:])}")
    
    return len(fields) >= 35


def verify_stats_method():
    """验证统计方法是否包含 type_stats"""
    print("\n" + "="*60)
    print("验证 2: 检查统计方法")
    print("="*60)
    
    # 读取服务文件
    service_file = os.path.join(os.path.dirname(__file__), '../../app/services/fund_data_service.py')
    
    with open(service_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找 get_fund_etf_spot_stats 方法
    method_start = content.find('async def get_fund_etf_spot_stats')
    if method_start == -1:
        print("✗ 未找到 get_fund_etf_spot_stats 方法")
        return False
    
    # 查找下一个方法开始位置作为结束
    next_method = content.find('async def ', method_start + 1)
    method_content = content[method_start:next_method] if next_method != -1 else content[method_start:]
    
    # 检查是否包含 type_stats
    if 'type_stats' not in method_content:
        print("✗ 方法中未找到 type_stats")
        return False
    
    print("✓ 方法中包含 type_stats")
    
    # 检查是否包含类型关键词定义
    if 'type_keywords' not in method_content:
        print("✗ 方法中未找到 type_keywords 定义")
        return False
    
    print("✓ 方法中包含 type_keywords 定义")
    
    # 检查返回值是否包含 type_stats
    return_section = method_content[method_content.rfind('return {'):]
    if "'type_stats'" not in return_section and '"type_stats"' not in return_section:
        print("✗ 返回值中未包含 type_stats")
        return False
    
    print("✓ 返回值中包含 type_stats")
    
    # 统计类型关键词数量
    import re
    type_keywords = re.findall(r"'([^']+ETF)':", method_content)
    print(f"\n定义了 {len(type_keywords)} 种 ETF 类型:")
    for keyword in type_keywords:
        print(f"  - {keyword}")
    
    return True


def verify_akshare_api():
    """验证 AKShare API 返回的字段"""
    print("\n" + "="*60)
    print("验证 3: 检查 AKShare API")
    print("="*60)
    
    try:
        import akshare as ak
        print("✓ AKShare 已安装")
        
        # 获取样本数据
        print("正在从 AKShare 获取样本数据...")
        df = ak.fund_etf_spot_em()
        
        if df is None or df.empty:
            print("⚠ AKShare 返回空数据")
            return False
        
        field_count = len(df.columns)
        print(f"✓ AKShare API 返回 {field_count} 个字段")
        
        # 显示所有字段
        print(f"\n字段列表:")
        for i, col in enumerate(df.columns, 1):
            print(f"  {i:2d}. {col}")
        
        return field_count >= 35
        
    except ImportError:
        print("⚠ AKShare 未安装，跳过 API 验证")
        return None
    except Exception as e:
        print(f"⚠ 无法连接 AKShare API: {e}")
        return None


def main():
    """主验证流程"""
    print("\n" + "█"*60)
    print("fund_etf_spot_em 修复验证")
    print("█"*60)
    
    results = []
    
    # 验证1: 字段定义
    try:
        result1 = verify_fields_definition()
        results.append(("字段定义", result1))
    except Exception as e:
        print(f"✗ 字段定义验证失败: {e}")
        results.append(("字段定义", False))
    
    # 验证2: 统计方法
    try:
        result2 = verify_stats_method()
        results.append(("统计方法", result2))
    except Exception as e:
        print(f"✗ 统计方法验证失败: {e}")
        results.append(("统计方法", False))
    
    # 验证3: AKShare API
    try:
        result3 = verify_akshare_api()
        if result3 is not None:
            results.append(("AKShare API", result3))
    except Exception as e:
        print(f"⚠ AKShare API 验证异常: {e}")
    
    # 汇总结果
    print("\n" + "="*60)
    print("验证结果汇总")
    print("="*60)
    
    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{name:20s}: {status}")
    
    # 总结
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    print("\n" + "="*60)
    if passed == total:
        print(f"✓ 所有验证通过 ({passed}/{total})")
        print("\n后续步骤:")
        print("1. 启动后端服务")
        print("2. 访问前端页面: /funds/collections/fund_etf_spot_em")
        print("3. 点击'更新数据'按钮")
        print("4. 验证'结构分布分析' tab 显示正常")
        print("5. 验证数据列表显示所有字段")
    else:
        print(f"⚠ 部分验证失败 ({passed}/{total})")
        print("\n请检查上述失败的验证项")
    print("="*60)
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
