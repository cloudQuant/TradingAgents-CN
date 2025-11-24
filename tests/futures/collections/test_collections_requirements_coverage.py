"""
验证 futures/collections 页面与需求文档 requirements 的一致性：
- 从 tests/futures/requirements/*.md 中解析出声明的集合路由，提取集合名
- 校验 /api/futures/collections 返回的数据集合包含这些集合名
- 访问前端页面 /futures/collections/{name}，确认能正常打开（返回 HTTP 200）
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
    # 本测试文件位于 tests/futures/collections/
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
        self.lines: List[str] = []
    
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
      http://localhost:3000/futures/collections/<collectionName>
    的集合路由，返回 {collectionName: 文档路径}
    """
    pattern = re.compile(r"http://localhost:3000/futures/collections/([a-zA-Z0-9_\-]+)")
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


class TestFuturesCollectionsRequirementsCoverage:
    
    def _extract_from_frontend_page(self, frontend_base_url: str, logger) -> Optional[list]:
        """使用Playwright从前端页面DOM提取集合数据"""
        try:
            from playwright.sync_api import sync_playwright
            
            logger.log(f"    启动浏览器...")
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                url = f"{frontend_base_url}/futures/collections"
                logger.log(f"    访问页面: {url}")
                page.goto(url, wait_until='networkidle', timeout=60000)
                
                # 等待集合列表加载
                logger.log(f"    等待数据加载...")
                time.sleep(3)
                
                # 检查是否重定向到登录页
                if "/login" in page.url or "登录" in page.title():
                    logger.log(f"    [!] 检测到登录页面，尝试自动登录...")
                    try:
                        page.wait_for_selector('input[type="text"]', state='visible', timeout=5000)
                        logger.log(f"    ...输入用户名")
                        page.fill('input[type="text"]', "admin")
                        logger.log(f"    ...输入密码")
                        page.fill('input[type="password"]', "admin123")
                        logger.log(f"    ...点击登录")
                        login_button = page.query_selector('button[type="submit"]') or \
                                     page.query_selector('button.el-button--primary') or \
                                     page.query_selector('button:has-text("登录")') or \
                                     page.query_selector('button:has-text("Login")')
                        if login_button:
                            login_button.click()
                            logger.log(f"    ...等待跳转")
                            page.wait_for_url(lambda u: "/login" not in u, timeout=10000)
                            if "/futures/collections" not in page.url:
                                logger.log(f"    ...重新访问集合页面")
                                page.goto(url, wait_until='networkidle', timeout=10000)
                            logger.log(f"    ...登录成功，等待数据加载")
                            time.sleep(5)
                        else:
                            logger.log(f"    [x] 未找到登录按钮")
                            return "AUTH_FAILED"
                    except Exception as e:
                        logger.log(f"    [x] 自动登录失败: {e}")
                        browser.close()
                        return "AUTH_FAILED"

                collections = []
                
                # 尝试1: 查找包含 /futures/collections/ 的链接
                links = page.query_selector_all('a[href*="/futures/collections/"]')
                if not links:
                    links = page.query_selector_all('tr td a')
                for link in links:
                    href = link.get_attribute('href')
                    if href and '/futures/collections/' in href:
                        name = href.split('/futures/collections/')[-1].split('?')[0].split('#')[0]
                        if name and name not in collections:
                            collections.append(name)

                # 尝试2: data 属性
                if not collections:
                    elements = page.query_selector_all('[data-collection-name]')
                    for elem in elements:
                        name = elem.get_attribute('data-collection-name')
                        if name and name not in collections:
                            collections.append(name)

                # 尝试3: 在浏览器上下文调用前端接口 /api/futures/collections
                if not collections:
                    try:
                        logger.log(f"    ...尝试通过前端API获取集合列表")
                        result = page.evaluate(
                            """
                            async () => {
                                try {
                                    const token = localStorage.getItem('access_token') || localStorage.getItem('token') || localStorage.getItem('auth_token');
                                    const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
                                    const resp = await fetch('/api/futures/collections', { credentials: 'include', headers });
                                    const ct = resp.headers.get('content-type') || '';
                                    let payload = null;
                                    if (ct.includes('application/json')) {
                                        try { payload = await resp.json(); } catch(e) { payload = null; }
                                    }
                                    // 统一返回 data 列表
                                    let data = null;
                                    if (payload) {
                                        if (Array.isArray(payload)) {
                                            data = payload;
                                        } else if (payload && Array.isArray(payload.data)) {
                                            data = payload.data;
                                        }
                                    }
                                    return { status: resp.status, data };
                                } catch (e) {
                                    return { status: -1, error: String(e) };
                                }
                            }
                            """
                        )
                        if result and isinstance(result, dict):  # type: ignore
                            data_json = result.get('data')
                            if isinstance(data_json, list) and data_json:
                                logger.log(f"    [+] 通过前端API获取到 {len(data_json)} 个集合")
                                for item in data_json:
                                    if isinstance(item, dict):
                                        n = item.get('name')
                                        if n and n not in collections:
                                            collections.append(n)
                            else:
                                logger.log(f"    [i] 前端API返回数据类型: {type(data_json).__name__ if data_json is not None else 'None'}")
                    except Exception as e:
                        logger.log(f"    [x] 前端API获取失败: {e}")

                browser.close()

                if collections:
                    logger.log(f"    [+] 从页面DOM提取到 {len(collections)} 个集合")
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
        backend_api_url = f"http://localhost:8000/api/futures/collections"
        logger.log(f"  方式2: 尝试后端API {backend_api_url}")
        
        try:
            with httpx.Client(trust_env=False, timeout=60.0, follow_redirects=True) as client:
                resp = client.get(backend_api_url, headers=auth_headers)
                if resp.status_code == 200:
                    try:
                        payload = resp.json()
                        # 统一为列表
                        if isinstance(payload, list):
                            data = payload
                        elif isinstance(payload, dict) and isinstance(payload.get("data"), list):
                            data = payload.get("data")
                        else:
                            data = None
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
        要求：前端 API /api/futures/collections 返回需包含 requirements 文档中声明的集合名
        """
        # 创建日志记录器
        log_file = _get_log_file_path()
        logger = Logger(log_file)
        
        req_dir = _requirements_dir()
        assert os.path.isdir(req_dir), f"requirements 目录不存在: {req_dir}"

        expected_map = extract_expected_collections(req_dir)
        assert expected_map, "未在需求文档中解析到任何集合路由，请检查文档格式是否包含 /futures/collections/{name}"

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
                route = f"{frontend_base_url}/futures/collections/{name}"
                logger.log(f"  {idx:3d}. [+] {name}")
                logger.log(f"         路由: {route}")
            logger.log(f"  额外集合名单: {', '.join(sorted(extra_in_api))}")
            logger.log(f"{'='*80}\n")
        
        if missing:
            logger.log(f"\n【缺失的集合详情】({len(missing)}个)")
            for idx, name in enumerate(sorted(missing), 1):
                doc = expected_map[name]
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
        else:
            logger.log(f"\n[+] 所有需求文档中声明的集合都已在数据集合列表中返回！")
            logger.log(f"{'='*80}\n")
            logger.save()
            logger.log(f"\n[+] 详细日志已保存到: {log_file}\n")

    def test_requirements_collections_frontend_openable(
        self,
        frontend_base_url: str,
        auth_headers: Dict[str, str],
    ):
        """
        要求：需求文档中声明的集合详情页 /futures/collections/{name} 可打开（HTTP 200）。
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
            for idx, name in enumerate(sorted(extra_in_api), 1):
                logger.log(f"      - {idx:3d}. {name} -> {frontend_base_url}/futures/collections/{name}")
            logger.log(f"  额外集合名单: {', '.join(sorted(extra_in_api))}")
        logger.log(f"  前端基础URL: {frontend_base_url}")
        logger.log(f"{'='*80}")

        # 检查前端是否可访问
        base_ok = False
        main_url = f"{frontend_base_url}/futures/collections"
        with httpx.Client(trust_env=False, timeout=60.0, follow_redirects=True) as client:
            try:
                r = client.get(main_url)
                base_ok = (200 <= r.status_code < 400) and r.url.path.startswith("/futures/collections")
            except httpx.RequestError as e:
                pytest.skip(f"前端未启动或无法访问: {main_url}\n错误: {e}")

        if not base_ok:
            pytest.skip(f"前端页面不可用或被重定向（可能需要登录）: {main_url}")

        failures: List[Tuple[str, int | str]] = []
        successes: List[str] = []
        
        logger.log(f"\n开始测试各集合详情页...")
        
        with httpx.Client(trust_env=False, timeout=30.0, follow_redirects=True) as client:
            for idx, name in enumerate(target_names, 1):
                detail_url = f"{frontend_base_url}/futures/collections/{name}"
                try:
                    r = client.get(detail_url)
                    ok = (200 <= r.status_code < 400) and r.url.path.startswith(f"/futures/collections/{name}")
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
                detail_url = f"{frontend_base_url}/futures/collections/{name}"
                logger.log(f"  {idx:3d}. [x] {name}")
                logger.log(f"         URL: {detail_url}")
                logger.log(f"         状态/错误: {status}")
                logger.log(f"         需求文档: {doc_short}")
            failed_names_line = ", ".join([n for n, _ in failures])
            logger.log(f"\n失败集合名单: {failed_names_line}")
            logger.log(f"{'='*80}\n")
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
            logger.save()
            logger.log(f"\n[+] 详细日志已保存到: {log_file}\n")
