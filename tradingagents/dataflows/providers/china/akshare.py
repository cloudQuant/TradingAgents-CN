"""
AKShare统一数据提供器
基于AKShare SDK的统一数据同步方案，提供标准化的数据接口
"""
import asyncio
import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, List, Optional, Union
import pandas as pd

from ..base_provider import BaseStockDataProvider

logger = logging.getLogger(__name__)


class AKShareProvider(BaseStockDataProvider):
    """
    AKShare统一数据提供器
    
    提供标准化的股票数据接口，支持：
    - 股票基础信息获取
    - 历史行情数据
    - 实时行情数据
    - 财务数据
    - 港股数据支持
    """
    
    def __init__(self):
        super().__init__("AKShare")
        self.ak = None
        self.connected = False
        self._stock_list_cache = None  # 缓存股票列表，避免重复获取
        self._cache_time = None  # 缓存时间
        self._initialize_akshare()
    
    def _initialize_akshare(self):
        """初始化AKShare连接"""
        try:
            import akshare as ak
            self.ak = ak
            self.connected = True
            
            # 配置超时和重试
            self._configure_timeout()
            
            logger.info("✅ AKShare连接成功")
        except ImportError as e:
            logger.error(f"❌ AKShare未安装: {e}")
            self.connected = False
        except Exception as e:
            logger.error(f"❌ AKShare初始化失败: {e}")
            self.connected = False
    
    def _configure_timeout(self):
        """配置AKShare的超时设置"""
        try:
            import socket
            socket.setdefaulttimeout(60)  # 60秒超时
            logger.info("🔧 AKShare超时配置完成: 60秒")
        except Exception as e:
            logger.warning(f"⚠️ AKShare超时配置失败: {e}")
    
    async def connect(self) -> bool:
        """连接到AKShare数据源"""
        return await self.test_connection()

    async def test_connection(self) -> bool:
        """测试AKShare连接"""
        if not self.connected:
            return False
        
        try:
            # 测试获取股票列表
            await asyncio.to_thread(self.ak.stock_info_a_code_name)
            logger.info("✅ AKShare连接测试成功")
            return True
        except Exception as e:
            logger.error(f"❌ AKShare连接测试失败: {e}")
            return False
    
    def get_stock_list_sync(self) -> Optional[pd.DataFrame]:
        """获取股票列表（同步版本）"""
        if not self.connected:
            return None

        try:
            logger.info("📋 获取AKShare股票列表（同步）...")
            stock_df = self.ak.stock_info_a_code_name()

            if stock_df is None or stock_df.empty:
                logger.warning("⚠️ AKShare股票列表为空")
                return None

            logger.info(f"✅ AKShare股票列表获取成功: {len(stock_df)}只股票")
            return stock_df

        except Exception as e:
            logger.error(f"❌ AKShare获取股票列表失败: {e}")
            return None

    async def get_stock_list(self) -> List[Dict[str, Any]]:
        """
        获取股票列表

        Returns:
            股票列表，包含代码和名称
        """
        if not self.connected:
            return []

        try:
            logger.info("📋 获取AKShare股票列表...")

            # 使用线程池异步获取股票列表，添加超时保护
            def fetch_stock_list():
                return self.ak.stock_info_a_code_name()

            stock_df = await asyncio.to_thread(fetch_stock_list)

            if stock_df is None or stock_df.empty:
                logger.warning("⚠️ AKShare股票列表为空")
                return []

            # 转换为标准格式
            stock_list = []
            for _, row in stock_df.iterrows():
                stock_list.append({
                    "code": str(row.get("code", "")),
                    "name": str(row.get("name", "")),
                    "source": "akshare"
                })

            logger.info(f"✅ AKShare股票列表获取成功: {len(stock_list)}只股票")
            return stock_list

        except Exception as e:
            logger.error(f"❌ AKShare获取股票列表失败: {e}")
            return []
    
    async def get_stock_basic_info(self, code: str) -> Optional[Dict[str, Any]]:
        """
        获取股票基础信息
        
        Args:
            code: 股票代码
            
        Returns:
            标准化的股票基础信息
        """
        if not self.connected:
            return None
        
        try:
            logger.debug(f"📊 获取{code}基础信息...")
            
            # 获取股票基本信息
            stock_info = await self._get_stock_info_detail(code)
            
            if not stock_info:
                logger.warning(f"⚠️ 未找到{code}的基础信息")
                return None
            
            # 转换为标准化字典
            basic_info = {
                "code": code,
                "name": stock_info.get("name", f"股票{code}"),
                "area": stock_info.get("area", "未知"),
                "industry": stock_info.get("industry", "未知"),
                "market": self._determine_market(code),
                "list_date": stock_info.get("list_date", ""),
                # 扩展字段
                "full_symbol": self._get_full_symbol(code),
                "market_info": self._get_market_info(code),
                "data_source": "akshare",
                "last_sync": datetime.now(timezone.utc),
                "sync_status": "success"
            }
            
            logger.debug(f"✅ {code}基础信息获取成功")
            return basic_info
            
        except Exception as e:
            logger.error(f"❌ 获取{code}基础信息失败: {e}")
            return None
    
    async def _get_stock_list_cached(self):
        """获取缓存的股票列表（避免重复获取）"""
        from datetime import datetime, timedelta

        # 如果缓存存在且未过期（1小时），直接返回
        if self._stock_list_cache is not None and self._cache_time is not None:
            if datetime.now() - self._cache_time < timedelta(hours=1):
                return self._stock_list_cache

        # 否则重新获取
        def fetch_stock_list():
            return self.ak.stock_info_a_code_name()

        try:
            stock_list = await asyncio.to_thread(fetch_stock_list)
            if stock_list is not None and not stock_list.empty:
                self._stock_list_cache = stock_list
                self._cache_time = datetime.now()
                logger.info(f"✅ 股票列表缓存更新: {len(stock_list)} 只股票")
                return stock_list
        except Exception as e:
            logger.error(f"❌ 获取股票列表失败: {e}")

        return None

    async def _get_stock_info_detail(self, code: str) -> Dict[str, Any]:
        """获取股票详细信息"""
        try:
            # 方法1: 尝试获取个股详细信息（包含行业、地区等详细信息）
            def fetch_individual_info():
                s = str(code).strip()
                if s.startswith('6'):
                    ak_sym = f"sh{s}"
                elif s.startswith(('0', '3', '2')):
                    ak_sym = f"sz{s}"
                elif s.startswith(('8', '4')):
                    ak_sym = f"bj{s}"
                else:
                    ak_sym = s
                return self.ak.stock_individual_info_em(symbol=ak_sym)

            try:
                stock_info = await asyncio.to_thread(fetch_individual_info)

                if stock_info is not None and not stock_info.empty:
                    # 解析信息
                    info = {"code": code}

                    # 提取股票名称
                    name_row = stock_info[stock_info['item'] == '股票简称']
                    if not name_row.empty:
                        info['name'] = str(name_row['value'].iloc[0])

                    # 提取行业信息
                    industry_row = stock_info[stock_info['item'] == '所属行业']
                    if not industry_row.empty:
                        info['industry'] = str(industry_row['value'].iloc[0])

                    # 提取地区信息
                    area_row = stock_info[stock_info['item'] == '所属地区']
                    if not area_row.empty:
                        info['area'] = str(area_row['value'].iloc[0])

                    # 提取上市日期
                    list_date_row = stock_info[stock_info['item'] == '上市时间']
                    if not list_date_row.empty:
                        info['list_date'] = str(list_date_row['value'].iloc[0])

                    return info
            except Exception as e:
                logger.debug(f"获取{code}个股详细信息失败: {e}")

            # 方法2: 从缓存的股票列表中获取基本信息（只有代码和名称）
            try:
                stock_list = await self._get_stock_list_cached()
                if stock_list is not None and not stock_list.empty:
                    stock_row = stock_list[stock_list['code'] == code]
                    if not stock_row.empty:
                        return {
                            "code": code,
                            "name": str(stock_row['name'].iloc[0]),
                            "industry": "未知",
                            "area": "未知"
                        }
            except Exception as e:
                logger.debug(f"从股票列表获取{code}信息失败: {e}")

            # 如果都失败，返回基本信息
            return {"code": code, "name": f"股票{code}", "industry": "未知", "area": "未知"}

        except Exception as e:
            logger.debug(f"获取{code}详细信息失败: {e}")
            return {"code": code, "name": f"股票{code}", "industry": "未知", "area": "未知"}
    
    def _determine_market(self, code: str) -> str:
        """根据股票代码判断市场"""
        if code.startswith(('60', '68')):
            return "上海证券交易所"
        elif code.startswith(('00', '30')):
            return "深圳证券交易所"
        elif code.startswith('8'):
            return "北京证券交易所"
        else:
            return "未知市场"
    
    def _get_full_symbol(self, code: str) -> str:
        """
        获取完整股票代码

        Args:
            code: 6位股票代码

        Returns:
            完整标准化代码，如果无法识别则返回原始代码（确保不为空）
        """
        # 确保 code 不为空
        if not code:
            return ""

        # 标准化为字符串
        code = str(code).strip()

        # 根据代码前缀判断交易所
        if code.startswith(('60', '68', '90')):  # 上海证券交易所（增加90开头的B股）
            return f"{code}.SS"
        elif code.startswith(('00', '30', '20')):  # 深圳证券交易所（增加20开头的B股）
            return f"{code}.SZ"
        elif code.startswith(('8', '4')):  # 北京证券交易所（增加4开头的新三板）
            return f"{code}.BJ"
        else:
            # 无法识别的代码，返回原始代码（确保不为空）
            return code if code else ""
    
    def _get_market_info(self, code: str) -> Dict[str, Any]:
        """获取市场信息"""
        if code.startswith(('60', '68')):
            return {
                "market_type": "CN",
                "exchange": "SSE",
                "exchange_name": "上海证券交易所",
                "currency": "CNY",
                "timezone": "Asia/Shanghai"
            }
        elif code.startswith(('00', '30')):
            return {
                "market_type": "CN",
                "exchange": "SZSE", 
                "exchange_name": "深圳证券交易所",
                "currency": "CNY",
                "timezone": "Asia/Shanghai"
            }
        elif code.startswith('8'):
            return {
                "market_type": "CN",
                "exchange": "BSE",
                "exchange_name": "北京证券交易所", 
                "currency": "CNY",
                "timezone": "Asia/Shanghai"
            }
        else:
            return {
                "market_type": "CN",
                "exchange": "UNKNOWN",
                "exchange_name": "未知交易所",
                "currency": "CNY",
                "timezone": "Asia/Shanghai"
            }
    
    async def get_batch_stock_quotes(self, codes: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        批量获取股票实时行情（优化版：一次获取全市场快照）

        优先使用新浪财经接口（更稳定），失败时回退到东方财富接口

        Args:
            codes: 股票代码列表

        Returns:
            股票代码到行情数据的映射字典
        """
        if not self.connected:
            return {}

        # 重试逻辑
        max_retries = 2
        retry_delay = 1  # 秒

        for attempt in range(max_retries):
            try:
                logger.debug(f"📊 批量获取 {len(codes)} 只股票的实时行情... (尝试 {attempt + 1}/{max_retries})")

                # 优先使用新浪财经接口（更稳定，不容易被封）
                def fetch_spot_data_sina():
                    import time
                    time.sleep(0.3)  # 添加延迟避免频率限制
                    return self.ak.stock_zh_a_spot()

                try:
                    spot_df = await asyncio.to_thread(fetch_spot_data_sina)
                    data_source = "sina"
                    logger.debug("✅ 使用新浪财经接口获取数据")
                except Exception as e:
                    logger.warning(f"⚠️ 新浪财经接口失败: {e}，尝试东方财富接口...")
                    # 回退到东方财富接口
                    def fetch_spot_data_em():
                        import time
                        time.sleep(0.5)
                        return self.ak.stock_zh_a_spot_em()
                    spot_df = await asyncio.to_thread(fetch_spot_data_em)
                    data_source = "eastmoney"
                    logger.debug("✅ 使用东方财富接口获取数据")

                if spot_df is None or spot_df.empty:
                    logger.warning("⚠️ 全市场快照为空")
                    if attempt < max_retries - 1:
                        await asyncio.sleep(retry_delay)
                        continue
                    return {}

                # 构建代码到行情的映射
                quotes_map = {}
                codes_set = set(codes)

                # 构建代码映射表（支持带前缀的代码匹配）
                # 例如：sh600000 -> 600000, sz000001 -> 000001
                code_mapping = {}
                for code in codes:
                    code_mapping[code] = code  # 原始代码
                    # 添加可能的前缀变体
                    for prefix in ['sh', 'sz', 'bj']:
                        code_mapping[f"{prefix}{code}"] = code

                for _, row in spot_df.iterrows():
                    raw_code = str(row.get("代码", ""))

                    # 尝试匹配代码（支持带前缀和不带前缀）
                    matched_code = None
                    if raw_code in code_mapping:
                        matched_code = code_mapping[raw_code]
                    elif raw_code in codes_set:
                        matched_code = raw_code

                    if matched_code:
                        quotes_data = {
                            "name": str(row.get("名称", f"股票{matched_code}")),
                            "price": self._safe_float(row.get("最新价", 0)),
                            "change": self._safe_float(row.get("涨跌额", 0)),
                            "change_percent": self._safe_float(row.get("涨跌幅", 0)),
                            "volume": self._safe_int(row.get("成交量", 0)),
                            "amount": self._safe_float(row.get("成交额", 0)),
                            "open": self._safe_float(row.get("今开", 0)),
                            "high": self._safe_float(row.get("最高", 0)),
                            "low": self._safe_float(row.get("最低", 0)),
                            "pre_close": self._safe_float(row.get("昨收", 0)),
                            # 🔥 新增：财务指标字段
                            "turnover_rate": self._safe_float(row.get("换手率", None)),  # 换手率（%）
                            "volume_ratio": self._safe_float(row.get("量比", None)),  # 量比
                            "pe": self._safe_float(row.get("市盈率-动态", None)),  # 动态市盈率
                            "pb": self._safe_float(row.get("市净率", None)),  # 市净率
                            "total_mv": self._safe_float(row.get("总市值", None)),  # 总市值（元）
                            "circ_mv": self._safe_float(row.get("流通市值", None)),  # 流通市值（元）
                        }

                        # 转换为标准化字典（使用匹配后的代码）
                        quotes_map[matched_code] = {
                            "code": matched_code,
                            "symbol": matched_code,
                            "name": quotes_data.get("name", f"股票{matched_code}"),
                            "price": float(quotes_data.get("price", 0)),
                            "change": float(quotes_data.get("change", 0)),
                            "change_percent": float(quotes_data.get("change_percent", 0)),
                            "volume": int(quotes_data.get("volume", 0)),
                            "amount": float(quotes_data.get("amount", 0)),
                            "open_price": float(quotes_data.get("open", 0)),
                            "high_price": float(quotes_data.get("high", 0)),
                            "low_price": float(quotes_data.get("low", 0)),
                            "pre_close": float(quotes_data.get("pre_close", 0)),
                            # 🔥 新增：财务指标字段
                            "turnover_rate": quotes_data.get("turnover_rate"),  # 换手率（%）
                            "volume_ratio": quotes_data.get("volume_ratio"),  # 量比
                            "pe": quotes_data.get("pe"),  # 动态市盈率
                            "pe_ttm": quotes_data.get("pe"),  # TTM市盈率（与动态市盈率相同）
                            "pb": quotes_data.get("pb"),  # 市净率
                            "total_mv": quotes_data.get("total_mv") / 1e8 if quotes_data.get("total_mv") else None,  # 总市值（转换为亿元）
                            "circ_mv": quotes_data.get("circ_mv") / 1e8 if quotes_data.get("circ_mv") else None,  # 流通市值（转换为亿元）
                            # 扩展字段
                            "full_symbol": self._get_full_symbol(matched_code),
                            "market_info": self._get_market_info(matched_code),
                            "data_source": "akshare",
                            "last_sync": datetime.now(timezone.utc),
                            "sync_status": "success"
                        }

                found_count = len(quotes_map)
                missing_count = len(codes) - found_count
                logger.debug(f"✅ 批量获取完成: 找到 {found_count} 只, 未找到 {missing_count} 只")

                # 记录未找到的股票
                if missing_count > 0:
                    missing_codes = codes_set - set(quotes_map.keys())
                    if missing_count <= 10:
                        logger.debug(f"⚠️ 未找到行情的股票: {list(missing_codes)}")
                    else:
                        logger.debug(f"⚠️ 未找到行情的股票: {list(missing_codes)[:10]}... (共{missing_count}只)")

                return quotes_map

            except Exception as e:
                logger.warning(f"⚠️ 批量获取实时行情失败 (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(retry_delay)
                else:
                    logger.error(f"❌ 批量获取实时行情失败，已达最大重试次数: {e}")
                    return {}

    async def get_stock_quotes(self, code: str) -> Optional[Dict[str, Any]]:
        """
        获取单个股票实时行情

        🔥 策略：使用 stock_bid_ask_em 接口获取单个股票的实时行情报价
        - 优点：只获取单个股票数据，速度快，不浪费资源
        - 适用场景：手动同步单个股票

        Args:
            code: 股票代码

        Returns:
            标准化的行情数据
        """
        if not self.connected:
            return None

        try:
            logger.info(f"📈 使用 stock_bid_ask_em 接口获取 {code} 实时行情...")

            # 🔥 使用 stock_bid_ask_em 接口获取单个股票实时行情
            def fetch_bid_ask():
                return self.ak.stock_bid_ask_em(symbol=code)

            bid_ask_df = await asyncio.to_thread(fetch_bid_ask)

            # 🔥 打印原始返回数据
            logger.info(f"📊 stock_bid_ask_em 返回数据类型: {type(bid_ask_df)}")
            if bid_ask_df is not None:
                logger.info(f"📊 DataFrame shape: {bid_ask_df.shape}")
                logger.info(f"📊 DataFrame columns: {list(bid_ask_df.columns)}")
                logger.info(f"📊 DataFrame 完整数据:\n{bid_ask_df.to_string()}")

            if bid_ask_df is None or bid_ask_df.empty:
                logger.warning(f"⚠️ 未找到{code}的行情数据")
                return None

            # 将 DataFrame 转换为字典
            data_dict = dict(zip(bid_ask_df['item'], bid_ask_df['value']))
            logger.info(f"📊 转换后的字典: {data_dict}")

            # 转换为标准化字典
            # 🔥 注意：字段名必须与 app/routers/stocks.py 中的查询字段一致
            # 前端查询使用的是 high/low/open，不是 high_price/low_price/open_price

            # 🔥 获取当前日期（UTC+8）
            from datetime import datetime, timezone, timedelta
            cn_tz = timezone(timedelta(hours=8))
            now_cn = datetime.now(cn_tz)
            trade_date = now_cn.strftime("%Y-%m-%d")  # 格式：2025-11-05

            # 🔥 成交量单位转换：手 → 股（1手 = 100股）
            volume_in_lots = int(data_dict.get("总手", 0))  # 单位：手
            volume_in_shares = volume_in_lots * 100  # 单位：股

            quotes = {
                "code": code,
                "symbol": code,
                "name": f"股票{code}",  # stock_bid_ask_em 不返回股票名称
                "price": float(data_dict.get("最新", 0)),
                "close": float(data_dict.get("最新", 0)),  # 🔥 close 字段（与 price 相同）
                "current_price": float(data_dict.get("最新", 0)),  # 🔥 current_price 字段（兼容旧数据）
                "change": float(data_dict.get("涨跌", 0)),
                "change_percent": float(data_dict.get("涨幅", 0)),
                "pct_chg": float(data_dict.get("涨幅", 0)),  # 🔥 pct_chg 字段（兼容旧数据）
                "volume": volume_in_shares,  # 🔥 单位：股（已转换）
                "amount": float(data_dict.get("金额", 0)),  # 单位：元
                "open": float(data_dict.get("今开", 0)),  # 🔥 使用 open 而不是 open_price
                "high": float(data_dict.get("最高", 0)),  # 🔥 使用 high 而不是 high_price
                "low": float(data_dict.get("最低", 0)),  # 🔥 使用 low 而不是 low_price
                "pre_close": float(data_dict.get("昨收", 0)),
                # 🔥 新增：财务指标字段
                "turnover_rate": float(data_dict.get("换手", 0)),  # 换手率（%）
                "volume_ratio": float(data_dict.get("量比", 0)),  # 量比
                "pe": None,  # stock_bid_ask_em 不返回市盈率
                "pe_ttm": None,
                "pb": None,  # stock_bid_ask_em 不返回市净率
                "total_mv": None,  # stock_bid_ask_em 不返回总市值
                "circ_mv": None,  # stock_bid_ask_em 不返回流通市值
                # 🔥 新增：交易日期和更新时间
                "trade_date": trade_date,  # 交易日期（格式：2025-11-05）
                "updated_at": now_cn.isoformat(),  # 更新时间（ISO格式，带时区）
                # 扩展字段
                "full_symbol": self._get_full_symbol(code),
                "market_info": self._get_market_info(code),
                "data_source": "akshare",
                "last_sync": datetime.now(timezone.utc),
                "sync_status": "success"
            }

            logger.info(f"✅ {code} 实时行情获取成功: 最新价={quotes['price']}, 涨跌幅={quotes['change_percent']}%, 成交量={quotes['volume']}, 成交额={quotes['amount']}")
            return quotes

        except Exception as e:
            logger.error(f"❌ 获取{code}实时行情失败: {e}", exc_info=True)
            return None
    
    async def _get_realtime_quotes_data(self, code: str) -> Dict[str, Any]:
        """获取实时行情数据"""
        try:
            # 方法1: 获取A股实时行情
            def fetch_spot_data():
                return self.ak.stock_zh_a_spot_em()

            try:
                spot_df = await asyncio.to_thread(fetch_spot_data)

                if spot_df is not None and not spot_df.empty:
                    # 查找对应股票
                    stock_data = spot_df[spot_df['代码'] == code]

                    if not stock_data.empty:
                        row = stock_data.iloc[0]

                        # 解析行情数据
                        return {
                            "name": str(row.get("名称", f"股票{code}")),
                            "price": self._safe_float(row.get("最新价", 0)),
                            "change": self._safe_float(row.get("涨跌额", 0)),
                            "change_percent": self._safe_float(row.get("涨跌幅", 0)),
                            "volume": self._safe_int(row.get("成交量", 0)),
                            "amount": self._safe_float(row.get("成交额", 0)),
                            "open": self._safe_float(row.get("今开", 0)),
                            "high": self._safe_float(row.get("最高", 0)),
                            "low": self._safe_float(row.get("最低", 0)),
                            "pre_close": self._safe_float(row.get("昨收", 0)),
                            # 🔥 新增：财务指标字段
                            "turnover_rate": self._safe_float(row.get("换手率", None)),  # 换手率（%）
                            "volume_ratio": self._safe_float(row.get("量比", None)),  # 量比
                            "pe": self._safe_float(row.get("市盈率-动态", None)),  # 动态市盈率
                            "pb": self._safe_float(row.get("市净率", None)),  # 市净率
                            "total_mv": self._safe_float(row.get("总市值", None)),  # 总市值（元）
                            "circ_mv": self._safe_float(row.get("流通市值", None)),  # 流通市值（元）
                        }
            except Exception as e:
                logger.debug(f"获取{code}A股实时行情失败: {e}")

            # 方法2: 尝试获取单只股票实时数据
            def fetch_individual_spot():
                return self.ak.stock_zh_a_hist(symbol=code, period="daily", adjust="")

            try:
                hist_df = await asyncio.to_thread(fetch_individual_spot)
                if hist_df is not None and not hist_df.empty:
                    # 取最新一天的数据作为当前行情
                    latest_row = hist_df.iloc[-1]
                    return {
                        "name": f"股票{code}",
                        "price": self._safe_float(latest_row.get("收盘", 0)),
                        "change": 0,  # 历史数据无法计算涨跌额
                        "change_percent": self._safe_float(latest_row.get("涨跌幅", 0)),
                        "volume": self._safe_int(latest_row.get("成交量", 0)),
                        "amount": self._safe_float(latest_row.get("成交额", 0)),
                        "open": self._safe_float(latest_row.get("开盘", 0)),
                        "high": self._safe_float(latest_row.get("最高", 0)),
                        "low": self._safe_float(latest_row.get("最低", 0)),
                        "pre_close": self._safe_float(latest_row.get("收盘", 0))
                    }
            except Exception as e:
                logger.debug(f"获取{code}历史数据作为行情失败: {e}")

            return {}

        except Exception as e:
            logger.debug(f"获取{code}实时行情数据失败: {e}")
            return {}
    
    def _safe_float(self, value: Any) -> float:
        """安全转换为浮点数"""
        try:
            if pd.isna(value) or value is None:
                return 0.0
            return float(value)
        except (ValueError, TypeError):
            return 0.0
    
    def _safe_int(self, value: Any) -> int:
        """安全转换为整数"""
        try:
            if pd.isna(value) or value is None:
                return 0
            return int(float(value))
        except (ValueError, TypeError):
            return 0
    
    def _safe_str(self, value: Any) -> str:
        """安全转换为字符串"""
        try:
            if pd.isna(value) or value is None:
                return ""
            return str(value)
        except:
            return ""

    async def get_historical_data(
        self,
        code: str,
        start_date: str,
        end_date: str,
        period: str = "daily"
    ) -> Optional[pd.DataFrame]:
        """
        获取历史行情数据

        Args:
            code: 股票代码
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            period: 周期 (daily, weekly, monthly)

        Returns:
            历史行情数据DataFrame
        """
        if not self.connected:
            return None

        try:
            logger.debug(f"📊 获取{code}历史数据: {start_date} 到 {end_date}")

            # 转换周期格式
            period_map = {
                "daily": "daily",
                "weekly": "weekly",
                "monthly": "monthly"
            }
            ak_period = period_map.get(period, "daily")

            # 格式化日期
            start_date_formatted = start_date.replace('-', '')
            end_date_formatted = end_date.replace('-', '')

            # 获取历史数据
            def fetch_historical_data():
                return self.ak.stock_zh_a_hist(
                    symbol=code,
                    period=ak_period,
                    start_date=start_date_formatted,
                    end_date=end_date_formatted,
                    adjust="qfq"  # 前复权
                )

            hist_df = await asyncio.to_thread(fetch_historical_data)

            if hist_df is None or hist_df.empty:
                logger.warning(f"⚠️ {code}历史数据为空")
                return None

            # 标准化列名
            hist_df = self._standardize_historical_columns(hist_df, code)

            logger.debug(f"✅ {code}历史数据获取成功: {len(hist_df)}条记录")
            return hist_df

        except Exception as e:
            logger.error(f"❌ 获取{code}历史数据失败: {e}")
            return None

    def _standardize_historical_columns(self, df: pd.DataFrame, code: str) -> pd.DataFrame:
        """标准化历史数据列名"""
        try:
            # 标准化列名映射
            column_mapping = {
                '日期': 'date',
                '开盘': 'open',
                '收盘': 'close',
                '最高': 'high',
                '最低': 'low',
                '成交量': 'volume',
                '成交额': 'amount',
                '振幅': 'amplitude',
                '涨跌幅': 'change_percent',
                '涨跌额': 'change',
                '换手率': 'turnover'
            }

            # 重命名列
            df = df.rename(columns=column_mapping)

            # 添加标准字段
            df['code'] = code
            df['full_symbol'] = self._get_full_symbol(code)

            # 确保日期格式
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'])

            # 数据类型转换
            numeric_columns = ['open', 'close', 'high', 'low', 'volume', 'amount']
            for col in numeric_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

            return df

        except Exception as e:
            logger.error(f"标准化{code}历史数据列名失败: {e}")
            return df

    async def get_financial_data(self, code: str) -> Dict[str, Any]:
        """
        获取财务数据

        Args:
            code: 股票代码

        Returns:
            财务数据字典
        """
        if not self.connected:
            return {}

        try:
            logger.debug(f"💰 获取{code}财务数据...")

            financial_data = {}

            # 1. 获取主要财务指标
            try:
                def fetch_financial_abstract():
                    return self.ak.stock_financial_abstract(symbol=code)

                main_indicators = await asyncio.to_thread(fetch_financial_abstract)
                if main_indicators is not None and not main_indicators.empty:
                    financial_data['main_indicators'] = main_indicators.to_dict('records')
                    logger.debug(f"✅ {code}主要财务指标获取成功")
            except Exception as e:
                logger.debug(f"获取{code}主要财务指标失败: {e}")

            # 2. 获取资产负债表
            try:
                def fetch_balance_sheet():
                    return self.ak.stock_balance_sheet_by_report_em(symbol=code)

                balance_sheet = await asyncio.to_thread(fetch_balance_sheet)
                if balance_sheet is not None and not balance_sheet.empty:
                    financial_data['balance_sheet'] = balance_sheet.to_dict('records')
                    logger.debug(f"✅ {code}资产负债表获取成功")
            except Exception as e:
                logger.debug(f"获取{code}资产负债表失败: {e}")

            # 3. 获取利润表
            try:
                def fetch_income_statement():
                    return self.ak.stock_profit_sheet_by_report_em(symbol=code)

                income_statement = await asyncio.to_thread(fetch_income_statement)
                if income_statement is not None and not income_statement.empty:
                    financial_data['income_statement'] = income_statement.to_dict('records')
                    logger.debug(f"✅ {code}利润表获取成功")
            except Exception as e:
                logger.debug(f"获取{code}利润表失败: {e}")

            # 4. 获取现金流量表
            try:
                def fetch_cash_flow():
                    return self.ak.stock_cash_flow_sheet_by_report_em(symbol=code)

                cash_flow = await asyncio.to_thread(fetch_cash_flow)
                if cash_flow is not None and not cash_flow.empty:
                    financial_data['cash_flow'] = cash_flow.to_dict('records')
                    logger.debug(f"✅ {code}现金流量表获取成功")
            except Exception as e:
                logger.debug(f"获取{code}现金流量表失败: {e}")

            if financial_data:
                logger.debug(f"✅ {code}财务数据获取完成: {len(financial_data)}个数据集")
            else:
                logger.warning(f"⚠️ {code}未获取到任何财务数据")

            return financial_data

        except Exception as e:
            logger.error(f"❌ 获取{code}财务数据失败: {e}")
            return {}

    async def get_market_status(self) -> Dict[str, Any]:
        """
        获取市场状态信息

        Returns:
            市场状态信息
        """
        try:
            # AKShare没有直接的市场状态API，返回基本信息
            now = datetime.now()

            # 简单的交易时间判断
            is_trading_time = (
                now.weekday() < 5 and  # 工作日
                ((9 <= now.hour < 12) or (13 <= now.hour < 15))  # 交易时间
            )

            return {
                "market_status": "open" if is_trading_time else "closed",
                "current_time": now.isoformat(),
                "data_source": "akshare",
                "trading_day": now.weekday() < 5
            }

        except Exception as e:
            logger.error(f"❌ 获取市场状态失败: {e}")
            return {
                "market_status": "unknown",
                "current_time": datetime.now().isoformat(),
                "data_source": "akshare",
                "error": str(e)
            }

    def get_stock_news_sync(self, symbol: str = None, limit: int = 10) -> Optional[pd.DataFrame]:
        """
        获取股票新闻（同步版本，返回原始 DataFrame）

        Args:
            symbol: 股票代码，为None时获取市场新闻
            limit: 返回数量限制

        Returns:
            新闻 DataFrame 或 None
        """
        if not self.is_available():
            return None

        try:
            import akshare as ak

            if symbol:
                # 获取个股新闻
                self.logger.debug(f"📰 获取AKShare个股新闻: {symbol}")

                # 标准化股票代码
                symbol_6 = symbol.zfill(6)

                # 获取东方财富个股新闻
                try:
                    news_df = ak.stock_news_em(symbol=symbol_6)
                except Exception as e:
                    msg = str(e)
                    if "Expecting value" in msg and "line 1 column 1" in msg:
                        self.logger.warning(f"⚠️ AKShare个股新闻接口返回空/非JSON响应 symbol={symbol}: {e}")
                        return None
                    raise

                if news_df is None:
                    self.logger.warning(f"⚠️ {symbol} 未获取到AKShare新闻数据")
                    return None

                if not isinstance(news_df, pd.DataFrame) or news_df.empty:
                    self.logger.warning(f"⚠️ {symbol} 未获取到AKShare新闻数据（类型={type(news_df)}）")
                    return None

                self.logger.info(f"✅ {symbol} AKShare新闻获取成功: {len(news_df)} 条")
                return news_df.head(limit) if limit else news_df
            else:
                # 获取市场新闻
                self.logger.debug("📰 获取AKShare市场新闻")

                try:
                    news_df = ak.news_cctv()
                except Exception as e:
                    msg = str(e)
                    if "Expecting value" in msg and "line 1 column 1" in msg:
                        self.logger.warning(f"⚠️ AKShare市场新闻接口返回空/非JSON响应: {e}")
                        return None
                    raise

                if news_df is None:
                    self.logger.warning("⚠️ 未获取到AKShare市场新闻数据")
                    return None

                if not isinstance(news_df, pd.DataFrame) or news_df.empty:
                    self.logger.warning(f"⚠️ 未获取到AKShare市场新闻数据（类型={type(news_df)}）")
                    return None

                self.logger.info(f"✅ AKShare市场新闻获取成功: {len(news_df)} 条")
                return news_df.head(limit) if limit else news_df

        except Exception as e:
            self.logger.error(f"❌ AKShare新闻获取失败: {e}")
            return None

    async def get_stock_news(self, symbol: str = None, limit: int = 10) -> Optional[List[Dict[str, Any]]]:
        """
        获取股票新闻（异步版本，返回结构化列表）

        Args:
            symbol: 股票代码，为None时获取市场新闻
            limit: 返回数量限制

        Returns:
            新闻列表
        """
        if not self.is_available():
            return None

        try:
            import akshare as ak

            if symbol:
                # 获取个股新闻
                self.logger.debug(f"📰 获取AKShare个股新闻: {symbol}")

                # 标准化股票代码
                symbol_6 = symbol.zfill(6)

                # 获取东方财富个股新闻
                try:
                    news_df = await asyncio.to_thread(
                        ak.stock_news_em,
                        symbol=symbol_6
                    )
                except Exception as e:
                    msg = str(e)
                    if "Expecting value" in msg and "line 1 column 1" in msg:
                        self.logger.warning(f"⚠️ AKShare个股新闻接口返回空/非JSON响应 symbol={symbol}: {e}")
                        return []
                    raise

                if news_df is None:
                    self.logger.warning(f"⚠️ {symbol} 未获取到AKShare新闻数据")
                    return []

                if not isinstance(news_df, pd.DataFrame) or news_df.empty:
                    self.logger.warning(f"⚠️ {symbol} 未获取到AKShare新闻数据（类型={type(news_df)}）")
                    return []

                news_list = []

                for _, row in news_df.head(limit).iterrows():
                    title = str(row.get('新闻标题', '') or row.get('标题', ''))
                    content = str(row.get('新闻内容', '') or row.get('内容', ''))
                    summary = str(row.get('新闻摘要', '') or row.get('摘要', ''))

                    news_item = {
                        "symbol": symbol,
                        "title": title,
                        "content": content,
                        "summary": summary,
                        "url": str(row.get('新闻链接', '') or row.get('链接', '')),
                        "source": str(row.get('文章来源', '') or row.get('来源', '') or '东方财富'),
                        "author": str(row.get('作者', '') or ''),
                        "publish_time": self._parse_news_time(row.get('发布时间', '') or row.get('时间', '')),
                        "category": self._classify_news(content, title),
                        "sentiment": self._analyze_news_sentiment(content, title),
                        "sentiment_score": self._calculate_sentiment_score(content, title),
                        "keywords": self._extract_keywords(content, title),
                        "importance": self._assess_news_importance(content, title),
                        "data_source": "akshare"
                    }

                    # 过滤空标题的新闻
                    if news_item["title"]:
                        news_list.append(news_item)

                self.logger.info(f"✅ {symbol} AKShare新闻获取成功: {len(news_list)} 条")
                return news_list
            else:
                # 获取市场新闻
                self.logger.debug("📰 获取AKShare市场新闻")

                try:
                    # 获取财经新闻
                    news_df = await asyncio.to_thread(
                        ak.news_cctv,
                        limit=limit
                    )
                except Exception as e:
                    msg = str(e)
                    if "Expecting value" in msg and "line 1 column 1" in msg:
                        self.logger.warning(f"⚠️ AKShare市场新闻接口返回空/非JSON响应: {e}")
                        return []
                    self.logger.debug(f"CCTV新闻获取失败: {e}")
                    return []

                if news_df is None:
                    self.logger.warning("⚠️ 未获取到AKShare市场新闻数据")
                    return []

                if not isinstance(news_df, pd.DataFrame) or news_df.empty:
                    self.logger.warning(f"⚠️ 未获取到AKShare市场新闻数据（类型={type(news_df)}）")
                    return []

                news_list = []

                for _, row in news_df.iterrows():
                    title = str(row.get('title', '') or row.get('标题', ''))
                    content = str(row.get('content', '') or row.get('内容', ''))
                    summary = str(row.get('brief', '') or row.get('摘要', ''))

                    news_item = {
                        "title": title,
                        "content": content,
                        "summary": summary,
                        "url": str(row.get('url', '') or row.get('链接', '')),
                        "source": str(row.get('source', '') or row.get('来源', '') or 'CCTV财经'),
                        "author": str(row.get('author', '') or ''),
                        "publish_time": self._parse_news_time(row.get('time', '') or row.get('时间', '')),
                        "category": self._classify_news(content, title),
                        "sentiment": self._analyze_news_sentiment(content, title),
                        "sentiment_score": self._calculate_sentiment_score(content, title),
                        "keywords": self._extract_keywords(content, title),
                        "importance": self._assess_news_importance(content, title),
                        "data_source": "akshare"
                    }

                    if news_item["title"]:
                        news_list.append(news_item)

                self.logger.info(f"✅ AKShare市场新闻获取成功: {len(news_list)} 条")
                return news_list

        except Exception as e:
            self.logger.error(f"❌ 获取AKShare新闻失败 symbol={symbol}: {e}")
            return None

    def _parse_news_time(self, time_str: str) -> Optional[datetime]:
        """解析新闻时间"""
        if not time_str:
            return datetime.utcnow()

        try:
            # 尝试多种时间格式
            formats = [
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%d %H:%M",
                "%Y-%m-%d",
                "%Y/%m/%d %H:%M:%S",
                "%Y/%m/%d %H:%M",
                "%Y/%m/%d",
                "%m-%d %H:%M",
                "%m/%d %H:%M"
            ]

            for fmt in formats:
                try:
                    parsed_time = datetime.strptime(str(time_str), fmt)

                    # 如果只有月日，补充年份
                    if fmt in ["%m-%d %H:%M", "%m/%d %H:%M"]:
                        current_year = datetime.now().year
                        parsed_time = parsed_time.replace(year=current_year)

                    return parsed_time
                except ValueError:
                    continue

            # 如果都失败了，返回当前时间
            self.logger.debug(f"⚠️ 无法解析新闻时间: {time_str}")
            return datetime.utcnow()

        except Exception as e:
            self.logger.debug(f"解析新闻时间异常: {e}")
            return datetime.utcnow()

    def _analyze_news_sentiment(self, content: str, title: str) -> str:
        """
        分析新闻情绪

        Args:
            content: 新闻内容
            title: 新闻标题

        Returns:
            情绪类型: positive/negative/neutral
        """
        text = f"{title} {content}".lower()

        # 积极关键词
        positive_keywords = [
            '利好', '上涨', '增长', '盈利', '突破', '创新高', '买入', '推荐',
            '看好', '乐观', '强势', '大涨', '飙升', '暴涨', '涨停', '涨幅',
            '业绩增长', '营收增长', '净利润增长', '扭亏为盈', '超预期',
            '获批', '中标', '签约', '合作', '并购', '重组', '分红', '回购'
        ]

        # 消极关键词
        negative_keywords = [
            '利空', '下跌', '亏损', '风险', '暴跌', '卖出', '警告', '下调',
            '看空', '悲观', '弱势', '大跌', '跳水', '暴跌', '跌停', '跌幅',
            '业绩下滑', '营收下降', '净利润下降', '亏损', '低于预期',
            '被查', '违规', '处罚', '诉讼', '退市', '停牌', '商誉减值'
        ]

        positive_count = sum(1 for keyword in positive_keywords if keyword in text)
        negative_count = sum(1 for keyword in negative_keywords if keyword in text)

        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'

    def _calculate_sentiment_score(self, content: str, title: str) -> float:
        """
        计算情绪分数

        Args:
            content: 新闻内容
            title: 新闻标题

        Returns:
            情绪分数: -1.0 到 1.0
        """
        text = f"{title} {content}".lower()

        # 积极关键词权重
        positive_keywords = {
            '涨停': 1.0, '暴涨': 0.9, '大涨': 0.8, '飙升': 0.8,
            '创新高': 0.7, '突破': 0.6, '上涨': 0.5, '增长': 0.4,
            '利好': 0.6, '看好': 0.5, '推荐': 0.5, '买入': 0.6
        }

        # 消极关键词权重
        negative_keywords = {
            '跌停': -1.0, '暴跌': -0.9, '大跌': -0.8, '跳水': -0.8,
            '创新低': -0.7, '破位': -0.6, '下跌': -0.5, '下滑': -0.4,
            '利空': -0.6, '看空': -0.5, '卖出': -0.6, '警告': -0.5
        }

        score = 0.0

        # 计算积极分数
        for keyword, weight in positive_keywords.items():
            if keyword in text:
                score += weight

        # 计算消极分数
        for keyword, weight in negative_keywords.items():
            if keyword in text:
                score += weight

        # 归一化到 [-1.0, 1.0]
        return max(-1.0, min(1.0, score / 3.0))

    def _extract_keywords(self, content: str, title: str) -> List[str]:
        """
        提取关键词

        Args:
            content: 新闻内容
            title: 新闻标题

        Returns:
            关键词列表
        """
        text = f"{title} {content}"

        # 常见财经关键词
        common_keywords = [
            '股票', '公司', '市场', '投资', '业绩', '财报', '政策', '行业',
            '分析', '预测', '涨停', '跌停', '上涨', '下跌', '盈利', '亏损',
            '并购', '重组', '分红', '回购', '增持', '减持', '融资', 'IPO',
            '监管', '央行', '利率', '汇率', 'GDP', '通胀', '经济', '贸易',
            '科技', '互联网', '新能源', '医药', '房地产', '金融', '制造业'
        ]

        keywords = []
        for keyword in common_keywords:
            if keyword in text:
                keywords.append(keyword)

        return keywords[:10]  # 最多返回10个关键词

    def _assess_news_importance(self, content: str, title: str) -> str:
        """
        评估新闻重要性

        Args:
            content: 新闻内容
            title: 新闻标题

        Returns:
            重要性级别: high/medium/low
        """
        text = f"{title} {content}".lower()

        # 高重要性关键词
        high_importance_keywords = [
            '业绩', '财报', '年报', '季报', '重大', '公告', '监管', '政策',
            '并购', '重组', '退市', '停牌', '涨停', '跌停', '暴涨', '暴跌',
            '央行', '证监会', '交易所', '违规', '处罚', '立案', '调查'
        ]

        # 中等重要性关键词
        medium_importance_keywords = [
            '分析', '预测', '观点', '建议', '行业', '市场', '趋势', '机会',
            '研报', '评级', '目标价', '增持', '减持', '买入', '卖出',
            '合作', '签约', '中标', '获批', '分红', '回购'
        ]

        # 检查高重要性
        if any(keyword in text for keyword in high_importance_keywords):
            return 'high'

        # 检查中等重要性
        if any(keyword in text for keyword in medium_importance_keywords):
            return 'medium'

        return 'low'

    def _classify_news(self, content: str, title: str) -> str:
        """
        分类新闻

        Args:
            content: 新闻内容
            title: 新闻标题

        Returns:
            新闻类别
        """
        text = f"{title} {content}".lower()

        # 公司公告
        if any(keyword in text for keyword in ['公告', '业绩', '财报', '年报', '季报']):
            return 'company_announcement'

        # 政策新闻
        if any(keyword in text for keyword in ['政策', '监管', '央行', '证监会', '国务院']):
            return 'policy_news'

        # 行业新闻
        if any(keyword in text for keyword in ['行业', '板块', '产业', '领域']):
            return 'industry_news'

        # 市场新闻
        if any(keyword in text for keyword in ['市场', '指数', '大盘', '沪指', '深成指']):
            return 'market_news'

        # 研究报告
        if any(keyword in text for keyword in ['研报', '分析', '评级', '目标价', '机构']):
            return 'research_report'

        return 'general'
    
    async def get_stock_sse_summary(self) -> Optional[pd.DataFrame]:
        """
        获取上海证券交易所-股票数据总貌
        
        Returns:
            股票数据总貌DataFrame，包含项目、股票、科创板、主板等信息
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info("📊 获取上海证券交易所-股票数据总貌...")
            
            def fetch_sse_summary():
                return self.ak.stock_sse_summary()
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_sse_summary)
            
            if df is None or df.empty:
                logger.warning("⚠️ 上海证券交易所数据总貌为空")
                return None
            
            logger.info(f"✅ 上海证券交易所数据总貌获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取上海证券交易所数据总貌失败: {e}")
            return None
    
    async def get_stock_szse_summary(self, date: str) -> Optional[pd.DataFrame]:
        """
        获取深圳证券交易所-市场总貌-证券类别统计
        
        Args:
            date: 日期，格式如 "20200619"
            
        Returns:
            证券类别统计DataFrame，包含证券类别、数量、成交金额、总市值、流通市值
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info(f"📊 获取深圳证券交易所证券类别统计 (日期: {date})...")
            
            def fetch_szse_summary():
                return self.ak.stock_szse_summary(date=date)
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_szse_summary)
            
            if df is None or df.empty:
                logger.warning(f"⚠️ 深圳证券交易所证券类别统计为空 (日期: {date})")
                return None
            
            logger.info(f"✅ 深圳证券交易所证券类别统计获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取深圳证券交易所证券类别统计失败 (日期: {date}): {e}")
            return None
    
    async def get_stock_szse_area_summary(self, date: str) -> Optional[pd.DataFrame]:
        """
        获取深圳证券交易所-市场总貌-地区交易排序
        
        Args:
            date: 年月，格式如 "202203"
            
        Returns:
            地区交易排序DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info(f"📊 获取深圳证券交易所地区交易排序 (年月: {date})...")
            
            def fetch_szse_area_summary():
                return self.ak.stock_szse_area_summary(date=date)
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_szse_area_summary)
            
            if df is None or df.empty:
                logger.warning(f"⚠️ 深圳证券交易所地区交易排序为空 (年月: {date})")
                return None
            
            logger.info(f"✅ 深圳证券交易所地区交易排序获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取深圳证券交易所地区交易排序失败 (年月: {date}): {e}")
            return None
    
    async def get_stock_szse_sector_summary(self, symbol: str, date: str) -> Optional[pd.DataFrame]:
        """
        获取深圳证券交易所-统计资料-股票行业成交
        
        Args:
            symbol: "当月" 或 "当年"
            date: 年月，格式如 "202501"
            
        Returns:
            股票行业成交DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info(f"📊 获取深圳证券交易所股票行业成交 (symbol: {symbol}, 年月: {date})...")
            
            def fetch_szse_sector_summary():
                return self.ak.stock_szse_sector_summary(symbol=symbol, date=date)
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_szse_sector_summary)
            
            if df is None or df.empty:
                logger.warning(f"⚠️ 深圳证券交易所股票行业成交为空 (symbol: {symbol}, 年月: {date})")
                return None
            
            logger.info(f"✅ 深圳证券交易所股票行业成交获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取深圳证券交易所股票行业成交失败 (symbol: {symbol}, 年月: {date}): {e}")
            return None
    
    async def get_stock_sse_deal_daily(self, date: str) -> Optional[pd.DataFrame]:
        """
        获取上海证券交易所-每日股票情况
        
        Args:
            date: 日期，格式如 "20250221"，注意仅支持获取在 20211227（包含）之后的数据
            
        Returns:
            每日股票情况DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info(f"📊 获取上海证券交易所每日股票情况 (日期: {date})...")
            
            def fetch_sse_deal_daily():
                return self.ak.stock_sse_deal_daily(date=date)
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_sse_deal_daily)
            
            if df is None or df.empty:
                logger.warning(f"⚠️ 上海证券交易所每日股票情况为空 (日期: {date})")
                return None
            
            logger.info(f"✅ 上海证券交易所每日股票情况获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取上海证券交易所每日股票情况失败 (日期: {date}): {e}")
            return None
    
    async def get_stock_individual_info_em(self, symbol: str, timeout: float = None) -> Optional[pd.DataFrame]:
        """
        获取东方财富-个股信息
        
        Args:
            symbol: 股票代码，如 "603777"
            timeout: 超时时间（秒）
            
        Returns:
            个股信息DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info(f"📊 获取东方财富个股信息 (股票: {symbol})...")
            
            def fetch_individual_info():
                if timeout:
                    return self.ak.stock_individual_info_em(symbol=symbol, timeout=timeout)
                else:
                    return self.ak.stock_individual_info_em(symbol=symbol)
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_individual_info)
            
            if df is None or df.empty:
                logger.warning(f"⚠️ 东方财富个股信息为空 (股票: {symbol})")
                return None
            
            logger.info(f"✅ 东方财富个股信息获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取东方财富个股信息失败 (股票: {symbol}): {e}")
            return None
    
    async def get_stock_individual_basic_info_xq(self, symbol: str, token: str = None, timeout: float = None) -> Optional[pd.DataFrame]:
        """
        获取雪球-个股基础信息
        
        Args:
            symbol: 股票代码（雪球格式），如 "SH601127"
            token: 雪球token（可选）
            timeout: 超时时间（秒）
            
        Returns:
            个股基础信息DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info(f"📊 获取雪球个股基础信息 (股票: {symbol})...")
            
            def fetch_basic_info():
                kwargs = {"symbol": symbol}
                if token:
                    kwargs["token"] = token
                if timeout:
                    kwargs["timeout"] = timeout
                return self.ak.stock_individual_basic_info_xq(**kwargs)
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_basic_info)
            
            if df is None or df.empty:
                logger.warning(f"⚠️ 雪球个股基础信息为空 (股票: {symbol})")
                return None
            
            logger.info(f"✅ 雪球个股基础信息获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取雪球个股基础信息失败 (股票: {symbol}): {e}")
            return None
    
    async def get_stock_bid_ask_em(self, symbol: str) -> Optional[pd.DataFrame]:
        """
        获取东方财富-行情报价
        
        Args:
            symbol: 股票代码，如 "000001"
            
        Returns:
            行情报价DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info(f"📊 获取东方财富行情报价 (股票: {symbol})...")
            
            def fetch_bid_ask():
                return self.ak.stock_bid_ask_em(symbol=symbol)
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_bid_ask)
            
            if df is None or df.empty:
                logger.warning(f"⚠️ 东方财富行情报价为空 (股票: {symbol})")
                return None
            
            logger.info(f"✅ 东方财富行情报价获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取东方财富行情报价失败 (股票: {symbol}): {e}")
            return None
    
    async def get_stock_zh_a_spot_em(self) -> Optional[pd.DataFrame]:
        """
        获取沪深京A股实时行情
        
        Returns:
            实时行情DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info("📊 获取沪深京A股实时行情...")
            
            def fetch_zh_a_spot():
                return self.ak.stock_zh_a_spot_em()
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_zh_a_spot)
            
            if df is None or df.empty:
                logger.warning("⚠️ 沪深京A股实时行情为空")
                return None
            
            logger.info(f"✅ 沪深京A股实时行情获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取沪深京A股实时行情失败: {e}")
            return None
    
    async def get_stock_sh_a_spot_em(self) -> Optional[pd.DataFrame]:
        """
        获取沪A股实时行情
        
        Returns:
            实时行情DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info("📊 获取沪A股实时行情...")
            
            def fetch_sh_a_spot():
                return self.ak.stock_sh_a_spot_em()
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_sh_a_spot)
            
            if df is None or df.empty:
                logger.warning("⚠️ 沪A股实时行情为空")
                return None
            
            logger.info(f"✅ 沪A股实时行情获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取沪A股实时行情失败: {e}")
            return None
    
    async def get_stock_sz_a_spot_em(self) -> Optional[pd.DataFrame]:
        """
        获取深A股实时行情
        
        Returns:
            实时行情DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info("📊 获取深A股实时行情...")
            
            def fetch_sz_a_spot():
                return self.ak.stock_sz_a_spot_em()
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_sz_a_spot)
            
            if df is None or df.empty:
                logger.warning("⚠️ 深A股实时行情为空")
                return None
            
            logger.info(f"✅ 深A股实时行情获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取深A股实时行情失败: {e}")
            return None
    
    async def get_stock_esg_hz_sina(self) -> Optional[pd.DataFrame]:
        """
        获取华证指数ESG评级
        
        Returns:
            ESG评级DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info("📊 获取华证指数ESG评级...")
            
            def fetch_esg_hz():
                return self.ak.stock_esg_hz_sina()
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_esg_hz)
            
            if df is None or df.empty:
                logger.warning("⚠️ 华证指数ESG评级为空")
                return None
            
            logger.info(f"✅ 华证指数ESG评级获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取华证指数ESG评级失败: {e}")
            return None
    
    async def get_stock_esg_zd_sina(self) -> Optional[pd.DataFrame]:
        """
        获取秩鼎ESG评级
        
        Returns:
            ESG评级DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info("📊 获取秩鼎ESG评级...")
            
            def fetch_esg_zd():
                return self.ak.stock_esg_zd_sina()
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_esg_zd)
            
            if df is None or df.empty:
                logger.warning("⚠️ 秩鼎ESG评级为空")
                return None
            
            logger.info(f"✅ 秩鼎ESG评级获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取秩鼎ESG评级失败: {e}")
            return None
    
    async def get_stock_esg_rft_sina(self) -> Optional[pd.DataFrame]:
        """
        获取路孚特ESG评级
        
        Returns:
            ESG评级DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info("📊 获取路孚特ESG评级...")
            
            def fetch_esg_rft():
                return self.ak.stock_esg_rft_sina()
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_esg_rft)
            
            if df is None or df.empty:
                logger.warning("⚠️ 路孚特ESG评级为空")
                return None
            
            logger.info(f"✅ 路孚特ESG评级获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取路孚特ESG评级失败: {e}")
            return None
    
    async def get_stock_esg_msci_sina(self) -> Optional[pd.DataFrame]:
        """
        获取MSCI ESG评级
        
        Returns:
            ESG评级DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info("📊 获取MSCI ESG评级...")
            
            def fetch_esg_msci():
                return self.ak.stock_esg_msci_sina()
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_esg_msci)
            
            if df is None or df.empty:
                logger.warning("⚠️ MSCI ESG评级为空")
                return None
            
            logger.info(f"✅ MSCI ESG评级获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取MSCI ESG评级失败: {e}")
            return None
    
    async def get_stock_esg_rate_sina(self) -> Optional[pd.DataFrame]:
        """
        获取ESG评级数据
        
        Returns:
            ESG评级DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info("📊 获取ESG评级数据...")
            
            def fetch_esg_rate():
                return self.ak.stock_esg_rate_sina()
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_esg_rate)
            
            if df is None or df.empty:
                logger.warning("⚠️ ESG评级数据为空")
                return None
            
            logger.info(f"✅ ESG评级数据获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取ESG评级数据失败: {e}")
            return None
    
    async def get_stock_rank_xzjp_ths(self) -> Optional[pd.DataFrame]:
        """
        获取险资举牌数据
        
        Returns:
            险资举牌DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info("📊 获取险资举牌数据...")
            
            def fetch_rank_xzjp():
                return self.ak.stock_rank_xzjp_ths()
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_rank_xzjp)
            
            if df is None or df.empty:
                logger.warning("⚠️ 险资举牌数据为空")
                return None
            
            logger.info(f"✅ 险资举牌数据获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取险资举牌数据失败: {e}")
            return None
    
    async def get_stock_rank_ljqd_ths(self) -> Optional[pd.DataFrame]:
        """
        获取量价齐跌数据
        
        Returns:
            量价齐跌DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info("📊 获取量价齐跌数据...")
            
            def fetch_rank_ljqd():
                return self.ak.stock_rank_ljqd_ths()
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_rank_ljqd)
            
            if df is None or df.empty:
                logger.warning("⚠️ 量价齐跌数据为空")
                return None
            
            logger.info(f"✅ 量价齐跌数据获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取量价齐跌数据失败: {e}")
            return None
    
    async def get_stock_rank_ljqs_ths(self) -> Optional[pd.DataFrame]:
        """
        获取量价齐升数据
        
        Returns:
            量价齐升DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info("📊 获取量价齐升数据...")
            
            def fetch_rank_ljqs():
                return self.ak.stock_rank_ljqs_ths()
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_rank_ljqs)
            
            if df is None or df.empty:
                logger.warning("⚠️ 量价齐升数据为空")
                return None
            
            logger.info(f"✅ 量价齐升数据获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取量价齐升数据失败: {e}")
            return None
    
    async def get_stock_rank_xxtp_ths(self, symbol: str = "500日均线") -> Optional[pd.DataFrame]:
        """
        获取向下突破数据
        
        Args:
            symbol: 均线类型，默认 "500日均线"
            
        Returns:
            向下突破DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info(f"📊 获取向下突破数据 ({symbol})...")
            
            def fetch_rank_xxtp():
                return self.ak.stock_rank_xxtp_ths(symbol=symbol)
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_rank_xxtp)
            
            if df is None or df.empty:
                logger.warning(f"⚠️ 向下突破数据 ({symbol}) 为空")
                return None
            
            logger.info(f"✅ 向下突破数据 ({symbol}) 获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取向下突破数据 ({symbol}) 失败: {e}")
            return None
    
    async def get_stock_rank_xstp_ths(self, symbol: str = "500日均线") -> Optional[pd.DataFrame]:
        """
        获取向上突破数据
        
        Args:
            symbol: 均线类型，默认 "500日均线"
            
        Returns:
            向上突破DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info(f"📊 获取向上突破数据 ({symbol})...")
            
            def fetch_rank_xstp():
                return self.ak.stock_rank_xstp_ths(symbol=symbol)
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_rank_xstp)
            
            if df is None or df.empty:
                logger.warning(f"⚠️ 向上突破数据 ({symbol}) 为空")
                return None
            
            logger.info(f"✅ 向上突破数据 ({symbol}) 获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取向上突破数据 ({symbol}) 失败: {e}")
            return None
    
    async def get_stock_rank_cxsl_ths(self) -> Optional[pd.DataFrame]:
        """
        获取持续缩量数据
        
        Returns:
            持续缩量DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info("📊 获取持续缩量数据...")
            
            def fetch_rank_cxsl():
                return self.ak.stock_rank_cxsl_ths()
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_rank_cxsl)
            
            if df is None or df.empty:
                logger.warning("⚠️ 持续缩量数据为空")
                return None
            
            logger.info(f"✅ 持续缩量数据获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取持续缩量数据失败: {e}")
            return None
    
    async def get_stock_rank_cxfl_ths(self) -> Optional[pd.DataFrame]:
        """
        获取持续放量数据
        
        Returns:
            持续放量DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info("📊 获取持续放量数据...")
            
            def fetch_rank_cxfl():
                return self.ak.stock_rank_cxfl_ths()
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_rank_cxfl)
            
            if df is None or df.empty:
                logger.warning("⚠️ 持续放量数据为空")
                return None
            
            logger.info(f"✅ 持续放量数据获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取持续放量数据失败: {e}")
            return None
    
    async def get_stock_market_activity_legu(self) -> Optional[pd.DataFrame]:
        """
        获取赚钱效应分析数据
        
        Returns:
            赚钱效应分析DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info("📊 获取赚钱效应分析数据...")
            
            def fetch_market_activity_legu():
                return self.ak.stock_market_activity_legu()
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_market_activity_legu)
            
            if df is None or df.empty:
                logger.warning("⚠️ 赚钱效应分析数据为空")
                return None
            
            logger.info(f"✅ 赚钱效应分析数据获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取赚钱效应分析数据失败: {e}")
            return None
    
    async def get_stock_zt_pool_dtgc_em(self, date: str = None) -> Optional[pd.DataFrame]:
        """
        获取跌停股池数据
        
        Args:
            date: 日期 (YYYYMMDD)，默认为最近交易日
            
        Returns:
            跌停股池DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            if not date:
                from datetime import datetime
                date = datetime.now().strftime("%Y%m%d")
            
            logger.info(f"📊 获取跌停股池数据 ({date})...")
            
            def fetch_zt_pool_dtgc():
                return self.ak.stock_zt_pool_dtgc_em(date=date)
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_zt_pool_dtgc)
            
            if df is None or df.empty:
                logger.warning(f"⚠️ 跌停股池数据 ({date}) 为空")
                return None
            
            logger.info(f"✅ 跌停股池数据 ({date}) 获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取跌停股池数据 ({date}) 失败: {e}")
            return None
    
    async def get_stock_zt_pool_zbgc_em(self, date: str = None) -> Optional[pd.DataFrame]:
        """
        获取炸板股池数据
        
        Args:
            date: 日期 (YYYYMMDD)，默认为最近交易日
            
        Returns:
            炸板股池DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            if not date:
                from datetime import datetime
                date = datetime.now().strftime("%Y%m%d")
            
            logger.info(f"📊 获取炸板股池数据 ({date})...")
            
            def fetch_zt_pool_zbgc():
                return self.ak.stock_zt_pool_zbgc_em(date=date)
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_zt_pool_zbgc)
            
            if df is None or df.empty:
                logger.warning(f"⚠️ 炸板股池数据 ({date}) 为空")
                return None
            
            logger.info(f"✅ 炸板股池数据 ({date}) 获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取炸板股池数据 ({date}) 失败: {e}")
            return None
    
    async def get_stock_zt_pool_sub_new_em(self, date: str = None) -> Optional[pd.DataFrame]:
        """
        获取次新股池数据
        
        Args:
            date: 日期 (YYYYMMDD)，默认为最近交易日
            
        Returns:
            次新股池DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            if not date:
                from datetime import datetime
                date = datetime.now().strftime("%Y%m%d")
            
            logger.info(f"📊 获取次新股池数据 ({date})...")
            
            def fetch_zt_pool_sub_new():
                return self.ak.stock_zt_pool_sub_new_em(date=date)
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_zt_pool_sub_new)
            
            if df is None or df.empty:
                logger.warning(f"⚠️ 次新股池数据 ({date}) 为空")
                return None
            
            logger.info(f"✅ 次新股池数据 ({date}) 获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取次新股池数据 ({date}) 失败: {e}")
            return None
    
    async def get_stock_zt_pool_strong_em(self, date: str = None) -> Optional[pd.DataFrame]:
        """
        获取强势股池数据
        
        Args:
            date: 日期 (YYYYMMDD)，默认为最近交易日
            
        Returns:
            强势股池DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            if not date:
                from datetime import datetime
                date = datetime.now().strftime("%Y%m%d")
            
            logger.info(f"📊 获取强势股池数据 ({date})...")
            
            def fetch_zt_pool_strong():
                return self.ak.stock_zt_pool_strong_em(date=date)
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_zt_pool_strong)
            
            if df is None or df.empty:
                logger.warning(f"⚠️ 强势股池数据 ({date}) 为空")
                return None
            
            logger.info(f"✅ 强势股池数据 ({date}) 获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取强势股池数据 ({date}) 失败: {e}")
            return None
    
    async def get_stock_zt_pool_previous_em(self, date: str = None) -> Optional[pd.DataFrame]:
        """
        获取昨日涨停股池数据
        
        Args:
            date: 日期 (YYYYMMDD)，默认为最近交易日
            
        Returns:
            昨日涨停股池DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            if not date:
                from datetime import datetime
                date = datetime.now().strftime("%Y%m%d")
            
            logger.info(f"📊 获取昨日涨停股池数据 ({date})...")
            
            def fetch_zt_pool_previous():
                return self.ak.stock_zt_pool_previous_em(date=date)
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_zt_pool_previous)
            
            if df is None or df.empty:
                logger.warning(f"⚠️ 昨日涨停股池数据 ({date}) 为空")
                return None
            
            logger.info(f"✅ 昨日涨停股池数据 ({date}) 获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取昨日涨停股池数据 ({date}) 失败: {e}")
            return None
    
    async def get_stock_zt_pool_em(self, date: str = None) -> Optional[pd.DataFrame]:
        """
        获取涨停股池数据
        
        Args:
            date: 日期 (YYYYMMDD)，默认为最近交易日
            
        Returns:
            涨停股池DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            if not date:
                from datetime import datetime
                date = datetime.now().strftime("%Y%m%d")
            
            logger.info(f"📊 获取涨停股池数据 ({date})...")
            
            def fetch_zt_pool():
                return self.ak.stock_zt_pool_em(date=date)
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_zt_pool)
            
            if df is None or df.empty:
                logger.warning(f"⚠️ 涨停股池数据 ({date}) 为空")
                return None
            
            logger.info(f"✅ 涨停股池数据 ({date}) 获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取涨停股池数据 ({date}) 失败: {e}")
            return None
    
    async def get_stock_board_change_em(self) -> Optional[pd.DataFrame]:
        """
        获取板块异动详情数据
        
        Returns:
            板块异动详情DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info("📊 获取板块异动详情数据...")
            
            def fetch_board_change():
                return self.ak.stock_board_change_em()
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_board_change)
            
            if df is None or df.empty:
                logger.warning("⚠️ 板块异动详情数据为空")
                return None
            
            logger.info(f"✅ 板块异动详情数据获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取板块异动详情数据失败: {e}")
            return None
    
    async def get_stock_changes_em(self, symbol: str = "大笔买入") -> Optional[pd.DataFrame]:
        """
        获取盘口异动数据
        
        Args:
            symbol: 异动类型，默认 "大笔买入"
            
        Returns:
            盘口异动DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info(f"📊 获取盘口异动数据 ({symbol})...")
            
            def fetch_stock_changes():
                return self.ak.stock_changes_em(symbol=symbol)
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_stock_changes)
            
            if df is None or df.empty:
                logger.warning(f"⚠️ 盘口异动数据 ({symbol}) 为空")
                return None
            
            logger.info(f"✅ 盘口异动数据 ({symbol}) 获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取盘口异动数据 ({symbol}) 失败: {e}")
            return None
    
    async def get_stock_hot_rank_relate_em(self, symbol: str = "SZ000665") -> Optional[pd.DataFrame]:
        """
        获取相关股票数据
        
        Args:
            symbol: 股票代码，默认 "SZ000665"
            
        Returns:
            相关股票DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info(f"📊 获取相关股票数据 ({symbol})...")
            
            def fetch_hot_rank_relate():
                return self.ak.stock_hot_rank_relate_em(symbol=symbol)
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_hot_rank_relate)
            
            if df is None or df.empty:
                logger.warning(f"⚠️ 相关股票数据 ({symbol}) 为空")
                return None
            
            logger.info(f"✅ 相关股票数据 ({symbol}) 获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取相关股票数据 ({symbol}) 失败: {e}")
            return None
    
    async def get_stock_hot_search_baidu(
        self, 
        symbol: str = "A股", 
        date: str = None, 
        time: str = "今日"
    ) -> Optional[pd.DataFrame]:
        """
        获取热搜股票数据
        
        Args:
            symbol: 市场类型，默认 "A股"
            date: 日期 (YYYYMMDD)
            time: 时间类型，默认 "今日"
            
        Returns:
            热搜股票DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            if not date:
                from datetime import datetime
                date = datetime.now().strftime("%Y%m%d")
            
            logger.info(f"📊 获取热搜股票数据 ({symbol}, {date}, {time})...")
            
            def fetch_hot_search_baidu():
                return self.ak.stock_hot_search_baidu(symbol=symbol, date=date, time=time)
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_hot_search_baidu)
            
            if df is None or df.empty:
                logger.warning(f"⚠️ 热搜股票数据 ({symbol}, {date}, {time}) 为空")
                return None
            
            logger.info(f"✅ 热搜股票数据 ({symbol}, {date}, {time}) 获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取热搜股票数据 ({symbol}, {date}, {time}) 失败: {e}")
            return None
    
    async def get_stock_hk_hot_rank_latest_em(self, symbol: str = "00700") -> Optional[pd.DataFrame]:
        """
        获取港股个股人气榜最新排名数据
        
        Args:
            symbol: 股票代码，默认 "00700"
            
        Returns:
            港股个股人气榜最新排名DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info(f"📊 获取港股个股人气榜最新排名数据 ({symbol})...")
            
            def fetch_hk_hot_rank_latest():
                return self.ak.stock_hk_hot_rank_latest_em(symbol=symbol)
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_hk_hot_rank_latest)
            
            if df is None or df.empty:
                logger.warning(f"⚠️ 港股个股人气榜最新排名数据 ({symbol}) 为空")
                return None
            
            logger.info(f"✅ 港股个股人气榜最新排名数据 ({symbol}) 获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取港股个股人气榜最新排名数据 ({symbol}) 失败: {e}")
            return None
    
    async def get_stock_hot_rank_latest_em(self, symbol: str = "SZ000665") -> Optional[pd.DataFrame]:
        """
        获取A股个股人气榜最新排名数据
        
        Args:
            symbol: 股票代码，默认 "SZ000665"
            
        Returns:
            A股个股人气榜最新排名DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info(f"📊 获取A股个股人气榜最新排名数据 ({symbol})...")
            
            def fetch_hot_rank_latest():
                return self.ak.stock_hot_rank_latest_em(symbol=symbol)
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_hot_rank_latest)
            
            if df is None or df.empty:
                logger.warning(f"⚠️ A股个股人气榜最新排名数据 ({symbol}) 为空")
                return None
            
            logger.info(f"✅ A股个股人气榜最新排名数据 ({symbol}) 获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取A股个股人气榜最新排名数据 ({symbol}) 失败: {e}")
            return None
    
    async def get_stock_inner_trade_xq(self) -> Optional[pd.DataFrame]:
        """
        获取内部交易数据
        
        Returns:
            内部交易DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info("📊 获取内部交易数据...")
            
            def fetch_inner_trade():
                return self.ak.stock_inner_trade_xq()
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_inner_trade)
            
            if df is None or df.empty:
                logger.warning("⚠️ 内部交易数据为空")
                return None
            
            logger.info(f"✅ 内部交易数据获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取内部交易数据失败: {e}")
            return None
    
    async def get_stock_hot_keyword_em(self, symbol: str = "SZ000665") -> Optional[pd.DataFrame]:
        """
        获取热门关键词数据
        
        Args:
            symbol: 股票代码，默认 "SZ000665"
            
        Returns:
            热门关键词DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info(f"📊 获取热门关键词数据 ({symbol})...")
            
            def fetch_hot_keyword():
                return self.ak.stock_hot_keyword_em(symbol=symbol)
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_hot_keyword)
            
            if df is None or df.empty:
                logger.warning(f"⚠️ 热门关键词数据 ({symbol}) 为空")
                return None
            
            logger.info(f"✅ 热门关键词数据 ({symbol}) 获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取热门关键词数据 ({symbol}) 失败: {e}")
            return None
    
    async def get_stock_hk_hot_rank_detail_realtime_em(self, symbol: str = "00700") -> Optional[pd.DataFrame]:
        """
        获取港股个股人气榜实时变动数据
        
        Args:
            symbol: 股票代码，默认 "00700"
            
        Returns:
            港股个股人气榜实时变动DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info(f"📊 获取港股个股人气榜实时变动数据 ({symbol})...")
            
            def fetch_hk_hot_rank_detail_realtime():
                return self.ak.stock_hk_hot_rank_detail_realtime_em(symbol=symbol)
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_hk_hot_rank_detail_realtime)
            
            if df is None or df.empty:
                logger.warning(f"⚠️ 港股个股人气榜实时变动数据 ({symbol}) 为空")
                return None
            
            logger.info(f"✅ 港股个股人气榜实时变动数据 ({symbol}) 获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取港股个股人气榜实时变动数据 ({symbol}) 失败: {e}")
            return None
    
    async def get_stock_hot_rank_detail_realtime_em(self, symbol: str = "SZ000665") -> Optional[pd.DataFrame]:
        """
        获取A股个股人气榜实时变动数据
        
        Args:
            symbol: 股票代码，默认 "SZ000665"
            
        Returns:
            A股个股人气榜实时变动DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info(f"📊 获取A股个股人气榜实时变动数据 ({symbol})...")
            
            def fetch_hot_rank_detail_realtime():
                return self.ak.stock_hot_rank_detail_realtime_em(symbol=symbol)
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_hot_rank_detail_realtime)
            
            if df is None or df.empty:
                logger.warning(f"⚠️ A股个股人气榜实时变动数据 ({symbol}) 为空")
                return None
            
            logger.info(f"✅ A股个股人气榜实时变动数据 ({symbol}) 获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取A股个股人气榜实时变动数据 ({symbol}) 失败: {e}")
            return None
    
    async def get_stock_sns_sseinfo(self, symbol: str = "603119") -> Optional[pd.DataFrame]:
        """
        获取上证e互动数据
        
        Args:
            symbol: 股票代码，默认 "603119"
            
        Returns:
            上证e互动DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info(f"📊 获取上证e互动数据 ({symbol})...")
            
            def fetch_sns_sseinfo():
                return self.ak.stock_sns_sseinfo(symbol=symbol)
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_sns_sseinfo)
            
            if df is None or df.empty:
                logger.warning(f"⚠️ 上证e互动数据 ({symbol}) 为空")
                return None
            
            logger.info(f"✅ 上证e互动数据 ({symbol}) 获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取上证e互动数据 ({symbol}) 失败: {e}")
            return None
    
    async def get_stock_irm_ans_cninfo(self, symbol: str = "1495108801386602496") -> Optional[pd.DataFrame]:
        """
        获取互动易-回答数据
        
        Args:
            symbol: 提问者编号，默认 "1495108801386602496"
            
        Returns:
            互动易-回答DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info(f"📊 获取互动易-回答数据 ({symbol})...")
            
            def fetch_irm_ans_cninfo():
                return self.ak.stock_irm_ans_cninfo(symbol=symbol)
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_irm_ans_cninfo)
            
            if df is None or df.empty:
                logger.warning(f"⚠️ 互动易-回答数据 ({symbol}) 为空")
                return None
            
            logger.info(f"✅ 互动易-回答数据 ({symbol}) 获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取互动易-回答数据 ({symbol}) 失败: {e}")
            return None
    
    async def get_stock_irm_cninfo(self, symbol: str = "002594") -> Optional[pd.DataFrame]:
        """
        获取互动易-提问数据
        
        Args:
            symbol: 股票代码，默认 "002594"
            
        Returns:
            互动易-提问DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info(f"📊 获取互动易-提问数据 ({symbol})...")
            
            def fetch_irm_cninfo():
                return self.ak.stock_irm_cninfo(symbol=symbol)
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_irm_cninfo)
            
            if df is None or df.empty:
                logger.warning(f"⚠️ 互动易-提问数据 ({symbol}) 为空")
                return None
            
            logger.info(f"✅ 互动易-提问数据 ({symbol}) 获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取互动易-提问数据 ({symbol}) 失败: {e}")
            return None
    
    async def get_stock_hk_hot_rank_detail_em(self, symbol: str = "00700") -> Optional[pd.DataFrame]:
        """
        获取港股股票热度-历史趋势数据
        
        Args:
            symbol: 股票代码，默认 "00700"
            
        Returns:
            港股股票热度-历史趋势DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info(f"📊 获取港股股票热度-历史趋势数据 ({symbol})...")
            
            def fetch_hk_hot_rank_detail():
                return self.ak.stock_hk_hot_rank_detail_em(symbol=symbol)
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_hk_hot_rank_detail)
            
            if df is None or df.empty:
                logger.warning(f"⚠️ 港股股票热度-历史趋势数据 ({symbol}) 为空")
                return None
            
            logger.info(f"✅ 港股股票热度-历史趋势数据 ({symbol}) 获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取港股股票热度-历史趋势数据 ({symbol}) 失败: {e}")
            return None
    
    async def get_stock_hot_rank_detail_em(self, symbol: str = "SZ000665") -> Optional[pd.DataFrame]:
        """
        获取A股股票热度-历史趋势及粉丝特征数据
        
        Args:
            symbol: 股票代码，默认 "SZ000665"
            
        Returns:
            A股股票热度-历史趋势及粉丝特征DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info(f"📊 获取A股股票热度-历史趋势及粉丝特征数据 ({symbol})...")
            
            def fetch_hot_rank_detail():
                return self.ak.stock_hot_rank_detail_em(symbol=symbol)
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_hot_rank_detail)
            
            if df is None or df.empty:
                logger.warning(f"⚠️ A股股票热度-历史趋势及粉丝特征数据 ({symbol}) 为空")
                return None
            
            logger.info(f"✅ A股股票热度-历史趋势及粉丝特征数据 ({symbol}) 获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取A股股票热度-历史趋势及粉丝特征数据 ({symbol}) 失败: {e}")
            return None
    
    async def get_stock_hk_hot_rank_em(self) -> Optional[pd.DataFrame]:
        """
        获取港股人气榜数据
        
        Returns:
            港股人气榜DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info("📊 获取港股人气榜数据...")
            
            def fetch_hk_hot_rank():
                return self.ak.stock_hk_hot_rank_em()
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_hk_hot_rank)
            
            if df is None or df.empty:
                logger.warning("⚠️ 港股人气榜数据为空")
                return None
            
            logger.info(f"✅ 港股人气榜数据获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取港股人气榜数据失败: {e}")
            return None
    
    async def get_stock_hot_up_em(self) -> Optional[pd.DataFrame]:
        """
        获取飙升榜-A股数据
        
        Returns:
            飙升榜-A股DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info("📊 获取飙升榜-A股数据...")
            
            def fetch_hot_up():
                return self.ak.stock_hot_up_em()
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_hot_up)
            
            if df is None or df.empty:
                logger.warning("⚠️ 飙升榜-A股数据为空")
                return None
            
            logger.info(f"✅ 飙升榜-A股数据获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取飙升榜-A股数据失败: {e}")
            return None
    
    async def get_stock_hot_rank_em(self) -> Optional[pd.DataFrame]:
        """
        获取人气榜-A股数据
        
        Returns:
            人气榜-A股DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info("📊 获取人气榜-A股数据...")
            
            def fetch_hot_rank():
                return self.ak.stock_hot_rank_em()
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_hot_rank)
            
            if df is None or df.empty:
                logger.warning("⚠️ 人气榜-A股数据为空")
                return None
            
            logger.info(f"✅ 人气榜-A股数据获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取人气榜-A股数据失败: {e}")
            return None
    
    async def get_stock_hot_deal_xq(self, symbol: str = "最热门") -> Optional[pd.DataFrame]:
        """
        获取交易排行榜数据
        
        Args:
            symbol: 榜单类型，默认 "最热门"，可选 "本周新增", "最热门"
            
        Returns:
            交易排行榜DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info(f"📊 获取交易排行榜数据 ({symbol})...")
            
            def fetch_hot_deal():
                return self.ak.stock_hot_deal_xq(symbol=symbol)
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_hot_deal)
            
            if df is None or df.empty:
                logger.warning(f"⚠️ 交易排行榜数据 ({symbol}) 为空")
                return None
            
            logger.info(f"✅ 交易排行榜数据 ({symbol}) 获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取交易排行榜数据 ({symbol}) 失败: {e}")
            return None
    
    async def get_stock_hot_tweet_xq(self, symbol: str = "最热门") -> Optional[pd.DataFrame]:
        """
        获取讨论排行榜数据
        
        Args:
            symbol: 榜单类型，默认 "最热门"，可选 "本周新增", "最热门"
            
        Returns:
            讨论排行榜DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info(f"📊 获取讨论排行榜数据 ({symbol})...")
            
            def fetch_hot_tweet():
                return self.ak.stock_hot_tweet_xq(symbol=symbol)
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_hot_tweet)
            
            if df is None or df.empty:
                logger.warning(f"⚠️ 讨论排行榜数据 ({symbol}) 为空")
                return None
            
            logger.info(f"✅ 讨论排行榜数据 ({symbol}) 获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取讨论排行榜数据 ({symbol}) 失败: {e}")
            return None
    
    async def get_stock_hot_follow_xq(self, symbol: str = "最热门") -> Optional[pd.DataFrame]:
        """
        获取关注排行榜数据
        
        Args:
            symbol: 榜单类型，默认 "最热门"，可选 "本周新增", "最热门"
            
        Returns:
            关注排行榜DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info(f"📊 获取关注排行榜数据 ({symbol})...")
            
            def fetch_hot_follow():
                return self.ak.stock_hot_follow_xq(symbol=symbol)
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_hot_follow)
            
            if df is None or df.empty:
                logger.warning(f"⚠️ 关注排行榜数据 ({symbol}) 为空")
                return None
            
            logger.info(f"✅ 关注排行榜数据 ({symbol}) 获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取关注排行榜数据 ({symbol}) 失败: {e}")
            return None
    
    async def get_stock_board_industry_hist_min_em(self, symbol: str = "小金属", period: str = "1") -> Optional[pd.DataFrame]:
        """
        获取东方财富-指数-分时数据
        
        Args:
            symbol: 行业代码，默认 "小金属"
            period: 周期，默认 "1"
            
        Returns:
            东方财富-指数-分时DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info(f"📊 获取东方财富-指数-分时数据 ({symbol}, {period})...")
            
            def fetch_board_industry_hist_min():
                return self.ak.stock_board_industry_hist_min_em(symbol=symbol, period=period)
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_board_industry_hist_min)
            
            if df is None or df.empty:
                logger.warning(f"⚠️ 东方财富-指数-分时数据 ({symbol}, {period}) 为空")
                return None
            
            logger.info(f"✅ 东方财富-指数-分时数据 ({symbol}, {period}) 获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取东方财富-指数-分时数据 ({symbol}, {period}) 失败: {e}")
            return None
    
    async def get_stock_board_industry_hist_em(self, symbol: str = "小金属", start_date: str = "20211201", end_date: str = "20220401", period: str = "日k", adjust: str = "") -> Optional[pd.DataFrame]:
        """
        获取东方财富-指数-日频数据
        
        Args:
            symbol: 行业代码，默认 "小金属"
            start_date: 开始日期，默认 "20211201"
            end_date: 结束日期，默认 "20220401"
            period: 周期，默认 "日k"
            adjust: 复权，默认 ""
            
        Returns:
            东方财富-指数-日频DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info(f"📊 获取东方财富-指数-日频数据 ({symbol}, {period}, {adjust})...")
            
            def fetch_board_industry_hist():
                return self.ak.stock_board_industry_hist_em(symbol=symbol, start_date=start_date, end_date=end_date, period=period, adjust=adjust)
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_board_industry_hist)
            
            if df is None or df.empty:
                logger.warning(f"⚠️ 东方财富-指数-日频数据 ({symbol}, {period}, {adjust}) 为空")
                return None
            
            logger.info(f"✅ 东方财富-指数-日频数据 ({symbol}, {period}, {adjust}) 获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取东方财富-指数-日频数据 ({symbol}, {period}, {adjust}) 失败: {e}")
            return None
    
    async def get_stock_board_industry_cons_em(self, symbol: str = "小金属") -> Optional[pd.DataFrame]:
        """
        获取东方财富-成份股数据
        
        Args:
            symbol: 行业代码，默认 "小金属"
            
        Returns:
            东方财富-成份股DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info(f"📊 获取东方财富-成份股数据 ({symbol})...")
            
            def fetch_board_industry_cons():
                return self.ak.stock_board_industry_cons_em(symbol=symbol)
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_board_industry_cons)
            
            if df is None or df.empty:
                logger.warning(f"⚠️ 东方财富-成份股数据 ({symbol}) 为空")
                return None
            
            logger.info(f"✅ 东方财富-成份股数据 ({symbol}) 获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取东方财富-成份股数据 ({symbol}) 失败: {e}")
            return None


    async def get_stock_comment_detail_zhpj_lspf_em(self, symbol: str = "600000") -> Optional[pd.DataFrame]:
        """
        获取历史评分数据
        
        Args:
            symbol: 股票代码，默认 "600000"
            
        Returns:
            历史评分DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info(f"📊 获取历史评分数据 ({symbol})...")
            
            def fetch_comment_detail():
                return self.ak.stock_comment_detail_zhpj_lspf_em(symbol=symbol)
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_comment_detail)
            
            if df is None or df.empty:
                logger.warning(f"⚠️ 历史评分数据 ({symbol}) 为空")
                return None
            
            logger.info(f"✅ 历史评分数据 ({symbol}) 获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取历史评分数据 ({symbol}) 失败: {e}")
            return None


    async def get_stock_comment_detail_scrd_focus_em(self, symbol: str = "600000") -> Optional[pd.DataFrame]:
        """
        获取用户关注指数数据
        
        Args:
            symbol: 股票代码，默认 "600000"
            
        Returns:
            用户关注指数DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info(f"📊 获取用户关注指数数据 ({symbol})...")
            
            def fetch_focus_data():
                return self.ak.stock_comment_detail_scrd_focus_em(symbol=symbol)
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_focus_data)
            
            if df is None or df.empty:
                logger.warning(f"⚠️ 用户关注指数数据 ({symbol}) 为空")
                return None
            
            logger.info(f"✅ 用户关注指数数据 ({symbol}) 获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取用户关注指数数据 ({symbol}) 失败: {e}")
            return None


    async def get_stock_comment_detail_scrd_desire_em(self, symbol: str = "600000") -> Optional[pd.DataFrame]:
        """
        获取市场参与意愿数据
        
        Args:
            symbol: 股票代码，默认 "600000"
            
        Returns:
            市场参与意愿 DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info(f"📊 获取市场参与意愿数据 ({symbol})...")
            
            def fetch_desire_data():
                return self.ak.stock_comment_detail_scrd_desire_em(symbol=symbol)
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_desire_data)
            
            if df is None or df.empty:
                logger.warning(f"⚠️ 市场参与意愿数据 ({symbol}) 为空")
                return None
            
            logger.info(f"✅ 市场参与意愿数据 ({symbol}) 获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取市场参与意愿数据 ({symbol}) 失败: {e}")
            return None


    async def get_stock_comment_detail_scrd_desire_daily_em(self, symbol: str = "600000") -> Optional[pd.DataFrame]:
        """
        获取日度市场参与意愿数据
        
        Args:
            symbol: 股票代码，默认 "600000"
            
        Returns:
            日度市场参与意愿 DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info(f"📊 获取日度市场参与意愿数据 ({symbol})...")
            
            def fetch_desire_daily_data():
                return self.ak.stock_comment_detail_scrd_desire_daily_em(symbol=symbol)
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_desire_daily_data)
            
            if df is None or df.empty:
                logger.warning(f"⚠️ 日度市场参与意愿数据 ({symbol}) 为空")
                return None
            
            logger.info(f"✅ 日度市场参与意愿数据 ({symbol}) 获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取日度市场参与意愿数据 ({symbol}) 失败: {e}")
            return None


    async def get_stock_hsgt_fund_flow_summary_em(self) -> Optional[pd.DataFrame]:
        """
        获取沪深港通资金流向数据
        
        Returns:
            沪深港通资金流向 DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info("📊 获取沪深港通资金流向数据...")
            
            def fetch_hsgt_data():
                return self.ak.stock_hsgt_fund_flow_summary_em()
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_hsgt_data)
            
            if df is None or df.empty:
                logger.warning("⚠️ 沪深港通资金流向数据为空")
                return None
            
            logger.info(f"✅ 沪深港通资金流向数据获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取沪深港通资金流向数据失败: {e}")
            return None


    async def get_stock_sgt_settlement_exchange_rate_szse(self) -> Optional[pd.DataFrame]:
        """
        获取结算汇率-深港通数据
        
        Returns:
            结算汇率-深港通 DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info("📊 获取结算汇率-深港通数据...")
            
            def fetch_sgt_rate():
                return self.ak.stock_sgt_settlement_exchange_rate_szse()
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_sgt_rate)
            
            if df is None or df.empty:
                logger.warning("⚠️ 结算汇率-深港通数据为空")
                return None
            
            logger.info(f"✅ 结算汇率-深港通数据获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取结算汇率-深港通数据失败: {e}")
            return None


    async def get_stock_sgt_settlement_exchange_rate_sse(self) -> Optional[pd.DataFrame]:
        """
        获取结算汇率-沪港通数据
        
        Returns:
            结算汇率-沪港通 DataFrame
        """
        if not self.connected:
            logger.error("❌ AKShare未连接")
            return None
        
        try:
            logger.info("📊 获取结算汇率-沪港通数据...")
            
            def fetch_sse_rate():
                return self.ak.stock_sgt_settlement_exchange_rate_sse()
            
            # 异步调用AKShare接口
            df = await asyncio.to_thread(fetch_sse_rate)
            
            if df is None or df.empty:
                logger.warning("⚠️ 结算汇率-沪港通数据为空")
                return None
            
            logger.info(f"✅ 结算汇率-沪港通数据获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取结算汇率-沪港通数据失败: {e}")
            return None

    async def get_stock_sgt_reference_exchange_rate_szse(self) -> Optional[pd.DataFrame]:
        """
        获取参考汇率-深港通数据 (需求107)
        
        接口: stock_sgt_reference_exchange_rate_szse
        描述: 深港通-港股通业务信息-参考汇率
        
        Returns:
            DataFrame: 参考汇率数据，包含字段：
                - 适用日期
                - 参考汇率买入价
                - 参考汇率卖出价
                - 货币种类
        """
        try:
            logger.info("🔍 开始获取参考汇率-深港通数据...")
            
            if not self.connected:
                logger.error("❌ AKShare未连接")
                return None
            
            # 调用akshare接口
            df = await asyncio.to_thread(
                self.ak.stock_sgt_reference_exchange_rate_szse
            )
            
            if df is None or df.empty:
                logger.warning("⚠️ 参考汇率-深港通数据为空")
                return None
            
            logger.info(f"✅ 参考汇率-深港通数据获取成功: {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取参考汇率-深港通数据失败: {e}")
            return None

    async def get_stock_sgt_reference_exchange_rate_sse(self) -> Optional[pd.DataFrame]:
        """获取参考汇率-沪港通数据 (需求108)"""
        try:
            logger.info("🔍 开始获取参考汇率-沪港通数据...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_sgt_reference_exchange_rate_sse)
            if df is None or df.empty:
                logger.warning("⚠️ 参考汇率-沪港通数据为空")
                return None
            logger.info(f"✅ 参考汇率-沪港通数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取参考汇率-沪港通数据失败: {e}")
            return None

    async def get_stock_hk_ggt_components_em(self) -> Optional[pd.DataFrame]:
        """获取港股通成份股数据 (需求109)"""
        try:
            logger.info("🔍 开始获取港股通成份股数据...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_hk_ggt_components_em)
            if df is None or df.empty:
                logger.warning("⚠️ 港股通成份股数据为空")
                return None
            logger.info(f"✅ 港股通成份股数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取港股通成份股数据失败: {e}")
            return None

    async def get_stock_hsgt_fund_min_em(self) -> Optional[pd.DataFrame]:
        """获取沪深港通分时数据 (需求110)"""
        try:
            logger.info("🔍 开始获取沪深港通分时数据...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_hsgt_fund_min_em)
            if df is None or df.empty:
                logger.warning("⚠️ 沪深港通分时数据为空")
                return None
            logger.info(f"✅ 沪深港通分时数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取沪深港通分时数据失败: {e}")
            return None

    async def get_stock_hsgt_board_rank_em(self, symbol: str = "北向") -> Optional[pd.DataFrame]:
        """获取板块排行数据 (需求111)"""
        try:
            logger.info(f"🔍 开始获取板块排行数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_hsgt_board_rank_em, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 板块排行数据为空")
                return None
            logger.info(f"✅ 板块排行数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取板块排行数据失败: {e}")
            return None

    async def get_stock_hsgt_hold_stock_em(self, symbol: str = "北向", indicator: str = "今日排行") -> Optional[pd.DataFrame]:
        """获取个股排行数据 (需求112)"""
        try:
            logger.info(f"🔍 开始获取个股排行数据: {symbol}-{indicator}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_hsgt_hold_stock_em, symbol=symbol, indicator=indicator)
            if df is None or df.empty:
                logger.warning("⚠️ 个股排行数据为空")
                return None
            logger.info(f"✅ 个股排行数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取个股排行数据失败: {e}")
            return None

    async def get_stock_hsgt_stock_statistics_em(self, symbol: str = "600519", start_date: str = "20210101", end_date: str = "20231231") -> Optional[pd.DataFrame]:
        """获取每日个股统计数据 (需求113)"""
        try:
            logger.info(f"🔍 开始获取每日个股统计数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_hsgt_stock_statistics_em, symbol=symbol, start_date=start_date, end_date=end_date)
            if df is None or df.empty:
                logger.warning("⚠️ 每日个股统计数据为空")
                return None
            logger.info(f"✅ 每日个股统计数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取每日个股统计数据失败: {e}")
            return None

    async def get_stock_hsgt_institution_statistics_em(self, symbol: str = "北向", start_date: str = "20210101", end_date: str = "20231231") -> Optional[pd.DataFrame]:
        """获取机构排行数据 (需求114)"""
        try:
            logger.info(f"🔍 开始获取机构排行数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_hsgt_institution_statistics_em, symbol=symbol, start_date=start_date, end_date=end_date)
            if df is None or df.empty:
                logger.warning("⚠️ 机构排行数据为空")
                return None
            logger.info(f"✅ 机构排行数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取机构排行数据失败: {e}")
            return None

    async def get_stock_hsgt_sh_hk_spot_em(self) -> Optional[pd.DataFrame]:
        """获取沪深港通-港股通(沪>港)实时行情数据 (需求115)"""
        try:
            logger.info("🔍 开始获取港股通(沪>港)实时行情数据...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_hsgt_sh_hk_spot_em)
            if df is None or df.empty:
                logger.warning("⚠️ 港股通实时行情数据为空")
                return None
            logger.info(f"✅ 港股通实时行情数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取港股通实时行情数据失败: {e}")
            return None

    async def get_stock_hsgt_hist_em(self, symbol: str = "沪股通") -> Optional[pd.DataFrame]:
        """获取沪深港通历史数据 (需求116)"""
        try:
            logger.info(f"🔍 开始获取沪深港通历史数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_hsgt_hist_em, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 沪深港通历史数据为空")
                return None
            logger.info(f"✅ 沪深港通历史数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取沪深港通历史数据失败: {e}")
            return None

    async def get_stock_hsgt_individual_em(self, symbol: str = "600519") -> Optional[pd.DataFrame]:
        """获取沪深港通持股-个股数据 (需求117)"""
        try:
            logger.info(f"🔍 开始获取沪深港通持股-个股数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_hsgt_individual_em, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 沪深港通持股-个股数据为空")
                return None
            logger.info(f"✅ 沪深港通持股-个股数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取沪深港通持股-个股数据失败: {e}")
            return None

    async def get_stock_hsgt_individual_detail_em(self, symbol: str = "600519", start_date: str = "20210101", end_date: str = "20231231") -> Optional[pd.DataFrame]:
        """获取沪深港通持股-个股详情数据 (需求118)"""
        try:
            logger.info(f"🔍 开始获取沪深港通持股-个股详情数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_hsgt_individual_detail_em, symbol=symbol, start_date=start_date, end_date=end_date)
            if df is None or df.empty:
                logger.warning("⚠️ 沪深港通持股-个股详情数据为空")
                return None
            logger.info(f"✅ 沪深港通持股-个股详情数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取沪深港通持股-个股详情数据失败: {e}")
            return None

    async def get_stock_em_hsgt_north_net_flow_in(self, indicator: str = "沪股通") -> Optional[pd.DataFrame]:
        """获取北向资金流入数据 (需求119)"""
        try:
            logger.info(f"🔍 开始获取北向资金流入数据: {indicator}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_em_hsgt_north_net_flow_in, indicator=indicator)
            if df is None or df.empty:
                logger.warning("⚠️ 北向资金流入数据为空")
                return None
            logger.info(f"✅ 北向资金流入数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取北向资金流入数据失败: {e}")
            return None

    async def get_stock_em_hsgt_south_net_flow_in(self, indicator: str = "港股通(沪)") -> Optional[pd.DataFrame]:
        """获取南向资金流入数据 (需求120)"""
        try:
            logger.info(f"🔍 开始获取南向资金流入数据: {indicator}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_em_hsgt_south_net_flow_in, indicator=indicator)
            if df is None or df.empty:
                logger.warning("⚠️ 南向资金流入数据为空")
                return None
            logger.info(f"✅ 南向资金流入数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取南向资金流入数据失败: {e}")
            return None

    async def get_news_trade_notify_dividend_baidu(self) -> Optional[pd.DataFrame]:
        """获取分红派息数据 (需求121)"""
        try:
            logger.info("🔍 开始获取分红派息数据...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.news_trade_notify_dividend_baidu)
            if df is None or df.empty:
                logger.warning("⚠️ 分红派息数据为空")
                return None
            logger.info(f"✅ 分红派息数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取分红派息数据失败: {e}")
            return None

    async def get_stock_news_em(self, symbol: str = "300059") -> Optional[pd.DataFrame]:
        """获取个股新闻数据 (需求122)"""
        try:
            logger.info(f"🔍 开始获取个股新闻数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_news_em, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 个股新闻数据为空")
                return None
            logger.info(f"✅ 个股新闻数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取个股新闻数据失败: {e}")
            return None

    async def get_stock_news_main_cx(self) -> Optional[pd.DataFrame]:
        """获取财经内容精选数据 (需求123)"""
        try:
            logger.info("🔍 开始获取财经内容精选数据...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_news_main_cx)
            if df is None or df.empty:
                logger.warning("⚠️ 财经内容精选数据为空")
                return None
            logger.info(f"✅ 财经内容精选数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取财经内容精选数据失败: {e}")
            return None

    async def get_news_report_time_baidu(self) -> Optional[pd.DataFrame]:
        """获取财报发行数据 (需求124)"""
        try:
            logger.info("🔍 开始获取财报发行数据...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.news_report_time_baidu)
            if df is None or df.empty:
                logger.warning("⚠️ 财报发行数据为空")
                return None
            logger.info(f"✅ 财报发行数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取财报发行数据失败: {e}")
            return None

    async def get_stock_dxsyl_em(self) -> Optional[pd.DataFrame]:
        """获取打新收益率数据 (需求125)"""
        try:
            logger.info("🔍 开始获取打新收益率数据...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_dxsyl_em)
            if df is None or df.empty:
                logger.warning("⚠️ 打新收益率数据为空")
                return None
            logger.info(f"✅ 打新收益率数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取打新收益率数据失败: {e}")
            return None

    async def get_stock_xgsglb_em(self) -> Optional[pd.DataFrame]:
        """获取新股申购与中签数据 (需求126)"""
        try:
            logger.info("🔍 开始获取新股申购与中签数据...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_xgsglb_em)
            if df is None or df.empty:
                logger.warning("⚠️ 新股申购与中签数据为空")
                return None
            logger.info(f"✅ 新股申购与中签数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取新股申购与中签数据失败: {e}")
            return None

    async def get_stock_yjbb_em(self, date: str = "20231231") -> Optional[pd.DataFrame]:
        """获取业绩报表数据 (需求127)"""
        try:
            logger.info(f"🔍 开始获取业绩报表数据: {date}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_yjbb_em, date=date)
            if df is None or df.empty:
                logger.warning("⚠️ 业绩报表数据为空")
                return None
            logger.info(f"✅ 业绩报表数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取业绩报表数据失败: {e}")
            return None

    async def get_stock_yjkb_em(self, date: str = "20231231") -> Optional[pd.DataFrame]:
        """获取业绩快报数据 (需求128)"""
        try:
            logger.info(f"🔍 开始获取业绩快报数据: {date}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_yjkb_em, date=date)
            if df is None or df.empty:
                logger.warning("⚠️ 业绩快报数据为空")
                return None
            logger.info(f"✅ 业绩快报数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取业绩快报数据失败: {e}")
            return None

    async def get_stock_yjyg_em(self) -> Optional[pd.DataFrame]:
        """获取业绩预告数据 (需求129)"""
        try:
            logger.info("🔍 开始获取业绩预告数据...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_yjyg_em)
            if df is None or df.empty:
                logger.warning("⚠️ 业绩预告数据为空")
                return None
            logger.info(f"✅ 业绩预告数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取业绩预告数据失败: {e}")
            return None

    async def get_stock_yysj_em(self) -> Optional[pd.DataFrame]:
        """获取营业收入数据 (需求130)"""
        try:
            logger.info("🔍 开始获取营业收入数据...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_yysj_em)
            if df is None or df.empty:
                logger.warning("⚠️ 营业收入数据为空")
                return None
            logger.info(f"✅ 营业收入数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取营业收入数据失败: {e}")
            return None

    async def get_stock_report_disclosure(self) -> Optional[pd.DataFrame]:
        """获取报告披露数据 (需求131)"""
        try:
            logger.info("🔍 开始获取报告披露数据...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_report_disclosure)
            if df is None or df.empty:
                logger.warning("⚠️ 报告披露数据为空")
                return None
            logger.info(f"✅ 报告披露数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取报告披露数据失败: {e}")
            return None

    async def get_stock_zh_a_disclosure_report_cninfo(self, symbol: str = "深市主板", date: str = "20231231") -> Optional[pd.DataFrame]:
        """获取信息披露报告数据 (需求132)"""
        try:
            logger.info(f"🔍 开始获取信息披露报告数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_zh_a_disclosure_report_cninfo, symbol=symbol, date=date)
            if df is None or df.empty:
                logger.warning("⚠️ 信息披露报告数据为空")
                return None
            logger.info(f"✅ 信息披露报告数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取信息披露报告数据失败: {e}")
            return None

    async def get_stock_zh_a_disclosure_relation_cninfo(self, symbol: str = "000001") -> Optional[pd.DataFrame]:
        """获取关联方披露数据 (需求133)"""
        try:
            logger.info(f"🔍 开始获取关联方披露数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_zh_a_disclosure_relation_cninfo, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 关联方披露数据为空")
                return None
            logger.info(f"✅ 关联方披露数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取关联方披露数据失败: {e}")
            return None

    async def get_stock_industry_category_cninfo(self, symbol: str = "巨潮行业分类标准") -> Optional[pd.DataFrame]:
        """获取行业分类数据 (需求134)"""
        try:
            logger.info(f"🔍 开始获取行业分类数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_industry_category_cninfo, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 行业分类数据为空")
                return None
            logger.info(f"✅ 行业分类数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取行业分类数据失败: {e}")
            return None

    async def get_stock_industry_change_cninfo(self, symbol: str = "000001", start_date: str = "20200101", end_date: str = "20231231") -> Optional[pd.DataFrame]:
        """获取行业变更数据 (需求135)"""
        try:
            logger.info(f"🔍 开始获取行业变更数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_industry_change_cninfo, symbol=symbol, start_date=start_date, end_date=end_date)
            if df is None or df.empty:
                logger.warning("⚠️ 行业变更数据为空")
                return None
            logger.info(f"✅ 行业变更数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取行业变更数据失败: {e}")
            return None

    async def get_stock_share_change_cninfo(self, symbol: str = "000001", start_date: str = "20200101", end_date: str = "20231231") -> Optional[pd.DataFrame]:
        """获取股本变动数据 (需求136)"""
        try:
            logger.info(f"🔍 开始获取股本变动数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_share_change_cninfo, symbol=symbol, start_date=start_date, end_date=end_date)
            if df is None or df.empty:
                logger.warning("⚠️ 股本变动数据为空")
                return None
            logger.info(f"✅ 股本变动数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取股本变动数据失败: {e}")
            return None

    async def get_stock_allotment_cninfo(self, symbol: str = "000001") -> Optional[pd.DataFrame]:
        """获取配股数据 (需求137)"""
        try:
            logger.info(f"🔍 开始获取配股数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_allotment_cninfo, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 配股数据为空")
                return None
            logger.info(f"✅ 配股数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取配股数据失败: {e}")
            return None

    async def get_stock_profile_cninfo(self, symbol: str = "000001") -> Optional[pd.DataFrame]:
        """获取公司概况数据 (需求138)"""
        try:
            logger.info(f"🔍 开始获取公司概况数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_profile_cninfo, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 公司概况数据为空")
                return None
            logger.info(f"✅ 公司概况数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取公司概况数据失败: {e}")
            return None

    async def get_stock_ipo_summary_cninfo(self) -> Optional[pd.DataFrame]:
        """获取IPO摘要数据 (需求139)"""
        try:
            logger.info("🔍 开始获取IPO摘要数据...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_ipo_summary_cninfo)
            if df is None or df.empty:
                logger.warning("⚠️ IPO摘要数据为空")
                return None
            logger.info(f"✅ IPO摘要数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取IPO摘要数据失败: {e}")
            return None

    async def get_stock_ipo_info_cninfo(self, symbol: str = "000001") -> Optional[pd.DataFrame]:
        """获取IPO信息数据 (需求140)"""
        try:
            logger.info(f"🔍 开始获取IPO信息数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_ipo_info_cninfo, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ IPO信息数据为空")
                return None
            logger.info(f"✅ IPO信息数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取IPO信息数据失败: {e}")
            return None

    async def get_stock_zcfz_em(self, symbol: str = "20231231") -> Optional[pd.DataFrame]:
        """获取资产负债表数据 (需求141)"""
        try:
            logger.info(f"🔍 开始获取资产负债表数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_zcfz_em, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 资产负债表数据为空")
                return None
            logger.info(f"✅ 资产负债表数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取资产负债表数据失败: {e}")
            return None

    async def get_stock_lrb_em(self, symbol: str = "20231231") -> Optional[pd.DataFrame]:
        """获取利润表数据 (需求142)"""
        try:
            logger.info(f"🔍 开始获取利润表数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_lrb_em, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 利润表数据为空")
                return None
            logger.info(f"✅ 利润表数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取利润表数据失败: {e}")
            return None

    async def get_stock_xjll_em(self, symbol: str = "20231231") -> Optional[pd.DataFrame]:
        """获取现金流量表数据 (需求143)"""
        try:
            logger.info(f"🔍 开始获取现金流量表数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_xjll_em, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 现金流量表数据为空")
                return None
            logger.info(f"✅ 现金流量表数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取现金流量表数据失败: {e}")
            return None

    async def get_stock_cwbbzy_em(self, symbol: str = "600519") -> Optional[pd.DataFrame]:
        """获取主要指标数据 (需求144)"""
        try:
            logger.info(f"🔍 开始获取主要指标数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_cwbbzy_em, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 主要指标数据为空")
                return None
            logger.info(f"✅ 主要指标数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取主要指标数据失败: {e}")
            return None

    async def get_stock_yjkb_em_v2(self, date: str = "20231231") -> Optional[pd.DataFrame]:
        """获取业绩快报V2数据 (需求145)"""
        try:
            logger.info(f"🔍 开始获取业绩快报V2数据: {date}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_yjkb_em, date=date)
            if df is None or df.empty:
                logger.warning("⚠️ 业绩快报V2数据为空")
                return None
            logger.info(f"✅ 业绩快报V2数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取业绩快报V2数据失败: {e}")
            return None

    async def get_stock_profit_forecast_em(self, symbol: str = "600519") -> Optional[pd.DataFrame]:
        """获取盈利预测数据 (需求146)"""
        try:
            logger.info(f"🔍 开始获取盈利预测数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_profit_forecast_em, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 盈利预测数据为空")
                return None
            logger.info(f"✅ 盈利预测数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取盈利预测数据失败: {e}")
            return None

    async def get_stock_fhps_detail_ths(self, symbol: str = "600519") -> Optional[pd.DataFrame]:
        """获取分红派送详情数据 (需求147)"""
        try:
            logger.info(f"🔍 开始获取分红派送详情数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_fhps_detail_ths, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 分红派送详情数据为空")
                return None
            logger.info(f"✅ 分红派送详情数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取分红派送详情数据失败: {e}")
            return None

    async def get_stock_hk_fhpx_detail_ths(self, symbol: str = "00700") -> Optional[pd.DataFrame]:
        """获取港股分红派息数据 (需求148)"""
        try:
            logger.info(f"🔍 开始获取港股分红派息数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_hk_fhpx_detail_ths, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 港股分红派息数据为空")
                return None
            logger.info(f"✅ 港股分红派息数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取港股分红派息数据失败: {e}")
            return None

    async def get_stock_fund_flow_individual(self, symbol: str = "000001") -> Optional[pd.DataFrame]:
        """获取个股资金流向数据 (需求149)"""
        try:
            logger.info(f"🔍 开始获取个股资金流向数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_fund_flow_individual, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 个股资金流向数据为空")
                return None
            logger.info(f"✅ 个股资金流向数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取个股资金流向数据失败: {e}")
            return None

    async def get_stock_fund_flow_concept(self, symbol: str = "数字货币") -> Optional[pd.DataFrame]:
        """获取概念资金流向数据 (需求150)"""
        try:
            logger.info(f"🔍 开始获取概念资金流向数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_fund_flow_concept, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 概念资金流向数据为空")
                return None
            logger.info(f"✅ 概念资金流向数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取概念资金流向数据失败: {e}")
            return None

    async def get_stock_fund_flow_industry(self, symbol: str = "电子信息") -> Optional[pd.DataFrame]:
        """获取行业资金流向数据 (需求151)"""
        try:
            logger.info(f"🔍 开始获取行业资金流向数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_fund_flow_industry, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 行业资金流向数据为空")
                return None
            logger.info(f"✅ 行业资金流向数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取行业资金流向数据失败: {e}")
            return None

    async def get_stock_fund_flow_big_deal(self, symbol: str = "全部") -> Optional[pd.DataFrame]:
        """获取大单资金流向数据 (需求152)"""
        try:
            logger.info(f"🔍 开始获取大单资金流向数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_fund_flow_big_deal, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 大单资金流向数据为空")
                return None
            logger.info(f"✅ 大单资金流向数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取大单资金流向数据失败: {e}")
            return None

    async def get_stock_individual_fund_flow(self, symbol: str = "000001", market: str = "sz") -> Optional[pd.DataFrame]:
        """获取个股历史资金流向数据 (需求153)"""
        try:
            logger.info(f"🔍 开始获取个股历史资金流向数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_individual_fund_flow, symbol=symbol, market=market)
            if df is None or df.empty:
                logger.warning("⚠️ 个股历史资金流向数据为空")
                return None
            logger.info(f"✅ 个股历史资金流向数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取个股历史资金流向数据失败: {e}")
            return None

    async def get_stock_individual_fund_flow_rank(self, indicator: str = "今日排行") -> Optional[pd.DataFrame]:
        """获取个股资金流排名数据 (需求154)"""
        try:
            logger.info(f"🔍 开始获取个股资金流排名数据: {indicator}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_individual_fund_flow_rank, indicator=indicator)
            if df is None or df.empty:
                logger.warning("⚠️ 个股资金流排名数据为空")
                return None
            logger.info(f"✅ 个股资金流排名数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取个股资金流排名数据失败: {e}")
            return None

    async def get_stock_market_fund_flow(self) -> Optional[pd.DataFrame]:
        """获取市场资金流向数据 (需求155)"""
        try:
            logger.info("🔍 开始获取市场资金流向数据...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_market_fund_flow)
            if df is None or df.empty:
                logger.warning("⚠️ 市场资金流向数据为空")
                return None
            logger.info(f"✅ 市场资金流向数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取市场资金流向数据失败: {e}")
            return None

    async def get_stock_sector_fund_flow_rank(self, indicator: str = "今日排行", sector_type: str = "行业资金流") -> Optional[pd.DataFrame]:
        """获取板块资金流排名数据 (需求156)"""
        try:
            logger.info(f"🔍 开始获取板块资金流排名数据: {indicator}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_sector_fund_flow_rank, indicator=indicator, sector_type=sector_type)
            if df is None or df.empty:
                logger.warning("⚠️ 板块资金流排名数据为空")
                return None
            logger.info(f"✅ 板块资金流排名数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取板块资金流排名数据失败: {e}")
            return None

    async def get_stock_main_fund_flow(self) -> Optional[pd.DataFrame]:
        """获取主力资金流向数据 (需求157)"""
        try:
            logger.info("🔍 开始获取主力资金流向数据...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_main_fund_flow)
            if df is None or df.empty:
                logger.warning("⚠️ 主力资金流向数据为空")
                return None
            logger.info(f"✅ 主力资金流向数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取主力资金流向数据失败: {e}")
            return None

    async def get_stock_sector_fund_flow_summary(self) -> Optional[pd.DataFrame]:
        """获取板块资金流汇总数据 (需求158)"""
        try:
            logger.info("🔍 开始获取板块资金流汇总数据...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_sector_fund_flow_summary)
            if df is None or df.empty:
                logger.warning("⚠️ 板块资金流汇总数据为空")
                return None
            logger.info(f"✅ 板块资金流汇总数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取板块资金流汇总数据失败: {e}")
            return None

    async def get_stock_sector_fund_flow_hist(self, symbol: str = "电子信息") -> Optional[pd.DataFrame]:
        """获取板块历史资金流向数据 (需求159)"""
        try:
            logger.info(f"🔍 开始获取板块历史资金流向数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_sector_fund_flow_hist, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 板块历史资金流向数据为空")
                return None
            logger.info(f"✅ 板块历史资金流向数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取板块历史资金流向数据失败: {e}")
            return None

    async def get_stock_concept_fund_flow_hist(self, symbol: str = "数字货币") -> Optional[pd.DataFrame]:
        """获取概念历史资金流向数据 (需求160)"""
        try:
            logger.info(f"🔍 开始获取概念历史资金流向数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_concept_fund_flow_hist, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 概念历史资金流向数据为空")
                return None
            logger.info(f"✅ 概念历史资金流向数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取概念历史资金流向数据失败: {e}")
            return None

    async def get_stock_cyq_em(self, symbol: str = "000001") -> Optional[pd.DataFrame]:
        """获取筹码分布数据 (需求161)"""
        try:
            logger.info(f"🔍 开始获取筹码分布数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_cyq_em, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 筹码分布数据为空")
                return None
            logger.info(f"✅ 筹码分布数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取筹码分布数据失败: {e}")
            return None

    async def get_stock_gddh_em(self, symbol: str = "600519") -> Optional[pd.DataFrame]:
        """获取股东大会数据 (需求162)"""
        try:
            logger.info(f"🔍 开始获取股东大会数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_gddh_em, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 股东大会数据为空")
                return None
            logger.info(f"✅ 股东大会数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取股东大会数据失败: {e}")
            return None

    async def get_stock_zdhtmx_em(self, symbol: str = "600519") -> Optional[pd.DataFrame]:
        """获取重大合同明细数据 (需求163)"""
        try:
            logger.info(f"🔍 开始获取重大合同明细数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_zdhtmx_em, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 重大合同明细数据为空")
                return None
            logger.info(f"✅ 重大合同明细数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取重大合同明细数据失败: {e}")
            return None

    async def get_stock_research_report_em(self, symbol: str = "600519") -> Optional[pd.DataFrame]:
        """获取研究报告数据 (需求164)"""
        try:
            logger.info(f"🔍 开始获取研究报告数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_research_report_em, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 研究报告数据为空")
                return None
            logger.info(f"✅ 研究报告数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取研究报告数据失败: {e}")
            return None

    async def get_stock_notice_report(self, symbol: str = "600519") -> Optional[pd.DataFrame]:
        """获取公告报告数据 (需求165)"""
        try:
            logger.info(f"🔍 开始获取公告报告数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_notice_report, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 公告报告数据为空")
                return None
            logger.info(f"✅ 公告报告数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取公告报告数据失败: {e}")
            return None

    async def get_stock_financial_report_sina(self, symbol: str = "sh600519", indicator: str = "利润表") -> Optional[pd.DataFrame]:
        """获取财务报告数据-新浪 (需求166)"""
        try:
            logger.info(f"🔍 开始获取财务报告数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_financial_report_sina, symbol=symbol, indicator=indicator)
            if df is None or df.empty:
                logger.warning("⚠️ 财务报告数据为空")
                return None
            logger.info(f"✅ 财务报告数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取财务报告数据失败: {e}")
            return None

    async def get_stock_balance_sheet_by_report_em(self, symbol: str = "600519") -> Optional[pd.DataFrame]:
        """获取资产负债表-按报告期数据 (需求167)"""
        try:
            logger.info(f"🔍 开始获取资产负债表-按报告期数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_balance_sheet_by_report_em, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 资产负债表数据为空")
                return None
            logger.info(f"✅ 资产负债表数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取资产负债表数据失败: {e}")
            return None

    async def get_stock_balance_sheet_by_yearly_em(self, symbol: str = "600519") -> Optional[pd.DataFrame]:
        """获取资产负债表-按年度数据 (需求168)"""
        try:
            logger.info(f"🔍 开始获取资产负债表-按年度数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_balance_sheet_by_yearly_em, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 资产负债表-按年度数据为空")
                return None
            logger.info(f"✅ 资产负债表-按年度数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取资产负债表-按年度数据失败: {e}")
            return None

    async def get_stock_profit_sheet_by_report_em(self, symbol: str = "600519") -> Optional[pd.DataFrame]:
        """获取利润表-按报告期数据 (需求169)"""
        try:
            logger.info(f"🔍 开始获取利润表-按报告期数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_profit_sheet_by_report_em, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 利润表数据为空")
                return None
            logger.info(f"✅ 利润表数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取利润表数据失败: {e}")
            return None

    async def get_stock_profit_sheet_by_quarterly_em(self, symbol: str = "600519") -> Optional[pd.DataFrame]:
        """获取利润表-按季度数据 (需求170)"""
        try:
            logger.info(f"🔍 开始获取利润表-按季度数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_profit_sheet_by_quarterly_em, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 利润表-按季度数据为空")
                return None
            logger.info(f"✅ 利润表-按季度数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取利润表-按季度数据失败: {e}")
            return None

    async def get_stock_profit_sheet_by_yearly_em(self, symbol: str = "600519") -> Optional[pd.DataFrame]:
        """获取利润表-按年度数据 (需求171)"""
        try:
            logger.info(f"🔍 开始获取利润表-按年度数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_profit_sheet_by_yearly_em, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 利润表-按年度数据为空")
                return None
            logger.info(f"✅ 利润表-按年度数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取利润表-按年度数据失败: {e}")
            return None

    async def get_stock_cash_flow_sheet_by_report_em(self, symbol: str = "600519") -> Optional[pd.DataFrame]:
        """获取现金流量表-按报告期数据 (需求172)"""
        try:
            logger.info(f"🔍 开始获取现金流量表-按报告期数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_cash_flow_sheet_by_report_em, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 现金流量表数据为空")
                return None
            logger.info(f"✅ 现金流量表数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取现金流量表数据失败: {e}")
            return None

    async def get_stock_cash_flow_sheet_by_yearly_em(self, symbol: str = "600519") -> Optional[pd.DataFrame]:
        """获取现金流量表-按年度数据 (需求173)"""
        try:
            logger.info(f"🔍 开始获取现金流量表-按年度数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_cash_flow_sheet_by_yearly_em, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 现金流量表-按年度数据为空")
                return None
            logger.info(f"✅ 现金流量表-按年度数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取现金流量表-按年度数据失败: {e}")
            return None

    async def get_stock_cash_flow_sheet_by_quarterly_em(self, symbol: str = "600519") -> Optional[pd.DataFrame]:
        """获取现金流量表-按季度数据 (需求174)"""
        try:
            logger.info(f"🔍 开始获取现金流量表-按季度数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_cash_flow_sheet_by_quarterly_em, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 现金流量表-按季度数据为空")
                return None
            logger.info(f"✅ 现金流量表-按季度数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取现金流量表-按季度数据失败: {e}")
            return None

    async def get_stock_financial_debt_ths(self, symbol: str = "600519") -> Optional[pd.DataFrame]:
        """获取财务负债数据-同花顺 (需求175)"""
        try:
            logger.info(f"🔍 开始获取财务负债数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_financial_debt_ths, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 财务负债数据为空")
                return None
            logger.info(f"✅ 财务负债数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取财务负债数据失败: {e}")
            return None

    async def get_stock_financial_benefit_ths(self, symbol: str = "600519") -> Optional[pd.DataFrame]:
        """获取财务收益数据-同花顺 (需求176)"""
        try:
            logger.info(f"🔍 开始获取财务收益数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_financial_benefit_ths, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 财务收益数据为空")
                return None
            logger.info(f"✅ 财务收益数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取财务收益数据失败: {e}")
            return None

    async def get_stock_financial_cash_ths(self, symbol: str = "600519") -> Optional[pd.DataFrame]:
        """获取财务现金数据-同花顺 (需求177)"""
        try:
            logger.info(f"🔍 开始获取财务现金数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_financial_cash_ths, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 财务现金数据为空")
                return None
            logger.info(f"✅ 财务现金数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取财务现金数据失败: {e}")
            return None

    async def get_stock_balance_sheet_by_report_delisted_em(self, symbol: str = "000003") -> Optional[pd.DataFrame]:
        """获取退市公司资产负债表数据 (需求178)"""
        try:
            logger.info(f"🔍 开始获取退市公司资产负债表数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_balance_sheet_by_report_delisted_em, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 退市公司资产负债表数据为空")
                return None
            logger.info(f"✅ 退市公司资产负债表数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取退市公司资产负债表数据失败: {e}")
            return None

    async def get_stock_profit_sheet_by_report_delisted_em(self, symbol: str = "000003") -> Optional[pd.DataFrame]:
        """获取退市公司利润表数据 (需求179)"""
        try:
            logger.info(f"🔍 开始获取退市公司利润表数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_profit_sheet_by_report_delisted_em, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 退市公司利润表数据为空")
                return None
            logger.info(f"✅ 退市公司利润表数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取退市公司利润表数据失败: {e}")
            return None

    async def get_stock_cash_flow_sheet_by_report_delisted_em(self, symbol: str = "000003") -> Optional[pd.DataFrame]:
        """获取退市公司现金流量表数据 (需求180)"""
        try:
            logger.info(f"🔍 开始获取退市公司现金流量表数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_cash_flow_sheet_by_report_delisted_em, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 退市公司现金流量表数据为空")
                return None
            logger.info(f"✅ 退市公司现金流量表数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取退市公司现金流量表数据失败: {e}")
            return None

    async def get_stock_financial_hk_report_em(self, symbol: str = "00700", indicator: str = "资产负债表") -> Optional[pd.DataFrame]:
        """获取港股财务报告数据 (需求181)"""
        try:
            logger.info(f"🔍 开始获取港股财务报告数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_financial_hk_report_em, symbol=symbol, indicator=indicator)
            if df is None or df.empty:
                logger.warning("⚠️ 港股财务报告数据为空")
                return None
            logger.info(f"✅ 港股财务报告数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取港股财务报告数据失败: {e}")
            return None

    async def get_stock_financial_us_report_em(self, symbol: str = "AAPL", indicator: str = "资产负债表") -> Optional[pd.DataFrame]:
        """获取美股财务报告数据 (需求182)"""
        try:
            logger.info(f"🔍 开始获取美股财务报告数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_financial_us_report_em, symbol=symbol, indicator=indicator)
            if df is None or df.empty:
                logger.warning("⚠️ 美股财务报告数据为空")
                return None
            logger.info(f"✅ 美股财务报告数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取美股财务报告数据失败: {e}")
            return None

    async def get_stock_financial_abstract(self, symbol: str = "600519") -> Optional[pd.DataFrame]:
        """获取财务摘要数据 (需求183)"""
        try:
            logger.info(f"🔍 开始获取财务摘要数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_financial_abstract, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 财务摘要数据为空")
                return None
            logger.info(f"✅ 财务摘要数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取财务摘要数据失败: {e}")
            return None

    async def get_stock_financial_abstract_ths(self, symbol: str = "600519") -> Optional[pd.DataFrame]:
        """获取财务摘要数据-同花顺 (需求184)"""
        try:
            logger.info(f"🔍 开始获取财务摘要数据-同花顺: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_financial_abstract_ths, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 财务摘要数据-同花顺为空")
                return None
            logger.info(f"✅ 财务摘要数据-同花顺获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取财务摘要数据-同花顺失败: {e}")
            return None

    async def get_stock_financial_analysis_indicator_em(self, symbol: str = "600519") -> Optional[pd.DataFrame]:
        """获取财务分析指标数据 (需求185)"""
        try:
            logger.info(f"🔍 开始获取财务分析指标数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_financial_analysis_indicator_em, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 财务分析指标数据为空")
                return None
            logger.info(f"✅ 财务分析指标数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取财务分析指标数据失败: {e}")
            return None

    async def get_stock_financial_analysis_indicator(self, symbol: str = "sh600519") -> Optional[pd.DataFrame]:
        """获取财务分析指标数据-新浪 (需求186)"""
        try:
            logger.info(f"🔍 开始获取财务分析指标数据-新浪: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_financial_analysis_indicator, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 财务分析指标数据-新浪为空")
                return None
            logger.info(f"✅ 财务分析指标数据-新浪获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取财务分析指标数据-新浪失败: {e}")
            return None

    async def get_stock_financial_hk_analysis_indicator_em(self, symbol: str = "00700") -> Optional[pd.DataFrame]:
        """获取港股财务分析指标数据 (需求187)"""
        try:
            logger.info(f"🔍 开始获取港股财务分析指标数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_financial_hk_analysis_indicator_em, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 港股财务分析指标数据为空")
                return None
            logger.info(f"✅ 港股财务分析指标数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取港股财务分析指标数据失败: {e}")
            return None

    async def get_stock_financial_us_analysis_indicator_em(self, symbol: str = "AAPL") -> Optional[pd.DataFrame]:
        """获取美股财务分析指标数据 (需求188)"""
        try:
            logger.info(f"🔍 开始获取美股财务分析指标数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_financial_us_analysis_indicator_em, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 美股财务分析指标数据为空")
                return None
            logger.info(f"✅ 美股财务分析指标数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取美股财务分析指标数据失败: {e}")
            return None

    async def get_stock_history_dividend(self) -> Optional[pd.DataFrame]:
        """获取历史分红数据 (需求189)"""
        try:
            logger.info("🔍 开始获取历史分红数据...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_history_dividend)
            if df is None or df.empty:
                logger.warning("⚠️ 历史分红数据为空")
                return None
            logger.info(f"✅ 历史分红数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取历史分红数据失败: {e}")
            return None

    async def get_stock_gdfx_free_top_10_em(self, symbol: str = "600519", date: str = "20231231") -> Optional[pd.DataFrame]:
        """获取股东分析-前10大流通股东数据 (需求190)"""
        try:
            logger.info(f"🔍 开始获取前10大流通股东数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_gdfx_free_top_10_em, symbol=symbol, date=date)
            if df is None or df.empty:
                logger.warning("⚠️ 前10大流通股东数据为空")
                return None
            logger.info(f"✅ 前10大流通股东数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取前10大流通股东数据失败: {e}")
            return None

    async def get_stock_gdfx_top_10_em(self, symbol: str = "600519", date: str = "20231231") -> Optional[pd.DataFrame]:
        """获取股东分析-前10大股东数据 (需求191)"""
        try:
            logger.info(f"🔍 开始获取前10大股东数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_gdfx_top_10_em, symbol=symbol, date=date)
            if df is None or df.empty:
                logger.warning("⚠️ 前10大股东数据为空")
                return None
            logger.info(f"✅ 前10大股东数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取前10大股东数据失败: {e}")
            return None

    async def get_stock_gdfx_free_holding_change_em(self, symbol: str = "600519") -> Optional[pd.DataFrame]:
        """获取股东分析-流通股东持股变化数据 (需求192)"""
        try:
            logger.info(f"🔍 开始获取流通股东持股变化数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_gdfx_free_holding_change_em, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 流通股东持股变化数据为空")
                return None
            logger.info(f"✅ 流通股东持股变化数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取流通股东持股变化数据失败: {e}")
            return None

    async def get_stock_gdfx_holding_change_em(self, symbol: str = "600519") -> Optional[pd.DataFrame]:
        """获取股东分析-股东持股变化数据 (需求193)"""
        try:
            logger.info(f"🔍 开始获取股东持股变化数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_gdfx_holding_change_em, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 股东持股变化数据为空")
                return None
            logger.info(f"✅ 股东持股变化数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取股东持股变化数据失败: {e}")
            return None

    async def get_stock_management_change_ths(self, symbol: str = "600519") -> Optional[pd.DataFrame]:
        """获取高管变动数据 (需求194)"""
        try:
            logger.info(f"🔍 开始获取高管变动数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_management_change_ths, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 高管变动数据为空")
                return None
            logger.info(f"✅ 高管变动数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取高管变动数据失败: {e}")
            return None

    async def get_stock_shareholder_change_ths(self, symbol: str = "600519") -> Optional[pd.DataFrame]:
        """获取股东变动数据 (需求195)"""
        try:
            logger.info(f"🔍 开始获取股东变动数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_shareholder_change_ths, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 股东变动数据为空")
                return None
            logger.info(f"✅ 股东变动数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取股东变动数据失败: {e}")
            return None

    async def get_stock_gdfx_free_holding_analyse_em(self, symbol: str = "600519") -> Optional[pd.DataFrame]:
        """获取流通股东持股分析数据 (需求196)"""
        try:
            logger.info(f"🔍 开始获取流通股东持股分析数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_gdfx_free_holding_analyse_em, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 流通股东持股分析数据为空")
                return None
            logger.info(f"✅ 流通股东持股分析数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取流通股东持股分析数据失败: {e}")
            return None

    async def get_stock_gdfx_holding_analyse_em(self, symbol: str = "600519") -> Optional[pd.DataFrame]:
        """获取股东持股分析数据 (需求197)"""
        try:
            logger.info(f"🔍 开始获取股东持股分析数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_gdfx_holding_analyse_em, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 股东持股分析数据为空")
                return None
            logger.info(f"✅ 股东持股分析数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取股东持股分析数据失败: {e}")
            return None

    async def get_stock_gdfx_free_holding_detail_em(self, symbol: str = "600519") -> Optional[pd.DataFrame]:
        """获取流通股东持股明细数据 (需求198)"""
        try:
            logger.info(f"🔍 开始获取流通股东持股明细数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_gdfx_free_holding_detail_em, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 流通股东持股明细数据为空")
                return None
            logger.info(f"✅ 流通股东持股明细数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取流通股东持股明细数据失败: {e}")
            return None

    async def get_stock_gdfx_holding_detail_em(self, symbol: str = "600519") -> Optional[pd.DataFrame]:
        """获取股东持股明细数据 (需求199)"""
        try:
            logger.info(f"🔍 开始获取股东持股明细数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_gdfx_holding_detail_em, symbol=symbol)
            if df is None or df.empty:
                logger.warning("⚠️ 股东持股明细数据为空")
                return None
            logger.info(f"✅ 股东持股明细数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取股东持股明细数据失败: {e}")
            return None

    async def get_stock_history_dividend_detail(self, symbol: str = "600519", indicator: str = "分红") -> Optional[pd.DataFrame]:
        """获取历史分红详细数据 (需求200)"""
        try:
            logger.info(f"🔍 开始获取历史分红详细数据: {symbol}...")
            if not self.connected:
                return None
            df = await asyncio.to_thread(self.ak.stock_history_dividend_detail, symbol=symbol, indicator=indicator)
            if df is None or df.empty:
                logger.warning("⚠️ 历史分红详细数据为空")
                return None
            logger.info(f"✅ 历史分红详细数据获取成功: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"❌ 获取历史分红详细数据失败: {e}")
            return None


# 全局提供器实例
_akshare_provider = None


def get_akshare_provider() -> AKShareProvider:
    """获取全局AKShare提供器实例"""
    global _akshare_provider
    if _akshare_provider is None:
        _akshare_provider = AKShareProvider()
    return _akshare_provider
