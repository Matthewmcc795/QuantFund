import requests
import json
from array import *
from Settings import PRICE_DOMAIN, ACCOUNT_DOMAIN, DEMO_ACCESS_TOKEN, ACCOUNT_ID, STRT, STRO, STRH, STRL, STRC, STRV, STRCO
import httplib
import urllib
from datetime import datetime, timedelta
import time
import matplotlib.pyplot as plt
import numpy as np
import sys

Sec = []
Sec.append("EUR_USD")
Sec.append("GBP_USD")
Sec.append("USD_CAD")
Sec.append("AUD_USD")
Sec.append("NZD_USD")

i = 0
bars = 95
h = {'Authorization' : DEMO_ACCESS_TOKEN}
url =   "https://api-fxpractice.oanda.com/v1/candles?instrument=" + Sec[i] + "&count=96&candleFormat=midpoint&granularity=D"

r = requests.get(url, headers=h)     
data = json.loads(r.text)
def Date(index):
    return data["candles"][index][STRT]
def Open(index):
    return data["candles"][index][STRO]
def High(index):
    return data["candles"][index][STRH]
def Low(index):
    return data["candles"][index][STRL]
def Close(index):
    return data["candles"][index][STRC]
def Volume(index):
    return data["candles"][index][STRV]
price_Chart = []
piv = []
mgnret = 0.0001
for i in range(2,92):
    price = Close(i)
    price_Chart.append(float(price))
    if Close(i-1)/Close(i)-1 > mgnret and Close(i+1)/Close(i)-1 > mgnret:
        piv.append(Close(i))
    elif Close(i-1)/Close(i)-1 < -mgnret and Close(i+1)/Close(i)-1 < -mgnret:
        piv.append(Close(i))
    else:
        piv.append(0)

plt.plot(price_Chart)
plt.plot(piv, 'ro')
plt.ylim(1.05,1.15)
plt.show()