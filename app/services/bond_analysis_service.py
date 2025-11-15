"""
债券分析服务
提供债券的AI分析功能，包括数据收集、LLM分析和报告生成
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import pandas as pd

from app.core.database import get_mongo_db
from app.services.bond_data_service import BondDataService
from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider
from tradingagents.dataflows.interface import get_cn_bond_info_unified
from tradingagents.utils.instrument_validator import normalize_bond_code

logger = logging.getLogger(__name__)

# 单例服务实例
_bond_analysis_service = None


def get_bond_analysis_service():
    """获取债券分析服务单例"""
    global _bond_analysis_service
    if _bond_analysis_service is None:
        _bond_analysis_service = BondAnalysisService()
    return _bond_analysis_service


class BondAnalysisService:
    """债券分析服务类"""
    
    def __init__(self):
        self.db = get_mongo_db()
        self.bond_data_service = BondDataService(self.db)
        self.bond_provider = AKShareBondProvider()
        self._tasks = {}  # 内存中存储任务状态
        
    async def create_analysis_task(
        self,
        user_id: str,
        task_id: str,
        request: Any
    ) -> Dict[str, Any]:
        """创建分析任务记录"""
        task_record = {
            "task_id": task_id,
            "user_id": user_id,
            "bond_code": request.bond_code,
            "parameters": request.parameters or {},
            "status": "pending",
            "progress": 0,
            "current_step": "初始化中...",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        # 保存到MongoDB
        await self.db.bond_analysis_tasks.insert_one(task_record)
        
        # 保存到内存
        self._tasks[task_id] = task_record
        
        return {"task_id": task_id}
    
    async def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """获取任务状态"""
        # 先从内存查找
        if task_id in self._tasks:
            task = self._tasks[task_id]
            return {
                "status": task.get("status", "pending"),
                "progress": task.get("progress", 0),
                "current_step": task.get("current_step", ""),
                "error": task.get("error")
            }
        
        # 从MongoDB查找
        task = await self.db.bond_analysis_tasks.find_one({"task_id": task_id})
        if task:
            return {
                "status": task.get("status", "pending"),
                "progress": task.get("progress", 0),
                "current_step": task.get("current_step", ""),
                "error": task.get("error")
            }
        
        return None
    
    async def get_task_result(self, task_id: str) -> Optional[Dict[str, Any]]:
        """获取任务结果"""
        result = await self.db.bond_analysis_results.find_one({"task_id": task_id})
        if result:
            # 移除MongoDB的_id字段
            result.pop("_id", None)
            result.pop("task_id", None)
            return result
        return None
    
    async def update_task_status(
        self,
        task_id: str,
        status: str,
        progress: int = None,
        current_step: str = None,
        error: str = None
    ):
        """更新任务状态"""
        update_data = {
            "status": status,
            "updated_at": datetime.utcnow()
        }
        
        if progress is not None:
            update_data["progress"] = progress
        if current_step is not None:
            update_data["current_step"] = current_step
        if error is not None:
            update_data["error"] = error
        
        # 更新MongoDB
        await self.db.bond_analysis_tasks.update_one(
            {"task_id": task_id},
            {"$set": update_data}
        )
        
        # 更新内存
        if task_id in self._tasks:
            self._tasks[task_id].update(update_data)
    
    async def execute_analysis_background(
        self,
        task_id: str,
        user_id: str,
        request: Any
    ):
        """在后台执行分析任务"""
        try:
            await self.update_task_status(task_id, "running", 0, "开始分析...")
            
            bond_code = request.bond_code
            parameters = request.parameters or {}
            analysis_date = parameters.get("analysis_date")
            research_depth = parameters.get("research_depth", "标准")
            selected_dimensions = parameters.get("selected_dimensions", [])
            
            # 步骤1: 收集债券数据
            await self.update_task_status(task_id, "running", 10, "收集债券数据...")
            bond_data = await self._collect_bond_data(bond_code, analysis_date, selected_dimensions)
            
            # 步骤2: 准备分析提示词
            await self.update_task_status(task_id, "running", 30, "准备分析提示词...")
            analysis_prompt = self._build_analysis_prompt(bond_data, research_depth, selected_dimensions)
            
            # 步骤3: 调用LLM进行分析
            await self.update_task_status(task_id, "running", 50, "AI分析中...")
            analysis_result = await self._call_llm_analysis(analysis_prompt, research_depth)
            
            # 步骤4: 解析和格式化结果
            await self.update_task_status(task_id, "running", 80, "生成分析报告...")
            formatted_result = self._format_analysis_result(bond_data, analysis_result)
            
            # 步骤5: 保存结果
            await self.update_task_status(task_id, "running", 90, "保存分析结果...")
            await self._save_analysis_result(task_id, user_id, bond_code, formatted_result)
            
            # 完成
            await self.update_task_status(task_id, "completed", 100, "分析完成")
            
        except Exception as e:
            logger.error(f"❌ 债券分析任务失败: {task_id}, 错误: {e}", exc_info=True)
            await self.update_task_status(task_id, "failed", 0, "分析失败", str(e))
            raise
    
    async def _collect_bond_data(
        self,
        bond_code: str,
        analysis_date: Optional[str],
        selected_dimensions: list
    ) -> Dict[str, Any]:
        """收集债券数据"""
        data = {
            "bond_code": bond_code,
            "analysis_date": analysis_date or datetime.now().strftime("%Y-%m-%d")
        }
        
        # 标准化债券代码
        norm = normalize_bond_code(bond_code)
        code_std = norm.get("code_std") or bond_code
        
        try:
            # 1. 基本信息
            if "fundamental" in selected_dimensions or not selected_dimensions:
                await self.bond_data_service.ensure_indexes()
                basic_info = await self.bond_data_service.query_bond_info(code_std)
                if basic_info:
                    data["basic_info"] = basic_info
                else:
                    # 从API获取
                    info_text = get_cn_bond_info_unified(bond_code)
                    if info_text and not info_text.startswith("❌"):
                        data["basic_info_text"] = info_text
            
            # 2. 历史行情数据
            if "technical" in selected_dimensions or not selected_dimensions:
                end_date = analysis_date or datetime.now().strftime("%Y-%m-%d")
                start_date = (datetime.now() - timedelta(days=180)).strftime("%Y-%m-%d")
                
                # 先从数据库查询
                daily_data = await self.bond_data_service.query_bond_daily(
                    code_std, start_date, end_date
                )
                
                # 如果数据库没有，从网络获取
                if daily_data is None or daily_data.empty:
                    logger.info(f"📡 数据库无历史数据，从网络获取: {code_std}")
                    try:
                        hist_df = await self.bond_provider.get_historical_data(
                            code_std, start_date, end_date, "daily"
                        )
                        if hist_df is not None and not hist_df.empty:
                            # 保存到数据库
                            saved = await self.bond_data_service.save_bond_daily(code_std, hist_df)
                            logger.info(f"💾 已保存 {saved} 条历史数据到数据库")
                            daily_data = hist_df
                    except Exception as e:
                        logger.warning(f"⚠️ 从网络获取历史数据失败: {e}")
                
                if daily_data is not None and not daily_data.empty:
                    data["daily_data"] = daily_data.to_dict(orient="records")
                    data["daily_summary"] = {
                        "total_days": len(daily_data),
                        "latest_price": float(daily_data.iloc[-1].get("close", 0)) if len(daily_data) > 0 else 0,
                        "price_change_pct": float(daily_data.iloc[-1].get("pct_chg", 0)) if len(daily_data) > 0 else 0,
                        "avg_volume": float(daily_data["volume"].mean()) if "volume" in daily_data.columns else 0
                    }
            
            # 3. 收益率曲线数据
            if "valuation" in selected_dimensions or not selected_dimensions:
                end_date = analysis_date or datetime.now().strftime("%Y-%m-%d")
                start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
                
                # 先从数据库查询
                yield_curve = await self.bond_data_service.query_yield_curve(start_date, end_date)
                
                # 如果数据库没有，从网络获取
                if yield_curve is None or yield_curve.empty:
                    logger.info(f"📡 数据库无收益率曲线数据，从网络获取")
                    try:
                        curve_df = await self.bond_provider.get_yield_curve(
                            start_date=start_date, end_date=end_date
                        )
                        if curve_df is not None and not curve_df.empty:
                            # 保存到数据库
                            saved = await self.bond_data_service.save_yield_curve(curve_df)
                            logger.info(f"💾 已保存 {saved} 条收益率曲线数据到数据库")
                            yield_curve = curve_df
                    except Exception as e:
                        logger.warning(f"⚠️ 从网络获取收益率曲线失败: {e}")
                
                if yield_curve is not None and not yield_curve.empty:
                    data["yield_curve"] = yield_curve.to_dict(orient="records")
                    data["yield_curve_summary"] = {
                        "latest_yield": float(yield_curve.iloc[-1].get("yield", 0)) if len(yield_curve) > 0 else 0,
                        "avg_yield": float(yield_curve["yield"].mean()) if "yield" in yield_curve.columns else 0
                    }
            
            # 4. 可转债相关数据
            if "convertible" in selected_dimensions:
                # 查询可转债估值数据
                cb_valuation = await self.db.bond_cb_valuation_daily.find_one(
                    {"code": code_std},
                    sort=[("date", -1)]
                )
                if cb_valuation:
                    data["convertible_data"] = cb_valuation
                
                # 查询可转债对比数据
                cb_comparison = await self.db.bond_cb_comparison.find_one(
                    {"code": code_std},
                    sort=[("date", -1)]
                )
                if cb_comparison:
                    data["convertible_comparison"] = cb_comparison
            
        except Exception as e:
            logger.warning(f"⚠️ 收集债券数据时出错: {e}", exc_info=True)
            data["data_collection_error"] = str(e)
        
        return data
    
    def _build_analysis_prompt(
        self,
        bond_data: Dict[str, Any],
        research_depth: str,
        selected_dimensions: list
    ) -> str:
        """构建分析提示词"""
        prompt_parts = []
        
        prompt_parts.append("你是一位专业的债券投资分析师。请根据以下债券数据，进行全面的投资分析。")
        prompt_parts.append(f"\n分析深度要求：{research_depth}")
        prompt_parts.append(f"\n分析维度：{', '.join(selected_dimensions) if selected_dimensions else '全部维度'}")
        
        # 基本信息
        if "basic_info" in bond_data:
            prompt_parts.append("\n## 债券基本信息：")
            basic_info = bond_data["basic_info"]
            prompt_parts.append(f"- 债券代码：{bond_data.get('bond_code', 'N/A')}")
            prompt_parts.append(f"- 债券名称：{basic_info.get('name', 'N/A')}")
            prompt_parts.append(f"- 债券类型：{basic_info.get('category', 'N/A')}")
            prompt_parts.append(f"- 发行人：{basic_info.get('issuer', 'N/A')}")
            prompt_parts.append(f"- 息票率：{basic_info.get('coupon_rate', 'N/A')}")
            prompt_parts.append(f"- 到期日：{basic_info.get('maturity_date', 'N/A')}")
            prompt_parts.append(f"- 上市日期：{basic_info.get('list_date', 'N/A')}")
        
        # 历史行情
        if "daily_summary" in bond_data:
            prompt_parts.append("\n## 历史行情摘要：")
            summary = bond_data["daily_summary"]
            prompt_parts.append(f"- 最新价格：{summary.get('latest_price', 0):.4f}")
            prompt_parts.append(f"- 涨跌幅：{summary.get('price_change_pct', 0):.2f}%")
            prompt_parts.append(f"- 平均成交量：{summary.get('avg_volume', 0):.2f}")
            prompt_parts.append(f"- 数据天数：{summary.get('total_days', 0)}")
        
        # 收益率曲线
        if "yield_curve_summary" in bond_data:
            prompt_parts.append("\n## 收益率曲线摘要：")
            summary = bond_data["yield_curve_summary"]
            prompt_parts.append(f"- 最新收益率：{summary.get('latest_yield', 0):.4f}%")
            prompt_parts.append(f"- 平均收益率：{summary.get('avg_yield', 0):.4f}%")
        
        # 可转债数据
        if "convertible_data" in bond_data:
            prompt_parts.append("\n## 可转债估值数据：")
            cb_data = bond_data["convertible_data"]
            # 添加关键可转债指标
            for key in ["转股溢价率", "纯债价值", "转股价值", "溢价率"]:
                if key in cb_data:
                    prompt_parts.append(f"- {key}：{cb_data[key]}")
        
        # 分析要求
        prompt_parts.append("\n## 分析要求：")
        prompt_parts.append("请从以下维度进行分析，并给出明确的投资建议（买入/持有/卖出）：")
        
        if "fundamental" in selected_dimensions or not selected_dimensions:
            prompt_parts.append("\n1. **基本面分析**：")
            prompt_parts.append("   - 债券基本信息评估")
            prompt_parts.append("   - 发行人信用状况分析")
            prompt_parts.append("   - 债券条款分析")
        
        if "technical" in selected_dimensions or not selected_dimensions:
            prompt_parts.append("\n2. **技术分析**：")
            prompt_parts.append("   - 价格走势分析")
            prompt_parts.append("   - 成交量分析")
            prompt_parts.append("   - 技术指标分析")
        
        if "valuation" in selected_dimensions or not selected_dimensions:
            prompt_parts.append("\n3. **估值分析**：")
            prompt_parts.append("   - 收益率分析")
            prompt_parts.append("   - 久期和凸性分析")
            prompt_parts.append("   - 相对价值分析")
        
        if "convertible" in selected_dimensions:
            prompt_parts.append("\n4. **可转债分析**：")
            prompt_parts.append("   - 转股溢价率分析")
            prompt_parts.append("   - 纯债价值分析")
            prompt_parts.append("   - 转股价值分析")
        
        prompt_parts.append("\n5. **风险评估**：")
        prompt_parts.append("   - 信用风险")
        prompt_parts.append("   - 利率风险")
        prompt_parts.append("   - 流动性风险")
        
        prompt_parts.append("\n请以Markdown格式输出分析报告，包括：")
        prompt_parts.append("- 分析摘要（200-300字）")
        prompt_parts.append("- 各维度详细分析")
        prompt_parts.append("- 综合投资建议（买入/持有/卖出，并说明理由）")
        prompt_parts.append("- 风险提示")
        
        return "\n".join(prompt_parts)
    
    async def _call_llm_analysis(self, prompt: str, research_depth: str) -> str:
        """调用LLM进行分析"""
        try:
            # 根据分析深度选择模型
            from app.core.config import settings
            model = "qwen-max" if research_depth == "深度" else "qwen-turbo"
            
            # 调用LLM
            from tradingagents.llm.providers import get_llm_provider
            provider = get_llm_provider("dashscope")
            
            response = await provider.agenerate(
                prompt=prompt,
                model=model,
                temperature=0.3,
                max_tokens=4000
            )
            
            return response.text if hasattr(response, 'text') else str(response)
            
        except Exception as e:
            logger.error(f"❌ LLM分析失败: {e}", exc_info=True)
            # 返回一个基本的分析结果
            return f"分析过程中出现错误：{str(e)}。请稍后重试。"
    
    def _format_analysis_result(
        self,
        bond_data: Dict[str, Any],
        llm_response: str
    ) -> Dict[str, Any]:
        """格式化分析结果"""
        # 解析LLM响应，提取各个部分
        result = {
            "bond_code": bond_data.get("bond_code"),
            "bond_name": bond_data.get("basic_info", {}).get("name", "未知"),
            "bond_type": bond_data.get("basic_info", {}).get("category", "未知"),
            "current_price": bond_data.get("daily_summary", {}).get("latest_price", 0),
            "price_change_percent": bond_data.get("daily_summary", {}).get("price_change_pct", 0),
            "maturity_date": bond_data.get("basic_info", {}).get("maturity_date"),
            "summary": "",
            "fundamental_analysis": "",
            "technical_analysis": "",
            "valuation_analysis": "",
            "convertible_analysis": "",
            "risk_assessment": "",
            "recommendation": ""
        }
        
        # 简单解析LLM响应（可以根据实际情况改进）
        response_text = llm_response
        
        # 提取摘要
        if "## 分析摘要" in response_text or "## 摘要" in response_text:
            parts = response_text.split("##")
            for part in parts:
                if "摘要" in part:
                    result["summary"] = part.split("\n", 1)[1] if "\n" in part else part
                    break
        
        # 提取各维度分析
        sections = {
            "fundamental_analysis": ["基本面分析", "基本面"],
            "technical_analysis": ["技术分析", "技术"],
            "valuation_analysis": ["估值分析", "估值"],
            "convertible_analysis": ["可转债分析", "可转债"],
            "risk_assessment": ["风险评估", "风险"],
            "recommendation": ["投资建议", "建议", "结论"]
        }
        
        for key, keywords in sections.items():
            for keyword in keywords:
                if f"## {keyword}" in response_text or f"### {keyword}" in response_text:
                    # 提取该部分内容
                    parts = response_text.split(f"## {keyword}")
                    if len(parts) > 1:
                        content = parts[1].split("##")[0].strip()
                        result[key] = content
                        break
        
        # 如果没有解析到，使用完整响应
        if not result["summary"]:
            result["summary"] = response_text[:500] + "..." if len(response_text) > 500 else response_text
        
        if not result["recommendation"]:
            # 尝试从响应中提取建议
            if "买入" in response_text or "buy" in response_text.lower():
                result["recommendation"] = "**买入建议**\n\n" + response_text
            elif "卖出" in response_text or "sell" in response_text.lower():
                result["recommendation"] = "**卖出建议**\n\n" + response_text
            elif "持有" in response_text or "hold" in response_text.lower():
                result["recommendation"] = "**持有建议**\n\n" + response_text
            else:
                result["recommendation"] = "**投资建议**\n\n" + response_text
        
        return result
    
    async def _save_analysis_result(
        self,
        task_id: str,
        user_id: str,
        bond_code: str,
        result: Dict[str, Any]
    ):
        """保存分析结果"""
        result_doc = {
            "task_id": task_id,
            "user_id": user_id,
            "bond_code": bond_code,
            **result,
            "created_at": datetime.utcnow()
        }
        
        await self.db.bond_analysis_results.insert_one(result_doc)

