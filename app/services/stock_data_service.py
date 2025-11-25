"""
股票数据服务层 - 统一数据访问接口
基于现有MongoDB集合，提供标准化的数据访问服务
"""
import logging
import uuid
from datetime import datetime, date
from typing import Optional, Dict, Any, List
from motor.motor_asyncio import AsyncIOMotorDatabase
import pandas as pd
from pymongo import UpdateOne

from app.core.database import get_mongo_db
from app.models.stock_models import (
    StockBasicInfoExtended, 
    MarketQuotesExtended,
    MarketInfo,
    MarketType,
    ExchangeType,
    CurrencyType
)

logger = logging.getLogger(__name__)


class StockDataService:
    """
    股票数据服务 - 统一数据访问层
    基于现有集合扩展，保持向后兼容
    """
    
    def __init__(self):
        self.basic_info_collection = "stock_basic_info"
        self.market_quotes_collection = "market_quotes"
    
    async def get_stock_basic_info(
        self,
        symbol: str,
        source: Optional[str] = None
    ) -> Optional[StockBasicInfoExtended]:
        """
        获取股票基础信息
        Args:
            symbol: 6位股票代码
            source: 数据源 (tushare/akshare/baostock/multi_source)，默认优先级：tushare > multi_source > akshare > baostock
        Returns:
            StockBasicInfoExtended: 扩展的股票基础信息
        """
        try:
            db = get_mongo_db()
            symbol6 = str(symbol).zfill(6)

            # 🔥 构建查询条件
            query = {"$or": [{"symbol": symbol6}, {"code": symbol6}]}

            if source:
                # 指定数据源
                query["source"] = source
                doc = await db[self.basic_info_collection].find_one(query, {"_id": 0})
            else:
                # 🔥 未指定数据源，按优先级查询
                source_priority = ["tushare", "multi_source", "akshare", "baostock"]
                doc = None

                for src in source_priority:
                    query_with_source = query.copy()
                    query_with_source["source"] = src
                    doc = await db[self.basic_info_collection].find_one(query_with_source, {"_id": 0})
                    if doc:
                        logger.debug(f"✅ 使用数据源: {src}")
                        break

                # 如果所有数据源都没有，尝试不带 source 条件查询（兼容旧数据）
                if not doc:
                    doc = await db[self.basic_info_collection].find_one(
                        {"$or": [{"symbol": symbol6}, {"code": symbol6}]},
                        {"_id": 0}
                    )
                    if doc:
                        logger.warning(f"⚠️ 使用旧数据（无 source 字段）: {symbol6}")

            if not doc:
                return None

            # 数据标准化处理
            standardized_doc = self._standardize_basic_info(doc)

            return StockBasicInfoExtended(**standardized_doc)

        except Exception as e:
            logger.error(f"获取股票基础信息失败 symbol={symbol}, source={source}: {e}")
            return None
    
    async def get_market_quotes(self, symbol: str) -> Optional[MarketQuotesExtended]:
        """
        获取实时行情数据
        Args:
            symbol: 6位股票代码
        Returns:
            MarketQuotesExtended: 扩展的实时行情数据
        """
        try:
            db = get_mongo_db()
            symbol6 = str(symbol).zfill(6)

            # 从现有集合查询 (优先使用symbol字段，兼容code字段)
            doc = await db[self.market_quotes_collection].find_one(
                {"$or": [{"symbol": symbol6}, {"code": symbol6}]},
                {"_id": 0}
            )

            if not doc:
                return None

            # 数据标准化处理
            standardized_doc = self._standardize_market_quotes(doc)

            return MarketQuotesExtended(**standardized_doc)

        except Exception as e:
            logger.error(f"获取实时行情失败 symbol={symbol}: {e}")
            return None
    
    async def get_stock_list(
        self,
        market: Optional[str] = None,
        industry: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
        source: Optional[str] = None
    ) -> List[StockBasicInfoExtended]:
        """
        获取股票列表
        Args:
            market: 市场筛选
            industry: 行业筛选
            page: 页码
            page_size: 每页大小
            source: 数据源（可选），默认使用优先级最高的数据源
        Returns:
            List[StockBasicInfoExtended]: 股票列表
        """
        try:
            db = get_mongo_db()

            # 🔥 获取数据源优先级配置
            if not source:
                from app.core.unified_config import UnifiedConfigManager
                config = UnifiedConfigManager()
                data_source_configs = await config.get_data_source_configs_async()

                # 提取启用的数据源，按优先级排序
                enabled_sources = [
                    ds.type.lower() for ds in data_source_configs
                    if ds.enabled and ds.type.lower() in ['tushare', 'akshare', 'baostock']
                ]

                if not enabled_sources:
                    enabled_sources = ['tushare', 'akshare', 'baostock']

                source = enabled_sources[0] if enabled_sources else 'tushare'

            # 构建查询条件
            query = {"source": source}  # 🔥 添加数据源筛选
            if market:
                query["market"] = market
            if industry:
                query["industry"] = industry

            # 分页查询
            skip = (page - 1) * page_size
            cursor = db[self.basic_info_collection].find(
                query,
                {"_id": 0}
            ).skip(skip).limit(page_size)

            docs = await cursor.to_list(length=page_size)

            # 数据标准化处理
            result = []
            for doc in docs:
                standardized_doc = self._standardize_basic_info(doc)
                result.append(StockBasicInfoExtended(**standardized_doc))

            return result
            
        except Exception as e:
            logger.error(f"获取股票列表失败: {e}")
            return []
    
    async def update_stock_basic_info(
        self,
        symbol: str,
        update_data: Dict[str, Any],
        source: str = "tushare"
    ) -> bool:
        """
        更新股票基础信息
        Args:
            symbol: 6位股票代码
            update_data: 更新数据
            source: 数据源 (tushare/akshare/baostock)，默认 tushare
        Returns:
            bool: 更新是否成功
        """
        try:
            db = get_mongo_db()
            symbol6 = str(symbol).zfill(6)

            # 添加更新时间
            update_data["updated_at"] = datetime.utcnow()

            # 确保symbol字段存在
            if "symbol" not in update_data:
                update_data["symbol"] = symbol6

            # 🔥 确保 code 字段存在
            if "code" not in update_data:
                update_data["code"] = symbol6

            # 🔥 确保 source 字段存在
            if "source" not in update_data:
                update_data["source"] = source

            # 🔥 执行更新 (使用 code + source 联合查询)
            result = await db[self.basic_info_collection].update_one(
                {"code": symbol6, "source": source},
                {"$set": update_data},
                upsert=True
            )

            return result.modified_count > 0 or result.upserted_id is not None

        except Exception as e:
            logger.error(f"更新股票基础信息失败 symbol={symbol}, source={source}: {e}")
            return False
    
    async def update_market_quotes(
        self,
        symbol: str,
        quote_data: Dict[str, Any]
    ) -> bool:
        """
        更新实时行情数据
        Args:
            symbol: 6位股票代码
            quote_data: 行情数据
        Returns:
            bool: 更新是否成功
        """
        try:
            db = get_mongo_db()
            symbol6 = str(symbol).zfill(6)

            # 添加更新时间
            quote_data["updated_at"] = datetime.utcnow()

            # 🔥 确保 symbol 和 code 字段都存在（兼容旧索引）
            if "symbol" not in quote_data:
                quote_data["symbol"] = symbol6
            if "code" not in quote_data:
                quote_data["code"] = symbol6  # code 和 symbol 使用相同的值

            # 执行更新 (使用symbol字段作为查询条件)
            result = await db[self.market_quotes_collection].update_one(
                {"symbol": symbol6},
                {"$set": quote_data},
                upsert=True
            )

            return result.modified_count > 0 or result.upserted_id is not None

        except Exception as e:
            logger.error(f"更新实时行情失败 symbol={symbol}: {e}")
            return False
    
    def _standardize_basic_info(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        """
        标准化股票基础信息数据
        将现有字段映射到标准化字段
        """
        # 保持现有字段不变
        result = doc.copy()

        # 获取股票代码 (优先使用symbol，兼容code)
        symbol = doc.get("symbol") or doc.get("code", "")
        result["symbol"] = symbol

        # 兼容旧字段
        if "code" in doc and "symbol" not in doc:
            result["code"] = doc["code"]
        
        # 生成完整代码 (优先使用已有的full_symbol)
        if "full_symbol" not in result or not result["full_symbol"]:
            if symbol and len(symbol) == 6:
                # 根据代码判断交易所
                if symbol.startswith(('60', '68', '90')):
                    result["full_symbol"] = f"{symbol}.SS"
                    exchange = "SSE"
                    exchange_name = "上海证券交易所"
                elif symbol.startswith(('00', '30', '20')):
                    result["full_symbol"] = f"{symbol}.SZ"
                    exchange = "SZSE"
                    exchange_name = "深圳证券交易所"
                else:
                    result["full_symbol"] = f"{symbol}.SZ"  # 默认深交所
                    exchange = "SZSE"
                    exchange_name = "深圳证券交易所"
            else:
                exchange = "SZSE"
                exchange_name = "深圳证券交易所"
        else:
            # 从full_symbol解析交易所
            full_symbol = result["full_symbol"]
            if ".SS" in full_symbol or ".SH" in full_symbol:
                exchange = "SSE"
                exchange_name = "上海证券交易所"
            else:
                exchange = "SZSE"
                exchange_name = "深圳证券交易所"
            
            # 添加市场信息
            result["market_info"] = {
                "market": "CN",
                "exchange": exchange,
                "exchange_name": exchange_name,
                "currency": "CNY",
                "timezone": "Asia/Shanghai",
                "trading_hours": {
                    "open": "09:30",
                    "close": "15:00",
                    "lunch_break": ["11:30", "13:00"]
                }
            }
        
        # 字段映射和标准化
        result["board"] = doc.get("sse")  # 板块标准化
        result["sector"] = doc.get("sec")  # 所属板块标准化
        result["status"] = "L"  # 默认上市状态
        result["data_version"] = 1

        # 处理日期字段格式转换
        list_date = doc.get("list_date")
        if list_date and isinstance(list_date, int):
            # 将整数日期转换为字符串格式 (YYYYMMDD -> YYYY-MM-DD)
            date_str = str(list_date)
            if len(date_str) == 8:
                result["list_date"] = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
            else:
                result["list_date"] = str(list_date)
        elif list_date:
            result["list_date"] = str(list_date)

        return result
    
    def _standardize_market_quotes(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        """
        标准化实时行情数据
        将现有字段映射到标准化字段
        """
        # 保持现有字段不变
        result = doc.copy()
        
        # 获取股票代码 (优先使用symbol，兼容code)
        symbol = doc.get("symbol") or doc.get("code", "")
        result["symbol"] = symbol

        # 兼容旧字段
        if "code" in doc and "symbol" not in doc:
            result["code"] = doc["code"]

        # 生成完整代码和市场标识 (优先使用已有的full_symbol)
        if "full_symbol" not in result or not result["full_symbol"]:
            if symbol and len(symbol) == 6:
                if symbol.startswith(('60', '68', '90')):
                    result["full_symbol"] = f"{symbol}.SS"
                else:
                    result["full_symbol"] = f"{symbol}.SZ"

        if "market" not in result:
            result["market"] = "CN"
        
        # 字段映射
        result["current_price"] = doc.get("close")  # 当前价格
        if doc.get("close") and doc.get("pre_close"):
            try:
                result["change"] = float(doc["close"]) - float(doc["pre_close"])
            except (ValueError, TypeError):
                result["change"] = None
        
        result["data_source"] = "market_quotes"
        result["data_version"] = 1
        
        return result
    
    async def save_stock_sse_summary(self, df) -> int:
        """
        保存上海证券交易所股票数据总貌
        
        Args:
            df: 股票数据总貌DataFrame
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning("⚠️ 上海证券交易所数据总貌为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_sse_summary"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳
            now = datetime.now()
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                # 使用"项目"字段作为唯一标识
                filter_dict = {"项目": record.get("项目", "")}
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存上海证券交易所数据总貌成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存上海证券交易所数据总貌失败: {e}")
            raise
    
    async def save_stock_szse_summary(self, df, date: str) -> int:
        """
        保存深圳证券交易所证券类别统计
        
        Args:
            df: 证券类别统计DataFrame
            date: 日期
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning("⚠️ 深圳证券交易所证券类别统计为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_szse_summary"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和日期
            now = datetime.now()
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                record['date'] = date
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                # 使用"证券类别"和日期作为唯一标识
                filter_dict = {
                    "证券类别": record.get("证券类别", ""),
                    "date": date
                }
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存深圳证券交易所证券类别统计成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存深圳证券交易所证券类别统计失败: {e}")
            raise
    
    async def save_stock_szse_area_summary(self, df, date: str) -> int:
        """
        保存深圳证券交易所地区交易排序
        
        Args:
            df: 地区交易排序DataFrame
            date: 年月
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning("⚠️ 深圳证券交易所地区交易排序为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_szse_area_summary"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和日期
            now = datetime.now()
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                record['date'] = date
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                # 使用"地区"和日期作为唯一标识
                filter_dict = {
                    "地区": record.get("地区", ""),
                    "date": date
                }
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存深圳证券交易所地区交易排序成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存深圳证券交易所地区交易排序失败: {e}")
            raise
    
    async def save_stock_szse_sector_summary(self, df, symbol: str, date: str) -> int:
        """
        保存深圳证券交易所股票行业成交数据
        
        Args:
            df: 股票行业成交DataFrame
            symbol: 统计类型（"当月" 或 "当年"）
            date: 年月（如"202501"）
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning("⚠️ 深圳证券交易所股票行业成交数据为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_szse_sector_summary"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和标识
            now = datetime.now()
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                record['symbol'] = symbol
                record['date'] = date
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                # 使用行业索引（如果有）、symbol和date作为唯一标识
                industry_key = record.get("index", "") or record.get("行业", "") or str(records.index(record))
                filter_dict = {
                    "industry": industry_key,
                    "symbol": symbol,
                    "date": date
                }
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存深圳证券交易所股票行业成交数据成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存深圳证券交易所股票行业成交数据失败: {e}")
            raise
    
    async def save_stock_sse_deal_daily(self, df, date: str) -> int:
        """
        保存上海证券交易所每日股票情况
        
        Args:
            df: 每日股票情况DataFrame
            date: 日期（如"20250221"）
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning("⚠️ 上海证券交易所每日股票情况为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_sse_deal_daily"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和日期
            now = datetime.now()
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                record['date'] = date
                record['trade_date'] = date
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                # 使用日期作为唯一标识
                filter_dict = {"date": date}
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存上海证券交易所每日股票情况成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存上海证券交易所每日股票情况失败: {e}")
            raise
    
    async def save_stock_individual_info_em(self, data: Dict[str, Any], symbol: str) -> int:
        """
        保存东方财富个股信息
        
        Args:
            data: 个股信息字典
            symbol: 股票代码
            
        Returns:
            保存的记录数
        """
        try:
            if not data:
                logger.warning(f"⚠️ 股票 {symbol} 的个股信息为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_individual_info_em"]
            
            # 添加时间戳和标识
            now = datetime.now()
            record = {
                'symbol': symbol,
                'code': symbol,
                'data': data,
                'updated_at': now,
                'source': 'eastmoney'
            }
            
            # 如果data是DataFrame格式，转换为字典
            if hasattr(data, 'to_dict'):
                record['data'] = data.to_dict('records')
            
            # 插入或更新
            result = await collection.update_one(
                {"symbol": symbol},
                {"$set": record},
                upsert=True
            )
            
            saved_count = 1 if result.upserted_id or result.modified_count > 0 else 0
            logger.info(f"✅ 保存东方财富个股信息成功: {symbol}")
            return saved_count
            
        except Exception as e:
            logger.error(f"❌ 保存东方财富个股信息失败 {symbol}: {e}")
            raise
    
    async def save_stock_individual_basic_info_xq(self, data: Dict[str, Any], symbol: str) -> int:
        """
        保存雪球个股基础信息
        
        Args:
            data: 个股基础信息字典
            symbol: 股票代码（雪球格式，如"SH601127"）
            
        Returns:
            保存的记录数
        """
        try:
            if not data:
                logger.warning(f"⚠️ 股票 {symbol} 的雪球基础信息为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_individual_basic_info_xq"]
            
            # 添加时间戳和标识
            now = datetime.now()
            record = {
                'symbol': symbol,
                'code': symbol,
                'data': data,
                'updated_at': now,
                'source': 'xueqiu'
            }
            
            # 如果data是DataFrame格式，转换为字典
            if hasattr(data, 'to_dict'):
                record['data'] = data.to_dict('records')
            
            # 插入或更新
            result = await collection.update_one(
                {"symbol": symbol},
                {"$set": record},
                upsert=True
            )
            
            saved_count = 1 if result.upserted_id or result.modified_count > 0 else 0
            logger.info(f"✅ 保存雪球个股基础信息成功: {symbol}")
            return saved_count
            
        except Exception as e:
            logger.error(f"❌ 保存雪球个股基础信息失败 {symbol}: {e}")
            raise
    
    async def save_stock_bid_ask_em(self, data: Dict[str, Any], symbol: str) -> int:
        """
        保存东方财富行情报价
        
        Args:
            data: 行情报价字典
            symbol: 股票代码
            
        Returns:
            保存的记录数
        """
        try:
            if not data:
                logger.warning(f"⚠️ 股票 {symbol} 的行情报价为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_bid_ask_em"]
            
            # 添加时间戳和标识
            now = datetime.now()
            record = {
                'symbol': symbol,
                'code': symbol,
                'data': data,
                'updated_at': now,
                'source': 'eastmoney'
            }
            
            # 如果data是DataFrame格式，转换为字典
            if hasattr(data, 'to_dict'):
                record['data'] = data.to_dict('records')
            
            # 插入或更新
            result = await collection.update_one(
                {"symbol": symbol},
                {"$set": record},
                upsert=True
            )
            
            saved_count = 1 if result.upserted_id or result.modified_count > 0 else 0
            logger.info(f"✅ 保存东方财富行情报价成功: {symbol}")
            return saved_count
            
        except Exception as e:
            logger.error(f"❌ 保存东方财富行情报价失败 {symbol}: {e}")
            raise
    
    async def save_stock_zh_a_spot_em(self, df) -> int:
        """
        保存沪深京A股实时行情
        
        Args:
            df: 实时行情DataFrame
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning("⚠️ 沪深京A股实时行情为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_zh_a_spot_em"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和标识
            now = datetime.now()
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                # 如果有'代码'字段，同时复制为'code'
                if '代码' in record:
                    record['code'] = record['代码']
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                # 使用代码作为唯一标识
                code = record.get("代码") or record.get("code")
                if not code:
                    continue
                    
                filter_dict = {"code": code}
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存沪深京A股实时行情成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存沪深京A股实时行情失败: {e}")
            raise
    
    async def save_stock_sh_a_spot_em(self, df) -> int:
        """
        保存沪A股实时行情
        
        Args:
            df: 实时行情DataFrame
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning("⚠️ 沪A股实时行情为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_sh_a_spot_em"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和标识
            now = datetime.now()
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                # 如果有'代码'字段，同时复制为'code'
                if '代码' in record:
                    record['code'] = record['代码']
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                # 使用代码作为唯一标识
                code = record.get("代码") or record.get("code")
                if not code:
                    continue
                    
                filter_dict = {"code": code}
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存沪A股实时行情成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存沪A股实时行情失败: {e}")
            raise
    
    async def save_stock_sz_a_spot_em(self, df) -> int:
        """
        保存深A股实时行情
        
        Args:
            df: 实时行情DataFrame
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning("⚠️ 深A股实时行情为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_sz_a_spot_em"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和标识
            now = datetime.now()
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                # 如果有'代码'字段，同时复制为'code'
                if '代码' in record:
                    record['code'] = record['代码']
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                # 使用代码作为唯一标识
                code = record.get("代码") or record.get("code")
                if not code:
                    continue
                    
                filter_dict = {"code": code}
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存深A股实时行情成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存深A股实时行情失败: {e}")
            raise
    
    async def save_stock_esg_hz_sina(self, df) -> int:
        """
        保存华证指数ESG评级
        
        Args:
            df: ESG评级DataFrame
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning("⚠️ 华证指数ESG评级为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_esg_hz_sina"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和标识
            now = datetime.now()
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                # 如果有'股票代码'字段，复制为'code'和'symbol'
                if '股票代码' in record:
                    record['code'] = record['股票代码']
                    record['symbol'] = record['股票代码']
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                # 使用股票代码作为唯一标识
                code = record.get("股票代码") or record.get("code")
                if not code:
                    continue
                    
                filter_dict = {"code": code}
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存华证指数ESG评级成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存华证指数ESG评级失败: {e}")
            raise
    
    async def save_stock_esg_zd_sina(self, df) -> int:
        """
        保存秩鼎ESG评级
        
        Args:
            df: ESG评级DataFrame
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning("⚠️ 秩鼎ESG评级为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_esg_zd_sina"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和标识
            now = datetime.now()
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                # 如果有'股票代码'字段，复制为'code'和'symbol'
                if '股票代码' in record:
                    record['code'] = record['股票代码']
                    record['symbol'] = record['股票代码']
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                # 使用股票代码作为唯一标识
                code = record.get("股票代码") or record.get("code")
                if not code:
                    continue
                    
                filter_dict = {"code": code}
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存秩鼎ESG评级成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存秩鼎ESG评级失败: {e}")
            raise
    
    async def save_stock_esg_rft_sina(self, df) -> int:
        """
        保存路孚特ESG评级
        
        Args:
            df: ESG评级DataFrame
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning("⚠️ 路孚特ESG评级为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_esg_rft_sina"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和标识
            now = datetime.now()
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                # 如果有'股票代码'字段，复制为'code'和'symbol'
                if '股票代码' in record:
                    record['code'] = record['股票代码']
                    record['symbol'] = record['股票代码']
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                # 使用股票代码作为唯一标识
                code = record.get("股票代码") or record.get("code")
                if not code:
                    continue
                    
                filter_dict = {"code": code}
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存路孚特ESG评级成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存路孚特ESG评级失败: {e}")
            raise
    
    async def save_stock_esg_msci_sina(self, df) -> int:
        """
        保存MSCI ESG评级
        
        Args:
            df: ESG评级DataFrame
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning("⚠️ MSCI ESG评级为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_esg_msci_sina"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和标识
            now = datetime.now()
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                # 如果有'股票代码'字段，复制为'code'和'symbol'
                if '股票代码' in record:
                    record['code'] = record['股票代码']
                    record['symbol'] = record['股票代码']
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                # 使用股票代码作为唯一标识
                code = record.get("股票代码") or record.get("code")
                if not code:
                    continue
                    
                filter_dict = {"code": code}
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存MSCI ESG评级成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存MSCI ESG评级失败: {e}")
            raise
    
    async def save_stock_esg_rate_sina(self, df) -> int:
        """
        保存ESG评级数据
        
        Args:
            df: ESG评级DataFrame
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning("⚠️ ESG评级数据为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_esg_rate_sina"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和标识
            now = datetime.now()
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                # 如果有'成分股代码'字段，复制为'code'和'symbol'
                if '成分股代码' in record:
                    record['code'] = record['成分股代码']
                    record['symbol'] = record['成分股代码']
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                # 使用成分股代码作为唯一标识
                code = record.get("成分股代码") or record.get("code")
                if not code:
                    continue
                    
                filter_dict = {"code": code}
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存ESG评级数据成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存ESG评级数据失败: {e}")
            raise
    
    async def save_stock_rank_xzjp_ths(self, df) -> int:
        """
        保存险资举牌数据
        
        Args:
            df: 险资举牌DataFrame
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning("⚠️ 险资举牌数据为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_rank_xzjp_ths"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和标识
            now = datetime.now()
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                # 如果有'股票代码'字段，复制为'code'和'symbol'
                if '股票代码' in record:
                    record['code'] = record['股票代码']
                    record['symbol'] = record['股票代码']
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                # 使用 股票代码+举牌公告日+举牌方 作为唯一标识
                code = record.get("股票代码") or record.get("code")
                date = record.get("举牌公告日") or record.get("announcement_date")
                bidder = record.get("举牌方") or record.get("bidder")
                
                if not code or not date or not bidder:
                    continue
                    
                filter_dict = {
                    "code": code,
                    "举牌公告日": date,
                    "举牌方": bidder
                }
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存险资举牌数据成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存险资举牌数据失败: {e}")
            raise
    
    async def save_stock_rank_ljqd_ths(self, df) -> int:
        """
        保存量价齐跌数据
        
        Args:
            df: 量价齐跌DataFrame
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning("⚠️ 量价齐跌数据为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_rank_ljqd_ths"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和标识
            now = datetime.now()
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                # 如果有'股票代码'字段，复制为'code'和'symbol'
                if '股票代码' in record:
                    record['code'] = record['股票代码']
                    record['symbol'] = record['股票代码']
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                # 使用 股票代码 作为唯一标识
                code = record.get("股票代码") or record.get("code")
                
                if not code:
                    continue
                    
                filter_dict = {"code": code}
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存量价齐跌数据成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存量价齐跌数据失败: {e}")
            raise
    
    async def save_stock_rank_ljqs_ths(self, df) -> int:
        """
        保存量价齐升数据
        
        Args:
            df: 量价齐升DataFrame
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning("⚠️ 量价齐升数据为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_rank_ljqs_ths"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和标识
            now = datetime.now()
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                # 如果有'股票代码'字段，复制为'code'和'symbol'
                if '股票代码' in record:
                    record['code'] = record['股票代码']
                    record['symbol'] = record['股票代码']
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                # 使用 股票代码 作为唯一标识
                code = record.get("股票代码") or record.get("code")
                
                if not code:
                    continue
                    
                filter_dict = {"code": code}
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存量价齐升数据成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存量价齐升数据失败: {e}")
            raise
    
    async def save_stock_rank_xxtp_ths(self, df) -> int:
        """
        保存向下突破数据
        
        Args:
            df: 向下突破DataFrame
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning("⚠️ 向下突破数据为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_rank_xxtp_ths"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和标识
            now = datetime.now()
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                # 如果有'股票代码'字段，复制为'code'和'symbol'
                if '股票代码' in record:
                    record['code'] = record['股票代码']
                    record['symbol'] = record['股票代码']
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                # 使用 股票代码 作为唯一标识
                code = record.get("股票代码") or record.get("code")
                
                if not code:
                    continue
                    
                filter_dict = {"code": code}
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存向下突破数据成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存向下突破数据失败: {e}")
            raise
    
    async def save_stock_rank_xstp_ths(self, df) -> int:
        """
        保存向上突破数据
        
        Args:
            df: 向上突破DataFrame
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning("⚠️ 向上突破数据为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_rank_xstp_ths"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和标识
            now = datetime.now()
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                # 如果有'股票代码'字段，复制为'code'和'symbol'
                if '股票代码' in record:
                    record['code'] = record['股票代码']
                    record['symbol'] = record['股票代码']
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                # 使用 股票代码 作为唯一标识
                code = record.get("股票代码") or record.get("code")
                
                if not code:
                    continue
                    
                filter_dict = {"code": code}
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存向上突破数据成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存向上突破数据失败: {e}")
            raise
    
    async def save_stock_rank_cxsl_ths(self, df) -> int:
        """
        保存持续缩量数据
        
        Args:
            df: 持续缩量DataFrame
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning("⚠️ 持续缩量数据为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_rank_cxsl_ths"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和标识
            now = datetime.now()
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                # 如果有'股票代码'字段，复制为'code'和'symbol'
                if '股票代码' in record:
                    record['code'] = record['股票代码']
                    record['symbol'] = record['股票代码']
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                # 使用 股票代码 作为唯一标识
                code = record.get("股票代码") or record.get("code")
                
                if not code:
                    continue
                    
                filter_dict = {"code": code}
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存持续缩量数据成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存持续缩量数据失败: {e}")
            raise
    
    async def save_stock_rank_cxfl_ths(self, df) -> int:
        """
        保存持续放量数据
        
        Args:
            df: 持续放量DataFrame
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning("⚠️ 持续放量数据为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_rank_cxfl_ths"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和标识
            now = datetime.now()
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                # 如果有'股票代码'字段，复制为'code'和'symbol'
                if '股票代码' in record:
                    record['code'] = record['股票代码']
                    record['symbol'] = record['股票代码']
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                # 使用 股票代码 作为唯一标识
                code = record.get("股票代码") or record.get("code")
                
                if not code:
                    continue
                    
                filter_dict = {"code": code}
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存持续放量数据成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存持续放量数据失败: {e}")
            raise
    
    async def save_stock_market_activity_legu(self, df) -> int:
        """
        保存赚钱效应分析数据
        
        Args:
            df: 赚钱效应分析DataFrame
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning("⚠️ 赚钱效应分析数据为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_market_activity_legu"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和标识
            now = datetime.now()
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                # 使用 item 作为唯一标识，如果不存在则使用 _id (不太可能)
                # 或者如果没有唯一标识，就清空后插入？
                # 假设 item 是唯一标识
                unique_key = record.get("item")
                
                if not unique_key:
                    # 尝试使用 标题
                    unique_key = record.get("标题")
                
                if not unique_key:
                    # 如果实在没有唯一标识，生成一个hash或者直接insert
                    # 这里假设总是有 item 或 标题
                    continue
                    
                filter_dict = {"item": unique_key} if "item" in record else {"标题": unique_key}
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存赚钱效应分析数据成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存赚钱效应分析数据失败: {e}")
            raise
    
    async def save_stock_zt_pool_dtgc_em(self, df, date_str: str = None) -> int:
        """
        保存跌停股池数据
        
        Args:
            df: 跌停股池DataFrame
            date_str: 数据日期 (YYYYMMDD)
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning("⚠️ 跌停股池数据为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_zt_pool_dtgc_em"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和标识
            now = datetime.now()
            
            # 如果没有传入date_str，尝试从df中获取，或者使用当天
            if not date_str:
                 date_str = now.strftime("%Y%m%d")
            
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                record['date'] = date_str
                # 统一字段名
                if '代码' in record:
                    record['code'] = record['代码']
                    record['symbol'] = record['代码']
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                code = record.get("code")
                if not code:
                    continue
                    
                # 使用 code + date 作为唯一标识
                filter_dict = {"code": code, "date": date_str}
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存跌停股池数据成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存跌停股池数据失败: {e}")
            raise
    
    async def save_stock_zt_pool_zbgc_em(self, df, date_str: str = None) -> int:
        """
        保存炸板股池数据
        
        Args:
            df: 炸板股池DataFrame
            date_str: 数据日期 (YYYYMMDD)
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning("⚠️ 炸板股池数据为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_zt_pool_zbgc_em"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和标识
            now = datetime.now()
            
            # 如果没有传入date_str，尝试从df中获取，或者使用当天
            if not date_str:
                 date_str = now.strftime("%Y%m%d")
            
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                record['date'] = date_str
                # 统一字段名
                if '代码' in record:
                    record['code'] = record['代码']
                    record['symbol'] = record['代码']
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                code = record.get("code")
                if not code:
                    continue
                    
                # 使用 code + date 作为唯一标识
                filter_dict = {"code": code, "date": date_str}
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存炸板股池数据成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存炸板股池数据失败: {e}")
            raise
    
    async def save_stock_zt_pool_sub_new_em(self, df, date_str: str = None) -> int:
        """
        保存次新股池数据
        
        Args:
            df: 次新股池DataFrame
            date_str: 数据日期 (YYYYMMDD)
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning("⚠️ 次新股池数据为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_zt_pool_sub_new_em"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和标识
            now = datetime.now()
            
            # 如果没有传入date_str，尝试从df中获取，或者使用当天
            if not date_str:
                 date_str = now.strftime("%Y%m%d")
            
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                record['date'] = date_str
                # 统一字段名
                if '代码' in record:
                    record['code'] = record['代码']
                    record['symbol'] = record['代码']
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                code = record.get("code")
                if not code:
                    continue
                    
                # 使用 code + date 作为唯一标识
                filter_dict = {"code": code, "date": date_str}
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存次新股池数据成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存次新股池数据失败: {e}")
            raise
    
    async def save_stock_zt_pool_strong_em(self, df, date_str: str = None) -> int:
        """
        保存强势股池数据
        
        Args:
            df: 强势股池DataFrame
            date_str: 数据日期 (YYYYMMDD)
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning("⚠️ 强势股池数据为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_zt_pool_strong_em"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和标识
            now = datetime.now()
            
            # 如果没有传入date_str，尝试从df中获取，或者使用当天
            if not date_str:
                 date_str = now.strftime("%Y%m%d")
            
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                record['date'] = date_str
                # 统一字段名
                if '代码' in record:
                    record['code'] = record['代码']
                    record['symbol'] = record['代码']
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                code = record.get("code")
                if not code:
                    continue
                    
                # 使用 code + date 作为唯一标识
                filter_dict = {"code": code, "date": date_str}
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存强势股池数据成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存强势股池数据失败: {e}")
            raise
    
    async def save_stock_zt_pool_previous_em(self, df, date_str: str = None) -> int:
        """
        保存昨日涨停股池数据
        
        Args:
            df: 昨日涨停股池DataFrame
            date_str: 数据日期 (YYYYMMDD)
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning("⚠️ 昨日涨停股池数据为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_zt_pool_previous_em"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和标识
            now = datetime.now()
            
            # 如果没有传入date_str，尝试从df中获取，或者使用当天
            if not date_str:
                 date_str = now.strftime("%Y%m%d")
            
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                record['date'] = date_str
                # 统一字段名
                if '代码' in record:
                    record['code'] = record['代码']
                    record['symbol'] = record['代码']
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                code = record.get("code")
                if not code:
                    continue
                    
                # 使用 code + date 作为唯一标识
                filter_dict = {"code": code, "date": date_str}
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存昨日涨停股池数据成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存昨日涨停股池数据失败: {e}")
            raise
    
    async def save_stock_zt_pool_em(self, df, date_str: str = None) -> int:
        """
        保存涨停股池数据
        
        Args:
            df: 涨停股池DataFrame
            date_str: 数据日期 (YYYYMMDD)
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning("⚠️ 涨停股池数据为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_zt_pool_em"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和标识
            now = datetime.now()
            
            # 如果没有传入date_str，尝试从df中获取，或者使用当天
            if not date_str:
                 date_str = now.strftime("%Y%m%d")
            
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                record['date'] = date_str
                # 统一字段名
                if '代码' in record:
                    record['code'] = record['代码']
                    record['symbol'] = record['代码']
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                code = record.get("code")
                if not code:
                    continue
                    
                # 使用 code + date 作为唯一标识
                filter_dict = {"code": code, "date": date_str}
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存涨停股池数据成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存涨停股池数据失败: {e}")
            raise
    
    async def save_stock_board_change_em(self, df) -> int:
        """
        保存板块异动详情数据
        
        Args:
            df: 板块异动详情DataFrame
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning("⚠️ 板块异动详情数据为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_board_change_em"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和标识
            now = datetime.now()
            date_str = now.strftime("%Y%m%d")
            
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                record['date'] = date_str
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                board = record.get("板块")
                if not board:
                    continue
                    
                # 使用 板块 + date 作为唯一标识
                filter_dict = {"板块": board, "date": date_str}
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存板块异动详情数据成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存板块异动详情数据失败: {e}")
            raise
    
    async def save_stock_changes_em(self, df) -> int:
        """
        保存盘口异动数据
        
        Args:
            df: 盘口异动DataFrame
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning("⚠️ 盘口异动数据为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_changes_em"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和标识
            now = datetime.now()
            date_str = now.strftime("%Y%m%d")
            
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                record['date'] = date_str
                # 统一字段名
                if '代码' in record:
                    record['code'] = record['代码']
                    record['symbol'] = record['代码']
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                code = record.get("code")
                time_val = record.get("时间")
                info = record.get("相关信息")
                
                if not code or not time_val:
                    continue
                    
                # 使用 code + date + time + info 作为唯一标识
                filter_dict = {
                    "code": code, 
                    "date": date_str, 
                    "时间": time_val,
                    "相关信息": info
                }
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存盘口异动数据成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存盘口异动数据失败: {e}")
            raise
    
    async def save_stock_hot_rank_relate_em(self, df) -> int:
        """
        保存相关股票数据
        
        Args:
            df: 相关股票DataFrame
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning("⚠️ 相关股票数据为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_hot_rank_relate_em"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和标识
            now = datetime.now()
            date_str = now.strftime("%Y%m%d")
            
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                record['date'] = date_str
                # 统一字段名
                if '股票代码' in record:
                    record['code'] = record['股票代码']
                    record['symbol'] = record['股票代码']
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                code = record.get("股票代码")
                related_code = record.get("相关股票代码")
                time_val = record.get("时间")
                
                if not code or not related_code:
                    continue
                    
                # 使用 股票代码 + 相关股票代码 + 时间 + date 作为唯一标识
                filter_dict = {
                    "股票代码": code, 
                    "相关股票代码": related_code,
                    "date": date_str
                }
                
                if time_val:
                    filter_dict["时间"] = time_val
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存相关股票数据成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存相关股票数据失败: {e}")
            raise
    
    async def save_stock_hot_search_baidu(self, df, date_str: str = None, time_param: str = "今日") -> int:
        """
        保存热搜股票数据
        
        Args:
            df: 热搜股票DataFrame
            date_str: 数据日期 (YYYYMMDD)
            time_param: 时间参数 ("今日" 或 "1小时")
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning("⚠️ 热搜股票数据为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_hot_search_baidu"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和标识
            now = datetime.now()
            if not date_str:
                date_str = now.strftime("%Y%m%d")
            
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                record['date'] = date_str
                record['time_param'] = time_param
                # 统一字段名
                if '代码' in record:
                    record['code'] = record['代码']
                    record['symbol'] = record['代码']
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                code = record.get("code")
                if not code:
                    continue
                    
                # 使用 code + date + time_param 作为唯一标识
                filter_dict = {
                    "code": code, 
                    "date": date_str,
                    "time_param": time_param
                }
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存热搜股票数据成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存热搜股票数据失败: {e}")
            raise
    
    async def save_stock_hk_hot_rank_latest_em(self, df, symbol: str) -> int:
        """
        保存港股个股人气榜最新排名数据
        
        Args:
            df: 港股个股人气榜最新排名DataFrame
            symbol: 股票代码
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning(f"⚠️ 港股个股人气榜最新排名数据 ({symbol}) 为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_hk_hot_rank_latest_em"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和标识
            now = datetime.now()
            date_str = now.strftime("%Y%m%d")
            
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                record['date'] = date_str
                record['code'] = symbol
                record['symbol'] = symbol
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                item = record.get("item")
                if not item:
                    continue
                    
                # 使用 code + item 作为唯一标识
                filter_dict = {
                    "code": symbol, 
                    "item": item
                }
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存港股个股人气榜最新排名数据 ({symbol}) 成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存港股个股人气榜最新排名数据 ({symbol}) 失败: {e}")
            raise
    
    async def save_stock_hot_rank_latest_em(self, df, symbol: str) -> int:
        """
        保存A股个股人气榜最新排名数据
        
        Args:
            df: A股个股人气榜最新排名DataFrame
            symbol: 股票代码
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning(f"⚠️ A股个股人气榜最新排名数据 ({symbol}) 为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_hot_rank_latest_em"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和标识
            now = datetime.now()
            date_str = now.strftime("%Y%m%d")
            
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                record['date'] = date_str
                record['code'] = symbol
                record['symbol'] = symbol
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                item = record.get("item")
                if not item:
                    continue
                    
                # 使用 code + item 作为唯一标识
                filter_dict = {
                    "code": symbol, 
                    "item": item
                }
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存A股个股人气榜最新排名数据 ({symbol}) 成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存A股个股人气榜最新排名数据 ({symbol}) 失败: {e}")
            raise
    
    async def save_stock_inner_trade_xq(self, df) -> int:
        """
        保存内部交易数据
        
        Args:
            df: 内部交易DataFrame
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning("⚠️ 内部交易数据为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_inner_trade_xq"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和标识
            now = datetime.now()
            date_str = now.strftime("%Y%m%d")
            
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                record['date'] = date_str
                # 统一字段名
                if '股票代码' in record:
                    record['code'] = record['股票代码']
                    record['symbol'] = record['股票代码']
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                code = record.get("股票代码")
                date = record.get("变动日期")
                person = record.get("变动人")
                change = record.get("变动股数")
                
                if not code or not date or not person:
                    continue
                    
                # 使用 股票代码 + 变动日期 + 变动人 + 变动股数 作为唯一标识
                filter_dict = {
                    "股票代码": code, 
                    "变动日期": date,
                    "变动人": person,
                    "变动股数": change
                }
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存内部交易数据成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存内部交易数据失败: {e}")
            raise
    
    async def save_stock_hot_keyword_em(self, df) -> int:
        """
        保存热门关键词数据
        
        Args:
            df: 热门关键词DataFrame
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning("⚠️ 热门关键词数据为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_hot_keyword_em"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和标识
            now = datetime.now()
            date_str = now.strftime("%Y%m%d")
            
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                record['date'] = date_str
                # 统一字段名
                if '股票代码' in record:
                    record['code'] = record['股票代码']
                    record['symbol'] = record['股票代码']
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                code = record.get("股票代码")
                concept_code = record.get("概念代码")
                keyword = record.get("关键词")
                time_val = record.get("时间")
                
                if not code or not keyword:
                    continue
                    
                # 使用 股票代码 + 概念代码 + 关键词 + 时间 + date 作为唯一标识
                filter_dict = {
                    "股票代码": code, 
                    "关键词": keyword,
                    "date": date_str
                }
                
                if concept_code:
                    filter_dict["概念代码"] = concept_code
                
                if time_val:
                    filter_dict["时间"] = time_val
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存热门关键词数据成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存热门关键词数据失败: {e}")
            raise
    
    async def save_stock_hk_hot_rank_detail_realtime_em(self, df, symbol: str) -> int:
        """
        保存港股个股人气榜实时变动数据
        
        Args:
            df: 港股个股人气榜实时变动DataFrame
            symbol: 股票代码
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning(f"⚠️ 港股个股人气榜实时变动数据 ({symbol}) 为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_hk_hot_rank_detail_realtime_em"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和标识
            now = datetime.now()
            date_str = now.strftime("%Y%m%d")
            
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                record['date'] = date_str
                record['code'] = symbol
                record['symbol'] = symbol
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                time_val = record.get("时间")
                if not time_val:
                    continue
                    
                # 使用 code + 时间 作为唯一标识
                filter_dict = {
                    "code": symbol, 
                    "时间": time_val
                }
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存港股个股人气榜实时变动数据 ({symbol}) 成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存港股个股人气榜实时变动数据 ({symbol}) 失败: {e}")
            raise
    
    async def save_stock_hot_rank_detail_realtime_em(self, df, symbol: str) -> int:
        """
        保存A股个股人气榜实时变动数据
        
        Args:
            df: A股个股人气榜实时变动DataFrame
            symbol: 股票代码
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning(f"⚠️ A股个股人气榜实时变动数据 ({symbol}) 为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_hot_rank_detail_realtime_em"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和标识
            now = datetime.now()
            date_str = now.strftime("%Y%m%d")
            
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                record['date'] = date_str
                record['code'] = symbol
                record['symbol'] = symbol
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                time_val = record.get("时间")
                if not time_val:
                    continue
                    
                # 使用 code + 时间 作为唯一标识
                filter_dict = {
                    "code": symbol, 
                    "时间": time_val
                }
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存A股个股人气榜实时变动数据 ({symbol}) 成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存A股个股人气榜实时变动数据 ({symbol}) 失败: {e}")
            raise
    
    async def save_stock_sns_sseinfo(self, df) -> int:
        """
        保存上证e互动数据
        
        Args:
            df: 上证e互动DataFrame
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning("⚠️ 上证e互动数据为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_sns_sseinfo"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和标识
            now = datetime.now()
            date_str = now.strftime("%Y%m%d")
            
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                record['date'] = date_str
                # 统一字段名
                if '股票代码' in record:
                    record['code'] = record['股票代码']
                    record['symbol'] = record['股票代码']
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                code = record.get("股票代码")
                question_time = record.get("问题时间")
                question = record.get("问题")
                
                if not code or not question_time:
                    continue
                    
                # 使用 股票代码 + 问题时间 + 问题 作为唯一标识
                filter_dict = {
                    "股票代码": code, 
                    "问题时间": question_time,
                    "问题": question
                }
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存上证e互动数据成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存上证e互动数据失败: {e}")
            raise
    
    async def save_stock_irm_ans_cninfo(self, df) -> int:
        """
        保存互动易-回答数据
        
        Args:
            df: 互动易-回答DataFrame
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning("⚠️ 互动易-回答数据为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_irm_ans_cninfo"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和标识
            now = datetime.now()
            date_str = now.strftime("%Y%m%d")
            
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                record['date'] = date_str
                # 统一字段名
                if '股票代码' in record:
                    record['code'] = record['股票代码']
                    record['symbol'] = record['股票代码']
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                code = record.get("股票代码")
                question_time = record.get("提问时间")
                question = record.get("问题")
                
                if not code or not question_time:
                    continue
                    
                # 使用 股票代码 + 提问时间 + 问题 作为唯一标识
                filter_dict = {
                    "股票代码": code, 
                    "提问时间": question_time,
                    "问题": question
                }
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存互动易-回答数据成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存互动易-回答数据失败: {e}")
            raise
    
    async def save_stock_irm_cninfo(self, df) -> int:
        """
        保存互动易-提问数据
        
        Args:
            df: 互动易-提问DataFrame
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning("⚠️ 互动易-提问数据为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_irm_cninfo"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和标识
            now = datetime.now()
            date_str = now.strftime("%Y%m%d")
            
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                record['date'] = date_str
                # 统一字段名
                if '股票代码' in record:
                    record['code'] = record['股票代码']
                    record['symbol'] = record['股票代码']
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                code = record.get("股票代码")
                question_time = record.get("提问时间")
                question = record.get("问题")
                question_id = record.get("问题编号")
                
                if not code or not question_time:
                    continue
                    
                # 使用 股票代码 + 提问时间 + 问题编号 作为唯一标识
                filter_dict = {
                    "股票代码": code, 
                    "提问时间": question_time,
                }
                
                if question_id:
                    filter_dict["问题编号"] = question_id
                elif question:
                    filter_dict["问题"] = question
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存互动易-提问数据成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存互动易-提问数据失败: {e}")
            raise
    
    async def save_stock_hk_hot_rank_detail_em(self, df, symbol: str) -> int:
        """
        保存港股股票热度-历史趋势数据
        
        Args:
            df: 港股股票热度-历史趋势DataFrame
            symbol: 股票代码
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning(f"⚠️ 港股股票热度-历史趋势数据 ({symbol}) 为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_hk_hot_rank_detail_em"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和标识
            now = datetime.now()
            date_str = now.strftime("%Y%m%d")
            
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                record['date'] = date_str
                record['code'] = symbol
                record['symbol'] = symbol
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                time_val = record.get("时间")
                if not time_val:
                    continue
                    
                # 使用 证券代码 + 时间 作为唯一标识
                filter_dict = {
                    "证券代码": symbol, 
                    "时间": time_val
                }
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存港股股票热度-历史趋势数据 ({symbol}) 成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存港股股票热度-历史趋势数据 ({symbol}) 失败: {e}")
            raise
    
    async def save_stock_hot_rank_detail_em(self, df, symbol: str) -> int:
        """
        保存A股股票热度-历史趋势及粉丝特征数据
        
        Args:
            df: A股股票热度-历史趋势及粉丝特征DataFrame
            symbol: 股票代码
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning(f"⚠️ A股股票热度-历史趋势及粉丝特征数据 ({symbol}) 为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_hot_rank_detail_em"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和标识
            now = datetime.now()
            date_str = now.strftime("%Y%m%d")
            
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                record['date'] = date_str
                record['code'] = symbol
                record['symbol'] = symbol
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                time_val = record.get("时间")
                if not time_val:
                    continue
                    
                # 使用 证券代码 + 时间 作为唯一标识
                filter_dict = {
                    "证券代码": symbol, 
                    "时间": time_val
                }
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存A股股票热度-历史趋势及粉丝特征数据 ({symbol}) 成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存A股股票热度-历史趋势及粉丝特征数据 ({symbol}) 失败: {e}")
            raise
    
    async def save_stock_hk_hot_rank_em(self, df) -> int:
        """
        保存港股人气榜数据
        
        Args:
            df: 港股人气榜DataFrame
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning("⚠️ 港股人气榜数据为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_hk_hot_rank_em"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和标识
            now = datetime.now()
            date_str = now.strftime("%Y%m%d")
            
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                record['date'] = date_str
                # 统一字段名
                if '代码' in record:
                    record['code'] = record['代码']
                    record['symbol'] = record['代码']
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                code = record.get("代码")
                rank = record.get("当前排名")
                
                if not code:
                    continue
                    
                # 使用 代码 + date 作为唯一标识
                filter_dict = {
                    "代码": code, 
                    "date": date_str
                }
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存港股人气榜数据成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存港股人气榜数据失败: {e}")
            raise
    
    async def save_stock_hot_up_em(self, df) -> int:
        """
        保存飙升榜-A股数据
        
        Args:
            df: 飙升榜-A股DataFrame
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning("⚠️ 飙升榜-A股数据为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_hot_up_em"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和标识
            now = datetime.now()
            date_str = now.strftime("%Y%m%d")
            
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                record['date'] = date_str
                # 统一字段名
                if '代码' in record:
                    record['code'] = record['代码']
                    record['symbol'] = record['代码']
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                code = record.get("代码")
                
                if not code:
                    continue
                    
                # 使用 代码 + date 作为唯一标识
                filter_dict = {
                    "代码": code, 
                    "date": date_str
                }
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存飙升榜-A股数据成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存飙升榜-A股数据失败: {e}")
            raise
    
    async def save_stock_hot_rank_em(self, df) -> int:
        """
        保存人气榜-A股数据
        
        Args:
            df: 人气榜-A股DataFrame
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning("⚠️ 人气榜-A股数据为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_hot_rank_em"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和标识
            now = datetime.now()
            date_str = now.strftime("%Y%m%d")
            
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                record['date'] = date_str
                # 统一字段名
                if '代码' in record:
                    record['code'] = record['代码']
                    record['symbol'] = record['代码']
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                code = record.get("代码")
                
                if not code:
                    continue
                    
                # 使用 代码 + date 作为唯一标识
                filter_dict = {
                    "代码": code, 
                    "date": date_str
                }
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存人气榜-A股数据成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存人气榜-A股数据失败: {e}")
            raise
    
    async def save_stock_hot_deal_xq(self, df) -> int:
        """
        保存交易排行榜数据
        
        Args:
            df: 交易排行榜DataFrame
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning("⚠️ 交易排行榜数据为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_hot_deal_xq"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和标识
            now = datetime.now()
            date_str = now.strftime("%Y%m%d")
            
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                record['date'] = date_str
                # 统一字段名
                if '股票代码' in record:
                    record['code'] = record['股票代码']
                    record['symbol'] = record['股票代码']
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                code = record.get("股票代码")
                
                if not code:
                    continue
                    
                # 使用 股票代码 + date 作为唯一标识
                filter_dict = {
                    "股票代码": code, 
                    "date": date_str
                }
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存交易排行榜数据成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存交易排行榜数据失败: {e}")
            raise
    
    async def save_stock_hot_tweet_xq(self, df) -> int:
        """
        保存讨论排行榜数据
        
        Args:
            df: 讨论排行榜DataFrame
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning("⚠️ 讨论排行榜数据为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_hot_tweet_xq"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和标识
            now = datetime.now()
            date_str = now.strftime("%Y%m%d")
            
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                record['date'] = date_str
                # 统一字段名
                if '股票代码' in record:
                    record['code'] = record['股票代码']
                    record['symbol'] = record['股票代码']
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                code = record.get("股票代码")
                
                if not code:
                    continue
                    
                # 使用 股票代码 + date 作为唯一标识
                filter_dict = {
                    "股票代码": code, 
                    "date": date_str
                }
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存讨论排行榜数据成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存讨论排行榜数据失败: {e}")
            raise
    
    async def save_stock_hot_follow_xq(self, df) -> int:
        """
        保存关注排行榜数据
        
        Args:
            df: 关注排行榜DataFrame
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning("⚠️ 关注排行榜数据为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_hot_follow_xq"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和标识
            now = datetime.now()
            date_str = now.strftime("%Y%m%d")
            
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                record['date'] = date_str
                # 统一字段名
                if '股票代码' in record:
                    record['code'] = record['股票代码']
                    record['symbol'] = record['股票代码']
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                code = record.get("股票代码")
                
                if not code:
                    continue
                    
                # 使用 股票代码 + date 作为唯一标识
                filter_dict = {
                    "股票代码": code, 
                    "date": date_str
                }
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存关注排行榜数据成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存关注排行榜数据失败: {e}")
            raise
    
    async def save_stock_board_industry_hist_min_em(self, df, symbol: str, period: str) -> int:
        """
        保存东方财富-指数-分时数据
        
        Args:
            df: 东方财富-指数-分时DataFrame
            symbol: 行业代码
            period: 周期
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning(f"⚠️ 东方财富-指数-分时数据 ({symbol}, {period}) 为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_board_industry_hist_min_em"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和标识
            now = datetime.now()
            date_str = now.strftime("%Y%m%d")
            
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                record['date'] = date_str
                record['symbol'] = symbol
                record['period'] = period
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                date_time = record.get("日期时间")
                
                if not date_time:
                    continue
                    
                # 使用 symbol + period + 日期时间 作为唯一标识
                filter_dict = {
                    "symbol": symbol,
                    "period": period,
                    "日期时间": date_time
                }
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存东方财富-指数-分时数据 ({symbol}, {period}) 成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存东方财富-指数-分时数据 ({symbol}, {period}) 失败: {e}")
            raise
    
    async def save_stock_board_industry_hist_em(self, df, symbol: str, start_date: str, end_date: str, period: str, adjust: str) -> int:
        """
        保存东方财富-指数-日频数据
        
        Args:
            df: 东方财富-指数-日频DataFrame
            symbol: 行业代码
            start_date: 开始日期
            end_date: 结束日期
            period: 周期
            adjust: 复权
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning(f"⚠️ 东方财富-指数-日频数据 ({symbol}, {period}, {adjust}) 为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_board_industry_hist_em"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和标识
            now = datetime.now()
            date_str = now.strftime("%Y%m%d")
            
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                record['date_str'] = date_str
                record['symbol'] = symbol
                record['period'] = period
                record['adjust'] = adjust
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                date_val = record.get("日期")
                
                if not date_val:
                    continue
                    
                # 使用 symbol + period + adjust + 日期 作为唯一标识
                filter_dict = {
                    "symbol": symbol,
                    "period": period,
                    "adjust": adjust,
                    "日期": date_val
                }
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存东方财富-指数-日频数据 ({symbol}, {period}, {adjust}) 成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存东方财富-指数-日频数据 ({symbol}, {period}, {adjust}) 失败: {e}")
            raise
    
    async def save_stock_board_industry_cons_em(self, df, symbol: str) -> int:
        """
        保存东方财富-成份股数据
        
        Args:
            df: 东方财富-成份股DataFrame
            symbol: 行业代码
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning(f"⚠️ 东方财富-成份股数据 ({symbol}) 为空，无法保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_board_industry_cons_em"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 添加时间戳和标识
            now = datetime.now()
            date_str = now.strftime("%Y%m%d")
            
            for record in records:
                record['updated_at'] = now
                record['source'] = 'akshare'
                record['date'] = date_str
                record['symbol'] = symbol
                # 统一字段名
                if '代码' in record:
                    record['code'] = record['代码']
            
            # 批量插入或更新
            from pymongo import UpdateOne
            operations = []
            
            for record in records:
                code = record.get("代码")
                
                if not code:
                    continue
                    
                # 使用 symbol + code + date 作为唯一标识
                filter_dict = {
                    "symbol": symbol,
                    "代码": code,
                    "date": date_str
                }
                
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations, ordered=False)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存东方财富-成份股数据 ({symbol}) 成功: {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存东方财富-成份股数据 ({symbol}) 失败: {e}")
            raise


    async def save_stock_comment_detail_zhpj_lspf_em(self, data: pd.DataFrame, symbol: str) -> int:
        """
        保存历史评分数据
        
        Args:
            data: 包含历史评分数据的DataFrame
            symbol: 股票代码
            
        Returns:
            保存的记录数
        """
        if data is None or data.empty:
            logger.warning(f"历史评分数据为空: {symbol}")
            return 0
            
        try:
            collection = self.db["stock_comment_detail_zhpj_lspf_em"]
            
            # 添加证券代码字段
            data = data.copy()
            data["证券代码"] = symbol
            
            # 转换为字典列表
            records = data.to_dict("records")
            
            # 批量更新
            operations = []
            for record in records:
                # 使用证券代码和日期作为唯一标识
                filter_dict = {
                    "证券代码": record.get("证券代码"),
                    "日期": record.get("日期")
                }
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"保存历史评分数据: {symbol}, 共 {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"保存历史评分数据失败: {symbol}, 错误: {e}")
            raise


    async def save_stock_comment_detail_scrd_focus_em(self, data: pd.DataFrame, symbol: str) -> int:
        """
        保存用户关注指数数据
        
        Args:
            data: 包含用户关注指数数据的DataFrame
            symbol: 股票代码
            
        Returns:
            保存的记录数
        """
        if data is None or data.empty:
            logger.warning(f"用户关注指数数据为空: {symbol}")
            return 0
            
        try:
            collection = self.db["stock_comment_detail_scrd_focus_em"]
            
            # 添加证券代码字段
            data = data.copy()
            data["证券代码"] = symbol
            
            # 转换为字典列表
            records = data.to_dict("records")
            
            # 批量更新
            operations = []
            for record in records:
                # 使用证券代码和交易日作为唯一标识
                filter_dict = {
                    "证券代码": record.get("证券代码"),
                    "交易日": record.get("交易日")
                }
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"保存用户关注指数数据: {symbol}, 共 {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"保存用户关注指数数据失败: {symbol}, 错误: {e}")
            raise


    async def save_stock_comment_detail_scrd_desire_em(self, data: pd.DataFrame, symbol: str) -> int:
        """
        保存市场参与意愿数据
        
        Args:
            data: 包含市场参与意愿数据的DataFrame
            symbol: 股票代码
            
        Returns:
            保存的记录数
        """
        if data is None or data.empty:
            logger.warning(f"市场参与意愿数据为空: {symbol}")
            return 0
            
        try:
            collection = self.db["stock_comment_detail_scrd_desire_em"]
            
            # 添加证券代码字段
            data = data.copy()
            data["证券代码"] = symbol
            
            # 转换为字典列表
            records = data.to_dict("records")
            
            # 批量更新
            operations = []
            for record in records:
                # 使用证券代码和日期时间作为唯一标识
                filter_dict = {
                    "证券代码": record.get("证券代码"),
                    "日期时间": record.get("日期时间")
                }
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"保存市场参与意愿数据: {symbol}, 共 {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"保存市场参与意愿数据失败: {symbol}, 错误: {e}")
            raise


    async def save_stock_comment_detail_scrd_desire_daily_em(self, data: pd.DataFrame, symbol: str) -> int:
        """
        保存日度市场参与意愿数据
        
        Args:
            data: 包含日度市场参与意愿数据的DataFrame
            symbol: 股票代码
            
        Returns:
            保存的记录数
        """
        if data is None or data.empty:
            logger.warning(f"日度市场参与意愿数据为空: {symbol}")
            return 0
            
        try:
            collection = self.db["stock_comment_detail_scrd_desire_daily_em"]
            
            # 添加证券代码字段
            data = data.copy()
            data["证券代码"] = symbol
            
            # 转换为字典列表
            records = data.to_dict("records")
            
            # 批量更新
            operations = []
            for record in records:
                # 使用证券代码和交易日作为唯一标识
                filter_dict = {
                    "证券代码": record.get("证券代码"),
                    "交易日": record.get("交易日")
                }
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"保存日度市场参与意愿数据: {symbol}, 共 {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"保存日度市场参与意愿数据失败: {symbol}, 错误: {e}")
            raise


    async def save_stock_hsgt_fund_flow_summary_em(self, data: pd.DataFrame) -> int:
        """
        保存沪深港通资金流向数据
        
        Args:
            data: 包含沪深港通资金流向数据的DataFrame
            
        Returns:
            保存的记录数
        """
        if data is None or data.empty:
            logger.warning("沪深港通资金流向数据为空")
            return 0
            
        try:
            collection = self.db["stock_hsgt_fund_flow_summary_em"]
            
            # 转换为字典列表
            records = data.to_dict("records")
            
            # 批量更新
            operations = []
            for record in records:
                # 使用交易日、类型、板块、资金方向作为唯一标识
                filter_dict = {
                    "交易日": record.get("交易日"),
                    "类型": record.get("类型"),
                    "板块": record.get("板块"),
                    "资金方向": record.get("资金方向")
                }
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"保存沪深港通资金流向数据: 共 {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"保存沪深港通资金流向数据失败: {e}")
            raise


    async def save_stock_sgt_settlement_exchange_rate_szse(self, data: pd.DataFrame) -> int:
        """
        保存结算汇率-深港通数据
        
        Args:
            data: 包含结算汇率-深港通数据的DataFrame
            
        Returns:
            保存的记录数
        """
        if data is None or data.empty:
            logger.warning("结算汇率-深港通数据为空")
            return 0
            
        try:
            collection = self.db["stock_sgt_settlement_exchange_rate_szse"]
            
            # 转换为字典列表
            records = data.to_dict("records")
            
            # 批量更新
            operations = []
            for record in records:
                # 使用适用日期和货币种类作为唯一标识
                filter_dict = {
                    "适用日期": record.get("适用日期"),
                    "货币种类": record.get("货币种类")
                }
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"保存结算汇率-深港通数据: 共 {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"保存结算汇率-深港通数据失败: {e}")
            raise


    async def save_stock_sgt_settlement_exchange_rate_sse(self, data: pd.DataFrame) -> int:
        """
        保存结算汇率-沪港通数据
        
        Args:
            data: 包含结算汇率-沪港通数据的DataFrame
            
        Returns:
            保存的记录数
        """
        if data is None or data.empty:
            logger.warning("结算汇率-沪港通数据为空")
            return 0
            
        try:
            collection = self.db["stock_sgt_settlement_exchange_rate_sse"]
            
            # 转换为字典列表
            records = data.to_dict("records")
            
            # 批量更新
            operations = []
            for record in records:
                # 使用适用日期和货币种类作为唯一标识
                filter_dict = {
                    "适用日期": record.get("适用日期"),
                    "货币种类": record.get("货币种类")
                }
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"保存结算汇率-沪港通数据: 共 {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"保存结算汇率-沪港通数据失败: {e}")
            raise

    async def save_stock_sgt_reference_exchange_rate_szse(self, df: pd.DataFrame) -> int:
        """
        保存参考汇率-深港通数据 (需求107)
        
        Args:
            df: 参考汇率数据DataFrame
            
        Returns:
            保存的记录数
        """
        try:
            if df is None or df.empty:
                logger.warning("参考汇率-深港通数据为空，跳过保存")
                return 0
            
            db = get_mongo_db()
            collection = db["stock_sgt_reference_exchange_rate_szse"]
            
            # 转换DataFrame为字典列表
            records = df.to_dict('records')
            
            # 批量upsert操作
            operations = []
            for record in records:
                # 使用适用日期作为唯一键
                filter_dict = {"适用日期": record.get("适用日期")}
                operations.append(
                    UpdateOne(
                        filter_dict,
                        {"$set": record},
                        upsert=True
                    )
                )
            
            if operations:
                result = await collection.bulk_write(operations)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存参考汇率-深港通数据: 共 {saved_count} 条")
                return saved_count
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ 保存参考汇率-深港通数据失败: {e}")
            raise

    async def save_stock_sgt_reference_exchange_rate_sse(self, df: pd.DataFrame) -> int:
        """保存参考汇率-沪港通数据 (需求108)"""
        return await self._save_with_date_key(df, "stock_sgt_reference_exchange_rate_sse", "适用日期")

    async def save_stock_hk_ggt_components_em(self, df: pd.DataFrame) -> int:
        """保存港股通成份股数据 (需求109)"""
        return await self._save_with_code_key(df, "stock_hk_ggt_components_em", "代码")

    async def save_stock_hsgt_fund_min_em(self, df: pd.DataFrame) -> int:
        """保存沪深港通分时数据 (需求110)"""
        return await self._save_with_datetime_key(df, "stock_hsgt_fund_min_em", ["日期", "时间"])

    async def save_stock_hsgt_board_rank_em(self, df: pd.DataFrame) -> int:
        """保存板块排行数据 (需求111)"""
        return await self._save_with_datetime_key(df, "stock_hsgt_board_rank_em", ["序号", "报告时间"])

    async def save_stock_hsgt_hold_stock_em(self, df: pd.DataFrame) -> int:
        """保存个股排行数据 (需求112)"""
        return await self._save_with_code_and_date_key(df, "stock_hsgt_hold_stock_em", "代码", "日期")

    async def save_stock_hsgt_stock_statistics_em(self, df: pd.DataFrame) -> int:
        """保存每日个股统计数据 (需求113)"""
        return await self._save_with_code_key(df, "stock_hsgt_stock_statistics_em", "代码")

    async def save_stock_hsgt_institution_statistics_em(self, df: pd.DataFrame) -> int:
        """保存机构排行数据 (需求114)"""
        return await self._save_with_seq_key(df, "stock_hsgt_institution_statistics_em", "序号")

    async def save_stock_hsgt_sh_hk_spot_em(self, df: pd.DataFrame) -> int:
        """保存沪深港通-港股通(沪>港)实时行情数据 (需求115)"""
        return await self._save_with_code_key(df, "stock_hsgt_sh_hk_spot_em", "代码")

    async def save_stock_hsgt_hist_em(self, df: pd.DataFrame) -> int:
        """保存沪深港通历史数据 (需求116)"""
        return await self._save_with_date_key(df, "stock_hsgt_hist_em", "日期")

    async def save_stock_hsgt_individual_em(self, df: pd.DataFrame) -> int:
        """保存沪深港通持股-个股数据 (需求117)"""
        return await self._save_with_date_key(df, "stock_hsgt_individual_em", "持股日期")

    async def save_stock_hsgt_individual_detail_em(self, df: pd.DataFrame) -> int:
        """保存沪深港通持股-个股详情数据 (需求118)"""
        return await self._save_with_datetime_key(df, "stock_hsgt_individual_detail_em", ["持股日期", "机构名称"])

    async def save_stock_em_hsgt_north_net_flow_in(self, df: pd.DataFrame) -> int:
        """保存北向资金流入数据 (需求119)"""
        return await self._save_with_date_key(df, "stock_em_hsgt_north_net_flow_in", "日期")

    async def save_stock_em_hsgt_south_net_flow_in(self, df: pd.DataFrame) -> int:
        """保存南向资金流入数据 (需求120)"""
        return await self._save_with_date_key(df, "stock_em_hsgt_south_net_flow_in", "日期")

    async def save_news_trade_notify_dividend_baidu(self, df: pd.DataFrame) -> int:
        """保存分红派息数据 (需求121)"""
        return await self._save_with_code_and_date_key(df, "news_trade_notify_dividend_baidu", "代码", "公告日期")

    async def save_stock_news_em(self, df: pd.DataFrame) -> int:
        """保存个股新闻数据 (需求122)"""
        return await self._save_with_datetime_key(df, "stock_news_em", ["关键词", "新闻标题", "发布时间"])

    async def save_stock_news_main_cx(self, df: pd.DataFrame) -> int:
        """保存财经内容精选数据 (需求123)"""
        return await self._save_with_datetime_key(df, "stock_news_main_cx", ["标题", "发布时间"])

    async def save_news_report_time_baidu(self, df: pd.DataFrame) -> int:
        """保存财报发行数据 (需求124)"""
        return await self._save_with_code_and_date_key(df, "news_report_time_baidu", "代码", "报告日期")

    async def save_stock_dxsyl_em(self, df: pd.DataFrame) -> int:
        """保存打新收益率数据 (需求125)"""
        return await self._save_with_code_key(df, "stock_dxsyl_em", "代码")

    async def save_stock_xgsglb_em(self, df: pd.DataFrame) -> int:
        """保存新股申购与中签数据 (需求126)"""
        return await self._save_with_code_key(df, "stock_xgsglb_em", "股票代码")

    async def save_stock_yjbb_em(self, df: pd.DataFrame) -> int:
        """保存业绩报表数据 (需求127)"""
        return await self._save_with_code_and_date_key(df, "stock_yjbb_em", "股票代码", "报告日期")

    async def save_stock_yjkb_em(self, df: pd.DataFrame) -> int:
        """保存业绩快报数据 (需求128)"""
        return await self._save_with_code_and_date_key(df, "stock_yjkb_em", "股票代码", "报告日期")

    async def save_stock_yjyg_em(self, df: pd.DataFrame) -> int:
        """保存业绩预告数据 (需求129)"""
        return await self._save_with_code_and_date_key(df, "stock_yjyg_em", "股票代码", "报告期")

    async def save_stock_yysj_em(self, df: pd.DataFrame) -> int:
        """保存营业收入数据 (需求130)"""
        return await self._save_with_code_and_date_key(df, "stock_yysj_em", "股票代码", "报告期")

    async def save_stock_report_disclosure(self, df: pd.DataFrame) -> int:
        """保存报告披露数据 (需求131)"""
        return await self._save_with_code_and_date_key(df, "stock_report_disclosure", "股票代码", "报告期")

    async def save_stock_zh_a_disclosure_report_cninfo(self, df: pd.DataFrame) -> int:
        """保存信息披露报告数据 (需求132)"""
        return await self._save_with_code_and_date_key(df, "stock_zh_a_disclosure_report_cninfo", "证券代码", "报告时间")

    async def save_stock_zh_a_disclosure_relation_cninfo(self, df: pd.DataFrame) -> int:
        """保存关联方披露数据 (需求133)"""
        return await self._save_with_code_key(df, "stock_zh_a_disclosure_relation_cninfo", "证券代码")

    async def save_stock_industry_category_cninfo(self, df: pd.DataFrame) -> int:
        """保存行业分类数据 (需求134)"""
        return await self._save_with_code_key(df, "stock_industry_category_cninfo", "证券代码")

    async def save_stock_industry_change_cninfo(self, df: pd.DataFrame) -> int:
        """保存行业变更数据 (需求135)"""
        return await self._save_with_code_and_date_key(df, "stock_industry_change_cninfo", "证券代码", "变更日期")

    async def save_stock_share_change_cninfo(self, df: pd.DataFrame) -> int:
        """保存股本变动数据 (需求136)"""
        return await self._save_with_code_and_date_key(df, "stock_share_change_cninfo", "证券代码", "变更日期")

    async def save_stock_allotment_cninfo(self, df: pd.DataFrame) -> int:
        """保存配股数据 (需求137)"""
        return await self._save_with_code_and_date_key(df, "stock_allotment_cninfo", "证券代码", "公告日期")

    async def save_stock_profile_cninfo(self, df: pd.DataFrame) -> int:
        """保存公司概况数据 (需求138)"""
        return await self._save_with_code_key(df, "stock_profile_cninfo", "证券代码")

    async def save_stock_ipo_summary_cninfo(self, df: pd.DataFrame) -> int:
        """保存IPO摘要数据 (需求139)"""
        return await self._save_with_code_key(df, "stock_ipo_summary_cninfo", "证券代码")

    async def save_stock_ipo_info_cninfo(self, df: pd.DataFrame) -> int:
        """保存IPO信息数据 (需求140)"""
        return await self._save_with_code_key(df, "stock_ipo_info_cninfo", "证券代码")

    async def save_stock_zcfz_em(self, df: pd.DataFrame) -> int:
        """保存资产负债表数据 (需求141)"""
        return await self._save_with_code_and_date_key(df, "stock_zcfz_em", "股票代码", "报告期")

    async def save_stock_lrb_em(self, df: pd.DataFrame) -> int:
        """保存利润表数据 (需求142)"""
        return await self._save_with_code_and_date_key(df, "stock_lrb_em", "股票代码", "报告期")

    async def save_stock_xjll_em(self, df: pd.DataFrame) -> int:
        """保存现金流量表数据 (需求143)"""
        return await self._save_with_code_and_date_key(df, "stock_xjll_em", "股票代码", "报告期")

    async def save_stock_cwbbzy_em(self, df: pd.DataFrame) -> int:
        """保存主要指标数据 (需求144)"""
        return await self._save_with_code_and_date_key(df, "stock_cwbbzy_em", "股票代码", "报告期")

    async def save_stock_yjkb_em_v2(self, df: pd.DataFrame) -> int:
        """保存业绩快报V2数据 (需求145)"""
        return await self._save_with_code_and_date_key(df, "stock_yjkb_em_v2", "股票代码", "报告期")

    async def save_stock_profit_forecast_em(self, df: pd.DataFrame) -> int:
        """保存盈利预测数据 (需求146)"""
        return await self._save_with_code_and_date_key(df, "stock_profit_forecast_em", "股票代码", "报告期")

    async def save_stock_fhps_detail_ths(self, df: pd.DataFrame) -> int:
        """保存分红派送详情数据 (需求147)"""
        return await self._save_with_code_and_date_key(df, "stock_fhps_detail_ths", "股票代码", "分红年度")

    async def save_stock_hk_fhpx_detail_ths(self, df: pd.DataFrame) -> int:
        """保存港股分红派息数据 (需求148)"""
        return await self._save_with_code_and_date_key(df, "stock_hk_fhpx_detail_ths", "股票代码", "除权除息日")

    async def save_stock_fund_flow_individual(self, df: pd.DataFrame) -> int:
        """保存个股资金流向数据 (需求149)"""
        return await self._save_with_code_and_date_key(df, "stock_fund_flow_individual", "股票代码", "日期")

    async def save_stock_fund_flow_concept(self, df: pd.DataFrame) -> int:
        """保存概念资金流向数据 (需求150)"""
        return await self._save_with_datetime_key(df, "stock_fund_flow_concept", ["名称", "日期"])

    async def save_stock_fund_flow_industry(self, df: pd.DataFrame) -> int:
        """保存行业资金流向数据 (需求151)"""
        return await self._save_with_datetime_key(df, "stock_fund_flow_industry", ["名称", "日期"])

    async def save_stock_fund_flow_big_deal(self, df: pd.DataFrame) -> int:
        """保存大单资金流向数据 (需求152)"""
        return await self._save_with_code_and_date_key(df, "stock_fund_flow_big_deal", "代码", "日期")

    async def save_stock_individual_fund_flow(self, df: pd.DataFrame) -> int:
        """保存个股历史资金流向数据 (需求153)"""
        return await self._save_with_date_key(df, "stock_individual_fund_flow", "日期")

    async def save_stock_individual_fund_flow_rank(self, df: pd.DataFrame) -> int:
        """保存个股资金流排名数据 (需求154)"""
        return await self._save_with_code_key(df, "stock_individual_fund_flow_rank", "代码")

    async def save_stock_market_fund_flow(self, df: pd.DataFrame) -> int:
        """保存市场资金流向数据 (需求155)"""
        return await self._save_with_date_key(df, "stock_market_fund_flow", "日期")

    async def save_stock_sector_fund_flow_rank(self, df: pd.DataFrame) -> int:
        """保存板块资金流排名数据 (需求156)"""
        return await self._save_with_datetime_key(df, "stock_sector_fund_flow_rank", ["序号", "名称"])

    async def save_stock_main_fund_flow(self, df: pd.DataFrame) -> int:
        """保存主力资金流向数据 (需求157)"""
        return await self._save_with_code_and_date_key(df, "stock_main_fund_flow", "代码", "日期")

    async def save_stock_sector_fund_flow_summary(self, df: pd.DataFrame) -> int:
        """保存板块资金流汇总数据 (需求158)"""
        return await self._save_with_datetime_key(df, "stock_sector_fund_flow_summary", ["名称", "日期"])

    async def save_stock_sector_fund_flow_hist(self, df: pd.DataFrame) -> int:
        """保存板块历史资金流向数据 (需求159)"""
        return await self._save_with_date_key(df, "stock_sector_fund_flow_hist", "日期")

    async def save_stock_concept_fund_flow_hist(self, df: pd.DataFrame) -> int:
        """保存概念历史资金流向数据 (需求160)"""
        return await self._save_with_date_key(df, "stock_concept_fund_flow_hist", "日期")

    async def save_stock_cyq_em(self, df: pd.DataFrame) -> int:
        """保存筹码分布数据 (需求161)"""
        return await self._save_with_code_and_date_key(df, "stock_cyq_em", "股票代码", "日期")

    async def save_stock_gddh_em(self, df: pd.DataFrame) -> int:
        """保存股东大会数据 (需求162)"""
        return await self._save_with_code_and_date_key(df, "stock_gddh_em", "股票代码", "公告日期")

    async def save_stock_zdhtmx_em(self, df: pd.DataFrame) -> int:
        """保存重大合同明细数据 (需求163)"""
        return await self._save_with_code_and_date_key(df, "stock_zdhtmx_em", "股票代码", "签订日期")

    async def save_stock_research_report_em(self, df: pd.DataFrame) -> int:
        """保存研究报告数据 (需求164)"""
        return await self._save_with_datetime_key(df, "stock_research_report_em", ["股票代码", "报告日期", "研究机构"])

    async def save_stock_notice_report(self, df: pd.DataFrame) -> int:
        """保存公告报告数据 (需求165)"""
        return await self._save_with_datetime_key(df, "stock_notice_report", ["股票代码", "公告日期", "公告标题"])

    async def save_stock_financial_report_sina(self, df: pd.DataFrame) -> int:
        """保存财务报告数据-新浪 (需求166)"""
        return await self._save_with_code_key(df, "stock_financial_report_sina", "股票代码")

    async def save_stock_balance_sheet_by_report_em(self, df: pd.DataFrame) -> int:
        """保存资产负债表-按报告期数据 (需求167)"""
        return await self._save_with_code_and_date_key(df, "stock_balance_sheet_by_report_em", "股票代码", "报告期")

    async def save_stock_balance_sheet_by_yearly_em(self, df: pd.DataFrame) -> int:
        """保存资产负债表-按年度数据 (需求168)"""
        return await self._save_with_code_and_date_key(df, "stock_balance_sheet_by_yearly_em", "股票代码", "报告期")

    async def save_stock_profit_sheet_by_report_em(self, df: pd.DataFrame) -> int:
        """保存利润表-按报告期数据 (需求169)"""
        return await self._save_with_code_and_date_key(df, "stock_profit_sheet_by_report_em", "股票代码", "报告期")

    async def save_stock_profit_sheet_by_quarterly_em(self, df: pd.DataFrame) -> int:
        """保存利润表-按季度数据 (需求170)"""
        return await self._save_with_code_and_date_key(df, "stock_profit_sheet_by_quarterly_em", "股票代码", "报告期")

    async def save_stock_profit_sheet_by_yearly_em(self, df: pd.DataFrame) -> int:
        """保存利润表-按年度数据 (需求171)"""
        return await self._save_with_code_and_date_key(df, "stock_profit_sheet_by_yearly_em", "股票代码", "报告期")

    async def save_stock_cash_flow_sheet_by_report_em(self, df: pd.DataFrame) -> int:
        """保存现金流量表-按报告期数据 (需求172)"""
        return await self._save_with_code_and_date_key(df, "stock_cash_flow_sheet_by_report_em", "股票代码", "报告期")

    async def save_stock_cash_flow_sheet_by_yearly_em(self, df: pd.DataFrame) -> int:
        """保存现金流量表-按年度数据 (需求173)"""
        return await self._save_with_code_and_date_key(df, "stock_cash_flow_sheet_by_yearly_em", "股票代码", "报告期")

    async def save_stock_cash_flow_sheet_by_quarterly_em(self, df: pd.DataFrame) -> int:
        """保存现金流量表-按季度数据 (需求174)"""
        return await self._save_with_code_and_date_key(df, "stock_cash_flow_sheet_by_quarterly_em", "股票代码", "报告期")

    async def save_stock_financial_debt_ths(self, df: pd.DataFrame) -> int:
        """保存财务负债数据-同花顺 (需求175)"""
        return await self._save_with_code_and_date_key(df, "stock_financial_debt_ths", "股票代码", "报告期")

    async def save_stock_financial_benefit_ths(self, df: pd.DataFrame) -> int:
        """保存财务收益数据-同花顺 (需求176)"""
        return await self._save_with_code_and_date_key(df, "stock_financial_benefit_ths", "股票代码", "报告期")

    async def save_stock_financial_cash_ths(self, df: pd.DataFrame) -> int:
        """保存财务现金数据-同花顺 (需求177)"""
        return await self._save_with_code_and_date_key(df, "stock_financial_cash_ths", "股票代码", "报告期")

    async def save_stock_balance_sheet_by_report_delisted_em(self, df: pd.DataFrame) -> int:
        """保存退市公司资产负债表数据 (需求178)"""
        return await self._save_with_code_and_date_key(df, "stock_balance_sheet_by_report_delisted_em", "股票代码", "报告期")

    async def save_stock_profit_sheet_by_report_delisted_em(self, df: pd.DataFrame) -> int:
        """保存退市公司利润表数据 (需求179)"""
        return await self._save_with_code_and_date_key(df, "stock_profit_sheet_by_report_delisted_em", "股票代码", "报告期")

    async def save_stock_cash_flow_sheet_by_report_delisted_em(self, df: pd.DataFrame) -> int:
        """保存退市公司现金流量表数据 (需求180)"""
        return await self._save_with_code_and_date_key(df, "stock_cash_flow_sheet_by_report_delisted_em", "股票代码", "报告期")

    async def save_stock_financial_hk_report_em(self, df: pd.DataFrame) -> int:
        """保存港股财务报告数据 (需求181)"""
        return await self._save_with_code_and_date_key(df, "stock_financial_hk_report_em", "股票代码", "报告期")

    async def save_stock_financial_us_report_em(self, df: pd.DataFrame) -> int:
        """保存美股财务报告数据 (需求182)"""
        return await self._save_with_code_and_date_key(df, "stock_financial_us_report_em", "股票代码", "报告期")

    async def save_stock_financial_abstract(self, df: pd.DataFrame) -> int:
        """保存财务摘要数据 (需求183)"""
        return await self._save_with_code_and_date_key(df, "stock_financial_abstract", "股票代码", "报告期")

    async def save_stock_financial_abstract_ths(self, df: pd.DataFrame) -> int:
        """保存财务摘要数据-同花顺 (需求184)"""
        return await self._save_with_code_and_date_key(df, "stock_financial_abstract_ths", "股票代码", "报告期")

    async def save_stock_financial_analysis_indicator_em(self, df: pd.DataFrame) -> int:
        """保存财务分析指标数据 (需求185)"""
        return await self._save_with_code_and_date_key(df, "stock_financial_analysis_indicator_em", "股票代码", "报告期")

    async def save_stock_financial_analysis_indicator(self, df: pd.DataFrame) -> int:
        """保存财务分析指标数据-新浪 (需求186)"""
        return await self._save_with_code_key(df, "stock_financial_analysis_indicator", "股票代码")

    async def save_stock_financial_hk_analysis_indicator_em(self, df: pd.DataFrame) -> int:
        """保存港股财务分析指标数据 (需求187)"""
        return await self._save_with_code_and_date_key(df, "stock_financial_hk_analysis_indicator_em", "股票代码", "报告期")

    async def save_stock_financial_us_analysis_indicator_em(self, df: pd.DataFrame) -> int:
        """保存美股财务分析指标数据 (需求188)"""
        return await self._save_with_code_and_date_key(df, "stock_financial_us_analysis_indicator_em", "股票代码", "报告期")

    async def save_stock_history_dividend(self, df: pd.DataFrame) -> int:
        """保存历史分红数据 (需求189)"""
        return await self._save_with_code_and_date_key(df, "stock_history_dividend", "股票代码", "除权除息日")

    async def save_stock_gdfx_free_top_10_em(self, df: pd.DataFrame) -> int:
        """保存前10大流通股东数据 (需求190)"""
        return await self._save_with_datetime_key(df, "stock_gdfx_free_top_10_em", ["股票代码", "报告期", "序号"])

    async def save_stock_gdfx_top_10_em(self, df: pd.DataFrame) -> int:
        """保存前10大股东数据 (需求191)"""
        return await self._save_with_datetime_key(df, "stock_gdfx_top_10_em", ["股票代码", "报告期", "序号"])

    async def save_stock_gdfx_free_holding_change_em(self, df: pd.DataFrame) -> int:
        """保存流通股东持股变化数据 (需求192)"""
        return await self._save_with_datetime_key(df, "stock_gdfx_free_holding_change_em", ["股票代码", "股东名称", "报告日期"])

    async def save_stock_gdfx_holding_change_em(self, df: pd.DataFrame) -> int:
        """保存股东持股变化数据 (需求193)"""
        return await self._save_with_datetime_key(df, "stock_gdfx_holding_change_em", ["股票代码", "股东名称", "报告日期"])

    async def save_stock_management_change_ths(self, df: pd.DataFrame) -> int:
        """保存高管变动数据 (需求194)"""
        return await self._save_with_datetime_key(df, "stock_management_change_ths", ["股票代码", "公告日期", "姓名"])

    async def save_stock_shareholder_change_ths(self, df: pd.DataFrame) -> int:
        """保存股东变动数据 (需求195)"""
        return await self._save_with_datetime_key(df, "stock_shareholder_change_ths", ["股票代码", "公告日期", "股东名称"])

    async def save_stock_gdfx_free_holding_analyse_em(self, df: pd.DataFrame) -> int:
        """保存流通股东持股分析数据 (需求196)"""
        return await self._save_with_code_and_date_key(df, "stock_gdfx_free_holding_analyse_em", "股票代码", "报告日期")

    async def save_stock_gdfx_holding_analyse_em(self, df: pd.DataFrame) -> int:
        """保存股东持股分析数据 (需求197)"""
        return await self._save_with_code_and_date_key(df, "stock_gdfx_holding_analyse_em", "股票代码", "报告日期")

    async def save_stock_gdfx_free_holding_detail_em(self, df: pd.DataFrame) -> int:
        """保存流通股东持股明细数据 (需求198)"""
        return await self._save_with_datetime_key(df, "stock_gdfx_free_holding_detail_em", ["股票代码", "报告期", "股东名称"])

    async def save_stock_gdfx_holding_detail_em(self, df: pd.DataFrame) -> int:
        """保存股东持股明细数据 (需求199)"""
        return await self._save_with_datetime_key(df, "stock_gdfx_holding_detail_em", ["股票代码", "报告期", "股东名称"])

    async def save_stock_history_dividend_detail(self, df: pd.DataFrame) -> int:
        """保存历史分红详细数据 (需求200)"""
        return await self._save_with_code_and_date_key(df, "stock_history_dividend_detail", "股票代码", "公告日期")

    # 通用保存方法
    async def _save_with_date_key(self, df: pd.DataFrame, collection_name: str, date_field: str) -> int:
        """使用日期作为唯一键保存数据"""
        try:
            if df is None or df.empty:
                logger.warning(f"{collection_name}数据为空，跳过保存")
                return 0
            
            db = get_mongo_db()
            collection = db[collection_name]
            records = df.to_dict('records')
            
            operations = []
            for record in records:
                filter_dict = {date_field: record.get(date_field)}
                operations.append(UpdateOne(filter_dict, {"$set": record}, upsert=True))
            
            if operations:
                result = await collection.bulk_write(operations)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存{collection_name}数据: 共 {saved_count} 条")
                return saved_count
            return 0
        except Exception as e:
            logger.error(f"❌ 保存{collection_name}数据失败: {e}")
            raise

    async def _save_with_code_key(self, df: pd.DataFrame, collection_name: str, code_field: str) -> int:
        """使用代码作为唯一键保存数据"""
        try:
            if df is None or df.empty:
                logger.warning(f"{collection_name}数据为空，跳过保存")
                return 0
            
            db = get_mongo_db()
            collection = db[collection_name]
            records = df.to_dict('records')
            
            operations = []
            for record in records:
                filter_dict = {code_field: record.get(code_field)}
                operations.append(UpdateOne(filter_dict, {"$set": record}, upsert=True))
            
            if operations:
                result = await collection.bulk_write(operations)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存{collection_name}数据: 共 {saved_count} 条")
                return saved_count
            return 0
        except Exception as e:
            logger.error(f"❌ 保存{collection_name}数据失败: {e}")
            raise

    async def _save_with_code_and_date_key(self, df: pd.DataFrame, collection_name: str, code_field: str, date_field: str) -> int:
        """使用代码和日期组合作为唯一键保存数据"""
        try:
            if df is None or df.empty:
                logger.warning(f"{collection_name}数据为空，跳过保存")
                return 0
            
            db = get_mongo_db()
            collection = db[collection_name]
            records = df.to_dict('records')
            
            operations = []
            for record in records:
                filter_dict = {
                    code_field: record.get(code_field),
                    date_field: record.get(date_field)
                }
                operations.append(UpdateOne(filter_dict, {"$set": record}, upsert=True))
            
            if operations:
                result = await collection.bulk_write(operations)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存{collection_name}数据: 共 {saved_count} 条")
                return saved_count
            return 0
        except Exception as e:
            logger.error(f"❌ 保存{collection_name}数据失败: {e}")
            raise

    async def _save_with_datetime_key(self, df: pd.DataFrame, collection_name: str, key_fields: list) -> int:
        """使用多个字段组合作为唯一键保存数据"""
        try:
            if df is None or df.empty:
                logger.warning(f"{collection_name}数据为空，跳过保存")
                return 0
            
            db = get_mongo_db()
            collection = db[collection_name]
            records = df.to_dict('records')
            
            operations = []
            for record in records:
                filter_dict = {field: record.get(field) for field in key_fields}
                operations.append(UpdateOne(filter_dict, {"$set": record}, upsert=True))
            
            if operations:
                result = await collection.bulk_write(operations)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存{collection_name}数据: 共 {saved_count} 条")
                return saved_count
            return 0
        except Exception as e:
            logger.error(f"❌ 保存{collection_name}数据失败: {e}")
            raise

    async def _save_with_seq_key(self, df: pd.DataFrame, collection_name: str, seq_field: str) -> int:
        """使用序号作为唯一键保存数据"""
        try:
            if df is None or df.empty:
                logger.warning(f"{collection_name}数据为空，跳过保存")
                return 0
            
            db = get_mongo_db()
            collection = db[collection_name]
            records = df.to_dict('records')
            
            operations = []
            for record in records:
                filter_dict = {seq_field: record.get(seq_field)}
                operations.append(UpdateOne(filter_dict, {"$set": record}, upsert=True))
            
            if operations:
                result = await collection.bulk_write(operations)
                saved_count = result.upserted_count + result.modified_count
                logger.info(f"✅ 保存{collection_name}数据: 共 {saved_count} 条")
                return saved_count
            return 0
        except Exception as e:
            logger.error(f"❌ 保存{collection_name}数据失败: {e}")
            raise

    async def import_data_from_file(self, collection_name: str, content: bytes, filename: str) -> Dict[str, Any]:
        """从文件导入数据到股票集合"""
        import io
        try:
            # 读取文件内容
            if filename.endswith('.csv'):
                df = pd.read_csv(io.BytesIO(content))
            else:
                df = pd.read_excel(io.BytesIO(content))
            
            if df.empty:
                return {"imported_count": 0, "message": "文件为空"}
            
            # 直接批量插入数据到指定集合
            db = get_mongo_db()
            collection = db[collection_name]
            records = df.to_dict('records')
            
            # 尝试批量插入（使用 upsert 避免重复）
            operations = []
            for record in records:
                # 尝试使用常见的唯一键字段
                filter_dict = {}
                if 'code' in record:
                    filter_dict['code'] = record['code']
                elif 'symbol' in record:
                    filter_dict['symbol'] = record['symbol']
                elif '代码' in record:
                    filter_dict['代码'] = record['代码']
                elif '序号' in record:
                    filter_dict['序号'] = record['序号']
                
                # 如果有日期字段，也加入过滤条件
                date_fields = ['trade_date', 'date', 'datetime', '日期', '交易日期']
                for date_field in date_fields:
                    if date_field in record:
                        filter_dict[date_field] = record[date_field]
                        break
                
                if filter_dict:
                    operations.append(UpdateOne(filter_dict, {"$set": record}, upsert=True))
                else:
                    # 如果没有唯一键，直接插入
                    operations.append(UpdateOne({"_temp_id": str(uuid.uuid4())}, {"$set": record}, upsert=True))
            
            if operations:
                result = await collection.bulk_write(operations)
                count = result.upserted_count + result.modified_count
                logger.info(f"✅ 导入{collection_name}数据: 共 {count} 条")
                return {"imported_count": count, "message": f"成功导入 {count} 条数据"}
            
            return {"imported_count": 0, "message": "无数据导入"}
            
        except Exception as e:
            logger.error(f"导入文件失败: {e}", exc_info=True)
            raise

    async def sync_data_from_remote(self, collection_name: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """从远程数据库同步数据到股票集合"""
        from motor.motor_asyncio import AsyncIOMotorClient
        try:
            host = config.get('host')
            port = int(config.get('port', 27017))
            username = config.get('username')
            password = config.get('password')
            auth_source = config.get('authSource', 'admin')
            remote_db_name = config.get('database', 'tradingagents') 
            remote_col_name = config.get('collection', collection_name)
            batch_size = int(config.get('batch_size', 1000))
            
            if username and password:
                uri = f"mongodb://{username}:{password}@{host}:{port}/{auth_source}"
            else:
                uri = f"mongodb://{host}:{port}"
            
            # 连接远程数据库
            remote_client = AsyncIOMotorClient(uri)
            remote_db = remote_client[remote_db_name]
            remote_collection = remote_db[remote_col_name]
            
            # 获取本地数据库
            local_db = get_mongo_db()
            local_collection = local_db[collection_name]
            
            # 统计信息
            total_synced = 0
            total_count = await remote_collection.count_documents({})
            
            logger.info(f"开始同步 {collection_name}，远程数据总数: {total_count}")
            
            # 分批同步
            cursor = remote_collection.find({})
            batch = []
            
            async for doc in cursor:
                # 移除 _id 字段，让本地数据库自动生成
                if '_id' in doc:
                    del doc['_id']
                batch.append(doc)
                
                if len(batch) >= batch_size:
                    # 批量插入
                    if batch:
                        operations = []
                        for record in batch:
                            # 尝试使用常见的唯一键字段
                            filter_dict = {}
                            if 'code' in record:
                                filter_dict['code'] = record['code']
                            elif 'symbol' in record:
                                filter_dict['symbol'] = record['symbol']
                            elif '代码' in record:
                                filter_dict['代码'] = record['代码']
                            elif '序号' in record:
                                filter_dict['序号'] = record['序号']
                            
                            # 如果有日期字段，也加入过滤条件
                            date_fields = ['trade_date', 'date', 'datetime', '日期', '交易日期']
                            for date_field in date_fields:
                                if date_field in record:
                                    filter_dict[date_field] = record[date_field]
                                    break
                            
                            if filter_dict:
                                operations.append(UpdateOne(filter_dict, {"$set": record}, upsert=True))
                        
                        if operations:
                            result = await local_collection.bulk_write(operations)
                            total_synced += result.upserted_count + result.modified_count
                        
                        logger.info(f"同步进度: {total_synced}/{total_count}")
                    batch = []
            
            # 处理最后一批
            if batch:
                operations = []
                for record in batch:
                    filter_dict = {}
                    if 'code' in record:
                        filter_dict['code'] = record['code']
                    elif 'symbol' in record:
                        filter_dict['symbol'] = record['symbol']
                    elif '代码' in record:
                        filter_dict['代码'] = record['代码']
                    elif '序号' in record:
                        filter_dict['序号'] = record['序号']
                    
                    date_fields = ['trade_date', 'date', 'datetime', '日期', '交易日期']
                    for date_field in date_fields:
                        if date_field in record:
                            filter_dict[date_field] = record[date_field]
                            break
                    
                    if filter_dict:
                        operations.append(UpdateOne(filter_dict, {"$set": record}, upsert=True))
                
                if operations:
                    result = await local_collection.bulk_write(operations)
                    total_synced += result.upserted_count + result.modified_count
            
            # 关闭远程连接
            remote_client.close()
            
            logger.info(f"✅ 同步完成: {collection_name}，共 {total_synced} 条")
            return {
                "synced_count": total_synced,
                "total_count": total_count,
                "message": f"成功同步 {total_synced} 条数据"
            }
            
        except Exception as e:
            logger.error(f"远程同步失败: {e}", exc_info=True)
            raise


# 全局服务实例
_stock_data_service = None

def get_stock_data_service() -> StockDataService:
    """获取股票数据服务实例"""
    global _stock_data_service
    if _stock_data_service is None:
        _stock_data_service = StockDataService()
    return _stock_data_service
