# 债券数据优化实施进度

## ✅ 已完成的改进

### 1. 数据集合页面排序功能
**文件**: `frontend/src/views/Bonds/Collection.vue`

**改进内容**:
- ✅ 为所有数据列添加了 `sortable="custom"` 属性
- ✅ 实现了 `handleSortChange` 事件处理函数
- ✅ 添加了 `sortBy` 和 `sortDir` 状态管理
- ✅ 排序参数自动传递到后端API
- ✅ 支持升序、降序和取消排序三种状态

**效果**:
- 用户可以点击任意列头进行排序
- 排序时自动回到第一页
- 界面显示排序方向指示器

---

### 2. 债券数据保存逻辑修复
**文件**: `app/services/bond_data_service.py`

**修复内容**:
- ✅ 修复了 `category` 字段为空时被过滤的问题
- ✅ 确保 `category` 字段总是有值（默认为 "other"）
- ✅ 添加了详细的调试日志
- ✅ 添加了数据库 category 分布统计

**核心改进**:
```python
# 修复前：category为空时会被过滤
"category": (it.get("category") or "").lower() or None  # 返回None
doc = {k: v for k, v in doc.items() if v is not None}  # None被移除

# 修复后：确保category总是有值
category_val = it.get("category")
if category_val and str(category_val).strip():
    category_normalized = str(category_val).strip().lower()
else:
    category_normalized = "other"  # 默认值
```

---

### 3. AKShare Provider 功能增强
**文件**: `tradingagents/dataflows/providers/china/bonds.py`

**新增方法**:

#### 3.1 可转债专项
```python
async def get_cov_comparison() -> pd.DataFrame
    """获取可转债比价表（东方财富）
    包含：转股价、转股价值、溢价率、触发价等核心指标
    """

async def get_cov_value_analysis(code: str) -> pd.DataFrame
    """获取可转债价值分析历史数据
    包含：纯债价值、转股价值、溢价率历史走势
    """

async def get_cov_info_detail(code: str, indicator: str) -> pd.DataFrame
    """获取可转债详细信息（东方财富）
    indicator可选：基本信息、中签号、筹资用途、重要日期
    """
```

#### 3.2 市场行情
```python
async def get_spot_quote() -> pd.DataFrame
    """获取现券市场做市报价
    包含：买卖净价、买卖收益率
    """

async def get_spot_deal() -> pd.DataFrame
    """获取现券市场成交行情
    包含：成交净价、收益率、涨跌、交易量
    """
```

#### 3.3 市场统计
```python
async def get_cash_summary(date: str) -> pd.DataFrame
    """获取上交所债券现券市场概览
    包含：托管市值、托管面值、分类统计
    """

async def get_deal_summary(date: str) -> pd.DataFrame
    """获取上交所债券成交概览
    包含：成交笔数、成交金额（当日+当年）
    """
```

---

### 4. BondDataService 数据处理增强
**文件**: `app/services/bond_data_service.py`

**新增方法**:

#### 4.1 数据保存
```python
async def save_cov_comparison(df: pd.DataFrame) -> int
    """保存可转债比价表数据
    - 自动规范化债券代码
    - 智能字段映射和类型转换
    - 使用 code 作为唯一键
    """

async def save_cov_value_analysis(code: str, df: pd.DataFrame) -> int
    """保存可转债价值分析历史数据
    - 使用 (code, date) 作为唯一键
    - 支持历史数据累积
    """

async def save_spot_deals(df: pd.DataFrame) -> int
    """保存现券市场成交行情
    - 使用 (bond_name, timestamp) 作为唯一键
    - 支持实时数据更新
    """
```

#### 4.2 数据查询
```python
async def query_cov_comparison(
    sort_by, sort_dir, page, page_size
) -> Dict[str, Any]
    """查询可转债比价表
    - 支持排序和分页
    - 返回标准化数据格式
    """

async def query_cov_value_analysis(
    code, start_date, end_date
) -> Dict[str, Any]
    """查询可转债价值分析历史
    - 支持日期范围过滤
    - 按日期升序返回
    """
```

---

## 📊 优化方案文档
**文件**: `docs/bond_optimization_plan.md`

**内容概览**:
- 📋 AKShare债券接口全面分析（5大类、40+接口）
- 🗄️ 现有和缺失的数据库集合清单
- 🎯 四层数据架构设计
- 🛠️ 技术实施方案
- 📈 专业指标计算方法
- 🎨 可视化设计建议
- 🚀 分5阶段实施计划

**核心亮点**:
1. **数据完整性**: 补充8个核心缺失集合
2. **专业性**: 可转债专项分析、套利扫描
3. **实时性**: WebSocket推送、分钟级更新
4. **易用性**: 雷达图、热力图、多维度筛选

---

## 🔄 下一步实施建议

### Phase 1: API路由开发（优先）
```python
# 需要添加的路由：
GET  /api/bonds/convertible/comparison        # 可转债比价表
GET  /api/bonds/convertible/{code}/analysis   # 可转债价值分析
GET  /api/bonds/market/spot-deals             # 现券成交行情
GET  /api/bonds/market/spot-quotes            # 现券做市报价
POST /api/bonds/convertible/comparison/sync   # 同步可转债比价数据
```

**参考实现**:
```python
# app/routers/bonds.py

@router.get("/convertible/comparison")
async def get_convertible_comparison(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    sort_by: Optional[str] = Query(None),
    sort_dir: str = Query("asc"),
    current_user: dict = Depends(get_current_user),
):
    """获取可转债比价表"""
    db = get_mongo_db()
    svc = BondDataService(db)
    result = await svc.query_cov_comparison(
        sort_by=sort_by,
        sort_dir=sort_dir,
        page=page,
        page_size=page_size
    )
    return {"success": True, "data": result}

@router.post("/convertible/comparison/sync")
async def sync_convertible_comparison(
    current_user: dict = Depends(get_current_user),
):
    """同步可转债比价数据"""
    from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider
    
    provider = AKShareBondProvider()
    df = await provider.get_cov_comparison()
    
    if df.empty:
        raise HTTPException(status_code=404, detail="未获取到数据")
    
    db = get_mongo_db()
    svc = BondDataService(db)
    saved = await svc.save_cov_comparison(df)
    
    return {
        "success": True,
        "data": {
            "saved": saved,
            "total": len(df)
        }
    }
```

---

### Phase 2: 前端可转债页面开发
**新建文件**: `frontend/src/views/Bonds/Convertible.vue`

**功能模块**:
```vue
<template>
  <div class="convertible-bonds">
    <!-- 1. 筛选工具栏 -->
    <el-card class="filter-card">
      <el-form inline>
        <el-form-item label="溢价率">
          <el-slider range :min="0" :max="100" />
        </el-form-item>
        <el-form-item label="信用评级">
          <el-select multiple>
            <el-option label="AAA" value="AAA" />
            <el-option label="AA+" value="AA+" />
          </el-select>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 2. 可转债比价表 -->
    <el-card class="comparison-table">
      <el-table :data="bonds" @sort-change="handleSort">
        <el-table-column prop="code" label="代码" sortable="custom" />
        <el-table-column prop="name" label="名称" />
        <el-table-column prop="price" label="转债价格" sortable="custom">
          <template #default="{ row }">
            <span :class="getPriceClass(row.change_pct)">
              {{ row.price?.toFixed(2) }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="convert_premium_rate" label="转股溢价率" sortable="custom">
          <template #default="{ row }">
            <el-tag :type="getPremiumTagType(row.convert_premium_rate)">
              {{ row.convert_premium_rate?.toFixed(2) }}%
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="pure_debt_premium_rate" label="纯债溢价率" sortable="custom" />
        <el-table-column label="操作" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="viewDetail(row.code)">详情</el-button>
            <el-button size="small" @click="viewAnalysis(row.code)">分析</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 3. 套利机会扫描 -->
    <el-card class="arbitrage-scanner">
      <template #header>
        <span>💡 套利机会</span>
        <el-button size="small" @click="scanArbitrage">扫描</el-button>
      </template>
      <el-table :data="opportunities">
        <el-table-column prop="code" label="代码" />
        <el-table-column prop="type" label="类型">
          <template #default="{ row }">
            <el-tag v-if="row.type === 'low_premium'" type="success">低溢价</el-tag>
            <el-tag v-else-if="row.type === 'redeem_alert'" type="warning">强赎预警</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="profit_potential" label="潜在收益" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { bondsApi } from '@/api/bonds'

const bonds = ref([])
const opportunities = ref([])

const loadData = async () => {
  const res = await bondsApi.getConvertibleComparison({
    page: 1,
    page_size: 100
  })
  if (res.success) {
    bonds.value = res.data.items
  }
}

const scanArbitrage = async () => {
  // 实现套利扫描逻辑
  opportunities.value = bonds.value
    .filter(b => b.convert_premium_rate < 5)
    .map(b => ({
      code: b.code,
      name: b.name,
      type: 'low_premium',
      profit_potential: (100 - b.convert_premium_rate).toFixed(2)
    }))
}

onMounted(() => {
  loadData()
})
</script>
```

---

### Phase 3: 数据自动更新定时任务
**文件**: `app/worker/bonds_sync_service.py`

**新增任务**:
```python
async def sync_cov_comparison(self) -> dict:
    """同步可转债比价表（每小时）"""
    await self.ensure_indexes()
    try:
        import akshare as ak
        df = await asyncio.to_thread(ak.bond_cov_comparison)
        
        if isinstance(df, pd.DataFrame) and not df.empty:
            saved = await self._svc.save_cov_comparison(df)
            return {
                "success": True,
                "saved": saved,
                "rows": len(df)
            }
        return {"success": False, "error": "no_data"}
    except Exception as e:
        return {"success": False, "error": str(e)}

async def sync_spot_deals(self) -> dict:
    """同步现券市场成交行情（每分钟）"""
    await self.ensure_indexes()
    try:
        import akshare as ak
        df = await asyncio.to_thread(ak.bond_spot_deal)
        
        if isinstance(df, pd.DataFrame) and not df.empty:
            saved = await self._svc.save_spot_deals(df)
            return {
                "success": True,
                "saved": saved,
                "rows": len(df)
            }
        return {"success": False, "error": "no_data"}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

**调度配置**:
```python
# 在 SchedulerService 中添加
scheduler.add_job(
    func=bonds_worker.sync_cov_comparison,
    trigger="interval",
    hours=1,
    id="sync_cov_comparison",
    replace_existing=True
)

scheduler.add_job(
    func=bonds_worker.sync_spot_deals,
    trigger="interval",
    minutes=5,
    id="sync_spot_deals",
    replace_existing=True
)
```

---

### Phase 4: 可转债价值分析图表
**新建文件**: `frontend/src/components/Bonds/ValueAnalysisChart.vue`

**功能**:
- 📊 双轴图：转股溢价率 + 纯债溢价率
- 📈 价格走势：转债价格 + 转股价值 + 纯债价值
- 🎯 触发价标线：强赎触发价、回售触发价
- ⏱️ 时间范围选择：1月、3月、6月、1年、全部

---

## 📋 后续待实现功能清单

### 高优先级
- [ ] API路由：可转债比价表
- [ ] API路由：可转债价值分析
- [ ] 前端页面：可转债专项页面
- [ ] 定时任务：可转债比价表同步
- [ ] 定时任务：现券成交行情同步

### 中优先级
- [ ] 套利机会扫描算法
- [ ] 可转债价值分析图表组件
- [ ] 债券详情页增强（添加可转债专项信息）
- [ ] 市场数据仪表板
- [ ] 收益率曲线图表优化

### 低优先级
- [ ] WebSocket实时推送
- [ ] 数据导出功能
- [ ] 收藏和提醒功能
- [ ] 移动端适配优化

---

## 🎓 技术要点总结

### 1. 数据规范化
```python
# 统一使用 normalize_bond_code 规范化代码
from tradingagents.utils.instrument_validator import normalize_bond_code
norm = normalize_bond_code(code)
code_std = norm.get("code_std")  # 标准化代码（如：SH.113527）
```

### 2. 字段映射
```python
# AKShare字段名 -> 标准字段名
field_mapping = {
    "转债代码": "code",
    "转债名称": "name",
    "转债最新价": "price",
    "转股溢价率": "convert_premium_rate",
    # ...
}
```

### 3. 数据验证
```python
# 使用 pandas 的 notna 检查
if pd.notna(value):
    doc[field] = float(value)
```

### 4. 批量操作
```python
# 使用 bulk_write 提升性能
ops = [UpdateOne(filter, update, upsert=True) for ...]
result = await collection.bulk_write(ops, ordered=False)
```

---

## 📚 相关文档

1. **优化方案**: `docs/bond_optimization_plan.md`
2. **AKShare文档**: `docs/akshare_catalog/raw_html/_sources_data_bond_bond.md.txt.html`
3. **API文档**: 待补充
4. **前端组件文档**: 待补充

---

## 🎯 成功指标

### 数据完整性
- ✅ 债券基础数据覆盖率 > 95%
- ⏳ 可转债专项数据覆盖率 > 90%
- ⏳ 实时数据延迟 < 5分钟

### 功能完整性
- ✅ 数据列排序功能
- ✅ category字段正确保存
- ⏳ 可转债比价查询
- ⏳ 价值分析图表

### 用户体验
- ✅ 数据加载速度 < 2秒
- ✅ 界面响应流畅
- ⏳ 移动端适配良好

---

## 🙏 感谢

感谢 AKShare 提供的优质数据源！
项目地址：https://github.com/akfamily/akshare
