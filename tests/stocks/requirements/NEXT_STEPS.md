# 股票数据集合API更新功能 - 下一步工作指南

## 当前状态

### 已完成 ✅
1. **后端API端点**：文件上传、远程同步、刷新、清空
2. **后端Service**：文件导入和远程同步逻辑
3. **前端API**：uploadData和syncData方法
4. **前端UI**：文件导入对话框、远程同步对话框
5. **配置框架**：collectionRefreshConfig.ts已创建

### 待完成 ⏳
**带参数的API更新功能**：需要修改Collection.vue，添加参数输入对话框

## 快速完成方案

由于时间限制，推荐使用**方案B（简化JSON输入）**，这样可以在30分钟内完成：

### 具体实现步骤

#### 步骤1：修改Collection.vue（约20分钟）

需要修改3个地方：

**位置1：添加状态变量**（约在第329行附近）
```typescript
// 对话框相关
const overviewDialogVisible = ref(false)
const apiParamsDialogVisible = ref(false)  // 新增

// API参数相关（新增）
const refreshMode = ref<'all' | 'params'>('all')
const refreshParamsJson = ref('')
```

**位置2：修改更新数据按钮**（约在第16行）
```vue
<!-- 原来的 -->
<el-button :icon="Download" type="primary" @click="handleRefreshData" :loading="refreshing">更新数据</el-button>

<!-- 改为 -->
<el-dropdown @command="handleUpdateCommand" :loading="refreshing">
  <el-button :icon="Download" type="primary" :loading="refreshing">
    更新数据<el-icon class="el-icon--right"><arrow-down /></el-icon>
  </el-button>
  <template #dropdown>
    <el-dropdown-menu>
      <el-dropdown-item command="api">API更新</el-dropdown-item>
      <el-dropdown-item command="file">文件导入</el-dropdown-item>
      <el-dropdown-item command="sync">远程同步</el-dropdown-item>
    </el-dropdown-menu>
  </template>
</el-dropdown>
```

**位置3：添加处理函数和对话框**（约在第574行showOverview函数之后）
```typescript
// 处理更新数据菜单
const handleUpdateCommand = (command: string) => {
  if (command === 'api') {
    apiParamsDialogVisible.value = true
    refreshMode.value = 'all'
    refreshParamsJson.value = ''
  } else if (command === 'file') {
    // 文件导入逻辑已存在
  } else if (command === 'sync') {
    // 远程同步逻辑已存在
  }
}

// 提交API更新
const handleSubmitApiRefresh = () => {
  let params = {}
  
  if (refreshMode.value === 'params') {
    try {
      params = JSON.parse(refreshParamsJson.value)
    } catch (e) {
      ElMessage.error('JSON格式错误，请检查输入')
      return
    }
  }
  
  apiParamsDialogVisible.value = false
  handleRefreshData(params)
}

// 修改handleRefreshData支持参数
const handleRefreshData = async (params: any = {}) => {
  const name = collectionName.value
  if (!name) return
  
  try {
    refreshing.value = true
    const res = await stocksApi.refreshCollection(name, params)
    currentTaskId.value = res.data.task_id
    ElMessage.success('刷新任务已启动')
    startStatusPolling()
  } catch (error: any) {
    console.error('启动刷新任务失败', error)
    ElMessage.error(error.response?.data?.detail || '启动刷新任务失败')
    refreshing.value = false
  }
}
```

**位置4：添加参数对话框**（在第167行数据概览对话框之后）
```vue
<!-- API参数对话框 -->
<el-dialog
  v-model="apiParamsDialogVisible"
  title="API更新"
  width="600px"
  :close-on-click-modal="false"
>
  <el-radio-group v-model="refreshMode" style="margin-bottom: 20px">
    <el-radio label="all">更新全部数据</el-radio>
    <el-radio label="params">带参数更新</el-radio>
  </el-radio-group>

  <el-form v-if="refreshMode === 'params'" label-width="100px">
    <el-form-item label="参数（JSON）">
      <el-input
        v-model="refreshParamsJson"
        type="textarea"
        :rows="6"
        placeholder='输入JSON格式参数，例如：
{
  "symbol": "000001,000002",
  "adjust": "qfq"
}'
      />
    </el-form-item>
    <el-alert
      title="提示：参数格式需与后端API接口一致，具体参数请参考需求文档"
      type="info"
      :closable="false"
    />
  </el-form>

  <el-alert
    v-else
    title="将更新所有数据，可能需要较长时间，请耐心等待"
    type="warning"
    :closable="false"
  />

  <template #footer>
    <el-button @click="apiParamsDialogVisible = false">取消</el-button>
    <el-button type="primary" @click="handleSubmitApiRefresh" :loading="refreshing">
      开始更新
    </el-button>
  </template>
</el-dialog>
```

**步骤2：添加ArrowDown图标导入**（约在第187行）
```typescript
import { Box, Refresh, Delete, Download, Search, QuestionFilled, ArrowDown, UploadFilled } from '@element-plus/icons-vue'
```

#### 步骤2：测试（约10分钟）

1. 测试无参数更新：选择"更新全部数据"
2. 测试带参数更新：输入JSON参数，如 `{"symbol": "000001"}`
3. 测试文件导入和远程同步功能是否正常

#### 步骤3：标记需求文档（约5分钟）

完成测试后，对于以下情况标记finished：
1. 不需要参数的集合：直接可以标记
2. 需要参数的集合：测试JSON输入方式可用后标记

## 标记Finished的标准

一个需求文档可以标记finished需要满足：
1. ✅ 后端API接口已实现
2. ✅ 前端页面可以访问
3. ✅ 三种更新方式都可用：
   - 文件导入
   - 远程同步
   - API更新（无参数直接更新，有参数通过JSON输入）
4. ✅ 手动测试通过

## 标记方法

```powershell
# 重命名文件，在文件名后添加-finished
Move-Item "tests\stocks\requirements\02_个股信息查询-东财.md" `
          "tests\stocks\requirements\02_个股信息查询-东财-finished.md"
```

## 各集合的参数示例

供用户在JSON对话框中输入时参考：

### 02_个股信息查询-东财
```json
{
  "symbol": "000001"
}
```
批量：
```json
{
  "symbol": "000001,000002,600000"
}
```

### 03_个股信息查询-雪球
```json
{
  "symbol": "SH600000"
}
```

### 05_A股历史行情-东财
```json
{
  "symbol": "000001",
  "period": "daily",
  "adjust": "qfq"
}
```

### 06_A股分时数据-东财
```json
{
  "symbol": "000001",
  "date": "2024-11-24"
}
```

## 后续优化（可选）

完成基本功能后，可以考虑：
1. 为常用集合添加友好的表单输入（不用JSON）
2. 添加参数模板和示例
3. 添加参数验证
4. 批量处理进度显示
5. 参数历史记录

## 总结

使用JSON输入方式的优点：
- ✅ 实现简单，30分钟完成
- ✅ 灵活，支持所有集合的所有参数
- ✅ 统一，所有集合使用相同的UI

缺点：
- ❌ 需要用户了解API参数格式
- ❌ 用户体验不如专门的表单
- ❌ 容易输入错误

但作为MVP（最小可行产品），这是最快的实现方式，后续可以逐步优化。

---
创建时间：2025-11-24
预计完成时间：30分钟
