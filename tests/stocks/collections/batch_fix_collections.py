#!/usr/bin/env python3
"""
批量修复所有Collection.vue文件，添加统一的操作按钮栏
包括：数据概览、刷新、更新数据、清空数据按钮
"""

import os
import re
from pathlib import Path

# 需要修复的文件路径列表
COLLECTION_FILES = [
    "frontend/src/views/Stocks/Collection.vue",
    "frontend/src/views/Bonds/Collection.vue",
    "frontend/src/views/Funds/Collection.vue",
    "frontend/src/views/Futures/Collection.vue",
    "frontend/src/views/Options/Collection.vue",
]

# 检查文件中是否已经有操作按钮栏
def has_action_bar(content: str) -> bool:
    """检查文件是否已经包含操作按钮栏"""
    return 'class="action-bar"' in content or '数据概览' in content

# 在<template>中添加操作按钮栏
def add_action_bar_to_template(content: str) -> str:
    """在模板中添加操作按钮栏"""
    
    # 查找插入位置：<template v-else> 之后
    pattern = r'(<template v-else>)\s*\n'
    
    action_bar_html = '''$1
        <!-- 操作按钮栏 -->
        <div class="action-bar">
          <el-button type="info" @click="showOverview">
            <el-icon><Document /></el-icon>
            数据概览
          </el-button>
          <el-button @click="refreshData">
            <el-icon><Refresh /></el-icon>
            刷新
          </el-button>
          <el-button type="primary" @click="showUpdateDialog">
            <el-icon><Upload /></el-icon>
            更新数据
          </el-button>
          <el-button type="danger" @click="handleClearData">
            <el-icon><Delete /></el-icon>
            清空数据
          </el-button>
        </div>

'''
    
    content = re.sub(pattern, action_bar_html, content, count=1)
    return content

# 添加更新数据对话框
def add_update_dialog(content: str) -> str:
    """添加更新数据对话框"""
    
    # 在</template>之前插入对话框
    dialog_html = '''
    <!-- 更新数据对话框 -->
    <el-dialog
      v-model="updateDialogVisible"
      title="更新数据"
      width="500px"
      @close="closeUpdateDialog"
    >
      <el-form label-width="100px">
        <el-form-item label="更新方式">
          <el-radio-group v-model="updateMethod">
            <el-radio label="file">文件导入</el-radio>
            <el-radio label="remote">远程同步</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <el-form-item v-if="updateMethod === 'file'" label="选择文件">
          <el-upload
            class="upload-demo"
            drag
            action="#"
            :auto-upload="false"
            :on-change="handleFileChange"
            :limit="1"
          >
            <el-icon class="el-icon--upload"><upload-filled /></el-icon>
            <div class="el-upload__text">
              拖拽文件到此处或 <em>点击上传</em>
            </div>
            <template #tip>
              <div class="el-upload__tip">
                支持 CSV, JSON 格式的文件
              </div>
            </template>
          </el-upload>
        </el-form-item>
        
        <el-form-item v-if="updateMethod === 'remote'" label="远程源">
          <el-input v-model="remoteSource" placeholder="请输入远程数据源URL" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="closeUpdateDialog">关闭</el-button>
          <el-button type="primary" @click="startUpdate" :loading="updating">
            开始更新
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 数据概览对话框 -->
    <el-dialog
      v-model="overviewDialogVisible"
      title="数据概览"
      width="80%"
    >
      <el-descriptions :column="2" border>
        <el-descriptions-item label="集合名称">{{ collectionName }}</el-descriptions-item>
        <el-descriptions-item label="显示名称">{{ collectionDef?.display_name }}</el-descriptions-item>
        <el-descriptions-item label="数据总数">{{ stats.total_count || 0 }} 条</el-descriptions-item>
        <el-descriptions-item label="最后更新">
          {{ stats.latest_update ? formatTime(stats.latest_update) : '暂无数据' }}
        </el-descriptions-item>
        <el-descriptions-item label="字段数量">{{ collectionDef?.fields.length || 0 }} 个</el-descriptions-item>
        <el-descriptions-item label="描述" :span="2">
          {{ collectionDef?.description }}
        </el-descriptions-item>
      </el-descriptions>
      
      <template #footer>
        <el-button type="primary" @click="overviewDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>'''
    
    content = content.replace('  </div>\n</template>', dialog_html)
    return content

# 更新图标导入
def update_icon_imports(content: str) -> str:
    """更新图标导入"""
    
    # 查找现有的图标导入行
    pattern = r'import \{ ([^}]+) \} from [\'"]@element-plus/icons-vue[\'"]'
    
    def replace_icons(match):
        existing_icons = match.group(1)
        # 添加新图标
        new_icons = ['Document', 'Upload', 'UploadFilled']
        for icon in new_icons:
            if icon not in existing_icons:
                existing_icons += f', {icon}'
        return f'import {{ {existing_icons} }} from \'@element-plus/icons-vue\''
    
    content = re.sub(pattern, replace_icons, content)
    return content

# 添加对话框状态变量
def add_dialog_state(content: str) -> str:
    """添加对话框相关的状态变量"""
    
    # 在刷新相关状态变量之后添加
    pattern = r'(let statusCheckInterval.*?\n)'
    
    dialog_state = '''$1
// 对话框相关
const updateDialogVisible = ref(false)
const overviewDialogVisible = ref(false)
const updateMethod = ref('remote')
const remoteSource = ref('')
const uploadFile = ref<File | null>(null)
const updating = ref(false)

'''
    
    content = re.sub(pattern, dialog_state, content)
    return content

# 添加对话框方法
def add_dialog_methods(content: str) -> str:
    """添加对话框相关的方法"""
    
    # 在getProgressPercentage方法之后添加
    pattern = r'(const getProgressPercentage.*?\n\})\n'
    
    methods = '''$1

// 显示数据概览
const showOverview = () => {
  overviewDialogVisible.value = true
}

// 显示更新数据对话框
const showUpdateDialog = () => {
  updateDialogVisible.value = true
}

// 关闭更新数据对话框
const closeUpdateDialog = () => {
  updateDialogVisible.value = false
  updateMethod.value = 'remote'
  remoteSource.value = ''
  uploadFile.value = null
}

// 处理文件变化
const handleFileChange = (file: any) => {
  uploadFile.value = file.raw
}

// 开始更新
const startUpdate = async () => {
  if (updateMethod.value === 'file') {
    if (!uploadFile.value) {
      ElMessage.warning('请先选择要上传的文件')
      return
    }
    // 文件导入逻辑（暂未实现后端接口）
    ElMessage.info('文件导入功能开发中...')
  } else {
    // 远程同步 - 调用现有的刷新接口
    await handleRefreshData()
    closeUpdateDialog()
  }
}

'''
    
    content = re.sub(pattern, methods, content, flags=re.DOTALL)
    return content

# 添加操作按钮栏样式
def add_action_bar_style(content: str) -> str:
    """添加操作按钮栏的样式"""
    
    # 在.content样式之后添加
    pattern = r'(\.content \{[^}]+\})\n'
    
    style = '''$1

.action-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
  padding: 16px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

'''
    
    content = re.sub(pattern, style, content)
    return content

def fix_collection_file(file_path: str, dry_run: bool = False) -> bool:
    """修复单个Collection.vue文件"""
    
    full_path = Path(__file__).parent.parent.parent.parent / file_path
    
    if not full_path.exists():
        print(f"[x] 文件不存在: {file_path}")
        return False
    
    print(f"\n[*] 处理文件: {file_path}")
    
    # 读取文件内容
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已经修复过
    if has_action_bar(content):
        print(f"  [+] 文件已包含操作按钮栏，跳过")
        return True
    
    original_content = content
    
    # 应用所有修复
    try:
        print(f"  [>] 添加操作按钮栏...")
        content = add_action_bar_to_template(content)
        
        print(f"  [>] 添加更新数据对话框...")
        content = add_update_dialog(content)
        
        print(f"  [>] 更新图标导入...")
        content = update_icon_imports(content)
        
        print(f"  [>] 添加对话框状态变量...")
        content = add_dialog_state(content)
        
        print(f"  [>] 添加对话框方法...")
        content = add_dialog_methods(content)
        
        print(f"  [>] 添加操作按钮栏样式...")
        content = add_action_bar_style(content)
        
        if dry_run:
            print(f"  [!] 演习模式：不保存文件")
            print(f"  [i] 原始长度: {len(original_content)} 字符")
            print(f"  [i] 修改后长度: {len(content)} 字符")
        else:
            # 保存文件
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  [+] 文件已成功修复")
        
        return True
        
    except Exception as e:
        print(f"  [x] 修复失败: {e}")
        return False

def main():
    """主函数"""
    import argparse
    import sys
    
    # 设置UTF-8编码输出
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    parser = argparse.ArgumentParser(description='批量修复Collection.vue文件')
    parser.add_argument('--dry-run', action='store_true', help='演习模式，不实际修改文件')
    args = parser.parse_args()
    
    print("=" * 80)
    print("[*] 批量修复Collection.vue文件")
    print("=" * 80)
    
    if args.dry_run:
        print("[!] 演习模式：将显示需要修改的内容，但不会实际保存")
    
    success_count = 0
    total_count = len(COLLECTION_FILES)
    
    for file_path in COLLECTION_FILES:
        if fix_collection_file(file_path, dry_run=args.dry_run):
            success_count += 1
    
    print("\n" + "=" * 80)
    print(f"[STATS] 修复完成统计")
    print(f"  总文件数: {total_count}")
    print(f"  成功修复: {success_count}")
    print(f"  失败数量: {total_count - success_count}")
    print("=" * 80)
    
    if success_count == total_count:
        print("[+] 所有文件修复成功！")
    else:
        print("[!] 部分文件修复失败，请检查日志")

if __name__ == '__main__':
    main()
