<template>
  <div class="collection-page">
    <!-- 页面头部 -->
    <CollectionPageHeader
      :collection-name="collectionName"
      :display-name="collectionInfo?.display_name || collectionName"
      :description="collectionInfo?.description"
      :stats="stats"
      :loading="statsLoading"
      @show-overview="overviewDialogVisible = true"
      @update-command="handleUpdateCommand"
      @clear-data="handleClearData"
      @export-data="handleExportData"
      @import-data="importDialogVisible = true"
      @sync-data="syncDialogVisible = true"
    />

    <!-- 数据表格 -->
    <CollectionDataTable
      :data="items"
      :fields="fields"
      :total="total"
      :page="page"
      :page-size="pageSize"
      :loading="loading"
      :sort-by="sortBy"
      :sort-dir="sortDir"
      @page-change="handlePageChange"
      @size-change="handleSizeChange"
      @sort-change="handleSortChange"
      @filter-change="handleFilterChange"
    />

    <!-- 数据概览对话框 -->
    <CollectionOverviewDialog
      v-model:visible="overviewDialogVisible"
      :collection-name="collectionName"
      :stats="stats"
    />

    <!-- API更新对话框 -->
    <el-dialog
      v-model="apiRefreshDialogVisible"
      title="API更新"
      width="600px"
      :close-on-click-modal="false"
    >
      <div v-if="updateConfig" class="update-dialog-content">
        <p class="update-description">{{ updateConfig.update_description }}</p>

        <!-- 单条更新 -->
        <el-card v-if="updateConfig.single_update?.enabled" class="update-card">
          <template #header>
            <div class="card-header">
              <span>单条更新</span>
              <el-tag size="small" type="success">可用</el-tag>
            </div>
          </template>
          <p class="update-hint">{{ updateConfig.single_update.description }}</p>
          <el-form :model="singleUpdateParams" label-width="100px">
            <el-form-item
              v-for="param in updateConfig.single_update.params"
              :key="param.name"
              :label="param.label"
              :required="param.required"
            >
              <el-input
                v-if="param.type === 'text'"
                v-model="singleUpdateParams[param.name]"
                :placeholder="param.placeholder"
              />
              <el-input-number
                v-else-if="param.type === 'number'"
                v-model="singleUpdateParams[param.name]"
                :min="param.min"
                :max="param.max"
                :step="param.step"
              />
              <el-select
                v-else-if="param.type === 'select'"
                v-model="singleUpdateParams[param.name]"
                :placeholder="param.placeholder"
              >
                <el-option
                  v-for="opt in param.options"
                  :key="opt.value"
                  :label="opt.label"
                  :value="opt.value"
                />
              </el-select>
            </el-form-item>
          </el-form>
          <el-button type="primary" @click="handleSingleUpdate" :loading="refreshing">
            执行单条更新
          </el-button>
        </el-card>

        <!-- 批量更新 -->
        <el-card v-if="updateConfig.batch_update?.enabled" class="update-card">
          <template #header>
            <div class="card-header">
              <span>批量更新</span>
              <el-tag size="small" type="warning">批量</el-tag>
            </div>
          </template>
          <p class="update-hint">{{ updateConfig.batch_update.description }}</p>
          
          <!-- 更新模式选择 -->
          <el-form-item label="更新模式">
            <el-radio-group v-model="updateMode">
              <el-radio label="incremental">增量更新</el-radio>
              <el-radio label="full">全量更新</el-radio>
            </el-radio-group>
          </el-form-item>
          
          <el-form :model="batchUpdateParams" label-width="100px">
            <el-form-item
              v-for="param in updateConfig.batch_update.params"
              :key="param.name"
              :label="param.label"
              :required="param.required"
            >
              <el-input
                v-if="param.type === 'text'"
                v-model="batchUpdateParams[param.name]"
                :placeholder="param.placeholder"
              />
              <el-input-number
                v-else-if="param.type === 'number'"
                v-model="batchUpdateParams[param.name]"
                :min="param.min"
                :max="param.max"
                :step="param.step"
              />
              <el-select
                v-else-if="param.type === 'select'"
                v-model="batchUpdateParams[param.name]"
                :placeholder="param.placeholder"
              >
                <el-option
                  v-for="opt in param.options"
                  :key="opt.value"
                  :label="opt.label"
                  :value="opt.value"
                />
              </el-select>
            </el-form-item>
          </el-form>
          <el-button type="warning" @click="handleBatchUpdate" :loading="refreshing">
            执行批量更新
          </el-button>
        </el-card>

        <!-- 进度显示 -->
        <div v-if="refreshing" class="progress-section">
          <el-progress :percentage="progressPercentage" :status="progressStatus" />
          <p class="progress-message">{{ progressMessage }}</p>
        </div>
      </div>
    </el-dialog>

    <!-- 文件导入对话框 -->
    <FileImportDialog
      v-model:visible="importDialogVisible"
      :collection-name="collectionName"
      @success="handleImportSuccess"
    />

    <!-- 远程同步对话框 -->
    <RemoteSyncDialog
      v-model:visible="syncDialogVisible"
      :collection-name="collectionName"
      @success="handleSyncSuccess"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { indexsApi } from '@/api/indexs'
import CollectionPageHeader from '@/components/collection/CollectionPageHeader.vue'
import CollectionDataTable from '@/components/collection/CollectionDataTable.vue'
import CollectionOverviewDialog from '@/components/collection/CollectionOverviewDialog.vue'
import FileImportDialog from '@/components/collection/FileImportDialog.vue'
import RemoteSyncDialog from '@/components/collection/RemoteSyncDialog.vue'

const route = useRoute()
const collectionName = computed(() => route.params.collectionName as string)

// 集合信息
const collectionInfo = ref<any>(null)
const stats = ref<any>({})
const statsLoading = ref(false)

// 数据表格
const items = ref<any[]>([])
const fields = ref<any[]>([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(20)
const loading = ref(false)
const sortBy = ref('')
const sortDir = ref<'asc' | 'desc'>('desc')
const filterField = ref('')
const filterValue = ref('')

// 对话框
const overviewDialogVisible = ref(false)
const apiRefreshDialogVisible = ref(false)
const importDialogVisible = ref(false)
const syncDialogVisible = ref(false)

// 更新配置
const updateConfig = ref<any>(null)
const singleUpdateParams = ref<Record<string, any>>({})
const batchUpdateParams = ref<Record<string, any>>({})
const updateMode = ref('incremental')

// 刷新状态
const refreshing = ref(false)
const taskId = ref('')
const progressPercentage = ref(0)
const progressMessage = ref('')
const progressStatus = ref<'' | 'success' | 'exception' | 'warning'>('')
let pollTimer: ReturnType<typeof setInterval> | null = null

// 加载集合信息
const loadCollectionInfo = async () => {
  try {
    const res = await indexsApi.getCollections()
    if (res.success) {
      collectionInfo.value = res.data.find((c: any) => c.name === collectionName.value)
    }
  } catch (error) {
    console.error('加载集合信息失败:', error)
  }
}

// 加载统计信息
const loadStats = async () => {
  statsLoading.value = true
  try {
    const res = await indexsApi.getCollectionStats(collectionName.value)
    if (res.success) {
      stats.value = res.data
    }
  } catch (error) {
    console.error('加载统计信息失败:', error)
  } finally {
    statsLoading.value = false
  }
}

// 加载数据
const loadData = async () => {
  loading.value = true
  try {
    const res = await indexsApi.getCollectionData(collectionName.value, {
      page: page.value,
      page_size: pageSize.value,
      sort_by: sortBy.value || undefined,
      sort_dir: sortDir.value,
      filter_field: filterField.value || undefined,
      filter_value: filterValue.value || undefined,
    })
    if (res.success) {
      items.value = res.data.items
      total.value = res.data.total
      fields.value = res.data.fields || []
    }
  } catch (error) {
    console.error('加载数据失败:', error)
    ElMessage.error('加载数据失败')
  } finally {
    loading.value = false
  }
}

// 加载更新配置
const loadUpdateConfig = async () => {
  try {
    const res = await indexsApi.getCollectionUpdateConfig(collectionName.value)
    if (res.success) {
      updateConfig.value = res.data
      // 初始化默认值
      if (updateConfig.value?.single_update?.params) {
        updateConfig.value.single_update.params.forEach((p: any) => {
          if (p.default !== undefined) {
            singleUpdateParams.value[p.name] = p.default
          }
        })
      }
      if (updateConfig.value?.batch_update?.params) {
        updateConfig.value.batch_update.params.forEach((p: any) => {
          if (p.default !== undefined) {
            batchUpdateParams.value[p.name] = p.default
          }
        })
      }
    }
  } catch (error) {
    console.error('加载更新配置失败:', error)
  }
}

// 处理分页
const handlePageChange = (newPage: number) => {
  page.value = newPage
  loadData()
}

const handleSizeChange = (newSize: number) => {
  pageSize.value = newSize
  page.value = 1
  loadData()
}

// 处理排序
const handleSortChange = ({ prop, order }: { prop: string; order: 'ascending' | 'descending' | null }) => {
  sortBy.value = prop
  sortDir.value = order === 'ascending' ? 'asc' : 'desc'
  loadData()
}

// 处理筛选
const handleFilterChange = ({ field, value }: { field: string; value: string }) => {
  filterField.value = field
  filterValue.value = value
  page.value = 1
  loadData()
}

// 处理更新命令
const handleUpdateCommand = (command: string) => {
  if (command === 'api') {
    apiRefreshDialogVisible.value = true
  }
}

// 单条更新
const handleSingleUpdate = async () => {
  refreshing.value = true
  progressPercentage.value = 0
  progressMessage.value = '正在提交更新请求...'
  progressStatus.value = ''

  try {
    const res = await indexsApi.refreshCollectionData(collectionName.value, {
      update_type: 'single',
      ...singleUpdateParams.value,
    })
    if (res.success) {
      taskId.value = res.data.task_id
      startPolling()
    } else {
      throw new Error(res.message || '提交更新请求失败')
    }
  } catch (error: any) {
    ElMessage.error(error.message || '更新失败')
    refreshing.value = false
  }
}

// 批量更新
const handleBatchUpdate = async () => {
  refreshing.value = true
  progressPercentage.value = 0
  progressMessage.value = '正在提交批量更新请求...'
  progressStatus.value = ''

  try {
    const res = await indexsApi.refreshCollectionData(collectionName.value, {
      update_type: 'batch',
      update_mode: updateMode.value,
      ...batchUpdateParams.value,
    })
    if (res.success) {
      taskId.value = res.data.task_id
      startPolling()
    } else {
      throw new Error(res.message || '提交更新请求失败')
    }
  } catch (error: any) {
    ElMessage.error(error.message || '更新失败')
    refreshing.value = false
  }
}

// 轮询任务状态
const startPolling = () => {
  if (pollTimer) {
    clearInterval(pollTimer)
  }
  pollTimer = setInterval(async () => {
    try {
      const res = await indexsApi.getRefreshTaskStatus(collectionName.value, taskId.value)
      if (res.success) {
        const task = res.data
        progressPercentage.value = Math.round((task.progress || 0) / (task.total || 100) * 100)
        progressMessage.value = task.message || ''

        if (task.status === 'completed' || task.status === 'success') {
          progressStatus.value = 'success'
          ElMessage.success('更新完成')
          stopPolling()
          loadData()
          loadStats()
        } else if (task.status === 'failed') {
          progressStatus.value = 'exception'
          ElMessage.error(task.error || '更新失败')
          stopPolling()
        }
      }
    } catch (error) {
      console.error('获取任务状态失败:', error)
    }
  }, 1000)
}

const stopPolling = () => {
  if (pollTimer) {
    clearInterval(pollTimer)
    pollTimer = null
  }
  refreshing.value = false
}

// 清空数据
const handleClearData = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要清空该集合的所有数据吗？此操作不可恢复！',
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    const res = await indexsApi.clearCollectionData(collectionName.value)
    if (res.success) {
      ElMessage.success(`成功清空 ${res.data.deleted_count} 条数据`)
      loadData()
      loadStats()
    } else {
      throw new Error(res.message || '清空失败')
    }
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '清空失败')
    }
  }
}

// 导出数据
const handleExportData = async (format: string) => {
  try {
    const blob = await indexsApi.exportCollectionData(collectionName.value, {
      file_format: format as 'csv' | 'xlsx' | 'json',
      filter_field: filterField.value,
      filter_value: filterValue.value,
    })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${collectionName.value}.${format}`
    a.click()
    window.URL.revokeObjectURL(url)
    ElMessage.success('导出成功')
  } catch (error: any) {
    ElMessage.error(error.message || '导出失败')
  }
}

// 导入成功
const handleImportSuccess = () => {
  loadData()
  loadStats()
}

// 同步成功
const handleSyncSuccess = () => {
  loadData()
  loadStats()
}

// 监听路由变化
watch(collectionName, () => {
  loadCollectionInfo()
  loadStats()
  loadData()
  loadUpdateConfig()
})

onMounted(() => {
  loadCollectionInfo()
  loadStats()
  loadData()
  loadUpdateConfig()
})

onUnmounted(() => {
  stopPolling()
})
</script>

<style lang="scss" scoped>
.collection-page {
  padding: 20px;
}

.update-dialog-content {
  .update-description {
    color: var(--el-text-color-secondary);
    margin-bottom: 16px;
  }

  .update-card {
    margin-bottom: 16px;

    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .update-hint {
      color: var(--el-text-color-secondary);
      font-size: 13px;
      margin-bottom: 12px;
    }
  }

  .progress-section {
    margin-top: 16px;
    padding: 16px;
    background: var(--el-fill-color-light);
    border-radius: 4px;

    .progress-message {
      margin-top: 8px;
      color: var(--el-text-color-secondary);
      font-size: 13px;
    }
  }
}
</style>
