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

  async getYieldCurve(start?: string, end?: string): Promise<ApiResponse<{ data: string }>> {
    return ApiClient.get('/api/bonds/yield-curve', { start, end })
  },

  async syncYieldCurve(start?: string, end?: string): Promise<ApiResponse<{ saved: number; rows: number }>> {
    return ApiClient.post('/api/bonds/yield-curve/sync', undefined, { params: { start, end } })
  }
}
