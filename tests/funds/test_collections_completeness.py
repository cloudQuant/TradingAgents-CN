"""
基金数据集合完整性测试

测试目标：
1. 检查 requirements 文档中定义的所有数据集合是否在后端 API 中实现
2. 验证这些数据集合能否正确打开（前端路由配置正确）
3. 如果发现缺失或问题，输出详细的修复建议

参考：tests/funds 目录下的需求文档（02-71）
"""

import os
import sys
import re
from typing import Dict, List, Set

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


class TestCollectionsCompleteness:
    """测试基金数据集合的完整性"""
    
    def __init__(self):
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
        self.tests_funds_dir = os.path.join(self.project_root, 'tests', 'funds')
        self.router_file = os.path.join(self.project_root, 'app', 'routers', 'funds.py')
        self.frontend_api_file = os.path.join(self.project_root, 'frontend', 'src', 'api', 'funds.ts')
        
        # 存储提取的数据
        self.requirement_collections: Dict[str, Dict] = {}  # {interface_name: {title, file}}
        self.backend_collections: Set[str] = set()  # 后端定义的集合名称
        self.missing_collections: List[Dict] = []  # 缺失的集合
        
    def extract_collections_from_requirements(self):
        """从需求文档中提取所有数据集合接口"""
        print("\n[步骤1] 从需求文档中提取数据集合...")
        
        # 遍历所有需求文档
        for filename in os.listdir(self.tests_funds_dir):
            if not filename.endswith('.md'):
                continue
            
            # 跳过非需求文档
            if filename.startswith('README') or filename.startswith('BUGFIX') or \
               filename.startswith('基金投研') or filename.startswith('生成完成') or \
               filename.startswith('需求文档清单') or '_实现总结' in filename or \
               '_修复说明' in filename or '01_基金数据集合文档' in filename:
                continue
            
            filepath = os.path.join(self.tests_funds_dir, filename)
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # 提取接口名称（格式：接口: xxxx）
                    match = re.search(r'接口:\s*(\w+)', content)
                    if match:
                        interface_name = match.group(1)
                        
                        # 提取标题（第一个非空行或者从文件名提取）
                        title_match = re.search(r'###\s*获取数据的API接口.*?[\r\n]+(.+)', content)
                        if title_match:
                            title = title_match.group(1).strip()
                        else:
                            # 从文件名提取标题
                            title = filename.replace('.md', '').split('_', 1)[-1] if '_' in filename else filename.replace('.md', '')
                        
                        self.requirement_collections[interface_name] = {
                            'title': title,
                            'file': filename
                        }
                        print(f"  [OK] 找到接口: {interface_name} ({title})")
            except Exception as e:
                print(f"  [ERROR] 读取文件失败: {filename} - {e}")
        
        print(f"\n  [汇总] 共找到 {len(self.requirement_collections)} 个数据集合接口")
        return len(self.requirement_collections)
    
    def extract_collections_from_backend(self):
        """从后端路由文件中提取已实现的数据集合"""
        print("\n[步骤2] 从后端路由中提取已实现的数据集合...")
        
        if not os.path.exists(self.router_file):
            print(f"  [ERROR] 后端路由文件不存在: {self.router_file}")
            return 0
        
        try:
            with open(self.router_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # 提取所有集合定义（格式：\"name\": \"xxxx\"）
                matches = re.findall(r'"name":\s*"(\w+)"', content)
                self.backend_collections = set(matches)
                
                for name in sorted(self.backend_collections):
                    print(f"  [OK] 后端已定义: {name}")
            
            print(f"\n  [汇总] 后端共定义 {len(self.backend_collections)} 个数据集合")
            return len(self.backend_collections)
        except Exception as e:
            print(f"  [ERROR] 读取后端路由文件失败: {e}")
            return 0
    
    def compare_collections(self):
        """对比需求文档和后端实现，找出缺失的集合"""
        print("\n[Step 3] Comparing requirements with backend...")
        
        requirement_set = set(self.requirement_collections.keys())
        
        # 找出缺失的集合
        missing = requirement_set - self.backend_collections
        
        if missing:
            print(f"\n  [WARNING] Found {len(missing)} collections missing in backend:")
            for interface_name in sorted(missing):
                info = self.requirement_collections[interface_name]
                self.missing_collections.append({
                    'interface': interface_name,
                    'title': info['title'],
                    'file': info['file']
                })
                # 使用 ASCII 安全的输出
                print(f"    - {interface_name} from [{info['file']}]")
        else:
            print(f"\n  [SUCCESS] All required collections are implemented!")
        
        # 找出后端多余的集合（不在需求文档中）
        extra = self.backend_collections - requirement_set
        if extra:
            print(f"\n  [INFO] Backend has {len(extra)} extra collections:")
            for name in sorted(extra):
                print(f"    + {name}")
        
        return len(missing) == 0
    
    def generate_fix_suggestions(self):
        """生成修复建议"""
        if not self.missing_collections:
            return
        
        print("\n" + "="*70)
        print("修复建议")
        print("="*70)
        
        print("\n需要在后端 app/routers/funds.py 的 collections 列表中添加以下集合定义：\n")
        
        for item in self.missing_collections:
            interface_name = item['interface']
            title = item['title']
            req_file = item['file']
            
            print(f"# 来自需求文档: {req_file}")
            print(f"{{")
            print(f'    "name": "{interface_name}",')
            print(f'    "display_name": "{title}",')
            print(f'    "description": "请根据需求文档 {req_file} 补充描述",')
            print(f'    "route": "/funds/collections/{interface_name}",')
            print(f'    "fields": ["请根据需求文档补充字段列表"],')
            print(f"}},\n")
        
        print("\n建议步骤：")
        print("1. 查看对应的需求文档，了解接口的详细信息")
        print("2. 在 app/routers/funds.py 的 collections 列表中添加集合定义")
        print("3. 确保字段名称、描述与需求文档一致")
        print("4. 重新运行此测试验证")
    
    def test_collections_completeness(self):
        """主测试：检查数据集合完整性"""
        print("="*70)
        print("基金数据集合完整性测试")
        print("="*70)
        
        # 步骤1: 提取需求文档中的集合
        req_count = self.extract_collections_from_requirements()
        assert req_count > 0, "未找到任何需求文档中的数据集合接口"
        
        # 步骤2: 提取后端已实现的集合
        backend_count = self.extract_collections_from_backend()
        assert backend_count > 0, "后端未定义任何数据集合"
        
        # 步骤3: 对比并找出缺失
        is_complete = self.compare_collections()
        
        # 如果有缺失，生成修复建议
        if not is_complete:
            self.generate_fix_suggestions()
        
        print("\n" + "="*70)
        if is_complete:
            print("[SUCCESS] 测试通过：所有需求文档中的数据集合都已实现")
        else:
            print(f"[FAILED] 测试失败：发现 {len(self.missing_collections)} 个集合未实现")
        print("="*70)
        
        return is_complete
    
    def test_backend_collections_have_required_fields(self):
        """测试后端集合定义是否包含必需字段"""
        print("\n" + "="*70)
        print("检查后端集合定义的字段完整性")
        print("="*70)
        
        if not os.path.exists(self.router_file):
            print(f"✗ 后端路由文件不存在")
            return False
        
        with open(self.router_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取所有集合定义
        collection_pattern = r'\{[^}]*?"name":\s*"(\w+)"[^}]*?\}'
        matches = re.finditer(collection_pattern, content, re.DOTALL)
        
        errors = []
        for match in matches:
            collection_def = match.group(0)
            name_match = re.search(r'"name":\s*"(\w+)"', collection_def)
            if not name_match:
                continue
            
            name = name_match.group(1)
            
            # 检查必需字段
            required_fields = ['display_name', 'description', 'route', 'fields']
            missing_fields = []
            
            for field in required_fields:
                if f'"{field}":' not in collection_def:
                    missing_fields.append(field)
            
            if missing_fields:
                errors.append({
                    'collection': name,
                    'missing_fields': missing_fields
                })
                print(f"  [WARNING] 集合 '{name}' 缺少字段: {', '.join(missing_fields)}")
        
        if errors:
            print(f"\n[FAILED] 发现 {len(errors)} 个集合定义不完整")
            return False
        else:
            print("\n[SUCCESS] 所有集合定义都包含必需字段")
            return True


def run_all_tests():
    """运行所有测试"""
    tester = TestCollectionsCompleteness()
    
    # 测试1: 集合完整性
    test1_passed = tester.test_collections_completeness()
    
    # 测试2: 字段完整性
    test2_passed = tester.test_backend_collections_have_required_fields()
    
    # 总结
    print("\n" + "="*70)
    print("测试总结")
    print("="*70)
    print(f"集合完整性测试: {'[PASS]' if test1_passed else '[FAIL]'}")
    print(f"字段完整性测试: {'[PASS]' if test2_passed else '[FAIL]'}")
    print("="*70)
    
    all_passed = test1_passed and test2_passed
    
    if all_passed:
        print("\n[SUCCESS] 所有测试通过！")
        return 0
    else:
        print("\n[WARNING] 部分测试失败，请根据上述建议进行修复")
        return 1


if __name__ == "__main__":
    # 设置 UTF-8 编码输出
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    
    exit_code = run_all_tests()
    sys.exit(exit_code)
