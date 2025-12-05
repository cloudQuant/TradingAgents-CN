"""
通用数据服务基类

所有数据服务（funds, bonds, stocks, futures, options等）都可以继承此基类。
提供通用的数据查询、更新、批量更新等功能。

使用示例：
    # 方式1：简单服务（无参数接口）
    class FundNameEmService(BaseService):
        collection_name = "fund_name_em"
        provider_class = FundNameEmProvider
    
    # 方式2：需要参数的服务
    class FundPortfolioHoldEmService(BaseService):
        collection_name = "fund_portfolio_hold_em"
        provider_class = FundPortfolioHoldEmProvider
        
        # 定义批量更新的数据源
        batch_source_collection = "fund_name_em"
        batch_source_field = "基金代码"
        batch_years_range = (2010, None)  # 从2010年到今年
        
        # 自定义批量更新的参数验证
        def get_batch_params(self, code, year):
            return {"fund_code": code, "year": year}
"""
from typing import Optional, Dict, Any, List, Set, Tuple, Type, Callable
from datetime import datetime
import logging
import asyncio
from abc import ABC
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import pandas as pd

from app.services.database.control_mongodb import ControlMongodb
from app.utils.task_manager import get_task_manager
from .base_provider import BaseProvider

logger = logging.getLogger(__name__)


class BaseService(ABC):
    """通用数据服务基类"""
    
    # -------------------------------------------------------------------------------------------------
    # 设计说明：
    # 1. BaseService 将“刷新任务”拆成 service / provider / ControlMongodb 三层。
    # 2. service 负责任务调度、进度管理、批量并发、增量判断、落库时机等；provider 只关心数据获取；
    # 3. 具体集合只需要声明 collection_name / provider_class 以及若干 batch 配置即可获得完整能力。
    # -------------------------------------------------------------------------------------------------

    # ===== 子类必须定义的属性 =====
    collection_name: str = ""               # 集合名称
    provider_class: Type[BaseProvider] = None  # Provider类
    
    # ===== 子类可选定义的属性 =====
    
    # 时间字段名（用于排序和概览）
    time_field: str = "更新时间"
    
    # 批量更新相关配置
    batch_source_collection: str = ""       # 批量更新时从哪个集合获取代码列表
    batch_source_field: str = ""            # 从源集合获取的字段名
    batch_years_range: Tuple[int, int] = None  # 年份范围，如 (2010, None) 表示2010到今年
    batch_use_year: bool = False            # 批量更新是否需要年份参数
    batch_concurrency: int = 3              # 默认并发数
    batch_progress_interval: int = 50       # 进度更新间隔
    batch_task_timeout: int = 300           # 单个任务超时时间（秒），默认5分钟
    
    # 增量更新：用于检查已存在数据的字段
    # 例如：["基金代码", "季度"] 用于检查组合是否已存在
    incremental_check_fields: List[str] = []
    
    # 字段值提取器：用于从字段值中提取关键信息
    # 例如：从"季度"字段（"2024年1季度"）中提取年份（"2024"）
    # 格式：{字段名: 提取函数}
    # incremental_field_extractor = {"季度": lambda q: q[:4] if len(q) >= 4 and q[:4].isdigit() else ""}
    incremental_field_extractor: Optional[Dict[str, Callable[[str], str]]] = None
    
    # 唯一键配置（如果provider没有get_unique_keys方法，使用此配置）
    unique_keys: List[str] = []
    
    # 额外的元数据字段
    extra_metadata: Dict[str, str] = {
        "数据源": "akshare",
    }
    
    def __init__(self, db: AsyncIOMotorClient, current_user: Optional[Dict[str, Any]] = None):
        self.db = db
        self.collection = db[self.collection_name]
        self.provider = self.provider_class() if self.provider_class else None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.current_user = current_user
    
    # ==================== 查询方法 ====================
    
    async def get_overview(self) -> Dict[str, Any]:
        """获取数据概览"""
        total_count = await self.collection.count_documents({})
        
        latest = await self.collection.find_one(sort=[(self.time_field, -1)])
        oldest = await self.collection.find_one(sort=[(self.time_field, 1)])
        
        return {
            "total_count": total_count,
            "last_updated": latest.get(self.time_field) if latest else None,
            "oldest_date": oldest.get(self.time_field) if oldest else None,
        }
    
    async def get_data(
        self,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """获取数据列表"""
        query = filters or {}
        
        cursor = self.collection.find(query).skip(skip).limit(limit).sort(self.time_field, -1)
        data = await cursor.to_list(length=limit)
        
        total = await self.collection.count_documents(query)
        
        # 转换 ObjectId 为字符串，datetime 转 ISO 格式
        for item in data:
            item["_id"] = str(item["_id"])
            if self.time_field in item and isinstance(item[self.time_field], datetime):
                item[self.time_field] = item[self.time_field].isoformat()
        
        return {
            "data": data,
            "total": total,
            "skip": skip,
            "limit": limit,
        }
    
    async def clear_data(self) -> Dict[str, Any]:
        """清空集合数据"""
        try:
            result = await self.collection.delete_many({})
            return {
                "success": True,
                "deleted_count": result.deleted_count,
                "message": f"已删除 {result.deleted_count} 条数据"
            }
        except Exception as e:
            self.logger.error(f"[{self.collection_name}] 清空数据失败: {e}")
            return {"success": False, "message": str(e)}
    
    # ==================== 更新方法 ====================
    
    async def update_single_data(self, **kwargs) -> Dict[str, Any]:
        """
        更新单条数据
        
        子类可重写此方法以实现自定义逻辑，如参数验证
        """
        try:
            self.logger.info(f"[{self.collection_name}] update_single_data 收到参数: {kwargs}")
            
            # 过滤掉前端特有的参数，这些参数不应该传递给 provider
            frontend_only_params = {
                'update_type', 'update_mode', 'batch_update', 'batch_size', 
                'page', 'limit', 'skip', 'filters', 'sort', 'order',
                'task_id', 'callback', 'async', 'timeout', '_t', '_timestamp',
                'force', 'clear_first', 'overwrite', 'mode', 'concurrency',
            }
            
            # 移除前端特有参数和值为None的参数
            provider_kwargs = {
                k: v for k, v in kwargs.items() 
                if k not in frontend_only_params and v is not None
            }
            
            # 调用 provider 获取数据
            df = self.provider.fetch_data(**provider_kwargs)
            
            if df is None or df.empty:
                self.logger.warning(f"[{self.collection_name}] provider 返回空数据")
                return {
                    "success": True,
                    "message": "No data available",
                    "inserted": 0,
                }
            
            # 按 field_info 的顺序重新排列 DataFrame 列
            df = self._reorder_dataframe_columns(df)
            
            # 使用 ControlMongodb 保存数据
            unique_keys = self._get_unique_keys()
            extra_fields = self._get_extra_fields()
            
            control_db = ControlMongodb(self.collection, unique_keys, self.current_user)
            result = await control_db.save_dataframe_to_collection(df, extra_fields=extra_fields)
            
            return {
                "success": result["success"],
                "message": result["message"],
                "inserted": result.get("inserted", 0) + result.get("updated", 0),
                "details": result,
            }
            
        except ValueError as e:
            # 参数验证错误
            return {
                "success": False,
                "message": str(e),
                "inserted": 0,
            }
        except Exception as e:
            self.logger.error(f"[{self.collection_name}] update_single_data 发生错误: {str(e)}")
            return {
                "success": False,
                "message": str(e),
                "inserted": 0,
            }
    
    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        """
        批量更新数据
        
        如果配置了 batch_source_collection，会自动从该集合获取代码列表进行批量更新。
        否则，简单调用 update_single_data。
        
        子类可重写此方法以实现完全自定义的批量逻辑。
        """
        try:
            task_manager = get_task_manager() if task_id else None
            
            # 过滤掉前端特有的参数，这些参数不应该传递给 provider
            frontend_only_params = {
                'update_type', 'update_mode', 'batch_update', 'batch_size', 
                'page', 'limit', 'skip', 'filters', 'sort', 'order',
                'task_id', 'callback', 'async', 'timeout', '_t', '_timestamp',
                'force', 'clear_first', 'overwrite', 'mode'
            }
            
            # 移除前端特有参数
            filtered_kwargs = {k: v for k, v in kwargs.items() if k not in frontend_only_params}
            
            concurrency_value = filtered_kwargs.pop("concurrency", None)
            concurrency = int(concurrency_value) if concurrency_value is not None else self.batch_concurrency
            
            # 如果没有配置批量源，简单调用单条更新
            if not self.batch_source_collection:
                return await self._simple_batch_update(task_id, task_manager, **filtered_kwargs)
            
            # 有批量源配置，执行完整的批量更新
            return await self._full_batch_update(task_id, task_manager, concurrency, **filtered_kwargs)
            
        except Exception as e:
            self.logger.error(f"[{self.collection_name}] 批量更新失败: {e}", exc_info=True)
            if task_manager and task_id:
                task_manager.fail_task(task_id, str(e))
            return {
                "success": False,
                "message": str(e),
                "inserted": 0,
            }
    
    async def _simple_batch_update(
        self, 
        task_id: str, 
        task_manager, 
        **kwargs
    ) -> Dict[str, Any]:
        """简单批量更新：直接调用provider获取全部数据"""
        # 适用于“单接口即可拿到全量数据”的场景（例如名单类集合）。
        # 整体流程：汇报任务->线程池调用 provider -> ControlMongodb upsert -> 更新任务结果。
        if task_manager and task_id:
            task_manager.update_progress(task_id, 5, 100, f"正在获取 {self.collection_name} 数据...")
        
        # 过滤掉前端特有参数和值为None的参数
        frontend_only_params = {
            'update_type', 'update_mode', 'batch_update', 'batch_size', 
            'page', 'limit', 'skip', 'filters', 'sort', 'order',
            'task_id', 'callback', 'async', 'timeout', '_t', '_timestamp',
            'force', 'clear_first', 'overwrite', 'mode', 'concurrency',
            # 可选业务参数（值为None时应过滤）
            'fund_code', 'symbol', 'year', 'date', 'period', 'adjust',
            'start_year', 'end_year', 'delay', 'code'
        }
        # 只保留非前端特有参数且值不为None的参数
        provider_kwargs = {k: v for k, v in kwargs.items() if k not in frontend_only_params and v is not None}
        
        # 在线程池中调用同步的 provider
        df = await asyncio.get_event_loop().run_in_executor(
            None, 
            lambda: self.provider.fetch_data(**provider_kwargs)
        )
        
        if df is None or df.empty:
            if task_manager and task_id:
                task_manager.fail_task(task_id, "未获取到数据")
            return {"success": False, "message": "未获取到数据", "inserted": 0}
        
        total_records = len(df)
        if task_manager and task_id:
            task_manager.update_progress(task_id, 10, 100, f"获取到 {total_records} 条数据，正在保存...")
        
        # 创建进度回调函数，用于在保存数据时更新进度
        def save_progress_callback(current: int, total: int, message: str):
            """ControlMongodb 保存进度回调"""
            if task_manager and task_id:
                # 保存阶段占进度的 10%-95%
                progress = 10 + int((current / total) * 85) if total > 0 else 10
                task_manager.update_progress(
                    task_id, progress, 100, 
                    f"正在保存数据: {current}/{total} 条 ({int(current/total*100)}%)"
                )
        
        # 保存数据
        unique_keys = self._get_unique_keys()
        extra_fields = self._get_extra_fields()
        
        control_db = ControlMongodb(self.collection, unique_keys, self.current_user)
        result = await control_db.save_dataframe_to_collection(
            df, 
            extra_fields=extra_fields,
            progress_callback=save_progress_callback
        )
        
        total_inserted = result.get("inserted", 0) + result.get("updated", 0)
        message = f"批量更新完成，保存 {total_inserted} 条数据"
        
        if task_manager and task_id:
            task_manager.update_progress(task_id, 100, 100, message)
            task_manager.complete_task(task_id, result={"inserted": total_inserted}, message=message)
        
        return {"success": True, "message": message, "inserted": total_inserted}
    
    async def _full_batch_update(
        self,
        task_id: str,
        task_manager,
        concurrency: int,
        **kwargs
    ) -> Dict[str, Any]:
        """完整批量更新：从源集合获取代码列表，并发获取数据"""
        # 这是“代码驱动”的刷新路径：通常 provider 需要基金代码/年份等参数才能返回数据。
        # - 先从 batch_source_collection 中抽取代码；
        # - 根据 incremental_check_fields 判断哪些组合尚未存在；
        # - 调用 _execute_batch_tasks 执行真正的并发抓取和缓冲写库。
        
        # 1. 获取代码列表
        if task_manager and task_id:
            task_manager.update_progress(
                task_id, 0, 100, 
                f"正在从 {self.batch_source_collection} 获取代码列表..."
            )
        
        codes = await self._get_source_codes()
        
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
        
        self.logger.info(f"[{self.collection_name}] 从 {self.batch_source_collection} 获取到 {len(codes)} 个代码")
        
        # 2. 确定年份范围（如果需要）
        years = self._get_years_range(kwargs.get("year"))
        
        # 3. 生成待处理的任务列表
        if task_manager and task_id:
            task_manager.update_progress(task_id, 5, 100, "正在检查已有数据...")
        
        tasks_to_process = await self._get_tasks_to_process(codes, years)
        
        if not tasks_to_process:
            if task_manager and task_id:
                task_manager.update_progress(task_id, 100, 100, "所有数据已存在，无需更新")
                task_manager.complete_task(task_id)
            return {
                "success": True,
                "message": "所有数据已存在，无需更新",
                "inserted": 0,
            }
        
        total_tasks = len(tasks_to_process)
        self.logger.info(f"[{self.collection_name}] 需要处理 {total_tasks} 个任务")
        
        if task_manager and task_id:
            task_manager.update_progress(task_id, 10, 100, f"需要处理 {total_tasks} 个任务...")
        
        # 4. 并发执行
        return await self._execute_batch_tasks(
            tasks_to_process, 
            task_id, 
            task_manager, 
            concurrency
        )
    
    async def _get_source_codes(self) -> List[str]:
        """从源集合获取代码列表"""
        codes: List[str] = []
        cursor = self.db[self.batch_source_collection].find({}, {self.batch_source_field: 1})
        async for doc in cursor:
            code = doc.get(self.batch_source_field)
            if code:
                codes.append(code)
        return list(set(codes))  # 去重
    
    def _get_years_range(self, year_param: Any) -> List[str]:
        """获取年份范围"""
        if not self.batch_use_year:
            return []
        
        current_year = datetime.now().year
        
        if year_param:
            try:
                return [str(int(year_param))]
            except ValueError:
                raise ValueError(f"年份参数无效: {year_param}")
        
        if self.batch_years_range:
            start_year, end_year = self.batch_years_range
            end_year = end_year or current_year
            return [str(y) for y in range(start_year, end_year + 1)]
        
        return [str(current_year)]
    
    async def _get_tasks_to_process(
        self, 
        codes: List[str], 
        years: List[str]
    ) -> List[Tuple]:
        """
        获取待处理的任务列表（增量更新）
        
        返回待处理的 (code,) 或 (code, year) 元组列表
        """
        if not self.incremental_check_fields:
            # 没有配置增量检查，返回所有组合
            if years:
                return [(code, year) for code in codes for year in years]
            else:
                return [(code,) for code in codes]
        
        # 获取已存在的组合
        existing = await self._get_existing_combinations()
        
        # 过滤出需要处理的任务
        if years:
            return [
                (code, year) 
                for code in codes 
                for year in years 
                if (code, year) not in existing
            ]
        else:
            return [
                (code,) 
                for code in codes 
                if (code,) not in existing
            ]
    
    async def _get_existing_combinations(self) -> Set[Tuple]:
        """
        获取已存在的数据组合（支持字段值提取器）
        
        支持从字段值中提取关键信息，例如：
        - 从"季度"字段（"2024年1季度"）中提取年份（"2024"）
        """
        existing: Set[Tuple] = set()
        
        if not self.incremental_check_fields:
            return existing
        
        projection = {field: 1 for field in self.incremental_check_fields}
        cursor = self.collection.find({}, projection)
        
        async for doc in cursor:
            values = []
            for field in self.incremental_check_fields:
                value = doc.get(field, "")
                
                # 如果配置了字段值提取器，使用提取器处理
                if self.incremental_field_extractor and field in self.incremental_field_extractor:
                    extractor = self.incremental_field_extractor[field]
                    try:
                        value = extractor(str(value)) if value else ""
                    except Exception as e:
                        self.logger.debug(f"字段值提取失败 {field}={value}: {e}")
                        value = str(value)
                else:
                    value = str(value)
                
                values.append(value)
            
            # 只有当所有值都存在时才添加到集合
            if all(values):
                existing.add(tuple(values))
        
        return existing
    
    async def _execute_batch_tasks(
        self,
        tasks: List[Tuple],
        task_id: str,
        task_manager,
        concurrency: int,
        should_complete_task: bool = True
    ) -> Dict[str, Any]:
        """
        并发执行批量任务（优化版：数据聚合批量保存）
        
        优化点：
        1. 数据聚合批量保存：多个任务获取的数据先聚合，然后批量保存
        2. 复用ControlMongodb实例：避免重复创建
        3. 优化进度更新：减少锁竞争
        4. 使用异步队列 + 独立协程进行写库，避免在采集协程里阻塞 I/O
        
        Args:
            tasks: 待处理的任务列表
            task_id: 任务ID
            task_manager: 任务管理器
            concurrency: 并发数
            should_complete_task: 是否完成任务（默认True，如果是在分批处理中调用，应设置为False）
        """
        semaphore = asyncio.Semaphore(concurrency)
        total_inserted = 0
        processed = 0
        success_count = 0  # 成功获取并保存数据的任务数
        failed = 0
        saved_fund_count = 0  # 已保存的基金数量（不重复的基金代码数）
        total_fetched_rows = 0  # 获取的数据总行数
        total_saved_rows = 0  # 保存的数据总行数
        lock = asyncio.Lock()
        total_tasks = len(tasks)
        
        # 复用ControlMongodb实例
        unique_keys = self._get_unique_keys()
        extra_fields = self._get_extra_fields()
        control_db = ControlMongodb(self.collection, unique_keys, self.current_user)
        
        async def process_task(task_params: Tuple):
            """处理单个任务：获取数据后立即保存"""
            nonlocal processed, failed, success_count, total_inserted, total_fetched_rows, total_saved_rows, saved_fund_count
            async with semaphore:
                try:
                    # 构建参数
                    params = self.get_batch_params(*task_params)
                    
                    # 验证参数
                    if not params:
                        raise ValueError(f"get_batch_params 返回空参数，task_params={task_params}")
                    
                    self.logger.debug(f"[{self.collection_name}] 处理任务 {task_params}, 参数: {params}")
                    
                    # 在线程池中调用同步的 provider（带超时保护）
                    try:
                        df = await asyncio.wait_for(
                            asyncio.get_event_loop().run_in_executor(
                                None,
                                lambda p=params: self.provider.fetch_data(**p)
                            ),
                            timeout=self.batch_task_timeout
                        )
                    except asyncio.TimeoutError:
                        self.logger.warning(f"[{self.collection_name}] 任务 {task_params} 超时（{self.batch_task_timeout}秒）")
                        raise TimeoutError(f"任务超时: {task_params}")
                    
                    if df is not None and not df.empty:
                        # 统计获取的数据行数
                        rows_count = len(df)
                        async with lock:
                            total_fetched_rows += rows_count
                        
                        # 按 field_info 的顺序重新排列 DataFrame 列
                        df = self._reorder_dataframe_columns(df)
                        
                        # 立即保存数据到数据库（不进行聚合）
                        try:
                            result = await control_db.save_dataframe_to_collection(
                                df,
                                extra_fields=extra_fields
                            )
                            
                            # 统计保存结果
                            inserted_count = result.get("inserted", 0) + result.get("updated", 0)
                            saved_rows = len(df)  # 实际保存的行数
                            
                            async with lock:
                                total_inserted += inserted_count
                                total_saved_rows += saved_rows
                                success_count += 1  # 只有成功保存才算成功
                            
                            self.logger.debug(
                                f"[{self.collection_name}] 任务 {task_params} 保存完成: "
                                f"新增={result.get('inserted', 0)}, "
                                f"更新={result.get('updated', 0)}, "
                                f"总行数={saved_rows}"
                            )
                        except Exception as save_error:
                            # 保存失败，记录错误但不抛出异常（避免影响其他任务）
                            self.logger.error(
                                f"[{self.collection_name}] 任务 {task_params} 保存失败: {save_error}",
                                exc_info=True
                            )
                            async with lock:
                                failed += 1
                    else:
                        # 数据为空，不算失败也不算成功
                        self.logger.debug(f"[{self.collection_name}] 任务 {task_params} 返回空数据")
                    
                    async with lock:
                        processed += 1
                        
                except Exception as e:
                    self.logger.error(f"[{self.collection_name}] 处理任务 {task_params} 失败: {e}", exc_info=True)
                    async with lock:
                        failed += 1
                        processed += 1
                
                # 优化进度更新：减少锁竞争
                if task_manager and task_id:
                    async with lock:
                        current_processed = processed
                        current_success = success_count
                        current_failed = failed
                        current_fetched_rows = total_fetched_rows
                        current_saved_rows = total_saved_rows
                    
                    # 更频繁地更新进度：每10个任务或每5秒更新一次
                    should_update = (
                        current_processed % max(1, min(10, self.batch_progress_interval)) == 0 or
                        current_processed == 1  # 第一个任务完成时立即更新
                    )
                    
                    if should_update:
                        progress = 10 + int((current_processed / total_tasks) * 85) if total_tasks > 0 else 10
                        # 构建进度消息，包含已保存的基金数量和数据行数
                        progress_parts = [
                            f"已处理 {current_processed}/{total_tasks}",
                            f"成功 {current_success}",
                            f"失败 {current_failed}"
                        ]
                        if current_fetched_rows > 0:
                            progress_parts.append(f"获取 {current_fetched_rows} 行")
                        if current_saved_rows > 0:
                            progress_parts.append(f"保存 {current_saved_rows} 行")
                        progress_msg = "，".join(progress_parts)
                        # task_manager.update_progress 是同步方法，直接调用
                        task_manager.update_progress(
                            task_id, progress, 100,
                            progress_msg
                        )
        
        # 启动定期进度更新协程
        async def periodic_progress_update():
            """定期更新进度，即使任务还在执行中"""
            while True:
                await asyncio.sleep(2)  # 每2秒更新一次进度
                if task_manager and task_id:
                    async with lock:
                        current_processed = processed
                        current_success = success_count
                        current_failed = failed
                        current_fetched_rows = total_fetched_rows
                        current_saved_rows = total_saved_rows
                    
                    # 如果所有任务都完成了，退出
                    if current_processed >= total_tasks:
                        break
                    
                    # 更新进度
                    progress = 10 + int((current_processed / total_tasks) * 85) if total_tasks > 0 else 10
                    # 构建进度消息，包含已保存的基金数量和数据行数
                    progress_parts = [
                        f"已处理 {current_processed}/{total_tasks}",
                        f"成功 {current_success}",
                        f"失败 {current_failed}"
                    ]
                    if current_fetched_rows > 0:
                        progress_parts.append(f"获取 {current_fetched_rows} 行")
                    if current_saved_rows > 0:
                        progress_parts.append(f"保存 {current_saved_rows} 行")
                    progress_msg = "，".join(progress_parts)
                    task_manager.update_progress(
                        task_id, progress, 100,
                        progress_msg
                    )
        
        progress_task = asyncio.create_task(periodic_progress_update())
        
        try:
            # 并发执行所有任务
            await asyncio.gather(*[process_task(t) for t in tasks], return_exceptions=True)
            
            # 停止定期进度更新
            progress_task.cancel()
            try:
                await progress_task
            except asyncio.CancelledError:
                pass
            
        except Exception as e:
            self.logger.error(f"[{self.collection_name}] 批量更新执行失败: {e}", exc_info=True)
            # 停止定期进度更新
            progress_task.cancel()
            try:
                await progress_task
            except asyncio.CancelledError:
                pass
        
        # 最终统计已保存的基金数量
        if self.incremental_check_fields and len(self.incremental_check_fields) > 0:
            try:
                fund_code_field = self.incremental_check_fields[0]
                distinct_count = await self.collection.distinct(fund_code_field)
                saved_fund_count = len([c for c in distinct_count if c])  # 过滤空值
            except Exception as e:
                self.logger.debug(f"[{self.collection_name}] 最终统计基金数量失败: {e}")
                saved_fund_count = 0
        
        # 完成消息，包含获取和保存的行数
        message_parts = [
            f"批量更新完成",
            f"处理 {processed} 个任务",
            f"成功 {success_count} 个",
            f"失败 {failed} 个"
        ]
        if total_fetched_rows > 0:
            message_parts.append(f"获取 {total_fetched_rows} 行数据")
        if total_saved_rows > 0:
            message_parts.append(f"保存 {total_saved_rows} 行数据")
        message_parts.append(f"保存 {total_inserted} 条记录（新增+更新）")
        if saved_fund_count > 0:
            message_parts.append(f"已保存 {saved_fund_count} 个基金")
        
        message = "，".join(message_parts)
        self.logger.info(f"[{self.collection_name}] {message}")
        
        if task_manager and task_id:
            # 更新进度，但不一定完成任务（如果是在分批处理中调用，由外层完成）
            if should_complete_task:
                task_manager.update_progress(task_id, 100, 100, message)
                task_manager.complete_task(
                    task_id,
                    result={
                        "inserted": total_inserted, 
                        "processed": processed, 
                        "success": success_count, 
                        "failed": failed,
                        "saved_fund_count": saved_fund_count,
                        "fetched_rows": total_fetched_rows,
                        "saved_rows": total_saved_rows
                    },
                    message=message
                )
            else:
                # 只更新进度，不完成任务（由外层完成）
                # 计算当前进度（基于已处理的任务数）
                progress = min(95, int((processed / len(tasks)) * 95)) if tasks else 95
                task_manager.update_progress(task_id, progress, 100, message)
        
        return {
            "success": True,
            "message": message,
            "inserted": total_inserted,
            "processed": processed,
            "success_count": success_count,
            "failed": failed,
            "saved_fund_count": saved_fund_count,
            "fetched_rows": total_fetched_rows,
            "saved_rows": total_saved_rows,
        }
    
    def get_batch_params(self, *args) -> Dict[str, Any]:
        """
        根据任务参数构建 provider 调用参数
        
        子类可重写此方法以自定义参数构建逻辑
        
        默认实现：
        - 1个参数：{"code": args[0]}
        - 2个参数：{"code": args[0], "year": args[1]}
        """
        if len(args) == 1:
            return {self.batch_source_field: args[0]}
        elif len(args) == 2:
            return {self.batch_source_field: args[0], "year": args[1]}
        else:
            return {}
    
    def _reorder_dataframe_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        按 provider 的 field_info 顺序重新排列 DataFrame 列
        
        Args:
            df: 原始 DataFrame
            
        Returns:
            重新排列后的 DataFrame
        """
        if not self.provider:
            return df
        
        field_info = self.provider.get_field_info()
        if not field_info:
            return df
        
        # 获取 field_info 中定义的字段顺序
        ordered_fields = [field.get("name") for field in field_info if field.get("name")]
        
        if not ordered_fields:
            return df
        
        # 获取 DataFrame 中实际存在的列
        existing_columns = list(df.columns)
        
        # 按 field_info 顺序排列，未在 field_info 中的列放在最后
        ordered_columns = []
        for field_name in ordered_fields:
            if field_name in existing_columns:
                ordered_columns.append(field_name)
        
        # 添加未在 field_info 中定义的列（保持原有顺序）
        for col in existing_columns:
            if col not in ordered_columns:
                ordered_columns.append(col)
        
        # 重新排列 DataFrame
        if ordered_columns != existing_columns:
            df = df[ordered_columns]
            self.logger.debug(
                f"[{self.collection_name}] 已按 field_info 顺序重新排列列: {ordered_columns[:5]}..."
            )
        
        return df
    
    def _get_unique_keys(self) -> List[str]:
        """
        获取唯一键（自动检测provider或使用配置）
        
        优先级：
        1. provider.get_unique_keys() 方法
        2. provider.unique_keys 属性
        3. service.unique_keys 配置
        4. 空列表
        """
        # 优先使用provider的方法
        if self.provider and hasattr(self.provider, 'get_unique_keys'):
            try:
                keys = self.provider.get_unique_keys()
                if keys:
                    return keys
            except (AttributeError, TypeError):
                pass
        
        # 其次使用provider的属性
        if self.provider and hasattr(self.provider, 'unique_keys'):
            keys = getattr(self.provider, 'unique_keys', [])
            if keys:
                return keys
        
        # 最后使用service配置
        if hasattr(self, 'unique_keys') and self.unique_keys:
            return self.unique_keys
        
        # 默认值
        return []
    
    def _get_extra_fields(self) -> Dict[str, str]:
        """
        获取额外的元数据字段（自动检测provider）
        
        自动检测provider的接口名称：
        1. provider.akshare_func 属性
        2. provider.collection_name 属性
        3. service.collection_name
        """
        fields = dict(self.extra_metadata)
        
        # 自动检测provider的接口名称
        if self.provider:
            # 优先使用akshare_func属性
            if hasattr(self.provider, 'akshare_func'):
                func_name = getattr(self.provider, 'akshare_func', None)
                if func_name:
                    fields["接口名称"] = func_name
            # 其次使用collection_name
            elif hasattr(self.provider, 'collection_name'):
                coll_name = getattr(self.provider, 'collection_name', None)
                if coll_name and not fields.get("接口名称"):
                    fields["接口名称"] = coll_name
        
        # 如果还没有接口名称，使用service的collection_name
        if not fields.get("接口名称") and hasattr(self, 'collection_name'):
            fields["接口名称"] = self.collection_name
        
        return fields


class SimpleService(BaseService):
    """
    简单服务类
    
    用于无参数或简单参数的接口，不需要复杂的批量更新逻辑。
    批量更新就是直接调用 provider 获取全部数据。
    """
    pass
