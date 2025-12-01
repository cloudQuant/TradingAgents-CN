import { ApiClient, request, type ApiResponse } from './request'
import type {
  FundCollection,
  CollectionDataQuery,
  CollectionData,
  CollectionStats,
  CollectionUpdateConfig,
  RefreshCollectionRequest,
  RefreshTask,
  CollectionExportRequest,
  RemoteSyncConfig,
  SyncResult,
} from '@/types/funds'

export const fundsApi = {
  // 获取基金概览
  async getOverview(): Promise<ApiResponse<any>> {
    return await ApiClient.get('/api/funds/overview')
  },

  // 获取基金集合列表
  async getCollections(): Promise<ApiResponse<FundCollection[]>> {
    return await ApiClient.get<FundCollection[]>('/api/funds/collections')
  },

  // 获取指定集合的数据
  async getCollectionData(
    collectionName: string,
    params?: CollectionDataQuery
  ): Promise<ApiResponse<CollectionData>> {
    return await ApiClient.get<CollectionData>(`/api/funds/collections/${collectionName}`, params)
  },

  // 获取基金公司列表
  async getFundCompanies(): Promise<ApiResponse<string[]>> {
    return await ApiClient.get<string[]>('/api/funds/companies')
  },

  // 获取集合统计信息
  async getCollectionStats(collectionName: string): Promise<ApiResponse<CollectionStats>> {
    return await ApiClient.get<CollectionStats>(`/api/funds/collections/${collectionName}/stats`)
  },

  // 获取集合更新配置
  async getCollectionUpdateConfig(collectionName: string): Promise<ApiResponse<CollectionUpdateConfig>> {
    return await ApiClient.get<CollectionUpdateConfig>(`/api/funds/collections/${collectionName}/update-config`)
  },

  // 搜索基金
  async searchFunds(keyword: string): Promise<ApiResponse<any>> {
    return await ApiClient.get('/api/funds/search', { keyword })
  },

  // 获取基金分析
  async getFundAnalysis(fundCode: string): Promise<ApiResponse<any>> {
    return await ApiClient.get(`/api/funds/analysis/${fundCode}`)
  },

  // 上传数据文件
  async uploadData(collectionName: string, file: File, onProgress?: (progress: number) => void): Promise<ApiResponse<any>> {
    return await ApiClient.upload(`/api/funds/collections/${collectionName}/upload`, file, onProgress)
  },

  // 远程同步数据
  async syncData(collectionName: string, config: RemoteSyncConfig): Promise<ApiResponse<SyncResult>> {
    return await ApiClient.post<SyncResult>(`/api/funds/collections/${collectionName}/sync`, config)
  },

  // 刷新集合数据
  async refreshCollectionData(
    collectionName: string,
    params: RefreshCollectionRequest
  ): Promise<ApiResponse<{ task_id: string; message: string }>> {
    return await ApiClient.post<{ task_id: string; message: string }>(
      `/api/funds/collections/${collectionName}/refresh`,
      params
    )
  },

  // 获取刷新任务状态
  async getRefreshTaskStatus(collectionName: string, taskId: string): Promise<ApiResponse<RefreshTask>> {
    return await ApiClient.get<RefreshTask>(`/api/funds/collections/${collectionName}/refresh/status/${taskId}`)
  },

  // 导出集合全部数据
  async exportCollectionData(
    collectionName: string,
    payload: CollectionExportRequest
  ): Promise<Blob> {
    // 大数据集导出可能需要较长时间，设置 5 分钟超时
    // 使用 request 直接调用以获取 blob 响应
    const response = await request.post(
      `/api/funds/collections/${collectionName}/export`,
      payload,
      {
        responseType: 'blob',
        timeout: 300000
      }
    )
    return response as unknown as Blob
  },

  // 清空集合数据
  async clearCollectionData(collectionName: string): Promise<ApiResponse<{ deleted_count: number; message: string }>> {
    return await ApiClient.delete<{ deleted_count: number; message: string }>(
      `/api/funds/collections/${collectionName}/clear`
    )
  }
}
