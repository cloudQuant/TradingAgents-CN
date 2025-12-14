"""
检查和修复 Provider 的 unique_keys 配置

问题：很多 provider 的 unique_keys 配置了不存在的字段，导致数据无法正确保存
解决：检查 akshare 返回的实际字段，修复 unique_keys 配置
"""
import os
import sys
import re
import akshare as ak
import pandas as pd
from typing import Dict, List, Tuple, Optional

# Provider 目录
PROVIDER_DIR = "/Users/yunjinqi/Documents/TradingAgents-CN/app/services/data_sources/stocks/providers"

# 接口参数配置
INTERFACE_PARAMS = {
    # 无参数接口
    "stock_sse_summary": {},
    "stock_szse_summary": {"date": "20231229"},
    "stock_szse_area_summary": {"date": "202312"},
    "stock_szse_sector_summary": {"date": "202312"},
    "stock_sse_deal_daily": {},
    "stock_zh_a_spot_em": {},
    "stock_sh_a_spot_em": {},
    "stock_sz_a_spot_em": {},
    "stock_bj_a_spot_em": {},
    "stock_new_a_spot_em": {},
    "stock_cy_a_spot_em": {},
    "stock_kc_a_spot_em": {},
    "stock_zh_b_spot_em": {},
    "stock_us_spot_em": {},
    "stock_hk_spot_em": {},
    "stock_hot_rank_em": {},
    "stock_hot_up_em": {},
    "stock_hk_hot_rank_em": {},
    "stock_board_change_em": {},
    "stock_market_activity_legu": {},
    "stock_hot_follow_xq": {},
    "stock_hot_tweet_xq": {},
    "stock_hot_deal_xq": {},
    "stock_rank_cxfl_ths": {},
    "stock_rank_cxsl_ths": {},
    "stock_rank_ljqs_ths": {},
    "stock_rank_ljqd_ths": {},
    "stock_rank_xzjp_ths": {},
    "stock_esg_rate_sina": {},
    "stock_esg_msci_sina": {},
    "stock_esg_rft_sina": {},
    "stock_esg_zd_sina": {},
    "stock_esg_hz_sina": {},
    
    # 需要股票代码的接口
    "stock_individual_info_em": {"symbol": "000001"},
    "stock_individual_basic_info_xq": {"symbol": "SZ000001"},
    "stock_bid_ask_em": {"symbol": "000001"},
}


def get_akshare_columns(func_name: str, params: dict) -> Optional[List[str]]:
    """获取 akshare 接口返回的列名"""
    try:
        func = getattr(ak, func_name, None)
        if not func:
            return None
        df = func(**params)
        if df is None or df.empty:
            return None
        return list(df.columns)
    except Exception as e:
        print(f"  获取 {func_name} 列名失败: {e}")
        return None


def parse_provider_file(filepath: str) -> Dict:
    """解析 provider 文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    result = {
        'filepath': filepath,
        'content': content,
        'collection_name': None,
        'akshare_func': None,
        'unique_keys': None,
        'field_info': None,
    }
    
    # 提取 collection_name
    match = re.search(r'collection_name\s*=\s*["\']([^"\']+)["\']', content)
    if match:
        result['collection_name'] = match.group(1)
    
    # 提取 akshare_func
    match = re.search(r'akshare_func\s*=\s*["\']([^"\']+)["\']', content)
    if match:
        result['akshare_func'] = match.group(1)
    
    # 提取 unique_keys
    match = re.search(r'unique_keys\s*=\s*\[([^\]]+)\]', content)
    if match:
        keys_str = match.group(1)
        keys = re.findall(r'["\']([^"\']+)["\']', keys_str)
        result['unique_keys'] = keys
    
    return result


def suggest_unique_keys(columns: List[str], func_name: str) -> List[str]:
    """根据列名建议 unique_keys"""
    # 常见的唯一键字段
    common_keys = [
        '代码', '股票代码', '证券代码', 'code', 'symbol',
        '项目', '名称', '股票名称', '证券名称',
        '日期', '交易日期', 'date', 'trade_date',
        '序号', 'index',
    ]
    
    # 查找存在的唯一键
    for key in common_keys:
        if key in columns:
            return [key]
    
    # 如果没有找到，使用第一个非数值列
    for col in columns:
        if col not in ['更新时间', '更新人', '创建时间', '创建人', '来源', 'scraped_at']:
            return [col]
    
    return columns[:1] if columns else ['项目']


def check_provider(filepath: str) -> Tuple[bool, str, Optional[List[str]]]:
    """检查单个 provider"""
    info = parse_provider_file(filepath)
    
    if not info['akshare_func']:
        return True, "无 akshare_func", None
    
    func_name = info['akshare_func']
    params = INTERFACE_PARAMS.get(func_name, {})
    
    # 获取实际列名
    columns = get_akshare_columns(func_name, params)
    if columns is None:
        return True, "无法获取列名", None
    
    # 检查 unique_keys 是否存在于列中
    unique_keys = info['unique_keys'] or []
    missing_keys = [k for k in unique_keys if k not in columns]
    
    if missing_keys:
        suggested = suggest_unique_keys(columns, func_name)
        return False, f"unique_keys {missing_keys} 不存在于列 {columns[:5]}...", suggested
    
    return True, "OK", None


def fix_provider(filepath: str, new_unique_keys: List[str]) -> bool:
    """修复 provider 的 unique_keys"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换 unique_keys
        new_keys_str = str(new_unique_keys)
        content = re.sub(
            r'unique_keys\s*=\s*\[[^\]]*\]',
            f'unique_keys = {new_keys_str}',
            content
        )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except Exception as e:
        print(f"  修复失败: {e}")
        return False


def main():
    print("=" * 70)
    print("检查和修复 Provider unique_keys 配置")
    print("=" * 70)
    
    # 获取所有 provider 文件
    provider_files = [f for f in os.listdir(PROVIDER_DIR) 
                      if f.endswith('_provider.py') and f != '__init__.py']
    
    print(f"发现 {len(provider_files)} 个 provider 文件")
    print()
    
    # 检查所有 provider
    provider_files = sorted(provider_files)
    
    issues = []
    
    for fn in provider_files:
        filepath = os.path.join(PROVIDER_DIR, fn)
        print(f"检查 {fn}...", end=" ")
        
        ok, msg, suggested = check_provider(filepath)
        
        if ok:
            print(f"✓ {msg}")
        else:
            print(f"✗ {msg}")
            if suggested:
                print(f"    建议: unique_keys = {suggested}")
                issues.append((filepath, suggested))
    
    print()
    print("=" * 70)
    print(f"发现 {len(issues)} 个需要修复的 provider")
    print("=" * 70)
    
    if issues:
        print("\n自动修复中...")
        fixed_count = 0
        for filepath, suggested in issues:
            fn = os.path.basename(filepath)
            print(f"修复 {fn}...", end=" ")
            if fix_provider(filepath, suggested):
                print("✓")
                fixed_count += 1
            else:
                print("✗")
        print(f"\n修复完成: {fixed_count}/{len(issues)} 个 provider")


if __name__ == "__main__":
    main()
