import { ApiClient, request, type ApiResponse } from './request'
import type {
  OptionsCollection,
  CollectionDataQuery,
  CollectionData,
  CollectionStats,
  CollectionUpdateConfig,
  RefreshCollectionRequest,
  RefreshTask,
  CollectionExportRequest,
  RemoteSyncConfig,
  SyncResult,
} from '@/types/options'

export const optionsApi = {
  // 获取期权概览
  async getOverview(): Promise<ApiResponse<any>> {
    return await ApiClient.get('/api/options/overview')
  },

  // 获取期权集合列表
  async getCollections(): Promise<ApiResponse<OptionsCollection[]>> {
    return await ApiClient.get<OptionsCollection[]>('/api/options/collections')
  },

  // 获取指定集合的数据
  async getCollectionData(
    collectionName: string,
    params?: CollectionDataQuery
  ): Promise<ApiResponse<CollectionData>> {
    return await ApiClient.get<CollectionData>(`/api/options/collections/${collectionName}`, params)
  },

  // 获取集合统计信息
  async getCollectionStats(collectionName: string): Promise<ApiResponse<CollectionStats>> {
    return await ApiClient.get<CollectionStats>(`/api/options/collections/${collectionName}/stats`)
  },

  // 获取集合更新配置
  async getCollectionUpdateConfig(collectionName: string): Promise<ApiResponse<CollectionUpdateConfig>> {
    return await ApiClient.get<CollectionUpdateConfig>(
      `/api/options/collections/${collectionName}/update-config`
    )
  },

  // 刷新集合数据
  async refreshCollectionData(
    collectionName: string,
    params?: RefreshCollectionRequest
  ): Promise<ApiResponse<{ task_id: string; message: string }>> {
    return await ApiClient.post<{ task_id: string; message: string }>(
      `/api/options/collections/${collectionName}/refresh`,
      params || {}
    )
  },

  // 兼容旧版方法名
  async refreshCollection(collectionName: string, payload?: any): Promise<ApiResponse<any>> {
    return this.refreshCollectionData(collectionName, payload)
  },

  // 获取刷新任务状态
  async getRefreshTaskStatus(collectionName: string, taskId: string): Promise<ApiResponse<RefreshTask>> {
    return await ApiClient.get<RefreshTask>(
      `/api/options/collections/${collectionName}/refresh/status/${taskId}`
    )
  },

  // 清空集合数据
  async clearCollection(collectionName: string): Promise<ApiResponse<{ deleted_count: number; message: string }>> {
    // 后端为 POST /clear，因此这里仍然使用 POST
    return await ApiClient.post<{ deleted_count: number; message: string }>(
      `/api/options/collections/${collectionName}/clear`,
      {}
    )
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
  async syncData(collectionName: string, config: RemoteSyncConfig): Promise<ApiResponse<SyncResult>> {
    return await ApiClient.post<SyncResult>(`/api/options/collections/${collectionName}/sync`, config)
  },

  // 导出集合全部数据
  async exportCollectionData(
    collectionName: string,
    payload: CollectionExportRequest
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
