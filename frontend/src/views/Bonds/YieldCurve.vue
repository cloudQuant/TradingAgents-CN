<template>
  <div class="bonds-yield-curve">
    <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1 class="page-title">
            <el-icon class="title-icon"><Tickets /></el-icon>
            债券 · 收益率曲线
          </h1>
          <p class="page-description">查询与同步国债收益率曲线（多期限点）</p>
        </div>
      </div>
    </div>

    <el-card shadow="hover" class="query-card">
      <template #header>
        <div class="card-header">
          <h3>查询条件</h3>
        </div>
      </template>

      <el-form :inline="true" @submit.prevent>
        <el-form-item label="开始日期">
          <el-date-picker v-model="start" type="date" value-format="YYYY-MM-DD" placeholder="开始日期" />
        </el-form-item>
        <el-form-item label="结束日期">
          <el-date-picker v-model="end" type="date" value-format="YYYY-MM-DD" placeholder="结束日期" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="fetchCurve">查询</el-button>
          <el-button :loading="syncing" @click="syncCurve">同步入库</el-button>
        </el-form-item>
      </el-form>

      <el-alert v-if="message" :title="message" type="info" show-icon :closable="false" style="margin-top: 8px;" />
    </el-card>

    <el-card shadow="hover" class="result-card" style="margin-top: 16px;">
      <template #header>
        <div class="card-header">
          <h3>结果</h3>
        </div>
      </template>

      <div v-if="loading" class="loading">
        <el-skeleton :rows="6" animated />
      </div>
      <div v-else>
        <pre class="result-pre" v-if="text">{{ text }}</pre>
        <el-empty v-else description="暂无数据" />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Tickets } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { bondsApi } from '@/api/bonds'

const start = ref<string | undefined>(undefined)
const end = ref<string | undefined>(undefined)
const loading = ref(false)
const syncing = ref(false)
const text = ref('')
const message = ref('')

const fetchCurve = async () => {
  try {
    loading.value = true
    message.value = ''
    text.value = ''
    const res = await bondsApi.getYieldCurve(start.value, end.value)
    if (res.success) {
      text.value = res.data as unknown as string
      if (!text.value) {
        message.value = '无返回数据'
      }
    } else {
      ElMessage.error(res.message || '查询失败')
    }
  } catch (e) {
    console.error(e)
    ElMessage.error('请求失败')
  } finally {
    loading.value = false
  }
}

const syncCurve = async () => {
  try {
    syncing.value = true
    const res = await bondsApi.syncYieldCurve(start.value, end.value)
    if (res.success) {
      ElMessage.success(`同步完成：saved=${(res.data as any)?.saved ?? '-'} rows=${(res.data as any)?.rows ?? '-'}`)
    } else {
      ElMessage.error(res.message || '同步失败')
    }
  } catch (e) {
    console.error(e)
    ElMessage.error('请求失败')
  } finally {
    syncing.value = false
  }
}
</script>

<style scoped>
.page-title {
  display: flex;
  align-items: center;
  gap: 8px;
}
.title-icon { vertical-align: middle; }
.result-pre {
  background: #0b1020;
  color: #e8eaf6;
  padding: 12px;
  border-radius: 8px;
  white-space: pre-wrap;
}
</style>
