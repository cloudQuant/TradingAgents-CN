#!/usr/bin/env python
"""
直接测试Service和Provider配置是否正确
不依赖后端服务，直接调用Service
"""
import sys
import asyncio
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))


async def test_service_direct():
    """直接测试Service"""
    print("=" * 70)
    print("直接测试Service和Provider配置")
    print("=" * 70)
    
    # 连接MongoDB
    from motor.motor_asyncio import AsyncIOMotorClient
    
    # 读取配置
    try:
        from app.config.settings import settings
        mongo_uri = settings.MONGODB_URI
    except:
        mongo_uri = "mongodb://localhost:27017"
    
    client = AsyncIOMotorClient(mongo_uri)
    db = client["tradingagents"]
    
    # 测试第一个Service
    print("\n1. 测试 OptionContractInfoCtpService")
    
    try:
        from app.services.data_sources.options.services.option_contract_info_ctp_service import OptionContractInfoCtpService
        
        service = OptionContractInfoCtpService(db)
        
        # 检查provider_class
        print(f"   provider_class: {service.provider_class}")
        print(f"   provider: {service.provider}")
        
        if service.provider is None:
            print("   ✗ provider为None，配置有问题")
        else:
            print("   ✓ provider已正确初始化")
            
            # 测试获取数据
            print("\n2. 测试获取数据...")
            try:
                df = service.provider.fetch_data()
                if df is not None and not df.empty:
                    print(f"   ✓ 获取到 {len(df)} 条数据")
                else:
                    print("   ✗ 未获取到数据")
            except Exception as e:
                print(f"   ✗ 获取数据失败: {e}")
            
            # 测试批量更新
            print("\n3. 测试批量更新...")
            try:
                result = await service.update_batch_data()
                print(f"   结果: {result}")
            except Exception as e:
                print(f"   ✗ 批量更新失败: {e}")
                import traceback
                traceback.print_exc()
    
    except ImportError as e:
        print(f"   ✗ 导入失败: {e}")
    except Exception as e:
        print(f"   ✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
    
    client.close()


if __name__ == "__main__":
    asyncio.run(test_service_direct())
