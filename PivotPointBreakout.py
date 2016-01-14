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
PP = [0,0,0]
R1 = [0,0,0]
R2 = [0,0,0]
S1 = [0,0,0]
S2 = [0,0,0]

Bars = 51
SL = 0.0006
TP = 0.0004
n = 50
dt = datetime.strptime('January 13 16  22:15', '%B %d %y %H:%M')
name = "PPBreakout.txt"
LowerPP = 0
UpperPP = 0
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
        file.write(str(datetime.now()) + " Getting Daily data for " + Sec[i] + "\n")
        file.close()
        h = {'Authorization' : ACCESS_TOKEN}
        url =   "https://api-fxpractice.oanda.com/v1/candles?instrument=" + Sec[i] + "&count=2&candleFormat=midpoint&granularity=D"
        r = requests.get(url, headers=h)     
        data = json.loads(r.text)
        def Date(index):
            return data["candles"][2 - index][STRT]
        def Open(index):
            return data["candles"][2 - index][STRO]
        def High(index):
            return data["candles"][2 - index][STRH]
        def Low(index):
            return data["candles"][2 - index][STRL]
        def Close(index):
            return data["candles"][2 - index][STRC]

        PP[i] = (High(1) + Low(1) + Close(1))/3
        S1[i] = 2*PP[i] - High(1)
        S2[i] = PP[i] - High(1) + Low(1)
        R1[i] = 2*PP[i] - Low(1)
        R2[i] = PP[i] + High(1) - Low(1)

    for i in range(0,3):
        file = open(name,'a')
        file.write(str(datetime.now()) + " Getting M15 data for " + Sec[i] + "\n")
        file.close()
        h = {'Authorization' : ACCESS_TOKEN}
        url =   "https://api-fxpractice.oanda.com/v1/candles?instrument=" + Sec[i] + "&count=2&candleFormat=bidask&granularity=M15"
        r = requests.get(url, headers=h)     
        data = json.loads(r.text)

        def CloseA(index):
            return data["candles"][index]["closeAsk"]
        def CloseB(index):
            return data["candles"][index]["closeBid"]

        if CloseB(1) > R2:
            UpperPP = Close(i)*2
            LowerPP = R2[i]
        elif CloseB(1) > R1[i] and CloseB(1) < R2[i]:
            UpperPP = R2[i]
            LowerPP = R1[i]
        elif CloseB(1) > PP and CloseB(1) < R1[i]:
            UpperPP = R1[i]
            LowerPP = PP[i]
        elif CloseB(1) > S1[i] and CloseB(1) < PP[i]:
            UpperPP = PP[i]
            LowerPP = S1[i]
        elif CloseB(1) > S2[i] and CloseB(1) < S1[i]:  
            UpperPP = S1[i]
            LowerPP = S2[i]
        elif CloseB(1) < S2[i]:
            UpperPP = S2[i]
            LowerPP = Close(i)/2

        if CloseB(0) < LowerPP and Close(1) > LowerPP:
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
        elif CloseB(0) > UpperPP and Close(1) < UpperPP:
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
            file.write(response + "\n")
            file.close()
        else:
            file = open(name,'a')
            file.write(str(datetime.now()) + " no trades\n")
            file.close() 

    dt = datetime.now() + timedelta(minutes=15)
    dt = dt.replace(second=1,microsecond=0)
    file = open(name,'a')
    file.write(str(datetime.now()) + " Waiting until " + str(dt) + "\n")
    file.close()