# 实现指南：news_report_time_baidu（财报发行）

## 需求概览
- **集合名称**: news_report_time_baidu
- **显示名称**: 财报发行
- **数据源**: AKShare `news_report_time_baidu` 接口
- **需求文档**: 124_财报发行-完成.md

## 数据字段
| 字段名 | 类型 | 描述 |
|--------|------|------|
| 股票代码 | object | 股票代码 |
| 交易所 | object | 交易所 |
| 股票简称 | object | 股票简称 |
| 财报期 | object | 财报期 |

## 实现步骤

### 1. 后端实现

#### 1.1 创建 Provider
位置: `F:\source_code\TradingAgents-CN\app\services\stock\providers\news_report_time_baidu_provider.py`

```python
"""
百度股市通-财报发行数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class NewsReportTimeBaiduProvider:
    """百度股市通-财报发行数据提供者"""
    
    def __init__(self):
        self.collection_name = "news_report_time_baidu"
        self.display_name = "财报发行"
        
    def fetch_data(self, date: str = None) -> pd.DataFrame:
        """
        获取财报发行数据
        
        Args:
            date: 日期，格式为 YYYYMMDD，如 "20241107"
            
        Returns:
            DataFrame: 财报发行数据
        """
        try:
            if date is None:
                date = datetime.now().strftime("%Y%m%d")
            
            logger.info(f"Fetching news_report_time_baidu data for date: {date}")
            df = ak.news_report_time_baidu(date=date)
            
            if df.empty:
                logger.warning(f"No data returned for date: {date}")
                return pd.DataFrame()
            
            # 添加元数据
            df['scraped_at'] = datetime.now()
            df['date'] = date
            
            logger.info(f"Successfully fetched {len(df)} records")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching news_report_time_baidu data: {e}")
            raise
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        """获取字段信息"""
        return [
            {"name": "股票代码", "type": "string", "description": "股票代码"},
            {"name": "交易所", "type": "string", "description": "交易所"},
            {"name": "股票简称", "type": "string", "description": "股票简称"},
            {"name": "财报期", "type": "string", "description": "财报期"},
            {"name": "date", "type": "string", "description": "查询日期"},
            {"name": "scraped_at", "type": "datetime", "description": "抓取时间"},
        ]
```

#### 1.2 创建 Service
位置: `F:\source_code\TradingAgents-CN\app\services\stock\news_report_time_baidu_service.py`

```python
"""
百度股市通-财报发行服务
"""
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging
from motor.motor_asyncio import AsyncIOMotorClient

from .providers.news_report_time_baidu_provider import NewsReportTimeBaiduProvider

logger = logging.getLogger(__name__)


class NewsReportTimeBaiduService:
    """百度股市通-财报发行服务"""
    
    def __init__(self, db: AsyncIOMotorClient):
        self.db = db
        self.collection = db.stocks.news_report_time_baidu
        self.provider = NewsReportTimeBaiduProvider()
        
    async def get_overview(self) -> Dict[str, Any]:
        """获取数据概览"""
        total_count = await self.collection.count_documents({})
        
        # 获取最新/最旧记录
        latest = await self.collection.find_one(sort=[("scraped_at", -1)])
        oldest = await self.collection.find_one(sort=[("scraped_at", 1)])
        
        # 统计不同交易所
        pipeline = [
            {"$group": {"_id": "$交易所", "count": {"$sum": 1}}}
        ]
        exchanges = await self.collection.aggregate(pipeline).to_list(None)
        
        return {
            "total_count": total_count,
            "latest_date": latest.get("date") if latest else None,
            "oldest_date": oldest.get("date") if oldest else None,
            "last_updated": latest.get("scraped_at") if latest else None,
            "exchanges": {item["_id"]: item["count"] for item in exchanges},
        }
    
    async def get_data(
        self,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """获取数据列表"""
        query = filters or {}
        
        cursor = self.collection.find(query).skip(skip).limit(limit).sort("scraped_at", -1)
        data = await cursor.to_list(length=limit)
        
        total = await self.collection.count_documents(query)
        
        # 转换 ObjectId 为字符串
        for item in data:
            item["_id"] = str(item["_id"])
            if "scraped_at" in item and isinstance(item["scraped_at"], datetime):
                item["scraped_at"] = item["scraped_at"].isoformat()
        
        return {
            "data": data,
            "total": total,
            "skip": skip,
            "limit": limit,
        }
    
    async def refresh_data(self, date: str = None) -> Dict[str, Any]:
        """刷新数据"""
        try:
            df = self.provider.fetch_data(date)
            
            if df.empty:
                return {
                    "success": True,
                    "message": "No data available for the specified date",
                    "inserted": 0,
                }
            
            # 转换为字典列表
            records = df.to_dict('records')
            
            # 批量插入或更新
            operations = []
            for record in records:
                # 使用股票代码和日期作为唯一标识
                filter_doc = {
                    "股票代码": record.get("股票代码"),
                    "date": record.get("date"),
                }
                operations.append({
                    "filter": filter_doc,
                    "update": {"$set": record},
                    "upsert": True,
                })
            
            if operations:
                from pymongo import UpdateOne
                bulk_ops = [UpdateOne(op["filter"], op["update"], upsert=op["upsert"]) for op in operations]
                result = await self.collection.bulk_write(bulk_ops)
                
                return {
                    "success": True,
                    "message": "Data refreshed successfully",
                    "inserted": result.upserted_count,
                    "updated": result.modified_count,
                }
            
            return {
                "success": True,
                "message": "No operations performed",
                "inserted": 0,
            }
            
        except Exception as e:
            logger.error(f"Error refreshing data: {e}")
            return {
                "success": False,
                "message": str(e),
                "inserted": 0,
            }
    
    async def clear_data(self) -> Dict[str, Any]:
        """清空数据"""
        result = await self.collection.delete_many({})
        return {
            "success": True,
            "message": f"Deleted {result.deleted_count} records",
            "deleted": result.deleted_count,
        }
```

#### 1.3 添加 API 路由
位置: `F:\source_code\TradingAgents-CN\app\routers\stocks.py`

在路由文件中添加以下端点：

```python
@router.get("/collections/news_report_time_baidu")
async def get_news_report_time_baidu(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取财报发行数据"""
    service = NewsReportTimeBaiduService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/news_report_time_baidu/overview")
async def get_news_report_time_baidu_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取财报发行数据概览"""
    service = NewsReportTimeBaiduService(db)
    return await service.get_overview()


@router.post("/collections/news_report_time_baidu/refresh")
async def refresh_news_report_time_baidu(
    date: Optional[str] = None,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新财报发行数据"""
    service = NewsReportTimeBaiduService(db)
    return await service.refresh_data(date=date)


@router.delete("/collections/news_report_time_baidu/clear")
async def clear_news_report_time_baidu(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空财报发行数据"""
    service = NewsReportTimeBaiduService(db)
    return await service.clear_data()
```

#### 1.4 注册到集合列表
在 `stocks.py` 的集合列表中添加：

```python
collections = [
    # ... 其他集合
    {
        "name": "news_report_time_baidu",
        "display_name": "财报发行",
        "description": "百度股市通-财报发行数据",
        "route": "/stocks/collections/news_report_time_baidu",
        "fields": NewsReportTimeBaiduProvider().get_field_info(),
    },
]
```

### 2. 前端实现

#### 2.1 创建页面组件
位置: `F:\source_code\TradingAgents-CN\frontend\src\views\Stocks\Collections\NewsReportTimeBaidu.vue`

```vue
<template>
  <div class="news-report-time-baidu-container">
    <el-card class="header-card">
      <h2>财报发行</h2>
      <p class="description">百度股市通-财报发行数据</p>
    </el-card>

    <!-- 数据概览 -->
    <el-card class="overview-card">
      <h3>数据概览</h3>
      <el-row :gutter="20">
        <el-col :span="6">
          <div class="stat-item">
            <div class="stat-value">{{ overview.total_count || 0 }}</div>
            <div class="stat-label">总记录数</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-item">
            <div class="stat-value">{{ overview.latest_date || '-' }}</div>
            <div class="stat-label">最新日期</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-item">
            <div class="stat-value">{{ formatDate(overview.last_updated) }}</div>
            <div class="stat-label">最后更新</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-item">
            <div class="stat-value">{{ Object.keys(overview.exchanges || {}).length }}</div>
            <div class="stat-label">交易所数量</div>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <!-- 操作按钮 -->
    <el-card class="actions-card">
      <el-row :gutter="10">
        <el-col :span="4">
          <el-button type="primary" @click="refreshData" :loading="loading">
            <el-icon><Refresh /></el-icon>
            刷新数据
          </el-button>
        </el-col>
        <el-col :span="4">
          <el-button type="danger" @click="clearData" :loading="loading">
            <el-icon><Delete /></el-icon>
            清空数据
          </el-button>
        </el-col>
        <el-col :span="4">
          <el-date-picker
            v-model="selectedDate"
            type="date"
            placeholder="选择日期"
            format="YYYY-MM-DD"
            value-format="YYYYMMDD"
          />
        </el-col>
      </el-row>
    </el-card>

    <!-- 数据表格 -->
    <el-card class="table-card">
      <el-table :data="tableData" v-loading="loading" stripe>
        <el-table-column prop="股票代码" label="股票代码" width="120" />
        <el-table-column prop="股票简称" label="股票简称" width="150" />
        <el-table-column prop="交易所" label="交易所" width="100" />
        <el-table-column prop="财报期" label="财报期" width="150" />
        <el-table-column prop="date" label="查询日期" width="120" />
        <el-table-column prop="scraped_at" label="抓取时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.scraped_at) }}
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Refresh, Delete } from '@element-plus/icons-vue'
import axios from 'axios'

const API_BASE = '/api/stocks/collections/news_report_time_baidu'

const loading = ref(false)
const overview = ref({})
const tableData = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)
const selectedDate = ref(null)

const loadOverview = async () => {
  try {
    const response = await axios.get(`${API_BASE}/overview`)
    overview.value = response.data
  } catch (error) {
    console.error('Failed to load overview:', error)
  }
}

const loadData = async () => {
  loading.value = true
  try {
    const skip = (currentPage.value - 1) * pageSize.value
    const response = await axios.get(API_BASE, {
      params: { skip, limit: pageSize.value }
    })
    tableData.value = response.data.data
    total.value = response.data.total
  } catch (error) {
    ElMessage.error('加载数据失败')
    console.error('Failed to load data:', error)
  } finally {
    loading.value = false
  }
}

const refreshData = async () => {
  loading.value = true
  try {
    const params = selectedDate.value ? { date: selectedDate.value } : {}
    const response = await axios.post(`${API_BASE}/refresh`, params)
    
    if (response.data.success) {
      ElMessage.success(`数据刷新成功！插入: ${response.data.inserted}, 更新: ${response.data.updated || 0}`)
      await loadOverview()
      await loadData()
    } else {
      ElMessage.error(response.data.message || '数据刷新失败')
    }
  } catch (error) {
    ElMessage.error('数据刷新失败')
    console.error('Failed to refresh data:', error)
  } finally {
    loading.value = false
  }
}

const clearData = async () => {
  try {
    await ElMessageBox.confirm('确定要清空所有数据吗？', '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    loading.value = true
    const response = await axios.delete(`${API_BASE}/clear`)
    
    if (response.data.success) {
      ElMessage.success(`已删除 ${response.data.deleted} 条记录`)
      await loadOverview()
      await loadData()
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('清空数据失败')
      console.error('Failed to clear data:', error)
    }
  } finally {
    loading.value = false
  }
}

const handleSizeChange = (val) => {
  pageSize.value = val
  loadData()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  loadData()
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleString('zh-CN')
}

onMounted(() => {
  loadOverview()
  loadData()
})
</script>

<style scoped>
.news-report-time-baidu-container {
  padding: 20px;
}

.header-card {
  margin-bottom: 20px;
}

.header-card h2 {
  margin: 0 0 10px 0;
}

.description {
  color: #666;
  margin: 0;
}

.overview-card {
  margin-bottom: 20px;
}

.stat-item {
  text-align: center;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

.actions-card {
  margin-bottom: 20px;
}

.table-card {
  margin-bottom: 20px;
}

.el-pagination {
  margin-top: 20px;
  justify-content: center;
}
</style>
```

#### 2.2 添加路由
位置: `F:\source_code\TradingAgents-CN\frontend\src\router\index.ts`

```typescript
{
  path: '/stocks/collections/news_report_time_baidu',
  name: 'NewsReportTimeBaidu',
  component: () => import('@/views/Stocks/Collections/NewsReportTimeBaidu.vue'),
  meta: { title: '财报发行', requiresAuth: true }
}
```

## 验证步骤

1. **启动后端服务**
```bash
cd F:\source_code\TradingAgents-CN
uvicorn app.main:app --host 0.0.0.0 --port 8848 --reload
```

2. **启动前端服务**
```bash
cd F:\source_code\TradingAgents-CN\frontend
npm run dev
```

3. **运行测试**
```bash
cd F:\source_code\TradingAgents-CN\tests\stocks
$env:API_BASE_URL="http://localhost:8848"; $env:API_AUTH_TOKEN="your_token"; pytest collections\124_news_report_time_baidu_collection.py -v
```

4. **手动验证**
- 访问 http://localhost:3000/stocks/collections/news_report_time_baidu
- 测试刷新数据功能
- 测试清空数据功能
- 查看数据概览
- 查看数据列表

## 完成后
确认所有测试通过后，在需求文档中注释掉URL：
```markdown
1. 数据集合：创建一个新的数据集合，名称为**财报发行** <!-- (http://localhost:3000/stocks/collections/news_report_time_baidu) -->
```
