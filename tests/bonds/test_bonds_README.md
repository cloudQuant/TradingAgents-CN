# 债券功能测试文档

## 测试文件清单

### 1. `test_bonds_convertible.py` - 单元测试
测试可转债数据服务层的核心功能：
- ✅ 保存可转债比价表数据
- ✅ 查询可转债比价表
- ✅ 保存可转债价值分析数据
- ✅ 查询可转债价值分析
- ✅ 保存现券市场成交行情
- ✅ 债券代码规范化
- ✅ category字段默认值（bug修复验证）
- ✅ 溢价率计算
- ✅ 空DataFrame处理
- ✅ NaN值处理

### 2. `test_bonds_api.py` - 集成测试
测试债券API路由功能：
- ✅ 获取可转债比价表API
- ✅ 同步可转债比价数据API
- ✅ 获取可转债价值分析API
- ✅ 同步价值分析数据API
- ✅ 获取现券市场成交行情API
- ✅ 获取现券市场做市报价API
- ✅ API错误处理
- ✅ API分页功能
- ✅ API过滤功能

### 3. `test_bonds_provider.py` - 数据提供商测试
测试AKShare数据提供商：
- ✅ 获取可转债比价表
- ✅ 获取可转债价值分析
- ✅ 获取现券市场成交行情
- ✅ 获取现券市场做市报价
- ✅ 获取上交所市场概览
- ✅ 获取上交所成交概览
- ✅ 获取可转债详细信息
- ✅ 错误处理
- ✅ 空数据处理
- ✅ 代码规范化

## 运行测试

### 运行所有债券测试
```bash
cd f:\source_code\TradingAgents-CN
pytest tests/test_bonds_*.py -v
```

### 运行特定测试文件
```bash
# 单元测试
pytest tests/test_bonds_convertible.py -v

# API测试
pytest tests/test_bonds_api.py -v

# 数据提供商测试
pytest tests/test_bonds_provider.py -v
```

### 运行特定测试用例
```bash
# 测试category字段修复
pytest tests/test_bonds_convertible.py::test_category_field_not_null -v

# 测试溢价率计算
pytest tests/test_bonds_convertible.py::test_premium_rate_calculation -v
```

### 生成覆盖率报告
```bash
pytest tests/test_bonds_*.py --cov=app.services.bond_data_service --cov=app.routers.bonds --cov=tradingagents.dataflows.providers.china.bonds --cov-report=html
```

## 测试依赖

确保安装了以下测试依赖：
```bash
pip install pytest pytest-asyncio pytest-cov fastapi[test]
```

## 已发现并修复的Bug

### Bug 1: category字段为空导致数据无法查询 ✅已修复
**问题**：
- 当category字段为None或空字符串时，数据保存时会被过滤掉
- 导致后续按category查询时找不到数据

**修复**：
- 在`save_basic_list`方法中，确保category字段总是有值
- 空值默认设置为"other"
- 修改代码：`category_normalized = "other"` 而不是 `None`

**测试验证**：
- `test_category_field_not_null` 测试用例验证修复

### Bug 2: NaN值未正确处理 ✅已修复
**问题**：
- DataFrame中的NaN值可能导致MongoDB保存失败
- NaN值在JSON序列化时会出错

**修复**：
- 使用`pd.notna()`检查值是否为NaN
- 过滤掉NaN值或转换为None

**测试验证**：
- `test_nan_value_handling` 测试用例验证修复

### Bug 3: 空DataFrame未正确处理 ✅已修复
**问题**：
- 空DataFrame传入保存方法可能导致异常

**修复**：
- 在保存前检查DataFrame是否为空
- 空DataFrame直接返回0

**测试验证**：
- `test_empty_dataframe_handling` 测试用例验证修复

## 测试覆盖的功能模块

### 数据服务层 (`app/services/bond_data_service.py`)
- [x] save_cov_comparison()
- [x] save_cov_value_analysis()
- [x] save_spot_deals()
- [x] query_cov_comparison()
- [x] query_cov_value_analysis()
- [x] save_basic_list() (category字段修复)

### API路由层 (`app/routers/bonds.py`)
- [x] GET /api/bonds/convertible/comparison
- [x] POST /api/bonds/convertible/comparison/sync
- [x] GET /api/bonds/convertible/{code}/value-analysis
- [x] POST /api/bonds/convertible/{code}/value-analysis/sync
- [x] GET /api/bonds/market/spot-deals
- [x] GET /api/bonds/market/spot-quotes

### 数据提供商层 (`tradingagents/dataflows/providers/china/bonds.py`)
- [x] get_cov_comparison()
- [x] get_cov_value_analysis()
- [x] get_spot_deal()
- [x] get_spot_quote()
- [x] get_cash_summary()
- [x] get_deal_summary()
- [x] get_cov_info_detail()

## 测试策略

### 单元测试
- 使用Mock隔离外部依赖
- 测试单个函数的逻辑正确性
- 验证边界条件和异常处理

### 集成测试
- 测试API端到端流程
- 验证各层之间的集成
- 使用TestClient模拟HTTP请求

### 数据验证
- 验证数据格式正确性
- 验证数据类型转换
- 验证NaN和None的处理

## 持续改进

### 待添加的测试
- [ ] 性能测试（大数据量）
- [ ] 并发测试
- [ ] 数据一致性测试
- [ ] 实际AKShare接口测试（需要网络）

### 测试最佳实践
1. 每个功能都应有对应的测试用例
2. 测试用例应该独立，不依赖执行顺序
3. 使用有意义的测试名称
4. 添加必要的注释说明测试目的
5. 及时更新测试以反映代码变更

## 问题反馈

如发现测试失败或新的bug，请：
1. 记录失败的测试用例
2. 复现步骤
3. 预期行为 vs 实际行为
4. 相关日志和错误信息
