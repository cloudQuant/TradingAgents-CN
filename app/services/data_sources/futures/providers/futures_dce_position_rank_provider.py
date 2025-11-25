"""
大连商品交易所持仓排名数据提供者
"""
import akshare as ak
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FuturesDcePositionRankProvider:
    """大连商品交易所持仓排名数据提供者"""
    
    def __init__(self):
        self.collection_name = "futures_dce_position_rank"
        self.display_name = "大连商品交易所持仓排名"
        self.akshare_func = "futures_dce_position_rank"
        
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取大连商品交易所持仓排名数据
        
        Args:
            date: 交易日期（必需），格式YYYYMMDD
            vars_list: 品种列表（可选），如["C", "CS"]
        """
        try:
            date = kwargs.get("date")
            vars_list = kwargs.get("vars_list")
            
            if not date:
                raise ValueError("缺少必须参数: date")
            
            logger.info(f"Fetching {self.collection_name} data, date={date}, vars_list={vars_list}")
            
            # API返回字典：{合约名: DataFrame}
            if vars_list:
                data_dict = ak.futures_dce_position_rank(date=date, vars_list=vars_list)
            else:
                data_dict = ak.futures_dce_position_rank(date=date)
            
            if not data_dict:
                logger.warning(f"No data returned for date={date}")
                return pd.DataFrame()
            
            # 合并所有DataFrame
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
        return ["查询参数_date", "symbol", "rank"]
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        """获取字段信息 - 完整版"""
        return [
            {"name": "rank", "type": "float", "description": "名次"},
            {"name": "vol_party_name", "type": "string", "description": "成交量会员简称"},
            {"name": "vol", "type": "float", "description": "成交量"},
            {"name": "vol_chg", "type": "float", "description": "成交量增减"},
            {"name": "long_party_name", "type": "string", "description": "持买单会员简称"},
            {"name": "long_open_interest", "type": "float", "description": "持买单量"},
            {"name": "long_open_interest_chg", "type": "float", "description": "持买单量增减"},
            {"name": "short_party_name", "type": "string", "description": "持卖单会员简称"},
            {"name": "short_open_interest", "type": "float", "description": "持卖单量"},
            {"name": "short_open_interest_chg", "type": "float", "description": "持卖单量增减"},
            {"name": "symbol", "type": "string", "description": "具体合约"},
            {"name": "variety", "type": "string", "description": "品种"},
        ]
