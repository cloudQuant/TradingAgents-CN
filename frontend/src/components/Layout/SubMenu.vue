<template>
  <div v-if="currentSubMenus.length > 0" class="sub-nav-bar">
    <div class="sub-nav-content">
      <router-link
        v-for="item in currentSubMenus"
        :key="item.path"
        :to="item.path"
        class="sub-nav-item"
        :class="{ active: isActive(item.path) }"
      >
        {{ item.title }}
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

interface MenuItem {
  title: string
  path: string
}

const menuItems: Record<string, MenuItem[]> = {
  stocks: [
    { title: '概览', path: '/stocks/overview' },
    { title: '数据集合', path: '/stocks/collections' },
    { title: '单股分析', path: '/analysis/single' },
    { title: '批量分析', path: '/analysis/batch' },
    { title: '分析报告', path: '/reports' },
  ],
  bonds: [
    { title: '概览', path: '/bonds/overview' },
    { title: '数据集合', path: '/bonds/collections' },
    { title: '债券分析', path: '/bonds/analysis' },
    { title: '收益率曲线', path: '/bonds/yield-curve' },
  ],
  funds: [
    { title: '概览', path: '/funds/overview' },
    { title: '数据集合', path: '/funds/collections' },
    { title: '基金分析', path: '/funds/analysis' },
  ],
  futures: [
    { title: '概览', path: '/futures/overview' },
    { title: '数据集合', path: '/futures/collections' },
    { title: '期货分析', path: '/futures/analysis' },
  ],
  options: [
    { title: '概览', path: '/options/overview' },
    { title: '数据集合', path: '/options/collections' },
    { title: '期权分析', path: '/options/analysis' },
  ],
  currencies: [
    { title: '概览', path: '/currencies/overview' },
    { title: '数据集合', path: '/currencies/collections' },
    { title: '外汇分析', path: '/currencies/analysis' },
  ],
  cryptos: [
    { title: '概览', path: '/cryptos/overview' },
    { title: '数据集合', path: '/cryptos/collections' },
    { title: '数字货币分析', path: '/cryptos/analysis' },
  ],
  settings: [
    { title: '通用设置', path: '/settings' },
    { title: '配置管理', path: '/settings/config' },
    { title: '缓存管理', path: '/settings/cache' },
    { title: '数据库管理', path: '/settings/database' },
    { title: '操作日志', path: '/settings/logs' },
    { title: '系统日志', path: '/settings/system-logs' },
    { title: '多数据源', path: '/settings/sync' },
    { title: '定时任务', path: '/settings/scheduler' },
    { title: '使用统计', path: '/settings/usage' },
  ]
}

const getCategory = (path: string) => {
  if (path.startsWith('/stocks') || path.startsWith('/analysis') || path === '/reports') return 'stocks'
  if (path.startsWith('/bonds')) return 'bonds'
  if (path.startsWith('/funds')) return 'funds'
  if (path.startsWith('/futures')) return 'futures'
  if (path.startsWith('/options')) return 'options'
  if (path.startsWith('/currencies')) return 'currencies'
  if (path.startsWith('/cryptos')) return 'cryptos'
  if (path.startsWith('/settings')) return 'settings'
  return ''
}

const currentSubMenus = computed(() => {
  const category = getCategory(route.path)
  return category ? menuItems[category] || [] : []
})

const isActive = (path: string) => {
  // For settings root path
  if (path === '/settings') {
    return route.path === path
  }
  // For other paths, check if current route starts with the menu item path
  // This ensures detail pages highlight their parent list page
  // e.g. /stocks/collections/sh600000 should highlight /stocks/collections
  return route.path === path || route.path.startsWith(path + '/')
}
</script>

<style lang="scss" scoped>
.sub-nav-bar {
  background-color: var(--el-bg-color);
  border-bottom: 1px solid var(--el-border-color-light);
  padding: 0 24px;
  height: 48px;
  display: flex;
  align-items: center;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  z-index: 999; // Below header
  
  .sub-nav-content {
    display: flex;
    align-items: center;
    gap: 24px;
    max-width: 1600px;
    margin: 0 auto;
    width: 100%;
    overflow-x: auto;
    
    // Hide scrollbar
    &::-webkit-scrollbar {
      display: none;
    }
    scrollbar-width: none;
  }

  .sub-nav-item {
    text-decoration: none;
    color: var(--el-text-color-regular);
    font-size: 14px;
    font-weight: 500;
    white-space: nowrap;
    position: relative;
    padding: 12px 0;
    transition: color 0.3s;

    &:hover {
      color: var(--el-color-primary);
    }

    &.active {
      color: var(--el-color-primary);
      font-weight: 600;

      &::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 2px;
        background-color: var(--el-color-primary);
        border-radius: 2px;
      }
    }
  }
}

// Responsive
@media (max-width: 768px) {
  .sub-nav-bar {
    padding: 0 16px;
    
    .sub-nav-content {
      gap: 16px;
    }
  }
}
</style>
