# 测试变更记录

## 2024-11-23 v4.1 - 修正：移除不存在的"前端API代理"方式

### 问题
用户指出：前端是Vue SPA应用，`http://localhost:3000/stocks/collections` 是页面路由（返回HTML），不是API端点。前端内部会调用后端API `http://localhost:8000/api/stocks/collections`，不存在所谓的"前端API代理"。

### 修正内容
移除了错误的"前端API代理"方式，现在只使用**2种正确的方式**：

**方式1: 后端API直连** (`http://localhost:8000/api/stocks/collections`)
- 直接访问后端API
- 前端页面实际调用的就是这个API
- 速度快，最优先

**方式2: Playwright页面DOM提取** (`http://localhost:3000/stocks/collections`)
- 启动真实浏览器访问前端页面
- 从渲染后的DOM提取集合链接
- 100%模拟真实用户行为，作为备选方案

### 影响的文件
1. `test_collections_requirements_coverage.py` - 移除前端API代理方式
2. `diagnose_api_access.py` - 移除前端API代理检查
3. 所有相关文档 - 更新说明

---

## 2024-11-23 v4 - 多方式智能获取：解决前端页面显示91个集合但测试获取不到的问题

### 问题背景
用户反馈：前端页面 `/stocks/collections` 能显示91个集合，但测试却获取不到数据。

### 解决方案：多方式智能获取
测试支持**依次尝试多种方式**，直到成功获取数据：

**后端API直连**
- 直接访问后端API
- 速度快、可靠

**Playwright页面DOM提取**
- 启动真实浏览器访问前端页面
- 从渲染后的DOM提取集合链接
- 100%模拟真实用户行为，最可靠

### 技术实现
1. 新增 `_extract_from_frontend_page()` 方法
2. 使用Playwright浏览器自动化
3. 智能识别集合链接和数据属性
4. 详细的尝试过程日志

### 安装要求
```bash
# 基础功能（方式1和2）
pip install httpx pytest

# 完整功能（包含方式3）
pip install playwright
playwright install chromium
```

### 影响的文件
1. `test_collections_requirements_coverage.py`
   - 两个测试都支持多方式获取
   - 新增DOM提取方法
2. `README_多方式数据获取.md` - 新增详细说明文档

### 测试输出示例
```
正在获取集合列表...
  方式1: 尝试前端API代理 http://localhost:3000/api/stocks/collections
  ✗ 前端API返回HTML，尝试其他方式...
  方式2: 尝试后端API http://localhost:8000/api/stocks/collections
  ✓ 后端API成功返回 91 个集合
```

---

## 2024-11-23 v3 - 修正：应该使用后端API而不是前端页面

### 变更内容
**重要修正**：前端 `/stocks/collections` 返回的是 HTML 页面（SPA应用），不是 JSON 数据。

**错误原因**：
- 访问 `http://localhost:3000/stocks/collections` 返回 HTML
- 解析 JSON 时报错：`JSONDecodeError: Expecting value: line 1 column 1`

**正确做法**：
- 前端通过 `ApiClient.get('/api/stocks/collections')` 调用后端API
- 测试应该直接调用后端API：`http://localhost:8000/api/stocks/collections`

**修改的地址**：
- 第一个测试：`http://localhost:3000/stocks/collections` → `http://localhost:8000/api/stocks/collections`
- 第二个测试：也从后端API获取集合列表
- 辅助脚本：`check_coverage_summary.py` 和 `quick_check.py`

### 影响的文件
1. `test_collections_requirements_coverage.py` - 改回使用后端API
2. `check_coverage_summary.py` - 改回使用后端API
3. `quick_check.py` - 改回使用后端API

### 环境变量
现在需要设置后端API地址：
```powershell
$env:API_BASE_URL="http://localhost:8000"  # 默认值
$env:FRONTEND_BASE_URL="http://localhost:3000"  # 用于测试详情页
```

---

## 2024-11-23 v2 - 增加超时时间和等待提示

### 变更内容
针对前端页面响应较慢的情况，增加所有HTTP请求的超时时间：

**超时时间调整**：
- 获取集合列表：15秒 → **60秒**
- 检查前端主页：10秒 → **60秒**  
- 测试详情页：10秒 → **30秒**

**增加友好提示**：
- 在获取集合列表前显示"请稍候，前端页面可能需要10-30秒加载..."
- 区分超时错误和其他请求错误
- 所有辅助脚本也增加了超时时间和提示

### 原因
用户反馈前端页面可以打开，但响应比较慢，需要等待10秒左右。原有的15秒超时可能不够，导致测试误报为无法访问。

### 影响的文件
1. `test_collections_requirements_coverage.py` - 所有HTTP请求超时增加
2. `check_coverage_summary.py` - 超时增加到60秒
3. `quick_check.py` - 超时增加到60秒

### 现在的行为
运行测试时会看到：
```
正在获取前端集合列表...
  前端地址: http://localhost:3000/stocks/collections
  请稍候，前端页面可能需要10-30秒加载...
```

如果超过60秒仍未响应，会显示：
```
❌ 错误：前端页面响应超时（超过60秒）
  建议：请确保前端服务正常运行且响应速度正常
```

---

## 2024-11-23 v1 - 修复集合列表获取地址

### 变更内容
修改了集合列表的获取方式，从后端 API 改为前端地址：

**修改前**：
- 获取集合列表：`http://localhost:8000/api/stocks/collections`
- 使用后端 API 地址

**修改后**：
- 获取集合列表：`http://localhost:3000/stocks/collections`
- 使用前端地址

### 原因
前端页面 `/stocks/collections` 可以直接返回集合列表的 JSON 数据，不需要通过后端 API。这样测试更加直接，反映了前端的实际数据展示情况。

### 影响的文件
1. `tests/stocks/collections/test_collections_requirements_coverage.py`
   - 第一个测试：`test_requirements_collections_covered_by_api` - 改为从前端获取
   - 第二个测试：`test_requirements_collections_frontend_openable` - 改为从前端获取

2. `tests/stocks/check_coverage_summary.py`
   - 快速检查脚本也改为从前端获取

### 测试命令
```powershell
# 快速检查（推荐）
python quick_check.py

# 完整测试
pytest .\collections\test_collections_requirements_coverage.py -v -s
```

### 环境变量
测试现在主要使用前端地址：
- `FRONTEND_BASE_URL`：默认 `http://localhost:3000`
- `TEST_AUTH_TOKEN`：可选，如果前端需要认证

不再需要设置 `API_BASE_URL` 用于获取集合列表。

### 预期结果
运行测试后会看到：
```
需求文档中解析到: 365 个数据集合
前端页面返回:     91 个数据集合
覆盖率:          91/365 (25%)

缺失的集合: 274 个
  1. ✗ stock_zh_a_hist
     文档: 05_A股历史行情-东财.md
  ...
```

这准确反映了前端当前实现的集合数量。
