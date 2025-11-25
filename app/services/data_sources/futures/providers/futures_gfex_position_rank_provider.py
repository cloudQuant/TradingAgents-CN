"""
广州期货交易所持仓排名数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FuturesGfexPositionRankProvider:
    """广州期货交易所持仓排名数据提供者"""
    
    def __init__(self):
        self.collection_name = "futures_gfex_position_rank"
        self.display_name = "广州期货交易所持仓排名"
        self.akshare_func = "futures_gfex_position_rank"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取广州期货交易所持仓排名数据
        
        Args:
            date: 交易日期（必需），格式YYYYMMDD
            vars_list: 品种列表（可选），如["SI", "LC"]
        """
        try:
            date = kwargs.get("date")
            vars_list = kwargs.get("vars_list")
            
            if not date:
                raise ValueError("缺少必须参数: date")
            
            logger.info(f"Fetching {self.collection_name} data, date={date}, vars_list={vars_list}")
            
            if vars_list:
                data_dict = ak.futures_gfex_position_rank(date=date, vars_list=vars_list)
            else:
                data_dict = ak.futures_gfex_position_rank(date=date)
            
            if not data_dict:
                logger.warning(f"No data returned for date={date}")
                return pd.DataFrame()
            
            all_dfs = []
            for symbol, df in data_dict.items():
                if df is not None and not df.empty:
                    df['symbol'] = symbol
                    all_dfs.append(df)
            
            if not all_dfs:
                return pd.DataFrame()
            
            result_df = pd.concat(all_dfs, ignore_index=True)
            result_df['更新时间'] = datetime.now()
            result_df['数据源'] = 'akshare'
            result_df['接口名称'] = self.akshare_func
            result_df['查询参数_date'] = date
            
            logger.info(f"Successfully fetched {len(result_df)} records")
            return result_df
            
        except Exception as e:
            logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
    
    def get_unique_keys(self) -> List[str]:
        """获取唯一键字段"""
        return ["查询参数_date", "symbol", "名次"]
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        """获取字段信息"""
        return [
            {"name": "symbol", "type": "string", "description": "合约代码"},
            {"name": "名次", "type": "int", "description": "排名"},
            {"name": "会员简称", "type": "string", "description": "会员简称"},
            {"name": "成交量", "type": "int", "description": "成交量"},
            {"name": "成交量增减", "type": "int", "description": "成交量增减"},
        ]
