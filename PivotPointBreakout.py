import requests
import json
from array import *
from Settings import PRICE_DOMAIN, ACCOUNT_DOMAIN, LIVE_ACCESS_TOKEN, ACCOUNT_ID, STRT, STRO, STRH, STRL, STRC, STRV, STRCO
import httplib
import urllib
from datetime import datetime, timedelta
import time
import sys

Sec = ["EUR_USD", "GBP_USD", "USD_CAD", "AUD_USD", "NZD_USD"]
PP = [0,0,0,0,0]
R1 = [0,0,0,0,0]
S1 = [0,0,0,0,0]
lst_ATR = [0,0,0,0,0]
lst_price = [0,0,0,0,0]
lst_SL = [0,0,0,0,0]
dt = datetime.strptime('March 1 16  6:02', '%B %d %y %H:%M')
name = "PPBreakout_Log2.txt"
first_run = True

def OpenOrder(Account_Num, instrument, units, order_type, order_side, Take_Profit, Stop_Loss):
    conn = httplib.HTTPSConnection("api-fxtrade.oanda.com")
    headers = {"Content-Type": "application/x-www-form-urlencoded","Authorization": LIVE_ACCESS_TOKEN}
    params = urllib.urlencode({
        "instrument" : str(instrument),
        "units" : units,
        "type" : order_type,
        "side" : order_side,
        "takeProfit": Take_Profit,
        "stopLoss": Stop_Loss
    })
    conn.request("POST", "/v1/accounts/" + str(Account_Num) + "/orders", params, headers)
    response = conn.getresponse().read()
    file = open(name,'a')
    file.write(response + "\n")
    file.close()

def UpdateStopLoss(Account_Num, trade_ID, Stop_Loss):
    conn = httplib.HTTPSConnection("api-fxtrade.oanda.com")
    headers = {"Content-Type": "application/x-www-form-urlencoded","Authorization": LIVE_ACCESS_TOKEN}
    params = urllib.urlencode({"stopLoss": Stop_Loss})
    conn.request("PATCH", "/v1/accounts/" + str(Account_Num) + "/trades/" + str(trade_ID), params, headers)
    response = conn.getresponse().read()
    file = open(name,'a')
    file.write(response + "\n")
    file.close()

while True:
    while True:
        if datetime.now() > dt:
            lst_dt = dt
            break 
        time.sleep(1)

    if first_run or dt.hour == 22:
        for i in range(0,5):
            h = {'Authorization' : LIVE_ACCESS_TOKEN}
            url =   "https://api-fxtrade.oanda.com/v1/candles?instrument=" + Sec[i] + "&count=2&candleFormat=midpoint&granularity=D"
            r = requests.get(url, headers=h)     
            data = json.loads(r.text)
            def Date(index):
                return data["candles"][1-index][STRT]
            def Open(index):
                return data["candles"][1-index][STRO]
            def High(index):
                return data["candles"][1-index][STRH]
            def Low(index):
                return data["candles"][1-index][STRL]
            def Close(index):
                return data["candles"][1-index][STRC]
            PP[i] = (High(1) + Low(1) + Close(1))/3
            S1[i] = 2*PP[i] - High(1)
            R1[i] = 2*PP[i] - Low(1)
            first_run = False
            time.sleep(2)

    for i in range(0,5):
        h = {'Authorization' : LIVE_ACCESS_TOKEN}
        url = "https://api-fxtrade.oanda.com/v1/accounts/229783/positions"
        r = requests.get(url, headers=h)     
        data2 = json.loads(r.text)
        chk = str(data2)
        if chk.find("instrument") == -1:
            Open_Units = 0 
        else:
            Open_Units = 0
            for positions in data2["positions"]:
                if positions["instrument"] == Sec[i]:
                    Open_Units = positions["units"]
        h = {'Authorization' : LIVE_ACCESS_TOKEN}
        url =   "https://api-fxtrade.oanda.com/v1/candles?instrument=" + Sec[i] + "&count=100&candleFormat=midpoint&granularity=M15"
        r = requests.get(url, headers=h)     
        data = json.loads(r.text)
        def MHigh(index):
            return data["candles"][99 - index][STRH]
        def MLow(index):
            return data["candles"][99 - index][STRL]
        def MClose(index):
            return data["candles"][99 - index][STRC]

        def TR(h,l,yc):
            x = h-l
            y = abs(h-yc)
            z = abs(l-yc)
            if y <= x >= z:
                TR = x
            elif x <= y >= z:
                TR = y
            elif x <= z >= y:
                TR = z
            return TR

        def ATR(index):
            p = 98
            TrueRanges = 0.0
            ATR_val = 0
            while p > 84:
                TrueRanges = TrueRanges + TR(MHigh(p),MLow(p),MClose(p+1))
                p -= 1
            ATR_val = TrueRanges/14
            while p >= 0:
                ATR_val = (ATR_val*13 + TR(MHigh(p),MLow(p),MClose(p+1)))/14
                p -= 1
            return ATR_val
        time.sleep(2)
        
        h = {'Authorization' : LIVE_ACCESS_TOKEN}
        url =   "https://api-fxtrade.oanda.com/v1/candles?instrument=" + Sec[i] + "&count=3&candleFormat=midpoint&granularity=M5"
        r = requests.get(url, headers=h)     
        data2 = json.loads(r.text)
        def M5Open(index):
            return data2["candles"][2 - index][STRO]
        def M5Close(index):
            return data2["candles"][2 - index][STRC]

        if Open_Units == 0 or (dt.hour <= 18 and dt.hour >= 8):
            if M5Close(0) < R1[i] and M5Close(1) < R1[i] and M5Close(2) > R1[i]:
                SL = round(M5Close(0) + ATR(0) + 0.00001,5)
                TP = round(M5Close(0) - ATR(0)*3 - 0.00001,5)
                OpenOrder(229783, Sec[i], 100, "market", "sell", TP, SL)
                lst_SL[i] = M5Close(0) + ATR(0) + 0.00001
            elif M5Close(0) > S1[i] and M5Close(1) > S1[i] and M5Close(2) < S1[i]:
                SL = round(M5Close(0) - ATR(0) - 0.00001,5)
                TP = round(M5Close(0) + ATR(0)*3 + 0.00001,5)
                OpenOrder(229783, Sec[i], 100, "market", "buy", TP, SL)
                lst_SL[i] = M5Close(0) - ATR(0) - 0.00001
        lst_ATR[i] = ATR(0)
        lst_price[i] = M5Close(0)
        time.sleep(2)

    for i in range(0,5):
        h = {'Authorization' : LIVE_ACCESS_TOKEN}
        url = "https://api-fxtrade.oanda.com/v1/accounts/229783/trades?instrument=" + str(Sec[i])
        r = requests.get(url, headers=h)     
        data2 = json.loads(r.text)
        if chk.find("id") != -1:
            for positions in data2["trades"]:
                trd_ID = positions["id"]
                trd_entry = positions["price"]
                trd_side = positions["side"]
                if trd_side == "buy":
                    if lst_price[i] > float(trd_entry) + lst_ATR[i]/2:
                        SL = trd_entry + 0.0001
                        UpdateStopLoss(229783, trd_ID, SL)
                        lst_SL[i] = SL                   
                    elif lst_price[i] > float(trd_entry) + lst_ATR[i]:
                        SL = max(lst_SL, lst_price[i] - lst_ATR[i])
                        UpdateStopLoss(229783, trd_ID, SL)
                        lst_SL[i] = SL
                elif trd_side == "sell":
                    if lst_price[i] < float(trd_entry) - lst_ATR[i]/2:
                        SL = trd_entry - 0.0001
                        UpdateStopLoss(229783, trd_ID, SL)
                        lst_SL[i] = SL
                    elif lst_price[i] < float(trd_entry) - lst_ATR[i]:
                        SL = min(lst_SL, lst_price[i] + lst_ATR[i])
                        UpdateStopLoss(229783, trd_ID, SL)
                        lst_SL[i] = SL
    
    dt = lst_dt + timedelta(minutes=5)
    dt = dt.replace(second=0,microsecond=1)
    file = open(name,'a')
    file.write(str(datetime.now()) + " Waiting until " + str(dt) + "\n")
    file.close()