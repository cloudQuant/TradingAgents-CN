"""
测试数据导出功能
使用 Playwright 自动化测试

验收条件：
1. 从 http://localhost:3000/funds/collections/fund_name_em 点击导出按钮
2. 选择 Excel 格式，全部数据
3. 点击导出能够成功，没有报错
4. 导出的文件名是 fund_name_em + 时间 的形式

运行方法：
pip install pytest-playwright
playwright install chromium
pytest tests/common/test_export_data.py -v
"""

import pytest
import re
import os
from datetime import datetime
from pathlib import Path
from playwright.sync_api import Page, expect, Download


# 测试配置
BASE_URL = "http://localhost:3000"
LOGIN_URL = f"{BASE_URL}/login"
COLLECTION_URL = f"{BASE_URL}/funds/collections/fund_name_em"
DOWNLOAD_DIR = Path(__file__).parent / "downloads"


@pytest.fixture(scope="function")
def setup_download_dir():
    """设置下载目录"""
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    yield DOWNLOAD_DIR
    # 清理下载的文件（可选）
    # for f in DOWNLOAD_DIR.glob("*"):
    #     f.unlink()


class TestExportData:
    """数据导出功能测试"""

    def login_and_open_collection(self, page: Page):
        """自动登录并打开集合页面"""
        page.goto(LOGIN_URL)

        # 输入账号密码
        page.fill('input[placeholder="请输入用户名"]', 'admin')
        page.fill('input[placeholder="请输入密码"]', 'admin123')

        # 点击登录
        page.click('button:has-text("登录")')

        # 等待登录完成
        page.wait_for_timeout(1000)

        # 进入集合页面
        page.goto(COLLECTION_URL)
        page.wait_for_selector(".el-table__body", timeout=30000)
        page.wait_for_timeout(1000)

    def test_export_current_page_csv(self, page: Page, setup_download_dir):
        """测试导出当前页数据为 CSV"""
        # 1. 登录并打开页面
        self.login_and_open_collection(page)
        
        # 2. 等待数据加载完成
        page.wait_for_selector(".el-table__body", timeout=30000)
        page.wait_for_timeout(1000)  # 额外等待确保数据加载
        
        # 3. 点击导出按钮（Excel 图标）
        export_button = page.locator(".export-icon")
        expect(export_button).to_be_visible()
        export_button.click()
        
        # 4. 等待导出对话框出现
        dialog = page.locator(".el-dialog").filter(has_text="导出数据")
        expect(dialog).to_be_visible()
        
        # 5. 选择 CSV 格式
        csv_radio = dialog.locator(".el-radio").filter(has_text="CSV")
        csv_radio.click()
        
        # 6. 确保选择当前页
        current_page_radio = dialog.locator(".el-radio").filter(has_text="当前页")
        current_page_radio.click()
        
        # 7. 验证文件名格式
        filename_input = dialog.locator("input").first
        filename_value = filename_input.input_value()
        
        # 文件名应该是 fund_name_em_YYYYMMDD_HHMMSS 格式
        assert filename_value.startswith("fund_name_em_"), f"文件名格式错误: {filename_value}"
        assert re.match(r"fund_name_em_\d{8}_\d{6}", filename_value), f"时间戳格式错误: {filename_value}"
        
        # 8. 点击导出按钮
        with page.expect_download() as download_info:
            export_btn = dialog.locator("button").filter(has_text="导出")
            export_btn.click()
        
        download: Download = download_info.value
        
        # 9. 验证下载的文件
        assert download.suggested_filename.endswith(".csv"), f"文件扩展名错误: {download.suggested_filename}"
        assert download.suggested_filename.startswith("fund_name_em_"), f"文件名前缀错误: {download.suggested_filename}"
        
        # 保存文件
        save_path = setup_download_dir / download.suggested_filename
        download.save_as(save_path)
        
        assert save_path.exists(), f"文件未保存: {save_path}"
        assert save_path.stat().st_size > 0, "文件内容为空"
        
        print(f"✅ CSV 导出成功: {save_path}")

    def test_export_current_page_xlsx(self, page: Page, setup_download_dir):
        """测试导出当前页数据为 Excel (XLSX)"""
        # 1. 登录并打开页面
        self.login_and_open_collection(page)
        
        # 2. 等待数据加载完成
        page.wait_for_selector(".el-table__body", timeout=30000)
        page.wait_for_timeout(1000)
        
        # 3. 点击导出按钮
        export_button = page.locator(".export-icon")
        export_button.click()
        
        # 4. 等待对话框
        dialog = page.locator(".el-dialog").filter(has_text="导出数据")
        expect(dialog).to_be_visible()
        
        # 5. 选择 Excel 格式（默认已选）
        xlsx_radio = dialog.locator(".el-radio").filter(has_text="Excel")
        xlsx_radio.click()
        
        # 6. 选择当前页
        current_page_radio = dialog.locator(".el-radio").filter(has_text="当前页")
        current_page_radio.click()
        
        # 7. 点击导出
        with page.expect_download() as download_info:
            export_btn = dialog.locator("button").filter(has_text="导出")
            export_btn.click()
        
        download: Download = download_info.value
        
        # 8. 验证文件
        assert download.suggested_filename.endswith(".xlsx"), f"文件扩展名错误: {download.suggested_filename}"
        assert download.suggested_filename.startswith("fund_name_em_"), f"文件名前缀错误: {download.suggested_filename}"
        
        save_path = setup_download_dir / download.suggested_filename
        download.save_as(save_path)
        
        assert save_path.exists(), f"文件未保存: {save_path}"
        assert save_path.stat().st_size > 0, "文件内容为空"
        
        print(f"✅ Excel 导出成功: {save_path}")

    def test_export_all_data_xlsx(self, page: Page, setup_download_dir):
        """测试导出全部数据为 Excel (XLSX) - 主要验收测试"""
        # 1. 登录并打开页面
        self.login_and_open_collection(page)
        
        # 2. 等待数据加载完成
        page.wait_for_selector(".el-table__body", timeout=30000)
        page.wait_for_timeout(2000)  # 等待更长时间确保完全加载
        
        # 3. 点击导出按钮
        export_button = page.locator(".export-icon")
        expect(export_button).to_be_visible()
        export_button.click()
        
        # 4. 等待对话框
        dialog = page.locator(".el-dialog").filter(has_text="导出数据")
        expect(dialog).to_be_visible()
        
        # 5. 选择 Excel 格式
        xlsx_radio = dialog.locator(".el-radio").filter(has_text="Excel")
        xlsx_radio.click()
        
        # 6. 选择全部数据
        all_data_radio = dialog.locator(".el-radio").filter(has_text="全部数据")
        all_data_radio.click()
        
        # 7. 验证文件名格式
        filename_input = dialog.locator("input").first
        filename_value = filename_input.input_value()
        
        # 验证文件名格式: fund_name_em_YYYYMMDD_HHMMSS
        assert filename_value.startswith("fund_name_em_"), f"文件名前缀错误: {filename_value}"
        timestamp_pattern = r"fund_name_em_\d{8}_\d{6}"
        assert re.match(timestamp_pattern, filename_value), f"时间戳格式错误: {filename_value}"
        
        print(f"📝 导出文件名: {filename_value}")
        
        # 8. 点击导出按钮并等待下载（可能需要较长时间）
        with page.expect_download(timeout=120000) as download_info:  # 2分钟超时
            export_btn = dialog.locator("button").filter(has_text="导出")
            export_btn.click()
            
            # 等待导出完成提示
            page.wait_for_timeout(5000)  # 等待API调用
        
        download: Download = download_info.value
        
        # 9. 验证下载的文件
        suggested_name = download.suggested_filename
        print(f"📁 下载文件: {suggested_name}")
        
        assert suggested_name.endswith(".xlsx"), f"文件扩展名错误: {suggested_name}"
        assert suggested_name.startswith("fund_name_em_"), f"文件名前缀错误: {suggested_name}"
        
        # 保存文件
        save_path = setup_download_dir / suggested_name
        download.save_as(save_path)
        
        assert save_path.exists(), f"文件未保存: {save_path}"
        file_size = save_path.stat().st_size
        assert file_size > 0, "文件内容为空"
        
        print(f"✅ 全部数据导出成功!")
        print(f"   文件路径: {save_path}")
        print(f"   文件大小: {file_size / 1024:.2f} KB")

    def test_export_dialog_cancel(self, page: Page):
        """测试取消导出"""
        # 1. 登录并打开页面
        self.login_and_open_collection(page)
        
        # 2. 点击导出按钮
        export_button = page.locator(".export-icon")
        export_button.click()
        
        # 3. 等待对话框
        dialog = page.locator(".el-dialog").filter(has_text="导出数据")
        expect(dialog).to_be_visible()
        
        # 4. 点击取消
        cancel_btn = dialog.locator("button").filter(has_text="取消")
        cancel_btn.click()
        
        # 5. 验证对话框关闭
        expect(dialog).not_to_be_visible()
        
        print("✅ 取消导出测试通过")

    def test_export_filename_format(self, page: Page):
        """测试导出文件名格式"""
        # 1. 登录并打开页面
        self.login_and_open_collection(page)

        # 3. 点击导出按钮
        export_button = page.locator(".export-icon")
        export_button.click()
        
        # 4. 等待对话框
        dialog = page.locator(".el-dialog").filter(has_text="导出数据")
        expect(dialog).to_be_visible()
        
        # 5. 获取文件名
        filename_input = dialog.locator("input").first
        filename_value = filename_input.input_value()

        # 6. 解析时间戳
        # 格式: fund_name_em_YYYYMMDD_HHMMSS
        match = re.match(r"fund_name_em_(\d{8})_(\d{6})", filename_value)
        assert match, f"文件名格式不匹配: {filename_value}"

        print(f"✅ 文件名格式验证通过: {filename_value}")


# 运行单个测试的入口
if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s", "--headed"])
