"""
验证清空集合功能
这个脚本用于手动验证清空功能是否正常工作
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

async def verify_clear_function():
    """验证清空功能"""
    
    # 连接MongoDB
    mongo_uri = os.getenv('MONGODB_CONNECTION_STRING', 'mongodb://localhost:27017')
    client = AsyncIOMotorClient(mongo_uri)
    db = client['tradingagents']
    
    # 选择一个测试集合
    test_collection_name = 'bond_cb_list'
    collection = db[test_collection_name]
    
    print(f"\n{'='*60}")
    print(f"验证清空功能 - 集合: {test_collection_name}")
    print(f"{'='*60}\n")
    
    # 1. 检查初始数据
    initial_count = await collection.count_documents({})
    print(f"[步骤1] 初始数据统计")
    print(f"   当前集合中有 {initial_count} 条记录")
    
    if initial_count == 0:
        print(f"\n[警告] 集合为空，插入测试数据...")
        # 插入测试数据
        test_data = [
            {'code': f'TEST{i:03d}', 'name': f'测试数据{i}', 'test': True}
            for i in range(1, 6)
        ]
        result = await collection.insert_many(test_data)
        print(f"   [OK] 已插入 {len(result.inserted_ids)} 条测试数据")
        initial_count = await collection.count_documents({})
        print(f"   当前集合中有 {initial_count} 条记录")
    
    # 2. 模拟清空操作
    print(f"\n[步骤2] 执行清空操作")
    print(f"   正在删除所有数据...")
    delete_result = await collection.delete_many({})
    deleted_count = delete_result.deleted_count
    print(f"   [OK] 成功删除 {deleted_count} 条记录")
    
    # 3. 验证清空结果
    print(f"\n[步骤3] 验证清空结果")
    final_count = await collection.count_documents({})
    print(f"   清空后集合中有 {final_count} 条记录")
    
    # 4. 结果判断
    print(f"\n{'='*60}")
    if final_count == 0:
        print(f"[SUCCESS] 验证成功！清空功能正常工作")
        print(f"   - 清空前: {initial_count} 条记录")
        print(f"   - 已删除: {deleted_count} 条记录")
        print(f"   - 清空后: {final_count} 条记录")
        success = True
    else:
        print(f"[FAILED] 验证失败！集合未完全清空")
        print(f"   - 清空前: {initial_count} 条记录")
        print(f"   - 已删除: {deleted_count} 条记录")
        print(f"   - 清空后: {final_count} 条记录（应为0）")
        success = False
    print(f"{'='*60}\n")
    
    # 关闭连接
    client.close()
    
    return success

if __name__ == '__main__':
    result = asyncio.run(verify_clear_function())
    exit(0 if result else 1)
