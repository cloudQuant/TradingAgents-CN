<template>
  <div class="collection-page">
    <!-- 顶部信息区域 -->
    <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1 class="page-title">
            <el-icon class="title-icon"><Box /></el-icon>
            {{ collectionDef?.display_name || collectionName }}
          </h1>
          <p class="page-description">{{ collectionDef?.description || '' }}</p>
        </div>
        <div class="header-actions">
          <el-button :icon="Box" @click="showOverview">数据概览</el-button>
          <el-button :icon="Refresh" @click="refreshData" :loading="loading">刷新</el-button>
          <el-button :icon="Download" type="primary" @click="handleRefreshData" :loading="refreshing">更新数据</el-button>
          <el-button :icon="Delete" type="danger" @click="handleClearData">清空数据</el-button>
        </div>
      </div>
    </div>

    <div class="content">
      <el-empty
        v-if="!collectionDef"
        description="未找到对应的数据集合定义"
      />

      <template v-else>
        <!-- 数据表格 -->
        <el-card shadow="hover" class="data-card">
          <template #header>
            <div class="card-header">
              <div style="display: flex; align-items: center;">
                <span>数据预览</span>
                <el-popover
                  placement="right"
                  title="字段说明"
                  :width="600"
                  trigger="hover"
                  v-if="fieldRows && fieldRows.length > 0"
                >
                  <template #reference>
                    <el-icon style="margin-left: 8px; cursor: pointer; color: #909399;"><QuestionFilled /></el-icon>
                  </template>
                  <el-table :data="fieldRows" stripe border size="small" style="width: 100%">
                    <el-table-column prop="name" label="字段名" width="180" />
                    <el-table-column prop="description" label="说明" />
                    <el-table-column prop="example" label="示例值" width="200">
                      <template #default="{ row }">
                        <span v-if="row.example !== null && row.example !== undefined">{{ row.example }}</span>
                        <span v-else class="example-placeholder">-</span>
                      </template>
                    </el-table-column>
                  </el-table>
                </el-popover>
              </div>
              <div class="card-actions">
                <el-input
                  v-model="filterValue"
                  placeholder="搜索..."
                  size="small"
                  style="width: 200px; margin-right: 8px;"
                  clearable
                >
                  <template #prefix>
                    <el-icon><Search /></el-icon>
                  </template>
                </el-input>
                <el-select
                  v-model="filterField"
                  placeholder="搜索字段"
                  size="small"
                  style="width: 150px; margin-right: 8px;"
                  clearable
                >
                  <el-option
                    v-for="field in displayFields"
                    :key="field"
                    :label="field"
                    :value="field"
                  />
                </el-select>
                <el-button size="small" @click="refreshData">刷新</el-button>
              </div>
            </div>
          </template>

          <el-table
            :data="filteredRows"
            size="small"
            stripe
            v-loading="loading"
            style="width: 100%"
          >
            <el-table-column
              v-for="field in displayFields"
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

    <!-- 数据概览对话框 -->
    <el-dialog
      v-model="overviewDialogVisible"
      title="数据概览"
      width="600px"
      :close-on-click-modal="false"
    >
      <div style="padding: 10px;">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="集合名称" label-align="right">
            {{ currentCollectionInfo.name }}
          </el-descriptions-item>
          <el-descriptions-item label="显示名称" label-align="right">
            {{ currentCollectionInfo.displayName }}
          </el-descriptions-item>
          <el-descriptions-item label="数据总数" label-align="right">
            {{ formatNumber(stats.total_count || 0) }} 条
          </el-descriptions-item>
          <el-descriptions-item label="字段数量" label-align="right">
            {{ currentCollectionInfo.fieldCount }} 个
          </el-descriptions-item>
          <el-descriptions-item label="最后更新" label-align="right" :span="2">
            {{ stats.latest_update ? formatTime(stats.latest_update) : '暂无数据' }}
          </el-descriptions-item>
          <el-descriptions-item label="数据来源" label-align="right" :span="2">
            <el-link :href="currentCollectionInfo.dataSource" target="_blank" type="primary" v-if="currentCollectionInfo.dataSource !== '暂无'">
              {{ currentCollectionInfo.dataSource }}
            </el-link>
            <span v-else>{{ currentCollectionInfo.dataSource }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="描述" label-align="right" :span="2">
            {{ collectionDef?.description || `数据集合：${collectionName}` }}
          </el-descriptions-item>
        </el-descriptions>
      </div>
      <template #footer>
        <el-button @click="overviewDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { Box, Refresh, Delete, Download, Search, QuestionFilled } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { stocksApi, type CollectionStatsResponse, type RefreshStatusResponse } from '@/api/stocks'

const route = useRoute()

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
  // 如果有预定义的集合定义则使用，否则创建默认定义
  if (collectionDefinitions[name]) {
    return collectionDefinitions[name]
  }
  
  // 为未定义的集合创建默认定义
  if (name) {
    return {
      display_name: name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
      description: `数据集合: ${name}`,
      fields: [] // 字段将从实际数据中获取
    }
  }
  
  return null
})

const fieldRows = computed<FieldRow[]>(() => {
  if (!collectionDef.value) return []

  // 优先使用预定义的字段
  if (collectionDef.value.fields && collectionDef.value.fields.length > 0) {
    return collectionDef.value.fields.map((name) => ({
      name,
      description: '',
      example: null,
    }))
  }

  // 如果没有预定义字段，从实际数据中获取
  if (rows.value.length > 0) {
    const firstRow = rows.value[0]
    return Object.keys(firstRow).map((name) => ({
      name,
      description: '',
      example: firstRow[name],
    }))
  }

  return []
})

// 用于表格显示的字段列表
const displayFields = computed<string[]>(() => {
  // 优先使用预定义的字段
  if (collectionDef.value?.fields && collectionDef.value.fields.length > 0) {
    return collectionDef.value.fields
  }
  
  // 从实际数据中获取字段
  if (rows.value.length > 0) {
    return Object.keys(rows.value[0])
  }
  
  return []
})

const rows = ref<any[]>([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

// 本地过滤条件
const filterField = ref('')
const filterValue = ref('')

// 过滤后的行数据（前端模糊搜索）
const filteredRows = computed(() => {
  if (!filterValue.value) {
    return rows.value
  }

  const keyword = filterValue.value.toLowerCase()

  return rows.value.filter((row) => {
    if (filterField.value) {
      const value = row[filterField.value]
      return (
        value !== null &&
        value !== undefined &&
        String(value).toLowerCase().includes(keyword)
      )
    }

    // 未选择字段时，在所有字段中模糊搜索
    return Object.values(row).some((value) => {
      return (
        value !== null &&
        value !== undefined &&
        String(value).toLowerCase().includes(keyword)
      )
    })
  })
})

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

// 对话框相关
const overviewDialogVisible = ref(false)

// 集合固定信息映射
const collectionStaticInfo: Record<string, any> = {
  stock_individual_info_em: {
    name: 'stock_individual_info_em',
    displayName: '个股信息查询-东财',
    fieldCount: 15,
    dataSource: 'http://quote.eastmoney.com/'
  },
  stock_individual_basic_info_xq: {
    name: 'stock_individual_basic_info_xq',
    displayName: '个股信息查询-雪球',
    fieldCount: 12,
    dataSource: 'https://xueqiu.com/'
  },
  stock_zh_a_spot_em: {
    name: 'stock_zh_a_spot_em',
    displayName: '沪深京A股实时行情-东财',
    fieldCount: 35,
    dataSource: 'http://quote.eastmoney.com/center/gridlist.html#hs_a_board'
  },
  stock_zh_a_hist: {
    name: 'stock_zh_a_hist',
    displayName: 'A股历史行情-东财',
    fieldCount: 13,
    dataSource: 'http://quote.eastmoney.com/'
  },
  stock_zh_a_hist_min_em: {
    name: 'stock_zh_a_hist_min_em',
    displayName: 'A股分时数据-东财',
    fieldCount: 5,
    dataSource: 'http://push2.eastmoney.com/'
  },
  stock_sh_a_spot_em: {
    name: 'stock_sh_a_spot_em',
    displayName: '沪A股实时行情-东财',
    fieldCount: 35,
    dataSource: 'http://quote.eastmoney.com/'
  },
  stock_sz_a_spot_em: {
    name: 'stock_sz_a_spot_em',
    displayName: '深A股实时行情-东财',
    fieldCount: 35,
    dataSource: 'http://quote.eastmoney.com/'
  },
  stock_cyb_spot_em: {
    name: 'stock_cyb_spot_em',
    displayName: '创业板实时行情-东财',
    fieldCount: 35,
    dataSource: 'http://quote.eastmoney.com/'
  },
  stock_kcb_spot_em: {
    name: 'stock_kcb_spot_em',
    displayName: '科创板实时行情-东财',
    fieldCount: 35,
    dataSource: 'http://quote.eastmoney.com/'
  },
  stock_bj_a_spot_em: {
    name: 'stock_bj_a_spot_em',
    displayName: '京A股实时行情-东财',
    fieldCount: 35,
    dataSource: 'http://quote.eastmoney.com/'
  }
}

// 获取当前集合的固定信息
const currentCollectionInfo = computed(() => {
  return collectionStaticInfo[collectionName.value] || {
    name: collectionName.value,
    displayName: collectionDef.value?.display_name || collectionName.value,
    fieldCount: displayFields.value.length,
    dataSource: '暂无'
  }
})

// 格式化数字
const formatNumber = (num: number): string => {
  return num.toLocaleString('zh-CN')
}

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


// 显示数据概览
const showOverview = () => {
  overviewDialogVisible.value = true
}

onMounted(() => {
  // 即使没有预定义的集合，也尝试加载数据
  if (collectionName.value) {
    // 加载统计信息和数据
    Promise.all([loadStats(), refreshData()])
  } else {
    ElMessage.warning('集合名称不能为空')
  }
})

onUnmounted(() => {
  // 组件卸载时停止轮询
  stopStatusPolling()
})
</script>

<style scoped lang="scss">
.collection-page {
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

.header-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.content {
  margin-top: 8px;
}

.action-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
  padding: 16px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
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
