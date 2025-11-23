import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export const optionsApi = {
  // 获取期权概览
  async getOverview() {
    const response = await axios.get(`${API_BASE_URL}/api/options/overview`)
    return response.data
  },

  // 获取期权集合列表
  async getCollections() {
    const response = await axios.get(`${API_BASE_URL}/api/options/collections`)
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
      `${API_BASE_URL}/api/options/collections/${collectionName}`,
      { params }
    )
    return response.data
  },

  // 获取集合统计信息
  async getCollectionStats(collectionName: string) {
    const response = await axios.get(
      `${API_BASE_URL}/api/options/collections/${collectionName}/stats`
    )
    return response.data
  },

  // 刷新集合数据
  async refreshCollection(collectionName: string) {
    const response = await axios.post(
      `${API_BASE_URL}/api/options/collections/${collectionName}/refresh`
    )
    return response.data
  },

  // 清空集合数据
  async clearCollection(collectionName: string) {
    const response = await axios.post(
      `${API_BASE_URL}/api/options/collections/${collectionName}/clear`
    )
    return response.data
  },

  // 搜索期权
  async searchOptions(keyword: string) {
    const response = await axios.get(`${API_BASE_URL}/api/options/search`, {
      params: { keyword }
    })
    return response.data
  },

  // 获取期权分析
  async getOptionAnalysis(optionCode: string) {
    const response = await axios.get(`${API_BASE_URL}/api/options/analysis/${optionCode}`)
    return response.data
  }
}
