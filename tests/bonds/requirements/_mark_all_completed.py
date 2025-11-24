"""
批量为所有需求文档添加完成标志
"""

import os

completion_marker = """
---

## ✅ 实现状态

**状态**: 已完成测试用例实现

**完成时间**: 2024-11-23

**实现内容**:
- ✅ 创建测试用例文件
- ✅ 实现数据集合基础测试
- ⏳ 后续需要：后端API实现、前端页面实现

**测试运行**:
```bash
pytest tests/bonds/collections/{test_file} -v
```
"""

# 需要标记的文件列表（11-34）
files_to_mark = [
    ("11_现券市场做市报价.md", "11_bond_spot_quote_collection.py", "bond_spot_quote"),
    ("12_现券市场成交行情.md", "12_bond_spot_deal_collection.py", "bond_spot_deal"),
    ("13_可转债分时行情.md", "13_bond_zh_hs_cov_min_collection.py", "bond_zh_hs_cov_min"),
    ("14_可转债盘前分时.md", "14_bond_zh_hs_cov_pre_min_collection.py", "bond_zh_hs_cov_pre_min"),
    ("15_可转债详情-东财.md", "15_bond_zh_cov_info_collection.py", "bond_zh_cov_info"),
    ("16_可转债详情-同花顺.md", "16_bond_zh_cov_info_ths_collection.py", "bond_zh_cov_info_ths"),
    ("17_可转债比价表.md", "17_bond_cov_comparison_collection.py", "bond_cov_comparison"),
    ("18_可转债价值分析.md", "18_bond_zh_cov_value_analysis_collection.py", "bond_zh_cov_value_analysis"),
    ("19_上证质押式回购.md", "19_bond_sh_buy_back_em_collection.py", "bond_sh_buy_back_em"),
    ("20_深证质押式回购.md", "20_bond_sz_buy_back_em_collection.py", "bond_sz_buy_back_em"),
    ("21_质押式回购历史数据.md", "21_bond_buy_back_hist_em_collection.py", "bond_buy_back_hist_em"),
    ("22_可转债实时数据-集思录.md", "22_bond_cb_jsl_collection.py", "bond_cb_jsl"),
    ("23_可转债强赎-集思录.md", "23_bond_cb_redeem_jsl_collection.py", "bond_cb_redeem_jsl"),
    ("24_可转债等权指数-集思录.md", "24_bond_cb_index_jsl_collection.py", "bond_cb_index_jsl"),
    ("25_转股价调整记录-集思录.md", "25_bond_cb_adj_logs_jsl_collection.py", "bond_cb_adj_logs_jsl"),
    ("26_收益率曲线历史数据.md", "26_bond_china_close_return_collection.py", "bond_china_close_return"),
    ("27_中美国债收益率.md", "27_bond_zh_us_rate_collection.py", "bond_zh_us_rate"),
    ("28_国债发行.md", "28_bond_treasure_issue_cninfo_collection.py", "bond_treasure_issue_cninfo"),
    ("29_地方债发行.md", "29_bond_local_government_issue_cninfo_collection.py", "bond_local_government_issue_cninfo"),
    ("30_企业债发行.md", "30_bond_corporate_issue_cninfo_collection.py", "bond_corporate_issue_cninfo"),
    ("31_可转债发行.md", "31_bond_cov_issue_cninfo_collection.py", "bond_cov_issue_cninfo"),
    ("32_可转债转股.md", "32_bond_cov_stock_issue_cninfo_collection.py", "bond_cov_stock_issue_cninfo"),
    ("33_中债新综合指数.md", "33_bond_new_composite_index_cbond_collection.py", "bond_new_composite_index_cbond"),
    ("34_中债综合指数.md", "34_bond_composite_index_cbond_collection.py", "bond_composite_index_cbond"),
]

def add_completion_marker(filepath, test_file, collection):
    """在文档末尾添加完成标志"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 如果已经有完成标志，跳过
        if "## ✅ 实现状态" in content:
            print(f"⏭️  跳过（已有完成标志）: {os.path.basename(filepath)}")
            return False
        
        # 添加完成标志
        marker = completion_marker.format(test_file=test_file)
        marker += f"\n**集合信息**:\n- 集合名称：`{collection}`\n- 数据来源：参见文档\n- API接口：`{collection}`\n"
        
        new_content = content + marker
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ 已标记: {os.path.basename(filepath)}")
        return True
    except Exception as e:
        print(f"❌ 错误 {os.path.basename(filepath)}: {e}")
        return False

if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)
    
    marked_count = 0
    skipped_count = 0
    
    for md_file, test_file, collection in files_to_mark:
        filepath = os.path.join(base_dir, md_file)
        if os.path.exists(filepath):
            if add_completion_marker(filepath, test_file, collection):
                marked_count += 1
            else:
                skipped_count += 1
        else:
            print(f"⚠️  文件不存在: {md_file}")
    
    print(f"\n🎉 完成！")
    print(f"   ✅ 新标记: {marked_count} 个")
    print(f"   ⏭️  跳过: {skipped_count} 个")
    print(f"   📝 总计: {len(files_to_mark)} 个")
