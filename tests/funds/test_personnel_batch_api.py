"""测试基金公告人事调整批量更新API"""
import requests

BASE_URL = "http://localhost:8000"

def test_apis():
    # 需要先登录获取token
    print("测试API端点:")
    print("1. POST /api/funds/collections/fund_announcement_personnel_em/update/single")
    print("   Body: {fund_code: '000001'}")
    print("\n2. POST /api/funds/collections/fund_announcement_personnel_em/update/batch")
    print("   Body: {fund_codes: ['000001', '000002']}")
    print("\n3. POST /api/funds/collections/fund_announcement_personnel_em/update/incremental")
    print("   Body: {limit: 10}")

if __name__ == "__main__":
    test_apis()
