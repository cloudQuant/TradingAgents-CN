import { ApiClient, request } from './request'

export interface QuoteResponse {
  symbol: string  // 主字段：6位股票代码
  code?: string   // 兼容字段（已废弃）
  full_symbol?: string  // 完整代码（如 000001.SZ）
  name?: string
  market?: string
  price?: number
  change_percent?: number
  amount?: number
  prev_close?: number
  turnover_rate?: number
  amplitude?: number  // 振幅（替代量比）
  trade_date?: string
  updated_at?: string
}

export interface FundamentalsResponse {
  symbol: string  // 主字段：6位股票代码
  code?: string   // 兼容字段（已废弃）
  full_symbol?: string  // 完整代码（如 000001.SZ）
  name?: string
  industry?: string
  market?: string
  sector?: string  // 板块
  pe?: number
  pb?: number
  ps?: number      // 🔥 新增：市销率
  pe_ttm?: number
  pb_mrq?: number
  ps_ttm?: number  // 🔥 新增：市销率（TTM）
  roe?: number
  debt_ratio?: number  // 🔥 新增：负债率
  total_mv?: number
  circ_mv?: number
  turnover_rate?: number
  volume_ratio?: number
  pe_is_realtime?: boolean  // PE是否为实时数据
  pe_source?: string        // PE数据来源
  pe_updated_at?: string    // PE更新时间
  updated_at?: string
}

export interface KlineBar {
  time: string
  open?: number
  high?: number
  low?: number
  close?: number
  volume?: number
  amount?: number
}

export interface KlineResponse {
  symbol: string  // 主字段：6位股票代码
  code?: string   // 兼容字段（已废弃）
  period: 'day'|'week'|'month'|'5m'|'15m'|'30m'|'60m'
  limit: number
  adj: 'none'|'qfq'|'hfq'
  source?: string
  items: KlineBar[]
}

export interface NewsItem {
  title: string
  source: string
  time: string
  url: string
  type: 'news' | 'announcement'
}

export interface NewsResponse {
  symbol: string  // 主字段：6位股票代码
  code?: string   // 兼容字段（已废弃）
  days: number
  limit: number
  include_announcements: boolean
  source?: string
  items: NewsItem[]
}

export interface QuotesOverviewItem {
  code: string
  name?: string
  market?: string
  latest_price?: number
  pct_chg?: number
  volume?: number
  amount?: number
  trade_date?: string
  updated_at?: string
}

export interface QuotesOverviewResponse {
  items: QuotesOverviewItem[]
  total: number
  page: number
  page_size: number
}

export interface StockCollectionDataResponse<T = any> {
  items: T[]
  total: number
  page: number
  page_size: number
}

export interface CollectionInfo {
  name: string
  display_name: string
  description: string
  route: string
  fields: string[]
}

export interface CollectionStatsResponse {
  total_count: number
  collection_name: string
  latest_update?: string
}

export interface RefreshTaskResponse {
  task_id: string
  message: string
}

export interface RefreshStatusResponse {
  task_id: string
  status: 'pending' | 'running' | 'completed' | 'failed'
  progress: number
  total: number
  message: string
  result?: any
  error?: string
}

export const stocksApi = {
  /**
   * 获取股票行情
   * @param symbol 6位股票代码
   */
  async getQuote(symbol: string) {
    return ApiClient.get<QuoteResponse>(`/api/stocks/${symbol}/quote`)
  },

  /**
   * 获取股票基本面数据
   * @param symbol 6位股票代码
   */
  async getFundamentals(symbol: string) {
    return ApiClient.get<FundamentalsResponse>(`/api/stocks/${symbol}/fundamentals`)
  },

  /**
   * 获取K线数据
   * @param symbol 6位股票代码
   * @param period K线周期
   * @param limit 数据条数
   * @param adj 复权方式
   */
  async getKline(symbol: string, period: KlineResponse['period'] = 'day', limit = 120, adj: KlineResponse['adj'] = 'none') {
    return ApiClient.get<KlineResponse>(`/api/stocks/${symbol}/kline`, { period, limit, adj })
  },

  /**
   * 获取股票新闻
   * @param symbol 6位股票代码
   * @param days 天数
   * @param limit 数量限制
   * @param includeAnnouncements 是否包含公告
   */
  async getNews(symbol: string, days = 2, limit = 50, includeAnnouncements = true) {
    return ApiClient.get<NewsResponse>(`/api/stocks/${symbol}/news`, { days, limit, include_announcements: includeAnnouncements })
  },

  /**
   * 获取市场行情一览（分页 + 搜索）
   */
  async getQuotesOverview(params: {
    page?: number
    page_size?: number
    sort_by?: string
    sort_dir?: string
    keyword?: string
  }) {
    return ApiClient.get<QuotesOverviewResponse>(
      '/api/stocks/quotes/overview',
      params,
    )
  },

  /**
   * 获取股票数据集合详情（分页）
   */
  async getStockCollectionData(collectionName: string, params: {
    page?: number
    page_size?: number
    sort_by?: string
    sort_dir?: string
    code?: string
  } = {}) {
    return ApiClient.get<StockCollectionDataResponse>(
      `/api/stocks/collections/${collectionName}/data`,
      params,
    )
  },

  /**
   * 获取所有股票数据集合列表
   */
  async getCollections() {
    return ApiClient.get<CollectionInfo[]>('/api/stocks/collections')
  },

  /**
   * 刷新股票数据集合
   */
  async refreshCollection(collectionName: string, params: any = {}) {
    return ApiClient.post<RefreshTaskResponse>(
      `/api/stocks/collections/${collectionName}/refresh`,
      params
    )
  },

  /**
   * 查询刷新任务状态
   */
  async getRefreshStatus(collectionName: string, taskId: string) {
    return ApiClient.get<RefreshStatusResponse>(
      `/api/stocks/collections/${collectionName}/refresh/status/${taskId}`
    )
  },

  /**
   * 获取集合数据统计信息
   */
  async getCollectionStats(collectionName: string) {
    return ApiClient.get<CollectionStatsResponse>(
      `/api/stocks/collections/${collectionName}/stats`
    )
  },

  /**
   * 清空集合数据
   */
  async clearCollection(collectionName: string) {
    return ApiClient.delete<{ deleted_count: number; message: string }>(
      `/api/stocks/collections/${collectionName}/clear`
    )
  },

  /**
   * 获取集合的更新配置
   */
  async getUpdateConfig(collectionName: string) {
    return ApiClient.get<any>(
      `/api/stocks/collections/${collectionName}/update-config`
    )
  },

  /**
   * 上传数据文件
   */
  async uploadData(collectionName: string, file: File, onProgress?: (progress: number) => void) {
    return await ApiClient.upload(`/api/stocks/collections/${collectionName}/upload`, file, onProgress)
  },

  /**
   * 远程同步数据
   */
  async syncData(collectionName: string, config: any) {
    return await ApiClient.post(`/api/stocks/collections/${collectionName}/sync`, config)
  },

  /**
   * 导出集合全部数据
   */
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
      `/api/stocks/collections/${collectionName}/export`,
      payload,
      {
        responseType: 'blob',
        timeout: 300000
      }
    )
    return response as unknown as Blob
  }
}

