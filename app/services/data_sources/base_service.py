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
    
    # ===== 子类必须定义的属性 =====
    collection_name: str = ""               # 集合名称
    provider_class: Type[BaseProvider] = None  # Provider类
    
    # ===== 子类可选定义的属性 =====
    
    # 时间字段名（用于排序和概览）
    time_field: str = "scraped_at"
    
    # 批量更新相关配置
    batch_source_collection: str = ""       # 批量更新时从哪个集合获取代码列表
    batch_source_field: str = ""            # 从源集合获取的字段名
    batch_years_range: Tuple[int, int] = None  # 年份范围，如 (2010, None) 表示2010到今年
    batch_use_year: bool = False            # 批量更新是否需要年份参数
    batch_concurrency: int = 3              # 默认并发数
    batch_progress_interval: int = 50       # 进度更新间隔
    
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
    
    def __init__(self, db: AsyncIOMotorClient):
        self.db = db
        self.collection = db[self.collection_name]
        self.provider = self.provider_class() if self.provider_class else None
        self.logger = logging.getLogger(self.__class__.__name__)
    
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
            
            # 调用 provider 获取数据
            df = self.provider.fetch_data(**kwargs)
            
            if df is None or df.empty:
                self.logger.warning(f"[{self.collection_name}] provider 返回空数据")
                return {
                    "success": True,
                    "message": "No data available",
                    "inserted": 0,
                }
            
            # 使用 ControlMongodb 保存数据
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
            concurrency = int(kwargs.pop("concurrency", self.batch_concurrency))
            
            # 如果没有配置批量源，简单调用单条更新
            if not self.batch_source_collection:
                return await self._simple_batch_update(task_id, task_manager, **kwargs)
            
            # 有批量源配置，执行完整的批量更新
            return await self._full_batch_update(task_id, task_manager, concurrency, **kwargs)
            
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
        if task_manager and task_id:
            task_manager.update_progress(task_id, 10, 100, f"正在获取 {self.collection_name} 数据...")
        
        # 在线程池中调用同步的 provider
        df = await asyncio.get_event_loop().run_in_executor(
            None, 
            lambda: self.provider.fetch_data(**kwargs)
        )
        
        if df is None or df.empty:
            if task_manager and task_id:
                task_manager.fail_task(task_id, "未获取到数据")
            return {"success": False, "message": "未获取到数据", "inserted": 0}
        
        if task_manager and task_id:
            task_manager.update_progress(task_id, 60, 100, f"正在保存 {len(df)} 条数据...")
        
        # 保存数据
        unique_keys = self._get_unique_keys()
        extra_fields = self._get_extra_fields()
        
        control_db = ControlMongodb(self.collection, unique_keys)
        result = await control_db.save_dataframe_to_collection(df, extra_fields=extra_fields)
        
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
        concurrency: int
    ) -> Dict[str, Any]:
        """
        并发执行批量任务（优化版：数据聚合批量保存）
        
        优化点：
        1. 数据聚合批量保存：多个任务获取的数据先聚合，然后批量保存
        2. 复用ControlMongodb实例：避免重复创建
        3. 优化进度更新：减少锁竞争
        4. 动态调整并发数：根据连接池大小限制
        """
        # 根据连接池大小动态调整并发数
        from app.core.config import settings
        max_allowed_concurrency = max(1, settings.MONGO_MAX_CONNECTIONS // 2)
        concurrency = min(concurrency, max_allowed_concurrency)
        
        semaphore = asyncio.Semaphore(concurrency)
        total_inserted = 0
        processed = 0
        failed = 0
        lock = asyncio.Lock()
        total_tasks = len(tasks)
        
        # 数据聚合队列：用于批量保存
        data_queue = asyncio.Queue()
        batch_size_threshold = 5000  # 达到5000条数据时批量保存
        save_interval = 5.0  # 5秒间隔批量保存
        
        # 复用ControlMongodb实例
        unique_keys = self._get_unique_keys()
        extra_fields = self._get_extra_fields()
        control_db = ControlMongodb(self.collection, unique_keys)
        
        # 批量保存协程
        save_task = None
        save_completed = asyncio.Event()
        
        async def batch_saver():
            """批量保存协程：定期从队列中取出数据并批量保存"""
            nonlocal total_inserted
            accumulated_dfs = []
            last_save_time = asyncio.get_event_loop().time()
            
            async def save_accumulated():
                """保存累积的数据"""
                if accumulated_dfs:
                    try:
                        combined_df = pd.concat(accumulated_dfs, ignore_index=True)
                        result = await control_db.save_dataframe_to_collection(
                            combined_df,
                            extra_fields=extra_fields
                        )
                        async with lock:
                            total_inserted += result.get("inserted", 0) + result.get("updated", 0)
                        
                        self.logger.debug(
                            f"[{self.collection_name}] 批量保存完成: "
                            f"新增={result.get('inserted', 0)}, "
                            f"更新={result.get('updated', 0)}, "
                            f"总行数={len(combined_df)}"
                        )
                        accumulated_dfs.clear()
                        return True
                    except Exception as e:
                        self.logger.error(f"[{self.collection_name}] 批量保存失败: {e}", exc_info=True)
                        return False
                return False
            
            while True:
                try:
                    # 检查是否需要退出
                    if save_completed.is_set() and data_queue.empty():
                        # 保存最后一批数据
                        await save_accumulated()
                        break
                    
                    # 等待数据或超时
                    current_time = asyncio.get_event_loop().time()
                    elapsed = current_time - last_save_time
                    timeout = max(0.1, save_interval - elapsed)
                    
                    try:
                        df = await asyncio.wait_for(data_queue.get(), timeout=timeout)
                        if df is not None and not df.empty:
                            accumulated_dfs.append(df)
                    except asyncio.TimeoutError:
                        # 超时，检查是否需要保存
                        pass
                    
                    # 检查是否需要保存：达到阈值或超时
                    total_rows = sum(len(df) for df in accumulated_dfs)
                    should_save = (
                        total_rows >= batch_size_threshold or  # 达到阈值
                        (save_completed.is_set() and data_queue.empty() and accumulated_dfs)  # 完成且有数据
                    )
                    
                    if should_save:
                        await save_accumulated()
                        last_save_time = asyncio.get_event_loop().time()
                            
                except Exception as e:
                    self.logger.error(f"[{self.collection_name}] 批量保存协程错误: {e}", exc_info=True)
                    # 发生错误时也尝试保存已累积的数据
                    await save_accumulated()
        
        async def process_task(task_params: Tuple):
            nonlocal processed, failed
            async with semaphore:
                try:
                    # 构建参数
                    params = self.get_batch_params(*task_params)
                    
                    # 在线程池中调用同步的 provider
                    df = await asyncio.get_event_loop().run_in_executor(
                        None,
                        lambda: self.provider.fetch_data(**params)
                    )
                    
                    if df is not None and not df.empty:
                        # 将数据放入队列，由批量保存协程处理
                        await data_queue.put(df)
                    
                    async with lock:
                        processed += 1
                        
                except Exception as e:
                    self.logger.debug(f"处理任务 {task_params} 失败: {e}")
                    async with lock:
                        failed += 1
                        processed += 1
                
                # 优化进度更新：减少锁竞争，使用原子操作
                if task_manager and task_id:
                    # 只在特定间隔更新进度，减少锁竞争
                    if processed % max(1, self.batch_progress_interval) == 0:
                        async with lock:
                            progress = 10 + int((processed / total_tasks) * 85)
                            # 使用异步更新，不阻塞
                            asyncio.create_task(
                                task_manager.update_progress(
                                    task_id, progress, 100,
                                    f"已处理 {processed}/{total_tasks}，成功 {total_inserted} 条"
                                )
                            )
        
        # 启动批量保存协程
        save_task = asyncio.create_task(batch_saver())
        
        try:
            # 并发执行所有任务
            await asyncio.gather(*[process_task(t) for t in tasks], return_exceptions=True)
            
            # 等待所有数据被处理
            while not data_queue.empty():
                await asyncio.sleep(0.1)
            
            # 通知批量保存协程可以退出
            save_completed.set()
            
            # 等待批量保存协程完成
            await save_task
            
        except Exception as e:
            self.logger.error(f"[{self.collection_name}] 批量更新执行失败: {e}", exc_info=True)
            if save_task:
                save_completed.set()
                await save_task
        
        # 完成
        message = f"批量更新完成，处理 {processed} 个任务，成功 {total_inserted} 条，失败 {failed} 个"
        self.logger.info(f"[{self.collection_name}] {message}")
        
        if task_manager and task_id:
            task_manager.update_progress(task_id, 100, 100, message)
            task_manager.complete_task(
                task_id,
                result={"inserted": total_inserted, "processed": processed, "failed": failed},
                message=message
            )
        
        return {
            "success": True,
            "message": message,
            "inserted": total_inserted,
            "processed": processed,
            "failed": failed,
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
