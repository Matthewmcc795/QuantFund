# Define all libraries, varaibles and functions
import requests
import json
from array import *
from Settings import PRICE_DOMAIN, ACCOUNT_DOMAIN, LIVe_ACCESS_TOKEN, ACCOUNT_ID, STRT, STRO, STRH, STRL, STRC, STRV, STRCO
from QF_Functions import *
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

dt =  datetime.now()
dt = dt.replace(minute=2, second=0,microsecond=1)
dt = dt + timedelta(hours=1)
name_strat1 = "PPBreakout_Log2.txt" 
account_id = 229783
first_run = True

# hr = [2,6,10,14,18,22]
hr = [0,4,8,12,16,20]
Bars = 50
SL = 0.0050
n = 50
name_strat2 = "MAC_Log.txt"
account_id2 = 406207
name_strat3 = "BusRide_Log.txt"
account_id3 = 4
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

while True:
    while True:
        if datetime.now() > dt_PPB:
            lst_dt_PPB = dt_PPB
            PivotPointBreakout()
            # Some other functions here to run the script
            dt = lst_dt + timedelta(minutes=5)
            dt = dt.replace(second=0,microsecosnd=1)
        time.sleep(1)
    # if
        #Repeat if structurure owith array of different start time. In the down time run price handler. 



    def PivotPointBreakout(m5_price):
        if Open_Units == 0 and (dt.hour <= 18 and dt.hour >= 8):
            if M5Close(0) < R1[i] and M5Close(1) < R1[i] and M5Close(2) > R1[i]:
                SL = round(M5Close(0) + lst_ATR[i] + 0.00001,5)
                TP = round(M5Close(0) - lst_ATR[i]*3 - 0.00001,5)
                OpenOrder(229783, Sec[i], 200, "market", "sell", TP, SL)
                lst_SL[i] = SL
            elif M5Close(0) > S1[i] and M5Close(1) > S1[i] and M5Close(2) < S1[i]:
                SL = round(M5Close(0) - lst_ATR[i] - 0.00001,5)
                TP = round(M5Close(0) + lst_ATR[i]*3 + 0.00001,5)
                OpenOrder(229783, Sec[i], 200, "market", "buy", TP, SL)
                lst_SL[i] = SL
        lst_price[i] = M5Close(0)

# Signal Generating Functions
#Input price arrays and indicator values
#Output boolean values

# Money Mananger

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
        h = {'Authorization' : LIVE_ACCESS_TOKEN}
        url = "https://api-fxtrade.oanda.com/v1/accounts/229783/trades?instrument=" + str(Sec[i])
        r = requests.get(url, headers=h)     
        data2 = json.loads(r.text)
        chk = str(data2)
        time.sleep(1)


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

        if chk.find("id") != -1:
            for positions in data2["trades"]:
                trd_ID = positions["id"]
                trd_entry = float(positions["price"])
                trd_side = positions["side"]
                if trd_side == "buy":
                    if lst_price[i] > trd_entry + lst_ATR[i]/2:
                        SL = round(trd_entry + 0.00001,5)
                        UpdateStopLoss(229783, trd_ID, SL)
                        lst_SL[i] = SL                   
                    elif lst_price[i] > trd_entry + lst_ATR[i]:
                        SL = round(max(lst_SL, lst_price[i] - lst_ATR[i]) + 0.00001,5)
                        UpdateStopLoss(229783, trd_ID, SL)
                        lst_SL[i] = SL
                elif trd_side == "sell":
                    if lst_price[i] < trd_entry - lst_ATR[i]/2:
                        SL = round(trd_entry - 0.00001,5)
                        UpdateStopLoss(229783, trd_ID, SL)
                        lst_SL[i] = SL
                    elif lst_price[i] < trd_entry - lst_ATR[i]:
                        SL = round(min(lst_SL, lst_price[i] + lst_ATR[i]) - 0.00001,5)
                        UpdateStopLoss(229783, trd_ID, SL)
                        lst_SL[i] = SL

# System Checks

while True:

    while True:
        if datetime.now() > dt:
            break 
        time.sleep(1)


    dt = lst_dt + timedelta(minutes=5)
    dt = dt.replace(second=0,microsecond=1)
    file = open(name,'a')
    file.write(str(datetime.now()) + " Waiting until " + str(dt) + "\n")
    file.close()
