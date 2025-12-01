"""
基金评级汇总-东财服务（重构版：继承SimpleService，无参数接口，不需要批量更新）
"""
from typing import Dict, Any
import logging
import asyncio

from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.funds.providers.fund_rating_all_em_provider import FundRatingAllEmProvider
from app.services.database.control_mongodb import ControlMongodb

logger = logging.getLogger(__name__)


class FundRatingAllEmService(SimpleService):
    """基金评级汇总-东财服务（无参数接口，直接获取所有数据）"""
    
    # ===== 必须定义的属性 =====
    collection_name = "fund_rating_all_em"
    provider_class = FundRatingAllEmProvider
    
    # ===== 可选配置 =====
    time_field = "scraped_at"
    
    # 唯一键配置（根据实际返回的数据字段）
    unique_keys = ["代码"]
    
    # 额外的元数据字段
    extra_metadata = {
        "数据源": "akshare",
        "接口名称": "fund_rating_all_em",
    }
    
    # 类级别的锁，防止并发执行更新
    _update_lock = asyncio.Lock()
    
    async def update_single_data(self, **kwargs) -> Dict[str, Any]:
        """
        更新单条数据（无参数接口，直接获取所有数据）
        
        重写基类方法，确保不传递任何参数给 provider
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
                self.logger.info(f"[{self.collection_name}] update_single_data 收到参数: {kwargs}（将忽略所有参数）")
                self.logger.info(f"[{self.collection_name}] 开始获取数据...")
                
                # 不传递任何参数给 provider（fund_rating_all_em 接口不需要参数）
                df = self.provider.fetch_data()
                
                self.logger.info(f"[{self.collection_name}] 数据获取完成，共 {len(df) if df is not None and not df.empty else 0} 条")
                
                if df is None or df.empty:
                    self.logger.warning(f"[{self.collection_name}] provider 返回空数据")
                    return {
                        "success": True,
                        "message": "No data available",
                        "inserted": 0,
                    }
                
                # 按 field_info 的顺序重新排列 DataFrame 列
                df = self._reorder_dataframe_columns(df)
                
                self.logger.info(f"[{self.collection_name}] 开始保存数据到数据库...")
                
                # 使用 ControlMongodb 保存数据
                unique_keys = self._get_unique_keys()
                extra_fields = self._get_extra_fields()
                
                control_db = ControlMongodb(self.collection, unique_keys, self.current_user)
                result = await control_db.save_dataframe_to_collection(df, extra_fields=extra_fields)
                
                self.logger.info(f"[{self.collection_name}] 数据保存完成: 新增={result.get('inserted', 0)}, 更新={result.get('updated', 0)}")
                
                return {
                    "success": result["success"],
                    "message": result["message"],
                    "inserted": result.get("inserted", 0) + result.get("updated", 0),
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
        批量更新（无参数接口，批量更新和单条更新是一样的，直接调用单条更新）
        
        重写基类方法，因为无参数接口不需要批量更新逻辑
        """
        # 对于无参数接口，批量更新和单条更新是一样的，直接调用单条更新
        return await self.update_single_data(**kwargs)
