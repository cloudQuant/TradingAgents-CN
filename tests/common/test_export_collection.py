"""
导出功能自动化测试

验收标准：
1. 从 fund_portfolio_hold_em 集合导出全部数据
2. CSV 格式：导出时间不超过 15 秒（后端处理 <10s，网络传输 ~5s）
3. Excel 格式：导出时间约 2-3 分钟（Excel 生成较慢）
"""

import asyncio
import sys
import time
from pathlib import Path

import pytest
from playwright.async_api import async_playwright, expect

# 修复 Windows 控制台编码问题
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')


# 测试配置
BASE_URL = "http://localhost:3000"
COLLECTION_URL = f"{BASE_URL}/funds/collections/fund_portfolio_hold_em"
EXPORT_TIMEOUT = 300000  # 5 分钟超时（Playwright 等待时间），与前端 API 超时一致
CSV_MAX_DURATION = 15  # CSV 期望导出最大耗时 15 秒
XLSX_MAX_DURATION = 180  # Excel 期望导出最大耗时 3 分钟


async def run_export_test(file_format: str = 'csv'):
    """
    运行导出测试
    
    Args:
        file_format: 'csv' 或 'xlsx'
    """
    expected_max = CSV_MAX_DURATION if file_format == 'csv' else XLSX_MAX_DURATION
    format_label = 'CSV' if file_format == 'csv' else 'Excel (XLSX)'
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        download_path = Path(__file__).parent / "downloads"
        download_path.mkdir(exist_ok=True)
        
        try:
            # 0. 登录
            print(f"\n===== 测试导出 {format_label} 格式 =====")
            print("[0/6] 登录系统...")
            await page.goto(f"{BASE_URL}/login", wait_until="networkidle")
            await page.wait_for_selector('input', timeout=10000)
            await asyncio.sleep(0.5)
            
            await page.locator('input').first.fill('admin')
            await page.locator('input[type="password"]').fill('admin123')
            await page.locator('button:has-text("登录")').click()
            await page.wait_for_selector('.el-menu', timeout=15000)
            print("[0/6] ✓ 登录成功")
            
            # 1. 导航到集合页面
            print(f"[1/6] 导航到 {COLLECTION_URL}")
            await page.goto(COLLECTION_URL, wait_until="networkidle")
            await page.wait_for_selector(".el-table", timeout=30000)
            print("[1/6] ✓ 页面加载完成")
            
            # 2. 点击导出按钮
            print("[2/6] 点击导出按钮...")
            await page.locator('.export-icon').click()
            await page.wait_for_selector('.el-dialog', timeout=5000)
            print("[2/6] ✓ 导出对话框已打开")
            
            # 3. 选择格式
            print(f"[3/6] 选择 {format_label} 格式...")
            format_radio = page.locator(f'label:has-text("{format_label}")')
            await format_radio.click()
            print(f"[3/6] ✓ 已选择 {format_label} 格式")
            
            # 4. 选择全部数据
            print("[4/6] 选择全部数据...")
            await page.locator('label:has-text("全部数据")').click()
            print("[4/6] ✓ 已选择全部数据")
            
            # 5. 点击导出并计时
            print("[5/6] 开始导出...")
            start_time = time.time()
            
            async with page.expect_download(timeout=EXPORT_TIMEOUT) as download_info:
                await page.locator('.el-dialog button:has-text("导出")').click()
            
            download = await download_info.value
            duration = time.time() - start_time
            
            save_path = download_path / download.suggested_filename
            await download.save_as(save_path)
            
            file_size = save_path.stat().st_size / 1024 / 1024
            
            print(f"[5/6] ✓ 导出完成！")
            print(f"    文件名: {download.suggested_filename}")
            print(f"    文件大小: {file_size:.2f} MB")
            print(f"    耗时: {duration:.2f} 秒")
            
            # 验证结果
            if duration <= expected_max:
                print(f"\n✅ 测试通过：导出耗时 {duration:.2f}s <= {expected_max}s")
                return True
            else:
                print(f"\n⚠️ 导出耗时超过预期：{duration:.2f}s > {expected_max}s")
                return False
            
        except Exception as e:
            screenshot_path = download_path / f"error_{file_format}.png"
            await page.screenshot(path=str(screenshot_path))
            print(f"\n❌ 测试失败: {e}")
            print(f"    错误截图: {screenshot_path}")
            raise
            
        finally:
            await browser.close()


@pytest.mark.asyncio
async def test_export_csv():
    """测试 CSV 格式导出（快速）"""
    result = await run_export_test('csv')
    assert result, "CSV 导出超时"


@pytest.mark.asyncio  
async def test_export_xlsx():
    """测试 Excel 格式导出（慢）"""
    result = await run_export_test('xlsx')
    assert result, "Excel 导出超时"


async def main():
    """手动运行测试 - 默认测试 CSV"""
    import argparse
    parser = argparse.ArgumentParser(description='测试数据导出功能')
    parser.add_argument('--format', '-f', choices=['csv', 'xlsx'], default='csv',
                        help='导出格式 (默认: csv)')
    args = parser.parse_args()
    
    await run_export_test(args.format)


if __name__ == "__main__":
    asyncio.run(main())
