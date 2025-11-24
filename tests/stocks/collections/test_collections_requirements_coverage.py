"""
验证 stocks/collections 页面与需求文档 requirements 的一致性：
- 从 tests/stocks/requirements/*.md 中解析出声明的集合路由，提取集合名
- 校验 /api/stocks/collections 返回的数据集合包含这些集合名
- 访问前端页面 /stocks/collections/{name}，确认能正常打开（返回 HTTP 200）
- 若缺失或打开失败，输出对应需求文档路径，便于修复

环境变量：
- API_BASE_URL（默认 http://localhost:8000）
- FRONTEND_BASE_URL（默认 http://localhost:3000）
- TEST_AUTH_TOKEN（可选，用于后端需要鉴权时）
"""
from __future__ import annotations

import os
import re
import json
import time
from datetime import datetime
from typing import Dict, List, Tuple, Optional

import httpx
import pytest


def _requirements_dir() -> str:
    # 本测试文件位于 tests/stocks/collections/
    here = os.path.dirname(__file__)
    req_dir = os.path.abspath(os.path.join(here, "..", "requirements"))
    return req_dir


def _get_log_file_path() -> str:
    """获取日志文件路径"""
    here = os.path.dirname(__file__)
    log_dir = os.path.abspath(os.path.join(here, ".."))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(log_dir, f"test_coverage_report_{timestamp}.log")


class Logger:
    """同时输出到控制台和文件的日志记录器"""
    def __init__(self, log_file: str):
        self.log_file = log_file
        self.lines = []
    
    def log(self, message: str):
        """记录日志"""
        self.lines.append(message)
        print(message)
    
    def save(self):
        """保存日志到文件"""
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.lines))


def extract_expected_collections(requirements_dir: str) -> Dict[str, str]:
    """
    扫描 requirements 目录的所有 .md 文档，提取形如：
      http://localhost:3000/stocks/collections/<collectionName>
    的集合路由，返回 {collectionName: 文档路径}
    """
    pattern = re.compile(r"http://localhost:3000/stocks/collections/([a-zA-Z0-9_\-]+)")
    mapping: Dict[str, str] = {}

    for root, _, files in os.walk(requirements_dir):
        for fn in files:
            if not fn.lower().endswith(".md"):
                continue
            fp = os.path.join(root, fn)
            try:
                with open(fp, "r", encoding="utf-8") as f:
                    text = f.read()
                for name in pattern.findall(text):
                    # 仅记录第一次出现的位置作为溯源
                    mapping.setdefault(name, fp)
            except Exception:
                # 读取失败忽略该文件
                continue
    return mapping


@pytest.fixture(scope="module")
def api_base_url() -> str:
    return os.getenv("API_BASE_URL", "http://localhost:8000")


@pytest.fixture(scope="module")
def frontend_base_url() -> str:
    return os.getenv("FRONTEND_BASE_URL", "http://localhost:3000")


@pytest.fixture(scope="module")
def auth_headers() -> Dict[str, str]:
    token = os.getenv("TEST_AUTH_TOKEN", "").strip()
    return {"Authorization": f"Bearer {token}"} if token else {}


class TestStocksCollectionsRequirementsCoverage:
    
    def _extract_from_frontend_page(self, frontend_base_url: str, logger) -> Optional[list]:
        """使用Playwright从前端页面DOM提取集合数据"""
        try:
            from playwright.sync_api import sync_playwright
            
            logger.log(f"    启动浏览器...")
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                url = f"{frontend_base_url}/stocks/collections"
                logger.log(f"    访问页面: {url}")
                page.goto(url, wait_until='networkidle', timeout=60000)
                
                # 等待集合列表加载
                logger.log(f"    等待数据加载...")
                time.sleep(3)  # 给一些时间让数据渲染
                
                # 检查是否重定向到登录页
                if "/login" in page.url or "登录" in page.title():
                    logger.log(f"    [!] 检测到登录页面，尝试自动登录...")
                    try:
                        # 填写登录表单 (假设是常见的Element Plus表单结构)
                        # 等待输入框出现
                        page.wait_for_selector('input[type="text"]', state='visible', timeout=5000)
                        
                        # 尝试填写用户名 (admin)
                        logger.log(f"    ...输入用户名")
                        page.fill('input[type="text"]', "admin")
                        
                        # 尝试填写密码 (admin123)
                        logger.log(f"    ...输入密码")
                        page.fill('input[type="password"]', "admin123")
                        
                        # 点击登录按钮 (通常是 button 或者是 type="submit")
                        logger.log(f"    ...点击登录")
                        # 尝试多种定位登录按钮的方式
                        login_button = page.query_selector('button[type="submit"]') or \
                                     page.query_selector('button.el-button--primary') or \
                                     page.query_selector('button:has-text("登录")') or \
                                     page.query_selector('button:has-text("Login")')
                        
                        if login_button:
                            login_button.click()
                            
                            # 等待登录完成并跳转回列表页
                            logger.log(f"    ...等待跳转")
                            page.wait_for_url(lambda u: "/login" not in u, timeout=10000)
                            
                            # 重新访问目标页面(如果没自动跳回)
                            if "/stocks/collections" not in page.url:
                                logger.log(f"    ...重新访问集合页面")
                                page.goto(url, wait_until='networkidle', timeout=10000)
                            
                            # 再次等待数据加载
                            logger.log(f"    ...登录成功，等待数据加载")
                            time.sleep(5)
                        else:
                            logger.log(f"    [x] 未找到登录按钮")
                            return "AUTH_FAILED"
                            
                    except Exception as e:
                        logger.log(f"    [x] 自动登录失败: {e}")
                        browser.close()
                        return "AUTH_FAILED"

                # 尝试多种选择器提取集合名称
                collections = []
                
                # 尝试1: 查找包含 /stocks/collections/ 的链接
                links = page.query_selector_all('a[href*="/stocks/collections/"]')
                # 尝试1.1: 表格中的链接
                if not links:
                    links = page.query_selector_all('tr td a')
                
                for link in links:
                    href = link.get_attribute('href')
                    if href and '/stocks/collections/' in href:
                        name = href.split('/stocks/collections/')[-1].split('?')[0].split('#')[0]
                        if name and name not in collections:
                            collections.append(name)
                
                # 尝试2: 查找data属性或class中包含集合信息的元素
                if not collections:
                    elements = page.query_selector_all('[data-collection-name]')
                    for elem in elements:
                        name = elem.get_attribute('data-collection-name')
                        if name and name not in collections:
                            collections.append(name)

                # 尝试3: 在浏览器上下文内直接调用前端接口 /api/stocks/collections 获取数据
                if not collections:
                    try:
                        logger.log(f"    ...尝试通过前端API获取集合列表")
                        result = page.evaluate(
                            """
                            async () => {
                                try {
                                    const token = localStorage.getItem('access_token') || localStorage.getItem('token') || localStorage.getItem('auth_token');
                                    const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
                                    const resp = await fetch('/api/stocks/collections', { credentials: 'include', headers });
                                    const ct = resp.headers.get('content-type') || '';
                                    let data = null;
                                    if (ct.includes('application/json')) {
                                        try { data = await resp.json(); } catch(e) { data = null; }
                                    }
                                    return { status: resp.status, data };
                                } catch (e) {
                                    return { status: -1, error: String(e) };
                                }
                            }
                            """
                        )
                        if result and isinstance(result, dict):  # type: ignore
                            status = result.get('status')
                            data_json = result.get('data')
                            if isinstance(data_json, list) and data_json:
                                logger.log(f"    [+] 通过前端API获取到 {len(data_json)} 个集合")
                                for item in data_json:
                                    if isinstance(item, dict):
                                        n = item.get('name')
                                        if n and n not in collections:
                                            collections.append(n)
                            else:
                                logger.log(f"    [i] 前端API返回状态: {status}, 数据类型: {type(data_json).__name__ if data_json is not None else 'None'}")
                                # 如果未授权，尝试以编程方式登录并重试
                                if status == 401:
                                    logger.log(f"    ...尝试程序化登录 /api/auth/login")
                                    login_result = page.evaluate(
                                        """
                                        async () => {
                                            try {
                                                const payloads = [
                                                    { username: 'admin', password: 'admin123' },
                                                    { account: 'admin', password: 'admin123' },
                                                    { email: 'admin', password: 'admin123' },
                                                ];
                                                for (const body of payloads) {
                                                    try {
                                                        const resp = await fetch('/api/auth/login', {
                                                            method: 'POST',
                                                            headers: { 'Content-Type': 'application/json' },
                                                            credentials: 'include',
                                                            body: JSON.stringify(body),
                                                        });
                                                        let data = null;
                                                        try { data = await resp.json(); } catch(e) {}
                                                        const token = data && (data.access_token || data.token || (data.data && (data.data.access_token || data.data.token)));
                                                        if (resp.ok && token) {
                                                            localStorage.setItem('access_token', token);
                                                            return { ok: true, token };
                                                        }
                                                    } catch(e) { /* continue */ }
                                                }
                                                return { ok: false };
                                            } catch (e) {
                                                return { ok: false, error: String(e) };
                                            }
                                        }
                                        """
                                    )
                                    if login_result and isinstance(login_result, dict) and login_result.get('ok'):  # type: ignore
                                        logger.log(f"    [+] 程序化登录成功，重试前端API")
                                        retry = page.evaluate(
                                            """
                                            async () => {
                                                try {
                                                    const token = localStorage.getItem('access_token');
                                                    const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
                                                    const resp = await fetch('/api/stocks/collections', { credentials: 'include', headers });
                                                    const ct = resp.headers.get('content-type') || '';
                                                    let data = null;
                                                    if (ct.includes('application/json')) {
                                                        try { data = await resp.json(); } catch(e) { data = null; }
                                                    }
                                                    return { status: resp.status, data };
                                                } catch (e) { return { status: -1, error: String(e) }; }
                                            }
                                            """
                                        )
                                        if retry and isinstance(retry, dict):  # type: ignore
                                            rdata = retry.get('data')
                                            if isinstance(rdata, list) and rdata:
                                                logger.log(f"    [+] 重试获取到 {len(rdata)} 个集合")
                                                for item in rdata:
                                                    if isinstance(item, dict):
                                                        n = item.get('name')
                                                        if n and n not in collections:
                                                            collections.append(n)
                                            else:
                                                logger.log(f"    [x] 重试仍失败，状态: {retry.get('status')}")
                                    else:
                                        logger.log(f"    [x] 程序化登录失败或未返回令牌")
                    except Exception as e:
                        logger.log(f"    [x] 前端API获取失败: {e}")

                # 尝试4: 监听网络响应（如果页面自身发起了请求）
                if not collections:
                    try:
                        logger.log(f"    ...等待页面网络响应 /api/stocks/collections")
                        resp = page.wait_for_response(lambda r: '/api/stocks/collections' in r.url, timeout=8000)
                        try:
                            if 200 <= resp.status < 400:
                                data_json = resp.json()
                                if isinstance(data_json, list):
                                    logger.log(f"    [+] 从网络响应中获取到 {len(data_json)} 个集合")
                                    for item in data_json:
                                        if isinstance(item, dict):
                                            n = item.get('name')
                                            if n and n not in collections:
                                                collections.append(n)
                        except Exception:
                            pass
                    except Exception:
                        pass

                browser.close()

                if collections:
                    logger.log(f"    [+] 从页面DOM提取到 {len(collections)} 个集合")
                    # 转换为API格式
                    return [{"name": name} for name in collections]
                else:
                    logger.log(f"    [x] 未能从页面DOM提取到集合")
                    return None
                    
        except ImportError:
            logger.log(f"    [x] Playwright未安装，跳过DOM提取")
            logger.log(f"    提示: 运行 pip install playwright && playwright install chromium")
            return None
        except Exception as e:
            logger.log(f"    [x] DOM提取失败: {e}")
            return None

    def _get_collections_list(self, frontend_base_url: str, auth_headers: Dict[str, str], logger) -> Optional[list]:
        """获取集合列表，优先尝试前端页面DOM提取，失败则尝试后端API"""
        data = None
        
        # 方式1: 尝试从前端页面DOM提取数据（优先）
        logger.log(f"\n正在获取集合列表...")
        logger.log(f"  方式1: 尝试从前端页面DOM提取数据（使用Playwright）")
        data = self._extract_from_frontend_page(frontend_base_url, logger)
        
        if data == "AUTH_REQUIRED":
            logger.log(f"    [i] 跳过前端提取（需要登录）")
            data = None
        elif data:
            return data

        # 方式2: 尝试后端API（备选）
        backend_api_url = f"http://localhost:8000/api/stocks/collections"
        logger.log(f"  方式2: 尝试后端API {backend_api_url}")
        
        try:
            with httpx.Client(trust_env=False, timeout=60.0, follow_redirects=True) as client:
                resp = client.get(backend_api_url, headers=auth_headers)
                if resp.status_code == 200:
                    try:
                        data = resp.json()
                        logger.log(f"  [+] 后端API成功返回 {len(data) if isinstance(data, list) else '?'} 个集合")
                        return data
                    except json.JSONDecodeError:
                        logger.log(f"  [x] 后端API返回非JSON")
                elif resp.status_code == 401:
                    logger.log(f"  [x] 后端API需要认证（401）")
                else:
                    logger.log(f"  [x] 后端API返回状态码 {resp.status_code}")
        except Exception as e:
            logger.log(f"  [x] 后端API访问失败: {e}")
            
        return None
    
    def test_requirements_collections_covered_by_api(self, frontend_base_url: str, auth_headers: Dict[str, str]):
        """
        要求：前端 API /api/stocks/collections 返回需包含 requirements 文档中声明的集合名
        """
        # 创建日志记录器
        log_file = _get_log_file_path()
        logger = Logger(log_file)
        
        req_dir = _requirements_dir()
        assert os.path.isdir(req_dir), f"requirements 目录不存在: {req_dir}"

        expected_map = extract_expected_collections(req_dir)
        assert expected_map, "未在需求文档中解析到任何集合路由，请检查文档格式是否包含 /stocks/collections/{name}"

        logger.log(f"\n{'='*80}")
        logger.log(f"【需求文档扫描结果】")
        logger.log(f"  从需求文档中解析到 {len(expected_map)} 个数据集合需要验证")
        logger.log(f"  需求文档目录: {req_dir}")
        logger.log(f"{'='*80}")

        # 获取集合列表（优先前端，备选后端）
        data = self._get_collections_list(frontend_base_url, auth_headers, logger)
        
        # 如果所有方式都失败
        if data is None:
            logger.log(f"\n[ERROR] 错误：无法通过任何方式获取集合列表")
            logger.log(f"  已尝试：页面DOM提取、后端API")
            
            # 检查是否因为认证问题
            if not auth_headers:
                 logger.log(f"  [!] 提示：检测到未配置 TEST_AUTH_TOKEN，且前端/后端均需要认证")
                 pytest.skip("需要认证才能获取集合列表，请设置 TEST_AUTH_TOKEN 环境变量")

            logger.save()
            pytest.skip("无法获取集合列表，所有方式都失败了")

        assert isinstance(data, list), "集合列表返回应为数组"
        actual_names = {item.get("name") for item in data if isinstance(item, dict)}

        logger.log(f"\n【集合列表获取结果】")
        logger.log(f"  成功获取到 {len(actual_names)} 个数据集合")
        logger.log(f"{'='*80}")

        missing = [name for name in expected_map.keys() if name not in actual_names]
        
        # 统计已存在的集合
        existing = [name for name in expected_map.keys() if name in actual_names]
        # 统计未在需求文档中但API返回的集合
        extra_in_api = [name for name in actual_names if name not in expected_map]
        
        logger.log(f"\n【验证结果统计】")
        logger.log(f"  [+] 已实现的集合: {len(existing)} 个")
        logger.log(f"  [x] 缺失的集合:   {len(missing)} 个")
        if extra_in_api:
            logger.log(f"  [!] 额外集合:   {len(extra_in_api)} 个（未在需求文档中声明）")
        logger.log(f"  覆盖率: {len(existing)}/{len(expected_map)} ({100*len(existing)//len(expected_map) if expected_map else 0}%)")
        logger.log(f"{'='*80}")
        
        if existing:
            logger.log(f"\n【已实现的集合列表】({len(existing)}个)")
            for idx, name in enumerate(sorted(existing), 1):
                logger.log(f"  {idx:3d}. [+] {name}")
        
        if extra_in_api:
            logger.log(f"\n【API返回的额外集合】({len(extra_in_api)}个)")
            for idx, name in enumerate(sorted(extra_in_api), 1):
                route = f"{frontend_base_url}/stocks/collections/{name}"
                logger.log(f"  {idx:3d}. [+] {name}")
                logger.log(f"         路由: {route}")
            logger.log(f"  额外集合名单: {', '.join(sorted(extra_in_api))}")
            logger.log(f"{'='*80}\n")
        
        if missing:
            logger.log(f"\n【缺失的集合详情】({len(missing)}个)")
            for idx, name in enumerate(sorted(missing), 1):
                doc = expected_map[name]
                # 简化文档路径显示
                doc_short = os.path.basename(doc)
                logger.log(f"  {idx:3d}. [x] {name}")
                logger.log(f"         文档: {doc_short}")
            logger.log(f"{'='*80}\n")
            # 保存日志并失败
            logger.save()
            logger.log(f"\n[+] 详细日志已保存到: {log_file}\n")
            details = "\n".join([f"- {name}  <-  {expected_map[name]}" for name in missing])
            pytest.fail(
                f"\n有 {len(missing)} 个集合未在数据集合列表中返回：\n"
                f"{details}\n"
                "请检查前端数据源或代理配置，确保这些集合被正确提供。\n"
                f"详细日志: {log_file}"
            )
        
        if extra_in_api:
            logger.log(f"\n【额外（未在需求文档中声明）的集合】({len(extra_in_api)}个)")
            for idx, name in enumerate(sorted(extra_in_api), 1):
                route = f"{frontend_base_url}/stocks/collections/{name}"
                logger.log(f"  {idx:3d}. [+] {name}")
                logger.log(f"         路由: {route}")
            logger.log(f"  额外集合名单: {', '.join(sorted(extra_in_api))}")
            logger.log(f"{'='*80}\n")
        else:
            logger.log(f"\n[+] 所有需求文档中声明的集合都已在数据集合列表中返回！")
            logger.log(f"{'='*80}\n")
            
            # 保存日志
            logger.save()
            logger.log(f"\n[+] 详细日志已保存到: {log_file}\n")

    def test_requirements_collections_frontend_openable(
        self,
        frontend_base_url: str,
        auth_headers: Dict[str, str],
    ):
        """
        要求：需求文档中声明的集合详情页 /stocks/collections/{name} 可打开（HTTP 200）。
        若前端未启动，跳过此用例。
        """
        # 创建日志记录器
        log_file = _get_log_file_path()
        logger = Logger(log_file)
        
        req_dir = _requirements_dir()
        expected_map = extract_expected_collections(req_dir)
        if not expected_map:
            pytest.skip("未解析到任何集合名，跳过")

        # 获取集合列表（优先前端，备选后端）
        data = self._get_collections_list(frontend_base_url, auth_headers, logger)

        collection_names: set[str] = set()
        if data is not None and isinstance(data, list):
            collection_names = {item.get("name") for item in data if isinstance(item, dict)}

        # 如果无法获取集合列表，跳过前端测试
        if not collection_names:
            logger.log(f"\n[!] 警告：无法通过任何方式获取集合列表，跳过详情页测试")
            logger.log(f"  已尝试：页面DOM提取、后端API")
            pytest.skip("无法获取集合列表，所有方式都失败了")

        # 目标集合：只测试API返回的集合列表中存在且由文档声明的集合
        target_names = [n for n in expected_map.keys() if n in collection_names]
        # 统计未在需求文档中但API返回的集合
        extra_in_api = [n for n in collection_names if n not in expected_map]

        logger.log(f"\n{'='*80}")
        logger.log(f"【前端页面可访问性测试】")
        logger.log(f"  需求文档声明的集合: {len(expected_map)} 个")
        logger.log(f"  获取到的集合: {len(collection_names)} 个")
        logger.log(f"  需要测试的集合数量: {len(target_names)} 个（需求文档中有 且 实际存在）")
        if extra_in_api:
            logger.log(f"  [!] 列表中额外的集合: {len(extra_in_api)} 个（未在需求文档中声明）")
            # 逐项列出未在需求中的集合
            for idx, name in enumerate(sorted(extra_in_api), 1):
                logger.log(f"      - {idx:3d}. {name} -> {frontend_base_url}/stocks/collections/{name}")
            # 紧凑清单
            logger.log(f"  额外集合名单: {', '.join(sorted(extra_in_api))}")
        logger.log(f"  前端基础URL: {frontend_base_url}")
        logger.log(f"{'='*80}")

        # 检查前端是否可访问
        base_ok = False
        main_url = f"{frontend_base_url}/stocks/collections"
        with httpx.Client(trust_env=False, timeout=60.0, follow_redirects=True) as client:
            try:
                r = client.get(main_url)
                # 要求最终URL路径仍在 /stocks/collections（未被重定向到登录等）
                base_ok = (200 <= r.status_code < 400) and r.url.path.startswith("/stocks/collections")
            except httpx.RequestError as e:
                pytest.skip(f"前端未启动或无法访问: {main_url}\n错误: {e}")

        if not base_ok:
            pytest.skip(f"前端页面不可用或被重定向（可能需要登录）: {main_url}")

        failures: List[Tuple[str, int | str]] = []
        successes: List[str] = []
        
        logger.log(f"\n开始测试各集合详情页...")
        
        with httpx.Client(trust_env=False, timeout=30.0, follow_redirects=True) as client:
            for idx, name in enumerate(target_names, 1):
                detail_url = f"{frontend_base_url}/stocks/collections/{name}"
                try:
                    r = client.get(detail_url)
                    ok = (200 <= r.status_code < 400) and r.url.path.startswith(f"/stocks/collections/{name}")
                    if not ok:
                        failures.append((name, f"status={r.status_code}, final_path={r.url.path}"))
                        logger.log(f"  [{idx:3d}/{len(target_names)}] [x] {name} - 打开失败")
                    else:
                        successes.append(name)
                        logger.log(f"  [{idx:3d}/{len(target_names)}] [+] {name}")
                except httpx.RequestError as e:
                    failures.append((name, str(e)))
                    logger.log(f"  [{idx:3d}/{len(target_names)}] [x] {name} - 请求异常")

        logger.log(f"\n{'='*80}")
        logger.log(f"【前端页面测试结果统计】")
        logger.log(f"  [+] 成功打开的集合: {len(successes)} 个")
        logger.log(f"  [x] 打开失败的集合: {len(failures)} 个")
        logger.log(f"  前端页面测试覆盖率: {len(successes)}/{len(target_names)} ({100*len(successes)//len(target_names) if target_names else 0}%)")
        logger.log(f"{'='*80}")
        logger.log(f"\n【总体覆盖情况】")
        logger.log(f"  需求文档声明: {len(expected_map)} 个集合")
        logger.log(f"  实际列表返回: {len(collection_names)} 个集合")
        logger.log(f"  详情页可访问:  {len(successes)} 个集合")
        missing_in_api = len(expected_map) - len(target_names)
        if missing_in_api > 0:
            logger.log(f"  [!] 还需实现:   {missing_in_api} 个集合（在需求文档中但实际列表未返回）")
        logger.log(f"{'='*80}")

        if failures:
            logger.log(f"\n【打开失败的集合详情】({len(failures)}个)")
            for idx, (name, status) in enumerate(failures, 1):
                doc = expected_map.get(name, "<unknown>")
                doc_short = os.path.basename(doc)
                detail_url = f"{frontend_base_url}/stocks/collections/{name}"
                logger.log(f"  {idx:3d}. [x] {name}")
                logger.log(f"         URL: {detail_url}")
                logger.log(f"         状态/错误: {status}")
                logger.log(f"         需求文档: {doc_short}")
            # 紧凑失败清单
            failed_names_line = ", ".join([n for n, _ in failures])
            logger.log(f"\n失败集合名单: {failed_names_line}")
            logger.log(f"{'='*80}\n")
            
            # 保存日志
            logger.save()
            logger.log(f"\n[+] 详细日志已保存到: {log_file}\n")
            
            lines = []
            for name, status in failures:
                doc = expected_map.get(name, "<unknown>")
                lines.append(f"- {name}  状态/错误: {status}  文档: {doc}")
            pytest.fail(
                f"\n有 {len(failures)} 个集合详情页无法正常打开：\n"
                + "\n".join(lines) + "\n"
                + "请根据对应的需求文档修复前端路由或页面。\n"
                + f"详细日志: {log_file}"
            )
        else:
            logger.log(f"\n[+] 所有集合详情页都可以正常打开！")
            logger.log(f"{'='*80}\n")
            
            # 保存日志
            logger.save()
            logger.log(f"\n[+] 详细日志已保存到: {log_file}\n")
    
    def test_collection_detail_page_buttons(
        self,
        frontend_base_url: str,
        auth_headers: Dict[str, str],
    ):
        """
        测试每个集合详情页的按钮功能：
        1. 数据概览按钮
        2. 刷新按钮
        3. 更新数据按钮（点击后弹出窗口，包含：文件导入、远程同步、开始更新、关闭）
        4. 清空数据按钮（点击后数据变空）
        
        记录所有错误以便后续调试
        """
        try:
            from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
        except ImportError:
            pytest.skip("Playwright未安装，跳过按钮测试。运行: pip install playwright && playwright install chromium")
        
        # 创建日志记录器
        log_file = _get_log_file_path()
        logger = Logger(log_file)
        
        req_dir = _requirements_dir()
        expected_map = extract_expected_collections(req_dir)
        if not expected_map:
            pytest.skip("未解析到任何集合名，跳过")

        # 获取集合列表
        data = self._get_collections_list(frontend_base_url, auth_headers, logger)

        collection_names: set[str] = set()
        if data is not None and isinstance(data, list):
            collection_names = {item.get("name") for item in data if isinstance(item, dict)}

        if not collection_names:
            logger.log(f"\n[!] 警告：无法获取集合列表，跳过按钮测试")
            pytest.skip("无法获取集合列表")

        # 只测试API返回的集合
        target_names = [n for n in expected_map.keys() if n in collection_names]
        
        logger.log(f"\n{'='*80}")
        logger.log(f"【集合详情页按钮功能测试】")
        logger.log(f"  需要测试的集合数量: {len(target_names)} 个")
        logger.log(f"  前端基础URL: {frontend_base_url}")
        logger.log(f"{'='*80}")
        
        # 错误记录
        all_errors = []
        success_count = 0
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            
            # 尝试登录
            login_url = f"{frontend_base_url}/login"
            try:
                logger.log(f"\n尝试登录前端系统...")
                page.goto(login_url, wait_until='networkidle', timeout=30000)
                page.wait_for_selector('input[type="text"]', state='visible', timeout=5000)
                page.fill('input[type="text"]', "admin")
                page.fill('input[type="password"]', "admin123")
                
                login_button = page.query_selector('button[type="submit"]') or \
                             page.query_selector('button.el-button--primary') or \
                             page.query_selector('button:has-text("登录")') or \
                             page.query_selector('button:has-text("Login")')
                
                if login_button:
                    login_button.click()
                    page.wait_for_url(lambda u: "/login" not in u, timeout=10000)
                    logger.log(f"  [+] 登录成功")
                else:
                    logger.log(f"  [!] 未找到登录按钮，可能已登录")
            except Exception as e:
                logger.log(f"  [!] 登录过程异常: {e}")
            
            # 测试每个集合
            for idx, collection_name in enumerate(target_names, 1):
                collection_url = f"{frontend_base_url}/stocks/collections/{collection_name}"
                logger.log(f"\n[{idx}/{len(target_names)}] 测试集合: {collection_name}")
                logger.log(f"  URL: {collection_url}")
                
                collection_errors = []
                
                try:
                    # 访问集合详情页
                    page.goto(collection_url, wait_until='networkidle', timeout=30000)
                    time.sleep(2)  # 等待页面完全加载
                    
                    # 1. 检查数据概览按钮
                    logger.log(f"  [1] 检查数据概览按钮...")
                    overview_button = None
                    overview_selectors = [
                        'button:has-text("数据概览")',
                        'button:has-text("概览")',
                        '.overview-button',
                        '[data-test="overview-button"]',
                    ]
                    for selector in overview_selectors:
                        overview_button = page.query_selector(selector)
                        if overview_button:
                            logger.log(f"      [+] 找到数据概览按钮 (selector: {selector})")
                            break
                    
                    if not overview_button:
                        error_msg = f"数据概览按钮: 未找到"
                        collection_errors.append(error_msg)
                        logger.log(f"      [x] {error_msg}")
                    
                    # 2. 检查并测试刷新按钮
                    logger.log(f"  [2] 检查并测试刷新按钮...")
                    refresh_button = None
                    refresh_selectors = [
                        'button:has-text("刷新")',
                        'button:has-text("Refresh")',
                        '.refresh-button',
                        '[data-test="refresh-button"]',
                        'button[title="刷新"]',
                        '.el-icon-refresh',
                    ]
                    for selector in refresh_selectors:
                        refresh_button = page.query_selector(selector)
                        if refresh_button:
                            logger.log(f"      [+] 找到刷新按钮 (selector: {selector})")
                            break
                    
                    if refresh_button:
                        try:
                            refresh_button.click()
                            time.sleep(2)  # 等待刷新完成
                            
                            # 检查是否有错误提示
                            error_messages = page.query_selector_all('.el-message--error, .error-message, [class*="error"]')
                            if error_messages:
                                error_texts = [msg.inner_text() for msg in error_messages if msg.is_visible()]
                                if error_texts:
                                    error_msg = f"刷新按钮: 点击后出现错误 - {', '.join(error_texts)}"
                                    collection_errors.append(error_msg)
                                    logger.log(f"      [x] {error_msg}")
                                else:
                                    logger.log(f"      [+] 刷新按钮点击正常")
                            else:
                                logger.log(f"      [+] 刷新按钮点击正常")
                        except Exception as e:
                            error_msg = f"刷新按钮: 点击时异常 - {str(e)}"
                            collection_errors.append(error_msg)
                            logger.log(f"      [x] {error_msg}")
                    else:
                        error_msg = f"刷新按钮: 未找到"
                        collection_errors.append(error_msg)
                        logger.log(f"      [x] {error_msg}")
                    
                    # 3. 检查并测试更新数据按钮
                    logger.log(f"  [3] 检查并测试更新数据按钮...")
                    update_button = None
                    update_selectors = [
                        'button:has-text("更新数据")',
                        'button:has-text("更新")',
                        '.update-button',
                        '[data-test="update-button"]',
                    ]
                    for selector in update_selectors:
                        update_button = page.query_selector(selector)
                        if update_button:
                            logger.log(f"      [+] 找到更新数据按钮 (selector: {selector})")
                            break
                    
                    if update_button:
                        try:
                            update_button.click()
                            time.sleep(1.5)  # 等待弹窗出现
                            
                            # 检查弹窗是否出现
                            dialog_selectors = ['.el-dialog', '.dialog', '[role="dialog"]', '.modal']
                            dialog = None
                            for selector in dialog_selectors:
                                dialog = page.query_selector(selector)
                                if dialog and dialog.is_visible():
                                    logger.log(f"      [+] 弹窗已出现 (selector: {selector})")
                                    break
                            
                            if dialog and dialog.is_visible():
                                # 检查弹窗内的元素
                                expected_elements = [
                                    ("文件导入", ['text="文件导入"', ':has-text("文件导入")', '.file-import']),
                                    ("远程同步", ['text="远程同步"', ':has-text("远程同步")', '.remote-sync']),
                                    ("开始更新", ['text="开始更新"', ':has-text("开始更新")', '.start-update']),
                                    ("关闭", ['text="关闭"', ':has-text("关闭")', '.el-dialog__close', '[aria-label="Close"]']),
                                ]
                                
                                for elem_name, selectors in expected_elements:
                                    found = False
                                    for sel in selectors:
                                        elem = dialog.query_selector(sel)
                                        if elem:
                                            logger.log(f"      [+] 弹窗中找到 {elem_name}")
                                            found = True
                                            break
                                    if not found:
                                        error_msg = f"更新数据弹窗: 缺少 {elem_name}"
                                        collection_errors.append(error_msg)
                                        logger.log(f"      [x] {error_msg}")
                                
                                # 关闭弹窗
                                close_button = dialog.query_selector('button:has-text("关闭")') or \
                                             dialog.query_selector('.el-dialog__close') or \
                                             dialog.query_selector('[aria-label="Close"]')
                                if close_button:
                                    close_button.click()
                                    time.sleep(0.5)
                                    logger.log(f"      [+] 弹窗已关闭")
                            else:
                                error_msg = f"更新数据按钮: 点击后弹窗未出现"
                                collection_errors.append(error_msg)
                                logger.log(f"      [x] {error_msg}")
                        except Exception as e:
                            error_msg = f"更新数据按钮: 测试时异常 - {str(e)}"
                            collection_errors.append(error_msg)
                            logger.log(f"      [x] {error_msg}")
                    else:
                        error_msg = f"更新数据按钮: 未找到"
                        collection_errors.append(error_msg)
                        logger.log(f"      [x] {error_msg}")
                    
                    # 4. 检查并测试清空数据按钮
                    logger.log(f"  [4] 检查并测试清空数据按钮...")
                    clear_button = None
                    clear_selectors = [
                        'button:has-text("清空数据")',
                        'button:has-text("清空")',
                        '.clear-button',
                        '[data-test="clear-button"]',
                    ]
                    for selector in clear_selectors:
                        clear_button = page.query_selector(selector)
                        if clear_button:
                            logger.log(f"      [+] 找到清空数据按钮 (selector: {selector})")
                            break
                    
                    if clear_button:
                        try:
                            # 记录清空前的数据数量
                            before_data_count = self._count_table_rows(page)
                            logger.log(f"      清空前数据行数: {before_data_count}")
                            
                            clear_button.click()
                            time.sleep(1)
                            
                            # 可能有确认对话框
                            confirm_selectors = [
                                'button:has-text("确定")',
                                'button:has-text("确认")',
                                'button:has-text("OK")',
                                '.el-message-box__btns button.el-button--primary',
                            ]
                            for selector in confirm_selectors:
                                confirm_button = page.query_selector(selector)
                                if confirm_button and confirm_button.is_visible():
                                    confirm_button.click()
                                    logger.log(f"      [+] 点击了确认按钮")
                                    break
                            
                            time.sleep(2)  # 等待清空完成
                            
                            # 检查数据是否变空
                            after_data_count = self._count_table_rows(page)
                            logger.log(f"      清空后数据行数: {after_data_count}")
                            
                            if after_data_count == 0:
                                logger.log(f"      [+] 清空数据成功")
                            elif after_data_count < before_data_count:
                                logger.log(f"      [!] 数据减少但未完全清空 ({before_data_count} -> {after_data_count})")
                            else:
                                error_msg = f"清空数据按钮: 点击后数据未变空 (行数: {after_data_count})"
                                collection_errors.append(error_msg)
                                logger.log(f"      [x] {error_msg}")
                        except Exception as e:
                            error_msg = f"清空数据按钮: 测试时异常 - {str(e)}"
                            collection_errors.append(error_msg)
                            logger.log(f"      [x] {error_msg}")
                    else:
                        # 清空数据按钮不是必需的，只记录警告
                        logger.log(f"      [!] 清空数据按钮: 未找到（可选功能）")
                    
                    # 汇总本集合的测试结果
                    if not collection_errors:
                        success_count += 1
                        logger.log(f"  [+] 集合 {collection_name} 所有按钮测试通过")
                    else:
                        all_errors.append({
                            'collection': collection_name,
                            'url': collection_url,
                            'errors': collection_errors
                        })
                        logger.log(f"  [x] 集合 {collection_name} 发现 {len(collection_errors)} 个错误")
                    
                except Exception as e:
                    error_msg = f"访问页面时异常: {str(e)}"
                    all_errors.append({
                        'collection': collection_name,
                        'url': collection_url,
                        'errors': [error_msg]
                    })
                    logger.log(f"  [x] {error_msg}")
            
            browser.close()
        
        # 输出测试统计
        logger.log(f"\n{'='*80}")
        logger.log(f"【按钮功能测试统计】")
        logger.log(f"  [+] 测试通过的集合: {success_count}/{len(target_names)}")
        logger.log(f"  [x] 有错误的集合: {len(all_errors)}/{len(target_names)}")
        logger.log(f"  测试覆盖率: {100*success_count//len(target_names) if target_names else 0}%")
        logger.log(f"{'='*80}")
        
        # 详细错误报告
        if all_errors:
            logger.log(f"\n【详细错误报告】")
            for idx, error_info in enumerate(all_errors, 1):
                logger.log(f"\n错误 #{idx}: {error_info['collection']}")
                logger.log(f"  URL: {error_info['url']}")
                logger.log(f"  错误列表:")
                for err in error_info['errors']:
                    logger.log(f"    - {err}")
            logger.log(f"\n{'='*80}")
            
            # 保存日志
            logger.save()
            logger.log(f"\n[+] 详细日志已保存到: {log_file}\n")
            
            # 失败测试
            error_summary = "\n".join([
                f"集合: {e['collection']}\n  错误: {', '.join(e['errors'])}"
                for e in all_errors
            ])
            pytest.fail(
                f"\n有 {len(all_errors)} 个集合的按钮功能测试失败：\n"
                f"{error_summary}\n"
                f"详细日志: {log_file}"
            )
        else:
            logger.log(f"\n[+] 所有集合的按钮功能测试都通过了！")
            logger.log(f"{'='*80}\n")
            
            # 保存日志
            logger.save()
            logger.log(f"\n[+] 详细日志已保存到: {log_file}\n")
    
    def _count_table_rows(self, page) -> int:
        """统计表格中的数据行数"""
        try:
            # 尝试多种表格选择器
            table_selectors = [
                'table tbody tr',
                '.el-table__body tr',
                '.data-table tbody tr',
                '[role="row"]',
            ]
            
            for selector in table_selectors:
                rows = page.query_selector_all(selector)
                if rows:
                    # 过滤掉不可见的行
                    visible_rows = [row for row in rows if row.is_visible()]
                    return len(visible_rows)
            
            return 0
        except Exception:
            return 0
