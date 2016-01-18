import requests
import json
from array import *
from Settings import PRICE_DOMAIN, ACCOUNT_DOMAIN, ACCESS_TOKEN, ACCOUNT_ID, STRT, STRO, STRH, STRL, STRC, STRV, STRCO
import httplib
import urllib
from datetime import datetime, timedelta
import time
import sys

Sec = []
Sec.append("EUR_USD")
Sec.append("GBP_USD")
Sec.append("AUD_USD")

Bars = 50
SL = 0.0006
TP = 0.0004
dt = datetime.strptime('January 18 16  08:00', '%B %d %y %H:%M')
n = 50
name = "MAC_Log.txt"

while True:

    while True:
        if datetime.now() > dt:
            file = open(name,'a')
            file.write(str(datetime.now()) + " Running script\n")
            file.close()
            break 
        time.sleep(1)

    for i in range(0,3):
        file = open(name,'a')
        file.write(str(datetime.now()) + " Getting data for " + Sec[i] + "\n")
        file.close()
        h = {'Authorization' : ACCESS_TOKEN}
        url =   "https://api-fxpractice.oanda.com/v1/candles?instrument=" + str(Sec[i]) + "&count=" + str(Bars) + "&candleFormat=midpoint&granularity=H4"
        r = requests.get(url, headers=h)     
        data = json.loads(r.text)

        def Date(index):
            return data["candles"][49 - index][STRT]
        def Open(index):
            return data["candles"][49 - index][STRO]
        def High(index):
            return data["candles"][49 - index][STRH]
        def Low(index):
            return data["candles"][49 - index][STRL]
        def Close(index):
            return data["candles"][49 - index][STRC]

        aavg = 0.0
        avg = 0.0
        sd = 0.0
        ssd = 0.0

        for j in range(0,n-1):
            aavg = Close(j) + aavg
        SMA = aavg/(n-1)

        for j in range(0,n-1):
            ssd = (Close(j) - SMA)**2 +ssd
        sd = (ssd/(n-2))**(0.5)

        Upper_Band = SMA + 2*sd
        Lower_Band = SMA - 2*sd
        file = open(name,'a')
        file.write(str(datetime.now()) + " Checking open orders...\n")
        file.close()
        h = {'Authorization' : ACCESS_TOKEN}
        url = "https://api-fxpractice.oanda.com/v1/accounts/5801231/positions"
        r = requests.get(url, headers=h)     
        data2 = json.loads(r.text)
        chk = str(data2)
        if chk.find("positions") == -1:
            Open_Units = 0 
        else:
            Open_Units = 0
            for positions in data2["positions"]:
                if positions["instrument"] == Sec[i]:
                    Open_Units = positions["units"]
        file = open(name,'a')
        file.write(str(datetime.now()) + " " + str(Open_Units) + " Units of " + str(Sec[i]) + "\n")
        file.close()
        if Close(0) > Upper_Band and Close(1) > Upper_Band and Open_Units == 0:
            file = open(name,'a')
            file.write(str(datetime.now()) + " Selling 200,000 of " + str(Sec[i]) + "\n")
            file.write(str(datetime.now()) + " Current Price is " + str(Close(0)) + "\n")
            file.write(str(datetime.now()) + " TP is " + str(round(Close(0) - TP - 0.0001,5)) + "\n")
            file.write(str(datetime.now()) + " SL is " + str(round(Close(0) + SL + 0.0001,5)) + "\n")
            file.close() 
            conn = httplib.HTTPSConnection("api-fxpractice.oanda.com")
            headers = {"Content-Type": "application/x-www-form-urlencoded","Authorization": ACCESS_TOKEN}
            params = urllib.urlencode({
                "instrument" : str(Sec[i]),
                "units" : 200000,
                "type" : "market",
                "side" : "sell",
                "takeProfit": round(Close(0) - TP,4),
                "stopLoss": round(Close(0) + SL,4)
            })
            conn.request("POST", "/v1/accounts/5801231/orders", params, headers)
            response = conn.getresponse().read()
            file = open(name,'a')
            file.write(response + "\n")
            file.close()
        elif Close(0) < Lower_Band and Close(1) < Lower_Band and Open_Units == 0:
            file = open(name,'a')
            file.write(str(datetime.now()) + " Buying 200,000 of " + str(Sec[i]) + "\n")
            file.write(str(datetime.now()) + " Current Price is " + str(Close(0)) + "\n")
            file.write(str(datetime.now()) + " TP is " + str(round(Close(0) + TP - 0.0001,5)) + "\n")
            file.write(str(datetime.now()) + " SL is " + str(round(Close(0) - SL + 0.0001,5)) + "\n")
            file.close() 
            conn = httplib.HTTPSConnection("api-fxpractice.oanda.com")
            headers = {"Content-Type": "application/x-www-form-urlencoded","Authorization": ACCESS_TOKEN}
            params = urllib.urlencode({
                "instrument" : str(Sec[i]),
                "units" : 200000,
                "type" : "market",
                "side" : "buy",
                "takeProfit": round(Close(0) + TP,4),
                "stopLoss": round(Close(0) - SL,4)
            })
            conn.request("POST", "/v1/accounts/5801231/orders", params, headers)
            response = conn.getresponse().read()
            file = open(name,'a')
            file.write(str(datetime.now()) + " " + str(response) + "\n")
            file.close()
        elif Open_Units > 0:
            file = open(name,'a')
            file.write(str(datetime.now()) + " Positions still open for " + str(Sec[i]) + "\n")
            file.close()
        else:
            file = open(name,'a')
            file.write(str(datetime.now()) + " No trades available for " + str(Sec[i]) + "\n")
            file.close()

    dt = datetime.now() + timedelta(hours=4)
    dt = dt.replace(minute=0,second=0,microsecond=1)
    file = open(name,'a')
    file.write(str(datetime.now()) + " Waiting until " + str(dt) + "\n")
    file.close()