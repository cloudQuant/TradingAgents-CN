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
    class FundOpenFundInfoEmProvider(BaseProvider):
        collection_name = "fund_open_fund_info_em"
        display_name = "开放式基金历史行情"
        akshare_func = "fund_open_fund_info_em"
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


SYSTEM_FIELDS = {"更新时间", "更新人", "创建时间", "创建人", "来源", "scraped_at"}


class BaseProvider(ABC):
    """通用数据提供者基类"""
    
    # BaseProvider 专注于“如何从第三方拿到干净的 DataFrame”，与落库无关。
    # 典型流程：
    #   1) _map_params：将前端/服务层传入的多种参数名映射为 akshare 认可的参数；
    #   2) _validate_params：补齐必填项，提前发现调用错误；
    #   3) _call_akshare：真正的 API 请求；失败时统一记录日志；
    #   4) _add_param_columns：把关键参数写入列，便于落库时作为唯一键；
    #   5) _add_metadata：写入时间戳等元数据，帮助追踪来源。
    # 子类只需要决定 “用哪个 akshare 函数 + 唯一键 + 参数映射”，剩余流程由基类兜底。

    # ===== 子类必须定义的属性 =====
    collection_name: str = ""           # 集合名称
    display_name: str = ""              # 显示名称
    akshare_func: str = ""              # akshare函数名
    
    # ===== 子类可选定义的属性 =====
    unique_keys: List[str] = []         # 数据去重的唯一键
    field_info: List[Dict[str, Any]] = []  # 字段信息列表
    collection_description: str = ""    # 集合描述
    collection_route: Optional[str] = None
    collection_category: str = "默认"
    collection_order: int = 100
    collection_tags: List[str] = []
    collection_visible: bool = True
    
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
    timestamp_field: str = "更新时间"
    
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
            # 1. 参数映射：支持多种前端命名，例如 fund_code / code / symbol -> symbol
            mapped_params = self._map_params(kwargs)
            
            # 2. 验证必填参数，尽早抛出友好错误信息
            self._validate_params(mapped_params)
            
            # 3. 记录调用日志，方便排查 akshare 限流/字段变动等问题
            self.logger.info(f"Fetching {self.collection_name} data, params={mapped_params}")
            
            # 4. 真正调用 akshare
            df = self._call_akshare(self.akshare_func, **mapped_params)
            
            if df is None or df.empty:
                self.logger.warning(f"No data returned for {self.collection_name}")
                return pd.DataFrame()
            
            # 5. 将关键参数写回 DataFrame，确保后续写库时有唯一索引
            df = self._add_param_columns(df, mapped_params)
            
            # 6. 加入时间戳等元数据，方便排查“数据何时刷新”
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
        # 过滤掉前端特有的参数，这些参数不应该传递给 akshare
        frontend_only_params = {
            'update_type', 'update_mode', 'batch_update', 'batch_size', 
            'page', 'limit', 'skip', 'filters', 'sort', 'order',
            'task_id', 'callback', 'async', 'timeout', '_t', '_timestamp',
            'force', 'clear_first', 'overwrite', 'mode', 'concurrency'
        }
        
        # 先过滤掉前端特有参数
        filtered_kwargs = {k: v for k, v in kwargs.items() if k not in frontend_only_params}
        
        result = {}
        used_keys = set()
        
        # 先处理 param_mapping 中自定义的别名
        for frontend_key, akshare_key in self.param_mapping.items():
            if frontend_key in filtered_kwargs and filtered_kwargs[frontend_key] is not None:
                # 如果akshare_key已经有值，跳过（优先使用第一个匹配的参数）
                if akshare_key not in result:
                    result[akshare_key] = filtered_kwargs[frontend_key]
                used_keys.add(frontend_key)
        
        # 其次保留那些"本来就是 akshare 参数名"的键，避免丢失
        for key, value in filtered_kwargs.items():
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
        
        策略：
        1. 如果列不存在，直接添加参数值
        2. 如果列已存在但值为空或NaN，用参数值填充
        3. 如果列已存在且值不为空，检查是否与参数值一致，不一致时记录警告并使用参数值
        """
        df = df.copy()
        for param_name, column_name in self.add_param_columns.items():
            if param_name in params:
                param_value = params[param_name]
                if column_name not in df.columns:
                    # 列不存在，直接添加
                    df[column_name] = param_value
                else:
                    # 列已存在，检查是否需要填充或覆盖
                    # 1. 填充空值
                    mask_empty = df[column_name].isna() | (df[column_name].astype(str).str.strip() == "")
                    if mask_empty.any():
                        df.loc[mask_empty, column_name] = param_value
                        self.logger.debug(f"填充 {column_name} 列的空值，使用参数值: {param_value}")
                    
                    # 2. 检查非空值是否与参数值一致
                    mask_filled = ~mask_empty
                    if mask_filled.any():
                        inconsistent = df.loc[mask_filled, column_name] != param_value
                        if inconsistent.any():
                            inconsistent_values = df.loc[mask_filled & inconsistent, column_name].unique()[:3]
                            self.logger.warning(
                                f"{column_name} 列的值与参数不一致: "
                                f"参数值={param_value}, 数据中的值={list(inconsistent_values)}, "
                                f"将使用参数值覆盖"
                            )
                            # 使用参数值覆盖，确保数据一致性
                            df[column_name] = param_value
        return df
    
    def _add_metadata(self, df: pd.DataFrame) -> pd.DataFrame:
        """添加元数据字段（时间戳）"""
        df = df.copy()
        # timestamp_field 默认为“更新时间”，子类可覆盖为“更新日期”等别名
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

    def get_collection_route(self) -> str:
        """获取集合路由"""
        if self.collection_route:
            return self.collection_route
        return f"/funds/collections/{self.collection_name}"

    def get_collection_description(self) -> str:
        """获取集合描述"""
        if self.collection_description:
            return self.collection_description
        if self.__doc__:
            return self.__doc__.strip()
        return self.display_name or self.collection_name

    def get_display_fields(self) -> List[str]:
        """获取需要展示的字段列表（排除系统字段）"""
        display_fields = []
        for field in self.get_field_info():
            name = field.get("name")
            if name and name not in SYSTEM_FIELDS:
                display_fields.append(name)
        return display_fields

    def get_collection_meta(self) -> Dict[str, Any]:
        """获取集合元信息"""
        return {
            "name": self.collection_name,
            "display_name": self.get_display_name() or self.collection_name,
            "description": self.get_collection_description(),
            "route": self.get_collection_route(),
            "fields": self.get_display_fields(),
            "category": self.collection_category,
            "order": self.collection_order,
            "tags": self.collection_tags,
        }


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
