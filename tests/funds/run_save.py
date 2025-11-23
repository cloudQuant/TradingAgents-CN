import akshare as ak
fund_etf_spot_ths_df = ak.fund_etf_spot_ths(date="20251121")
fund_etf_spot_ths_df.to_csv("fund_etf_spot_ths.csv", index=False)