"""
香港基金历史数据-东财服务（重构版：继承BaseService）

支持批量更新，从 fund_hk_rank_em 获取香港基金代码列表
目前只获取历史净值明细数据（分红送配详情接口暂时有问题，已禁用）
"""
from typing import Dict, Any, List
import logging
from app.services.data_sources.base_service import BaseService
from ..providers.fund_hk_hist_em_provider import FundHkHistEmProvider
from app.services.database.control_mongodb import ControlMongodb

logger = logging.getLogger(__name__)


class FundHkHistEmService(BaseService):
    """香港基金历史数据-东财服务"""
    
    # ===== 必须定义的属性 =====
    collection_name = "fund_hk_hist_em"
    provider_class = FundHkHistEmProvider
    
    # ===== 可选配置 =====
    time_field = "净值日期"
    
    # 批量更新配置：从 fund_hk_rank_em 获取香港基金代码列表
    batch_source_collection = "fund_hk_rank_em"
    batch_source_field = "香港基金代码"  # 使用香港基金代码字段
    batch_concurrency = 3
    batch_progress_interval = 50
    batch_size = 3  # 批量处理时，每批处理的基金数量（默认3个）
    
    # 增量更新检查字段（只检查 code，因为目前只获取净值数据）
    incremental_check_fields = ["code"]
    
    # 唯一键配置（code + symbol + 净值日期）
    # 注意：虽然只获取净值数据，但保留 symbol 字段以便后续扩展
    unique_keys = ["code", "symbol", "净值日期"]
    
    # 额外的元数据字段
    extra_metadata = {
        "数据源": "akshare",
        "接口名称": "fund_hk_fund_hist_em",
    }
    
    def get_batch_params(self, *args) -> Dict[str, Any]:
        """
        构建批量任务的参数
        
        目前只支持获取历史净值明细数据（分红送配详情接口暂时有问题，已禁用）
        """
        if len(args) >= 1:
            # 只返回历史净值明细的参数
            return {"code": args[0], "symbol": "历史净值明细"}
        else:
            return {}
    
    async def _get_tasks_to_process(
        self, 
        codes: List[str], 
        years: List[str],
        update_mode: str = "incremental"
    ) -> List[tuple]:
        """
        重写任务生成逻辑，只生成历史净值明细任务
        
        注意：分红送配详情接口暂时有问题，已禁用
        批量处理时，将基金代码列表分成多个批次，每批默认3个
        
        Args:
            codes: 基金代码列表
            years: 年份列表（此服务不使用）
            update_mode: 更新模式，'full' 表示全量更新（跳过增量检查），'incremental' 表示增量更新
        """
        # 只生成历史净值明细任务
        symbol = "历史净值明细"
        
        self.logger.info(
            f"[{self.collection_name}] 生成任务：收到 {len(codes)} 个代码，"
            f"更新模式: {update_mode}, 增量检查字段: {self.incremental_check_fields}"
        )
        
        # 全量更新时，跳过增量检查，直接返回所有代码
        if update_mode == "full":
            self.logger.info(
                f"[{self.collection_name}] 全量更新模式，跳过增量检查，返回所有 {len(codes)} 个代码"
            )
            return [(code,) for code in codes]
        
        if not self.incremental_check_fields:
            # 没有配置增量检查，返回所有基金代码
            self.logger.info(f"[{self.collection_name}] 无增量检查，返回所有 {len(codes)} 个代码")
            return [(code,) for code in codes]
        
        # 获取已存在的组合（只检查 code）
        existing = await self._get_existing_combinations()
        self.logger.info(
            f"[{self.collection_name}] 已存在 {len(existing)} 个组合，"
            f"待处理代码数: {len(codes)}"
        )
        
        # 过滤出需要处理的任务
        tasks = [
            (code,) 
            for code in codes 
            if (code,) not in existing
        ]
        
        self.logger.info(
            f"[{self.collection_name}] 过滤后需要处理 {len(tasks)} 个任务"
        )
        
        return tasks
    
    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        """
        重写批量更新方法，支持分批处理
        
        将基金代码列表分成多个批次，每批默认3个，逐批处理
        """
        try:
            from app.utils.task_manager import get_task_manager
            task_manager = get_task_manager() if task_id else None
            
            # 获取批量大小（默认3个）
            batch_size = getattr(self, 'batch_size', 3)
            if batch_size <= 0:
                batch_size = 3
            
            # 获取所有基金代码
            if task_manager and task_id:
                task_manager.update_progress(
                    task_id, 0, 100, 
                    f"正在从 {self.batch_source_collection} 获取代码列表..."
                )
            
            codes = await self._get_source_codes()
            
            self.logger.info(
                f"[{self.collection_name}] 从 {self.batch_source_collection} "
                f"获取到 {len(codes)} 个代码（字段: {self.batch_source_field}）"
            )
            
            if not codes:
                if task_manager and task_id:
                    task_manager.fail_task(
                        task_id, 
                        f"{self.batch_source_collection} 集合为空，请先更新相关数据"
                    )
                return {
                    "success": False,
                    "message": f"{self.batch_source_collection} 集合为空",
                    "inserted": 0,
                }
            
            total_codes = len(codes)
            self.logger.info(
                f"[{self.collection_name}] 从 {self.batch_source_collection} 获取到 {total_codes} 个代码，"
                f"将分成 {batch_size} 个一批进行处理"
            )
            
            # 将代码列表分成多个批次
            batches = [codes[i:i + batch_size] for i in range(0, total_codes, batch_size)]
            total_batches = len(batches)
            
            # 获取并发数（从 kwargs 中获取，默认使用 batch_concurrency）
            concurrency = int(kwargs.get("concurrency", self.batch_concurrency))
            
            if task_manager and task_id:
                task_manager.update_progress(
                    task_id, 5, 100, 
                    f"共 {total_codes} 个基金，分成 {total_batches} 批处理（每批 {batch_size} 个，并发数 {concurrency}）"
                )
            
            # 累计结果
            total_inserted = 0
            total_processed = 0
            total_success = 0
            total_failed = 0
            
            # 逐批处理
            for batch_idx, batch_codes in enumerate(batches, 1):
                self.logger.info(
                    f"[{self.collection_name}] 处理第 {batch_idx}/{total_batches} 批，"
                    f"包含 {len(batch_codes)} 个基金: {batch_codes[:3]}{'...' if len(batch_codes) > 3 else ''}"
                )
                
                # 为当前批次生成任务
                years = self._get_years_range(kwargs.get("year"))
                update_mode = kwargs.get("update_mode", "incremental")
                tasks_to_process = await self._get_tasks_to_process(batch_codes, years, update_mode)
                
                if tasks_to_process:
                    # 更新进度：显示当前批次信息
                    if task_manager and task_id:
                        progress_base = 5  # 起始进度
                        progress_range = 90  # 可用进度范围
                        current_progress = progress_base + int((batch_idx - 1) / total_batches * progress_range)
                        task_manager.update_progress(
                            task_id, 
                            current_progress,
                            100,
                            f"正在处理第 {batch_idx}/{total_batches} 批（{len(batch_codes)} 个基金，并发数 {concurrency}）..."
                        )
                    
                    # 执行当前批次的任务（使用之前获取的并发数）
                    # 注意：should_complete_task=False，因为这是分批处理，由外层完成所有批次后再完成任务
                    batch_result = await self._execute_batch_tasks(
                        tasks_to_process,
                        task_id,
                        task_manager,
                        concurrency,
                        should_complete_task=False
                    )
                    
                    # 累计结果
                    total_inserted += batch_result.get("inserted", 0)
                    total_processed += batch_result.get("processed", 0)
                    total_success += batch_result.get("success_count", 0)
                    total_failed += batch_result.get("failed", 0)
                    
                    # 更新进度：显示当前批次完成情况
                    if task_manager and task_id:
                        progress_base = 5
                        progress_range = 90
                        current_progress = progress_base + int(batch_idx / total_batches * progress_range)
                        task_manager.update_progress(
                            task_id,
                            current_progress,
                            100,
                            f"第 {batch_idx}/{total_batches} 批完成：成功 {batch_result.get('success_count', 0)} 个，失败 {batch_result.get('failed', 0)} 个"
                        )
                else:
                    self.logger.info(f"[{self.collection_name}] 第 {batch_idx} 批数据已存在，跳过")
            
            # 返回总体结果
            message_parts = [
                f"批量更新完成：共处理 {total_batches} 批（每批 {batch_size} 个，并发数 {concurrency}）",
                f"成功 {total_success} 个",
                f"失败 {total_failed} 个",
                f"保存 {total_inserted} 条记录"
            ]
            message = "，".join(message_parts)
            
            self.logger.info(
                f"[{self.collection_name}] {message}，"
                f"总处理数: {total_processed}"
            )
            
            if task_manager and task_id:
                task_manager.update_progress(task_id, 100, 100, message)
                task_manager.complete_task(
                    task_id,
                    result={
                        "inserted": total_inserted,
                        "processed": total_processed,
                        "success_count": total_success,
                        "failed": total_failed,
                    },
                    message=message
                )
            
            return {
                "success": True,
                "message": message,
                "inserted": total_inserted,
                "processed": total_processed,
                "success_count": total_success,
                "failed": total_failed,
            }
            
        except Exception as e:
            self.logger.error(f"[{self.collection_name}] 批量更新失败: {e}", exc_info=True)
            if task_manager and task_id:
                task_manager.fail_task(task_id, str(e))
            return {
                "success": False,
                "message": str(e),
                "inserted": 0,
            }
    
    
    async def update_single_data(self, **kwargs) -> Dict[str, Any]:
        """
        更新单条数据（需要 code 和 symbol 参数）
        
        如果没有提供 symbol，默认获取 "历史净值明细"
        """
        try:
            self.logger.info(f"[{self.collection_name}] update_single_data 收到参数: {kwargs}")
            
            # 参数解析
            code = kwargs.get("code") or kwargs.get("fund_code") or kwargs.get("fund")
            symbol = kwargs.get("symbol", "历史净值明细")  # 默认获取历史净值明细
            
            self.logger.info(f"[{self.collection_name}] 解析参数: code={code}, symbol={symbol}")
            
            # 参数验证
            if not code:
                return {
                    "success": False,
                    "message": "缺少必须参数: code（香港基金代码，单条更新需要提供基金代码）",
                    "inserted": 0,
                }
            
            # 验证 symbol 参数（目前只支持历史净值明细）
            if symbol != "历史净值明细":
                return {
                    "success": False,
                    "message": f"symbol 参数无效: {symbol}，目前只支持 '历史净值明细'（分红送配详情接口暂时有问题，已禁用）",
                    "inserted": 0,
                }
            
            self.logger.info(f"[{self.collection_name}] 调用 provider.fetch_data(code={code}, symbol={symbol})")
            df = self.provider.fetch_data(code=code, symbol=symbol)
            
            if df is None or df.empty:
                self.logger.warning(f"[{self.collection_name}] provider 返回空数据")
                return {
                    "success": True,
                    "message": "No data available",
                    "inserted": 0,
                }
            
            # 按 field_info 的顺序重新排列 DataFrame 列
            df = self._reorder_dataframe_columns(df)
            
            # 使用 ControlMongodb 处理数据去重
            unique_keys = self._get_unique_keys()
            extra_fields = self._get_extra_fields()
            
            control_db = ControlMongodb(self.collection, unique_keys)
            result = await control_db.save_dataframe_to_collection(df, extra_fields=extra_fields)
            
            return {
                "success": result["success"],
                "message": result["message"],
                "inserted": result.get("inserted", 0) + result.get("updated", 0),
                "details": result,
            }
            
        except Exception as e:
            self.logger.error(f"[{self.collection_name}] update_single_data 发生错误: {str(e)}")
            return {
                "success": False,
                "message": str(e),
                "inserted": 0,
            }
