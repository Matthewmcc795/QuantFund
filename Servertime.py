import requests
import json
from array import *
from Settings import CSTokens, STRT, LIVE_ACCESS_TOKEN
import httplib
import urllib
from datetime import datetime, timedelta
import time
import sys

dt = datetime.now()
print "Now" dt

dt_PPB =  datetime.now()
dt_PPB = dt_PPB.replace(minute=2, second=0,microsecond=1)
while dt_PPB < datetime.now():
    dt_PPB += timedelta(minutes=5)
print "Current PPB", dt_PPB

dt_PPB =  datetime.now()
dt_PPB = dt_PPB.replace(minute=2, second=0,microsecond=1)
while dt_PPB < datetime.now():
    dt_PPB += timedelta(minutes=5)
dt_PPB -= timedelta(minutes=10)
print "New PPB", dt_PPB

dt_PPB =  datetime.now()
dt_PPB = dt_PPB.replace(minute=0, second=0,microsecond=1)
while dt_PPB < datetime.now():
    dt_PPB += timedelta(minutes=5)
print "New PPB 2", dt_PPB

D = []
h = {'Authorization' : LIVE_ACCESS_TOKEN}
url =   "https://api-fxtrade.oanda.com/v1/candles?instrument=EUR_USD&count=1&candleFormat=midpoint&granularity=M1"
r = requests.get(url, headers=h)     
data = json.loads(r.text)
D.append(data["candles"][0][STRT])
print "Current Candle", D[0]

