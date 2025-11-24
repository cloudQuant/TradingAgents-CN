"""
基金数据服务
负责从akshare获取基金数据并存储到MongoDB
"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, date
import pandas as pd
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import UpdateOne
import asyncio
import io

logger = logging.getLogger("webapi")


class FundDataService:
    """基金数据服务类"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.col_fund_name_em = db.get_collection("fund_name_em")
        self.col_fund_basic_info = db.get_collection("fund_basic_info")
        self.col_fund_info_index = db.get_collection("fund_info_index_em")
        self.col_fund_purchase_status = db.get_collection("fund_purchase_status")
        self.col_fund_etf_spot = db.get_collection("fund_etf_spot_em")
        self.col_fund_etf_spot_ths = db.get_collection("fund_etf_spot_ths")
        self.col_fund_lof_spot = db.get_collection("fund_lof_spot_em")
        self.col_fund_spot_sina = db.get_collection("fund_spot_sina")
        self.col_fund_etf_hist_min_em = db.get_collection("fund_etf_hist_min_em")
        self.col_fund_lof_hist_min_em = db.get_collection("fund_lof_hist_min_em")
        self.col_fund_etf_hist_em = db.get_collection("fund_etf_hist_em")
        self.col_fund_lof_hist_em = db.get_collection("fund_lof_hist_em")
        self.col_fund_hist_sina = db.get_collection("fund_hist_sina")
        self.col_fund_open_fund_daily_em = db.get_collection("fund_open_fund_daily_em")
        self.col_fund_open_fund_info_em = db.get_collection("fund_open_fund_info_em")
        self.col_fund_money_fund_daily_em = db.get_collection("fund_money_fund_daily_em")
        self.col_fund_money_fund_info_em = db.get_collection("fund_money_fund_info_em")
        self.col_fund_financial_fund_daily_em = db.get_collection("fund_financial_fund_daily_em")
        self.col_fund_financial_fund_info_em = db.get_collection("fund_financial_fund_info_em")
        self.col_fund_graded_fund_daily_em = db.get_collection("fund_graded_fund_daily_em")
        self.col_fund_graded_fund_info_em = db.get_collection("fund_graded_fund_info_em")
        self.col_fund_etf_fund_daily_em = db.get_collection("fund_etf_fund_daily_em")
        self.col_fund_hk_hist_em = db.get_collection("fund_hk_hist_em")
        self.col_fund_etf_fund_info_em = db.get_collection("fund_etf_fund_info_em")
        self.col_fund_etf_dividend_sina = db.get_collection("fund_etf_dividend_sina")
        self.col_fund_fh_em = db.get_collection("fund_fh_em")
        self.col_fund_cf_em = db.get_collection("fund_cf_em")
        self.col_fund_fh_rank_em = db.get_collection("fund_fh_rank_em")
        self.col_fund_open_fund_rank_em = db.get_collection("fund_open_fund_rank_em")
        self.col_fund_exchange_rank_em = db.get_collection("fund_exchange_rank_em")
        self.col_fund_money_rank_em = db.get_collection("fund_money_rank_em")
        self.col_fund_lcx_rank_em = db.get_collection("fund_lcx_rank_em")
        self.col_fund_hk_rank_em = db.get_collection("fund_hk_rank_em")
        self.col_fund_individual_achievement_xq = db.get_collection("fund_individual_achievement_xq")
        self.col_fund_value_estimation_em = db.get_collection("fund_value_estimation_em")
        self.col_fund_individual_analysis_xq = db.get_collection("fund_individual_analysis_xq")
        self.col_fund_individual_profit_probability_xq = db.get_collection("fund_individual_profit_probability_xq")
        self.col_fund_individual_detail_hold_xq = db.get_collection("fund_individual_detail_hold_xq")
        self.col_fund_overview_em = db.get_collection("fund_overview_em")
        self.col_fund_fee_em = db.get_collection("fund_fee_em")
        self.col_fund_individual_detail_info_xq = db.get_collection("fund_individual_detail_info_xq")
        self.col_fund_portfolio_hold_em = db.get_collection("fund_portfolio_hold_em")
        self.col_fund_portfolio_bond_hold_em = db.get_collection("fund_portfolio_bond_hold_em")
        self.col_fund_portfolio_change_em = db.get_collection("fund_portfolio_change_em")
        self.col_fund_rating_all_em = db.get_collection("fund_rating_all_em")
        self.col_fund_rating_sh_em = db.get_collection("fund_rating_sh_em")
        self.col_fund_rating_zs_em = db.get_collection("fund_rating_zs_em")
        self.col_fund_rating_ja_em = db.get_collection("fund_rating_ja_em")
        self.col_fund_manager_em = db.get_collection("fund_manager_em")
        self.col_fund_new_found_em = db.get_collection("fund_new_found_em")
        self.col_fund_scale_open_sina = db.get_collection("fund_scale_open_sina")
        self.col_fund_scale_close_sina = db.get_collection("fund_scale_close_sina")
        self.col_fund_scale_structured_sina = db.get_collection("fund_scale_structured_sina")
        self.col_fund_aum_em = db.get_collection("fund_aum_em")
        self.col_fund_aum_trend_em = db.get_collection("fund_aum_trend_em")
        self.col_fund_aum_hist_em = db.get_collection("fund_aum_hist_em")
        self.col_reits_realtime_em = db.get_collection("reits_realtime_em")
        self.col_reits_hist_em = db.get_collection("reits_hist_em")
        self.col_fund_report_stock_cninfo = db.get_collection("fund_report_stock_cninfo")
        self.col_fund_report_industry_allocation_cninfo = db.get_collection("fund_report_industry_allocation_cninfo")
        self.col_fund_report_asset_allocation_cninfo = db.get_collection("fund_report_asset_allocation_cninfo")
        self.col_fund_scale_change_em = db.get_collection("fund_scale_change_em")
        self.col_fund_hold_structure_em = db.get_collection("fund_hold_structure_em")
        self.col_fund_stock_position_lg = db.get_collection("fund_stock_position_lg")
        self.col_fund_balance_position_lg = db.get_collection("fund_balance_position_lg")
        self.col_fund_linghuo_position_lg = db.get_collection("fund_linghuo_position_lg")
        self.col_fund_announcement_dividend_em = db.get_collection("fund_announcement_dividend_em")
        self.col_fund_announcement_report_em = db.get_collection("fund_announcement_report_em")
        self.col_fund_announcement_personnel_em = db.get_collection("fund_announcement_personnel_em")
    
    async def save_fund_name_em_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """
        保存基金基本信息数据到MongoDB
        
        Args:
            df: 包含基金基本信息的DataFrame
            
        Returns:
            保存的记录数
        """
        if df is None or df.empty:
            logger.warning("没有基金基本信息数据需要保存")
            return 0
        
        try:
            # 清理无效的浮点数值（NaN, Infinity等），防止JSON序列化错误
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条基金数据...")
            
            # 分批处理，每批500条
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            logger.info(f"📦 将分 {total_batches} 批次处理，每批 {batch_size} 条")
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                logger.info(f"📝 处理第 {batch_idx + 1}/{total_batches} 批，记录范围: {start_idx + 1}-{end_idx}")
                
                # 构建批量操作
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    # 清理NaN/Infinity值（to_dict()可能会重新引入NaN）
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        # 转换 datetime.date 对象为字符串
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        # 转换 datetime.datetime 对象为字符串
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    # 添加元数据
                    fund_code = str(doc.get('基金代码', ''))
                    doc['code'] = fund_code
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_name_em'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    # 使用基金代码作为唯一标识
                    ops.append(
                        UpdateOne(
                            {'code': fund_code, 'endpoint': 'fund_name_em'},
                            {'$set': doc},
                            upsert=True
                        )
                    )
                
                # 执行批量写入
                if ops:
                    result = await self.col_fund_name_em.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    logger.info(
                        f"✅ 第 {batch_idx + 1}/{total_batches} 批写入完成: "
                        f"新增={result.upserted_count}, 更新={result.matched_count}, "
                        f"本批保存={batch_saved}, 累计={total_saved}/{total_count}"
                    )
                    
                    # 调用进度回调（如果提供）
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条基金数据")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存基金基本信息数据失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_name_em_data(self) -> int:
        """
        清空基金基本信息数据
        
        Returns:
            删除的记录数
        """
        try:
            result = await self.col_fund_name_em.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条基金基本信息数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空基金基本信息数据失败: {e}", exc_info=True)
            raise
    
    async def get_fund_name_em_stats(self) -> Dict[str, Any]:
        """
        获取基金基本信息统计
        
        Returns:
            统计信息字典
        """
        try:
            total_count = await self.col_fund_name_em.count_documents({})
            
            # 按基金类型统计
            pipeline = [
                {
                    '$group': {
                        '_id': '$基金类型',
                        'count': {'$sum': 1}
                    }
                },
                {
                    '$sort': {'count': -1}
                }
            ]
            
            type_stats = []
            async for doc in self.col_fund_name_em.aggregate(pipeline):
                type_stats.append({
                    'type': doc['_id'],
                    'count': doc['count']
                })
            
            return {
                'total_count': total_count,
                'type_stats': type_stats
            }
        except Exception as e:
            logger.error(f"获取基金基本信息统计失败: {e}", exc_info=True)
            raise
    
    async def save_fund_basic_info_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """
        保存基金基本信息数据到fund_basic_info集合
        使用 fund_individual_basic_info_xq 数据源
        
        Args:
            df: 包含基金基本信息的DataFrame
            
        Returns:
            保存的记录数
        """
        if df is None or df.empty:
            logger.warning("没有基金基本信息数据需要保存")
            return 0
        
        try:
            # 清理无效的浮点数值（NaN, Infinity等），防止JSON序列化错误
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条基金数据到fund_basic_info集合...")
            
            # 分批处理，每批500条
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            logger.info(f"📦 将分 {total_batches} 批次处理，每批 {batch_size} 条")
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                logger.info(f"📝 处理第 {batch_idx + 1}/{total_batches} 批，记录范围: {start_idx + 1}-{end_idx}")
                
                # 构建批量操作
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    # 清理NaN/Infinity值（to_dict()可能会重新引入NaN）
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        # 转换 datetime.date 对象为字符串
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        # 转换 datetime.datetime 对象为字符串
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    # 添加元数据
                    fund_code = str(doc.get('基金代码', ''))
                    doc['code'] = fund_code
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_individual_basic_info_xq'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    # 使用基金代码作为唯一标识
                    ops.append(
                        UpdateOne(
                            {'code': fund_code},
                            {'$set': doc},
                            upsert=True
                        )
                    )
                
                # 执行批量写入
                if ops:
                    result = await self.col_fund_basic_info.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    logger.info(
                        f"✅ 第 {batch_idx + 1}/{total_batches} 批写入fund_basic_info完成: "
                        f"新增={result.upserted_count}, 更新={result.matched_count}, "
                        f"本批保存={batch_saved}, 累计={total_saved}/{total_count}"
                    )
                    
                    # 调用进度回调（如果提供）
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据到fund_basic_info ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入fund_basic_info完成: 总计保存 {total_saved}/{total_count} 条基金数据")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存基金基本信息数据到fund_basic_info失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_basic_info_data(self) -> int:
        """
        清空fund_basic_info基金数据
        
        Returns:
            删除的记录数
        """
        try:
            result = await self.col_fund_basic_info.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空fund_basic_info {deleted_count} 条数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空fund_basic_info数据失败: {e}", exc_info=True)
            raise
    
    async def get_fund_basic_info_stats(self) -> Dict[str, Any]:
        """
        获取fund_basic_info集合统计
        
        Returns:
            统计信息字典
        """
        try:
            total_count = await self.col_fund_basic_info.count_documents({})
            
            # 按基金类型统计
            pipeline = [
                {
                    '$group': {
                        '_id': '$基金类型',
                        'count': {'$sum': 1}
                    }
                },
                {
                    '$sort': {'count': -1}
                }
            ]
            
            type_stats = []
            async for doc in self.col_fund_basic_info.aggregate(pipeline):
                type_stats.append({
                    'type': doc['_id'],
                    'count': doc['count']
                })
            
            return {
                'total_count': total_count,
                'type_stats': type_stats
            }
        except Exception as e:
            logger.error(f"获取fund_basic_info统计失败: {e}", exc_info=True)
            raise

    async def save_fund_info_index_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存指数型基金基本信息数据到 fund_info_index_em 集合。

        使用 akshare fund_info_index_em 接口数据，
        以 基金代码 + 日期 作为唯一标识。
        """
        if df is None or df.empty:
            logger.warning("没有指数型基金基本信息数据需要保存")
            return 0

        try:
            # 清理无效的浮点数值（NaN, Infinity等），防止JSON序列化错误
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)  # 替换无穷大为None
            df = df.where(pd.notna(df), None)  # 替换NaN为None
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条指数型基金数据到 fund_info_index_em 集合...")

            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size

            logger.info(f"📦 将分 {total_batches} 批次处理，每批 {batch_size} 条")

            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]

                logger.info(f"📝 处理第 {batch_idx + 1}/{total_batches} 批，记录范围: {start_idx + 1}-{end_idx}")

                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    # 再次清理NaN/Infinity值（to_dict()可能会重新引入NaN）
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        # 转换 datetime.date 对象为字符串
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        # 转换 datetime.datetime 对象为字符串
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')

                    fund_code = str(doc.get('基金代码', '')).strip()
                    date_str = str(doc.get('日期', '')).strip()
                    tracking_target = str(doc.get('跟踪标的', '')).strip()
                    
                    if not fund_code or not date_str or not tracking_target:
                        continue

                    # 元数据
                    doc['code'] = fund_code
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_info_index_em'
                    doc['updated_at'] = datetime.now().isoformat()

                    # 使用 日期 + 基金代码 + 跟踪标的 作为唯一标识
                    ops.append(
                        UpdateOne(
                            {
                                '日期': date_str,
                                'code': fund_code,
                                '跟踪标的': tracking_target
                            },
                            {'$set': doc},
                            upsert=True
                        )
                    )

                if ops:
                    result = await self.col_fund_info_index.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved

                    logger.info(
                        f"✅ 第 {batch_idx + 1}/{total_batches} 批写入 fund_info_index_em 完成: "
                        f"新增={result.upserted_count}, 更新={result.matched_count}, "
                        f"本批保存={batch_saved}, 累计={total_saved}/{total_count}"
                    )

                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据到 fund_info_index_em ({progress}%)"
                        )

            logger.info(
                f"🎉 全部数据写入 fund_info_index_em 完成: 总计保存 {total_saved}/{total_count} 条指数型基金数据"
            )
            return total_saved
        except Exception as e:
            logger.error(f"保存指数型基金基本信息数据到 fund_info_index_em 失败: {e}", exc_info=True)
            raise

    async def clear_fund_info_index_data(self) -> int:
        """清空 fund_info_index_em 指数型基金数据"""
        try:
            result = await self.col_fund_info_index.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 fund_info_index_em {deleted_count} 条数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空 fund_info_index_em 数据失败: {e}", exc_info=True)
            raise

    async def get_fund_info_index_stats(self) -> Dict[str, Any]:
        """获取 fund_info_index_em 集合统计信息"""
        try:
            total_count = await self.col_fund_info_index.count_documents({})

            # 按跟踪标的统计
            pipeline_type = [
                {
                    '$group': {
                        '_id': '$跟踪标的',
                        'count': {'$sum': 1}
                    }
                },
                {
                    '$sort': {'count': -1}
                }
            ]

            type_stats: List[Dict[str, Any]] = []
            async for doc in self.col_fund_info_index.aggregate(pipeline_type):
                type_stats.append({
                    'type': doc['_id'],
                    'count': doc['count']
                })

            # 计算最早和最晚日期
            earliest_date = None
            latest_date = None
            pipeline_date = [
                {
                    '$group': {
                        '_id': None,
                        'earliest': {'$min': '$日期'},
                        'latest': {'$max': '$日期'}
                    }
                }
            ]

            async for doc in self.col_fund_info_index.aggregate(pipeline_date):
                earliest_date = doc.get('earliest')
                latest_date = doc.get('latest')

            return {
                'total_count': total_count,
                'type_stats': type_stats,
                'earliest_date': earliest_date,
                'latest_date': latest_date
            }
        except Exception as e:
            logger.error(f"获取 fund_info_index_em 统计失败: {e}", exc_info=True)
            raise

    async def import_data_from_file(self, collection_name: str, content: bytes, filename: str) -> Dict[str, Any]:
        """从文件导入数据"""
        try:
            if filename.endswith('.csv'):
                df = pd.read_csv(io.BytesIO(content))
            else:
                df = pd.read_excel(io.BytesIO(content))
            
            if df.empty:
                return {"imported_count": 0, "message": "文件为空"}
                
            count = 0
            if collection_name == 'fund_name_em':
                count = await self.save_fund_name_em_data(df)
            elif collection_name == 'fund_basic_info':
                count = await self.save_fund_basic_info_data(df)
            elif collection_name == 'fund_info_index_em':
                count = await self.save_fund_info_index_data(df)
            elif collection_name == 'fund_purchase_status':
                count = await self.save_fund_purchase_status_data(df)
            elif collection_name == 'fund_etf_spot_em':
                count = await self.save_fund_etf_spot_data(df)
            elif collection_name == 'fund_etf_spot_ths':
                count = await self.save_fund_etf_spot_ths_data(df)
            elif collection_name == 'fund_lof_spot_em':
                count = await self.save_fund_lof_spot_data(df)
            elif collection_name == 'fund_spot_sina':
                count = await self.save_fund_spot_sina_data(df)
            elif collection_name == 'fund_etf_hist_min_em':
                count = await self.save_fund_etf_hist_min_data(df)
            elif collection_name == 'fund_etf_hist_em':
                count = await self.save_fund_etf_hist_data(df)
            elif collection_name == 'fund_lof_hist_em':
                count = await self.save_fund_lof_hist_data(df)
            elif collection_name == 'fund_hist_sina':
                count = await self.save_fund_hist_sina_data(df)
            elif collection_name == 'fund_open_fund_daily_em':
                count = await self.save_fund_open_fund_daily_data(df)
            elif collection_name == 'fund_open_fund_info_em':
                # 文件导入需要指定 fund_code 和 indicator
                logger.warning("开放式基金历史行情文件导入需要特殊处理，请使用 API 刷新")
                return {"imported_count": 0, "message": "该集合需要通过 API 刷新"}
            elif collection_name == 'fund_money_fund_daily_em':
                count = await self.save_fund_money_fund_daily_data(df)
            elif collection_name == 'fund_money_fund_info_em':
                logger.warning("货币型基金历史行情文件导入需要指定基金代码")
                return {"imported_count": 0, "message": "该集合需要通过 API 刷新"}
            elif collection_name == 'fund_financial_fund_daily_em':
                count = await self.save_fund_financial_fund_daily_data(df)
            elif collection_name == 'fund_financial_fund_info_em':
                logger.warning("理财型基金历史行惁文件导入需要指定基金代码")
                return {"imported_count": 0, "message": "该集合需要通过 API 刷新"}
            elif collection_name == 'fund_graded_fund_daily_em':
                count = await self.save_fund_graded_fund_daily_data(df)
            elif collection_name == 'fund_graded_fund_info_em':
                logger.warning("分级基金历史数据文件导入需要指定基金代码")
                return {"imported_count": 0, "message": "该集合需要通过 API 刷新"}
            elif collection_name == 'fund_etf_fund_daily_em':
                count = await self.save_fund_etf_fund_daily_data(df)
            elif collection_name == 'fund_hk_hist_em':
                count = await self.save_fund_hk_hist_em_data(df)
            elif collection_name == 'fund_cf_em':
                count = await self.save_fund_cf_em_data(df)
            elif collection_name == 'fund_fh_rank_em':
                count = await self.save_fund_fh_rank_em_data(df)
            elif collection_name == 'fund_open_fund_rank_em':
                count = await self.save_fund_open_fund_rank_em_data(df)
            elif collection_name == 'fund_exchange_rank_em':
                count = await self.save_fund_exchange_rank_em_data(df)
            elif collection_name == 'fund_money_rank_em':
                count = await self.save_fund_money_rank_em_data(df)
            elif collection_name == 'fund_lcx_rank_em':
                count = await self.save_fund_lcx_rank_em_data(df)
            elif collection_name == 'fund_hk_rank_em':
                count = await self.save_fund_hk_rank_em_data(df)
            elif collection_name == 'fund_individual_achievement_xq':
                count = await self.save_fund_individual_achievement_xq_data(df)
            elif collection_name == 'fund_value_estimation_em':
                count = await self.save_fund_value_estimation_em_data(df)
            elif collection_name == 'fund_individual_analysis_xq':
                count = await self.save_fund_individual_analysis_xq_data(df)
            elif collection_name == 'fund_individual_profit_probability_xq':
                count = await self.save_fund_individual_profit_probability_xq_data(df)
            elif collection_name == 'fund_individual_detail_hold_xq':
                count = await self.save_fund_individual_detail_hold_xq_data(df)
            elif collection_name == 'fund_overview_em':
                count = await self.save_fund_overview_em_data(df)
            elif collection_name == 'fund_fee_em':
                count = await self.save_fund_fee_em_data(df)
            elif collection_name == 'fund_individual_detail_info_xq':
                count = await self.save_fund_individual_detail_info_xq_data(df)
            elif collection_name == 'fund_portfolio_hold_em':
                count = await self.save_fund_portfolio_hold_em_data(df)
            elif collection_name == 'fund_portfolio_bond_hold_em':
                count = await self.save_fund_portfolio_bond_hold_em_data(df)
            elif collection_name == 'fund_portfolio_industry_allocation_em':
                count = await self.save_fund_portfolio_industry_allocation_em_data(df)
            elif collection_name == 'fund_portfolio_change_em':
                count = await self.save_fund_portfolio_change_em_data(df)
            elif collection_name == 'fund_rating_all_em':
                count = await self.save_fund_rating_all_em_data(df)
            elif collection_name == 'fund_rating_sh_em':
                count = await self.save_fund_rating_sh_em_data(df)
            elif collection_name == 'fund_rating_zs_em':
                count = await self.save_fund_rating_zs_em_data(df)
            elif collection_name == 'fund_rating_ja_em':
                count = await self.save_fund_rating_ja_em_data(df)
            elif collection_name == 'fund_manager_em':
                count = await self.save_fund_manager_em_data(df)
            elif collection_name == 'fund_new_found_em':
                count = await self.save_fund_new_found_em_data(df)
            elif collection_name == 'fund_scale_open_sina':
                count = await self.save_fund_scale_open_sina_data(df)
            elif collection_name == 'fund_scale_close_sina':
                count = await self.save_fund_scale_close_sina_data(df)
            elif collection_name == 'fund_scale_structured_sina':
                count = await self.save_fund_scale_structured_sina_data(df)
            elif collection_name == 'fund_aum_em':
                count = await self.save_fund_aum_em_data(df)
            elif collection_name == 'fund_aum_trend_em':
                count = await self.save_fund_aum_trend_em_data(df)
            elif collection_name == 'fund_aum_hist_em':
                count = await self.save_fund_aum_hist_em_data(df)
            elif collection_name == 'reits_realtime_em':
                count = await self.save_reits_realtime_em_data(df)
            elif collection_name == 'reits_hist_em':
                count = await self.save_reits_hist_em_data(df)
            elif collection_name == 'fund_report_stock_cninfo':
                count = await self.save_fund_report_stock_cninfo_data(df)
            elif collection_name == 'fund_report_industry_allocation_cninfo':
                count = await self.save_fund_report_industry_allocation_cninfo_data(df)
            elif collection_name == 'fund_report_asset_allocation_cninfo':
                count = await self.save_fund_report_asset_allocation_cninfo_data(df)
            elif collection_name == 'fund_scale_change_em':
                count = await self.save_fund_scale_change_em_data(df)
            elif collection_name == 'fund_hold_structure_em':
                count = await self.save_fund_hold_structure_em_data(df)
            elif collection_name == 'fund_stock_position_lg':
                count = await self.save_fund_stock_position_lg_data(df)
            elif collection_name == 'fund_balance_position_lg':
                count = await self.save_fund_balance_position_lg_data(df)
            elif collection_name == 'fund_linghuo_position_lg':
                count = await self.save_fund_linghuo_position_lg_data(df)
            elif collection_name == 'fund_announcement_dividend_em':
                count = await self.save_fund_announcement_dividend_em_data(df)
            elif collection_name == 'fund_announcement_report_em':
                count = await self.save_fund_announcement_report_em_data(df)
            elif collection_name == 'fund_announcement_personnel_em':
                count = await self.save_fund_announcement_personnel_em_data(df)
            else:
                raise ValueError(f"不支持的文件导入集合: {collection_name}")
                
            return {"imported_count": count, "message": f"成功导入 {count} 条数据"}
        except Exception as e:
            logger.error(f"导入文件失败: {e}", exc_info=True)
            raise

    async def sync_data_from_remote(self, collection_name: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """从远程数据库同步数据"""
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
            
            if "mongodb://" in host:
                client = AsyncIOMotorClient(host)
            else:
                client = AsyncIOMotorClient(uri)
                
            try:
                if "mongodb://" in host and "/" in host.split("://")[1]:
                     remote_db = client.get_default_database()
                else:
                     remote_db = client[remote_db_name]
            except Exception:
                remote_db = client[remote_db_name]

            remote_col = remote_db[remote_col_name]
            
            cursor = remote_col.find({})
            
            batch = []
            total_synced = 0
            
            async for doc in cursor:
                if '_id' in doc:
                    del doc['_id']
                batch.append(doc)
                
                if len(batch) >= batch_size:
                    df = pd.DataFrame(batch)
                    if collection_name == 'fund_name_em':
                        await self.save_fund_name_em_data(df)
                    elif collection_name == 'fund_basic_info':
                        await self.save_fund_basic_info_data(df)
                    elif collection_name == 'fund_info_index_em':
                        await self.save_fund_info_index_data(df)
                    elif collection_name == 'fund_purchase_status':
                        await self.save_fund_purchase_status_data(df)
                    elif collection_name == 'fund_etf_spot_em':
                        await self.save_fund_etf_spot_data(df)
                    elif collection_name == 'fund_etf_spot_ths':
                        await self.save_fund_etf_spot_ths_data(df)
                    elif collection_name == 'fund_lof_spot_em':
                        await self.save_fund_lof_spot_data(df)
                    elif collection_name == 'fund_spot_sina':
                        await self.save_fund_spot_sina_data(df)
                    elif collection_name == 'fund_etf_hist_min_em':
                        await self.save_fund_etf_hist_min_data(df)
                    elif collection_name == 'fund_etf_hist_em':
                        await self.save_fund_etf_hist_data(df)
                    elif collection_name == 'fund_lof_hist_em':
                        await self.save_fund_lof_hist_data(df)
                    elif collection_name == 'fund_hist_sina':
                        await self.save_fund_hist_sina_data(df)
                    elif collection_name == 'fund_open_fund_daily_em':
                        await self.save_fund_open_fund_daily_data(df)
                    elif collection_name == 'fund_open_fund_info_em':
                        logger.warning("开放式基金历史行情需要特殊处理")
                    elif collection_name == 'fund_money_fund_daily_em':
                        await self.save_fund_money_fund_daily_data(df)
                    elif collection_name == 'fund_money_fund_info_em':
                        logger.warning("货币型基金历史行情需要特殊处理")
                    elif collection_name == 'fund_hk_hist_em':
                        await self.save_fund_hk_hist_em_data(df)
                    elif collection_name == 'fund_cf_em':
                        await self.save_fund_cf_em_data(df)
                    elif collection_name == 'fund_fh_rank_em':
                        await self.save_fund_fh_rank_em_data(df)
                    elif collection_name == 'fund_open_fund_rank_em':
                        await self.save_fund_open_fund_rank_em_data(df)
                    elif collection_name == 'fund_exchange_rank_em':
                        await self.save_fund_exchange_rank_em_data(df)
                    elif collection_name == 'fund_money_rank_em':
                        await self.save_fund_money_rank_em_data(df)
                    elif collection_name == 'fund_lcx_rank_em':
                        await self.save_fund_lcx_rank_em_data(df)
                    elif collection_name == 'fund_hk_rank_em':
                        await self.save_fund_hk_rank_em_data(df)
                    elif collection_name == 'fund_individual_achievement_xq':
                        await self.save_fund_individual_achievement_xq_data(df)
                    elif collection_name == 'fund_value_estimation_em':
                        await self.save_fund_value_estimation_em_data(df)
                    elif collection_name == 'fund_individual_analysis_xq':
                        await self.save_fund_individual_analysis_xq_data(df)
                    elif collection_name == 'fund_individual_profit_probability_xq':
                        await self.save_fund_individual_profit_probability_xq_data(df)
                    elif collection_name == 'fund_individual_detail_hold_xq':
                        await self.save_fund_individual_detail_hold_xq_data(df)
                    elif collection_name == 'fund_overview_em':
                        await self.save_fund_overview_em_data(df)
                    elif collection_name == 'fund_fee_em':
                        await self.save_fund_fee_em_data(df)
                    elif collection_name == 'fund_individual_detail_info_xq':
                        await self.save_fund_individual_detail_info_xq_data(df)
                    elif collection_name == 'fund_portfolio_hold_em':
                        await self.save_fund_portfolio_hold_em_data(df)
                    elif collection_name == 'fund_portfolio_bond_hold_em':
                        await self.save_fund_portfolio_bond_hold_em_data(df)
                    elif collection_name == 'fund_portfolio_industry_allocation_em':
                        await self.save_fund_portfolio_industry_allocation_em_data(df)
                    elif collection_name == 'fund_portfolio_change_em':
                        await self.save_fund_portfolio_change_em_data(df)
                    elif collection_name == 'fund_rating_all_em':
                        await self.save_fund_rating_all_em_data(df)
                    elif collection_name == 'fund_rating_sh_em':
                        await self.save_fund_rating_sh_em_data(df)
                    elif collection_name == 'fund_rating_zs_em':
                        await self.save_fund_rating_zs_em_data(df)
                    elif collection_name == 'fund_rating_ja_em':
                        await self.save_fund_rating_ja_em_data(df)
                    elif collection_name == 'fund_manager_em':
                        await self.save_fund_manager_em_data(df)
                    elif collection_name == 'fund_new_found_em':
                        await self.save_fund_new_found_em_data(df)
                    elif collection_name == 'fund_scale_open_sina':
                        await self.save_fund_scale_open_sina_data(df)
                    elif collection_name == 'fund_scale_close_sina':
                        await self.save_fund_scale_close_sina_data(df)
                    elif collection_name == 'fund_scale_structured_sina':
                        await self.save_fund_scale_structured_sina_data(df)
                    elif collection_name == 'fund_aum_em':
                        await self.save_fund_aum_em_data(df)
                    elif collection_name == 'fund_aum_trend_em':
                        await self.save_fund_aum_trend_em_data(df)
                    elif collection_name == 'fund_aum_hist_em':
                        await self.save_fund_aum_hist_em_data(df)
                    elif collection_name == 'reits_realtime_em':
                        await self.save_reits_realtime_em_data(df)
                    elif collection_name == 'reits_hist_em':
                        await self.save_reits_hist_em_data(df)
                    elif collection_name == 'fund_report_stock_cninfo':
                        await self.save_fund_report_stock_cninfo_data(df)
                    elif collection_name == 'fund_report_industry_allocation_cninfo':
                        await self.save_fund_report_industry_allocation_cninfo_data(df)
                    elif collection_name == 'fund_report_asset_allocation_cninfo':
                        await self.save_fund_report_asset_allocation_cninfo_data(df)
                    elif collection_name == 'fund_scale_change_em':
                        await self.save_fund_scale_change_em_data(df)
                    elif collection_name == 'fund_hold_structure_em':
                        await self.save_fund_hold_structure_em_data(df)
                    elif collection_name == 'fund_stock_position_lg':
                        await self.save_fund_stock_position_lg_data(df)
                    elif collection_name == 'fund_balance_position_lg':
                        await self.save_fund_balance_position_lg_data(df)
                    elif collection_name == 'fund_linghuo_position_lg':
                        await self.save_fund_linghuo_position_lg_data(df)
                    elif collection_name == 'fund_announcement_dividend_em':
                        await self.save_fund_announcement_dividend_em_data(df)
                    elif collection_name == 'fund_announcement_report_em':
                        await self.save_fund_announcement_report_em_data(df)
                    elif collection_name == 'fund_announcement_personnel_em':
                        await self.save_fund_announcement_personnel_em_data(df)
                    total_synced += len(batch)
                    batch = []
            
            if batch:
                df = pd.DataFrame(batch)
                if collection_name == 'fund_name_em':
                    await self.save_fund_name_em_data(df)
                elif collection_name == 'fund_basic_info':
                    await self.save_fund_basic_info_data(df)
                elif collection_name == 'fund_info_index_em':
                    await self.save_fund_info_index_data(df)
                elif collection_name == 'fund_purchase_status':
                    await self.save_fund_purchase_status_data(df)
                elif collection_name == 'fund_etf_spot_em':
                    await self.save_fund_etf_spot_data(df)
                elif collection_name == 'fund_etf_spot_ths':
                    await self.save_fund_etf_spot_ths_data(df)
                elif collection_name == 'fund_lof_spot_em':
                    await self.save_fund_lof_spot_data(df)
                elif collection_name == 'fund_spot_sina':
                    await self.save_fund_spot_sina_data(df)
                elif collection_name == 'fund_etf_hist_min_em':
                    await self.save_fund_etf_hist_min_data(df)
                elif collection_name == 'fund_etf_hist_em':
                    await self.save_fund_etf_hist_data(df)
                elif collection_name == 'fund_lof_hist_em':
                    await self.save_fund_lof_hist_data(df)
                elif collection_name == 'fund_hist_sina':
                    await self.save_fund_hist_sina_data(df)
                elif collection_name == 'fund_open_fund_daily_em':
                    await self.save_fund_open_fund_daily_data(df)
                elif collection_name == 'fund_open_fund_info_em':
                    logger.warning("开放式基金历史行情需要特殊处理")
                elif collection_name == 'fund_money_fund_daily_em':
                    await self.save_fund_money_fund_daily_data(df)
                elif collection_name == 'fund_money_fund_info_em':
                    logger.warning("货币型基金历史行情需要特殊处理")
                elif collection_name == 'fund_hk_hist_em':
                    await self.save_fund_hk_hist_em_data(df)
                elif collection_name == 'fund_cf_em':
                    await self.save_fund_cf_em_data(df)
                elif collection_name == 'fund_fh_rank_em':
                    await self.save_fund_fh_rank_em_data(df)
                elif collection_name == 'fund_open_fund_rank_em':
                    await self.save_fund_open_fund_rank_em_data(df)
                elif collection_name == 'fund_exchange_rank_em':
                    await self.save_fund_exchange_rank_em_data(df)
                elif collection_name == 'fund_money_rank_em':
                    await self.save_fund_money_rank_em_data(df)
                elif collection_name == 'fund_lcx_rank_em':
                    await self.save_fund_lcx_rank_em_data(df)
                elif collection_name == 'fund_hk_rank_em':
                    await self.save_fund_hk_rank_em_data(df)
                elif collection_name == 'fund_individual_achievement_xq':
                    await self.save_fund_individual_achievement_xq_data(df)
                elif collection_name == 'fund_value_estimation_em':
                    await self.save_fund_value_estimation_em_data(df)
                elif collection_name == 'fund_individual_analysis_xq':
                    await self.save_fund_individual_analysis_xq_data(df)
                elif collection_name == 'fund_individual_profit_probability_xq':
                    await self.save_fund_individual_profit_probability_xq_data(df)
                elif collection_name == 'fund_individual_detail_hold_xq':
                    await self.save_fund_individual_detail_hold_xq_data(df)
                elif collection_name == 'fund_overview_em':
                    await self.save_fund_overview_em_data(df)
                elif collection_name == 'fund_fee_em':
                    await self.save_fund_fee_em_data(df)
                elif collection_name == 'fund_individual_detail_info_xq':
                    await self.save_fund_individual_detail_info_xq_data(df)
                elif collection_name == 'fund_portfolio_hold_em':
                    await self.save_fund_portfolio_hold_em_data(df)
                elif collection_name == 'fund_portfolio_bond_hold_em':
                    await self.save_fund_portfolio_bond_hold_em_data(df)
                elif collection_name == 'fund_portfolio_industry_allocation_em':
                    await self.save_fund_portfolio_industry_allocation_em_data(df)
                elif collection_name == 'fund_portfolio_change_em':
                    await self.save_fund_portfolio_change_em_data(df)
                elif collection_name == 'fund_rating_all_em':
                    await self.save_fund_rating_all_em_data(df)
                elif collection_name == 'fund_rating_sh_em':
                    await self.save_fund_rating_sh_em_data(df)
                elif collection_name == 'fund_rating_zs_em':
                    await self.save_fund_rating_zs_em_data(df)
                elif collection_name == 'fund_rating_ja_em':
                    await self.save_fund_rating_ja_em_data(df)
                elif collection_name == 'fund_manager_em':
                    await self.save_fund_manager_em_data(df)
                elif collection_name == 'fund_new_found_em':
                    await self.save_fund_new_found_em_data(df)
                elif collection_name == 'fund_scale_open_sina':
                    await self.save_fund_scale_open_sina_data(df)
                elif collection_name == 'fund_scale_close_sina':
                    await self.save_fund_scale_close_sina_data(df)
                elif collection_name == 'fund_scale_structured_sina':
                    await self.save_fund_scale_structured_sina_data(df)
                elif collection_name == 'fund_aum_em':
                    await self.save_fund_aum_em_data(df)
                elif collection_name == 'fund_aum_trend_em':
                    await self.save_fund_aum_trend_em_data(df)
                elif collection_name == 'fund_aum_hist_em':
                    await self.save_fund_aum_hist_em_data(df)
                elif collection_name == 'reits_realtime_em':
                    await self.save_reits_realtime_em_data(df)
                elif collection_name == 'reits_hist_em':
                    await self.save_reits_hist_em_data(df)
                elif collection_name == 'fund_report_stock_cninfo':
                    await self.save_fund_report_stock_cninfo_data(df)
                elif collection_name == 'fund_report_industry_allocation_cninfo':
                    await self.save_fund_report_industry_allocation_cninfo_data(df)
                elif collection_name == 'fund_report_asset_allocation_cninfo':
                    await self.save_fund_report_asset_allocation_cninfo_data(df)
                elif collection_name == 'fund_scale_change_em':
                    await self.save_fund_scale_change_em_data(df)
                elif collection_name == 'fund_hold_structure_em':
                    await self.save_fund_hold_structure_em_data(df)
                elif collection_name == 'fund_stock_position_lg':
                    await self.save_fund_stock_position_lg_data(df)
                elif collection_name == 'fund_balance_position_lg':
                    await self.save_fund_balance_position_lg_data(df)
                elif collection_name == 'fund_linghuo_position_lg':
                    await self.save_fund_linghuo_position_lg_data(df)
                elif collection_name == 'fund_announcement_dividend_em':
                    await self.save_fund_announcement_dividend_em_data(df)
                elif collection_name == 'fund_announcement_report_em':
                    await self.save_fund_announcement_report_em_data(df)
                elif collection_name == 'fund_announcement_personnel_em':
                    await self.save_fund_announcement_personnel_em_data(df)
                total_synced += len(batch)
                
            client.close()
            
            return {
                "synced_count": total_synced, 
                "remote_total": total_synced,
                "message": f"成功同步 {total_synced} 条数据"
            }
            
        except Exception as e:
            logger.error(f"远程同步失败: {e}", exc_info=True)
            raise
    
    async def save_fund_purchase_status_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """
        保存基金申购状态数据到fund_purchase_status集合
        
        Args:
            df: 包含基金申购状态的DataFrame
            progress_callback: 进度回调函数
            
        Returns:
            保存的记录数
        """
        if df is None or df.empty:
            logger.warning("没有基金申购状态数据需要保存")
            return 0
        
        try:
            # 清理无效的浮点数值
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条基金申购状态数据...")
            
            # 分批处理
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            logger.info(f"📦 将分 {total_batches} 批次处理，每批 {batch_size} 条")
            
            # 获取当前日期作为数据日期
            current_date = datetime.now().strftime('%Y-%m-%d')
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                logger.info(f"📝 处理第 {batch_idx + 1}/{total_batches} 批，记录范围: {start_idx + 1}-{end_idx}")
                
                # 构建批量操作
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    # 清理NaN/Infinity值
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        # 转换 datetime.date 对象为字符串
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        # 转换 datetime.datetime 对象为字符串
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    # 获取基金代码和报告时间
                    fund_code = str(doc.get('基金代码', ''))
                    report_time = str(doc.get('最新净值/万份收益-报告时间', current_date))
                    
                    # 添加元数据
                    doc['code'] = fund_code
                    doc['date'] = report_time
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_purchase_em'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    # 使用基金代码和日期作为唯一标识（如需求所述）
                    ops.append(
                        UpdateOne(
                            {'code': fund_code, 'date': report_time},
                            {'$set': doc},
                            upsert=True
                        )
                    )
                
                # 执行批量写入
                if ops:
                    result = await self.col_fund_purchase_status.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    logger.info(
                        f"✅ 第 {batch_idx + 1}/{total_batches} 批写入完成: "
                        f"新增={result.upserted_count}, 更新={result.matched_count}, "
                        f"本批保存={batch_saved}, 累计={total_saved}/{total_count}"
                    )
                    
                    # 调用进度回调
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条基金申购状态数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条基金申购状态数据")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存基金申购状态数据失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_purchase_status_data(self) -> int:
        """
        清空基金申购状态数据
        
        Returns:
            删除的记录数
        """
        try:
            result = await self.col_fund_purchase_status.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条基金申购状态数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空基金申购状态数据失败: {e}", exc_info=True)
            raise
    
    async def get_fund_purchase_status_stats(self) -> Dict[str, Any]:
        """
        获取基金申购状态统计信息
        
        Returns:
            统计信息字典
        """
        try:
            total_count = await self.col_fund_purchase_status.count_documents({})
            
            # 按基金类型统计
            pipeline_type = [
                {
                    '$group': {
                        '_id': '$基金类型',
                        'count': {'$sum': 1}
                    }
                },
                {
                    '$sort': {'count': -1}
                }
            ]
            
            type_stats: List[Dict[str, Any]] = []
            async for doc in self.col_fund_purchase_status.aggregate(pipeline_type):
                type_stats.append({
                    'type': doc['_id'],
                    'count': doc['count']
                })
            
            # 按申购状态统计
            pipeline_purchase = [
                {
                    '$group': {
                        '_id': '$申购状态',
                        'count': {'$sum': 1}
                    }
                },
                {
                    '$sort': {'count': -1}
                }
            ]
            
            purchase_status_stats: List[Dict[str, Any]] = []
            async for doc in self.col_fund_purchase_status.aggregate(pipeline_purchase):
                purchase_status_stats.append({
                    'status': doc['_id'],
                    'count': doc['count']
                })
            
            # 按赎回状态统计
            pipeline_redeem = [
                {
                    '$group': {
                        '_id': '$赎回状态',
                        'count': {'$sum': 1}
                    }
                },
                {
                    '$sort': {'count': -1}
                }
            ]
            
            redeem_status_stats: List[Dict[str, Any]] = []
            async for doc in self.col_fund_purchase_status.aggregate(pipeline_redeem):
                redeem_status_stats.append({
                    'status': doc['_id'],
                    'count': doc['count']
                })
            
            # 计算最早和最晚日期
            earliest_date = None
            latest_date = None
            pipeline_date = [
                {
                    '$group': {
                        '_id': None,
                        'earliest': {'$min': '$date'},
                        'latest': {'$max': '$date'}
                    }
                }
            ]
            
            async for doc in self.col_fund_purchase_status.aggregate(pipeline_date):
                earliest_date = doc.get('earliest')
                latest_date = doc.get('latest')
            
            return {
                'total_count': total_count,
                'type_stats': type_stats,
                'purchase_status_stats': purchase_status_stats,
                'redeem_status_stats': redeem_status_stats,
                'earliest_date': earliest_date,
                'latest_date': latest_date
            }
        except Exception as e:
            logger.error(f"获取基金申购状态统计失败: {e}", exc_info=True)
            raise
    
    async def save_fund_etf_spot_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """
        保存ETF基金实时行情数据到fund_etf_spot_em集合
        
        Args:
            df: 包含ETF基金实时行情的DataFrame
            progress_callback: 进度回调函数
            
        Returns:
            保存的记录数
        """
        if df is None or df.empty:
            logger.warning("没有ETF基金实时行情数据需要保存")
            return 0
        
        try:
            # 清理无效的浮点数值
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条ETF基金实时行情数据...")
            
            # 分批处理
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            logger.info(f"📦 将分 {total_batches} 批次处理，每批 {batch_size} 条")
            
            # 获取当前日期作为数据日期（如果数据中没有日期字段）
            current_date = datetime.now().strftime('%Y-%m-%d')
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                logger.info(f"📝 处理第 {batch_idx + 1}/{total_batches} 批，记录范围: {start_idx + 1}-{end_idx}")
                
                # 构建批量操作
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    # 清理NaN/Infinity值和转换日期类型
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        # 转换 datetime.date 对象为字符串
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        # 转换 datetime.datetime 对象为字符串
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d %H:%M:%S')
                    
                    # 获取基金代码和数据日期
                    fund_code = str(doc.get('代码', ''))
                    data_date = str(doc.get('数据日期', current_date))
                    
                    # 添加元数据
                    doc['code'] = fund_code
                    doc['date'] = data_date
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_etf_spot_em'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    # 使用基金代码和日期作为唯一标识
                    ops.append(
                        UpdateOne(
                            {'code': fund_code, 'date': data_date},
                            {'$set': doc},
                            upsert=True
                        )
                    )
                
                # 执行批量写入
                if ops:
                    result = await self.col_fund_etf_spot.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    logger.info(
                        f"✅ 第 {batch_idx + 1}/{total_batches} 批写入完成: "
                        f"新增={result.upserted_count}, 更新={result.matched_count}, "
                        f"本批保存={batch_saved}, 累计={total_saved}/{total_count}"
                    )
                    
                    # 调用进度回调
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条ETF基金实时行情数据")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存ETF基金实时行情数据失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_etf_spot_data(self) -> int:
        """
        清空ETF基金实时行情数据
        
        Returns:
            删除的记录数
        """
        try:
            result = await self.col_fund_etf_spot.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"🗑️  已清空 {deleted_count} 条ETF基金实时行情数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空ETF基金实时行情数据失败: {e}", exc_info=True)
            raise
    
    async def get_fund_etf_spot_stats(self) -> Dict[str, Any]:
        """
        获取ETF基金实时行情统计信息
        
        Returns:
            统计信息字典
        """
        try:
            total_count = await self.col_fund_etf_spot.count_documents({})
            
            # 统计涨跌数量
            rise_count = await self.col_fund_etf_spot.count_documents({'涨跌幅': {'$gt': 0}})
            fall_count = await self.col_fund_etf_spot.count_documents({'涨跌幅': {'$lt': 0}})
            flat_count = total_count - rise_count - fall_count
            
            # 统计成交额TOP10
            pipeline_volume = [
                {
                    '$sort': {'成交额': -1}
                },
                {
                    '$limit': 10
                },
                {
                    '$project': {
                        'name': '$名称',
                        'code': '$代码',
                        'volume': '$成交额',
                        'price': '$最新价',
                        'change_pct': '$涨跌幅'
                    }
                }
            ]
            
            top_volume: List[Dict[str, Any]] = []
            async for doc in self.col_fund_etf_spot.aggregate(pipeline_volume):
                top_volume.append({
                    'name': doc.get('name'),
                    'code': doc.get('code'),
                    'volume': doc.get('volume'),
                    'price': doc.get('price'),
                    'change_pct': doc.get('change_pct')
                })
            
            # 统计涨跌幅TOP10
            pipeline_rise = [
                {
                    '$sort': {'涨跌幅': -1}
                },
                {
                    '$limit': 10
                },
                {
                    '$project': {
                        'name': '$名称',
                        'code': '$代码',
                        'change_pct': '$涨跌幅',
                        'price': '$最新价',
                        'volume': '$成交额'
                    }
                }
            ]
            
            top_gainers: List[Dict[str, Any]] = []
            async for doc in self.col_fund_etf_spot.aggregate(pipeline_rise):
                top_gainers.append({
                    'name': doc.get('name'),
                    'code': doc.get('code'),
                    'change_pct': doc.get('change_pct'),
                    'price': doc.get('price'),
                    'volume': doc.get('volume')
                })
            
            # 计算最新日期
            pipeline_date = [
                {
                    '$group': {
                        '_id': None,
                        'latest': {'$max': '$date'}
                    }
                }
            ]
            
            latest_date = None
            async for doc in self.col_fund_etf_spot.aggregate(pipeline_date):
                latest_date = doc.get('latest')
            
            # 统计基金类型分布（基于名称关键词分类）
            type_keywords = {
                '行业ETF': ['芯片', '半导体', '医药', '消费', '金融', '地产', '能源', '化工', '军工', '汽车', '通信', '传媒', '电子', '计算机', '机械', '电气', '建筑', '钢铁', '有色', '煤炭', '石油', '银行', '证券', '保险'],
                '宽基ETF': ['沪深300', '中证500', '创业板', '科创50', '上证50', '中证1000', '红利', '价值', '成长', '质量', '低波'],
                '主题ETF': ['新能源', '科技', '碳中和', '数字经济', '大数据', '人工智能', '5G', '物联网', '云计算', '智能', '创新', '转型'],
                '行业指数ETF': ['证券公司', '非银金融', '房地产', '国防军工', '食品饮料', '家用电器', '纺织服装', '农林牧渔'],
                '港股ETF': ['港股', '恒生', '香港', 'H股', 'HKEX'],
                '债券ETF': ['债', '国债', '地方债', '企业债', '可转债', '信用债'],
                '商品ETF': ['黄金', '白银', '原油', '商品', '有色金属', '贵金属'],
                '跨境ETF': ['美股', '纳斯达克', '标普', '德国', '法国', '日本', '印度', '越南', '全球'],
            }
            
            type_counts: Dict[str, int] = {}
            
            # 获取所有基金名称并分类
            async for doc in self.col_fund_etf_spot.find({}, {'名称': 1}):
                name = doc.get('名称', '')
                classified = False
                
                # 按关键词匹配类型
                for fund_type, keywords in type_keywords.items():
                    if any(keyword in name for keyword in keywords):
                        type_counts[fund_type] = type_counts.get(fund_type, 0) + 1
                        classified = True
                        break
                
                # 未匹配的归为其他类型
                if not classified:
                    type_counts['其他ETF'] = type_counts.get('其他ETF', 0) + 1
            
            # 转换为列表格式
            type_stats = [
                {'type': fund_type, 'count': count}
                for fund_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True)
            ]
            
            return {
                'total_count': total_count,
                'rise_count': rise_count,
                'fall_count': fall_count,
                'flat_count': flat_count,
                'top_volume': top_volume,
                'top_gainers': top_gainers,
                'latest_date': latest_date,
                'type_stats': type_stats
            }
        except Exception as e:
            logger.error(f"获取ETF基金实时行情统计失败: {e}", exc_info=True)
            raise
    
    async def save_fund_etf_spot_ths_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """
        保存同花顺ETF实时行情数据到MongoDB
        
        Args:
            df: 包含ETF实时行情的DataFrame
            progress_callback: 进度回调函数(current, total, percentage, message)
            
        Returns:
            保存的记录数
        """
        if df is None or df.empty:
            logger.warning("DataFrame为空，无数据需要保存")
            return 0
        
        try:
            # 清理数据：替换无效值
            df = df.replace([float('inf'), float('-inf')], None)
            df = df.where(pd.notna(df), None)
            
            # 准备批量操作
            ops = []
            total_count = len(df)
            batch_size = 500
            
            for idx, row in df.iterrows():
                # 获取基金代码和查询日期作为唯一标识
                fund_code = str(row['基金代码']).strip()
                query_date = str(row['查询日期']).strip() if pd.notna(row.get('查询日期')) else ''
                
                if not fund_code or not query_date:
                    continue
                
                # 构建文档
                doc = {
                    '序号': int(row['序号']) if pd.notna(row.get('序号')) else None,
                    '基金代码': fund_code,
                    '基金名称': str(row['基金名称']).strip() if pd.notna(row.get('基金名称')) else '',
                    '当前-单位净值': float(row['当前-单位净值']) if pd.notna(row.get('当前-单位净值')) else None,
                    '当前-累计净值': float(row['当前-累计净值']) if pd.notna(row.get('当前-累计净值')) else None,
                    '前一日-单位净值': float(row['前一日-单位净值']) if pd.notna(row.get('前一日-单位净值')) else None,
                    '前一日-累计净值': float(row['前一日-累计净值']) if pd.notna(row.get('前一日-累计净值')) else None,
                    '增长值': float(row['增长值']) if pd.notna(row.get('增长值')) else None,
                    '增长率': float(row['增长率']) if pd.notna(row.get('增长率')) else None,
                    '赎回状态': str(row['赎回状态']).strip() if pd.notna(row.get('赎回状态')) else '',
                    '申购状态': str(row['申购状态']).strip() if pd.notna(row.get('申购状态')) else '',
                    '最新-交易日': str(row['最新-交易日']).strip() if pd.notna(row.get('最新-交易日')) else '',
                    '最新-单位净值': float(row['最新-单位净值']) if pd.notna(row.get('最新-单位净值')) else None,
                    '最新-累计净值': float(row['最新-累计净值']) if pd.notna(row.get('最新-累计净值')) else None,
                    '基金类型': str(row['基金类型']).strip() if pd.notna(row.get('基金类型')) else '',
                    '查询日期': query_date,
                    'code': fund_code,
                    'date': query_date,
                    'source': 'akshare',
                    'endpoint': 'fund_etf_spot_ths',
                    'updated_at': datetime.now()
                }
                
                # 处理日期类型字段
                for field in ['查询日期', '最新-交易日', 'date']:
                    if field in doc and doc[field] and isinstance(doc[field], (date, datetime)):
                        doc[field] = doc[field].isoformat() if hasattr(doc[field], 'isoformat') else str(doc[field])
                
                # 添加到批量操作
                ops.append(
                    UpdateOne(
                        {'code': fund_code, 'date': query_date},
                        {'$set': doc},
                        upsert=True
                    )
                )
                
                # 批量执行
                if len(ops) >= batch_size:
                    result = await self.col_fund_etf_spot_ths.bulk_write(ops, ordered=False)
                    
                    if progress_callback:
                        current = idx + 1
                        percentage = int((current / total_count) * 100)
                        progress_callback(current, total_count, percentage, f"已保存 {current}/{total_count} 条数据")
                    
                    ops = []
            
            # 执行剩余操作
            saved_count = 0
            if ops:
                result = await self.col_fund_etf_spot_ths.bulk_write(ops, ordered=False)
                saved_count = result.upserted_count + result.modified_count
            
            if progress_callback:
                progress_callback(total_count, total_count, 100, f"完成！共保存 {total_count} 条数据")
            
            logger.info(f"成功保存 {total_count} 条同花顺ETF实时行情数据")
            return total_count
            
        except Exception as e:
            logger.error(f"保存同花顺ETF实时行情数据失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_etf_spot_ths_data(self) -> int:
        """
        清空同花顺ETF实时行情数据
        
        Returns:
            删除的记录数
        """
        try:
            result = await self.col_fund_etf_spot_ths.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条同花顺ETF实时行情数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空同花顺ETF实时行情数据失败: {e}", exc_info=True)
            raise
    
    async def get_fund_etf_spot_ths_stats(self) -> Dict[str, Any]:
        """
        获取同花顺ETF实时行情统计信息
        
        Returns:
            统计信息字典
        """
        try:
            # 总记录数
            total_count = await self.col_fund_etf_spot_ths.count_documents({})
            
            # 涨跌统计
            rise_count = await self.col_fund_etf_spot_ths.count_documents({'增长率': {'$gt': 0}})
            fall_count = await self.col_fund_etf_spot_ths.count_documents({'增长率': {'$lt': 0}})
            flat_count = await self.col_fund_etf_spot_ths.count_documents({'增长率': 0})
            
            # 基金类型分布
            type_pipeline = [
                {'$group': {'_id': '$基金类型', 'count': {'$sum': 1}}},
                {'$sort': {'count': -1}}
            ]
            type_stats = []
            async for doc in self.col_fund_etf_spot_ths.aggregate(type_pipeline):
                if doc['_id']:
                    type_stats.append({
                        'type': doc['_id'],
                        'count': doc['count']
                    })
            
            # 涨幅TOP10
            top_gainers = []
            cursor = self.col_fund_etf_spot_ths.find(
                {'增长率': {'$ne': None, '$gt': 0}},
                {'基金代码': 1, '基金名称': 1, '增长率': 1, '_id': 0}
            ).sort('增长率', -1).limit(10)
            
            async for doc in cursor:
                top_gainers.append({
                    'code': doc.get('基金代码'),
                    'name': doc.get('基金名称'),
                    'rate': doc.get('增长率')
                })
            
            # 跌幅TOP10
            top_losers = []
            cursor = self.col_fund_etf_spot_ths.find(
                {'增长率': {'$ne': None, '$lt': 0}},
                {'基金代码': 1, '基金名称': 1, '增长率': 1, '_id': 0}
            ).sort('增长率', 1).limit(10)
            
            async for doc in cursor:
                top_losers.append({
                    'code': doc.get('基金代码'),
                    'name': doc.get('基金名称'),
                    'rate': doc.get('增长率')
                })
            
            # 申赎状态统计
            purchase_pipeline = [
                {'$group': {'_id': '$申购状态', 'count': {'$sum': 1}}},
                {'$sort': {'count': -1}}
            ]
            purchase_stats = []
            async for doc in self.col_fund_etf_spot_ths.aggregate(purchase_pipeline):
                if doc['_id']:
                    purchase_stats.append({
                        'status': doc['_id'],
                        'count': doc['count']
                    })
            
            redeem_pipeline = [
                {'$group': {'_id': '$赎回状态', 'count': {'$sum': 1}}},
                {'$sort': {'count': -1}}
            ]
            redeem_stats = []
            async for doc in self.col_fund_etf_spot_ths.aggregate(redeem_pipeline):
                if doc['_id']:
                    redeem_stats.append({
                        'status': doc['_id'],
                        'count': doc['count']
                    })
            
            # 最新日期
            latest_date = None
            cursor = self.col_fund_etf_spot_ths.find(
                {'查询日期': {'$ne': None}},
                {'查询日期': 1, '_id': 0}
            ).sort('查询日期', -1).limit(1)
            
            async for doc in cursor:
                latest_date = doc.get('查询日期')
            
            return {
                'total_count': total_count,
                'rise_count': rise_count,
                'fall_count': fall_count,
                'flat_count': flat_count,
                'type_stats': type_stats,
                'top_gainers': top_gainers,
                'top_losers': top_losers,
                'purchase_status_stats': purchase_stats,
                'redeem_status_stats': redeem_stats,
                'latest_date': latest_date
            }
        except Exception as e:
            logger.error(f"获取同花顺ETF实时行情统计失败: {e}", exc_info=True)
            raise
    
    async def save_fund_lof_spot_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """
        保存LOF基金实时行情数据到MongoDB
        
        Args:
            df: 包含LOF基金实时行情的DataFrame
            progress_callback: 进度回调函数(current, total, percentage, message)
            
        Returns:
            保存的记录数
        """
        if df is None or df.empty:
            logger.warning("DataFrame为空，无数据需要保存")
            return 0
        
        try:
            # 清理数据：替换无效值
            df = df.replace([float('inf'), float('-inf')], None)
            df = df.where(pd.notna(df), None)
            
            # 准备批量操作
            ops = []
            total_count = len(df)
            batch_size = 500
            
            # 添加数据日期
            data_date = datetime.now().strftime('%Y-%m-%d')
            
            for idx, row in df.iterrows():
                # 获取基金代码作为唯一标识
                fund_code = str(row['代码']).strip()
                
                if not fund_code:
                    continue
                
                # 构建文档
                doc = {
                    '代码': fund_code,
                    '名称': str(row['名称']).strip() if pd.notna(row.get('名称')) else '',
                    '最新价': float(row['最新价']) if pd.notna(row.get('最新价')) else None,
                    '涨跌额': float(row['涨跌额']) if pd.notna(row.get('涨跌额')) else None,
                    '涨跌幅': float(row['涨跌幅']) if pd.notna(row.get('涨跌幅')) else None,
                    '成交量': float(row['成交量']) if pd.notna(row.get('成交量')) else None,
                    '成交额': float(row['成交额']) if pd.notna(row.get('成交额')) else None,
                    '开盘价': float(row['开盘价']) if pd.notna(row.get('开盘价')) else None,
                    '最高价': float(row['最高价']) if pd.notna(row.get('最高价')) else None,
                    '最低价': float(row['最低价']) if pd.notna(row.get('最低价')) else None,
                    '昨收': float(row['昨收']) if pd.notna(row.get('昨收')) else None,
                    '换手率': float(row['换手率']) if pd.notna(row.get('换手率')) else None,
                    '流通市值': int(row['流通市值']) if pd.notna(row.get('流通市值')) else None,
                    '总市值': int(row['总市值']) if pd.notna(row.get('总市值')) else None,
                    '数据日期': data_date,
                    'code': fund_code,
                    'date': data_date,
                    'source': 'akshare',
                    'endpoint': 'fund_lof_spot_em',
                    'updated_at': datetime.now()
                }
                
                # 添加到批量操作
                ops.append(
                    UpdateOne(
                        {'code': fund_code, 'date': data_date},
                        {'$set': doc},
                        upsert=True
                    )
                )
                
                # 批量执行
                if len(ops) >= batch_size:
                    result = await self.col_fund_lof_spot.bulk_write(ops, ordered=False)
                    
                    if progress_callback:
                        current = idx + 1
                        percentage = int((current / total_count) * 100)
                        progress_callback(current, total_count, percentage, f"已保存 {current}/{total_count} 条数据")
                    
                    ops = []
            
            # 执行剩余操作
            saved_count = 0
            if ops:
                result = await self.col_fund_lof_spot.bulk_write(ops, ordered=False)
                saved_count = result.upserted_count + result.modified_count
            
            if progress_callback:
                progress_callback(total_count, total_count, 100, f"完成！共保存 {total_count} 条数据")
            
            logger.info(f"成功保存 {total_count} 条LOF基金实时行情数据")
            return total_count
            
        except Exception as e:
            logger.error(f"保存LOF基金实时行情数据失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_lof_spot_data(self) -> int:
        """
        清空LOF基金实时行情数据
        
        Returns:
            删除的记录数
        """
        try:
            result = await self.col_fund_lof_spot.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条LOF基金实时行情数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空LOF基金实时行情数据失败: {e}", exc_info=True)
            raise
    
    async def get_fund_lof_spot_stats(self) -> Dict[str, Any]:
        """
        获取LOF基金实时行情统计信息
        
        Returns:
            统计信息字典
        """
        try:
            # 总记录数
            total_count = await self.col_fund_lof_spot.count_documents({})
            
            # 涨跌统计
            rise_count = await self.col_fund_lof_spot.count_documents({'涨跌幅': {'$gt': 0}})
            fall_count = await self.col_fund_lof_spot.count_documents({'涨跌幅': {'$lt': 0}})
            flat_count = await self.col_fund_lof_spot.count_documents({'涨跌幅': 0})
            
            # 成交额TOP10
            top_volume = []
            cursor = self.col_fund_lof_spot.find(
                {'成交额': {'$ne': None}},
                {'代码': 1, '名称': 1, '成交额': 1, '_id': 0}
            ).sort('成交额', -1).limit(10)
            
            async for doc in cursor:
                top_volume.append({
                    'code': doc.get('代码'),
                    'name': doc.get('名称'),
                    'amount': doc.get('成交额')
                })
            
            # 涨幅TOP10
            top_gainers = []
            cursor = self.col_fund_lof_spot.find(
                {'涨跌幅': {'$ne': None, '$gt': 0}},
                {'代码': 1, '名称': 1, '涨跌幅': 1, '_id': 0}
            ).sort('涨跌幅', -1).limit(10)
            
            async for doc in cursor:
                top_gainers.append({
                    'code': doc.get('代码'),
                    'name': doc.get('名称'),
                    'rate': doc.get('涨跌幅')
                })
            
            # 跌幅TOP10
            top_losers = []
            cursor = self.col_fund_lof_spot.find(
                {'涨跌幅': {'$ne': None, '$lt': 0}},
                {'代码': 1, '名称': 1, '涨跌幅': 1, '_id': 0}
            ).sort('涨跌幅', 1).limit(10)
            
            async for doc in cursor:
                top_losers.append({
                    'code': doc.get('代码'),
                    'name': doc.get('名称'),
                    'rate': doc.get('涨跌幅')
                })
            
            # 市值分布统计（按市值范围分组）
            market_cap_ranges = [
                {'name': '10亿以下', 'min': 0, 'max': 1000000000},
                {'name': '10-50亿', 'min': 1000000000, 'max': 5000000000},
                {'name': '50-100亿', 'min': 5000000000, 'max': 10000000000},
                {'name': '100亿以上', 'min': 10000000000, 'max': float('inf')}
            ]
            
            market_cap_stats = []
            for range_item in market_cap_ranges:
                count = await self.col_fund_lof_spot.count_documents({
                    '总市值': {
                        '$gte': range_item['min'],
                        '$lt': range_item['max'] if range_item['max'] != float('inf') else 999999999999
                    }
                })
                if count > 0:
                    market_cap_stats.append({
                        'range': range_item['name'],
                        'count': count
                    })
            
            # 最新日期
            latest_date = None
            cursor = self.col_fund_lof_spot.find(
                {'数据日期': {'$ne': None}},
                {'数据日期': 1, '_id': 0}
            ).sort('数据日期', -1).limit(1)
            
            async for doc in cursor:
                latest_date = doc.get('数据日期')
            
            return {
                'total_count': total_count,
                'rise_count': rise_count,
                'fall_count': fall_count,
                'flat_count': flat_count,
                'top_volume': top_volume,
                'top_gainers': top_gainers,
                'top_losers': top_losers,
                'market_cap_stats': market_cap_stats,
                'latest_date': latest_date
            }
        except Exception as e:
            logger.error(f"获取LOF基金实时行情统计失败: {e}", exc_info=True)
            raise
    
    async def save_fund_spot_sina_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存基金实时行情-新浪数据到 MongoDB。

        使用 `code + date` 作为唯一键进行 upsert，结构与 LOF 实时行情保持一致，
        并通过 `UpdateOne` 构造合法的 bulk_write 请求。

        Args:
            df: 包含基金实时行情的 DataFrame
            progress_callback: 进度回调函数 (current, total, percentage, message)

        Returns:
            保存的记录数
        """
        if df is None or df.empty:
            logger.warning("基金实时行情-新浪数据为空")
            return 0

        try:
            logger.info(f"开始保存基金实时行情-新浪数据，共 {len(df)} 条")

            # 拷贝一份，避免修改原始数据
            df = df.copy()

            # 添加元数据
            current_date = datetime.now().strftime("%Y-%m-%d")
            df["数据日期"] = current_date
            # 部分场景下可能没有 code 列，这里显式从 代码 衍生
            if "code" not in df.columns:
                df["code"] = df["代码"].astype(str)
            df["date"] = current_date
            df["source"] = "akshare"
            df["endpoint"] = "fund_etf_category_sina"
            df["updated_at"] = datetime.now()

            # 清理数据：将 NaN 和 Infinity 替换为 None，避免 JSON 序列化问题
            df = df.replace([float("inf"), float("-inf")], None)
            df = df.where(pd.notnull(df), None)

            batch_size = 500
            total_count = len(df)
            total_saved = 0

            for batch_start in range(0, total_count, batch_size):
                batch_end = min(batch_start + batch_size, total_count)
                batch_df = df.iloc[batch_start:batch_end]

                ops = []
                for _, row in batch_df.iterrows():
                    record = row.to_dict()

                    code = str(record.get("code") or record.get("代码") or "").strip()
                    if not code:
                        continue

                    date_value = record.get("date") or current_date
                    record["code"] = code
                    record["date"] = date_value

                    ops.append(
                        UpdateOne(
                            {"code": code, "date": date_value},
                            {"$set": record},
                            upsert=True,
                        )
                    )

                if ops:
                    result = await self.col_fund_spot_sina.bulk_write(ops, ordered=False)
                    saved_count = (result.upserted_count or 0) + (result.modified_count or 0)
                    total_saved += saved_count

                # 更新进度
                if progress_callback:
                    current = batch_end
                    percentage = int((current / total_count) * 100)
                    progress_callback(current, total_count, percentage, f"已保存 {current}/{total_count} 条数据")

            logger.info(f"基金实时行情-新浪数据保存完成，共保存 {total_saved} 条")
            return total_saved

        except Exception as e:
            logger.error(f"保存基金实时行情-新浪数据失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_spot_sina_data(self) -> int:
        """清空基金实时行情-新浪数据"""
        try:
            result = await self.col_fund_spot_sina.delete_many({})
            logger.info(f"清空基金实时行情-新浪数据成功，删除 {result.deleted_count} 条")
            return result.deleted_count
        except Exception as e:
            logger.error(f"清空基金实时行情-新浪数据失败: {e}", exc_info=True)
            raise
    
    async def get_fund_spot_sina_stats(self) -> dict:
        """
        获取基金实时行情-新浪统计信息
        
        Returns:
            统计信息字典
        """
        try:
            # 总数
            total_count = await self.col_fund_spot_sina.count_documents({})
            
            # 涨跌统计
            rise_count = await self.col_fund_spot_sina.count_documents({
                "涨跌幅": {"$gt": 0}
            })
            fall_count = await self.col_fund_spot_sina.count_documents({
                "涨跌幅": {"$lt": 0}
            })
            flat_count = await self.col_fund_spot_sina.count_documents({
                "涨跌幅": 0
            })
            
            # 基金类型分布统计
            type_pipeline = [
                {
                    "$group": {
                        "_id": "$基金类型",
                        "count": {"$sum": 1}
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "type": "$_id",
                        "count": 1
                    }
                },
                {"$sort": {"count": -1}}
            ]
            type_stats = await self.col_fund_spot_sina.aggregate(type_pipeline).to_list(None)
            
            # 成交额TOP10
            volume_pipeline = [
                {"$match": {"成交额": {"$ne": None}}},
                {"$sort": {"成交额": -1}},
                {"$limit": 10},
                {
                    "$project": {
                        "_id": 0,
                        "code": "$代码",
                        "name": "$名称",
                        "amount": "$成交额",
                        "type": "$基金类型"
                    }
                }
            ]
            top_volume = await self.col_fund_spot_sina.aggregate(volume_pipeline).to_list(None)
            
            # 涨幅TOP10
            gainers_pipeline = [
                {"$match": {"涨跌幅": {"$ne": None, "$gt": 0}}},
                {"$sort": {"涨跌幅": -1}},
                {"$limit": 10},
                {
                    "$project": {
                        "_id": 0,
                        "code": "$代码",
                        "name": "$名称",
                        "rate": "$涨跌幅",
                        "type": "$基金类型"
                    }
                }
            ]
            top_gainers = await self.col_fund_spot_sina.aggregate(gainers_pipeline).to_list(None)
            
            # 跌幅TOP10
            losers_pipeline = [
                {"$match": {"涨跌幅": {"$ne": None, "$lt": 0}}},
                {"$sort": {"涨跌幅": 1}},
                {"$limit": 10},
                {
                    "$project": {
                        "_id": 0,
                        "code": "$代码",
                        "name": "$名称",
                        "rate": "$涨跌幅",
                        "type": "$基金类型"
                    }
                }
            ]
            top_losers = await self.col_fund_spot_sina.aggregate(losers_pipeline).to_list(None)
            
            # 最新数据日期
            latest_doc = await self.col_fund_spot_sina.find_one(
                {},
                sort=[("updated_at", -1)]
            )
            latest_date = latest_doc.get("数据日期") if latest_doc else None
            
            return {
                'total_count': total_count,
                'rise_count': rise_count,
                'fall_count': fall_count,
                'flat_count': flat_count,
                'type_stats': type_stats,
                'top_volume': top_volume,
                'top_gainers': top_gainers,
                'top_losers': top_losers,
                'latest_date': latest_date
            }
        except Exception as e:
            logger.error(f"获取基金实时行情-新浪统计失败: {e}", exc_info=True)
            return {
                'total_count': 0,
                'rise_count': 0,
                'fall_count': 0,
                'flat_count': 0,
                'latest_date': None
            }

    async def save_fund_etf_hist_min_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存 ETF 基金分时行情数据到 fund_etf_hist_min_em 集合。

        使用 `code + time + period + adjust` 作为唯一键进行 upsert。

        Args:
            df: 包含 ETF 分时行情数据的 DataFrame，至少需包含 `代码` 和 `时间` 列。
            progress_callback: 进度回调函数 (current, total, percentage, message)

        Returns:
            实际写入(新增+更新)的记录数
        """
        if df is None or df.empty:
            logger.warning("ETF 分时行情数据为空，无需保存")
            return 0

        try:
            # 拷贝一份，避免修改外部 DataFrame
            df = df.copy()

            # 统一清理无效数值
            df = df.replace([float("inf"), float("-inf")], None)
            df = df.where(pd.notnull(df), None)

            total_count = len(df)
            batch_size = 1000  # 达到1000条保存一次，退出时不足1000条也保存
            total_saved = 0

            for batch_start in range(0, total_count, batch_size):
                batch_end = min(batch_start + batch_size, total_count)
                batch_df = df.iloc[batch_start:batch_end]

                ops: List[UpdateOne] = []

                for _, row in batch_df.iterrows():
                    record = row.to_dict()

                    # 代码
                    code = str(record.get("代码") or record.get("code") or "").strip()
                    if not code:
                        continue

                    # 时间 -> 统一为字符串，并派生 date
                    time_val = record.get("时间") or record.get("time") or record.get("datetime")
                    if time_val is None or (isinstance(time_val, float) and pd.isna(time_val)):
                        continue

                    if isinstance(time_val, pd.Timestamp):
                        time_str = time_val.strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        time_str = str(time_val).strip()

                    if not time_str:
                        continue

                    date_str = time_str[:10]

                    # 周期与复权方式（默认 5 分钟、后复权）
                    period = str(record.get("period") or "5")
                    adjust = str(record.get("adjust") or "hfq")

                    # 写回规范化字段
                    record["代码"] = code
                    record["时间"] = time_str
                    record["code"] = code
                    record["time"] = time_str
                    record["date"] = date_str
                    record["period"] = period
                    record["adjust"] = adjust
                    record["source"] = record.get("source") or "akshare"
                    record["endpoint"] = record.get("endpoint") or "fund_etf_hist_min_em"
                    record["updated_at"] = datetime.now()

                    # 构造 upsert 操作
                    ops.append(
                        UpdateOne(
                            {"code": code, "time": time_str, "period": period, "adjust": adjust},
                            {"$set": record},
                            upsert=True,
                        )
                    )

                if ops:
                    result = await self.col_fund_etf_hist_min_em.bulk_write(ops, ordered=False)
                    saved_count = (result.upserted_count or 0) + (result.modified_count or 0)
                    total_saved += saved_count

                # 进度回调
                if progress_callback:
                    current = batch_end
                    percentage = int((current / total_count) * 100)
                    progress_callback(
                        current,
                        total_count,
                        percentage,
                        f"已保存 {current}/{total_count} 条 ETF 分时行情数据",
                    )

            logger.info(f"成功保存 {total_saved}/{total_count} 条 ETF 分时行情数据")
            return total_saved

        except Exception as e:
            logger.error(f"保存 ETF 分时行情数据失败: {e}", exc_info=True)
            raise

    async def clear_fund_etf_hist_min_data(self) -> int:
        """清空 ETF 分时行情数据集合。"""
        try:
            result = await self.col_fund_etf_hist_min_em.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条 ETF 分时行情数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空 ETF 分时行情数据失败: {e}", exc_info=True)
            raise

    async def get_fund_etf_hist_min_stats(self) -> Dict[str, Any]:
        """获取 ETF 分时行情统计信息。

        当前提供：
        - total_count: 总记录数
        - code_stats: 按代码分组的记录数
        - earliest_time / latest_time: 最早和最晚的时间戳
        """
        try:
            total_count = await self.col_fund_etf_hist_min_em.count_documents({})

            # 按代码分组统计数量
            code_stats: List[Dict[str, Any]] = []
            pipeline_codes = [
                {"$group": {"_id": "$code", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
            ]
            async for doc in self.col_fund_etf_hist_min_em.aggregate(pipeline_codes):
                if doc.get("_id"):
                    code_stats.append({"code": doc["_id"], "count": doc["count"]})

            # 计算时间范围
            earliest_time = None
            latest_time = None
            pipeline_time = [
                {
                    "$group": {
                        "_id": None,
                        "earliest": {"$min": "$time"},
                        "latest": {"$max": "$time"},
                    }
                }
            ]

            async for doc in self.col_fund_etf_hist_min_em.aggregate(pipeline_time):
                earliest_time = doc.get("earliest")
                latest_time = doc.get("latest")

            return {
                "total_count": total_count,
                "code_stats": code_stats,
                "earliest_time": earliest_time,
                "latest_time": latest_time,
            }
        except Exception as e:
            logger.error(f"获取 ETF 分时行情统计失败: {e}", exc_info=True)
            return {
                "total_count": 0,
                "code_stats": [],
                "earliest_time": None,
                "latest_time": None,
            }

    async def save_fund_lof_hist_min_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存 LOF 基金分时行情数据到 fund_lof_hist_min_em 集合。

        使用 `code + time + period + adjust` 作为唯一键进行 upsert。

        Args:
            df: 包含 LOF 分时行情数据的 DataFrame，至少需包含 `代码` 和 `时间` 列。
            progress_callback: 进度回调函数 (current, total, percentage, message)

        Returns:
            实际写入(新增+更新)的记录数
        """
        if df is None or df.empty:
            logger.warning("LOF 分时行情数据为空，无需保存")
            return 0

        try:
            # 拷贝一份，避免修改外部 DataFrame
            df = df.copy()

            # 统一清理无效数值
            df = df.replace([float("inf"), float("-inf")], None)
            df = df.where(pd.notnull(df), None)

            total_count = len(df)
            batch_size = 1000  # 达到1000条保存一次，退出时不足1000条也保存
            total_saved = 0

            for batch_start in range(0, total_count, batch_size):
                batch_end = min(batch_start + batch_size, total_count)
                batch_df = df.iloc[batch_start:batch_end]

                ops: List[UpdateOne] = []

                for _, row in batch_df.iterrows():
                    record = row.to_dict()

                    # 代码
                    code = str(record.get("代码") or record.get("code") or "").strip()
                    if not code:
                        continue

                    # 时间 -> 统一为字符串，并派生 date
                    time_val = record.get("时间") or record.get("time") or record.get("datetime")
                    if time_val is None or (isinstance(time_val, float) and pd.isna(time_val)):
                        continue

                    if isinstance(time_val, pd.Timestamp):
                        time_str = time_val.strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        time_str = str(time_val).strip()

                    if not time_str:
                        continue

                    date_str = time_str[:10]

                    # 周期与复权方式（默认 5 分钟、后复权）
                    period = str(record.get("period") or "5")
                    adjust = str(record.get("adjust") or "hfq")

                    # 写回规范化字段
                    record["代码"] = code
                    record["时间"] = time_str
                    record["code"] = code
                    record["time"] = time_str
                    record["date"] = date_str
                    record["period"] = period
                    record["adjust"] = adjust
                    record["source"] = record.get("source") or "akshare"
                    record["endpoint"] = record.get("endpoint") or "fund_lof_hist_min_em"
                    record["updated_at"] = datetime.now()

                    # 构造 upsert 操作
                    ops.append(
                        UpdateOne(
                            {"code": code, "time": time_str, "period": period, "adjust": adjust},
                            {"$set": record},
                            upsert=True,
                        )
                    )

                if ops:
                    result = await self.col_fund_lof_hist_min_em.bulk_write(ops, ordered=False)
                    saved_count = (result.upserted_count or 0) + (result.modified_count or 0)
                    total_saved += saved_count

                # 进度回调
                if progress_callback:
                    current = batch_end
                    percentage = int((current / total_count) * 100)
                    progress_callback(
                        current,
                        total_count,
                        percentage,
                        f"已保存 {current}/{total_count} 条 LOF 分时行情数据",
                    )

            logger.info(f"成功保存 {total_saved}/{total_count} 条 LOF 分时行情数据")
            return total_saved

        except Exception as e:
            logger.error(f"保存 LOF 分时行情数据失败: {e}", exc_info=True)
            raise

    async def clear_fund_lof_hist_min_data(self) -> int:
        """清空 LOF 分时行情数据集合。"""
        try:
            result = await self.col_fund_lof_hist_min_em.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条 LOF 分时行情数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空 LOF 分时行情数据失败: {e}", exc_info=True)
            raise

    async def get_fund_lof_hist_min_stats(self) -> Dict[str, Any]:
        """获取 LOF 分时行情统计信息。

        当前提供：
        - total_count: 总记录数
        - code_stats: 按代码分组的记录数
        - earliest_time / latest_time: 最早和最晚的时间戳
        """
        try:
            total_count = await self.col_fund_lof_hist_min_em.count_documents({})

            # 按代码分组统计数量
            code_stats: List[Dict[str, Any]] = []
            pipeline_codes = [
                {"$group": {"_id": "$code", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
            ]
            async for doc in self.col_fund_lof_hist_min_em.aggregate(pipeline_codes):
                if doc.get("_id"):
                    code_stats.append({"code": doc["_id"], "count": doc["count"]})

            # 计算时间范围
            earliest_time = None
            latest_time = None
            pipeline_time = [
                {
                    "$group": {
                        "_id": None,
                        "earliest": {"$min": "$time"},
                        "latest": {"$max": "$time"},
                    }
                }
            ]

            async for doc in self.col_fund_lof_hist_min_em.aggregate(pipeline_time):
                earliest_time = doc.get("earliest")
                latest_time = doc.get("latest")

            return {
                "total_count": total_count,
                "code_stats": code_stats,
                "earliest_time": earliest_time,
                "latest_time": latest_time,
            }
        except Exception as e:
            logger.error(f"获取 LOF 分时行情统计失败: {e}", exc_info=True)
            return {
                "total_count": 0,
                "code_stats": [],
                "earliest_time": None,
                "latest_time": None,
            }

    async def save_fund_etf_hist_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存 ETF 基金历史行情数据到 fund_etf_hist_em 集合。

        使用 `code + date + period + adjust` 作为唯一键进行 upsert。

        Args:
            df: 包含 ETF 历史行情数据的 DataFrame，至少需包含 `代码` 和 `日期` 列。
            progress_callback: 进度回调函数 (current, total, percentage, message)

        Returns:
            实际写入(新增+更新)的记录数
        """
        if df is None or df.empty:
            logger.warning("ETF 历史行情数据为空，无需保存")
            return 0

        try:
            # 拷贝一份，避免修改外部 DataFrame
            df = df.copy()

            # 统一清理无效数值
            df = df.replace([float("inf"), float("-inf")], None)
            df = df.where(pd.notnull(df), None)

            total_count = len(df)
            batch_size = 500
            total_saved = 0

            for batch_start in range(0, total_count, batch_size):
                batch_end = min(batch_start + batch_size, total_count)
                batch_df = df.iloc[batch_start:batch_end]

                ops: List[UpdateOne] = []

                for _, row in batch_df.iterrows():
                    record = row.to_dict()

                    # 代码
                    code = str(record.get("代码") or record.get("code") or "").strip()
                    if not code:
                        continue

                    # 日期 -> 统一为字符串
                    date_val = record.get("日期") or record.get("date")
                    if date_val is None or (isinstance(date_val, float) and pd.isna(date_val)):
                        continue

                    if isinstance(date_val, pd.Timestamp):
                        date_str = date_val.strftime("%Y-%m-%d")
                    else:
                        date_str = str(date_val).strip()[:10]

                    if not date_str:
                        continue

                    # 周期与复权方式（默认 daily、后复权）
                    period = str(record.get("period") or "daily")
                    adjust = str(record.get("adjust") or "hfq")

                    # 写回规范化字段
                    record["代码"] = code
                    record["日期"] = date_str
                    record["code"] = code
                    record["date"] = date_str
                    record["period"] = period
                    record["adjust"] = adjust
                    record["source"] = record.get("source") or "akshare"
                    record["endpoint"] = record.get("endpoint") or "fund_etf_hist_em"
                    record["updated_at"] = datetime.now()

                    # 构造 upsert 操作
                    ops.append(
                        UpdateOne(
                            {"code": code, "date": date_str, "period": period, "adjust": adjust},
                            {"$set": record},
                            upsert=True,
                        )
                    )

                if ops:
                    result = await self.col_fund_etf_hist_em.bulk_write(ops, ordered=False)
                    saved_count = (result.upserted_count or 0) + (result.modified_count or 0)
                    total_saved += saved_count

                # 进度回调
                if progress_callback:
                    current = batch_end
                    percentage = int((current / total_count) * 100)
                    progress_callback(
                        current,
                        total_count,
                        percentage,
                        f"已保存 {current}/{total_count} 条 ETF 历史行情数据",
                    )

            logger.info(f"成功保存 {total_saved}/{total_count} 条 ETF 历史行情数据")
            return total_saved

        except Exception as e:
            logger.error(f"保存 ETF 历史行情数据失败: {e}", exc_info=True)
            raise

    async def clear_fund_etf_hist_data(self) -> int:
        """清空 ETF 历史行情数据集合。"""
        try:
            result = await self.col_fund_etf_hist_em.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条 ETF 历史行情数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空 ETF 历史行情数据失败: {e}", exc_info=True)
            raise

    async def get_fund_etf_hist_stats(self) -> Dict[str, Any]:
        """获取 ETF 历史行情统计信息。

        Returns:
            统计信息字典，包含：
            - total_count: 总记录数
            - code_stats: 各代码的统计 [{code, count}, ...]
            - earliest_date: 最早日期
            - latest_date: 最新日期
        """
        try:
            # 总记录数
            total_count = await self.col_fund_etf_hist_em.count_documents({})

            # 各代码统计
            code_pipeline = [
                {"$group": {"_id": "$code", "count": {"$sum": 1}}},
                {"$project": {"code": "$_id", "count": 1, "_id": 0}},
                {"$sort": {"count": -1}},
                {"$limit": 100},
            ]
            code_stats = await self.col_fund_etf_hist_em.aggregate(code_pipeline).to_list(100)

            # 最早和最新日期
            earliest_date = None
            latest_date = None

            if total_count > 0:
                earliest_doc = (
                    await self.col_fund_etf_hist_em.find({}, {"date": 1})
                    .sort("date", 1)
                    .limit(1)
                    .to_list(1)
                )
                if earliest_doc:
                    earliest_date = earliest_doc[0].get("date")

                latest_doc = (
                    await self.col_fund_etf_hist_em.find({}, {"date": 1})
                    .sort("date", -1)
                    .limit(1)
                    .to_list(1)
                )
                if latest_doc:
                    latest_date = latest_doc[0].get("date")

            result = {
                "total_count": total_count,
                "code_stats": code_stats,
                "earliest_date": earliest_date,
                "latest_date": latest_date,
            }

            logger.debug(f"ETF 历史行情统计: {result}")
            return result

        except Exception as e:
            logger.error(f"获取 ETF 历史行情统计失败: {e}", exc_info=True)
            return {
                "total_count": 0,
                "code_stats": [],
                "earliest_date": None,
                "latest_date": None,
            }

    async def save_fund_lof_hist_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存 LOF 基金历史行情数据到 fund_lof_hist_em 集合。

        使用 `code + date + period + adjust` 作为唯一键进行 upsert。

        Args:
            df: 包含 LOF 历史行情数据的 DataFrame，至少需包含 `代码` 和 `日期` 列。
            progress_callback: 进度回调函数 (current, total, percentage, message)

        Returns:
            实际写入(新增+更新)的记录数
        """
        if df is None or df.empty:
            logger.warning("LOF 历史行情数据为空，无需保存")
            return 0

        try:
            # 拷贝一份，避免修改外部 DataFrame
            df = df.copy()

            # 统一清理无效数值
            df = df.replace([float("inf"), float("-inf")], None)
            df = df.where(pd.notnull(df), None)

            total_count = len(df)
            batch_size = 500
            total_saved = 0

            for batch_start in range(0, total_count, batch_size):
                batch_end = min(batch_start + batch_size, total_count)
                batch_df = df.iloc[batch_start:batch_end]

                ops: List[UpdateOne] = []

                for _, row in batch_df.iterrows():
                    record = row.to_dict()

                    # 代码
                    code = str(record.get("代码") or record.get("code") or "").strip()
                    if not code:
                        continue

                    # 日期 -> 统一为字符串
                    date_val = record.get("日期") or record.get("date")
                    if date_val is None or (isinstance(date_val, float) and pd.isna(date_val)):
                        continue

                    if isinstance(date_val, pd.Timestamp):
                        date_str = date_val.strftime("%Y-%m-%d")
                    else:
                        date_str = str(date_val).strip()[:10]

                    if not date_str:
                        continue

                    # 周期与复权方式（默认 daily、后复权）
                    period = str(record.get("period") or "daily")
                    adjust = str(record.get("adjust") or "hfq")

                    # 写回规范化字段
                    record["代码"] = code
                    record["日期"] = date_str
                    record["code"] = code
                    record["date"] = date_str
                    record["period"] = period
                    record["adjust"] = adjust
                    record["source"] = record.get("source") or "akshare"
                    record["endpoint"] = record.get("endpoint") or "fund_lof_hist_em"
                    record["updated_at"] = datetime.now()

                    # 构造 upsert 操作
                    ops.append(
                        UpdateOne(
                            {"code": code, "date": date_str, "period": period, "adjust": adjust},
                            {"$set": record},
                            upsert=True,
                        )
                    )

                if ops:
                    result = await self.col_fund_lof_hist_em.bulk_write(ops, ordered=False)
                    saved_count = (result.upserted_count or 0) + (result.modified_count or 0)
                    total_saved += saved_count

                # 进度回调
                if progress_callback:
                    current = batch_end
                    percentage = int((current / total_count) * 100)
                    progress_callback(
                        current,
                        total_count,
                        percentage,
                        f"已保存 {current}/{total_count} 条 LOF 历史行情数据",
                    )

            logger.info(f"成功保存 {total_saved}/{total_count} 条 LOF 历史行情数据")
            return total_saved

        except Exception as e:
            logger.error(f"保存 LOF 历史行情数据失败: {e}", exc_info=True)
            raise

    async def clear_fund_lof_hist_data(self) -> int:
        """清空 LOF 历史行情数据集合。"""
        try:
            result = await self.col_fund_lof_hist_em.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条 LOF 历史行情数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空 LOF 历史行情数据失败: {e}", exc_info=True)
            raise

    async def get_fund_lof_hist_stats(self) -> Dict[str, Any]:
        """获取 LOF 历史行情统计信息。

        Returns:
            统计信息字典，包含：
            - total_count: 总记录数
            - code_stats: 各代码的统计 [{code, count}, ...]
            - earliest_date: 最早日期
            - latest_date: 最新日期
        """
        try:
            # 总记录数
            total_count = await self.col_fund_lof_hist_em.count_documents({})

            # 各代码统计
            code_pipeline = [
                {"$group": {"_id": "$code", "count": {"$sum": 1}}},
                {"$project": {"code": "$_id", "count": 1, "_id": 0}},
                {"$sort": {"count": -1}},
                {"$limit": 100},
            ]
            code_stats = await self.col_fund_lof_hist_em.aggregate(code_pipeline).to_list(100)

            # 最早和最新日期
            earliest_date = None
            latest_date = None

            if total_count > 0:
                earliest_doc = (
                    await self.col_fund_lof_hist_em.find({}, {"date": 1})
                    .sort("date", 1)
                    .limit(1)
                    .to_list(1)
                )
                if earliest_doc:
                    earliest_date = earliest_doc[0].get("date")

                latest_doc = (
                    await self.col_fund_lof_hist_em.find({}, {"date": 1})
                    .sort("date", -1)
                    .limit(1)
                    .to_list(1)
                )
                if latest_doc:
                    latest_date = latest_doc[0].get("date")

            result = {
                "total_count": total_count,
                "code_stats": code_stats,
                "earliest_date": earliest_date,
                "latest_date": latest_date,
            }

            logger.debug(f"LOF 历史行情统计: {result}")
            return result

        except Exception as e:
            logger.error(f"获取 LOF 历史行情统计失败: {e}", exc_info=True)
            return {
                "total_count": 0,
                "code_stats": [],
                "earliest_date": None,
                "latest_date": None,
            }

    async def save_fund_hist_sina_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存新浪基金历史行情数据

        Args:
            df: 包含历史行情数据的 DataFrame，必须包含 date, open, high, low, close, volume 和代码字段
            progress_callback: 进度回调函数

        Returns:
            保存的记录数
        """
        if df is None or df.empty:
            logger.warning("新浪基金历史行情数据为空，无需保存")
            return 0

        try:
            df = df.copy()

            # 字段映射和规范化
            field_mapping = {
                "date": "date",
                "日期": "date",
                "open": "open",
                "开盘": "open",
                "high": "high",
                "最高": "high",
                "low": "low",
                "最低": "low",
                "close": "close",
                "收盘": "close",
                "volume": "volume",
                "成交量": "volume",
                "代码": "code",
                "code": "code",
            }

            # 重命名列
            df = df.rename(columns=field_mapping)

            # 检查必需字段
            required_fields = ["date", "open", "high", "low", "close", "volume", "code"]
            missing = [f for f in required_fields if f not in df.columns]
            if missing:
                logger.error(f"缺少必需字段: {missing}")
                return 0

            # 数据清理：处理无效数值（inf、NaN）
            numeric_fields = ["open", "high", "low", "close", "volume"]
            for field in numeric_fields:
                if field in df.columns:
                    df[field] = pd.to_numeric(df[field], errors="coerce")
                    df[field] = df[field].replace([float("inf"), float("-inf")], None)

            # 删除关键字段为空的行
            df = df.dropna(subset=["date", "code"])

            # 日期格式转换
            if df["date"].dtype == "object":
                try:
                    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
                except Exception as e:
                    logger.warning(f"日期格式转换失败: {e}")

            ops = []
            total = len(df)

            for idx, row in df.iterrows():
                code = str(row.get("code", "")).strip()
                date_str = str(row.get("date", "")).strip()

                if not code or not date_str:
                    continue

                record = {
                    "code": code,
                    "date": date_str,
                    "open": float(row["open"]) if pd.notna(row.get("open")) else None,
                    "high": float(row["high"]) if pd.notna(row.get("high")) else None,
                    "low": float(row["low"]) if pd.notna(row.get("low")) else None,
                    "close": float(row["close"]) if pd.notna(row.get("close")) else None,
                    "volume": int(row["volume"]) if pd.notna(row.get("volume")) else None,
                }

                # 唯一键：code + date
                ops.append(
                    UpdateOne(
                        {"code": code, "date": date_str},
                        {"$set": record},
                        upsert=True,
                    )
                )

                # 进度回调
                if progress_callback and (idx + 1) % 100 == 0:
                    await progress_callback(idx + 1, total)

            if not ops:
                logger.warning("没有有效数据可保存")
                return 0

            result = await self.col_fund_hist_sina.bulk_write(ops, ordered=False)
            saved_count = (result.upserted_count or 0) + (result.modified_count or 0)

            logger.info(f"成功保存 {saved_count} 条新浪基金历史行情数据")
            return saved_count

        except Exception as e:
            logger.error(f"保存新浪基金历史行情数据失败: {e}", exc_info=True)
            raise

    async def clear_fund_hist_sina_data(self) -> int:
        """清空新浪基金历史行情数据

        Returns:
            删除的记录数
        """
        try:
            result = await self.col_fund_hist_sina.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条新浪基金历史行情数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空新浪基金历史行情数据失败: {e}", exc_info=True)
            raise

    async def get_fund_hist_sina_stats(self) -> Dict[str, Any]:
        """获取新浪基金历史行情统计信息

        Returns:
            统计信息字典，包括总数、各代码记录数、最早/最新日期
        """
        try:
            total_count = await self.col_fund_hist_sina.count_documents({})

            # 按代码统计记录数（Top 100）
            code_pipeline = [
                {"$group": {"_id": "$code", "count": {"$sum": 1}}},
                {"$project": {"code": "$_id", "count": 1, "_id": 0}},
                {"$sort": {"count": -1}},
                {"$limit": 100},
            ]
            code_stats = await self.col_fund_hist_sina.aggregate(code_pipeline).to_list(100)

            # 获取最早和最新日期
            earliest_doc = (
                await self.col_fund_hist_sina.find({}, {"date": 1})
                .sort("date", 1)
                .limit(1)
                .to_list(1)
            )
            latest_doc = (
                await self.col_fund_hist_sina.find({}, {"date": 1})
                .sort("date", -1)
                .limit(1)
                .to_list(1)
            )

            earliest_date = earliest_doc[0]["date"] if earliest_doc else None
            latest_date = latest_doc[0]["date"] if latest_doc else None

            result = {
                "total_count": total_count,
                "code_stats": code_stats,
                "earliest_date": earliest_date,
                "latest_date": latest_date,
            }

            logger.debug(f"新浪基金历史行情统计: {result}")
            return result

        except Exception as e:
            logger.error(f"获取新浪基金历史行情统计失败: {e}", exc_info=True)
            return {
                "total_count": 0,
                "code_stats": [],
                "earliest_date": None,
                "latest_date": None,
            }

    async def save_fund_open_fund_daily_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存开放式基金实时行情数据

        Args:
            df: 包含开放式基金实时行情的 DataFrame
            progress_callback: 进度回调函数

        Returns:
            保存的记录数
        """
        if df is None or df.empty:
            logger.warning("开放式基金实时行情数据为空，无需保存")
            return 0

        try:
            df = df.copy()

            # 从列名中提取日期（列名格式如 "2024-01-01-单位净值"）
            date_str = None
            for col in df.columns:
                if "-单位净值" in col:
                    # 提取日期部分
                    date_str = col.split("-单位净值")[0]
                    break

            if not date_str:
                # 如果没有找到日期，使用当前日期
                from datetime import datetime

                date_str = datetime.now().strftime("%Y-%m-%d")
                logger.warning(f"未从列名中找到日期，使用当前日期: {date_str}")

            # 字段映射
            field_mapping = {
                "基金代码": "fund_code",
                "基金简称": "fund_name",
                f"{date_str}-单位净值": "unit_net_value",
                f"{date_str}-累计净值": "cumulative_net_value",
                f"{date_str}-前交易日-单位净值": "prev_unit_net_value",
                f"{date_str}-前交易日-累计净值": "prev_cumulative_net_value",
                "日增长值": "daily_growth_value",
                "日增长率": "daily_growth_rate",
                "申购状态": "purchase_status",
                "赎回状态": "redemption_status",
                "手续费": "fee",
            }

            # 重命名列
            df = df.rename(columns=field_mapping)

            # 检查必需字段
            required_fields = ["fund_code"]
            missing = [f for f in required_fields if f not in df.columns]
            if missing:
                logger.error(f"缺少必需字段: {missing}")
                return 0

            # 数据清理：处理无效数值（inf、NaN）
            numeric_fields = [
                "unit_net_value",
                "cumulative_net_value",
                "prev_unit_net_value",
                "prev_cumulative_net_value",
                "daily_growth_value",
                "daily_growth_rate",
            ]
            for field in numeric_fields:
                if field in df.columns:
                    df[field] = pd.to_numeric(df[field], errors="coerce")
                    df[field] = df[field].replace([float("inf"), float("-inf")], None)

            # 删除关键字段为空的行
            df = df.dropna(subset=["fund_code"])

            ops = []
            total = len(df)
            batch_size = 1000  # 每批处理1000条
            total_saved = 0

            for idx, row in df.iterrows():
                fund_code = str(row.get("fund_code", "")).strip()

                if not fund_code:
                    continue

                record = {
                    "fund_code": fund_code,
                    "date": date_str,
                    "fund_name": str(row.get("fund_name", "")).strip() if pd.notna(row.get("fund_name")) else None,
                    "unit_net_value": float(row["unit_net_value"]) if pd.notna(row.get("unit_net_value")) else None,
                    "cumulative_net_value": float(row["cumulative_net_value"]) if pd.notna(row.get("cumulative_net_value")) else None,
                    "prev_unit_net_value": float(row["prev_unit_net_value"]) if pd.notna(row.get("prev_unit_net_value")) else None,
                    "prev_cumulative_net_value": float(row["prev_cumulative_net_value"]) if pd.notna(row.get("prev_cumulative_net_value")) else None,
                    "daily_growth_value": float(row["daily_growth_value"]) if pd.notna(row.get("daily_growth_value")) else None,
                    "daily_growth_rate": float(row["daily_growth_rate"]) if pd.notna(row.get("daily_growth_rate")) else None,
                    "purchase_status": str(row.get("purchase_status", "")).strip() if pd.notna(row.get("purchase_status")) else None,
                    "redemption_status": str(row.get("redemption_status", "")).strip() if pd.notna(row.get("redemption_status")) else None,
                    "fee": str(row.get("fee", "")).strip() if pd.notna(row.get("fee")) else None,
                }

                # 唯一键：fund_code + date
                ops.append(
                    UpdateOne(
                        {"fund_code": fund_code, "date": date_str},
                        {"$set": record},
                        upsert=True,
                    )
                )

                # 批量保存：每1000条保存一次
                if len(ops) >= batch_size:
                    result = await self.col_fund_open_fund_daily_em.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.modified_count or 0)
                    total_saved += batch_saved
                    logger.info(f"已保存 {len(ops)} 条数据，累计保存 {total_saved} 条")
                    ops = []  # 清空已处理的操作

                # 进度回调
                if progress_callback and (idx + 1) % 100 == 0:
                    await progress_callback(idx + 1, total)

            # 保存剩余数据
            if ops:
                result = await self.col_fund_open_fund_daily_em.bulk_write(ops, ordered=False)
                batch_saved = (result.upserted_count or 0) + (result.modified_count or 0)
                total_saved += batch_saved
                logger.info(f"已保存剩余 {len(ops)} 条数据")

            if total_saved == 0:
                logger.warning("没有有效数据可保存")
                return 0

            logger.info(f"成功保存 {total_saved} 条开放式基金实时行情数据（日期: {date_str}）")
            return total_saved

        except Exception as e:
            logger.error(f"保存开放式基金实时行情数据失败: {e}", exc_info=True)
            raise

    async def clear_fund_open_fund_daily_data(self) -> int:
        """清空开放式基金实时行情数据

        Returns:
            删除的记录数
        """
        try:
            result = await self.col_fund_open_fund_daily_em.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条开放式基金实时行情数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空开放式基金实时行情数据失败: {e}", exc_info=True)
            raise

    async def get_fund_open_fund_daily_stats(self) -> Dict[str, Any]:
        """获取开放式基金实时行情统计信息

        Returns:
            统计信息字典，包括总数、最早/最新日期
        """
        try:
            total_count = await self.col_fund_open_fund_daily_em.count_documents({})

            # 获取最早和最新日期
            earliest_doc = (
                await self.col_fund_open_fund_daily_em.find({}, {"date": 1})
                .sort("date", 1)
                .limit(1)
                .to_list(1)
            )
            latest_doc = (
                await self.col_fund_open_fund_daily_em.find({}, {"date": 1})
                .sort("date", -1)
                .limit(1)
                .to_list(1)
            )

            earliest_date = earliest_doc[0]["date"] if earliest_doc else None
            latest_date = latest_doc[0]["date"] if latest_doc else None

            # 按日期统计记录数
            date_pipeline = [
                {"$group": {"_id": "$date", "count": {"$sum": 1}}},
                {"$project": {"date": "$_id", "count": 1, "_id": 0}},
                {"$sort": {"date": -1}},
                {"$limit": 30},
            ]
            date_stats = await self.col_fund_open_fund_daily_em.aggregate(date_pipeline).to_list(30)

            result = {
                "total_count": total_count,
                "date_stats": date_stats,
                "earliest_date": earliest_date,
                "latest_date": latest_date,
            }

            logger.debug(f"开放式基金实时行情统计: {result}")
            return result

        except Exception as e:
            logger.error(f"获取开放式基金实时行情统计失败: {e}", exc_info=True)
            return {
                "total_count": 0,
                "date_stats": [],
                "earliest_date": None,
                "latest_date": None,
            }

    async def save_fund_open_fund_info_data(
        self, df: pd.DataFrame, fund_code: str, indicator: str, progress_callback=None
    ) -> int:
        """保存开放式基金历史行情数据（支持所有7个指标）

        Args:
            df: 包含历史行情数据的 DataFrame
            fund_code: 基金代码
            indicator: 指标类型（单位净值走势、累计净值走势、累计收益率走势等）
            progress_callback: 进度回调函数

        Returns:
            保存的记录数
        """
        if df is None or df.empty:
            logger.warning(f"开放式基金历史行情数据为空（{fund_code}, {indicator}）")
            return 0

        try:
            df = df.copy()

            # 根据不同的 indicator 确定日期字段名称
            date_field_map = {
                "单位净值走势": "净值日期",
                "累计净值走势": "净值日期",
                "累计收益率走势": "日期",
                "同类排名走势": "报告日期",
                "同类排名百分比": "报告日期",
                "分红送配详情": "权益登记日",  # 或除息日
                "拆分详情": "拆分折算日",
            }

            source_date_field = date_field_map.get(indicator)
            if not source_date_field or source_date_field not in df.columns:
                # 尝试其他可能的日期字段
                possible_date_fields = ["净值日期", "日期", "报告日期", "权益登记日", "除息日", "拆分折算日", "分红发放日"]
                source_date_field = None
                for field in possible_date_fields:
                    if field in df.columns:
                        source_date_field = field
                        break

            if not source_date_field:
                logger.error(f"无法找到日期字段: indicator={indicator}, columns={df.columns.tolist()}")
                return 0

            ops = []
            total = len(df)

            for idx, row in df.iterrows():
                date_value = str(row.get(source_date_field, "")).strip()
                if not date_value or date_value == "nan":
                    continue

                # 构建记录 - 动态保存所有字段
                record = {
                    "fund_code": fund_code,
                    "indicator": indicator,
                    "date": date_value,
                }

                # 保存所有其他字段
                for col in df.columns:
                    if col != source_date_field:  # 日期字段已经保存为 date
                        value = row.get(col)
                        if pd.notna(value):
                            # 尝试转换数值类型
                            if isinstance(value, (int, float)):
                                record[col] = float(value) if not isinstance(value, int) else int(value)
                            else:
                                record[col] = str(value).strip()

                # 唯一键：fund_code + indicator + date
                ops.append(
                    UpdateOne(
                        {"fund_code": fund_code, "indicator": indicator, "date": date_value},
                        {"$set": record},
                        upsert=True,
                    )
                )

                # 进度回调
                if progress_callback and (idx + 1) % 100 == 0:
                    await progress_callback(idx + 1, total)

            if not ops:
                logger.warning("没有有效数据可保存")
                return 0

            result = await self.col_fund_open_fund_info_em.bulk_write(ops, ordered=False)
            saved_count = (result.upserted_count or 0) + (result.modified_count or 0)

            logger.info(
                f"成功保存 {saved_count} 条开放式基金历史行情数据（{fund_code}, {indicator}）"
            )
            return saved_count

        except Exception as e:
            logger.error(f"保存开放式基金历史行情数据失败: {e}", exc_info=True)
            raise

    async def save_fund_open_fund_info_merged_data(
        self, df_unit: pd.DataFrame, df_acc: pd.DataFrame, fund_code: str, progress_callback=None
    ) -> int:
        """合并单位净值走势和累计净值走势，保存到数据库
        
        Args:
            df_unit: 单位净值走势DataFrame
            df_acc: 累计净值走势DataFrame
            fund_code: 基金代码
            progress_callback: 进度回调函数
            
        Returns:
            保存的记录数
        """
        if df_unit is None or df_unit.empty or df_acc is None or df_acc.empty:
            logger.warning(f"单位净值或累计净值数据为空（{fund_code}）")
            return 0
            
        try:
            df_unit = df_unit.copy()
            df_acc = df_acc.copy()
            
            # 确保两个DataFrame都有日期字段
            if "净值日期" not in df_unit.columns or "净值日期" not in df_acc.columns:
                logger.error(f"数据缺少净值日期字段: df_unit columns={df_unit.columns.tolist()}, df_acc columns={df_acc.columns.tolist()}")
                return 0
            
            # 重命名列以便区分
            df_unit = df_unit.rename(columns={"单位净值": "unit_net_value", "日增长率": "daily_growth_rate"})
            df_acc = df_acc.rename(columns={"累计净值": "cumulative_net_value"})
            
            # 按日期合并
            merged_df = pd.merge(
                df_unit[["净值日期", "unit_net_value", "daily_growth_rate"]],
                df_acc[["净值日期", "cumulative_net_value"]],
                on="净值日期",
                how="inner"
            )
            
            if merged_df.empty:
                logger.warning(f"合并后数据为空（{fund_code}）")
                return 0
            
            # 批量保存
            ops = []
            total = len(merged_df)
            batch_size = 1000
            total_saved = 0
            
            for idx, row in merged_df.iterrows():
                date_value = str(row.get("净值日期", "")).strip()
                if not date_value or date_value == "nan":
                    continue
                
                record = {
                    "fund_code": fund_code,
                    "date": date_value,
                    "unit_net_value": float(row["unit_net_value"]) if pd.notna(row.get("unit_net_value")) else None,
                    "daily_growth_rate": float(row["daily_growth_rate"]) if pd.notna(row.get("daily_growth_rate")) else None,
                    "cumulative_net_value": float(row["cumulative_net_value"]) if pd.notna(row.get("cumulative_net_value")) else None,
                }
                
                # 唯一键：fund_code + date
                ops.append(
                    UpdateOne(
                        {"fund_code": fund_code, "date": date_value},
                        {"$set": record},
                        upsert=True,
                    )
                )
                
                # 批量保存：每1000条保存一次
                if len(ops) >= batch_size:
                    result = await self.col_fund_open_fund_info_em.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.modified_count or 0)
                    total_saved += batch_saved
                    logger.info(f"已保存 {len(ops)} 条数据，累计保存 {total_saved} 条（{fund_code}）")
                    ops = []
                
                # 进度回调
                if progress_callback and (idx + 1) % 100 == 0:
                    await progress_callback(idx + 1, total)
            
            # 保存剩余数据
            if ops:
                result = await self.col_fund_open_fund_info_em.bulk_write(ops, ordered=False)
                batch_saved = (result.upserted_count or 0) + (result.modified_count or 0)
                total_saved += batch_saved
                logger.info(f"已保存剩余 {len(ops)} 条数据（{fund_code}）")
            
            if total_saved == 0:
                logger.warning("没有有效数据可保存")
                return 0
            
            logger.info(f"成功保存 {total_saved} 条开放式基金历史行情数据（{fund_code}）")
            return total_saved
            
        except Exception as e:
            logger.error(f"保存合并后的开放式基金历史行情数据失败: {e}", exc_info=True)
            raise

    async def clear_fund_open_fund_info_data(self) -> int:
        """清空开放式基金历史行情数据

        Returns:
            删除的记录数
        """
        try:
            result = await self.col_fund_open_fund_info_em.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条开放式基金历史行情数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空开放式基金历史行情数据失败: {e}", exc_info=True)
            raise

    async def get_fund_open_fund_info_stats(self) -> Dict[str, Any]:
        """获取开放式基金历史行情统计信息

        Returns:
            统计信息字典，包括总数、各基金代码记录数、各指标记录数
        """
        try:
            total_count = await self.col_fund_open_fund_info_em.count_documents({})

            # 按基金代码统计记录数（Top 50）
            fund_code_pipeline = [
                {"$group": {"_id": "$fund_code", "count": {"$sum": 1}}},
                {"$project": {"fund_code": "$_id", "count": 1, "_id": 0}},
                {"$sort": {"count": -1}},
                {"$limit": 50},
            ]
            fund_code_stats = await self.col_fund_open_fund_info_em.aggregate(
                fund_code_pipeline
            ).to_list(50)

            # 按指标统计记录数
            indicator_pipeline = [
                {"$group": {"_id": "$indicator", "count": {"$sum": 1}}},
                {"$project": {"indicator": "$_id", "count": 1, "_id": 0}},
                {"$sort": {"count": -1}},
            ]
            indicator_stats = await self.col_fund_open_fund_info_em.aggregate(
                indicator_pipeline
            ).to_list(10)

            # 获取最早和最新日期
            earliest_doc = (
                await self.col_fund_open_fund_info_em.find({}, {"date": 1})
                .sort("date", 1)
                .limit(1)
                .to_list(1)
            )
            latest_doc = (
                await self.col_fund_open_fund_info_em.find({}, {"date": 1})
                .sort("date", -1)
                .limit(1)
                .to_list(1)
            )

            earliest_date = earliest_doc[0]["date"] if earliest_doc else None
            latest_date = latest_doc[0]["date"] if latest_doc else None

            result = {
                "total_count": total_count,
                "fund_code_stats": fund_code_stats,
                "indicator_stats": indicator_stats,
                "earliest_date": earliest_date,
                "latest_date": latest_date,
            }

            logger.debug(f"开放式基金历史行情统计: {result}")
            return result

        except Exception as e:
            logger.error(f"获取开放式基金历史行情统计失败: {e}", exc_info=True)
            return {
                "total_count": 0,
                "fund_code_stats": [],
                "indicator_stats": [],
                "earliest_date": None,
                "latest_date": None,
            }

    async def save_fund_money_fund_daily_data(
        self, df: pd.DataFrame, progress_callback=None
    ) -> int:
        """保存货币型基金实时行情数据

        Args:
            df: 包含货币型基金实时行情数据的 DataFrame
            progress_callback: 进度回调函数

        Returns:
            保存的记录数
        """
        if df is None or df.empty:
            logger.warning("货币型基金实时行情数据为空")
            return 0

        try:
            df = df.copy()

            # 获取当前日期作为数据日期
            from datetime import datetime
            current_date = datetime.now().strftime("%Y-%m-%d")

            # 清理和规范化列名
            df.columns = df.columns.str.strip()

            # 字段映射
            field_map = {
                "基金代码": "fund_code",
                "基金简称": "fund_name",
                "当前交易日-万份收益": "current_daily_profit_per_10k",
                "当前交易日-7日年化%": "current_7day_annual_yield",
                "当前交易日-单位净值": "current_unit_net_value",
                "前一交易日-万份收益": "prev_daily_profit_per_10k",
                "前一交易日-7日年化%": "prev_7day_annual_yield",
                "前一交易日-单位净值": "prev_unit_net_value",
                "日涨幅": "daily_change",
                "成立日期": "establishment_date",
                "基金经理": "fund_manager",
                "手续费": "fee",
                "可购全部": "purchasable",
            }

            ops = []
            total = len(df)

            for idx, row in df.iterrows():
                fund_code = str(row.get("基金代码", "")).strip()
                if not fund_code or fund_code == "nan":
                    continue

                # 构建记录
                record = {
                    "fund_code": fund_code,
                    "date": current_date,
                }

                # 映射其他字段
                for cn_field, en_field in field_map.items():
                    if cn_field == "基金代码":  # 已处理
                        continue
                    
                    value = row.get(cn_field)
                    if pd.notna(value):
                        value_str = str(value).strip()
                        # 跳过 "---" 等无效值
                        if value_str and value_str != "---" and value_str != "nan":
                            # 处理百分比字段
                            if "%" in cn_field or cn_field == "日涨幅":
                                # 保留原始字符串格式
                                record[en_field] = value_str
                            else:
                                # 尝试转换数值
                                try:
                                    if isinstance(value, (int, float)):
                                        record[en_field] = float(value)
                                    else:
                                        record[en_field] = value_str
                                except:
                                    record[en_field] = value_str

                # 唯一键：fund_code + date
                ops.append(
                    UpdateOne(
                        {"fund_code": fund_code, "date": current_date},
                        {"$set": record},
                        upsert=True,
                    )
                )

                # 进度回调
                if progress_callback and (idx + 1) % 100 == 0:
                    await progress_callback(idx + 1, total)

            if not ops:
                logger.warning("没有有效数据可保存")
                return 0

            result = await self.col_fund_money_fund_daily_em.bulk_write(ops, ordered=False)
            saved_count = (result.upserted_count or 0) + (result.modified_count or 0)

            logger.info(f"成功保存 {saved_count} 条货币型基金实时行情数据")
            return saved_count

        except Exception as e:
            logger.error(f"保存货币型基金实时行情数据失败: {e}", exc_info=True)
            raise

    async def clear_fund_money_fund_daily_data(self) -> int:
        """清空货币型基金实时行情数据

        Returns:
            删除的记录数
        """
        try:
            result = await self.col_fund_money_fund_daily_em.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条货币型基金实时行情数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空货币型基金实时行情数据失败: {e}", exc_info=True)
            raise

    async def get_fund_money_fund_daily_stats(self) -> Dict[str, Any]:
        """获取货币型基金实时行情统计信息

        Returns:
            统计信息字典，包括总数、各基金代码记录数、最早/最新日期
        """
        try:
            total_count = await self.col_fund_money_fund_daily_em.count_documents({})

            # 按基金代码统计记录数（Top 50）
            fund_code_pipeline = [
                {"$group": {"_id": "$fund_code", "count": {"$sum": 1}}},
                {"$project": {"fund_code": "$_id", "count": 1, "_id": 0}},
                {"$sort": {"count": -1}},
                {"$limit": 50},
            ]
            fund_code_stats = await self.col_fund_money_fund_daily_em.aggregate(
                fund_code_pipeline
            ).to_list(50)

            # 按日期统计记录数
            date_pipeline = [
                {"$group": {"_id": "$date", "count": {"$sum": 1}}},
                {"$project": {"date": "$_id", "count": 1, "_id": 0}},
                {"$sort": {"date": -1}},
                {"$limit": 30},
            ]
            date_stats = await self.col_fund_money_fund_daily_em.aggregate(
                date_pipeline
            ).to_list(30)

            # 获取最早和最新日期
            earliest_doc = (
                await self.col_fund_money_fund_daily_em.find({}, {"date": 1})
                .sort("date", 1)
                .limit(1)
                .to_list(1)
            )
            latest_doc = (
                await self.col_fund_money_fund_daily_em.find({}, {"date": 1})
                .sort("date", -1)
                .limit(1)
                .to_list(1)
            )

            earliest_date = earliest_doc[0]["date"] if earliest_doc else None
            latest_date = latest_doc[0]["date"] if latest_doc else None

            result = {
                "total_count": total_count,
                "fund_code_stats": fund_code_stats,
                "date_stats": date_stats,
                "earliest_date": earliest_date,
                "latest_date": latest_date,
            }

            logger.debug(f"货币型基金实时行情统计: {result}")
            return result

        except Exception as e:
            logger.error(f"获取货币型基金实时行情统计失败: {e}", exc_info=True)
            return {
                "total_count": 0,
                "fund_code_stats": [],
                "date_stats": [],
                "earliest_date": None,
                "latest_date": None,
            }

    async def save_fund_money_fund_info_data(
        self, df: pd.DataFrame, fund_code: str, progress_callback=None
    ) -> int:
        """保存货币型基金历史行情数据

        Args:
            df: 包含历史行情数据的 DataFrame
            fund_code: 基金代码
            progress_callback: 进度回调函数

        Returns:
            保存的记录数
        """
        if df is None or df.empty:
            logger.warning(f"货币型基金历史行情数据为空（{fund_code}）")
            return 0

        try:
            df = df.copy()
            df.columns = df.columns.str.strip()

            # 字段映射
            field_map = {
                "净值日期": "date",
                "每万份收益": "daily_profit_per_10k",
                "7日年化收益率": "seven_day_annual_yield",
                "申购状态": "purchase_status",
                "赎回状态": "redemption_status",
            }

            ops = []
            total = len(df)

            for idx, row in df.iterrows():
                date_value = str(row.get("净值日期", "")).strip()
                if not date_value or date_value == "nan":
                    continue

                record = {
                    "fund_code": fund_code,
                    "date": date_value,
                }

                # 映射其他字段
                for cn_field, en_field in field_map.items():
                    if cn_field == "净值日期":
                        continue
                    value = row.get(cn_field)
                    if pd.notna(value):
                        if isinstance(value, (int, float)):
                            record[en_field] = float(value)
                        else:
                            record[en_field] = str(value).strip()

                ops.append(
                    UpdateOne(
                        {"fund_code": fund_code, "date": date_value},
                        {"$set": record},
                        upsert=True,
                    )
                )

                if progress_callback and (idx + 1) % 100 == 0:
                    await progress_callback(idx + 1, total)

            if not ops:
                logger.warning("没有有效数据可保存")
                return 0

            result = await self.col_fund_money_fund_info_em.bulk_write(ops, ordered=False)
            saved_count = (result.upserted_count or 0) + (result.modified_count or 0)

            logger.info(f"成功保存 {saved_count} 条货币型基金历史行情数据（{fund_code}）")
            return saved_count

        except Exception as e:
            logger.error(f"保存货币型基金历史行情数据失败: {e}", exc_info=True)
            raise

    async def clear_fund_money_fund_info_data(self) -> int:
        """清空货币型基金历史行情数据

        Returns:
            删除的记录数
        """
        try:
            result = await self.col_fund_money_fund_info_em.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条货币型基金历史行情数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空货币型基金历史行情数据失败: {e}", exc_info=True)
            raise

    async def get_fund_money_fund_info_stats(self) -> Dict[str, Any]:
        """获取货币型基金历史行情统计信息

        Returns:
            统计信息字典
        """
        try:
            total_count = await self.col_fund_money_fund_info_em.count_documents({})

            # 按基金代码统计记录数（Top 50）
            fund_code_pipeline = [
                {"$group": {"_id": "$fund_code", "count": {"$sum": 1}}},
                {"$project": {"fund_code": "$_id", "count": 1, "_id": 0}},
                {"$sort": {"count": -1}},
                {"$limit": 50},
            ]
            fund_code_stats = await self.col_fund_money_fund_info_em.aggregate(
                fund_code_pipeline
            ).to_list(50)

            # 获取最早和最新日期
            earliest_doc = (
                await self.col_fund_money_fund_info_em.find({}, {"date": 1})
                .sort("date", 1)
                .limit(1)
                .to_list(1)
            )
            latest_doc = (
                await self.col_fund_money_fund_info_em.find({}, {"date": 1})
                .sort("date", -1)
                .limit(1)
                .to_list(1)
            )

            earliest_date = earliest_doc[0]["date"] if earliest_doc else None
            latest_date = latest_doc[0]["date"] if latest_doc else None

            result = {
                "total_count": total_count,
                "fund_code_stats": fund_code_stats,
                "earliest_date": earliest_date,
                "latest_date": latest_date,
            }

            return result

        except Exception as e:
            logger.error(f"获取货币型基金历史行情统计失败: {e}", exc_info=True)
            return {
                "total_count": 0,
                "fund_code_stats": [],
                "earliest_date": None,
                "latest_date": None,
            }

    async def save_fund_financial_fund_daily_data(
        self, df: pd.DataFrame, progress_callback=None
    ) -> int:
        """保存理财型基金实时行情数据

        Args:
            df: 包含理财型基金实时行情数据的 DataFrame
            progress_callback: 进度回调函数

        Returns:
            保存的记录数
        """
        if df is None or df.empty:
            logger.warning("理财型基金实时行情数据为空")
            return 0

        try:
            df = df.copy()
            from datetime import datetime
            current_date = datetime.now().strftime("%Y-%m-%d")
            df.columns = df.columns.str.strip()

            field_map = {
                "序号": "sequence",
                "基金代码": "fund_code",
                "基金简称": "fund_name",
                "上一期年化收益率": "last_period_annual_yield",
                "当前交易日-万份收益": "current_daily_profit_per_10k",
                "当前交易日-7日年华": "current_7day_annual_yield",
                "前一个交易日-万份收益": "prev_daily_profit_per_10k",
                "前一个交易日-7日年华": "prev_7day_annual_yield",
                "封闭期": "closed_period",
                "申购状态": "purchase_status",
            }

            ops = []
            total = len(df)

            for idx, row in df.iterrows():
                fund_code = str(row.get("基金代码", "")).strip()
                if not fund_code or fund_code == "nan":
                    continue

                record = {"fund_code": fund_code, "date": current_date}

                for cn_field, en_field in field_map.items():
                    if cn_field == "基金代码":
                        continue
                    
                    value = row.get(cn_field)
                    if pd.notna(value):
                        value_str = str(value).strip()
                        if value_str and value_str != "---" and value_str != "nan":
                            try:
                                if isinstance(value, (int, float)):
                                    record[en_field] = float(value)
                                else:
                                    record[en_field] = value_str
                            except:
                                record[en_field] = value_str

                ops.append(
                    UpdateOne(
                        {"fund_code": fund_code, "date": current_date},
                        {"$set": record},
                        upsert=True,
                    )
                )

                if progress_callback and (idx + 1) % 100 == 0:
                    await progress_callback(idx + 1, total)

            if not ops:
                logger.warning("没有有效数据可保存")
                return 0

            result = await self.col_fund_financial_fund_daily_em.bulk_write(ops, ordered=False)
            saved_count = (result.upserted_count or 0) + (result.modified_count or 0)

            logger.info(f"成功保存 {saved_count} 条理财型基金实时行情数据")
            return saved_count

        except Exception as e:
            logger.error(f"保存理财型基金实时行情数据失败: {e}", exc_info=True)
            raise

    async def clear_fund_financial_fund_daily_data(self) -> int:
        """清空理财型基金实时行情数据

        Returns:
            删除的记录数
        """
        try:
            result = await self.col_fund_financial_fund_daily_em.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条理财型基金实时行情数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空理财型基金实时行情数据失败: {e}", exc_info=True)
            raise

    async def get_fund_financial_fund_daily_stats(self) -> Dict[str, Any]:
        """获取理财型基金实时行情统计信息

        Returns:
            统计信息字典，包括总数、各基金代码记录数、最早/最新日期
        """
        try:
            total_count = await self.col_fund_financial_fund_daily_em.count_documents({})

            fund_code_pipeline = [
                {"$group": {"_id": "$fund_code", "count": {"$sum": 1}}},
                {"$project": {"fund_code": "$_id", "count": 1, "_id": 0}},
                {"$sort": {"count": -1}},
                {"$limit": 50},
            ]
            fund_code_stats = await self.col_fund_financial_fund_daily_em.aggregate(
                fund_code_pipeline
            ).to_list(50)

            date_pipeline = [
                {"$group": {"_id": "$date", "count": {"$sum": 1}}},
                {"$project": {"date": "$_id", "count": 1, "_id": 0}},
                {"$sort": {"date": -1}},
                {"$limit": 30},
            ]
            date_stats = await self.col_fund_financial_fund_daily_em.aggregate(
                date_pipeline
            ).to_list(30)

            earliest_doc = (
                await self.col_fund_financial_fund_daily_em.find({}, {"date": 1})
                .sort("date", 1)
                .limit(1)
                .to_list(1)
            )
            latest_doc = (
                await self.col_fund_financial_fund_daily_em.find({}, {"date": 1})
                .sort("date", -1)
                .limit(1)
                .to_list(1)
            )

            earliest_date = earliest_doc[0]["date"] if earliest_doc else None
            latest_date = latest_doc[0]["date"] if latest_doc else None

            result = {
                "total_count": total_count,
                "fund_code_stats": fund_code_stats,
                "date_stats": date_stats,
                "earliest_date": earliest_date,
                "latest_date": latest_date,
            }

            logger.debug(f"理财型基金实时行情统计: {result}")
            return result

        except Exception as e:
            logger.error(f"获取理财型基金实时行情统计失败: {e}", exc_info=True)
            return {
                "total_count": 0,
                "fund_code_stats": [],
                "date_stats": [],
                "earliest_date": None,
                "latest_date": None,
            }

    async def save_fund_financial_fund_info_data(
        self, df: pd.DataFrame, fund_code: str, progress_callback=None
    ) -> int:
        """保存理财型基金历史行情数据

        Args:
            df: 包含历史行情数据的 DataFrame
            fund_code: 基金代码
            progress_callback: 进度回调函数

        Returns:
            保存的记录数
        """
        if df is None or df.empty:
            logger.warning(f"理财型基金历史行情数据为空（{fund_code}）")
            return 0

        try:
            df = df.copy()
            df.columns = df.columns.str.strip()

            # 字段映射
            field_map = {
                "净值日期": "date",
                "单位净值": "unit_net_value",
                "累计净值": "accumulative_net_value",
                "日增长率": "daily_growth_rate",
                "申购状态": "purchase_status",
                "赎回状态": "redemption_status",
                "分红送配": "dividend_distribution",
            }

            ops = []
            total = len(df)

            for idx, row in df.iterrows():
                date_value = str(row.get("净值日期", "")).strip()
                if not date_value or date_value == "nan":
                    continue

                record = {
                    "fund_code": fund_code,
                    "date": date_value,
                }

                # 映射其他字段
                for cn_field, en_field in field_map.items():
                    if cn_field == "净值日期":
                        continue
                    value = row.get(cn_field)
                    if pd.notna(value):
                        if isinstance(value, (int, float)):
                            record[en_field] = float(value)
                        else:
                            record[en_field] = str(value).strip()

                ops.append(
                    UpdateOne(
                        {"fund_code": fund_code, "date": date_value},
                        {"$set": record},
                        upsert=True,
                    )
                )

                if progress_callback and (idx + 1) % 100 == 0:
                    await progress_callback(idx + 1, total)

            if not ops:
                logger.warning("没有有效数据可保存")
                return 0

            result = await self.col_fund_financial_fund_info_em.bulk_write(ops, ordered=False)
            saved_count = (result.upserted_count or 0) + (result.modified_count or 0)

            logger.info(f"成功保存 {saved_count} 条理财型基金历史行情数据（{fund_code}）")
            return saved_count

        except Exception as e:
            logger.error(f"保存理财型基金历史行情数据失败: {e}", exc_info=True)
            raise

    async def clear_fund_financial_fund_info_data(self) -> int:
        """清空理财型基金历史行情数据

        Returns:
            删除的记录数
        """
        try:
            result = await self.col_fund_financial_fund_info_em.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条理财型基金历史行情数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空理财型基金历史行情数据失败: {e}", exc_info=True)
            raise

    async def get_fund_financial_fund_info_stats(self) -> Dict[str, Any]:
        """获取理财型基金历史行情统计信息

        Returns:
            统计信息字典
        """
        try:
            total_count = await self.col_fund_financial_fund_info_em.count_documents({})

            # 按基金代码统计记录数（Top 50）
            fund_code_pipeline = [
                {"$group": {"_id": "$fund_code", "count": {"$sum": 1}}},
                {"$project": {"fund_code": "$_id", "count": 1, "_id": 0}},
                {"$sort": {"count": -1}},
                {"$limit": 50},
            ]
            fund_code_stats = await self.col_fund_financial_fund_info_em.aggregate(
                fund_code_pipeline
            ).to_list(50)

            # 获取最早和最新日期
            earliest_doc = (
                await self.col_fund_financial_fund_info_em.find({}, {"date": 1})
                .sort("date", 1)
                .limit(1)
                .to_list(1)
            )
            latest_doc = (
                await self.col_fund_financial_fund_info_em.find({}, {"date": 1})
                .sort("date", -1)
                .limit(1)
                .to_list(1)
            )

            earliest_date = earliest_doc[0]["date"] if earliest_doc else None
            latest_date = latest_doc[0]["date"] if latest_doc else None

            result = {
                "total_count": total_count,
                "fund_code_stats": fund_code_stats,
                "earliest_date": earliest_date,
                "latest_date": latest_date,
            }

            return result

        except Exception as e:
            logger.error(f"获取理财型基金历史行情统计失败: {e}", exc_info=True)
            return {
                "total_count": 0,
                "fund_code_stats": [],
                "earliest_date": None,
                "latest_date": None,
            }

    async def save_fund_graded_fund_daily_data(
        self, df: pd.DataFrame, progress_callback=None
    ) -> int:
        """保存分级基金实时数据

        Args:
            df: 包含分级基金实时数据的 DataFrame
            progress_callback: 进度回调函数

        Returns:
            保存的记录数
        """
        if df is None or df.empty:
            logger.warning("分级基金实时数据为空")
            return 0

        try:
            df = df.copy()
            from datetime import datetime
            current_date = datetime.now().strftime("%Y-%m-%d")
            df.columns = df.columns.str.strip()

            field_map = {
                "基金代码": "fund_code",
                "基金简称": "fund_name",
                "单位净值": "unit_net_value",
                "累计净值": "accumulative_net_value",
                "前交易日-单位净值": "prev_unit_net_value",
                "前交易日-累计净值": "prev_accumulative_net_value",
                "日增长值": "daily_growth_value",
                "日增长率": "daily_growth_rate",
                "市价": "market_price",
                "折价率": "discount_rate",
                "手续费": "fee",
            }

            ops = []
            total = len(df)

            for idx, row in df.iterrows():
                fund_code = str(row.get("基金代码", "")).strip()
                if not fund_code or fund_code == "nan":
                    continue

                record = {"fund_code": fund_code, "date": current_date}

                for cn_field, en_field in field_map.items():
                    if cn_field == "基金代码":
                        continue
                    value = row.get(cn_field)
                    if pd.notna(value):
                        value_str = str(value).strip()
                        if value_str and value_str != "---" and value_str != "nan":
                            try:
                                if isinstance(value, (int, float)):
                                    record[en_field] = float(value)
                                else:
                                    record[en_field] = value_str
                            except:
                                record[en_field] = value_str

                ops.append(
                    UpdateOne(
                        {"fund_code": fund_code, "date": current_date},
                        {"$set": record},
                        upsert=True,
                    )
                )

                if progress_callback and (idx + 1) % 100 == 0:
                    await progress_callback(idx + 1, total)

            if not ops:
                return 0

            result = await self.col_fund_graded_fund_daily_em.bulk_write(ops, ordered=False)
            saved_count = (result.upserted_count or 0) + (result.modified_count or 0)
            logger.info(f"成功保存 {saved_count} 条分级基金实时数据")
            return saved_count

        except Exception as e:
            logger.error(f"保存分级基金实时数据失败: {e}", exc_info=True)
            raise

    async def clear_fund_graded_fund_daily_data(self) -> int:
        """清空分级基金实时数据

        Returns:
            删除的记录数
        """
        try:
            result = await self.col_fund_graded_fund_daily_em.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条分级基金实时数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空分级基金实时数据失败: {e}", exc_info=True)
            raise

    async def get_fund_graded_fund_daily_stats(self) -> Dict[str, Any]:
        """获取分级基金实时数据统计信息

        Returns:
            统计信息字典
        """
        try:
            total_count = await self.col_fund_graded_fund_daily_em.count_documents({})

            fund_code_pipeline = [
                {"$group": {"_id": "$fund_code", "count": {"$sum": 1}}},
                {"$project": {"fund_code": "$_id", "count": 1, "_id": 0}},
                {"$sort": {"count": -1}},
                {"$limit": 50},
            ]
            fund_code_stats = await self.col_fund_graded_fund_daily_em.aggregate(
                fund_code_pipeline
            ).to_list(50)

            date_pipeline = [
                {"$group": {"_id": "$date", "count": {"$sum": 1}}},
                {"$project": {"date": "$_id", "count": 1, "_id": 0}},
                {"$sort": {"date": -1}},
                {"$limit": 30},
            ]
            date_stats = await self.col_fund_graded_fund_daily_em.aggregate(
                date_pipeline
            ).to_list(30)

            earliest_doc = (
                await self.col_fund_graded_fund_daily_em.find({}, {"date": 1})
                .sort("date", 1)
                .limit(1)
                .to_list(1)
            )
            latest_doc = (
                await self.col_fund_graded_fund_daily_em.find({}, {"date": 1})
                .sort("date", -1)
                .limit(1)
                .to_list(1)
            )

            result = {
                "total_count": total_count,
                "fund_code_stats": fund_code_stats,
                "date_stats": date_stats,
                "earliest_date": earliest_doc[0]["date"] if earliest_doc else None,
                "latest_date": latest_doc[0]["date"] if latest_doc else None,
            }

            return result

        except Exception as e:
            logger.error(f"获取分级基金实时数据统计失败: {e}", exc_info=True)
            return {
                "total_count": 0,
                "fund_code_stats": [],
                "date_stats": [],
                "earliest_date": None,
                "latest_date": None,
            }

    async def save_fund_graded_fund_info_data(
        self, df: pd.DataFrame, fund_code: str, progress_callback=None
    ) -> int:
        """保存分级基金历史数据

        Args:
            df: 包含历史数据的 DataFrame
            fund_code: 基金代码
            progress_callback: 进度回调函数

        Returns:
            保存的记录数
        """
        if df is None or df.empty:
            logger.warning(f"分级基金历史数据为空（{fund_code}）")
            return 0

        try:
            df = df.copy()
            df.columns = df.columns.str.strip()

            # 字段映射
            field_map = {
                "净值日期": "date",
                "单位净值": "unit_net_value",
                "累计净值": "accumulative_net_value",
                "日增长率": "daily_growth_rate",
                "申购状态": "purchase_status",
                "赎回状态": "redemption_status",
            }

            ops = []
            total = len(df)

            for idx, row in df.iterrows():
                date_value = str(row.get("净值日期", "")).strip()
                if not date_value or date_value == "nan":
                    continue

                record = {
                    "fund_code": fund_code,
                    "date": date_value,
                }

                # 映射其他字段
                for cn_field, en_field in field_map.items():
                    if cn_field == "净值日期":
                        continue
                    value = row.get(cn_field)
                    if pd.notna(value):
                        if isinstance(value, (int, float)):
                            record[en_field] = float(value)
                        else:
                            record[en_field] = str(value).strip()

                ops.append(
                    UpdateOne(
                        {"fund_code": fund_code, "date": date_value},
                        {"$set": record},
                        upsert=True,
                    )
                )

                if progress_callback and (idx + 1) % 100 == 0:
                    await progress_callback(idx + 1, total)

            if not ops:
                logger.warning("没有有效数据可保存")
                return 0

            result = await self.col_fund_graded_fund_info_em.bulk_write(ops, ordered=False)
            saved_count = (result.upserted_count or 0) + (result.modified_count or 0)

            logger.info(f"成功保存 {saved_count} 条分级基金历史数据（{fund_code}）")
            return saved_count

        except Exception as e:
            logger.error(f"保存分级基金历史数据失败: {e}", exc_info=True)
            raise

    async def clear_fund_graded_fund_info_data(self) -> int:
        """清空分级基金历史数据

        Returns:
            删除的记录数
        """
        try:
            result = await self.col_fund_graded_fund_info_em.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条分级基金历史数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空分级基金历史数据失败: {e}", exc_info=True)
            raise

    async def get_fund_graded_fund_info_stats(self) -> Dict[str, Any]:
        """获取分级基金历史数据统计信息

        Returns:
            统计信息字典
        """
        try:
            total_count = await self.col_fund_graded_fund_info_em.count_documents({})

            # 按基金代码统计记录数（Top 50）
            fund_code_pipeline = [
                {"$group": {"_id": "$fund_code", "count": {"$sum": 1}}},
                {"$project": {"fund_code": "$_id", "count": 1, "_id": 0}},
                {"$sort": {"count": -1}},
                {"$limit": 50},
            ]
            fund_code_stats = await self.col_fund_graded_fund_info_em.aggregate(
                fund_code_pipeline
            ).to_list(50)

            # 获取最早和最新日期
            earliest_doc = (
                await self.col_fund_graded_fund_info_em.find({}, {"date": 1})
                .sort("date", 1)
                .limit(1)
                .to_list(1)
            )
            latest_doc = (
                await self.col_fund_graded_fund_info_em.find({}, {"date": 1})
                .sort("date", -1)
                .limit(1)
                .to_list(1)
            )

            earliest_date = earliest_doc[0]["date"] if earliest_doc else None
            latest_date = latest_doc[0]["date"] if latest_doc else None

            result = {
                "total_count": total_count,
                "fund_code_stats": fund_code_stats,
                "earliest_date": earliest_date,
                "latest_date": latest_date,
            }

            return result

        except Exception as e:
            logger.error(f"获取分级基金历史数据统计失败: {e}", exc_info=True)
            return {
                "total_count": 0,
                "fund_code_stats": [],
                "earliest_date": None,
                "latest_date": None,
            }

    async def save_fund_etf_fund_daily_data(
        self, df: pd.DataFrame, progress_callback=None
    ) -> int:
        """保存场内交易基金实时数据

        Args:
            df: 包含场内交易基金实时数据的 DataFrame
            progress_callback: 进度回调函数

        Returns:
            保存的记录数
        """
        if df is None or df.empty:
            logger.warning("场内交易基金实时数据为空")
            return 0

        try:
            import numpy as np
            # 清理无效的浮点数值
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            df = df.copy()
            
            current_date = datetime.now().strftime("%Y-%m-%d")
            df.columns = df.columns.str.strip()

            total = len(df)
            logger.info(f"📊 开始处理 {total} 条场内交易基金实时数据...")
            
            # 分批处理，每批500条
            batch_size = 500
            total_saved = 0
            total_batches = (total + batch_size - 1) // batch_size
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total)
                batch_df = df.iloc[start_idx:end_idx]
                
                logger.info(f"📝 处理第 {batch_idx + 1}/{total_batches} 批，记录范围: {start_idx + 1}-{end_idx}")
                
                ops = []
                for idx, row in batch_df.iterrows():
                    fund_code = str(row.get("基金代码", "")).strip()
                    if not fund_code or fund_code == "nan":
                        continue

                    record = {
                        "fund_code": fund_code,
                        "date": current_date,
                        "source": "akshare",
                        "endpoint": "fund_etf_fund_daily_em",
                        "updated_at": datetime.now().isoformat()
                    }

                    # 静态字段映射
                    static_fields = {
                        "基金简称": "fund_name",
                        "类型": "fund_type",
                        "增长值": "growth_value",
                        "增长率": "growth_rate",
                        "市价": "market_price",
                        "折价率": "discount_rate",
                    }

                    for cn_field, en_field in static_fields.items():
                        value = row.get(cn_field)
                        if pd.notna(value):
                            value_str = str(value).strip()
                            if value_str and value_str != "---" and value_str != "nan":
                                try:
                                    # 尝试转换为数值类型
                                    if isinstance(value, (int, float)):
                                        record[en_field] = float(value)
                                    else:
                                        record[en_field] = value_str
                                except:
                                    record[en_field] = value_str

                    # 处理动态日期字段 - 改进版本
                    # 查找当前交易日和前一个交易日的数据
                    current_date_fields = {}
                    prev_date_fields = {}
                    
                    for col in df.columns:
                        col_str = str(col).strip()
                        value = row.get(col)
                        
                        if pd.notna(value) and str(value).strip() not in ["", "---", "nan"]:
                            try:
                                if "-单位净值" in col_str:
                                    date_part = col_str.split("-")[0]
                                    float_val = float(value)
                                    current_date_fields[f"{date_part}_unit_net_value"] = float_val
                                    # 假设最后一个是当前交易日
                                    record["current_unit_net_value"] = float_val
                                elif "-累计净值" in col_str:
                                    date_part = col_str.split("-")[0]
                                    float_val = float(value)
                                    current_date_fields[f"{date_part}_accumulative_net_value"] = float_val
                                    record["current_accumulative_net_value"] = float_val
                            except (ValueError, TypeError):
                                pass
                    
                    # 存储所有动态日期字段
                    if current_date_fields:
                        record["date_fields"] = current_date_fields

                    ops.append(
                        UpdateOne(
                            {"fund_code": fund_code, "date": current_date},
                            {"$set": record},
                            upsert=True,
                        )
                    )

                # 执行批量写入
                if ops:
                    result = await self.col_fund_etf_fund_daily_em.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    logger.info(
                        f"✅ 第 {batch_idx + 1}/{total_batches} 批写入完成: "
                        f"新增={result.upserted_count}, 更新={result.matched_count}, "
                        f"本批保存={batch_saved}, 累计={total_saved}/{total}"
                    )
                    
                    if progress_callback:
                        progress = int((end_idx / total) * 100)
                        await progress_callback(
                            current=end_idx,
                            total=total,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total} 条数据 ({progress}%)"
                        )

            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total} 条场内交易基金实时数据")
            return total_saved

        except Exception as e:
            logger.error(f"保存场内交易基金实时数据失败: {e}", exc_info=True)
            raise

    async def clear_fund_etf_fund_daily_data(self) -> int:
        """清空场内交易基金实时数据

        Returns:
            删除的记录数
        """
        try:
            result = await self.col_fund_etf_fund_daily_em.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条场内交易基金实时数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空场内交易基金实时数据失败: {e}", exc_info=True)
            raise

    async def get_fund_etf_fund_daily_stats(self) -> Dict[str, Any]:
        """获取场内交易基金实时数据统计信息

        Returns:
            统计信息字典
        """
        try:
            total_count = await self.col_fund_etf_fund_daily_em.count_documents({})

            fund_code_pipeline = [
                {"$group": {"_id": "$fund_code", "count": {"$sum": 1}}},
                {"$project": {"fund_code": "$_id", "count": 1, "_id": 0}},
                {"$sort": {"count": -1}},
                {"$limit": 50},
            ]
            fund_code_stats = await self.col_fund_etf_fund_daily_em.aggregate(
                fund_code_pipeline
            ).to_list(50)

            date_pipeline = [
                {"$group": {"_id": "$date", "count": {"$sum": 1}}},
                {"$project": {"date": "$_id", "count": 1, "_id": 0}},
                {"$sort": {"date": -1}},
                {"$limit": 30},
            ]
            date_stats = await self.col_fund_etf_fund_daily_em.aggregate(
                date_pipeline
            ).to_list(30)

            earliest_doc = (
                await self.col_fund_etf_fund_daily_em.find({}, {"date": 1})
                .sort("date", 1)
                .limit(1)
                .to_list(1)
            )
            latest_doc = (
                await self.col_fund_etf_fund_daily_em.find({}, {"date": 1})
                .sort("date", -1)
                .limit(1)
                .to_list(1)
            )

            result = {
                "total_count": total_count,
                "fund_code_stats": fund_code_stats,
                "date_stats": date_stats,
                "earliest_date": earliest_doc[0]["date"] if earliest_doc else None,
                "latest_date": latest_doc[0]["date"] if latest_doc else None,
            }

            return result

        except Exception as e:
            logger.error(f"获取场内交易基金实时数据统计失败: {e}", exc_info=True)
            return {
                "total_count": 0,
                "fund_code_stats": [],
                "date_stats": [],
                "earliest_date": None,
                "latest_date": None,
            }
    
    # ========== 香港基金历史数据 ==========
    async def save_fund_hk_hist_em_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存香港基金历史数据（历史净值明细或分红送配详情）
        
        Args:
            df: 包含香港基金历史数据的DataFrame
            progress_callback: 进度回调函数
            
        Returns:
            保存的记录数
        """
        if df is None or df.empty:
            logger.warning("没有香港基金历史数据需要保存")
            return 0
        
        try:
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条香港基金历史数据...")
            
            # 分批处理，每批500条
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                logger.info(f"📝 处理第 {batch_idx + 1}/{total_batches} 批，记录范围: {start_idx + 1}-{end_idx}")
                
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    # 清理NaN/Infinity值
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    # 添加元数据
                    fund_code = str(doc.get('code', ''))
                    symbol = str(doc.get('symbol', '历史净值明细'))
                    
                    # 确定日期字段
                    date_field = None
                    if '净值日期' in doc:
                        date_field = str(doc.get('净值日期', ''))
                    elif '除息日' in doc:
                        date_field = str(doc.get('除息日', ''))
                    
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_hk_fund_hist_em'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    # 构建唯一标识（code + date + symbol）
                    filter_query = {'code': fund_code, 'symbol': symbol}
                    if date_field:
                        filter_query['date'] = date_field
                        doc['date'] = date_field
                    
                    ops.append(
                        UpdateOne(
                            filter_query,
                            {'$set': doc},
                            upsert=True
                        )
                    )
                
                # 执行批量写入
                if ops:
                    result = await self.col_fund_hk_hist_em.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    logger.info(
                        f"✅ 第 {batch_idx + 1}/{total_batches} 批写入完成: "
                        f"新增={result.upserted_count}, 更新={result.matched_count}, "
                        f"本批保存={batch_saved}, 累计={total_saved}/{total_count}"
                    )
                    
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        await progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条香港基金历史数据")
            return total_saved
            
        except Exception as e:
            logger.error(f"保存香港基金历史数据失败: {e}", exc_info=True)
            raise
    
    async def get_fund_hk_hist_em_stats(self) -> Dict[str, Any]:
        """获取香港基金历史数据统计信息
        
        Returns:
            统计信息字典
        """
        try:
            total_count = await self.col_fund_hk_hist_em.count_documents({})
            
            # 基金数量统计
            fund_count_pipeline = [
                {"$group": {"_id": "$code"}},
                {"$count": "count"}
            ]
            fund_count_result = await self.col_fund_hk_hist_em.aggregate(fund_count_pipeline).to_list(1)
            fund_count = fund_count_result[0]["count"] if fund_count_result else 0
            
            # symbol分布统计
            symbol_pipeline = [
                {"$group": {"_id": "$symbol", "count": {"$sum": 1}}},
                {"$project": {"symbol": "$_id", "count": 1, "_id": 0}},
                {"$sort": {"count": -1}}
            ]
            symbol_stats = await self.col_fund_hk_hist_em.aggregate(symbol_pipeline).to_list(10)
            
            # 日期范围统计
            earliest_doc = (
                await self.col_fund_hk_hist_em.find({"date": {"$exists": True, "$ne": None}}, {"date": 1})
                .sort("date", 1)
                .limit(1)
                .to_list(1)
            )
            latest_doc = (
                await self.col_fund_hk_hist_em.find({"date": {"$exists": True, "$ne": None}}, {"date": 1})
                .sort("date", -1)
                .limit(1)
                .to_list(1)
            )
            
            # 基金代码分布
            fund_code_pipeline = [
                {"$group": {"_id": "$code", "count": {"$sum": 1}}},
                {"$project": {"fund_code": "$_id", "count": 1, "_id": 0}},
                {"$sort": {"count": -1}},
                {"$limit": 20}
            ]
            fund_code_stats = await self.col_fund_hk_hist_em.aggregate(fund_code_pipeline).to_list(20)
            
            result = {
                "total_count": total_count,
                "fund_count": fund_count,
                "symbol_distribution": symbol_stats,
                "fund_code_stats": fund_code_stats,
                "earliest_date": earliest_doc[0]["date"] if earliest_doc else None,
                "latest_date": latest_doc[0]["date"] if latest_doc else None,
            }
            
            return result
            
        except Exception as e:
            logger.error(f"获取香港基金历史数据统计失败: {e}", exc_info=True)
            return {
                "total_count": 0,
                "fund_count": 0,
                "symbol_distribution": [],
                "fund_code_stats": [],
                "earliest_date": None,
                "latest_date": None,
            }
    
    async def import_fund_hk_hist_em_from_file(self, content: bytes, filename: Optional[str] = None) -> Dict[str, Any]:
        """从文件导入香港基金历史数据
        
        Args:
            content: 文件内容（字节）
            filename: 文件名
            
        Returns:
            导入结果字典
        """
        if not content:
            raise ValueError("上传文件为空")
        
        name = (filename or "").lower()
        buffer = io.BytesIO(content)
        
        df: Optional[pd.DataFrame] = None
        try:
            if name.endswith(".csv") or name.endswith(".txt"):
                df = pd.read_csv(buffer)
            elif name.endswith(".xls") or name.endswith(".xlsx"):
                df = pd.read_excel(buffer)
            else:
                try:
                    df = pd.read_csv(buffer)
                except Exception:
                    buffer.seek(0)
                    df = pd.read_excel(buffer)
        except Exception as e:
            logger.error(f"❌ [fund_hk_hist_em 导入] 读取文件失败: {e}", exc_info=True)
            raise ValueError("无法解析上传文件，请确认为有效的 CSV 或 Excel 文件")
        
        if df is None or df.empty:
            logger.warning("⚠️ [fund_hk_hist_em 导入] 解析结果为空 DataFrame")
            return {"saved": 0, "rows": 0}
        
        rows = len(df)
        saved = await self.save_fund_hk_hist_em_data(df)
        logger.info(f"💾 [fund_hk_hist_em 导入] 从文件 {filename} 导入 {rows} 行，保存 {saved} 条记录")
        
        return {"saved": saved, "rows": rows}
    
    async def sync_fund_hk_hist_em_from_remote(
        self,
        remote_host: str,
        batch_size: int = 1000,
        remote_collection: Optional[str] = None,
        remote_username: Optional[str] = None,
        remote_password: Optional[str] = None,
        remote_auth_source: Optional[str] = None,
    ) -> Dict[str, Any]:
        """从远程MongoDB同步香港基金历史数据
        
        Args:
            remote_host: 远程主机地址
            batch_size: 批量大小
            remote_collection: 远程集合名称
            remote_username: 远程用户名
            remote_password: 远程密码
            remote_auth_source: 认证数据库
            
        Returns:
            同步结果字典
        """
        from motor.motor_asyncio import AsyncIOMotorClient
        
        if not remote_host:
            raise ValueError("远程主机地址不能为空")
        
        # 构建远程连接URI
        if remote_username and remote_password:
            auth_source = remote_auth_source or self.db.name
            remote_uri = f"mongodb://{remote_username}:{remote_password}@{remote_host}/?authSource={auth_source}"
        else:
            remote_uri = f"mongodb://{remote_host}"
        
        remote_client = None
        try:
            remote_client = AsyncIOMotorClient(remote_uri)
            remote_db = remote_client[self.db.name]
            remote_col_name = remote_collection or "fund_hk_hist_em"
            remote_col = remote_db[remote_col_name]
            
            # 获取远程数据总数
            remote_total = await remote_col.count_documents({})
            logger.info(f"🔗 远程集合 {remote_col_name} 共有 {remote_total} 条数据")
            
            if remote_total == 0:
                return {"remote_total": 0, "synced": 0, "message": "远程集合为空"}
            
            # 分批同步
            synced = 0
            skip = 0
            
            while skip < remote_total:
                cursor = remote_col.find({}).skip(skip).limit(batch_size)
                batch_docs = await cursor.to_list(batch_size)
                
                if not batch_docs:
                    break
                
                # 转换为DataFrame并保存
                df = pd.DataFrame(batch_docs)
                if '_id' in df.columns:
                    df = df.drop('_id', axis=1)
                
                batch_saved = await self.save_fund_hk_hist_em_data(df)
                synced += batch_saved
                skip += len(batch_docs)
                
                logger.info(f"📥 已同步 {skip}/{remote_total} 条数据")
            
            logger.info(f"✅ 同步完成: 远程 {remote_total} 条，本地保存/更新 {synced} 条")
            
            return {
                "remote_total": remote_total,
                "synced": synced,
                "message": f"成功同步 {synced} 条香港基金历史数据"
            }
            
        except Exception as e:
            logger.error(f"❌ 从远程同步香港基金历史数据失败: {e}", exc_info=True)
            raise
        finally:
            if remote_client:
                remote_client.close()
    
    async def clear_fund_hk_hist_em_data(self) -> int:
        """清空香港基金历史数据
        
        Returns:
            删除的记录数
        """
        try:
            result = await self.col_fund_hk_hist_em.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条香港基金历史数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空香港基金历史数据失败: {e}", exc_info=True)
            raise
    
    # ========== 场内交易基金历史行情 ==========
    async def save_fund_etf_fund_info_data(self, df: pd.DataFrame, fund_code: str = None, progress_callback=None) -> int:
        """保存场内交易基金历史行情数据
        
        Args:
            df: 包含历史行情数据的DataFrame
            fund_code: 基金代码
            progress_callback: 进度回调函数
            
        Returns:
            保存的记录数
        """
        if df is None or df.empty:
            logger.warning("没有场内交易基金历史行情数据需要保存")
            return 0
        
        try:
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条场内交易基金历史行情数据...")
            
            # 分批处理，每批500条
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                logger.info(f"📝 处理第 {batch_idx + 1}/{total_batches} 批，记录范围: {start_idx + 1}-{end_idx}")
                
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    # 清理NaN/Infinity值
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    # 添加元数据
                    if fund_code:
                        doc['fund_code'] = fund_code
                    elif 'fund_code' not in doc:
                        doc['fund_code'] = doc.get('code', '')
                    
                    # 确定日期字段
                    date_field = str(doc.get('净值日期', ''))
                    doc['date'] = date_field
                    
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_etf_fund_info_em'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    # 构建唯一标识（fund_code + date）
                    filter_query = {
                        'fund_code': doc['fund_code'],
                        'date': date_field
                    }
                    
                    ops.append(
                        UpdateOne(
                            filter_query,
                            {'$set': doc},
                            upsert=True
                        )
                    )
                
                # 执行批量写入
                if ops:
                    result = await self.col_fund_etf_fund_info_em.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    logger.info(
                        f"✅ 第 {batch_idx + 1}/{total_batches} 批写入完成: "
                        f"新增={result.upserted_count}, 更新={result.matched_count}, "
                        f"本批保存={batch_saved}, 累计={total_saved}/{total_count}"
                    )
                    
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        await progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条场内交易基金历史行情数据")
            return total_saved
            
        except Exception as e:
            logger.error(f"保存场内交易基金历史行情数据失败: {e}", exc_info=True)
            raise
    
    async def get_fund_etf_fund_info_stats(self) -> Dict[str, Any]:
        """获取场内交易基金历史行情统计信息
        
        Returns:
            统计信息字典
        """
        try:
            total_count = await self.col_fund_etf_fund_info_em.count_documents({})
            
            # 基金代码分布
            fund_code_pipeline = [
                {"$group": {"_id": "$fund_code", "count": {"$sum": 1}}},
                {"$project": {"fund_code": "$_id", "count": 1, "_id": 0}},
                {"$sort": {"count": -1}},
                {"$limit": 20}
            ]
            fund_code_stats = await self.col_fund_etf_fund_info_em.aggregate(fund_code_pipeline).to_list(20)
            
            # 日期范围统计
            earliest_doc = (
                await self.col_fund_etf_fund_info_em.find({"date": {"$exists": True, "$ne": None}}, {"date": 1})
                .sort("date", 1)
                .limit(1)
                .to_list(1)
            )
            latest_doc = (
                await self.col_fund_etf_fund_info_em.find({"date": {"$exists": True, "$ne": None}}, {"date": 1})
                .sort("date", -1)
                .limit(1)
                .to_list(1)
            )
            
            result = {
                "total_count": total_count,
                "fund_code_stats": fund_code_stats,
                "earliest_date": earliest_doc[0]["date"] if earliest_doc else None,
                "latest_date": latest_doc[0]["date"] if latest_doc else None,
            }
            
            return result
            
        except Exception as e:
            logger.error(f"获取场内交易基金历史行情统计失败: {e}", exc_info=True)
            return {
                "total_count": 0,
                "fund_code_stats": [],
                "earliest_date": None,
                "latest_date": None,
            }
    
    async def clear_fund_etf_fund_info_data(self) -> int:
        """清空场内交易基金历史行情数据
        
        Returns:
            删除的记录数
        """
        try:
            result = await self.col_fund_etf_fund_info_em.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条场内交易基金历史行情数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空场内交易基金历史行情数据失败: {e}", exc_info=True)
            raise
    
    async def save_fund_etf_dividend_sina_data(self, df: pd.DataFrame, fund_code: str, progress_callback=None) -> int:
        """保存基金累计分红数据到MongoDB
        
        Args:
            df: 包含基金累计分红数据的DataFrame
            fund_code: 基金代码（如 sh510050）
            progress_callback: 进度回调函数
            
        Returns:
            保存的记录数
        """
        if df is None or df.empty:
            logger.warning(f"没有基金累计分红数据需要保存: {fund_code}")
            return 0
        
        try:
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {fund_code} 的 {total_count} 条累计分红数据...")
            
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime("%Y-%m-%d")
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime("%Y-%m-%d %H:%M:%S")
                        elif pd.isna(value):
                            doc[key] = None
                    
                    doc["fund_code"] = fund_code
                    doc["code"] = fund_code.replace("sh", "").replace("sz", "")
                    doc["source"] = "sina"
                    doc["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    date_str = doc.get("日期")
                    if date_str:
                        filter_query = {"fund_code": fund_code, "日期": date_str}
                        ops.append(UpdateOne(filter_query, {"$set": doc}, upsert=True))
                
                if ops:
                    result = await self.col_fund_etf_dividend_sina.bulk_write(ops, ordered=False)
                    batch_saved = result.upserted_count + result.modified_count
                    total_saved += batch_saved
                    
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        await progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"✅ {fund_code} 累计分红数据保存完成: {total_saved}/{total_count}")
            return total_saved
            
        except Exception as e:
            logger.error(f"保存基金累计分红数据失败: {e}", exc_info=True)
            raise
    
    async def get_fund_etf_dividend_sina_stats(self) -> Dict[str, Any]:
        """获取基金累计分红统计信息
        
        Returns:
            统计信息字典
        """
        try:
            total_count = await self.col_fund_etf_dividend_sina.count_documents({})
            
            fund_code_pipeline = [
                {"$group": {"_id": "$fund_code", "count": {"$sum": 1}}},
                {"$project": {"fund_code": "$_id", "count": 1, "_id": 0}},
                {"$sort": {"count": -1}},
                {"$limit": 20}
            ]
            fund_code_stats = await self.col_fund_etf_dividend_sina.aggregate(fund_code_pipeline).to_list(20)
            
            earliest_doc = (
                await self.col_fund_etf_dividend_sina.find({"日期": {"$exists": True, "$ne": None}}, {"日期": 1})
                .sort("日期", 1)
                .limit(1)
                .to_list(1)
            )
            latest_doc = (
                await self.col_fund_etf_dividend_sina.find({"日期": {"$exists": True, "$ne": None}}, {"日期": 1})
                .sort("日期", -1)
                .limit(1)
                .to_list(1)
            )
            
            result = {
                "total_count": total_count,
                "fund_code_stats": fund_code_stats,
                "earliest_date": earliest_doc[0]["日期"] if earliest_doc else None,
                "latest_date": latest_doc[0]["日期"] if latest_doc else None,
            }
            
            return result
            
        except Exception as e:
            logger.error(f"获取基金累计分红统计失败: {e}", exc_info=True)
            return {
                "total_count": 0,
                "fund_code_stats": [],
                "earliest_date": None,
                "latest_date": None,
            }
    
    async def clear_fund_etf_dividend_sina_data(self) -> int:
        """清空基金累计分红数据
        
        Returns:
            删除的记录数
        """
        try:
            result = await self.col_fund_etf_dividend_sina.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条基金累计分红数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空基金累计分红数据失败: {e}", exc_info=True)
            raise
    
    async def import_fund_etf_dividend_sina_from_file(self, content: bytes, filename: Optional[str] = None) -> Dict[str, Any]:
        """从文件导入基金累计分红数据
        
        Args:
            content: 文件内容
            filename: 文件名
            
        Returns:
            导入结果
        """
        if not content:
            raise ValueError("上传文件为空")
        
        name = (filename or "").lower()
        buffer = io.BytesIO(content)
        
        df: Optional[pd.DataFrame] = None
        try:
            if name.endswith(".csv") or name.endswith(".txt"):
                df = pd.read_csv(buffer)
            elif name.endswith(".xls") or name.endswith(".xlsx"):
                df = pd.read_excel(buffer)
            else:
                try:
                    df = pd.read_csv(buffer)
                except Exception:
                    buffer.seek(0)
                    df = pd.read_excel(buffer)
        except Exception as e:
            logger.error(f"读取文件失败: {e}", exc_info=True)
            raise ValueError("无法解析上传文件，请确认为有效的 CSV 或 Excel 文件")
        
        if df is None or df.empty:
            logger.warning("解析结果为空 DataFrame")
            return {"saved": 0, "rows": 0}
        
        rows = len(df)
        fund_code = df.iloc[0].get("fund_code", "unknown") if "fund_code" in df.columns else "unknown"
        saved = await self.save_fund_etf_dividend_sina_data(df, fund_code)
        logger.info(f"从文件 {filename} 导入 {rows} 行，保存 {saved} 条记录")
        
        return {"saved": saved, "rows": rows}
    
    async def sync_fund_etf_dividend_sina_from_remote(self, remote_host: str, batch_size: int = 5000, 
                                                       remote_collection: Optional[str] = None,
                                                       remote_username: Optional[str] = None,
                                                       remote_password: Optional[str] = None,
                                                       remote_auth_source: Optional[str] = None) -> Dict[str, Any]:
        """从远程MongoDB同步基金累计分红数据
        
        Args:
            remote_host: 远程主机地址
            batch_size: 批次大小
            remote_collection: 远程集合名称
            remote_username: 远程用户名
            remote_password: 远程密码
            remote_auth_source: 认证数据库
            
        Returns:
            同步结果
        """
        from motor.motor_asyncio import AsyncIOMotorClient
        from bson import ObjectId
        
        if not remote_host:
            raise ValueError("远程主机地址不能为空")
        
        try:
            batch = int(batch_size)
        except Exception:
            batch = 5000
        if batch <= 0:
            batch = 5000
        
        db_name = self.db.name
        auth_source = (remote_auth_source or db_name) if remote_username else None
        
        if remote_host.startswith("mongodb://") or remote_host.startswith("mongodb+srv://"):
            uri = remote_host
        else:
            host = remote_host
            port = 27017
            if ":" in remote_host:
                host_part, port_str = remote_host.split(":", 1)
                host = host_part or host
                try:
                    port = int(port_str)
                except Exception:
                    port = 27017
            
            if remote_username:
                if remote_password:
                    cred = f"{remote_username}:{remote_password}"
                else:
                    cred = remote_username
                
                if auth_source:
                    uri = f"mongodb://{cred}@{host}:{port}/{db_name}?authSource={auth_source}"
                else:
                    uri = f"mongodb://{cred}@{host}:{port}/{db_name}"
            else:
                uri = f"mongodb://{host}:{port}/{db_name}"
        
        logger.info(f"开始从 {uri} 同步基金累计分红数据，batch_size={batch}")
        
        client: AsyncIOMotorClient = AsyncIOMotorClient(uri, serverSelectionTimeoutMS=5000)
        try:
            try:
                remote_db = client.get_default_database() or client[self.db.name]
            except Exception:
                remote_db = client[self.db.name]
            
            target_collection = remote_collection or "fund_etf_dividend_sina"
            remote_col = remote_db[target_collection]
            
            base_filter: Dict[str, Any] = {}
            
            try:
                remote_total = await remote_col.count_documents(base_filter)
            except Exception as e:
                logger.warning(f"统计远程文档数量失败: {e}")
                remote_total = 0
            
            synced = 0
            last_id: Optional[ObjectId] = None
            
            while True:
                if last_id is not None:
                    query: Dict[str, Any] = {"_id": {"$gt": last_id}}
                else:
                    query = base_filter
                
                cursor = remote_col.find(query).sort("_id", 1).limit(batch)
                docs = await cursor.to_list(length=batch)
                if not docs:
                    break
                
                last_id = docs[-1].get("_id")
                
                for d in docs:
                    d.pop("_id", None)
                
                ops = []
                for doc in docs:
                    fund_code = doc.get("fund_code", "unknown")
                    date_str = doc.get("日期")
                    if date_str:
                        filter_query = {"fund_code": fund_code, "日期": date_str}
                        ops.append(UpdateOne(filter_query, {"$set": doc}, upsert=True))
                
                if ops:
                    result = await self.col_fund_etf_dividend_sina.bulk_write(ops, ordered=False)
                    synced += result.upserted_count + result.modified_count
            
            logger.info(f"完成同步：remote_total={remote_total}, synced={synced}")
            
            return {"collection_name": "fund_etf_dividend_sina", "remote_total": remote_total, "synced": synced}
        finally:
            try:
                client.close()
            except Exception:
                pass
    
    async def save_fund_fh_em_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存基金分红数据到MongoDB
        
        Args:
            df: 包含基金分红数据的DataFrame
            progress_callback: 进度回调函数
            
        Returns:
            保存的记录数
        """
        if df is None or df.empty:
            logger.warning("没有基金分红数据需要保存")
            return 0
        
        try:
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条基金分红数据...")
            
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime("%Y-%m-%d")
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime("%Y-%m-%d %H:%M:%S")
                        elif pd.isna(value):
                            doc[key] = None
                    
                    doc["source"] = "eastmoney"
                    doc["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    # 唯一标识：基金代码 + 权益登记日 + 除息日期
                    fund_code = doc.get("基金代码")
                    equity_date = doc.get("权益登记日")
                    ex_dividend_date = doc.get("除息日期")
                    
                    if fund_code and equity_date and ex_dividend_date:
                        filter_query = {
                            "基金代码": fund_code,
                            "权益登记日": equity_date,
                            "除息日期": ex_dividend_date
                        }
                        ops.append(UpdateOne(filter_query, {"$set": doc}, upsert=True))
                
                if ops:
                    result = await self.col_fund_fh_em.bulk_write(ops, ordered=False)
                    batch_saved = result.upserted_count + result.modified_count
                    total_saved += batch_saved
                    
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        await progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"✅ 基金分红数据保存完成: {total_saved}/{total_count}")
            return total_saved
            
        except Exception as e:
            logger.error(f"保存基金分红数据失败: {e}", exc_info=True)
            raise
    
    async def get_fund_fh_em_stats(self) -> Dict[str, Any]:
        """获取基金分红统计信息
        
        Returns:
            统计信息字典
        """
        try:
            total_count = await self.col_fund_fh_em.count_documents({})
            
            # 基金代码分布（分红次数最多的基金）
            fund_code_pipeline = [
                {"$group": {"_id": "$基金代码", "count": {"$sum": 1}, "基金简称": {"$first": "$基金简称"}}},
                {"$project": {"基金代码": "$_id", "基金简称": 1, "分红次数": "$count", "_id": 0}},
                {"$sort": {"分红次数": -1}},
                {"$limit": 20}
            ]
            fund_code_stats = await self.col_fund_fh_em.aggregate(fund_code_pipeline).to_list(20)
            
            # 日期范围统计
            earliest_doc = (
                await self.col_fund_fh_em.find({"权益登记日": {"$exists": True, "$ne": None}}, {"权益登记日": 1})
                .sort("权益登记日", 1)
                .limit(1)
                .to_list(1)
            )
            latest_doc = (
                await self.col_fund_fh_em.find({"权益登记日": {"$exists": True, "$ne": None}}, {"权益登记日": 1})
                .sort("权益登记日", -1)
                .limit(1)
                .to_list(1)
            )
            
            # 分红金额统计
            total_dividend_pipeline = [
                {"$group": {"_id": None, "total_dividend": {"$sum": "$分红"}}}
            ]
            total_dividend_result = await self.col_fund_fh_em.aggregate(total_dividend_pipeline).to_list(1)
            total_dividend = total_dividend_result[0]["total_dividend"] if total_dividend_result else 0
            
            result = {
                "total_count": total_count,
                "fund_code_stats": fund_code_stats,
                "earliest_date": earliest_doc[0]["权益登记日"] if earliest_doc else None,
                "latest_date": latest_doc[0]["权益登记日"] if latest_doc else None,
                "total_dividend": round(total_dividend, 4) if total_dividend else 0,
            }
            
            return result
            
        except Exception as e:
            logger.error(f"获取基金分红统计失败: {e}", exc_info=True)
            return {
                "total_count": 0,
                "fund_code_stats": [],
                "earliest_date": None,
                "latest_date": None,
                "total_dividend": 0,
            }
    
    async def clear_fund_fh_em_data(self) -> int:
        """清空基金分红数据
        
        Returns:
            删除的记录数
        """
        try:
            result = await self.col_fund_fh_em.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条基金分红数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空基金分红数据失败: {e}", exc_info=True)
            raise
    
    async def import_fund_fh_em_from_file(self, content: bytes, filename: Optional[str] = None) -> Dict[str, Any]:
        """从文件导入基金分红数据
        
        Args:
            content: 文件内容
            filename: 文件名
            
        Returns:
            导入结果
        """
        if not content:
            raise ValueError("上传文件为空")
        
        name = (filename or "").lower()
        buffer = io.BytesIO(content)
        
        df: Optional[pd.DataFrame] = None
        try:
            if name.endswith(".csv") or name.endswith(".txt"):
                df = pd.read_csv(buffer)
            elif name.endswith(".xls") or name.endswith(".xlsx"):
                df = pd.read_excel(buffer)
            else:
                try:
                    df = pd.read_csv(buffer)
                except Exception:
                    buffer.seek(0)
                    df = pd.read_excel(buffer)
        except Exception as e:
            logger.error(f"读取文件失败: {e}", exc_info=True)
            raise ValueError("无法解析上传文件，请确认为有效的 CSV 或 Excel 文件")
        
        if df is None or df.empty:
            logger.warning("解析结果为空 DataFrame")
            return {"saved": 0, "rows": 0}
        
        rows = len(df)
        saved = await self.save_fund_fh_em_data(df)
        logger.info(f"从文件 {filename} 导入 {rows} 行，保存 {saved} 条记录")
        
        return {"saved": saved, "rows": rows}
    
    async def sync_fund_fh_em_from_remote(self, remote_host: str, batch_size: int = 5000, 
                                          remote_collection: Optional[str] = None,
                                          remote_username: Optional[str] = None,
                                          remote_password: Optional[str] = None,
                                          remote_auth_source: Optional[str] = None) -> Dict[str, Any]:
        """从远程MongoDB同步基金分红数据
        
        Args:
            remote_host: 远程主机地址
            batch_size: 批次大小
            remote_collection: 远程集合名称
            remote_username: 远程用户名
            remote_password: 远程密码
            remote_auth_source: 认证数据库
            
        Returns:
            同步结果
        """
        from motor.motor_asyncio import AsyncIOMotorClient
        from bson import ObjectId
        
        if not remote_host:
            raise ValueError("远程主机地址不能为空")
        
        try:
            batch = int(batch_size)
        except Exception:
            batch = 5000
        if batch <= 0:
            batch = 5000
        
        db_name = self.db.name
        auth_source = (remote_auth_source or db_name) if remote_username else None
        
        if remote_host.startswith("mongodb://") or remote_host.startswith("mongodb+srv://"):
            uri = remote_host
        else:
            host = remote_host
            port = 27017
            if ":" in remote_host:
                host_part, port_str = remote_host.split(":", 1)
                host = host_part or host
                try:
                    port = int(port_str)
                except Exception:
                    port = 27017
            
            if remote_username:
                if remote_password:
                    cred = f"{remote_username}:{remote_password}"
                else:
                    cred = remote_username
                
                if auth_source:
                    uri = f"mongodb://{cred}@{host}:{port}/{db_name}?authSource={auth_source}"
                else:
                    uri = f"mongodb://{cred}@{host}:{port}/{db_name}"
            else:
                uri = f"mongodb://{host}:{port}/{db_name}"
        
        logger.info(f"开始从 {uri} 同步基金分红数据，batch_size={batch}")
        
        client: AsyncIOMotorClient = AsyncIOMotorClient(uri, serverSelectionTimeoutMS=5000)
        try:
            try:
                remote_db = client.get_default_database() or client[self.db.name]
            except Exception:
                remote_db = client[self.db.name]
            
            target_collection = remote_collection or "fund_fh_em"
            remote_col = remote_db[target_collection]
            
            base_filter: Dict[str, Any] = {}
            
            try:
                remote_total = await remote_col.count_documents(base_filter)
            except Exception as e:
                logger.warning(f"统计远程文档数量失败: {e}")
                remote_total = 0
            
            synced = 0
            last_id: Optional[ObjectId] = None
            
            while True:
                if last_id is not None:
                    query: Dict[str, Any] = {"_id": {"$gt": last_id}}
                else:
                    query = base_filter
                
                cursor = remote_col.find(query).sort("_id", 1).limit(batch)
                docs = await cursor.to_list(length=batch)
                if not docs:
                    break
                
                last_id = docs[-1].get("_id")
                
                for d in docs:
                    d.pop("_id", None)
                
                ops = []
                for doc in docs:
                    fund_code = doc.get("基金代码")
                    equity_date = doc.get("权益登记日")
                    ex_dividend_date = doc.get("除息日期")
                    
                    if fund_code and equity_date and ex_dividend_date:
                        filter_query = {
                            "基金代码": fund_code,
                            "权益登记日": equity_date,
                            "除息日期": ex_dividend_date
                        }
                        ops.append(UpdateOne(filter_query, {"$set": doc}, upsert=True))
                
                if ops:
                    result = await self.col_fund_fh_em.bulk_write(ops, ordered=False)
                    synced += result.upserted_count + result.modified_count
            
            logger.info(f"完成同步：remote_total={remote_total}, synced={synced}")
            
            return {"collection_name": "fund_fh_em", "remote_total": remote_total, "synced": synced}
        finally:
            try:
                client.close()
            except Exception:
                pass
    
    async def save_fund_cf_em_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """
        保存基金拆分数据到MongoDB
        
        Args:
            df: 包含基金拆分信息的DataFrame
            progress_callback: 进度回调函数
            
        Returns:
            保存的记录数
        """
        if df is None or df.empty:
            logger.warning("没有基金拆分数据需要保存")
            return 0
        
        try:
            # 清理无效的浮点数值（NaN, Infinity等），防止JSON序列化错误
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条基金拆分数据...")
            
            # 分批处理，每批500条
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            logger.info(f"📦 将分 {total_batches} 批次处理，每批 {batch_size} 条")
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                logger.info(f"📝 处理第 {batch_idx + 1}/{total_batches} 批，记录范围: {start_idx + 1}-{end_idx}")
                
                # 构建批量操作
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    # 清理NaN/Infinity值
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        # 转换 datetime.date 对象为字符串
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        # 转换 datetime.datetime 对象为字符串
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    # 添加元数据
                    fund_code = str(doc.get('基金代码', ''))
                    split_date = str(doc.get('拆分折算日', ''))
                    doc['code'] = fund_code
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_cf_em'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    # 使用基金代码和拆分折算日作为唯一标识
                    ops.append(
                        UpdateOne(
                            {'code': fund_code, '拆分折算日': split_date},
                            {'$set': doc},
                            upsert=True
                        )
                    )
                
                # 执行批量写入
                if ops:
                    result = await self.col_fund_cf_em.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    logger.info(
                        f"✅ 第 {batch_idx + 1}/{total_batches} 批写入完成: "
                        f"新增={result.upserted_count}, 更新={result.matched_count}, "
                        f"本批保存={batch_saved}, 累计={total_saved}/{total_count}"
                    )
                    
                    # 调用进度回调（如果提供）
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条基金拆分数据")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存基金拆分数据失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_cf_em_data(self) -> int:
        """
        清空基金拆分数据
        
        Returns:
            删除的记录数
        """
        try:
            result = await self.col_fund_cf_em.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条基金拆分数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空基金拆分数据失败: {e}", exc_info=True)
            raise
    
    async def get_fund_cf_em_stats(self) -> Dict[str, Any]:
        """
        获取基金拆分统计
        
        Returns:
            统计信息字典
        """
        try:
            total_count = await self.col_fund_cf_em.count_documents({})
            
            # 按拆分类型统计
            pipeline = [
                {
                    '$group': {
                        '_id': '$拆分类型',
                        'count': {'$sum': 1}
                    }
                },
                {
                    '$sort': {'count': -1}
                }
            ]
            
            type_stats = []
            async for doc in self.col_fund_cf_em.aggregate(pipeline):
                type_stats.append({
                    'type': doc['_id'],
                    'count': doc['count']
                })
            
            # 获取最早和最晚的拆分日期
            earliest_date = None
            latest_date = None
            pipeline_date = [
                {
                    '$group': {
                        '_id': None,
                        'earliest': {'$min': '$拆分折算日'},
                        'latest': {'$max': '$拆分折算日'}
                    }
                }
            ]
            
            async for doc in self.col_fund_cf_em.aggregate(pipeline_date):
                earliest_date = doc.get('earliest')
                latest_date = doc.get('latest')
            
            return {
                'total_count': total_count,
                'type_stats': type_stats,
                'earliest_date': earliest_date,
                'latest_date': latest_date
            }
        except Exception as e:
            logger.error(f"获取基金拆分统计失败: {e}", exc_info=True)
            raise
    
    async def save_fund_fh_rank_em_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """
        保存基金分红排行数据到MongoDB
        
        Args:
            df: 包含基金分红排行信息的DataFrame
            progress_callback: 进度回调函数
            
        Returns:
            保存的记录数
        """
        if df is None or df.empty:
            logger.warning("没有基金分红排行数据需要保存")
            return 0
        
        try:
            # 清理无效的浮点数值（NaN, Infinity等），防止JSON序列化错误
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条基金分红排行数据...")
            
            # 分批处理，每批500条
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            logger.info(f"📦 将分 {total_batches} 批次处理，每批 {batch_size} 条")
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                logger.info(f"📝 处理第 {batch_idx + 1}/{total_batches} 批，记录范围: {start_idx + 1}-{end_idx}")
                
                # 构建批量操作
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    # 清理NaN/Infinity值
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        # 转换 datetime.date 对象为字符串
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        # 转换 datetime.datetime 对象为字符串
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    # 添加元数据
                    fund_code = str(doc.get('基金代码', ''))
                    doc['code'] = fund_code
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_fh_rank_em'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    # 使用基金代码作为唯一标识
                    ops.append(
                        UpdateOne(
                            {'code': fund_code},
                            {'$set': doc},
                            upsert=True
                        )
                    )
                
                # 执行批量写入
                if ops:
                    result = await self.col_fund_fh_rank_em.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    logger.info(
                        f"✅ 第 {batch_idx + 1}/{total_batches} 批写入完成: "
                        f"新增={result.upserted_count}, 更新={result.matched_count}, "
                        f"本批保存={batch_saved}, 累计={total_saved}/{total_count}"
                    )
                    
                    # 调用进度回调（如果提供）
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条基金分红排行数据")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存基金分红排行数据失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_fh_rank_em_data(self) -> int:
        """
        清空基金分红排行数据
        
        Returns:
            删除的记录数
        """
        try:
            result = await self.col_fund_fh_rank_em.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条基金分红排行数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空基金分红排行数据失败: {e}", exc_info=True)
            raise
    
    async def get_fund_fh_rank_em_stats(self) -> Dict[str, Any]:
        """
        获取基金分红排行统计
        
        Returns:
            统计信息字典
        """
        try:
            total_count = await self.col_fund_fh_rank_em.count_documents({})
            
            # 获取最早和最晚的成立日期
            earliest_date = None
            latest_date = None
            pipeline_date = [
                {
                    '$group': {
                        '_id': None,
                        'earliest': {'$min': '$成立日期'},
                        'latest': {'$max': '$成立日期'}
                    }
                }
            ]
            
            async for doc in self.col_fund_fh_rank_em.aggregate(pipeline_date):
                earliest_date = doc.get('earliest')
                latest_date = doc.get('latest')
            
            # 获取累计分红TOP10
            pipeline_top_dividend = [
                {
                    '$sort': {'累计分红': -1}
                },
                {
                    '$limit': 10
                },
                {
                    '$project': {
                        'code': '$基金代码',
                        'name': '$基金简称',
                        'total_dividend': '$累计分红',
                        'dividend_times': '$累计次数'
                    }
                }
            ]
            
            top_dividend = []
            async for doc in self.col_fund_fh_rank_em.aggregate(pipeline_top_dividend):
                top_dividend.append({
                    'code': doc.get('code'),
                    'name': doc.get('name'),
                    'total_dividend': doc.get('total_dividend'),
                    'dividend_times': doc.get('dividend_times')
                })
            
            # 获取累计次数TOP10
            pipeline_top_times = [
                {
                    '$sort': {'累计次数': -1}
                },
                {
                    '$limit': 10
                },
                {
                    '$project': {
                        'code': '$基金代码',
                        'name': '$基金简称',
                        'total_dividend': '$累计分红',
                        'dividend_times': '$累计次数'
                    }
                }
            ]
            
            top_times = []
            async for doc in self.col_fund_fh_rank_em.aggregate(pipeline_top_times):
                top_times.append({
                    'code': doc.get('code'),
                    'name': doc.get('name'),
                    'total_dividend': doc.get('total_dividend'),
                    'dividend_times': doc.get('dividend_times')
                })
            
            return {
                'total_count': total_count,
                'earliest_date': earliest_date,
                'latest_date': latest_date,
                'top_dividend': top_dividend,
                'top_times': top_times
            }
        except Exception as e:
            logger.error(f"获取基金分红排行统计失败: {e}", exc_info=True)
            raise
    
    async def save_fund_open_fund_rank_em_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """
        保存开放式基金排行数据到MongoDB
        
        Args:
            df: 包含开放式基金排行信息的DataFrame
            progress_callback: 进度回调函数
            
        Returns:
            保存的记录数
        """
        if df is None or df.empty:
            logger.warning("没有开放式基金排行数据需要保存")
            return 0
        
        try:
            # 清理无效的浮点数值（NaN, Infinity等），防止JSON序列化错误
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条开放式基金排行数据...")
            
            # 分批处理，每批500条
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            logger.info(f"📦 将分 {total_batches} 批次处理，每批 {batch_size} 条")
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                logger.info(f"📝 处理第 {batch_idx + 1}/{total_batches} 批，记录范围: {start_idx + 1}-{end_idx}")
                
                # 构建批量操作
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    # 清理NaN/Infinity值
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        # 转换 datetime.date 对象为字符串
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        # 转换 datetime.datetime 对象为字符串
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    # 添加元数据
                    fund_code = str(doc.get('基金代码', ''))
                    date_str = str(doc.get('日期', ''))
                    doc['code'] = fund_code
                    doc['date'] = date_str
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_open_fund_rank_em'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    # 使用基金代码和日期作为唯一标识
                    ops.append(
                        UpdateOne(
                            {'code': fund_code, 'date': date_str},
                            {'$set': doc},
                            upsert=True
                        )
                    )
                
                # 执行批量写入
                if ops:
                    result = await self.col_fund_open_fund_rank_em.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    logger.info(
                        f"✅ 第 {batch_idx + 1}/{total_batches} 批写入完成: "
                        f"新增={result.upserted_count}, 更新={result.matched_count}, "
                        f"本批保存={batch_saved}, 累计={total_saved}/{total_count}"
                    )
                    
                    # 调用进度回调（如果提供）
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条开放式基金排行数据")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存开放式基金排行数据失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_open_fund_rank_em_data(self) -> int:
        """
        清空开放式基金排行数据
        
        Returns:
            删除的记录数
        """
        try:
            result = await self.col_fund_open_fund_rank_em.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条开放式基金排行数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空开放式基金排行数据失败: {e}", exc_info=True)
            raise
    
    async def get_fund_open_fund_rank_em_stats(self) -> Dict[str, Any]:
        """
        获取开放式基金排行统计
        
        Returns:
            统计信息字典
        """
        try:
            total_count = await self.col_fund_open_fund_rank_em.count_documents({})
            
            # 获取最早和最晚的日期
            earliest_date = None
            latest_date = None
            pipeline_date = [
                {
                    '$group': {
                        '_id': None,
                        'earliest': {'$min': '$日期'},
                        'latest': {'$max': '$日期'}
                    }
                }
            ]
            
            async for doc in self.col_fund_open_fund_rank_em.aggregate(pipeline_date):
                earliest_date = doc.get('earliest')
                latest_date = doc.get('latest')
            
            # 获取近1年收益率TOP10
            pipeline_top_1year = [
                {
                    '$match': {'近1年': {'$ne': None}}
                },
                {
                    '$sort': {'近1年': -1}
                },
                {
                    '$limit': 10
                },
                {
                    '$project': {
                        'code': '$基金代码',
                        'name': '$基金简称',
                        'return_1year': '$近1年',
                        'return_ytd': '$今年来'
                    }
                }
            ]
            
            top_performers = []
            async for doc in self.col_fund_open_fund_rank_em.aggregate(pipeline_top_1year):
                top_performers.append({
                    'code': doc.get('code'),
                    'name': doc.get('name'),
                    'return_1year': doc.get('return_1year'),
                    'return_ytd': doc.get('return_ytd')
                })
            
            # 获取今年来收益率TOP10
            pipeline_top_ytd = [
                {
                    '$match': {'今年来': {'$ne': None}}
                },
                {
                    '$sort': {'今年来': -1}
                },
                {
                    '$limit': 10
                },
                {
                    '$project': {
                        'code': '$基金代码',
                        'name': '$基金简称',
                        'return_ytd': '$今年来',
                        'return_1year': '$近1年'
                    }
                }
            ]
            
            top_ytd = []
            async for doc in self.col_fund_open_fund_rank_em.aggregate(pipeline_top_ytd):
                top_ytd.append({
                    'code': doc.get('code'),
                    'name': doc.get('name'),
                    'return_ytd': doc.get('return_ytd'),
                    'return_1year': doc.get('return_1year')
                })
            
            return {
                'total_count': total_count,
                'earliest_date': earliest_date,
                'latest_date': latest_date,
                'top_performers': top_performers,
                'top_ytd': top_ytd
            }
        except Exception as e:
            logger.error(f"获取开放式基金排行统计失败: {e}", exc_info=True)
            raise
    
    async def save_fund_exchange_rank_em_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存场内交易基金排行数据到MongoDB"""
        if df is None or df.empty:
            logger.warning("没有场内交易基金排行数据需要保存")
            return 0
        
        try:
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条场内交易基金排行数据...")
            
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    fund_code = str(doc.get('基金代码', ''))
                    date_str = str(doc.get('日期', ''))
                    doc['code'] = fund_code
                    doc['date'] = date_str
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_exchange_rank_em'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    ops.append(
                        UpdateOne(
                            {'code': fund_code, 'date': date_str},
                            {'$set': doc},
                            upsert=True
                        )
                    )
                
                if ops:
                    result = await self.col_fund_exchange_rank_em.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条场内交易基金排行数据")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存场内交易基金排行数据失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_exchange_rank_em_data(self) -> int:
        """清空场内交易基金排行数据"""
        try:
            result = await self.col_fund_exchange_rank_em.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条场内交易基金排行数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空场内交易基金排行数据失败: {e}", exc_info=True)
            raise
    
    async def get_fund_exchange_rank_em_stats(self) -> Dict[str, Any]:
        """获取场内交易基金排行统计"""
        try:
            total_count = await self.col_fund_exchange_rank_em.count_documents({})
            
            pipeline_date = [
                {'$group': {'_id': None, 'earliest': {'$min': '$日期'}, 'latest': {'$max': '$日期'}}}
            ]
            
            earliest_date = None
            latest_date = None
            async for doc in self.col_fund_exchange_rank_em.aggregate(pipeline_date):
                earliest_date = doc.get('earliest')
                latest_date = doc.get('latest')
            
            pipeline_type = [
                {'$group': {'_id': '$类型', 'count': {'$sum': 1}}},
                {'$sort': {'count': -1}}
            ]
            
            type_stats = []
            async for doc in self.col_fund_exchange_rank_em.aggregate(pipeline_type):
                type_stats.append({'type': doc['_id'], 'count': doc['count']})
            
            pipeline_top = [
                {'$match': {'近1年': {'$ne': None}}},
                {'$sort': {'近1年': -1}},
                {'$limit': 10},
                {'$project': {'code': '$基金代码', 'name': '$基金简称', 'type': '$类型', 'return_1year': '$近1年'}}
            ]
            
            top_performers = []
            async for doc in self.col_fund_exchange_rank_em.aggregate(pipeline_top):
                top_performers.append({
                    'code': doc.get('code'),
                    'name': doc.get('name'),
                    'type': doc.get('type'),
                    'return_1year': doc.get('return_1year')
                })
            
            return {
                'total_count': total_count,
                'earliest_date': earliest_date,
                'latest_date': latest_date,
                'type_stats': type_stats,
                'top_performers': top_performers
            }
        except Exception as e:
            logger.error(f"获取场内交易基金排行统计失败: {e}", exc_info=True)
            raise
    
    async def save_fund_money_rank_em_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存货币型基金排行数据到MongoDB"""
        if df is None or df.empty:
            logger.warning("没有货币型基金排行数据需要保存")
            return 0
        
        try:
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条货币型基金排行数据...")
            
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    fund_code = str(doc.get('基金代码', ''))
                    date_str = str(doc.get('日期', ''))
                    doc['code'] = fund_code
                    doc['date'] = date_str
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_money_rank_em'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    ops.append(
                        UpdateOne(
                            {'code': fund_code, 'date': date_str},
                            {'$set': doc},
                            upsert=True
                        )
                    )
                
                if ops:
                    result = await self.col_fund_money_rank_em.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条货币型基金排行数据")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存货币型基金排行数据失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_money_rank_em_data(self) -> int:
        """清空货币型基金排行数据"""
        try:
            result = await self.col_fund_money_rank_em.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条货币型基金排行数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空货币型基金排行数据失败: {e}", exc_info=True)
            raise
    
    async def get_fund_money_rank_em_stats(self) -> Dict[str, Any]:
        """获取货币型基金排行统计"""
        try:
            total_count = await self.col_fund_money_rank_em.count_documents({})
            
            pipeline_date = [
                {'$group': {'_id': None, 'earliest': {'$min': '$日期'}, 'latest': {'$max': '$日期'}}}
            ]
            
            earliest_date = None
            latest_date = None
            async for doc in self.col_fund_money_rank_em.aggregate(pipeline_date):
                earliest_date = doc.get('earliest')
                latest_date = doc.get('latest')
            
            # 获取年化收益率7日TOP10
            pipeline_top_7d = [
                {'$match': {'年化收益率7日': {'$ne': None}}},
                {'$sort': {'年化收益率7日': -1}},
                {'$limit': 10},
                {'$project': {
                    'code': '$基金代码',
                    'name': '$基金简称',
                    'yield_7d': '$年化收益率7日',
                    'yield_10k': '$万份收益'
                }}
            ]
            
            top_yield_7d = []
            async for doc in self.col_fund_money_rank_em.aggregate(pipeline_top_7d):
                top_yield_7d.append({
                    'code': doc.get('code'),
                    'name': doc.get('name'),
                    'yield_7d': doc.get('yield_7d'),
                    'yield_10k': doc.get('yield_10k')
                })
            
            # 获取近1年收益TOP10
            pipeline_top_1y = [
                {'$match': {'近1年': {'$ne': None}}},
                {'$sort': {'近1年': -1}},
                {'$limit': 10},
                {'$project': {
                    'code': '$基金代码',
                    'name': '$基金简称',
                    'return_1y': '$近1年',
                    'yield_7d': '$年化收益率7日'
                }}
            ]
            
            top_return_1y = []
            async for doc in self.col_fund_money_rank_em.aggregate(pipeline_top_1y):
                top_return_1y.append({
                    'code': doc.get('code'),
                    'name': doc.get('name'),
                    'return_1y': doc.get('return_1y'),
                    'yield_7d': doc.get('yield_7d')
                })
            
            return {
                'total_count': total_count,
                'earliest_date': earliest_date,
                'latest_date': latest_date,
                'top_yield_7d': top_yield_7d,
                'top_return_1y': top_return_1y
            }
        except Exception as e:
            logger.error(f"获取货币型基金排行统计失败: {e}", exc_info=True)
            raise
    
    async def save_fund_lcx_rank_em_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存理财基金排行数据到MongoDB"""
        if df is None or df.empty:
            logger.warning("没有理财基金排行数据需要保存")
            return 0
        
        try:
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条理财基金排行数据...")
            
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    fund_code = str(doc.get('基金代码', ''))
                    date_str = str(doc.get('日期', ''))
                    doc['code'] = fund_code
                    doc['date'] = date_str
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_lcx_rank_em'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    ops.append(
                        UpdateOne(
                            {'code': fund_code, 'date': date_str},
                            {'$set': doc},
                            upsert=True
                        )
                    )
                
                if ops:
                    result = await self.col_fund_lcx_rank_em.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条理财基金排行数据")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存理财基金排行数据失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_lcx_rank_em_data(self) -> int:
        """清空理财基金排行数据"""
        try:
            result = await self.col_fund_lcx_rank_em.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条理财基金排行数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空理财基金排行数据失败: {e}", exc_info=True)
            raise
    
    async def get_fund_lcx_rank_em_stats(self) -> Dict[str, Any]:
        """获取理财基金排行统计"""
        try:
            total_count = await self.col_fund_lcx_rank_em.count_documents({})
            
            pipeline_date = [
                {'$group': {'_id': None, 'earliest': {'$min': '$日期'}, 'latest': {'$max': '$日期'}}}
            ]
            
            earliest_date = None
            latest_date = None
            async for doc in self.col_fund_lcx_rank_em.aggregate(pipeline_date):
                earliest_date = doc.get('earliest')
                latest_date = doc.get('latest')
            
            # 获取年化收益率7日TOP10
            pipeline_top_7d = [
                {'$match': {'年化收益率7日': {'$ne': None}}},
                {'$sort': {'年化收益率7日': -1}},
                {'$limit': 10},
                {'$project': {
                    'code': '$基金代码',
                    'name': '$基金简称',
                    'yield_7d': '$年化收益率7日',
                    'yield_10k': '$万份收益',
                    'purchasable': '$可购买'
                }}
            ]
            
            top_yield_7d = []
            async for doc in self.col_fund_lcx_rank_em.aggregate(pipeline_top_7d):
                top_yield_7d.append({
                    'code': doc.get('code'),
                    'name': doc.get('name'),
                    'yield_7d': doc.get('yield_7d'),
                    'yield_10k': doc.get('yield_10k'),
                    'purchasable': doc.get('purchasable')
                })
            
            # 获取成立来收益TOP10
            pipeline_top_since = [
                {'$match': {'成立来': {'$ne': None}}},
                {'$sort': {'成立来': -1}},
                {'$limit': 10},
                {'$project': {
                    'code': '$基金代码',
                    'name': '$基金简称',
                    'return_since': '$成立来',
                    'yield_7d': '$年化收益率7日',
                    'purchasable': '$可购买'
                }}
            ]
            
            top_return_since = []
            async for doc in self.col_fund_lcx_rank_em.aggregate(pipeline_top_since):
                top_return_since.append({
                    'code': doc.get('code'),
                    'name': doc.get('name'),
                    'return_since': doc.get('return_since'),
                    'yield_7d': doc.get('yield_7d'),
                    'purchasable': doc.get('purchasable')
                })
            
            return {
                'total_count': total_count,
                'earliest_date': earliest_date,
                'latest_date': latest_date,
                'top_yield_7d': top_yield_7d,
                'top_return_since': top_return_since
            }
        except Exception as e:
            logger.error(f"获取理财基金排行统计失败: {e}", exc_info=True)
            raise
    
    async def save_fund_hk_rank_em_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存香港基金排行数据到MongoDB"""
        if df is None or df.empty:
            logger.warning("没有香港基金排行数据需要保存")
            return 0
        
        try:
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条香港基金排行数据...")
            
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    fund_code = str(doc.get('基金代码', ''))
                    date_str = str(doc.get('日期', ''))
                    doc['code'] = fund_code
                    doc['date'] = date_str
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_hk_rank_em'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    ops.append(
                        UpdateOne(
                            {'code': fund_code, 'date': date_str},
                            {'$set': doc},
                            upsert=True
                        )
                    )
                
                if ops:
                    result = await self.col_fund_hk_rank_em.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条香港基金排行数据")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存香港基金排行数据失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_hk_rank_em_data(self) -> int:
        """清空香港基金排行数据"""
        try:
            result = await self.col_fund_hk_rank_em.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条香港基金排行数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空香港基金排行数据失败: {e}", exc_info=True)
            raise
    
    async def get_fund_hk_rank_em_stats(self) -> Dict[str, Any]:
        """获取香港基金排行统计"""
        try:
            total_count = await self.col_fund_hk_rank_em.count_documents({})
            
            pipeline_date = [
                {'$group': {'_id': None, 'earliest': {'$min': '$日期'}, 'latest': {'$max': '$日期'}}}
            ]
            
            earliest_date = None
            latest_date = None
            async for doc in self.col_fund_hk_rank_em.aggregate(pipeline_date):
                earliest_date = doc.get('earliest')
                latest_date = doc.get('latest')
            
            # 获取币种分布统计
            pipeline_currency = [
                {'$group': {'_id': '$币种', 'count': {'$sum': 1}}},
                {'$sort': {'count': -1}}
            ]
            
            currency_stats = []
            async for doc in self.col_fund_hk_rank_em.aggregate(pipeline_currency):
                currency_stats.append({
                    'currency': doc.get('_id'),
                    'count': doc.get('count')
                })
            
            # 获取近1年收益TOP10
            pipeline_top_1y = [
                {'$match': {'近1年': {'$ne': None}}},
                {'$sort': {'近1年': -1}},
                {'$limit': 10},
                {'$project': {
                    'code': '$基金代码',
                    'name': '$基金简称',
                    'currency': '$币种',
                    'return_1y': '$近1年',
                    'nav': '$单位净值',
                    'purchasable': '$可购买'
                }}
            ]
            
            top_return_1y = []
            async for doc in self.col_fund_hk_rank_em.aggregate(pipeline_top_1y):
                top_return_1y.append({
                    'code': doc.get('code'),
                    'name': doc.get('name'),
                    'currency': doc.get('currency'),
                    'return_1y': doc.get('return_1y'),
                    'nav': doc.get('nav'),
                    'purchasable': doc.get('purchasable')
                })
            
            # 获取成立来收益TOP10
            pipeline_top_since = [
                {'$match': {'成立来': {'$ne': None}}},
                {'$sort': {'成立来': -1}},
                {'$limit': 10},
                {'$project': {
                    'code': '$基金代码',
                    'name': '$基金简称',
                    'currency': '$币种',
                    'return_since': '$成立来',
                    'purchasable': '$可购买'
                }}
            ]
            
            top_return_since = []
            async for doc in self.col_fund_hk_rank_em.aggregate(pipeline_top_since):
                top_return_since.append({
                    'code': doc.get('code'),
                    'name': doc.get('name'),
                    'currency': doc.get('currency'),
                    'return_since': doc.get('return_since'),
                    'purchasable': doc.get('purchasable')
                })
            
            return {
                'total_count': total_count,
                'earliest_date': earliest_date,
                'latest_date': latest_date,
                'currency_stats': currency_stats,
                'top_return_1y': top_return_1y,
                'top_return_since': top_return_since
            }
        except Exception as e:
            logger.error(f"获取香港基金排行统计失败: {e}", exc_info=True)
            raise
    
    async def save_fund_individual_achievement_xq_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存基金业绩数据到MongoDB"""
        if df is None or df.empty:
            logger.warning("没有基金业绩数据需要保存")
            return 0
        
        try:
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条基金业绩数据...")
            
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    fund_code = str(doc.get('基金代码', ''))
                    perf_type = str(doc.get('业绩类型', ''))
                    period = str(doc.get('周期', ''))
                    doc['code'] = fund_code
                    doc['performance_type'] = perf_type
                    doc['period'] = period
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_individual_achievement_xq'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    ops.append(
                        UpdateOne(
                            {'code': fund_code, 'performance_type': perf_type, 'period': period},
                            {'$set': doc},
                            upsert=True
                        )
                    )
                
                if ops:
                    result = await self.col_fund_individual_achievement_xq.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条基金业绩数据")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存基金业绩数据失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_individual_achievement_xq_data(self) -> int:
        """清空基金业绩数据"""
        try:
            result = await self.col_fund_individual_achievement_xq.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条基金业绩数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空基金业绩数据失败: {e}", exc_info=True)
            raise
    
    async def get_fund_individual_achievement_xq_stats(self) -> Dict[str, Any]:
        """获取基金业绩统计"""
        try:
            total_count = await self.col_fund_individual_achievement_xq.count_documents({})
            
            # 获取唯一基金数量
            pipeline_funds = [
                {'$group': {'_id': '$code'}},
                {'$count': 'unique_funds'}
            ]
            
            unique_funds = 0
            async for doc in self.col_fund_individual_achievement_xq.aggregate(pipeline_funds):
                unique_funds = doc.get('unique_funds', 0)
            
            # 获取业绩类型分布
            pipeline_types = [
                {'$group': {'_id': '$业绩类型', 'count': {'$sum': 1}}},
                {'$sort': {'count': -1}}
            ]
            
            performance_types = []
            async for doc in self.col_fund_individual_achievement_xq.aggregate(pipeline_types):
                performance_types.append({
                    'type': doc.get('_id'),
                    'count': doc.get('count')
                })
            
            # 获取成立以来收益TOP10
            pipeline_top_return = [
                {'$match': {'周期': '成立以来', '本产品区间收益': {'$ne': None}}},
                {'$sort': {'本产品区间收益': -1}},
                {'$limit': 10},
                {'$project': {
                    'code': '$基金代码',
                    'return': '$本产品区间收益',
                    'max_drawdown': '$本产品最大回撒',
                    'ranking': '$周期收益同类排名'
                }}
            ]
            
            top_return_since = []
            async for doc in self.col_fund_individual_achievement_xq.aggregate(pipeline_top_return):
                top_return_since.append({
                    'code': doc.get('code'),
                    'return': doc.get('return'),
                    'max_drawdown': doc.get('max_drawdown'),
                    'ranking': doc.get('ranking')
                })
            
            # 获取最小回撤TOP10(成立以来)
            pipeline_min_drawdown = [
                {'$match': {'周期': '成立以来', '本产品最大回撒': {'$ne': None}}},
                {'$sort': {'本产品最大回撒': 1}},
                {'$limit': 10},
                {'$project': {
                    'code': '$基金代码',
                    'return': '$本产品区间收益',
                    'max_drawdown': '$本产品最大回撒',
                    'ranking': '$周期收益同类排名'
                }}
            ]
            
            min_drawdown_since = []
            async for doc in self.col_fund_individual_achievement_xq.aggregate(pipeline_min_drawdown):
                min_drawdown_since.append({
                    'code': doc.get('code'),
                    'return': doc.get('return'),
                    'max_drawdown': doc.get('max_drawdown'),
                    'ranking': doc.get('ranking')
                })
            
            return {
                'total_count': total_count,
                'unique_funds': unique_funds,
                'performance_types': performance_types,
                'top_return_since': top_return_since,
                'min_drawdown_since': min_drawdown_since
            }
        except Exception as e:
            logger.error(f"获取基金业绩统计失败: {e}", exc_info=True)
            raise
    
    async def save_fund_value_estimation_em_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存净值估算数据到MongoDB"""
        if df is None or df.empty:
            logger.warning("没有净值估算数据需要保存")
            return 0
        
        try:
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条净值估算数据...")
            
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    fund_code = str(doc.get('基金代码', ''))
                    trade_date = str(doc.get('交易日', ''))
                    doc['code'] = fund_code
                    doc['trade_date'] = trade_date
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_value_estimation_em'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    ops.append(
                        UpdateOne(
                            {'code': fund_code, 'trade_date': trade_date},
                            {'$set': doc},
                            upsert=True
                        )
                    )
                
                if ops:
                    result = await self.col_fund_value_estimation_em.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条净值估算数据")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存净值估算数据失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_value_estimation_em_data(self) -> int:
        """清空净值估算数据"""
        try:
            result = await self.col_fund_value_estimation_em.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条净值估算数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空净值估算数据失败: {e}", exc_info=True)
            raise
    
    async def get_fund_value_estimation_em_stats(self) -> Dict[str, Any]:
        """获取净值估算统计"""
        try:
            total_count = await self.col_fund_value_estimation_em.count_documents({})
            
            # 获取交易日范围
            pipeline_date = [
                {'$group': {'_id': None, 'earliest': {'$min': '$交易日'}, 'latest': {'$max': '$交易日'}}}
            ]
            
            earliest_date = None
            latest_date = None
            async for doc in self.col_fund_value_estimation_em.aggregate(pipeline_date):
                earliest_date = doc.get('earliest')
                latest_date = doc.get('latest')
            
            # 获取估算增长率TOP10
            pipeline_top_growth = [
                {'$match': {'交易日-估算数据-估算增长率': {'$ne': None}}},
                {'$sort': {'交易日-估算数据-估算增长率': -1}},
                {'$limit': 10},
                {'$project': {
                    'code': '$基金代码',
                    'name': '$基金名称',
                    'estimated_value': '$交易日-估算数据-估算值',
                    'estimated_growth': '$交易日-估算数据-估算增长率',
                    'published_nav': '$交易日-公布数据-单位净值',
                    'deviation': '$估算偏差'
                }}
            ]
            
            top_estimated_growth = []
            async for doc in self.col_fund_value_estimation_em.aggregate(pipeline_top_growth):
                top_estimated_growth.append({
                    'code': doc.get('code'),
                    'name': doc.get('name'),
                    'estimated_value': doc.get('estimated_value'),
                    'estimated_growth': doc.get('estimated_growth'),
                    'published_nav': doc.get('published_nav'),
                    'deviation': doc.get('deviation')
                })
            
            # 获取估算偏差最小TOP10（绝对值）
            pipeline_min_deviation = [
                {'$match': {'估算偏差': {'$ne': None}}},
                {'$addFields': {'abs_deviation': {'$abs': '$估算偏差'}}},
                {'$sort': {'abs_deviation': 1}},
                {'$limit': 10},
                {'$project': {
                    'code': '$基金代码',
                    'name': '$基金名称',
                    'estimated_value': '$交易日-估算数据-估算值',
                    'estimated_growth': '$交易日-估算数据-估算增长率',
                    'published_nav': '$交易日-公布数据-单位净值',
                    'deviation': '$估算偏差'
                }}
            ]
            
            min_deviation_funds = []
            async for doc in self.col_fund_value_estimation_em.aggregate(pipeline_min_deviation):
                min_deviation_funds.append({
                    'code': doc.get('code'),
                    'name': doc.get('name'),
                    'estimated_value': doc.get('estimated_value'),
                    'estimated_growth': doc.get('estimated_growth'),
                    'published_nav': doc.get('published_nav'),
                    'deviation': doc.get('deviation')
                })
            
            return {
                'total_count': total_count,
                'earliest_date': earliest_date,
                'latest_date': latest_date,
                'top_estimated_growth': top_estimated_growth,
                'min_deviation_funds': min_deviation_funds
            }
        except Exception as e:
            logger.error(f"获取净值估算统计失败: {e}", exc_info=True)
            raise
    
    async def save_fund_individual_analysis_xq_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存基金数据分析到MongoDB"""
        if df is None or df.empty:
            logger.warning("没有基金数据分析需要保存")
            return 0
        
        try:
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条基金数据分析...")
            
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    fund_code = str(doc.get('基金代码', ''))
                    period = str(doc.get('周期', ''))
                    doc['code'] = fund_code
                    doc['period'] = period
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_individual_analysis_xq'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    ops.append(
                        UpdateOne(
                            {'code': fund_code, 'period': period},
                            {'$set': doc},
                            upsert=True
                        )
                    )
                
                if ops:
                    result = await self.col_fund_individual_analysis_xq.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条基金数据分析")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存基金数据分析失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_individual_analysis_xq_data(self) -> int:
        """清空基金数据分析"""
        try:
            result = await self.col_fund_individual_analysis_xq.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条基金数据分析")
            return deleted_count
        except Exception as e:
            logger.error(f"清空基金数据分析失败: {e}", exc_info=True)
            raise
    
    async def get_fund_individual_analysis_xq_stats(self) -> Dict[str, Any]:
        """获取基金数据分析统计"""
        try:
            total_count = await self.col_fund_individual_analysis_xq.count_documents({})
            
            # 获取唯一基金数
            unique_funds = await self.col_fund_individual_analysis_xq.distinct('code')
            
            # 获取周期分布
            pipeline_periods = [
                {'$group': {'_id': '$周期', 'count': {'$sum': 1}}},
                {'$sort': {'count': -1}}
            ]
            
            period_distribution = []
            async for doc in self.col_fund_individual_analysis_xq.aggregate(pipeline_periods):
                period_distribution.append({
                    'period': doc['_id'],
                    'count': doc['count']
                })
            
            # 获取年化夏普比率TOP10
            pipeline_top_sharpe = [
                {'$match': {'年化夏普比率': {'$ne': None}}},
                {'$sort': {'年化夏普比率': -1}},
                {'$limit': 10},
                {'$project': {
                    'code': '$code',
                    'period': '$周期',
                    'sharpe_ratio': '$年化夏普比率',
                    'volatility': '$年化波动率',
                    'max_drawdown': '$最大回撤',
                    'risk_return_ratio': '$较同类风险收益比'
                }}
            ]
            
            top_sharpe_ratio = []
            async for doc in self.col_fund_individual_analysis_xq.aggregate(pipeline_top_sharpe):
                top_sharpe_ratio.append({
                    'code': doc.get('code'),
                    'period': doc.get('period'),
                    'sharpe_ratio': doc.get('sharpe_ratio'),
                    'volatility': doc.get('volatility'),
                    'max_drawdown': doc.get('max_drawdown'),
                    'risk_return_ratio': doc.get('risk_return_ratio')
                })
            
            # 获取最小回撤TOP10（最大回撤的绝对值最小）
            pipeline_min_drawdown = [
                {'$match': {'最大回撤': {'$ne': None}}},
                {'$addFields': {'abs_drawdown': {'$abs': '$最大回撤'}}},
                {'$sort': {'abs_drawdown': 1}},
                {'$limit': 10},
                {'$project': {
                    'code': '$code',
                    'period': '$周期',
                    'max_drawdown': '$最大回撤',
                    'sharpe_ratio': '$年化夏普比率',
                    'volatility': '$年化波动率',
                    'anti_risk': '$较同类抗风险波动'
                }}
            ]
            
            min_drawdown_funds = []
            async for doc in self.col_fund_individual_analysis_xq.aggregate(pipeline_min_drawdown):
                min_drawdown_funds.append({
                    'code': doc.get('code'),
                    'period': doc.get('period'),
                    'max_drawdown': doc.get('max_drawdown'),
                    'sharpe_ratio': doc.get('sharpe_ratio'),
                    'volatility': doc.get('volatility'),
                    'anti_risk': doc.get('anti_risk')
                })
            
            return {
                'total_count': total_count,
                'unique_funds': len(unique_funds),
                'period_distribution': period_distribution,
                'top_sharpe_ratio': top_sharpe_ratio,
                'min_drawdown_funds': min_drawdown_funds
            }
        except Exception as e:
            logger.error(f"获取基金数据分析统计失败: {e}", exc_info=True)
            raise
    
    async def save_fund_individual_profit_probability_xq_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存基金盈利概率到MongoDB"""
        if df is None or df.empty:
            logger.warning("没有基金盈利概率需要保存")
            return 0
        
        try:
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条基金盈利概率...")
            
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    fund_code = str(doc.get('基金代码', ''))
                    holding_period = str(doc.get('持有时长', ''))
                    doc['code'] = fund_code
                    doc['holding_period'] = holding_period
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_individual_profit_probability_xq'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    ops.append(
                        UpdateOne(
                            {'code': fund_code, 'holding_period': holding_period},
                            {'$set': doc},
                            upsert=True
                        )
                    )
                
                if ops:
                    result = await self.col_fund_individual_profit_probability_xq.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条基金盈利概率")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存基金盈利概率失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_individual_profit_probability_xq_data(self) -> int:
        """清空基金盈利概率"""
        try:
            result = await self.col_fund_individual_profit_probability_xq.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条基金盈利概率")
            return deleted_count
        except Exception as e:
            logger.error(f"清空基金盈利概率失败: {e}", exc_info=True)
            raise
    
    async def get_fund_individual_profit_probability_xq_stats(self) -> Dict[str, Any]:
        """获取基金盈利概率统计"""
        try:
            total_count = await self.col_fund_individual_profit_probability_xq.count_documents({})
            
            # 获取唯一基金数
            unique_funds = await self.col_fund_individual_profit_probability_xq.distinct('code')
            
            # 获取持有时长分布
            pipeline_periods = [
                {'$group': {'_id': '$持有时长', 'count': {'$sum': 1}}},
                {'$sort': {'count': -1}}
            ]
            
            holding_period_distribution = []
            async for doc in self.col_fund_individual_profit_probability_xq.aggregate(pipeline_periods):
                holding_period_distribution.append({
                    'holding_period': doc['_id'],
                    'count': doc['count']
                })
            
            # 获取盈利概率TOP10（长期持有）
            pipeline_top_probability = [
                {'$match': {'盈利概率': {'$ne': None}}},
                {'$sort': {'盈利概率': -1}},
                {'$limit': 10},
                {'$project': {
                    'code': '$code',
                    'holding_period': '$持有时长',
                    'profit_probability': '$盈利概率',
                    'average_return': '$平均收益'
                }}
            ]
            
            top_profit_probability = []
            async for doc in self.col_fund_individual_profit_probability_xq.aggregate(pipeline_top_probability):
                top_profit_probability.append({
                    'code': doc.get('code'),
                    'holding_period': doc.get('holding_period'),
                    'profit_probability': doc.get('profit_probability'),
                    'average_return': doc.get('average_return')
                })
            
            # 获取平均收益TOP10
            pipeline_top_return = [
                {'$match': {'平均收益': {'$ne': None}}},
                {'$sort': {'平均收益': -1}},
                {'$limit': 10},
                {'$project': {
                    'code': '$code',
                    'holding_period': '$持有时长',
                    'profit_probability': '$盈利概率',
                    'average_return': '$平均收益'
                }}
            ]
            
            top_average_return = []
            async for doc in self.col_fund_individual_profit_probability_xq.aggregate(pipeline_top_return):
                top_average_return.append({
                    'code': doc.get('code'),
                    'holding_period': doc.get('holding_period'),
                    'profit_probability': doc.get('profit_probability'),
                    'average_return': doc.get('average_return')
                })
            
            return {
                'total_count': total_count,
                'unique_funds': len(unique_funds),
                'holding_period_distribution': holding_period_distribution,
                'top_profit_probability': top_profit_probability,
                'top_average_return': top_average_return
            }
        except Exception as e:
            logger.error(f"获取基金盈利概率统计失败: {e}", exc_info=True)
            raise
    
    async def save_fund_individual_detail_hold_xq_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存基金持仓资产比例到MongoDB"""
        if df is None or df.empty:
            logger.warning("没有基金持仓资产比例需要保存")
            return 0
        
        try:
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条基金持仓资产比例...")
            
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    fund_code = str(doc.get('基金代码', ''))
                    date_str = str(doc.get('日期', ''))
                    asset_type = str(doc.get('资产类型', ''))
                    doc['code'] = fund_code
                    doc['date'] = date_str
                    doc['asset_type'] = asset_type
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_individual_detail_hold_xq'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    ops.append(
                        UpdateOne(
                            {'code': fund_code, 'date': date_str, 'asset_type': asset_type},
                            {'$set': doc},
                            upsert=True
                        )
                    )
                
                if ops:
                    result = await self.col_fund_individual_detail_hold_xq.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条基金持仓资产比例")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存基金持仓资产比例失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_individual_detail_hold_xq_data(self) -> int:
        """清空基金持仓资产比例"""
        try:
            result = await self.col_fund_individual_detail_hold_xq.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条基金持仓资产比例")
            return deleted_count
        except Exception as e:
            logger.error(f"清空基金持仓资产比例失败: {e}", exc_info=True)
            raise
    
    async def get_fund_individual_detail_hold_xq_stats(self) -> Dict[str, Any]:
        """获取基金持仓资产比例统计"""
        try:
            total_count = await self.col_fund_individual_detail_hold_xq.count_documents({})
            
            # 获取唯一基金数
            unique_funds = await self.col_fund_individual_detail_hold_xq.distinct('code')
            
            # 获取唯一日期数
            unique_dates = await self.col_fund_individual_detail_hold_xq.distinct('date')
            
            # 获取资产类型分布
            pipeline_asset_types = [
                {'$group': {'_id': '$资产类型', 'count': {'$sum': 1}, 'avg_position': {'$avg': '$仓位占比'}}},
                {'$sort': {'count': -1}}
            ]
            
            asset_type_distribution = []
            async for doc in self.col_fund_individual_detail_hold_xq.aggregate(pipeline_asset_types):
                asset_type_distribution.append({
                    'asset_type': doc['_id'],
                    'count': doc['count'],
                    'avg_position': round(doc.get('avg_position', 0), 2) if doc.get('avg_position') else None
                })
            
            # 获取最新日期
            pipeline_latest_date = [
                {'$sort': {'date': -1}},
                {'$limit': 1},
                {'$project': {'date': 1}}
            ]
            
            latest_date = None
            async for doc in self.col_fund_individual_detail_hold_xq.aggregate(pipeline_latest_date):
                latest_date = doc.get('date')
            
            # 获取股票仓位最高的基金TOP10（最新日期）
            pipeline_top_stock = [
                {'$match': {'资产类型': '股票'}},
                {'$sort': {'date': -1, '仓位占比': -1}},
                {'$limit': 10},
                {'$project': {
                    'code': '$code',
                    'date': '$date',
                    'asset_type': '$资产类型',
                    'position': '$仓位占比'
                }}
            ]
            
            top_stock_position = []
            async for doc in self.col_fund_individual_detail_hold_xq.aggregate(pipeline_top_stock):
                top_stock_position.append({
                    'code': doc.get('code'),
                    'date': doc.get('date'),
                    'asset_type': doc.get('asset_type'),
                    'position': doc.get('position')
                })
            
            # 获取债券仓位最高的基金TOP10（最新日期）
            pipeline_top_bond = [
                {'$match': {'资产类型': '债券'}},
                {'$sort': {'date': -1, '仓位占比': -1}},
                {'$limit': 10},
                {'$project': {
                    'code': '$code',
                    'date': '$date',
                    'asset_type': '$资产类型',
                    'position': '$仓位占比'
                }}
            ]
            
            top_bond_position = []
            async for doc in self.col_fund_individual_detail_hold_xq.aggregate(pipeline_top_bond):
                top_bond_position.append({
                    'code': doc.get('code'),
                    'date': doc.get('date'),
                    'asset_type': doc.get('asset_type'),
                    'position': doc.get('position')
                })
            
            return {
                'total_count': total_count,
                'unique_funds': len(unique_funds),
                'unique_dates': len(unique_dates),
                'latest_date': latest_date,
                'asset_type_distribution': asset_type_distribution,
                'top_stock_position': top_stock_position,
                'top_bond_position': top_bond_position
            }
        except Exception as e:
            logger.error(f"获取基金持仓资产比例统计失败: {e}", exc_info=True)
            raise
    
    async def save_fund_overview_em_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存基金基本概况到MongoDB"""
        if df is None or df.empty:
            logger.warning("没有基金基本概况需要保存")
            return 0
        
        try:
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条基金基本概况...")
            
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    fund_code = str(doc.get('基金代码', ''))
                    doc['code'] = fund_code
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_overview_em'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    ops.append(
                        UpdateOne(
                            {'code': fund_code},
                            {'$set': doc},
                            upsert=True
                        )
                    )
                
                if ops:
                    result = await self.col_fund_overview_em.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条基金基本概况")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存基金基本概况失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_overview_em_data(self) -> int:
        """清空基金基本概况"""
        try:
            result = await self.col_fund_overview_em.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条基金基本概况")
            return deleted_count
        except Exception as e:
            logger.error(f"清空基金基本概况失败: {e}", exc_info=True)
            raise
    
    async def get_fund_overview_em_stats(self) -> Dict[str, Any]:
        """获取基金基本概况统计"""
        try:
            total_count = await self.col_fund_overview_em.count_documents({})
            
            # 获取基金类型分布
            pipeline_fund_types = [
                {'$group': {'_id': '$基金类型', 'count': {'$sum': 1}}},
                {'$sort': {'count': -1}}
            ]
            
            fund_type_distribution = []
            async for doc in self.col_fund_overview_em.aggregate(pipeline_fund_types):
                fund_type_distribution.append({
                    'fund_type': doc['_id'],
                    'count': doc['count']
                })
            
            # 获取基金管理人分布（TOP10）
            pipeline_managers = [
                {'$group': {'_id': '$基金管理人', 'count': {'$sum': 1}}},
                {'$sort': {'count': -1}},
                {'$limit': 10}
            ]
            
            top_managers = []
            async for doc in self.col_fund_overview_em.aggregate(pipeline_managers):
                top_managers.append({
                    'manager': doc['_id'],
                    'count': doc['count']
                })
            
            # 获取基金规模TOP10
            pipeline_top_scale = [
                {'$match': {'基金规模': {'$ne': None}}},
                {'$sort': {'基金规模': -1}},
                {'$limit': 10},
                {'$project': {
                    'code': '$code',
                    'name': '$基金简称',
                    'scale': '$基金规模',
                    'manager': '$基金管理人',
                    'fund_type': '$基金类型'
                }}
            ]
            
            top_scale_funds = []
            async for doc in self.col_fund_overview_em.aggregate(pipeline_top_scale):
                top_scale_funds.append({
                    'code': doc.get('code'),
                    'name': doc.get('name'),
                    'scale': doc.get('scale'),
                    'manager': doc.get('manager'),
                    'fund_type': doc.get('fund_type')
                })
            
            # 获取成立日期最早的基金TOP10
            pipeline_oldest = [
                {'$match': {'成立日期': {'$ne': None}}},
                {'$sort': {'成立日期': 1}},
                {'$limit': 10},
                {'$project': {
                    'code': '$code',
                    'name': '$基金简称',
                    'established_date': '$成立日期',
                    'manager': '$基金管理人',
                    'fund_type': '$基金类型'
                }}
            ]
            
            oldest_funds = []
            async for doc in self.col_fund_overview_em.aggregate(pipeline_oldest):
                oldest_funds.append({
                    'code': doc.get('code'),
                    'name': doc.get('name'),
                    'established_date': doc.get('established_date'),
                    'manager': doc.get('manager'),
                    'fund_type': doc.get('fund_type')
                })
            
            return {
                'total_count': total_count,
                'fund_type_distribution': fund_type_distribution,
                'top_managers': top_managers,
                'top_scale_funds': top_scale_funds,
                'oldest_funds': oldest_funds
            }
        except Exception as e:
            logger.error(f"获取基金基本概况统计失败: {e}", exc_info=True)
            raise
    
    async def save_fund_fee_em_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存基金交易费率到MongoDB"""
        if df is None or df.empty:
            logger.warning("没有基金交易费率需要保存")
            return 0
        
        try:
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条基金交易费率...")
            
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    fund_code = str(doc.get('基金代码', ''))
                    fee_type = str(doc.get('费用类型', ''))
                    condition = str(doc.get('条件', ''))
                    doc['code'] = fund_code
                    doc['fee_type'] = fee_type
                    doc['condition'] = condition
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_fee_em'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    ops.append(
                        UpdateOne(
                            {'code': fund_code, 'fee_type': fee_type, 'condition': condition},
                            {'$set': doc},
                            upsert=True
                        )
                    )
                
                if ops:
                    result = await self.col_fund_fee_em.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条基金交易费率")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存基金交易费率失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_fee_em_data(self) -> int:
        """清空基金交易费率"""
        try:
            result = await self.col_fund_fee_em.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条基金交易费率")
            return deleted_count
        except Exception as e:
            logger.error(f"清空基金交易费率失败: {e}", exc_info=True)
            raise
    
    async def get_fund_fee_em_stats(self) -> Dict[str, Any]:
        """获取基金交易费率统计"""
        try:
            total_count = await self.col_fund_fee_em.count_documents({})
            
            # 获取唯一基金数
            unique_funds = await self.col_fund_fee_em.distinct('code')
            
            # 获取费用类型分布
            pipeline_fee_types = [
                {'$group': {'_id': '$费用类型', 'count': {'$sum': 1}}},
                {'$sort': {'count': -1}}
            ]
            
            fee_type_distribution = []
            async for doc in self.col_fund_fee_em.aggregate(pipeline_fee_types):
                fee_type_distribution.append({
                    'fee_type': doc['_id'],
                    'count': doc['count']
                })
            
            # 获取申购费最低的基金TOP10
            pipeline_lowest_purchase = [
                {'$match': {'费用类型': '申购费', '优惠费率': {'$ne': None}}},
                {'$group': {'_id': '$code', 'avg_fee': {'$avg': '$优惠费率'}}},
                {'$sort': {'avg_fee': 1}},
                {'$limit': 10}
            ]
            
            lowest_purchase_fee_funds = []
            async for doc in self.col_fund_fee_em.aggregate(pipeline_lowest_purchase):
                lowest_purchase_fee_funds.append({
                    'code': doc['_id'],
                    'avg_fee': round(doc.get('avg_fee', 0), 3) if doc.get('avg_fee') else None
                })
            
            # 获取赎回费最低的基金TOP10
            pipeline_lowest_redemption = [
                {'$match': {'费用类型': '赎回费', '费率': {'$ne': None}}},
                {'$group': {'_id': '$code', 'avg_fee': {'$avg': '$费率'}}},
                {'$sort': {'avg_fee': 1}},
                {'$limit': 10}
            ]
            
            lowest_redemption_fee_funds = []
            async for doc in self.col_fund_fee_em.aggregate(pipeline_lowest_redemption):
                lowest_redemption_fee_funds.append({
                    'code': doc['_id'],
                    'avg_fee': round(doc.get('avg_fee', 0), 3) if doc.get('avg_fee') else None
                })
            
            return {
                'total_count': total_count,
                'unique_funds': len(unique_funds),
                'fee_type_distribution': fee_type_distribution,
                'lowest_purchase_fee_funds': lowest_purchase_fee_funds,
                'lowest_redemption_fee_funds': lowest_redemption_fee_funds
            }
        except Exception as e:
            logger.error(f"获取基金交易费率统计失败: {e}", exc_info=True)
            raise
    
    async def save_fund_individual_detail_info_xq_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存基金交易规则到MongoDB"""
        if df is None or df.empty:
            logger.warning("没有基金交易规则需要保存")
            return 0
        
        try:
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条基金交易规则...")
            
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    fund_code = str(doc.get('基金代码', ''))
                    fee_type = str(doc.get('费用类型', ''))
                    doc['code'] = fund_code
                    doc['fee_type'] = fee_type
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_individual_detail_info_xq'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    ops.append(
                        UpdateOne(
                            {'code': fund_code, 'fee_type': fee_type},
                            {'$set': doc},
                            upsert=True
                        )
                    )
                
                if ops:
                    result = await self.col_fund_individual_detail_info_xq.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条基金交易规则")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存基金交易规则失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_individual_detail_info_xq_data(self) -> int:
        """清空基金交易规则"""
        try:
            result = await self.col_fund_individual_detail_info_xq.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条基金交易规则")
            return deleted_count
        except Exception as e:
            logger.error(f"清空基金交易规则失败: {e}", exc_info=True)
            raise
    
    async def get_fund_individual_detail_info_xq_stats(self) -> Dict[str, Any]:
        """获取基金交易规则统计"""
        try:
            total_count = await self.col_fund_individual_detail_info_xq.count_documents({})
            
            # 获取唯一基金数
            unique_funds = await self.col_fund_individual_detail_info_xq.distinct('code')
            
            # 获取费用类型分布
            pipeline_fee_types = [
                {'$group': {'_id': '$费用类型', 'count': {'$sum': 1}}},
                {'$sort': {'count': -1}}
            ]
            
            fee_type_distribution = []
            async for doc in self.col_fund_individual_detail_info_xq.aggregate(pipeline_fee_types):
                fee_type_distribution.append({
                    'fee_type': doc['_id'],
                    'count': doc['count']
                })
            
            return {
                'total_count': total_count,
                'unique_funds': len(unique_funds),
                'fee_type_distribution': fee_type_distribution
            }
        except Exception as e:
            logger.error(f"获取基金交易规则统计失败: {e}", exc_info=True)
            raise
    
    async def save_fund_portfolio_hold_em_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存基金持仓到MongoDB"""
        if df is None or df.empty:
            logger.warning("没有基金持仓需要保存")
            return 0
        
        try:
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条基金持仓...")
            
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    fund_code = str(doc.get('基金代码', ''))
                    stock_code = str(doc.get('股票代码', ''))
                    quarter = str(doc.get('季度', ''))
                    doc['code'] = fund_code
                    doc['stock_code'] = stock_code
                    doc['quarter'] = quarter
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_portfolio_hold_em'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    ops.append(
                        UpdateOne(
                            {'code': fund_code, 'stock_code': stock_code, 'quarter': quarter},
                            {'$set': doc},
                            upsert=True
                        )
                    )
                
                if ops:
                    result = await self.col_fund_portfolio_hold_em.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条基金持仓")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存基金持仓失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_portfolio_hold_em_data(self) -> int:
        """清空基金持仓"""
        try:
            result = await self.col_fund_portfolio_hold_em.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条基金持仓")
            return deleted_count
        except Exception as e:
            logger.error(f"清空基金持仓失败: {e}", exc_info=True)
            raise
    
    async def get_fund_portfolio_hold_em_stats(self) -> Dict[str, Any]:
        """获取基金持仓统计"""
        try:
            total_count = await self.col_fund_portfolio_hold_em.count_documents({})
            
            # 获取唯一基金数
            unique_funds = await self.col_fund_portfolio_hold_em.distinct('code')
            
            # 获取唯一股票数
            unique_stocks = await self.col_fund_portfolio_hold_em.distinct('stock_code')
            
            # 获取季度分布
            pipeline_quarters = [
                {'$group': {'_id': '$季度', 'count': {'$sum': 1}}},
                {'$sort': {'_id': -1}}
            ]
            
            quarter_distribution = []
            async for doc in self.col_fund_portfolio_hold_em.aggregate(pipeline_quarters):
                quarter_distribution.append({
                    'quarter': doc['_id'],
                    'count': doc['count']
                })
            
            # 获取最受基金青睐的股票TOP10
            pipeline_top_stocks = [
                {'$group': {'_id': '$股票代码', 'stock_name': {'$first': '$股票名称'}, 'fund_count': {'$sum': 1}}},
                {'$sort': {'fund_count': -1}},
                {'$limit': 10}
            ]
            
            top_stocks = []
            async for doc in self.col_fund_portfolio_hold_em.aggregate(pipeline_top_stocks):
                top_stocks.append({
                    'stock_code': doc['_id'],
                    'stock_name': doc.get('stock_name'),
                    'fund_count': doc['fund_count']
                })
            
            # 获取持仓占比最高的记录TOP10
            pipeline_top_holdings = [
                {'$match': {'持仓占比': {'$ne': None}}},
                {'$sort': {'持仓占比': -1}},
                {'$limit': 10},
                {'$project': {'基金代码': 1, '股票代码': 1, '股票名称': 1, '季度': 1, '持仓占比': 1}}
            ]
            
            top_holdings = []
            async for doc in self.col_fund_portfolio_hold_em.aggregate(pipeline_top_holdings):
                top_holdings.append({
                    'fund_code': doc.get('基金代码'),
                    'stock_code': doc.get('股票代码'),
                    'stock_name': doc.get('股票名称'),
                    'quarter': doc.get('季度'),
                    'holding_ratio': doc.get('持仓占比')
                })
            
            return {
                'total_count': total_count,
                'unique_funds': len(unique_funds),
                'unique_stocks': len(unique_stocks),
                'quarter_distribution': quarter_distribution,
                'top_stocks': top_stocks,
                'top_holdings': top_holdings
            }
        except Exception as e:
            logger.error(f"获取基金持仓统计失败: {e}", exc_info=True)
            raise
    
    async def save_fund_portfolio_bond_hold_em_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存债券持仓到MongoDB"""
        if df is None or df.empty:
            logger.warning("没有债券持仓需要保存")
            return 0
        
        try:
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条债券持仓...")
            
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    fund_code = str(doc.get('基金代码', ''))
                    bond_code = str(doc.get('债券代码', ''))
                    quarter = str(doc.get('季度', ''))
                    doc['code'] = fund_code
                    doc['bond_code'] = bond_code
                    doc['quarter'] = quarter
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_portfolio_bond_hold_em'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    ops.append(
                        UpdateOne(
                            {'code': fund_code, 'bond_code': bond_code, 'quarter': quarter},
                            {'$set': doc},
                            upsert=True
                        )
                    )
                
                if ops:
                    result = await self.col_fund_portfolio_bond_hold_em.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条债券持仓")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存债券持仓失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_portfolio_bond_hold_em_data(self) -> int:
        """清空债券持仓"""
        try:
            result = await self.col_fund_portfolio_bond_hold_em.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条债券持仓")
            return deleted_count
        except Exception as e:
            logger.error(f"清空债券持仓失败: {e}", exc_info=True)
            raise
    
    async def get_fund_portfolio_bond_hold_em_stats(self) -> Dict[str, Any]:
        """获取债券持仓统计"""
        try:
            total_count = await self.col_fund_portfolio_bond_hold_em.count_documents({})
            
            unique_funds = await self.col_fund_portfolio_bond_hold_em.distinct('code')
            unique_bonds = await self.col_fund_portfolio_bond_hold_em.distinct('bond_code')
            
            pipeline_quarters = [
                {'$group': {'_id': '$季度', 'count': {'$sum': 1}}},
                {'$sort': {'_id': -1}}
            ]
            
            quarter_distribution = []
            async for doc in self.col_fund_portfolio_bond_hold_em.aggregate(pipeline_quarters):
                quarter_distribution.append({
                    'quarter': doc['_id'],
                    'count': doc['count']
                })
            
            pipeline_top_bonds = [
                {'$group': {'_id': '$债券代码', 'bond_name': {'$first': '$债券名称'}, 'fund_count': {'$sum': 1}}},
                {'$sort': {'fund_count': -1}},
                {'$limit': 10}
            ]
            
            top_bonds = []
            async for doc in self.col_fund_portfolio_bond_hold_em.aggregate(pipeline_top_bonds):
                top_bonds.append({
                    'bond_code': doc['_id'],
                    'bond_name': doc.get('bond_name'),
                    'fund_count': doc['fund_count']
                })
            
            pipeline_top_holdings = [
                {'$match': {'持仓占比': {'$ne': None}}},
                {'$sort': {'持仓占比': -1}},
                {'$limit': 10},
                {'$project': {'基金代码': 1, '债券代码': 1, '债券名称': 1, '季度': 1, '持仓占比': 1}}
            ]
            
            top_holdings = []
            async for doc in self.col_fund_portfolio_bond_hold_em.aggregate(pipeline_top_holdings):
                top_holdings.append({
                    'fund_code': doc.get('基金代码'),
                    'bond_code': doc.get('债券代码'),
                    'bond_name': doc.get('债券名称'),
                    'quarter': doc.get('季度'),
                    'holding_ratio': doc.get('持仓占比')
                })
            
            return {
                'total_count': total_count,
                'unique_funds': len(unique_funds),
                'unique_bonds': len(unique_bonds),
                'quarter_distribution': quarter_distribution,
                'top_bonds': top_bonds,
                'top_holdings': top_holdings
            }
        except Exception as e:
            logger.error(f"获取债券持仓统计失败: {e}", exc_info=True)
            raise
    
    async def save_fund_portfolio_industry_allocation_em_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存行业配置到MongoDB"""
        if df is None or df.empty:
            logger.warning("没有行业配置需要保存")
            return 0
        
        try:
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条行业配置...")
            
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    fund_code = str(doc.get('基金代码', ''))
                    industry = str(doc.get('行业类别', ''))
                    end_date = str(doc.get('截止时间', ''))
                    doc['code'] = fund_code
                    doc['industry'] = industry
                    doc['end_date'] = end_date
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_portfolio_industry_allocation_em'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    ops.append(
                        UpdateOne(
                            {'code': fund_code, 'industry': industry, 'end_date': end_date},
                            {'$set': doc},
                            upsert=True
                        )
                    )
                
                if ops:
                    result = await self.col_fund_portfolio_industry_allocation_em.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条行业配置")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存行业配置失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_portfolio_industry_allocation_em_data(self) -> int:
        """清空行业配置"""
        try:
            result = await self.col_fund_portfolio_industry_allocation_em.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条行业配置")
            return deleted_count
        except Exception as e:
            logger.error(f"清空行业配置失败: {e}", exc_info=True)
            raise
    
    async def get_fund_portfolio_industry_allocation_em_stats(self) -> Dict[str, Any]:
        """获取行业配置统计"""
        try:
            total_count = await self.col_fund_portfolio_industry_allocation_em.count_documents({})
            
            unique_funds = await self.col_fund_portfolio_industry_allocation_em.distinct('code')
            unique_industries = await self.col_fund_portfolio_industry_allocation_em.distinct('industry')
            
            pipeline_industries = [
                {'$group': {'_id': '$行业类别', 'count': {'$sum': 1}}},
                {'$sort': {'count': -1}},
                {'$limit': 20}
            ]
            
            industry_distribution = []
            async for doc in self.col_fund_portfolio_industry_allocation_em.aggregate(pipeline_industries):
                industry_distribution.append({
                    'industry': doc['_id'],
                    'count': doc['count']
                })
            
            pipeline_top_allocation = [
                {'$match': {'占净值比例': {'$ne': None}}},
                {'$sort': {'占净值比例': -1}},
                {'$limit': 10},
                {'$project': {'基金代码': 1, '行业类别': 1, '截止时间': 1, '占净值比例': 1}}
            ]
            
            top_allocations = []
            async for doc in self.col_fund_portfolio_industry_allocation_em.aggregate(pipeline_top_allocation):
                top_allocations.append({
                    'fund_code': doc.get('基金代码'),
                    'industry': doc.get('行业类别'),
                    'end_date': doc.get('截止时间'),
                    'ratio': doc.get('占净值比例')
                })
            
            return {
                'total_count': total_count,
                'unique_funds': len(unique_funds),
                'unique_industries': len(unique_industries),
                'industry_distribution': industry_distribution,
                'top_allocations': top_allocations
            }
        except Exception as e:
            logger.error(f"获取行业配置统计失败: {e}", exc_info=True)
            raise
    
    async def save_fund_portfolio_change_em_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存重大变动到MongoDB"""
        if df is None or df.empty:
            logger.warning("没有重大变动需要保存")
            return 0
        
        try:
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条重大变动...")
            
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    fund_code = str(doc.get('基金代码', ''))
                    stock_code = str(doc.get('股票代码', ''))
                    indicator_type = str(doc.get('指标类型', ''))
                    quarter = str(doc.get('季度', ''))
                    doc['code'] = fund_code
                    doc['stock_code'] = stock_code
                    doc['indicator_type'] = indicator_type
                    doc['quarter'] = quarter
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_portfolio_change_em'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    ops.append(
                        UpdateOne(
                            {'code': fund_code, 'stock_code': stock_code, 'indicator_type': indicator_type, 'quarter': quarter},
                            {'$set': doc},
                            upsert=True
                        )
                    )
                
                if ops:
                    result = await self.col_fund_portfolio_change_em.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条重大变动")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存重大变动失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_portfolio_change_em_data(self) -> int:
        """清空重大变动"""
        try:
            result = await self.col_fund_portfolio_change_em.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条重大变动")
            return deleted_count
        except Exception as e:
            logger.error(f"清空重大变动失败: {e}", exc_info=True)
            raise
    
    async def get_fund_portfolio_change_em_stats(self) -> Dict[str, Any]:
        """获取重大变动统计"""
        try:
            total_count = await self.col_fund_portfolio_change_em.count_documents({})
            
            unique_funds = await self.col_fund_portfolio_change_em.distinct('code')
            unique_stocks = await self.col_fund_portfolio_change_em.distinct('stock_code')
            
            pipeline_indicator_types = [
                {'$group': {'_id': '$指标类型', 'count': {'$sum': 1}}},
                {'$sort': {'count': -1}}
            ]
            
            indicator_type_distribution = []
            async for doc in self.col_fund_portfolio_change_em.aggregate(pipeline_indicator_types):
                indicator_type_distribution.append({
                    'indicator_type': doc['_id'],
                    'count': doc['count']
                })
            
            pipeline_quarters = [
                {'$group': {'_id': '$季度', 'count': {'$sum': 1}}},
                {'$sort': {'_id': -1}}
            ]
            
            quarter_distribution = []
            async for doc in self.col_fund_portfolio_change_em.aggregate(pipeline_quarters):
                quarter_distribution.append({
                    'quarter': doc['_id'],
                    'count': doc['count']
                })
            
            return {
                'total_count': total_count,
                'unique_funds': len(unique_funds),
                'unique_stocks': len(unique_stocks),
                'indicator_type_distribution': indicator_type_distribution,
                'quarter_distribution': quarter_distribution
            }
        except Exception as e:
            logger.error(f"获取重大变动统计失败: {e}", exc_info=True)
            raise

    async def save_fund_rating_all_em_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存基金评级总汇到MongoDB"""
        if df is None or df.empty:
            logger.warning("没有基金评级总汇数据需要保存")
            return 0
        
        try:
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条基金评级总汇数据...")
            
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    # 添加元数据
                    fund_code = str(doc.get('代码', ''))
                    doc['code'] = fund_code
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_rating_all'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    # 使用基金代码作为唯一标识
                    if fund_code:
                        ops.append(
                            UpdateOne(
                                {'code': fund_code},
                                {'$set': doc},
                                upsert=True
                            )
                        )
                
                if ops:
                    result = await self.col_fund_rating_all_em.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条基金评级总汇数据")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存基金评级总汇数据失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_rating_all_em_data(self) -> int:
        """清空基金评级总汇数据"""
        try:
            result = await self.col_fund_rating_all_em.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条基金评级总汇数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空基金评级总汇数据失败: {e}", exc_info=True)
            raise
    
    async def get_fund_rating_all_em_stats(self) -> Dict[str, Any]:
        """获取基金评级总汇统计"""
        try:
            total_count = await self.col_fund_rating_all_em.count_documents({})
            
            unique_funds = await self.col_fund_rating_all_em.distinct('code')
            
            # 评级分布（按招商证券评级）
            pipeline_rating = [
                {'$group': {'_id': '$招商证券', 'count': {'$sum': 1}}},
                {'$sort': {'_id': -1}}
            ]
            
            rating_distribution = []
            async for doc in self.col_fund_rating_all_em.aggregate(pipeline_rating):
                if doc['_id'] is not None:
                    rating_distribution.append({
                        'rating': doc['_id'],
                        'count': doc['count']
                    })
            
            return {
                'total_count': total_count,
                'unique_funds': len(unique_funds),
                'rating_distribution': rating_distribution
            }
        except Exception as e:
            logger.error(f"获取基金评级总汇统计失败: {e}", exc_info=True)
            raise

    async def save_fund_rating_sh_em_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存上海证券评级到MongoDB"""
        if df is None or df.empty:
            logger.warning("没有上海证券评级数据需要保存")
            return 0
        
        try:
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条上海证券评级数据...")
            
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    # 添加元数据
                    fund_code = str(doc.get('代码', ''))
                    date_str = str(doc.get('日期', ''))
                    doc['code'] = fund_code
                    doc['date'] = date_str
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_rating_sh'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    # 使用基金代码和日期作为唯一标识
                    if fund_code and date_str:
                        ops.append(
                            UpdateOne(
                                {'code': fund_code, 'date': date_str},
                                {'$set': doc},
                                upsert=True
                            )
                        )
                
                if ops:
                    result = await self.col_fund_rating_sh_em.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条上海证券评级数据")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存上海证券评级数据失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_rating_sh_em_data(self) -> int:
        """清空上海证券评级数据"""
        try:
            result = await self.col_fund_rating_sh_em.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条上海证券评级数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空上海证券评级数据失败: {e}", exc_info=True)
            raise
    
    async def get_fund_rating_sh_em_stats(self) -> Dict[str, Any]:
        """获取上海证券评级统计"""
        try:
            total_count = await self.col_fund_rating_sh_em.count_documents({})
            
            unique_funds = await self.col_fund_rating_sh_em.distinct('code')
            
            # 3年期评级分布
            pipeline_rating = [
                {'$group': {'_id': '$3年期评级-3年评级', 'count': {'$sum': 1}}},
                {'$sort': {'_id': -1}}
            ]
            
            rating_distribution = []
            async for doc in self.col_fund_rating_sh_em.aggregate(pipeline_rating):
                if doc['_id'] is not None:
                    rating_distribution.append({
                        'rating': doc['_id'],
                        'count': doc['count']
                    })
            
            return {
                'total_count': total_count,
                'unique_funds': len(unique_funds),
                'rating_distribution': rating_distribution
            }
        except Exception as e:
            logger.error(f"获取上海证券评级统计失败: {e}", exc_info=True)
            raise

    async def save_fund_rating_zs_em_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存招商证券评级到MongoDB"""
        if df is None or df.empty:
            logger.warning("没有招商证券评级数据需要保存")
            return 0
        
        try:
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条招商证券评级数据...")
            
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    # 添加元数据
                    fund_code = str(doc.get('代码', ''))
                    date_str = str(doc.get('日期', ''))
                    doc['code'] = fund_code
                    doc['date'] = date_str
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_rating_zs'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    # 使用基金代码和日期作为唯一标识
                    if fund_code and date_str:
                        ops.append(
                            UpdateOne(
                                {'code': fund_code, 'date': date_str},
                                {'$set': doc},
                                upsert=True
                            )
                        )
                
                if ops:
                    result = await self.col_fund_rating_zs_em.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条招商证券评级数据")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存招商证券评级数据失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_rating_zs_em_data(self) -> int:
        """清空招商证券评级数据"""
        try:
            result = await self.col_fund_rating_zs_em.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条招商证券评级数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空招商证券评级数据失败: {e}", exc_info=True)
            raise
    
    async def get_fund_rating_zs_em_stats(self) -> Dict[str, Any]:
        """获取招商证券评级统计"""
        try:
            total_count = await self.col_fund_rating_zs_em.count_documents({})
            
            unique_funds = await self.col_fund_rating_zs_em.distinct('code')
            
            # 3年期评级分布
            pipeline_rating = [
                {'$group': {'_id': '$3年期评级-3年评级', 'count': {'$sum': 1}}},
                {'$sort': {'_id': -1}}
            ]
            
            rating_distribution = []
            async for doc in self.col_fund_rating_zs_em.aggregate(pipeline_rating):
                if doc['_id'] is not None:
                    rating_distribution.append({
                        'rating': doc['_id'],
                        'count': doc['count']
                    })
            
            return {
                'total_count': total_count,
                'unique_funds': len(unique_funds),
                'rating_distribution': rating_distribution
            }
        except Exception as e:
            logger.error(f"获取招商证券评级统计失败: {e}", exc_info=True)
            raise

    async def save_fund_rating_ja_em_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存济安金信评级到MongoDB"""
        if df is None or df.empty:
            logger.warning("没有济安金信评级数据需要保存")
            return 0
        
        try:
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条济安金信评级数据...")
            
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    # 添加元数据
                    fund_code = str(doc.get('代码', ''))
                    date_str = str(doc.get('日期', ''))
                    doc['code'] = fund_code
                    doc['date'] = date_str
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_rating_ja'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    # 使用基金代码和日期作为唯一标识
                    if fund_code and date_str:
                        ops.append(
                            UpdateOne(
                                {'code': fund_code, 'date': date_str},
                                {'$set': doc},
                                upsert=True
                            )
                        )
                
                if ops:
                    result = await self.col_fund_rating_ja_em.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条济安金信评级数据")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存济安金信评级数据失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_rating_ja_em_data(self) -> int:
        """清空济安金信评级数据"""
        try:
            result = await self.col_fund_rating_ja_em.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条济安金信评级数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空济安金信评级数据失败: {e}", exc_info=True)
            raise
    
    async def get_fund_rating_ja_em_stats(self) -> Dict[str, Any]:
        """获取济安金信评级统计"""
        try:
            total_count = await self.col_fund_rating_ja_em.count_documents({})
            
            unique_funds = await self.col_fund_rating_ja_em.distinct('code')
            
            # 3年期评级分布
            pipeline_rating = [
                {'$group': {'_id': '$3年期评级-3年评级', 'count': {'$sum': 1}}},
                {'$sort': {'_id': -1}}
            ]
            
            rating_distribution = []
            async for doc in self.col_fund_rating_ja_em.aggregate(pipeline_rating):
                if doc['_id'] is not None:
                    rating_distribution.append({
                        'rating': doc['_id'],
                        'count': doc['count']
                    })
            
            return {
                'total_count': total_count,
                'unique_funds': len(unique_funds),
                'rating_distribution': rating_distribution
            }
        except Exception as e:
            logger.error(f"获取济安金信评级统计失败: {e}", exc_info=True)
            raise

    async def save_fund_manager_em_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存基金经理到MongoDB"""
        if df is None or df.empty:
            logger.warning("没有基金经理数据需要保存")
            return 0
        
        try:
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条基金经理数据...")
            
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    # 添加元数据
                    name = str(doc.get('姓名', ''))
                    fund_codes = str(doc.get('现任基金代码', ''))
                    doc['name'] = name
                    doc['fund_codes'] = fund_codes
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_manager_em'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    # 使用姓名和现任基金代码作为唯一标识（如果基金代码为空，可能需要其他标识，如序号）
                    unique_key = {'name': name, 'fund_codes': fund_codes}
                    
                    # 如果有序号，优先使用序号作为辅助（假设序号是唯一ID）
                    # 但API返回的序号不一定是固定的ID，可能是本次查询的序号。
                    # 所以还是用 name + fund_codes 比较稳妥。
                    
                    ops.append(
                        UpdateOne(
                            unique_key,
                            {'$set': doc},
                            upsert=True
                        )
                    )
                
                if ops:
                    result = await self.col_fund_manager_em.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条基金经理数据")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存基金经理数据失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_manager_em_data(self) -> int:
        """清空基金经理数据"""
        try:
            result = await self.col_fund_manager_em.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条基金经理数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空基金经理数据失败: {e}", exc_info=True)
            raise
    
    async def get_fund_manager_em_stats(self) -> Dict[str, Any]:
        """获取基金经理统计"""
        try:
            total_count = await self.col_fund_manager_em.count_documents({})
            
            unique_companies = await self.col_fund_manager_em.distinct('所属公司')
            
            # 基金经理人数最多的公司TOP10
            pipeline_company = [
                {'$group': {'_id': '$所属公司', 'count': {'$sum': 1}}},
                {'$sort': {'count': -1}},
                {'$limit': 10}
            ]
            
            company_distribution = []
            async for doc in self.col_fund_manager_em.aggregate(pipeline_company):
                if doc['_id']:
                    company_distribution.append({
                        'company': doc['_id'],
                        'count': doc['count']
                    })
            
            return {
                'total_count': total_count,
                'unique_companies': len(unique_companies),
                'company_distribution': company_distribution
            }
        except Exception as e:
            logger.error(f"获取基金经理统计失败: {e}", exc_info=True)
            raise

    async def save_fund_new_found_em_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存新发基金到MongoDB"""
        if df is None or df.empty:
            logger.warning("没有新发基金数据需要保存")
            return 0
        
        try:
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条新发基金数据...")
            
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    # 添加元数据
                    fund_code = str(doc.get('基金代码', ''))
                    doc['code'] = fund_code
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_new_found_em'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    # 使用基金代码作为唯一标识
                    if fund_code:
                        ops.append(
                            UpdateOne(
                                {'code': fund_code},
                                {'$set': doc},
                                upsert=True
                            )
                        )
                
                if ops:
                    result = await self.col_fund_new_found_em.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条新发基金数据")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存新发基金数据失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_new_found_em_data(self) -> int:
        """清空新发基金数据"""
        try:
            result = await self.col_fund_new_found_em.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条新发基金数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空新发基金数据失败: {e}", exc_info=True)
            raise
    
    async def get_fund_new_found_em_stats(self) -> Dict[str, Any]:
        """获取新发基金统计"""
        try:
            total_count = await self.col_fund_new_found_em.count_documents({})
            
            unique_funds = await self.col_fund_new_found_em.distinct('code')
            
            # 基金类型分布（假设有'基金类型'字段）
            pipeline_type = [
                {'$group': {'_id': '$基金类型', 'count': {'$sum': 1}}},
                {'$sort': {'count': -1}}
            ]
            
            type_distribution = []
            async for doc in self.col_fund_new_found_em.aggregate(pipeline_type):
                if doc['_id']:
                    type_distribution.append({
                        'type': doc['_id'],
                        'count': doc['count']
                    })
            
            return {
                'total_count': total_count,
                'unique_funds': len(unique_funds),
                'type_distribution': type_distribution
            }
        except Exception as e:
            logger.error(f"获取新发基金统计失败: {e}", exc_info=True)
            raise

    async def save_fund_scale_open_sina_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存开放式基金规模到MongoDB"""
        if df is None or df.empty:
            logger.warning("没有开放式基金规模数据需要保存")
            return 0
        
        try:
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条开放式基金规模数据...")
            
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    # 添加元数据
                    fund_code = str(doc.get('基金代码', ''))
                    # 假设有日期字段，如果没有，使用当前日期
                    date_str = str(doc.get('更新日期', '')) or str(doc.get('截止日期', '')) or datetime.now().strftime('%Y-%m-%d')
                    
                    doc['code'] = fund_code
                    doc['date'] = date_str
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_scale_open_sina'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    # 使用基金代码和日期作为唯一标识
                    if fund_code:
                        ops.append(
                            UpdateOne(
                                {'code': fund_code, 'date': date_str},
                                {'$set': doc},
                                upsert=True
                            )
                        )
                
                if ops:
                    result = await self.col_fund_scale_open_sina.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条开放式基金规模数据")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存开放式基金规模数据失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_scale_open_sina_data(self) -> int:
        """清空开放式基金规模数据"""
        try:
            result = await self.col_fund_scale_open_sina.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条开放式基金规模数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空开放式基金规模数据失败: {e}", exc_info=True)
            raise
    
    async def get_fund_scale_open_sina_stats(self) -> Dict[str, Any]:
        """获取开放式基金规模统计"""
        try:
            total_count = await self.col_fund_scale_open_sina.count_documents({})
            
            unique_funds = await self.col_fund_scale_open_sina.distinct('code')
            
            # 规模TOP10（需要根据最新日期过滤，这里简单按规模排序，假设规模字段为'总资产'或类似）
            # 假设字段名为 '资产净值' 或 '基金规模'
            # 这是一个简单的统计，不需要太复杂
            
            return {
                'total_count': total_count,
                'unique_funds': len(unique_funds)
            }
        except Exception as e:
            logger.error(f"获取开放式基金规模统计失败: {e}", exc_info=True)
            raise

    async def save_fund_scale_close_sina_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存封闭式基金规模到MongoDB"""
        if df is None or df.empty:
            logger.warning("没有封闭式基金规模数据需要保存")
            return 0
        
        try:
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条封闭式基金规模数据...")
            
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    # 添加元数据
                    fund_code = str(doc.get('基金代码', ''))
                    date_str = str(doc.get('更新日期', '')) or str(doc.get('截止日期', '')) or datetime.now().strftime('%Y-%m-%d')
                    
                    doc['code'] = fund_code
                    doc['date'] = date_str
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_scale_close_sina'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    # 使用基金代码和日期作为唯一标识
                    if fund_code:
                        ops.append(
                            UpdateOne(
                                {'code': fund_code, 'date': date_str},
                                {'$set': doc},
                                upsert=True
                            )
                        )
                
                if ops:
                    result = await self.col_fund_scale_close_sina.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条封闭式基金规模数据")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存封闭式基金规模数据失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_scale_close_sina_data(self) -> int:
        """清空封闭式基金规模数据"""
        try:
            result = await self.col_fund_scale_close_sina.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条封闭式基金规模数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空封闭式基金规模数据失败: {e}", exc_info=True)
            raise
    
    async def get_fund_scale_close_sina_stats(self) -> Dict[str, Any]:
        """获取封闭式基金规模统计"""
        try:
            total_count = await self.col_fund_scale_close_sina.count_documents({})
            
            unique_funds = await self.col_fund_scale_close_sina.distinct('code')
            
            return {
                'total_count': total_count,
                'unique_funds': len(unique_funds)
            }
        except Exception as e:
            logger.error(f"获取封闭式基金规模统计失败: {e}", exc_info=True)
            raise

    async def save_fund_scale_structured_sina_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存分级子基金规模到MongoDB"""
        if df is None or df.empty:
            logger.warning("没有分级子基金规模数据需要保存")
            return 0
        
        try:
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条分级子基金规模数据...")
            
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    # 添加元数据
                    fund_code = str(doc.get('基金代码', ''))
                    date_str = str(doc.get('更新日期', '')) or str(doc.get('截止日期', '')) or datetime.now().strftime('%Y-%m-%d')
                    
                    doc['code'] = fund_code
                    doc['date'] = date_str
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_scale_structured_sina'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    # 使用基金代码和日期作为唯一标识
                    if fund_code:
                        ops.append(
                            UpdateOne(
                                {'code': fund_code, 'date': date_str},
                                {'$set': doc},
                                upsert=True
                            )
                        )
                
                if ops:
                    result = await self.col_fund_scale_structured_sina.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条分级子基金规模数据")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存分级子基金规模数据失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_scale_structured_sina_data(self) -> int:
        """清空分级子基金规模数据"""
        try:
            result = await self.col_fund_scale_structured_sina.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条分级子基金规模数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空分级子基金规模数据失败: {e}", exc_info=True)
            raise
    
    async def get_fund_scale_structured_sina_stats(self) -> Dict[str, Any]:
        """获取分级子基金规模统计"""
        try:
            total_count = await self.col_fund_scale_structured_sina.count_documents({})
            
            unique_funds = await self.col_fund_scale_structured_sina.distinct('code')
            
            return {
                'total_count': total_count,
                'unique_funds': len(unique_funds)
            }
        except Exception as e:
            logger.error(f"获取分级子基金规模统计失败: {e}", exc_info=True)
            raise

    async def save_fund_aum_em_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存基金规模详情到MongoDB"""
        if df is None or df.empty:
            logger.warning("没有基金规模详情数据需要保存")
            return 0
        
        try:
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条基金规模详情数据...")
            
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    # 添加元数据
                    fund_company = str(doc.get('基金公司', ''))
                    # 假设有更新日期字段
                    date_str = str(doc.get('更新日期', '')) or str(doc.get('截止日期', '')) or datetime.now().strftime('%Y-%m-%d')
                    
                    doc['company'] = fund_company
                    doc['date'] = date_str
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_aum_em'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    # 使用基金公司和日期作为唯一标识
                    if fund_company:
                        ops.append(
                            UpdateOne(
                                {'company': fund_company, 'date': date_str},
                                {'$set': doc},
                                upsert=True
                            )
                        )
                
                if ops:
                    result = await self.col_fund_aum_em.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条基金规模详情数据")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存基金规模详情数据失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_aum_em_data(self) -> int:
        """清空基金规模详情数据"""
        try:
            result = await self.col_fund_aum_em.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条基金规模详情数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空基金规模详情数据失败: {e}", exc_info=True)
            raise
    
    async def get_fund_aum_em_stats(self) -> Dict[str, Any]:
        """获取基金规模详情统计"""
        try:
            total_count = await self.col_fund_aum_em.count_documents({})
            
            unique_companies = await self.col_fund_aum_em.distinct('company')
            
            return {
                'total_count': total_count,
                'unique_companies': len(unique_companies)
            }
        except Exception as e:
            logger.error(f"获取基金规模详情统计失败: {e}", exc_info=True)
            raise

    async def save_fund_aum_trend_em_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存基金规模走势到MongoDB"""
        if df is None or df.empty:
            logger.warning("没有基金规模走势数据需要保存")
            return 0
        
        try:
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条基金规模走势数据...")
            
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    # 添加元数据
                    date_str = str(doc.get('date', '')) or str(doc.get('截止日期', '')) or datetime.now().strftime('%Y-%m-%d')
                    
                    doc['date'] = date_str
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_aum_trend_em'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    # 使用日期作为唯一标识
                    if date_str:
                        ops.append(
                            UpdateOne(
                                {'date': date_str},
                                {'$set': doc},
                                upsert=True
                            )
                        )
                
                if ops:
                    result = await self.col_fund_aum_trend_em.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条基金规模走势数据")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存基金规模走势数据失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_aum_trend_em_data(self) -> int:
        """清空基金规模走势数据"""
        try:
            result = await self.col_fund_aum_trend_em.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条基金规模走势数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空基金规模走势数据失败: {e}", exc_info=True)
            raise
    
    async def get_fund_aum_trend_em_stats(self) -> Dict[str, Any]:
        """获取基金规模走势统计"""
        try:
            total_count = await self.col_fund_aum_trend_em.count_documents({})
            
            # 假设我们只关心总记录数
            
            return {
                'total_count': total_count
            }
        except Exception as e:
            logger.error(f"获取基金规模走势统计失败: {e}", exc_info=True)
            raise

    async def save_fund_aum_hist_em_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存基金公司历年管理规模到MongoDB"""
        if df is None or df.empty:
            logger.warning("没有基金公司历年管理规模数据需要保存")
            return 0
        
        try:
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条基金公司历年管理规模数据...")
            
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    # 添加元数据
                    fund_company = str(doc.get('基金公司', ''))
                    date_str = str(doc.get('更新日期', '')) or str(doc.get('截止日期', '')) or datetime.now().strftime('%Y-%m-%d')
                    
                    doc['company'] = fund_company
                    doc['date'] = date_str
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_aum_hist_em'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    # 使用基金公司和日期作为唯一标识
                    if fund_company and date_str:
                        ops.append(
                            UpdateOne(
                                {'company': fund_company, 'date': date_str},
                                {'$set': doc},
                                upsert=True
                            )
                        )
                
                if ops:
                    result = await self.col_fund_aum_hist_em.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条基金公司历年管理规模数据")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存基金公司历年管理规模数据失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_aum_hist_em_data(self) -> int:
        """清空基金公司历年管理规模数据"""
        try:
            result = await self.col_fund_aum_hist_em.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条基金公司历年管理规模数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空基金公司历年管理规模数据失败: {e}", exc_info=True)
            raise
    
    async def get_fund_aum_hist_em_stats(self) -> Dict[str, Any]:
        """获取基金公司历年管理规模统计"""
        try:
            total_count = await self.col_fund_aum_hist_em.count_documents({})
            
            unique_companies = await self.col_fund_aum_hist_em.distinct('company')
            
            return {
                'total_count': total_count,
                'unique_companies': len(unique_companies)
            }
        except Exception as e:
            logger.error(f"获取基金公司历年管理规模统计失败: {e}", exc_info=True)
            raise

    async def save_reits_realtime_em_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存REITs实时行情到MongoDB"""
        if df is None or df.empty:
            logger.warning("没有REITs实时行情数据需要保存")
            return 0
        
        try:
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条REITs实时行情数据...")
            
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    # 添加元数据
                    code = str(doc.get('代码', ''))
                    date_str = datetime.now().strftime('%Y-%m-%d')
                    
                    doc['code'] = code
                    doc['date'] = date_str
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'reits_realtime_em'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    # 使用代码和日期作为唯一标识
                    if code:
                        ops.append(
                            UpdateOne(
                                {'code': code, 'date': date_str},
                                {'$set': doc},
                                upsert=True
                            )
                        )
                
                if ops:
                    result = await self.col_reits_realtime_em.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条REITs实时行情数据")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存REITs实时行情数据失败: {e}", exc_info=True)
            raise
    
    async def clear_reits_realtime_em_data(self) -> int:
        """清空REITs实时行情数据"""
        try:
            result = await self.col_reits_realtime_em.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条REITs实时行情数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空REITs实时行情数据失败: {e}", exc_info=True)
            raise
    
    async def get_reits_realtime_em_stats(self) -> Dict[str, Any]:
        """获取REITs实时行情统计"""
        try:
            total_count = await self.col_reits_realtime_em.count_documents({})
            
            unique_codes = await self.col_reits_realtime_em.distinct('code')
            
            return {
                'total_count': total_count,
                'unique_codes': len(unique_codes)
            }
        except Exception as e:
            logger.error(f"获取REITs实时行情统计失败: {e}", exc_info=True)
            raise

    async def save_reits_hist_em_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存REITs历史行情到MongoDB"""
        if df is None or df.empty:
            logger.warning("没有REITs历史行情数据需要保存")
            return 0
        
        try:
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条REITs历史行情数据...")
            
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    # 添加元数据
                    code = str(doc.get('code', '')) or str(doc.get('代码', ''))
                    date_str = str(doc.get('date', '')) or str(doc.get('日期', ''))
                    
                    doc['code'] = code
                    doc['date'] = date_str
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'reits_hist_em'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    # 使用代码和日期作为唯一标识
                    if code and date_str:
                        ops.append(
                            UpdateOne(
                                {'code': code, 'date': date_str},
                                {'$set': doc},
                                upsert=True
                            )
                        )
                
                if ops:
                    result = await self.col_reits_hist_em.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条REITs历史行情数据")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存REITs历史行情数据失败: {e}", exc_info=True)
            raise
    
    async def clear_reits_hist_em_data(self) -> int:
        """清空REITs历史行情数据"""
        try:
            result = await self.col_reits_hist_em.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条REITs历史行情数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空REITs历史行情数据失败: {e}", exc_info=True)
            raise
    
    async def get_reits_hist_em_stats(self) -> Dict[str, Any]:
        """获取REITs历史行情统计"""
        try:
            total_count = await self.col_reits_hist_em.count_documents({})
            
            unique_codes = await self.col_reits_hist_em.distinct('code')
            
            return {
                'total_count': total_count,
                'unique_codes': len(unique_codes)
            }
        except Exception as e:
            logger.error(f"获取REITs历史行情统计失败: {e}", exc_info=True)
            raise

    async def save_fund_report_stock_cninfo_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存基金重仓股-巨潮数据到MongoDB"""
        if df is None or df.empty:
            logger.warning("没有基金重仓股数据需要保存")
            return 0
        
        try:
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条基金重仓股数据...")
            
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    # 添加元数据
                    # 假设字段包含：基金代码、股票代码、截止日期/报告期
                    fund_code = str(doc.get('基金代码', '')) or str(doc.get('fund_code', ''))
                    stock_code = str(doc.get('股票代码', '')) or str(doc.get('stock_code', ''))
                    date_str = str(doc.get('报告期', '')) or str(doc.get('date', '')) or str(doc.get('截止日期', ''))
                    
                    doc['fund_code'] = fund_code
                    doc['stock_code'] = stock_code
                    doc['date'] = date_str
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_report_stock_cninfo'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    # 使用 基金代码 + 股票代码 + 报告期 作为唯一标识
                    if fund_code and stock_code and date_str:
                        ops.append(
                            UpdateOne(
                                {'fund_code': fund_code, 'stock_code': stock_code, 'date': date_str},
                                {'$set': doc},
                                upsert=True
                            )
                        )
                
                if ops:
                    result = await self.col_fund_report_stock_cninfo.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条基金重仓股数据")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存基金重仓股数据失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_report_stock_cninfo_data(self) -> int:
        """清空基金重仓股数据"""
        try:
            result = await self.col_fund_report_stock_cninfo.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条基金重仓股数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空基金重仓股数据失败: {e}", exc_info=True)
            raise
    
    async def get_fund_report_stock_cninfo_stats(self) -> Dict[str, Any]:
        """获取基金重仓股统计"""
        try:
            total_count = await self.col_fund_report_stock_cninfo.count_documents({})
            
            return {
                'total_count': total_count
            }
        except Exception as e:
            logger.error(f"获取基金重仓股统计失败: {e}", exc_info=True)
            raise

    async def save_fund_report_industry_allocation_cninfo_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存基金行业配置-巨潮数据到MongoDB"""
        if df is None or df.empty:
            logger.warning("没有基金行业配置数据需要保存")
            return 0
        
        try:
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条基金行业配置数据...")
            
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    # 添加元数据
                    # 假设字段包含：基金代码、行业名称、行业编码、截止日期/报告期
                    fund_code = str(doc.get('基金代码', '')) or str(doc.get('fund_code', ''))
                    industry_name = str(doc.get('行业名称', '')) or str(doc.get('industry_name', ''))
                    date_str = str(doc.get('报告期', '')) or str(doc.get('date', '')) or str(doc.get('截止日期', ''))
                    
                    doc['fund_code'] = fund_code
                    doc['industry_name'] = industry_name
                    doc['date'] = date_str
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_report_industry_allocation_cninfo'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    # 使用 基金代码 + 行业名称 + 报告期 作为唯一标识
                    if fund_code and industry_name and date_str:
                        ops.append(
                            UpdateOne(
                                {'fund_code': fund_code, 'industry_name': industry_name, 'date': date_str},
                                {'$set': doc},
                                upsert=True
                            )
                        )
                
                if ops:
                    result = await self.col_fund_report_industry_allocation_cninfo.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条基金行业配置数据")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存基金行业配置数据失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_report_industry_allocation_cninfo_data(self) -> int:
        """清空基金行业配置数据"""
        try:
            result = await self.col_fund_report_industry_allocation_cninfo.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条基金行业配置数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空基金行业配置数据失败: {e}", exc_info=True)
            raise
    
    async def get_fund_report_industry_allocation_cninfo_stats(self) -> Dict[str, Any]:
        """获取基金行业配置统计"""
        try:
            total_count = await self.col_fund_report_industry_allocation_cninfo.count_documents({})
            
            return {
                'total_count': total_count
            }
        except Exception as e:
            logger.error(f"获取基金行业配置统计失败: {e}", exc_info=True)
            raise

    async def save_fund_report_asset_allocation_cninfo_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存基金资产配置-巨潮数据到MongoDB"""
        if df is None or df.empty:
            logger.warning("没有基金资产配置数据需要保存")
            return 0
        
        try:
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条基金资产配置数据...")
            
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    # 添加元数据
                    # 假设字段包含：基金代码、截止日期/报告期
                    fund_code = str(doc.get('基金代码', '')) or str(doc.get('fund_code', ''))
                    date_str = str(doc.get('报告期', '')) or str(doc.get('date', '')) or str(doc.get('截止日期', ''))
                    
                    doc['fund_code'] = fund_code
                    doc['date'] = date_str
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_report_asset_allocation_cninfo'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    # 使用 基金代码 + 报告期 作为唯一标识
                    if fund_code and date_str:
                        ops.append(
                            UpdateOne(
                                {'fund_code': fund_code, 'date': date_str},
                                {'$set': doc},
                                upsert=True
                            )
                        )
                
                if ops:
                    result = await self.col_fund_report_asset_allocation_cninfo.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条基金资产配置数据")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存基金资产配置数据失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_report_asset_allocation_cninfo_data(self) -> int:
        """清空基金资产配置数据"""
        try:
            result = await self.col_fund_report_asset_allocation_cninfo.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条基金资产配置数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空基金资产配置数据失败: {e}", exc_info=True)
            raise
    
    async def get_fund_report_asset_allocation_cninfo_stats(self) -> Dict[str, Any]:
        """获取基金资产配置统计"""
        try:
            total_count = await self.col_fund_report_asset_allocation_cninfo.count_documents({})
            
            return {
                'total_count': total_count
            }
        except Exception as e:
            logger.error(f"获取基金资产配置统计失败: {e}", exc_info=True)
            raise

    async def save_fund_scale_change_em_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存规模变动-东财数据到MongoDB"""
        if df is None or df.empty:
            logger.warning("没有规模变动数据需要保存")
            return 0
        
        try:
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条规模变动数据...")
            
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    # 添加元数据
                    # 假设字段包含：截止日期、净资产、期间申购、期间赎回等，需要code
                    # 由于接口是按code查的，df里可能没有code，需要确保传入前加上
                    fund_code = str(doc.get('code', '')) or str(doc.get('fund_code', ''))
                    date_str = str(doc.get('截止日期', '')) or str(doc.get('date', ''))
                    
                    doc['fund_code'] = fund_code
                    doc['date'] = date_str
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_scale_change_em'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    # 使用 基金代码 + 截止日期 作为唯一标识
                    if fund_code and date_str:
                        ops.append(
                            UpdateOne(
                                {'fund_code': fund_code, 'date': date_str},
                                {'$set': doc},
                                upsert=True
                            )
                        )
                
                if ops:
                    result = await self.col_fund_scale_change_em.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条规模变动数据")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存规模变动数据失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_scale_change_em_data(self) -> int:
        """清空规模变动数据"""
        try:
            result = await self.col_fund_scale_change_em.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条规模变动数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空规模变动数据失败: {e}", exc_info=True)
            raise
    
    async def get_fund_scale_change_em_stats(self) -> Dict[str, Any]:
        """获取规模变动统计"""
        try:
            total_count = await self.col_fund_scale_change_em.count_documents({})
            unique_funds = await self.col_fund_scale_change_em.distinct('fund_code')
            
            return {
                'total_count': total_count,
                'unique_funds': len(unique_funds)
            }
        except Exception as e:
            logger.error(f"获取规模变动统计失败: {e}", exc_info=True)
            raise

    async def save_fund_hold_structure_em_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存持有人结构-东财数据到MongoDB"""
        if df is None or df.empty:
            logger.warning("没有持有人结构数据需要保存")
            return 0
        
        try:
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条持有人结构数据...")
            
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    # 添加元数据
                    # 假设字段包含：截止日期、机构持有比例、个人持有比例、内部持有比例、总份额等
                    # 需要code
                    fund_code = str(doc.get('code', '')) or str(doc.get('fund_code', ''))
                    date_str = str(doc.get('截止日期', '')) or str(doc.get('date', ''))
                    
                    doc['fund_code'] = fund_code
                    doc['date'] = date_str
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_hold_structure_em'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    # 使用 基金代码 + 截止日期 作为唯一标识
                    if fund_code and date_str:
                        ops.append(
                            UpdateOne(
                                {'fund_code': fund_code, 'date': date_str},
                                {'$set': doc},
                                upsert=True
                            )
                        )
                
                if ops:
                    result = await self.col_fund_hold_structure_em.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条持有人结构数据")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存持有人结构数据失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_hold_structure_em_data(self) -> int:
        """清空持有人结构数据"""
        try:
            result = await self.col_fund_hold_structure_em.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条持有人结构数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空持有人结构数据失败: {e}", exc_info=True)
            raise
    
    async def get_fund_hold_structure_em_stats(self) -> Dict[str, Any]:
        """获取持有人结构统计"""
        try:
            total_count = await self.col_fund_hold_structure_em.count_documents({})
            unique_funds = await self.col_fund_hold_structure_em.distinct('fund_code')
            
            return {
                'total_count': total_count,
                'unique_funds': len(unique_funds)
            }
        except Exception as e:
            logger.error(f"获取持有人结构统计失败: {e}", exc_info=True)
            raise

    async def save_fund_stock_position_lg_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存股票型基金仓位-乐咕乐股数据到MongoDB"""
        if df is None or df.empty:
            logger.warning("没有股票型基金仓位数据需要保存")
            return 0
        
        try:
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条股票型基金仓位数据...")
            
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    # 添加元数据
                    # 假设字段包含：date, 仓位
                    date_str = str(doc.get('date', '')) or str(doc.get('日期', ''))
                    
                    doc['date'] = date_str
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_stock_position_lg'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    # 使用 date 作为唯一标识
                    if date_str:
                        ops.append(
                            UpdateOne(
                                {'date': date_str},
                                {'$set': doc},
                                upsert=True
                            )
                        )
                
                if ops:
                    result = await self.col_fund_stock_position_lg.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条股票型基金仓位数据")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存股票型基金仓位数据失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_stock_position_lg_data(self) -> int:
        """清空股票型基金仓位数据"""
        try:
            result = await self.col_fund_stock_position_lg.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条股票型基金仓位数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空股票型基金仓位数据失败: {e}", exc_info=True)
            raise
    
    async def get_fund_stock_position_lg_stats(self) -> Dict[str, Any]:
        """获取股票型基金仓位统计"""
        try:
            total_count = await self.col_fund_stock_position_lg.count_documents({})
            
            return {
                'total_count': total_count
            }
        except Exception as e:
            logger.error(f"获取股票型基金仓位统计失败: {e}", exc_info=True)
            raise

    async def save_fund_balance_position_lg_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存平衡混合型基金仓位-乐咕乐股数据到MongoDB"""
        if df is None or df.empty:
            logger.warning("没有平衡混合型基金仓位数据需要保存")
            return 0
        
        try:
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条平衡混合型基金仓位数据...")
            
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    # 添加元数据
                    # 假设字段包含：date, 仓位
                    date_str = str(doc.get('date', '')) or str(doc.get('日期', ''))
                    
                    doc['date'] = date_str
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_balance_position_lg'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    # 使用 date 作为唯一标识
                    if date_str:
                        ops.append(
                            UpdateOne(
                                {'date': date_str},
                                {'$set': doc},
                                upsert=True
                            )
                        )
                
                if ops:
                    result = await self.col_fund_balance_position_lg.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条平衡混合型基金仓位数据")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存平衡混合型基金仓位数据失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_balance_position_lg_data(self) -> int:
        """清空平衡混合型基金仓位数据"""
        try:
            result = await self.col_fund_balance_position_lg.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条平衡混合型基金仓位数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空平衡混合型基金仓位数据失败: {e}", exc_info=True)
            raise
    
    async def get_fund_balance_position_lg_stats(self) -> Dict[str, Any]:
        """获取平衡混合型基金仓位统计"""
        try:
            total_count = await self.col_fund_balance_position_lg.count_documents({})
            
            return {
                'total_count': total_count
            }
        except Exception as e:
            logger.error(f"获取平衡混合型基金仓位统计失败: {e}", exc_info=True)
            raise

    async def save_fund_linghuo_position_lg_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存灵活配置型基金仓位-乐咕乐股数据到MongoDB"""
        if df is None or df.empty:
            logger.warning("没有灵活配置型基金仓位数据需要保存")
            return 0
        
        try:
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条灵活配置型基金仓位数据...")
            
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    # 添加元数据
                    # 假设字段包含：date, 仓位
                    date_str = str(doc.get('date', '')) or str(doc.get('日期', ''))
                    
                    doc['date'] = date_str
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_linghuo_position_lg'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    # 使用 date 作为唯一标识
                    if date_str:
                        ops.append(
                            UpdateOne(
                                {'date': date_str},
                                {'$set': doc},
                                upsert=True
                            )
                        )
                
                if ops:
                    result = await self.col_fund_linghuo_position_lg.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条灵活配置型基金仓位数据")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存灵活配置型基金仓位数据失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_linghuo_position_lg_data(self) -> int:
        """清空灵活配置型基金仓位数据"""
        try:
            result = await self.col_fund_linghuo_position_lg.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条灵活配置型基金仓位数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空灵活配置型基金仓位数据失败: {e}", exc_info=True)
            raise
    
    async def get_fund_linghuo_position_lg_stats(self) -> Dict[str, Any]:
        """获取灵活配置型基金仓位统计"""
        try:
            total_count = await self.col_fund_linghuo_position_lg.count_documents({})
            
            return {
                'total_count': total_count
            }
        except Exception as e:
            logger.error(f"获取灵活配置型基金仓位统计失败: {e}", exc_info=True)
            raise

    async def save_fund_announcement_dividend_em_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存基金公告分红配送-东财数据到MongoDB"""
        if df is None or df.empty:
            logger.warning("没有基金公告分红配送数据需要保存")
            return 0
        
        try:
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条基金公告分红配送数据...")
            
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    # 添加元数据
                    # 假设字段包含：公告日期、公告标题、公告内容等
                    # 唯一标识可能是：基金代码 + 公告标题 + 公告日期
                    
                    fund_code = str(doc.get('code', '')) or str(doc.get('symbol', ''))
                    title = str(doc.get('公告标题', '')) or str(doc.get('title', ''))
                    date_str = str(doc.get('公告日期', '')) or str(doc.get('date', ''))
                    
                    doc['fund_code'] = fund_code
                    doc['title'] = title
                    doc['date'] = date_str
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_announcement_dividend_em'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    # 唯一标识：fund_code + title + date
                    if fund_code and title and date_str:
                        ops.append(
                            UpdateOne(
                                {'fund_code': fund_code, 'title': title, 'date': date_str},
                                {'$set': doc},
                                upsert=True
                            )
                        )
                
                if ops:
                    result = await self.col_fund_announcement_dividend_em.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条基金公告分红配送数据")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存基金公告分红配送数据失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_announcement_dividend_em_data(self) -> int:
        """清空基金公告分红配送数据"""
        try:
            result = await self.col_fund_announcement_dividend_em.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条基金公告分红配送数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空基金公告分红配送数据失败: {e}", exc_info=True)
            raise
    
    async def get_fund_announcement_dividend_em_stats(self) -> Dict[str, Any]:
        """获取基金公告分红配送统计"""
        try:
            total_count = await self.col_fund_announcement_dividend_em.count_documents({})
            unique_funds = await self.col_fund_announcement_dividend_em.distinct('fund_code')
            
            return {
                'total_count': total_count,
                'unique_funds': len(unique_funds)
            }
        except Exception as e:
            logger.error(f"获取基金公告分红配送统计失败: {e}", exc_info=True)
            raise

    async def save_fund_announcement_report_em_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存基金公告定期报告-东财数据到MongoDB"""
        if df is None or df.empty:
            logger.warning("没有基金公告定期报告数据需要保存")
            return 0
        
        try:
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条基金公告定期报告数据...")
            
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    # 添加元数据
                    # 假设字段包含：公告日期、公告标题、公告内容等
                    
                    fund_code = str(doc.get('code', '')) or str(doc.get('symbol', ''))
                    title = str(doc.get('公告标题', '')) or str(doc.get('title', ''))
                    date_str = str(doc.get('公告日期', '')) or str(doc.get('date', ''))
                    
                    doc['fund_code'] = fund_code
                    doc['title'] = title
                    doc['date'] = date_str
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_announcement_report_em'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    # 唯一标识：fund_code + title + date
                    if fund_code and title and date_str:
                        ops.append(
                            UpdateOne(
                                {'fund_code': fund_code, 'title': title, 'date': date_str},
                                {'$set': doc},
                                upsert=True
                            )
                        )
                
                if ops:
                    result = await self.col_fund_announcement_report_em.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条基金公告定期报告数据")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存基金公告定期报告数据失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_announcement_report_em_data(self) -> int:
        """清空基金公告定期报告数据"""
        try:
            result = await self.col_fund_announcement_report_em.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条基金公告定期报告数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空基金公告定期报告数据失败: {e}", exc_info=True)
            raise
    
    async def get_fund_announcement_report_em_stats(self) -> Dict[str, Any]:
        """获取基金公告定期报告统计"""
        try:
            total_count = await self.col_fund_announcement_report_em.count_documents({})
            unique_funds = await self.col_fund_announcement_report_em.distinct('fund_code')
            
            return {
                'total_count': total_count,
                'unique_funds': len(unique_funds)
            }
        except Exception as e:
            logger.error(f"获取基金公告定期报告统计失败: {e}", exc_info=True)
            raise

    async def save_fund_announcement_personnel_em_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """保存基金公告人事调整-东财数据到MongoDB"""
        if df is None or df.empty:
            logger.warning("没有基金公告人事调整数据需要保存")
            return 0
        
        try:
            import numpy as np
            df = df.replace([np.inf, -np.inf], None)
            df = df.where(pd.notna(df), None)
            
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条基金公告人事调整数据...")
            
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    import math
                    import datetime as dt
                    for key, value in list(doc.items()):
                        if isinstance(value, (int, float)) and not isinstance(value, bool):
                            try:
                                if math.isnan(value) or math.isinf(value):
                                    doc[key] = None
                            except (TypeError, ValueError):
                                pass
                        elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                        elif isinstance(value, dt.datetime):
                            doc[key] = value.strftime('%Y-%m-%d')
                    
                    # 添加元数据
                    # 字段：基金代码、公告标题、基金名称、公告日期、报告ID
                    
                    fund_code = str(doc.get('基金代码', '')) or str(doc.get('code', ''))
                    title = str(doc.get('公告标题', '')) or str(doc.get('title', ''))
                    fund_name = str(doc.get('基金名称', '')) or str(doc.get('name', ''))
                    date_str = str(doc.get('公告日期', '')) or str(doc.get('date', ''))
                    report_id = str(doc.get('报告ID', '')) or str(doc.get('report_id', ''))
                    
                    doc['fund_code'] = fund_code
                    doc['title'] = title
                    doc['fund_name'] = fund_name
                    doc['date'] = date_str
                    doc['report_id'] = report_id
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_announcement_personnel_em'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    # 唯一标识：fund_code + report_id（报告ID是唯一的）
                    if fund_code and report_id:
                        ops.append(
                            UpdateOne(
                                {'fund_code': fund_code, 'report_id': report_id},
                                {'$set': doc},
                                upsert=True
                            )
                        )
                
                if ops:
                    result = await self.col_fund_announcement_personnel_em.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条基金公告人事调整数据")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存基金公告人事调整数据失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_announcement_personnel_em_data(self) -> int:
        """清空基金公告人事调整数据"""
        try:
            result = await self.col_fund_announcement_personnel_em.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条基金公告人事调整数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空基金公告人事调整数据失败: {e}", exc_info=True)
            raise
    
    async def get_fund_announcement_personnel_em_stats(self) -> Dict[str, Any]:
        """获取基金公告人事调整统计"""
        try:
            total_count = await self.col_fund_announcement_personnel_em.count_documents({})
            unique_funds = await self.col_fund_announcement_personnel_em.distinct('fund_code')
            
            return {
                'total_count': total_count,
                'unique_funds': len(unique_funds)
            }
        except Exception as e:
            logger.error(f"获取基金公告人事调整统计失败: {e}", exc_info=True)
            raise
