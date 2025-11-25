"""
中债综合指数数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BondCompositeIndexCbondProvider:
    """中债综合指数数据提供者"""
    
    def __init__(self):
        self.collection_name = "bond_composite_index_cbond"
        self.display_name = "中债综合指数"
        
    # 指标类型选项
    INDICATOR_OPTIONS = [
        "全价", "净价", "财富", "平均市值法久期", "平均现金流法久期",
        "平均市值法凸性", "平均现金流法凸性", "平均现金流法到期收益率",
        "平均市值法到期收益率", "平均基点价值", "平均待偿期", "平均派息率",
        "指数上日总市值", "财富指数涨跌幅", "全价指数涨跌幅", "净价指数涨跌幅", "现券结算量"
    ]
    
    # 期限选项
    PERIOD_OPTIONS = [
        "总值", "1年以下", "1-3年", "3-5年", "5-7年", "7-10年", "10年以上",
        "0-3个月", "3-6个月", "6-9个月", "9-12个月", "0-6个月", "6-12个月"
    ]
    
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取中债综合指数数据
        
        Args:
            indicator: 指标类型，默认"财富"
                可选: 全价、净价、财富、平均市值法久期、平均现金流法久期等
            period: 期限，默认"总值"
                可选: 总值、1年以下、1-3年、3-5年、5-7年、7-10年、10年以上等
            
        Returns:
            DataFrame: 中债综合指数历史数据
        """
        try:
            indicator = kwargs.get("indicator", "财富")
            period = kwargs.get("period", "总值")
            
            logger.info(f"Fetching {self.collection_name} data: indicator={indicator}, period={period}")
            
            df = ak.bond_composite_index_cbond(indicator=indicator, period=period)
            
            if df is None or df.empty:
                return pd.DataFrame()
            
            df['指标类型'] = indicator
            df['期限'] = period
            df['数据源'] = 'akshare'
            df['接口名称'] = 'bond_composite_index_cbond'
            df['更新时间'] = datetime.now()
            
            logger.info(f"Successfully fetched {len(df)} records")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        """获取字段信息"""
        return [
            {"name": "date", "type": "string", "description": "日期"},
            {"name": "value", "type": "float", "description": "指数值"},
        ]
