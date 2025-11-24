import os
import re
import sys
import logging
from typing import Dict, List, Set

import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch

# 1) Mock akshare early to avoid optional dependency issues during import
sys.modules["akshare"] = MagicMock()

# 2) Add project root to sys.path so we can import the FastAPI app
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, ROOT_DIR)

from app.main import app  # noqa: E402
from app.routers.auth_db import get_current_user  # noqa: E402


# 3) Override authentication dependency so we can call protected APIs without real tokens
def _mock_get_current_user():
    return {"username": "test_user", "id": "user_id"}


app.dependency_overrides[get_current_user] = _mock_get_current_user
client = TestClient(app)


def _requirements_dir() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "requirements"))


def _collect_requirement_collections() -> Dict[str, str]:
    """Parse tests/futures/requirements/*.md filenames and build mapping of
    collection_name -> requirement_doc_path.

    Filename format examples:
    - 001_期货交易费用参照表_futures_fees_info.md -> futures_fees_info
    - 051_生猪市场价格指数_index_hog_spot_price.md -> index_hog_spot_price
    """
    req_dir = _requirements_dir()
    mapping: Dict[str, str] = {}
    if not os.path.isdir(req_dir):
        return mapping

    slug_pattern = re.compile(r"_(?P<slug>[A-Za-z0-9_]+)$")
    for fname in os.listdir(req_dir):
        if not fname.lower().endswith(".md"):
            continue
        base = os.path.splitext(fname)[0]
        m = slug_pattern.search(base)
        if not m:
            continue
        collection_name = m.group("slug")
        mapping[collection_name] = os.path.join(req_dir, fname)
    return mapping


class TestFuturesCollectionsPage:
    @pytest.fixture(scope="class")
    def frontend_collections_page_path(self) -> str:
        """Path to frontend Futures Collections.vue"""
        return os.path.join(ROOT_DIR, "frontend", "src", "views", "Futures", "Collections.vue")

    @pytest.fixture(scope="class")
    def requirement_map(self) -> Dict[str, str]:
        mapping = _collect_requirement_collections()
        assert mapping, f"未找到需求文档，请确认目录存在: {_requirements_dir()}"
        return mapping

    @pytest.fixture(scope="class")
    def expected_collections(self, requirement_map: Dict[str, str]) -> Set[str]:
        return set(requirement_map.keys())

    def test_collections_endpoint_contains_requirements(self, expected_collections: Set[str], requirement_map: Dict[str, str]):
        """验证 /api/futures/collections 返回的集合包含 requirements 文档声明的所有集合。
        如果缺失，报告对应需求文档路径以便修复。
        """
        resp = client.get("/api/futures/collections")
        assert resp.status_code == 200, f"/api/futures/collections 状态码异常: {resp.status_code}"
        payload = resp.json()

        # 后端约定：{ success: bool, data: list }
        assert isinstance(payload, dict) and payload.get("success") is True, f"接口返回异常: {payload}"
        data = payload.get("data")
        assert isinstance(data, list), f"data 应为列表，实际: {type(data)}"

        available_names = {item.get("name") for item in data if isinstance(item, dict)}
        missing = sorted([name for name in expected_collections if name not in available_names])

        expected_count = len(expected_collections)
        page_count = len(available_names)
        summary_lines = [
            f"需要验证的数据集合数: {expected_count}",
            f"页面（API）返回的数据集合数: {page_count}",
            f"缺少的数据集合数: {len(missing)}",
        ]
        if missing:
            summary_lines.append("缺少集合清单:")
            summary_lines.extend([f"- {name}  (需求文档: {requirement_map[name]})" for name in missing])

        summary = "\n".join(summary_lines)
        logging.info(summary)
        print(summary)

        assert not missing, (
            "以下集合在 /api/futures/collections 列表中缺失，请按需求文档修复注册/路由/命名:\n" +
            "\n".join([f"- {name}  (需求文档: {requirement_map[name]})" for name in missing]) +
            f"\n实际返回集合: {sorted(available_names)}"
        )

    def test_frontend_page_exists_and_uses_collections_api(self, frontend_collections_page_path: str):
        """前端页面存在且包含加载集合与导航逻辑，确保页面可展示并点击打开集合。"""
        assert os.path.exists(frontend_collections_page_path), \
            f"缺少页面文件: {frontend_collections_page_path}"
        with open(frontend_collections_page_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 基本结构
        assert "<template>" in content and "<script" in content and "</template>" in content and "</script>" in content

        # 文案与渲染
        assert "期货数据集合" in content
        assert "v-for" in content, "页面中缺少列表渲染逻辑 (v-for)"

        # 加载集合与导航
        assert "getCollections" in content or "loadCollections" in content, "缺少获取集合的函数调用"
        assert "router.push(`/futures/collections/" in content or "goToCollection" in content, "缺少点击跳转到集合详情的逻辑"

    @patch("app.routers.futures.get_mongo_db")
    def test_each_requirement_collection_openable(self, mock_get_db, expected_collections: Set[str], requirement_map: Dict[str, str]):
        """对每个需求文档声明的集合调用 /api/futures/collections/{name} 打开数据。
        为避免真实数据库依赖，mock Mongo 层，确保路由本身可用。
        失败时输出对应需求文档路径，便于定位修复。
        """
        # Mock DB plumbing shared for all collections
        mock_db = MagicMock()
        mock_collection = MagicMock()
        mock_get_db.return_value = mock_db
        mock_db.get_collection.return_value = mock_collection

        async def _mock_count_documents(*args, **kwargs):
            return 0

        mock_collection.count_documents.side_effect = _mock_count_documents

        # mock async cursor for find()
        mock_cursor = MagicMock()
        mock_cursor.__aiter__.return_value = []  # no items is fine, we just test route opens
        mock_cursor.sort.return_value = mock_cursor
        mock_cursor.skip.return_value = mock_cursor
        mock_cursor.limit.return_value = mock_cursor
        mock_collection.find.return_value = mock_cursor

        # Iterate and try opening each collection endpoint
        failures: List[str] = []
        for name in sorted(expected_collections):
            url = f"/api/futures/collections/{name}"
            resp = client.get(url, params={"page": 1, "page_size": 1})
            if resp.status_code != 200:
                failures.append(f"- {name}: HTTP {resp.status_code}  需求文档: {requirement_map[name]}")
                continue
            payload = resp.json()
            if not isinstance(payload, dict) or payload.get("success") is not True:
                failures.append(f"- {name}: 返回 {payload}  需求文档: {requirement_map[name]}")

        # Output summary before assertion
        summary_lines = [
            f"需要验证的数据集合数: {len(expected_collections)}",
            f"打开失败的数据集合数: {len(failures)}",
        ]
        if failures:
            summary_lines.append("打开失败清单:")
            summary_lines.extend(failures)
        summary = "\n".join(summary_lines)
        logging.info(summary)
        print(summary)

        assert not failures, (
            "以下集合打开失败，请根据需求文档修复相应后端注册/数据库配置/路由:\n" +
            "\n".join(failures)
        )
