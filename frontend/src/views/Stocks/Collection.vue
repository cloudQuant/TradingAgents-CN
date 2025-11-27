<template>
  <div class="collection-page">
    <!-- 页面头部 -->
    <CollectionPageHeader
      :collection-name="collectionName"
      :display-name="collectionDef?.display_name"
      :description="collectionDef?.description"
      :loading="loading"
      :updating="refreshing"
      :clearing="clearing"
      @show-overview="overviewDialogVisible = true"
      @refresh="refreshData"
      @update-command="handleUpdateCommand"
      @clear-data="handleClearData"
    />

    <div class="content">
      <el-empty
        v-if="!collectionDef"
        description="未找到对应的数据集合定义"
      />

      <template v-else>
        <!-- 数据表格 -->
        <CollectionDataTable
          :data="filteredRows"
          :fields="fieldRows"
          :total="total"
          :loading="loading"
          :collection-name="collectionName"
          :export-all-data="exportAllData"
          v-model:page="currentPage"
          v-model:page-size="pageSize"
          v-model:filter-value="filterValue"
          v-model:filter-field="filterField"
          @search="refreshData"
          @refresh="refreshData"
          @page-change="handlePageChange"
          @size-change="refreshData"
        />
      </template>
    </div>

    <!-- 数据概览对话框 -->
    <CollectionOverviewDialog
      v-model:visible="overviewDialogVisible"
      :collection-name="collectionName"
      :display-name="collectionDef?.display_name"
      :description="collectionDef?.description"
      :total-count="stats.total_count"
      :field-count="fieldRows.length"
      :latest-update="stats.latest_update"
      :data-source="currentCollectionInfo.dataSource"
    />

    <!-- API更新对话框（定制化） -->
    <el-dialog
      v-model="apiParamsDialogVisible"
      title="API更新"
      width="650px"
      :close-on-click-modal="false"
    >
      <el-form label-width="100px">
        <el-form-item label="集合名称">
          <el-input :value="refreshConfig?.displayName || collectionName" disabled />
        </el-form-item>

        <!-- 描述信息 -->
        <el-alert 
          v-if="refreshConfig?.description"
          :title="refreshConfig.description"
          type="info"
          :closable="false"
          style="margin-bottom: 16px;"
        />

        <!-- 不需要参数的集合（uiType=none） -->
        <template v-if="refreshConfig?.uiType === 'none'">
          <el-alert
            :title="refreshConfig?.allUpdate?.tips || '将更新所有数据，可能需要较长时间'"
            type="warning"
            :closable="false"
            show-icon
          />
        </template>

        <!-- 单个更新（uiType=single或single-batch） -->
        <template v-if="refreshConfig?.singleUpdate?.enabled">
          <el-divider content-position="left">单个更新</el-divider>
          
          <!-- 单个更新参数 -->
          <div v-for="param in refreshConfig.singleUpdate.params" :key="param.key">
            <!-- 文本输入 -->
            <el-form-item v-if="param.type === 'string'" :label="param.name">
              <el-input
                v-model="singleParams[param.key]"
                :placeholder="param.placeholder"
                clearable
              >
                <template #append>
                  <el-button 
                    @click="handleSingleRefresh"
                    :loading="refreshing"
                    :disabled="!singleParams[param.key] || refreshing"
                  >
                    {{ refreshConfig.singleUpdate.buttonText || '更新' }}
                  </el-button>
                </template>
              </el-input>
              <div v-if="param.description" class="param-description">
                {{ param.description }}
              </div>
            </el-form-item>
            
            <!-- 选择框 -->
            <el-form-item v-else-if="param.type === 'select'" :label="param.name">
              <el-select v-model="singleParams[param.key]" style="width: 100%">
                <el-option
                  v-for="opt in param.options"
                  :key="opt.value"
                  :label="opt.label"
                  :value="opt.value"
                />
              </el-select>
            </el-form-item>

            <!-- 数字输入 -->
            <el-form-item v-else-if="param.type === 'number'" :label="param.name">
              <el-input-number
                v-model="singleParams[param.key]"
                :min="param.min"
                :max="param.max"
                :step="param.step"
                style="width: 100%"
              />
            </el-form-item>
          </div>

          <el-alert 
            v-if="refreshConfig.singleUpdate.tips"
            :title="refreshConfig.singleUpdate.tips"
            type="info"
            :closable="false"
            show-icon
            style="margin-top: 12px;"
          />
        </template>

        <!-- 批量更新（uiType=batch或single-batch） -->
        <template v-if="refreshConfig?.batchUpdate?.enabled">
          <el-divider content-position="left">批量更新配置</el-divider>
          
          <el-alert 
            v-if="refreshConfig.batchUpdate.tips"
            :title="refreshConfig.batchUpdate.tips"
            type="info"
            :closable="false"
            show-icon
            style="margin-bottom: 16px;"
          />

          <!-- 批量更新参数（如果有） -->
          <div v-if="refreshConfig.batchUpdate.params">
            <div v-for="param in refreshConfig.batchUpdate.params" :key="param.key">
              <el-form-item v-if="param.type === 'select'" :label="param.name">
                <el-select v-model="batchParams[param.key]" style="width: 100%">
                  <el-option
                    v-for="opt in param.options"
                    :key="opt.value"
                    :label="opt.label"
                    :value="opt.value"
                  />
                </el-select>
              </el-form-item>
            </div>
          </div>

          <el-row :gutter="20">
            <!-- 批次大小配置 -->
            <el-col :span="12" v-if="refreshConfig.batchUpdate.batchSizeConfig">
              <el-form-item label="批次大小">
                <el-input-number 
                  v-model="batchSize"
                  :min="refreshConfig.batchUpdate.batchSizeConfig.min"
                  :max="refreshConfig.batchUpdate.batchSizeConfig.max"
                  :step="10"
                  style="width: 100%"
                />
              </el-form-item>
            </el-col>

            <!-- 并发数配置 -->
            <el-col :span="12" v-if="refreshConfig.batchUpdate.concurrencyConfig">
              <el-form-item label="并发数">
                <el-input-number 
                  v-model="concurrency"
                  :min="refreshConfig.batchUpdate.concurrencyConfig.min"
                  :max="refreshConfig.batchUpdate.concurrencyConfig.max"
                  :step="1"
                  style="width: 100%"
                />
              </el-form-item>
            </el-col>

            <!-- 延迟配置 -->
            <el-col :span="12" v-if="refreshConfig.batchUpdate.delayConfig">
              <el-form-item label="请求延迟(秒)">
                <el-input-number 
                  v-model="delay"
                  :min="refreshConfig.batchUpdate.delayConfig.min"
                  :max="refreshConfig.batchUpdate.delayConfig.max"
                  :step="refreshConfig.batchUpdate.delayConfig.step"
                  :precision="1"
                  style="width: 100%"
                />
              </el-form-item>
            </el-col>
          </el-row>

          <el-button 
            type="primary" 
            @click="handleBatchRefresh"
            :loading="refreshing"
            :disabled="refreshing"
            style="width: 100%;"
          >
            {{ refreshConfig.batchUpdate.buttonText || '开始批量更新' }}
          </el-button>
        </template>

        <!-- 全部更新按钮（针对不需要参数的集合） -->
        <template v-if="refreshConfig?.uiType === 'none'">
          <el-button 
            type="primary" 
            @click="handleAllRefresh"
            :loading="refreshing"
            :disabled="refreshing"
            style="width: 100%; margin-top: 16px;"
          >
            {{ refreshConfig?.allUpdate?.buttonText || '更新全部数据' }}
          </el-button>
        </template>
      </el-form>

      <template #footer>
        <el-button @click="apiParamsDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>

    <!-- 文件导入对话框 -->
    <FileImportDialog
      ref="fileImportRef"
      v-model:visible="uploadDialogVisible"
      :importing="importing"
      @import="handleImportFile"
    />

    <!-- 远程同步对话框 -->
    <RemoteSyncDialog
      v-model:visible="syncDialogVisible"
      :collection-name="collectionName"
      :syncing="remoteSyncing"
      :sync-result="remoteSyncStats"
      @sync="handleRemoteSync"
    />
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { UploadFilled } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { stocksApi, type CollectionStatsResponse, type RefreshStatusResponse } from '@/api/stocks'
import { getRefreshConfig, type CollectionRefreshConfig } from './collectionRefreshConfig'
import {
  CollectionDataTable,
  CollectionPageHeader,
  CollectionOverviewDialog,
  FileImportDialog,
  RemoteSyncDialog,
  type RemoteSyncConfig,
} from '@/components/collection'

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
const clearing = ref(false)
const refreshStatus = ref<RefreshStatusResponse | null>(null)
const currentTaskId = ref<string | null>(null)
let statusCheckInterval: number | null = null

// 对话框相关
const overviewDialogVisible = ref(false)
const uploadDialogVisible = ref(false)
const syncDialogVisible = ref(false)
const apiParamsDialogVisible = ref(false)

// 文件导入相关
const fileImportRef = ref()
const importing = ref(false)

// 远程同步相关
const remoteSyncHost = ref('')
const remoteSyncDbType = ref('mongodb')
const remoteSyncBatchSize = ref(1000)
const remoteSyncCollection = ref('')
const remoteSyncUsername = ref('')
const remoteSyncPassword = ref('')
const remoteSyncAuthSource = ref('admin')
const remoteSyncing = ref(false)
const remoteSyncStats = ref<any>(null)

// API更新参数相关（现在 getRefreshConfig 不会返回 null，未配置的集合使用默认配置）
const refreshConfig = computed<CollectionRefreshConfig>(() => {
  return getRefreshConfig(collectionName.value)
})
const singleParams = ref<Record<string, any>>({})
const batchParams = ref<Record<string, any>>({})
const batchSize = ref(50)
const concurrency = ref(3)
const delay = ref(0.5)

// 获取当前集合的固定信息（从 refreshConfig 动态获取）
const currentCollectionInfo = computed(() => {
  const config = refreshConfig.value
  return {
    name: collectionName.value,
    displayName: config?.displayName || collectionDef.value?.display_name || collectionName.value,
    fieldCount: displayFields.value.length,
    dataSource: 'https://akshare.akfamily.xyz/'
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

// 处理更新数据菜单命令
const handleUpdateCommand = (command: string) => {
  if (command === 'api') {
    // 打开API更新对话框前，初始化参数
    const config = refreshConfig.value
    apiParamsDialogVisible.value = true
    
    // 初始化单个更新参数
    singleParams.value = {}
    if (config?.singleUpdate?.params) {
      config.singleUpdate.params.forEach(param => {
        singleParams.value[param.key] = param.defaultValue || ''
      })
    }
    
    // 初始化批量更新参数
    batchParams.value = {}
    if (config?.batchUpdate?.params) {
      config.batchUpdate.params.forEach(param => {
        batchParams.value[param.key] = param.defaultValue || ''
      })
    }
    
    // 初始化批量配置
    if (config?.batchUpdate?.batchSizeConfig) {
      batchSize.value = config.batchUpdate.batchSizeConfig.default
    }
    if (config?.batchUpdate?.concurrencyConfig) {
      concurrency.value = config.batchUpdate.concurrencyConfig.default
    }
    if (config?.batchUpdate?.delayConfig) {
      delay.value = config.batchUpdate.delayConfig.default
    }
  } else if (command === 'file') {
    uploadDialogVisible.value = true
  } else if (command === 'sync') {
    syncDialogVisible.value = true
  }
}

// 单个更新
const handleSingleRefresh = async () => {
  const config = refreshConfig.value
  if (!config?.singleUpdate) return
  
  // 验证必填参数
  for (const param of config.singleUpdate.params) {
    if (param.required && !singleParams.value[param.key]) {
      ElMessage.warning(`请输入${param.name}`)
      return
    }
  }
  
  // 调用刷新
  await handleRefreshDataWithParams({ ...singleParams.value, mode: 'single' })
}

// 批量更新
const handleBatchRefresh = async () => {
  const params: any = {
    mode: 'batch',
    ...batchParams.value
  }
  
  // 添加批量配置
  if (batchSize.value) params.batch_size = batchSize.value
  if (concurrency.value) params.concurrency = concurrency.value
  if (delay.value) params.delay = delay.value
  
  await handleRefreshDataWithParams(params)
}

// 全部更新（不需要参数）
const handleAllRefresh = async () => {
  await handleRefreshDataWithParams({})
}

// 带参数的刷新数据
const handleRefreshDataWithParams = async (params: any = {}) => {
  const name = collectionName.value
  if (!name) return
  
  try {
    refreshing.value = true
    const res = await stocksApi.refreshCollection(name, params)
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

// 文件导入处理（使用共享组件）
const handleImportFile = async (files: File[]) => {
  if (!files.length) return
  
  importing.value = true
  
  try {
    const res = await stocksApi.uploadData(collectionName.value, files[0])
    
    if (res.success) {
      ElMessage.success(res.data?.message || '导入成功')
      fileImportRef.value?.clearFiles()
      uploadDialogVisible.value = false
      await Promise.all([loadStats(), refreshData()])
    } else {
      ElMessage.error(res.message || '导入失败')
    }
  } catch (error: any) {
    ElMessage.error(error.message || '导入失败')
  } finally {
    importing.value = false
  }
}

// 远程同步处理（使用共享组件）
const handleRemoteSync = async (config: RemoteSyncConfig) => {
  remoteSyncing.value = true
  remoteSyncStats.value = null

  try {
    const res = await stocksApi.syncData(collectionName.value, {
      host: config.host,
      username: config.username,
      password: config.password,
      authSource: config.authSource,
      collection: config.collection || collectionName.value,
      batch_size: config.batchSize
    })

    if (res.success) {
      remoteSyncStats.value = res.data
      ElMessage.success(res.data?.message || '同步成功')
      await Promise.all([loadStats(), refreshData()])
    } else {
      ElMessage.error(res.message || '同步失败')
    }
  } catch (error: any) {
    ElMessage.error(error.message || '同步失败')
  } finally {
    remoteSyncing.value = false
  }
}

// 后端全量导出
const exportAllData = async ({ fileName, format }: { fileName: string; format: 'csv' | 'xlsx' | 'json' }) => {
  try {
    const blob = await stocksApi.exportCollectionData(collectionName.value, {
      file_format: format,
      filter_field: filterField.value || undefined,
      filter_value: filterValue.value || undefined,
    })
    downloadBlob(blob, buildExportFileName(fileName, format))
  } catch (error: any) {
    console.error('导出全部数据失败:', error)
    const msg = error?.message || error?.response?.data?.detail || '导出失败'
    ElMessage.error(msg)
    throw error
  }
}

const buildExportFileName = (baseName: string, format: 'csv' | 'xlsx' | 'json'): string => {
  const normalized = baseName.replace(/\.(csv|xlsx|json)$/i, '')
  const suffix = format === 'xlsx' ? 'xlsx' : format
  return `${normalized}.${suffix}`
}

const downloadBlob = (blob: Blob, filename: string) => {
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
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

<style lang="scss" scoped>
@use '@/styles/collection.scss' as *;
</style>
