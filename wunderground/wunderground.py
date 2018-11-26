from datetime import date, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import pandas as pd
import  requests

boerderij = 'IDALEN3'
de_krim ='IDEKRIM2'
veenoord = 'IDRENTHE91'
schoonebeek = 'IDRENTHE68'

today = date.today().strftime('%Y%m%d')


r ='https://www.wunderground.com/personal-weather-station/dashboard?ID={}#history/tdata/s20181101/e{}/myear'.format(boerderij, today)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox') # required when running as root user. otherwise you would get no sandbox errors.
driver = webdriver.Chrome(chrome_options=chrome_options)

driver.get(r)

WebDriverWait(driver,10)

html = driver.page_source
soup = BeautifulSoup(html,'html')
table = soup.find('table', id='history_table')
for tr in table.find_all('tr', class_='column-heading'):
    tr.extract()
for tr in table.find_all('tr', class_='row-subheading'):
    tr.extract()
for span in table.find_all('span', class_='table-unit'):
    span.extract()

body = table.find('tbody')
rows = body.find_all('tr')
rows_reversed = list(reversed(rows))
start_date = date(year=2018,month=date.today().month,day=date.today().day)
data = []
for tr in rows_reversed:
    td = tr.find_all('td')

    day_data = []
    day_data.append(start_date)
    start_date = start_date - timedelta(days=1)
    for x in td:
        day_data.append(x.text)
    data.append(day_data)



df = pd.DataFrame(data)
df=df.drop(columns=[1,5,6,7,8,9,10,11,12,13,14,15,16])


print(df)