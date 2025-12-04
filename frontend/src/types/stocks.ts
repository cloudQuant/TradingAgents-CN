/**
 * 股票模块类型定义
 *
 * 与后端 app/schemas/stocks.py 对应
 */

// ==================== 集合相关类型 ====================

/**
 * 股票数据集合
 */
export interface StockCollection {
  name: string
  display_name: string
  description: string
  route: string
  fields: string[]
  category?: string
  order?: number
}

/**
 * 字段定义
 */
export interface FieldDefinition {
  name: string
  type: string
  description?: string
  example?: any
}

/**
 * 集合数据查询参数
 */
export interface CollectionDataQuery {
  page?: number
  page_size?: number
  sort_by?: string
  sort_dir?: 'asc' | 'desc'
  filter_field?: string
  filter_value?: string
}

/**
 * 集合数据响应
 */
export interface CollectionData {
  items: Record<string, any>[]
  total: number
  page: number
  page_size: number
  fields: FieldDefinition[]
}

/**
 * 集合统计信息
 */
export interface CollectionStats {
  total_count: number
  collection_name?: string
  latest_date?: string
  latest_time?: string
  earliest_date?: string
  rise_count?: number
  fall_count?: number
  flat_count?: number
}

// ==================== 更新配置类型 ====================

/**
 * 更新参数定义
 */
export interface UpdateParam {
  name: string
  label: string
  type: 'text' | 'number' | 'select' | 'date'
  placeholder?: string
  required?: boolean
  default?: any
  options?: Array<{ label: string; value: any }>
  min?: number
  max?: number
  step?: number
}

/**
 * 更新配置
 */
export interface UpdateConfig {
  enabled: boolean
  description: string
  params: UpdateParam[]
}

/**
 * 集合更新配置
 */
export interface CollectionUpdateConfig {
  collection_name: string
  display_name: string
  update_description?: string
  single_update: UpdateConfig
  batch_update: UpdateConfig
}

// ==================== 任务相关类型 ====================

/**
 * 任务状态枚举
 */
export type TaskStatus = 'pending' | 'running' | 'success' | 'failed' | 'completed'

/**
 * 任务结果
 */
export interface TaskResult {
  saved?: number
  inserted?: number
  updated?: number
  deleted?: number
  fetched_rows?: number
  processed?: number
  success?: number
  failed?: number
}

/**
 * 刷新任务
 */
export interface RefreshTask {
  task_id: string
  status: TaskStatus
  progress?: number
  total?: number
  message?: string
  error?: string
  result?: TaskResult
}

/**
 * 刷新请求
 */
export interface RefreshCollectionRequest {
  update_type?: 'single' | 'batch'
  update_mode?: 'incremental' | 'full'
  symbol?: string
  date?: string
  start_date?: string
  end_date?: string
  period?: string
  adjust?: string
  concurrency?: number
  limit?: number
  [key: string]: any
}

// ==================== 导出相关类型 ====================

/**
 * 导出请求
 */
export interface CollectionExportRequest {
  file_format?: 'csv' | 'xlsx' | 'json'
  filter_field?: string
  filter_value?: string
  sort_by?: string
  sort_dir?: 'asc' | 'desc'
}

// ==================== 同步相关类型 ====================

/**
 * 远程同步配置
 */
export interface RemoteSyncConfig {
  host: string
  username?: string
  password?: string
  auth_source?: string
  collection?: string
  batch_size?: number
  // 兼容snake_case
  authSource?: string
  batchSize?: number
}

/**
 * 同步结果
 */
export interface SyncResult {
  inserted: number
  updated: number
  failed: number
  message: string
}
