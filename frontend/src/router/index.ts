import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { nextTick } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useAppStore } from '@/stores/app'
import { ElMessage } from 'element-plus'
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'

// 配置NProgress
NProgress.configure({
  showSpinner: false,
  minimum: 0.2,
  easing: 'ease',
  speed: 500
})

// 路由配置
const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/bonds',
    name: 'Bonds',
    component: () => import('@/layouts/BasicLayout.vue'),
    redirect: '/bonds/overview',
    meta: {
      title: '债券分析',
      icon: 'Tickets',
      requiresAuth: true,
      transition: 'slide-up'
    },
    children: [
      {
        path: 'overview',
        name: 'BondsHome',
        component: () => import('@/views/Bonds/index.vue'),
        meta: {
          title: '债券分析',
          requiresAuth: true
        }
      },
      {
        path: 'analysis',
        name: 'BondAnalysis',
        component: () => import('@/views/Bonds/BondAnalysis.vue'),
        meta: {
          title: '债券分析',
          requiresAuth: true
        }
      },
      {
        path: 'yield-curve',
        name: 'BondsYieldCurve',
        component: () => import('@/views/Bonds/YieldCurve.vue'),
        meta: {
          title: '收益率曲线',
          requiresAuth: true
        }
      },
      {
        path: 'convertible',
        name: 'BondsConvertible',
        component: () => import('@/views/Bonds/Convertible.vue'),
        meta: {
          title: '可转债分析',
          requiresAuth: true
        }
      },
      {
        path: 'collections',
        name: 'BondCollections',
        component: () => import('@/views/Bonds/Collections.vue'),
        meta: {
          title: '债券数据集合',
          requiresAuth: true
        }
      },
      {
        path: 'collections/:collectionName',
        name: 'BondCollection',
        component: () => import('@/views/Bonds/collections/index.vue'),
        meta: {
          title: '债券数据集合详情',
          requiresAuth: true
        }
      },
      {
        path: '',
        name: 'BondsDefault',
        redirect: { name: 'BondsHome' }
      }
    ]
  },
  {
    path: '/funds',
    name: 'Funds',
    component: () => import('@/layouts/BasicLayout.vue'),
    redirect: '/funds/overview',
    meta: {
      title: '基金投研',
      icon: 'TrendCharts',
      requiresAuth: true,
      transition: 'slide-up'
    },
    children: [
      {
        path: 'overview',
        name: 'FundsHome',
        component: () => import('@/views/Funds/index.vue'),
        meta: {
          title: '基金概览',
          requiresAuth: true
        }
      },
      {
        path: 'collections',
        name: 'FundCollections',
        component: () => import('@/views/Funds/Collections.vue'),
        meta: {
          title: '基金数据集合',
          requiresAuth: true
        }
      },
      {
        path: 'collections/:collectionName',
        name: 'FundCollection',
        component: () => import('@/views/Funds/collections/index.vue'),
        meta: {
          title: '基金数据集合详情',
          requiresAuth: true
        }
      },
      {
        path: 'analysis',
        name: 'FundAnalysis',
        component: () => import('@/views/Funds/FundAnalysis.vue'),
        meta: {
          title: '基金分析',
          requiresAuth: true
        }
      },
      {
        path: '',
        name: 'FundsDefault',
        redirect: { name: 'FundsHome' }
      }
    ]
  },
  {
    path: '/futures',
    name: 'Futures',
    component: () => import('@/layouts/BasicLayout.vue'),
    redirect: '/futures/overview',
    meta: {
      title: '期货投研',
      icon: 'TrendCharts',
      requiresAuth: true,
      transition: 'slide-up'
    },
    children: [
      {
        path: 'overview',
        name: 'FuturesHome',
        component: () => import('@/views/Futures/index.vue'),
        meta: {
          title: '期货概览',
          requiresAuth: true
        }
      },
      {
        path: 'collections',
        name: 'FuturesCollections',
        component: () => import('@/views/Futures/Collections.vue'),
        meta: {
          title: '期货数据集合',
          requiresAuth: true
        }
      },
      {
        path: 'collections/:collectionName',
        name: 'FuturesCollection',
        component: () => import('@/views/Futures/collections/index.vue'),
        meta: {
          title: '期货数据集合详情',
          requiresAuth: true,
          hideInMenu: true
        }
      },
      {
        path: 'analysis',
        name: 'FuturesAnalysis',
        component: () => import('@/views/Futures/FuturesAnalysis.vue'),
        meta: {
          title: '期货分析',
          requiresAuth: true
        }
      },
      {
        path: '',
        name: 'FuturesDefault',
        redirect: { name: 'FuturesHome' }
      }
    ]
  },
  {
    path: '/options',
    name: 'Options',
    component: () => import('@/layouts/BasicLayout.vue'),
    redirect: '/options/overview',
    meta: {
      title: '期权投研',
      icon: 'TrendCharts',
      requiresAuth: true,
      transition: 'slide-up'
    },
    children: [
      {
        path: 'overview',
        name: 'OptionsHome',
        component: () => import('@/views/Options/index.vue'),
        meta: {
          title: '期权概览',
          requiresAuth: true
        }
      },
      {
        path: 'collections',
        name: 'OptionsCollections',
        component: () => import('@/views/Options/Collections.vue'),
        meta: {
          title: '期权数据集合',
          requiresAuth: true
        }
      },
      {
        path: 'collections/:collectionName',
        name: 'OptionsCollectionDetail',
        component: () => import('@/views/Options/collections/index.vue'),
        meta: {
          title: '期权数据集合详情',
          requiresAuth: true,
          hideInMenu: true
        }
      },
      {
        path: 'analysis',
        name: 'OptionsAnalysis',
        component: () => import('@/views/Options/OptionsAnalysis.vue'),
        meta: {
          title: '期权分析',
          requiresAuth: true
        }
      },
      {
        path: '',
        name: 'OptionsDefault',
        redirect: { name: 'OptionsHome' }
      }
    ]
  },
  {
    path: '/indexs',
    name: 'Indexs',
    component: () => import('@/layouts/BasicLayout.vue'),
    redirect: '/indexs/overview',
    meta: {
      title: '指数投研',
      icon: 'TrendCharts',
      requiresAuth: true,
      transition: 'slide-up'
    },
    children: [
      {
        path: 'overview',
        name: 'IndexsHome',
        component: () => import('@/views/Indexs/index.vue'),
        meta: {
          title: '指数概览',
          requiresAuth: true
        }
      },
      {
        path: 'collections',
        name: 'IndexsCollections',
        component: () => import('@/views/Indexs/Collections.vue'),
        meta: {
          title: '指数数据集合',
          requiresAuth: true
        }
      },
      {
        path: 'collections/:collectionName',
        name: 'IndexsCollectionDetail',
        component: () => import('@/views/Indexs/collections/index.vue'),
        meta: {
          title: '指数数据集合详情',
          requiresAuth: true,
          hideInMenu: true
        }
      },
      {
        path: '',
        name: 'IndexsDefault',
        redirect: { name: 'IndexsHome' }
      }
    ]
  },
  {
    path: '/currencies',
    name: 'Currencies',
    component: () => import('@/layouts/BasicLayout.vue'),
    redirect: '/currencies/overview',
    meta: { title: '外汇投研', icon: 'TrendCharts', requiresAuth: true, transition: 'slide-up' },
    children: [
      { path: 'overview', name: 'CurrenciesHome', component: () => import('@/views/Currencies/index.vue'), meta: { title: '外汇概览', requiresAuth: true } },
      { path: 'collections', name: 'CurrenciesCollections', component: () => import('@/views/Currencies/Collections.vue'), meta: { title: '外汇数据集合', requiresAuth: true } },
      { path: 'collections/:collectionName', name: 'CurrenciesCollectionDetail', component: () => import('@/views/Currencies/collections/index.vue'), meta: { title: '外汇数据集合详情', requiresAuth: true, hideInMenu: true } },
      { path: 'analysis', name: 'CurrenciesAnalysis', component: () => import('@/views/Currencies/CurrenciesAnalysis.vue'), meta: { title: '外汇分析', requiresAuth: true } },
      { path: '', name: 'CurrenciesDefault', redirect: { name: 'CurrenciesHome' } }
    ]
  },
  {
    path: '/cryptos',
    name: 'Cryptos',
    component: () => import('@/layouts/BasicLayout.vue'),
    redirect: '/cryptos/overview',
    meta: { title: '数字货币投研', icon: 'TrendCharts', requiresAuth: true, transition: 'slide-up' },
    children: [
      { path: 'overview', name: 'CryptosHome', component: () => import('@/views/Cryptos/index.vue'), meta: { title: '数字货币概览', requiresAuth: true } },
      { path: 'collections', name: 'CryptosCollections', component: () => import('@/views/Cryptos/Collections.vue'), meta: { title: '数字货币数据集合', requiresAuth: true } },
      { path: 'analysis', name: 'CryptosAnalysis', component: () => import('@/views/Cryptos/CryptosAnalysis.vue'), meta: { title: '数字货币分析', requiresAuth: true } },
      { path: '', name: 'CryptosDefault', redirect: { name: 'CryptosHome' } }
    ]
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/layouts/BasicLayout.vue'),
    meta: {
      title: '仪表板',
      icon: 'Dashboard',
      requiresAuth: true,
      transition: 'fade'
    },
    children: [
      {
        path: '',
        name: 'DashboardHome',
        component: () => import('@/views/Dashboard/index.vue'),
        meta: {
          title: '仪表板',
          requiresAuth: true
        }
      }
    ]
  },
  {
    path: '/analysis',
    name: 'Analysis',
    component: () => import('@/layouts/BasicLayout.vue'),
    redirect: '/analysis/single',
    children: [
      {
        path: 'single',
        name: 'SingleAnalysis',
        component: () => import('@/views/Analysis/SingleAnalysis.vue')
      },
      {
        path: 'batch',
        name: 'BatchAnalysis',
        component: () => import('@/views/Analysis/BatchAnalysis.vue')
      },

    ]
  },
  {
    path: '/screening',
    name: 'StockScreening',
    component: () => import('@/layouts/BasicLayout.vue'),
    meta: {
      title: '股票筛选',
      icon: 'Search',
      requiresAuth: true,
      transition: 'slide-up'
    },
    children: [
      {
        path: '',
        name: 'StockScreeningHome',
        component: () => import('@/views/Screening/index.vue'),
        meta: {
          title: '股票筛选',
          requiresAuth: true
        }
      }
    ]
  },

  {
    path: '/favorites',
    name: 'Favorites',
    component: () => import('@/layouts/BasicLayout.vue'),
    meta: {
      title: '我的自选股',
      icon: 'Star',
      requiresAuth: true,
      transition: 'slide-up'
    },
    children: [
      {
        path: '',
        name: 'FavoritesHome',
        component: () => import('@/views/Favorites/index.vue'),
        meta: {
          title: '我的自选股',
          requiresAuth: true
        }
      }
    ]
  },
  {
    path: '/stocks',
    name: 'Stocks',
    component: () => import('@/layouts/BasicLayout.vue'),
    meta: {
      title: '股票投研',
      icon: 'TrendCharts',
      requiresAuth: true,
      transition: 'fade'
    },
    children: [
      {
        path: 'overview',
        name: 'StocksOverview',
        component: () => import('@/views/Stocks/index.vue'),
        meta: {
          title: '股票概览',
          requiresAuth: true,
          transition: 'fade'
        }
      },
      {
        path: 'collections',
        name: 'StocksCollections',
        component: () => import('@/views/Stocks/Collections.vue'),
        meta: {
          title: '股票数据集合',
          requiresAuth: true,
          transition: 'fade'
        }
      },
      {
        path: 'collections/:collectionName',
        name: 'StocksCollectionDetail',
        component: () => import('@/views/Stocks/Collections/index.vue'),
        meta: {
          title: '股票数据集合详情',
          requiresAuth: true,
          hideInMenu: true,
          transition: 'fade',
        },
      },
      {
        path: ':code',
        name: 'StockDetail',
        component: () => import('@/views/Stocks/Detail.vue'),
        meta: {
          title: '股票详情',
          requiresAuth: true,
          hideInMenu: true,
          transition: 'fade'
        }
      }
    ]
  },


  {
    path: '/tasks',
    name: 'TaskCenter',
    component: () => import('@/layouts/BasicLayout.vue'),
    meta: {
      title: '任务中心',
      icon: 'List',
      requiresAuth: true,
      transition: 'slide-up'
    },
    children: [
      {
        path: '',
        name: 'TaskCenterHome',
        component: () => import('@/views/Tasks/TaskCenter.vue'),
        meta: { title: '任务中心', requiresAuth: true }
      }
    ]
  },
  { path: '/queue', redirect: '/tasks' },
  { path: '/analysis/history', redirect: '/tasks?tab=completed' },
  {
    path: '/reports',
    name: 'Reports',
    component: () => import('@/layouts/BasicLayout.vue'),
    meta: {
      title: '分析报告',
      icon: 'Document',
      requiresAuth: true,
      transition: 'fade'
    },
    children: [
      {
        path: '',
        name: 'ReportsHome',
        component: () => import('@/views/Reports/index.vue'),
        meta: {
          title: '分析报告',
          requiresAuth: true
        }
      },
      {
        path: 'view/:id',
        name: 'ReportDetail',
        component: () => import('@/views/Reports/ReportDetail.vue'),
        meta: {
          title: '报告详情',
          requiresAuth: true
        }
      },
      {
        path: 'token',
        name: 'TokenStatistics',
        component: () => import('@/views/Reports/TokenStatistics.vue'),
        meta: {
          title: 'Token统计',
          requiresAuth: true
        }
      }
    ]
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('@/layouts/BasicLayout.vue'),
    meta: {
      title: '设置',
      icon: 'Setting',
      requiresAuth: true,
      transition: 'slide-left'
    },
    children: [
      {
        path: '',
        name: 'SettingsHome',
        component: () => import('@/views/Settings/index.vue'),
        meta: {
          title: '设置',
          requiresAuth: true
        }
      },
      {
        path: 'config',
        name: 'ConfigManagement',
        component: () => import('@/views/Settings/ConfigManagement.vue'),
        meta: {
          title: '配置管理',
          requiresAuth: true
        }
      },
      {
        path: 'database',
        name: 'DatabaseManagement',
        component: () => import('@/views/System/DatabaseManagement.vue'),
        meta: {
          title: '数据库管理',
          requiresAuth: true
        }
      },
      {
        path: 'logs',
        name: 'OperationLogs',
        component: () => import('@/views/System/OperationLogs.vue'),
        meta: {
          title: '操作日志',
          requiresAuth: true
        }
      },
      {
        path: 'system-logs',
        name: 'LogManagement',
        component: () => import('@/views/System/LogManagement.vue'),
        meta: {
          title: '系统日志',
          requiresAuth: true
        }
      },
      {
        path: 'sync',
        name: 'MultiSourceSync',
        component: () => import('@/views/System/MultiSourceSync.vue'),
        meta: {
          title: '多数据源同步',
          requiresAuth: true
        }
      },
      {
        path: 'cache',
        name: 'CacheManagement',
        component: () => import('@/views/Settings/CacheManagement.vue'),
        meta: {
          title: '缓存管理',
          requiresAuth: true
        }
      },
      {
        path: 'usage',
        name: 'UsageStatistics',
        component: () => import('@/views/Settings/UsageStatistics.vue'),
        meta: {
          title: '使用统计',
          requiresAuth: true
        }
      },
      {
        path: 'scheduler',
        name: 'SchedulerManagement',
        component: () => import('@/views/System/SchedulerManagement.vue'),
        meta: {
          title: '定时任务',
          requiresAuth: true
        }
      }
    ]
  },
  {
    path: '/sync',
    name: 'Sync',
    component: () => import('@/layouts/BasicLayout.vue'),
    redirect: '/sync/nodes',
    meta: {
      title: '数据同步',
      icon: 'Connection',
      requiresAuth: true,
      transition: 'fade'
    },
    children: [
      {
        path: 'nodes',
        name: 'SyncNodes',
        component: () => import('@/views/Sync/SyncNodes.vue'),
        meta: {
          title: '同步节点',
          requiresAuth: true
        }
      },
      {
        path: 'tasks',
        name: 'SyncTasks',
        component: () => import('@/views/Sync/SyncTasks.vue'),
        meta: {
          title: '同步任务',
          requiresAuth: true
        }
      }
    ]
  },

  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Auth/Login.vue'),
    meta: {
      title: '登录',
      hideInMenu: true,
      transition: 'fade'
    }
  },

  {
    path: '/about',
    name: 'About',
    component: () => import('@/views/About/index.vue'),
    meta: {
      title: '关于',
      icon: 'InfoFilled',
      requiresAuth: false, // 关于页面不需要认证
      transition: 'fade'
    }
  },
  {
    path: '/paper',
    name: 'PaperTrading',
    component: () => import('@/layouts/BasicLayout.vue'),
    meta: {
      title: '模拟交易',
      icon: 'CreditCard',
      requiresAuth: true,
      transition: 'slide-up'
    },
    children: [
      {
        path: '',
        name: 'PaperTradingHome',
        component: () => import('@/views/PaperTrading/index.vue'),
        meta: {
          title: '模拟交易',
          requiresAuth: true
        }
      }
    ]
  },

  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/Error/404.vue'),
    meta: {
      title: '页面不存在',
      hideInMenu: true,
      requiresAuth: true
    }
  }
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(_to, _from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// 全局前置守卫
router.beforeEach(async (to, _from, next) => {
  // 开始进度条
  NProgress.start()

  const authStore = useAuthStore()
  const appStore = useAppStore()

  // 设置页面标题
  const title = to.meta.title as string
  if (title) {
    document.title = `${title} - 云子量化`
  }

  console.log('🚦 路由守卫检查:', {
    path: to.fullPath,
    name: to.name,
    requiresAuth: to.meta.requiresAuth,
    isAuthenticated: authStore.isAuthenticated,
    hasToken: !!authStore.token
  })

  // 检查是否需要认证
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    console.log('🔒 需要认证但用户未登录:', {
      path: to.fullPath,
      requiresAuth: to.meta.requiresAuth,
      isAuthenticated: authStore.isAuthenticated,
      token: authStore.token ? '存在' : '不存在'
    })
    // 保存原始路径，登录后跳转
    authStore.setRedirectPath(to.fullPath)
    next('/login')
    return
  }



  // 如果已登录且访问登录页，重定向到仪表板
  if (authStore.isAuthenticated && to.name === 'Login') {
    next('/dashboard')
    return
  }

  // 更新当前路由信息
  appStore.setCurrentRoute(to)

  next()
})

// 全局后置守卫
router.afterEach((_to, _from) => {
  // 结束进度条
  NProgress.done()

  // 页面切换后的处理
  nextTick(() => {
    // 可以在这里添加页面分析、埋点等逻辑
  })
})

// 路由错误处理
router.onError((error) => {
  console.error('路由错误:', error)
  console.error('错误详情:', {
    message: error.message,
    stack: error.stack,
    name: error.name
  })
  NProgress.done()
  ElMessage.error(`页面加载失败: ${error.message || '未知错误'}，请检查控制台`)
})

export default router

// 导出路由配置供其他地方使用
export { routes }
