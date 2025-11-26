<template>
  <el-dialog
    :model-value="visible"
    title="文件导入"
    width="600px"
    :close-on-click-modal="false"
    @update:model-value="$emit('update:visible', $event)"
  >
    <el-upload
      ref="uploadRef"
      :auto-upload="false"
      :multiple="allowMultiple"
      :limit="maxFiles"
      :on-change="handleFileChange"
      :on-remove="handleFileRemove"
      :accept="acceptTypes"
      drag
    >
      <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
      <div class="el-upload__text">
        拖拽文件到此处或<em>点击选择文件</em>
      </div>
      <template #tip>
        <div class="el-upload__tip">
          {{ uploadTip || `支持 ${acceptTypes} 文件，文件结构需与集合字段一致` }}
        </div>
      </template>
    </el-upload>
    
    <!-- 额外配置插槽 -->
    <slot name="extra-config"></slot>
    
    <template #footer>
      <el-button @click="handleClose">取消</el-button>
      <el-button
        type="primary"
        @click="handleImport"
        :loading="importing"
        :disabled="selectedFiles.length === 0 || importing"
      >
        导入
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { UploadFilled } from '@element-plus/icons-vue'
import type { UploadFile, UploadInstance } from 'element-plus'

const props = withDefaults(defineProps<{
  visible: boolean
  importing?: boolean
  allowMultiple?: boolean
  maxFiles?: number
  acceptTypes?: string
  uploadTip?: string
}>(), {
  importing: false,
  allowMultiple: false,
  maxFiles: 1,
  acceptTypes: '.csv,.xlsx,.xls',
})

const emit = defineEmits<{
  (e: 'update:visible', value: boolean): void
  (e: 'import', files: File[]): void
}>()

const uploadRef = ref<UploadInstance>()
const selectedFiles = ref<UploadFile[]>([])

// 监听可见性变化，重置文件列表
watch(() => props.visible, (newVal) => {
  if (!newVal) {
    selectedFiles.value = []
    uploadRef.value?.clearFiles()
  }
})

const handleFileChange = (file: UploadFile, fileList: UploadFile[]) => {
  if (props.allowMultiple) {
    selectedFiles.value = fileList
  } else {
    selectedFiles.value = fileList.slice(-1)
  }
}

const handleFileRemove = (file: UploadFile, fileList: UploadFile[]) => {
  selectedFiles.value = fileList
}

const handleImport = () => {
  const files = selectedFiles.value
    .filter(f => f.raw)
    .map(f => f.raw as File)
  
  if (files.length > 0) {
    emit('import', files)
  }
}

const handleClose = () => {
  emit('update:visible', false)
}

// 暴露方法供父组件调用
defineExpose({
  clearFiles: () => {
    selectedFiles.value = []
    uploadRef.value?.clearFiles()
  }
})
</script>
