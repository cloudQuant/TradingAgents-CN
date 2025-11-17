import { ApiClient, type ApiResponse } from './request'

export const fundsApi = {
  // 获取基金概览
  async getOverview(): Promise<ApiResponse<any>> {
    return await ApiClient.get('/api/funds/overview')
  },

  // 获取基金集合列表
  async getCollections(): Promise<ApiResponse<any>> {
    return await ApiClient.get('/api/funds/collections')
  },

  // 获取指定集合的数据
  async getCollectionData(
    collectionName: string,
    params?: {
      page?: number
      page_size?: number
      sort_by?: string
      sort_dir?: string
      filter_field?: string
      filter_value?: string
    }
  ): Promise<ApiResponse<any>> {
    return await ApiClient.get(`/api/funds/collections/${collectionName}`, params)
  },

  // 获取集合统计信息
  async getCollectionStats(collectionName: string): Promise<ApiResponse<any>> {
    return await ApiClient.get(`/api/funds/collections/${collectionName}/stats`)
  },

  // 搜索基金
  async searchFunds(keyword: string): Promise<ApiResponse<any>> {
    return await ApiClient.get('/api/funds/search', { keyword })
  },

  // 获取基金分析
  async getFundAnalysis(fundCode: string): Promise<ApiResponse<any>> {
    return await ApiClient.get(`/api/funds/analysis/${fundCode}`)
  },

  // 刷新集合数据
  async refreshCollectionData(collectionName: string, params?: any): Promise<ApiResponse<any>> {
    return await ApiClient.post(`/api/funds/collections/${collectionName}/refresh`, params || {})
  },

  // 获取刷新任务状态
  async getRefreshTaskStatus(collectionName: string, taskId: string): Promise<ApiResponse<any>> {
    return await ApiClient.get(`/api/funds/collections/${collectionName}/refresh/status/${taskId}`)
  },

  // 清空集合数据
  async clearCollectionData(collectionName: string): Promise<ApiResponse<any>> {
    return await ApiClient.delete(`/api/funds/collections/${collectionName}/clear`)
  }
}
