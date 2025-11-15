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
  }
}
