# This script handles executing specific trading plans and all related calculaitons
import requests
import json
from array import *
from Settings import PRICE_DOMAIN, ACCOUNT_DOMAIN, LIVE_ACCESS_TOKEN, ACCOUNT_ID, STRT, STRO, STRH, STRL, STRC, STRV, STRCO
import httplib
import urllib
from datetime import datetime, timedelta
import time
import sys
main_log = "QF.txt"
PPB = {
    "ATR": {
        "EUR_USD": 0,
        "GBP_USD": 0,
        "USD_CAD": 0,
        "AUD_USD": 0,
        "NZD_USD": 0
    }, 
    "SL": {
        "EUR_USD": 0,
        "GBP_USD": 0,
        "USD_CAD": 0,
        "AUD_USD": 0,
        "NZD_USD": 0,
    }
}

MAC = {
    "Z": {
        "EUR_USD": 0,
        "GBP_USD": 0,
        "USD_CAD": 0,
        "AUD_USD": 0,
        "NZD_USD": 0
    },
    "Correl": {
        "EUR_USD": 0,
        "GBP_USD": 0,
        "USD_CAD": 0,
        "AUD_USD": 0,
        "NZD_USD": 0,
    }, 
    "Expected_Z": {
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
        O.append(data["candles"][bars - i - 1][STRO])
        H.append(data["candles"][bars - i - 1][STRH])
        L.append(data["candles"][bars - i - 1][STRL])
        C.append(data["candles"][bars - i - 1][STRC])
    time.sleep(1)
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

def PivotPointBreakout(account_id, sec, vol, file_nm):
    for i in range(len(sec)):
        file = open(main_log,'a')
        file.write("Collecting PPB data for " + sec[i] + " " + str(datetime.now()) +"\n")
        file.close()
        dh, dl, dc = Get_Price(sec[i], "D", 2, "hlc")
        s1, r1 = Get_Pivot_Points(dh, dl, dc)
        m15h, m15l, m15c = Get_Price(sec[i], "M15", 100, "hlc")
        atr = Get_ATR(m15h, m15l, m15c, sec[i])
        m5c = Get_Price(sec[i], "M5", 3, "c")
        Open_Units = GetOpenUnits(account_id, sec[i])
        dt = datetime.now()
        if Open_Units == 0 and (dt.hour <= 18 and dt.hour >= 8):
            file = open(main_log,'a')
            file.write("Checking PPB signals for " + sec[i] + " " + str(datetime.now()) +"\n")
            file.close()
            if m5c[0] < r1 and m5c[1] < r1 and m5c[2] > r1:
                file = open(main_log,'a')
                file.write("PPB: Sell " + sec[i] + " " + str(datetime.now()) +"\n")
                file.close()
                SL = round(m5c[0] + atr + 0.00001,5)
                TP = round(m5c[0] - 3*atr - 0.00001,5)
                OpenMarketOrder(account_id, sec[i], vol, "market", "sell", TP, SL, file_nm)
                lst_SL[i] = SL
            elif m5c[0] > s1 and m5c[1] > s1 and m5c[2] < s1:
                file = open(main_log,'a')
                file.write("PPB: Sell " + sec[i] + " " + str(datetime.now()) +"\n")
                file.close()
                SL = round(m5c[0] - atr - 0.00001,5)
                TP = round(m5c[0] + 3*atr + 0.00001,5)
                OpenMarketOrder(account_id, sec[i], vol, "market", "buy", TP, SL, file_nm)
                PPB["SL"][sec[i]] = SL
        elif Open_Units != 0:
            file = open(main_log,'a')
            file.write("PPB: updating stops for " + sec[i] + " " + str(datetime.now()) +"\n")
            file.close()
            Open_Trades = GetOpenTrades(account_id, sec[i])
            for positions in Open_Trades["trades"]:
                trd_ID = positions["id"]
                trd_entry = float(positions["price"])
                trd_side = positions["side"]
                if trd_side == "buy":
                    if m5c[0] > trd_entry + atr/2:
                        SL = round(trd_entry + 0.00001,5)
                        UpdateStopLoss(account_id, trd_ID, SL, file_nm)
                        PPB["SL"][sec[i]] = SL                   
                    elif m5c[0] > trd_entry + atr:
                        SL = round(max(PPB["SL"][sec[i]], m5c[0] + atr/2) + 0.00001,5)
                        UpdateStopLoss(account_id, trd_ID, SL, file_nm)
                        PPB["SL"][sec[i]] = SL
                elif trd_side == "sell":
                    if m5c[0] < trd_entry - atr/2:
                        SL = round(trd_entry - 0.00001,5)
                        UpdateStopLoss(account_id, trd_ID, SL, file_nm)
                        PPB["SL"][sec[i]] = SL
                    elif m5c[0] < trd_entry - atr:
                        SL = round(min(PPB["SL"][sec[i]], m5c[0] - atr/2) - 0.00001,5)
                        UpdateStopLoss(account_id, trd_ID, SL, file_nm)
                        PPB["SL"][sec[i]] = SL

def MovingAverageContrarian(account_id, sec, vol, file_nm):
    for i in range(len(sec)):
        c = Get_Price(sec[i], "H4", 50, "c")
        ma = SMA(c,50)
        sd = STDEV(c,50)
        Z = (c[0] - ma)/sd
        MAC["Z"][sec[i]] = Z
        Open_Units = GetOpenUnits(account_id, sec[i])
        if Open_Units == 0:
            if Z > 2:
                SL = round(c[0] + sd/2 + 0.00001,5)
                TP = round(c[0] - sd/2 - 0.00001,5)
                OpenMarketOrder(account_id, sec[i], vol, "market", "sell", TP, SL, file_nm)
            elif Z < -2:
                SL = round(c[0] - sd/2 - 0.00001,5)
                TP = round(c[0] + sd/2 + 0.00001,5)
                OpenMarketOrder(account_id, sec[i], vol, "market", "buy", TP, SL, file_nm)

def BusRide(account_id, sec, vol, file_nm):
    for i in range(len(sec)):
        o, h, l, c = Get_Price(sec[i], "H4", 5, "ohlc")
        Open_Units = GetOpenUnits(account_id, sec[i])
        lvl_min = round(o[1],2)
        lvl_max = round(o[1],2) + 0.01
        sell_tp, buy_tp = Get_Pivot_Points(h, l, c)
        if Open_Units == 0:
            if o[0] > lvl_min and c[0] < lvl_min:
                SL = round(o[0] + 0.00001,5)
                OpenMarketOrder(account_id, sec[i], vol, "market", "sell", sell_tp, o[0], file_nm)
            elif o[0] < lvl_max and c[0] > lvl_max:
                SL = round(o[0] + 0.00001,5)
                OpenMarketOrder(account_id, sec[i], vol, "market", "buy", buy_tp, o[0], file_nm)

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

def UpdateStopLoss(Account_Num, trade_ID, Stop_Loss, file_str):
    conn = httplib.HTTPSConnection("api-fxtrade.oanda.com")
    headers = {"Content-Type": "application/x-www-form-urlencoded","Authorization": LIVE_ACCESS_TOKEN}
    params = urllib.urlencode({"stopLoss": Stop_Loss})
    file = open(file_str,'a')
    file.write("Updating Stop Loss ... " + "\n")
    file.close()
    conn.request("PATCH", "/v1/accounts/" + str(Account_Num) + "/trades/" + str(trade_ID), params, headers)
    response = conn.getresponse().read()
    file = open(file_str,'a')
    file.write(response + "\n")
    file.close()
    time.sleep(1)

# def CloseOrders(Account_Num, order_id):
#     conn = httplib.HTTPSConnection("api-fxtrade.oanda.com")
#     headers = {"Content-Type": "application/x-www-form-urlencoded","Authorization": LIVE_ACCESS_TOKEN}
#     file = open(name,'a')
#     file.write("Sending order... " + "\n")
#     file.close()
#     params = urllib.urlencode({
#         "order_id" : str(order_id)
#     })
#     conn.request("DELETE", "/v1/accounts/" + str(Account_Num) + "/orders", params, headers)
#     response = conn.getresponse().read()
#     file = open(name,'a')
#     file.write(response + "\n")
#     file.close()

def GetOpenTrades(Account_Num, sec):
    h = {'Authorization' : LIVE_ACCESS_TOKEN}
    url = "https://api-fxtrade.oanda.com/v1/accounts/" + str(Account_Num) + "/trades?instrument=" + str(sec)
    r = requests.get(url, headers=h) 
    time.sleep(1)    
    return json.loads(r.text)


def OpenMarketOrder(Account_Num, instrument, units, order_type, order_side, Take_Profit, Stop_Loss, file_str):
    conn = httplib.HTTPSConnection("api-fxtrade.oanda.com")
    headers = {"Content-Type": "application/x-www-form-urlencoded","Authorization": LIVE_ACCESS_TOKEN}
    file = open(file_str,'a')
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
    file = open(file_str,'a')
    file.write(response + "\n")
    file.close()
    time.sleep(1)

def GetOpenUnits(account_id, sec):
    h = {'Authorization' : LIVE_ACCESS_TOKEN}
    url = "https://api-fxtrade.oanda.com/v1/accounts/" + str(account_id) + "/positions"
    r = requests.get(url, headers=h)     
    data2 = json.loads(r.text)
    chk = str(data2)
    if chk.find("positions") == -1:
        Units = 0 
    else:
        Units = 0
        for positions in data2["positions"]:
            if positions["instrument"] == sec:
                Units = positions["units"]
    time.sleep(1)
    return Units

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


def Get_ATR(h, l, c, sec):
    if PPB["ATR"][sec] == 0:
        return ATR(h,l,c)
    else:
        PPB["ATR"][sec] = (PPB["ATR"][sec]*13 + TR(h[0], l[0], c[1]))/14
        return PPB["ATR"][sec]

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
    for i in range(n):
        sma_val += c[i]
    return sma_val/n

def STDEV(c, n):
    ma = SMA(c,n)
    sd_val = 0.0
    for i in range(n):
        sd_val += (ma - c[i])**2 
    return (sd_val/(n-1))**(0.5)

def CORREL(c1, c2):
    ma1 = SMA(c1,len(c1))
    ma2 = SMA(c2,len(c2))
    for i in range(len(c1)):
        exy += (c1[i] - ma1)*(c2[i]-ma2)
    exy = exy/len(c1)