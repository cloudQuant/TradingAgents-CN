"""
沪深债券实时行情服务（重构版：继承SimpleService）

需求文档: tests/bonds/requirements/03_沪深债券实时行情.md
数据唯一标识: 代码
"""
import asyncio
from typing import Dict, Any

from app.services.data_sources.base_service import SimpleService
from app.services.database.control_mongodb import ControlMongodb
from ..providers.bond_zh_hs_spot_provider import BondZhHsSpotProvider


class BondZhHsSpotService(SimpleService):
    """沪深债券实时行情服务"""
    
    collection_name = "bond_zh_hs_spot"
    provider_class = BondZhHsSpotProvider
    
    # 类级别的锁，防止并发执行更新
    _update_lock = asyncio.Lock()
    
    async def update_single_data(self, **kwargs) -> Dict[str, Any]:
        """
        更新数据（支持 start_page 和 end_page 参数）
        
        使用锁机制防止并发执行，避免重复获取数据
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
                self.logger.info(f"[{self.collection_name}] update_single_data 收到参数: {kwargs}")
                
                # 过滤掉前端特有的参数
                frontend_only_params = {
                    'update_type', 'update_mode', 'batch_update', 'batch_size',
                    'page', 'limit', 'skip', 'filters', 'sort', 'order',
                    'task_id', 'callback', 'async', 'timeout', '_t', '_timestamp',
                    'force', 'clear_first', 'overwrite', 'mode', 'concurrency'
                }
                
                provider_kwargs = {
                    k: v for k, v in kwargs.items()
                    if k not in frontend_only_params and v is not None
                }
                
                self.logger.info(f"[{self.collection_name}] 开始获取数据, 参数: {provider_kwargs}")
                
                # 调用 provider 获取数据
                df = self.provider.fetch_data(**provider_kwargs)
                
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
