import { ApiClient, request, type ApiResponse } from './request'

export const optionsApi = {
  // 获取期权概览
  async getOverview(): Promise<ApiResponse<any>> {
    return await ApiClient.get('/api/options/overview')
  },

  // 获取期权集合列表
  async getCollections(): Promise<ApiResponse<any>> {
    return await ApiClient.get('/api/options/collections')
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
    return await ApiClient.get(`/api/options/collections/${collectionName}`, params)
  },

  // 获取集合统计信息
  async getCollectionStats(collectionName: string): Promise<ApiResponse<any>> {
    return await ApiClient.get(`/api/options/collections/${collectionName}/stats`)
  },

  // 刷新集合数据
  async refreshCollection(collectionName: string, payload?: any): Promise<ApiResponse<any>> {
    return await ApiClient.post(`/api/options/collections/${collectionName}/refresh`, payload || {})
  },

  // 清空集合数据
  async clearCollection(collectionName: string): Promise<ApiResponse<any>> {
    // 后端为 POST /clear，因此这里仍然使用 POST
    return await ApiClient.post(`/api/options/collections/${collectionName}/clear`, {})
  },

  // 搜索期权
  async searchOptions(keyword: string): Promise<ApiResponse<any>> {
    return await ApiClient.get('/api/options/search', { keyword })
  },

  // 获取期权分析
  async getOptionAnalysis(optionCode: string): Promise<ApiResponse<any>> {
    return await ApiClient.get(`/api/options/analysis/${optionCode}`)
  },

  // 上传数据文件
  async uploadData(
    collectionName: string,
    file: File,
    onProgress?: (progress: number) => void
  ): Promise<ApiResponse<any>> {
    return await ApiClient.upload(`/api/options/collections/${collectionName}/upload`, file, onProgress)
  },

  // 远程同步数据
  async syncData(collectionName: string, config: any): Promise<ApiResponse<any>> {
    return await ApiClient.post(`/api/options/collections/${collectionName}/sync`, config)
  },

  // 导出集合全部数据
  async exportCollectionData(
    collectionName: string,
    payload: {
      file_format: 'csv' | 'xlsx' | 'json'
      filter_field?: string
      filter_value?: string
      sort_by?: string
      sort_dir?: 'asc' | 'desc'
    }
  ): Promise<Blob> {
    const response = await request.post(
      `/api/options/collections/${collectionName}/export`,
      payload,
      {
        responseType: 'blob',
        timeout: 300000
      }
    )
    return response as unknown as Blob
  }
}
