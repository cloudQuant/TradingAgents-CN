<template>
  <div class="collection-page">
    <!-- 页面头部 -->
    <CollectionPageHeader
      :collection-name="collectionName"
      :display-name="collectionInfo?.display_name"
      :description="collectionInfo?.description"
      :loading="loading"
      :updating="refreshing"
      :clearing="clearing"
      @show-overview="overviewDialogVisible = true"
      @refresh="loadData"
      @update-command="handleUpdateCommand"
      @clear-data="handleClearData"
    />

    <div class="content">
      <!-- 实时行情图表 (仅futures_zh_spot显示) -->
      <el-card shadow="hover" class="chart-card" v-if="collectionName === 'futures_zh_spot' && chartData.length > 0">
        <template #header>
          <span>价格走势</span>
        </template>
        <v-chart
          :option="priceChartOption"
          :autoresize="true"
          style="height: 300px; width: 100%"
        />
      </el-card>

      <!-- 数据表格 -->
      <CollectionDataTable
        :data="tableData"
        :fields="fields"
        :total="total"
        :loading="loading"
        :collection-name="collectionName"
        :export-all-data="exportAllData"
        v-model:page="currentPage"
        v-model:page-size="pageSize"
        v-model:filter-value="filterValue"
        v-model:filter-field="filterField"
        @search="handleFilter"
        @refresh="loadData"
        @page-change="loadData"
        @size-change="loadData"
      />
    </div>

    <!-- 更新数据对话框 -->
    <el-dialog
      v-model="refreshDialogVisible"
      title="更新数据"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form label-width="120px">
        <el-form-item label="集合名称">
          <el-input :value="collectionInfo?.display_name || collectionName" disabled />
        </el-form-item>

        <el-form-item label="更新说明" v-if="updateConfig?.update_description">
          <el-text type="info">{{ updateConfig.update_description }}</el-text>
        </el-form-item>

        <!-- 更新类型选择 -->
        <el-form-item label="更新类型" v-if="updateConfig?.batch_update?.enabled">
          <el-radio-group v-model="updateType">
            <el-radio value="single" v-if="updateConfig?.single_update?.enabled">单条更新</el-radio>
            <el-radio value="batch">批量更新</el-radio>
          </el-radio-group>
        </el-form-item>

        <!-- 动态参数表单 -->
        <template v-if="updateType === 'single' && updateConfig?.single_update?.params">
          <el-form-item
            v-for="param in updateConfig.single_update.params"
            :key="param.name"
            :label="param.label || param.name"
          >
            <el-select
              v-if="param.options"
              v-model="updateParams[param.name]"
              style="width: 100%"
              :placeholder="param.placeholder || `请选择${param.label}`"
            >
              <el-option
                v-for="opt in param.options"
                :key="opt.value"
                :label="opt.label"
                :value="opt.value"
              />
            </el-select>
            <el-input
              v-else
              v-model="updateParams[param.name]"
              :placeholder="param.placeholder || `请输入${param.label}`"
            />
            <div class="param-hint" v-if="param.description">
              <el-text size="small" type="info">{{ param.description }}</el-text>
            </div>
          </el-form-item>
        </template>

        <template v-if="updateType === 'batch' && updateConfig?.batch_update?.params">
          <el-form-item
            v-for="param in updateConfig.batch_update.params"
            :key="param.name"
            :label="param.label || param.name"
          >
            <el-select
              v-if="param.options"
              v-model="updateParams[param.name]"
              style="width: 100%"
              :placeholder="param.placeholder || `请选择${param.label}`"
            >
              <el-option
                v-for="opt in param.options"
                :key="opt.value"
                :label="opt.label"
                :value="opt.value"
              />
            </el-select>
            <el-input-number
              v-else-if="param.type === 'number'"
              v-model="updateParams[param.name]"
              :min="param.min || 1"
              :max="param.max || 100"
              style="width: 100%"
            />
            <el-input
              v-else
              v-model="updateParams[param.name]"
              :placeholder="param.placeholder || `请输入${param.label}`"
            />
            <div class="param-hint" v-if="param.description">
              <el-text size="small" type="info">{{ param.description }}</el-text>
            </div>
          </el-form-item>
        </template>

        <!-- 进度显示 -->
        <div v-if="refreshing" style="margin-top: 20px;">
          <el-progress
            :percentage="taskProgress"
            :status="taskStatus === 'completed' ? 'success' : (taskStatus === 'failed' ? 'exception' : '')"
            :stroke-width="18"
          />
          <p style="margin-top: 10px; font-size: 14px; color: #606266; text-align: center;">
            {{ taskMessage || '数据更新中，请稍候...' }}
          </p>
        </div>
      </el-form>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="handleCancelRefresh" :disabled="refreshing && taskStatus === 'running'">
            {{ refreshing ? '后台运行' : '取消' }}
          </el-button>
          <el-button type="primary" @click="handleRefresh" :loading="refreshing" :disabled="refreshing">
            开始更新
          </el-button>
        </span>
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

    <!-- 数据概览对话框 -->
    <CollectionOverviewDialog
      v-model:visible="overviewDialogVisible"
      :collection-name="collectionName"
      :display-name="collectionInfo?.display_name"
      :description="collectionInfo?.description"
      :total-count="stats?.total_count"
      :field-count="fields.length"
      :latest-update="stats?.latest_date || stats?.latest_time"
      :data-source="collectionInfo?.data_source"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
// import { UploadFilled } from '@element-plus/icons-vue'  // 已由共享组件处理
import { ElMessage, ElMessageBox } from 'element-plus'
import { futuresApi } from '@/api/futures'
import VChart from 'vue-echarts'
import {
  CollectionDataTable,
  CollectionPageHeader,
  CollectionOverviewDialog,
  FileImportDialog,
  RemoteSyncDialog,
  type RemoteSyncConfig,
} from '@/components/collection'

const route = useRoute()
const collectionName = ref(route.params.collectionName as string)

// 数据状态
const loading = ref(false)
const refreshing = ref(false)
const clearing = ref(false)
const tableData = ref<any[]>([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(50)
const stats = ref<any>(null)
const collectionInfo = ref<any>(null)
const chartData = ref<any[]>([])
const fields = ref<any[]>([])
const overviewDialogVisible = ref(false)
const currentCollectionInfo = ref<any>({
  name: '',
  displayName: '',
  fieldCount: 0,
  dataSource: '暂无',
})

// 筛选
const filterValue = ref('')
const filterField = ref('')

// 更新数据对话框
const refreshDialogVisible = ref(false)
const uploadDialogVisible = ref(false)
const syncDialogVisible = ref(false)
const symbol = ref('')
const market = ref('CF')
const adjust = ref('0')

// 新增：更新配置和任务状态
const updateConfig = ref<any>(null)
const updateType = ref('single')
const updateParams = ref<Record<string, any>>({})
const currentTaskId = ref('')
const taskProgress = ref(0)
const taskStatus = ref('')
const taskMessage = ref('')
let taskPollTimer: any = null

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

// 计算显示的字段
const displayFields = computed(() => {
  if (tableData.value.length === 0) return []
  const firstRow = tableData.value[0]
  return Object.keys(firstRow).filter(key => key !== '_id')
})

const displayColumns = computed(() => {
  if (fields.value && fields.value.length > 0) {
    return fields.value.map((f: any) => f.name)
  }
  return displayFields.value
})

// 价格图表配置
const priceChartOption = computed(() => {
  if (chartData.value.length === 0) return null
  
  const symbols = chartData.value.map(item => item.symbol)
  const prices = chartData.value.map(item => item.current_price)
  
  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    xAxis: {
      type: 'category',
      data: symbols,
      axisLabel: {
        rotate: 45
      }
    },
    yAxis: {
      type: 'value',
      name: '价格'
    },
    series: [{
      data: prices,
      type: 'bar',
      itemStyle: {
        color: '#409EFF'
      }
    }]
  }
})

const formatNumber = (value: number) => {
  if (!value) return '0'
  return value.toLocaleString()
}

// 加载集合信息
const loadCollectionInfo = async () => {
  try {
    const res = await futuresApi.getCollections()
    if (res.success) {
      collectionInfo.value = res.data.find((c: any) => c.name === collectionName.value)
    }
  } catch (error) {
    console.error('加载集合信息失败:', error)
  }
}

// 加载统计数据
const loadStats = async () => {
  try {
    const res = await futuresApi.getCollectionStats(collectionName.value)
    if (res.success) {
      stats.value = res.data
    }
  } catch (error) {
    console.error('加载统计数据失败:', error)
  }
}

// 加载数据
const loadData = async () => {
  loading.value = true
  try {
    const res = await futuresApi.getCollectionData(collectionName.value, {
      page: currentPage.value,
      page_size: pageSize.value,
      filter_field: filterField.value,
      filter_value: filterValue.value
    })
    
    if (res.success) {
      tableData.value = res.data.items || []
      total.value = res.data.total || 0
      fields.value = res.data.fields || []
      
      // 为图表准备数据（取前20条）
      if (collectionName.value === 'futures_zh_spot') {
        chartData.value = (res.data.items || []).slice(0, 20)
      }
    } else {
      ElMessage.error(res.error || '加载数据失败')
    }
  } catch (error: any) {
    console.error('加载数据失败:', error)
    ElMessage.error(error.message || '加载数据失败')
  } finally {
    loading.value = false
  }
}

const showOverviewDialog = () => {
  const info = collectionInfo.value || {}
  const name = info.name || collectionName.value
  const displayName = info.display_name || collectionName.value
  const fieldCount = Array.isArray(info.fields) ? info.fields.length : (fields.value?.length || 0)
  const dataSource = info.data_source || info.source || '暂无'
  currentCollectionInfo.value = {
    name,
    displayName,
    fieldCount,
    dataSource,
  }
  overviewDialogVisible.value = true
}

// 显示更新对话框
const showRefreshDialog = () => {
  refreshDialogVisible.value = true
}

// 处理更新数据下拉菜单命令
const handleUpdateCommand = (command: string) => {
  if (command === 'api') {
    refreshDialogVisible.value = true
  } else if (command === 'file') {
    uploadDialogVisible.value = true
  } else if (command === 'sync') {
    syncDialogVisible.value = true
  }
}

// 文件导入处理（使用共享组件）
const handleImportFile = async (files: File[]) => {
  if (!files.length) return
  
  importing.value = true
  
  try {
    const res = await futuresApi.uploadData(collectionName.value, files[0])
    
    if (res.success) {
      ElMessage.success(res.message || '导入成功')
      fileImportRef.value?.clearFiles()
      uploadDialogVisible.value = false
      await loadStats()
      await loadData()
    } else {
      ElMessage.error(res.message || '导入失败')
    }
  } catch (error: any) {
    console.error('导入失败:', error)
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
    const res = await futuresApi.syncData(collectionName.value, {
      host: config.host,
      username: config.username,
      password: config.password,
      authSource: config.authSource,
      collection: config.collection || collectionName.value,
      batch_size: config.batchSize
    })

    if (res.success) {
      remoteSyncStats.value = res.data
      ElMessage.success(res.message || '同步成功')
      await loadStats()
      await loadData()
    } else {
      ElMessage.error(res.message || '同步失败')
    }
  } catch (error: any) {
    console.error('同步失败:', error)
    ElMessage.error(error.message || '同步失败')
  } finally {
    remoteSyncing.value = false
  }
}

// 加载更新配置
const loadUpdateConfig = async () => {
  try {
    const res = await futuresApi.getCollectionUpdateConfig(collectionName.value)
    if (res.success) {
      updateConfig.value = res.data
      // 根据配置设置默认更新类型
      if (updateConfig.value?.single_update?.enabled) {
        updateType.value = 'single'
      } else if (updateConfig.value?.batch_update?.enabled) {
        updateType.value = 'batch'
      }
      // 初始化默认参数值
      initDefaultParams()
    }
  } catch (error) {
    console.error('加载更新配置失败:', error)
  }
}

// 初始化默认参数值
const initDefaultParams = () => {
  updateParams.value = {}
  const config = updateType.value === 'batch' 
    ? updateConfig.value?.batch_update 
    : updateConfig.value?.single_update
  
  if (config?.params) {
    for (const param of config.params) {
      if (param.default !== undefined) {
        updateParams.value[param.name] = param.default
      }
    }
  }
}

// 轮询任务状态
const pollTaskStatus = async () => {
  if (!currentTaskId.value) return
  
  try {
    const res = await futuresApi.getRefreshTaskStatus(currentTaskId.value)
    if (res.success && res.data) {
      const task = res.data
      taskProgress.value = task.progress || 0
      taskStatus.value = task.status || ''
      taskMessage.value = task.message || ''
      
      if (task.status === 'completed') {
        ElMessage.success('更新完成')
        stopTaskPoll()
        refreshing.value = false
        loadData()
        loadStats()
      } else if (task.status === 'failed') {
        ElMessage.error(task.error || '更新失败')
        stopTaskPoll()
        refreshing.value = false
      }
    }
  } catch (error) {
    console.error('获取任务状态失败:', error)
  }
}

// 开始轮询
const startTaskPoll = () => {
  stopTaskPoll()
  taskPollTimer = setInterval(pollTaskStatus, 2000)
}

// 停止轮询
const stopTaskPoll = () => {
  if (taskPollTimer) {
    clearInterval(taskPollTimer)
    taskPollTimer = null
  }
}

// 取消/后台运行
const handleCancelRefresh = () => {
  if (refreshing.value) {
    // 后台运行，关闭对话框但继续轮询
    refreshDialogVisible.value = false
    ElMessage.info('任务将在后台继续运行')
  } else {
    refreshDialogVisible.value = false
  }
}

// 更新数据（使用新API）
const handleRefresh = async () => {
  refreshing.value = true
  taskProgress.value = 0
  taskStatus.value = 'pending'
  taskMessage.value = '准备更新...'
  
  try {
    // 构建参数
    const params: any = { ...updateParams.value }
    if (updateType.value === 'batch') {
      params.batch = true
    }
    
    // 兼容旧逻辑
    if (collectionName.value === 'futures_zh_spot') {
      if (symbol.value) params.symbol = symbol.value
      params.market = market.value
      params.adjust = adjust.value
    }
    
    // 调用新的刷新API
    const res = await futuresApi.refreshCollectionV2(collectionName.value, params)
    
    if (res.success && res.data?.task_id) {
      currentTaskId.value = res.data.task_id
      ElMessage.success('更新任务已提交')
      startTaskPoll()
    } else {
      ElMessage.error(res.error || '更新失败')
      refreshing.value = false
    }
  } catch (error: any) {
    console.error('更新失败:', error)
    ElMessage.error(error.response?.data?.detail || error.message || '更新失败')
    refreshing.value = false
  }
}

// 清空数据
const handleClearData = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要清空所有数据吗？此操作不可恢复！',
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    clearing.value = true
    const res = await futuresApi.clearCollection(collectionName.value)
    
    if (res.success) {
      ElMessage.success('数据已清空')
      loadData()
      loadStats()
    } else {
      ElMessage.error(res.error || '清空失败')
    }
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('清空数据失败:', error)
      ElMessage.error(error.message || '清空失败')
    }
  } finally {
    clearing.value = false
  }
}

// 筛选
const handleFilter = () => {
  currentPage.value = 1
  loadData()
}

// 分页
const handleSizeChange = (val: number) => {
  pageSize.value = val
  currentPage.value = 1
  loadData()
}

const handlePageChange = (val: number) => {
  currentPage.value = val
  loadData()
}

// 监听路由变化
watch(() => route.params.collectionName, (newVal) => {
  if (newVal) {
    collectionName.value = newVal as string
    currentPage.value = 1
    stopTaskPoll()
    loadCollectionInfo()
    loadUpdateConfig()
    loadStats()
    loadData()
  }
})

// 监听更新类型变化，重新初始化参数
watch(updateType, () => {
  initDefaultParams()
})

// 后端全量导出
const exportAllData = async ({ fileName, format }: { fileName: string; format: 'csv' | 'xlsx' | 'json' }) => {
  try {
    const blob = await futuresApi.exportCollectionData(collectionName.value, {
      file_format: format,
      filter_field: filterField.value || undefined,
      filter_value: filterValue.value || undefined,
    })
    downloadBlob(blob, buildExportFileName(fileName, format))
  } catch (error: any) {
    console.error('导出全部数据失败:', error)
    ElMessage.error(error?.message || '导出失败')
    throw error
  }
}

const buildExportFileName = (baseName: string, format: 'csv' | 'xlsx' | 'json'): string => {
  const normalized = baseName.replace(/\.(csv|xlsx|json)$/i, '')
  return `${normalized}.${format === 'xlsx' ? 'xlsx' : format}`
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

// 初始化
onMounted(() => {
  loadCollectionInfo()
  loadUpdateConfig()
  loadStats()
  loadData()
})
</script>

<style lang="scss" scoped>
@use '@/styles/collection.scss' as *;
</style>
