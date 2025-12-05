/**
 * 货币集合通用逻辑 Composable
 */
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { currenciesApi } from '@/api/currencies'
import { handleFundError, handleDangerousOperation } from '@/utils/fundErrorHandler'

interface FieldDefinition {
  name: string
  type: string
  example?: string | null
}

interface CurrencyCollection {
  name: string
  display_name: string
  description: string
  route: string
  fields: string[]
}

interface CollectionStats {
  total_count: number
  collection_name?: string
  earliest_date?: string
  latest_date?: string
}

interface RemoteSyncConfig {
  host: string
  username?: string
  password?: string
  authSource?: string
  collection?: string
  batchSize?: number
}

export function useCurrenciesCollection() {
  const route = useRoute()
  const collectionName = computed(() => route.params.collectionName as string)

  const loading = ref(false)
  const items = ref<Record<string, any>[]>([])
  const fields = ref<FieldDefinition[]>([])
  const page = ref(1)
  const pageSize = ref(50)
  const total = ref(0)
  const filterField = ref('')
  const filterValue = ref('')
  const sortBy = ref('')
  const sortDir = ref<'asc' | 'desc'>('desc')
  const stats = ref<CollectionStats | null>(null)
  const collectionInfo = ref<CurrencyCollection | null>(null)

  const apiRefreshDialogVisible = ref(false)
  const fileImportDialogVisible = ref(false)
  const remoteSyncDialogVisible = ref(false)
  const refreshing = ref(false)
  const currentTaskId = ref('')
  const progressPercentage = ref(0)
  const progressStatus = ref<'success' | 'exception' | 'warning' | ''>('')
  const progressMessage = ref('')
  let batchProgressTimer: ReturnType<typeof setInterval> | null = null

  const updateConfig = ref<any>(null)
  const singleUpdateParams = ref<Record<string, any>>({})
  const batchUpdateParams = ref<Record<string, any>>({})
  const updateMode = ref<string>('incremental')
  const singleUpdating = ref(false)
  const batchUpdating = ref(false)
  const fileImportRef = ref()
  const importing = ref(false)
  const remoteSyncing = ref(false)
  const remoteSyncStats = ref<any>(null)
  const clearing = ref(false)
  const overviewDialogVisible = ref(false)

  const currentCollectionInfo = computed(() => ({
    name: collectionName.value,
    displayName: collectionInfo.value?.display_name || collectionName.value,
    fieldCount: fields.value.length,
    dataSource: '暂无'
  }))

  const loadData = async (extraParams: Record<string, any> = {}) => {
    loading.value = true
    try {
      const collectionsRes = await currenciesApi.getCollections()
      if (collectionsRes.success && collectionsRes.data) {
        collectionInfo.value = collectionsRes.data.find((c: any) => c.name === collectionName.value) || null
      }

      const statsRes = await currenciesApi.getCollectionStats(collectionName.value)
      if (statsRes.success && statsRes.data) {
        stats.value = statsRes.data as any
      }

      const dataRes = await currenciesApi.getCollectionData(collectionName.value, {
        page: page.value,
        page_size: pageSize.value,
        sort_by: sortBy.value || undefined,
        sort_dir: sortDir.value,
        filter_field: filterField.value || undefined,
        filter_value: filterValue.value || undefined,
        ...extraParams,
      })
      
      if (dataRes.success && dataRes.data) {
        items.value = dataRes.data.items || []
        const allFields = dataRes.data.fields || []
        const metaFields = ['code', 'endpoint', 'source', 'updated_at', 'scraped_at']
        const mainFields = allFields.filter((f: FieldDefinition) => !metaFields.includes(f.name))
        const metaFieldsData = allFields.filter((f: FieldDefinition) => metaFields.includes(f.name))
        fields.value = [...mainFields, ...metaFieldsData]
        total.value = dataRes.data.total || 0
      }
    } catch (error) {
      handleFundError(error, '加载数据失败')
    } finally {
      loading.value = false
    }
  }

  const handleSortChange = ({ prop, order }: any) => {
    sortBy.value = order ? prop : ''
    sortDir.value = order === 'ascending' ? 'asc' : 'desc'
    loadData()
  }

  const exportAllData = async ({ fileName, format }: { fileName: string; format: 'csv' | 'xlsx' | 'json' }) => {
    try {
      const blob = await currenciesApi.exportCollectionData(collectionName.value, {
        file_format: format,
        sort_by: sortBy.value || undefined,
        sort_dir: sortDir.value,
        filter_field: filterField.value || undefined,
        filter_value: filterValue.value || undefined,
      })
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `${fileName}.${format}`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      URL.revokeObjectURL(url)
    } catch (error) {
      handleFundError(error, '导出失败')
    }
  }

  const handleUpdateCommand = (command: string) => {
    progressPercentage.value = 0
    progressStatus.value = ''
    progressMessage.value = ''
    if (command === 'api') apiRefreshDialogVisible.value = true
    else if (command === 'file') fileImportDialogVisible.value = true
    else if (command === 'sync' || command === 'remote') remoteSyncDialogVisible.value = true
  }

  const loadUpdateConfig = async () => {
    try {
      updateConfig.value = null
      singleUpdateParams.value = {}
      batchUpdateParams.value = {}
      const res = await currenciesApi.getCollectionUpdateConfig(collectionName.value)
      if (res.success && res.data) {
        updateConfig.value = res.data
        if (res.data.single_update?.params) {
          for (const param of res.data.single_update.params) {
            if (param.default !== undefined) singleUpdateParams.value[param.name] = param.default
          }
        }
        if (res.data.batch_update?.params) {
          for (const param of res.data.batch_update.params) {
            if (param.default !== undefined) batchUpdateParams.value[param.name] = param.default
          }
        }
      }
    } catch (error) {
      ElMessage.error('加载更新配置失败')
    }
  }

  const canSingleUpdate = computed(() => {
    if (!updateConfig.value?.single_update?.enabled) return false
    const params = updateConfig.value.single_update.params || []
    return params.every((p: any) => !p.required || singleUpdateParams.value[p.name])
  })

  const canBatchUpdate = computed(() => {
    if (!updateConfig.value?.batch_update?.enabled) return false
    const params = updateConfig.value.batch_update.params || []
    return params.every((p: any) => !p.required || batchUpdateParams.value[p.name])
  })

  const pollTaskStatus = async () => {
    if (batchProgressTimer) clearInterval(batchProgressTimer)
    let pollCount = 0
    batchProgressTimer = setInterval(async () => {
      pollCount++
      if (pollCount > 1800) {
        clearInterval(batchProgressTimer!)
        batchProgressTimer = null
        progressStatus.value = 'warning'
        progressMessage.value = '任务超时'
        batchUpdating.value = false
        singleUpdating.value = false
        return
      }
      try {
        const res = await currenciesApi.getRefreshTaskStatus(collectionName.value, currentTaskId.value)
        if (res.success && res.data) {
          const task = res.data
          if (task.progress && task.total) progressPercentage.value = Math.round((task.progress / task.total) * 100)
          progressMessage.value = task.message || '正在更新...'
          if ((task.status as string) === 'success' || task.status === 'completed') {
            clearInterval(batchProgressTimer!)
            batchProgressTimer = null
            progressStatus.value = 'success'
            progressPercentage.value = 100
            progressMessage.value = task.message || '更新完成'
            batchUpdating.value = false
            singleUpdating.value = false
            await loadData()
            ElMessage.success('更新完成')
          } else if (task.status === 'failed') {
            clearInterval(batchProgressTimer!)
            batchProgressTimer = null
            progressStatus.value = 'exception'
            progressMessage.value = task.error || '更新失败'
            batchUpdating.value = false
            singleUpdating.value = false
            ElMessage.error(task.error || '更新失败')
          }
        }
      } catch (e) {
        if (pollCount > 5) {
          clearInterval(batchProgressTimer!)
          batchProgressTimer = null
          progressStatus.value = 'exception'
          batchUpdating.value = false
          singleUpdating.value = false
        }
      }
    }, 1000)
  }

  const handleSingleUpdate = async () => {
    if (!canSingleUpdate.value || singleUpdating.value || batchUpdating.value) return
    singleUpdating.value = true
    progressPercentage.value = 0
    progressMessage.value = '正在更新...'
    try {
      const params: any = { update_type: 'single', ...singleUpdateParams.value }
      const res = await currenciesApi.refreshCollectionData(collectionName.value, params)
      if (res.success && res.data?.task_id) {
        currentTaskId.value = res.data.task_id
        pollTaskStatus()
      } else {
        progressPercentage.value = 100
        progressStatus.value = 'success'
        progressMessage.value = (res.data as any)?.message || '更新完成'
        await loadData()
        singleUpdating.value = false
      }
    } catch (error) {
      progressStatus.value = 'exception'
      handleFundError(error, '更新失败')
      singleUpdating.value = false
    }
  }

  const handleBatchUpdate = async () => {
    if (!canBatchUpdate.value) return
    batchUpdating.value = true
    progressPercentage.value = 0
    progressMessage.value = '正在创建任务...'
    try {
      const params: any = { update_type: 'batch', update_mode: updateMode.value, ...batchUpdateParams.value }
      const res = await currenciesApi.refreshCollectionData(collectionName.value, params)
      if (res.success && res.data?.task_id) {
        currentTaskId.value = res.data.task_id
        pollTaskStatus()
      } else {
        progressPercentage.value = 100
        progressStatus.value = 'success'
        await loadData()
        batchUpdating.value = false
      }
    } catch (error) {
      progressStatus.value = 'exception'
      handleFundError(error, '批量更新失败')
      batchUpdating.value = false
    }
  }

  const handleImportFile = async (files: File[]) => {
    if (!files.length) return
    importing.value = true
    try {
      const res = await currenciesApi.uploadData(collectionName.value, files[0])
      if (res.success) {
        ElMessage.success('导入成功')
        fileImportRef.value?.clearFiles()
        fileImportDialogVisible.value = false
        loadData()
      }
    } catch (error) {
      handleFundError(error, '导入失败')
    } finally {
      importing.value = false
    }
  }

  const handleRemoteSync = async (config: RemoteSyncConfig) => {
    remoteSyncing.value = true
    try {
      const res = await currenciesApi.syncData(collectionName.value, config)
      if (res.success && res.data) {
        remoteSyncStats.value = res.data
        ElMessage.success('同步成功')
        loadData()
      }
    } catch (error) {
      handleFundError(error, '同步失败')
    } finally {
      remoteSyncing.value = false
    }
  }

  const handleClearData = async () => {
    const confirmed = await handleDangerousOperation(
      `确认要清空 "${collectionInfo.value?.display_name || collectionName.value}" 集合的所有数据吗？`,
      '警告', '确认清空', '取消'
    )
    if (!confirmed) return
    clearing.value = true
    try {
      const res = await currenciesApi.clearCollectionData(collectionName.value)
      if (res.success) {
        ElMessage.success(`成功清空 ${(res.data as any)?.deleted_count || 0} 条数据`)
        await loadData()
      }
    } catch (error) {
      handleFundError(error, '清空失败')
    } finally {
      clearing.value = false
    }
  }

  const cleanup = () => {
    if (batchProgressTimer) {
      clearInterval(batchProgressTimer)
      batchProgressTimer = null
    }
  }

  return {
    collectionName, loading, items, fields, page, pageSize, total, filterField, filterValue, sortBy, sortDir,
    stats, collectionInfo, currentCollectionInfo, apiRefreshDialogVisible, fileImportDialogVisible,
    remoteSyncDialogVisible, overviewDialogVisible, updateConfig, singleUpdateParams, batchUpdateParams,
    updateMode, singleUpdating, batchUpdating, canSingleUpdate, canBatchUpdate, progressPercentage,
    progressStatus, progressMessage, currentTaskId, refreshing, importing, remoteSyncing, clearing,
    fileImportRef, remoteSyncStats, loadData, handleSortChange, exportAllData, handleUpdateCommand,
    loadUpdateConfig, handleSingleUpdate, handleBatchUpdate, pollTaskStatus, handleImportFile,
    handleRemoteSync, handleClearData, cleanup,
  }
}
