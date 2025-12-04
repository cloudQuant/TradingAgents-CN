/**
 * 期货模块 TypeScript 类型定义
 * 提供完整的类型安全支持
 */

// ==================== 基础类型 ====================

export type SortDirection = 'asc' | 'desc'

export type FileFormat = 'csv' | 'xlsx' | 'json'

export type UpdateType = 'single' | 'batch'

export type TaskStatus = 'pending' | 'running' | 'success' | 'failed' | 'completed'

// ==================== 集合相关 ====================

export interface FuturesCollection {
  name: string
  display_name: string
  description: string
  route: string
  fields: string[]
}

export interface FieldDefinition {
  name: string
  type: string
  example: string | null
}

export interface CollectionDataQuery {
  page?: number
  page_size?: number
  sort_by?: string
  sort_dir?: SortDirection
  filter_field?: string
  filter_value?: string
}

export interface CollectionData {
  items: Record<string, any>[]
  total: number
  page: number
  page_size: number
  fields: FieldDefinition[]
}

// ==================== 统计相关 ====================

export interface ExchangeStat {
  exchange: string
  count: number
}

export interface TypeStat {
  type: string
  count: number
}

export interface CollectionStats {
  total_count: number
  collection_name?: string
  earliest_date?: string
  latest_date?: string
  date_field?: string
  exchange_stats?: ExchangeStat[]
  type_stats?: TypeStat[]
}

// ==================== 更新相关 ====================

export interface UpdateParam {
  name: string
  label: string
  type: 'text' | 'number' | 'select' | 'date'
  placeholder?: string
  required?: boolean
  default?: any
  options?: Array<{ label: string; value: any }>
}

export interface UpdateConfig {
  enabled: boolean
  description?: string
  params?: UpdateParam[]
}

export interface CollectionUpdateConfig {
  collection_name: string
  display_name: string
  update_description?: string
  single_update: UpdateConfig
  batch_update: UpdateConfig
}

export interface RefreshCollectionRequest {
  update_type?: UpdateType
  params?: Record<string, any>
  symbol?: string
  market?: string
  adjust?: string
  date?: string
  [key: string]: any
}

// ==================== 任务相关 ====================

export interface TaskResult {
  saved?: number
  inserted?: number
  updated?: number
  deleted?: number
  rows?: number
  processed?: number
  success?: number
  failed?: number
}

export interface RefreshTask {
  task_id: string
  task_type?: string
  description?: string
  status: TaskStatus
  progress?: number
  total?: number
  message?: string
  created_at?: string
  started_at?: string | null
  completed_at?: string | null
  result?: any
  error?: string | null
}

// ==================== 导出相关 ====================

export interface CollectionExportRequest {
  file_format: FileFormat
  filter_field?: string
  filter_value?: string
  sort_by?: string
  sort_dir?: SortDirection
}

// ==================== API 响应 ====================

export interface ApiResponse<T = any> {
  success: boolean
  data?: T
  error?: string
  detail?: any
  timestamp?: string
}

// ==================== 远程同步 ====================

export interface RemoteSyncConfig {
  host?: string
  remote_host?: string
  username?: string
  password?: string
  authSource?: string
  auth_source?: string
  collection?: string
  remote_collection?: string
  batchSize?: number
  batch_size?: number
}

export interface SyncResult {
  inserted: number
  updated: number
  failed: number
  message: string
}
