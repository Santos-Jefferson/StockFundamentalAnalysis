import requests
import json
from pandas.io.json import json_normalize
import pandas as pd

STOCK = 'AAPL'
FREQUENCY = 'ANNUAL'
if FREQUENCY == 'ANNUAL':
    NASDAQ_API_URL = 'https://api.nasdaq.com/api/company/' + STOCK + '/financials?frequency=1'
else:
    NASDAQ_API_URL = 'https://api.nasdaq.com/api/company/' + STOCK + '/financials?frequency=2'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'referer': 'https://www.nasdaq.com/market-activity/stocks/aapl/financials'}

page = requests.get(NASDAQ_API_URL, headers=headers)
y = json.loads(page.content)
income_statement_data = y['data']['incomeStatementTable']['rows']
income_statement_headers = y['data']['incomeStatementTable']['headers']
balance_sheet_data = y['data']['balanceSheetTable']['rows']
balance_sheet_headers = y['data']['balanceSheetTable']['headers']
cash_flow_data = y['data']['cashFlowTable']['rows']
cash_flow_headers = y['data']['cashFlowTable']['headers']
financial_ratios_data = y['data']['financialRatiosTable']['rows']
financial_ratios_headers = y['data']['financialRatiosTable']['headers']

df_isd = json_normalize(income_statement_data)
df_bsd = json_normalize(balance_sheet_data)
df_cfd = json_normalize(cash_flow_data)
df_frd = json_normalize(financial_ratios_data)

df_isd.columns = [value for key, value in income_statement_headers.items()]
df_bsd.columns = [value for key, value in balance_sheet_headers.items()]
df_cfd.columns = [value for key, value in cash_flow_headers.items()]
df_frd.columns = [value for key, value in financial_ratios_headers.items()]

df_isd.set_index('Period Ending:', inplace=True)
df_bsd.set_index('Period Ending:', inplace=True)
df_cfd.set_index('Period Ending:', inplace=True)
df_frd.set_index('Period Ending:', inplace=True)

df_all = pd.concat([df_isd, df_bsd, df_cfd, df_frd])

df_all.to_csv(STOCK + '.csv')