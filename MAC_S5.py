import requests
import json
from array import *
from Settings import PRICE_DOMAIN, ACCOUNT_DOMAIN, ACCESS_TOKEN, ACCOUNT_ID, STRT, STRO, STRH, STRL, STRC, STRV, STRCO
import httplib
import urllib
from datetime import datetime, timedelta
import time
Sec = []
Sec.append("EUR_USD")
Sec.append("GBP_USD")
Sec.append("USD_CAD")
Sec.append("AUD_USD")
Sec.append("NZD_USD")
Sec_Status = []
Sec_Status.append(False)
Sec_Status.append(False)
Sec_Status.append(False)
Sec_Status.append(False)
Sec_Status.append(False)

Bars = 50
SL = 0.0004
TP = 0.0003
last_trade = 0
Open_Units =0
Open_Trade = False
while True:
    for i in range(0,4):
        h = {'Authorization' : ACCESS_TOKEN}
        url =   "https://api-fxpractice.oanda.com/v1/candles?instrument=" + str(Sec[i]) + "&count=" + str(Bars) + "&candleFormat=bidask&granularity=S5"
        r = requests.get(url, headers=h)     
        data = json.loads(r.text)
        def CloseA(index):
            return data["candles"][49-index]["closeAsk"]
        def CloseB(index):
            return data["candles"][49-index]["closeBid"]

        n = 50
        last_i = 0
        spacer = 5
        aavg = 0.0
        avg = 0.0
        
        SMA = 0.0
        sd = 0.0
        ssd = 0.0

        for j in range(0,n):
            aavg = (CloseA(j)+CloseB(j))/2 + aavg
        SMA = aavg/n

        for j in range(0,n):
            ssd = ((CloseA(j)+CloseB(j))/2 - SMA)**2 +ssd
        sd = (ssd/(n-1))**(0.5)

        Upper_Band = SMA + sd
        Lower_Band = SMA - sd

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
        print str(Open_Units) + " Units of " + str(Sec[i])

        if CloseA(0) > Upper_Band and CloseA(1) < Upper_Band and Open_Units == 0:
            print CloseA(0)
            print "Buying 500,000 of " + str(Sec[i])
            print "Current Bid is " + str(CloseB(0)) 
            print "Current Ask is " + str(CloseA(0))   
            print "TP is " + str(round(CloseA(1) - TP+0.0001,5)) 
            print "SL is " + str(round(CloseA(1) + SL-0.0001,5))  
            conn = httplib.HTTPSConnection("api-fxpractice.oanda.com")
            headers = {"Content-Type": "application/x-www-form-urlencoded","Authorization": ACCESS_TOKEN}
            params = urllib.urlencode({
                "instrument" : str(Sec[i]),
                "units" : 200000,
                "type" : "market",
                "side" : "buy",
                "takeProfit": round(CloseA(1) + TP,4),
                "stopLoss": round(CloseA(1) - SL,4)
            })
            conn.request("POST", "/v1/accounts/5801231/orders", params, headers)
            response = conn.getresponse().read()
            print response
        elif CloseB(0) < Lower_Band and CloseB(1) > Lower_Band and Open_Units == 0:
            print "Selling 500,000 of " + str(Sec[i]) 
            print "Current Bid is " + str(CloseB(0)) 
            print "Current Ask is " + str(CloseA(0))
            print "TP is " + str(round(CloseB(1) + TP-0.0001,5)) 
            print "SL is " + str(round(CloseB(1) - SL+0.0001,5))    
            conn = httplib.HTTPSConnection("api-fxpractice.oanda.com")
            headers = {"Content-Type": "application/x-www-form-urlencoded","Authorization": ACCESS_TOKEN}
            params = urllib.urlencode({
                "instrument" : str(Sec[i]),
                "units" : 200000,
                "type" : "market",
                "side" : "sell",
                "takeProfit": round(CloseB(1) - TP,4),
                "stopLoss": round(CloseB(1) + SL,4)
            })
            conn.request("POST", "/v1/accounts/5801231/orders", params, headers)
            response = conn.getresponse().read()
            print response
        elif Open_Units > 0:
            print "Positions still open for " + str(Sec[i])  
        else:
            print "No trades available"
        time.sleep(0.75)