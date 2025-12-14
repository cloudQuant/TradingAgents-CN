# 股票详情页分析报告展示功能修复

## 📋 问题描述

### 原始问题

前端股票详情页可以获取到该股票的分析报告，但是没有展示出来。

### 问题分析

#### 1. 后端数据格式 ✅ 正确

通过测试脚本 `scripts/test_stock_detail_reports.py` 验证，后端 API 返回的数据格式完全正确：

```json
{
  "success": true,
  "data": {
    "analysis_id": "...",
    "stock_symbol": "002475",
    "analysis_date": "2025-09-30",
    "summary": "...",
    "recommendation": "...",
    "confidence_score": 0.9,
    "reports": {
      "market_report": "# 002475 股票技术分析报告\n\n...",
      "fundamentals_report": "### 1. **公司基本信息分析...",
      "investment_plan": "我们来一场真正意义上的投资决策辩论...",
      "trader_investment_plan": "最终交易建议: **卖出**\n\n...",
      "final_trade_decision": "---\n\n## 📌 **最终决策...",
      "research_team_decision": "我们来一场真正意义上的投资决策辩论...",
      "risk_management_decision": "---\n\n## 📌 **最终决策..."
    }
  }
}

```bash

- *reports 字段包含 7 个详细报告**：
- `market_report` - 📈 市场分析
- `fundamentals_report` - 📊 基本面分析
- `investment_plan` - 💼 投资计划
- `trader_investment_plan` - 🎯 交易员计划
- `final_trade_decision` - ✅ 最终决策
- `research_team_decision` - 🔬 研究团队决策
- `risk_management_decision` - ⚠️ 风险管理决策

#### 2. 前端展示问题 ❌ 缺失

前端股票详情页（`frontend/src/views/Stocks/Detail.vue`）只显示了：

- `summary` - 分析摘要
- `recommendation` - 投资建议
- `confidence_score` - 信心度

- *但没有展示 `reports` 字段中的详细报告内容！**

- --

## ✅ 解决方案

### 修改内容

#### 1. 添加报告展示区域

在分析结果卡片中添加报告预览和"查看完整报告"按钮：

```vue
<!-- 详细报告展示 -->
<div v-if="lastAnalysis?.reports && Object.keys(lastAnalysis.reports).length > 0" class="reports-section">
  <el-divider />
  <div class="reports-header">
    <span class="reports-title">📊 详细分析报告 ({{ Object.keys(lastAnalysis.reports).length }})</span>
    <el-button
      text
      type="primary"
      @click="showReportsDialog = true"
      :icon="Document"
    >
      查看完整报告
    </el-button>
  </div>

  <!-- 报告列表预览 -->
  <div class="reports-preview">
    <el-tag
      v-for="(content, key) in lastAnalysis.reports"
      :key="key"
      size="small"
      effect="plain"
      class="report-tag"
    >
      {{ formatReportName(key) }}
    </el-tag>
  </div>
</div>

```bash

#### 2. 添加报告对话框

使用 Element Plus 的 Dialog 和 Tabs 组件展示详细报告：

```vue
<!-- 详细报告对话框 -->
<el-dialog
  v-model="showReportsDialog"
  title="📊 详细分析报告"
  width="80%"
  :close-on-click-modal="false"
  class="reports-dialog"
>
  <el-tabs v-model="activeReportTab" type="border-card">
    <el-tab-pane
      v-for="(content, key) in lastAnalysis?.reports"
      :key="key"
      :label="formatReportName(key)"
      :name="key"
    >
      <div class="report-content">
        <el-scrollbar height="500px">
          <div class="markdown-body" v-html="renderMarkdown(content)"></div>
        </el-scrollbar>
      </div>
    </el-tab-pane>
  </el-tabs>

  <template #footer>
    <el-button @click="showReportsDialog = false">关闭</el-button>
    <el-button type="primary" @click="exportReport">导出报告</el-button>
  </template>
</el-dialog>

```bash

#### 3. 添加辅助函数

- *格式化报告名称**：

```typescript
function formatReportName(key: string): string {
  const nameMap: Record<string, string> = {
    'market_report': '📈 市场分析',
    'fundamentals_report': '📊 基本面分析',
    'sentiment_report': '💭 情绪分析',
    'news_report': '📰 新闻分析',
    'investment_plan': '💼 投资计划',
    'trader_investment_plan': '🎯 交易员计划',
    'final_trade_decision': '✅ 最终决策',
    'research_team_decision': '🔬 研究团队决策',
    'risk_management_decision': '⚠️ 风险管理决策'
  }
  return nameMap[key] || key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())

}

```bash

- *渲染 Markdown**：

```typescript
function renderMarkdown(content: string): string {
  if (!content) return '<p>暂无内容</p>'
  try {
    return marked(content)
  } catch (e) {
    console.error('Markdown 渲染失败:', e)
    return `<pre>${content}</pre>`
  }
}

```bash

- *导出报告**：

```typescript
function exportReport() {
  if (!lastAnalysis.value?.reports) {
    ElMessage.warning('暂无报告可导出')
    return
  }

  // 生成 Markdown 格式的完整报告
  let fullReport = `# ${code.value} 股票分析报告\n\n`
  fullReport += `**分析日期**: ${lastAnalysis.value.analysis_date}\n`
  fullReport += `**投资建议**: ${lastAnalysis.value.recommendation}\n`
  fullReport += `**信心度**: ${fmtConf(lastAnalysis.value.confidence_score)}\n\n`
  fullReport += `---\n\n`

  for (const [key, content] of Object.entries(lastAnalysis.value.reports)) {
    fullReport += `## ${formatReportName(key)}\n\n`
    fullReport += `${content}\n\n`
    fullReport += `---\n\n`
  }

  // 创建下载链接
  const blob = new Blob([fullReport], { type: 'text/markdown;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = `${code.value}_分析报告_${lastAnalysis.value.analysis_date}.md`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)

  ElMessage.success('报告已导出')
}

```bash

- --

## 🧪 测试步骤

### 1. 运行测试脚本验证后端数据

```bash
.\.venv\Scripts\python scripts/test_stock_detail_reports.py

```bash

- *预期输出**：

```bash
✅ 所有测试通过
✅ 测试完成：前后端数据格式一致
📊 可展示的报告数量: 7/7

```bash

### 2. 启动前端开发服务器

```bash
cd frontend
npm run dev

```bash

### 3. 访问股票详情页

打开浏览器访问：

```bash
<http://localhost:5173/stocks/002475>

```bash

### 4. 验证功能

#### ✅ 应该看到：

1. **分析结果卡片**显示：
   - 投资建议标签
   - 信心度
   - 分析日期
   - 分析摘要

1. **详细报告区域**显示：
   - "📊 详细分析报告 (7)" 标题
   - "查看完整报告" 按钮
   - 7 个报告标签预览

1. **点击"查看完整报告"按钮**后：
   - 弹出对话框
   - 显示 7 个标签页
   - 每个标签页显示对应的 Markdown 格式报告
   - 报告内容格式化良好（标题、列表、表格等）

1. **点击"导出报告"按钮**后：
   - 下载一个 Markdown 文件
   - 文件名格式：`002475_分析报告_2025-09-30.md`
   - 文件包含所有报告内容

- --

## 📊 功能特性

### 1. 报告预览

- 在分析结果卡片中显示报告数量
- 显示所有报告的标签列表
- 一键打开完整报告对话框

### 2. 报告展示

- 使用标签页组织多个报告
- Markdown 格式渲染
- 滚动条支持长内容
- 响应式设计

### 3. 报告导出

- 导出为 Markdown 格式
- 包含所有报告内容
- 自动命名（股票代码_分析日期）

### 4. 样式优化

- 美观的 Markdown 渲染样式
- 标题、列表、表格、代码块等格式化
- 深色/浅色主题适配

- --

## 🎯 技术要点

### 1. 数据流

```bash
后端 API (/api/analysis/tasks/{task_id}/result)
  ↓
前端 API 调用 (analysisApi.getTaskResult)
  ↓
存储到 lastAnalysis.value
  ↓
模板渲染 (v-if="lastAnalysis?.reports")
  ↓
用户交互 (查看/导出)

```bash

### 2. 关键依赖

- `marked` - Markdown 渲染库（已安装）
- `Element Plus` - UI 组件库
- `Vue 3` - 响应式框架

### 3. 兼容性

- 兼容旧数据（没有 reports 字段时不显示）
- 兼容不同报告类型
- 兼容空报告内容

- --

## 📝 提交信息

```bash
feat: 股票详情页添加分析报告展示功能

- 添加报告预览区域，显示报告数量和标签列表
- 添加"查看完整报告"对话框，使用标签页展示多个报告
- 支持 Markdown 格式渲染
- 添加报告导出功能（Markdown 格式）
- 优化报告展示样式

修复问题：前端股票详情页可以获取到分析报告但没有展示

```bash

- --

## 🔍 相关文件

### 修改的文件

- `frontend/src/views/Stocks/Detail.vue` - 股票详情页主文件

### 测试脚本

- `scripts/test_stock_detail_reports.py` - 后端数据格式测试

### 文档

- `docs/STOCK_DETAIL_REPORTS_FIX.md` - 本文档
