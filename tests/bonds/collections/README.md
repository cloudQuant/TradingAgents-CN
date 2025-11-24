# 债券数据集合测试用例

本目录包含了所有债券数据集合的测试用例（03-34号需求）。

## 📁 目录结构

```
collections/
├── 03_bond_zh_hs_spot_collection.py              # 沪深债券实时行情
├── 04_bond_zh_hs_daily_collection.py             # 沪深债券历史行情
├── 05_bond_zh_hs_cov_spot_collection.py          # 可转债实时行情
├── 06_bond_zh_hs_cov_daily_collection.py         # 可转债历史行情
├── 07_bond_zh_cov_collection.py                  # 可转债数据一览表
├── 08_bond_cash_summary_sse_collection.py        # 债券现券市场概览
├── 09_bond_deal_summary_sse_collection.py        # 债券成交概览
├── 10_bond_debt_nafmii_collection.py             # 银行间市场债券发行数据
├── 11_bond_spot_quote_collection.py              # 现券市场做市报价
├── 12_bond_spot_deal_collection.py               # 现券市场成交行情
├── 13_bond_zh_hs_cov_min_collection.py           # 可转债分时行情
├── 14_bond_zh_hs_cov_pre_min_collection.py       # 可转债盘前分时
├── 15_bond_zh_cov_info_collection.py             # 可转债详情-东财
├── 16_bond_zh_cov_info_ths_collection.py         # 可转债详情-同花顺
├── 17-34...                                       # 其他测试用例（使用生成脚本创建）
├── _generate_remaining_tests.py                  # 批量生成测试用例脚本
└── README.md                                      # 本文件
```

## 🚀 快速开始

### 运行单个测试

```bash
# 运行沪深债券实时行情测试
pytest tests/bonds/collections/03_bond_zh_hs_spot_collection.py -v

# 运行可转债历史行情测试
pytest tests/bonds/collections/06_bond_zh_hs_cov_daily_collection.py -v
```

### 运行所有测试

```bash
# 运行所有债券集合测试
pytest tests/bonds/collections/ -v

# 运行特定模式的测试
pytest tests/bonds/collections/ -k "bond_zh" -v
```

### 批量生成剩余测试用例

如果需要生成17-34号的测试用例（如果尚未生成）：

```bash
cd tests/bonds/collections
python _generate_remaining_tests.py
```

## 📋 测试覆盖

### 已完成测试用例（03-16）

- ✅ **03**: 沪深债券实时行情 - `bond_zh_hs_spot`
- ✅ **04**: 沪深债券历史行情 - `bond_zh_hs_daily`
- ✅ **05**: 可转债实时行情 - `bond_zh_hs_cov_spot`
- ✅ **06**: 可转债历史行情 - `bond_zh_hs_cov_daily`
- ✅ **07**: 可转债数据一览表 - `bond_zh_cov`
- ✅ **08**: 债券现券市场概览 - `bond_cash_summary_sse`
- ✅ **09**: 债券成交概览 - `bond_deal_summary_sse`
- ✅ **10**: 银行间市场债券发行数据 - `bond_debt_nafmii`
- ✅ **11**: 现券市场做市报价 - `bond_spot_quote`
- ✅ **12**: 现券市场成交行情 - `bond_spot_deal`
- ✅ **13**: 可转债分时行情 - `bond_zh_hs_cov_min`
- ✅ **14**: 可转债盘前分时 - `bond_zh_hs_cov_pre_min`
- ✅ **15**: 可转债详情-东财 - `bond_zh_cov_info`
- ✅ **16**: 可转债详情-同花顺 - `bond_zh_cov_info_ths`

### 待生成测试用例（17-34）

使用 `_generate_remaining_tests.py` 脚本可快速生成以下测试用例：

- **17**: 可转债比价表 - `bond_cov_comparison`
- **18**: 可转债价值分析 - `bond_zh_cov_value_analysis`
- **19**: 上证质押式回购 - `bond_sh_buy_back_em`
- **20**: 深证质押式回购 - `bond_sz_buy_back_em`
- **21**: 质押式回购历史数据 - `bond_buy_back_hist_em`
- **22**: 可转债实时数据-集思录 - `bond_cb_jsl`
- **23**: 可转债强赎-集思录 - `bond_cb_redeem_jsl`
- **24**: 可转债等权指数-集思录 - `bond_cb_index_jsl`
- **25**: 转股价调整记录-集思录 - `bond_cb_adj_logs_jsl`
- **26**: 收益率曲线历史数据 - `bond_china_close_return`
- **27**: 中美国债收益率 - `bond_zh_us_rate`
- **28**: 国债发行 - `bond_treasure_issue_cninfo`
- **29**: 地方债发行 - `bond_local_government_issue_cninfo`
- **30**: 企业债发行 - `bond_corporate_issue_cninfo`
- **31**: 可转债发行 - `bond_cov_issue_cninfo`
- **32**: 可转债转股 - `bond_cov_stock_issue_cninfo`
- **33**: 中债新综合指数 - `bond_new_composite_index_cbond`
- **34**: 中债综合指数 - `bond_composite_index_cbond`

## 🧪 测试内容

每个测试用例文件通常包含以下测试：

1. **集合存在性测试** - 验证MongoDB集合可以访问
2. **数据插入测试** - 验证数据可以正确插入
3. **数据更新测试** - 验证数据可以正确更新（upsert）
4. **数据查询测试** - 验证数据可以正确查询
5. **分页测试** - 验证分页功能正常
6. **排序测试** - 验证排序功能正常
7. **筛选测试** - 验证条件筛选功能正常
8. **索引测试** - 验证索引创建正常
9. **批量操作测试** - 验证批量插入/更新功能

## 📝 测试编写规范

### 命名规范

- 文件名：`{编号}_{API接口名}_collection.py`
- 类名：`Test{API接口名驼峰}Collection`
- 测试方法：`test_{功能描述}`

### 测试结构

```python
import pytest
from datetime import datetime
from app.core.database import get_mongo_db, init_database, close_database

class TestXxxCollection:
    @pytest.fixture(scope="class", autouse=True)
    async def setup_database(self):
        await init_database()
        yield
        await close_database()
    
    @pytest.fixture
    async def collection(self):
        db = get_mongo_db()
        coll = db.get_collection("collection_name")
        await coll.delete_many({})
        yield coll
        await coll.delete_many({})
    
    async def test_xxx(self, collection):
        # 测试逻辑
        pass
```

## 🔧 环境配置

### 前置条件

1. MongoDB 服务运行中
2. Python 环境已配置
3. 依赖包已安装：
   ```bash
   pip install pytest pytest-asyncio motor pymongo
   ```

### 数据库配置

测试使用的数据库配置：

- 数据库名：`test_trading_agents` （测试环境）
- 连接字符串：从环境变量或配置文件读取

## 📊 测试报告

### 生成HTML测试报告

```bash
pytest tests/bonds/collections/ --html=report.html --self-contained-html
```

### 生成覆盖率报告

```bash
pytest tests/bonds/collections/ --cov=app.services --cov-report=html
```

## ⚠️ 注意事项

1. **测试隔离**：每个测试前后都会清空集合数据，确保测试独立性
2. **异步测试**：所有测试都使用 `async/await` 语法
3. **数据清理**：测试完成后自动清理测试数据
4. **索引创建**：某些测试会创建索引，可能需要额外时间

## 🆘 故障排除

### 问题：测试无法连接数据库

**解决方案**：
1. 检查MongoDB服务是否运行
2. 检查数据库连接配置
3. 检查网络连接

### 问题：测试超时

**解决方案**：
1. 增加pytest超时时间：`pytest --timeout=300`
2. 检查数据库性能
3. 减少测试数据量

### 问题：索引创建失败

**解决方案**：
1. 手动删除已存在的索引
2. 检查索引名称冲突
3. 查看数据库日志

## 📚 相关文档

- [需求文档目录](../requirements/README.md)
- [API文档](../../docs/API.md)
- [数据库设计文档](../../docs/Database.md)

## 🤝 贡献指南

如果需要添加新的测试用例：

1. 参考现有测试用例结构
2. 遵循命名规范
3. 确保测试独立性
4. 添加适当的注释
5. 运行测试确保通过

---

**更新时间**: 2024-11-23
**维护者**: Trading Agents Team
