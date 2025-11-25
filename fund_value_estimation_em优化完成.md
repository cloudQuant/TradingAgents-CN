# fund_value_estimation_em 集合优化完成

## ✅ 完成的修改

### 1. 后端数据处理逻辑

#### 新增列名处理方法 (`_process_fund_value_estimation_columns`)
**位置：** `app/services/fund_refresh_service.py`

**功能：**
- 从列名中提取日期（格式：`YYYY-MM-DD`）
- 去除列名中的日期前缀
- 添加独立的"日期"字段

**示例转换：**
```
原始列名:
- 2025-11-24-估算数据-估算值
- 2025-11-24-估算数据-估算增长率
- 2025-11-24-公布数据-单位净值
- 2025-11-24-公布数据-日增长率
- 2025-11-21-单位净值

处理后:
- 估算数据-估算值
- 估算数据-估算增长率
- 公布数据-单位净值
- 公布数据-日增长率
- 单位净值
- 日期: 2025-11-24  (新增字段)
```

**核心代码：**
```python
def _process_fund_value_estimation_columns(self, df: pd.DataFrame) -> pd.DataFrame:
    import re
    
    # 提取日期（从列名中找到日期）
    date_pattern = re.compile(r'(\d{4}-\d{2}-\d{2})')
    dates_found = set()
    
    for col in df.columns:
        match = date_pattern.search(str(col))
        if match:
            dates_found.add(match.group(1))
    
    # 使用最新的日期作为数据日期
    if dates_found:
        estimation_date = sorted(dates_found, reverse=True)[0]
    else:
        from datetime import datetime
        estimation_date = datetime.now().strftime('%Y-%m-%d')
    
    # 重命名列：去除日期前缀
    new_columns = {}
    for col in df.columns:
        if date_pattern.search(str(col)):
            new_col = date_pattern.sub('', str(col)).lstrip('-')
            new_columns[col] = new_col
        else:
            new_columns[col] = col
    
    df = df.rename(columns=new_columns)
    
    # 添加日期字段
    df['日期'] = estimation_date
    
    return df
```

#### 修改刷新方法 (`_refresh_fund_value_estimation_em`)
**位置：** `app/services/fund_refresh_service.py`

**变更：**
- 在保存数据前调用列名处理方法
- 增加进度提示："正在处理列名和日期..."

```python
# 处理列名：提取日期并重命名列
df = self._process_fund_value_estimation_columns(df)
```

### 2. 数据保存逻辑优化

#### 修改保存方法 (`save_fund_value_estimation_em_data`)
**位置：** `app/services/fund_data_service.py`

**变更：**
- 使用新的"日期"字段替代"交易日"
- **唯一标识从 `code + trade_date` 改为 `code + date`**

**修改前：**
```python
fund_code = str(doc.get('基金代码', ''))
trade_date = str(doc.get('交易日', ''))
doc['code'] = fund_code
doc['trade_date'] = trade_date

ops.append(
    UpdateOne(
        {'code': fund_code, 'trade_date': trade_date},
        {'$set': doc},
        upsert=True
    )
)
```

**修改后：**
```python
fund_code = str(doc.get('基金代码', ''))
estimation_date = str(doc.get('日期', ''))  # 使用新增的日期字段
doc['code'] = fund_code
doc['date'] = estimation_date

# 以日期+基金代码作为唯一标识
ops.append(
    UpdateOne(
        {'code': fund_code, 'date': estimation_date},
        {'$set': doc},
        upsert=True
    )
)
```

**优势：**
- ✅ **数据唯一性保证** - 日期+基金代码组合唯一
- ✅ **避免重复数据** - 相同日期的同一基金只保存一次
- ✅ **支持历史数据** - 可以保存不同日期的估值数据

### 3. 前端界面增强

#### 添加集合支持
**位置：** `frontend/src/views/Funds/Collection.vue`

**变更：**
1. 在 `supportedCollections` 数组中添加 `'fund_value_estimation_em'`
2. 添加 `fundValueSymbol` 响应式变量（默认值："全部"）
3. 在API刷新对话框中添加基金类型选择配置

**UI配置：**
```vue
<!-- fund_value_estimation_em 特殊配置：基金类型选择 -->
<template v-if="collectionName === 'fund_value_estimation_em'">
  <el-divider content-position="left">基金类型选择</el-divider>
  <el-alert
    title="净值估算说明"
    type="info"
    :closable="false"
    style="margin-bottom: 12px;"
  >
    <div>获取东方财富网的基金净值估算数据，支持按基金类型筛选</div>
    <div style="margin-top: 4px;">数据将按【日期+基金代码】作为唯一标识保存</div>
  </el-alert>
  <el-form-item label="基金类型">
    <el-select v-model="fundValueSymbol" placeholder="请选择基金类型" style="width: 100%">
      <el-option label="全部" value="全部" />
      <el-option label="股票型" value="股票型" />
      <el-option label="混合型" value="混合型" />
      <el-option label="债券型" value="债券型" />
      <el-option label="指数型" value="指数型" />
      <el-option label="QDII" value="QDII" />
      <el-option label="ETF联接" value="ETF联接" />
      <el-option label="LOF" value="LOF" />
      <el-option label="场内交易基金" value="场内交易基金" />
    </el-select>
  </el-form-item>
</template>
```

**参数传递：**
```typescript
else if (collectionName.value === 'fund_value_estimation_em') {
  // 净值估算：传入基金类型参数
  params.symbol = fundValueSymbol.value
}
```

### 4. 数据流程

```
1. 前端选择基金类型 (fundValueSymbol)
   ↓
2. 调用后端 API: /api/funds/collections/fund_value_estimation_em/refresh
   参数: { symbol: "全部" }
   ↓
3. 后端获取 AKShare 数据
   原始列名: 2025-11-24-估算数据-估算值, 2025-11-24-公布数据-单位净值, ...
   ↓
4. 处理列名
   - 提取日期: 2025-11-24
   - 重命名列: 估算数据-估算值, 公布数据-单位净值, ...
   - 添加字段: 日期 = 2025-11-24
   ↓
5. 批量保存 (500条/批)
   唯一键: { code: "004260", date: "2025-11-24" }
   ↓
6. 返回结果
   成功保存 N 条记录
```

## 🎯 使用方法

1. 进入 funds/collections/fund_value_estimation_em 页面
2. 点击"更新数据"下拉菜单 → 选择"API刷新"
3. 在基金类型下拉框中选择类型（默认"全部"）
4. 点击"开始更新"
5. 等待进度完成

## 📊 数据结构

### MongoDB 存储格式

```json
{
  "_id": "...",
  "序号": 1,
  "基金代码": "004260",
  "基金名称": "德邦稳盈增长灵活配置混合A",
  "估算数据-估算值": "1.0102",
  "估算数据-估算增长率": "7.35%",
  "公布数据-单位净值": "1.0056",
  "公布数据-日增长率": "6.85%",
  "估算偏差": "0.50%",
  "单位净值": "0.9411",
  "日期": "2025-11-24",
  "code": "004260",
  "date": "2025-11-24",
  "source": "akshare",
  "endpoint": "fund_value_estimation_em",
  "updated_at": "2025-11-24T21:45:00"
}
```

### 唯一索引

- **组合键：** `{ code: 1, date: 1 }` (唯一)
- **说明：** 同一基金在同一日期只保存一条记录

## ✨ 优化亮点

1. **数据规范化** - 日期从列名中提取到独立字段
2. **列名简化** - 去除冗余的日期前缀，提高可读性
3. **唯一性保证** - 日期+基金代码作为联合主键
4. **历史追踪** - 可以保存不同日期的估值数据
5. **批量高效** - 500条/批次，支持大规模数据
6. **用户友好** - 前端提供基金类型筛选

## 📝 测试验证

运行测试脚本：
```bash
cd f:\source_code\TradingAgents-CN
python test_fund_value_estimation_process.py
```

**预期输出：**
- ✅ 成功提取日期: 2025-11-24
- ✅ 列名正确转换（去除日期前缀）
- ✅ 新增"日期"字段
- ✅ 唯一键：code=基金代码, date=日期

## 🔧 相关文件

- **后端服务:** `app/services/fund_refresh_service.py`
- **数据服务:** `app/services/fund_data_service.py`
- **前端组件:** `frontend/src/views/Funds/Collection.vue`
- **测试脚本:** `test_fund_value_estimation_process.py`
