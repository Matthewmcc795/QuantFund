import requests
import json
from Settings import PRICE_DOMAIN, ACCOUNT_DOMAIN, ACCESS_TOKEN, ACCOUNT_ID, STRT, STRO, STRH, STRL, STRC, STRV, STRCO
import httplib
import urllib
from datetime import datetime, timedelta
import time

h = {'Authorization' : ACCESS_TOKEN}
url =   "https://api-fxpractice.oanda.com/v1/candles?instrument=EUR_USD&count=1&candleFormat=midpoint&granularity=S5"
r = requests.get(url, headers=h)     
data = json.loads(r.text)
print data["candles"][0][STRT]
print str(datetime.now())
dt = datetime.strptime('January 25 16 11:30', '%B %d %y %H:%M')
print dt
dt = datetime.now() + timedelta(minutes=4)
print dt
dt = dt.replace(second=30,microsecond=1)
print dt