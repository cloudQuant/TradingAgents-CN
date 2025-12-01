"""
基金报告持股-巨潮数据提供者（重构版：继承BaseProvider，需要date参数）
"""
import pandas as pd
from datetime import datetime
from app.services.data_sources.base_provider import BaseProvider


class FundReportStockCninfoProvider(BaseProvider):
    """基金报告持股-巨潮数据提供者（需要日期参数）"""

    collection_description = "巨潮资讯-数据中心-专题统计-基金报表-基金重仓股（需要日期参数，格式：YYYYMMDD，如 20210630）"
    collection_route = "/funds/collections/fund_report_stock_cninfo"
    collection_order = 61

    collection_name = "fund_report_stock_cninfo"
    display_name = "基金重仓股-巨潮"
    akshare_func = "fund_report_stock_cninfo"
    unique_keys = ["股票代码", "日期"]
    
    # 参数映射：支持多种参数名
    param_mapping = {
        "date": "date",
        "quarter_date": "date",
        "qdate": "date",
    }
    required_params = ["date"]
    
    # 自定义时间戳字段名
    timestamp_field = "更新时间"
    
    field_info = [
        {"name": "序号", "type": "int", "description": "序号"},
        {"name": "股票代码", "type": "string", "description": "股票代码"},
        {"name": "股票简称", "type": "string", "description": "股票简称"},
        {"name": "报告期", "type": "string", "description": "报告期"},
        {"name": "基金覆盖家数", "type": "int", "description": "基金覆盖家数"},
        {"name": "持股总数", "type": "string", "description": "持股总数"},
        {"name": "持股总市值", "type": "string", "description": "持股总市值"},
        {"name": "日期", "type": "string", "description": "日期（从date参数中提取，格式：YYYY-MM-DD）"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_report_stock_cninfo"},
    ]
    
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取数据的主方法
        
        重写以添加"日期"字段（从date参数中提取）
        参数格式：YYYYMMDD（如 20210630）
        """
        try:
            # 1. 参数映射
            mapped_params = self._map_params(kwargs)
            
            # 2. 验证必填参数
            self._validate_params(mapped_params)
            
            # 3. 处理日期参数：将日期格式转换为YYYYMMDD格式
            date_param = mapped_params.get("date")
            date_str = None  # 保存格式化的日期字符串（YYYY-MM-DD）
            
            if date_param:
                date_str_input = str(date_param)
                # 如果输入是 YYYY-MM-DD 格式，转换为 YYYYMMDD
                if len(date_str_input) == 10 and date_str_input.count("-") == 2:
                    # YYYY-MM-DD 格式
                    date_str = date_str_input
                    mapped_params["date"] = date_str_input.replace("-", "")
                elif len(date_str_input) == 8 and date_str_input.isdigit():
                    # YYYYMMDD 格式，转换为 YYYY-MM-DD 作为日期字段
                    date_str = f"{date_str_input[:4]}-{date_str_input[4:6]}-{date_str_input[6:8]}"
                else:
                    # 尝试解析其他格式
                    try:
                        dt = datetime.strptime(date_str_input, "%Y-%m-%d")
                        date_str = date_str_input
                        mapped_params["date"] = dt.strftime("%Y%m%d")
                    except:
                        # 如果无法解析，保持原样
                        date_str = date_str_input
            
            # 4. 记录调用日志
            self.logger.info(f"Fetching {self.collection_name} data, params={mapped_params}, date_str={date_str}")
            
            # 5. 调用 akshare
            df = self._call_akshare(self.akshare_func, **mapped_params)
            
            if df is None or df.empty:
                self.logger.warning(f"No data returned for {self.collection_name}")
                return pd.DataFrame()
            
            # 6. 添加日期字段（从date参数中提取）
            if date_str:
                df["日期"] = date_str
                self.logger.debug(f"添加日期字段: {date_str}")
            else:
                # 如果无法从参数中提取，尝试从报告期字段中提取
                if "报告期" in df.columns and not df.empty:
                    # 报告期格式可能是 "2021-06-30"，直接使用
                    df["日期"] = df["报告期"].astype(str)
                else:
                    df["日期"] = ""
            
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
