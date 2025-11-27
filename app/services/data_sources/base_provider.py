"""
通用数据提供者基类

所有数据提供者（funds, bonds, stocks, futures, options等）都可以继承此基类。
提供通用的数据获取、参数映射、元数据添加等功能。

使用示例：
    # 简单provider（无参数）
    class FundNameEmProvider(SimpleProvider):
        collection_name = "fund_name_em"
        display_name = "基金基本信息"
        akshare_func = "fund_name_em"
        unique_keys = ["基金代码"]
    
    # 单参数provider（需要fund_code）
    class FundFinancialFundInfoEmProvider(BaseProvider):
        collection_name = "fund_financial_fund_info_em"
        display_name = "理财型基金历史行情"
        akshare_func = "fund_financial_fund_info_em"
        unique_keys = ["基金代码", "净值日期"]
        
        # 参数映射：多个前端参数映射到一个akshare参数
        param_mapping = {
            "fund_code": "fund",
            "fund": "fund",
            "code": "fund",
        }
        required_params = ["fund"]
        
        # 自动添加参数列：将fund参数值写入"基金代码"列
        add_param_columns = {
            "fund": "基金代码",
        }
    
    # 多参数provider（需要fund_code和year）
    class FundPortfolioHoldEmProvider(BaseProvider):
        collection_name = "fund_portfolio_hold_em"
        display_name = "基金持仓股票"
        akshare_func = "fund_portfolio_hold_em"
        unique_keys = ["基金代码", "股票代码", "季度"]
        
        param_mapping = {
            "fund_code": "symbol",
            "symbol": "symbol",
            "code": "symbol",
            "year": "date",
            "date": "date",
        }
        required_params = ["symbol", "date"]
        
        add_param_columns = {
            "symbol": "基金代码",
        }
        
        # 自定义时间戳字段名
        timestamp_field = "更新时间"
"""
import akshare as ak
import pandas as pd
from abc import ABC
from typing import Dict, Any, List, Optional, Callable, Union
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BaseProvider(ABC):
    """通用数据提供者基类"""
    
    # ===== 子类必须定义的属性 =====
    collection_name: str = ""           # 集合名称
    display_name: str = ""              # 显示名称
    akshare_func: str = ""              # akshare函数名
    
    # ===== 子类可选定义的属性 =====
    unique_keys: List[str] = []         # 数据去重的唯一键
    field_info: List[Dict[str, Any]] = []  # 字段信息列表
    
    # 参数映射：将前端参数名映射到akshare参数名
    # 支持多个前端参数映射到一个akshare参数
    # 例如：{"fund_code": "fund", "fund": "fund", "code": "fund"}
    param_mapping: Dict[str, str] = {}
    
    # 必填参数列表（akshare参数名）
    required_params: List[str] = []
    
    # 额外添加到数据中的字段名（用于保留原始参数，如基金代码）
    # 例如：{"fund": "基金代码"} 表示将fund参数值写入"基金代码"列
    add_param_columns: Dict[str, str] = {}
    
    # 时间戳字段名
    timestamp_field: str = "scraped_at"
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取数据的主方法
        
        1. 映射参数名称
        2. 验证必填参数
        3. 调用 akshare 接口
        4. 添加参数列（如基金代码）
        5. 添加元数据字段
        
        子类可以重写此方法以实现自定义逻辑
        """
        try:
            # 1. 参数映射
            mapped_params = self._map_params(kwargs)
            
            # 2. 验证必填参数
            self._validate_params(mapped_params)
            
            # 3. 记录调用日志
            self.logger.info(f"Fetching {self.collection_name} data, params={mapped_params}")
            
            # 4. 调用 akshare
            df = self._call_akshare(self.akshare_func, **mapped_params)
            
            if df is None or df.empty:
                self.logger.warning(f"No data returned for {self.collection_name}")
                return pd.DataFrame()
            
            # 5. 添加参数列（如基金代码）
            df = self._add_param_columns(df, mapped_params)
            
            # 6. 添加元数据
            df = self._add_metadata(df)
            
            self.logger.info(f"Successfully fetched {len(df)} records for {self.collection_name}")
            return df
            
        except ValueError as e:
            # 参数验证错误，直接抛出
            raise
        except Exception as e:
            self.logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
    
    def _map_params(self, kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """
        将前端参数名映射到 akshare 参数名
        
        支持多个前端参数映射到一个akshare参数
        例如：fund_code/symbol/code 都映射到 symbol
        """
        result = {}
        used_keys = set()
        
        # 首先处理映射
        for frontend_key, akshare_key in self.param_mapping.items():
            if frontend_key in kwargs and kwargs[frontend_key] is not None:
                # 如果akshare_key已经有值，跳过（优先使用第一个匹配的参数）
                if akshare_key not in result:
                    result[akshare_key] = kwargs[frontend_key]
                used_keys.add(frontend_key)
        
        # 保留未映射的参数（如果参数名直接匹配akshare参数名）
        for key, value in kwargs.items():
            if key not in used_keys and value is not None:
                # 如果key不在映射表中，且不在结果中，直接使用
                if key not in result:
                    result[key] = value
        
        return result
    
    def _validate_params(self, params: Dict[str, Any]) -> None:
        """验证必填参数"""
        missing = []
        for param in self.required_params:
            if param not in params or params[param] is None:
                missing.append(param)
        
        if missing:
            raise ValueError(f"缺少必须参数: {', '.join(missing)}")
    
    def _call_akshare(self, func_name: str, **kwargs) -> pd.DataFrame:
        """
        调用 akshare 函数
        
        子类可重写此方法以自定义调用逻辑
        """
        try:
            func = getattr(ak, func_name)
            # 将参数值转换为字符串（akshare 通常需要字符串参数）
            str_kwargs = {k: str(v) if v is not None else v for k, v in kwargs.items()}
            return func(**str_kwargs)
        except AttributeError:
            raise ValueError(f"akshare 不存在函数: {func_name}")
        except Exception as e:
            self.logger.error(f"调用 akshare.{func_name} 失败: {e}")
            raise
    
    def _add_param_columns(self, df: pd.DataFrame, params: Dict[str, Any]) -> pd.DataFrame:
        """
        将参数值作为列添加到 DataFrame
        
        例如：将 symbol 参数的值写入 "基金代码" 列
        """
        df = df.copy()
        for param_name, column_name in self.add_param_columns.items():
            if param_name in params and column_name not in df.columns:
                df[column_name] = params[param_name]
        return df
    
    def _add_metadata(self, df: pd.DataFrame) -> pd.DataFrame:
        """添加元数据字段（时间戳）"""
        df = df.copy()
        df[self.timestamp_field] = datetime.now()
        return df
    
    def get_unique_keys(self) -> List[str]:
        """获取唯一键"""
        return self.unique_keys
    
    def get_field_info(self) -> List[Dict[str, Any]]:
        """获取字段信息"""
        # 如果子类定义了 field_info，使用子类的定义
        if self.field_info:
            return self.field_info
        
        # 否则返回基础字段
        return [
            {"name": self.timestamp_field, "type": "datetime", "description": "抓取时间"},
        ]
    
    def get_collection_name(self) -> str:
        """获取集合名称"""
        return self.collection_name
    
    def get_display_name(self) -> str:
        """获取显示名称"""
        return self.display_name


class SimpleProvider(BaseProvider):
    """
    简单数据提供者
    
    用于无参数或简单参数的 akshare 接口
    直接调用无需复杂的参数处理
    
    使用示例：
        class FundNameEmProvider(SimpleProvider):
            collection_name = "fund_name_em"
            display_name = "基金基本信息"
            akshare_func = "fund_name_em"
            unique_keys = ["基金代码"]
    """
    
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """简单获取数据，直接传递所有参数"""
        try:
            self.logger.info(f"Fetching {self.collection_name} data")
            
            # 直接调用akshare，传递所有参数
            df = self._call_akshare(self.akshare_func, **kwargs)
            
            if df is None or df.empty:
                self.logger.warning(f"No data returned for {self.collection_name}")
                return pd.DataFrame()
            
            # 添加元数据
            df = self._add_metadata(df)
            
            self.logger.info(f"Successfully fetched {len(df)} records")
            return df
            
        except Exception as e:
            self.logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
