<template>
  <el-menu
    :default-active="activeMenu"
    mode="horizontal"
    :ellipsis="true"
    router
    class="top-menu"
  >
    <el-menu-item index="/dashboard">
      <el-icon><Odometer /></el-icon>
      <template #title>仪表板</template>
    </el-menu-item>

    <el-sub-menu index="/stocks">
      <template #title>
        <el-icon><Histogram /></el-icon>
        <span>股票</span>
      </template>
      <el-menu-item index="/stocks/overview">概览</el-menu-item>
      <el-menu-item index="/stocks/collections">数据集合</el-menu-item>
      <el-menu-item index="/analysis/single">单股分析</el-menu-item>
      <el-menu-item index="/analysis/batch">批量分析</el-menu-item>
      <el-menu-item index="/reports">分析报告</el-menu-item>
    </el-sub-menu>

    <el-sub-menu index="/bonds">
      <template #title>
        <el-icon><Collection /></el-icon>
        <span>债券</span>
      </template>
      <el-menu-item index="/bonds/overview">概览</el-menu-item>
      <el-menu-item index="/bonds/collections">数据集合</el-menu-item>
      <el-menu-item index="/bonds/analysis">债券分析</el-menu-item>
      <el-menu-item index="/bonds/yield-curve">收益率曲线</el-menu-item>
    </el-sub-menu>

    <el-sub-menu index="/funds">
      <template #title>
        <el-icon><PieChart /></el-icon>
        <span>基金</span>
      </template>
      <el-menu-item index="/funds/overview">概览</el-menu-item>
      <el-menu-item index="/funds/collections">数据集合</el-menu-item>
      <el-menu-item index="/funds/analysis">基金分析</el-menu-item>
    </el-sub-menu>

    <el-sub-menu index="/futures">
      <template #title>
        <el-icon><DataLine /></el-icon>
        <span>期货</span>
      </template>
      <el-menu-item index="/futures/overview">概览</el-menu-item>
      <el-menu-item index="/futures/collections">数据集合</el-menu-item>
      <el-menu-item index="/futures/analysis">期货分析</el-menu-item>
    </el-sub-menu>

    <el-sub-menu index="/options">
      <template #title>
        <el-icon><Operation /></el-icon>
        <span>期权</span>
      </template>
      <el-menu-item index="/options/overview">概览</el-menu-item>
      <el-menu-item index="/options/collections">数据集合</el-menu-item>
      <el-menu-item index="/options/analysis">期权分析</el-menu-item>
    </el-sub-menu>

    <el-sub-menu index="/currencies">
      <template #title>
        <el-icon><Money /></el-icon>
        <span>外汇</span>
      </template>
      <el-menu-item index="/currencies/overview">概览</el-menu-item>
      <el-menu-item index="/currencies/collections">数据集合</el-menu-item>
      <el-menu-item index="/currencies/analysis">外汇分析</el-menu-item>
    </el-sub-menu>

    <el-sub-menu index="/cryptos">
      <template #title>
        <el-icon><Wallet /></el-icon>
        <span>Crypto</span>
      </template>
      <el-menu-item index="/cryptos/overview">概览</el-menu-item>
      <el-menu-item index="/cryptos/collections">数据集合</el-menu-item>
      <el-menu-item index="/cryptos/analysis">数字货币分析</el-menu-item>
    </el-sub-menu>

    <el-menu-item index="/tasks">
      <el-icon><List /></el-icon>
      <template #title>任务中心</template>
    </el-menu-item>

    <el-menu-item index="/screening">
      <el-icon><Filter /></el-icon>
      <template #title>股票筛选</template>
    </el-menu-item>

    <el-menu-item index="/favorites">
      <el-icon><Star /></el-icon>
      <template #title>我的自选股</template>
    </el-menu-item>

    <el-menu-item index="/paper">
      <el-icon><CreditCard /></el-icon>
      <template #title>模拟交易</template>
    </el-menu-item>

    <el-sub-menu index="/settings">
      <template #title>
        <el-icon><Setting /></el-icon>
        <span>设置</span>
      </template>

      <!-- 个人设置 -->
      <el-sub-menu index="/settings-personal">
        <template #title>个人设置</template>
        <el-menu-item index="/settings">通用设置</el-menu-item>
        <el-menu-item index="/settings?tab=appearance">外观设置</el-menu-item>
        <el-menu-item index="/settings?tab=analysis">分析偏好</el-menu-item>
        <el-menu-item index="/settings?tab=notifications">通知设置</el-menu-item>
        <el-menu-item index="/settings?tab=security">安全设置</el-menu-item>
      </el-sub-menu>

      <!-- 系统配置 -->
      <el-sub-menu index="/settings-config">
        <template #title>系统配置</template>
        <el-menu-item index="/settings/config">配置管理</el-menu-item>
        <el-menu-item index="/settings/cache">缓存管理</el-menu-item>
      </el-sub-menu>

      <!-- 系统管理 -->
      <el-sub-menu index="/settings-admin">
        <template #title>系统管理</template>
        <el-menu-item index="/settings/database">数据库管理</el-menu-item>
        <el-menu-item index="/settings/logs">操作日志</el-menu-item>
        <el-menu-item index="/settings/system-logs">系统日志</el-menu-item>
        <el-menu-item index="/settings/sync">多数据源同步</el-menu-item>
        <el-menu-item index="/settings/scheduler">定时任务</el-menu-item>
        <el-menu-item index="/settings/usage">使用统计</el-menu-item>
      </el-sub-menu>
    </el-sub-menu>

    <el-menu-item index="/about">
      <el-icon><InfoFilled /></el-icon>
      <template #title>关于</template>
    </el-menu-item>
  </el-menu>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAppStore } from '@/stores/app'
import {
  Odometer,
  Histogram,
  Collection,
  PieChart,
  DataLine,
  Operation,
  Money,
  Wallet,
  List,
  Filter,
  Star,
  CreditCard,
  Setting,
  InfoFilled
} from '@element-plus/icons-vue'

const route = useRoute()
const appStore = useAppStore()

const activeMenu = computed(() => {
  const path = route.path
  // Find the menu item that matches the current path prefix
  // This ensures sub-pages (like /stocks/collections/detail) keep the parent menu active
  const menuIndices = [
    '/dashboard',
    '/stocks/overview', '/stocks/collections', '/analysis/single', '/analysis/batch', '/reports',
    '/bonds/overview', '/bonds/collections', '/bonds/analysis', '/bonds/yield-curve',
    '/funds/overview', '/funds/collections', '/funds/analysis',
    '/futures/overview', '/futures/collections', '/futures/analysis',
    '/options/overview', '/options/collections', '/options/analysis',
    '/currencies/overview', '/currencies/collections', '/currencies/analysis',
    '/cryptos/overview', '/cryptos/collections', '/cryptos/analysis',
    '/tasks',
    '/screening',
    '/favorites',
    '/paper',
    '/settings', '/settings/config', '/settings/cache', '/settings/database', 
    '/settings/logs', '/settings/system-logs', '/settings/sync', 
    '/settings/scheduler', '/settings/usage',
    '/about'
  ]
  
  // Sort by length descending to match longest prefix first
  const sortedIndices = [...menuIndices].sort((a, b) => b.length - a.length)
  
  const matched = sortedIndices.find(index => path.startsWith(index))
  return matched || path
})
</script>

<style lang="scss" scoped>
.top-menu {
  border-bottom: none;
  height: 60px;
  flex: 1;
  min-width: 0; // Allow shrinking for flexbox
  
  :deep(.el-menu-item),
  :deep(.el-sub-menu__title) {
    height: 60px;
    line-height: 60px;
    padding: 0 8px;
    
    .el-icon {
      margin-right: 4px;
    }

    .el-sub-menu__icon-arrow {
      color: #FFD700;
    }
  }

  :deep(.el-menu-item.is-active) {
    border-bottom: 2px solid var(--el-color-primary);
    color: var(--el-color-primary);
    background-color: transparent !important;
  }
}
</style>
