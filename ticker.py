import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import time
import datetime
import csv

class Ticker():
    '''
        Ticker object that gets scrapped data from yahoo finance.
    '''

    user_agent = {'User-agent': 'Mozilla/5.0'}

    def __init__(self, symbol):
        self.symbol = symbol

    @staticmethod
    def connectUrl(url_):
        '''
            Connects to URL, initialize and GET soup content for scraping.
        '''
        scrapURL = url_
        page = requests.get(scrapURL, headers=Ticker.user_agent)
        soup = BeautifulSoup(page.content, "html.parser")
        return soup

    def mainInfo(self):
        '''
            Returns Ticker main information, JSON formatted.
        '''
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
        '''
            Returns Ticker profile information, JSON formatted.
        '''
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

    def statisticsInfo(self):
        '''
            Returns Ticker statistics, JSON formatted.
        '''
        tickerURL = f"https://finance.yahoo.com/quote/{self.symbol}/key-statistics?p={self.symbol}"
        soup = self.connectUrl(tickerURL)

        # Valuations ----------------------------------------------------------------------
        valueTable = soup.find("table", {"data-reactid": "13"}).find_all("td")
        valuations = []
        for row in valueTable:
            text_ = row.find("span")
            if not text_:
                text_ = row.text
                valuations.append(text_)
            else:
                text_ = text_.text
                valuations.append(text_)
        valuations_out = {}
        for i in range(0, len(valuations), 2):
            valuations_out[valuations[i]] = valuations[i+1]

        # Fiscal Year ----------------------------------------------------------------------
        fiscalTable = soup.find("table", {"data-reactid": "324"}).find_all("td")
        fiscalYear = []
        for row in fiscalTable:
            text_ = row.find("span")
            if not text_:
                text_ = row.text
                fiscalYear.append(text_)
            else:
                text_ = text_.text
                fiscalYear.append(text_)
        fiscalYear_out = {}
        for i in range(0, len(fiscalYear), 2):
            fiscalYear_out[fiscalYear[i]] = fiscalYear[i+1]

        # Profitability --------------------------------------------------------------------
        profitTable = soup.find("table", {"data-reactid": "345"}).find_all("td")
        profit = []
        for row in profitTable:
            text_ = row.find("span")
            if not text_:
                text_ = row.text
                profit.append(text_)
            else:
                text_ = text_.text
                profit.append(text_)
        profit_out = {}
        for i in range(0, len(profit), 2):
            profit_out[profit[i]] = profit[i+1]

        # Management Effectiveness --------------------------------------------------------------------
        manageTable = soup.find("table", {"data-reactid": "366"}).find_all("td")
        manage = []
        for row in manageTable:
            text_ = row.find("span")
            if not text_:
                text_ = row.text
                manage.append(text_)
            else:
                text_ = text_.text
                manage.append(text_)
        manage_out = {}
        for i in range(0, len(manage), 2):
            manage_out[manage[i]] = manage[i+1]

        # Income Statement ---------------------------------------------------------------------------
        incomeTable = soup.find("table", {"data-reactid": "387"}).find_all("td")
        income = []
        for row in incomeTable:
            text_ = row.find("span")
            if not text_:
                text_ = row.text
                income.append(text_)
            else:
                text_ = text_.text
                income.append(text_)
        income_out = {}
        for i in range(0, len(income), 2):
            income_out[income[i]] = income[i+1]

        # Balance Sheet ---------------------------------------------------------------------------
        balanceTable = soup.find("table", {"data-reactid": "450"}).find_all("td")
        balance = []
        for row in balanceTable:
            text_ = row.find("span")
            if not text_:
                text_ = row.text
                balance.append(text_)
            else:
                text_ = text_.text
                balance.append(text_)
        balance_out = {}
        for i in range(0, len(balance), 2):
            balance_out[balance[i]] = balance[i+1]

        # CashFlow Statement ---------------------------------------------------------------------------
        cashFlowTable = soup.find("table", {"data-reactid": "499"}).find_all("td")
        cashFlow = []
        for row in cashFlowTable:
            text_ = row.find("span")
            if not text_:
                text_ = row.text
                cashFlow.append(text_)
            else:
                text_ = text_.text
                cashFlow.append(text_)
        cashFlow_out = {}
        for i in range(0, len(cashFlow), 2):
            cashFlow_out[cashFlow[i]] = cashFlow[i+1]

        # CashFlow Statement ---------------------------------------------------------------------------
        stockHistoryTable = soup.find("table", {"data-reactid": "87"}).find_all("td")
        stockHistory = []
        for row in stockHistoryTable:
            text_ = row.find("span")
            if not text_:
                text_ = row.text
                stockHistory.append(text_)
            else:
                text_ = text_.text
                stockHistory.append(text_)
        stockHistory_out = {}
        for i in range(0, len(stockHistory), 2):
            stockHistory_out[stockHistory[i]] = stockHistory[i+1]

        # ShareStatistics Statement ---------------------------------------------------------------------------
        shareStatsTable = soup.find("table", {"data-reactid": "143"}).find_all("td")
        shareStats = []
        for row in shareStatsTable:
            text_ = row.find("span")
            if not text_:
                text_ = row.text
                shareStats.append(text_)
            else:
                text_ = text_.text
                shareStats.append(text_)
        shareStats_out = {}
        for i in range(0, len(shareStats), 2):
            shareStats_out[shareStats[i]] = shareStats[i+1]

        # Dividends Statement ---------------------------------------------------------------------------
        dividendsTable = soup.find("table", {"data-reactid": "234"}).find_all("td")
        dividends = []
        for row in dividendsTable:
            text_ = row.find("span")
            if not text_:
                text_ = row.text
                dividends.append(text_)
            else:
                text_ = text_.text
                dividends.append(text_)
        dividends_out = {}
        for i in range(0, len(dividends), 2):
            dividends_out[dividends[i]] = dividends[i+1]

        # Output
        stats_out = {
            "statistics": [
                {
                    "Valuations": valuations_out
                },
                {
                    "FiscalYear": fiscalYear_out
                },
                {
                    "Profitability": profit_out
                },
                {
                    "Management Effectiveness": manage_out
                },
                {
                    "Income Statement": income_out
                },
                {
                    "Balance Sheet": balance_out
                },
                {
                    "Cash Flow Statement": cashFlow_out
                },
                {
                    "Stock Price History": stockHistory_out
                },
                {
                    "Share Statistics": shareStats_out
                },
                {
                    "Dividends & Splits": dividends_out
                }
            ]
        }

        return stats_out

    def historicalData(self, start_date, end_date, interval="day"):
        '''
            Returns historical data, JSON formatted.
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
        
        return {"historical-data": [df.to_json()]}


if __name__ == "__main__":
    myTicker = Ticker("FB")
    print(myTicker.historicalData((2020, 1, 1), (2021, 7, 22), "month"))
