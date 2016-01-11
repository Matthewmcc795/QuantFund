import requests
import json
from array import *
from Settings import PRICE_DOMAIN, ACCOUNT_DOMAIN, ACCESS_TOKEN, ACCOUNT_ID, STRT, STRO, STRH, STRL, STRC, STRV, STRCO
import httplib
import urllib

Bars = 51
SL = 0.01
TP = 0.005
print "Getting data..."
h = {'Authorization' : ACCESS_TOKEN}
url =   "https://api-fxpractice.oanda.com/v1/candles?instrument=EUR_USD&count=" + str(Bars) + "&candleFormat=midpoint&granularity=H4"
r = requests.get(url, headers=h)     
data = json.loads(r.text)

def Open(index):
    return data["candles"][50 - index][STRO]
def High(index):
    return data["candles"][50 - index][STRH]
def Low(index):
    return data["candles"][50 - index][STRL]
def Close(index):
    return data["candles"][50 - index][STRC]

n = 50
last_i = 0
spacer = 5
aavg = 0.0
avg = 0.0
sd = 0.0
ssd = 0.0

for j in range(0,n):
    aavg = Close(j) + aavg
SMA = aavg/n

for j in range(0,n):
    ssd = (Close(j) - SMA)**2 +ssd
sd = (ssd/(n-1))**(0.5)

Upper_Band = SMA + 2*sd
Lower_Band = SMA - 2*sd

print "Checking open orders..."
h = {'Authorization' : ACCESS_TOKEN}
url = "https://api-fxpractice.oanda.com/v1/accounts/5801231/positions"
r = requests.get(url, headers=h)     
data2 = json.loads(r.text)

if len(data2) == 1:
    Open_Units = 0 
else:
    Open_Units = data2["positions"][0]["units"]
print Open_Units

if Close(1) < Lower_Band and Open_Units == 0:
    conn = httplib.HTTPSConnection("api-fxpractice.oanda.com")
    headers = {"Content-Type": "application/x-www-form-urlencoded","Authorization": ACCESS_TOKEN}
    params = urllib.urlencode({
        "instrument" : "EUR_USD",
        "units" : 1000,
        "type" : "market",
        "side" : "buy",
        "takeProfit": round(Close(1) + TP,4),
        "stopLoss": round(Close(1) - SL,4)
    })
    conn.request("POST", "/v1/accounts/5801231/orders", params, headers)
    response = conn.getresponse().read()
    print response
elif Close(1) > Upper_Band and Open_Units == 0:
    conn = httplib.HTTPSConnection("api-fxpractice.oanda.com")
    headers = {"Content-Type": "application/x-www-form-urlencoded","Authorization": ACCESS_TOKEN}
    params = urllib.urlencode({
        "instrument" : "EUR_USD",
        "units" : 1000,
        "type" : "market",
        "side" : "sell",
        "takeProfit": round(Close(1) - TP,4),
        "stopLoss": round(Close(1) + TP,4)
    })
    conn.request("POST", "/v1/accounts/5801231/orders", params, headers)
    response = conn.getresponse().read()
    print response
elif Open_Units > 0:
    print "Positions still open"  
else:
    print "No trades available"         