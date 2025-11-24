"""
批量生成所有缺失集合的后端和前端代码
"""
import re
import os
from pathlib import Path
from datetime import datetime

# 读取日志文件提取缺失集合
log_file = "test_coverage_report_20251123_221322.log"
with open(log_file, 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'\d+\. \[x\] (\w+)\s+文档: (.+\.md)'
missing_collections = re.findall(pattern, content)

print(f"找到 {len(missing_collections)} 个缺失的集合")

# 项目根目录
project_root = Path(__file__).parent.parent.parent

# 为每个集合生成代码
for idx, (collection_name, doc_file) in enumerate(missing_collections, 1):
    print(f"\n[{idx}/{len(missing_collections)}] 生成 {collection_name}...")
    
    # 从文档名称提取显示名称
    display_name = doc_file.split('_', 1)[1].replace('.md', '').replace('-完成', '')
    
    # 生成 Provider 代码
    provider_code = f'''"""
{display_name}数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class {collection_name.title().replace('_', '')}Provider:
    """{display_name}数据提供者"""
    
    def __init__(self):
        self.collection_name = "{collection_name}"
        self.display_name = "{display_name}"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取{display_name}数据
        
        Returns:
            DataFrame: {display_name}数据
        """
        try:
            logger.info(f"Fetching {{self.collection_name}} data")
            df = ak.{collection_name}(**kwargs)
            
            if df.empty:
                logger.warning(f"No data returned")
                return pd.DataFrame()
            
            # 添加元数据
            df['scraped_at'] = datetime.now()
            
            logger.info(f"Successfully fetched {{len(df)}} records")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching {{self.collection_name}} data: {{e}}")
            raise
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        """获取字段信息"""
        # 这里需要根据实际API返回的字段来定义
        return [
            {{"name": "scraped_at", "type": "datetime", "description": "抓取时间"}},
        ]
'''
    
    # 生成 Service 代码
    service_code = f'''"""
{display_name}服务
"""
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import UpdateOne

from .providers.{collection_name}_provider import {collection_name.title().replace('_', '')}Provider

logger = logging.getLogger(__name__)


class {collection_name.title().replace('_', '')}Service:
    """{display_name}服务"""
    
    def __init__(self, db: AsyncIOMotorClient):
        self.db = db
        self.collection = db.stocks.{collection_name}
        self.provider = {collection_name.title().replace('_', '')}Provider()
        
    async def get_overview(self) -> Dict[str, Any]:
        """获取数据概览"""
        total_count = await self.collection.count_documents({{}})
        
        latest = await self.collection.find_one(sort=[("scraped_at", -1)])
        oldest = await self.collection.find_one(sort=[("scraped_at", 1)])
        
        return {{
            "total_count": total_count,
            "last_updated": latest.get("scraped_at") if latest else None,
            "oldest_date": oldest.get("scraped_at") if oldest else None,
        }}
    
    async def get_data(
        self,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """获取数据列表"""
        query = filters or {{}}
        
        cursor = self.collection.find(query).skip(skip).limit(limit).sort("scraped_at", -1)
        data = await cursor.to_list(length=limit)
        
        total = await self.collection.count_documents(query)
        
        # 转换 ObjectId 为字符串
        for item in data:
            item["_id"] = str(item["_id"])
            if "scraped_at" in item and isinstance(item["scraped_at"], datetime):
                item["scraped_at"] = item["scraped_at"].isoformat()
        
        return {{
            "data": data,
            "total": total,
            "skip": skip,
            "limit": limit,
        }}
    
    async def refresh_data(self, **kwargs) -> Dict[str, Any]:
        """刷新数据"""
        try:
            df = self.provider.fetch_data(**kwargs)
            
            if df.empty:
                return {{
                    "success": True,
                    "message": "No data available",
                    "inserted": 0,
                }}
            
            records = df.to_dict('records')
            
            # 批量插入
            if records:
                result = await self.collection.insert_many(records)
                return {{
                    "success": True,
                    "message": "Data refreshed successfully",
                    "inserted": len(result.inserted_ids),
                }}
            
            return {{
                "success": True,
                "message": "No operations performed",
                "inserted": 0,
            }}
            
        except Exception as e:
            logger.error(f"Error refreshing data: {{e}}")
            return {{
                "success": False,
                "message": str(e),
                "inserted": 0,
            }}
    
    async def clear_data(self) -> Dict[str, Any]:
        """清空数据"""
        result = await self.collection.delete_many({{}})
        return {{
            "success": True,
            "message": f"Deleted {{result.deleted_count}} records",
            "deleted": result.deleted_count,
        }}
'''
    
    # 生成 API 路由代码片段
    api_routes = f'''
# {display_name} - {collection_name}
@router.get("/collections/{collection_name}")
async def get_{collection_name}(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取{display_name}数据"""
    from app.services.stock.{collection_name}_service import {collection_name.title().replace('_', '')}Service
    service = {collection_name.title().replace('_', '')}Service(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/{collection_name}/overview")
async def get_{collection_name}_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取{display_name}数据概览"""
    from app.services.stock.{collection_name}_service import {collection_name.title().replace('_', '')}Service
    service = {collection_name.title().replace('_', '')}Service(db)
    return await service.get_overview()


@router.post("/collections/{collection_name}/refresh")
async def refresh_{collection_name}(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新{display_name}数据"""
    from app.services.stock.{collection_name}_service import {collection_name.title().replace('_', '')}Service
    service = {collection_name.title().replace('_', '')}Service(db)
    return await service.refresh_data()


@router.delete("/collections/{collection_name}/clear")
async def clear_{collection_name}(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空{display_name}数据"""
    from app.services.stock.{collection_name}_service import {collection_name.title().replace('_', '')}Service
    service = {collection_name.title().replace('_', '')}Service(db)
    return await service.clear_data()
'''
    
    # 生成前端页面代码（简化版）
    vue_component = f'''<template>
  <div class="{collection_name}-container">
    <el-card class="header-card">
      <h2>{display_name}</h2>
    </el-card>

    <el-card class="overview-card">
      <h3>数据概览</h3>
      <el-row :gutter="20">
        <el-col :span="8">
          <div class="stat-item">
            <div class="stat-value">{{{{ overview.total_count || 0 }}}}</div>
            <div class="stat-label">总记录数</div>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="stat-item">
            <div class="stat-value">{{{{ formatDate(overview.last_updated) }}}}</div>
            <div class="stat-label">最后更新</div>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <el-card class="actions-card">
      <el-button type="primary" @click="refreshData" :loading="loading">
        <el-icon><Refresh /></el-icon>
        刷新数据
      </el-button>
      <el-button type="danger" @click="clearData" :loading="loading">
        <el-icon><Delete /></el-icon>
        清空数据
      </el-button>
    </el-card>

    <el-card class="table-card">
      <el-table :data="tableData" v-loading="loading" stripe>
        <el-table-column 
          v-for="col in columns" 
          :key="col.prop"
          :prop="col.prop" 
          :label="col.label"
          :width="col.width"
        />
      </el-table>

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
import {{ ref, onMounted, computed }} from 'vue'
import {{ ElMessage, ElMessageBox }} from 'element-plus'
import {{ Refresh, Delete }} from '@element-plus/icons-vue'
import axios from 'axios'

const API_BASE = '/api/stocks/collections/{collection_name}'

const loading = ref(false)
const overview = ref({{}})
const tableData = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)

const columns = computed(() => {{
  if (tableData.value.length === 0) return []
  const firstRow = tableData.value[0]
  return Object.keys(firstRow)
    .filter(key => key !== '_id')
    .map(key => ({{
      prop: key,
      label: key,
      width: 150
    }}))
}})

const loadOverview = async () => {{
  try {{
    const response = await axios.get(`${{API_BASE}}/overview`)
    overview.value = response.data
  }} catch (error) {{
    console.error('Failed to load overview:', error)
  }}
}}

const loadData = async () => {{
  loading.value = true
  try {{
    const skip = (currentPage.value - 1) * pageSize.value
    const response = await axios.get(API_BASE, {{
      params: {{ skip, limit: pageSize.value }}
    }})
    tableData.value = response.data.data
    total.value = response.data.total
  }} catch (error) {{
    ElMessage.error('加载数据失败')
  }} finally {{
    loading.value = false
  }}
}}

const refreshData = async () => {{
  loading.value = true
  try {{
    const response = await axios.post(`${{API_BASE}}/refresh`)
    if (response.data.success) {{
      ElMessage.success(`数据刷新成功！插入: ${{response.data.inserted}}`)
      await loadOverview()
      await loadData()
    }}
  }} catch (error) {{
    ElMessage.error('数据刷新失败')
  }} finally {{
    loading.value = false
  }}
}}

const clearData = async () => {{
  try {{
    await ElMessageBox.confirm('确定要清空所有数据吗？', '警告', {{
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }})
    
    loading.value = true
    const response = await axios.delete(`${{API_BASE}}/clear`)
    
    if (response.data.success) {{
      ElMessage.success(`已删除 ${{response.data.deleted}} 条记录`)
      await loadOverview()
      await loadData()
    }}
  }} catch (error) {{
    if (error !== 'cancel') {{
      ElMessage.error('清空数据失败')
    }}
  }} finally {{
    loading.value = false
  }}
}}

const handleSizeChange = (val) => {{
  pageSize.value = val
  loadData()
}}

const handleCurrentChange = (val) => {{
  currentPage.value = val
  loadData()
}}

const formatDate = (dateStr) => {{
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleString('zh-CN')
}}

onMounted(() => {{
  loadOverview()
  loadData()
}})
</script>

<style scoped>
.{collection_name}-container {{
  padding: 20px;
}}

.header-card, .overview-card, .actions-card, .table-card {{
  margin-bottom: 20px;
}}

.stat-item {{
  text-align: center;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
}}

.stat-value {{
  font-size: 24px;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 8px;
}}

.stat-label {{
  font-size: 14px;
  color: #909399;
}}

.el-pagination {{
  margin-top: 20px;
  justify-content: center;
}}
</style>
'''
    
    # 生成路由配置
    route_config = f'''{{
  path: '/stocks/collections/{collection_name}',
  name: '{collection_name.title().replace('_', '')}',
  component: () => import('@/views/Stocks/Collections/{collection_name.title().replace('_', '')}.vue'),
  meta: {{ title: '{display_name}', requiresAuth: true }}
}},'''
    
    # 保存到输出目录
    output_dir = Path(__file__).parent / "generated_code" / collection_name
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 写入文件
    (output_dir / "provider.py").write_text(provider_code, encoding='utf-8')
    (output_dir / "service.py").write_text(service_code, encoding='utf-8')
    (output_dir / "api_routes.py").write_text(api_routes, encoding='utf-8')
    (output_dir / "component.vue").write_text(vue_component, encoding='utf-8')
    (output_dir / "route_config.ts").write_text(route_config, encoding='utf-8')
    
    # 生成集合注册代码
    collection_registration = f'''{{
    "name": "{collection_name}",
    "display_name": "{display_name}",
    "description": "{display_name}数据",
    "route": "/stocks/collections/{collection_name}",
    "fields": [],
}},'''
    (output_dir / "collection_registration.py").write_text(collection_registration, encoding='utf-8')

print(f"\n完成！所有代码已生成到 generated_code/ 目录")
print(f"总共生成了 {len(missing_collections)} 个集合的代码")
