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
  }
}
