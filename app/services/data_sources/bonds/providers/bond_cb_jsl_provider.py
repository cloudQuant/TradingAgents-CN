"""可转债实时数据-集思录数据提供者（重构版）

需求文档: tests/bonds/requirements/22_可转债实时数据-集思录.md
数据唯一标识: 代码

说明:
- 优先使用请求参数中的 ``cookie``，否则使用 ``user/password``
- ``user/password`` 默认从 .env 中的 ``JISILU_USER`` / ``JISILU_PASSWORD`` 读取
"""
import pandas as pd

from app.services.data_sources.base_provider import SimpleProvider
from app.core.config import get_settings


class BondCbJslProvider(SimpleProvider):
    """可转债实时数据-集思录数据提供者"""
    
    collection_name = "bond_cb_jsl"
    display_name = "可转债实时数据-集思录"
    akshare_func = "bond_cb_jsl"
    unique_keys = ["代码"]
    
    collection_description = "集思录可转债实时数据，包含转股溢价率、双低等指标"
    collection_route = "/bonds/collections/bond_cb_jsl"
    collection_order = 22
    
    field_info = [
        {"name": "代码", "type": "string", "description": "可转债代码"},
        {"name": "转债名称", "type": "string", "description": "可转债名称"},
        {"name": "现价", "type": "float", "description": "可转债现价"},
        {"name": "涨跌幅", "type": "float", "description": "涨跌幅(%)"},
        {"name": "正股代码", "type": "string", "description": "正股代码"},
        {"name": "正股名称", "type": "string", "description": "正股名称"},
        {"name": "正股价", "type": "float", "description": "正股价格"},
        {"name": "转股价", "type": "float", "description": "转股价"},
        {"name": "转股价值", "type": "float", "description": "转股价值"},
        {"name": "转股溢价率", "type": "float", "description": "转股溢价率(%)"},
        {"name": "债券评级", "type": "string", "description": "债券评级"},
        {"name": "剩余年限", "type": "float", "description": "剩余年限"},
        {"name": "剩余规模", "type": "float", "description": "剩余规模(亿元)"},
        {"name": "成交额", "type": "float", "description": "成交额(万元)"},
        {"name": "双低", "type": "float", "description": "双低值"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "来源", "type": "string", "description": "来源接口"},
    ]

    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """获取集思录可转债实时数据

        参数优先级:
        1. 如果提供 ``cookie``，则使用 cookie 调用 ak.bond_cb_jsl(cookie=...)
        2. 否则，如果提供 ``user``/``password``，或 .env 中配置了 JISILU_USER/JISILU_PASSWORD，
           则调用 ak.bond_cb_jsl(user=..., password=...)
        3. 如果两者都没有，抛出友好的错误提示。
        """

        settings = get_settings()

        cookie = kwargs.get("cookie")
        # 请求参数优先，其次使用环境变量
        user = (kwargs.get("user") or settings.JISILU_USER or "").strip()
        password = (kwargs.get("password") or settings.JISILU_PASSWORD or "").strip()

        ak_kwargs = {}
        if cookie:
            ak_kwargs["cookie"] = cookie
            auth_mode = "cookie"
        elif user and password:
            ak_kwargs["user"] = user
            ak_kwargs["password"] = password
            auth_mode = "user/password"
        else:
            raise ValueError(
                "缺少集思录认证信息，请在 .env 中配置 JISILU_USER/JISILU_PASSWORD，"
                "或在更新参数中提供 user/password，或提供 cookie 参数。"
            )

        self.logger.info(
            f"Fetching {self.collection_name} data from Jisilu with auth_mode={auth_mode}"
        )

        df = self._call_akshare(self.akshare_func, **ak_kwargs)
        if df is None or df.empty:
            self.logger.warning(f"No data returned for {self.collection_name}")
            return pd.DataFrame()

        # 添加时间戳等元数据
        df = self._add_metadata(df)
        self.logger.info(f"Successfully fetched {len(df)} records for {self.collection_name}")
        return df
