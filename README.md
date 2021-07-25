# StockScrape
## _YahooFinance data scraper_

Stockscrape is a webscraper that scrapes Yahoo Finance for financial data. :sparkles: It returns it in a JSON format, execellent for integration into REST APIs.

## Features
- Scrape financial data from [Yahoo Finance](https://finance.yahoo.com/)!
- Download historical quote data using specific timeframes
- Up to 2000 data calls per hour.
- Data exported in JSON format.

## Requirements
Stockscrape uses a number of python packages to work properly.
- [Requests](https://docs.python-requests.org/en/master/) - GET data from Yahoo Finance.
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - Parse and locates data for output
- [pandas](https://pandas.pydata.org/) - Data / table tools

## Installation
Stockscrape requires Python 3+ to run.

Install the module using pip. Simply input this command in your terminal.
```
pip install stockscrape
```

## Example Usage
To get data using stockscrape, firstly import the required module.
```python
import stockscrape
```

Then use the intialize a ticker object.
```python
myTicker = stockscrape.Ticker("FB") # Insert your ticker symbol here.
```

Getting historical data...
```python
data = myTicker.historicalData((2020, 1, 1), (2021, 7, 22), "day")
# output >>> JSON formatted historical data for Facebook stock, from dates 01/01/2020 to 01/01/2021 in daily intervals.
```

Getting stock information...
```python
myTicker.mainInfo() # Returns general stock information such as price, P/E ratios, market capitalization etc.
myTicker.profileInfo() # Returns stock corporate information such as CEOs, description etc.
myTicker.statisticsInfo() # Returns stock statistics.
```

To get in a python dictionary use json, json_loads
```python
import json
json.loads(myTicker.mainInfo()) # Converts json to dictionary.
```

## License
MIT
