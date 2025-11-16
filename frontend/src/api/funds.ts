import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export const fundsApi = {
  // 获取基金概览
  async getOverview() {
    const response = await axios.get(`${API_BASE_URL}/api/funds/overview`)
    return response.data
  },

  // 获取基金集合列表
  async getCollections() {
    const response = await axios.get(`${API_BASE_URL}/api/funds/collections`)
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
      `${API_BASE_URL}/api/funds/collections/${collectionName}`,
      { params }
    )
    return response.data
  },

  // 获取集合统计信息
  async getCollectionStats(collectionName: string) {
    const response = await axios.get(
      `${API_BASE_URL}/api/funds/collections/${collectionName}/stats`
    )
    return response.data
  },

  // 搜索基金
  async searchFunds(keyword: string) {
    const response = await axios.get(`${API_BASE_URL}/api/funds/search`, {
      params: { keyword }
    })
    return response.data
  },

  // 获取基金分析
  async getFundAnalysis(fundCode: string) {
    const response = await axios.get(`${API_BASE_URL}/api/funds/analysis/${fundCode}`)
    return response.data
  }
}
