<template>
  <component :is="collectionComponent" v-if="collectionComponent" />
  <div v-else class="loading-container">
    <el-loading :loading="true" text="加载中..." />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, defineAsyncComponent } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'

const route = useRoute()
const collectionName = computed(() => route.params.collectionName as string)

// 将集合名称转换为 PascalCase 组件名
function toPascalCase(name: string): string {
  return name.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join('')
}

// 使用 Vite 的 import.meta.glob 预加载同目录下所有 .vue 组件
const moduleMap = import.meta.glob('./*.vue')

// 动态生成集合到组件加载函数的映射
const collectionComponents: Record<string, () => Promise<any>> = {}
const collectionNames = [
  // A股指数
  'stock_zh_index_spot_em',
  'stock_zh_index_spot_sina',
  'stock_zh_index_daily',
  'stock_zh_index_daily_em',
  'index_zh_a_hist',
  'index_zh_a_hist_min_em',
  // 港股指数
  'stock_hk_index_spot_sina',
  'stock_hk_index_daily_sina',
  'stock_hk_index_spot_em',
  'stock_hk_index_daily_em',
  // 美股指数
  'index_us_stock_sina',
  // 全球指数
  'index_global_spot_em',
  'index_global_hist_em',
]

// 为每个集合注册组件
collectionNames.forEach(name => {
  const componentName = toPascalCase(name)
  const path = `./${componentName}.vue`

  if (moduleMap[path]) {
    collectionComponents[name] = moduleMap[path] as () => Promise<any>
  }
})

const collectionComponent = ref<any>(null)
const loading = ref(true)

onMounted(async () => {
  try {
    const name = collectionName.value
    if (!name) {
      ElMessage.error('集合名称不能为空')
      return
    }

    const componentLoader = collectionComponents[name]
    if (componentLoader) {
      collectionComponent.value = defineAsyncComponent(componentLoader)
    } else {
      // 如果没有找到对应的组件，使用通用组件
      ElMessage.warning(`集合 ${name} 的组件尚未创建，使用默认组件`)
      collectionComponent.value = defineAsyncComponent(() => import('./DefaultCollection.vue'))
    }
  } catch (error: any) {
    console.error('加载集合组件失败:', error)
    ElMessage.error(`加载集合组件失败: ${error.message}`)
  } finally {
    loading.value = false
  }
})
</script>

<style lang="scss" scoped>
.loading-container {
  min-height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
