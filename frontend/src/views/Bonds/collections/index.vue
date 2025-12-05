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

// 债券数据集合名称列表（如有特定组件则添加到此列表）
const collectionNames: string[] = [
  // 这里可以添加有特定组件的集合名称
  // 例如: 'bond_info_cm', 'bond_zh_hs_spot', ...
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
