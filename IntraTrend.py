import requests
import json
from array import *
from Settings import PRICE_DOMAIN, ACCOUNT_DOMAIN, ACCESS_TOKEN, ACCOUNT_ID, STRT, STRO, STRH, STRL, STRC, STRV, STRCO
import httplib
import urllib
from datetime import datetime, timedelta
import time
import sys
import Tkinter
top = Tkinter.Tk()
# Code to add widgets will go here...
top.mainloop()
Sec = []
Sec.append("EUR_USD")
Sec.append("GBP_USD")
Sec.append("USD_CAD")
Sec.append("AUD_USD")
Sec.append("NZD_USD")
PP = [0,0,0,0,0]
R1 = [0,0,0,0,0]
R2 = [0,0,0,0,0]
S1 = [0,0,0,0,0]
S2 = [0,0,0,0,0]

Bars = 51
SL = 0.0006
TP = 0.0004
n = 50
dt = datetime.strptime('January 18 16  06:00', '%B %d %y %H:%M')
name = "IntraTend.txt"

while True:

    while True:
        if datetime.now() > dt:
            file = open(name,'a')
            file.write(str(datetime.now()) + " Running script\n")
            file.close()
            break 
        time.sleep(1)

    for i in range(0,5):

        file = open(name,'a')
        file.write(str(datetime.now()) + " Getting M5 data for " + Sec[i] + "\n")
        file.close()
        h = {'Authorization' : ACCESS_TOKEN}
        url =   "https://api-fxpractice.oanda.com/v1/candles?instrument=" + str(Sec[i]) + "&count=" + str(Bars) + "&candleFormat=midpoint&granularity=M5"
        r = requests.get(url, headers=h)     
        data = json.loads(r.text)

        def Date(index):
            return data["candles"][50 - index][STRT]
        def Open(index):
            return data["candles"][50 - index][STRO]
        def High(index):
            return data["candles"][50 - index][STRH]
        def Low(index):
            return data["candles"][50 - index][STRL]
        def Close(index):
            return data["candles"][50 - index][STRC]

        aavg = 0.0
        for j in range(0,n):
            aavg = Close(j) + aavg
        SMA50 = aavg/n

        aavg = 0.0
        for j in range(0,21):
            aavg = Close(j) + aavg
        SMA21 = aavg/21

        aavg = 0.0
        for j in range(0,10):
            aavg = Close(j) + aavg
        SMA10 = aavg/10

        if Close(0) > SMA10 and Close(0) < SMA21 and Close(0) < SMA50:
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
                "takeProfit": round(2*Close(0)-SMA50,4),
                "stopLoss": round(SMA50,4)
            })
            conn.request("POST", "/v1/accounts/5801231/orders", params, headers)
            response = conn.getresponse().read()
            file = open(name,'a')
            file.write(response + "\n")
            file.close()
        elif Close(0) < SMA10 and Close(0) > SMA21 and Close(0) > SMA50:
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
                "takeProfit": round(2*Close(0)-SMA50,4),
                "stopLoss": round(SMA50,4)
            })
            conn.request("POST", "/v1/accounts/5801231/orders", params, headers)
            response = conn.getresponse().read()
            file = open(name,'a')
            file.write(response + "\n")
            file.close()
        else:
            file = open(name,'a')
            file.write(str(datetime.now()) + " no trades\n")
            file.close() 

    dt = datetime.now() + timedelta(minutes=5)
    dt = dt.replace(second=0,microsecond=1)
    file = open(name,'a')
    file.write(str(datetime.now()) + " Waiting until " + str(dt) + "\n")
    file.close()