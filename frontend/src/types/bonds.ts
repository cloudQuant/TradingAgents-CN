/**
 * 债券模块 TypeScript 类型定义
 * 提供完整的类型安全支持
 */

// ==================== 基础类型 ====================

export type SortDirection = 'asc' | 'desc'

export type FileFormat = 'csv' | 'xlsx' | 'json'

export type UpdateType = 'single' | 'batch'

export type TaskStatus = 'pending' | 'running' | 'success' | 'failed' | 'completed'

// ==================== 集合相关 ====================

export interface BondCollection {
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

export interface CategoryStat {
  category: string
  count: number
}

export interface ExchangeStat {
  exchange: string
  count: number
}

export interface BondTypeStat {
  type: string
  count: number
}

export interface GradeStat {
  grade: string
  count: number
}

export interface CollectionStats {
  total_count: number
  collection_name: string
  earliest_date?: string
  latest_date?: string
  date_field?: string
  category_stats?: CategoryStat[]
  exchange_stats?: ExchangeStat[]
  bond_type_stats?: BondTypeStat[]
  grade_stats?: GradeStat[]
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
  start_date?: string
  end_date?: string
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
  task_type: string
  description: string
  status: TaskStatus
  progress: number
  total: number
  message: string
  created_at: string
  started_at: string | null
  completed_at: string | null
  result: any
  error: string | null
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
  remote_host: string
  db_type?: string
  batch_size?: number
  remote_collection?: string
  remote_username?: string
  remote_password?: string
  remote_auth_source?: string
}

export interface SyncResult {
  collection_name: string
  synced: number
  remote_total: number
  batch_size: number
  message: string
}

// ==================== 债券实体 ====================

export interface BondItem {
  code: string
  name?: string
  exchange?: string
  category?: 'convertible' | 'exchangeable' | 'interest' | 'credit' | 'other'
  maturity_date?: string
  type?: string
  [key: string]: any
}

// ==================== 可转债相关 ====================

export interface ConvertibleBond {
  code: string
  name: string
  price?: number
  change_pct?: number
  stock_code: string
  stock_name: string
  stock_price?: number
  stock_change_pct?: number
  convert_price?: number
  convert_value?: number
  convert_premium_rate?: number
  pure_debt_premium_rate?: number
  put_trigger_price?: number
  redeem_trigger_price?: number
  maturity_redeem_price?: number
  pure_debt_value?: number
  start_convert_date?: string
  list_date?: string
  apply_date?: string
  timestamp?: string
}

export interface ConvertibleValueAnalysis {
  date: string
  close_price?: number
  pure_debt_value?: number
  convert_value?: number
  pure_debt_premium_rate?: number
  convert_premium_rate?: number
}
