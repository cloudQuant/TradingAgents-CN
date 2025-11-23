"""
期权数据服务
负责从akshare获取期权数据并存储到MongoDB
"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import pandas as pd
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import UpdateOne
import akshare as ak

logger = logging.getLogger("webapi")

class OptionDataService:
    """期权数据服务类"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.col_option_contract_info_ctp = db.get_collection("option_contract_info_ctp")
        self.col_option_finance_board = db.get_collection("option_finance_board")
        self.col_option_risk_indicator_sse = db.get_collection("option_risk_indicator_sse")
        self.col_option_current_day_sse = db.get_collection("option_current_day_sse")
        self.col_option_current_day_szse = db.get_collection("option_current_day_szse")
        self.col_option_daily_stats_sse = db.get_collection("option_daily_stats_sse")
        self.col_option_daily_stats_szse = db.get_collection("option_daily_stats_szse")
        self.col_option_cffex_sz50_list_sina = db.get_collection("option_cffex_sz50_list_sina")
        self.col_option_cffex_hs300_list_sina = db.get_collection("option_cffex_hs300_list_sina")
        self.col_option_cffex_zz1000_list_sina = db.get_collection("option_cffex_zz1000_list_sina")
        self.col_option_cffex_sz50_spot_sina = db.get_collection("option_cffex_sz50_spot_sina")
        self.col_option_cffex_hs300_spot_sina = db.get_collection("option_cffex_hs300_spot_sina")
        self.col_option_cffex_zz1000_spot_sina = db.get_collection("option_cffex_zz1000_spot_sina")
        self.col_option_cffex_sz50_daily_sina = db.get_collection("option_cffex_sz50_daily_sina")
        self.col_option_cffex_hs300_daily_sina = db.get_collection("option_cffex_hs300_daily_sina")
        self.col_option_cffex_zz1000_daily_sina = db.get_collection("option_cffex_zz1000_daily_sina")
        self.col_option_sse_list_sina = db.get_collection("option_sse_list_sina")
        self.col_option_sse_expire_day_sina = db.get_collection("option_sse_expire_day_sina")
        self.col_option_sse_codes_sina = db.get_collection("option_sse_codes_sina")
        self.col_option_current_em = db.get_collection("option_current_em")
        self.col_option_sse_underlying_spot_price_sina = db.get_collection("option_sse_underlying_spot_price_sina")
        self.col_option_sse_greeks_sina = db.get_collection("option_sse_greeks_sina")
        self.col_option_sse_minute_sina = db.get_collection("option_sse_minute_sina")
        self.col_option_sse_daily_sina = db.get_collection("option_sse_daily_sina")
        self.col_option_finance_minute_sina = db.get_collection("option_finance_minute_sina")
        self.col_option_minute_em = db.get_collection("option_minute_em")
        self.col_option_lhb_em = db.get_collection("option_lhb_em")
        self.col_option_value_analysis_em = db.get_collection("option_value_analysis_em")
        self.col_option_risk_analysis_em = db.get_collection("option_risk_analysis_em")
        self.col_option_premium_analysis_em = db.get_collection("option_premium_analysis_em")
        self.col_option_commodity_contract_sina = db.get_collection("option_commodity_contract_sina")
        self.col_option_commodity_contract_table_sina = db.get_collection("option_commodity_contract_table_sina")
        self.col_option_commodity_hist_sina = db.get_collection("option_commodity_hist_sina")
        self.col_option_comm_info = db.get_collection("option_comm_info")
        self.col_option_margin = db.get_collection("option_margin")
        self.col_option_hist_shfe = db.get_collection("option_hist_shfe")
        self.col_option_hist_dce = db.get_collection("option_hist_dce")
        self.col_option_hist_czce = db.get_collection("option_hist_czce")
        self.col_option_hist_gfex = db.get_collection("option_hist_gfex")
        self.col_option_vol_gfex = db.get_collection("option_vol_gfex")
        self.col_option_czce_hist = db.get_collection("option_czce_hist")
        
    async def save_option_contract_info_ctp(self, df: pd.DataFrame) -> int:
        """
        保存OpenCTP期权合约信息到MongoDB
        
        Args:
            df: 包含期权合约信息的DataFrame
            
        Returns:
            保存的记录数
        """
        if df.empty:
            return 0
            
        # 转换字段名 (假设DataFrame列名是中文，需要映射到英文)
        # 根据 requirements/01_openctp期权合约信息.md 的输出参数
        column_mapping = {
            "交易所ID": "exchange_id",
            "合约ID": "instrument_id",
            "合约名称": "instrument_name",
            "商品类别": "product_class",
            "品种ID": "product_id",
            "合约乘数": "volume_multiple",
            "最小变动价位": "price_tick",
            "做多保证金率": "long_margin_ratio",
            "做空保证金率": "short_margin_ratio",
            "做多保证金/手": "long_margin_per_lot",
            "做空保证金/手": "short_margin_per_lot",
            "开仓手续费率": "open_fee_ratio",
            "开仓手续费/手": "open_fee_per_lot",
            "平仓手续费率": "close_fee_ratio",
            "平仓手续费/手": "close_fee_per_lot",
            "平今手续费率": "close_today_fee_ratio",
            "平今手续费/手": "close_today_fee_per_lot",
            "交割年份": "delivery_year",
            "交割月份": "delivery_month",
            "上市日期": "create_date",
            "最后交易日": "expire_date",
            "交割日": "delivery_date",
            "标的合约ID": "underlying_instrument_id",
            "标的合约乘数": "underlying_multiple",
            "期权类型": "option_type",
            "行权价": "strike_price",
            "合约状态": "instrument_status"
        }
        
        # 重命名列
        df = df.rename(columns=column_mapping)
        
        # 添加更新时间
        df["updated_at"] = datetime.now()
        
        records = df.to_dict("records")
        operations = []
        
        for record in records:
            # 使用 exchange_id + instrument_id 作为唯一标识
            filter_query = {
                "exchange_id": record.get("exchange_id"),
                "instrument_id": record.get("instrument_id")
            }
            operations.append(
                UpdateOne(filter_query, {"$set": record}, upsert=True)
            )
            
        if operations:
            result = await self.col_option_contract_info_ctp.bulk_write(operations)
            return result.upserted_count + result.modified_count
        return 0

    async def fetch_and_save_option_contract_info_ctp(self) -> int:
        """
        获取并保存OpenCTP期权合约信息
        """
        try:
            logger.info("开始获取OpenCTP期权合约信息...")
            df = ak.option_contract_info_ctp()
            logger.info(f"获取到 {len(df)} 条OpenCTP期权合约信息")
            
            saved_count = await self.save_option_contract_info_ctp(df)
            logger.info(f"成功保存 {saved_count} 条OpenCTP期权合约信息")
            return saved_count
        except Exception as e:
            logger.error(f"获取OpenCTP期权合约信息失败: {str(e)}")
            raise e

    async def get_option_contract_info_ctp(
        self, 
        page: int = 1, 
        page_size: int = 20,
        keyword: str = None
    ) -> Dict[str, Any]:
        """
        查询OpenCTP期权合约信息
        """
        query = {}
        if keyword:
            query["$or"] = [
                {"instrument_id": {"$regex": keyword, "$options": "i"}},
                {"instrument_name": {"$regex": keyword, "$options": "i"}}
            ]
            
        total = await self.col_option_contract_info_ctp.count_documents(query)
        cursor = self.col_option_contract_info_ctp.find(query)
        
        cursor.sort("instrument_id", 1)
        cursor.skip((page - 1) * page_size).limit(page_size)
        
        items = await cursor.to_list(length=page_size)
        
        # 处理ObjectId
        for item in items:
            if "_id" in item:
                item["_id"] = str(item["_id"])
                
        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size
        }
    
    async def clear_option_contract_info_ctp(self) -> int:
        """清空OpenCTP期权合约信息"""
        result = await self.col_option_contract_info_ctp.delete_many({})
        return result.deleted_count

    async def save_option_finance_board(self, df: pd.DataFrame, symbol: str, end_month: str) -> int:
        """
        保存金融期权行情数据
        """
        if df.empty:
            return 0
            
        # Mapping
        column_mapping = {
            "日期": "date",
            "合约交易代码": "code",
            "当前价": "current_price",
            "涨跌幅": "change_pct",
            "前结价": "pre_settle",
            "行权价": "strike_price",
            "数量": "quantity"
        }
        df = df.rename(columns=column_mapping)
        df["symbol"] = symbol
        df["end_month"] = end_month
        df["updated_at"] = datetime.now()
        
        records = df.to_dict("records")
        operations = []
        for record in records:
            filter_query = {
                "code": record.get("code"),
                "date": record.get("date") # Assuming date is unique per contract per day, or maybe just code is unique if it's snapshot?
                # The description says "单次返回当前交易日...". So it's a snapshot. 
                # If we run multiple times a day, we overwrite.
                # If date changes, we might keep history? 
                # For now, let's use code + date as unique key if date is present.
            }
            operations.append(UpdateOne(filter_query, {"$set": record}, upsert=True))
            
        if operations:
            result = await self.col_option_finance_board.bulk_write(operations)
            return result.upserted_count + result.modified_count
        return 0

    async def fetch_and_save_option_finance_board(self) -> int:
        """
        获取并保存金融期权行情数据
        """
        logger.info("开始获取金融期权行情数据...")
        total_saved = 0
        
        symbols = [
            "华夏上证50ETF期权",
            "华泰柏瑞沪深300ETF期权",
            "嘉实沪深300ETF期权",
            "沪深300股指期权",
            "中证1000股指期权",
            "上证50股指期权"
        ]
        
        # Calculate next 4 months
        today = datetime.now()
        months = []
        for i in range(4):
            # i=0 -> current month
            # Note: logic for year rollover
            m = (today.month + i - 1) % 12 + 1
            y = today.year + (today.month + i - 1) // 12
            months.append(f"{y % 100:02d}{m:02d}")
            
        for symbol in symbols:
            for end_month in months:
                try:
                    logger.info(f"Fetching {symbol} {end_month}...")
                    # akshare call
                    df = ak.option_finance_board(symbol=symbol, end_month=end_month)
                    count = await self.save_option_finance_board(df, symbol, end_month)
                    total_saved += count
                except Exception as e:
                    logger.warning(f"获取 {symbol} {end_month} 失败: {e}")
                    continue
                    
        logger.info(f"成功保存 {total_saved} 条金融期权行情数据")
        return total_saved

    async def clear_option_finance_board(self) -> int:
        """清空金融期权行情数据"""
        result = await self.col_option_finance_board.delete_many({})
        return result.deleted_count

    async def save_option_risk_indicator_sse(self, df: pd.DataFrame) -> int:
        """保存上海证券交易所期权风险指标数据"""
        if df.empty:
            return 0
            
        # Mapping
        # Output params: TRADE_DATE, SECURITY_ID, CONTRACT_ID, CONTRACT_SYMBOL, DELTA_VALUE, THETA_VALUE, GAMMA_VALUE, VEGA_VALUE, RHO_VALUE, IMPLC_VOLATLTY
        column_mapping = {
            "TRADE_DATE": "trade_date",
            "SECURITY_ID": "security_id",
            "CONTRACT_ID": "contract_id",
            "CONTRACT_SYMBOL": "contract_symbol",
            "DELTA_VALUE": "delta",
            "THETA_VALUE": "theta",
            "GAMMA_VALUE": "gamma",
            "VEGA_VALUE": "vega",
            "RHO_VALUE": "rho",
            "IMPLC_VOLATLTY": "implied_volatility"
        }
        
        # API might return uppercase or lowercase, check columns
        df_cols = df.columns.tolist()
        # Try to map if columns match
        
        df = df.rename(columns=column_mapping)
        df["updated_at"] = datetime.now()
        
        records = df.to_dict("records")
        operations = []
        for record in records:
            # Unique key: trade_date + contract_id
            filter_query = {
                "trade_date": record.get("trade_date"),
                "contract_id": record.get("contract_id")
            }
            operations.append(UpdateOne(filter_query, {"$set": record}, upsert=True))
            
        if operations:
            result = await self.col_option_risk_indicator_sse.bulk_write(operations)
            return result.upserted_count + result.modified_count
        return 0

    async def fetch_and_save_option_risk_indicator_sse(self) -> int:
        """获取并保存上海证券交易所期权风险指标数据"""
        logger.info("开始获取上海证券交易所期权风险指标数据...")
        
        # Fetch data for recent trading days?
        # API requires specific date. 
        # Default to today. If today is not trading day, maybe previous day?
        # Let's try today.
        
        dates_to_fetch = []
        today = datetime.now()
        # Simple logic: fetch last 5 days to be safe/cover holidays
        for i in range(5):
            d = today - timedelta(days=i)
            dates_to_fetch.append(d.strftime("%Y%m%d"))
            
        total_saved = 0
        for date_str in dates_to_fetch:
            try:
                logger.info(f"Fetching option_risk_indicator_sse for {date_str}...")
                df = ak.option_risk_indicator_sse(date=date_str)
                if not df.empty:
                    count = await self.save_option_risk_indicator_sse(df)
                    total_saved += count
                    # If we got data for a date, maybe we stop? or keep fetching history?
                    # The requirement says "单次返回指定 date 的数据".
                    # Let's try to fetch a few days.
            except Exception as e:
                logger.warning(f"获取 option_risk_indicator_sse {date_str} 失败: {e}")
                continue
                
        logger.info(f"成功保存 {total_saved} 条上海证券交易所期权风险指标数据")
        return total_saved

    async def clear_option_risk_indicator_sse(self) -> int:
        """清空上海证券交易所期权风险指标数据"""
        result = await self.col_option_risk_indicator_sse.delete_many({})
        return result.deleted_count

    async def save_option_current_day_sse(self, df: pd.DataFrame) -> int:
        """保存上海证券交易所产品股票期权信息披露当日合约数据"""
        if df.empty:
            return 0
            
        # Mapping
        # Output: 合约编码, 合约交易代码, 合约简称, 标的券名称及代码, 类型, 行权价, 合约单位, 期权行权日, 行权交收日, 到期日, 开始日期
        column_mapping = {
            "合约编码": "contract_code",
            "合约交易代码": "trade_code",
            "合约简称": "contract_name",
            "标的券名称及代码": "underlying_name_code",
            "类型": "option_type",
            "行权价": "strike_price",
            "合约单位": "contract_unit",
            "期权行权日": "exercise_date",
            "行权交收日": "delivery_date",
            "到期日": "expire_date",
            "开始日期": "start_date"
        }
        
        df = df.rename(columns=column_mapping)
        df["updated_at"] = datetime.now()
        
        records = df.to_dict("records")
        operations = []
        for record in records:
            # Unique key: contract_code
            filter_query = {
                "contract_code": record.get("contract_code")
            }
            operations.append(UpdateOne(filter_query, {"$set": record}, upsert=True))
            
        if operations:
            result = await self.col_option_current_day_sse.bulk_write(operations)
            return result.upserted_count + result.modified_count
        return 0

    async def fetch_and_save_option_current_day_sse(self) -> int:
        """获取并保存上海证券交易所产品股票期权信息披露当日合约数据"""
        try:
            logger.info("开始获取上海证券交易所产品股票期权信息披露当日合约数据...")
            df = ak.option_current_day_sse()
            if not df.empty:
                count = await self.save_option_current_day_sse(df)
                logger.info(f"成功保存 {count} 条上海证券交易所产品股票期权信息披露当日合约数据")
                return count
            else:
                logger.warning("上海证券交易所产品股票期权信息披露当日合约数据为空")
                return 0
        except Exception as e:
            logger.error(f"获取 option_current_day_sse 失败: {e}")
            raise e

    async def clear_option_current_day_sse(self) -> int:
        """清空上海证券交易所产品股票期权信息披露当日合约数据"""
        result = await self.col_option_current_day_sse.delete_many({})
        return result.deleted_count

    async def save_option_current_day_szse(self, df: pd.DataFrame) -> int:
        """保存深圳证券交易所期权子网行情数据当日合约数据"""
        if df.empty:
            return 0
            
        # Mapping
        column_mapping = {
            "序号": "serial_number",
            "合约编码": "contract_code_id",
            "合约代码": "contract_code",
            "合约简称": "contract_name",
            "标的证券简称(代码)": "underlying_name_code",
            "合约类型": "contract_type",
            "行权价": "strike_price",
            "合约单位": "contract_unit",
            "最后交易日": "last_trade_date",
            "行权日": "exercise_date",
            "到期日": "expire_date",
            "交收日": "delivery_date",
            "新挂": "is_new",
            "涨停价格": "limit_up",
            "跌停价格": "limit_down",
            "前结算价": "pre_settle",
            "合约调整": "is_adjusted",
            "停牌": "is_suspended",
            "合约总持仓": "open_interest",
            "挂牌原因": "list_reason",
            "原合约代码": "original_contract_code",
            "原合约简称": "original_contract_name",
            "原行权价格": "original_strike_price",
            "原合约单位": "original_contract_unit",
            "合约到期剩余交易天数": "days_to_expire_trading",
            "合约到期剩余自然天数": "days_to_expire_natural",
            "下次合约调整剩余交易天数": "days_to_adjust_trading",
            "下次合约调整剩余自然天数": "days_to_adjust_natural",
            "交易日期": "trade_date"
        }
        
        df = df.rename(columns=column_mapping)
        df["updated_at"] = datetime.now()
        
        records = df.to_dict("records")
        operations = []
        for record in records:
            # Unique key: contract_code
            filter_query = {
                "contract_code": record.get("contract_code")
            }
            operations.append(UpdateOne(filter_query, {"$set": record}, upsert=True))
            
        if operations:
            result = await self.col_option_current_day_szse.bulk_write(operations)
            return result.upserted_count + result.modified_count
        return 0

    async def fetch_and_save_option_current_day_szse(self) -> int:
        """获取并保存深圳证券交易所期权子网行情数据当日合约数据"""
        try:
            logger.info("开始获取深圳证券交易所期权子网行情数据当日合约数据...")
            df = ak.option_current_day_szse()
            if not df.empty:
                count = await self.save_option_current_day_szse(df)
                logger.info(f"成功保存 {count} 条深圳证券交易所期权子网行情数据当日合约数据")
                return count
            else:
                logger.warning("深圳证券交易所期权子网行情数据当日合约数据为空")
                return 0
        except Exception as e:
            logger.error(f"获取 option_current_day_szse 失败: {e}")
            raise e

    async def clear_option_current_day_szse(self) -> int:
        """清空深圳证券交易所期权子网行情数据当日合约数据"""
        result = await self.col_option_current_day_szse.delete_many({})
        return result.deleted_count

    async def save_option_daily_stats_sse(self, df: pd.DataFrame) -> int:
        """保存上海证券交易所产品股票期权每日统计数据"""
        if df.empty:
            return 0
            
        # Mapping
        # Output: 合约标的代码, 合约标的名称, 合约数量, 总成交额, 总成交量, 认购成交量, 认沽成交量, 认沽/认购, 未平仓合约总数, 未平仓认购合约数, 未平仓认沽合约数
        column_mapping = {
            "合约标的代码": "underlying_code",
            "合约标的名称": "underlying_name",
            "合约数量": "contract_quantity",
            "总成交额": "total_turnover",
            "总成交量": "total_volume",
            "认购成交量": "call_volume",
            "认沽成交量": "put_volume",
            "认沽/认购": "put_call_ratio",
            "未平仓合约总数": "open_interest_total",
            "未平仓认购合约数": "open_interest_call",
            "未平仓认沽合约数": "open_interest_put"
        }
        
        df = df.rename(columns=column_mapping)
        df["updated_at"] = datetime.now()
        # Assuming data comes with a date or we can attach it. 
        # The API returns data for a specific date input.
        # But the dataframe itself might not contain the date.
        # We should probably pass date from fetch function if it's missing.
        
        records = df.to_dict("records")
        operations = []
        for record in records:
            # Unique key: trade_date + underlying_code
            # If record has trade_date, use it. If not, use what we passed (not implemented yet, see fetch)
            
            # Check if date column exists
            date_val = record.get("trade_date")
            
            filter_query = {
                "trade_date": date_val,
                "underlying_code": record.get("underlying_code")
            }
            operations.append(UpdateOne(filter_query, {"$set": record}, upsert=True))
            
        if operations:
            result = await self.col_option_daily_stats_sse.bulk_write(operations)
            return result.upserted_count + result.modified_count
        return 0

    async def fetch_and_save_option_daily_stats_sse(self) -> int:
        """获取并保存上海证券交易所产品股票期权每日统计数据"""
        logger.info("开始获取上海证券交易所产品股票期权每日统计数据...")
        
        dates_to_fetch = []
        today = datetime.now()
        # Fetch last 5 days
        for i in range(5):
            d = today - timedelta(days=i)
            dates_to_fetch.append(d.strftime("%Y%m%d"))
            
        total_saved = 0
        for date_str in dates_to_fetch:
            try:
                logger.info(f"Fetching option_daily_stats_sse for {date_str}...")
                df = ak.option_daily_stats_sse(date=date_str)
                if not df.empty:
                    # Add date column if missing
                    if "trade_date" not in df.columns:
                        df["trade_date"] = date_str
                        
                    count = await self.save_option_daily_stats_sse(df)
                    total_saved += count
            except Exception as e:
                logger.warning(f"获取 option_daily_stats_sse {date_str} 失败: {e}")
                continue
                
        logger.info(f"成功保存 {total_saved} 条上海证券交易所产品股票期权每日统计数据")
        return total_saved

    async def clear_option_daily_stats_sse(self) -> int:
        """清空上海证券交易所产品股票期权每日统计数据"""
        result = await self.col_option_daily_stats_sse.delete_many({})
        return result.deleted_count

    async def save_option_daily_stats_szse(self, df: pd.DataFrame) -> int:
        """保存深圳证券交易所市场数据期权数据日度概况数据"""
        if df.empty:
            return 0
            
        # Mapping
        # Output: 合约标的代码, 合约标的名称, 成交量, 认购成交量, 认沽成交量, 认沽/认购持仓比, 未平仓合约总数, 未平仓认购合约数, 未平仓认沽合约数, 交易日
        column_mapping = {
            "合约标的代码": "underlying_code",
            "合约标的名称": "underlying_name",
            "成交量": "total_volume",
            "认购成交量": "call_volume",
            "认沽成交量": "put_volume",
            "认沽/认购持仓比": "put_call_ratio",
            "未平仓合约总数": "open_interest_total",
            "未平仓认购合约数": "open_interest_call",
            "未平仓认沽合约数": "open_interest_put",
            "交易日": "trade_date"
        }
        
        df = df.rename(columns=column_mapping)
        df["updated_at"] = datetime.now()
        
        records = df.to_dict("records")
        operations = []
        for record in records:
            # Unique key: trade_date + underlying_code
            filter_query = {
                "trade_date": record.get("trade_date"),
                "underlying_code": record.get("underlying_code")
            }
            operations.append(UpdateOne(filter_query, {"$set": record}, upsert=True))
            
        if operations:
            result = await self.col_option_daily_stats_szse.bulk_write(operations)
            return result.upserted_count + result.modified_count
        return 0

    async def fetch_and_save_option_daily_stats_szse(self) -> int:
        """获取并保存深圳证券交易所市场数据期权数据日度概况数据"""
        logger.info("开始获取深圳证券交易所市场数据期权数据日度概况数据...")
        
        dates_to_fetch = []
        today = datetime.now()
        # Fetch last 5 days
        for i in range(5):
            d = today - timedelta(days=i)
            dates_to_fetch.append(d.strftime("%Y%m%d"))
            
        total_saved = 0
        for date_str in dates_to_fetch:
            try:
                logger.info(f"Fetching option_daily_stats_szse for {date_str}...")
                df = ak.option_daily_stats_szse(date=date_str)
                if not df.empty:
                    # Ensure date format consistent if API returns weird date
                    # But "交易日" is in output, so it should be there.
                    count = await self.save_option_daily_stats_szse(df)
                    total_saved += count
            except Exception as e:
                logger.warning(f"获取 option_daily_stats_szse {date_str} 失败: {e}")
                continue
                
        logger.info(f"成功保存 {total_saved} 条深圳证券交易所市场数据期权数据日度概况数据")
        return total_saved

    async def clear_option_daily_stats_szse(self) -> int:
        """清空深圳证券交易所市场数据期权数据日度概况数据"""
        result = await self.col_option_daily_stats_szse.delete_many({})
        return result.deleted_count

    async def save_option_cffex_sz50_list_sina(self, contracts: List[str]) -> int:
        """保存中金所上证50指数所有合约数据"""
        if not contracts:
            return 0
            
        records = [{"contract_code": code, "updated_at": datetime.now()} for code in contracts]
        
        # Replace all since it's a list of current contracts
        # Or update? 
        # "返回的第一个合约为主力合约" - The order matters.
        # Maybe we should store them with an index?
        # The requirement just says "数据集合...option_cffex_sz50_list_sina".
        # And "单次返回所有合约".
        # If we want to keep history of what was available when, we need a date.
        # But the API doesn't seem to take a date. It returns *current* list.
        # Let's clear and insert for "current list" or append with date for history.
        # Given it's a "list", maybe we just want the current available contracts.
        # Let's use update with upsert on contract_code to keep a master list of all contracts ever seen?
        # Or just current snapshot?
        # Let's go with master list of contracts seen.
        
        operations = []
        for record in records:
            filter_query = {"contract_code": record["contract_code"]}
            operations.append(UpdateOne(filter_query, {"$set": record}, upsert=True))
            
        if operations:
            result = await self.col_option_cffex_sz50_list_sina.bulk_write(operations)
            return result.upserted_count + result.modified_count
        return 0

    async def fetch_and_save_option_cffex_sz50_list_sina(self) -> int:
        """获取并保存中金所上证50指数所有合约数据"""
        try:
            logger.info("开始获取中金所上证50指数所有合约数据...")
            # akshare returns a list of strings
            contracts = ak.option_cffex_sz50_list_sina()
            if contracts:
                # Ensure it is a list of strings
                if isinstance(contracts, (list, tuple)):
                    count = await self.save_option_cffex_sz50_list_sina(list(contracts))
                    logger.info(f"成功保存 {count} 条中金所上证50指数合约数据")
                    return count
                else:
                    logger.warning(f"API returned unexpected type: {type(contracts)}")
                    return 0
            else:
                logger.warning("中金所上证50指数合约数据为空")
                return 0
        except Exception as e:
            logger.error(f"获取 option_cffex_sz50_list_sina 失败: {e}")
            raise e

    async def clear_option_cffex_sz50_list_sina(self) -> int:
        """清空中金所上证50指数所有合约数据"""
        result = await self.col_option_cffex_sz50_list_sina.delete_many({})
        return result.deleted_count


    async def save_option_cffex_hs300_list_sina(self, contracts: List[str]) -> int:
        """保存中金所沪深300指数所有合约数据"""
        if not contracts:
            return 0
            
        records = [{"contract_code": code, "updated_at": datetime.now()} for code in contracts]
        
        operations = []
        for record in records:
            filter_query = {"contract_code": record["contract_code"]}
            operations.append(UpdateOne(filter_query, {"$set": record}, upsert=True))
            
        if operations:
            result = await self.col_option_cffex_hs300_list_sina.bulk_write(operations)
            return result.upserted_count + result.modified_count
        return 0


    async def fetch_and_save_option_cffex_hs300_list_sina(self) -> int:
        """获取并保存中金所沪深300指数所有合约数据"""
        try:
            logger.info("开始获取中金所沪深300指数所有合约数据...")
            contracts = ak.option_cffex_hs300_list_sina()
            if contracts:
                if isinstance(contracts, (list, tuple)):
                    count = await self.save_option_cffex_hs300_list_sina(list(contracts))
                    logger.info(f"成功保存 {count} 条中金所沪深300指数合约数据")
                    return count
                else:
                    logger.warning(f"API returned unexpected type for hs300 list: {type(contracts)}")
                    return 0
            else:
                logger.warning("中金所沪深300指数合约数据为空")
                return 0
        except Exception as e:
            logger.error(f"获取 option_cffex_hs300_list_sina 失败: {e}")
            raise e


    async def clear_option_cffex_hs300_list_sina(self) -> int:
        """清空中金所沪深300指数所有合约数据"""
        result = await self.col_option_cffex_hs300_list_sina.delete_many({})
        return result.deleted_count


    async def save_option_cffex_zz1000_list_sina(self, contracts: List[str]) -> int:
        """保存中金所中证1000指数所有合约数据"""
        if not contracts:
            return 0
            
        records = [{"contract_code": code, "updated_at": datetime.now()} for code in contracts]
        
        operations = []
        for record in records:
            filter_query = {"contract_code": record["contract_code"]}
            operations.append(UpdateOne(filter_query, {"$set": record}, upsert=True))
            
        if operations:
            result = await self.col_option_cffex_zz1000_list_sina.bulk_write(operations)
            return result.upserted_count + result.modified_count
        return 0


    async def fetch_and_save_option_cffex_zz1000_list_sina(self) -> int:
        """获取并保存中金所中证1000指数所有合约数据"""
        try:
            logger.info("开始获取中金所中证1000指数所有合约数据...")
            contracts = ak.option_cffex_zz1000_list_sina()
            if contracts:
                if isinstance(contracts, (list, tuple)):
                    count = await self.save_option_cffex_zz1000_list_sina(list(contracts))
                    logger.info(f"成功保存 {count} 条中金所中证1000指数合约数据")
                    return count
                else:
                    logger.warning(f"API returned unexpected type for zz1000 list: {type(contracts)}")
                    return 0
            else:
                logger.warning("中金所中证1000指数合约数据为空")
                return 0
        except Exception as e:
            logger.error(f"获取 option_cffex_zz1000_list_sina 失败: {e}")
            raise e


    async def clear_option_cffex_zz1000_list_sina(self) -> int:
        """清空中金所中证1000指数所有合约数据"""
        result = await self.col_option_cffex_zz1000_list_sina.delete_many({})
        return result.deleted_count


    async def save_option_cffex_sz50_spot_sina(self, df: pd.DataFrame, symbol: str) -> int:
        """保存新浪财经中金所上证50指数指定合约实时行情数据"""
        if df is None or df.empty:
            return 0
        
        # 字段映射：中文 -> 英文
        field_mapping = {
            "看涨合约-买量": "call_bid_volume",
            "看涨合约-买价": "call_bid_price",
            "看涨合约-最新价": "call_last_price",
            "看涨合约-卖价": "call_ask_price",
            "看涨合约-卖量": "call_ask_volume",
            "看涨合约-持仓量": "call_open_interest",
            "看涨合约-涨跌": "call_change",
            "行权价": "strike_price",
            "看涨合约-标识": "call_symbol",
            "看跌合约-买量": "put_bid_volume",
            "看跌合约-买价": "put_bid_price",
            "看跌合约-最新价": "put_last_price",
            "看跌合约-卖价": "put_ask_price",
            "看跌合约-卖量": "put_ask_volume",
            "看跌合约-持仓量": "put_open_interest",
            "看跌合约-涨跌": "put_change",
            "看跌合约-标识": "put_symbol",
        }
        
        df_renamed = df.rename(columns=field_mapping)
        df_renamed["symbol"] = symbol
        df_renamed["updated_at"] = datetime.now()
        
        records = df_renamed.to_dict("records")
        
        operations = []
        for record in records:
            # 使用 symbol + strike_price 作为唯一标识
            filter_query = {
                "symbol": record.get("symbol"),
                "strike_price": record.get("strike_price")
            }
            operations.append(UpdateOne(filter_query, {"$set": record}, upsert=True))
        
        if operations:
            result = await self.col_option_cffex_sz50_spot_sina.bulk_write(operations)
            return result.upserted_count + result.modified_count
        return 0


    async def fetch_and_save_option_cffex_sz50_spot_sina(self, symbol: str = "ho2303") -> int:
        """获取并保存新浪财经中金所上证50指数指定合约实时行情数据"""
        try:
            logger.info(f"开始获取中金所上证50指数合约 {symbol} 实时行情数据...")
            df = ak.option_cffex_sz50_spot_sina(symbol=symbol)
            if df is not None and not df.empty:
                count = await self.save_option_cffex_sz50_spot_sina(df, symbol)
                logger.info(f"成功保存 {count} 条中金所上证50指数合约 {symbol} 实时行情数据")
                return count
            else:
                logger.warning(f"中金所上证50指数合约 {symbol} 实时行情数据为空")
                return 0
        except Exception as e:
            logger.error(f"获取 option_cffex_sz50_spot_sina {symbol} 失败: {e}")
            raise e


    async def clear_option_cffex_sz50_spot_sina(self) -> int:
        """清空新浪财经中金所上证50指数指定合约实时行情数据"""
        result = await self.col_option_cffex_sz50_spot_sina.delete_many({})
        return result.deleted_count


    # HS300 Spot methods
    async def save_option_cffex_hs300_spot_sina(self, df: pd.DataFrame, symbol: str) -> int:
        """保存新浪财经中金所沪深300指数指定合约实时行情数据"""
        if df is None or df.empty:
            return 0
        
        field_mapping = {
            "看涨合约-买量": "call_bid_volume",
            "看涨合约-买价": "call_bid_price",
            "看涨合约-最新价": "call_last_price",
            "看涨合约-卖价": "call_ask_price",
            "看涨合约-卖量": "call_ask_volume",
            "看涨合约-持仓量": "call_open_interest",
            "看涨合约-涨跌": "call_change",
            "行权价": "strike_price",
            "看涨合约-标识": "call_symbol",
            "看跌合约-买量": "put_bid_volume",
            "看跌合约-买价": "put_bid_price",
            "看跌合约-最新价": "put_last_price",
            "看跌合约-卖价": "put_ask_price",
            "看跌合约-卖量": "put_ask_volume",
            "看跌合约-持仓量": "put_open_interest",
            "看跌合约-涨跌": "put_change",
            "看跌合约-标识": "put_symbol",
        }
        
        df_renamed = df.rename(columns=field_mapping)
        df_renamed["symbol"] = symbol
        df_renamed["updated_at"] = datetime.now()
        
        records = df_renamed.to_dict("records")
        
        operations = []
        for record in records:
            filter_query = {
                "symbol": record.get("symbol"),
                "strike_price": record.get("strike_price")
            }
            operations.append(UpdateOne(filter_query, {"$set": record}, upsert=True))
        
        if operations:
            result = await self.col_option_cffex_hs300_spot_sina.bulk_write(operations)
            return result.upserted_count + result.modified_count
        return 0


    async def fetch_and_save_option_cffex_hs300_spot_sina(self, symbol: str = "io2104") -> int:
        """获取并保存新浪财经中金所沪深300指数指定合约实时行情数据"""
        try:
            logger.info(f"开始获取中金所沪深300指数合约 {symbol} 实时行情数据...")
            df = ak.option_cffex_hs300_spot_sina(symbol=symbol)
            if df is not None and not df.empty:
                count = await self.save_option_cffex_hs300_spot_sina(df, symbol)
                logger.info(f"成功保存 {count} 条中金所沪深300指数合约 {symbol} 实时行情数据")
                return count
            else:
                logger.warning(f"中金所沪深300指数合约 {symbol} 实时行情数据为空")
                return 0
        except Exception as e:
            logger.error(f"获取 option_cffex_hs300_spot_sina {symbol} 失败: {e}")
            raise e


    async def clear_option_cffex_hs300_spot_sina(self) -> int:
        """清空新浪财经中金所沪深300指数指定合约实时行情数据"""
        result = await self.col_option_cffex_hs300_spot_sina.delete_many({})
        return result.deleted_count


    # ZZ1000 Spot methods
    async def save_option_cffex_zz1000_spot_sina(self, df: pd.DataFrame, symbol: str) -> int:
        """保存新浪财经中金所中证1000指数指定合约实时行情数据"""
        if df is None or df.empty:
            return 0
        
        field_mapping = {
            "看涨合约-买量": "call_bid_volume",
            "看涨合约-买价": "call_bid_price",
            "看涨合约-最新价": "call_last_price",
            "看涨合约-卖价": "call_ask_price",
            "看涨合约-卖量": "call_ask_volume",
            "看涨合约-持仓量": "call_open_interest",
            "看涨合约-涨跌": "call_change",
            "行权价": "strike_price",
            "看涨合约-标识": "call_symbol",
            "看跌合约-买量": "put_bid_volume",
            "看跌合约-买价": "put_bid_price",
            "看跌合约-最新价": "put_last_price",
            "看跌合约-卖价": "put_ask_price",
            "看跌合约-卖量": "put_ask_volume",
            "看跌合约-持仓量": "put_open_interest",
            "看跌合约-涨跌": "put_change",
            "看跌合约-标识": "put_symbol",
        }
        
        df_renamed = df.rename(columns=field_mapping)
        df_renamed["symbol"] = symbol
        df_renamed["updated_at"] = datetime.now()
        
        records = df_renamed.to_dict("records")
        
        operations = []
        for record in records:
            filter_query = {
                "symbol": record.get("symbol"),
                "strike_price": record.get("strike_price")
            }
            operations.append(UpdateOne(filter_query, {"$set": record}, upsert=True))
        
        if operations:
            result = await self.col_option_cffex_zz1000_spot_sina.bulk_write(operations)
            return result.upserted_count + result.modified_count
        return 0


    async def fetch_and_save_option_cffex_zz1000_spot_sina(self, symbol: str = "mo2104") -> int:
        """获取并保存新浪财经中金所中证1000指数指定合约实时行情数据"""
        try:
            logger.info(f"开始获取中金所中证1000指数合约 {symbol} 实时行情数据...")
            df = ak.option_cffex_zz1000_spot_sina(symbol=symbol)
            if df is not None and not df.empty:
                count = await self.save_option_cffex_zz1000_spot_sina(df, symbol)
                logger.info(f"成功保存 {count} 条中金所中证1000指数合约 {symbol} 实时行情数据")
                return count
            else:
                logger.warning(f"中金所中证1000指数合约 {symbol} 实时行情数据为空")
                return 0
        except Exception as e:
            logger.error(f"获取 option_cffex_zz1000_spot_sina {symbol} 失败: {e}")
            raise e


    async def clear_option_cffex_zz1000_spot_sina(self) -> int:
        """清空新浪财经中金所中证1000指数指定合约实时行情数据"""
        result = await self.col_option_cffex_zz1000_spot_sina.delete_many({})
        return result.deleted_count


    # Daily methods for SZ50/HS300/ZZ1000
    async def save_option_cffex_sz50_daily_sina(self, df: pd.DataFrame, symbol: str) -> int:
        """保存中金所上证50指数指定合约日频行情数据"""
        if df is None or df.empty:
            return 0
        
        df_copy = df.copy()
        df_copy["symbol"] = symbol
        df_copy["updated_at"] = datetime.now()
        
        records = df_copy.to_dict("records")
        
        operations = []
        for record in records:
            filter_query = {
                "symbol": record.get("symbol"),
                "date": record.get("date")
            }
            operations.append(UpdateOne(filter_query, {"$set": record}, upsert=True))
        
        if operations:
            result = await self.col_option_cffex_sz50_daily_sina.bulk_write(operations)
            return result.upserted_count + result.modified_count
        return 0


    async def fetch_and_save_option_cffex_sz50_daily_sina(self, symbol: str = "ho2303P2350") -> int:
        """获取并保存中金所上证50指数指定合约日频行情数据"""
        try:
            logger.info(f"开始获取中金所上证50指数合约 {symbol} 日频行情数据...")
            df = ak.option_cffex_sz50_daily_sina(symbol=symbol)
            if df is not None and not df.empty:
                count = await self.save_option_cffex_sz50_daily_sina(df, symbol)
                logger.info(f"成功保存 {count} 条中金所上证50指数合约 {symbol} 日频行情数据")
                return count
            else:
                logger.warning(f"中金所上证50指数合约 {symbol} 日频行情数据为空")
                return 0
        except Exception as e:
            logger.error(f"获取 option_cffex_sz50_daily_sina {symbol} 失败: {e}")
            raise e


    async def clear_option_cffex_sz50_daily_sina(self) -> int:
        """清空中金所上证50指数指定合约日频行情数据"""
        result = await self.col_option_cffex_sz50_daily_sina.delete_many({})
        return result.deleted_count


    async def save_option_cffex_hs300_daily_sina(self, df: pd.DataFrame, symbol: str) -> int:
        """保存中金所沪深300指数指定合约日频行情数据"""
        if df is None or df.empty:
            return 0
        
        df_copy = df.copy()
        df_copy["symbol"] = symbol
        df_copy["updated_at"] = datetime.now()
        
        records = df_copy.to_dict("records")
        
        operations = []
        for record in records:
            filter_query = {
                "symbol": record.get("symbol"),
                "date": record.get("date")
            }
            operations.append(UpdateOne(filter_query, {"$set": record}, upsert=True))
        
        if operations:
            result = await self.col_option_cffex_hs300_daily_sina.bulk_write(operations)
            return result.upserted_count + result.modified_count
        return 0


    async def fetch_and_save_option_cffex_hs300_daily_sina(self, symbol: str = "io2104P3800") -> int:
        """获取并保存中金所沪深300指数指定合约日频行情数据"""
        try:
            logger.info(f"开始获取中金所沪深300指数合约 {symbol} 日频行情数据...")
            df = ak.option_cffex_hs300_daily_sina(symbol=symbol)
            if df is not None and not df.empty:
                count = await self.save_option_cffex_hs300_daily_sina(df, symbol)
                logger.info(f"成功保存 {count} 条中金所沪深300指数合约 {symbol} 日频行情数据")
                return count
            else:
                logger.warning(f"中金所沪深300指数合约 {symbol} 日频行情数据为空")
                return 0
        except Exception as e:
            logger.error(f"获取 option_cffex_hs300_daily_sina {symbol} 失败: {e}")
            raise e


    async def clear_option_cffex_hs300_daily_sina(self) -> int:
        """清空中金所沪深300指数指定合约日频行情数据"""
        result = await self.col_option_cffex_hs300_daily_sina.delete_many({})
        return result.deleted_count


    async def save_option_cffex_zz1000_daily_sina(self, df: pd.DataFrame, symbol: str) -> int:
        """保存中金所中证1000指数指定合约日频行情数据"""
        if df is None or df.empty:
            return 0
        
        df_copy = df.copy()
        df_copy["symbol"] = symbol
        df_copy["updated_at"] = datetime.now()
        
        records = df_copy.to_dict("records")
        
        operations = []
        for record in records:
            filter_query = {
                "symbol": record.get("symbol"),
                "date": record.get("date")
            }
            operations.append(UpdateOne(filter_query, {"$set": record}, upsert=True))
        
        if operations:
            result = await self.col_option_cffex_zz1000_daily_sina.bulk_write(operations)
            return result.upserted_count + result.modified_count
        return 0


    async def fetch_and_save_option_cffex_zz1000_daily_sina(self, symbol: str = "mo2104P5600") -> int:
        """获取并保存中金所中证1000指数指定合约日频行情数据"""
        try:
            logger.info(f"开始获取中金所中证1000指数合约 {symbol} 日频行情数据...")
            df = ak.option_cffex_zz1000_daily_sina(symbol=symbol)
            if df is not None and not df.empty:
                count = await self.save_option_cffex_zz1000_daily_sina(df, symbol)
                logger.info(f"成功保存 {count} 条中金所中证1000指数合约 {symbol} 日频行情数据")
                return count
            else:
                logger.warning(f"中金所中证1000指数合约 {symbol} 日频行情数据为空")
                return 0
        except Exception as e:
            logger.error(f"获取 option_cffex_zz1000_daily_sina {symbol} 失败: {e}")
            raise e


    async def clear_option_cffex_zz1000_daily_sina(self) -> int:
        """清空中金所中证1000指数指定合约日频行情数据"""
        result = await self.col_option_cffex_zz1000_daily_sina.delete_many({})
        return result.deleted_count


    async def save_option_sse_list_sina(self, months: List[str], symbol: str) -> int:
        """保存上交所50ETF/300ETF合约到期月份列表"""
        if not months:
            return 0
            
        records = [{"symbol": symbol, "month": month, "updated_at": datetime.now()} for month in months]
        
        operations = []
        for record in records:
            filter_query = {"symbol": record["symbol"], "month": record["month"]}
            operations.append(UpdateOne(filter_query, {"$set": record}, upsert=True))
            
        if operations:
            result = await self.col_option_sse_list_sina.bulk_write(operations)
            return result.upserted_count + result.modified_count
        return 0


    async def fetch_and_save_option_sse_list_sina(self, symbol: str = "50ETF", exchange: str = "null") -> int:
        """获取并保存上交所50ETF/300ETF合约到期月份列表"""
        try:
            logger.info(f"开始获取上交所 {symbol} 合约到期月份列表...")
            months = ak.option_sse_list_sina(symbol=symbol, exchange=exchange)
            if months and isinstance(months, (list, tuple)):
                count = await self.save_option_sse_list_sina(list(months), symbol)
                logger.info(f"成功保存 {count} 条上交所 {symbol} 合约到期月份数据")
                return count
            else:
                logger.warning(f"上交所 {symbol} 合约到期月份数据为空")
                return 0
        except Exception as e:
            logger.error(f"获取 option_sse_list_sina {symbol} 失败: {e}")
            raise e


    async def clear_option_sse_list_sina(self) -> int:
        """清空上交所50ETF/300ETF合约到期月份列表"""
        result = await self.col_option_sse_list_sina.delete_many({})
        return result.deleted_count


    async def save_option_sse_expire_day_sina(self, expire_days: int, trade_date: str, symbol: str) -> int:
        """保存指定到期月份指定品种的剩余到期时间"""
        record = {
            "trade_date": trade_date,
            "symbol": symbol,
            "expire_days": expire_days,
            "updated_at": datetime.now()
        }
        
        filter_query = {"trade_date": trade_date, "symbol": symbol}
        result = await self.col_option_sse_expire_day_sina.update_one(
            filter_query, {"$set": record}, upsert=True
        )
        return 1 if result.upserted_id or result.modified_count else 0


    async def fetch_and_save_option_sse_expire_day_sina(self, trade_date: str = "202002", symbol: str = "50ETF", exchange: str = "null") -> int:
        """获取并保存指定到期月份指定品种的剩余到期时间"""
        try:
            logger.info(f"开始获取 {symbol} {trade_date} 剩余到期时间...")
            expire_days = ak.option_sse_expire_day_sina(trade_date=trade_date, symbol=symbol, exchange=exchange)
            if expire_days is not None:
                count = await self.save_option_sse_expire_day_sina(int(expire_days), trade_date, symbol)
                logger.info(f"成功保存 {symbol} {trade_date} 剩余到期时间: {expire_days}天")
                return count
            else:
                logger.warning(f"{symbol} {trade_date} 剩余到期时间数据为空")
                return 0
        except Exception as e:
            logger.error(f"获取 option_sse_expire_day_sina 失败: {e}")
            raise e


    async def clear_option_sse_expire_day_sina(self) -> int:
        """清空指定到期月份指定品种的剩余到期时间"""
        result = await self.col_option_sse_expire_day_sina.delete_many({})
        return result.deleted_count


    async def save_option_sse_codes_sina(self, codes: List[str], trade_date: str, symbol: str) -> int:
        """保存新浪期权看涨看跌合约代码"""
        if not codes:
            return 0
            
        records = [{"trade_date": trade_date, "symbol": symbol, "contract_code": code, "updated_at": datetime.now()} for code in codes]
        
        operations = []
        for record in records:
            filter_query = {"trade_date": record["trade_date"], "symbol": record["symbol"], "contract_code": record["contract_code"]}
            operations.append(UpdateOne(filter_query, {"$set": record}, upsert=True))
            
        if operations:
            result = await self.col_option_sse_codes_sina.bulk_write(operations)
            return result.upserted_count + result.modified_count
        return 0


    async def fetch_and_save_option_sse_codes_sina(self, trade_date: str = "202002", symbol: str = "50ETF", exchange: str = "null") -> int:
        """获取并保存新浪期权看涨看跌合约代码"""
        try:
            logger.info(f"开始获取 {symbol} {trade_date} 合约代码...")
            codes = ak.option_sse_codes_sina(trade_date=trade_date, symbol=symbol, exchange=exchange)
            if codes and isinstance(codes, (list, tuple)):
                count = await self.save_option_sse_codes_sina(list(codes), trade_date, symbol)
                logger.info(f"成功保存 {count} 条 {symbol} {trade_date} 合约代码")
                return count
            else:
                logger.warning(f"{symbol} {trade_date} 合约代码数据为空")
                return 0
        except Exception as e:
            logger.error(f"获取 option_sse_codes_sina 失败: {e}")
            raise e


    async def clear_option_sse_codes_sina(self) -> int:
        """清空新浪期权看涨看跌合约代码"""
        result = await self.col_option_sse_codes_sina.delete_many({})
        return result.deleted_count


    async def save_option_current_em(self, df: pd.DataFrame) -> int:
        """保存期权实时数据"""
        if df is None or df.empty:
            return 0
        
        df_copy = df.copy()
        df_copy["updated_at"] = datetime.now()
        
        # Field mapping from Chinese to English
        field_mapping = {
            "代码": "code",
            "名称": "name",
            "交易日": "trade_date",
            "结算价": "settlement_price",
            "最新价": "latest_price",
            "涨跌幅": "change_pct",
            "成交量": "volume",
            "持仓量": "open_interest",
        }
        
        df_copy = df_copy.rename(columns=field_mapping)
        records = df_copy.to_dict("records")
        
        operations = []
        for record in records:
            filter_query = {"code": record.get("code")}
            operations.append(UpdateOne(filter_query, {"$set": record}, upsert=True))
        
        if operations:
            result = await self.col_option_current_em.bulk_write(operations)
            return result.upserted_count + result.modified_count
        return 0


    async def fetch_and_save_option_current_em(self) -> int:
        """获取并保存期权实时数据"""
        try:
            logger.info("开始获取期权实时数据...")
            df = ak.option_current_em()
            if df is not None and not df.empty:
                count = await self.save_option_current_em(df)
                logger.info(f"成功保存 {count} 条期权实时数据")
                return count
            else:
                logger.warning("期权实时数据为空")
                return 0
        except Exception as e:
            logger.error(f"获取 option_current_em 失败: {e}")
            raise e


    async def clear_option_current_em(self) -> int:
        """清空期权实时数据"""
        result = await self.col_option_current_em.delete_many({})
        return result.deleted_count


    async def save_option_sse_underlying_spot_price_sina(self, df: pd.DataFrame, symbol: str) -> int:
        """保存期权标的物的实时数据"""
        if df is None or df.empty:
            return 0
        
        df_copy = df.copy()
        df_copy["symbol"] = symbol
        df_copy["updated_at"] = datetime.now()
        
        # Rename columns to match model
        df_copy.columns = ["field", "value", "symbol", "updated_at"]
        records = df_copy.to_dict("records")
        
        operations = []
        for record in records:
            filter_query = {"symbol": record.get("symbol"), "field": record.get("field")}
            operations.append(UpdateOne(filter_query, {"$set": record}, upsert=True))
        
        if operations:
            result = await self.col_option_sse_underlying_spot_price_sina.bulk_write(operations)
            return result.upserted_count + result.modified_count
        return 0


    async def fetch_and_save_option_sse_underlying_spot_price_sina(self, symbol: str = "sh510300") -> int:
        """获取并保存期权标的物的实时数据"""
        try:
            logger.info(f"开始获取标的物 {symbol} 实时数据...")
            df = ak.option_sse_underlying_spot_price_sina(symbol=symbol)
            if df is not None and not df.empty:
                count = await self.save_option_sse_underlying_spot_price_sina(df, symbol)
                logger.info(f"成功保存 {count} 条标的物 {symbol} 实时数据")
                return count
            else:
                logger.warning(f"标的物 {symbol} 实时数据为空")
                return 0
        except Exception as e:
            logger.error(f"获取 option_sse_underlying_spot_price_sina 失败: {e}")
            raise e


    async def clear_option_sse_underlying_spot_price_sina(self) -> int:
        """清空期权标的物的实时数据"""
        result = await self.col_option_sse_underlying_spot_price_sina.delete_many({})
        return result.deleted_count


    async def save_option_sse_greeks_sina(self, df: pd.DataFrame) -> int:
        """保存新浪财经期权希腊字母信息"""
        if df is None or df.empty:
            return 0
        
        df_copy = df.copy()
        df_copy["updated_at"] = datetime.now()
        
        # Assuming df has columns matching the model
        records = df_copy.to_dict("records")
        
        operations = []
        for record in records:
            filter_query = {"symbol": record.get("symbol")}
            operations.append(UpdateOne(filter_query, {"$set": record}, upsert=True))
        
        if operations:
            result = await self.col_option_sse_greeks_sina.bulk_write(operations)
            return result.upserted_count + result.modified_count
        return 0


    async def fetch_and_save_option_sse_greeks_sina(self, symbol: str = "10004025") -> int:
        """获取并保存新浪财经期权希腊字母信息"""
        try:
            logger.info(f"开始获取合约 {symbol} 希腊字母数据...")
            df = ak.option_sse_greeks_sina(symbol=symbol)
            if df is not None and not df.empty:
                count = await self.save_option_sse_greeks_sina(df)
                logger.info(f"成功保存 {count} 条希腊字母数据")
                return count
            else:
                logger.warning(f"合约 {symbol} 希腊字母数据为空")
                return 0
        except Exception as e:
            logger.error(f"获取 option_sse_greeks_sina 失败: {e}")
            raise e


    async def clear_option_sse_greeks_sina(self) -> int:
        """清空新浪财经期权希腊字母信息"""
        result = await self.col_option_sse_greeks_sina.delete_many({})
        return result.deleted_count


    async def save_option_sse_minute_sina(self, df: pd.DataFrame, symbol: str) -> int:
        """保存期权行情分钟数据"""
        if df is None or df.empty:
            return 0
        
        df_copy = df.copy()
        df_copy["symbol"] = symbol
        df_copy["updated_at"] = datetime.now()
        
        records = df_copy.to_dict("records")
        
        operations = []
        for record in records:
            filter_query = {"symbol": record.get("symbol"), "datetime": record.get("datetime")}
            operations.append(UpdateOne(filter_query, {"$set": record}, upsert=True))
        
        if operations:
            result = await self.col_option_sse_minute_sina.bulk_write(operations)
            return result.upserted_count + result.modified_count
        return 0


    async def fetch_and_save_option_sse_minute_sina(self, symbol: str = "10004025") -> int:
        """获取并保存期权行情分钟数据"""
        try:
            logger.info(f"开始获取合约 {symbol} 分钟数据...")
            df = ak.option_sse_minute_sina(symbol=symbol)
            if df is not None and not df.empty:
                count = await self.save_option_sse_minute_sina(df, symbol)
                logger.info(f"成功保存 {count} 条分钟数据")
                return count
            else:
                logger.warning(f"合约 {symbol} 分钟数据为空")
                return 0
        except Exception as e:
            logger.error(f"获取 option_sse_minute_sina 失败: {e}")
            raise e


    async def clear_option_sse_minute_sina(self) -> int:
        """清空期权行情分钟数据"""
        result = await self.col_option_sse_minute_sina.delete_many({})
        return result.deleted_count


    async def save_option_sse_daily_sina(self, df: pd.DataFrame, symbol: str) -> int:
        """保存期权行情日数据"""
        if df is None or df.empty:
            return 0
        
        df_copy = df.copy()
        df_copy["symbol"] = symbol
        df_copy["updated_at"] = datetime.now()
        
        records = df_copy.to_dict("records")
        
        operations = []
        for record in records:
            filter_query = {"symbol": record.get("symbol"), "date": record.get("date")}
            operations.append(UpdateOne(filter_query, {"$set": record}, upsert=True))
        
        if operations:
            result = await self.col_option_sse_daily_sina.bulk_write(operations)
            return result.upserted_count + result.modified_count
        return 0


    async def fetch_and_save_option_sse_daily_sina(self, symbol: str = "10004025") -> int:
        """获取并保存期权行情日数据"""
        try:
            logger.info(f"开始获取合约 {symbol} 日数据...")
            df = ak.option_sse_daily_sina(symbol=symbol)
            if df is not None and not df.empty:
                count = await self.save_option_sse_daily_sina(df, symbol)
                logger.info(f"成功保存 {count} 条日数据")
                return count
            else:
                logger.warning(f"合约 {symbol} 日数据为空")
                return 0
        except Exception as e:
            logger.error(f"获取 option_sse_daily_sina 失败: {e}")
            raise e


    async def clear_option_sse_daily_sina(self) -> int:
        """清空期权行情日数据"""
        result = await self.col_option_sse_daily_sina.delete_many({})
        return result.deleted_count


    # Requirements 25-31 methods
    async def save_option_finance_minute_sina(self, df: pd.DataFrame, symbol: str) -> int:
        """保存新浪财经金融期权分时行情数据"""
        if df is None or df.empty:
            return 0
        
        df_copy = df.copy()
        df_copy["symbol"] = symbol
        df_copy["updated_at"] = datetime.now()
        
        records = df_copy.to_dict("records")
        
        operations = []
        for record in records:
            filter_query = {"symbol": record.get("symbol"), "date": record.get("date"), "time": record.get("time")}
            operations.append(UpdateOne(filter_query, {"$set": record}, upsert=True))
        
        if operations:
            result = await self.col_option_finance_minute_sina.bulk_write(operations)
            return result.upserted_count + result.modified_count
        return 0


    async def fetch_and_save_option_finance_minute_sina(self, symbol: str = "10002530") -> int:
        """获取并保存新浪财经金融期权分时行情数据"""
        try:
            logger.info(f"开始获取合约 {symbol} 分时行情数据...")
            df = ak.option_finance_minute_sina(symbol=symbol)
            if df is not None and not df.empty:
                count = await self.save_option_finance_minute_sina(df, symbol)
                logger.info(f"成功保存 {count} 条分时行情数据")
                return count
            else:
                logger.warning(f"合约 {symbol} 分时行情数据为空")
                return 0
        except Exception as e:
            logger.error(f"获取 option_finance_minute_sina 失败: {e}")
            raise e


    async def clear_option_finance_minute_sina(self) -> int:
        """清空新浪财经金融期权分时行情数据"""
        result = await self.col_option_finance_minute_sina.delete_many({})
        return result.deleted_count


    async def save_option_minute_em(self, df: pd.DataFrame, symbol: str) -> int:
        """保存东方财富网期权分时行情数据"""
        if df is None or df.empty:
            return 0
        
        df_copy = df.copy()
        df_copy["symbol"] = symbol
        df_copy["updated_at"] = datetime.now()
        
        records = df_copy.to_dict("records")
        
        operations = []
        for record in records:
            filter_query = {"symbol": record.get("symbol"), "datetime": record.get("datetime")}
            operations.append(UpdateOne(filter_query, {"$set": record}, upsert=True))
        
        if operations:
            result = await self.col_option_minute_em.bulk_write(operations)
            return result.upserted_count + result.modified_count
        return 0


    async def fetch_and_save_option_minute_em(self, symbol: str = "151.cu2404P61000") -> int:
        """获取并保存东方财富网期权分时行情数据"""
        try:
            logger.info(f"开始获取合约 {symbol} 东财分时行情数据...")
            df = ak.option_minute_em(symbol=symbol)
            if df is not None and not df.empty:
                count = await self.save_option_minute_em(df, symbol)
                logger.info(f"成功保存 {count} 条东财分时行情数据")
                return count
            else:
                logger.warning(f"合约 {symbol} 东财分时行情数据为空")
                return 0
        except Exception as e:
            logger.error(f"获取 option_minute_em 失败: {e}")
            raise e


    async def clear_option_minute_em(self) -> int:
        """清空东方财富网期权分时行情数据"""
        result = await self.col_option_minute_em.delete_many({})
        return result.deleted_count


    async def save_option_lhb_em(self, df: pd.DataFrame) -> int:
        """保存东方财富网期权龙虎榜数据"""
        if df is None or df.empty:
            return 0
        
        df_copy = df.copy()
        df_copy["updated_at"] = datetime.now()
        
        # Field mapping
        field_mapping = {
            "排名": "rank",
            "代码": "code",
            "名称": "name",
            "最新价": "latest_price",
            "涨跌幅": "change_pct",
            "成交量": "volume",
            "成交额": "turnover",
            "振幅": "amplitude",
        }
        
        df_copy = df_copy.rename(columns=field_mapping)
        records = df_copy.to_dict("records")
        
        operations = []
        for record in records:
            filter_query = {"code": record.get("code")}
            operations.append(UpdateOne(filter_query, {"$set": record}, upsert=True))
        
        if operations:
            result = await self.col_option_lhb_em.bulk_write(operations)
            return result.upserted_count + result.modified_count
        return 0


    async def fetch_and_save_option_lhb_em(self) -> int:
        """获取并保存东方财富网期权龙虎榜数据"""
        try:
            logger.info("开始获取期权龙虎榜数据...")
            df = ak.option_lhb_em()
            if df is not None and not df.empty:
                count = await self.save_option_lhb_em(df)
                logger.info(f"成功保存 {count} 条期权龙虎榜数据")
                return count
            else:
                logger.warning("期权龙虎榜数据为空")
                return 0
        except Exception as e:
            logger.error(f"获取 option_lhb_em 失败: {e}")
            raise e


    async def clear_option_lhb_em(self) -> int:
        """清空东方财富网期权龙虎榜数据"""
        result = await self.col_option_lhb_em.delete_many({})
        return result.deleted_count


    async def save_option_value_analysis_em(self, df: pd.DataFrame) -> int:
        """保存东方财富网期权价值分析数据"""
        if df is None or df.empty:
            return 0
        
        df_copy = df.copy()
        df_copy["updated_at"] = datetime.now()
        
        # Field mapping
        field_mapping = {
            "代码": "code",
            "名称": "name",
            "最新价": "latest_price",
            "内在价值": "intrinsic_value",
            "时间价值": "time_value",
        }
        
        df_copy = df_copy.rename(columns=field_mapping)
        records = df_copy.to_dict("records")
        
        operations = []
        for record in records:
            filter_query = {"code": record.get("code")}
            operations.append(UpdateOne(filter_query, {"$set": record}, upsert=True))
        
        if operations:
            result = await self.col_option_value_analysis_em.bulk_write(operations)
            return result.upserted_count + result.modified_count
        return 0


    async def fetch_and_save_option_value_analysis_em(self) -> int:
        """获取并保存东方财富网期权价值分析数据"""
        try:
            logger.info("开始获取期权价值分析数据...")
            df = ak.option_value_analysis_em()
            if df is not None and not df.empty:
                count = await self.save_option_value_analysis_em(df)
                logger.info(f"成功保存 {count} 条期权价值分析数据")
                return count
            else:
                logger.warning("期权价值分析数据为空")
                return 0
        except Exception as e:
            logger.error(f"获取 option_value_analysis_em 失败: {e}")
            raise e


    async def clear_option_value_analysis_em(self) -> int:
        """清空东方财富网期权价值分析数据"""
        result = await self.col_option_value_analysis_em.delete_many({})
        return result.deleted_count


    async def save_option_risk_analysis_em(self, df: pd.DataFrame) -> int:
        """保存东方财富网期权风险分析数据"""
        if df is None or df.empty:
            return 0
        
        df_copy = df.copy()
        df_copy["updated_at"] = datetime.now()
        
        # Field mapping
        field_mapping = {
            "代码": "code",
            "名称": "name",
            "杠杆比率": "leverage_ratio",
            "Delta": "delta",
            "Gamma": "gamma",
            "Theta": "theta",
            "Vega": "vega",
        }
        
        df_copy = df_copy.rename(columns=field_mapping)
        records = df_copy.to_dict("records")
        
        operations = []
        for record in records:
            filter_query = {"code": record.get("code")}
            operations.append(UpdateOne(filter_query, {"$set": record}, upsert=True))
        
        if operations:
            result = await self.col_option_risk_analysis_em.bulk_write(operations)
            return result.upserted_count + result.modified_count
        return 0


    async def fetch_and_save_option_risk_analysis_em(self) -> int:
        """获取并保存东方财富网期权风险分析数据"""
        try:
            logger.info("开始获取期权风险分析数据...")
            df = ak.option_risk_analysis_em()
            if df is not None and not df.empty:
                count = await self.save_option_risk_analysis_em(df)
                logger.info(f"成功保存 {count} 条期权风险分析数据")
                return count
            else:
                logger.warning("期权风险分析数据为空")
                return 0
        except Exception as e:
            logger.error(f"获取 option_risk_analysis_em 失败: {e}")
            raise e


    async def clear_option_risk_analysis_em(self) -> int:
        """清空东方财富网期权风险分析数据"""
        result = await self.col_option_risk_analysis_em.delete_many({})
        return result.deleted_count


    async def save_option_premium_analysis_em(self, df: pd.DataFrame) -> int:
        """保存东方财富网期权折溢价数据"""
        if df is None or df.empty:
            return 0
        
        df_copy = df.copy()
        df_copy["updated_at"] = datetime.now()
        
        # Field mapping
        field_mapping = {
            "代码": "code",
            "名称": "name",
            "溢价率": "premium_rate",
        }
        
        df_copy = df_copy.rename(columns=field_mapping)
        records = df_copy.to_dict("records")
        
        operations = []
        for record in records:
            filter_query = {"code": record.get("code")}
            operations.append(UpdateOne(filter_query, {"$set": record}, upsert=True))
        
        if operations:
            result = await self.col_option_premium_analysis_em.bulk_write(operations)
            return result.upserted_count + result.modified_count
        return 0


    async def fetch_and_save_option_premium_analysis_em(self) -> int:
        """获取并保存东方财富网期权折溢价数据"""
        try:
            logger.info("开始获取期权折溢价数据...")
            df = ak.option_premium_analysis_em()
            if df is not None and not df.empty:
                count = await self.save_option_premium_analysis_em(df)
                logger.info(f"成功保存 {count} 条期权折溢价数据")
                return count
            else:
                logger.warning("期权折溢价数据为空")
                return 0
        except Exception as e:
            logger.error(f"获取 option_premium_analysis_em 失败: {e}")
            raise e


    async def clear_option_premium_analysis_em(self) -> int:
        """清空东方财富网期权折溢价数据"""
        result = await self.col_option_premium_analysis_em.delete_many({})
        return result.deleted_count


    # Requirements 32-36 commodity options methods
    async def save_option_commodity_contract_sina(self, contracts: List[str], symbol: str) -> int:
        """保存新浪财经商品期权在交易合约"""
        if not contracts:
            return 0
            
        records = [{"symbol": symbol, "contract": contract, "updated_at": datetime.now()} for contract in contracts]
        
        operations = []
        for record in records:
            filter_query = {"symbol": record["symbol"], "contract": record["contract"]}
            operations.append(UpdateOne(filter_query, {"$set": record}, upsert=True))
            
        if operations:
            result = await self.col_option_commodity_contract_sina.bulk_write(operations)
            return result.upserted_count + result.modified_count
        return 0


    async def fetch_and_save_option_commodity_contract_sina(self, symbol: str = "SR") -> int:
        """获取并保存新浪财经商品期权在交易合约"""
        try:
            logger.info(f"开始获取商品期权 {symbol} 在交易合约...")
            contracts = ak.option_commodity_contract_sina(symbol=symbol)
            if contracts and isinstance(contracts, (list, tuple)):
                count = await self.save_option_commodity_contract_sina(list(contracts), symbol)
                logger.info(f"成功保存 {count} 条商品期权合约")
                return count
            else:
                logger.warning(f"商品期权 {symbol} 合约数据为空")
                return 0
        except Exception as e:
            logger.error(f"获取 option_commodity_contract_sina 失败: {e}")
            raise e


    async def clear_option_commodity_contract_sina(self) -> int:
        """清空新浪财经商品期权在交易合约数据"""
        result = await self.col_option_commodity_contract_sina.delete_many({})
        return result.deleted_count


    async def save_option_commodity_contract_table_sina(self, df: pd.DataFrame, symbol: str) -> int:
        """保存新浪财经商品期权T型报价表"""
        if df is None or df.empty:
            return 0
        
        df_copy = df.copy()
        df_copy["symbol"] = symbol
        df_copy["updated_at"] = datetime.now()
        
        records = df_copy.to_dict("records")
        
        operations = []
        for record in records:
            filter_query = {"symbol": record.get("symbol"), "contract": record.get("contract")}
            operations.append(UpdateOne(filter_query, {"$set": record}, upsert=True))
        
        if operations:
            result = await self.col_option_commodity_contract_table_sina.bulk_write(operations)
            return result.upserted_count + result.modified_count
        return 0


    async def fetch_and_save_option_commodity_contract_table_sina(self, symbol: str = "SR", contract: str = "2405") -> int:
        """获取并保存新浪财经商品期权T型报价表"""
        try:
            logger.info(f"开始获取商品期权 {symbol} {contract} T型报价表...")
            df = ak.option_commodity_contract_table_sina(symbol=symbol, contract=contract)
            if df is not None and not df.empty:
                count = await self.save_option_commodity_contract_table_sina(df, symbol)
                logger.info(f"成功保存 {count} 条T型报价数据")
                return count
            else:
                logger.warning(f"商品期权 {symbol} {contract} T型报价表为空")
                return 0
        except Exception as e:
            logger.error(f"获取 option_commodity_contract_table_sina 失败: {e}")
            raise e


    async def clear_option_commodity_contract_table_sina(self) -> int:
        """清空新浪财经商品期权T型报价表数据"""
        result = await self.col_option_commodity_contract_table_sina.delete_many({})
        return result.deleted_count


    async def save_option_commodity_hist_sina(self, df: pd.DataFrame, symbol: str) -> int:
        """保存新浪财经商品期权历史行情数据"""
        if df is None or df.empty:
            return 0
        
        df_copy = df.copy()
        df_copy["symbol"] = symbol
        df_copy["updated_at"] = datetime.now()
        
        records = df_copy.to_dict("records")
        
        operations = []
        for record in records:
            filter_query = {"symbol": record.get("symbol"), "date": record.get("date")}
            operations.append(UpdateOne(filter_query, {"$set": record}, upsert=True))
        
        if operations:
            result = await self.col_option_commodity_hist_sina.bulk_write(operations)
            return result.upserted_count + result.modified_count
        return 0


    async def fetch_and_save_option_commodity_hist_sina(self, symbol: str = "SR405C7000") -> int:
        """获取并保存新浪财经商品期权历史行情数据"""
        try:
            logger.info(f"开始获取商品期权 {symbol} 历史行情...")
            df = ak.option_commodity_hist_sina(symbol=symbol)
            if df is not None and not df.empty:
                count = await self.save_option_commodity_hist_sina(df, symbol)
                logger.info(f"成功保存 {count} 条商品期权历史行情")
                return count
            else:
                logger.warning(f"商品期权 {symbol} 历史行情为空")
                return 0
        except Exception as e:
            logger.error(f"获取 option_commodity_hist_sina 失败: {e}")
            raise e


    async def clear_option_commodity_hist_sina(self) -> int:
        """清空新浪财经商品期权历史行情数据"""
        result = await self.col_option_commodity_hist_sina.delete_many({})
        return result.deleted_count


    async def save_option_comm_info(self, df: pd.DataFrame) -> int:
        """保存九期网商品期权手续费数据"""
        if df is None or df.empty:
            return 0
        
        df_copy = df.copy()
        df_copy["updated_at"] = datetime.now()
        
        # Field mapping
        field_mapping = {
            "交易所": "exchange",
            "品种": "symbol",
            "手续费类型": "fee_type",
            "手续费率": "fee_rate",
        }
        
        df_copy = df_copy.rename(columns=field_mapping)
        records = df_copy.to_dict("records")
        
        operations = []
        for record in records:
            filter_query = {"exchange": record.get("exchange"), "symbol": record.get("symbol")}
            operations.append(UpdateOne(filter_query, {"$set": record}, upsert=True))
        
        if operations:
            result = await self.col_option_comm_info.bulk_write(operations)
            return result.upserted_count + result.modified_count
        return 0


    async def fetch_and_save_option_comm_info(self) -> int:
        """获取并保存九期网商品期权手续费数据"""
        try:
            logger.info("开始获取商品期权手续费数据...")
            df = ak.option_comm_info()
            if df is not None and not df.empty:
                count = await self.save_option_comm_info(df)
                logger.info(f"成功保存 {count} 条商品期权手续费数据")
                return count
            else:
                logger.warning("商品期权手续费数据为空")
                return 0
        except Exception as e:
            logger.error(f"获取 option_comm_info 失败: {e}")
            raise e


    async def clear_option_comm_info(self) -> int:
        """清空九期网商品期权手续费数据"""
        result = await self.col_option_comm_info.delete_many({})
        return result.deleted_count


    async def save_option_margin(self, df: pd.DataFrame) -> int:
        """保存唯爱期货期权保证金数据"""
        if df is None or df.empty:
            return 0
        
        df_copy = df.copy()
        df_copy["updated_at"] = datetime.now()
        
        # Field mapping
        field_mapping = {
            "交易所": "exchange",
            "品种": "symbol",
            "保证金率": "margin_rate",
        }
        
        df_copy = df_copy.rename(columns=field_mapping)
        records = df_copy.to_dict("records")
        
        operations = []
        for record in records:
            filter_query = {"exchange": record.get("exchange"), "symbol": record.get("symbol")}
            operations.append(UpdateOne(filter_query, {"$set": record}, upsert=True))
        
        if operations:
            result = await self.col_option_margin.bulk_write(operations)
            return result.upserted_count + result.modified_count
        return 0


    async def fetch_and_save_option_margin(self) -> int:
        """获取并保存唯爱期货期权保证金数据"""
        try:
            logger.info("开始获取期权保证金数据...")
            df = ak.option_margin()
            if df is not None and not df.empty:
                count = await self.save_option_margin(df)
                logger.info(f"成功保存 {count} 条期权保证金数据")
                return count
            else:
                logger.warning("期权保证金数据为空")
                return 0
        except Exception as e:
            logger.error(f"获取 option_margin 失败: {e}")
            raise e


    async def clear_option_margin(self) -> int:
        """清空唯爱期货期权保证金数据"""
        result = await self.col_option_margin.delete_many({})
        return result.deleted_count


    # Requirements 37-42 exchange commodity options methods
    async def save_option_hist_shfe(self, df: pd.DataFrame) -> int:
        """保存上海期货交易所商品期权数据"""
        if df is None or df.empty:
            return 0
        
        df_copy = df.copy()
        df_copy["updated_at"] = datetime.now()
        
        records = df_copy.to_dict("records")
        
        operations = []
        for record in records:
            filter_query = {"trade_date": record.get("trade_date"), "symbol": record.get("symbol")}
            operations.append(UpdateOne(filter_query, {"$set": record}, upsert=True))
        
        if operations:
            result = await self.col_option_hist_shfe.bulk_write(operations)
            return result.upserted_count + result.modified_count
        return 0


    async def fetch_and_save_option_hist_shfe(self, trade_date: str = "20231201") -> int:
        """获取并保存上海期货交易所商品期权数据"""
        try:
            logger.info(f"开始获取上期所商品期权数据 {trade_date}...")
            df = ak.option_hist_shfe(trade_date=trade_date)
            if df is not None and not df.empty:
                count = await self.save_option_hist_shfe(df)
                logger.info(f"成功保存 {count} 条上期所商品期权数据")
                return count
            else:
                logger.warning(f"上期所商品期权数据 {trade_date} 为空")
                return 0
        except Exception as e:
            logger.error(f"获取 option_hist_shfe 失败: {e}")
            raise e


    async def clear_option_hist_shfe(self) -> int:
        """清空上海期货交易所商品期权数据"""
        result = await self.col_option_hist_shfe.delete_many({})
        return result.deleted_count


    async def save_option_hist_dce(self, df: pd.DataFrame) -> int:
        """保存大连商品交易所商品期权数据"""
        if df is None or df.empty:
            return 0
        
        df_copy = df.copy()
        df_copy["updated_at"] = datetime.now()
        
        records = df_copy.to_dict("records")
        
        operations = []
        for record in records:
            filter_query = {"trade_date": record.get("trade_date"), "symbol": record.get("symbol")}
            operations.append(UpdateOne(filter_query, {"$set": record}, upsert=True))
        
        if operations:
            result = await self.col_option_hist_dce.bulk_write(operations)
            return result.upserted_count + result.modified_count
        return 0


    async def fetch_and_save_option_hist_dce(self, trade_date: str = "20231201") -> int:
        """获取并保存大连商品交易所商品期权数据"""
        try:
            logger.info(f"开始获取大商所商品期权数据 {trade_date}...")
            df = ak.option_hist_dce(trade_date=trade_date)
            if df is not None and not df.empty:
                count = await self.save_option_hist_dce(df)
                logger.info(f"成功保存 {count} 条大商所商品期权数据")
                return count
            else:
                logger.warning(f"大商所商品期权数据 {trade_date} 为空")
                return 0
        except Exception as e:
            logger.error(f"获取 option_hist_dce 失败: {e}")
            raise e


    async def clear_option_hist_dce(self) -> int:
        """清空大连商品交易所商品期权数据"""
        result = await self.col_option_hist_dce.delete_many({})
        return result.deleted_count


    async def save_option_hist_czce(self, df: pd.DataFrame) -> int:
        """保存郑州商品交易所商品期权数据"""
        if df is None or df.empty:
            return 0
        
        df_copy = df.copy()
        df_copy["updated_at"] = datetime.now()
        
        records = df_copy.to_dict("records")
        
        operations = []
        for record in records:
            filter_query = {"trade_date": record.get("trade_date"), "symbol": record.get("symbol")}
            operations.append(UpdateOne(filter_query, {"$set": record}, upsert=True))
        
        if operations:
            result = await self.col_option_hist_czce.bulk_write(operations)
            return result.upserted_count + result.modified_count
        return 0


    async def fetch_and_save_option_hist_czce(self, trade_date: str = "20231201") -> int:
        """获取并保存郑州商品交易所商品期权数据"""
        try:
            logger.info(f"开始获取郑商所商品期权数据 {trade_date}...")
            df = ak.option_hist_czce(trade_date=trade_date)
            if df is not None and not df.empty:
                count = await self.save_option_hist_czce(df)
                logger.info(f"成功保存 {count} 条郑商所商品期权数据")
                return count
            else:
                logger.warning(f"郑商所商品期权数据 {trade_date} 为空")
                return 0
        except Exception as e:
            logger.error(f"获取 option_hist_czce 失败: {e}")
            raise e


    async def clear_option_hist_czce(self) -> int:
        """清空郑州商品交易所商品期权数据"""
        result = await self.col_option_hist_czce.delete_many({})
        return result.deleted_count


    async def save_option_hist_gfex(self, df: pd.DataFrame) -> int:
        """保存广州期货交易所商品期权数据"""
        if df is None or df.empty:
            return 0
        
        df_copy = df.copy()
        df_copy["updated_at"] = datetime.now()
        
        records = df_copy.to_dict("records")
        
        operations = []
        for record in records:
            filter_query = {"trade_date": record.get("trade_date"), "symbol": record.get("symbol")}
            operations.append(UpdateOne(filter_query, {"$set": record}, upsert=True))
        
        if operations:
            result = await self.col_option_hist_gfex.bulk_write(operations)
            return result.upserted_count + result.modified_count
        return 0


    async def fetch_and_save_option_hist_gfex(self, trade_date: str = "20231201") -> int:
        """获取并保存广州期货交易所商品期权数据"""
        try:
            logger.info(f"开始获取广期所商品期权数据 {trade_date}...")
            df = ak.option_hist_gfex(trade_date=trade_date)
            if df is not None and not df.empty:
                count = await self.save_option_hist_gfex(df)
                logger.info(f"成功保存 {count} 条广期所商品期权数据")
                return count
            else:
                logger.warning(f"广期所商品期权数据 {trade_date} 为空")
                return 0
        except Exception as e:
            logger.error(f"获取 option_hist_gfex 失败: {e}")
            raise e


    async def clear_option_hist_gfex(self) -> int:
        """清空广州期货交易所商品期权数据"""
        result = await self.col_option_hist_gfex.delete_many({})
        return result.deleted_count


    async def save_option_vol_gfex(self, df: pd.DataFrame) -> int:
        """保存广州期货交易所商品期权隐含波动率数据"""
        if df is None or df.empty:
            return 0
        
        df_copy = df.copy()
        df_copy["updated_at"] = datetime.now()
        
        records = df_copy.to_dict("records")
        
        operations = []
        for record in records:
            filter_query = {"trade_date": record.get("trade_date"), "symbol": record.get("symbol")}
            operations.append(UpdateOne(filter_query, {"$set": record}, upsert=True))
        
        if operations:
            result = await self.col_option_vol_gfex.bulk_write(operations)
            return result.upserted_count + result.modified_count
        return 0


    async def fetch_and_save_option_vol_gfex(self, trade_date: str = "20231201") -> int:
        """获取并保存广州期货交易所商品期权隐含波动率数据"""
        try:
            logger.info(f"开始获取广期所隐含波动率数据 {trade_date}...")
            df = ak.option_vol_gfex(trade_date=trade_date)
            if df is not None and not df.empty:
                count = await self.save_option_vol_gfex(df)
                logger.info(f"成功保存 {count} 条广期所隐含波动率数据")
                return count
            else:
                logger.warning(f"广期所隐含波动率数据 {trade_date} 为空")
                return 0
        except Exception as e:
            logger.error(f"获取 option_vol_gfex 失败: {e}")
            raise e


    async def clear_option_vol_gfex(self) -> int:
        """清空广州期货交易所商品期权隐含波动率数据"""
        result = await self.col_option_vol_gfex.delete_many({})
        return result.deleted_count


    async def save_option_czce_hist(self, df: pd.DataFrame) -> int:
        """保存郑州商品交易所商品期权历史行情数据"""
        if df is None or df.empty:
            return 0
        
        df_copy = df.copy()
        df_copy["updated_at"] = datetime.now()
        
        records = df_copy.to_dict("records")
        
        operations = []
        for record in records:
            filter_query = {"trade_date": record.get("trade_date"), "symbol": record.get("symbol")}
            operations.append(UpdateOne(filter_query, {"$set": record}, upsert=True))
        
        if operations:
            result = await self.col_option_czce_hist.bulk_write(operations)
            return result.upserted_count + result.modified_count
        return 0


    async def fetch_and_save_option_czce_hist(self, symbol: str = "CF", start_date: str = "20231101", end_date: str = "20231201") -> int:
        """获取并保存郑州商品交易所商品期权历史行情数据"""
        try:
            logger.info(f"开始获取郑商所期权历史行情 {symbol} {start_date}-{end_date}...")
            df = ak.option_czce_hist(symbol=symbol, start_date=start_date, end_date=end_date)
            if df is not None and not df.empty:
                count = await self.save_option_czce_hist(df)
                logger.info(f"成功保存 {count} 条郑商所期权历史行情")
                return count
            else:
                logger.warning(f"郑商所期权历史行情 {symbol} 为空")
                return 0
        except Exception as e:
            logger.error(f"获取 option_czce_hist 失败: {e}")
            raise e


    async def clear_option_czce_hist(self) -> int:
        """清空郑州商品交易所商品期权历史行情数据"""
        result = await self.col_option_czce_hist.delete_many({})
        return result.deleted_count







