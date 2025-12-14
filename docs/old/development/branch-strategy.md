# 分支管理策略

## 🌿 分支架构设计

### 主要分支

```bash
main (生产分支)
├── develop (开发主分支)
├── feature/* (功能开发分支)
├── enhancement/* (中文增强分支)
├── hotfix/* (紧急修复分支)
├── release/* (发布准备分支)
└── upstream-sync/* (上游同步分支)

```bash

### 分支说明

#### 🏠 **main**- 生产主分支

- **用途**: 稳定的生产版本
- **保护**: 受保护，只能通过 PR 合并
- **来源**: develop、hotfix、upstream-sync
- **特点**: 始终保持可发布状态

#### 🚀 **develop**- 开发主分支

- **用途**: 集成所有功能开发
- **保护**: 受保护，通过 PR 合并
- **来源**: feature、enhancement 分支
- **特点**: 最新的开发进度

#### ✨ **feature/**- 功能开发分支

- **命名**: `feature/功能名称`
- **用途**: 开发新功能
- **生命周期**: 短期（1-2 周）
- **示例**: `feature/portfolio-optimization`

#### 🇨🇳 **enhancement/**- 中文增强分支

- **命名**: `enhancement/增强名称`
- **用途**: 中文本地化和增强功能
- **生命周期**: 中期（2-4 周）
- **示例**: `enhancement/chinese-llm-integration`

#### 🚨 **hotfix/**- 紧急修复分支

- **命名**: `hotfix/修复描述`
- **用途**: 紧急 Bug 修复
- **生命周期**: 短期（1-3 天）
- **示例**: `hotfix/api-timeout-fix`

#### 📦 **release/**- 发布准备分支

- **命名**: `release/版本号`
- **用途**: 发布前的最后准备
- **生命周期**: 短期（3-7 天）
- **示例**: `release/v1.1.0-cn`

#### 🔄 **upstream-sync/**- 上游同步分支

- **命名**: `upstream-sync/日期`
- **用途**: 同步上游更新
- **生命周期**: 临时（1 天）
- **示例**: `upstream-sync/20240115`

## 🔄 工作流程

### 功能开发流程

```mermaid
graph LR
    A[main] --> B[develop]
    B --> C[feature/new-feature]
    C --> D[开发和测试]
    D --> E[PR to develop]
    E --> F[代码审查]
    F --> G[合并到 develop]
    G --> H[测试集成]
    H --> I[PR to main]
    I --> J[发布]

```bash

### 中文增强流程

```mermaid
graph LR
    A[develop] --> B[enhancement/chinese-feature]
    B --> C[本地化开发]
    C --> D[中文测试]
    D --> E[文档更新]
    E --> F[PR to develop]
    F --> G[审查和合并]

```bash

### 紧急修复流程

```mermaid
graph LR
    A[main] --> B[hotfix/urgent-fix]
    B --> C[快速修复]
    C --> D[测试验证]
    D --> E[PR to main]
    E --> F[立即发布]
    F --> G[合并到 develop]

```bash

## 📋 分支操作指南

### 创建功能分支

```bash

# 从 develop 创建功能分支

git checkout develop
git pull origin develop
git checkout -b feature/portfolio-analysis

# 开发完成后推送

git push -u origin feature/portfolio-analysis

```bash

### 创建中文增强分支

```bash

# 从 develop 创建增强分支

git checkout develop
git pull origin develop
git checkout -b enhancement/tushare-integration

# 推送分支

git push -u origin enhancement/tushare-integration

```bash

### 创建紧急修复分支

```bash

# 从 main 创建修复分支

git checkout main
git pull origin main
git checkout -b hotfix/api-error-fix

# 推送分支

git push -u origin hotfix/api-error-fix

```bash

## 🔒 分支保护规则

### main 分支保护

- ✅ 要求 PR 审查
- ✅ 要求状态检查通过
- ✅ 要求分支为最新
- ✅ 限制推送权限
- ✅ 限制强制推送

### develop 分支保护

- ✅ 要求 PR 审查
- ✅ 要求 CI 通过
- ✅ 允许管理员绕过

### 功能分支

- ❌ 无特殊保护
- ✅ 自动删除已合并分支

## 🏷️ 命名规范

### 分支命名

```bash

# 功能开发

feature/功能名称-简短描述
feature/chinese-data-source
feature/risk-management-enhancement

# 中文增强

enhancement/增强类型-具体内容
enhancement/llm-baidu-integration
enhancement/chinese-financial-terms

# Bug 修复

hotfix/问题描述
hotfix/memory-leak-fix
hotfix/config-loading-error

# 发布准备

release/版本号
release/v1.1.0-cn
release/v1.2.0-cn-beta

```bash

### 提交信息规范

```bash

# 功能开发

feat(agents): 添加量化分析师智能体
feat(data): 集成 Tushare 数据源

# 中文增强

enhance(llm): 集成文心一言 API
enhance(docs): 完善中文文档体系

# Bug 修复

fix(api): 修复 API 超时问题
fix(config): 解决配置文件加载错误

# 文档更新

docs(readme): 更新安装指南
docs(api): 添加 API 使用示例

```bash

## 🧪 测试策略

### 分支测试要求

#### feature 分支

- ✅ 单元测试覆盖率 > 80%
- ✅ 功能测试通过
- ✅ 代码风格检查

#### enhancement 分支

- ✅ 中文功能测试
- ✅ 兼容性测试
- ✅ 文档完整性检查

#### develop 分支

- ✅ 完整测试套件
- ✅ 集成测试
- ✅ 性能测试

#### main 分支

- ✅ 生产环境测试
- ✅ 端到端测试
- ✅ 安全扫描

## 📊 分支监控

### 分支健康度指标

```bash

# 检查分支状态

git branch -a --merged    # 已合并分支

git branch -a --no-merged # 未合并分支

# 检查分支差异

git log develop..main --oneline
git log feature/branch..develop --oneline

# 检查分支大小

git rev-list --count develop..feature/branch

```bash

### 定期清理

```bash

# 删除已合并的本地分支

git branch --merged develop | grep -v "develop\|main" | xargs -n 1 git branch -d

# 删除远程跟踪分支

git remote prune origin

# 清理过期分支

git for-each-ref --format='%(refname:short) %(committerdate)' refs/heads | awk '$2 <= "'$(date -d '30 days ago' '+%Y-%m-%d')'"' | cut -d' ' -f1

```bash

## 🚀 发布流程

### 版本发布步骤

1. **创建发布分支**

   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b release/v1.1.0-cn
   ```

1. **版本准备**

   ```bash

# 更新版本号

# 更新 CHANGELOG.md

# 最后测试
   ```

1. **合并到 main**

   ```bash
   git checkout main
   git merge release/v1.1.0-cn
   git tag v1.1.0-cn
   git push origin main --tags
   ```

1. **回合并到 develop**

   ```bash
   git checkout develop
   git merge main
   git push origin develop
   ```

## 🔧 自动化工具

### Git Hooks

```bash

# pre-commit hook

# !/bin/sh

# 运行代码风格检查

black --check .
flake8 .

# pre-push hook

# !/bin/sh

# 运行测试

python -m pytest tests/

```bash

### GitHub Actions

```yaml

# 分支保护检查

on:
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:

      - uses: actions/checkout@v4
      - name: Run tests

        run: python -m pytest

```bash

## 🚀 推荐的开发工作流

### 1. 日常功能开发流程

#### 标准功能开发

```bash

# 步骤 1: 创建功能分支

python scripts/branch_manager.py create feature portfolio-optimization -d "投资组合优化功能"

# 步骤 2: 开发功能

# 编写代码...

git add .
git commit -m "feat: 添加投资组合优化算法"

# 步骤 3: 定期同步 develop 分支

git fetch origin
git merge origin/develop  # 或使用 git rebase origin/develop

# 步骤 4: 推送到远程

git push origin feature/portfolio-optimization

# 步骤 5: 创建 Pull Request

# 在 GitHub 上创建 PR: feature/portfolio-optimization -> develop

# 填写 PR 模板，包含功能描述、测试说明等

# 步骤 6: 代码审查

# 等待团队成员审查，根据反馈修改代码

# 步骤 7: 合并和清理

# PR 合并后，删除本地和远程分支

python scripts/branch_manager.py delete feature/portfolio-optimization

```bash

#### 功能开发检查清单

- [ ] 功能需求明确，有详细的设计文档
- [ ] 创建了合适的分支名称和描述
- [ ] 编写了完整的单元测试
- [ ] 代码符合项目编码规范
- [ ] 更新了相关文档
- [ ] 通过了所有自动化测试
- [ ] 进行了代码审查
- [ ] 测试了与现有功能的兼容性

### 2. 中文增强开发流程

#### 本地化功能开发

```bash

# 步骤 1: 创建增强分支

python scripts/branch_manager.py create enhancement tushare-integration -d "集成 Tushare A 股数据源"

# 步骤 2: 开发中文功能

# 集成中文数据源

git add tradingagents/data/tushare_source.py
git commit -m "enhance(data): 添加 Tushare 数据源适配器"

# 添加中文配置

git add config/chinese_config.yaml
git commit -m "enhance(config): 添加中文市场配置"

# 步骤 3: 更新中文文档

git add docs/data/tushare-integration.md
git commit -m "docs: 添加 Tushare 集成文档"

# 步骤 4: 中文功能测试

python -m pytest tests/test_tushare_integration.py
git add tests/test_tushare_integration.py
git commit -m "test: 添加 Tushare 集成测试"

# 步骤 5: 推送和合并

git push origin enhancement/tushare-integration

# 创建 PR 到 develop 分支

```bash

#### 中文增强检查清单

- [ ] 功能适配中国金融市场特点
- [ ] 添加了完整的中文文档
- [ ] 支持中文金融术语
- [ ] 兼容现有的国际化功能
- [ ] 测试了中文数据处理
- [ ] 更新了配置文件和示例

### 3. 紧急修复流程

#### 生产环境 Bug 修复

```bash

# 步骤 1: 从 main 创建修复分支

python scripts/branch_manager.py create hotfix api-timeout-fix -d "修复 API 请求超时问题"

# 步骤 2: 快速定位和修复

# 分析问题根因

# 实施最小化修复

git add tradingagents/api/client.py
git commit -m "fix: 增加 API 请求超时重试机制"

# 步骤 3: 紧急测试

python -m pytest tests/test_api_client.py -v

# 手动测试关键路径

# 步骤 4: 立即部署到 main

git push origin hotfix/api-timeout-fix

# 创建 PR 到 main，标记为紧急修复

# 步骤 5: 同步到 develop

git checkout develop
git merge main
git push origin develop

```bash

#### 紧急修复检查清单

- [ ] 问题影响评估和优先级确认
- [ ] 实施最小化修复方案
- [ ] 通过了关键路径测试
- [ ] 有回滚计划
- [ ] 同步到所有相关分支
- [ ] 通知相关团队成员

### 4. 版本发布流程

#### 正式版本发布

```bash

# 步骤 1: 创建发布分支

python scripts/branch_manager.py create release v1.1.0-cn -d "v1.1.0 中文增强版发布"

# 步骤 2: 版本准备

# 更新版本号

echo "1.1.0-cn" > VERSION
git add VERSION
git commit -m "bump: 版本号更新到 v1.1.0-cn"

# 更新变更日志

git add CHANGELOG.md
git commit -m "docs: 更新 v1.1.0-cn 变更日志"

# 最终测试

python -m pytest tests/ --cov=tradingagents
python examples/full_test.py

# 步骤 3: 合并到 main

git checkout main
git merge release/v1.1.0-cn
git tag v1.1.0-cn
git push origin main --tags

# 步骤 4: 回合并到 develop

git checkout develop
git merge main
git push origin develop

# 步骤 5: 清理发布分支

python scripts/branch_manager.py delete release/v1.1.0-cn

```bash

#### 版本发布检查清单

- [ ] 所有计划功能已完成并合并
- [ ] 通过了完整的测试套件
- [ ] 更新了版本号和变更日志
- [ ] 创建了版本标签
- [ ] 准备了发布说明
- [ ] 通知了用户和社区

### 5. 上游同步集成流程

#### 与原项目保持同步

```bash

# 步骤 1: 检查上游更新

python scripts/sync_upstream.py

# 步骤 2: 如果有更新，会自动创建同步分支

# upstream-sync/20240115

# 步骤 3: 解决可能的冲突

# 保护我们的中文文档和增强功能

# 采用上游的核心代码更新

# 步骤 4: 测试同步结果

python -m pytest tests/
python examples/basic_example.py

# 步骤 5: 合并到主分支

git checkout main
git merge upstream-sync/20240115
git push origin main

# 步骤 6: 同步到 develop

git checkout develop
git merge main
git push origin develop

```bash

## 📈 最佳实践

### 开发建议

1. **小而频繁的提交**- 每个提交解决一个具体问题

2.**描述性分支名**- 清楚表达分支用途
3.**及时同步**- 定期从 develop 拉取最新更改
4.**完整测试**- 合并前确保所有测试通过
5.**文档同步**- 功能开发同时更新文档

### 协作规范

1.**PR 模板**- 使用标准的 PR 描述模板
2.**代码审查**- 至少一人审查后合并
3.**冲突解决**- 及时解决合并冲突
4.**分支清理**- 及时删除已合并分支
5.**版本标记**- 重要节点创建版本标签

### 质量保证

1.**自动化测试**- 每个 PR 都要通过 CI 测试
2.**代码覆盖率**- 保持 80%以上的测试覆盖率
3.**性能测试**- 重要功能要进行性能测试
4.**安全扫描**- 定期进行安全漏洞扫描
5.**文档更新** - 功能变更同步更新文档

通过这套完整的分支管理策略和开发工作流，我们可以确保项目开发的有序进行，同时保持代码质量和发布稳定性。
