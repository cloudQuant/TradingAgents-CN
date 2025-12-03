/**
 * 多数据源同步相关API
 */
import { ApiClient } from './request'

// 数据源状态接口
export interface DataSourceStatus {
  name: string
  priority: number
  available: boolean
  description: string
  token_source?: 'database' | 'env'  // Token 来源（仅 Tushare）
}

// 同步状态接口
export interface SyncStatus {
  job: string
  status: 'idle' | 'running' | 'success' | 'success_with_errors' | 'failed' | 'never_run'
  started_at?: string
  finished_at?: string
  total: number
  inserted: number
  updated: number
  errors: number
  last_trade_date?: string
  data_sources_used: string[]
  source_stats?: Record<string, Record<string, number>>
  message?: string
}

// 同步请求参数
export interface SyncRequest {
  force?: boolean
  preferred_sources?: string[]
}

// API响应格式
export interface ApiResponse<T = any> {
  success: boolean
  message?: string
  error?: string
  data: T
}

// 基础测试结果接口
export interface BaseTestResult {
  success: boolean
  message: string
  count?: number
  date?: string
}

// 测试结果接口（简化版）
export interface DataSourceTestResult {
  name: string
  priority: number
  available: boolean
  message: string
  token_source?: 'database' | 'env'  // Token 来源（仅 Tushare）
}

// 使用建议接口
export interface SyncRecommendations {
  primary_source?: {
    name: string
    priority: number
    reason: string
  }
  fallback_sources: Array<{
    name: string
    priority: number
  }>
  suggestions: string[]
  warnings: string[]
}

/**
 * 获取数据源状态
 */
export const getDataSourcesStatus = (): Promise<ApiResponse<DataSourceStatus[]>> => {
  return ApiClient.get('/api/sync/multi-source/sources/status')
}

/**
 * 获取当前正在使用的数据源
 */
export const getCurrentDataSource = (): Promise<ApiResponse<{
  name: string
  priority: number
  description: string
  token_source?: 'database' | 'env'
  token_source_display?: string
}>> => {
  return ApiClient.get('/api/sync/multi-source/sources/current')
}

/**
 * 获取同步状态
 */
export const getSyncStatus = (): Promise<ApiResponse<SyncStatus>> => {
  return ApiClient.get('/api/sync/multi-source/status')
}

/**
 * 运行股票基础信息同步
 */
export const runStockBasicsSync = (params?: {
  force?: boolean
  preferred_sources?: string
}): Promise<ApiResponse<SyncStatus>> => {
  const queryParams = new URLSearchParams()
  if (params?.force) {
    queryParams.append('force', 'true')
  }
  if (params?.preferred_sources) {
    queryParams.append('preferred_sources', params.preferred_sources)
  }

  const url = `/api/sync/multi-source/stock_basics/run${queryParams.toString() ? '?' + queryParams.toString() : ''}`
  return ApiClient.post(url, undefined, {
    timeout: 600000 // 🔥 同步操作需要更长时间，设置为10分钟（BaoStock需要逐个获取估值数据）
  })
}

/**
 * 测试数据源连接
 * @param sourceName - 可选，指定要测试的数据源名称。如果不指定，则测试所有数据源
 */
export const testDataSources = (sourceName?: string): Promise<ApiResponse<{ test_results: DataSourceTestResult[] }>> => {
  const params = sourceName ? { source_name: sourceName } : {}
  return ApiClient.post('/api/sync/multi-source/test-sources', params, {
    timeout: 15000 // 单个数据源测试超时15秒，多个数据源最多30秒
  })
}

/**
 * 获取同步建议
 */
export const getSyncRecommendations = (): Promise<ApiResponse<SyncRecommendations>> => {
  return ApiClient.get('/api/sync/multi-source/recommendations')
}

/**
 * 获取同步历史记录
 */
export const getSyncHistory = (params?: {
  page?: number
  page_size?: number
  status?: string
}): Promise<ApiResponse<{
  records: SyncStatus[]
  total: number
  page: number
  page_size: number
  has_more: boolean
}>> => {
  const queryParams = new URLSearchParams()
  if (params?.page) {
    queryParams.append('page', params.page.toString())
  }
  if (params?.page_size) {
    queryParams.append('page_size', params.page_size.toString())
  }
  if (params?.status) {
    queryParams.append('status', params.status)
  }

  const url = `/api/sync/multi-source/history${queryParams.toString() ? '?' + queryParams.toString() : ''}`
  return ApiClient.get(url)
}

/**
 * 清空同步缓存
 */
export const clearSyncCache = (): Promise<ApiResponse<{ cleared: boolean }>> => {
  return ApiClient.delete('/api/sync/multi-source/cache')
}

// 传统单一数据源同步API（保持兼容性）
export const runSingleSourceSync = (): Promise<ApiResponse<any>> => {
  return ApiClient.post('/api/sync/stock_basics/run')
}

export const getSingleSourceSyncStatus = (): Promise<ApiResponse<any>> => {
  return ApiClient.get('/api/sync/stock_basics/status')
}


// ==================== 数据集合同步 API ====================

// 同步节点接口
export interface SyncNode {
  _id?: string
  node_id: string
  name: string
  url: string
  api_key?: string
  api_key_masked?: string
  description?: string
  tags?: string[]
  status: 'active' | 'inactive'
  last_sync_at?: string
  created_at?: string
  updated_at?: string
}

// 同步任务接口
export interface SyncTask {
  _id?: string
  task_id: string
  direction: 'push' | 'pull'
  source_node: string
  target_node: string
  collection: string
  filter?: Record<string, any>
  strategy: 'full' | 'incremental'
  status: 'pending' | 'running' | 'completed' | 'failed'
  stats: {
    total_records: number
    transferred: number
    inserted: number
    updated: number
    failed: number
  }
  started_at?: string
  completed_at?: string
  error_message?: string
}

// 可同步集合信息
export interface SyncableCollection {
  name: string
  count: number
  unique_keys: string[]
  incremental_field?: string
  chunk_size: number
}

// 节点连接测试结果
export interface NodeTestResult {
  success: boolean
  latency_ms?: number
  version?: string
  node_name?: string
  error?: string
}

/**
 * 获取所有同步节点
 */
export const getSyncNodes = (): Promise<ApiResponse<SyncNode[]>> => {
  return ApiClient.get('/api/sync/nodes')
}

/**
 * 获取单个同步节点
 */
export const getSyncNode = (nodeId: string): Promise<ApiResponse<SyncNode>> => {
  return ApiClient.get(`/api/sync/nodes/${nodeId}`)
}

/**
 * 创建同步节点
 */
export const createSyncNode = (node: Partial<SyncNode>): Promise<ApiResponse<SyncNode>> => {
  return ApiClient.post('/api/sync/nodes', node)
}

/**
 * 更新同步节点
 */
export const updateSyncNode = (nodeId: string, node: Partial<SyncNode>): Promise<ApiResponse<SyncNode>> => {
  return ApiClient.put(`/api/sync/nodes/${nodeId}`, node)
}

/**
 * 删除同步节点
 */
export const deleteSyncNode = (nodeId: string): Promise<ApiResponse<{ message: string }>> => {
  return ApiClient.delete(`/api/sync/nodes/${nodeId}`)
}

/**
 * 测试节点连接
 */
export const testSyncNode = (nodeId: string): Promise<ApiResponse<NodeTestResult>> => {
  return ApiClient.post(`/api/sync/nodes/${nodeId}/test`)
}

/**
 * 获取同步任务列表
 */
export const getSyncTasks = (params?: {
  limit?: number
  skip?: number
}): Promise<ApiResponse<SyncTask[]>> => {
  const queryParams = new URLSearchParams()
  if (params?.limit) queryParams.append('limit', params.limit.toString())
  if (params?.skip) queryParams.append('skip', params.skip.toString())
  const url = `/api/sync/tasks${queryParams.toString() ? '?' + queryParams.toString() : ''}`
  return ApiClient.get(url)
}

/**
 * 获取单个同步任务状态
 */
export const getSyncTask = (taskId: string): Promise<ApiResponse<SyncTask>> => {
  return ApiClient.get(`/api/sync/tasks/${taskId}`)
}

/**
 * 从远程节点拉取数据
 */
export const pullData = (params: {
  source_node: string
  collection: string
  strategy?: 'full' | 'incremental'
  filter?: Record<string, any>
}): Promise<ApiResponse<SyncTask>> => {
  return ApiClient.post('/api/sync/pull', params)
}

/**
 * 推送数据到远程节点
 */
export const pushData = (params: {
  target_node: string
  collection: string
  strategy?: 'full' | 'incremental'
  filter?: Record<string, any>
}): Promise<ApiResponse<SyncTask>> => {
  return ApiClient.post('/api/sync/push', params)
}

/**
 * 获取可同步的集合列表
 */
export const getSyncableCollections = (): Promise<ApiResponse<SyncableCollection[]>> => {
  return ApiClient.get('/api/sync/collections')
}
