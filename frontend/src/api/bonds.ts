import { ApiClient, type ApiResponse } from './request'

export interface BondItem {
  code: string
  name?: string
  exchange?: string
  category?: 'convertible' | 'exchangeable' | 'interest' | 'credit' | 'other'
  maturity_date?: string
  type?: string
  [key: string]: any
}

export const bondsApi = {
  async list(params?: { q?: string; limit?: number; category?: string; exchange?: string; only_not_matured?: boolean; page?: number; page_size?: number; sort_by?: string; sort_dir?: 'asc' | 'desc' }): Promise<ApiResponse<{ total: number; items: BondItem[]; page?: number; page_size?: number }>> {
    return ApiClient.get('/api/bonds/list', params)
  },

  async getInfo(code: string): Promise<ApiResponse<any>> {
    return ApiClient.get(`/api/bonds/${encodeURIComponent(code)}/info`)
  },

  async getHistory(code: string, start: string, end: string, period: string = 'daily'): Promise<ApiResponse<{ data: string }>> {
    return ApiClient.get(`/api/bonds/${encodeURIComponent(code)}/history`, { start, end, period })
  },

  async syncHistory(code: string, start: string, end: string): Promise<ApiResponse<{ saved: number; rows: number }>> {
    return ApiClient.post(`/api/bonds/${encodeURIComponent(code)}/history/sync`, undefined, { params: { start, end } })
  },

  async getYieldCurve(
    start?: string,
    end?: string,
    curveName?: string,
    format: 'json' | 'text' = 'json'
  ): Promise<ApiResponse<{
    records?: Array<{
      date: string
      tenor: string
      yield: number
      curve_name?: string
      yield_type?: string
    }>
    chart_data?: Record<string, Record<string, Record<string, number>>>
    statistics?: {
      total_records: number
      curve_names: string[]
      tenors: string[]
      date_range: {
        start: string | null
        end: string | null
        count: number
      }
    }
    data?: string
  }>> {
    return ApiClient.get('/api/bonds/yield-curve', { start, end, curve_name: curveName, format })
  },

  async syncYieldCurve(start?: string, end?: string): Promise<ApiResponse<{ saved: number; rows: number }>> {
    return ApiClient.post('/api/bonds/yield-curve/sync', undefined, { params: { start, end } })
  },

  async getCollections(): Promise<ApiResponse<Array<{
    name: string
    display_name: string
    description: string
    route: string
    fields: string[]
  }>>> {
    return ApiClient.get('/api/bonds/collections')
  },

  async getCollectionData(
    collectionName: string,
    params?: {
      page?: number
      page_size?: number
      sort_by?: string
      sort_dir?: 'asc' | 'desc'
      filter_field?: string
      filter_value?: string
    }
  ): Promise<ApiResponse<{
    items: any[]
    total: number
    page: number
    page_size: number
    fields: Array<{ name: string; type: string; example: string | null }>
  }>> {
    return ApiClient.get(`/api/bonds/collections/${encodeURIComponent(collectionName)}`, params)
  },

  async getCollectionStats(collectionName: string): Promise<ApiResponse<{
    total_count: number
    collection_name: string
    earliest_date?: string
    latest_date?: string
    date_field?: string
    category_stats?: Array<{ category: string; count: number }>
    exchange_stats?: Array<{ exchange: string; count: number }>
  }>> {
    return ApiClient.get(`/api/bonds/collections/${encodeURIComponent(collectionName)}/stats`)
  },

  async getBondInfoIssuanceYearly(): Promise<ApiResponse<{
    items: Array<{ year: string; count: number }>;
    total_years: number
  }>> {
    return ApiClient.get('/api/bonds/collections/bond_info_cm/issuance/yearly')
  },

  // 债券分析相关API
  async startAnalysis(request: {
    bond_code: string
    parameters?: {
      bond_type?: string
      analysis_date?: string
      research_depth?: string
      selected_dimensions?: string[]
    }
  }): Promise<ApiResponse<{ task_id: string }>> {
    return ApiClient.post('/api/bonds/analysis', request)
  },

  async getAnalysisStatus(taskId: string): Promise<ApiResponse<{
    status: 'pending' | 'running' | 'completed' | 'failed'
    progress: number
    current_step: string
    error?: string
  }>> {
    return ApiClient.get(`/api/bonds/analysis/${encodeURIComponent(taskId)}/status`)
  },

  async getAnalysisResult(taskId: string): Promise<ApiResponse<{
    bond_code: string
    bond_name: string
    bond_type: string
    current_price: number
    price_change_percent: number
    maturity_date?: string
    summary: string
    fundamental_analysis?: string
    technical_analysis?: string
    valuation_analysis?: string
    convertible_analysis?: string
    risk_assessment?: string
    recommendation: string
  }>> {
    return ApiClient.get(`/api/bonds/analysis/${encodeURIComponent(taskId)}/result`)
  },

  // 刷新集合数据（返回task_id）
  async refreshCollectionData(
    collectionName: string,
    params?: {
      start_date?: string
      end_date?: string
      date?: string
    }
  ): Promise<ApiResponse<{
    task_id: string
    message: string
  }>> {
    const response = await ApiClient.post(`/api/bonds/collections/${encodeURIComponent(collectionName)}/refresh`, undefined, { params })
    return response
  },

  // 查询刷新任务状态
  async getRefreshTaskStatus(taskId: string): Promise<ApiResponse<{
    task_id: string
    task_type: string
    description: string
    status: string
    progress: number
    total: number
    message: string
    created_at: string
    started_at: string | null
    completed_at: string | null
    result: any
    error: string | null
  }>> {
    return ApiClient.get(`/api/bonds/collections/refresh/task/${taskId}`)
  },

  async importCollectionData(
    collectionName: string,
    file: File
  ): Promise<ApiResponse<{
    collection_name: string
    saved: number
    rows: number
    message: string
  }>> {
    const formData = new FormData()
    formData.append('file', file)

    return ApiClient.post(
      `/api/bonds/collections/${encodeURIComponent(collectionName)}/import`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
    )
  },

  async syncCollectionFromRemote(
    collectionName: string,
    params: {
      remote_host: string
      db_type?: string
      batch_size?: number
      remote_collection?: string
      remote_username?: string
      remote_password?: string
    }
  ): Promise<ApiResponse<{
    collection_name: string
    synced: number
    remote_total: number
    batch_size: number
    message: string
  }>> {
    const payload: any = {
      db_type: params.db_type || 'mongodb',
      remote_host: params.remote_host,
      batch_size: params.batch_size ?? 5000,
    }

    if (params.remote_collection) {
      payload.remote_collection = params.remote_collection
    }
    if (params.remote_username) {
      payload.remote_username = params.remote_username
    }
    if (params.remote_password) {
      payload.remote_password = params.remote_password
    }

    return ApiClient.post(
      `/api/bonds/collections/${encodeURIComponent(collectionName)}/sync-remote`,
      undefined,
      { params: payload }
    )
  },

  // ==================== 可转债专项功能 ====================

  /**
   * 获取可转债比价表
   */
  async getConvertibleComparison(params?: {
    page?: number
    page_size?: number
    sort_by?: string
    sort_dir?: 'asc' | 'desc'
    min_premium?: number
    max_premium?: number
  }): Promise<ApiResponse<{
    total: number
    page: number
    page_size: number
    items: Array<{
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
    }>
  }>> {
    return ApiClient.get('/api/bonds/convertible/comparison', params)
  },

  /**
   * 同步可转债比价数据
   */
  async syncConvertibleComparison(): Promise<ApiResponse<{
    saved: number
    total: number
    message: string
  }>> {
    return ApiClient.post('/api/bonds/convertible/comparison/sync')
  },

  /**
   * 获取可转债价值分析历史数据
   */
  async getConvertibleValueAnalysis(
    code: string,
    params?: {
      start_date?: string
      end_date?: string
    }
  ): Promise<ApiResponse<{
    code: string
    data: Array<{
      date: string
      close_price?: number
      pure_debt_value?: number
      convert_value?: number
      pure_debt_premium_rate?: number
      convert_premium_rate?: number
    }>
  }>> {
    return ApiClient.get(`/api/bonds/convertible/${encodeURIComponent(code)}/value-analysis`, params)
  },

  /**
   * 同步指定可转债的价值分析数据
   */
  async syncConvertibleValueAnalysis(code: string): Promise<ApiResponse<{
    saved: number
    total: number
    message: string
  }>> {
    return ApiClient.post(`/api/bonds/convertible/${encodeURIComponent(code)}/value-analysis/sync`)
  },

  /**
   * 获取现券市场成交行情
   */
  async getSpotDeals(): Promise<ApiResponse<{
    total: number
    items: Array<any>
  }>> {
    return ApiClient.get('/api/bonds/market/spot-deals')
  },

  /**
   * 获取现券市场做市报价
   */
  async getSpotQuotes(): Promise<ApiResponse<{
    total: number
    items: Array<any>
  }>> {
    return ApiClient.get('/api/bonds/market/spot-quotes')
  },

  /**
   * 清空集合数据
   */
  async clearCollectionData(collectionName: string): Promise<ApiResponse<{
    deleted_count: number
    collection_name: string
    message: string
  }>> {
    return ApiClient.delete(`/api/bonds/collections/${encodeURIComponent(collectionName)}/clear`)
  }
}
