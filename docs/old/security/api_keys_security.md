# API 密钥安全指南

## 🚨 重要安全提醒

### ⚠️ 绝对不要做的事情

1. **不要将.env 文件提交到 Git 仓库**
   - .env 文件包含敏感的 API 密钥
   - 一旦提交到公开仓库，密钥可能被恶意使用
   - 即使删除提交，Git 历史中仍然存在

1. **不要在代码中硬编码 API 密钥**

   ```python

# ❌ 错误做法
   api_key = "sk-1234567890abcdef"

# ✅ 正确做法
   api_key = os.getenv("DASHSCOPE_API_KEY")
   ```

1. **不要在日志中输出完整的 API 密钥**

   ```python

# ❌ 错误做法
   print(f"Using API key: {api_key}")

# ✅ 正确做法
   print(f"Using API key: {api_key[:12]}...")
   ```

### ✅ 安全最佳实践

#### 1. 使用环境变量

```bash

# 在.env 文件中配置

DASHSCOPE_API_KEY=your_real_api_key_here
FINNHUB_API_KEY=your_real_finnhub_key_here

```bash

#### 2. 正确的文件权限

```bash

# 设置.env 文件只有所有者可读写

chmod 600 .env

```bash

#### 3. 使用.gitignore

确保.gitignore 包含：

```bash
.env
.env.local
.env.*.local

```bash

#### 4. 定期轮换 API 密钥

- 定期更换 API 密钥
- 如果怀疑密钥泄露，立即更换
- 监控 API 使用情况，发现异常立即处理

## 🔧 配置步骤

### 1. 复制示例文件

```bash
cp .env.example .env

```bash

### 2. 编辑.env 文件

```bash

# 使用您喜欢的编辑器

notepad .env        # Windows

nano .env           # Linux/Mac

code .env           # VS Code

```bash

### 3. 填入真实 API 密钥

```bash

# 阿里百炼 API 密钥 (推荐)

DASHSCOPE_API_KEY=sk-your-real-dashscope-key

# 金融数据 API 密钥 (必需)

FINNHUB_API_KEY=your-real-finnhub-key

```bash

### 4. 验证配置

```bash
python -m cli.main config

```bash

## 🔍 API 密钥获取指南

### 阿里百炼 (推荐)

1. 访问 <https://dashscope.aliyun.com/>
2. 注册/登录阿里云账号
3. 开通百炼服务
4. 在控制台获取 API 密钥

### FinnHub (必需)

1. 访问 <https://finnhub.io/>
2. 注册免费账号
3. 在 Dashboard 获取 API 密钥
4. 免费账户每分钟 60 次请求

### OpenAI (可选)

1. 访问 <https://platform.openai.com/>
2. 注册账号并充值
3. 在 API Keys 页面创建密钥

## 🚨 如果 API 密钥泄露了怎么办？

### 立即行动

1. **立即撤销泄露的 API 密钥**
   - 登录对应的 API 提供商控制台
   - 删除或禁用泄露的密钥

1. **生成新的 API 密钥**
   - 创建新的 API 密钥
   - 更新.env 文件中的配置

1. **检查使用记录**
   - 查看 API 使用日志
   - 确认是否有异常使用

1. **更新代码配置**
   - 更新本地.env 文件
   - 通知团队成员更新配置

### 预防措施

1. **使用 Git hooks**
   - 设置 pre-commit hooks 检查敏感文件
   - 防止意外提交.env 文件

1. **定期审计**
   - 定期检查 Git 历史
   - 确保没有敏感信息泄露

1. **团队培训**
   - 培训团队成员安全意识
   - 建立安全操作规范

## 📋 安全检查清单

- [ ] .env 文件已添加到.gitignore
- [ ] 没有在代码中硬编码 API 密钥
- [ ] .env 文件权限设置正确 (600)
- [ ] 定期轮换 API 密钥
- [ ] 监控 API 使用情况
- [ ] 团队成员了解安全规范
- [ ] 设置了 pre-commit hooks (可选)

## 🔗 相关资源

- [Git 安全最佳实践](<https://docs.github.com/en/authentication/keeping-your-account-and-data-secure)>
- [环境变量安全指南](<https://12factor.net/config)>
- [API 密钥管理最佳实践](<https://owasp.org/www-project-api-security/)>

- --

- *记住：安全无小事，API 密钥保护是每个开发者的责任！** 🔐
