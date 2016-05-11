import requests
import json
from array import *
from Settings import PRICE_DOMAIN, ACCOUNT_DOMAIN, DEMO_ACCESS_TOKEN, ACCOUNT_ID, STRT, STRO, STRH, STRL, STRC, STRV, STRCO
import httplib
import urllib
from datetime import datetime, timedelta
import time
import sys

Sec = ["EUR_USD", "GBP_USD", "USD_CAD", "AUD_USD", "NZD_USD"]
hr = [2,6,10,14,18,22]
Bars = 50
SL = 0.0050
n = 50
name = "MAC_Log.txt"
account_id = 406207
first_run = True

dt =  datetime.now()
dt = dt + timedelta(hours=1)
dt = dt.replace(minute=3, second=0,microsecond=1)
while not dt.hour in hr:
    print dt.hour
    dt = dt + timedelta(hours=1)
print dt.hour
file = open(name,'a')
file.write("Starting at " + str(dt) + "\n")
file.close()

def OpenOrder(Account_Num, instrument, units, order_type, price, order_side, Take_Profit, Stop_Loss):
    conn = httplib.HTTPSConnection("api-fxtrade.oanda.com")
    headers = {"Content-Type": "application/x-www-form-urlencoded","Authorization": LIVE_ACCESS_TOKEN}
    file = open(name,'a')
    file.write("Sending order... " + "\n")
    file.close()
    params = urllib.urlencode({
        "instrument" : str(instrument),
        "units" : units,
        "type" : order_type,
        "price" : price,
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
    file = open(name,'a')
    file.write("Updating Stop Loss ... " + "\n")
    file.close()
    conn.request("PATCH", "/v1/accounts/" + str(Account_Num) + "/trades/" + str(trade_ID), params, headers)
    response = conn.getresponse().read()
    file = open(name,'a')
    file.write(response + "\n")
    file.close()

def CloseOrders(Account_Num, order_id):
    conn = httplib.HTTPSConnection("api-fxtrade.oanda.com")
    headers = {"Content-Type": "application/x-www-form-urlencoded","Authorization": LIVE_ACCESS_TOKEN}
    file = open(name,'a')
    file.write("Sending order... " + "\n")
    file.close()
    params = urllib.urlencode({
        "order_id" : str(order_id)
    })
    conn.request("DELETE", "/v1/accounts/" + str(Account_Num) + "/orders", params, headers)
    response = conn.getresponse().read()
    file = open(name,'a')
    file.write(response + "\n")
    file.close()

while True:

    while True:
        if datetime.now() > dt:
            break 
        time.sleep(1)

    # Clear all unfilled limit orders
    for i in range(5):
        h = {'Authorization' : LIVE_ACCESS_TOKEN}
        url = "https://api-fxtrade.oanda.com/v1/accounts/" + str(account_id) + "/orders?instrument=" + str(Sec[i])
        r = requests.get(url, headers=h)     
        data2 = json.loads(r.text)
        chk = str(data2)
        file = open(name,'a')
        file.write(chk + "\n")
        file.close()
        if chk.find("id") != -1:
            for positions in data2["orders"]:
                file = open(name,'a')
                file.write("Closing all unfilled orders \n")
                file.close()
                CloseOrders(account_id, data2["id"])

        h = {'Authorization' : LIVE_ACCESS_TOKEN}
        url =   "https://api-fxtrade.oanda.com/v1/candles?instrument=" + str(Sec[i]) + "&count=" + str(Bars) + "&candleFormat=midpoint&granularity=H4"
        r = requests.get(url, headers=h)     
        data = json.loads(r.text)

        def Close(index):
            return data["candles"][49 - index][STRC]

        aavg = 0.0
        avg = 0.0
        sd = 0.0
        ssd = 0.0

        for j in range(20):
            aavg += Close(j)
        SMA = aavg/(20)

        for j in range(20):
            ssd += (Close(j) - SMA)**2
        sd = (ssd/(19))**(0.5)

        Upper_Band = SMA + 2*sd
        Lower_Band = SMA - 2*sd
        h = {'Authorization' : LIVE_ACCESS_TOKEN}
        url = "https://api-fxtrade.oanda.com/v1/accounts/" + str(account_id) + "/positions"
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

        if Close(0) > Upper_Band and Close(1) > Upper_Band and Open_Units == 0:
            pr_entry = Close(0) + SL/2
            OpenOrder(account_id, Sec[i], 100, "limit", price ,"sell", Close(0) - 1.5*SL, Close(0) + SL)
        elif Close(0) < Lower_Band and Close(1) < Lower_Band and Open_Units == 0:
            pr_entry = Close(0) - SL/2
            OpenOrder(account_id, Sec[i], 100, "limit", price,"buy", Close(0) + 1.5*SL , Close(0) - SL)
        lst_price[i] = Close(0)
    
    for i in range(5): # Update stop losses
        h = {'Authorization' : LIVE_ACCESS_TOKEN}
        url = "https://api-fxtrade.oanda.com/v1/accounts/" + str(account_id) + "/trades?instrument=" + str(Sec[i])
        r = requests.get(url, headers=h)     
        data2 = json.loads(r.text)
        chk = str(data2)
        file = open(name,'a')
        file.write("Positions... " + "\n")
        file.write(chk + "\n")
        file.close()
        time.sleep(1)

        if chk.find("id") != -1:
            for positions in data2["trades"]:
                trd_ID = positions["id"]
                trd_entry = float(positions["price"])
                trd_side = positions["side"]
                if trd_side == "buy":
                    if lst_price[i] > trd_entry + 0.0050:
                        SL = round(trd_entry + 0.0025,5)
                        UpdateStopLoss(account_id, trd_ID, SL)
                        lst_SL[i] = SL                   
                elif trd_side == "sell":
                    if lst_price[i] < trd_entry - 0.050:
                        SL = round(trd_entry - 0.0025,5)
                        UpdateStopLoss(account_id, trd_ID, SL)
                        lst_SL[i] = SL

    dt = dt + timedelta(hours=4)
    dt = dt.replace(minute=3, second=0, microsecond=1)
    file = open(name,'a')
    file.write(str(datetime.now()) + " Waiting until " + str(dt) + "\n")
    file.close()