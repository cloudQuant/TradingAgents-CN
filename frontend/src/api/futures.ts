import { ApiClient, request, type ApiResponse } from './request'
import type {
  FuturesCollection,
  CollectionDataQuery,
  CollectionData,
  CollectionStats,
  CollectionUpdateConfig,
  RefreshCollectionRequest,
  RefreshTask,
  CollectionExportRequest,
  RemoteSyncConfig,
  SyncResult,
} from '@/types/futures'

export const futuresApi = {
  // 获取期货概览
  async getOverview(): Promise<ApiResponse<any>> {
    return await ApiClient.get('/api/futures/overview')
  },

  // 获取期货集合列表
  async getCollections(): Promise<ApiResponse<FuturesCollection[]>> {
    return await ApiClient.get<FuturesCollection[]>('/api/futures/collections')
  },

  // 获取集合更新配置
  async getCollectionUpdateConfig(collectionName: string): Promise<ApiResponse<CollectionUpdateConfig>> {
    return await ApiClient.get<CollectionUpdateConfig>(
      `/api/futures/collections/${collectionName}/update-config`
    )
  },

  // 刷新集合数据
  async refreshCollectionData(
    collectionName: string,
    params?: RefreshCollectionRequest
  ): Promise<ApiResponse<{ task_id: string; message: string }>> {
    return await ApiClient.post<{ task_id: string; message: string }>(
      `/api/futures/collections/${collectionName}/refresh`,
      params || {}
    )
  },

  // 兼容旧版V2方法名
  async refreshCollectionV2(collectionName: string, params?: Record<string, any>) {
    return this.refreshCollectionData(collectionName, { params })
  },

  // 获取刷新任务状态
  async getRefreshTaskStatus(taskId: string): Promise<ApiResponse<RefreshTask>> {
    return await ApiClient.get<RefreshTask>(
      `/api/futures/refresh/task/${taskId}`
    )
  },

  // 获取支持刷新的集合列表
  async getSupportedRefreshCollections(): Promise<ApiResponse<string[]>> {
    return await ApiClient.get<string[]>(
      '/api/futures/refresh/supported-collections'
    )
  },

  // 获取指定集合的数据
  async getCollectionData(
    collectionName: string,
    params?: CollectionDataQuery
  ): Promise<ApiResponse<CollectionData>> {
    return await ApiClient.get<CollectionData>(
      `/api/futures/collections/${collectionName}`,
      params
    )
  },

  // 获取集合统计信息
  async getCollectionStats(collectionName: string): Promise<ApiResponse<CollectionStats>> {
    return await ApiClient.get<CollectionStats>(
      `/api/futures/collections/${collectionName}/stats`
    )
  },

  // 搜索期货
  async searchFutures(keyword: string): Promise<ApiResponse<any>> {
    return await ApiClient.get('/api/futures/search', { keyword })
  },

  // 获取期货分析
  async getFuturesAnalysis(futuresCode: string): Promise<ApiResponse<any>> {
    return await ApiClient.get(`/api/futures/analysis/${futuresCode}`)
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
  ): Promise<ApiResponse<any>> {
    return await ApiClient.post(
      `/api/futures/collections/${collectionName}/update`,
      null,
      { params }
    )
  },

  // 清空集合数据
  async clearCollection(collectionName: string): Promise<ApiResponse<{ deleted_count: number; message: string }>> {
    return await ApiClient.delete<{ deleted_count: number; message: string }>(
      `/api/futures/collections/${collectionName}`
    )
  },

  // 上传数据文件
  async uploadData(
    collectionName: string,
    file: File,
    onProgress?: (progress: number) => void
  ): Promise<ApiResponse<any>> {
    return await ApiClient.upload(
      `/api/futures/collections/${collectionName}/upload`,
      file,
      onProgress
    )
  },

  // 远程同步数据
  async syncData(collectionName: string, config: RemoteSyncConfig): Promise<ApiResponse<SyncResult>> {
    return await ApiClient.post<SyncResult>(
      `/api/futures/collections/${collectionName}/sync`,
      config
    )
  },

  // 导出集合全部数据
  async exportCollectionData(
    collectionName: string,
    payload: CollectionExportRequest
  ): Promise<Blob> {
    const response = await request.post(
      `/api/futures/collections/${collectionName}/export`,
      payload,
      {
        responseType: 'blob',
        timeout: 300000
      }
    )
    return response as unknown as Blob
  }
}
