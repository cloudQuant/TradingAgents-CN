"""
API访问诊断工具

快速检查哪种方式可以成功获取集合列表数据
"""
import sys
import os

# 添加项目路径
here = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(here, '..', '..', '..')))

import httpx
import time

def check_backend_api():
    """检查后端API直连"""
    url = "http://localhost:8000/api/stocks/collections"
    print(f"\n{'='*80}")
    print(f"方式1: 后端API直连")
    print(f"URL: {url}")
    print(f"{'='*80}")
    
    try:
        with httpx.Client(trust_env=False, timeout=10.0) as client:
            resp = client.get(url)
            print(f"✓ HTTP状态: {resp.status_code}")
            print(f"✓ Content-Type: {resp.headers.get('content-type', 'unknown')}")
            
            if resp.status_code == 200:
                try:
                    data = resp.json()
                    if isinstance(data, list):
                        print(f"✓ ✅ 成功！返回 {len(data)} 个集合")
                        print(f"✓ 示例集合: {[item.get('name') for item in data[:3]]}")
                        return True, len(data)
                    else:
                        print(f"✗ 返回了JSON但不是列表格式")
                        return False, 0
                except Exception as e:
                    print(f"✗ 返回内容无法解析为JSON: {e}")
                    return False, 0
            elif resp.status_code == 401:
                print(f"✗ 需要认证（401 Unauthorized）")
                print(f"  提示: 设置环境变量 TEST_AUTH_TOKEN")
                return False, 0
            else:
                print(f"✗ HTTP状态码不是200")
                return False, 0
                
    except httpx.ConnectError as e:
        print(f"✗ 连接失败: {e}")
        print(f"  提示: 后端服务可能未启动")
        return False, 0
    except httpx.TimeoutException:
        print(f"✗ 请求超时（10秒）")
        return False, 0
    except Exception as e:
        print(f"✗ 其他错误: {e}")
        return False, 0

def check_playwright_dom():
    """检查Playwright页面DOM提取"""
    url = "http://localhost:3000/stocks/collections"
    print(f"\n{'='*80}")
    print(f"方式2: Playwright页面DOM提取")
    print(f"URL: {url}")
    print(f"{'='*80}")
    
    try:
        from playwright.sync_api import sync_playwright
        print(f"✓ Playwright已安装")
        
        print(f"  启动浏览器...")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            print(f"  访问页面: {url}")
            page.goto(url, wait_until='networkidle', timeout=30000)
            
            print(f"  等待数据加载...")
            time.sleep(3)
            
            # 提取集合链接
            links = page.query_selector_all('a[href*="/stocks/collections/"]')
            collections = []
            for link in links:
                href = link.get_attribute('href')
                if href and '/stocks/collections/' in href:
                    name = href.split('/stocks/collections/')[-1].split('?')[0].split('#')[0]
                    if name and name not in collections:
                        collections.append(name)
            
            browser.close()
            
            if collections:
                print(f"✓ ✅ 成功！从页面提取到 {len(collections)} 个集合")
                print(f"✓ 示例集合: {collections[:3]}")
                return True, len(collections)
            else:
                print(f"✗ 未能从页面提取到集合链接")
                print(f"  提示: 页面结构可能与预期不同")
                return False, 0
                
    except ImportError:
        print(f"✗ Playwright未安装")
        print(f"  提示: 运行 pip install playwright && playwright install chromium")
        return False, 0
    except Exception as e:
        print(f"✗ DOM提取失败: {e}")
        return False, 0

def main():
    print(f"\n{'='*80}")
    print(f"🔍 API访问诊断工具")
    print(f"{'='*80}")
    print(f"说明: 测试会尝试2种方式获取集合列表数据")
    print(f"      只要有一种方式成功，测试就能正常运行")
    print(f"{'='*80}")
    
    results = []
    
    # 方式1: 后端API
    success1, count1 = check_backend_api()
    results.append(("后端API直连", success1, count1))
    
    # 方式2: Playwright DOM提取
    success2, count2 = check_playwright_dom()
    results.append(("Playwright DOM提取", success2, count2))
    
    # 总结
    print(f"\n{'='*80}")
    print(f"📊 诊断结果总结")
    print(f"{'='*80}")
    
    for name, success, count in results:
        status = "✅ 可用" if success else "❌ 不可用"
        info = f"（{count}个集合）" if success else ""
        print(f"{status} {name} {info}")
    
    print(f"{'='*80}")
    
    # 建议
    success_count = sum(1 for _, success, _ in results if success)
    
    if success_count == 0:
        print(f"\n⚠️  警告：所有方式都不可用！")
        print(f"\n建议：")
        print(f"  1. 确保前端服务运行在 http://localhost:3000")
        print(f"  2. 确保后端服务运行在 http://localhost:8000")
        print(f"  3. 在浏览器中访问 http://localhost:3000/stocks/collections")
        print(f"     检查页面是否能正常显示集合列表")
        print(f"  4. 如果需要认证，设置环境变量 TEST_AUTH_TOKEN")
        print(f"\n环境变量设置方法（PowerShell）：")
        print(f"  $env:TEST_AUTH_TOKEN=\"your-token-here\"")
        
    elif success_count == 1:
        working = [name for name, success, _ in results if success][0]
        print(f"\n✅ 有1种方式可用：{working}")
        print(f"\n测试可以正常运行！运行命令：")
        print(f"  cd tests/stocks")
        print(f"  pytest .\\collections\\test_collections_requirements_coverage.py -v -s")
        
    else:
        print(f"\n✅ 有{success_count}种方式可用，测试运行无障碍！")
        print(f"\n运行测试命令：")
        print(f"  cd tests/stocks")
        print(f"  pytest .\\collections\\test_collections_requirements_coverage.py -v -s")
    
    print(f"\n{'='*80}")
    
    return success_count > 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
