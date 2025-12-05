import { ApiClient, request, type ApiResponse } from './request'

export const currenciesApi = {
  async getOverview(): Promise<ApiResponse<any>> {
    return ApiClient.get('/api/currencies/overview')
  },
  async getConfig(): Promise<ApiResponse<{ default_api_key: string }>> {
    return ApiClient.get('/api/currencies/config')
  },
  async getCollections(): Promise<ApiResponse<Array<{
    name: string
    display_name: string
    description: string
    route: string
    fields: string[]
  }>>> {
    return ApiClient.get('/api/currencies/collections')
  },
  async getCollectionData(collectionName: string, params?: any): Promise<ApiResponse<any>> {
    // Generic endpoint if implemented, or specific ones
    if (collectionName === 'currency_latest') {
      return this.getCurrencyLatestList(params)
    }
    if (collectionName === 'currency_history') {
      return this.getCurrencyHistoryList(params)
    }
    if (collectionName === 'currency_time_series') {
      return this.getCurrencyTimeSeriesList(params)
    }
    if (collectionName === 'currency_currencies') {
      return this.getCurrencyCurrenciesList(params)
    }
    if (collectionName === 'currency_convert') {
      return this.getCollectionDataUnified(collectionName, params)
    }
    return ApiClient.get(`/api/currencies/collections/${collectionName}`, params)
  },
  async searchCurrencies(keyword: string): Promise<ApiResponse<any>> {
    return ApiClient.get('/api/currencies/search', { keyword })
  },
  async getCurrencyAnalysis(currencyPair: string): Promise<ApiResponse<any>> {
    return ApiClient.get(`/api/currencies/analysis/${currencyPair}`)
  },
  
  // Currency Latest Specific
  async getCurrencyLatestList(params?: any): Promise<ApiResponse<any>> {
    return ApiClient.get('/api/currencies/latest/list', params)
  },
  async uploadCurrencyLatest(file: File): Promise<ApiResponse<any>> {
    const formData = new FormData()
    formData.append('file', file)
    return ApiClient.post('/api/currencies/latest/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
  async syncCurrencyLatest(params: { base?: string, symbols?: string, api_key: string }): Promise<ApiResponse<any>> {
    return ApiClient.post('/api/currencies/latest/sync', undefined, { params })
  },
  async batchSyncCurrencyLatest(params: { api_key: string }): Promise<ApiResponse<any>> {
    return ApiClient.post('/api/currencies/latest/batch-sync', undefined, { params })
  },
  async updateCurrencyLatest(params: { code: string, base?: string, api_key: string }): Promise<ApiResponse<any>> {
    return ApiClient.post('/api/currencies/latest/update', undefined, { params })
  },
  async clearCurrencyLatest(): Promise<ApiResponse<any>> {
    return ApiClient.delete('/api/currencies/latest/clear')
  },
  async remoteSyncCurrencyLatest(params: { remote_host: string, remote_collection: string, remote_username?: string, remote_password?: string, remote_auth_source?: string, batch_size?: number }): Promise<ApiResponse<any>> {
    return ApiClient.post('/api/currencies/latest/remote-sync', params)
  },
  
  // Currency History Specific
  async getCurrencyHistoryList(params?: any): Promise<ApiResponse<any>> {
    return ApiClient.get('/api/currencies/history/list', params)
  },
  async uploadCurrencyHistory(file: File): Promise<ApiResponse<any>> {
    const formData = new FormData()
    formData.append('file', file)
    return ApiClient.post('/api/currencies/history/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
  async syncCurrencyHistory(params: { base?: string, date: string, symbols?: string, api_key: string }): Promise<ApiResponse<any>> {
    return ApiClient.post('/api/currencies/history/sync', undefined, { params })
  },
   async batchSyncCurrencyHistory(params: { base?: string, date: string, api_key: string, max_codes?: number, batch_size?: number }): Promise<ApiResponse<any>> {
    return ApiClient.post('/api/currencies/history/batch-sync', undefined, { params })
  },
  async clearCurrencyHistory(): Promise<ApiResponse<any>> {
    return ApiClient.delete('/api/currencies/history/clear')
  },
  async remoteSyncCurrencyHistory(params: { remote_host: string, remote_collection: string, remote_username?: string, remote_password?: string, remote_auth_source?: string, batch_size?: number }): Promise<ApiResponse<any>> {
    return ApiClient.post('/api/currencies/history/remote-sync', params)
  },
  
  // Currency Time Series Specific
  async getCurrencyTimeSeriesList(params?: any): Promise<ApiResponse<any>> {
    return ApiClient.get('/api/currencies/timeseries/list', params)
  },
  async uploadCurrencyTimeSeries(file: File): Promise<ApiResponse<any>> {
    const formData = new FormData()
    formData.append('file', file)
    return ApiClient.post('/api/currencies/timeseries/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
  async syncCurrencyTimeSeries(params: { base?: string, start_date: string, end_date: string, symbols?: string, api_key: string }): Promise<ApiResponse<any>> {
    return ApiClient.post('/api/currencies/timeseries/sync', undefined, { params })
  },
  async batchSyncCurrencyTimeSeries(params: { base?: string, start_date: string, end_date: string, api_key: string, max_codes?: number, batch_size?: number }): Promise<ApiResponse<any>> {
    return ApiClient.post('/api/currencies/timeseries/batch-sync', undefined, { params })
  },
  async clearCurrencyTimeSeries(): Promise<ApiResponse<any>> {
    return ApiClient.delete('/api/currencies/timeseries/clear')
  },
  async remoteSyncCurrencyTimeSeries(params: { remote_host: string, remote_collection: string, remote_username?: string, remote_password?: string, remote_auth_source?: string, batch_size?: number }): Promise<ApiResponse<any>> {
    return ApiClient.post('/api/currencies/timeseries/remote-sync', params)
  },

  // Currency Currencies Specific
  async getCurrencyCurrenciesList(params?: any): Promise<ApiResponse<any>> {
    return ApiClient.get('/api/currencies/currencies/list', params)
  },
  async uploadCurrencyCurrencies(file: File): Promise<ApiResponse<any>> {
    const formData = new FormData()
    formData.append('file', file)
    return ApiClient.post('/api/currencies/currencies/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
  async syncCurrencyCurrencies(params: { c_type?: string, api_key: string, code?: string }): Promise<ApiResponse<any>> {
    return ApiClient.post('/api/currencies/currencies/sync', undefined, { params })
  },
  async clearCurrencyCurrencies(): Promise<ApiResponse<any>> {
    return ApiClient.delete('/api/currencies/currencies/clear')
  },
  async remoteSyncCurrencyCurrencies(params: { remote_host: string, remote_collection: string, remote_username?: string, remote_password?: string, remote_auth_source?: string, batch_size?: number }): Promise<ApiResponse<any>> {
    return ApiClient.post('/api/currencies/currencies/remote-sync', params)
  },

  // Currency Convert Tool
  async convertCurrencyTool(params: { base: string, to: string, amount: string, api_key: string }): Promise<ApiResponse<any>> {
    return ApiClient.get('/api/currencies/tool/convert', params)
  },

  // ============== 统一刷新 API ==============
  
  // 获取集合更新配置
  async getCollectionUpdateConfig(collectionName: string): Promise<ApiResponse<any>> {
    return ApiClient.get(`/api/currencies/collections/${collectionName}/update-config`)
  },

  // 刷新集合数据（统一接口）
  async refreshCollectionData(collectionName: string, params?: any): Promise<ApiResponse<any>> {
    return ApiClient.post(`/api/currencies/collections/${collectionName}/refresh`, params || {})
  },

  // 获取刷新任务状态
  async getRefreshTaskStatus(collectionName: string, taskId: string): Promise<ApiResponse<any>> {
    return ApiClient.get(`/api/currencies/collections/${collectionName}/refresh/status/${taskId}`)
  },

  // 获取集合数据（统一接口）
  async getCollectionDataUnified(collectionName: string, params?: { page?: number, page_size?: number }): Promise<ApiResponse<any>> {
    return ApiClient.get(`/api/currencies/collections/${collectionName}/data`, params)
  },

  // 获取集合概览（统一接口）
  async getCollectionOverview(collectionName: string): Promise<ApiResponse<any>> {
    return ApiClient.get(`/api/currencies/collections/${collectionName}/overview`)
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
      `/api/currencies/collections/${collectionName}/export`,
      payload,
      {
        responseType: 'blob',
        timeout: 300000
      }
    )
    return response as unknown as Blob
  },

  // 获取集合统计信息
  async getCollectionStats(collectionName: string): Promise<ApiResponse<any>> {
    return ApiClient.get(`/api/currencies/collections/${collectionName}/stats`)
  },

  // 上传数据文件
  async uploadData(collectionName: string, file: File): Promise<ApiResponse<any>> {
    const formData = new FormData()
    formData.append('file', file)
    return ApiClient.post(`/api/currencies/collections/${collectionName}/upload`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },

  // 远程同步数据
  async syncData(collectionName: string, config: any): Promise<ApiResponse<any>> {
    return ApiClient.post(`/api/currencies/collections/${collectionName}/sync`, config)
  },

  // 清空集合数据
  async clearCollectionData(collectionName: string): Promise<ApiResponse<any>> {
    return ApiClient.delete(`/api/currencies/collections/${collectionName}`)
  }
}
