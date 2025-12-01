"""
基金实时行情-新浪服务（重构版：继承SimpleService）
"""
from typing import Any, Dict, List

from app.services.data_sources.base_service import SimpleService
from ..providers.fund_spot_sina_provider import FundSpotSinaProvider


class FundSpotSinaService(SimpleService):
    """基金实时行情-新浪服务"""
    
    collection_name = "fund_spot_sina"
    provider_class = FundSpotSinaProvider

    async def get_overview(self) -> Dict[str, Any]:
        """
        为前端结构/市场分析提供专用统计数据：
            - total_count / rise_count / fall_count / flat_count
            - type_stats：按基金类型分布
            - top_volume / top_gainers / top_losers
        """
        total_count = await self.collection.count_documents({})
        if total_count == 0:
            return {
                "total_count": 0,
                "rise_count": 0,
                "fall_count": 0,
                "flat_count": 0,
                "type_stats": [],
                "top_volume": [],
                "top_gainers": [],
                "top_losers": [],
            }

        rise_count = await self._count_by_rate({"$gt": 0})
        fall_count = await self._count_by_rate({"$lt": 0})
        flat_count = max(0, total_count - rise_count - fall_count)

        type_stats = await self.collection.aggregate(
            [
                {"$group": {"_id": "$基金类型", "count": {"$sum": 1}}},
                {
                    "$project": {
                        "_id": 0,
                        "type": {"$ifNull": ["$_id", "未分类"]},
                        "count": 1,
                    }
                },
                {"$sort": {"count": -1}},
                {"$limit": 20},
            ]
        ).to_list(length=20)

        top_volume = await self.collection.aggregate(
            [
                {"$match": {"成交额": {"$ne": None}}},
                {
                    "$project": {
                        "_id": 0,
                        "code": "$代码",
                        "name": "$名称",
                        "amount": "$成交额",
                    }
                },
                {"$sort": {"amount": -1}},
                {"$limit": 10},
            ]
        ).to_list(length=10)

        top_gainers = await self._build_rank_list(sort_direction=-1)
        top_losers = await self._build_rank_list(sort_direction=1)

        return {
            "total_count": total_count,
            "rise_count": rise_count,
            "fall_count": fall_count,
            "flat_count": flat_count,
            "type_stats": type_stats,
            "top_volume": top_volume,
            "top_gainers": top_gainers,
            "top_losers": top_losers,
        }

    async def _count_by_rate(self, condition: Dict[str, Any]) -> int:
        return await self.collection.count_documents({"涨跌幅": condition})

    async def _build_rank_list(self, sort_direction: int) -> List[Dict[str, Any]]:
        cursor = (
            self.collection.find(
                {"涨跌幅": {"$ne": None}},
                {"代码": 1, "名称": 1, "涨跌幅": 1},
            )
            .sort("涨跌幅", sort_direction)
            .limit(10)
        )

        results: List[Dict[str, Any]] = []
        async for doc in cursor:
            rate_value = doc.get("涨跌幅")
            try:
                rate_float = float(rate_value) if rate_value is not None else None
            except (TypeError, ValueError):
                rate_float = None

            results.append(
                {
                    "code": doc.get("代码"),
                    "name": doc.get("名称"),
                    "rate": rate_float,
                }
            )
        return results
