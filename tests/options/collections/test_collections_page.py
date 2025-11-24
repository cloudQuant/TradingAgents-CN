"""
测试期权数据集合页面与需求文档的一致性

测试目标：
1. 解析 tests/options/requirements 中的需求文档，提取应实现的数据集合 slug（如 option_contract_info_ctp）
2. 验证后端 /api/options/collections 返回的数据集合包含上述集合
3. 验证前端路由存在 /options/collections/:collectionName 详情路由，且列表页点击跳转到该路径
4. 尝试打开每个集合的后端数据接口 /api/options/collections/{collection_name}（若需认证则跳过）

若缺失或接口失败，断言信息会包含对应的需求文档路径，方便定位修复。
"""

import os
import re
import sys
import pytest
import httpx
from typing import List, Dict

# 添加项目根目录到路径
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, ROOT_DIR)

REQ_DIR = os.path.join(ROOT_DIR, "tests", "options", "requirements")
FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")
ROUTER_PATH = os.path.join(FRONTEND_DIR, "src", "router", "index.ts")
OPTIONS_COLLECTIONS_PAGE = os.path.join(FRONTEND_DIR, "src", "views", "Options", "Collections.vue")
OPTIONS_COLLECTION_DETAIL_PAGE = os.path.join(FRONTEND_DIR, "src", "views", "Options", "Collection.vue")

SLUG_PATTERN = re.compile(r"/options/collections/([a-zA-Z0-9_\-]+)")
NAME_PATTERN = re.compile(r"名称为\*\*(.+?)\*\*")


def parse_requirements(requirements_dir: str) -> List[Dict[str, str]]:
    """从需求文档中解析出集合 slug 及显示名，返回 [{slug, display_name, doc_path}]"""
    expected = []
    for fname in sorted(os.listdir(requirements_dir)):
        if not fname.endswith(".md"):
            continue
        path = os.path.join(requirements_dir, fname)
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            slug_match = SLUG_PATTERN.search(content)
            if not slug_match:
                # 如果文档没有显式链接，跳过但不报错
                continue
            slug = slug_match.group(1)
            name_match = NAME_PATTERN.search(content)
            display_name = name_match.group(1).strip() if name_match else ""
            expected.append({
                "slug": slug,
                "display_name": display_name,
                "doc_path": path,
            })
        except Exception:
            # 忽略单个文档解析失败，后续测试会提示缺失集合
            continue
    return expected


class TestOptionsCollectionsPage:
    @pytest.fixture(scope="class")
    def api_base_url(self) -> str:
        return os.getenv("API_BASE_URL", "http://localhost:8000")

    @pytest.fixture(scope="class")
    def auth_headers(self) -> Dict[str, str]:
        token = os.getenv("TEST_AUTH_TOKEN", "").strip()
        return {"Authorization": f"Bearer {token}"} if token else {}

    @pytest.fixture(scope="class")
    def expected_from_requirements(self) -> List[Dict[str, str]]:
        assert os.path.isdir(REQ_DIR), f"需求目录不存在: {REQ_DIR}"
        items = parse_requirements(REQ_DIR)
        assert len(items) > 0, "未能从需求文档中解析到任何集合，请检查 tests/options/requirements/*.md 的格式是否包含 /options/collections/<slug> 链接"
        return items

    def test_pages_and_router_exist(self):
        """验证页面文件与路由存在，包括详情路由 /options/collections/:collectionName"""
        assert os.path.exists(OPTIONS_COLLECTIONS_PAGE), f"缺少列表页: {OPTIONS_COLLECTIONS_PAGE}"
        assert os.path.exists(OPTIONS_COLLECTION_DETAIL_PAGE), f"缺少详情页: {OPTIONS_COLLECTION_DETAIL_PAGE}"
        assert os.path.exists(ROUTER_PATH), f"缺少前端路由文件: {ROUTER_PATH}"

        with open(ROUTER_PATH, "r", encoding="utf-8") as f:
            router_content = f.read()

        # 仅在 /options 路由块中检查子路由，避免匹配到其他模块的 collections 详情路由
        options_start = router_content.find("path: '/options'")
        assert options_start != -1, "路由中缺少 /options 路由块"
        # 粗略定位 Options 区块结束位置：寻找下一个顶级 path 标记
        next_markers = [
            "path: '/currencies'",
            "path: '/cryptos'",
            "path: '/dashboard'",
            "path: '/analysis'",
            "path: '/screening'",
            "path: '/favorites'",
            "path: '/stocks'",
            "path: '/tasks'",
            "path: '/reports'",
            "path: '/settings'",
            "path: '/login'",
            "path: '/about'",
            "path: '/paper'",
            "path: '/:pathMatch(.*)*'",
        ]
        indices = [router_content.find(m, options_start + 1) for m in next_markers]
        indices = [i for i in indices if i != -1]
        end_index = min(indices) if indices else options_start + 2000
        options_block = router_content[options_start:end_index]

        # 列表页子路由存在（在 options 块内）
        assert ("path: 'collections'" in options_block) or ("path: \"/options/collections\"" in options_block), \
            "路由中缺少 Options 下的列表路由 (path: 'collections')"

        # 详情页子路由存在（在 options 块内）
        assert ("path: 'collections/:collectionName'" in options_block) or ("path: \"/options/collections/:collectionName\"" in options_block), \
            "路由中缺少 Options 下的详情路由 (path: 'collections/:collectionName')，请在 frontend/src/router/index.ts 的 /options 下添加，组件应为 '@/views/Options/Collection.vue'"

        # 列表页跳转逻辑应使用 /options/collections/<name>
        with open(OPTIONS_COLLECTIONS_PAGE, "r", encoding="utf-8") as f:
            col_page = f.read()
        assert "/options/collections/" in col_page, "列表页跳转应导航到 /options/collections/<collectionName>"

    def test_collections_endpoint_exists_and_structure(self, api_base_url: str, auth_headers: Dict[str, str]):
        """验证 /api/options/collections 存在且结构正确；未认证返回 401 时跳过结构校验"""
        url = f"{api_base_url}/api/options/collections"
        try:
            with httpx.Client(trust_env=False, timeout=10.0) as client:
                resp = client.get(url, headers=auth_headers)
        except httpx.HTTPError as e:
            pytest.skip(f"服务未运行或连接失败，跳过接口结构校验: {e}")
        assert resp.status_code in [200, 401], f"期权集合接口应存在，实际: {resp.status_code}"
        if resp.status_code == 401:
            pytest.skip("需要认证，跳过结构校验")
        data = resp.json()
        assert isinstance(data, dict) and data.get("success") is True, f"返回应为 {{success: True, data: [...]}}，实际: {data}"
        assert isinstance(data.get("data"), list), "data 应为列表"
        # 校验项结构
        for item in data["data"]:
            assert "name" in item and "display_name" in item and "description" in item and "route" in item and "fields" in item, \
                f"集合项字段缺失: {item}"

    def test_expected_collections_present(self, api_base_url: str, auth_headers: Dict[str, str], expected_from_requirements: List[Dict[str, str]]):
        """验证需求文档中的集合全部包含在 /api/options/collections 的返回中"""
        
        # 首先显示需求文档统计（无论后端是否可用）
        expected_slugs = [it["slug"] for it in expected_from_requirements]
        print("\n" + "=" * 70)
        print("[统计] OPTIONS 数据集合需求分析")
        print("=" * 70)
        print(f"[检查] 需求文档中定义的数据集合总数: {len(expected_slugs)} 个")
        print(f"[目录] 需求文档目录: tests/options/requirements")
        print(f"[文档] 需求文档数量: {len(expected_from_requirements)} 个")
        
        # 显示前几个集合作为示例
        print(f"\n[示例] 部分数据集合列表:")
        for i, item in enumerate(expected_from_requirements[:8], 1):
            slug = item["slug"]
            display_name = item["display_name"] or "未定义"
            doc_name = os.path.basename(item["doc_path"])
            print(f"   {i}. {slug}")
            print(f"      名称: {display_name}")
            print(f"      文档: {doc_name}")
        if len(expected_from_requirements) > 8:
            print(f"   ... 还有 {len(expected_from_requirements) - 8} 个集合")
        
        # 尝试连接后端API
        url = f"{api_base_url}/api/options/collections"
        try:
            with httpx.Client(trust_env=False, timeout=15.0) as client:
                resp = client.get(url, headers=auth_headers)
        except httpx.HTTPError as e:
            print(f"\n[警告] 后端服务状态: 未运行或连接失败")
            print(f"   错误信息: {e}")
            print(f"   [提示] 启动后端服务后可查看完整的对比统计")
            print("=" * 70)
            pytest.skip(f"服务未运行或连接失败，跳过集合包含性校验: {e}")
        
        if resp.status_code == 401:
            print(f"\n[警告] 后端服务状态: 需要认证")
            print(f"   [提示] 配置认证令牌后可查看完整的对比统计")
            print("=" * 70)
            pytest.skip("需要认证，跳过集合包含性校验")
        assert resp.status_code == 200
        payload = resp.json()
        assert payload.get("success") is True and isinstance(payload.get("data"), list), f"无效返回: {payload}"
        names = {x.get("name") for x in payload["data"]}

        expected_slugs = [it["slug"] for it in expected_from_requirements]
        
        # 数据集合统计总览
        print("\n" + "=" * 70)
        print("[对比] OPTIONS 数据集合检查统计")
        print("=" * 70)
        print(f"[检查] 检查的数据集合总数: {len(expected_slugs)} 个")
        print(f"[页面] 页面/API 返回的集合数: {len(names)} 个")
        
        missing = []
        for item in expected_from_requirements:
            slug = item["slug"]
            if slug not in names:
                missing.append(f"{slug}  <- {os.path.basename(item['doc_path'])}")
        
        existing_count = len(expected_slugs) - len(missing)
        print(f"[存在] 存在的数据集合数: {existing_count} 个")
        print(f"[缺失] 不存在的数据集合数: {len(missing)} 个")
        
        # 详细列表（可选显示）
        print(f"\n[详情] 统计详细信息:")
        print(f"   需求集合数量: {len(expected_slugs)}")
        print(f"   页面返回数量: {len(names)}")
        print(f"   覆盖率: {existing_count}/{len(expected_slugs)} ({100*existing_count//len(expected_slugs) if len(expected_slugs) > 0 else 0}%)")
        
        if missing:
            print(f"\n[缺失] 缺失的数据集合清单 (共{len(missing)}个):")
            for i, m in enumerate(missing, 1):
                print(f"   {i:2d}. {m}")
        assert not missing, (
            "以下集合在需求文档中定义，但未出现在 /api/options/collections 返回中，请对照文档修复后端集合列表或需求文档:\n" + "\n".join(missing)
        )

    def test_each_required_collection_openable(self, api_base_url: str, auth_headers: Dict[str, str], expected_from_requirements: List[Dict[str, str]]):
        """逐个尝试打开集合的数据接口 /api/options/collections/{name}，验证 success=True（未认证则跳过）"""
        
        # 显示可打开性检查概览
        total_to_verify = len(expected_from_requirements)
        print("\n" + "=" * 70)
        print("[预检] 数据集合可打开性预检")
        print("=" * 70)
        print(f"[目标] 准备验证 {total_to_verify} 个数据集合的可打开性")
        print(f"[后端] 后端地址: {api_base_url}")
        
        # 先探测认证
        try:
            with httpx.Client(trust_env=False, timeout=10.0) as client:
                ping = client.get(f"{api_base_url}/api/options/collections", headers=auth_headers)
        except httpx.HTTPError as e:
            print(f"\n[警告] 后端连接状态: 失败")
            print(f"   错误信息: {e}")
            print(f"   [提示] 启动后端服务: uvicorn app.main:app --host 127.0.0.1 --port 8000")
            print("=" * 70)
            pytest.skip(f"服务未运行或连接失败，跳过逐集合可打开性校验: {e}")
        
        if ping.status_code == 401:
            print(f"\n[警告] 认证状态: 需要令牌")
            print(f"   [提示] 设置环境变量 TEST_AUTH_TOKEN")
            print("=" * 70)
            pytest.skip("需要认证，跳过逐集合可打开性校验")
        
        print(f"\n[成功] 后端连接成功，开始详细检查...")

        total_to_verify = len(expected_from_requirements)
        
        print("\n" + "=" * 70)
        print("[检查] 数据集合可打开性检查")
        print("=" * 70)
        print(f"[开始] 开始验证集合可打开性: 共 {total_to_verify} 个")
        
        failed = []
        success_count = 0
        
        for i, item in enumerate(expected_from_requirements, 1):
            slug = item["slug"]
            url = f"{api_base_url}/api/options/collections/{slug}"
            print(f"   检查进度: {i}/{total_to_verify} - {slug}", end=" ... ")
            
            try:
                with httpx.Client(trust_env=False, timeout=15.0) as client:
                    resp = client.get(url, headers=auth_headers, params={"page": 1, "page_size": 1})
                if resp.status_code != 200:
                    failed.append(f"{slug} -> HTTP {resp.status_code}  文档: {os.path.basename(item['doc_path'])}")
                    print("[X]")
                    continue
                data = resp.json()
                if not isinstance(data, dict) or data.get("success") is not True:
                    failed.append(f"{slug} -> 响应异常: {str(data)[:100]}...  文档: {os.path.basename(item['doc_path'])}")
                    print("[X]")
                else:
                    success_count += 1
                    print("[OK]")
            except httpx.HTTPError as e:
                failed.append(f"{slug} -> 请求异常: {str(e)}  文档: {os.path.basename(item['doc_path'])}")
                print("[X]")

        # 可打开性统计总结
        print("\n" + "=" * 70)
        print("[结果] 可打开性检查结果统计")
        print("=" * 70)
        print(f"[检查] 检查的数据集合总数: {total_to_verify} 个")
        print(f"[成功] 可以打开的集合数: {success_count} 个")
        print(f"[失败] 打不开的集合数: {len(failed)} 个")
        print(f"[成功率] 成功率: {success_count}/{total_to_verify} ({100*success_count//total_to_verify if total_to_verify > 0 else 0}%)")
        
        if failed:
            print(f"\n[失败] 打不开的数据集合清单 (共{len(failed)}个):")
            for i, f in enumerate(failed, 1):
                print(f"   {i:2d}. {f}")
        else:
            print(f"\n[完美] 所有集合都可以正常打开！")
        
        # 总体健康度评估
        if success_count == total_to_verify:
            health_status = "[优秀] 优秀"
        elif success_count >= total_to_verify * 0.8:
            health_status = "[良好] 良好"
        else:
            health_status = "[待改进] 需要改进"
        
        print(f"\n[评估] 系统健康度评估: {health_status}")
        print("=" * 70)
        assert not failed, (
            "以下集合详情接口打开失败，请修复集合映射或实现，或校对需求文档对应集合名称:\n" + "\n".join(failed)
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
