"""
批量生成17-34号需求的测试用例文件
运行此脚本以快速生成所有剩余的测试用例
"""

test_specs = [
    # 17-24: 可转债比价、质押回购、集思录
    ("17", "bond_cov_comparison", "可转债比价表", "转债代码"),
    ("18", "bond_zh_cov_value_analysis", "可转债价值分析", "债券代码+日期"),
    ("19", "bond_sh_buy_back_em", "上证质押式回购", "代码"),
    ("20", "bond_sz_buy_back_em", "深证质押式回购", "代码"),
    ("21", "bond_buy_back_hist_em", "质押式回购历史数据", "回购代码+日期"),
    ("22", "bond_cb_jsl", "可转债实时数据-集思录", "代码"),
    ("23", "bond_cb_redeem_jsl", "可转债强赎-集思录", "代码"),
    ("24", "bond_cb_index_jsl", "可转债等权指数-集思录", "日期"),
    # 25-34: 收益率曲线、发行数据、中债指数
    ("25", "bond_cb_adj_logs_jsl", "转股价调整记录-集思录", "代码+股东大会日"),
    ("26", "bond_china_close_return", "收益率曲线历史数据", "债券类型+日期+期限"),
    ("27", "bond_zh_us_rate", "中美国债收益率", "日期"),
    ("28", "bond_treasure_issue_cninfo", "国债发行", "债券代码"),
    ("29", "bond_local_government_issue_cninfo", "地方债发行", "债券代码"),
    ("30", "bond_corporate_issue_cninfo", "企业债发行", "债券代码"),
    ("31", "bond_cov_issue_cninfo", "可转债发行", "债券代码"),
    ("32", "bond_cov_stock_issue_cninfo", "可转债转股", "债券代码"),
    ("33", "bond_new_composite_index_cbond", "中债新综合指数", "指标+期限+日期"),
    ("34", "bond_composite_index_cbond", "中债综合指数", "指标+期限+日期"),
]

template = '''"""
{name}数据集合测试
API: {api}
集合: {collection}
唯一标识: {unique_key}
"""

import pytest
from datetime import datetime
from app.core.database import get_mongo_db, init_database, close_database


class Test{class_name}Collection:
    """{ name}测试"""
    
    @pytest.fixture(scope="class", autouse=True)
    async def setup_database(self):
        await init_database()
        yield
        await close_database()
    
    @pytest.fixture
    async def collection(self):
        db = get_mongo_db()
        coll = db.get_collection("{collection}")
        await coll.delete_many({{}})
        yield coll
        await coll.delete_many({{}})
    
    async def test_collection_exists(self, collection):
        """测试集合是否可访问"""
        assert collection is not None
    
    async def test_insert_data(self, collection):
        """测试插入数据"""
        data = {{"test_field": "test_value", "更新时间": datetime.now()}}
        result = await collection.insert_one(data)
        assert result.inserted_id is not None
        
        count = await collection.count_documents({{}})
        assert count == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
'''

def generate_class_name(api_name):
    """生成类名"""
    parts = api_name.split('_')
    return ''.join([p.capitalize() for p in parts])

if __name__ == "__main__":
    import os
    
    base_dir = os.path.dirname(__file__)
    
    for num, api, name, unique_key in test_specs:
        class_name = generate_class_name(api)
        content = template.format(
            name=name,
            api=api,
            collection=api,
            unique_key=unique_key,
            class_name=class_name
        )
        
        filename = f"{num}_{api}_collection.py"
        filepath = os.path.join(base_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已生成: {filename}")
    
    print(f"\n🎉 完成！共生成{len(test_specs)}个测试文件")
