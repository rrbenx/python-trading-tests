#!/usr/bin/env python
# -*- coding: utf-8 -*-

import finsymbols
import json
import requests
import datetime
import time

sp500 = finsymbols.symbols.get_sp500_symbols()
print ('# Symbols : {}'.format(len(sp500))) #comprobamos su longitud, el número de valores.

symbols = [str(sp500[a]['symbol']) for a in range(len(sp500))]

start_date = "2018-01-01"
end_date = "2018-06-13"

mainURL = "https://www.alphavantage.co/query?"
#API key that will be needed to authenticate
myKey = "my-api-key"

requestTypeURL = "function=TIME_SERIES_DAILY_ADJUSTED&datatype=csv&outputsize=full"

def dailyData(symbol, requestType=requestTypeURL, apiKey=myKey):
    symbolURL = "symbol=" + str(symbol)
    apiURL = "apikey=" + myKey
    completeURL = mainURL + requestType + '&' + symbolURL + '&' + apiURL
    r = requests.get(completeURL)
    return r.text

idx = 0
for symbol in symbols:
    idx += 1
    print ("[%i / %i] Get %s symbol. output '%s.csv'" % (idx, len(symbols), symbol, symbol));
    data = dailyData(symbol)
    f = open("data/%s.csv" % symbol, "w+")
    f.write(data)
    f.close()
    time.sleep(5)
