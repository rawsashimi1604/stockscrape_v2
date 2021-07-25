import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import time
import datetime
import csv

class Ticker():
    '''
        Ticker object that gets scrapped data from yfinance.
    '''

    user_agent = {'User-agent': 'Mozilla/5.0'}

    def __init__(self, symbol):
        self.symbol = symbol

    @staticmethod
    def connectUrl(url_):
        scrapURL = url_
        page = requests.get(scrapURL, headers=Ticker.user_agent)
        soup = BeautifulSoup(page.content, "html.parser")
        return soup

    def mainInfo(self):
        tickerURL = "https://finance.yahoo.com/quote/{}".format(self.symbol)
        soup = self.connectUrl(tickerURL)

        price = soup.find("div", {"class": "D(ib) Mend(20px)"}).find("span").text
        table1 = soup.find("table", {"data-reactid": "37"}).find_all("tr")
        table2 = soup.find("table", {"data-reactid": "78"}).find_all("tr")

        priceData = {"price": price}
        data = {}

        for tr in table1:
            extracted = tr.find_all("td")
            data[extracted[0].text] = extracted[1].text

        for tr in table2:
            extracted = tr.find_all("td")
            data[extracted[0].text] = extracted[1].text

        mainInfo = {"main-info": data}

        return {f"{self.symbol} ticker": [priceData, mainInfo]}

    def profileInfo(self):
        tickerURL = f"https://finance.yahoo.com/quote/{self.symbol}/profile?p={self.symbol}"
        soup = self.connectUrl(tickerURL)

        # Description
        description = soup.find("section", {"class": "quote-sub-section"}).find("p").text

        # Name
        name_ = soup.find("div", {"class": "asset-profile-container"}).find("h3").text

        # Sectors
        output = soup.find("p", {"data-reactid": "18"}).find_all("span")
        data = [x.text for x in output]
        data.pop()
        sectors = {}
        for i in range(0, len(data), 2):
            sectors[data[i]] = data[i+1]

        # Key Execs
        table_headers = soup.find("table").find_all("th")
        table_data = soup.find("table").find_all("tr")


        headers = [x.text for x in table_headers]
        key_execs = []

        for row in table_data:
            list_ = [x.get_text() for x in row]
            key_execs.append(list_)

        key_execs.pop(0)
        df = pd.DataFrame(data=key_execs, columns=headers, dtype=str)
        df.set_index("Name", inplace=True)

        # Output
        output = {
            "name": name_,
            "description": description,
            "sectors": sectors,
            "key-executives": df.to_json().replace("\\", "")
        }

        return output

    def historicalData(self, start_date, end_date, interval="day"):
        '''
            start date: (year, month, date) # tuple
            end date: (year, month, date) # tuple
            interval: "day", "week", "month"
        '''
        intervalKeywords = {
            "day": "1d",
            "week": "1wk",
            "month": "1mo"
        }

        start_ = datetime.date(*start_date)
        start_unix = int(time.mktime(start_.timetuple()))

        end_ = datetime.date(*end_date)
        end_unix = int(time.mktime(end_.timetuple()))

        try:
            downloadUrl = f"https://query1.finance.yahoo.com/v7/finance/download/{self.symbol}?period1={start_unix}&period2={end_unix}&interval={intervalKeywords[interval]}&events=history&includeAdjustedClose=true"
        
        except:
            raise KeyError("Please use one of the 3 values, 'day', 'week', 'month'.")

        with requests.Session() as s:
            download = s.get(downloadUrl, headers=Ticker.user_agent)
            decoded_content = download.content.decode('utf-8')

            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)

            data = [row for row in my_list]
            headers = data[0]
            data.pop(0)

            df = pd.DataFrame(data=data, columns=headers, dtype=str)
            df.set_index("Date", inplace=True)
        
        return {"historical-data": df.to_json()}


myTicker = Ticker("FB")
# print(myTicker.historicalData((2020, 1, 1), (2021, 7, 22), "month"))
print(myTicker.historicalData((2020, 1, 1), (2021, 1, 1)))

