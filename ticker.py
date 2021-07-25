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

        mainInfo = {"mainInfo": data}

        return {f"{self.symbol} ticker": [priceData, mainInfo]}

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
        
        return df.to_json()


myTicker = Ticker("FB")
# print(myTicker.historicalData((2020, 1, 1), (2021, 7, 22), "month"))


