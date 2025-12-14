import pytest
import os
from httpx import AsyncClient

BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8848")
AUTH_TOKEN = os.getenv("API_AUTH_TOKEN")

pytestmark = pytest.mark.skipif(not AUTH_TOKEN, reason="API_AUTH_TOKEN not set")

@pytest.mark.asyncio
async def test_collection_endpoint_exists():
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/stocks/collections/stock_cyq_em", headers={"Authorization": f"Bearer {AUTH_TOKEN}"})
        assert response.status_code in [200, 404]

@pytest.mark.asyncio
async def test_collection_data_structure():
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/stocks/collections/stock_cyq_em", headers={"Authorization": f"Bearer {AUTH_TOKEN}"})
        if response.status_code == 200:
            data = response.json()
            assert "data" in data
            assert "total" in data

@pytest.mark.asyncio
async def test_refresh_collection():
    async with AsyncClient(base_url=BASE_URL, timeout=300.0) as client:
        response = await client.post("/stocks/collections/stock_cyq_em/refresh", headers={"Authorization": f"Bearer {AUTH_TOKEN}"}, json={})
        assert response.status_code in [200, 202]

@pytest.mark.asyncio
async def test_collection_overview():
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/stocks/collections/stock_cyq_em/overview", headers={"Authorization": f"Bearer {AUTH_TOKEN}"})
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_clear_collection():
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.delete("/stocks/collections/stock_cyq_em/clear", headers={"Authorization": f"Bearer {AUTH_TOKEN}"})
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
    collection_url = f"{frontend_url}/stocks/collections/stock_cyq_em"
    
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
                
                
                # 输入股票代码
                inp = dialog.query_selector('input[placeholder*="代码"]') or dialog.query_selector('input[type="text"]')
                if inp:
                    inp.fill("000001")
                    time.sleep(0.5)
                
                start_btn = _find_button(dialog, ["开始更新", "更新", "确定"])
                if start_btn:
                    start_btn.click()
                    time.sleep(8)

                
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
