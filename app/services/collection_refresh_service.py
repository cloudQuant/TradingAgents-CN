"""
数据集合刷新服务
为所有债券数据集合提供统一的更新接口，支持进度追踪
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import pandas as pd

from pymongo import UpdateOne
from app.services.bond_data_service import BondDataService
from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider
from app.utils.task_manager import get_task_manager

logger = logging.getLogger("webapi")


class CollectionRefreshService:
    """集合刷新服务"""
    
    def __init__(self, bond_service: BondDataService, provider: AKShareBondProvider = None):
        self.svc = bond_service
        self.provider = provider or AKShareBondProvider()
        self.task_manager = get_task_manager()
    
    async def refresh_collection(
        self,
        collection_name: str,
        task_id: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """刷新指定集合的数据
        
        Args:
            collection_name: 集合名称
            task_id: 任务ID
            params: 参数字典，包含所有可能的参数
        """
        
        try:
            self.task_manager.start_task(task_id)
            
            if params is None:
                params = {}
            
            # 根据集合名称路由到对应的处理方法
            handlers = {
                "bond_basic_info": self._refresh_bond_basic_info,
                "yield_curve_daily": self._refresh_yield_curve_daily,
                "bond_daily": self._refresh_bond_daily,
                "bond_cb_list_jsl": self._refresh_bond_cb_list_jsl,
                "bond_cov_list": self._refresh_bond_cov_list,
                "bond_cb_profiles": self._refresh_bond_cb_profiles,
                "bond_spot_quotes": self._refresh_bond_spot_quotes,
                "bond_cash_summary": self._refresh_bond_cash_summary,
                "bond_deal_summary": self._refresh_bond_deal_summary,
                "bond_nafmii_debts": self._refresh_bond_nafmii_debts,
                "bond_spot_quote_detail": self._refresh_bond_spot_quote_detail,
                "bond_spot_deals": self._refresh_bond_spot_deals,
                "bond_indices_daily": self._refresh_bond_indices_daily,
                "us_yield_daily": self._refresh_us_yield_daily,
                "yield_curve_map": self._refresh_yield_curve_map,
                "bond_buybacks": self._refresh_bond_buybacks,
                "bond_cb_summary": self._refresh_bond_cb_summary,
                "bond_info_cm": self._refresh_bond_info_cm,
            }
            
            handler = handlers.get(collection_name)
            if not handler:
                raise ValueError(f"集合 {collection_name} 暂不支持自动更新")
            
            result = await handler(task_id, params)
            
            self.task_manager.complete_task(task_id, result=result)
            return {"success": True, "data": result}
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"❌ 刷新集合 {collection_name} 失败: {error_msg}", exc_info=True)
            self.task_manager.fail_task(task_id, error_msg)
            return {"success": False, "error": error_msg}
    
    # ========== 各集合的具体刷新方法 ==========
    
    async def _refresh_bond_basic_info(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新债券基本信息"""
        self.task_manager.update_progress(task_id, 10, 100, "正在从AKShare获取债券列表...")
        
        bond_list = await self.provider.get_symbol_list()
        if not bond_list:
            raise ValueError("未获取到债券列表")
        
        self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(bond_list)} 条数据...")
        saved = await self.svc.save_basic_list(bond_list)
        
        return {"saved": saved, "total": len(bond_list)}
    
    async def _refresh_yield_curve_daily(
        self, task_id: str, params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """刷新收益率曲线"""
        start_date = params.get("start_date")
        end_date = params.get("end_date")
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        
        self.task_manager.update_progress(task_id, 10, 100, f"正在获取 {start_date} 至 {end_date} 的数据...")
        curve_df = await self.provider.get_yield_curve(start_date, end_date)
        
        if curve_df is None or curve_df.empty:
            raise ValueError("未获取到收益率曲线数据，请检查日期范围（需要小于一年）")
        
        self.task_manager.update_progress(task_id, 50, 100, f"正在保存 {len(curve_df)} 条数据...")
        saved = await self.svc.save_yield_curve(curve_df)
        
        return {"saved": saved, "rows": len(curve_df)}
    
    async def _refresh_bond_daily(
        self, task_id: str, params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """刷新债券历史行情"""
        start_date = params.get("start_date")
        end_date = params.get("end_date")
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
        if not start_date:
            start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        
        self.task_manager.update_progress(task_id, 10, 100, "正在获取债券列表...")
        cursor = self.svc.col_basic.find({}, {"code": 1, "name": 1}).limit(10)
        bonds = await cursor.to_list(length=10)
        
        if not bonds:
            raise ValueError("未找到债券列表，请先更新 bond_basic_info")
        
        total_saved = 0
        success_count = 0
        fail_count = 0
        
        for i, bond in enumerate(bonds):
            code = bond.get("code")
            if not code:
                continue
            
            progress = 10 + (i + 1) * 80 // len(bonds)
            self.task_manager.update_progress(
                task_id, progress, 100, 
                f"正在更新 {bond.get('name', code)} ({i+1}/{len(bonds)})..."
            )
            
            try:
                hist_df = await self.provider.get_historical_data(code, start_date, end_date, "daily")
                if hist_df is not None and not hist_df.empty:
                    saved = await self.svc.save_bond_daily(code, hist_df)
                    total_saved += saved
                    success_count += 1
            except Exception as e:
                fail_count += 1
                logger.debug(f"更新 {code} 失败: {e}")
        
        return {
            "saved": total_saved,
            "success_count": success_count,
            "fail_count": fail_count,
            "total": len(bonds)
        }
    
    async def _refresh_bond_cb_list_jsl(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新集思录可转债"""
        import akshare as ak
        
        self.task_manager.update_progress(task_id, 20, 100, "正在从集思录获取数据...")
        df = await asyncio.to_thread(ak.bond_cb_jsl)
        
        if df is None or df.empty:
            raise ValueError("未获取到集思录可转债数据")
        
        self.task_manager.update_progress(task_id, 60, 100, f"正在保存 {len(df)} 条数据...")
        ops = []
        for _, row in df.iterrows():
            doc = row.to_dict()
            code = str(doc.get("bond_id", "") or doc.get("转债代码", ""))
            if code:
                doc["code"] = code
                ops.append(UpdateOne({"code": code}, {"$set": doc}, upsert=True))
        
        if ops:
            result = await self.svc.col_cb_list_jsl.bulk_write(ops, ordered=False)
            saved = (result.upserted_count or 0) + (result.modified_count or 0)
        else:
            saved = 0
        
        return {"saved": saved, "rows": len(df)}
    
    async def _refresh_bond_cov_list(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新东财可转债列表"""
        import akshare as ak
        
        self.task_manager.update_progress(task_id, 20, 100, "正在从东财获取数据...")
        df = await asyncio.to_thread(ak.bond_cov_comparison)
        
        if df is None or df.empty:
            raise ValueError("未获取到可转债列表")
        
        self.task_manager.update_progress(task_id, 60, 100, f"正在保存 {len(df)} 条数据...")
        ops = []
        for _, row in df.iterrows():
            doc = row.to_dict()
            code = str(doc.get("债券代码", ""))
            if code:
                doc["code"] = code
                ops.append(UpdateOne({"code": code}, {"$set": doc}, upsert=True))
        
        if ops:
            result = await self.svc.col_cov_list.bulk_write(ops, ordered=False)
            saved = (result.upserted_count or 0) + (result.modified_count or 0)
        else:
            saved = 0
        
        return {"saved": saved, "rows": len(df)}
    
    async def _refresh_bond_cb_profiles(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新可转债档案"""
        import akshare as ak
        
        self.task_manager.update_progress(task_id, 20, 100, "正在获取可转债档案...")
        df = await asyncio.to_thread(ak.bond_cb_profile)
        
        if df is None or df.empty:
            raise ValueError("未获取到可转债档案数据")
        
        self.task_manager.update_progress(task_id, 60, 100, f"正在保存 {len(df)} 条数据...")
        ops = []
        for _, row in df.iterrows():
            doc = row.to_dict()
            code = str(doc.get("可转债代码", "") or doc.get("代码", ""))
            if code:
                doc["code"] = code
                ops.append(UpdateOne({"code": code}, {"$set": doc}, upsert=True))
        
        if ops:
            result = await self.svc.col_cb_profiles.bulk_write(ops, ordered=False)
            saved = (result.upserted_count or 0) + (result.modified_count or 0)
        else:
            saved = 0
        
        return {"saved": saved, "rows": len(df)}
    
    async def _refresh_bond_spot_quotes(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新现货报价"""
        import akshare as ak
        import time
        
        self.task_manager.update_progress(task_id, 20, 100, "正在获取现货报价...")
        df = await asyncio.to_thread(ak.bond_spot_quote)
        
        if df is None or df.empty:
            raise ValueError("未获取到现货报价数据")
        
        self.task_manager.update_progress(task_id, 60, 100, f"正在保存 {len(df)} 条数据...")
        timestamp = int(time.time())
        ops = []
        for _, row in df.iterrows():
            doc = row.to_dict()
            doc["timestamp"] = timestamp
            code = str(doc.get("债券简称", ""))
            category = str(doc.get("报价机构", ""))
            if code:
                doc["code"] = code
                doc["category"] = category
                ops.append(UpdateOne(
                    {"code": code, "timestamp": timestamp, "category": category},
                    {"$set": doc},
                    upsert=True
                ))
        
        if ops:
            result = await self.svc.col_spot.bulk_write(ops, ordered=False)
            saved = (result.upserted_count or 0) + (result.modified_count or 0)
        else:
            saved = 0
        
        return {"saved": saved, "rows": len(df)}
    
    async def _refresh_bond_cash_summary(
        self, task_id: str, params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """刷新现券市场概览"""
        import akshare as ak
        
        date = params.get("date")
        if not date:
            date = datetime.now().strftime("%Y%m%d")
        else:
            date = date.replace("-", "")
        
        self.task_manager.update_progress(task_id, 20, 100, f"正在获取 {date} 的数据...")
        df = await asyncio.to_thread(ak.bond_cash_summary_sse, date=date)
        
        if df is None or df.empty:
            raise ValueError(f"未获取到 {date} 的数据")
        
        self.task_manager.update_progress(task_id, 60, 100, f"正在保存 {len(df)} 条数据...")
        ops = []
        for _, row in df.iterrows():
            doc = row.to_dict()
            doc["date"] = str(doc.get("数据日期", date))
            ops.append(UpdateOne(
                {"date": doc["date"], "债券现货": doc.get("债券现货")},
                {"$set": doc},
                upsert=True
            ))
        
        if ops:
            result = await self.svc.col_cash_summary.bulk_write(ops, ordered=False)
            saved = (result.upserted_count or 0) + (result.modified_count or 0)
        else:
            saved = 0
        
        return {"saved": saved, "rows": len(df)}
    
    async def _refresh_bond_deal_summary(
        self, task_id: str, params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """刷新成交概览"""
        import akshare as ak
        
        date = params.get("date")
        if not date:
            date = datetime.now().strftime("%Y%m%d")
        else:
            date = date.replace("-", "")
        
        self.task_manager.update_progress(task_id, 20, 100, f"正在获取 {date} 的数据...")
        df = await asyncio.to_thread(ak.bond_deal_summary_sse, date=date)
        
        if df is None or df.empty:
            raise ValueError(f"未获取到 {date} 的数据")
        
        self.task_manager.update_progress(task_id, 60, 100, f"正在保存 {len(df)} 条数据...")
        ops = []
        for _, row in df.iterrows():
            doc = row.to_dict()
            doc["date"] = str(doc.get("数据日期", date))
            ops.append(UpdateOne(
                {"date": doc["date"], "债券类型": doc.get("债券类型")},
                {"$set": doc},
                upsert=True
            ))
        
        if ops:
            result = await self.svc.col_deal_summary.bulk_write(ops, ordered=False)
            saved = (result.upserted_count or 0) + (result.modified_count or 0)
        else:
            saved = 0
        
        return {"saved": saved, "rows": len(df)}
    
    async def _refresh_bond_nafmii_debts(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新银行间市场债务"""
        import akshare as ak
        
        all_data = []
        for page in range(1, 11):
            self.task_manager.update_progress(
                task_id, 10 + page * 7, 100, 
                f"正在获取第 {page}/10 页数据..."
            )
            try:
                df = await asyncio.to_thread(ak.bond_debt_nafmii, page=str(page))
                if df is not None and not df.empty:
                    all_data.append(df)
            except Exception as e:
                logger.debug(f"获取第{page}页失败: {e}")
                break
        
        if not all_data:
            raise ValueError("未获取到NAFMII数据")
        
        combined_df = pd.concat(all_data, ignore_index=True)
        
        self.task_manager.update_progress(task_id, 85, 100, f"正在保存 {len(combined_df)} 条数据...")
        ops = []
        for _, row in combined_df.iterrows():
            doc = row.to_dict()
            reg_no = str(doc.get("注册通知书文号", ""))
            if reg_no and reg_no != "nan":
                doc["reg_no"] = reg_no
                ops.append(UpdateOne(
                    {"reg_no": reg_no},
                    {"$set": doc},
                    upsert=True
                ))
        
        if ops:
            result = await self.svc.col_nafmii.bulk_write(ops, ordered=False)
            saved = (result.upserted_count or 0) + (result.modified_count or 0)
        else:
            saved = 0
        
        return {"saved": saved, "rows": len(combined_df)}
    
    async def _refresh_bond_spot_quote_detail(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新现货报价明细（同 bond_spot_quotes）"""
        return await self._refresh_bond_spot_quotes(task_id, params)
    
    async def _refresh_bond_spot_deals(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新现货成交明细"""
        import akshare as ak
        import time
        
        self.task_manager.update_progress(task_id, 20, 100, "正在获取现货成交数据...")
        df = await asyncio.to_thread(ak.bond_spot_deal)
        
        if df is None or df.empty:
            raise ValueError("未获取到现货成交数据")
        
        self.task_manager.update_progress(task_id, 60, 100, f"正在保存 {len(df)} 条数据...")
        timestamp = int(time.time())
        ops = []
        for _, row in df.iterrows():
            doc = row.to_dict()
            doc["timestamp"] = timestamp
            code = str(doc.get("债券简称", ""))
            if code:
                doc["code"] = code
                ops.append(UpdateOne(
                    {"code": code, "timestamp": timestamp},
                    {"$set": doc},
                    upsert=True
                ))
        
        if ops:
            result = await self.svc.col_spot_deals.bulk_write(ops, ordered=False)
            saved = (result.upserted_count or 0) + (result.modified_count or 0)
        else:
            saved = 0
        
        return {"saved": saved, "rows": len(df)}
    
    async def _refresh_bond_indices_daily(
        self, task_id: str, params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """刷新债券指数（暂不实现，数据源复杂）"""
        raise ValueError("债券指数数据源复杂，暂不支持自动更新。请手动导入数据或联系管理员。")
    
    async def _refresh_us_yield_daily(
        self, task_id: str, params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """刷新美国国债收益率（暂不实现）"""
        raise ValueError("美国国债收益率数据暂不支持自动更新。请手动导入数据或联系管理员。")
    
    async def _refresh_yield_curve_map(
        self, task_id: str, params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """刷新收益率曲线映射（基于 yield_curve_daily）"""
        raise ValueError("收益率曲线映射需要复杂的数据处理，暂不支持自动更新。请先更新 yield_curve_daily。")
    
    async def _refresh_bond_buybacks(
        self, task_id: str, params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """刷新债券回购（暂不实现）"""
        raise ValueError("债券回购数据暂不支持自动更新。请手动导入数据或联系管理员。")
    
    async def _refresh_bond_cb_summary(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新可转债概况（暂不实现）"""
        raise ValueError("可转债概况数据暂不支持自动更新。请手动导入数据或联系管理员。")
    
    async def _refresh_bond_info_cm(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """刷新中债信息查询
        
        支持按参数查询：
        - bond_name: 债券名称
        - bond_code: 债券代码
        - bond_issue: 发行人
        - bond_type: 债券类型
        - coupon_type: 付息方式
        - issue_year: 发行年份
        - underwriter: 承销商
        - grade: 评级
        
        如果所有参数为空，则获取所有债券数据（可能较慢）
        """
        # 提取bond_info_cm相关参数
        bond_name = params.get("bond_name") or ""
        bond_code = params.get("bond_code") or ""
        bond_issue = params.get("bond_issue") or ""
        bond_type = params.get("bond_type") or ""
        coupon_type = params.get("coupon_type") or ""
        issue_year = params.get("issue_year") or ""
        underwriter = params.get("underwriter") or ""
        grade = params.get("grade") or ""
        
        # 构建参数描述
        param_desc = []
        if bond_name:
            param_desc.append(f"债券名称={bond_name}")
        if bond_code:
            param_desc.append(f"债券代码={bond_code}")
        if bond_issue:
            param_desc.append(f"发行人={bond_issue}")
        if bond_type:
            param_desc.append(f"债券类型={bond_type}")
        if coupon_type:
            param_desc.append(f"付息方式={coupon_type}")
        if issue_year:
            param_desc.append(f"发行年份={issue_year}")
        if underwriter:
            param_desc.append(f"承销商={underwriter}")
        if grade:
            param_desc.append(f"评级={grade}")
        
        if param_desc:
            desc_text = ", ".join(param_desc)
            self.task_manager.update_progress(task_id, 10, 100, f"正在查询中债信息（{desc_text}）...")
        else:
            self.task_manager.update_progress(task_id, 10, 100, "正在查询所有中债信息（可能较慢）...")
        
        # 调用provider获取数据
        df = await self.provider.get_bond_info_cm(
            bond_name=bond_name,
            bond_code=bond_code,
            bond_issue=bond_issue,
            bond_type=bond_type,
            coupon_type=coupon_type,
            issue_year=issue_year,
            underwriter=underwriter,
            grade=grade
        )
        
        if df is None or df.empty:
            raise ValueError("未获取到符合条件的债券信息数据，请调整查询参数")
        
        self.task_manager.update_progress(task_id, 60, 100, f"正在保存 {len(df)} 条数据...")
        
        # 保存到数据库
        saved = await self.svc.save_info_cm(df)
        
        self.task_manager.update_progress(task_id, 100, 100, f"完成！保存了 {saved} 条数据")
        
        return {
            "saved": saved,
            "rows": len(df),
            "query_params": {
                "bond_name": bond_name,
                "bond_code": bond_code,
                "bond_issue": bond_issue,
                "bond_type": bond_type,
                "coupon_type": coupon_type,
                "issue_year": issue_year,
                "underwriter": underwriter,
                "grade": grade
            }
        }
