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

// 复用 funds 的类型定义，因为结构相同
export type IndexCollection = FundCollection

export const indexsApi = {
    // 获取指数概览
    async getOverview(): Promise<ApiResponse<any>> {
        return await ApiClient.get('/api/indexs/overview')
    },

    // 获取指数集合列表
    async getCollections(): Promise<ApiResponse<IndexCollection[]>> {
        return await ApiClient.get<IndexCollection[]>('/api/indexs/collections')
    },

    // 获取指定集合的数据
    async getCollectionData(
        collectionName: string,
        params?: CollectionDataQuery
    ): Promise<ApiResponse<CollectionData>> {
        return await ApiClient.get<CollectionData>(`/api/indexs/collections/${collectionName}`, params)
    },

    // 获取集合统计信息
    async getCollectionStats(collectionName: string): Promise<ApiResponse<CollectionStats>> {
        return await ApiClient.get<CollectionStats>(`/api/indexs/collections/${collectionName}/stats`)
    },

    // 获取集合更新配置
    async getCollectionUpdateConfig(collectionName: string): Promise<ApiResponse<CollectionUpdateConfig>> {
        return await ApiClient.get<CollectionUpdateConfig>(`/api/indexs/collections/${collectionName}/update-config`)
    },

    // 上传数据文件
    async uploadData(collectionName: string, file: File, onProgress?: (progress: number) => void): Promise<ApiResponse<any>> {
        return await ApiClient.upload(`/api/indexs/collections/${collectionName}/upload`, file, onProgress)
    },

    // 远程同步数据
    async syncData(collectionName: string, config: RemoteSyncConfig): Promise<ApiResponse<SyncResult>> {
        const payload = {
            host: config.host,
            username: config.username,
            password: config.password,
            auth_source: config.authSource,
            collection: config.collection,
            batch_size: config.batchSize
        }
        return await ApiClient.post<SyncResult>(
            `/api/indexs/collections/${collectionName}/sync`,
            payload as any
        )
    },

    // 刷新集合数据
    async refreshCollectionData(
        collectionName: string,
        params: RefreshCollectionRequest
    ): Promise<ApiResponse<{ task_id: string; message: string }>> {
        return await ApiClient.post<{ task_id: string; message: string }>(
            `/api/indexs/collections/${collectionName}/refresh`,
            params
        )
    },

    // 获取刷新任务状态
    async getRefreshTaskStatus(collectionName: string, taskId: string): Promise<ApiResponse<RefreshTask>> {
        return await ApiClient.get<RefreshTask>(`/api/indexs/collections/${collectionName}/refresh/status/${taskId}`)
    },

    // 导出集合全部数据
    async exportCollectionData(
        collectionName: string,
        payload: CollectionExportRequest
    ): Promise<Blob> {
        const response = await request.post(
            `/api/indexs/collections/${collectionName}/export`,
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
            `/api/indexs/collections/${collectionName}/clear`
        )
    }
}
