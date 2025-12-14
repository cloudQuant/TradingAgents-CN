<template>
  <div class="indexs-overview">
    <div class="page-header">
      <h1 class="page-title">
        <el-icon class="title-icon"><TrendCharts /></el-icon>
        指数概览
      </h1>
      <p class="page-description">
        查看全球主要指数的实时行情和历史数据
      </p>
    </div>

    <el-row :gutter="20">
      <el-col :span="8">
        <el-card shadow="hover" class="stat-card">
          <template #header>
            <div class="card-header">
              <span>A股指数</span>
            </div>
          </template>
          <div class="stat-content">
            <el-statistic title="数据集合" :value="aStockCollections" />
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover" class="stat-card">
          <template #header>
            <div class="card-header">
              <span>港股指数</span>
            </div>
          </template>
          <div class="stat-content">
            <el-statistic title="数据集合" :value="hkCollections" />
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover" class="stat-card">
          <template #header>
            <div class="card-header">
              <span>全球指数</span>
            </div>
          </template>
          <div class="stat-content">
            <el-statistic title="数据集合" :value="globalCollections" />
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-card shadow="hover" class="quick-access-card">
      <template #header>
        <div class="card-header">
          <span>快速访问</span>
        </div>
      </template>
      <el-row :gutter="16">
        <el-col :span="6">
          <el-button type="primary" @click="goToCollections" style="width: 100%">
            <el-icon><Box /></el-icon>
            数据集合
          </el-button>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { TrendCharts, Box } from '@element-plus/icons-vue'

const router = useRouter()

// 统计数据
const aStockCollections = ref(7)  // A股指数相关集合数
const hkCollections = ref(4)      // 港股指数相关集合数
const globalCollections = ref(3)  // 全球指数相关集合数（含美股）

const goToCollections = () => {
  router.push('/indexs/collections')
}
</script>

<style lang="scss" scoped>
.indexs-overview {
  padding: 20px;
}

.page-header {
  margin-bottom: 24px;
  
  .page-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 24px;
    font-weight: 600;
    margin: 0 0 8px 0;
    
    .title-icon {
      font-size: 28px;
    }
  }
  
  .page-description {
    color: var(--el-text-color-secondary);
    margin: 0;
  }
}

.stat-card {
  margin-bottom: 20px;
  
  .card-header {
    font-weight: 600;
  }
  
  .stat-content {
    text-align: center;
  }
}

.quick-access-card {
  .card-header {
    font-weight: 600;
  }
}
</style>
