# 在update_futures_collection函数中需要添加的elif分支

# 022 futures_spot_sys
elif collection_name == "futures_spot_sys":
    if not symbol:
        return {"success": False, "error": "更新现期图数据需要提供 symbol 参数，格式: symbol:indicator"}
    parts = symbol.split(":")
    if len(parts) != 2:
        return {"success": False, "error": "symbol 参数格式错误，应为: symbol:indicator"}
    sym, indicator = parts
    background_tasks.add_task(update_futures_spot_sys_task, sym, indicator)
    return {"success": True, "data": {"message": f"更新任务已提交 (symbol={sym}, indicator={indicator})", "task_id": str(uuid.uuid4())}}

# 023 futures_contract_info_shfe
elif collection_name == "futures_contract_info_shfe":
    date = symbol if symbol else datetime.now().strftime("%Y%m%d")
    background_tasks.add_task(update_futures_contract_info_shfe_task, date)
    return {"success": True, "data": {"message": f"更新任务已提交 (date={date})", "task_id": str(uuid.uuid4())}}

# 024 futures_contract_info_ine
elif collection_name == "futures_contract_info_ine":
    date = symbol if symbol else datetime.now().strftime("%Y%m%d")
    background_tasks.add_task(update_futures_contract_info_ine_task, date)
    return {"success": True, "data": {"message": f"更新任务已提交 (date={date})", "task_id": str(uuid.uuid4())}}

# 025 futures_contract_info_dce
elif collection_name == "futures_contract_info_dce":
    background_tasks.add_task(update_futures_contract_info_dce_task)
    return {"success": True, "data": {"message": "更新任务已提交", "task_id": str(uuid.uuid4())}}

# 026 futures_contract_info_czce
elif collection_name == "futures_contract_info_czce":
    date = symbol if symbol else datetime.now().strftime("%Y%m%d")
    background_tasks.add_task(update_futures_contract_info_czce_task, date)
    return {"success": True, "data": {"message": f"更新任务已提交 (date={date})", "task_id": str(uuid.uuid4())}}

# 027 futures_contract_info_gfex
elif collection_name == "futures_contract_info_gfex":
    background_tasks.add_task(update_futures_contract_info_gfex_task)
    return {"success": True, "data": {"message": "更新任务已提交", "task_id": str(uuid.uuid4())}}

# 028 futures_contract_info_cffex
elif collection_name == "futures_contract_info_cffex":
    date = symbol if symbol else datetime.now().strftime("%Y%m%d")
    background_tasks.add_task(update_futures_contract_info_cffex_task, date)
    return {"success": True, "data": {"message": f"更新任务已提交 (date={date})", "task_id": str(uuid.uuid4())}}

# 029 futures_zh_spot
elif collection_name == "futures_zh_spot":
    background_tasks.add_task(update_futures_zh_spot_task, symbol)
    return {"success": True, "data": {"message": "更新任务已提交", "task_id": str(uuid.uuid4())}}

# 030 futures_zh_realtime
elif collection_name == "futures_zh_realtime":
    if not symbol:
        return {"success": False, "error": "更新实时行情数据需要提供 symbol 参数"}
    background_tasks.add_task(update_futures_zh_realtime_task, symbol)
    return {"success": True, "data": {"message": f"更新任务已提交 (symbol={symbol})", "task_id": str(uuid.uuid4())}}

# 031 futures_zh_minute_sina
elif collection_name == "futures_zh_minute_sina":
    if not symbol:
        return {"success": False, "error": "更新分时行情数据需要提供 symbol 参数，格式: symbol:period"}
    parts = symbol.split(":")
    if len(parts) != 2:
        return {"success": False, "error": "symbol 参数格式错误，应为: symbol:period"}
    sym, period = parts
    background_tasks.add_task(update_futures_zh_minute_sina_task, sym, period)
    return {"success": True, "data": {"message": f"更新任务已提交 (symbol={sym}, period={period})", "task_id": str(uuid.uuid4())}}

# 032 futures_hist_em
elif collection_name == "futures_hist_em":
    if not symbol:
        return {"success": False, "error": "更新历史行情数据需要提供 symbol 参数"}
    background_tasks.add_task(update_futures_hist_em_task, symbol)
    return {"success": True, "data": {"message": f"更新任务已提交 (symbol={symbol})", "task_id": str(uuid.uuid4())}}

# 033 futures_zh_daily_sina
elif collection_name == "futures_zh_daily_sina":
    if not symbol:
        return {"success": False, "error": "更新日频数据需要提供 symbol 参数"}
    background_tasks.add_task(update_futures_zh_daily_sina_task, symbol)
    return {"success": True, "data": {"message": f"更新任务已提交 (symbol={symbol})", "task_id": str(uuid.uuid4())}}

# 034 get_futures_daily
elif collection_name == "get_futures_daily":
    background_tasks.add_task(update_get_futures_daily_task, symbol)
    return {"success": True, "data": {"message": "更新任务已提交", "task_id": str(uuid.uuid4())}}

# 035 futures_hq_subscribe_exchange_symbol
elif collection_name == "futures_hq_subscribe_exchange_symbol":
    background_tasks.add_task(update_futures_hq_subscribe_exchange_symbol_task)
    return {"success": True, "data": {"message": "更新任务已提交", "task_id": str(uuid.uuid4())}}

# 036 futures_foreign_commodity_realtime
elif collection_name == "futures_foreign_commodity_realtime":
    if not symbol:
        return {"success": False, "error": "更新外盘实时行情需要提供 symbol 参数"}
    background_tasks.add_task(update_futures_foreign_commodity_realtime_task, symbol)
    return {"success": True, "data": {"message": f"更新任务已提交 (symbol={symbol})", "task_id": str(uuid.uuid4())}}

# 037 futures_global_spot_em
elif collection_name == "futures_global_spot_em":
    background_tasks.add_task(update_futures_global_spot_em_task)
    return {"success": True, "data": {"message": "更新任务已提交", "task_id": str(uuid.uuid4())}}

# 038 futures_global_hist_em
elif collection_name == "futures_global_hist_em":
    if not symbol:
        return {"success": False, "error": "更新外盘历史行情需要提供 symbol 参数"}
    background_tasks.add_task(update_futures_global_hist_em_task, symbol)
    return {"success": True, "data": {"message": f"更新任务已提交 (symbol={symbol})", "task_id": str(uuid.uuid4())}}

# 039 futures_foreign_hist
elif collection_name == "futures_foreign_hist":
    if not symbol:
        return {"success": False, "error": "更新外盘历史行情需要提供 symbol 参数"}
    background_tasks.add_task(update_futures_foreign_hist_task, symbol)
    return {"success": True, "data": {"message": f"更新任务已提交 (symbol={symbol})", "task_id": str(uuid.uuid4())}}

# 040 futures_foreign_detail
elif collection_name == "futures_foreign_detail":
    if not symbol:
        return {"success": False, "error": "更新外盘合约详情需要提供 symbol 参数"}
    background_tasks.add_task(update_futures_foreign_detail_task, symbol)
    return {"success": True, "data": {"message": f"更新任务已提交 (symbol={symbol})", "task_id": str(uuid.uuid4())}}

# 041 futures_settlement_price_sgx
elif collection_name == "futures_settlement_price_sgx":
    date = symbol if symbol else datetime.now().strftime("%Y%m%d")
    background_tasks.add_task(update_futures_settlement_price_sgx_task, date)
    return {"success": True, "data": {"message": f"更新任务已提交 (date={date})", "task_id": str(uuid.uuid4())}}

# 042 futures_main_sina
elif collection_name == "futures_main_sina":
    if not symbol:
        return {"success": False, "error": "更新连续合约需要提供 symbol 参数"}
    background_tasks.add_task(update_futures_main_sina_task, symbol)
    return {"success": True, "data": {"message": f"更新任务已提交 (symbol={symbol})", "task_id": str(uuid.uuid4())}}

# 043 futures_contract_detail
elif collection_name == "futures_contract_detail":
    if not symbol:
        return {"success": False, "error": "更新合约详情需要提供 symbol 参数"}
    background_tasks.add_task(update_futures_contract_detail_task, symbol)
    return {"success": True, "data": {"message": f"更新任务已提交 (symbol={symbol})", "task_id": str(uuid.uuid4())}}

# 044 futures_contract_detail_em
elif collection_name == "futures_contract_detail_em":
    if not symbol:
        return {"success": False, "error": "更新合约详情需要提供 symbol 参数"}
    background_tasks.add_task(update_futures_contract_detail_em_task, symbol)
    return {"success": True, "data": {"message": f"更新任务已提交 (symbol={symbol})", "task_id": str(uuid.uuid4())}}

# 045 futures_index_ccidx
elif collection_name == "futures_index_ccidx":
    if not symbol:
        symbol = "中证商品期货指数"
    background_tasks.add_task(update_futures_index_ccidx_task, symbol)
    return {"success": True, "data": {"message": f"更新任务已提交 (symbol={symbol})", "task_id": str(uuid.uuid4())}}

# 046 futures_spot_stock
elif collection_name == "futures_spot_stock":
    if not symbol:
        return {"success": False, "error": "更新现货与股票数据需要提供 symbol 参数"}
    background_tasks.add_task(update_futures_spot_stock_task, symbol)
    return {"success": True, "data": {"message": f"更新任务已提交 (symbol={symbol})", "task_id": str(uuid.uuid4())}}

# 047 futures_comex_inventory
elif collection_name == "futures_comex_inventory":
    if not symbol:
        return {"success": False, "error": "更新COMEX库存数据需要提供 symbol 参数"}
    background_tasks.add_task(update_futures_comex_inventory_task, symbol)
    return {"success": True, "data": {"message": f"更新任务已提交 (symbol={symbol})", "task_id": str(uuid.uuid4())}}

# 048 futures_hog_core
elif collection_name == "futures_hog_core":
    if not symbol:
        return {"success": False, "error": "更新核心数据需要提供 symbol 参数"}
    background_tasks.add_task(update_futures_hog_core_task, symbol)
    return {"success": True, "data": {"message": f"更新任务已提交 (symbol={symbol})", "task_id": str(uuid.uuid4())}}

# 049 futures_hog_cost
elif collection_name == "futures_hog_cost":
    if not symbol:
        return {"success": False, "error": "更新成本维度数据需要提供 symbol 参数"}
    background_tasks.add_task(update_futures_hog_cost_task, symbol)
    return {"success": True, "data": {"message": f"更新任务已提交 (symbol={symbol})", "task_id": str(uuid.uuid4())}}

# 050 futures_hog_supply
elif collection_name == "futures_hog_supply":
    if not symbol:
        return {"success": False, "error": "更新供应维度数据需要提供 symbol 参数"}
    background_tasks.add_task(update_futures_hog_supply_task, symbol)
    return {"success": True, "data": {"message": f"更新任务已提交 (symbol={symbol})", "task_id": str(uuid.uuid4())}}

# 051 index_hog_spot_price
elif collection_name == "index_hog_spot_price":
    background_tasks.add_task(update_index_hog_spot_price_task)
    return {"success": True, "data": {"message": "更新任务已提交", "task_id": str(uuid.uuid4())}}

# 052 futures_news_shmet
elif collection_name == "futures_news_shmet":
    if not symbol:
        symbol = "全部"
    background_tasks.add_task(update_futures_news_shmet_task, symbol)
    return {"success": True, "data": {"message": f"更新任务已提交 (symbol={symbol})", "task_id": str(uuid.uuid4())}}
