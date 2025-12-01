"""
基金持仓债券-东财数据提供者（重构版：继承BaseProvider）
"""
import pandas as pd
from app.services.data_sources.base_provider import BaseProvider


class FundPortfolioBondHoldEmProvider(BaseProvider):
    """基金持仓债券-东财数据提供者"""

    collection_description = "东方财富网-数据中心-债券持仓（需要基金代码和日期，支持单个/批量更新）"
    collection_route = "/funds/collections/fund_portfolio_bond_hold_em"
    collection_order = 44

    collection_name = "fund_portfolio_bond_hold_em"
    display_name = "债券持仓-东财"
    akshare_func = "fund_portfolio_bond_hold_em"
    unique_keys = ["基金代码", "债券代码", "季度"]
    
    # 参数映射：多个前端参数映射到akshare参数
    param_mapping = {
        "fund_code": "symbol",
        "symbol": "symbol",
        "code": "symbol",
        "year": "date",
        "date": "date",
    }
    required_params = ["symbol", "date"]
    
    # 自动添加基金代码字段
    add_param_columns = {
        "symbol": "基金代码",
    }
    
    # 自定义时间戳字段名
    timestamp_field = "更新时间"
    
    field_info = [
        {"name": "基金代码", "type": "string", "description": "基金代码"},
        {"name": "债券代码", "type": "string", "description": "债券代码"},
        {"name": "债券名称", "type": "string", "description": "债券名称"},
        {"name": "占净值比例", "type": "float", "description": "持仓占比"},
        {"name": "持仓数", "type": "int", "description": "持仓数量"},
        {"name": "持仓市值", "type": "float", "description": "持仓市值"},
        {"name": "季度", "type": "string", "description": "季度"},
        {"name": "年份", "type": "string", "description": "年份（从date参数中提取）"},
        {"name": "更新时间", "type": "datetime", "description": "更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_portfolio_bond_hold_em"},
    ]
    
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取数据的主方法
        
        重写以添加"年份"字段（从date参数中提取）
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
            
            # 6. 添加年份字段（从date参数中提取）
            date_param = mapped_params.get("date")
            if date_param:
                # 从date参数中提取年份（支持多种格式：2024, "2024", "2024-01-01"等）
                year = str(date_param)
                if len(year) >= 4 and year[:4].isdigit():
                    year = year[:4]
                else:
                    # 如果无法提取，尝试从季度字段中提取
                    if "季度" in df.columns and not df.empty:
                        # 从第一条记录的季度字段中提取年份
                        first_quarter = str(df.iloc[0]["季度"]) if not df.empty else ""
                        if len(first_quarter) >= 4 and first_quarter[:4].isdigit():
                            year = first_quarter[:4]
                        else:
                            year = ""
                    else:
                        year = ""
                
                df["年份"] = year
                self.logger.debug(f"添加年份字段: {year}")
            else:
                # 如果没有date参数，尝试从季度字段中提取
                if "季度" in df.columns and not df.empty:
                    # 从季度字段中提取年份
                    df["年份"] = df["季度"].apply(
                        lambda q: str(q)[:4] if len(str(q)) >= 4 and str(q)[:4].isdigit() else ""
                    )
                else:
                    df["年份"] = ""
            
            # 7. 添加元数据
            df = self._add_metadata(df)
            
            self.logger.info(f"Successfully fetched {len(df)} records for {self.collection_name}")
            return df
            
        except ValueError as e:
            # 参数验证错误，直接抛出
            raise
        except Exception as e:
            self.logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
