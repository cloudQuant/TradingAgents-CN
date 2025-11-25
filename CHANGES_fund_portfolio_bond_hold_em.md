# fund_portfolio_bond_hold_em 参数修改说明

## 修改日期
2024-11-25

## 修改原因
参考 `fund_portfolio_hold_em` 的实现方式，`fund_portfolio_bond_hold_em` AKShare接口同样接受的是**年份参数**（如"2024"），而不是季度日期参数（如"2024-09-30"）。

## 测试验证
通过 `test_akshare_bond_hold.py` 验证：
- ✅ 年份参数 `"2024"` - 成功，返回101条记录
- ❌ 季度日期 `"2024-09-30"` - 失败，返回"No value to decode"

## 修改内容

### 1. 后端修改 (`app/services/fund_refresh_service.py`)

#### 1.1 函数签名更新
```python
# 修改前
def _fetch_fund_portfolio_bond_hold_em(self, symbol: str, date: str):
    """获取单个基金债券持仓"""
    df = ak.fund_portfolio_bond_hold_em(symbol=symbol, date=date)

# 修改后  
def _fetch_fund_portfolio_bond_hold_em(self, symbol: str, year: str):
    """获取单个基金债券持仓（同步方法，在线程池中执行）
    
    Args:
        symbol: 基金代码
        year: 查询年份 (YYYY)
    """
    df = ak.fund_portfolio_bond_hold_em(symbol=symbol, date=year)
```

#### 1.2 参数验证更新
```python
# 修改前
if not date:
    raise ValueError("必须提供 date 参数（格式: YYYY-MM-DD）")

# 修改后
if not batch_mode and not year:
    raise ValueError("单个更新必须提供 year 参数（格式: YYYY）")
```

#### 1.3 批量更新逻辑
```python
# 修改前：仅支持指定日期的批量更新
elif batch_mode:
    await self._update_task_progress(task_id, 5, f"开始批量刷新债券持仓 ({date})...")
    limit = params.get('limit', 100)
    fund_codes = []
    async for doc in self.data_service.col_fund_name_em.find({}, {'基金代码': 1}).limit(limit):
        fund_codes.append(code)
    
    for idx, code in enumerate(fund_codes):
        df = await loop.run_in_executor(_executor, self._fetch_fund_portfolio_bond_hold_em, code, date)

# 修改后：支持年份遍历和并发更新
elif batch_mode:
    # 生成年份列表
    years = []
    if year:
        years = [str(year_int)]
    else:
        years = [str(y) for y in range(2010, current_year + 1)]
    
    # 获取所有基金代码（不设置limit）
    fund_codes = []
    async for doc in self.data_service.col_fund_name_em.find({}, {'基金代码': 1}):
        fund_codes.append(code)
    
    # 并发更新
    async def update_one(code, y):
        async with semaphore:
            df = await loop.run_in_executor(_executor, self._fetch_fund_portfolio_bond_hold_em, code, y)
    
    tasks = []
    for code in fund_codes:
        for y in years:
            tasks.append(update_one(code, y))
    
    await asyncio.gather(*tasks)
```

### 2. 前端修改 (`frontend/src/views/Funds/Collection.vue`)

#### 2.1 UI界面更新
```vue
<!-- 新增完整的单个更新和批量更新UI -->
<template v-if="collectionName === 'fund_portfolio_bond_hold_em'">
  <!-- 单个更新 -->
  <el-divider content-position="left">单个更新</el-divider>
  <el-row :gutter="20">
    <el-col :span="12">
      <el-form-item label="基金代码">
        <el-input v-model="singleFundCode" placeholder="请输入基金代码（如 000001）" />
      </el-form-item>
    </el-col>
    <el-col :span="12">
      <el-form-item label="查询年份">
        <el-input v-model="singleYear" placeholder="如 2024" />
      </el-form-item>
    </el-col>
  </el-row>
  <el-button :disabled="!singleFundCode || !singleYear || refreshing">更新单个</el-button>
  
  <!-- 批量更新配置 -->
  <el-divider content-position="left">批量更新配置</el-divider>
  <el-row :gutter="20">
    <el-col :span="12">
      <el-form-item label="批量更新年份（可选）">
        <el-input v-model="batchYear" placeholder="留空更新所有年份，如 2024" />
      </el-form-item>
    </el-col>
    <el-col :span="12">
      <el-form-item label="并发数">
        <el-input-number v-model="concurrency" :min="1" :max="10" />
      </el-form-item>
    </el-col>
  </el-row>
</template>
```

#### 2.2 参数发送逻辑
```javascript
} else if (String(collectionName.value) === 'fund_portfolio_bond_hold_em') {
  if (actualMode === 'single') {
    // 单个更新：必须提供基金代码和年份
    if (!singleFundCode.value || !singleYear.value) {
      ElMessage.warning('请输入基金代码和查询年份')
      return
    }
    params.fund_code = singleFundCode.value
    params.year = singleYear.value
  } else {
    // 批量更新模式：从 fund_name_em 获取所有代码，遍历年份
    params.batch = true
    params.concurrency = concurrency.value
    // year 参数可选，为空时更新2010-今年所有年份
    if (batchYear.value) {
      params.year = batchYear.value
    }
  }
}
```

#### 2.3 集合列表更新
```javascript
// 添加到支持的集合列表
const supportedCollections = [..., 'fund_portfolio_bond_hold_em']
const singleUpdateCollections = [..., 'fund_portfolio_bond_hold_em']
```

### 3. 测试用例更新 (`tests/funds/test_fund_portfolio_bond_hold_em.py`)

```python
# 修改前
json={"fund_code": "000001", "date": "2024-09-30"}
json={"batch": True, "limit": 10, "date": "2024-09-30"}

# 修改后
json={"fund_code": "000001", "year": "2024"}
json={"batch": True, "year": "2024"}
```

## 主要改进

### 单个更新
- **参数变化**：`fund_code` + `date` → `fund_code` + `year`
- **UI增强**：新增完整的单个更新表单（之前没有）
- **返回数据**：该基金在该年份的所有债券持仓数据（包含所有季度）

### 批量更新
- **参数变化**：
  - 移除 `limit` 参数限制
  - `date` 必需 → `year` 可选
- **行为变化**：
  - 指定年份：只更新该年份
  - 不指定年份：更新2010年至今所有年份
- **并发优化**：
  - 使用 `asyncio.Semaphore` 控制并发数
  - 从顺序执行改为并发执行
  - 支持配置并发数（默认3）
- **任务数量**：从 `基金数 × 1` 变为 `基金数 × 年份数`

## 性能影响
- **与股票持仓一致**：使用相同的年份参数模式
- **并发控制**：通过Semaphore限制并发，避免API限流
- **灵活性提升**：支持指定年份或全量更新

## 对比 fund_portfolio_hold_em
两个集合现在使用完全相同的实现模式：
- ✅ 都使用年份参数
- ✅ 都支持单个更新和批量更新
- ✅ 都支持并发控制
- ✅ 都支持年份可选（默认全量更新）
- ✅ 前端UI完全一致

## 验证方法

### 1. API测试
```bash
python test_akshare_bond_hold.py
```

### 2. 单元测试
```bash
pytest tests/funds/test_fund_portfolio_bond_hold_em.py -v
```

## 注意事项
1. ⚠️ **数据兼容性**：返回的数据中仍包含"季度"字段，数据库存储结构不需要变化
2. ⚠️ **唯一标识**：数据唯一标识：`基金代码 + 债券代码 + 季度`
3. ⚠️ **历史数据**：已存储的数据不受影响

## 相关文件
- 后端服务：`app/services/fund_refresh_service.py` (行5775-5773)
- 前端界面：`frontend/src/views/Funds/Collection.vue` (行1103-1171, 3411-3439)
- 测试用例：`tests/funds/test_fund_portfolio_bond_hold_em.py`
- 验证脚本：`test_akshare_bond_hold.py`

## 与基金持仓的一致性
本次修改确保了 `fund_portfolio_bond_hold_em` (债券持仓) 与 `fund_portfolio_hold_em` (股票持仓) 使用完全相同的实现模式，提升了代码的一致性和可维护性。
