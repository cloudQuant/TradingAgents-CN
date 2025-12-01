#!/usr/bin/env python3
"""
获取全部ETF基金累计分红数据脚本

功能：
1. 从 fund_spot_sina 集合获取基金代码列表（如果数据库可用）
2. 如果集合为空，从 fund_etf_category_sina 接口获取三种类型的基金代码
3. 对每个基金代码调用 fund_etf_dividend_sina 获取累计分红数据
4. 保存到本地CSV文件：data/fund_etf_dividend_sina.csv
"""

import asyncio
import logging
import sys
from pathlib import Path
from typing import List, Set
from datetime import datetime

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import akshare as ak
import pandas as pd

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def get_codes_from_db(db, collection_name: str, field_name: str) -> List[str]:
    """从数据库集合获取代码列表"""
    try:
        collection = db[collection_name]
        count = await collection.count_documents({})
        logger.info(f"集合 {collection_name} 中有 {count} 条记录")
        
        if count == 0:
            return []
        
        codes = []
        cursor = collection.find({}, {field_name: 1})
        async for doc in cursor:
            code = doc.get(field_name)
            if code:
                codes.append(code)
        
        # 去重
        unique_codes = list(set(codes))
        logger.info(f"从 {collection_name} 获取到 {len(unique_codes)} 个唯一代码")
        return unique_codes
    except Exception as e:
        logger.error(f"从数据库获取代码失败: {e}", exc_info=True)
        return []


def get_codes_from_api() -> List[str]:
    """从 fund_etf_category_sina 接口获取所有基金代码"""
    codes: Set[str] = set()
    supported_types = ("封闭式基金", "ETF基金", "LOF基金")
    
    logger.info("从 fund_etf_category_sina 接口获取基金代码...")
    
    for fund_type in supported_types:
        try:
            logger.info(f"正在获取 {fund_type} 的代码列表...")
            df = ak.fund_etf_category_sina(symbol=fund_type)
            
            if df is not None and not df.empty:
                if "代码" in df.columns:
                    type_codes = df["代码"].dropna().unique().tolist()
                    codes.update(type_codes)
                    logger.info(f"{fund_type}: 获取到 {len(type_codes)} 个代码")
                else:
                    logger.warning(f"{fund_type}: 返回数据中没有'代码'字段，列名: {df.columns.tolist()}")
            else:
                logger.warning(f"{fund_type}: 返回空数据")
        except Exception as e:
            logger.error(f"获取 {fund_type} 代码失败: {e}", exc_info=True)
    
    unique_codes = list(codes)
    logger.info(f"从接口共获取到 {len(unique_codes)} 个唯一代码")
    return unique_codes


async def fetch_dividend_data(code: str) -> pd.DataFrame:
    """获取单个基金的累计分红数据"""
    try:
        df = ak.fund_etf_dividend_sina(symbol=code)
        
        if df is None or df.empty:
            logger.debug(f"代码 {code}: 无分红数据")
            return pd.DataFrame()
        
        # 确保有代码字段
        if "代码" not in df.columns:
            df["代码"] = code
        
        logger.debug(f"代码 {code}: 获取到 {len(df)} 条分红记录")
        return df
    except Exception as e:
        logger.warning(f"代码 {code} 获取分红数据失败: {e}")
        return pd.DataFrame()


def save_dividend_data_to_csv(all_data: List[pd.DataFrame], output_file: str):
    """将所有分红数据合并并保存到CSV文件"""
    if not all_data:
        logger.warning("没有数据需要保存")
        return
    
    try:
        # 合并所有数据
        combined_df = pd.concat(all_data, ignore_index=True)
        
        # 确保字段顺序：代码、日期、累计分红
        if "代码" in combined_df.columns and "日期" in combined_df.columns:
            # 按代码和日期排序
            combined_df = combined_df.sort_values(by=["代码", "日期"])
            # 重新排列列顺序
            columns_order = ["代码", "日期", "累计分红"]
            other_columns = [col for col in combined_df.columns if col not in columns_order]
            combined_df = combined_df[columns_order + other_columns]
        
        # 保存到CSV文件
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        combined_df.to_csv(output_path, index=False, encoding='utf-8-sig')
        
        logger.info(f"数据已保存到: {output_path}")
        logger.info(f"总记录数: {len(combined_df)}")
        logger.info(f"唯一基金代码数: {combined_df['代码'].nunique() if '代码' in combined_df.columns else 'N/A'}")
        
    except Exception as e:
        logger.error(f"保存CSV文件失败: {e}", exc_info=True)
        raise


async def main():
    """主函数"""
    logger.info("=" * 60)
    logger.info("开始获取全部ETF基金累计分红数据")
    logger.info("=" * 60)
    
    # 1. 尝试从数据库获取代码（如果数据库可用）
    codes = []
    try:
        from motor.motor_asyncio import AsyncIOMotorClient
        from app.core.config import settings
        
        mongo_client = AsyncIOMotorClient(settings.MONGO_URI)
        db = mongo_client[settings.MONGO_DB]
        logger.info(f"已连接到数据库: {settings.MONGO_DB}")
        
        # 尝试从 fund_spot_sina 集合获取代码
        codes = await get_codes_from_db(db, "fund_spot_sina", "代码")
        mongo_client.close()
    except Exception as e:
        logger.warning(f"无法连接数据库或获取代码: {e}")
        logger.info("将从接口获取代码...")
    
    # 2. 如果集合为空，从接口获取
    if not codes:
        logger.info("从 fund_etf_category_sina 接口获取代码...")
        codes = get_codes_from_api()
        
        if not codes:
            logger.error("无法获取基金代码，退出")
            return
    
    logger.info(f"共需要处理 {len(codes)} 个基金代码")
    
    # 3. 批量获取分红数据
    all_dataframes: List[pd.DataFrame] = []
    total_failed = 0
    success_codes = []
    failed_codes = []
    
    logger.info("开始批量获取分红数据...")
    
    for idx, code in enumerate(codes, 1):
        logger.info(f"[{idx}/{len(codes)}] 正在处理代码: {code}")
        
        try:
            # 获取分红数据
            df = await fetch_dividend_data(code)
            
            if df is not None and not df.empty:
                # 确保代码字段存在
                if "代码" not in df.columns:
                    df["代码"] = code
                
                all_dataframes.append(df)
                success_codes.append(code)
                logger.info(f"代码 {code}: 获取到 {len(df)} 条分红记录")
            else:
                logger.debug(f"代码 {code}: 无分红数据，跳过")
                # 无数据不算失败
        except Exception as e:
            logger.error(f"代码 {code} 处理失败: {e}", exc_info=True)
            total_failed += 1
            failed_codes.append(code)
        
        # 每处理10个代码输出一次进度
        if idx % 10 == 0:
            total_records = sum(len(df) for df in all_dataframes)
            logger.info(f"进度: {idx}/{len(codes)}，已获取 {len(all_dataframes)} 个基金的数据，共 {total_records} 条记录，失败 {total_failed} 个")
    
    # 4. 保存到CSV文件
    output_file = project_root / "data" / "fund_etf_dividend_sina.csv"
    logger.info("=" * 60)
    logger.info("开始保存数据到CSV文件...")
    
    try:
        save_dividend_data_to_csv(all_dataframes, str(output_file))
    except Exception as e:
        logger.error(f"保存CSV文件失败: {e}", exc_info=True)
        return
    
    # 5. 输出统计信息
    total_records = sum(len(df) for df in all_dataframes)
    logger.info("=" * 60)
    logger.info("处理完成！")
    logger.info(f"总代码数: {len(codes)}")
    logger.info(f"成功处理: {len(success_codes)} 个")
    logger.info(f"失败: {len(failed_codes)} 个")
    logger.info(f"总记录数: {total_records}")
    logger.info(f"输出文件: {output_file}")
    
    if failed_codes:
        logger.warning(f"失败的代码: {failed_codes[:10]}{'...' if len(failed_codes) > 10 else ''}")
    
    logger.info("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

