/**
 * 基金模块 TypeScript 类型定义
 * 提供完整的类型安全支持
 */

// ==================== 基础类型 ====================

export type SortDirection = 'asc' | 'desc'

export type FileFormat = 'csv' | 'xlsx' | 'json'

export type UpdateType = 'single' | 'batch'

export type TaskStatus = 'pending' | 'running' | 'success' | 'failed' | 'completed'

// ==================== 集合相关 ====================

export interface FundCollection {
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
  tracking_target?: string
  tracking_method?: string
  fund_company?: string
}

export interface CollectionData {
  items: Record<string, any>[]
  total: number
  page: number
  page_size: number
  fields: FieldDefinition[]
}

// ==================== 统计相关 ====================

export interface TypeStat {
  type: string
  count: number
}

export interface StatusStat {
  status: string
  count: number
}

export interface TopItem {
  name?: string
  code?: string
  rate?: number
  amount?: number
}

export interface MarketCapStat {
  range: string
  count: number
}

export interface CollectionStats {
  total_count: number
  latest_date?: string
  latest_time?: string
  type_stats?: TypeStat[]
  rise_count?: number
  fall_count?: number
  flat_count?: number
  purchase_status_stats?: StatusStat[]
  redeem_status_stats?: StatusStat[]
  top_gainers?: TopItem[]
  top_losers?: TopItem[]
  top_volume?: TopItem[]
  market_cap_stats?: MarketCapStat[]
}

// ==================== 更新相关 ====================

export interface UpdateParam {
  name: string
  label: string
  type: 'text' | 'number' | 'select'
  placeholder?: string
  required?: boolean
  default?: any
  options?: Array<{ label: string; value: any }>
  min?: number
  max?: number
  step?: number
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
  update_type: UpdateType
  fund_code?: string
  symbol?: string
  year?: number
  date?: string
  period?: string
  adjust?: string
  concurrency?: number
  limit?: number
  start_year?: number
  end_year?: number
  delay?: number
  [key: string]: any
}

// ==================== 任务相关 ====================

export interface TaskResult {
  saved?: number
  inserted?: number
  updated?: number
  deleted?: number
  // 批量任务统计字段（后端可选返回）
  processed?: number
  success?: number
  failed?: number
  fetched_rows?: number
  saved_rows?: number
  saved_fund_count?: number
}

export interface RefreshTask {
  task_id: string
  status: TaskStatus
  progress?: number
  total?: number
  message?: string
  error?: string
  result?: TaskResult
}

// ==================== 导出相关 ====================

export interface CollectionExportRequest {
  file_format: FileFormat
  filter_field?: string
  filter_value?: string
  sort_by?: string
  sort_dir?: SortDirection
  tracking_target?: string
  tracking_method?: string
  fund_company?: string
}

// ==================== API 响应 ====================

export interface ApiResponse<T = any> {
  success: boolean
  data?: T
  error?: string
  detail?: any
  timestamp?: string
}

export interface CollectionListResponse extends ApiResponse<FundCollection[]> {}

export interface CollectionDataResponse extends ApiResponse<CollectionData> {}

export interface CollectionStatsResponse extends ApiResponse<CollectionStats> {}

export interface RefreshTaskResponse extends ApiResponse<{ task_id: string; message: string }> {}

export interface ClearCollectionResponse extends ApiResponse<{ deleted_count: number; message: string }> {}

// ==================== 远程同步 ====================

export interface RemoteSyncConfig {
  host: string
  username?: string
  password?: string
  authSource?: string
  collection?: string
  batchSize?: number
}

export interface SyncResult {
  inserted: number
  updated: number
  failed: number
  message: string
}
