import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export const cryptosApi = {
  async getOverview() {
    const response = await axios.get(`${API_BASE_URL}/api/cryptos/overview`)
    return response.data
  },
  async getCollections() {
    const response = await axios.get(`${API_BASE_URL}/api/cryptos/collections`)
    return response.data
  },
  async getCollectionData(collectionName: string, params?: any) {
    const response = await axios.get(`${API_BASE_URL}/api/cryptos/collections/${collectionName}`, { params })
    return response.data
  },
  async searchCryptos(keyword: string) {
    const response = await axios.get(`${API_BASE_URL}/api/cryptos/search`, { params: { keyword } })
    return response.data
  },
  async getCryptoAnalysis(cryptoSymbol: string) {
    const response = await axios.get(`${API_BASE_URL}/api/cryptos/analysis/${cryptoSymbol}`)
    return response.data
  }
}
