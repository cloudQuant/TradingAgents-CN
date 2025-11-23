<template>
  <div class="basic-layout">
    <!-- 顶部导航栏 -->
    <header class="header">
      <div class="header-left">
        <router-link to="/" class="logo">
          <img src="/logo.svg" alt="cloudQuant" />
          <span class="logo-text">cloudQuant</span>
        </router-link>
      </div>

      <div class="header-center">
        <TopMenu />
      </div>
      
      <div class="header-right">
        <HeaderActions />
        <div class="user-profile-wrapper">
          <UserProfile />
        </div>
      </div>
    </header>

    <!-- 主内容区 -->
    <div class="main-container">
      <!-- 二级菜单 -->
      <SubMenu />
      
      <main class="main-content">
        <div class="content-wrapper">
          <router-view v-slot="{ Component, route }">
            <transition
              :name="route.meta.transition || 'fade'"
              mode="out-in"
              appear
            >
              <keep-alive :include="keepAliveComponents">
                <component :is="Component" :key="route.fullPath" />
              </keep-alive>
            </transition>
          </router-view>
        </div>
      </main>

      <!-- 页脚 -->
      <footer class="footer">
        <AppFooter />
      </footer>
    </div>

    <!-- 回到顶部 -->
    <el-backtop :right="40" :bottom="40" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAppStore } from '@/stores/app'
import TopMenu from '@/components/Layout/TopMenu.vue'
import SubMenu from '@/components/Layout/SubMenu.vue'
import UserProfile from '@/components/Layout/UserProfile.vue'
import HeaderActions from '@/components/Layout/HeaderActions.vue'
import AppFooter from '@/components/Layout/AppFooter.vue'

const appStore = useAppStore()

// 需要缓存的组件
const keepAliveComponents = computed(() => [
  'Dashboard',
  'StockScreening',
  'AnalysisHistory',
  'QueueManagement'
])
</script>

<style lang="scss" scoped>
.basic-layout {
  min-height: 100vh;
  background-color: var(--el-bg-color-page);
  display: flex;
  flex-direction: column;
}

.header {
  height: 60px;
  background-color: var(--el-bg-color);
  border-bottom: 1px solid var(--el-border-color-light);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);

  .header-left {
    display: flex;
    align-items: center;
    flex-shrink: 0;
    margin-right: 24px;

    .logo {
      display: flex;
      align-items: center;
      gap: 12px;
      text-decoration: none;
      cursor: pointer;

      img {
        width: 32px;
        height: 32px;
      }

      .logo-text {
        font-size: 18px;
        font-weight: 600;
        color: var(--el-text-color-primary);
        white-space: nowrap;
      }
    }
  }

  .header-center {
    flex: 1;
    min-width: 0;
    overflow: hidden;
  }

  .header-right {
    display: flex;
    align-items: center;
    gap: 16px;
    flex-shrink: 0;
    margin-left: 16px;

    .user-profile-wrapper {
      margin-left: 8px;
    }
  }
}

.main-container {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  padding: 24px;
  max-width: 1600px;
  margin: 0 auto;
  width: 100%;
  box-sizing: border-box;

  .breadcrumb-wrapper {
    margin-bottom: 16px;
  }

  .content-wrapper {
    width: 100%;
  }
}

.footer {
  height: 60px;
  background-color: var(--el-bg-color);
  border-top: 1px solid var(--el-border-color-light);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: auto;
}

// 响应式调整
@media (max-width: 768px) {
  .header {
    padding: 0 16px;
    
    .header-left {
      margin-right: 16px;
      
      .logo-text {
        display: none;
      }
    }
  }

  .main-content {
    padding: 16px;
  }
}

// 路由过渡动画
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
