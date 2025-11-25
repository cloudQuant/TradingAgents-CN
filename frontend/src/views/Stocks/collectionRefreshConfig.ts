/**
 * 股票数据集合刷新参数配置
 * 定义每个集合在"API更新"时需要的参数
 */

// UI类型定义
export type UIType = 'none' | 'single' | 'batch' | 'single-batch' | 'custom'

export interface RefreshParam {
  key: string
  name: string
  type: 'string' | 'number' | 'boolean' | 'select' | 'date'
  required: boolean
  defaultValue?: any
  options?: { label: string; value: any }[]
  placeholder?: string
  description?: string
  min?: number
  max?: number
  step?: number
}

export interface CollectionRefreshConfig {
  collectionName: string
  displayName: string
  uiType: UIType
  description?: string
  // 单个更新配置
  singleUpdate?: {
    enabled: boolean
    params: RefreshParam[]
    buttonText?: string
    tips?: string
  }
  // 批量更新配置
  batchUpdate?: {
    enabled: boolean
    params?: RefreshParam[]
    buttonText?: string
    tips?: string
    batchSizeConfig?: {
      min: number
      max: number
      default: number
    }
    concurrencyConfig?: {
      min: number
      max: number
      default: number
    }
    delayConfig?: {
      min: number
      max: number
      default: number
      step: number
    }
  }
  // 全部更新配置
  allUpdate?: {
    enabled: boolean
    buttonText?: string
    tips?: string
  }
}

// 集合刷新配置映射
export const collectionRefreshConfigs: Record<string, CollectionRefreshConfig> = {
  // ========== 需要参数的集合 ==========
  
  // ========== 02_个股信息查询-东财 ==========
  stock_individual_info_em: {
    collectionName: 'stock_individual_info_em',
    displayName: '个股信息查询-东财',
    uiType: 'single-batch',
    description: '获取个股的基本信息，包括股票代码、简称、总股本、流通股、总市值、流通市值、行业、上市时间等',
    singleUpdate: {
      enabled: true,
      params: [
        {
          key: 'symbol',
          name: '股票代码',
          type: 'string',
          required: true,
          placeholder: '请输入股票代码（如 000001）',
          description: '6位股票代码'
        }
      ],
      buttonText: '更新单个',
      tips: '输入单个股票代码，快速更新该股票信息'
    },
    batchUpdate: {
      enabled: true,
      buttonText: '开始批量更新',
      tips: '从沪深京A股实时行情数据（stock_zh_a_spot_em）中获取所有股票代码列表，批量更新个股信息。批量更新需要较长时间，请耐心等待',
      concurrencyConfig: {
        min: 1,
        max: 10,
        default: 3
      },
      delayConfig: {
        min: 0,
        max: 5,
        default: 0.5,
        step: 0.1
      }
    }
  },

  // ========== 03_个股信息查询-雪球 ==========
  stock_individual_basic_info_xq: {
    collectionName: 'stock_individual_basic_info_xq',
    displayName: '个股信息查询-雪球',
    uiType: 'single-batch',
    description: '从雪球获取个股详细信息，包括公司中文名、公司简称、主营业务、经营范围、法定代表人、注册资本、员工人数、实际控制人等',
    singleUpdate: {
      enabled: true,
      params: [
        {
          key: 'symbol',
          name: '股票代码',
          type: 'string',
          required: true,
          placeholder: '请输入股票代码（如 SH600000）',
          description: '雪球格式：SH/SZ/BJ + 6位代码'
        }
      ],
      buttonText: '更新单个',
      tips: '输入单个股票代码，快速更新该股票的雪球详细信息'
    },
    batchUpdate: {
      enabled: true,
      buttonText: '开始批量更新',
      tips: '从个股信息查询-东财（stock_individual_info_em）集合中获取股票代码列表，自动转换为雪球格式后批量更新。雪球API限流严格，建议并发数2-3，延时1-2秒',
      concurrencyConfig: {
        min: 1,
        max: 5,
        default: 2
      },
      delayConfig: {
        min: 0.5,
        max: 5,
        default: 1,
        step: 0.1
      }
    }
  },

  // A股历史行情-东财
  stock_zh_a_hist: {
    collectionName: 'stock_zh_a_hist',
    displayName: 'A股历史行情-东财',
    uiType: 'single-batch',
    description: '获取A股历史行情数据',
    singleUpdate: {
      enabled: true,
      params: [
        {
          key: 'symbol',
          name: '股票代码',
          type: 'string',
          required: true,
          placeholder: '如 000001'
        },
        {
          key: 'period',
          name: '周期',
          type: 'select',
          required: false,
          defaultValue: 'daily',
          options: [
            { label: '日线', value: 'daily' },
            { label: '周线', value: 'weekly' },
            { label: '月线', value: 'monthly' }
          ]
        },
        {
          key: 'adjust',
          name: '复权类型',
          type: 'select',
          required: false,
          defaultValue: 'qfq',
          options: [
            { label: '前复权', value: 'qfq' },
            { label: '后复权', value: 'hfq' },
            { label: '不复权', value: '' }
          ]
        }
      ],
      buttonText: '更新单个'
    },
    batchUpdate: {
      enabled: true,
      params: [
        {
          key: 'period',
          name: '周期',
          type: 'select',
          required: false,
          defaultValue: 'daily',
          options: [
            { label: '日线', value: 'daily' },
            { label: '周线', value: 'weekly' },
            { label: '月线', value: 'monthly' }
          ]
        },
        {
          key: 'adjust',
          name: '复权类型',
          type: 'select',
          required: false,
          defaultValue: 'qfq',
          options: [
            { label: '前复权', value: 'qfq' },
            { label: '后复权', value: 'hfq' },
            { label: '不复权', value: '' }
          ]
        }
      ],
      buttonText: '批量更新',
      tips: '批量获取所有A股的历史行情数据',
      concurrencyConfig: {
        min: 1,
        max: 10,
        default: 5
      }
    }
  },

  // A股分时数据-东财
  stock_zh_a_hist_min_em: {
    collectionName: 'stock_zh_a_hist_min_em',
    displayName: 'A股分时数据-东财',
    uiType: 'single',
    description: '获取A股分时数据',
    singleUpdate: {
      enabled: true,
      params: [
        {
          key: 'symbol',
          name: '股票代码',
          type: 'string',
          required: true,
          placeholder: '如 000001'
        },
        {
          key: 'period',
          name: '周期',
          type: 'select',
          required: false,
          defaultValue: '1',
          options: [
            { label: '1分钟', value: '1' },
            { label: '5分钟', value: '5' },
            { label: '15分钟', value: '15' },
            { label: '30分钟', value: '30' },
            { label: '60分钟', value: '60' }
          ]
        },
        {
          key: 'adjust',
          name: '复权类型',
          type: 'select',
          required: false,
          defaultValue: 'qfq',
          options: [
            { label: '前复权', value: 'qfq' },
            { label: '后复权', value: 'hfq' },
            { label: '不复权', value: '' }
          ]
        }
      ],
      buttonText: '获取分时数据'
    }
  },

  // ========== 不需要参数的集合 ==========
  
  // ========== 04_沪深京A股实时行情-东财 ==========
  stock_zh_a_spot_em: {
    collectionName: 'stock_zh_a_spot_em',
    displayName: '沪深京A股实时行情-东财',
    uiType: 'none',
    description: '获取沪深京A股实时行情数据，包括最新价、涨跌幅、成交量、成交额、换手率、市盈率、市净率、总市值、流通市值等',
    allUpdate: {
      enabled: true,
      buttonText: '更新全部数据',
      tips: '一次性获取所有沪深京A股（约5000+只）的实时行情数据。数据以【股票代码+日期】作为唯一标识保存'
    }
  }
}

// 获取集合刷新配置
export function getRefreshConfig(collectionName: string): CollectionRefreshConfig | null {
  return collectionRefreshConfigs[collectionName] || null
}

// 判断集合是否需要参数
export function requiresParams(collectionName: string): boolean {
  const config = getRefreshConfig(collectionName)
  return config ? config.uiType !== 'none' : false
}
