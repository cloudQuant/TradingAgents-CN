"""
债券基础信息批量更新服务

根据需求文档要求，实现：
1. 批量更新：从bond_info_cm表查询债券简称，从bond_info_detail_cm获取详细信息，多线程批量更新
2. 增量更新：查找缺失的债券基础信息并更新
3. 统计信息查询
"""

import asyncio
import signal
from typing import Dict, List, Any, Optional, Set
from datetime import datetime
import pandas as pd
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import UpdateOne
from loguru import logger
from concurrent.futures import ThreadPoolExecutor
import threading

from app.services.bond_data_service import BondDataService
from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider
from tradingagents.utils.instrument_validator import normalize_bond_code

# 全局停止事件，确保所有实例都能接收到停止信号
_global_shutdown_event = asyncio.Event()
_signal_handlers_setup = False
_signal_received_count = 0  # 记录收到信号的次数
_graceful_shutdown_timeout = 5  # 优雅停止超时时间（秒）

def setup_global_signal_handlers():
    """设置全局信号处理器（只设置一次）"""
    global _signal_handlers_setup
    
    if _signal_handlers_setup:
        logger.debug("⚠️ [信号处理] 信号处理器已经设置，跳过重复设置")
        return
    
    def signal_handler(signum, frame):
        global _signal_received_count
        _signal_received_count += 1
        
        if _signal_received_count == 1:
            logger.info(f"📶 [信号处理] 接收到信号 {signum}，开始优雅停止...")
            logger.info(f"💡 [提示] 再次按 Ctrl+C 将立即退出，或等待 {_graceful_shutdown_timeout} 秒自动强制退出")
            _global_shutdown_event.set()
            
            # 启动超时强制退出机制
            def force_exit_after_timeout():
                import time
                import os
                time.sleep(_graceful_shutdown_timeout)
                logger.warning(f"⏰ [超时退出] 优雅停止超过 {_graceful_shutdown_timeout} 秒，强制退出程序")
                os._exit(1)
            
            # 在后台线程中启动超时机制
            import threading
            timeout_thread = threading.Thread(target=force_exit_after_timeout, daemon=True)
            timeout_thread.start()
            
            # 关键修复：恢复默认信号处理器，让后续的Ctrl+C能正常工作
            signal.signal(signal.SIGINT, signal.SIG_DFL)
            signal.signal(signal.SIGTERM, signal.SIG_DFL)
            logger.debug("🔄 [信号处理] 已恢复默认信号处理器")
        else:
            # 这个分支理论上不会执行，因为已经恢复了默认处理器
            logger.warning(f"⚠️ [信号处理] 意外的信号重复，强制退出...")
            import os
            os._exit(1)
    
    try:
        # 恢复默认信号处理器，避免冲突
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        signal.signal(signal.SIGTERM, signal.SIG_DFL)
        
        # 设置新的信号处理器
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        _signal_handlers_setup = True
        logger.info("✅ [信号处理] 全局信号处理器设置完成")
    except ValueError as e:
        logger.warning(f"⚠️ [信号处理] 无法设置全局信号处理器: {e}")

# 初始化全局信号处理（只在模块加载时执行一次）
setup_global_signal_handlers()


class BondBasicInfoService:
    """债券基础信息批量更新服务"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.bond_data_service = BondDataService(db)
        self.provider = AKShareBondProvider()
        self._lock = threading.Lock()
        
        # 集合引用
        self.col_info_cm = db.get_collection("bond_info_cm")
        self.col_basic = db.get_collection("bond_basic_info")
    
    def should_shutdown(self) -> bool:
        """检查是否应该停止处理"""
        return _global_shutdown_event.is_set()
    
    def _extract_bond_name(self, raw_name: str) -> str:
        """
        从原始债券名称中提取纯净的债券简称
        
        处理各种格式：
        - "111887384(18稠州商行CD016)" -> "18稠州商行CD016"
        - "18稠州商行CD016" -> "18稠州商行CD016"
        - "123456 19万林投资CP001" -> "19万林投资CP001"
        
        Args:
            raw_name: 原始债券名称
            
        Returns:
            清理后的债券简称
        """
        if not raw_name:
            return ""
        
        name = str(raw_name).strip()
        
        # 方法1: 处理括号格式 "代码(简称)"
        if '(' in name and ')' in name:
            start = name.find('(')
            end = name.find(')')
            if start != -1 and end != -1 and end > start:
                extracted = name[start + 1:end].strip()
                if extracted:
                    logger.debug(f"🔄 [名称提取] 从括号格式提取: '{name}' -> '{extracted}'")
                    return extracted
        
        # 方法2: 处理空格分隔格式 "代码 简称"
        parts = name.split()
        if len(parts) >= 2:
            # 如果第一部分是纯数字（可能是债券代码），取后面的部分
            if parts[0].isdigit():
                extracted = ' '.join(parts[1:]).strip()
                if extracted:
                    logger.debug(f"🔄 [名称提取] 从空格格式提取: '{name}' -> '{extracted}'")
                    return extracted
        
        # 方法3: 如果没有特殊格式，直接返回原始名称
        logger.debug(f"🔄 [名称提取] 保持原格式: '{name}'")
        return name
    
    def _convert_detail_dataframe_to_dict(self, df: pd.DataFrame, code: str, name: str) -> Dict[str, Any]:
        """
        将 akshare.bond_info_detail_cm 返回的 DataFrame 转换为字典格式
        
        DataFrame 格式：
        name                       value
        bondFullName              xxx
        bondDefinedCode           xxx
        ...
        
        转换为：
        {
            "bondFullName": "xxx",
            "bondDefinedCode": "xxx",
            ...
            "code": code,
            "endpoint": "bond_info_detail_cm",
            "债券简称": name
        }
        """
        try:
            # 将DataFrame转换为字典
            data_dict = {}
            
            if isinstance(df, pd.DataFrame) and not df.empty:
                # 使用 name 列作为键，value 列作为值
                logger.debug(f"🔄 [数据转换] 开始转换DataFrame，共 {len(df)} 行数据")
                for idx, row in df.iterrows():
                    key = row.get('name', '').strip() if pd.notna(row.get('name')) else ''
                    value = row.get('value', '').strip() if pd.notna(row.get('value')) else ''
                    
                    if key:
                        # 处理特殊的空值情况
                        if value in ['---', 'None', 'null', 'NaN', '']:
                            data_dict[str(key)] = None
                        else:
                            data_dict[str(key)] = str(value)
                        
                        # 调试日志，显示转换的键值对
                        if idx < 5:  # 只显示前5条，避免日志过多
                            logger.debug(f"  - {key}: {value}")
                
                logger.debug(f"✅ [数据转换] 成功转换 {len(data_dict)} 个字段")
            else:
                logger.warning("⚠️ [数据转换] DataFrame 为空或格式不正确")
            
            # 添加必要的元数据
            data_dict.update({
                "code": code,
                "endpoint": "bond_info_detail_cm",
                "债券简称": name,
                "数据来源": "akshare.bond_info_detail_cm",
                "更新时间": datetime.now().isoformat()
            })
            
            return data_dict
            
        except Exception as e:
            logger.error(f"❌ [数据转换] DataFrame 转换失败: {e}")
            return {
                "code": code,
                "endpoint": "bond_info_detail_cm",
                "债券简称": name,
                "error": str(e),
                "更新时间": datetime.now().isoformat()
            }
    
    async def _save_bond_detail_dict(self, data_dict: Dict[str, Any]) -> int:
        """保存债券详细信息字典到 bond_info_cm 集合"""
        try:
            # 使用 upsert 操作，避免重复数据
            filter_query = {
                "code": data_dict["code"],
                "endpoint": "bond_info_detail_cm"
            }
            
            result = await self.col_info_cm.update_one(
                filter_query,
                {"$set": data_dict},
                upsert=True
            )
            
            return 1 if result.upserted_id or result.modified_count > 0 else 0
            
        except Exception as e:
            logger.error(f"❌ [数据保存] 保存失败: {e}")
            return 0
    
    async def batch_update_from_bond_info_cm(
        self,
        batch_size: int = 1000,
        concurrent_threads: int = 3,
        save_interval: int = 1000
    ) -> Dict[str, Any]:
        """
        批量更新功能：从bond_info_cm表查询债券简称，然后从bond_info_detail_cm中获取债券的详细信息，
        更新bond_info_detail_cm到这个集合中
        
        Args:
            batch_size: 每批处理的数量
            concurrent_threads: 并发线程数，默认3个
            save_interval: 每获取多少条数据保存到集合一次，默认1000条
            
        Returns:
            Dict包含处理结果统计
        """
        logger.info(f"🚀 [批量更新] 开始批量更新，线程数={concurrent_threads}，批次大小={batch_size}")
        
        # 在方法开始就检查停止信号
        if self.should_shutdown():
            logger.info("🛑 [批量更新] 开始时检测到停止信号，立即退出")
            return {
                "success": True,
                "message": "接收到停止信号，批量更新已停止",
                "stopped": True
            }
        
        start_time = datetime.now()
        total_processed = 0
        total_updated = 0
        total_errors = 0
        
        try:
            # 1. 从bond_info_cm表查询所有债券简称
            logger.info("📊 [批量更新] 正在查询bond_info_cm表中的债券简称...")
            
            # 查询bond_info_cm集合中的债券代码，过滤掉详细信息记录
            cursor = self.col_info_cm.find(
                {"endpoint": "bond_info_cm"},  # 只查询标准数据记录
                {"code": 1, "债券简称": 1, "债券代码": 1}
            )
            
            bond_codes = []
            async for doc in cursor:
                code = doc.get("code") or doc.get("债券代码")
                bond_name = doc.get("债券简称", "")
                if code:
                    bond_codes.append({
                        "code": str(code).strip(),
                        "name": str(bond_name).strip()
                    })
            
            total_bonds = len(bond_codes)
            logger.info(f"📈 [批量更新] 找到 {total_bonds} 个债券代码需要处理")
            
            if total_bonds == 0:
                return {
                    "success": True,
                    "total_bonds": 0,
                    "total_processed": 0,
                    "total_updated": 0,
                    "total_errors": 0,
                    "message": "未找到需要处理的债券代码"
                }
            
            # 2. 批量处理
            semaphore = asyncio.Semaphore(concurrent_threads)
            
            async def process_bond_batch(codes_batch: List[Dict[str, str]]) -> Dict[str, Any]:
                """处理单批债券"""
                async with semaphore:
                    batch_updated = 0
                    batch_errors = 0
                    batch_details = []
                    
                    for bond_info in codes_batch:
                        # 检查是否需要停止
                        if self.should_shutdown():
                            logger.info("🛑 [批量更新] 接收到停止信号，提前退出批次处理")
                            break
                            
                        code = bond_info["code"]
                        name = bond_info["name"]
                        
                        try:
                            # 检查是否已有详细信息
                            existing_detail = await self.col_info_cm.find_one({
                                "code": code,
                                "endpoint": "bond_info_detail_cm"
                            })
                            
                            if existing_detail:
                                logger.debug(f"⏭️ [批量更新] {code} 已有详细信息，跳过")
                                continue
                            
                            # 使用债券简称获取详细信息（按需求文档使用bond_info_detail_cm接口）
                            try:
                                # 提取纯净的债券简称
                                clean_name = self._extract_bond_name(name)
                                logger.debug(f"🔄 [批量更新] 原始名称: '{name}' -> 清理后: '{clean_name}'")
                                
                                if not clean_name:
                                    logger.warning(f"⚠️ [批量更新] 无法提取有效的债券简称: '{name}'")
                                    batch_errors += 1
                                    batch_details.append({
                                        "code": code,
                                        "name": name,
                                        "status": "error",
                                        "error": "invalid_bond_name_format"
                                    })
                                    continue
                                
                                import akshare as ak
                                # 根据需求文档，使用债券简称查询详细信息
                                detail_df = await asyncio.to_thread(ak.bond_info_detail_cm, symbol=clean_name)
                                
                                if isinstance(detail_df, pd.DataFrame) and not detail_df.empty:
                                    # 转换DataFrame为字典格式
                                    data_dict = self._convert_detail_dataframe_to_dict(detail_df, code, name)
                                    
                                    # 保存详细信息
                                    saved = await self._save_bond_detail_dict(data_dict)
                                    if saved > 0:
                                        batch_updated += 1
                                        batch_details.append({
                                            "code": code,
                                            "name": name,
                                            "status": "updated",
                                            "saved_count": saved,
                                            "fields_count": len([k for k in data_dict.keys() if not k.startswith('_')])
                                        })
                                    else:
                                        batch_details.append({
                                            "code": code,
                                            "name": name,
                                            "status": "no_update",
                                            "reason": "save_returned_zero"
                                        })
                                else:
                                    batch_errors += 1
                                    batch_details.append({
                                        "code": code,
                                        "name": name,
                                        "status": "error",
                                        "error": "no_detail_data_returned"
                                    })
                                    
                            except Exception as detail_error:
                                # 如果获取详细信息失败，尝试用基础信息接口
                                basic_info = await self.provider.get_basic_info(code)
                                
                                if basic_info and "error" not in basic_info:
                                    # 保存基础信息
                                    saved = await self.bond_data_service.save_bond_info_from_api(code, basic_info)
                                    if saved > 0:
                                        batch_updated += 1
                                        batch_details.append({
                                            "code": code,
                                            "name": name,
                                            "status": "updated_basic",
                                            "saved_count": saved
                                        })
                                    else:
                                        batch_details.append({
                                            "code": code,
                                            "name": name,
                                            "status": "no_update",
                                            "reason": "basic_save_returned_zero"
                                        })
                                else:
                                    batch_errors += 1
                                    error_msg = basic_info.get("error", "unknown_error") if basic_info else str(detail_error)
                                    batch_details.append({
                                        "code": code,
                                        "name": name,
                                        "status": "error",
                                        "error": error_msg
                                    })
                                    logger.debug(f"❌ [批量更新] {code}({name}) 获取失败: {error_msg}")
                            
                            # 添加延迟避免API限流
                            await asyncio.sleep(0.1)
                            
                        except Exception as e:
                            batch_errors += 1
                            batch_details.append({
                                "code": code,
                                "name": name,
                                "status": "exception",
                                "error": str(e)
                            })
                            logger.error(f"❌ [批量更新] {code}({name}) 处理异常: {e}")
                    
                    return {
                        "updated": batch_updated,
                        "errors": batch_errors,
                        "details": batch_details
                    }
            
            # 3. 分批处理
            tasks = []
            for i in range(0, total_bonds, batch_size):
                batch_codes = bond_codes[i:i + batch_size]
                task = asyncio.create_task(process_bond_batch(batch_codes))
                tasks.append(task)
            
            # 等待所有任务完成
            logger.info(f"🔄 [批量更新] 启动 {len(tasks)} 个批次任务...")
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # 4. 统计结果
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    logger.error(f"❌ [批量更新] 批次 {i} 执行异常: {result}")
                    total_errors += batch_size  # 假设整批都失败
                else:
                    total_updated += result["updated"]
                    total_errors += result["errors"]
                    total_processed += len(result["details"])
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            logger.info(f"✅ [批量更新] 完成！处理 {total_processed}/{total_bonds} 个债券，"
                       f"更新 {total_updated} 个，错误 {total_errors} 个，耗时 {duration:.2f}s")
            
            return {
                "success": True,
                "total_bonds": total_bonds,
                "total_processed": total_processed,
                "total_updated": total_updated,
                "total_errors": total_errors,
                "duration_seconds": duration,
                "concurrent_threads": concurrent_threads,
                "batch_size": batch_size,
                "message": f"批量更新完成，更新了 {total_updated} 个债券基础信息"
            }
            
        except Exception as e:
            logger.error(f"❌ [批量更新] 执行失败: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "total_processed": total_processed,
                "total_updated": total_updated,
                "total_errors": total_errors
            }
    
    async def incremental_update_missing_info(self) -> Dict[str, Any]:
        """
        增量更新功能：从bond_info_cm集合中查询债券简称，然后从bond_info_detail_cm集合中获取债券的简称，
        获取债券基础信息这个里面没有的债券简称，然后更新这些债券的基础信息到集合中
        
        Returns:
            Dict包含处理结果统计
        """
        logger.info("🔍 [增量更新] 开始增量更新缺失的债券基础信息...")
        
        # 在方法开始就检查停止信号
        if self.should_shutdown():
            logger.info("🛑 [增量更新] 开始时检测到停止信号，立即退出")
            return {
                "success": True,
                "message": "接收到停止信号，增量更新已停止",
                "stopped": True
            }
        
        start_time = datetime.now()
        
        try:
            # 1. 获取bond_info_cm中的所有债券代码和简称
            logger.info("📊 [增量更新] 正在查询bond_info_cm中的债券代码...")
            cursor_basic = self.col_info_cm.find(
                {"endpoint": "bond_info_cm"},
                {"code": 1, "债券代码": 1, "债券简称": 1}
            )
            
            basic_bonds = {}
            async for doc in cursor_basic:
                # 在查询循环中检查停止信号
                if self.should_shutdown():
                    logger.info("🛑 [增量更新] 在查询bond_info_cm时接收到停止信号")
                    return {
                        "success": True,
                        "message": "在查询阶段接收到停止信号，增量更新已停止",
                        "stopped": True
                    }
                
                code = doc.get("code") or doc.get("债券代码")
                name = doc.get("债券简称", "")
                if code:
                    basic_bonds[str(code).strip()] = str(name).strip()
            
            logger.info(f"📈 [增量更新] bond_info_cm中找到 {len(basic_bonds)} 个债券代码")
            
            # 2. 获取bond_info_detail_cm中已有的债券代码
            logger.info("📊 [增量更新] 正在查询bond_info_detail_cm中的债券代码...")
            cursor_detail = self.col_info_cm.find(
                {"endpoint": "bond_info_detail_cm"},
                {"code": 1}
            )
            
            detail_codes = set()
            async for doc in cursor_detail:
                # 在查询循环中检查停止信号
                if self.should_shutdown():
                    logger.info("🛑 [增量更新] 在查询bond_info_detail_cm时接收到停止信号")
                    return {
                        "success": True,
                        "message": "在查询阶段接收到停止信号，增量更新已停止",
                        "stopped": True
                    }
                
                code = doc.get("code")
                if code:
                    detail_codes.add(str(code).strip())
            
            logger.info(f"📈 [增量更新] bond_info_detail_cm中找到 {len(detail_codes)} 个债券代码")
            
            # 3. 找出缺失的债券代码
            missing_codes = set(basic_bonds.keys()) - detail_codes
            logger.info(f"🔍 [增量更新] 发现 {len(missing_codes)} 个缺失的债券基础信息")
            
            if not missing_codes:
                return {
                    "success": True,
                    "total_basic_codes": len(basic_bonds),
                    "total_detail_codes": len(detail_codes),
                    "missing_codes": 0,
                    "updated": 0,
                    "errors": 0,
                    "message": "没有发现缺失的债券基础信息"
                }
            
            # 4. 逐个获取缺失的基础信息
            updated_count = 0
            error_count = 0
            error_details = []
            
            for i, code in enumerate(missing_codes, 1):
                try:
                    # 检查是否需要停止
                    if self.should_shutdown():
                        logger.info("🛑 [增量更新] 接收到停止信号，提前退出处理")
                        break
                        
                    name = basic_bonds.get(code, "")
                    logger.info(f"🔄 [增量更新] ({i}/{len(missing_codes)}) 正在获取 {code}({name}) 的基础信息...")
                    
                    # 优先使用债券简称获取详细信息
                    detail_saved = False
                    if name:
                        try:
                            # 提取纯净的债券简称
                            clean_name = self._extract_bond_name(name)
                            logger.debug(f"🔄 [增量更新] 原始名称: '{name}' -> 清理后: '{clean_name}'")
                            
                            if not clean_name:
                                logger.warning(f"⚠️ [增量更新] 无法提取有效的债券简称: '{name}'")
                                continue
                            
                            import akshare as ak
                            detail_df = await asyncio.to_thread(ak.bond_info_detail_cm, symbol=clean_name)
                            
                            if isinstance(detail_df, pd.DataFrame) and not detail_df.empty:
                                # 转换DataFrame为字典格式
                                data_dict = self._convert_detail_dataframe_to_dict(detail_df, code, name)
                                
                                # 保存详细信息
                                saved = await self._save_bond_detail_dict(data_dict)
                                if saved > 0:
                                    updated_count += 1
                                    detail_saved = True
                                    logger.debug(f"✅ [增量更新] {code}({name}) 详细信息更新成功，字段数: {len(data_dict)}")
                        except Exception as detail_error:
                            logger.debug(f"⚠️ [增量更新] {code}({name}) 详细信息获取失败: {detail_error}")
                    
                    # 如果详细信息获取失败，尝试基础信息
                    if not detail_saved:
                        # 再次检查停止信号
                        if self.should_shutdown():
                            logger.info("🛑 [增量更新] 接收到停止信号，退出基础信息获取")
                            break
                            
                        basic_info = await self.provider.get_basic_info(code)
                        
                        if basic_info and "error" not in basic_info:
                            saved = await self.bond_data_service.save_bond_info_from_api(code, basic_info)
                            if saved > 0:
                                updated_count += 1
                                logger.debug(f"✅ [增量更新] {code}({name}) 基础信息更新成功")
                            else:
                                logger.debug(f"⚠️ [增量更新] {code}({name}) 基础信息保存失败")
                        else:
                            error_count += 1
                            error_details.append({
                                "code": code,
                                "name": name,
                                "error": basic_info.get("error", "unknown") if basic_info else "no_basic_info"
                            })
                            logger.debug(f"❌ [增量更新] {code}({name}) 基础信息获取失败")
                    
                    # 限流 - 在sleep期间也检查停止信号
                    for _ in range(10):  # 100ms分成10个10ms检查
                        if self.should_shutdown():
                            logger.info("🛑 [增量更新] 在休眠期间接收到停止信号")
                            break
                        await asyncio.sleep(0.01)
                    
                except Exception as e:
                    error_count += 1
                    error_details.append({"code": code, "name": name, "error": str(e)})
                    logger.error(f"❌ [增量更新] {code}({name}) 处理异常: {e}")
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            logger.info(f"✅ [增量更新] 完成！处理 {len(missing_codes)} 个缺失代码，"
                       f"更新 {updated_count} 个，错误 {error_count} 个，耗时 {duration:.2f}s")
            
            return {
                "success": True,
                "total_basic_codes": len(basic_bonds),
                "total_detail_codes": len(detail_codes),
                "missing_codes": len(missing_codes),
                "updated": updated_count,
                "errors": error_count,
                "error_details": error_details[:10],  # 只返回前10个错误详情
                "duration_seconds": duration,
                "message": f"增量更新完成，更新了 {updated_count} 个缺失的债券基础信息"
            }
            
        except Exception as e:
            logger.error(f"❌ [增量更新] 执行失败: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_update_statistics(self) -> Dict[str, Any]:
        """
        获取更新统计信息
        
        Returns:
            Dict包含各种统计数据
        """
        try:
            # 统计bond_info_cm中的记录数
            basic_count = await self.col_info_cm.count_documents({"endpoint": "bond_info_cm"})
            
            # 统计bond_info_detail_cm中的记录数
            detail_count = await self.col_info_cm.count_documents({"endpoint": "bond_info_detail_cm"})
            
            # 统计bond_basic_info中的记录数
            basic_info_count = await self.col_basic.count_documents({})
            
            # 计算覆盖率
            coverage_rate = (detail_count / basic_count * 100) if basic_count > 0 else 0
            
            return {
                "success": True,
                "bond_info_cm_count": basic_count,
                "bond_info_detail_cm_count": detail_count,
                "bond_basic_info_count": basic_info_count,
                "coverage_rate": round(coverage_rate, 2),
                "missing_detail_count": max(0, basic_count - detail_count)
            }
            
        except Exception as e:
            logger.error(f"❌ [统计信息] 获取失败: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e)
            }
