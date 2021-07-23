import requests
from bs4 import BeautifulSoup
import json

user_agent = {'User-agent': 'Mozilla/5.0'}

URL = "https://finance.yahoo.com/quote/FB"
page = requests.get(URL, headers=user_agent)

soup = BeautifulSoup(page.content, "html.parser")

price = soup.find("div", {"class": "D(ib) Mend(20px)"}).find("span").text
table1 = soup.find("table", {"data-reactid": "37"}).find_all("tr")
table2 = soup.find("table", {"data-reactid": "78"}).find_all("tr")


data = {}

for tr in table1:
    extracted = tr.find_all("td")
    data[extracted[0].text] = extracted[1].text

for tr in table2:
    extracted = tr.find_all("td")
    data[extracted[0].text] = extracted[1].text

print(json.dumps({"finData": data}, indent=4))
