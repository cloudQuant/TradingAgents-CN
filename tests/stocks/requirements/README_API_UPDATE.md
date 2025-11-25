# 股票数据集合API更新功能说明

## 📋 快速导航

- **当前状态**：见 `CURRENT_STATUS_SUMMARY.md`
- **下一步工作**：见 `NEXT_STEPS.md`  
- **完整实现指南**：见 `API_UPDATE_IMPLEMENTATION_GUIDE.md`
- **实现状态追踪**：见 `IMPLEMENTATION_STATUS.md`

## 🎯 当前进度

### ✅ 已完成（70%）
1. **文件导入功能**：所有股票数据集合都支持CSV/Excel文件上传
2. **远程同步功能**：所有股票数据集合都支持从远程MongoDB同步数据
3. **API更新基础**：支持无参数的直接更新

### ⏳ 进行中（30%）
4. **带参数的API更新**：配置文件已创建，UI待完善

## 💡 快速开始

### 当前可用的功能

#### 1. 文件导入
```
1. 打开任意股票数据集合页面
2. 点击"更新数据"按钮
3. 上传CSV或Excel文件
4. 系统自动导入数据
```

#### 2. 远程同步
```
1. 打开任意股票数据集合页面
2. 点击"更新数据"按钮
3. 配置远程MongoDB连接
4. 开始同步数据
```

#### 3. API更新（简单）
```
1. 打开任意股票数据集合页面
2. 点击"更新数据"按钮
3. 系统调用AKShare API更新数据
```

### 待完善的功能

#### 4. API更新（带参数）
**需要补充**：参数输入对话框，支持用户输入股票代码等参数

**实现方案**：见 `NEXT_STEPS.md`，预计30分钟完成

## 📁 文件结构

### 后端
```
app/
├── routers/
│   └── stocks.py              # API端点（上传、同步、刷新、清空）
└── services/
    └── stock_data_service.py  # 数据服务（导入、同步逻辑）
```

### 前端
```
frontend/src/
├── api/
│   └── stocks.ts                      # API调用方法
└── views/Stocks/
    ├── Collection.vue                 # 主要组件（需要完善）
    ├── collectionConfig.ts            # 集合配置
    └── collectionRefreshConfig.ts     # 刷新参数配置（已创建）
```

### 需求文档
```
tests/stocks/requirements/
├── 02_个股信息查询-东财.md           # 待处理
├── 03_个股信息查询-雪球.md           # 待处理
├── 07_上海证券交易所-完成.md         # 已完成
├── 08_证券类别统计-完成.md           # 已完成
└── ...                               # 更多文档
```

## 🚀 下一步工作

### 立即可做（推荐）
按照 `NEXT_STEPS.md` 的步骤，30分钟内完成参数支持：

1. **修改Collection.vue**（20分钟）
   - 将"更新数据"按钮改为下拉菜单
   - 添加API参数输入对话框
   - 支持JSON格式参数输入

2. **测试功能**（10分钟）
   - 测试无参数更新
   - 测试带参数更新
   - 测试文件导入和远程同步

3. **标记完成的需求文档**
   - 测试通过后，重命名文件添加"-finished"后缀

### 批量处理需求文档
完成参数支持后，逐个处理 `tests/stocks/requirements/` 中的需求文档：

1. 分析API参数要求
2. 测试功能
3. 标记finished

## 📝 标记Finished的标准

一个需求文档可以标记为finished需要满足：

✅ **必需条件**：
1. 后端API接口已实现
2. 前端页面可以访问和展示数据
3. 三种更新方式都可用：
   - 文件导入 ✅
   - 远程同步 ✅  
   - API更新 ⏳（待完善参数支持）

✅ **验证方式**：
1. 手动测试每种更新方式
2. 确认数据能正确获取和存储
3. UI交互正常无异常

✅ **标记方法**：
```powershell
# 重命名文件，添加-finished后缀
Move-Item "02_个股信息查询-东财.md" "02_个股信息查询-东财-finished.md"
```

## 🔧 技术细节

### 已实现的核心功能

#### 1. 文件导入 (stock_data_service.py)
```python
async def import_data_from_file(collection_name: str, content: bytes, filename: str):
    # 读取CSV或Excel
    # 自动识别字段（code, symbol, 代码等）
    # 批量upsert避免重复
    # 返回导入数量
```

#### 2. 远程同步 (stock_data_service.py)
```python
async def sync_data_from_remote(collection_name: str, config: Dict):
    # 连接远程MongoDB
    # 分批同步数据
    # 支持认证和配置
    # 返回同步统计
```

#### 3. API刷新 (stocks.py)
```python
@router.post("/collections/{collection_name}/refresh")
async def refresh_collection(collection_name: str, params: Dict):
    # 创建后台任务
    # 调用刷新服务
    # 返回task_id供轮询状态
```

### 待实现的功能

#### 4. 参数化API刷新 (Collection.vue)
```vue
<!-- 需要添加 -->
<el-dialog v-model="apiParamsDialogVisible">
  <el-radio-group v-model="refreshMode">
    <el-radio label="all">更新全部</el-radio>
    <el-radio label="params">带参数更新</el-radio>
  </el-radio-group>
  
  <el-input v-if="refreshMode === 'params'"
            v-model="refreshParamsJson"
            type="textarea"
            placeholder='{"symbol": "000001"}' />
</el-dialog>
```

## 📞 使用示例

### 参数格式参考

当用户选择"带参数更新"时，需要输入JSON格式的参数：

**个股信息查询**：
```json
{"symbol": "000001"}
```

**批量查询**：
```json
{"symbol": "000001,000002,600000"}
```

**历史行情查询**：
```json
{
  "symbol": "000001",
  "period": "daily",
  "adjust": "qfq"
}
```

**分时数据查询**：
```json
{
  "symbol": "000001",
  "date": "2024-11-24"
}
```

## ❓ 常见问题

### Q1: 为什么采用JSON输入而不是友好的表单？
A: JSON输入是MVP方案，实现快速（30分钟），支持所有集合的所有参数。后续可以为常用集合添加专门的表单。

### Q2: 哪些集合不需要参数？
A: 所有标记为"完成"的集合（如"上海证券交易所-完成.md"）都不需要参数，可以直接更新。

### Q3: 如何知道某个集合需要什么参数？
A: 查看对应的需求文档，文档中有API接口说明和参数说明。

### Q4: 文件导入和API更新有什么区别？
A: 
- **文件导入**：适合已有数据文件，批量导入历史数据
- **API更新**：调用AKShare等API实时获取最新数据

### Q5: 可以同时使用多种更新方式吗？
A: 可以。三种方式互不影响，数据会根据唯一键（如股票代码）自动去重。

## 📚 相关文档

- `CURRENT_STATUS_SUMMARY.md` - 当前状态详细说明
- `NEXT_STEPS.md` - 下一步工作详细步骤
- `API_UPDATE_IMPLEMENTATION_GUIDE.md` - 完整实现指南
- `IMPLEMENTATION_STATUS.md` - 实现状态追踪

## 🎉 总结

**当前状态**：基础功能完成70%，所有集合都支持文件导入和远程同步。

**关键待办**：完善参数输入UI（预计30分钟）。

**最终目标**：所有需求文档标记为finished，所有集合支持三种更新方式。

---
最后更新：2025-11-24  
维护者：开发团队
