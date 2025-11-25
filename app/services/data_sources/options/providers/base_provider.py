"""
期权数据提供者基类
所有期权数据提供者都应该继承此类
"""

import akshare as ak
from typing import Dict, Any, List, Optional
from datetime import datetime
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class BaseOptionProvider:
    """期权数据提供者基类"""
    
    # 子类需要定义的属性
    collection_name: str = ""
    display_name: str = ""
    akshare_func: str = ""  # akshare函数名
    
    # 字段信息
    field_info: Dict[str, str] = {}
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
    
    async def fetch_data(self, **kwargs) -> Dict[str, Any]:
        """
        获取数据的主方法
        子类应该重写此方法实现具体的数据获取逻辑
        
        Returns:
            Dict包含:
            - success: bool
            - data: List[Dict] 或 pd.DataFrame
            - message: str
            - field_info: Dict[str, str] (可选)
        """
        raise NotImplementedError("子类必须实现 fetch_data 方法")
    
    def _call_akshare(self, func_name: str, **kwargs) -> pd.DataFrame:
        """
        调用akshare函数的通用方法
        
        Args:
            func_name: akshare函数名
            **kwargs: 传递给akshare函数的参数
            
        Returns:
            pd.DataFrame
        """
        try:
            func = getattr(ak, func_name)
            df = func(**kwargs)
            return df
        except Exception as e:
            self.logger.error(f"调用akshare.{func_name}失败: {str(e)}")
            raise
    
    def _add_metadata(self, df: pd.DataFrame) -> pd.DataFrame:
        """添加元数据字段"""
        df = df.copy()
        df['更新时间'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df['数据来源'] = self.collection_name
        return df
    
    def _clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """清理DataFrame，处理NaN值等"""
        df = df.copy()
        # 将NaN替换为None，便于JSON序列化
        df = df.where(pd.notnull(df), None)
        return df
    
    def _df_to_records(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """将DataFrame转换为记录列表"""
        df = self._clean_dataframe(df)
        return df.to_dict('records')
    
    def get_field_info(self) -> Dict[str, str]:
        """获取字段信息"""
        return self.field_info
