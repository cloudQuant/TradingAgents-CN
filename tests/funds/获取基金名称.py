import akshare as ak
df = ak.fund_name_em()
df.to_csv('fund_name_em.csv', index=False)