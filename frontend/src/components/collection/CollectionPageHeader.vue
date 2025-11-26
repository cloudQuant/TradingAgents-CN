<template>
  <div class="page-header">
    <div class="header-content">
      <div class="title-section">
        <h1 class="page-title">
          <el-icon class="title-icon"><Box /></el-icon>
          {{ displayName || collectionName }}
          <span v-if="showEnglishName && collectionName" class="collection-name-en">({{ collectionName }})</span>
        </h1>
        <p class="page-description">{{ description || '' }}</p>
      </div>
      <div class="header-actions">
        <!-- 数据概览按钮 -->
        <el-button v-if="showOverviewButton" :icon="Box" @click="$emit('show-overview')">
          数据概览
        </el-button>
        
        <!-- 刷新按钮 -->
        <el-button :icon="Refresh" @click="$emit('refresh')" :loading="loading">
          刷新
        </el-button>
        
        <!-- 更新数据下拉菜单 -->
        <el-dropdown v-if="showUpdateDropdown" @command="handleUpdateCommand" trigger="click">
          <el-button :icon="Download" type="primary" :loading="updating">
            更新数据<el-icon class="el-icon--right"><ArrowDown /></el-icon>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="api" :icon="Download">API更新</el-dropdown-item>
              <el-dropdown-item command="file" :icon="Upload">文件导入</el-dropdown-item>
              <el-dropdown-item command="sync" :icon="Connection">远程同步</el-dropdown-item>
              <!-- 自定义菜单项插槽 -->
              <slot name="update-menu-items"></slot>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
        
        <!-- 清空数据按钮 -->
        <el-button 
          v-if="showClearButton" 
          :icon="Delete" 
          type="danger" 
          @click="handleClearData" 
          :loading="clearing"
        >
          清空数据
        </el-button>
        
        <!-- 额外操作按钮插槽 -->
        <slot name="extra-actions"></slot>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Box, Refresh, Delete, Download, ArrowDown, Upload, Connection } from '@element-plus/icons-vue'
import { ElMessageBox } from 'element-plus'

const props = withDefaults(defineProps<{
  collectionName: string
  displayName?: string
  description?: string
  loading?: boolean
  updating?: boolean
  clearing?: boolean
  showOverviewButton?: boolean
  showUpdateDropdown?: boolean
  showClearButton?: boolean
  showEnglishName?: boolean
  clearConfirmMessage?: string
}>(), {
  loading: false,
  updating: false,
  clearing: false,
  showOverviewButton: true,
  showUpdateDropdown: true,
  showClearButton: true,
  showEnglishName: false,
  clearConfirmMessage: '确定要清空该集合的所有数据吗？此操作不可恢复。',
})

const emit = defineEmits<{
  (e: 'show-overview'): void
  (e: 'refresh'): void
  (e: 'update-command', command: string): void
  (e: 'clear-data'): void
}>()

const handleUpdateCommand = (command: string) => {
  emit('update-command', command)
}

const handleClearData = async () => {
  try {
    await ElMessageBox.confirm(props.clearConfirmMessage, '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    emit('clear-data')
  } catch {
    // 用户取消
  }
}
</script>

<style lang="scss" scoped>
.page-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  padding: 24px 32px;
  margin-bottom: 24px;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.title-section {
  flex: 1;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: #fff;
  margin: 0 0 8px 0;
  display: flex;
  align-items: center;
  gap: 12px;
}

.title-icon {
  font-size: 28px;
}

.collection-name-en {
  font-size: 14px;
  font-weight: 400;
  opacity: 0.8;
}

.page-description {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.85);
  margin: 0;
  max-width: 600px;
}

.header-actions {
  display: flex;
  gap: 12px;
  flex-shrink: 0;
}

.header-actions .el-button {
  border: none;
  background: rgba(255, 255, 255, 0.15);
  color: #fff;
  
  &:hover {
    background: rgba(255, 255, 255, 0.25);
  }
  
  &.el-button--primary {
    background: rgba(255, 255, 255, 0.9);
    color: #667eea;
    
    &:hover {
      background: #fff;
    }
  }
  
  &.el-button--danger {
    background: rgba(245, 108, 108, 0.9);
    color: #fff;
    
    &:hover {
      background: #f56c6c;
    }
  }
}
</style>
