# fund_portfolio_hold_em 参数修改说明

## 修改日期
2024-11-25

## 修改原因
`fund_portfolio_hold_em` AKShare接口实际接受的是**年份参数**（如"2024"），而不是季度日期参数（如"2024-09-30"）。

## 测试验证
通过 `test_akshare_portfolio.py` 验证：
- ✅ 年份参数 `"2024"` - 成功，返回369条记录
- ❌ 季度日期 `"2024-09-30"` - 失败，返回"No value to decode"
- ❌ 季度格式 `"2024-Q3"` - 失败，返回"No value to decode"

## 修改内容

### 1. 后端修改 (`app/services/fund_refresh_service.py`)

#### 1.1 函数签名更新
```python
# 修改前
def _fetch_fund_portfolio_hold_em(self, symbol: str, date: str):
    """
    Args:
        date: 查询日期 (YYYY-MM-DD)
    """
    df = ak.fund_portfolio_hold_em(symbol=symbol, date=date)

# 修改后  
def _fetch_fund_portfolio_hold_em(self, symbol: str, year: str):
    """
    Args:
        year: 查询年份 (YYYY)
    """
    df = ak.fund_portfolio_hold_em(symbol=symbol, date=year)
```

#### 1.2 参数验证更新
```python
# 修改前
if not batch_mode and not date:
    raise ValueError("单个更新必须提供 date 参数（格式: YYYY-MM-DD）")

# 修改后
if not batch_mode and not year:
    raise ValueError("单个更新必须提供 year 参数（格式: YYYY）")
```

#### 1.3 批量更新逻辑
```python
# 修改前：生成季度日期列表
quarter_dates = []
if year:
    quarter_dates = [
        f"{year_int}-03-31",
        f"{year_int}-06-30",
        f"{year_int}-09-30",
        f"{year_int}-12-31"
    ]
else:
    for y in range(2010, current_year + 1):
        quarter_dates.extend([...])

# 修改后：生成年份列表
years = []
if year:
    years = [str(year_int)]
else:
    years = [str(y) for y in range(2010, current_year + 1)]
```

#### 1.4 返回结果更新
```python
# 修改前
return {
    "total_quarters": len(quarter_dates),
    ...
}

# 修改后
return {
    "total_years": len(years),
    ...
}
```

### 2. 前端修改 (`frontend/src/views/Funds/Collection.vue`)

#### 2.1 UI界面更新
```vue
<!-- 修改前 -->
<el-form-item label="查询日期">
  <el-input v-model="singleDate" placeholder="如 2024-09-30" />
</el-form-item>
<el-button :disabled="!singleFundCode || !singleDate || refreshing">

<!-- 修改后 -->
<el-form-item label="查询年份">
  <el-input v-model="singleYear" placeholder="如 2024" />
</el-form-item>
<el-button :disabled="!singleFundCode || !singleYear || refreshing">
```

#### 2.2 变量定义
```javascript
// 新增
const batchYear = ref('')  // fund_portfolio_hold_em 的批量更新年份参数
```

#### 2.3 参数发送逻辑
```javascript
// 修改前
if (actualMode === 'single') {
    params.fund_code = singleFundCode.value
    params.date = singleDate.value
} else {
    params.batch = true
    if (singleYear.value) {
        params.year = singleYear.value
    }
}

// 修改后
if (actualMode === 'single') {
    params.fund_code = singleFundCode.value
    params.year = singleYear.value
} else {
    params.batch = true
    if (batchYear.value) {
        params.year = batchYear.value
    }
}
```

#### 2.4 说明文本更新
```vue
<!-- 修改前 -->
<div>📅 自动遍历每个季度（3/31, 6/30, 9/30, 12/31）</div>
<div>💡 指定年份时：只更新该年份的4个季度</div>

<!-- 修改后 -->
<div>📅 自动遍历指定年份获取持仓数据</div>
<div>💡 指定年份时：只更新该年份的持仓数据</div>
```

### 3. 测试用例更新 (`tests/funds/test_fund_portfolio_hold_em.py`)

```python
# 修改前
json={"fund_code": "000001", "date": "2024-09-30"}

# 修改后
json={"fund_code": "000001", "year": "2024"}
```

## 影响范围

### 单个更新
- 参数：`fund_code` + `year` (如 "2024")
- 返回：该基金在该年份的所有持仓数据（包含所有季度）

### 批量更新
- 参数：`batch=True` + 可选的 `year`
- 行为：
  - 指定年份：只更新该年份
  - 不指定年份：更新2010年至今所有年份
- 减少任务数：原来是 `基金数 × 年份数 × 4个季度`，现在是 `基金数 × 年份数`

## 性能影响
- **任务数量减少75%**：从每年4个季度请求减少到每年1个请求
- **API调用减少**：大幅降低对AKShare接口的请求次数
- **更新速度提升**：批量更新完成时间显著缩短

## 验证方法

### 1. 参数验证脚本
```bash
python test_portfolio_params.py
```

### 2. 实际API测试
```bash
python test_akshare_portfolio.py
```

### 3. 单元测试
```bash
pytest tests/funds/test_fund_portfolio_hold_em.py -v
```

## 注意事项
1. ⚠️ **数据兼容性**：虽然参数改为年份，但返回的数据中仍包含"季度"字段（如"2024-09-30"），数据库存储结构不需要变化
2. ⚠️ **唯一标识**：数据唯一标识仍然是：`基金代码 + 股票代码 + 季度`
3. ⚠️ **历史数据**：已存储的数据不受影响，可以正常查询和使用

## 回滚方案
如需回滚，将以下文件恢复到修改前的版本：
- `app/services/fund_refresh_service.py`
- `frontend/src/views/Funds/Collection.vue`
- `tests/funds/test_fund_portfolio_hold_em.py`

## 相关文件
- 后端服务：`app/services/fund_refresh_service.py` (行5579-5773)
- 前端界面：`frontend/src/views/Funds/Collection.vue` (行1033-1100, 3157-3339)
- 测试用例：`tests/funds/test_fund_portfolio_hold_em.py`
- 验证脚本：`test_portfolio_params.py`, `test_akshare_portfolio.py`
