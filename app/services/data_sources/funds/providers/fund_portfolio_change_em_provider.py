"""
基金持仓变动-东财数据提供者（重构版：继承BaseProvider）
"""
from app.services.data_sources.base_provider import BaseProvider
import pandas as pd


class FundPortfolioChangeEmProvider(BaseProvider):
    """基金持仓变动-东财数据提供者"""
    
    collection_name = "fund_portfolio_change_em"
    display_name = "重大变动-东财"
    akshare_func = "fund_portfolio_change_em"
    unique_keys = ["基金代码", "指标", "季度", "股票代码"]
    
    # 参数映射：多个前端参数映射到akshare参数
    param_mapping = {
        "fund_code": "symbol",
        "symbol": "symbol",
        "code": "symbol",
        "year": "date",
        "date": "date",
        "indicator": "indicator",
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
        {"name": "股票代码", "type": "string", "description": "股票代码"},
        {"name": "股票名称", "type": "string", "description": "股票名称"},
        {"name": "持仓变动", "type": "string", "description": "持仓变动类型"},
        {"name": "变动数量", "type": "float", "description": "变动数量"},
        {"name": "变动市值", "type": "float", "description": "变动市值"},
        {"name": "季度", "type": "string", "description": "季度"},
        {"name": "指标", "type": "string", "description": "指标类型（累计买入/累计卖出）"},
        {"name": "年份", "type": "string", "description": "年份（从date参数中提取）"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_portfolio_change_em"},
    ]
    
    collection_description = "东方财富网-数据中心-重大变动（需要基金代码和年份，支持单个/批量更新）"
    collection_route = "/funds/collections/fund_portfolio_change_em"
    collection_order = 46

    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取基金持仓变动数据
        
        重写以支持indicator默认值和添加指标、年份字段
        """
        try:
            # 设置indicator默认值
            if "indicator" not in kwargs:
                kwargs["indicator"] = "累计买入"
            
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
            
            # 6. 添加指标字段（从indicator参数中获取）
            indicator_param = mapped_params.get("indicator", "累计买入")
            df["指标"] = indicator_param
            self.logger.debug(f"添加指标字段: {indicator_param}")
            
            # 7. 添加年份字段（从date参数中提取）
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
            
            # 8. 添加元数据
            df = self._add_metadata(df)
            
            self.logger.info(f"Successfully fetched {len(df)} records for {self.collection_name}")
            return df
            
        except ValueError as e:
            # 参数验证错误，直接抛出
            raise
        except Exception as e:
            self.logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
