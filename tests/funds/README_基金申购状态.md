# 基金申购状态功能使用指南

## 快速开始

### 1. 验证功能
运行验证脚本确保功能正常：
```bash
cd /Users/yunjinqi/Documents/TradingAgents-CN
python tests/funds/verify_fund_purchase_status.py
```

### 2. 启动服务

**后端服务**:
```bash
cd /Users/yunjinqi/Documents/TradingAgents-CN
python main.py
# 服务将在 http://localhost:8000 启动
```

**前端服务**:
```bash
cd /Users/yunjinqi/Documents/TradingAgents-CN/frontend
npm run dev
# 服务将在 http://localhost:5173 启动
```

### 3. 访问页面
1. 浏览器打开: http://localhost:5173
2. 登录系统
3. 导航路径: **基金投研** → **数据集合** → **基金申购状态**

## 功能说明

### 数据概览
页面顶部显示：
- 📊 总记录数
- 📅 时间跨度
- 📈 基金类型分布图表
- 📊 申购状态分布图表
- 📊 赎回状态分布图表

### 数据列表
- ✅ 分页展示（每页20/50/100/200条可选）
- ✅ 字段排序（点击表头）
- ✅ 数据筛选（搜索框）
- ✅ 字段说明（鼠标悬停查看）

### 更新数据
点击"更新数据"按钮，打开更新数据对话框，支持三种方式：

#### 方式1: API更新（推荐）
从东方财富网自动获取最新数据：
1. 在对话框中直接点击底部的"开始更新"按钮
2. 系统自动调用AKShare的`fund_purchase_em()`接口
3. 实时显示进度条和状态信息
4. 完成后自动刷新页面数据

**优点**：
- ✅ 数据最新最全（14000+条记录）
- ✅ 自动去重和更新
- ✅ 无需准备数据文件

#### 方式2: 文件导入
从本地CSV或Excel文件导入数据：

**步骤**：
1. 准备数据文件（CSV或Excel格式）
2. 在对话框的"文件导入"区域，拖拽文件或点击选择
3. 点击"导入文件"按钮
4. 等待导入完成

**文件格式要求**：
- 支持格式：`.csv`, `.xlsx`, `.xls`
- 必需字段：
  - `基金代码`（6位数字）
  - `基金简称`
  - `基金类型`
  - `申购状态`
  - `赎回状态`
- 可选字段：
  - `最新净值/万份收益`
  - `最新净值/万份收益-报告时间`
  - `下一开放日`
  - `购买起点`
  - `日累计限定金额`
  - `手续费`

**示例CSV内容**：
```csv
基金代码,基金简称,基金类型,申购状态,赎回状态,最新净值/万份收益,手续费
000001,华夏成长混合,混合型,开放申购,开放赎回,1.234,0.15
000002,测试基金,债券型,暂停申购,开放赎回,2.345,0.08
```

**测试文件**：
可以使用提供的示例CSV文件进行测试：
```
tests/funds/fund_purchase_status_sample.csv
```

**优点**：
- ✅ 适合批量导入历史数据
- ✅ 可以从其他系统导出后导入
- ✅ 支持自定义数据

#### 方式3: 远程同步
从远程MongoDB数据库同步数据：

**步骤**：
1. 在对话框的"远程同步"区域，填写连接信息：
   - **远程主机**：IP地址或MongoDB URI
     - 简单格式：`192.168.1.10`
     - 完整URI：`mongodb://user:pwd@host:27017/db`
   - **数据库类型**：默认MongoDB（不可修改）
   - **批次大小**：1000/2000/5000/10000（建议2000）
   - **远程集合名称**：默认为`fund_purchase_status`
   - **用户名**：MongoDB用户名（可选）
   - **认证库**：通常为`admin`或`tradingagents`
   - **密码**：MongoDB密码（可选）

2. 点击"远程同步"按钮
3. 等待同步完成，查看同步统计

**连接示例**：

*简单连接（无认证）*：
```
主机：192.168.1.100
集合：fund_purchase_status
批次大小：2000
```

*完整连接（带认证）*：
```
主机：mongodb://admin:password@192.168.1.100:27017/tradingagents
集合：fund_purchase_status
用户名：admin
密码：password
认证库：admin
批次大小：2000
```

**优点**：
- ✅ 快速同步大量数据
- ✅ 适合多环境数据迁移
- ✅ 支持增量更新

### 其他功能
- **刷新**: 重新加载当前页面数据
- **清空数据**: 删除所有数据（需确认）

## 数据字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| 序号 | 字符串 | 记录序号 |
| 基金代码 | 字符串 | 6位基金代码 |
| 基金简称 | 字符串 | 基金简称 |
| 基金类型 | 字符串 | 混合型/债券型/股票型等 |
| 最新净值/万份收益 | 浮点数 | 最新净值或万份收益 |
| 最新净值/万份收益-报告时间 | 日期 | 净值报告日期 |
| 申购状态 | 字符串 | 开放申购/暂停申购等 |
| 赎回状态 | 字符串 | 开放赎回/暂停赎回等 |
| 下一开放日 | 日期 | 下一个开放日 |
| 购买起点 | 浮点数 | 最低购买金额 |
| 日累计限定金额 | 浮点数 | 单日累计限额 |
| 手续费 | 浮点数 | 手续费率（百分比） |

## API接口

### 获取数据
```bash
curl -X GET "http://localhost:8000/api/funds/collections/fund_purchase_status?page=1&page_size=50" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 获取统计
```bash
curl -X GET "http://localhost:8000/api/funds/collections/fund_purchase_status/stats" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 刷新数据
```bash
curl -X POST "http://localhost:8000/api/funds/collections/fund_purchase_status/refresh" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}'
```

### 清空数据
```bash
curl -X DELETE "http://localhost:8000/api/funds/collections/fund_purchase_status/clear" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 常见问题

### Q1: 更新数据失败？
**A**: 检查以下几点：
1. 网络连接是否正常
2. AKShare是否已安装（`pip install akshare`）
3. 查看后端日志了解具体错误

### Q2: 数据不显示？
**A**: 
1. 检查是否已执行"更新数据"
2. 刷新页面
3. 检查MongoDB连接是否正常

### Q3: 如何导出数据？
**A**: 可以使用MongoDB工具导出：
```bash
mongoexport --db=tradingagents --collection=fund_purchase_status --out=fund_purchase_status.json
```

### Q4: 数据多久更新一次？
**A**: 
- 手动更新：点击"更新数据"按钮
- 自动更新：可配置定时任务（需要额外开发）

## 技术支持

- 📖 详细文档: `tests/funds/05_基金申购状态_实现总结.md`
- 🧪 测试用例: `tests/funds/test_fund_purchase_status.py`
- 🔧 验证脚本: `tests/funds/verify_fund_purchase_status.py`

## 注意事项

1. **数据唯一性**: 同一基金同一日期的数据会被覆盖（upsert）
2. **大数据量**: 首次更新可能需要较长时间（14000+条记录）
3. **手续费单位**: 显示为百分比（如0.15表示0.15%）
4. **日期格式**: 统一使用YYYY-MM-DD格式

## 下一步优化

- [ ] 增加数据导出功能
- [ ] 实现定时自动更新
- [ ] 添加更多筛选条件
- [ ] 支持数据历史对比
- [ ] 优化大数据量加载性能
