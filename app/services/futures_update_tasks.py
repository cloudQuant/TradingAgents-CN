"""
期货数据更新任务函数
包含001-052号新增集合的所有update任务函数
"""
import logging
from datetime import datetime
from app.core.database import get_mongo_db

logger = logging.getLogger("webapi")


# 001 futures_fees_info
async def update_futures_fees_info_task():
    """更新期货交易费用参照表任务
    
    无需参数，获取所有期货交易费用数据
    """
    try:
        import akshare as ak
        logger.info("开始更新期货交易费用参照表")
        
        try:
            df = ak.futures_fees_info()
        except Exception as e:
            logger.error(f"获取期货交易费用参照表失败: {e}")
            return
        
        if df is None or df.empty:
            logger.warning("获取期货交易费用参照表为空")
            return
        
        data = df.to_dict(orient="records")
        db = get_mongo_db()
        collection = db.get_collection("futures_fees_info")
        
        count = 0
        for item in data:
            item["update_time"] = datetime.now()
            # 唯一键：交易所 + 合约代码
            key = {"交易所": item.get("交易所"), "合约代码": item.get("合约代码")}
            if key["交易所"] and key["合约代码"]:
                await collection.update_one(key, {"$set": item}, upsert=True)
                count += 1
        
        logger.info(f"期货交易费用参照表更新完成，共处理 {count} 条记录")
    except Exception as e:
        logger.error(f"更新期货交易费用参照表失败: {e}", exc_info=True)


# 002 futures_comm_info
async def update_futures_comm_info_task(symbol: str = "所有"):
    """更新期货手续费与保证金任务
    
    Args:
        symbol: 交易所选择，默认"所有"
    """
    try:
        import akshare as ak
        logger.info(f"开始更新期货手续费与保证金 (symbol={symbol})")
        
        try:
            df = ak.futures_comm_info(symbol=symbol)
        except Exception as e:
            logger.error(f"获取期货手续费与保证金失败 (symbol={symbol}): {e}")
            return
        
        if df is None or df.empty:
            logger.warning(f"获取期货手续费与保证金为空 (symbol={symbol})")
            return
        
        data = df.to_dict(orient="records")
        db = get_mongo_db()
        collection = db.get_collection("futures_comm_info")
        
        count = 0
        for item in data:
            item["update_time"] = datetime.now()
            item["query_symbol"] = symbol
            # 唯一键：交易所名称 + 合约代码
            key = {"交易所名称": item.get("交易所名称"), "合约代码": item.get("合约代码")}
            if key["交易所名称"] and key["合约代码"]:
                await collection.update_one(key, {"$set": item}, upsert=True)
                count += 1
        
        logger.info(f"期货手续费与保证金更新完成，共处理 {count} 条记录 (symbol={symbol})")
    except Exception as e:
        logger.error(f"更新期货手续费与保证金失败: {e}", exc_info=True)


# 003 futures_rule
async def update_futures_rule_task(date: str = None):
    """更新期货规则-交易日历表任务
    
    Args:
        date: 交易日期，格式YYYYMMDD，需要是近期交易日
    """
    try:
        import akshare as ak
        
        # 如果未提供日期，使用今天或最近的工作日
        if not date:
            from datetime import datetime, timedelta
            today = datetime.now()
            # 简单处理：如果是周末，往前推到周五
            if today.weekday() == 5:  # 周六
                today = today - timedelta(days=1)
            elif today.weekday() == 6:  # 周日
                today = today - timedelta(days=2)
            date = today.strftime("%Y%m%d")
        
        logger.info(f"开始更新期货规则-交易日历表 (date={date})")
        
        try:
            df = ak.futures_rule(date=date)
        except Exception as e:
            logger.error(f"获取期货规则-交易日历表失败 (date={date}): {e}")
            return
        
        if df is None or df.empty:
            logger.warning(f"获取期货规则-交易日历表为空 (date={date})")
            return
        
        data = df.to_dict(orient="records")
        db = get_mongo_db()
        collection = db.get_collection("futures_rule")
        
        count = 0
        for item in data:
            item["update_time"] = datetime.now()
            item["query_date"] = date
            # 唯一键：交易所 + 代码 + 日期
            key = {"交易所": item.get("交易所"), "代码": item.get("代码"), "query_date": date}
            if key["交易所"] and key["代码"]:
                await collection.update_one(key, {"$set": item}, upsert=True)
                count += 1
        
        logger.info(f"期货规则-交易日历表更新完成，共处理 {count} 条记录 (date={date})")
    except Exception as e:
        logger.error(f"更新期货规则-交易日历表失败: {e}", exc_info=True)


# 004 futures_inventory_99
async def update_futures_inventory_99_task(symbol: str):
    """更新库存数据-99期货网任务
    
    Args:
        symbol: 品种名称或代码，如"豆一"
    """
    try:
        import akshare as ak
        logger.info(f"开始更新库存数据-99期货网 (symbol={symbol})")
        
        if not symbol:
            logger.error("需要提供symbol参数")
            return
        
        try:
            df = ak.futures_inventory_99(symbol=symbol)
        except Exception as e:
            logger.error(f"获取库存数据-99期货网失败 (symbol={symbol}): {e}")
            return
        
        if df is None or df.empty:
            logger.warning(f"获取库存数据-99期货网为空 (symbol={symbol})")
            return
        
        data = df.to_dict(orient="records")
        db = get_mongo_db()
        collection = db.get_collection("futures_inventory_99")
        
        count = 0
        for item in data:
            item["update_time"] = datetime.now()
            item["query_symbol"] = symbol
            # 唯一键：symbol + 日期
            key = {"query_symbol": symbol, "日期": item.get("日期")}
            if key["日期"]:
                await collection.update_one(key, {"$set": item}, upsert=True)
                count += 1
        
        logger.info(f"库存数据-99期货网更新完成，共处理 {count} 条记录 (symbol={symbol})")
    except Exception as e:
        logger.error(f"更新库存数据-99期货网失败: {e}", exc_info=True)


# 005 futures_inventory_em
async def update_futures_inventory_em_task(symbol: str):
    """更新库存数据-东方财富任务
    
    Args:
        symbol: 品种代码或名称，如"A"
    """
    try:
        import akshare as ak
        logger.info(f"开始更新库存数据-东方财富 (symbol={symbol})")
        
        if not symbol:
            logger.error("需要提供symbol参数")
            return
        
        try:
            df = ak.futures_inventory_em(symbol=symbol)
        except Exception as e:
            logger.error(f"获取库存数据-东方财富失败 (symbol={symbol}): {e}")
            return
        
        if df is None or df.empty:
            logger.warning(f"获取库存数据-东方财富为空 (symbol={symbol})")
            return
        
        data = df.to_dict(orient="records")
        db = get_mongo_db()
        collection = db.get_collection("futures_inventory_em")
        
        count = 0
        for item in data:
            item["update_time"] = datetime.now()
            item["query_symbol"] = symbol
            # 唯一键：symbol + 日期
            key = {"query_symbol": symbol, "日期": item.get("日期")}
            if key["日期"]:
                await collection.update_one(key, {"$set": item}, upsert=True)
                count += 1
        
        logger.info(f"库存数据-东方财富更新完成，共处理 {count} 条记录 (symbol={symbol})")
    except Exception as e:
        logger.error(f"更新库存数据-东方财富失败: {e}", exc_info=True)


# 006 futures_dce_position_rank
async def update_futures_dce_position_rank_task(date: str, vars_list: list = None):
    """更新大连商品交易所持仓排名任务
    
    Args:
        date: 交易日期，格式YYYYMMDD
        vars_list: 品种列表，如["C", "CS"]，默认None获取全部
    """
    try:
        import akshare as ak
        logger.info(f"开始更新大连商品交易所持仓排名 (date={date}, vars_list={vars_list})")
        
        if not date:
            logger.error("需要提供date参数")
            return
        
        try:
            # API返回字典：{合约名: DataFrame}
            if vars_list:
                data_dict = ak.futures_dce_position_rank(date=date, vars_list=vars_list)
            else:
                data_dict = ak.futures_dce_position_rank(date=date)
        except Exception as e:
            logger.error(f"获取大连商品交易所持仓排名失败 (date={date}): {e}")
            return
        
        if not data_dict:
            logger.warning(f"获取大连商品交易所持仓排名为空 (date={date})")
            return
        
        db = get_mongo_db()
        collection = db.get_collection("futures_dce_position_rank")
        
        total_count = 0
        for symbol, df in data_dict.items():
            if df is None or df.empty:
                continue
            
            data = df.to_dict(orient="records")
            for item in data:
                item["update_time"] = datetime.now()
                item["query_date"] = date
                item["symbol"] = symbol
                # 唯一键：date + symbol + 名次
                key = {"query_date": date, "symbol": symbol, "名次": item.get("名次")}
                if key["名次"] is not None:
                    await collection.update_one(key, {"$set": item}, upsert=True)
                    total_count += 1
        
        logger.info(f"大连商品交易所持仓排名更新完成，共处理 {total_count} 条记录 (date={date})")
    except Exception as e:
        logger.error(f"更新大连商品交易所持仓排名失败: {e}", exc_info=True)


# 007 futures_gfex_position_rank
async def update_futures_gfex_position_rank_task(date: str, vars_list: list = None):
    """更新广州期货交易所日成交持仓排名任务
    
    Args:
        date: 交易日期，格式YYYYMMDD
        vars_list: 品种列表，如["SI", "LC"]，默认None获取全部
    """
    try:
        import akshare as ak
        logger.info(f"开始更新广州期货交易所日成交持仓排名 (date={date}, vars_list={vars_list})")
        
        if not date:
            logger.error("需要提供date参数")
            return
        
        try:
            # API返回字典：{合约名: DataFrame}
            if vars_list:
                data_dict = ak.futures_gfex_position_rank(date=date, vars_list=vars_list)
            else:
                data_dict = ak.futures_gfex_position_rank(date=date)
        except Exception as e:
            logger.error(f"获取广州期货交易所日成交持仓排名失败 (date={date}): {e}")
            return
        
        if not data_dict:
            logger.warning(f"获取广州期货交易所日成交持仓排名为空 (date={date})")
            return
        
        db = get_mongo_db()
        collection = db.get_collection("futures_gfex_position_rank")
        
        total_count = 0
        for symbol, df in data_dict.items():
            if df is None or df.empty:
                continue
            
            data = df.to_dict(orient="records")
            for item in data:
                item["update_time"] = datetime.now()
                item["query_date"] = date
                item["symbol"] = symbol
                # 唯一键：date + symbol + 名次
                key = {"query_date": date, "symbol": symbol, "名次": item.get("名次")}
                if key["名次"] is not None:
                    await collection.update_one(key, {"$set": item}, upsert=True)
                    total_count += 1
        
        logger.info(f"广州期货交易所日成交持仓排名更新完成，共处理 {total_count} 条记录 (date={date})")
    except Exception as e:
        logger.error(f"更新广州期货交易所日成交持仓排名失败: {e}", exc_info=True)


# 008 futures_warehouse_receipt_czce
async def update_futures_warehouse_receipt_czce_task(date: str):
    """更新郑州商品交易所仓单日报任务
    
    Args:
        date: 交易日期，格式YYYYMMDD
    """
    try:
        import akshare as ak
        logger.info(f"开始更新郑州商品交易所仓单日报 (date={date})")
        
        if not date:
            logger.error("需要提供date参数")
            return
        
        try:
            # API返回字典：{品种代码: DataFrame}
            data_dict = ak.futures_warehouse_receipt_czce(date=date)
        except Exception as e:
            logger.error(f"获取郑州商品交易所仓单日报失败 (date={date}): {e}")
            return
        
        if not data_dict:
            logger.warning(f"获取郑州商品交易所仓单日报为空 (date={date})")
            return
        
        db = get_mongo_db()
        collection = db.get_collection("futures_warehouse_receipt_czce")
        
        total_count = 0
        for symbol, df in data_dict.items():
            if df is None or df.empty:
                continue
            
            data = df.to_dict(orient="records")
            for item in data:
                item["update_time"] = datetime.now()
                item["query_date"] = date
                item["symbol"] = symbol
                # 唯一键：date + symbol + 仓库名称（如果有）
                # 检查数据字段，可能有"仓库"、"仓库名称"等字段
                warehouse = item.get("仓库") or item.get("仓库名称") or item.get("warehouse")
                key = {"query_date": date, "symbol": symbol}
                if warehouse:
                    key["warehouse"] = warehouse
                await collection.update_one(key, {"$set": item}, upsert=True)
                total_count += 1
        
        logger.info(f"郑州商品交易所仓单日报更新完成，共处理 {total_count} 条记录 (date={date})")
    except Exception as e:
        logger.error(f"更新郑州商品交易所仓单日报失败: {e}", exc_info=True)


# 009 futures_warehouse_receipt_dce
async def update_futures_warehouse_receipt_dce_task(date: str):
    """更新大连商品交易所仓单日报任务
    
    Args:
        date: 交易日期，格式YYYYMMDD
    """
    try:
        import akshare as ak
        logger.info(f"开始更新大连商品交易所仓单日报 (date={date})")
        
        if not date:
            logger.error("需要提供date参数")
            return
        
        try:
            df = ak.futures_warehouse_receipt_dce(date=date)
        except Exception as e:
            logger.error(f"获取大连商品交易所仓单日报失败 (date={date}): {e}")
            return
        
        if df is None or df.empty:
            logger.warning(f"获取大连商品交易所仓单日报为空 (date={date})")
            return
        
        db = get_mongo_db()
        collection = db.get_collection("futures_warehouse_receipt_dce")
        
        data = df.to_dict(orient="records")
        count = 0
        for item in data:
            item["update_time"] = datetime.now()
            item["query_date"] = date
            # 唯一键：date + 品种代码 + 仓库/分库
            key = {"query_date": date, "品种代码": item.get("品种代码"), "仓库/分库": item.get("仓库/分库")}
            if key["品种代码"]:
                await collection.update_one(key, {"$set": item}, upsert=True)
                count += 1
        
        logger.info(f"大连商品交易所仓单日报更新完成，共处理 {count} 条记录 (date={date})")
    except Exception as e:
        logger.error(f"更新大连商品交易所仓单日报失败: {e}", exc_info=True)


# 010 futures_shfe_warehouse_receipt
async def update_futures_shfe_warehouse_receipt_task(date: str):
    """更新上海期货交易所仓单日报任务
    
    Args:
        date: 交易日期，格式YYYYMMDD
    """
    try:
        import akshare as ak
        logger.info(f"开始更新上海期货交易所仓单日报 (date={date})")
        
        if not date:
            logger.error("需要提供date参数")
            return
        
        try:
            # API返回字典：{品种代码: DataFrame}
            data_dict = ak.futures_shfe_warehouse_receipt(date=date)
        except Exception as e:
            logger.error(f"获取上海期货交易所仓单日报失败 (date={date}): {e}")
            return
        
        if not data_dict:
            logger.warning(f"获取上海期货交易所仓单日报为空 (date={date})")
            return
        
        db = get_mongo_db()
        collection = db.get_collection("futures_shfe_warehouse_receipt")
        
        total_count = 0
        for symbol, df in data_dict.items():
            if df is None or df.empty:
                continue
            
            data = df.to_dict(orient="records")
            for item in data:
                item["update_time"] = datetime.now()
                item["query_date"] = date
                item["symbol"] = symbol
                # 唯一键：date + symbol + 仓库（如果有）
                warehouse = item.get("仓库") or item.get("仓库名称") or item.get("地点")
                key = {"query_date": date, "symbol": symbol}
                if warehouse:
                    key["warehouse"] = warehouse
                await collection.update_one(key, {"$set": item}, upsert=True)
                total_count += 1
        
        logger.info(f"上海期货交易所仓单日报更新完成，共处理 {total_count} 条记录 (date={date})")
    except Exception as e:
        logger.error(f"更新上海期货交易所仓单日报失败: {e}", exc_info=True)


# 011 futures_gfex_warehouse_receipt
async def update_futures_gfex_warehouse_receipt_task(date: str):
    """更新广州期货交易所仓单日报任务
    
    Args:
        date: 交易日期，格式YYYYMMDD
    """
    try:
        import akshare as ak
        logger.info(f"开始更新广州期货交易所仓单日报 (date={date})")
        
        if not date:
            logger.error("需要提供date参数")
            return
        
        try:
            # API返回字典：{品种代码: DataFrame}
            data_dict = ak.futures_gfex_warehouse_receipt(date=date)
        except Exception as e:
            logger.error(f"获取广州期货交易所仓单日报失败 (date={date}): {e}")
            return
        
        if not data_dict:
            logger.warning(f"获取广州期货交易所仓单日报为空 (date={date})")
            return
        
        db = get_mongo_db()
        collection = db.get_collection("futures_gfex_warehouse_receipt")
        
        total_count = 0
        for symbol, df in data_dict.items():
            if df is None or df.empty:
                continue
            
            data = df.to_dict(orient="records")
            for item in data:
                item["update_time"] = datetime.now()
                item["query_date"] = date
                item["symbol"] = symbol
                # 唯一键：date + symbol + 仓库（如果有）
                warehouse = item.get("仓库") or item.get("仓库名称")
                key = {"query_date": date, "symbol": symbol}
                if warehouse:
                    key["warehouse"] = warehouse
                await collection.update_one(key, {"$set": item}, upsert=True)
                total_count += 1
        
        logger.info(f"广州期货交易所仓单日报更新完成，共处理 {total_count} 条记录 (date={date})")
    except Exception as e:
        logger.error(f"更新广州期货交易所仓单日报失败: {e}", exc_info=True)


# 012 futures_to_spot_dce
async def update_futures_to_spot_dce_task(date: str):
    """更新大连商品交易所期转现统计数据任务
    
    Args:
        date: 交易年月，格式YYYYMM（例如：202312）
    """
    try:
        import akshare as ak
        logger.info(f"开始更新大连商品交易所期转现统计数据 (date={date})")
        
        if not date:
            logger.error("需要提供date参数")
            return
        
        try:
            df = ak.futures_to_spot_dce(date=date)
        except Exception as e:
            logger.error(f"获取大连商品交易所期转现统计数据失败 (date={date}): {e}")
            return
        
        if df is None or df.empty:
            logger.warning(f"获取大连商品交易所期转现统计数据为空 (date={date})")
            return
        
        db = get_mongo_db()
        collection = db.get_collection("futures_to_spot_dce")
        
        data = df.to_dict(orient="records")
        count = 0
        for item in data:
            item["update_time"] = datetime.now()
            item["query_date"] = date
            # 唯一键：合约代码 + 期转现发生日期
            key = {"合约代码": item.get("合约代码"), "期转现发生日期": item.get("期转现发生日期")}
            if key["合约代码"] and key["期转现发生日期"]:
                await collection.update_one(key, {"$set": item}, upsert=True)
                count += 1
        
        logger.info(f"大连商品交易所期转现统计数据更新完成，共处理 {count} 条记录 (date={date})")
    except Exception as e:
        logger.error(f"更新大连商品交易所期转现统计数据失败: {e}", exc_info=True)


# 013 futures_to_spot_czce
async def update_futures_to_spot_czce_task(date: str):
    """更新郑州商品交易所期转现统计数据任务
    
    Args:
        date: 交易日期，格式YYYYMMDD（例如：20210112）
    """
    try:
        import akshare as ak
        logger.info(f"开始更新郑州商品交易所期转现统计数据 (date={date})")
        
        if not date:
            logger.error("需要提供date参数")
            return
        
        try:
            df = ak.futures_to_spot_czce(date=date)
        except Exception as e:
            logger.error(f"获取郑州商品交易所期转现统计数据失败 (date={date}): {e}")
            return
        
        if df is None or df.empty:
            logger.warning(f"获取郑州商品交易所期转现统计数据为空 (date={date})")
            return
        
        db = get_mongo_db()
        collection = db.get_collection("futures_to_spot_czce")
        
        data = df.to_dict(orient="records")
        count = 0
        for item in data:
            item["update_time"] = datetime.now()
            item["query_date"] = date
            # 唯一键：date + 合约代码
            key = {"query_date": date, "合约代码": item.get("合约代码")}
            if key["合约代码"]:
                await collection.update_one(key, {"$set": item}, upsert=True)
                count += 1
        
        logger.info(f"郑州商品交易所期转现统计数据更新完成，共处理 {count} 条记录 (date={date})")
    except Exception as e:
        logger.error(f"更新郑州商品交易所期转现统计数据失败: {e}", exc_info=True)


# 014 futures_to_spot_shfe
async def update_futures_to_spot_shfe_task(date: str):
    """更新上海期货交易所期转现数据任务
    
    Args:
        date: 交易月份，格式YYYYMM（例如：202312）
    """
    try:
        import akshare as ak
        logger.info(f"开始更新上海期货交易所期转现数据 (date={date})")
        
        if not date:
            logger.error("需要提供date参数")
            return
        
        try:
            df = ak.futures_to_spot_shfe(date=date)
        except Exception as e:
            logger.error(f"获取上海期货交易所期转现数据失败 (date={date}): {e}")
            return
        
        if df is None or df.empty:
            logger.warning(f"获取上海期货交易所期转现数据为空 (date={date})")
            return
        
        db = get_mongo_db()
        collection = db.get_collection("futures_to_spot_shfe")
        
        data = df.to_dict(orient="records")
        count = 0
        for item in data:
            item["update_time"] = datetime.now()
            item["query_date"] = date
            # 唯一键：日期 + 合约
            key = {"日期": item.get("日期"), "合约": item.get("合约")}
            if key["日期"] and key["合约"]:
                await collection.update_one(key, {"$set": item}, upsert=True)
                count += 1
        
        logger.info(f"上海期货交易所期转现数据更新完成，共处理 {count} 条记录 (date={date})")
    except Exception as e:
        logger.error(f"更新上海期货交易所期转现数据失败: {e}", exc_info=True)


# 022 futures_spot_sys
async def update_futures_spot_sys_task(symbol: str, indicator: str):
    """更新现期图任务"""
    try:
        import akshare as ak
        logger.info(f"开始更新现期图 (symbol={symbol}, indicator={indicator})")
        df = ak.futures_spot_sys(symbol=symbol, contract=indicator)
        if df is None or df.empty:
            logger.warning("获取现期图数据为空")
            return
        data = df.to_dict(orient="records")
        db = get_mongo_db()
        collection = db.get_collection("futures_spot_sys")
        count = 0
        for item in data:
            item["symbol"] = symbol
            item["indicator"] = indicator
            key = {"日期": item.get("日期"), "symbol": symbol, "indicator": indicator}
            if not key["日期"]:
                continue
            await collection.update_one(key, {"$set": item}, upsert=True)
            count += 1
        logger.info(f"现期图更新完成，共处理 {count} 条记录")
    except Exception as e:
        logger.error(f"更新现期图失败: {e}", exc_info=True)


# 023 futures_contract_info_shfe
async def update_futures_contract_info_shfe_task(date: str):
    """更新上海期货交易所合约信息任务"""
    try:
        import akshare as ak
        logger.info(f"开始更新上海期货交易所合约信息 (date={date})")
        df = ak.futures_contract_info_shfe(date=date)
        if df is None or df.empty:
            logger.warning("获取上海期货交易所合约信息为空")
            return
        data = df.to_dict(orient="records")
        db = get_mongo_db()
        collection = db.get_collection("futures_contract_info_shfe")
        count = 0
        for item in data:
            key = {"合约代码": item.get("合约代码"), "交易日": item.get("交易日")}
            if not key["合约代码"]:
                continue
            await collection.update_one(key, {"$set": item}, upsert=True)
            count += 1
        logger.info(f"上海期货交易所合约信息更新完成，共处理 {count} 条记录")
    except Exception as e:
        logger.error(f"更新上海期货交易所合约信息失败: {e}", exc_info=True)


# 024 futures_contract_info_ine
async def update_futures_contract_info_ine_task(date: str):
    """更新上海国际能源交易中心合约信息任务"""
    try:
        import akshare as ak
        logger.info(f"开始更新上海国际能源交易中心合约信息 (date={date})")
        df = ak.futures_contract_info_ine(date=date)
        if df is None or df.empty:
            logger.warning("获取合约信息为空")
            return
        data = df.to_dict(orient="records")
        db = get_mongo_db()
        collection = db.get_collection("futures_contract_info_ine")
        count = 0
        for item in data:
            key = {"合约代码": item.get("合约代码"), "交易日": item.get("交易日")}
            if not key["合约代码"]:
                continue
            await collection.update_one(key, {"$set": item}, upsert=True)
            count += 1
        logger.info(f"合约信息更新完成，共处理 {count} 条记录")
    except Exception as e:
        logger.error(f"更新合约信息失败: {e}", exc_info=True)


# 025 futures_contract_info_dce
async def update_futures_contract_info_dce_task():
    try:
        import akshare as ak
        logger.info("开始更新大连商品交易所合约信息")
        df = ak.futures_contract_info_dce()
        if df is None or df.empty:
            return
        db = get_mongo_db()
        collection = db.get_collection("futures_contract_info_dce")
        count = 0
        for item in df.to_dict(orient="records"):
            key = {"合约代码": item.get("合约代码")}
            if key["合约代码"]:
                await collection.update_one(key, {"$set": item}, upsert=True)
                count += 1
        logger.info(f"更新完成，共{count}条")
    except Exception as e:
        logger.error(f"更新失败: {e}", exc_info=True)


# 026 futures_contract_info_czce
async def update_futures_contract_info_czce_task(date: str):
    try:
        import akshare as ak
        logger.info(f"开始更新郑州商品交易所合约信息 (date={date})")
        df = ak.futures_contract_info_czce(date=date)
        if df is None or df.empty:
            return
        db = get_mongo_db()
        collection = db.get_collection("futures_contract_info_czce")
        count = 0
        for item in df.to_dict(orient="records"):
            key = {"合约代码": item.get("合约代码")}
            if key["合约代码"]:
                await collection.update_one(key, {"$set": item}, upsert=True)
                count += 1
        logger.info(f"更新完成，共{count}条")
    except Exception as e:
        logger.error(f"更新失败: {e}", exc_info=True)


# 027 futures_contract_info_gfex
async def update_futures_contract_info_gfex_task():
    try:
        import akshare as ak
        logger.info("开始更新广州期货交易所合约信息")
        df = ak.futures_contract_info_gfex()
        if df is None or df.empty:
            return
        db = get_mongo_db()
        collection = db.get_collection("futures_contract_info_gfex")
        count = 0
        for item in df.to_dict(orient="records"):
            key = {"合约代码": item.get("合约代码")}
            if key["合约代码"]:
                await collection.update_one(key, {"$set": item}, upsert=True)
                count += 1
        logger.info(f"更新完成，共{count}条")
    except Exception as e:
        logger.error(f"更新失败: {e}", exc_info=True)


# 028 futures_contract_info_cffex
async def update_futures_contract_info_cffex_task(date: str):
    try:
        import akshare as ak
        logger.info(f"开始更新中国金融期货交易所合约信息 (date={date})")
        df = ak.futures_contract_info_cffex(date=date)
        if df is None or df.empty:
            return
        db = get_mongo_db()
        collection = db.get_collection("futures_contract_info_cffex")
        count = 0
        for item in df.to_dict(orient="records"):
            key = {"合约代码": item.get("合约代码")}
            if key["合约代码"]:
                await collection.update_one(key, {"$set": item}, upsert=True)
                count += 1
        logger.info(f"更新完成，共{count}条")
    except Exception as e:
        logger.error(f"更新失败: {e}", exc_info=True)

"""
通用实现模式：

async def update_<collection_name>_task(params):
    try:
        import akshare as ak
        logger.info(f"开始更新...")
        
        # 1. 调用akshare API获取数据
        df = ak.<api_function_name>(params)
        
        if df is None or df.empty:
            logger.warning("获取数据为空")
            return
        
        # 2. 转换为字典列表
        data = df.to_dict(orient="records")
        
        # 3. 获取MongoDB集合
        db = get_mongo_db()
        collection = db.get_collection("<collection_name>")
        
        # 4. 批量更新
        count = 0
        for item in data:
            # 添加额外字段
            item["extra_field"] = extra_value
            
            # 定义唯一键
            key = {"field1": item.get("field1"), "field2": item.get("field2")}
            
            if not key["field1"]:
                continue
            
            await collection.update_one(key, {"$set": item}, upsert=True)
            count += 1
        
        logger.info(f"更新完成，共处理 {count} 条记录")
    except Exception as e:
        logger.error(f"更新失败: {e}", exc_info=True)
"""

# 029-052 剩余函数stub实现（后续可按需完善）

async def update_futures_zh_spot_task(symbol: str = None, market: str = "CF", adjust: str = "0"):
    """更新内盘实时行情数据任务
    
    Args:
        symbol: 需要订阅的合约代码（可选）
        market: CF-商品期货, FF-金融期货（默认CF）
        adjust: 0-基本数据, 1-包含交易所和最小变动单位（默认0）
    """
    try:
        import akshare as ak
        logger.info(f"开始更新内盘实时行情数据 (market={market}, adjust={adjust})")
        
        # 调用akshare API获取数据
        try:
            df = ak.futures_zh_spot(subscribe_list=symbol, market=market, adjust=adjust)
        except Exception as e:
            logger.error(f"获取内盘实时行情数据失败: {e}")
            return
        
        if df is None or df.empty:
            logger.warning("获取内盘实时行情数据为空")
            return
        
        # 转换为字典列表
        data = df.to_dict(orient="records")
        
        # 获取MongoDB集合
        db = get_mongo_db()
        collection = db.get_collection("futures_zh_spot")
        
        # 批量更新
        count = 0
        for item in data:
            # 添加更新时间和参数
            item["update_time"] = datetime.now()
            item["market"] = market
            
            # 定义唯一键：symbol + time
            key = {
                "symbol": item.get("symbol"),
                "time": item.get("time")
            }
            
            if not key["symbol"] or not key["time"]:
                continue
            
            await collection.update_one(key, {"$set": item}, upsert=True)
            count += 1
        
        logger.info(f"内盘实时行情数据更新完成，共处理 {count} 条记录")
    except Exception as e:
        logger.error(f"更新内盘实时行情数据失败: {e}", exc_info=True)

async def update_futures_zh_realtime_task(symbol: str):
    """更新内盘实时行情数据(品种)任务
    
    Args:
        symbol: 品种名称（必需），如"白糖"、"铜"等
    """
    try:
        import akshare as ak
        logger.info(f"开始更新内盘实时行情数据(品种) (symbol={symbol})")
        
        if not symbol:
            logger.error("更新内盘实时行情数据(品种)需要提供symbol参数")
            return
        
        # 调用akshare API获取数据
        try:
            df = ak.futures_zh_realtime(symbol=symbol)
        except Exception as e:
            logger.error(f"获取内盘实时行情数据(品种)失败 (symbol={symbol}): {e}")
            return
        
        if df is None or df.empty:
            logger.warning(f"获取内盘实时行情数据(品种)为空 (symbol={symbol})")
            return
        
        # 转换为字典列表
        data = df.to_dict(orient="records")
        
        # 获取MongoDB集合
        db = get_mongo_db()
        collection = db.get_collection("futures_zh_realtime")
        
        # 批量更新
        count = 0
        for item in data:
            # 添加更新时间和品种信息
            item["update_time"] = datetime.now()
            item["query_symbol"] = symbol  # 保存查询的品种名称
            
            # 定义唯一键：symbol + tradedate
            key = {
                "symbol": item.get("symbol"),
                "tradedate": item.get("tradedate")
            }
            
            if not key["symbol"] or not key["tradedate"]:
                continue
            
            await collection.update_one(key, {"$set": item}, upsert=True)
            count += 1
        
        logger.info(f"内盘实时行情数据(品种)更新完成，共处理 {count} 条记录 (symbol={symbol})")
    except Exception as e:
        logger.error(f"更新内盘实时行情数据(品种)失败: {e}", exc_info=True)

async def update_futures_zh_minute_sina_task(symbol: str, period: str = "1"):
    """更新内盘分时行情数据任务
    
    Args:
        symbol: 合约代码（必需），如"IF2008"
        period: 分钟周期，可选值: "1", "5", "15", "30", "60"（默认"1"）
    """
    try:
        import akshare as ak
        logger.info(f"开始更新内盘分时行情数据 (symbol={symbol}, period={period})")
        
        if not symbol:
            logger.error("更新内盘分时行情数据需要提供symbol参数")
            return
        
        # 调用akshare API获取数据
        try:
            df = ak.futures_zh_minute_sina(symbol=symbol, period=period)
        except Exception as e:
            logger.error(f"获取内盘分时行情数据失败 (symbol={symbol}, period={period}): {e}")
            return
        
        if df is None or df.empty:
            logger.warning(f"获取内盘分时行情数据为空 (symbol={symbol}, period={period})")
            return
        
        # 转换为字典列表
        data = df.to_dict(orient="records")
        
        # 获取MongoDB集合
        db = get_mongo_db()
        collection = db.get_collection("futures_zh_minute_sina")
        
        # 批量更新
        count = 0
        for item in data:
            # 添加更新时间和查询参数
            item["update_time"] = datetime.now()
            item["query_symbol"] = symbol
            item["query_period"] = period
            
            # 定义唯一键：symbol + period + datetime
            key = {
                "query_symbol": symbol,
                "query_period": period,
                "datetime": item.get("datetime")
            }
            
            if not key["datetime"]:
                continue
            
            await collection.update_one(key, {"$set": item}, upsert=True)
            count += 1
        
        logger.info(f"内盘分时行情数据更新完成，共处理 {count} 条记录 (symbol={symbol}, period={period})")
    except Exception as e:
        logger.error(f"更新内盘分时行情数据失败: {e}", exc_info=True)

async def update_futures_hist_em_task(
    symbol: str,
    period: str = "daily",
    start_date: str = "19900101",
    end_date: str = "20500101"
):
    """更新内盘历史行情数据-东财任务
    
    Args:
        symbol: 合约代码（必需），如"热卷主连"
        period: 周期，可选值: "daily", "weekly", "monthly"（默认"daily"）
        start_date: 开始日期，格式YYYYMMDD（默认"19900101"）
        end_date: 结束日期，格式YYYYMMDD（默认"20500101"）
    """
    try:
        import akshare as ak
        logger.info(f"开始更新内盘历史行情数据-东财 (symbol={symbol}, period={period}, date_range={start_date}-{end_date})")
        
        if not symbol:
            logger.error("更新内盘历史行情数据-东财需要提供symbol参数")
            return
        
        # 调用akshare API获取数据
        try:
            df = ak.futures_hist_em(
                symbol=symbol,
                period=period,
                start_date=start_date,
                end_date=end_date
            )
        except Exception as e:
            logger.error(f"获取内盘历史行情数据-东财失败 (symbol={symbol}): {e}")
            return
        
        if df is None or df.empty:
            logger.warning(f"获取内盘历史行情数据-东财为空 (symbol={symbol})")
            return
        
        # 转换为字典列表
        data = df.to_dict(orient="records")
        
        # 获取MongoDB集合
        db = get_mongo_db()
        collection = db.get_collection("futures_hist_em")
        
        # 批量更新
        count = 0
        for item in data:
            # 添加更新时间和查询参数
            item["update_time"] = datetime.now()
            item["query_symbol"] = symbol
            item["query_period"] = period
            
            # 定义唯一键：symbol + period + 时间
            key = {
                "query_symbol": symbol,
                "query_period": period,
                "时间": item.get("时间")
            }
            
            if not key["时间"]:
                continue
            
            await collection.update_one(key, {"$set": item}, upsert=True)
            count += 1
        
        logger.info(f"内盘历史行情数据-东财更新完成，共处理 {count} 条记录 (symbol={symbol}, period={period})")
    except Exception as e:
        logger.error(f"更新内盘历史行情数据-东财失败: {e}", exc_info=True)

async def update_futures_zh_daily_sina_task(symbol: str):
    """更新内盘历史行情数据-新浪任务
    
    Args:
        symbol: 合约代码（必需），如"RB0"（螺纹钢连续合约）
    """
    try:
        import akshare as ak
        logger.info(f"开始更新内盘历史行情数据-新浪 (symbol={symbol})")
        
        if not symbol:
            logger.error("更新内盘历史行情数据-新浪需要提供symbol参数")
            return
        
        # 调用akshare API获取数据
        try:
            df = ak.futures_zh_daily_sina(symbol=symbol)
        except Exception as e:
            logger.error(f"获取内盘历史行情数据-新浪失败 (symbol={symbol}): {e}")
            return
        
        if df is None or df.empty:
            logger.warning(f"获取内盘历史行情数据-新浪为空 (symbol={symbol})")
            return
        
        # 转换为字典列表
        data = df.to_dict(orient="records")
        
        # 获取MongoDB集合
        db = get_mongo_db()
        collection = db.get_collection("futures_zh_daily_sina")
        
        # 批量更新
        count = 0
        for item in data:
            # 添加更新时间和查询参数
            item["update_time"] = datetime.now()
            item["query_symbol"] = symbol
            
            # 定义唯一键：symbol + date
            key = {
                "query_symbol": symbol,
                "date": item.get("date")
            }
            
            if not key["date"]:
                continue
            
            await collection.update_one(key, {"$set": item}, upsert=True)
            count += 1
        
        logger.info(f"内盘历史行情数据-新浪更新完成，共处理 {count} 条记录 (symbol={symbol})")
    except Exception as e:
        logger.error(f"更新内盘历史行情数据-新浪失败: {e}", exc_info=True)

async def update_get_futures_daily_task(
    start_date: str = "20200701",
    end_date: str = "20200716",
    market: str = "DCE"
):
    """更新内盘历史行情数据-交易所任务
    
    Args:
        start_date: 开始日期，格式YYYYMMDD（默认"20200701"）
        end_date: 结束日期，格式YYYYMMDD（默认"20200716"）
        market: 交易所，可选值: CFFEX/INE/CZCE/DCE/SHFE/GFEX（默认"DCE"）
    """
    try:
        import akshare as ak
        logger.info(f"开始更新内盘历史行情数据-交易所 (market={market}, date_range={start_date}-{end_date})")
        
        # 调用akshare API获取数据
        try:
            df = ak.get_futures_daily(
                start_date=start_date,
                end_date=end_date,
                market=market
            )
        except Exception as e:
            logger.error(f"获取内盘历史行情数据-交易所失败 (market={market}): {e}")
            return
        
        if df is None or df.empty:
            logger.warning(f"获取内盘历史行情数据-交易所为空 (market={market}, date_range={start_date}-{end_date})")
            return
        
        # 转换为字典列表
        data = df.to_dict(orient="records")
        
        # 获取MongoDB集合
        db = get_mongo_db()
        collection = db.get_collection("get_futures_daily")
        
        # 批量更新
        count = 0
        for item in data:
            # 添加更新时间和查询参数
            item["update_time"] = datetime.now()
            item["query_market"] = market
            item["query_start_date"] = start_date
            item["query_end_date"] = end_date
            
            # 定义唯一键：market + symbol + date
            key = {
                "query_market": market,
                "symbol": item.get("symbol"),
                "date": item.get("date")
            }
            
            if not key["symbol"] or not key["date"]:
                continue
            
            await collection.update_one(key, {"$set": item}, upsert=True)
            count += 1
        
        logger.info(f"内盘历史行情数据-交易所更新完成，共处理 {count} 条记录 (market={market}, date_range={start_date}-{end_date})")
    except Exception as e:
        logger.error(f"更新内盘历史行情数据-交易所失败: {e}", exc_info=True)

async def update_futures_hq_subscribe_exchange_symbol_task():
    """更新外盘品种代码表任务
    
    无需参数，获取所有外盘期货品种代码
    """
    try:
        import akshare as ak
        logger.info("开始更新外盘品种代码表")
        
        # 调用akshare API获取数据
        try:
            df = ak.futures_hq_subscribe_exchange_symbol()
        except Exception as e:
            logger.error(f"获取外盘品种代码表失败: {e}")
            return
        
        if df is None or df.empty:
            logger.warning("获取外盘品种代码表为空")
            return
        
        # 转换为字典列表
        data = df.to_dict(orient="records")
        
        # 获取MongoDB集合
        db = get_mongo_db()
        collection = db.get_collection("futures_hq_subscribe_exchange_symbol")
        
        # 批量更新
        count = 0
        for item in data:
            # 添加更新时间
            item["update_time"] = datetime.now()
            
            # 定义唯一键：code（品种代码）
            key = {"code": item.get("code")}
            
            if not key["code"]:
                continue
            
            await collection.update_one(key, {"$set": item}, upsert=True)
            count += 1
        
        logger.info(f"外盘品种代码表更新完成，共处理 {count} 条记录")
    except Exception as e:
        logger.error(f"更新外盘品种代码表失败: {e}", exc_info=True)

async def update_futures_foreign_commodity_realtime_task(symbol: str):
    """更新外盘实时行情数据任务
    
    Args:
        symbol: 品种代码（必需），如"黄金"、"原油"
    """
    try:
        import akshare as ak
        logger.info(f"开始更新外盘实时行情数据 (symbol={symbol})")
        
        if not symbol:
            logger.error("更新外盘实时行情数据需要提供symbol参数")
            return
        
        try:
            df = ak.futures_foreign_commodity_realtime(symbol=symbol)
        except Exception as e:
            logger.error(f"获取外盘实时行情数据失败 (symbol={symbol}): {e}")
            return
        
        if df is None or df.empty:
            logger.warning(f"获取外盘实时行情数据为空 (symbol={symbol})")
            return
        
        data = df.to_dict(orient="records")
        db = get_mongo_db()
        collection = db.get_collection("futures_foreign_commodity_realtime")
        
        count = 0
        for item in data:
            item["update_time"] = datetime.now()
            item["query_symbol"] = symbol
            key = {"名称": item.get("名称")}
            if key["名称"]:
                await collection.update_one(key, {"$set": item}, upsert=True)
                count += 1
        
        logger.info(f"外盘实时行情数据更新完成，共处理 {count} 条记录 (symbol={symbol})")
    except Exception as e:
        logger.error(f"更新外盘实时行情数据失败: {e}", exc_info=True)

async def update_futures_global_spot_em_task():
    """更新外盘实时行情数据-东财任务
    
    无需参数，获取所有外盘期货实时数据
    """
    try:
        import akshare as ak
        logger.info("开始更新外盘实时行情数据-东财")
        
        try:
            df = ak.futures_global_spot_em()
        except Exception as e:
            logger.error(f"获取外盘实时行情数据-东财失败: {e}")
            return
        
        if df is None or df.empty:
            logger.warning("获取外盘实时行情数据-东财为空")
            return
        
        data = df.to_dict(orient="records")
        db = get_mongo_db()
        collection = db.get_collection("futures_global_spot_em")
        
        count = 0
        for item in data:
            item["update_time"] = datetime.now()
            key = {"代码": item.get("代码")}
            if key["代码"]:
                await collection.update_one(key, {"$set": item}, upsert=True)
                count += 1
        
        logger.info(f"外盘实时行情数据-东财更新完成，共处理 {count} 条记录")
    except Exception as e:
        logger.error(f"更新外盘实时行情数据-东财失败: {e}", exc_info=True)

async def update_futures_global_hist_em_task(symbol: str, start_date: str = "19700101", end_date: str = "20500101"):
    """更新外盘历史行情数据-东财任务
    
    Args:
        symbol: 合约代码（必需）
        start_date: 开始日期（默认"19700101"）
        end_date: 结束日期（默认"20500101")
    """
    try:
        import akshare as ak
        logger.info(f"开始更新外盘历史行情数据-东财 (symbol={symbol})")
        
        if not symbol:
            logger.error("更新外盘历史行情数据-东财需要提供symbol参数")
            return
        
        try:
            df = ak.futures_global_hist_em(symbol=symbol, start_date=start_date, end_date=end_date)
        except Exception as e:
            logger.error(f"获取外盘历史行情数据-东财失败 (symbol={symbol}): {e}")
            return
        
        if df is None or df.empty:
            logger.warning(f"获取外盘历史行情数据-东财为空 (symbol={symbol})")
            return
        
        data = df.to_dict(orient="records")
        db = get_mongo_db()
        collection = db.get_collection("futures_global_hist_em")
        
        count = 0
        for item in data:
            item["update_time"] = datetime.now()
            item["query_symbol"] = symbol
            key = {"query_symbol": symbol, "日期": item.get("日期")}
            if key["日期"]:
                await collection.update_one(key, {"$set": item}, upsert=True)
                count += 1
        
        logger.info(f"外盘历史行情数据-东财更新完成，共处理 {count} 条记录 (symbol={symbol})")
    except Exception as e:
        logger.error(f"更新外盘历史行情数据-东财失败: {e}", exc_info=True)

async def update_futures_foreign_hist_task(symbol: str):
    """更新外盘历史行情数据-新浪任务
    
    Args:
        symbol: 合约代码（必需）
    """
    try:
        import akshare as ak
        logger.info(f"开始更新外盘历史行情数据-新浪 (symbol={symbol})")
        
        if not symbol:
            logger.error("更新外盘历史行情数据-新浪需要提供symbol参数")
            return
        
        try:
            df = ak.futures_foreign_hist(symbol=symbol)
        except Exception as e:
            logger.error(f"获取外盘历史行情数据-新浪失败 (symbol={symbol}): {e}")
            return
        
        if df is None or df.empty:
            logger.warning(f"获取外盘历史行情数据-新浪为空 (symbol={symbol})")
            return
        
        data = df.to_dict(orient="records")
        db = get_mongo_db()
        collection = db.get_collection("futures_foreign_hist")
        
        count = 0
        for item in data:
            item["update_time"] = datetime.now()
            item["query_symbol"] = symbol
            key = {"query_symbol": symbol, "date": item.get("date")}
            if key["date"]:
                await collection.update_one(key, {"$set": item}, upsert=True)
                count += 1
        
        logger.info(f"外盘历史行情数据-新浪更新完成，共处理 {count} 条记录 (symbol={symbol})")
    except Exception as e:
        logger.error(f"更新外盘历史行情数据-新浪失败: {e}", exc_info=True)

async def update_futures_foreign_detail_task(symbol: str):
    """更新外盘合约详情任务
    
    Args:
        symbol: 合约代码（必需）
    """
    try:
        import akshare as ak
        logger.info(f"开始更新外盘合约详情 (symbol={symbol})")
        
        if not symbol:
            logger.error("更新外盘合约详情需要提供symbol参数")
            return
        
        try:
            df = ak.futures_foreign_detail(symbol=symbol)
        except Exception as e:
            logger.error(f"获取外盘合约详情失败 (symbol={symbol}): {e}")
            return
        
        if df is None or df.empty:
            logger.warning(f"获取外盘合约详情为空 (symbol={symbol})")
            return
        
        data = df.to_dict(orient="records")
        db = get_mongo_db()
        collection = db.get_collection("futures_foreign_detail")
        
        count = 0
        for item in data:
            item["update_time"] = datetime.now()
            item["query_symbol"] = symbol
            key = {"query_symbol": symbol, "交易品种": item.get("交易品种")}
            if key["交易品种"]:
                await collection.update_one(key, {"$set": item}, upsert=True)
                count += 1
        
        logger.info(f"外盘合约详情更新完成，共处理 {count} 条记录 (symbol={symbol})")
    except Exception as e:
        logger.error(f"更新外盘合约详情失败: {e}", exc_info=True)

async def update_futures_settlement_price_sgx_task(date: str = None):
    """更新新加坡交易所期货任务
    
    Args:
        date: 日期，格式YYYYMMDD（可选）
    """
    try:
        import akshare as ak
        logger.info(f"开始更新新加坡交易所期货 (date={date})")
        
        try:
            df = ak.futures_settlement_price_sgx(date=date) if date else ak.futures_settlement_price_sgx()
        except Exception as e:
            logger.error(f"获取新加坡交易所期货失败: {e}")
            return
        
        if df is None or df.empty:
            logger.warning("获取新加坡交易所期货为空")
            return
        
        data = df.to_dict(orient="records")
        db = get_mongo_db()
        collection = db.get_collection("futures_settlement_price_sgx")
        
        count = 0
        for item in data:
            item["update_time"] = datetime.now()
            if date:
                item["query_date"] = date
            key = {"合约": item.get("合约")}
            if key["合约"]:
                await collection.update_one(key, {"$set": item}, upsert=True)
                count += 1
        
        logger.info(f"新加坡交易所期货更新完成，共处理 {count} 条记录")
    except Exception as e:
        logger.error(f"更新新加坡交易所期货失败: {e}", exc_info=True)

async def update_futures_main_sina_task(symbol: str):
    """更新期货连续合约任务
    
    Args:
        symbol: 品种代码（必需）
    """
    try:
        import akshare as ak
        logger.info(f"开始更新期货连续合约 (symbol={symbol})")
        
        if not symbol:
            logger.error("更新期货连续合约需要提供symbol参数")
            return
        
        try:
            df = ak.futures_main_sina(symbol=symbol)
        except Exception as e:
            logger.error(f"获取期货连续合约失败 (symbol={symbol}): {e}")
            return
        
        if df is None or df.empty:
            logger.warning(f"获取期货连续合约为空 (symbol={symbol})")
            return
        
        data = df.to_dict(orient="records")
        db = get_mongo_db()
        collection = db.get_collection("futures_main_sina")
        
        count = 0
        for item in data:
            item["update_time"] = datetime.now()
            item["query_symbol"] = symbol
            key = {"query_symbol": symbol, "date": item.get("date")}
            if key["date"]:
                await collection.update_one(key, {"$set": item}, upsert=True)
                count += 1
        
        logger.info(f"期货连续合约更新完成，共处理 {count} 条记录 (symbol={symbol})")
    except Exception as e:
        logger.error(f"更新期货连续合约失败: {e}", exc_info=True)

async def update_futures_contract_detail_task(symbol: str):
    """更新期货合约详情-新浪任务
    
    Args:
        symbol: 合约代码（必需）
    """
    try:
        import akshare as ak
        logger.info(f"开始更新期货合约详情-新浪 (symbol={symbol})")
        
        if not symbol:
            logger.error("更新期货合约详情-新浪需要提供symbol参数")
            return
        
        try:
            df = ak.futures_contract_detail(symbol=symbol)
        except Exception as e:
            logger.error(f"获取期货合约详情-新浪失败 (symbol={symbol}): {e}")
            return
        
        if df is None or df.empty:
            logger.warning(f"获取期货合约详情-新浪为空 (symbol={symbol})")
            return
        
        data = df.to_dict(orient="records")
        db = get_mongo_db()
        collection = db.get_collection("futures_contract_detail")
        
        count = 0
        for item in data:
            item["update_time"] = datetime.now()
            item["query_symbol"] = symbol
            key = {"query_symbol": symbol}
            await collection.update_one(key, {"$set": item}, upsert=True)
            count += 1
        
        logger.info(f"期货合约详情-新浪更新完成，共处理 {count} 条记录 (symbol={symbol})")
    except Exception as e:
        logger.error(f"更新期货合约详情-新浪失败: {e}", exc_info=True)

async def update_futures_contract_detail_em_task(symbol: str):
    """更新期货合约详情-东财任务
    
    Args:
        symbol: 合约代码（必需）
    """
    try:
        import akshare as ak
        logger.info(f"开始更新期货合约详情-东财 (symbol={symbol})")
        
        if not symbol:
            logger.error("更新期货合约详情-东财需要提供symbol参数")
            return
        
        try:
            df = ak.futures_contract_detail_em(symbol=symbol)
        except Exception as e:
            logger.error(f"获取期货合约详情-东财失败 (symbol={symbol}): {e}")
            return
        
        if df is None or df.empty:
            logger.warning(f"获取期货合约详情-东财为空 (symbol={symbol})")
            return
        
        data = df.to_dict(orient="records")
        db = get_mongo_db()
        collection = db.get_collection("futures_contract_detail_em")
        
        count = 0
        for item in data:
            item["update_time"] = datetime.now()
            item["query_symbol"] = symbol
            key = {"query_symbol": symbol}
            await collection.update_one(key, {"$set": item}, upsert=True)
            count += 1
        
        logger.info(f"期货合约详情-东财更新完成，共处理 {count} 条记录 (symbol={symbol})")
    except Exception as e:
        logger.error(f"更新期货合约详情-东财失败: {e}", exc_info=True)

async def update_futures_index_ccidx_task(symbol: str):
    """更新中证商品指数任务
    
    Args:
        symbol: 指数名称（必需）
    """
    try:
        import akshare as ak
        logger.info(f"开始更新中证商品指数 (symbol={symbol})")
        
        if not symbol:
            logger.error("更新中证商品指数需要提供symbol参数")
            return
        
        try:
            df = ak.futures_index_ccidx(symbol=symbol)
        except Exception as e:
            logger.error(f"获取中证商品指数失败 (symbol={symbol}): {e}")
            return
        
        if df is None or df.empty:
            logger.warning(f"获取中证商品指数为空 (symbol={symbol})")
            return
        
        data = df.to_dict(orient="records")
        db = get_mongo_db()
        collection = db.get_collection("futures_index_ccidx")
        
        count = 0
        for item in data:
            item["update_time"] = datetime.now()
            item["query_symbol"] = symbol
            key = {"query_symbol": symbol, "date": item.get("date")}
            if key["date"]:
                await collection.update_one(key, {"$set": item}, upsert=True)
                count += 1
        
        logger.info(f"中证商品指数更新完成，共处理 {count} 条记录 (symbol={symbol})")
    except Exception as e:
        logger.error(f"更新中证商品指数失败: {e}", exc_info=True)

async def update_futures_spot_stock_task(symbol: str):
    """更新现货与股票任务
    
    Args:
        symbol: 品种名称（必需）
    """
    try:
        import akshare as ak
        logger.info(f"开始更新现货与股票 (symbol={symbol})")
        
        if not symbol:
            logger.error("更新现货与股票需要提供symbol参数")
            return
        
        try:
            df = ak.futures_spot_stock(symbol=symbol)
        except Exception as e:
            logger.error(f"获取现货与股票失败 (symbol={symbol}): {e}")
            return
        
        if df is None or df.empty:
            logger.warning(f"获取现货与股票为空 (symbol={symbol})")
            return
        
        data = df.to_dict(orient="records")
        db = get_mongo_db()
        collection = db.get_collection("futures_spot_stock")
        
        count = 0
        for item in data:
            item["update_time"] = datetime.now()
            item["query_symbol"] = symbol
            key = {"query_symbol": symbol, "date": item.get("date")}
            if key["date"]:
                await collection.update_one(key, {"$set": item}, upsert=True)
                count += 1
        
        logger.info(f"现货与股票更新完成，共处理 {count} 条记录 (symbol={symbol})")
    except Exception as e:
        logger.error(f"更新现货与股票失败: {e}", exc_info=True)

async def update_futures_comex_inventory_task(symbol: str):
    """更新COMEX库存数据任务
    
    Args:
        symbol: 品种代码（必需）
    """
    try:
        import akshare as ak
        logger.info(f"开始更新COMEX库存数据 (symbol={symbol})")
        
        if not symbol:
            logger.error("更新COMEX库存数据需要提供symbol参数")
            return
        
        try:
            df = ak.futures_comex_inventory(symbol=symbol)
        except Exception as e:
            logger.error(f"获取COMEX库存数据失败 (symbol={symbol}): {e}")
            return
        
        if df is None or df.empty:
            logger.warning(f"获取COMEX库存数据为空 (symbol={symbol})")
            return
        
        data = df.to_dict(orient="records")
        db = get_mongo_db()
        collection = db.get_collection("futures_comex_inventory")
        
        count = 0
        for item in data:
            item["update_time"] = datetime.now()
            item["query_symbol"] = symbol
            key = {"query_symbol": symbol, "date": item.get("date")}
            if key["date"]:
                await collection.update_one(key, {"$set": item}, upsert=True)
                count += 1
        
        logger.info(f"COMEX库存数据更新完成，共处理 {count} 条记录 (symbol={symbol})")
    except Exception as e:
        logger.error(f"更新COMEX库存数据失败: {e}", exc_info=True)

async def update_futures_hog_core_task(symbol: str):
    """更新生猪核心数据任务
    
    Args:
        symbol: 区域代码（必需）
    """
    try:
        import akshare as ak
        logger.info(f"开始更新生猪核心数据 (symbol={symbol})")
        
        if not symbol:
            logger.error("更新生猪核心数据需要提供symbol参数")
            return
        
        try:
            df = ak.futures_hog_core(symbol=symbol)
        except Exception as e:
            logger.error(f"获取生猪核心数据失败 (symbol={symbol}): {e}")
            return
        
        if df is None or df.empty:
            logger.warning(f"获取生猪核心数据为空 (symbol={symbol})")
            return
        
        data = df.to_dict(orient="records")
        db = get_mongo_db()
        collection = db.get_collection("futures_hog_core")
        
        count = 0
        for item in data:
            item["update_time"] = datetime.now()
            item["query_symbol"] = symbol
            key = {"query_symbol": symbol, "日期": item.get("日期")}
            if key["日期"]:
                await collection.update_one(key, {"$set": item}, upsert=True)
                count += 1
        
        logger.info(f"生猪核心数据更新完成，共处理 {count} 条记录 (symbol={symbol})")
    except Exception as e:
        logger.error(f"更新生猪核心数据失败: {e}", exc_info=True)

async def update_futures_hog_cost_task(symbol: str):
    """更新生猪成本数据任务
    
    Args:
        symbol: 区域代码（必需）
    """
    try:
        import akshare as ak
        logger.info(f"开始更新生猪成本数据 (symbol={symbol})")
        
        if not symbol:
            logger.error("更新生猪成本数据需要提供symbol参数")
            return
        
        try:
            df = ak.futures_hog_cost(symbol=symbol)
        except Exception as e:
            logger.error(f"获取生猪成本数据失败 (symbol={symbol}): {e}")
            return
        
        if df is None or df.empty:
            logger.warning(f"获取生猪成本数据为空 (symbol={symbol})")
            return
        
        data = df.to_dict(orient="records")
        db = get_mongo_db()
        collection = db.get_collection("futures_hog_cost")
        
        count = 0
        for item in data:
            item["update_time"] = datetime.now()
            item["query_symbol"] = symbol
            key = {"query_symbol": symbol, "日期": item.get("日期")}
            if key["日期"]:
                await collection.update_one(key, {"$set": item}, upsert=True)
                count += 1
        
        logger.info(f"生猪成本数据更新完成，共处理 {count} 条记录 (symbol={symbol})")
    except Exception as e:
        logger.error(f"更新生猪成本数据失败: {e}", exc_info=True)

async def update_futures_hog_supply_task(symbol: str):
    """更新生猪供应数据任务
    
    Args:
        symbol: 区域代码（必需）
    """
    try:
        import akshare as ak
        logger.info(f"开始更新生猪供应数据 (symbol={symbol})")
        
        if not symbol:
            logger.error("更新生猪供应数据需要提供symbol参数")
            return
        
        try:
            df = ak.futures_hog_supply(symbol=symbol)
        except Exception as e:
            logger.error(f"获取生猪供应数据失败 (symbol={symbol}): {e}")
            return
        
        if df is None or df.empty:
            logger.warning(f"获取生猪供应数据为空 (symbol={symbol})")
            return
        
        data = df.to_dict(orient="records")
        db = get_mongo_db()
        collection = db.get_collection("futures_hog_supply")
        
        count = 0
        for item in data:
            item["update_time"] = datetime.now()
            item["query_symbol"] = symbol
            key = {"query_symbol": symbol, "日期": item.get("日期")}
            if key["日期"]:
                await collection.update_one(key, {"$set": item}, upsert=True)
                count += 1
        
        logger.info(f"生猪供应数据更新完成，共处理 {count} 条记录 (symbol={symbol})")
    except Exception as e:
        logger.error(f"更新生猪供应数据失败: {e}", exc_info=True)

async def update_futures_hog_info_task():
    """更新生猪信息数据任务
    
    无需参数，获取所有生猪相关信息
    """
    try:
        import akshare as ak
        logger.info("开始更新生猪信息数据")
        
        try:
            df = ak.futures_hog_info()
        except Exception as e:
            logger.error(f"获取生猪信息数据失败: {e}")
            return
        
        if df is None or df.empty:
            logger.warning("获取生猪信息数据为空")
            return
        
        data = df.to_dict(orient="records")
        db = get_mongo_db()
        collection = db.get_collection("futures_hog_info")
        
        count = 0
        for item in data:
            item["update_time"] = datetime.now()
            key = {"类别": item.get("类别")}
            if key["类别"]:
                await collection.update_one(key, {"$set": item}, upsert=True)
                count += 1
        
        logger.info(f"生猪信息数据更新完成，共处理 {count} 条记录")
    except Exception as e:
        logger.error(f"更新生猪信息数据失败: {e}", exc_info=True)


async def update_futures_news_shmet_task(symbol: str):
    """TODO: 实现期货资讯更新"""
    logger.info("期货资讯更新功能待实现")
