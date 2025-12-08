"""
可转债分时行情服务（重构版）

数据集合名称: bond_zh_hs_cov_min
"""
from app.services.data_sources.base_service import BaseService
from ..providers.bond_zh_hs_cov_min_provider import BondZhHsCovMinProvider


class BondZhHsCovMinService(BaseService):
    """可转债分时行情服务"""
    
    collection_name = "bond_zh_hs_cov_min"
    provider_class = BondZhHsCovMinProvider
    
    # 批量更新：从可转债实时行情集合中按代码（带交易所前缀，如 sh110044、sz128039）驱动
    batch_source_collection = "bond_zh_hs_cov_spot"
    batch_source_field = "代码"

    def get_batch_params(self, code):
        """根据可转债代码构造 Provider 调用参数，转换为带交易所前缀的 symbol。

        bond_zh_hs_cov_spot 集合中的 `代码` 字段为 6 位数字代码，例如 128044、113584。
        AkShare 的 bond_zh_hs_cov_min 需要带交易所前缀的 symbol，例如 sz128044、sh113584。
        这里根据可转债代码前缀简单推断交易所：
        - 以 11 开头 -> 上海 (sh)
        - 以 12 开头 -> 深圳 (sz)
        其他情况按常见规则回退到：
        - 113/118/132 -> 上海
        - 否则默认为深圳
        """
        if not code:
            return {}

        code_str = str(code).strip()
        if not code_str:
            return {}

        exchange = "sz"
        if code_str.startswith("11"):
            exchange = "sh"
        elif code_str.startswith("12"):
            exchange = "sz"
        elif code_str.startswith(("113", "118", "132")):
            exchange = "sh"

        symbol = f"{exchange}{code_str}"
        return {"symbol": symbol}

    async def _get_source_codes(self):
        """仅使用 bond_zh_hs_cov_spot 集合中最新更新时间对应的代码(字段 `代码`) 作为批量更新代码源。

        步骤：
        1. 在源集合中找到最大的 `更新时间`；
        2. 仅选择 `更新时间` 等于该最大值的文档，提取其中的 `代码` 字段；
        3. 返回去重后的代码列表。
        """
        if not self.batch_source_collection or not self.batch_source_field:
            return []

        source_coll = self.db[self.batch_source_collection]

        # 先找到最新的更新时间
        latest_doc = await source_coll.find_one({}, sort=[("更新时间", -1)], projection={"更新时间": 1})
        if not latest_doc or "更新时间" not in latest_doc:
            return []

        latest_time = latest_doc["更新时间"]

        # 只取该更新时间下的 symbol
        cursor = source_coll.find({"更新时间": latest_time}, {self.batch_source_field: 1})
        codes = set()
        async for doc in cursor:
            code = doc.get(self.batch_source_field)
            if code:
                codes.add(code)

        return list(codes)
