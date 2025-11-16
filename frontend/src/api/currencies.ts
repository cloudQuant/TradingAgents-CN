import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export const currenciesApi = {
  async getOverview() {
    const response = await axios.get(`${API_BASE_URL}/api/currencies/overview`)
    return response.data
  },
  async getCollections() {
    const response = await axios.get(`${API_BASE_URL}/api/currencies/collections`)
    return response.data
  },
  async getCollectionData(collectionName: string, params?: any) {
    const response = await axios.get(`${API_BASE_URL}/api/currencies/collections/${collectionName}`, { params })
    return response.data
  },
  async searchCurrencies(keyword: string) {
    const response = await axios.get(`${API_BASE_URL}/api/currencies/search`, { params: { keyword } })
    return response.data
  },
  async getCurrencyAnalysis(currencyPair: string) {
    const response = await axios.get(`${API_BASE_URL}/api/currencies/analysis/${currencyPair}`)
    return response.data
  }
}
