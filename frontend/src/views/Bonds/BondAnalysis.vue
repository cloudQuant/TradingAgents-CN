<template>
  <div class="bond-analysis">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1 class="page-title">
            <el-icon class="title-icon"><Tickets /></el-icon>
            债券分析
          </h1>
          <p class="page-description">
            AI驱动的智能债券分析，多维度评估投资价值与风险
          </p>
        </div>
      </div>
    </div>

    <!-- 主要分析表单 -->
    <div class="analysis-container">
      <el-row :gutter="24">
        <!-- 左侧：基础配置 -->
        <el-col :span="18">
          <el-card class="main-form-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <h3>分析配置</h3>
                <el-tag type="info" size="small">必填信息</el-tag>
              </div>
            </template>

            <el-form :model="analysisForm" label-width="100px" class="analysis-form">
              <!-- 债券信息 -->
              <div class="form-section">
                <h4 class="section-title">📊 债券信息</h4>
                <el-row :gutter="16">
                  <el-col :span="12">
                    <el-form-item label="债券代码" required>
                      <el-input
                        v-model="analysisForm.bondCode"
                        placeholder="如：110062.SH、123456.SZ"
                        clearable
                        size="large"
                        class="bond-input"
                        :class="{ 'is-error': bondCodeError }"
                        @blur="validateBondCodeInput"
                        @input="onBondCodeInput"
                      >
                        <template #prefix>
                          <el-icon><Tickets /></el-icon>
                        </template>
                      </el-input>
                      <div v-if="bondCodeError" class="error-message">
                        <el-icon><WarningFilled /></el-icon>
                        {{ bondCodeError }}
                      </div>
                      <div v-else-if="bondCodeHelp" class="help-message">
                        <el-icon><InfoFilled /></el-icon>
                        {{ bondCodeHelp }}
                      </div>
                    </el-form-item>
                  </el-col>
                  <el-col :span="12">
                    <el-form-item label="债券类型">
                      <el-select
                        v-model="analysisForm.bondType"
                        placeholder="选择债券类型"
                        size="large"
                        style="width: 100%"
                        @change="onBondTypeChange"
                      >
                        <el-option label="可转债" value="convertible" />
                        <el-option label="可交债" value="exchangeable" />
                        <el-option label="利率债" value="interest" />
                        <el-option label="信用债" value="credit" />
                        <el-option label="其他" value="other" />
                      </el-select>
                    </el-form-item>
                  </el-col>
                </el-row>

                <el-form-item label="分析日期">
                  <el-date-picker
                    v-model="analysisForm.analysisDate"
                    type="date"
                    placeholder="选择分析基准日期"
                    size="large"
                    style="width: 100%"
                    :disabled-date="disabledDate"
                  />
                </el-form-item>
              </div>

              <!-- 分析深度 -->
              <div class="form-section">
                <h4 class="section-title">🎯 分析深度</h4>
                <div class="depth-selector">
                  <div
                    v-for="(depth, index) in depthOptions"
                    :key="index"
                    class="depth-option"
                    :class="{ active: analysisForm.researchDepth === index + 1 }"
                    @click="analysisForm.researchDepth = index + 1"
                  >
                    <div class="depth-icon">{{ depth.icon }}</div>
                    <div class="depth-info">
                      <div class="depth-name">{{ depth.name }}</div>
                      <div class="depth-desc">{{ depth.description }}</div>
                      <div class="depth-time">{{ depth.time }}</div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- 分析维度 -->
              <div class="form-section">
                <h4 class="section-title">📈 分析维度</h4>
                <div class="analysts-grid">
                  <div
                    v-for="dimension in ANALYSIS_DIMENSIONS"
                    :key="dimension.id"
                    class="analyst-card"
                    :class="{ 
                      active: analysisForm.selectedDimensions.includes(dimension.id)
                    }"
                    @click="toggleDimension(dimension.id)"
                  >
                    <div class="analyst-avatar">
                      <el-icon>
                        <component :is="dimension.icon" />
                      </el-icon>
                    </div>
                    <div class="analyst-content">
                      <div class="analyst-name">{{ dimension.name }}</div>
                      <div class="analyst-desc">{{ dimension.description }}</div>
                    </div>
                    <div class="analyst-check">
                      <el-icon v-if="analysisForm.selectedDimensions.includes(dimension.id)" class="check-icon">
                        <Check />
                      </el-icon>
                    </div>
                  </div>
                </div>
              </div>

              <!-- 操作按钮 -->
              <div class="form-section">
                <div class="action-buttons" style="display: flex; justify-content: center; align-items: center; width: 100%; text-align: center;">
                  <el-button
                    v-if="analysisStatus === 'idle'"
                    type="primary"
                    size="large"
                    @click="submitAnalysis"
                    :loading="submitting"
                    :disabled="!analysisForm.bondCode.trim()"
                    class="submit-btn large-analysis-btn"
                    style="width: 280px; height: 56px; font-size: 18px; font-weight: 700; border-radius: 16px;"
                  >
                    <el-icon><TrendCharts /></el-icon>
                    开始智能分析
                  </el-button>

                  <el-button
                    v-else-if="analysisStatus === 'running'"
                    type="warning"
                    size="large"
                    disabled
                    class="submit-btn large-analysis-btn"
                    style="width: 280px; height: 56px; font-size: 18px; font-weight: 700; border-radius: 16px;"
                  >
                    <el-icon><Loading /></el-icon>
                    分析进行中...
                  </el-button>

                  <div v-else-if="analysisStatus === 'completed'" style="display: flex; gap: 12px;">
                    <el-button
                      type="success"
                      size="large"
                      @click="showResults = !showResults"
                      class="submit-btn"
                      style="width: 180px; height: 56px; font-size: 16px; font-weight: 700; border-radius: 16px;"
                    >
                      <el-icon><Document /></el-icon>
                      {{ showResults ? '隐藏结果' : '查看结果' }}
                    </el-button>

                    <el-button
                      type="primary"
                      size="large"
                      @click="restartAnalysis"
                      class="submit-btn"
                      style="width: 180px; height: 56px; font-size: 16px; font-weight: 700; border-radius: 16px;"
                    >
                      <el-icon><Refresh /></el-icon>
                      重新分析
                    </el-button>
                  </div>

                  <el-button
                    v-else-if="analysisStatus === 'failed'"
                    type="danger"
                    size="large"
                    @click="restartAnalysis"
                    class="submit-btn large-analysis-btn"
                    style="width: 280px; height: 56px; font-size: 18px; font-weight: 700; border-radius: 16px;"
                  >
                    <el-icon><Refresh /></el-icon>
                    重新分析
                  </el-button>
                </div>
              </div>

              <!-- 分析进度显示 -->
              <div v-if="analysisStatus === 'running'" class="progress-section">
                <el-card class="progress-card" shadow="hover">
                  <template #header>
                    <div class="progress-header">
                      <h4>
                        <el-icon class="rotating-icon">
                          <Loading />
                        </el-icon>
                        分析进行中...
                      </h4>
                    </div>
                  </template>

                  <div class="progress-content">
                    <div class="overall-progress-info">
                      <div class="progress-stats">
                        <div class="stat-item">
                          <div class="stat-label">已用时间</div>
                          <div class="stat-value">{{ formatTime(progressInfo.elapsedTime) }}</div>
                        </div>
                        <div class="stat-item">
                          <div class="stat-label">预计剩余</div>
                          <div class="stat-value">{{ formatTime(progressInfo.remainingTime) }}</div>
                        </div>
                      </div>
                    </div>

                    <div class="progress-bar-section">
                      <el-progress
                        :percentage="Math.round(progressInfo.progress)"
                        :stroke-width="12"
                        :show-text="true"
                        :status="getProgressStatus()"
                        class="main-progress-bar"
                      />
                    </div>

                    <div class="current-task-info">
                      <div class="task-title">
                        <el-icon class="task-icon">
                          <Loading />
                        </el-icon>
                        {{ progressInfo.currentStep || '正在初始化分析引擎...' }}
                      </div>
                    </div>
                  </div>
                </el-card>
              </div>
            </el-form>
          </el-card>
        </el-col>

        <!-- 右侧：提示信息 -->
        <el-col :span="6">
          <el-card class="tips-card" shadow="hover">
            <template #header>
              <h3>💡 使用提示</h3>
            </template>
            <div class="tips-content">
              <el-alert
                title="债券代码格式"
                type="info"
                :closable="false"
                show-icon
                style="margin-bottom: 16px;"
              >
                <template #default>
                  <div style="font-size: 12px; line-height: 1.6;">
                    <p>• 上交所：代码.SH（如：110062.SH）</p>
                    <p>• 深交所：代码.SZ（如：123456.SZ）</p>
                    <p>• 银行间：代码.IB（如：210001.IB）</p>
                  </div>
                </template>
              </el-alert>

              <el-alert
                title="分析维度说明"
                type="info"
                :closable="false"
                show-icon
                style="margin-bottom: 16px;"
              >
                <template #default>
                  <div style="font-size: 12px; line-height: 1.6;">
                    <p><strong>基本面分析：</strong>债券基本信息、发行人信用状况</p>
                    <p><strong>技术分析：</strong>价格走势、成交量、技术指标</p>
                    <p><strong>估值分析：</strong>收益率、久期、凸性等</p>
                    <p><strong>可转债分析：</strong>转股溢价率、纯债价值等</p>
                  </div>
                </template>
              </el-alert>

              <el-alert
                title="分析深度"
                type="warning"
                :closable="false"
                show-icon
              >
                <template #default>
                  <div style="font-size: 12px; line-height: 1.6;">
                    <p>• <strong>快速分析：</strong>基础数据，约1-2分钟</p>
                    <p>• <strong>标准分析：</strong>完整分析，约3-5分钟</p>
                    <p>• <strong>深度分析：</strong>全面分析，约5-10分钟</p>
                  </div>
                </template>
              </el-alert>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <!-- 分析结果展示 -->
      <div v-if="showResults && analysisResults" class="results-section">
        <el-card class="results-card" shadow="hover">
          <template #header>
            <div class="results-header">
              <h3>📊 分析结果</h3>
              <div class="results-actions">
                <el-button size="small" @click="exportResults">导出报告</el-button>
                <el-button size="small" type="primary" @click="applyToTrading">应用到交易</el-button>
              </div>
            </div>
          </template>

          <div class="results-content">
            <!-- 债券基本信息 -->
            <div class="result-section">
              <h4 class="section-title">债券基本信息</h4>
              <el-descriptions :column="3" border>
                <el-descriptions-item label="债券代码">{{ analysisResults.bond_code || '-' }}</el-descriptions-item>
                <el-descriptions-item label="债券名称">{{ analysisResults.bond_name || '-' }}</el-descriptions-item>
                <el-descriptions-item label="债券类型">{{ analysisResults.bond_type || '-' }}</el-descriptions-item>
                <el-descriptions-item label="当前价格">{{ formatPrice(analysisResults.current_price) }}</el-descriptions-item>
                <el-descriptions-item label="涨跌幅">{{ formatPercent(analysisResults.price_change_percent) }}</el-descriptions-item>
                <el-descriptions-item label="到期日">{{ analysisResults.maturity_date || '-' }}</el-descriptions-item>
              </el-descriptions>
            </div>

            <!-- 投资建议 -->
            <div class="result-section">
              <h4 class="section-title">投资建议</h4>
              <el-alert
                :title="getRecommendationTitle()"
                :type="getRecommendationType()"
                :closable="false"
                show-icon
                style="margin-bottom: 16px;"
              >
                <template #default>
                  <div v-html="formatRecommendation(analysisResults.recommendation)"></div>
                </template>
              </el-alert>
            </div>

            <!-- 分析摘要 -->
            <div class="result-section" v-if="analysisResults.summary">
              <h4 class="section-title">分析摘要</h4>
              <div class="markdown-content" v-html="formatMarkdown(analysisResults.summary)"></div>
            </div>

            <!-- 详细分析 -->
            <div class="result-section" v-if="analysisResults.fundamental_analysis">
              <h4 class="section-title">基本面分析</h4>
              <div class="markdown-content" v-html="formatMarkdown(analysisResults.fundamental_analysis)"></div>
            </div>

            <div class="result-section" v-if="analysisResults.technical_analysis">
              <h4 class="section-title">技术分析</h4>
              <div class="markdown-content" v-html="formatMarkdown(analysisResults.technical_analysis)"></div>
            </div>

            <div class="result-section" v-if="analysisResults.valuation_analysis">
              <h4 class="section-title">估值分析</h4>
              <div class="markdown-content" v-html="formatMarkdown(analysisResults.valuation_analysis)"></div>
            </div>

            <div class="result-section" v-if="analysisResults.convertible_analysis">
              <h4 class="section-title">可转债分析</h4>
              <div class="markdown-content" v-html="formatMarkdown(analysisResults.convertible_analysis)"></div>
            </div>

            <div class="result-section" v-if="analysisResults.risk_assessment">
              <h4 class="section-title">风险评估</h4>
              <div class="markdown-content" v-html="formatMarkdown(analysisResults.risk_assessment)"></div>
            </div>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Tickets, TrendCharts, Document, Refresh, Loading, WarningFilled, InfoFilled, Check } from '@element-plus/icons-vue'
// DataAnalysis, Switch - used in dynamic icons
import { ElMessage } from 'element-plus'
import { bondsApi } from '@/api/bonds'
import dayjs from 'dayjs'
import { marked } from 'marked'

// 分析维度配置
const ANALYSIS_DIMENSIONS = [
  {
    id: 'fundamental',
    name: '基本面分析',
    description: '债券基本信息、发行人信用状况',
    icon: 'Document'
  },
  {
    id: 'technical',
    name: '技术分析',
    description: '价格走势、成交量、技术指标',
    icon: 'TrendCharts'
  },
  {
    id: 'valuation',
    name: '估值分析',
    description: '收益率、久期、凸性等',
    icon: 'DataAnalysis'
  },
  {
    id: 'convertible',
    name: '可转债分析',
    description: '转股溢价率、纯债价值等',
    icon: 'Switch'
  }
]

// 分析深度选项
const depthOptions = [
  {
    icon: '⚡',
    name: '快速分析',
    description: '基础数据，快速评估',
    time: '约1-2分钟'
  },
  {
    icon: '📊',
    name: '标准分析',
    description: '完整分析，全面评估',
    time: '约3-5分钟'
  },
  {
    icon: '🔍',
    name: '深度分析',
    description: '全面分析，深入评估',
    time: '约5-10分钟'
  }
]

// 表单数据
const analysisForm = ref({
  bondCode: '',
  bondType: '',
  analysisDate: new Date(),
  researchDepth: 2, // 默认标准分析
  selectedDimensions: ['fundamental', 'technical', 'valuation'] // 默认选择
})

// 状态
const analysisStatus = ref<'idle' | 'running' | 'completed' | 'failed'>('idle')
const submitting = ref(false)
const showResults = ref(false)
const bondCodeError = ref('')
const bondCodeHelp = ref('')
const currentTaskId = ref('')

// 进度信息
const progressInfo = ref({
  progress: 0,
  currentStep: '',
  elapsedTime: 0,
  remainingTime: 0
})

// 分析结果
const analysisResults = ref<any>(null)

// 方法
const validateBondCodeInput = () => {
  const code = analysisForm.value.bondCode.trim()
  if (!code) {
    bondCodeError.value = '请输入债券代码'
    return false
  }
  
  // 验证债券代码格式
  const pattern = /^(\d{6})\.(SH|SZ|IB)$/i
  if (!pattern.test(code)) {
    bondCodeError.value = '债券代码格式不正确，应为：代码.交易所（如：110062.SH）'
    return false
  }
  
  bondCodeError.value = ''
  return true
}

const onBondCodeInput = () => {
  bondCodeError.value = ''
  const code = analysisForm.value.bondCode.trim()
  if (code && /^(\d{6})\.(SH|SZ|IB)$/i.test(code)) {
    bondCodeHelp.value = '债券代码格式正确'
  } else {
    bondCodeHelp.value = ''
  }
}

const onBondTypeChange = () => {
  // 根据债券类型自动调整分析维度
  if (analysisForm.value.bondType === 'convertible' || analysisForm.value.bondType === 'exchangeable') {
    if (!analysisForm.value.selectedDimensions.includes('convertible')) {
      analysisForm.value.selectedDimensions.push('convertible')
    }
  }
}

const toggleDimension = (dimensionId: string) => {
  const index = analysisForm.value.selectedDimensions.indexOf(dimensionId)
  if (index > -1) {
    analysisForm.value.selectedDimensions.splice(index, 1)
  } else {
    analysisForm.value.selectedDimensions.push(dimensionId)
  }
}

const disabledDate = (time: Date) => {
  return time.getTime() > Date.now()
}

const submitAnalysis = async () => {
  if (!validateBondCodeInput()) {
    return
  }

  if (analysisForm.value.selectedDimensions.length === 0) {
    ElMessage.warning('请至少选择一个分析维度')
    return
  }

  submitting.value = true
  analysisStatus.value = 'running'
  showResults.value = false
  analysisResults.value = null

  try {
    const request = {
      bond_code: analysisForm.value.bondCode.trim(),
      parameters: {
        bond_type: analysisForm.value.bondType,
        analysis_date: dayjs(analysisForm.value.analysisDate).format('YYYY-MM-DD'),
        research_depth: getDepthDescription(analysisForm.value.researchDepth),
        selected_dimensions: analysisForm.value.selectedDimensions
      }
    }

    const response = await bondsApi.startAnalysis(request)
    
    if (response.success && response.data) {
      currentTaskId.value = response.data.task_id
      ElMessage.success('分析任务已提交，正在处理中...')
      
      // 开始轮询任务状态
      startPolling()
    } else {
      throw new Error(response.message || '提交分析任务失败')
    }
  } catch (error: any) {
    console.error('提交分析失败:', error)
    ElMessage.error('提交分析失败: ' + (error.message || '未知错误'))
    analysisStatus.value = 'failed'
  } finally {
    submitting.value = false
  }
}

const startPolling = () => {
  const startTime = Date.now()
  const pollInterval = setInterval(async () => {
    try {
      const response = await bondsApi.getAnalysisStatus(currentTaskId.value)
      
      if (response.success && response.data) {
        const status = response.data.status
        progressInfo.value = {
          progress: response.data.progress || 0,
          currentStep: response.data.current_step || '',
          elapsedTime: Math.floor((Date.now() - startTime) / 1000),
          remainingTime: estimateRemainingTime(response.data.progress || 0, Date.now() - startTime)
        }

        if (status === 'completed') {
          clearInterval(pollInterval)
          analysisStatus.value = 'completed'
          
          // 获取分析结果
          const resultResponse = await bondsApi.getAnalysisResult(currentTaskId.value)
          if (resultResponse.success && resultResponse.data) {
            analysisResults.value = resultResponse.data
            showResults.value = true
            ElMessage.success('分析完成！')
          }
        } else if (status === 'failed') {
          clearInterval(pollInterval)
          analysisStatus.value = 'failed'
          ElMessage.error('分析失败: ' + (response.data.error || '未知错误'))
        }
      }
    } catch (error) {
      console.error('轮询状态失败:', error)
    }
  }, 2000) // 每2秒轮询一次
}

const estimateRemainingTime = (progress: number, elapsed: number): number => {
  if (progress <= 0) return 0
  const total = (elapsed / progress) * 100
  return Math.max(0, Math.floor((total - elapsed) / 1000))
}

const getDepthDescription = (depth: number): string => {
  const descriptions = ['快速', '标准', '深度']
  return descriptions[depth - 1] || '标准'
}

const restartAnalysis = () => {
  analysisStatus.value = 'idle'
  showResults.value = false
  analysisResults.value = null
  currentTaskId.value = ''
  progressInfo.value = {
    progress: 0,
    currentStep: '',
    elapsedTime: 0,
    remainingTime: 0
  }
}

const formatTime = (seconds: number): string => {
  if (seconds < 60) return `${seconds}秒`
  const minutes = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${minutes}分${secs}秒`
}

type ProgressStatus = '' | 'success' | 'warning' | 'exception'
const getProgressStatus = (): ProgressStatus => {
  if (progressInfo.value.progress >= 100) return 'success'
  if (progressInfo.value.progress >= 50) return ''
  return 'exception'
}

const formatPrice = (price: number | null | undefined): string => {
  if (price === null || price === undefined) return '-'
  return price.toFixed(4)
}

const formatPercent = (percent: number | null | undefined): string => {
  if (percent === null || percent === undefined) return '-'
  return `${percent >= 0 ? '+' : ''}${percent.toFixed(2)}%`
}

const formatMarkdown = (text: string): string => {
  if (!text) return ''
  const result = marked(text)
  return typeof result === 'string' ? result : text
}

const formatRecommendation = (recommendation: string): string => {
  if (!recommendation) return ''
  return formatMarkdown(recommendation)
}

const getRecommendationTitle = (): string => {
  if (!analysisResults.value?.recommendation) return '暂无建议'
  const rec = analysisResults.value.recommendation.toLowerCase()
  if (rec.includes('买入') || rec.includes('buy')) return '买入建议'
  if (rec.includes('卖出') || rec.includes('sell')) return '卖出建议'
  if (rec.includes('持有') || rec.includes('hold')) return '持有建议'
  return '投资建议'
}

type AlertType = 'success' | 'warning' | 'info' | 'error'
const getRecommendationType = (): AlertType => {
  if (!analysisResults.value?.recommendation) return 'info'
  const rec = analysisResults.value.recommendation.toLowerCase()
  if (rec.includes('买入') || rec.includes('buy')) return 'success'
  if (rec.includes('卖出') || rec.includes('sell')) return 'error'
  if (rec.includes('持有') || rec.includes('hold')) return 'warning'
  return 'info'
}

const exportResults = () => {
  ElMessage.info('导出功能开发中...')
}

const applyToTrading = () => {
  ElMessage.info('应用到交易功能开发中...')
}

onMounted(() => {
  // 设置默认分析日期为今天
  analysisForm.value.analysisDate = new Date()
})
</script>

<style scoped>
.bond-analysis {
  padding: 20px;
}

.page-header {
  margin-bottom: 24px;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
  font-size: 24px;
  font-weight: 600;
}

.title-icon {
  font-size: 28px;
  color: #409eff;
}

.page-description {
  margin: 8px 0 0 0;
  color: #909399;
  font-size: 14px;
}

.analysis-container {
  max-width: 1400px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.form-section {
  margin-bottom: 32px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 16px;
  color: #303133;
}

.depth-selector {
  display: flex;
  gap: 16px;
}

.depth-option {
  flex: 1;
  padding: 16px;
  border: 2px solid #e4e7ed;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.depth-option:hover {
  border-color: #409eff;
}

.depth-option.active {
  border-color: #409eff;
  background-color: #ecf5ff;
}

.depth-icon {
  font-size: 32px;
  text-align: center;
  margin-bottom: 8px;
}

.depth-info {
  text-align: center;
}

.depth-name {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 4px;
}

.depth-desc {
  font-size: 12px;
  color: #909399;
  margin-bottom: 4px;
}

.depth-time {
  font-size: 12px;
  color: #409eff;
}

.analysts-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.analyst-card {
  display: flex;
  align-items: center;
  padding: 16px;
  border: 2px solid #e4e7ed;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.analyst-card:hover {
  border-color: #409eff;
}

.analyst-card.active {
  border-color: #409eff;
  background-color: #ecf5ff;
}

.analyst-avatar {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f7fa;
  border-radius: 50%;
  margin-right: 12px;
  font-size: 24px;
}

.analyst-content {
  flex: 1;
}

.analyst-name {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 4px;
}

.analyst-desc {
  font-size: 12px;
  color: #909399;
}

.analyst-check {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.check-icon {
  color: #409eff;
  font-size: 20px;
}

.error-message {
  color: #f56c6c;
  font-size: 12px;
  margin-top: 4px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.help-message {
  color: #909399;
  font-size: 12px;
  margin-top: 4px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.progress-section {
  margin-top: 24px;
}

.progress-header h4 {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
}

.rotating-icon {
  animation: rotate 2s linear infinite;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.progress-stats {
  display: flex;
  gap: 24px;
  margin-bottom: 16px;
}

.stat-item {
  flex: 1;
}

.stat-label {
  font-size: 12px;
  color: #909399;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.results-section {
  margin-top: 24px;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.results-content {
  padding: 16px 0;
}

.result-section {
  margin-bottom: 32px;
}

.markdown-content {
  line-height: 1.8;
  color: #303133;
}

.markdown-content :deep(h1),
.markdown-content :deep(h2),
.markdown-content :deep(h3) {
  margin-top: 16px;
  margin-bottom: 8px;
  font-weight: 600;
}

.markdown-content :deep(p) {
  margin-bottom: 12px;
}

.markdown-content :deep(ul),
.markdown-content :deep(ol) {
  margin-bottom: 12px;
  padding-left: 24px;
}

.markdown-content :deep(li) {
  margin-bottom: 4px;
}

.tips-content {
  font-size: 14px;
}
</style>

