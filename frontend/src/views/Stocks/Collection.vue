<template>
  <div class="collection-page">
    <!-- 顶部信息区域 -->
    <div class="page-header">
      <div class="header-content" v-if="collectionDef">
        <div class="title-section">
          <h1 class="page-title">
            <el-icon class="title-icon"><Box /></el-icon>
            {{ collectionDef.display_name }}
            <span class="collection-name-en">({{ collectionName }})</span>
          </h1>
          <p class="page-description">{{ collectionDef.description }}</p>
        </div>
        <div class="header-actions">
          <el-button @click="goBack" icon="ArrowLeft" round>返回数据集合列表</el-button>
        </div>
      </div>
      <div class="header-content" v-else>
        <div class="title-section">
          <h1 class="page-title">
            <el-icon class="title-icon"><Box /></el-icon>
            未找到数据集合
          </h1>
          <p class="page-description">集合名称：{{ collectionName }}</p>
        </div>
        <div class="header-actions">
          <el-button @click="goBack" icon="ArrowLeft" round>返回数据集合列表</el-button>
        </div>
      </div>
    </div>

    <div class="content">
      <el-empty
        v-if="!collectionDef"
        description="未找到对应的数据集合定义"
      />

      <template v-else>
        <!-- 操作按钮栏 -->
        <div class="action-bar">
          <el-button type="info" @click="showOverview">
            <el-icon><Document /></el-icon>
            数据概览
          </el-button>
          <el-button @click="refreshData">
            <el-icon><Refresh /></el-icon>
            刷新
          </el-button>
          <el-button type="primary" @click="showUpdateDialog">
            <el-icon><Upload /></el-icon>
            更新数据
          </el-button>
          <el-button type="danger" @click="handleClearData">
            <el-icon><Delete /></el-icon>
            清空数据
          </el-button>
        </div>

        <!-- 数据统计卡片 -->
        <el-card shadow="hover" class="stats-card">
          <template #header>
            <div class="card-header">
              <span>数据统计</span>
              <div class="card-actions">
                <el-button 
                  type="primary" 
                  size="small" 
                  :loading="refreshing"
                  @click="handleRefreshData"
                >
                  <el-icon><Refresh /></el-icon>
                  更新数据
                </el-button>
                <el-button 
                  type="danger" 
                  size="small" 
                  @click="handleClearData"
                >
                  <el-icon><Delete /></el-icon>
                  清空数据
                </el-button>
              </div>
            </div>
          </template>
          
          <el-row :gutter="20" v-loading="statsLoading">
            <el-col :span="8">
              <el-statistic title="数据总数" :value="stats.total_count || 0">
                <template #suffix>条</template>
              </el-statistic>
            </el-col>
            <el-col :span="8">
              <el-statistic title="最后更新">
                <template #default>
                  <span v-if="stats.latest_update">{{ formatTime(stats.latest_update) }}</span>
                  <span v-else class="text-muted">暂无数据</span>
                </template>
              </el-statistic>
            </el-col>
            <el-col :span="8">
              <el-statistic title="刷新状态">
                <template #default>
                  <el-tag v-if="refreshStatus" :type="getStatusType(refreshStatus.status)">
                    {{ getStatusText(refreshStatus.status) }}
                  </el-tag>
                  <span v-else class="text-muted">无任务</span>
                </template>
              </el-statistic>
            </el-col>
          </el-row>
          
          <!-- 刷新进度条 -->
          <div v-if="refreshing && refreshStatus" class="refresh-progress">
            <el-progress 
              :percentage="getProgressPercentage(refreshStatus)" 
              :status="refreshStatus.status === 'failed' ? 'exception' : undefined"
            >
              <template #default="{ percentage }">
                <span class="progress-text">{{ refreshStatus.message }} - {{ percentage }}%</span>
              </template>
            </el-progress>
          </div>
        </el-card>

        <!-- 字段说明 -->
        <el-card shadow="hover" class="fields-card">
          <template #header>
            <div class="card-header">
              <span>字段说明</span>
            </div>
          </template>

          <el-table :data="fieldRows" size="small" style="width: 100%">
            <el-table-column prop="name" label="字段名" width="180" />
            <el-table-column prop="description" label="说明" />
            <el-table-column prop="example" label="示例值" width="200">
              <template #default="{ row }">
                <span v-if="row.example !== null && row.example !== undefined">{{ row.example }}</span>
                <span v-else class="example-placeholder">-</span>
              </template>
            </el-table-column>
          </el-table>
        </el-card>

        <!-- 数据表格 -->
        <el-card shadow="hover" class="data-card">
          <template #header>
            <div class="card-header">
              <span>数据预览</span>
              <div class="card-actions">
                <el-button size="small" @click="refreshData">刷新</el-button>
              </div>
            </div>
          </template>

          <el-table
            :data="rows"
            size="small"
            stripe
            v-loading="loading"
            style="width: 100%"
          >
            <el-table-column
              v-for="field in collectionDef.fields"
              :key="field"
              :prop="field"
              :label="field"
              :min-width="120"
            />
          </el-table>

          <div class="pagination-wrapper">
            <el-pagination
              background
              layout="prev, pager, next, jumper"
              :total="total"
              :page-size="pageSize"
              :current-page="currentPage"
              @current-change="handlePageChange"
            />
          </div>
        </el-card>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Box, Refresh, Delete } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { stocksApi, type CollectionStatsResponse, type RefreshStatusResponse } from '@/api/stocks'

const route = useRoute()
const router = useRouter()

const collectionName = computed(() => (route.params.collectionName as string) || '')

interface CollectionDefinition {
  display_name: string
  description: string
  fields: string[]
}

interface FieldRow {
  name: string
  description: string
  example: any
}

// 集合定义：与后端 /api/stocks/collections 中的字段保持一致
const collectionDefinitions: Record<string, CollectionDefinition> = {
  stock_basic_info: {
    display_name: '股票基础信息',
    description: '股票的基础信息，包括代码、名称、行业、市场、总市值、流通市值等',
    fields: ['code', 'name', 'industry', 'market', 'list_date', 'total_mv', 'circ_mv', 'pe', 'pb'],
  },
  market_quotes: {
    display_name: '实时行情数据',
    description: '股票的实时行情数据，包括最新价、涨跌幅、成交量、成交额等',
    fields: ['code', 'trade_date', 'open', 'high', 'low', 'close', 'volume', 'amount', 'pct_chg', 'turnover_rate'],
  },
  stock_financial_data: {
    display_name: '财务数据',
    description: '股票的财务数据，包括营业收入、净利润、ROE、负债率等财务指标',
    fields: ['code', 'report_period', 'revenue', 'net_profit', 'roe', 'debt_to_assets', 'eps'],
  },
  stock_daily: {
    display_name: '日线行情',
    description: '股票的日线历史行情数据，包括开盘价、最高价、最低价、收盘价、成交量等',
    fields: ['code', 'trade_date', 'open', 'high', 'low', 'close', 'volume', 'amount'],
  },
  stock_weekly: {
    display_name: '周线行情',
    description: '股票的周线历史行情数据',
    fields: ['code', 'trade_date', 'open', 'high', 'low', 'close', 'volume', 'amount'],
  },
  stock_monthly: {
    display_name: '月线行情',
    description: '股票的月线历史行情数据',
    fields: ['code', 'trade_date', 'open', 'high', 'low', 'close', 'volume', 'amount'],
  },
}

const collectionDef = computed<CollectionDefinition | null>(() => {
  const name = collectionName.value
  return collectionDefinitions[name] || null
})

const fieldRows = computed<FieldRow[]>(() => {
  if (!collectionDef.value) return []
  return collectionDef.value.fields.map((name) => ({
    name,
    description: '',
    example: null,
  }))
})

const rows = ref<any[]>([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

// 统计信息
const stats = ref<CollectionStatsResponse>({
  total_count: 0,
  collection_name: collectionName.value
})
const statsLoading = ref(false)

// 刷新相关
const refreshing = ref(false)
const refreshStatus = ref<RefreshStatusResponse | null>(null)
const currentTaskId = ref<string | null>(null)
let statusCheckInterval: number | null = null

const loadCollectionPage = async () => {
  const name = collectionName.value
  if (!name) return

  try {
    const res = await stocksApi.getStockCollectionData(name, {
      page: currentPage.value,
      page_size: pageSize.value,
    })
    const data = res.data
    rows.value = data.items || []
    total.value = data.total ?? 0
    currentPage.value = data.page ?? currentPage.value
    pageSize.value = data.page_size ?? pageSize.value
  } catch (error) {
    console.error('加载集合数据失败', error)
    ElMessage.error('加载集合数据失败')
  }
}

const refreshData = async () => {
  loading.value = true
  try {
    // 当前版本使用本地Mock数据，后续可替换为真实API调用
    await loadCollectionPage()
  } finally {
    loading.value = false
  }
}

const handlePageChange = (page: number) => {
  currentPage.value = page
  refreshData()
}

const goBack = () => {
  router.push('/stocks/collections')
}

// 加载统计信息
const loadStats = async () => {
  const name = collectionName.value
  if (!name) return
  
  statsLoading.value = true
  try {
    const res = await stocksApi.getCollectionStats(name)
    stats.value = res.data
  } catch (error) {
    console.error('加载统计信息失败', error)
  } finally {
    statsLoading.value = false
  }
}

// 刷新数据
const handleRefreshData = async () => {
  const name = collectionName.value
  if (!name) return
  
  try {
    refreshing.value = true
    const res = await stocksApi.refreshCollection(name, {})
    currentTaskId.value = res.data.task_id
    ElMessage.success('刷新任务已启动')
    
    // 开始轮询任务状态
    startStatusPolling()
  } catch (error: any) {
    console.error('启动刷新任务失败', error)
    ElMessage.error(error.response?.data?.detail || '启动刷新任务失败')
    refreshing.value = false
  }
}

// 清空数据
const handleClearData = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要清空此集合的所有数据吗？此操作不可恢复！',
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    const name = collectionName.value
    if (!name) return
    
    const res = await stocksApi.clearCollection(name)
    ElMessage.success(`已清空 ${res.data.deleted_count} 条数据`)
    
    // 重新加载统计和数据
    await Promise.all([loadStats(), refreshData()])
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('清空数据失败', error)
      ElMessage.error(error.response?.data?.detail || '清空数据失败')
    }
  }
}

// 开始轮询任务状态
const startStatusPolling = () => {
  // 清除之前的轮询
  if (statusCheckInterval) {
    clearInterval(statusCheckInterval)
  }
  
  // 每2秒检查一次状态
  statusCheckInterval = window.setInterval(async () => {
    await checkRefreshStatus()
  }, 2000)
}

// 检查刷新任务状态
const checkRefreshStatus = async () => {
  const name = collectionName.value
  const taskId = currentTaskId.value
  if (!name || !taskId) return
  
  try {
    const res = await stocksApi.getRefreshStatus(name, taskId)
    refreshStatus.value = res.data
    
    // 如果任务完成或失败，停止轮询
    if (res.data.status === 'completed' || res.data.status === 'failed') {
      stopStatusPolling()
      refreshing.value = false
      
      if (res.data.status === 'completed') {
        ElMessage.success('数据刷新完成')
        // 重新加载统计和数据
        await Promise.all([loadStats(), refreshData()])
      } else {
        ElMessage.error(`数据刷新失败: ${res.data.error || '未知错误'}`)
      }
    }
  } catch (error) {
    console.error('查询刷新状态失败', error)
  }
}

// 停止轮询
const stopStatusPolling = () => {
  if (statusCheckInterval) {
    clearInterval(statusCheckInterval)
    statusCheckInterval = null
  }
}

// 格式化时间
const formatTime = (timeStr: string) => {
  try {
    const date = new Date(timeStr)
    return date.toLocaleString('zh-CN')
  } catch {
    return timeStr
  }
}

// 获取状态类型
const getStatusType = (status: string) => {
  const typeMap: Record<string, any> = {
    pending: 'info',
    running: 'warning',
    completed: 'success',
    failed: 'danger'
  }
  return typeMap[status] || 'info'
}

// 获取状态文本
const getStatusText = (status: string) => {
  const textMap: Record<string, string> = {
    pending: '等待中',
    running: '进行中',
    completed: '已完成',
    failed: '失败'
  }
  return textMap[status] || status
}

// 获取进度百分比
const getProgressPercentage = (status: RefreshStatusResponse) => {
  if (!status.total || status.total === 0) return 0
  return Math.round((status.progress / status.total) * 100)
}

onMounted(() => {
  if (!collectionDef.value) {
    ElMessage.warning('未找到对应的数据集合定义')
    return
  }
  // 加载统计信息和数据
  Promise.all([loadStats(), refreshData()])
})

onUnmounted(() => {
  // 组件卸载时停止轮询
  stopStatusPolling()
})
</script>

<style scoped lang="scss">
.collection-page {
  padding: 20px;
  background: #f5f7fa;
  min-height: calc(100vh - 60px);
}

.page-header {
  margin-bottom: 24px;

  .header-content {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding: 24px;
    background: linear-gradient(135deg, #409eff 0%, #3a8ee6 100%);
    border-radius: 12px;
    color: white;
    box-shadow: 0 4px 20px rgba(64, 158, 255, 0.4);
  }

  .title-section {
    flex: 1;
  }

  .page-title {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 26px;
    font-weight: 600;
    margin: 0 0 8px 0;

    .title-icon {
      font-size: 32px;
    }

    .collection-name-en {
      font-size: 16px;
      opacity: 0.9;
    }
  }

  .page-description {
    font-size: 14px;
    opacity: 0.9;
    margin: 0;
  }

  .header-actions {
    display: flex;
    align-items: center;
  }
}

.content {
  margin-top: 8px;
}

.fields-card {
  margin-bottom: 16px;
}

.data-card {
  margin-bottom: 16px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
}

.pagination-wrapper {
  margin-top: 12px;
  display: flex;
  justify-content: flex-end;
}

.example-placeholder {
  color: #c0c4cc;
}

.stats-card {
  margin-bottom: 16px;
  
  .card-actions {
    display: flex;
    gap: 8px;
  }
}

.refresh-progress {
  margin-top: 16px;
  
  .progress-text {
    font-size: 13px;
    color: #606266;
  }
}

.text-muted {
  color: #909399;
  font-size: 14px;
}

@media (max-width: 768px) {
  .page-header {
    .header-content {
      flex-direction: column;
      gap: 16px;
    }

    .header-actions {
      width: 100%;
      justify-content: flex-end;
    }
  }
}
</style>
