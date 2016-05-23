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
Account_Num = 836663

dt =  datetime.now()
dt = dt.replace(minute=2, second=0,microsecond=1)
while dt.hour != 21
    dt += timedelta(hours=1)
name = "BusRide_Log.txt" 

def OpenOrder(Account_Num, instrument, units, order_type, order_side, Take_Profit, Stop_Loss):
    conn = httplib.HTTPSConnection("api-fxtrade.oanda.com")
    headers = {"Content-Type": "application/x-www-form-urlencoded","Authorization": LIVE_ACCESS_TOKEN}
    file = open(name,'a')
    file.write("Sending order... " + "\n")
    file.close()
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

while True:
    while True:
        if datetime.now() > dt:
            break 
        time.sleep(1)

    for i in range(5):
        h = {'Authorization' : LIVE_ACCESS_TOKEN}
        url = "https://api-fxtrade.oanda.com/v1/accounts/" + str(Account_Num) + "/positions"
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

        time.sleep(1)

        h = {'Authorization' : LIVE_ACCESS_TOKEN}
        url =   "https://api-fxtrade.oanda.com/v1/candles?instrument=" + Sec[i] + "&count=2&candleFormat=midpoint&granularity=D"
        r = requests.get(url, headers=h)     
        data = json.loads(r.text)
        def Open(index):
            return data["candles"][1-index][STRO]
        def High(index):
            return data["candles"][1-index][STRH]
        def Low(index):
            return data["candles"][1-index][STRL]
        def Close(index):
            return data["candles"][1-index][STRC]

        lvl_min = round(Open(1),2)
        lvl_max = round(Open(1),2) + 0.01
        pp = (High(1) + Low(1) + Close(1))/3
        sell_tp = 2*pp - High(1)
        buy_tp = 2*pp - Low(1)

        if Open_Units == 0:
            if Open(1) > lvl_min and Close(1) < lvl_min:
                SL = round(Open(1) + 0.00001,5)
                OpenOrder(Account_Num, Sec[i], 100, "market", "sell", sell_tp, SL)
            elif Open(1) < lvl_max and Close(1) > lvl_max:
                SL = round(Open(1) + 0.00001,5)
                OpenOrder(Account_Num, Sec[i], 100, "market", "buy", buy_tp, SL)
    
        time.sleep(1)
        
    dt += timedelta(hours=24)
    dt = dt.replace(second=0,microsecond=1)
    file = open(name,'a')
    file.write(str(datetime.now()) + " Waiting until " + str(dt) + "\n")
    file.close()