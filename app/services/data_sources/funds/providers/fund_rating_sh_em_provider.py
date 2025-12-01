"""
基金评级-上海证券-东财数据提供者（重构版：继承BaseProvider，需要季度日期参数）
"""
import pandas as pd
from datetime import datetime
from app.services.data_sources.base_provider import BaseProvider


class FundRatingShEmProvider(BaseProvider):
    """基金评级-上海证券-东财数据提供者（需要季度日期参数）"""

    collection_description = "东方财富网-基金评级-上海证券评级（需要季度日期参数，格式：YYYY-MM-DD）"
    collection_route = "/funds/collections/fund_rating_sh_em"
    collection_order = 48

    collection_name = "fund_rating_sh_em"
    display_name = "上海证券评级-东财"
    akshare_func = "fund_rating_sh"
    unique_keys = ["代码", "日期"]
    
    # 参数映射：支持多种参数名
    param_mapping = {
        "quarter_date": "date",
        "date": "date",
        "qdate": "date",
    }
    required_params = ["date"]
    
    # 自定义时间戳字段名
    timestamp_field = "更新时间"
    
    field_info = [
        {"name": "代码", "type": "string", "description": "基金代码"},
        {"name": "简称", "type": "string", "description": "基金简称"},
        {"name": "基金经理", "type": "string", "description": "基金经理"},
        {"name": "基金公司", "type": "string", "description": "基金公司"},
        {"name": "3年期评级-3年评级", "type": "int", "description": "3年期评级"},
        {"name": "3年期评级-较上期", "type": "float", "description": "3年期评级较上期变化"},
        {"name": "5年期评级-5年评级", "type": "float", "description": "5年期评级"},
        {"name": "5年期评级-较上期", "type": "float", "description": "5年期评级较上期变化"},
        {"name": "单位净值", "type": "float", "description": "单位净值"},
        {"name": "日期", "type": "string", "description": "日期（YYYYMMDD格式）"},
        {"name": "季度日期", "type": "string", "description": "季度日期（YYYY-MM-DD格式）"},
        {"name": "日增长率", "type": "float", "description": "日增长率（%）"},
        {"name": "近1年涨幅", "type": "float", "description": "近1年涨幅（%）"},
        {"name": "近3年涨幅", "type": "float", "description": "近3年涨幅（%）"},
        {"name": "近5年涨幅", "type": "float", "description": "近5年涨幅（%）"},
        {"name": "手续费", "type": "string", "description": "手续费"},
        {"name": "类型", "type": "string", "description": "基金类型"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_rating_sh_em"},
    ]
    
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取数据的主方法
        
        重写以添加"季度日期"字段（从date参数中提取）
        参数可以是季度日期格式（YYYY-MM-DD）或YYYYMMDD格式
        """
        try:
            # 1. 参数映射
            mapped_params = self._map_params(kwargs)
            
            # 2. 验证必填参数
            self._validate_params(mapped_params)
            
            # 3. 处理日期参数：将季度日期格式转换为YYYYMMDD格式
            date_param = mapped_params.get("date")
            quarter_date = None  # 保存原始季度日期
            
            if date_param:
                date_str = str(date_param)
                # 如果输入是 YYYY-MM-DD 格式，转换为 YYYYMMDD
                if len(date_str) == 10 and date_str.count("-") == 2:
                    # YYYY-MM-DD 格式
                    quarter_date = date_str
                    mapped_params["date"] = date_str.replace("-", "")
                elif len(date_str) == 8 and date_str.isdigit():
                    # YYYYMMDD 格式，转换为 YYYY-MM-DD 作为季度日期
                    quarter_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
                else:
                    # 尝试解析其他格式
                    try:
                        dt = datetime.strptime(date_str, "%Y-%m-%d")
                        quarter_date = date_str
                        mapped_params["date"] = dt.strftime("%Y%m%d")
                    except:
                        # 如果无法解析，保持原样
                        quarter_date = date_str
            
            # 4. 记录调用日志
            self.logger.info(f"Fetching {self.collection_name} data, params={mapped_params}, quarter_date={quarter_date}")
            
            # 5. 调用 akshare，处理 akshare 内部抛出非标准异常的情况
            try:
                df = self._call_akshare(self.akshare_func, **mapped_params)
            except Exception as call_error:
                error_msg = str(call_error)
                if "exceptions must derive from BaseException" in error_msg:
                    self.logger.warning(
                        "akshare.fund_rating_sh(%s) 返回异常信息: %s，视为无数据",
                        mapped_params,
                        error_msg,
                    )
                    return pd.DataFrame()
                raise
            
            if df is None or df.empty:
                self.logger.warning(f"No data returned for {self.collection_name}")
                return pd.DataFrame()
            
            # 6. 添加季度日期字段
            if quarter_date:
                df["季度日期"] = quarter_date
                self.logger.debug(f"添加季度日期字段: {quarter_date}")
            else:
                # 如果无法从参数中提取，尝试从日期字段中提取
                if "日期" in df.columns and not df.empty:
                    df["季度日期"] = df["日期"].apply(
                        lambda d: f"{str(d)[:4]}-{str(d)[4:6]}-{str(d)[6:8]}" 
                        if len(str(d)) == 8 and str(d).isdigit() 
                        else str(d)
                    )
                else:
                    df["季度日期"] = ""
            
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
