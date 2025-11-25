"""
为缺失的集合生成 Provider 和 Service 文件
"""
import sys
import os
import re

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def snake_to_pascal(name):
    """将下划线命名转换为帕斯卡命名"""
    return ''.join(word.capitalize() for word in name.split('_'))

def get_router_collections():
    """从 routers/stocks.py 中提取集合名称"""
    router_file = 'F:/source_code/TradingAgents-CN/app/routers/stocks.py'
    with open(router_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    collections = re.findall(r'"name":\s*"([^"]+)"', content)
    stock_collections = [c for c in collections if c.startswith('stock_') or c.startswith('news_')]
    return list(set(stock_collections))

def get_service_collections():
    """获取已实现的服务集合"""
    from app.services.data_sources.stocks.service_factory import get_supported_stock_collections
    return get_supported_stock_collections()

PROVIDER_TEMPLATE = '''"""
{display_name}数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class {class_name}Provider:
    """{display_name}数据提供者"""
    
    def __init__(self):
        self.collection_name = "{collection_name}"
        self.display_name = "{display_name}"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取{display_name}数据
        
        Returns:
            DataFrame: {display_name}数据
        """
        try:
            logger.info(f"Fetching {{self.collection_name}} data")
            df = ak.{akshare_func}(**kwargs)
            
            if df is None or df.empty:
                logger.warning(f"No data returned")
                return pd.DataFrame()
            
            # 添加元数据
            df['scraped_at'] = datetime.now()
            
            logger.info(f"Successfully fetched {{len(df)}} records")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching {{self.collection_name}} data: {{e}}")
            raise
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        """获取字段信息"""
        return [
            {{"name": "scraped_at", "type": "datetime", "description": "抓取时间"}},
        ]
'''

SERVICE_TEMPLATE = '''"""
{display_name}服务
"""
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import UpdateOne

from ..providers.{collection_name}_provider import {class_name}Provider

logger = logging.getLogger(__name__)


class {class_name}Service:
    """{display_name}服务"""
    
    def __init__(self, db: AsyncIOMotorClient):
        self.db = db
        self.collection = db.stocks.{collection_name}
        self.provider = {class_name}Provider()
        
    async def get_overview(self) -> Dict[str, Any]:
        """获取数据概览"""
        total_count = await self.collection.count_documents({{}})
        
        latest = await self.collection.find_one(sort=[("scraped_at", -1)])
        oldest = await self.collection.find_one(sort=[("scraped_at", 1)])
        
        return {{
            "total_count": total_count,
            "last_updated": latest.get("scraped_at") if latest else None,
            "oldest_date": oldest.get("scraped_at") if oldest else None,
        }}
    
    async def get_data(
        self,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """获取数据列表"""
        query = filters or {{}}
        
        cursor = self.collection.find(query).skip(skip).limit(limit).sort("scraped_at", -1)
        data = await cursor.to_list(length=limit)
        
        total = await self.collection.count_documents(query)
        
        # 转换 ObjectId 为字符串
        for item in data:
            item["_id"] = str(item["_id"])
            if "scraped_at" in item and isinstance(item["scraped_at"], datetime):
                item["scraped_at"] = item["scraped_at"].isoformat()
        
        return {{
            "data": data,
            "total": total,
            "skip": skip,
            "limit": limit,
        }}
    
    async def refresh_data(self, **kwargs) -> Dict[str, Any]:
        """刷新数据"""
        try:
            df = self.provider.fetch_data(**kwargs)
            
            if df.empty:
                return {{
                    "success": True,
                    "message": "No data available",
                    "inserted": 0,
                }}
            
            records = df.to_dict('records')
            
            # 批量插入
            if records:
                result = await self.collection.insert_many(records)
                return {{
                    "success": True,
                    "message": "Data refreshed successfully",
                    "inserted": len(result.inserted_ids),
                }}
            
            return {{
                "success": True,
                "message": "No operations performed",
                "inserted": 0,
            }}
            
        except Exception as e:
            logger.error(f"Error refreshing data: {{e}}")
            return {{
                "success": False,
                "message": str(e),
                "inserted": 0,
            }}
    
    async def clear_data(self) -> Dict[str, Any]:
        """清空数据"""
        result = await self.collection.delete_many({{}})
        return {{
            "success": True,
            "message": f"Deleted {{result.deleted_count}} records",
            "deleted": result.deleted_count,
        }}
'''

def generate_files(collection_name):
    """为集合生成 Provider 和 Service 文件"""
    class_name = snake_to_pascal(collection_name)
    display_name = collection_name.replace('_', ' ').title()
    akshare_func = collection_name
    
    providers_dir = 'F:/source_code/TradingAgents-CN/app/services/data_sources/stocks/providers'
    services_dir = 'F:/source_code/TradingAgents-CN/app/services/data_sources/stocks/services'
    
    # 生成 Provider
    provider_file = os.path.join(providers_dir, f'{collection_name}_provider.py')
    if not os.path.exists(provider_file):
        provider_content = PROVIDER_TEMPLATE.format(
            display_name=display_name,
            class_name=class_name,
            collection_name=collection_name,
            akshare_func=akshare_func
        )
        with open(provider_file, 'w', encoding='utf-8') as f:
            f.write(provider_content)
        print(f"  Created: {collection_name}_provider.py")
    
    # 生成 Service
    service_file = os.path.join(services_dir, f'{collection_name}_service.py')
    if not os.path.exists(service_file):
        service_content = SERVICE_TEMPLATE.format(
            display_name=display_name,
            class_name=class_name,
            collection_name=collection_name
        )
        with open(service_file, 'w', encoding='utf-8') as f:
            f.write(service_content)
        print(f"  Created: {collection_name}_service.py")

def main():
    router_collections = set(get_router_collections())
    service_collections = set(get_service_collections())
    missing_services = router_collections - service_collections
    
    print(f"需要生成 {len(missing_services)} 个服务")
    print("=" * 60)
    
    for collection in sorted(missing_services):
        print(f"\n处理: {collection}")
        generate_files(collection)
    
    print("\n" + "=" * 60)
    print(f"完成！共生成 {len(missing_services)} 个 Provider 和 Service")

if __name__ == "__main__":
    main()
