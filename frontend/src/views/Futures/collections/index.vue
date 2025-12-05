<template>
  <component :is="collectionComponent" v-if="collectionComponent" />
  <div v-else class="loading-container"><el-loading :loading="true" text="加载中..." /></div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, defineAsyncComponent } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'

const route = useRoute()
const collectionName = computed(() => route.params.collectionName as string)

const moduleMap = import.meta.glob('./*.vue')
const collectionComponents: Record<string, () => Promise<any>> = {}

// 注册现有组件
Object.keys(moduleMap)
  .filter(path => !path.includes('DefaultCollection') && !path.includes('index'))
  .forEach(path => {
    const match = path.match(/\.\/(.+)\.vue$/)
    if (match) {
      const snakeName = match[1].replace(/([A-Z])/g, '_$1').toLowerCase().replace(/^_/, '')
      collectionComponents[snakeName] = moduleMap[path] as () => Promise<any>
    }
  })

const collectionComponent = ref<any>(null)

onMounted(async () => {
  try {
    const name = collectionName.value
    if (!name) { ElMessage.error('集合名称不能为空'); return }
    const loader = collectionComponents[name]
    collectionComponent.value = defineAsyncComponent(loader || (() => import('./DefaultCollection.vue')))
  } catch (error: any) {
    ElMessage.error(`加载组件失败: ${error.message}`)
  }
})
</script>

<style lang="scss" scoped>
.loading-container { min-height: 400px; display: flex; align-items: center; justify-content: center; }
</style>
