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

// 使用 Vite 的 import.meta.glob 预加载同目录下所有 .vue 组件
const moduleMap = import.meta.glob('./*.vue')

// 动态生成集合到组件加载函数的映射
const collectionComponents: Record<string, () => Promise<any>> = {}

// 股票数据集合名称列表（有特定组件的集合）
// 现有的290个组件都可以在这里使用
const existingComponents = Object.keys(moduleMap)
  .filter(path => !path.includes('DefaultCollection') && !path.includes('index'))
  .map(path => {
    // 从路径 "./StockZhASpotEm.vue" 提取组件名 "StockZhASpotEm"
    const match = path.match(/\.\/(.+)\.vue$/)
    return match ? match[1] : null
  })
  .filter(Boolean) as string[]

// 为每个现有组件注册
existingComponents.forEach(componentName => {
  const path = `./${componentName}.vue`
  if (moduleMap[path]) {
    // 将 PascalCase 转换回 snake_case 作为集合名称
    const snakeName = componentName
      .replace(/([A-Z])/g, '_$1')
      .toLowerCase()
      .replace(/^_/, '')
    collectionComponents[snakeName] = moduleMap[path] as () => Promise<any>
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
      // 使用特定组件
      collectionComponent.value = defineAsyncComponent(componentLoader)
    } else {
      // 使用默认组件
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
