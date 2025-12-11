"""库存数据-99期货网数据提供者"""
from typing import List

from app.services.data_sources.base_provider import BaseProvider


class FuturesInventory99Provider(BaseProvider):
    """库存数据-99期货网数据提供者"""
    
    collection_name = "futures_inventory_99"
    display_name = "库存数据-99期货网"
    akshare_func = "futures_inventory_99"
    unique_keys = ["品种", "日期"]
    
    collection_description = "99期货网期货库存数据"
    collection_route = "/futures/collections/futures_inventory_99"
    collection_order = 4
    
    param_mapping = {"symbol": "symbol"}
    required_params = ["symbol"]
    add_param_columns = {"symbol": "品种"}

    SYMBOL_LIST: List[str] = [
        "20号胶",
        "PTA",
        "丁二烯橡胶",
        "不锈钢",
        "丙烯",
        "乙二醇",
        "低硫燃料油",
        "动力煤",
        "原木",
        "原油",
        "多晶硅",
        "天然橡胶",
        "对二甲苯",
        "尿素",
        "工业硅",
        "强麦",
        "早籼稻",
        "晚籼稻",
        "普麦",
        "棉纱",
        "棉花",
        "棕榈油",
        "氧化铝",
        "油菜籽",
        "液化石油气",
        "烧碱",
        "热轧卷板",
        "焦炭",
        "焦煤",
        "燃料油",
        "玉米",
        "玉米淀粉",
        "玻璃",
        "瓶片",
        "生猪",
        "甲醇",
        "白糖",
        "白银",
        "短纤",
        "石油沥青",
        "硅铁",
        "碳酸锂",
        "粳稻",
        "粳米",
        "红枣",
        "纤维板",
        "纯碱",
        "纯苯",
        "纸浆",
        "线材",
        "聚丙烯",
        "聚丙烯月均价",
        "聚乙烯",
        "聚乙烯月均价",
        "聚氯乙烯",
        "聚氯乙烯月均价",
        "胶合板",
        "胶版印刷纸",
        "花生",
        "苯乙烯",
        "苹果",
        "菜籽油",
        "菜籽粕",
        "螺纹钢",
        "豆一",
        "豆二",
        "豆油",
        "豆粕",
        "钯",
        "铁矿石",
        "铂",
        "铅",
        "铜",
        "铜(BC)",
        "铝",
        "铸造铝合金",
        "锌",
        "锡",
        "锰硅",
        "镍",
        "鸡蛋",
        "黄金",
    ]

    field_info = [
        {"name": "品种", "type": "string", "description": "品种名称"},
        {"name": "日期", "type": "string", "description": "日期"},
        {"name": "收盘价", "type": "float", "description": "收盘价"},
        {"name": "库存", "type": "float", "description": "库存量"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
