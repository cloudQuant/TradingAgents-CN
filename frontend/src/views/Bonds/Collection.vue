<template>
  <div class="collection-view">
    <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1 class="page-title">
            <el-icon class="title-icon"><Box /></el-icon>
            {{ collectionInfo?.display_name || collectionName }}
          </h1>
          <p class="page-description">{{ collectionInfo?.description || '' }}</p>
        </div>
        <div class="header-actions">
          <el-button :icon="Refresh" @click="loadData" :loading="loading">刷新</el-button>
        </div>
      </div>
    </div>

    <div class="content">
      <!-- 统计数据卡片 -->
      <el-card shadow="hover" class="stats-card" v-if="stats">
        <template #header>
          <div class="card-header">数据统计</div>
        </template>
        <el-row :gutter="16">
          <el-col :xs="12" :sm="8" :md="6" :lg="4">
            <el-statistic title="总记录数" :value="stats.total_count">
              <template #prefix>
                <el-icon><Document /></el-icon>
              </template>
            </el-statistic>
          </el-col>
          <el-col :xs="12" :sm="8" :md="6" :lg="4" v-if="stats.earliest_date">
            <el-statistic title="最早日期" :value="stats.earliest_date">
              <template #prefix>
                <el-icon><Calendar /></el-icon>
              </template>
            </el-statistic>
          </el-col>
          <el-col :xs="12" :sm="8" :md="6" :lg="4" v-if="stats.latest_date">
            <el-statistic title="最新日期" :value="stats.latest_date">
              <template #prefix>
                <el-icon><Calendar /></el-icon>
              </template>
            </el-statistic>
          </el-col>
          <el-col :xs="24" :sm="24" :md="12" :lg="12" v-if="stats.category_stats && stats.category_stats.length > 0">
            <div class="category-stats">
              <span class="stats-label">类别分布：</span>
              <el-tag
                v-for="cat in stats.category_stats"
                :key="cat.category"
                size="small"
                style="margin-right: 8px; margin-bottom: 4px;"
              >
                {{ cat.category }}: {{ cat.count }}
              </el-tag>
            </div>
          </el-col>
          <el-col :xs="24" :sm="24" :md="12" :lg="12" v-if="stats.exchange_stats && stats.exchange_stats.length > 0">
            <div class="exchange-stats">
              <span class="stats-label">交易所分布：</span>
              <el-tag
                v-for="ex in stats.exchange_stats"
                :key="ex.exchange"
                size="small"
                style="margin-right: 8px; margin-bottom: 4px;"
              >
                {{ ex.exchange }}: {{ ex.count }}
              </el-tag>
            </div>
          </el-col>
        </el-row>
      </el-card>

      <!-- 字段说明 -->
      <el-card shadow="hover" class="fields-card" v-if="fields && fields.length > 0">
        <template #header>
          <div class="card-header">字段说明</div>
        </template>
        <el-table :data="fields" stripe border size="small" style="width: 100%">
          <el-table-column prop="name" label="字段名" width="200" />
          <el-table-column prop="type" label="类型" width="120" />
          <el-table-column prop="example" label="示例" show-overflow-tooltip>
            <template #default="{ row }">
              <span v-if="row.example" class="example-text">{{ row.example }}</span>
              <span v-else class="text-muted">-</span>
            </template>
          </el-table-column>
        </el-table>
      </el-card>

      <!-- 数据列表 -->
      <el-card shadow="hover" class="data-card">
        <template #header>
          <div class="card-header">
            <span>数据列表</span>
            <div class="header-actions">
              <el-input
                v-model="filterValue"
                placeholder="搜索..."
                style="width: 200px; margin-right: 8px;"
                clearable
                @clear="handleFilter"
                @keyup.enter="handleFilter"
              >
                <template #prefix>
                  <el-icon><Search /></el-icon>
                </template>
              </el-input>
              <el-select
                v-model="filterField"
                placeholder="搜索字段"
                style="width: 150px; margin-right: 8px;"
                clearable
              >
                <el-option
                  v-for="field in fields"
                  :key="field.name"
                  :label="field.name"
                  :value="field.name"
                />
              </el-select>
              <el-button size="small" :icon="Search" @click="handleFilter">搜索</el-button>
            </div>
          </div>
        </template>
        
        <el-table
          :data="items"
          v-loading="loading"
          stripe
          border
          style="width: 100%"
          max-height="600"
        >
          <el-table-column
            v-for="field in fields"
            :key="field.name"
            :prop="field.name"
            :label="field.name"
            :min-width="120"
            show-overflow-tooltip
          >
            <template #default="{ row }">
              <span v-if="row[field.name] !== null && row[field.name] !== undefined">
                {{ formatValue(row[field.name]) }}
              </span>
              <span v-else class="text-muted">-</span>
            </template>
          </el-table-column>
        </el-table>

        <!-- 分页 -->
        <div class="pagination-wrapper">
          <el-pagination
            v-model:current-page="page"
            v-model:page-size="pageSize"
            :page-sizes="[20, 50, 100, 200]"
            :total="total"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleSizeChange"
            @current-change="handlePageChange"
          />
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Box, Refresh, Search, Document, Calendar } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { bondsApi } from '@/api/bonds'

const route = useRoute()
const router = useRouter()

const collectionName = computed(() => route.params.collectionName as string)

// 数据状态
const loading = ref(false)
const items = ref<any[]>([])
const fields = ref<Array<{ name: string; type: string; example: string | null }>>([])
const page = ref(1)
const pageSize = ref(50)
const total = ref(0)

// 过滤条件
const filterField = ref('')
const filterValue = ref('')

// 统计数据
const stats = ref<any>(null)
const collectionInfo = ref<any>(null)

// 加载数据
const loadData = async () => {
  loading.value = true
  try {
    // 加载集合信息
    const collectionsRes = await bondsApi.getCollections()
    if (collectionsRes.success && collectionsRes.data) {
      collectionInfo.value = collectionsRes.data.find((c: any) => c.name === collectionName.value)
    }

    // 加载统计数据
    const statsRes = await bondsApi.getCollectionStats(collectionName.value)
    if (statsRes.success && statsRes.data) {
      stats.value = statsRes.data
    }

    // 加载数据
    const dataRes = await bondsApi.getCollectionData(collectionName.value, {
      page: page.value,
      page_size: pageSize.value,
      sort_dir: 'desc',
      filter_field: filterField.value || undefined,
      filter_value: filterValue.value || undefined,
    })
    
    if (dataRes.success && dataRes.data) {
      items.value = dataRes.data.items || []
      fields.value = dataRes.data.fields || []
      total.value = dataRes.data.total || 0
    } else {
      ElMessage.error('加载数据失败')
    }
  } catch (e: any) {
    console.error('加载数据失败:', e)
    ElMessage.error('加载数据失败: ' + (e.message || '未知错误'))
  } finally {
    loading.value = false
  }
}

// 格式化值
const formatValue = (value: any): string => {
  if (value === null || value === undefined) {
    return '-'
  }
  if (typeof value === 'object') {
    return JSON.stringify(value)
  }
  return String(value)
}

// 分页处理
const handleSizeChange = (size: number) => {
  pageSize.value = size
  page.value = 1
  loadData()
}

const handlePageChange = (p: number) => {
  page.value = p
  loadData()
}

// 过滤处理
const handleFilter = () => {
  page.value = 1
  loadData()
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.collection-view {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
  font-size: 24px;
  font-weight: 600;
}

.title-icon {
  font-size: 28px;
  color: #409eff;
}

.page-description {
  margin: 8px 0 0 0;
  color: #909399;
  font-size: 14px;
}

.content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
}

.stats-card,
.fields-card,
.data-card {
  margin-bottom: 16px;
}

.stats-label {
  font-size: 14px;
  color: #606266;
  margin-right: 8px;
}

.category-stats,
.exchange-stats {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 4px;
}

.example-text {
  font-family: monospace;
  font-size: 12px;
  color: #606266;
}

.text-muted {
  color: #c0c4cc;
}

.pagination-wrapper {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 16px;
  }

  .header-actions {
    width: 100%;
    flex-wrap: wrap;
  }
}
</style>


