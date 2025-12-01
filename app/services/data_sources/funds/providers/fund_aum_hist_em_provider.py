"""
基金规模历史-东财数据提供者（重构版：继承BaseProvider，需要年份参数）
"""
import pandas as pd
from app.services.data_sources.base_provider import BaseProvider


class FundAumHistEmProvider(BaseProvider):
    """基金规模历史-东财数据提供者（需要年份参数）"""

    collection_description = "东方财富网-基金数据-基金公司历年管理规模（需要年份参数，从2001年开始）"
    collection_route = "/funds/collections/fund_aum_hist_em"
    collection_order = 58

    collection_name = "fund_aum_hist_em"
    display_name = "基金公司历年管理规模-东财"
    akshare_func = "fund_aum_hist_em"
    unique_keys = ["基金公司", "年份"]
    
    # 参数映射：支持多种参数名
    param_mapping = {
        "year": "year",
        "date": "year",
    }
    required_params = ["year"]
    
    # 自定义时间戳字段名
    timestamp_field = "更新时间"
    
    field_info = [
        {"name": "序号", "type": "int", "description": "序号"},
        {"name": "基金公司", "type": "string", "description": "基金公司名称"},
        {"name": "总规模", "type": "float", "description": "总规模"},
        {"name": "股票型", "type": "float", "description": "股票型基金规模"},
        {"name": "混合型", "type": "float", "description": "混合型基金规模"},
        {"name": "债券型", "type": "float", "description": "债券型基金规模"},
        {"name": "指数型", "type": "float", "description": "指数型基金规模"},
        {"name": "QDII", "type": "float", "description": "QDII基金规模"},
        {"name": "货币型", "type": "float", "description": "货币型基金规模"},
        {"name": "年份", "type": "string", "description": "年份（从year参数中提取）"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_aum_hist_em"},
    ]
    
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取数据的主方法
        
        重写以添加"年份"字段（从year参数中提取）
        """
        try:
            # 1. 参数映射
            mapped_params = self._map_params(kwargs)
            
            # 2. 验证必填参数
            self._validate_params(mapped_params)
            
            # 3. 记录调用日志
            year_param = mapped_params.get("year")
            self.logger.info(f"Fetching {self.collection_name} data, params={mapped_params}")
            
            # 4. 调用 akshare
            df = self._call_akshare(self.akshare_func, **mapped_params)
            
            if df is None or df.empty:
                self.logger.warning(f"No data returned for {self.collection_name}")
                return pd.DataFrame()
            
            # 5. 添加年份字段（从year参数中提取）
            if year_param:
                # 确保年份是字符串格式
                year = str(year_param)
                # 如果年份长度大于4，只取前4位
                if len(year) > 4:
                    year = year[:4]
                df["年份"] = year
                self.logger.debug(f"添加年份字段: {year}")
            else:
                df["年份"] = ""
            
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
