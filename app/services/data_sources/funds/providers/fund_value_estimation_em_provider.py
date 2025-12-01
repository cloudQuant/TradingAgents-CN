"""
基金净值估算-东财数据提供者（重构版：继承SimpleProvider，需要特殊处理列名和交易日）
"""
import pandas as pd
import re
from app.services.data_sources.base_provider import SimpleProvider


class FundValueEstimationEmProvider(SimpleProvider):
    """基金净值估算-东财数据提供者"""
    
    collection_description = "东方财富网-数据中心-净值估算（无参数接口，默认获取全部数据）"
    collection_route = "/funds/collections/fund_value_estimation_em"
    collection_order = 36

    collection_name = "fund_value_estimation_em"
    display_name = "净值估算-东财"
    akshare_func = "fund_value_estimation_em"
    unique_keys = ["基金代码", "交易日"]

    field_info = [
        {"name": "序号", "type": "string", "description": ""},
        {"name": "基金代码", "type": "string", "description": ""},
        {"name": "基金名称", "type": "string", "description": ""},
        {"name": "估算数据-估算值", "type": "string", "description": ""},
        {"name": "估算数据-估算增长率", "type": "string", "description": ""},
        {"name": "公布数据-单位净值", "type": "string", "description": ""},
        {"name": "公布数据-日增长率", "type": "string", "description": ""},
        {"name": "估算偏差", "type": "string", "description": ""},
        {"name": "单位净值", "type": "string", "description": ""},
        {"name": "交易日", "type": "string", "description": "交易日（从列名中提取）"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_value_estimation_em"},
    ]
    
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """
        获取数据的主方法
        
        特殊处理：
        1. 调用 akshare 接口时不传递参数（默认获取全部数据）
        2. 处理列名：去掉"交易日-"前缀
        3. 从列名中提取交易日（格式：YYYY-MM-DD）
        4. 添加"交易日"列，放到"单位净值"后面
        """
        try:
            # 1. 调用 akshare（不传递任何参数，默认获取全部数据）
            df = self._call_akshare(self.akshare_func)
            
            if df is None or df.empty:
                self.logger.warning(f"No data returned for {self.collection_name}")
                return pd.DataFrame()
            
            # 2. 处理列名：提取交易日并去掉日期前缀
            trading_date = None
            new_columns = {}
            
            for col in df.columns:
                # 检查列名是否包含日期格式（YYYY-MM-DD）
                date_match = re.search(r'(\d{4}-\d{2}-\d{2})', col)
                if date_match:
                    # 提取交易日（只取第一个匹配的日期）
                    if trading_date is None:
                        trading_date = date_match.group(1)
                    
                    # 去掉日期部分，保留列名
                    # 例如："交易日-估算数据-估算值" -> "估算数据-估算值"
                    # 或者："2021-02-18-单位净值" -> "单位净值"
                    # 或者："交易日-单位净值" -> "单位净值"
                    new_col = re.sub(r'交易日-', '', col)
                    new_col = re.sub(r'\d{4}-\d{2}-\d{2}-', '', new_col)
                    new_col = new_col.strip()
                    
                    # 如果处理后的列名为空，保持原列名
                    if not new_col:
                        new_col = col
                    
                    new_columns[col] = new_col
                else:
                    # 检查是否有"交易日-"前缀（但没有日期格式）
                    if col.startswith("交易日-"):
                        new_col = col.replace("交易日-", "", 1).strip()
                        if not new_col:
                            new_col = col
                        new_columns[col] = new_col
                    else:
                        # 没有日期前缀的列保持不变
                        new_columns[col] = col
            
            # 重命名列
            df = df.rename(columns=new_columns)
            
            # 3. 添加"交易日"列（放到"单位净值"后面）
            if trading_date:
                # 找到"单位净值"列的位置
                if "单位净值" in df.columns:
                    unit_net_value_idx = df.columns.get_loc("单位净值")
                    # 在"单位净值"后面插入"交易日"列
                    df.insert(unit_net_value_idx + 1, "交易日", trading_date)
                else:
                    # 如果"单位净值"列不存在，直接添加到末尾
                    df["交易日"] = trading_date
            else:
                # 如果没有找到交易日，使用空字符串
                if "单位净值" in df.columns:
                    unit_net_value_idx = df.columns.get_loc("单位净值")
                    df.insert(unit_net_value_idx + 1, "交易日", "")
                else:
                    df["交易日"] = ""
            
            # 4. 添加元数据
            df = self._add_metadata(df)
            
            self.logger.info(f"Successfully fetched {len(df)} records for {self.collection_name}, trading_date: {trading_date}")
            return df
            
        except Exception as e:
            self.logger.error(f"Error fetching {self.collection_name} data: {e}")
            raise
