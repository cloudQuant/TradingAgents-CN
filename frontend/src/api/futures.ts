import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export const futuresApi = {
  // 获取期货概览
  async getOverview() {
    const response = await axios.get(`${API_BASE_URL}/api/futures/overview`)
    return response.data
  },

  // 获取期货集合列表
  async getCollections() {
    const response = await axios.get(`${API_BASE_URL}/api/futures/collections`)
    return response.data
  },

  // 获取集合更新配置（新）
  async getCollectionUpdateConfig(collectionName: string) {
    const response = await axios.get(
      `${API_BASE_URL}/api/futures/collections/${collectionName}/update-config`
    )
    return response.data
  },

  // 刷新集合数据（新版V2，使用FuturesRefreshService）
  async refreshCollectionV2(collectionName: string, params?: Record<string, any>) {
    const response = await axios.post(
      `${API_BASE_URL}/api/futures/collections/${collectionName}/refresh`,
      { params: params || {} }
    )
    return response.data
  },

  // 获取刷新任务状态
  async getRefreshTaskStatus(taskId: string) {
    const response = await axios.get(
      `${API_BASE_URL}/api/futures/refresh/task/${taskId}`
    )
    return response.data
  },

  // 获取支持刷新的集合列表
  async getSupportedRefreshCollections() {
    const response = await axios.get(
      `${API_BASE_URL}/api/futures/refresh/supported-collections`
    )
    return response.data
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
  ) {
    const response = await axios.get(
      `${API_BASE_URL}/api/futures/collections/${collectionName}`,
      { params }
    )
    return response.data
  },

  // 获取集合统计信息
  async getCollectionStats(collectionName: string) {
    const response = await axios.get(
      `${API_BASE_URL}/api/futures/collections/${collectionName}/stats`
    )
    return response.data
  },

  // 搜索期货
  async searchFutures(keyword: string) {
    const response = await axios.get(`${API_BASE_URL}/api/futures/search`, {
      params: { keyword }
    })
    return response.data
  },

  // 获取期货分析
  async getFuturesAnalysis(futuresCode: string) {
    const response = await axios.get(`${API_BASE_URL}/api/futures/analysis/${futuresCode}`)
    return response.data
  },

  // 更新集合数据
  async updateCollection(
    collectionName: string,
    params?: {
      symbol?: string
      market?: string
      adjust?: string
      [key: string]: any
    }
  ) {
    const response = await axios.post(
      `${API_BASE_URL}/api/futures/collections/${collectionName}/update`,
      null,
      { params }
    )
    return response.data
  },

  // 清空集合数据
  async clearCollection(collectionName: string) {
    const response = await axios.delete(
      `${API_BASE_URL}/api/futures/collections/${collectionName}`
    )
    return response.data
  },

  // 上传数据文件
  async uploadData(collectionName: string, file: File) {
    const formData = new FormData()
    formData.append('file', file)
    
    const response = await axios.post(
      `${API_BASE_URL}/api/futures/collections/${collectionName}/upload`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
    )
    return response.data
  },

  // 远程同步数据
  async syncData(collectionName: string, config: any) {
    const response = await axios.post(
      `${API_BASE_URL}/api/futures/collections/${collectionName}/sync`,
      config
    )
    return response.data
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
    const response = await axios.post(
      `${API_BASE_URL}/api/futures/collections/${collectionName}/export`,
      payload,
      {
        responseType: 'blob',
        timeout: 300000
      }
    )
    return response.data
  }
}
