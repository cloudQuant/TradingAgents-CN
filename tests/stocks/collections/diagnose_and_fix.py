"""
诊断和修复数据集合 API 更新问题

功能：
1. 检查每个数据集合的 API 状态
2. 测试更新功能是否正常
3. 记录错误信息
4. 生成修复建议
"""
import os
import sys
import httpx
import json
from datetime import datetime

# API 配置
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
AUTH_TOKEN = os.getenv("API_AUTH_TOKEN", "")

# 接口参数配置
INTERFACE_PARAMS = {
    # 无参数接口
    "stock_sse_summary": {},
    "stock_szse_summary": {},
    "stock_szse_area_summary": {},
    "stock_szse_sector_summary": {},
    "stock_sse_deal_daily": {},
    "stock_zh_a_spot_em": {},
    "stock_sh_a_spot_em": {},
    "stock_sz_a_spot_em": {},
    "stock_bj_a_spot_em": {},
    "stock_new_a_spot_em": {},
    "stock_cy_a_spot_em": {},
    "stock_kc_a_spot_em": {},
    "stock_zh_b_spot_em": {},
    "stock_us_spot_em": {},
    "stock_hk_spot_em": {},
    "stock_hot_rank_em": {},
    "stock_hot_up_em": {},
    "stock_hk_hot_rank_em": {},
    "stock_board_change_em": {},
    "stock_market_activity_legu": {},
    "stock_hot_follow_xq": {},
    "stock_hot_tweet_xq": {},
    "stock_hot_deal_xq": {},
    "stock_rank_cxfl_ths": {},
    "stock_rank_cxsl_ths": {},
    "stock_rank_ljqs_ths": {},
    "stock_rank_ljqd_ths": {},
    "stock_rank_xzjp_ths": {},
    "stock_esg_rate_sina": {},
    "stock_esg_msci_sina": {},
    "stock_esg_rft_sina": {},
    "stock_esg_zd_sina": {},
    "stock_esg_hz_sina": {},
    
    # 需要股票代码的接口
    "stock_individual_info_em": {"symbol": "000001"},
    "stock_individual_basic_info_xq": {"symbol": "SZ000001"},
    "stock_bid_ask_em": {"symbol": "000001"},
    "stock_inner_trade_xq": {"symbol": "SZ000001"},
    "stock_hot_rank_detail_em": {"symbol": "000001"},
    "stock_hot_rank_detail_realtime_em": {"symbol": "000001"},
    "stock_hot_rank_latest_em": {"symbol": "000001"},
    "stock_hot_rank_relate_em": {"symbol": "000001"},
    "stock_changes_em": {"symbol": "000001"},
    "stock_irm_cninfo": {"symbol": "000001"},
    "stock_irm_ans_cninfo": {"symbol": "000001"},
    "stock_sns_sseinfo": {"symbol": "600000"},
    "stock_hot_keyword_em": {"symbol": "000001"},
    
    # 港股代码接口
    "stock_hk_hot_rank_detail_em": {"symbol": "00700"},
    "stock_hk_hot_rank_detail_realtime_em": {"symbol": "00700"},
    "stock_hk_hot_rank_latest_em": {"symbol": "00700"},
    
    # 板块接口
    "stock_board_industry_cons_em": {"board": "小金属"},
    "stock_board_industry_hist_em": {"board": "小金属"},
    "stock_board_industry_hist_min_em": {"board": "小金属"},
    
    # 日期接口
    "stock_zt_pool_em": {"date": "20231215"},
    "stock_zt_pool_previous_em": {"date": "20231215"},
    "stock_zt_pool_strong_em": {"date": "20231215"},
    "stock_zt_pool_sub_new_em": {"date": "20231215"},
    "stock_zt_pool_zbgc_em": {"date": "20231215"},
    "stock_zt_pool_dtgc_em": {"date": "20231215"},
    "stock_hot_search_baidu": {"date": "20231215"},
    
    # 排名接口（需要天数参数）
    "stock_rank_xstp_ths": {"days": 5},
    "stock_rank_xxtp_ths": {"days": 5},
}


def get_headers():
    """获取请求头"""
    headers = {"Content-Type": "application/json"}
    if AUTH_TOKEN:
        headers["Authorization"] = f"Bearer {AUTH_TOKEN}"
    return headers


def check_collection_exists(collection_name: str) -> dict:
    """检查集合是否存在"""
    url = f"{API_BASE_URL}/api/stocks/collections/{collection_name}"
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(url, headers=get_headers())
            return {
                "exists": response.status_code == 200,
                "status_code": response.status_code,
                "error": None if response.status_code == 200 else response.text[:200]
            }
    except Exception as e:
        return {"exists": False, "status_code": 0, "error": str(e)}


def check_collection_data(collection_name: str) -> dict:
    """检查集合数据"""
    url = f"{API_BASE_URL}/api/stocks/collections/{collection_name}/data"
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(url, headers=get_headers(), params={"page": 1, "page_size": 10})
            if response.status_code == 200:
                data = response.json()
                total = data.get("data", {}).get("total", 0)
                return {
                    "has_data": total > 0,
                    "total": total,
                    "status_code": response.status_code,
                    "error": None
                }
            return {
                "has_data": False,
                "total": 0,
                "status_code": response.status_code,
                "error": response.text[:200]
            }
    except Exception as e:
        return {"has_data": False, "total": 0, "status_code": 0, "error": str(e)}


def test_refresh(collection_name: str) -> dict:
    """测试刷新功能"""
    url = f"{API_BASE_URL}/api/stocks/collections/{collection_name}/refresh"
    params = INTERFACE_PARAMS.get(collection_name, {})
    
    try:
        with httpx.Client(timeout=60.0) as client:
            response = client.post(url, headers=get_headers(), json=params)
            if response.status_code in [200, 202]:
                return {
                    "success": True,
                    "status_code": response.status_code,
                    "error": None,
                    "response": response.text[:500]
                }
            return {
                "success": False,
                "status_code": response.status_code,
                "error": response.text[:500],
                "response": None
            }
    except Exception as e:
        return {"success": False, "status_code": 0, "error": str(e), "response": None}


def diagnose_collection(collection_name: str) -> dict:
    """诊断单个集合"""
    result = {
        "name": collection_name,
        "params": INTERFACE_PARAMS.get(collection_name, {}),
    }
    
    # 1. 检查集合是否存在
    exists_result = check_collection_exists(collection_name)
    result["exists"] = exists_result
    
    if not exists_result["exists"]:
        result["status"] = "NOT_FOUND"
        return result
    
    # 2. 检查是否有数据
    data_result = check_collection_data(collection_name)
    result["data"] = data_result
    
    # 3. 测试刷新功能
    refresh_result = test_refresh(collection_name)
    result["refresh"] = refresh_result
    
    # 确定状态
    if refresh_result["success"] and data_result["has_data"]:
        result["status"] = "OK"
    elif refresh_result["success"] and not data_result["has_data"]:
        result["status"] = "NO_DATA"
    elif not refresh_result["success"]:
        result["status"] = "REFRESH_ERROR"
    else:
        result["status"] = "UNKNOWN"
    
    return result


def main():
    print("=" * 70)
    print("数据集合 API 诊断工具")
    print("=" * 70)
    print(f"API 地址: {API_BASE_URL}")
    print(f"认证: {'已配置' if AUTH_TOKEN else '未配置'}")
    print()
    
    # 获取所有集合名称
    script_dir = os.path.dirname(os.path.abspath(__file__))
    test_files = [f for f in os.listdir(script_dir) 
                  if f.endswith('_collection.py') and f[0].isdigit()]
    
    collections = []
    for fn in test_files:
        # 007_stock_sse_summary_collection.py -> stock_sse_summary
        import re
        match = re.match(r'\d+_(.+)_collection\.py', fn)
        if match:
            collections.append(match.group(1))
    
    print(f"发现 {len(collections)} 个数据集合")
    print()
    
    # 诊断结果
    results = {
        "OK": [],
        "NO_DATA": [],
        "REFRESH_ERROR": [],
        "NOT_FOUND": [],
        "UNKNOWN": []
    }
    
    # 逐个诊断
    for i, name in enumerate(sorted(collections)[:20], 1):  # 先测试前20个
        print(f"[{i}/{min(20, len(collections))}] 诊断 {name}...", end=" ")
        result = diagnose_collection(name)
        status = result["status"]
        results[status].append(result)
        
        if status == "OK":
            print(f"✓ 正常 (数据: {result['data']['total']}条)")
        elif status == "NO_DATA":
            print(f"⚠ 无数据")
        elif status == "REFRESH_ERROR":
            print(f"✗ 刷新失败: {result['refresh']['error'][:50]}...")
        elif status == "NOT_FOUND":
            print(f"✗ 接口不存在")
        else:
            print(f"? 未知状态")
    
    # 输出统计
    print()
    print("=" * 70)
    print("诊断结果统计")
    print("=" * 70)
    print(f"  正常: {len(results['OK'])}")
    print(f"  无数据: {len(results['NO_DATA'])}")
    print(f"  刷新失败: {len(results['REFRESH_ERROR'])}")
    print(f"  接口不存在: {len(results['NOT_FOUND'])}")
    
    # 保存详细报告
    report_file = os.path.join(script_dir, f"diagnose_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n详细报告已保存到: {report_file}")
    
    # 输出需要修复的接口
    if results['REFRESH_ERROR']:
        print()
        print("=" * 70)
        print("需要修复的接口")
        print("=" * 70)
        for r in results['REFRESH_ERROR']:
            print(f"\n{r['name']}:")
            print(f"  参数: {r['params']}")
            print(f"  错误: {r['refresh']['error'][:100]}")


if __name__ == "__main__":
    main()
