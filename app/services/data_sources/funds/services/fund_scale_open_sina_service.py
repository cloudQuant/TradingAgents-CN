"""
开放式基金规模-新浪服务（重构版：继承SimpleService，遍历所有基金类型）
"""
from typing import Dict, Any, List
import logging
import asyncio
import pandas as pd

from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.funds.providers.fund_scale_open_sina_provider import FundScaleOpenSinaProvider
from app.services.database.control_mongodb import ControlMongodb

logger = logging.getLogger(__name__)


class FundScaleOpenSinaService(SimpleService):
    """开放式基金规模-新浪服务（遍历所有基金类型）"""
    
    # ===== 必须定义的属性 =====
    collection_name = "fund_scale_open_sina"
    provider_class = FundScaleOpenSinaProvider
    
    # ===== 可选配置 =====
    time_field = "scraped_at"
    
    # 唯一键配置（基金代码 + 更新日期）
    unique_keys = ["基金代码", "更新日期"]
    
    # 基金类型列表
    FUND_TYPES = ["股票型基金", "混合型基金", "债券型基金", "货币型基金", "QDII基金"]
    
    # 额外的元数据字段
    extra_metadata = {
        "数据源": "akshare",
        "接口名称": "fund_scale_open_sina",
    }
    
    # 类级别的锁，防止并发执行更新
    _update_lock = asyncio.Lock()
    
    async def update_single_data(self, **kwargs) -> Dict[str, Any]:
        """
        更新单条数据（遍历所有基金类型）
        
        重写基类方法，遍历所有基金类型，分别获取数据并保存
        使用锁机制防止并发执行
        """
        # 使用锁防止并发执行
        if self._update_lock.locked():
            self.logger.warning(f"[{self.collection_name}] 检测到并发更新请求，跳过本次请求（已有更新任务在进行中）")
            return {
                "success": False,
                "message": "已有更新任务正在进行中，请稍后再试",
                "inserted": 0,
            }
        
        async with self._update_lock:
            try:
                self.logger.info(f"[{self.collection_name}] update_single_data 收到参数: {kwargs}（将遍历所有基金类型）")
                self.logger.info(f"[{self.collection_name}] 开始遍历基金类型获取数据...")
                
                all_dfs = []
                total_inserted = 0
                total_updated = 0
                
                # 遍历所有基金类型
                for fund_type in self.FUND_TYPES:
                    try:
                        self.logger.info(f"[{self.collection_name}] 正在获取 {fund_type} 的数据...")
                        
                        # 调用 provider 获取数据
                        df = self.provider.fetch_data(symbol=fund_type)
                        
                        if df is not None and not df.empty:
                            all_dfs.append(df)
                            self.logger.info(f"[{self.collection_name}] {fund_type} 获取完成，共 {len(df)} 条")
                        else:
                            self.logger.warning(f"[{self.collection_name}] {fund_type} 返回空数据")
                            
                    except Exception as e:
                        self.logger.error(f"[{self.collection_name}] 获取 {fund_type} 数据失败: {str(e)}", exc_info=True)
                        # 继续处理其他基金类型
                        continue
                
                if not all_dfs:
                    self.logger.warning(f"[{self.collection_name}] 所有基金类型都返回空数据")
                    return {
                        "success": True,
                        "message": "No data available",
                        "inserted": 0,
                    }
                
                # 合并所有 DataFrame
                combined_df = pd.concat(all_dfs, ignore_index=True)
                self.logger.info(f"[{self.collection_name}] 数据获取完成，共 {len(combined_df)} 条（来自 {len(all_dfs)} 个基金类型）")
                
                # 按 field_info 的顺序重新排列 DataFrame 列
                combined_df = self._reorder_dataframe_columns(combined_df)
                
                self.logger.info(f"[{self.collection_name}] 开始保存数据到数据库...")
                
                # 使用 ControlMongodb 保存数据
                unique_keys = self._get_unique_keys()
                extra_fields = self._get_extra_fields()
                
                control_db = ControlMongodb(self.collection, unique_keys, self.current_user)
                result = await control_db.save_dataframe_to_collection(combined_df, extra_fields=extra_fields)
                
                total_inserted = result.get("inserted", 0)
                total_updated = result.get("updated", 0)
                
                self.logger.info(f"[{self.collection_name}] 数据保存完成: 新增={total_inserted}, 更新={total_updated}")
                
                return {
                    "success": result["success"],
                    "message": result["message"],
                    "inserted": total_inserted + total_updated,
                    "details": result,
                }
                
            except Exception as e:
                self.logger.error(f"[{self.collection_name}] update_single_data 发生错误: {str(e)}", exc_info=True)
                return {
                    "success": False,
                    "message": str(e),
                    "inserted": 0,
                }
    
    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        """
        批量更新（遍历所有基金类型，批量更新和单条更新是一样的，直接调用单条更新）
        
        重写基类方法，因为不需要批量更新逻辑
        """
        # 对于遍历所有基金类型的接口，批量更新和单条更新是一样的，直接调用单条更新
        return await self.update_single_data(**kwargs)
