import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

user_agent = {'User-agent': 'Mozilla/5.0'}

ticker = "FB"
URL = "https://finance.yahoo.com/quote/{}/financials?p={}".format(
    ticker, ticker)
page = requests.get(URL, headers=user_agent)

soup = BeautifulSoup(page.content, "html.parser")

table_headers = soup.find(
    "div", {"class": "D(tbr) C($primaryColor)"}).find_all("span")
table_rows = soup.find_all("div", {"data-test": "fin-row"})

# Get HEADERS
headers = [x.text.split("/")[-1] for x in table_headers]

data = []
# Populate Data
for row in table_rows:
    output = [x.text for x in row.find_all("span")]
    data.append(output)

df = pd.DataFrame(data=data, columns=headers, dtype=str)
print(df)
