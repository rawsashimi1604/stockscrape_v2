import requests
import csv

user_agent = {'User-agent': 'Mozilla/5.0'}

ticker = "FB"
downloadUrl = f"https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1=1595462400&period2=1626998400&interval=1d&events=history&includeAdjustedClose=true"

with requests.Session() as s:
    download = s.get(downloadUrl, headers=user_agent)
    decoded_content = download.content.decode('utf-8')

    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    my_list = list(cr)
    for row in my_list:
        print(row)
