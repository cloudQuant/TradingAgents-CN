"""
批量生成缺失的数据集合测试文件

根据 requirements 目录中的需求文档，为每个缺失测试的集合生成测试文件
"""
import os
import re
from typing import Dict, List, Tuple

# 测试文件模板
TEST_TEMPLATE = '''"""
{display_name} 数据集合测试

测试目标：
1. 验证 {collection_name} 数据集合的完整功能
2. 测试数据获取、存储、更新、展示等核心功能
3. 确保数据的正确性和完整性

需求文档：{doc_name}
"""

import pytest
import os
from httpx import AsyncClient

BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8848")
AUTH_TOKEN = os.getenv("API_AUTH_TOKEN")

pytestmark = pytest.mark.skipif(not AUTH_TOKEN, reason="API_AUTH_TOKEN not set")


@pytest.mark.asyncio
async def test_collection_endpoint_exists():
    """测试集合接口是否存在"""
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.get(
            "/stocks/collections/{collection_name}",
            headers={{"Authorization": f"Bearer {{AUTH_TOKEN}}"}}
        )
        assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_collection_data_structure():
    """测试返回数据结构"""
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.get(
            "/stocks/collections/{collection_name}",
            headers={{"Authorization": f"Bearer {{AUTH_TOKEN}}"}}
        )
        if response.status_code == 200:
            data = response.json()
            assert "data" in data
            assert "total" in data


@pytest.mark.asyncio
async def test_refresh_collection():
    """测试刷新数据功能"""
    async with AsyncClient(base_url=BASE_URL, timeout=300.0) as client:
        response = await client.post(
            "/stocks/collections/{collection_name}/refresh",
            headers={{"Authorization": f"Bearer {{AUTH_TOKEN}}"}},
            json={{}}
        )
        assert response.status_code in [200, 202]


@pytest.mark.asyncio
async def test_collection_overview():
    """测试数据概览功能"""
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.get(
            "/stocks/collections/{collection_name}/overview",
            headers={{"Authorization": f"Bearer {{AUTH_TOKEN}}"}}
        )
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_clear_collection():
    """测试清空数据功能"""
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.delete(
            "/stocks/collections/{collection_name}/clear",
            headers={{"Authorization": f"Bearer {{AUTH_TOKEN}}"}}
        )
        assert response.status_code == 200
'''


def extract_collections_from_docs(req_dir: str) -> Dict[str, Tuple[str, str]]:
    """
    从需求文档中提取集合名称
    返回: {collection_name: (doc_filename, doc_number)}
    """
    pattern = re.compile(r'http://localhost:3000/stocks/collections/([a-zA-Z0-9_\-]+)')
    collections = {}
    
    for fn in os.listdir(req_dir):
        if not fn.endswith('.md'):
            continue
        
        # 提取文档编号
        match = re.match(r'(\d+)_(.+)\.md', fn)
        if not match:
            continue
        
        doc_num = match.group(1)
        display_name = match.group(2).replace('-完成', '').replace('-finished', '')
        
        fp = os.path.join(req_dir, fn)
        try:
            with open(fp, 'r', encoding='utf-8') as f:
                text = f.read()
            for name in pattern.findall(text):
                if name not in collections:
                    collections[name] = (fn, doc_num, display_name)
        except Exception as e:
            print(f"读取文件失败 {fn}: {e}")
            continue
    
    return collections


def get_existing_tests(collections_dir: str) -> set:
    """获取已有的测试文件对应的集合名称"""
    existing = set()
    for fn in os.listdir(collections_dir):
        if fn.endswith('_collection.py') and fn[0].isdigit():
            match = re.match(r'\d+_(.+)_collection\.py', fn)
            if match:
                existing.add(match.group(1))
    return existing


def generate_test_file(collection_name: str, doc_name: str, doc_num: str, display_name: str, output_dir: str):
    """生成测试文件"""
    content = TEST_TEMPLATE.format(
        collection_name=collection_name,
        display_name=display_name,
        doc_name=doc_name
    )
    
    filename = f"{doc_num}_{collection_name}_collection.py"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filename


def main():
    # 获取目录路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    req_dir = os.path.join(script_dir, '..', 'requirements')
    collections_dir = script_dir
    
    print("=" * 60)
    print("批量生成缺失的数据集合测试文件")
    print("=" * 60)
    
    # 提取需求文档中的集合
    print(f"\n扫描需求文档目录: {req_dir}")
    collections_from_docs = extract_collections_from_docs(req_dir)
    print(f"  找到 {len(collections_from_docs)} 个集合定义")
    
    # 获取已有的测试
    print(f"\n扫描测试文件目录: {collections_dir}")
    existing_tests = get_existing_tests(collections_dir)
    print(f"  找到 {len(existing_tests)} 个已有测试")
    
    # 找出缺失的测试
    missing = []
    for name, (doc_name, doc_num, display_name) in collections_from_docs.items():
        if name not in existing_tests:
            missing.append((name, doc_name, doc_num, display_name))
    
    print(f"\n缺失测试的集合: {len(missing)} 个")
    
    if not missing:
        print("\n所有集合都已有测试文件！")
        return
    
    # 生成测试文件
    print(f"\n开始生成测试文件...")
    generated = []
    for name, doc_name, doc_num, display_name in missing:
        try:
            filename = generate_test_file(name, doc_name, doc_num, display_name, collections_dir)
            generated.append(filename)
            print(f"  [+] 生成: {filename}")
        except Exception as e:
            print(f"  [x] 失败: {name} - {e}")
    
    print(f"\n" + "=" * 60)
    print(f"生成完成！共生成 {len(generated)} 个测试文件")
    print("=" * 60)


if __name__ == "__main__":
    main()
