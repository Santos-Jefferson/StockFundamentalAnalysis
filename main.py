import requests
from bs4 import BeautifulSoup
import json
import csv
import time
import sys
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

sys.exit()

all_financial_data = []
csv_headers = ['TYPE', 'MAKE', 'MODEL', 'TRIM', 'YEAR', 'AUTO_TRANSM', 'FUELTYPE', 'CITY', 'STATE_REG', 'OWNER_NAME',
               'ALLSTARTHOST', 'DEFAULT_AVR_DAILY_PRICE', 'AVR_DAILY_PRICE', 'RATING', 'RENTER_TRIPS', 'NUM_RENTALS',
               'DAILY_MIL', 'WEEKLY_MIL', 'MONTHLY_MIL', 'WEEKLY_DISC', 'MONTHLY_DISC', 'FREQ_BOOKED',
               'COLOR', 'CURRENT_PROT', 'DESCRIPTION', 'URL', 'ID']
for i in range(len(y['list'])):
    car_details = []
    print(i)
    vehicle_id = y['list'][i]['vehicle']['id']
    url_detail = 'https://turo.com/api/vehicle/detail?' + end_date + '&' + start_date + '&vehicleId=' + str(vehicle_id)
    page_details = requests.get(url_detail, headers=headers_details)
    y_details = json.loads(page_details.content)

    car_details.append(y['list'][i]['vehicle']['type'])
    car_details.append(y['list'][i]['vehicle']['make'])
    car_details.append(y['list'][i]['vehicle']['model'])
    car_details.append(y_details['vehicle']['trim'])
    car_details.append(y['list'][i]['vehicle']['year'])
    car_details.append(y['list'][i]['vehicle']['automaticTransmission'])
    car_details.append(y['list'][i]['fuelType'])
    car_details.append(y['list'][i]['location']['city'])
    car_details.append(y_details['vehicle']['registration']['state'])
    car_details.append(y['list'][i]['owner']['name'])
    car_details.append(y['list'][i]['owner']['allStarHost'])
    car_details.append(y_details['dateRangeRate']['defaultAverageDailyPrice'])
    car_details.append(y['list'][i]['rate']['averageDailyPrice'])
    car_details.append(y['list'][i]['rating'])
    car_details.append(y['list'][i]['renterTripsTaken'])
    car_details.append(y_details['numberOfRentals'])
    car_details.append(y_details['rate']['dailyMileage'])
    car_details.append(y_details['rate']['weeklyMileage'])
    car_details.append(y_details['rate']['monthlyMileage'])
    car_details.append(y_details['rate']['weeklyDiscountPercentage'])
    car_details.append(y_details['rate']['monthlyDiscountPercentage'])
    car_details.append(y_details['frequentlyBooked'])
    car_details.append(y_details['color'])
    car_details.append(y_details['currentVehicleProtection']['label'])
    car_details.append(y_details['description'])
    car_details.append(y['list'][i]['vehicle']['url'])
    car_details.append(y['list'][i]['vehicle']['id'])
    all_cars.append(car_details)

with open('turo_' + str(time.time()) + '.csv', "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(csv_headers)
    writer.writerows(all_cars)
