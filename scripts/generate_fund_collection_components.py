#!/usr/bin/env python3
"""
批量生成基金集合组件文件
每个集合对应一个 Vue 组件文件
"""

import os
from pathlib import Path

# 所有集合名称
COLLECTIONS = [
    'fund_name_em', 'fund_basic_info', 'fund_info_index_em', 'fund_net_value', 'fund_ranking',
    'fund_purchase_status', 'fund_etf_spot_em', 'fund_etf_spot_ths', 'fund_lof_spot_em', 'fund_spot_sina',
    'fund_etf_hist_min_em', 'fund_lof_hist_min_em', 'fund_etf_hist_em', 'fund_lof_hist_em', 'fund_etf_hist_sina',
    'fund_open_fund_daily_em', 'fund_open_fund_info_em', 'fund_money_fund_daily_em', 'fund_money_fund_info_em',
    'fund_etf_fund_daily_em', 'fund_hk_hist_em', 'fund_etf_fund_info_em', 'fund_etf_dividend_sina',
    'fund_fh_em', 'fund_cf_em', 'fund_fh_rank_em', 'fund_open_fund_rank_em', 'fund_exchange_rank_em',
    'fund_money_rank_em', 'fund_lcx_rank_em', 'fund_hk_rank_em', 'fund_individual_achievement_xq',
    'fund_value_estimation_em', 'fund_individual_analysis_xq', 'fund_individual_profit_probability_xq',
    'fund_individual_detail_hold_xq', 'fund_overview_em', 'fund_fee_em', 'fund_individual_detail_info_xq',
    'fund_portfolio_hold_em', 'fund_portfolio_bond_hold_em', 'fund_portfolio_industry_allocation_em',
    'fund_portfolio_change_em', 'fund_rating_all_em', 'fund_rating_sh_em', 'fund_rating_zs_em', 'fund_rating_ja_em',
    'fund_manager_em', 'fund_new_found_em', 'fund_scale_open_sina', 'fund_scale_close_sina',
    'fund_aum_em', 'fund_aum_trend_em', 'fund_aum_hist_em',
    'reits_realtime_em', 'reits_hist_em', 'fund_report_stock_cninfo', 'fund_report_industry_allocation_cninfo',
    'fund_report_asset_allocation_cninfo', 'fund_scale_change_em', 'fund_hold_structure_em',
    'fund_stock_position_lg', 'fund_balance_position_lg', 'fund_linghuo_position_lg',
    'fund_announcement_dividend_em', 'fund_announcement_report_em', 'fund_announcement_personnel_em'
]

# 特殊集合（需要自定义逻辑的）
SPECIAL_COLLECTIONS = {
    'fund_purchase_status',
    'fund_etf_spot_ths',
    'fund_lof_spot_em',
    'fund_info_index_em',
}

def to_pascal_case(name: str) -> str:
    """将 snake_case 转换为 PascalCase"""
    parts = name.split('_')
    return ''.join(word.capitalize() for word in parts)

def get_component_template(collection_name: str, is_special: bool = False) -> str:
    """生成组件模板"""
    pascal_name = to_pascal_case(collection_name)
    
    if is_special:
        # 特殊集合使用 DefaultCollection 作为基础，可以扩展
        return f'''<template>
  <DefaultCollection />
</template>

<script setup lang="ts">
import DefaultCollection from './DefaultCollection.vue'
import {{ useRoute }} from 'vue-router'

const route = useRoute()
const collectionName = route.params.collectionName as string

// TODO: 在此添加 {collection_name} 的特殊逻辑
// 例如：自定义图表、筛选器、更新参数等
</script>

<style lang="scss" scoped>
@use '@/styles/collection.scss' as *;
</style>
'''
    else:
        # 普通集合直接使用 DefaultCollection
        return f'''<template>
  <DefaultCollection />
</template>

<script setup lang="ts">
import DefaultCollection from './DefaultCollection.vue'
</script>

<style lang="scss" scoped>
@use '@/styles/collection.scss' as *;
</style>
'''

def main():
    """主函数"""
    # 获取项目根目录
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    collections_dir = project_root / 'frontend' / 'src' / 'views' / 'Funds' / 'collections'
    
    # 确保目录存在
    collections_dir.mkdir(parents=True, exist_ok=True)
    
    created_count = 0
    skipped_count = 0
    
    for collection_name in COLLECTIONS:
        pascal_name = to_pascal_case(collection_name)
        file_path = collections_dir / f'{pascal_name}.vue'
        
        # 如果文件已存在，跳过
        if file_path.exists():
            print(f'⏭️  跳过已存在的文件: {pascal_name}.vue')
            skipped_count += 1
            continue
        
        # 生成组件内容
        is_special = collection_name in SPECIAL_COLLECTIONS
        content = get_component_template(collection_name, is_special)
        
        # 写入文件
        file_path.write_text(content, encoding='utf-8')
        print(f'✅ 创建组件: {pascal_name}.vue')
        created_count += 1
    
    print(f'\n📊 统计:')
    print(f'  创建: {created_count} 个文件')
    print(f'  跳过: {skipped_count} 个文件')
    print(f'  总计: {len(COLLECTIONS)} 个集合')

if __name__ == '__main__':
    main()
