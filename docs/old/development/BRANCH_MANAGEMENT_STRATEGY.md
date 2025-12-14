# 🌳 TradingAgents-CN 分支管理策略

## 📋 当前分支状况分析

基于项目的发展历程，当前可能存在以下分支：

### 🎯 主要分支

- **main**- 稳定的生产版本
- **develop**- 开发主分支
- **feature/tushare-integration**- Tushare 集成和 v0.1.6 功能
- **feature/deepseek-v3-integration**- DeepSeek V3 集成（可能已合并）

### 🔧 功能分支（可能存在）

- **feature/dashscope-openai-fix**- 阿里百炼修复
- **feature/data-source-upgrade**- 数据源升级
- **hotfix/*** - 紧急修复分支

## 🎯 推荐的分支管理策略

### 1. 简化分支结构

#### 目标结构

```bash
main (生产版本)
├── develop (开发主分支)
├── feature/v0.1.7 (下一版本开发)
└── hotfix/* (紧急修复)

```bash

#### 清理策略

```bash

# 1. 确保所有重要功能都在 main 分支

# 2. 删除已合并的功能分支

# 3. 保持简洁的分支结构

```bash

### 2. 版本发布流程

#### 当前 v0.1.6 发布流程

```bash

# Step 1: 确保 feature/tushare-integration 包含所有 v0.1.6 功能

git checkout feature/tushare-integration
git status

# Step 2: 合并到 develop 分支

git checkout develop
git merge feature/tushare-integration

# Step 3: 合并到 main 分支并打标签

git checkout main
git merge develop
git tag v0.1.6
git push origin main --tags

# Step 4: 清理功能分支

git branch -d feature/tushare-integration
git push origin --delete feature/tushare-integration

```bash

### 3. 未来版本开发流程

#### v0.1.7 开发流程

```bash

# Step 1: 从 main 创建新的功能分支

git checkout main
git pull origin main
git checkout -b feature/v0.1.7

# Step 2: 开发新功能

# ... 开发工作 ...

# Step 3: 定期同步 main 分支

git checkout main
git pull origin main
git checkout feature/v0.1.7
git merge main

# Step 4: 完成后合并回 main

git checkout main
git merge feature/v0.1.7
git tag v0.1.7

```bash

## 🔧 分支清理脚本

### 检查分支状态

```bash

# !/bin/bash

echo "🔍 检查分支状态"
echo "=================="

echo "📋 本地分支:"
git branch

echo -e "\n🌐 远程分支:"
git branch -r

echo -e "\n📊 分支关系:"
git log --oneline --graph --all -10

echo -e "\n🎯 当前分支:"
git branch --show-current

echo -e "\n📝 未提交的更改:"
git status --porcelain

```bash

### 分支清理脚本

```bash

# !/bin/bash

echo "🧹 分支清理脚本"
echo "=================="

# 1. 切换到 main 分支

git checkout main
git pull origin main

# 2. 查看已合并的分支

echo "📋 已合并到 main 的分支:"
git branch --merged main

# 3. 查看未合并的分支

echo "⚠️ 未合并到 main 的分支:"
git branch --no-merged main

# 4. 删除已合并的功能分支（交互式）

echo "🗑️ 删除已合并的功能分支..."
git branch --merged main | grep -E "feature/|hotfix/" | while read branch; do

    echo "删除分支: $branch"
    read -p "确认删除? (y/N): " confirm
    if [[ $confirm == [yY] ]]; then
        git branch -d "$branch"
        git push origin --delete "$branch" 2>/dev/null || true

    fi
done

```bash

## 📋 具体操作建议

### 立即执行的操作

#### 1. 确认当前状态

```bash

# 检查当前分支

git branch --show-current

# 检查未提交的更改

git status

# 查看最近的提交

git log --oneline -5

```bash

#### 2. 整理 v0.1.6 版本

```bash

# 如果当前在 feature/tushare-integration 分支

# 确保所有 v0.1.6 功能都已提交

git add .
git commit -m "完成 v0.1.6 所有功能"

# 推送到远程

git push origin feature/tushare-integration

```bash

#### 3. 发布 v0.1.6 正式版

```bash

# 合并到 main 分支

git checkout main
git merge feature/tushare-integration

# 创建版本标签

git tag -a v0.1.6 -m "TradingAgents-CN v0.1.6 正式版"

# 推送到远程

git push origin main --tags

```bash

### 长期维护策略

#### 1. 分支命名规范

- **功能分支**: `feature/功能名称` 或 `feature/v 版本号`
- **修复分支**: `hotfix/问题描述`
- **发布分支**: `release/v 版本号` (可选)

#### 2. 提交信息规范

```bash
类型(范围): 简短描述

详细描述（可选）

- 具体更改 1
- 具体更改 2

Closes #issue 号

```bash

#### 3. 版本发布检查清单

- [ ] 所有功能开发完成
- [ ] 测试通过
- [ ] 文档更新
- [ ] 版本号更新
- [ ] CHANGELOG 更新
- [ ] 创建发布标签

## 🎯 推荐的下一步行动

### 立即行动（今天）

1. **确认当前分支状态**
2. **提交所有未保存的更改**
3. **发布 v0.1.6 正式版**

### 短期行动（本周）

1. **清理已合并的功能分支**
2. **建立标准的分支管理流程**
3. **创建 v0.1.7 开发分支**

### 长期行动（持续）

1. **遵循分支命名规范**
2. **定期清理过时分支**
3. **维护清晰的版本历史**

## 🛠️ 分支管理工具

### Git 别名配置

```bash

# 添加有用的 Git 别名

git config --global alias.br branch
git config --global alias.co checkout
git config --global alias.st status
git config --global alias.lg "log --oneline --graph --all"
git config --global alias.cleanup "!git branch --merged main | grep -v main | xargs -n 1 git branch -d"

```bash

### VSCode 扩展推荐

- **GitLens**- Git 历史可视化
- **Git Graph**- 分支图形化显示
- **Git History**- 文件历史查看

## 📞 需要帮助时

如果在分支管理过程中遇到问题：

1.**备份当前工作**

   ```bash
   git stash push -m "备份当前工作"
   ```

1. **寻求帮助**
   - 查看 Git 文档
   - 使用 `git help <command>`
   - 咨询团队成员

1. **恢复工作**

   ```bash
   git stash pop
   ```

- --

- *记住**: 分支管理的目标是让开发更有序，而不是增加复杂性。保持简单、清晰的分支结构是关键。
