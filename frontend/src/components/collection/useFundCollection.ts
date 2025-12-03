/**
 * 基金集合通用逻辑 Composable
 * 提供数据加载、更新、导出等通用功能
 */
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { fundsApi } from '@/api/funds'
import { handleFundError, handleDangerousOperation } from '@/utils/fundErrorHandler'
import type {
  RemoteSyncConfig,
  CollectionDataQuery,
  CollectionStats,
  FundCollection,
  FieldDefinition,
  RefreshCollectionRequest,
  CollectionExportRequest,
} from '@/types/funds'

export function useFundCollection() {
  const route = useRoute()
  const collectionName = computed(() => route.params.collectionName as string)

  // 数据状态
  const loading = ref(false)
  const items = ref<Record<string, any>[]>([])
  const fields = ref<FieldDefinition[]>([])
  const page = ref(1)
  const pageSize = ref(50)
  const total = ref(0)

  // 过滤条件
  const filterField = ref('')
  const filterValue = ref('')

  // 排序条件
  const sortBy = ref('')
  const sortDir = ref<'asc' | 'desc'>('desc')

  // 统计数据
  const stats = ref<CollectionStats | null>(null)
  const collectionInfo = ref<FundCollection | null>(null)

  // 更新数据相关
  const apiRefreshDialogVisible = ref(false)
  const fileImportDialogVisible = ref(false)
  const remoteSyncDialogVisible = ref(false)
  const refreshing = ref(false)
  const currentTaskId = ref('')
  const progressPercentage = ref(0)
  const progressStatus = ref<'success' | 'exception' | 'warning' | ''>('')
  const progressMessage = ref('')
  let batchProgressTimer: ReturnType<typeof setInterval> | null = null

  // 更新配置
  const updateConfig = ref<any>(null)
  const singleUpdateParams = ref<Record<string, any>>({})
  const batchUpdateParams = ref<Record<string, any>>({})
  const updateMode = ref<string>('incremental') // 更新方式：incremental（增量更新）或 full（全量更新）
  const singleUpdating = ref(false)
  const batchUpdating = ref(false)

  // 文件导入相关
  const fileImportRef = ref()
  const importing = ref(false)

  // 远程同步相关
  const remoteSyncing = ref(false)
  const remoteSyncStats = ref<any>(null)

  // 清空数据相关
  const clearing = ref(false)

  // 数据概览对话框
  const overviewDialogVisible = ref(false)

  // 集合固定信息
  const collectionStaticInfo: Record<string, any> = {}
  const currentCollectionInfo = computed(() => {
    return collectionStaticInfo[collectionName.value] || {
      name: collectionName.value,
      displayName: collectionInfo.value?.display_name || collectionName.value,
      fieldCount: fields.value.length,
      dataSource: '暂无'
    }
  })

  // 加载数据
  const loadData = async (extraParams: Partial<CollectionDataQuery> = {}) => {
    loading.value = true
    try {
      const collectionsRes = await fundsApi.getCollections()
      if (collectionsRes.success && collectionsRes.data) {
        collectionInfo.value = collectionsRes.data.find(c => c.name === collectionName.value) || null
      }

      const statsRes = await fundsApi.getCollectionStats(collectionName.value)
      if (statsRes.success && statsRes.data) {
        stats.value = statsRes.data
      }

      const dataRes = await fundsApi.getCollectionData(collectionName.value, {
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
        
        // 对于 fund_hk_hist_em 集合，直接使用后端返回的字段顺序
        // 后端已经按照 provider 的 field_info 顺序排列了字段
        if (collectionName.value === 'fund_hk_hist_em') {
          fields.value = allFields
        } else {
          // 其他集合保持原有逻辑
          const metaFields = ['code', 'endpoint', 'source', 'updated_at']
          const mainFields = allFields.filter(f => !metaFields.includes(f.name))
          const metaFieldsData = allFields.filter(f => metaFields.includes(f.name))
          fields.value = [...mainFields, ...metaFieldsData]
        }
        
        total.value = dataRes.data.total || 0
      } else {
        const msg = (dataRes as any)?.message || (dataRes as any)?.error || '加载数据失败'
        handleFundError(new Error(msg))
      }
    } catch (error) {
      console.error('加载数据失败:', error)
      handleFundError(error, '加载数据失败')
    } finally {
      loading.value = false
    }
  }

  // 排序处理
  const handleSortChange = ({ prop, order }: any) => {
    if (!order) {
      sortBy.value = ''
      sortDir.value = 'desc'
    } else {
      sortBy.value = prop
      sortDir.value = order === 'ascending' ? 'asc' : 'desc'
    }
    loadData()
  }

  // 导出数据
  const exportAllData = async (
    { fileName, format }: { fileName: string; format: 'csv' | 'xlsx' | 'json' },
    extraParams: Partial<CollectionExportRequest> = {}
  ) => {
    try {
      const payload: CollectionExportRequest = {
        file_format: format,
        sort_by: sortBy.value || undefined,
        sort_dir: sortDir.value,
        filter_field: filterField.value || undefined,
        filter_value: filterValue.value || undefined,
        ...extraParams,
      }

      const blob = await fundsApi.exportCollectionData(collectionName.value, payload)
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `${fileName}.${format === 'xlsx' ? 'xlsx' : format}`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      URL.revokeObjectURL(url)
    } catch (error) {
      console.error('导出全部数据失败:', error)
      handleFundError(error, '导出失败')
      throw error
    }
  }

  // 处理下拉菜单命令
  const handleUpdateCommand = (command: string) => {
    progressPercentage.value = 0
    progressStatus.value = ''
    progressMessage.value = ''

    // 与共享页头组件保持一致：
    // - 'api'  -> API 更新
    // - 'file' -> 文件导入
    // - 'sync' -> 远程同步（历史上曾用 'remote'，这里同时兼容）
    switch (command) {
      case 'api':
        apiRefreshDialogVisible.value = true
        break
      case 'file':
        fileImportDialogVisible.value = true
        break
      case 'sync':
      case 'remote':
        remoteSyncDialogVisible.value = true
        break
    }
  }

  // 加载更新配置
  const loadUpdateConfig = async () => {
    try {
      updateConfig.value = null
      singleUpdateParams.value = {}
      batchUpdateParams.value = {}
      
      const res = await fundsApi.getCollectionUpdateConfig(collectionName.value)
      if (res.success && res.data) {
        updateConfig.value = res.data
        
        if (res.data.single_update?.params) {
          for (const param of res.data.single_update.params) {
            if (param.default !== undefined) {
              singleUpdateParams.value[param.name] = param.default
            }
          }
        }
        
        if (res.data.batch_update?.params) {
          for (const param of res.data.batch_update.params) {
            if (param.default !== undefined) {
              batchUpdateParams.value[param.name] = param.default
            }
          }
        }
      }
    } catch (error: any) {
      console.error('加载更新配置失败:', error)
      ElMessage.error('加载更新配置失败')
    }
  }

  // 计算是否可以更新
  const canSingleUpdate = computed(() => {
    if (!updateConfig.value?.single_update?.enabled) return false
    const params = updateConfig.value.single_update.params || []
    for (const param of params) {
      if (param.required && !singleUpdateParams.value[param.name]) {
        return false
      }
    }
    return true
  })

  const canBatchUpdate = computed(() => {
    if (!updateConfig.value?.batch_update?.enabled) return false
    const params = updateConfig.value.batch_update.params || []
    for (const param of params) {
      if (param.required && !batchUpdateParams.value[param.name]) {
        return false
      }
    }
    return true
  })

  // 处理单条更新
  const handleSingleUpdate = async () => {
    if (!canSingleUpdate.value) return
    if (singleUpdating.value) return // 防止重复点击
    if (batchUpdating.value) return // 如果批量更新正在进行，不允许单条更新
    if (batchProgressTimer) return // 如果轮询正在进行，不允许新的更新
    
    singleUpdating.value = true
    progressPercentage.value = 0
    progressMessage.value = '正在执行单条更新...'
    
    try {
      // 处理参数，确保 year 等数字字段正确转换
      const processedParams: any = {
        update_type: 'single',
      }
      
      // 复制参数并转换类型
      for (const [key, value] of Object.entries(singleUpdateParams.value)) {
        if (value !== undefined && value !== null && value !== '') {
          // 如果是 year 字段，尝试转换为数字
          if (key === 'year' && typeof value === 'string') {
            const numValue = parseInt(value, 10)
            if (!isNaN(numValue)) {
              processedParams[key] = numValue
            } else {
              processedParams[key] = value
            }
          } else {
            processedParams[key] = value
          }
        }
      }
      
      const res = await fundsApi.refreshCollectionData(collectionName.value, processedParams)
      
      if (res.success && res.data) {
        // 检查是否有 task_id，如果有则启动轮询
        if (res.data.task_id) {
          currentTaskId.value = res.data.task_id
          progressMessage.value = '任务已创建，正在更新数据...'
          // 启动轮询（复用批量更新的轮询逻辑）
          pollBatchTaskStatus()
        } else {
          // 没有 task_id，直接完成
          progressPercentage.value = 100
          progressStatus.value = 'success'
          progressMessage.value = res.data.message || '单条更新完成'
          ElMessage.success('单条更新成功')
          await loadData()
          singleUpdating.value = false
        }
      } else {
        const msg = (res as any)?.message || (res as any)?.error || '更新失败'
        progressStatus.value = 'exception'
        progressMessage.value = msg
        handleFundError(new Error(msg || '单条更新失败'))
        singleUpdating.value = false
      }
    } catch (error) {
      progressStatus.value = 'exception'
      progressMessage.value = error instanceof Error ? error.message : '更新失败'
      handleFundError(error, '单条更新失败')
      singleUpdating.value = false
    }
  }

  // 轮询批量更新任务状态
  const pollBatchTaskStatus = async () => {
    // 如果已经有轮询在运行，先清除它
    if (batchProgressTimer) {
      clearInterval(batchProgressTimer)
      batchProgressTimer = null
    }
    
    let pollCount = 0
    const maxPollCount = 1800
    
    batchProgressTimer = setInterval(async () => {
      try {
        pollCount++
        
        if (pollCount > maxPollCount) {
          if (batchProgressTimer) {
            clearInterval(batchProgressTimer)
            batchProgressTimer = null
          }
          progressStatus.value = 'warning'
          progressMessage.value = '任务超时，请刷新页面查看结果'
          ElMessage.warning('任务执行时间过长，请刷新页面查看结果')
          batchUpdating.value = false
          return
        }
        
        const res = await fundsApi.getRefreshTaskStatus(collectionName.value, currentTaskId.value)
        
        if (res.success && res.data) {
          const task = res.data
          
          if (task.progress !== undefined && task.total !== undefined) {
            progressPercentage.value = Math.round((task.progress / task.total) * 100)
          }
          
          // 构建进度消息，包含获取和保存的行数
          let progressMsg = task.message || '正在批量更新...'
          if (task.result) {
            const parts: string[] = []
            
            // 处理任务数
            if (task.result.processed !== undefined) {
              parts.push(`已处理 ${task.result.processed} 个任务`)
            }
            
            // 成功和失败数
            if (task.result.success !== undefined) {
              parts.push(`成功 ${task.result.success} 个`)
            }
            if (task.result.failed !== undefined && task.result.failed > 0) {
              parts.push(`失败 ${task.result.failed} 个`)
            }
            
            // 获取的行数
            if (task.result.fetched_rows !== undefined && task.result.fetched_rows > 0) {
              parts.push(`获取 ${task.result.fetched_rows.toLocaleString()} 行数据`)
            }
            
            // 保存的行数
            if (task.result.saved_rows !== undefined && task.result.saved_rows > 0) {
              parts.push(`保存 ${task.result.saved_rows.toLocaleString()} 行数据`)
            }
            
            // 已保存的基金数量
            if (task.result.saved_fund_count !== undefined && task.result.saved_fund_count > 0) {
              parts.push(`已保存 ${task.result.saved_fund_count} 个基金`)
            }
            
            if (parts.length > 0) {
              progressMsg = parts.join('，')
            }
          }
          progressMessage.value = progressMsg
          
          if (task.status === 'success' || task.status === 'completed') {
            // 立即停止轮询，防止重复处理
            if (batchProgressTimer) {
              clearInterval(batchProgressTimer)
              batchProgressTimer = null
            }
            
            progressStatus.value = 'success'
            progressPercentage.value = 100
            
            // 构建完成消息
            let message = task.message || '更新完成'
            if (task.result) {
              const parts: string[] = []
              
              // 处理任务数（批量更新才有）
              if (task.result.processed !== undefined) {
                parts.push(`处理 ${task.result.processed} 个任务`)
              }
              
              // 成功和失败数（批量更新才有）
              if (task.result.success !== undefined) {
                parts.push(`成功 ${task.result.success} 个`)
              }
              if (task.result.failed !== undefined && task.result.failed > 0) {
                parts.push(`失败 ${task.result.failed} 个`)
              }
              
              // 获取的行数
              if (task.result.fetched_rows !== undefined && task.result.fetched_rows > 0) {
                parts.push(`获取 ${task.result.fetched_rows.toLocaleString()} 行数据`)
              }
              
              // 保存的行数
              if (task.result.saved_rows !== undefined && task.result.saved_rows > 0) {
                parts.push(`保存 ${task.result.saved_rows.toLocaleString()} 行数据`)
              }
              
              // 插入/更新的记录数
              if (task.result.inserted !== undefined) {
                parts.push(`保存 ${task.result.inserted.toLocaleString()} 条记录（新增+更新）`)
              }
              
              // 单条更新的保存数量
              if (task.result.saved !== undefined && task.result.saved > 0) {
                parts.push(`保存 ${task.result.saved} 条数据`)
              }
              
              // 已保存的基金数量
              if (task.result.saved_fund_count !== undefined && task.result.saved_fund_count > 0) {
                parts.push(`已保存 ${task.result.saved_fund_count} 个基金`)
              }
              
              if (parts.length > 0) {
                message = parts.join('，')
              } else {
                message = task.message || '更新完成'
              }
            }
            
            progressMessage.value = message
            
            // 先重置状态，防止在 loadData 期间再次触发更新
            batchUpdating.value = false
            singleUpdating.value = false
            
            await loadData()
            
            ElMessage.success(message)
            
          } else if (task.status === 'failed') {
            progressStatus.value = 'exception'
            progressMessage.value = task.error || task.message || '更新失败'
            ElMessage.error(task.error || '更新失败')
            
            if (batchProgressTimer) {
              clearInterval(batchProgressTimer)
              batchProgressTimer = null
            }
            // 同时重置单条更新和批量更新的状态
            batchUpdating.value = false
            singleUpdating.value = false
          }
        }
      } catch (e: any) {
        console.error('轮询批量更新状态失败:', e)
        if (pollCount > 5) {
          if (batchProgressTimer) {
            clearInterval(batchProgressTimer)
            batchProgressTimer = null
          }
          progressStatus.value = 'exception'
          progressMessage.value = '查询任务状态失败'
          // 同时重置单条更新和批量更新的状态
          batchUpdating.value = false
          singleUpdating.value = false
        }
      }
    }, 1000)
  }

  // 处理批量更新
  const handleBatchUpdate = async () => {
    if (!canBatchUpdate.value) return
    
    batchUpdating.value = true
    progressPercentage.value = 0
    progressStatus.value = ''
    progressMessage.value = '正在创建批量更新任务...'
    
    try {
      const params: RefreshCollectionRequest = {
        update_type: 'batch',
        update_mode: updateMode.value,
        ...batchUpdateParams.value
      }
      const res = await fundsApi.refreshCollectionData(collectionName.value, params)
      
      if (res.success && res.data) {
        if (res.data.task_id) {
          currentTaskId.value = res.data.task_id
          progressMessage.value = '任务已创建，正在批量更新数据...'
          pollBatchTaskStatus()
        } else {
          progressPercentage.value = 100
          progressStatus.value = 'success'
          progressMessage.value = res.data.message || '批量更新完成'
          ElMessage.success('批量更新成功')
          await loadData()
          batchUpdating.value = false
        }
      } else {
        const msg = (res as any)?.message || (res as any)?.error || '更新失败'
        progressStatus.value = 'exception'
        progressMessage.value = msg
        handleFundError(new Error(msg || '批量更新失败'))
        batchUpdating.value = false
      }
    } catch (error) {
      progressStatus.value = 'exception'
      progressMessage.value = error instanceof Error ? error.message : '更新失败'
      handleFundError(error, '批量更新失败')
      batchUpdating.value = false
    }
  }

  // 文件导入处理
  const handleImportFile = async (files: File[]) => {
    if (!files.length) return
    
    importing.value = true
    
    try {
      const res = await fundsApi.uploadData(collectionName.value, files[0])
      
      if (res.success && res.data) {
        ElMessage.success(res.data.message || '导入成功')
        fileImportRef.value?.clearFiles()
        fileImportDialogVisible.value = false
        loadData()
      } else {
        const msg = (res as any)?.message || (res as any)?.error || '导入失败'
        handleFundError(new Error(msg))
      }
    } catch (error) {
      handleFundError(error, '导入失败')
    } finally {
      importing.value = false
    }
  }

  // 远程同步处理
  const handleRemoteSync = async (config: RemoteSyncConfig) => {
    remoteSyncing.value = true
    remoteSyncStats.value = null

    try {
      const res = await fundsApi.syncData(collectionName.value, {
        host: config.host,
        username: config.username,
        password: config.password,
        authSource: config.authSource,
        collection: config.collection || collectionName.value,
        batchSize: config.batchSize
      })

      if (res.success && res.data) {
        remoteSyncStats.value = res.data
        ElMessage.success(res.data.message || '同步成功')
        loadData()
      } else {
        const msg = (res as any)?.message || (res as any)?.error || '同步失败'
        handleFundError(new Error(msg))
      }
    } catch (error) {
      handleFundError(error, '同步失败')
    } finally {
      remoteSyncing.value = false
    }
  }

  // 处理清空数据
  const handleClearData = async () => {
    const confirmed = await handleDangerousOperation(
      `确认要清空 "${collectionInfo.value?.display_name || collectionName.value}" 集合的所有数据吗？此操作不可恢复！`,
      '警告',
      '确认清空',
      '取消'
    )
    
    if (!confirmed) return
    
    clearing.value = true
    try {
      const res = await fundsApi.clearCollectionData(collectionName.value)
      if (res.success && res.data) {
        ElMessage.success(`成功清空 ${res.data.deleted_count || 0} 条数据`)
        await loadData()
      } else {
        const msg = (res as any)?.message || (res as any)?.error || '清空数据失败'
        handleFundError(new Error(msg))
      }
    } catch (error) {
      handleFundError(error, '清空数据失败')
    } finally {
      clearing.value = false
    }
  }

  // 清理函数
  const cleanup = () => {
    if (batchProgressTimer) {
      clearInterval(batchProgressTimer)
      batchProgressTimer = null
    }
  }

  return {
    // 状态
    collectionName,
    loading,
    items,
    fields,
    page,
    pageSize,
    total,
    filterField,
    filterValue,
    sortBy,
    sortDir,
    stats,
    collectionInfo,
    currentCollectionInfo,
    
    // 对话框状态
    apiRefreshDialogVisible,
    fileImportDialogVisible,
    remoteSyncDialogVisible,
    overviewDialogVisible,
    
    // 更新相关
    updateConfig,
    singleUpdateParams,
    batchUpdateParams,
    updateMode,
    singleUpdating,
    batchUpdating,
    canSingleUpdate,
    canBatchUpdate,
    progressPercentage,
    progressStatus,
    progressMessage,
    currentTaskId,
    
    // 其他状态
    refreshing,
    importing,
    remoteSyncing,
    clearing,
    fileImportRef,
    remoteSyncStats,
    
    // 方法
    loadData,
    handleSortChange,
    exportAllData,
    handleUpdateCommand,
    loadUpdateConfig,
    handleSingleUpdate,
    handleBatchUpdate,
    pollBatchTaskStatus,
    handleImportFile,
    handleRemoteSync,
    handleClearData,
    cleanup,
  }
}
