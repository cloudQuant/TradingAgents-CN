<template>
  <el-menu
    :default-active="activeMenu"
    :collapse="appStore.sidebarCollapsed"
    :unique-opened="true"
    router
    class="sidebar-menu"
  >
    <el-menu-item index="/dashboard">
      <el-icon><Odometer /></el-icon>
      <template #title>仪表板</template>
    </el-menu-item>

    <el-sub-menu index="/stocks">
      <template #title>
        <el-icon><TrendCharts /></el-icon>
        <span>股票投研</span>
      </template>
      <el-menu-item index="/stocks/overview">概览</el-menu-item>
      <el-menu-item index="/stocks/collections">数据集合</el-menu-item>
      <el-menu-item index="/analysis/single">单股分析</el-menu-item>
      <el-menu-item index="/analysis/batch">批量分析</el-menu-item>
      <el-menu-item index="/reports">分析报告</el-menu-item>
    </el-sub-menu>

    <el-sub-menu index="/bonds">
      <template #title>
        <el-icon><Tickets /></el-icon>
        <span>债券投研</span>
      </template>
      <el-menu-item index="/bonds/overview">概览</el-menu-item>
      <el-menu-item index="/bonds/collections">数据集合</el-menu-item>
      <el-menu-item index="/bonds/analysis">债券分析</el-menu-item>
      <el-menu-item index="/bonds/yield-curve">收益率曲线</el-menu-item>
    </el-sub-menu>

    <el-sub-menu index="/funds">
      <template #title>
        <el-icon><TrendCharts /></el-icon>
        <span>基金投研</span>
      </template>
      <el-menu-item index="/funds/overview">概览</el-menu-item>
      <el-menu-item index="/funds/collections">数据集合</el-menu-item>
      <el-menu-item index="/funds/analysis">基金分析</el-menu-item>
    </el-sub-menu>

    <el-sub-menu index="/futures">
      <template #title>
        <el-icon><TrendCharts /></el-icon>
        <span>期货投研</span>
      </template>
      <el-menu-item index="/futures/overview">概览</el-menu-item>
      <el-menu-item index="/futures/collections">数据集合</el-menu-item>
      <el-menu-item index="/futures/analysis">期货分析</el-menu-item>
    </el-sub-menu>

    <el-sub-menu index="/options">
      <template #title>
        <el-icon><TrendCharts /></el-icon>
        <span>期权投研</span>
      </template>
      <el-menu-item index="/options/overview">概览</el-menu-item>
      <el-menu-item index="/options/collections">数据集合</el-menu-item>
      <el-menu-item index="/options/analysis">期权分析</el-menu-item>
    </el-sub-menu>

    <el-sub-menu index="/currencies">
      <template #title>
        <el-icon><TrendCharts /></el-icon>
        <span>外汇投研</span>
      </template>
      <el-menu-item index="/currencies/overview">概览</el-menu-item>
      <el-menu-item index="/currencies/collections">数据集合</el-menu-item>
      <el-menu-item index="/currencies/analysis">外汇分析</el-menu-item>
    </el-sub-menu>

    <el-sub-menu index="/cryptos">
      <template #title>
        <el-icon><TrendCharts /></el-icon>
        <span>Crypto投研</span>
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
      <el-icon><Search /></el-icon>
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


    <!-- 分析报告已移至“股票分析”子菜单，保留注释便于追踪 -->
    <!--
    <el-menu-item index="/reports">
      <el-icon><Document /></el-icon>
      <template #title>分析报告</template>
    </el-menu-item>
    -->

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
  TrendCharts,
  Tickets,
  Search,
  Star,
  List,
  /* Document 移除：不再使用顶级分析报告菜单图标 */
  Setting,
  Tools,
  InfoFilled,
  CreditCard
} from '@element-plus/icons-vue'

const route = useRoute()
const appStore = useAppStore()

const activeMenu = computed(() => route.path)
</script>

<style lang="scss" scoped>
.sidebar-menu {
  border: none;
  height: 100%;

  :deep(.el-menu-item),
  :deep(.el-sub-menu__title) {
    height: 48px;
    line-height: 48px;
  }

  :deep(.el-menu-item.is-active) {
    background-color: var(--el-color-primary-light-9);
    color: var(--el-color-primary);
  }
}
</style>
