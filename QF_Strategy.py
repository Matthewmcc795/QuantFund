import requests
import json
from array import *
from Settings import PRICE_DOMAIN, ACCOUNT_DOMAIN, LIVE_ACCESS_TOKEN, ACCOUNT_ID, STRT, STRO, STRH, STRL, STRC, STRV, STRCO
import httplib
import urllib
from datetime import datetime, timedelta
import time
import sys

PivotPointBreakout = {
    "ATR": {
        "EUR_USD": 0,
        "GBP_USD": 0,
        "USD_CAD": 0,
        "AUD_USD": 0,
        "NZD_USD": 0,
    "S1": {
        "EUR_USD": 0,
        "GBP_USD": 0,
        "USD_CAD": 0,
        "AUD_USD": 0,
        "NZD_USD": 0,
    "R1": {
        "EUR_USD": 0,
        "GBP_USD": 0,
        "USD_CAD": 0,
        "AUD_USD": 0,
        "NZD_USD": 0,
    }
}

##########################################################################################################
#                                                                                                        #
#                                                Prices                                                  #
#                                                                                                        #
##########################################################################################################

def Get_Price(curr_pair, tf, bars, ohlc):
    O = []
    H = []
    L = []
    C = []
    h = {'Authorization' : LIVE_ACCESS_TOKEN}
    url =   "https://api-fxtrade.oanda.com/v1/candles?instrument=" + str(curr_pair) + "&count=" + str(bars) + "&candleFormat=midpoint&granularity=" + str(tf)
    r = requests.get(url, headers=h)     
    data = json.loads(r.text)
    for i in range(len(data["candles"])):
        O.append(data["candles"][i][STRO])
        H.append(data["candles"][i][STRH])
        L.append(data["candles"][i][STRL])
        C.append(data["candles"][i][STRC])
    if ohlc == "ohlc":
        return O, H, L, C
    elif ohlc == "hlc":
        return H, L, C
    elif ohlc == "c":
        return C

##########################################################################################################
#                                                                                                        #
#                                              Strategies                                                #
#                                                                                                        #
##########################################################################################################

def PivotPointBreakout(account_id, sec, vol):
    dh, dl, dc = Get_Price(sec, "D", 2)
    s1, r1 = Get_Pivot_Points(dh, dl, dc)
    m15h, m15l, m15c = Get_Price(sec[i], "M15", 100)
    atr = Get_ATR(m15h, m15l, m15c)
    m5c = Get_Price(sec[i], "M5", 3)
    head = {'Authorization' : LIVE_ACCESS_TOKEN}
    url = "https://api-fxtrade.oanda.com/v1/accounts/" + str(account_id) + "/trades?instrument=" + str(sec[i])
    r = requests.get(url, headers=head)     
    data2 = json.loads(r.text)
    chk = str(data2)
    if chk.find("id") == -1:
        Open_Units = 0
        for positions in data2["positions"]:
            if positions["instrument"] == sec[i]:
                Open_Units = positions["units"]
        if Open_Units == 0 and (dt.hour <= 18 and dt.hour >= 8):
            if m5c[0] < r1 and m5c[1] < r1 and m5c[2] > r1:
                SL = round(m5c[0] + atr + 0.00001,5)
                TP = round(m5c[0] - 3*atr - 0.00001,5)
                OpenOrder(account_id, sec[i], vol, "market", "sell", TP, SL)
                lst_SL[i] = SL
            elif m5c[0] > s1 and m5c[1] > s1 and m5c[2] < s1:
                SL = round(m5c[0] - atr - 0.00001,5)
                TP = round(m5c[0] + 3*atr + 0.00001,5)
                OpenOrder(account_id, sec[i], vol, "market", "buy", TP, SL)
                lst_SL[i] = SL
        lst_price[i] = m5c[0]
    elif chk.find("id") != -1:
        for positions in data2["trades"]:
            trd_ID = positions["id"]
            trd_entry = float(positions["price"])
            trd_side = positions["side"]
            if trd_side == "buy":
                if lst_price[i] > trd_entry + atr/2:
                    SL = round(trd_entry + 0.00001,5)
                    UpdateStopLoss(229783, trd_ID, SL)
                    lst_SL[i] = SL                   
                elif lst_price[i] > trd_entry + atr:
                    SL = round(max(lst_SL, lst_price[i] - atr) + 0.00001,5)
                    UpdateStopLoss(229783, trd_ID, SL)
                    lst_SL[i] = SL
            elif trd_side == "sell":
                if lst_price[i] < trd_entry - atr]/2:
                    SL = round(trd_entry - 0.00001,5)
                    UpdateStopLoss(229783, trd_ID, SL)
                    lst_SL[i] = SL
                elif lst_price[i] < trd_entry - atr:
                    SL = round(min(lst_SL, lst_price[i] + atr) - 0.00001,5)
                    UpdateStopLoss(229783, trd_ID, SL)
                    lst_SL[i] = SL

def MovingAverageContrarian(account_id, sec, vol):
    c = Get_Price(sec,"H4",51)
    ma = SMA(c,50)
    sd = STDEV(c,50)
    Z = (c[0] - ma)/sd
    h = {'Authorization' : LIVE_ACCESS_TOKEN}
    url = "https://api-fxtrade.oanda.com/v1/accounts/" + str(account_id) + "/trades?instrument=" + str(sec)
    r = requests.get(url, headers=h)     
    data2 = json.loads(r.text)
    chk = str(data2)
    if chk.find("id") == -1:
        Open_Units = 0
        for positions in data2["positions"]:
            if positions["instrument"] == sec:
                Open_Units = positions["units"]
        if Open_Units == 0 and (dt.hour <= 18 and dt.hour >= 8):
            if Z > 2:
                SL = round(c[0] + sd/2 + 0.00001,5)
                TP = round(c[0] - sd/2 - 0.00001,5)
                OpenMarketOrder(account_id, sec, vol, "market", "sell", TP, SL)
            elif Z < -2:
                SL = round(c[0] - sd/2 - 0.00001,5)
                TP = round(c[0] + sd/2 + 0.00001,5)
                OpenMarketOrder(account_id, sec, vol, "market", "buy", TP, SL)

def BusRide(account_id, sec, vol):
    o, h, l, c = Get_Price(sec, "D", 2)
    time.sleep(1)
    h = {'Authorization' : LIVE_ACCESS_TOKEN}
    url = "https://api-fxtrade.oanda.com/v1/accounts/" + str(account_id) + "/trades?instrument=" + str(sec)
    r = requests.get(url, headers=h)     
    data2 = json.loads(r.text)
    chk = str(data2)
    if chk.find("instrument") == -1:
        Open_Units = 0 
    else:
        Open_Units = 0
        for positions in data2["positions"]:
            if positions["instrument"] == sec:
                Open_Units = positions["units"]
    lvl_min = round(o[1],2)
    lvl_max = round(o[1],2) + 0.01
    pp = (h[1] + l[1] + c[1])/3
    sell_tp = 2*pp - h[1]
    buy_tp = 2*pp - l[1]

    if Open_Units == 0:
        if o[0] > lvl_min and c[0] < lvl_min:
            SL = round(Open(1) + 0.00001,5)
            OpenOrder(account_id, sec, vol, "market", "sell", sell_tp, SL)
        elif o[0] < lvl_max and c[0] > lvl_max:
            SL = round(o[0] + 0.00001,5)
            OpenOrder(account_id, sec, v0l, "market", "buy", buy_tp, SL)

##########################################################################################################
#                                                                                                        #
#                                               Orders                                                   #
#                                                                                                        #
##########################################################################################################

# def OpenLimitOrder(Account_Num, instrument, units, order_type, price, order_side, Take_Profit, Stop_Loss):
#     conn = httplib.HTTPSConnection("api-fxtrade.oanda.com")
#     headers = {"Content-Type": "application/x-www-form-urlencoded","Authorization": LIVE_ACCESS_TOKEN}
#     file = open(name,'a')
#     file.write("Sending order... " + "\n")
#     file.close()
#     params = urllib.urlencode({
#         "instrument" : str(instrument),
#         "units" : units,
#         "type" : order_type,
#         "price" : price,
#         "side" : order_side,
#         "takeProfit": Take_Profit,
#         "stopLoss": Stop_Loss
#     })
#     conn.request("POST", "/v1/accounts/" + str(Account_Num) + "/orders", params, headers)
#     response = conn.getresponse().read()
#     file = open(name,'a')
#     file.write(response + "\n")
#     file.close()

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

def OpenMarketOrder(Account_Num, instrument, units, order_type, order_side, Take_Profit, Stop_Loss):
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

##########################################################################################################
#                                                                                                        #
#                                              Indicators                                                #
#                                                                                                        #
##########################################################################################################

def Get_Pivot_Points(h,l,c):
    PP_val = (h[1] + l[1] + c[1])/3
    S1_val = 2*PP_val - h[1]
    R1_val = 2*PP_val - l[1]
    return S1_val, R1_val
    
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


def Get_ATR(h, l, c, first):
    if first:
        return ATR(h,l,c)
    # else:
        # lst_ATR[i] = (lst_ATR[i]*13 + TR(h[0], l[0], c[1]))/14

def ATR(h, l, c):
    p = 98
    TrueRanges = 0.0
    ATR_val = 0
    while p > 84:
        TrueRanges = TrueRanges + TR(h[p], l[p], c[p+1])
        p -= 1
    ATR_val = TrueRanges/14
    while p >= 0:
        ATR_val = (ATR_val*13 + TR(h[p], l[p], c[p+1]))/14
        p -= 1
    return ATR_val

def SMA(c, n):
    sma_val = 0.0
    for i in range(len(c)-1):
        sma_val += c[i]
    sma_val /= len(sma_val)
    return sma_val

def STDEV(c,n):
    ma = SMA(c,n)
    sd_val = 0.0
    for i in range(len(c)-1):
        sd_val += (ma - c[i])**2
    sd_val = (sd_val/(len(c)-1))**(0.5)
    return sd_val