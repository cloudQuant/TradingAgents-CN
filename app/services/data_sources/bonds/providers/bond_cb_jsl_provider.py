"""
可转债实时数据-集思录数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BondCbJslProvider:
    """可转债实时数据-集思录数据提供者"""
    
    def __init__(self):
        self.collection_name = "bond_cb_jsl"
        self.display_name = "可转债实时数据-集思录"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """获取集思录可转债数据"""
        try:
            cookie = kwargs.get("cookie", "")
            logger.info(f"Fetching {self.collection_name} data")
            
            if cookie:
                df = ak.bond_cb_jsl(cookie=cookie)
            else:
                df = ak.bond_cb_jsl()
            
            if df is None or df.empty:
                return pd.DataFrame()
            
            df['数据源'] = 'akshare'
            df['接口名称'] = 'bond_cb_jsl'
            df['更新时间'] = datetime.now()
            
            logger.info(f"Successfully fetched {len(df)} records")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        """获取字段信息（无cookie只返回前30条）"""
        return [
            {"name": "代码", "type": "string", "description": "可转债代码"},
            {"name": "转债名称", "type": "string", "description": "可转债名称"},
            {"name": "现价", "type": "float", "description": "可转债现价"},
            {"name": "涨跌幅", "type": "float", "description": "涨跌幅(%)"},
            {"name": "正股代码", "type": "string", "description": "正股代码"},
            {"name": "正股名称", "type": "string", "description": "正股名称"},
            {"name": "正股价", "type": "float", "description": "正股价格"},
            {"name": "正股涨跌", "type": "float", "description": "正股涨跌(%)"},
            {"name": "正股PB", "type": "float", "description": "正股市净率"},
            {"name": "转股价", "type": "float", "description": "转股价"},
            {"name": "转股价值", "type": "float", "description": "转股价值"},
            {"name": "转股溢价率", "type": "float", "description": "转股溢价率(%)"},
            {"name": "债券评级", "type": "string", "description": "债券评级"},
            {"name": "回售触发价", "type": "float", "description": "回售触发价"},
            {"name": "强赎触发价", "type": "float", "description": "强赎触发价"},
            {"name": "转债占比", "type": "float", "description": "转债占比(%)"},
            {"name": "到期时间", "type": "string", "description": "到期时间"},
            {"name": "剩余年限", "type": "float", "description": "剩余年限"},
            {"name": "剩余规模", "type": "float", "description": "剩余规模(亿元)"},
            {"name": "成交额", "type": "float", "description": "成交额(万元)"},
            {"name": "换手率", "type": "float", "description": "换手率(%)"},
            {"name": "到期税前收益", "type": "float", "description": "到期税前收益(%)"},
            {"name": "双低", "type": "float", "description": "双低值"},
        ]
