# Define all libraries, varaibles and functions
import requests
import json
from array import *
from Settings import PRICE_DOMAIN, ACCOUNT_DOMAIN, LIVe_ACCESS_TOKEN, ACCOUNT_ID, STRT, STRO, STRH, STRL, STRC, STRV, STRCO
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

# Perform first run initalizaiton calculations (Indicators)
if first_run or dt.hour == 22:
        


            time.sleep(1)
        first_run = False

# Price handler
#Try pulling 5m data and H4 Data and the constructing Daily data from the H4 then pass the lists containing price data to the other functions.

def H4_Prices(curr_pair):
    h = {'Authorization' : LIVE_ACCESS_TOKEN}
    url =   "https://api-fxtrade.oanda.com/v1/candles?instrument=" + curr_pair + "&count=2&candleFormat=midpoint&granularity=D"
    r = requests.get(url, headers=h)     
    data = json.loads(r.text)
    def High(index):
        return data["candles"][1-index][STRH]
    def Low(index):
        return data["candles"][1-index][STRL]
    def Close(index):
        return data["candles"][1-index][STRC]
    print len(data["candles"])
    # for i in range(len(data["candles"]))

def M5_Prices(curr_pair):
    h = {'Authorization' : LIVE_ACCESS_TOKEN}
    url =   "https://api-fxtrade.oanda.com/v1/candles?instrument=" + curr_pair + "&count=2&candleFormat=midpoint&granularity=m5"
    r = requests.get(url, headers=h)     
    data = json.loads(r.text)
    def High(index):
        return data["candles"][1-index][STRH]
    def Low(index):
        return data["candles"][1-index][STRL]
    def Close(index):
        return data["candles"][1-index][STRC]
    print len(data["candles"])
    # for i in range(len(data["candles"]))

def H4_to_D(h4_price):
    h = {'Authorization' : LIVE_ACCESS_TOKEN}
    url =   "https://api-fxtrade.oanda.com/v1/candles?instrument=" + curr_pair + "&count=2&candleFormat=midpoint&granularity=m5"
    r = requests.get(url, headers=h)     
    data = json.loads(r.text)
    def High(index):
        return data["candles"][1-index][STRH]
    def Low(index):
        return data["candles"][1-index][STRL]
    def Close(index):
        return data["candles"][1-index][STRC]
    print len(data["candles"])
    # for i in range(len(data["candles"]))

def D_Prices(curr_pair):
    h4 = H4_Prices(curr_pair)
    D = H4_to_D(h4)
    return D

# Signal Generating Functions
#Input price arrays and indicator values
#Output boolean values
def PivotPointBreakout(m5_price):

    class PivotPointBreakout:
        def __init__(self, symbol, m5_price):
            High_array
            Low_array
            Close_array = D

            for i in range(0,5):
                PP[i] = (High(1) + Low(1) + Close(1))/3
                S1[i] = 2*PP[i] - High(1)
                R1[i] = 2*PP[i] - Low(1)
                url =   "https://api-fxtrade.oanda.com/v1/candles?instrument=" + Sec[i] + "&count=100&candleFormat=midpoint&granularity=M15"
                r = requests.get(url, headers=h)     
                data = json.loads(r.text)
                def MHigh(index):
                    return data["candles"][99 - index][STRH]
                def MLow(index):
                    return data["candles"][99 - index][STRL]
                def MClose(index):
                    return data["candles"][99 - index][STRC]
            self.symbol = symbol

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

            lst_ATR[i] = ATR(0)

        def Generate_Entry(self):
            h = {'Authorization' : LIVE_ACCESS_TOKEN}
            url =   "https://api-fxtrade.oanda.com/v1/candles?instrument=" + Sec[i] + "&count=5&candleFormat=midpoint&granularity=M15"
            r = requests.get(url, headers=h)     
            data = json.loads(r.text)
            def MHigh(index):
                return data["candles"][4 - index][STRH]
            def MLow(index):
                return data["candles"][4 - index][STRL]
            def MClose(index):
                return data["candles"][4 - index][STRC]
            
            lst_ATR[i] = (lst_ATR[i]*13 + TR(MHigh(0), MLow(0), MClose(1)))/14
            time.sleep(1)
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
                    SL = round(M5Close(0) + lst_ATR[i] + 0.00001,5)
                    TP = round(M5Close(0) - lst_ATR[i]*3 - 0.00001,5)
                    if order_is_valid(M5Close(0), SL, TP):
                        OpenOrder(229783, Sec[i], 200, "market", "sell", TP, SL)
                    lst_SL[i] = SL
                elif M5Close(0) > S1[i] and M5Close(1) > S1[i] and M5Close(2) < S1[i]:
                    SL = round(M5Close(0) - lst_ATR[i] - 0.00001,5)
                    TP = round(M5Close(0) + lst_ATR[i]*3 + 0.00001,5)
                    if order_is_valid(M5Close(0), SL, TP):
                        OpenOrder(229783, Sec[i], 200, "market", "sell", TP, SL)
                    lst_SL[i] = SL
            lst_price[i] = M5Close(0)
                def order_is_valid(pr, SL, TP):
                    if abs(TP- pr)/abs(SL- pr) < 2.835 and abs(TP- pr)/abs(SL- pr) > 0.485:
                        if abs(TP- pr) < 78 and abs(TP- pr) > 25:
                            if abs(SL- pr) < 30 and abs(SL- pr) > 5:
                                return True
                    else:
                        return False
        def Manage_Trades(self):

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



def MAC(h4_price):

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
            if Close(0) > Upper_Band and Close(1) > Upper_Band and Open_Units == 0:
            pr_entry = Close(0) + SL/2
            OpenOrder(account_id, Sec[i], 100, "limit", price ,"sell", Close(0) - 1.5*SL, Close(0) + SL)
        elif Close(0) < Lower_Band and Close(1) < Lower_Band and Open_Units == 0:
            pr_entry = Close(0) - SL/2
            OpenOrder(account_id, Sec[i], 100, "limit", price,"buy", Close(0) + 1.5*SL , Close(0) - SL)
        lst_price[i] = Close(0)
    
def BusRide(h4_price):
    

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
