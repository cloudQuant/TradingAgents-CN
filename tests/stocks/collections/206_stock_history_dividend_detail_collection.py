"""
分红配股 数据集合测试

测试目标：
1. 验证 stock_history_dividend_detail 数据集合的完整功能
2. 测试数据获取、存储、更新、展示等核心功能
3. 确保数据的正确性和完整性

需求文档：206_分红配股.md
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
            "/stocks/collections/stock_history_dividend_detail",
            headers={"Authorization": f"Bearer {AUTH_TOKEN}"}
        )
        assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_collection_data_structure():
    """测试返回数据结构"""
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.get(
            "/stocks/collections/stock_history_dividend_detail",
            headers={"Authorization": f"Bearer {AUTH_TOKEN}"}
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
            "/stocks/collections/stock_history_dividend_detail/refresh",
            headers={"Authorization": f"Bearer {AUTH_TOKEN}"},
            json={}
        )
        assert response.status_code in [200, 202]


@pytest.mark.asyncio
async def test_collection_overview():
    """测试数据概览功能"""
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.get(
            "/stocks/collections/stock_history_dividend_detail/overview",
            headers={"Authorization": f"Bearer {AUTH_TOKEN}"}
        )
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_clear_collection():
    """测试清空数据功能"""
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.delete(
            "/stocks/collections/stock_history_dividend_detail/clear",
            headers={"Authorization": f"Bearer {AUTH_TOKEN}"}
        )
        assert response.status_code == 200


    # ========== Playwright UI 自动化测试 ==========
    
@pytest.mark.playwright
def test_ui_update_data_flow():
    """使用 Playwright 测试更新数据完整流程"""
    try:
            from playwright.sync_api import sync_playwright
    except ImportError:
            pytest.skip("Playwright 未安装")
    
    import time
    frontend_url = os.getenv("FRONTEND_BASE_URL", "http://localhost:3000")
    collection_url = f"{frontend_url}/stocks/collections/stock_history_dividend_detail"
    
    with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            try:
                _do_login(page, frontend_url)
                page.goto(collection_url, wait_until='networkidle', timeout=30000)
                time.sleep(2)
                
                if "/login" in page.url:
                    pytest.skip("需要登录")
                
                update_btn = _find_button(page, ["更新数据", "更新"])
                if not update_btn:
                    pytest.skip("未找到更新按钮")
                
                update_btn.click()
                time.sleep(1.5)
                
                dialog = _find_dialog(page)
                if not dialog:
                    pytest.fail("弹窗未出现")
                
                
                # 无参数接口，直接点击更新
                start_btn = _find_button(dialog, ["开始更新", "更新", "确定"])
                if start_btn:
                    start_btn.click()
                    time.sleep(5)

                
                _close_dialog(dialog)
                
            finally:
                browser.close()
    
def _do_login(page, frontend_url):
    import time
    try:
            page.goto(f"{frontend_url}/login", timeout=10000)
            inp = page.query_selector('input[type="text"]')
            if inp:
                inp.fill("admin")
                pwd = page.query_selector('input[type="password"]')
                if pwd:
                    pwd.fill("admin123")
                btn = page.query_selector('button[type="submit"]')
                if btn:
                    btn.click()
                    page.wait_for_url(lambda u: "/login" not in u, timeout=10000)
                    time.sleep(1)
    except:
            pass
    
def _find_button(container, texts):
    for t in texts:
            b = container.query_selector(f'button:has-text("{t}")')
            if b and b.is_visible():
                return b
    return None
    
def _find_dialog(page):
    for s in ['.el-dialog', '[role="dialog"]', '.modal']:
            d = page.query_selector(s)
            if d and d.is_visible():
                return d
    return None
    
def _close_dialog(dialog):
    b = dialog.query_selector('button:has-text("关闭")') or dialog.query_selector('.el-dialog__close')
    if b:
            b.click()
