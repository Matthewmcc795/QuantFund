# This script handles executing specific trading plans and all related calculaitons
import requests
import json
from array import *
from Settings import LIVE_ACCESS_TOKEN, STRT, STRO, STRH, STRL, STRC, STRV, STRCO
import httplib
import urllib
from QF_Optimizer import *
from QF_Functions import *
from datetime import datetime, timedelta
import time
import sys
main_log = "QF.txt"

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
hr = [2,6,10,14,18,22]

##########################################################################################################
#                                                                                                        #
#                                              Strategies                                                #
#                                                                                                        #
##########################################################################################################

def PivotPointBreakout(account_id, sec, vol, tf, file_nm):
    for i in range(len(sec)):
        SaveToLog(main_log, "Collecting PPB data for " + sec[i])
        m15h, m15l, m15c = Get_Price(sec[i], tf[1], 101, "hlc")
        ma = SMA(m15c, 20,0)
        atr = Get_ATR(m15h, m15l, m15c, sec[i])
        m5c = Get_Price(sec[i], tf[0], 20, "c")
        s, r = Get_Pivot_Points(sec[i], tf[2], m5c[0])
        Open_Units = GetOpenUnits(account_id, sec[i], sec, LIVE_ACCESS_TOKEN)
        dt = datetime.now()
        if Open_Units == 0 and (dt.hour <= 18 and dt.hour >= 8):
            PPB["Open"][sec[i]] = 0
            PPB["Status"][sec[i]] = ""
            if m5c[0] > s and m5c[1] > s and m5c[2] < s and ma > s:
                SaveToLog(main_log, "PPB: Sell " + sec[i])
                PPB["SL"][sec[i]] = round(m5c[0] + atr + 0.00001,5)
                PPB["TP"][sec[i]] = max(PP[pos[-2:]][sec], round(m5c[0] - 2*atr - 0.00001,5))
                OpenMarketOrder(account_id, sec[i], vol, "market", "sell", PPB["TP"][sec[i]], PPB["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN)
                PPB["Open"][sec[i]] = dt
                PPB["Status"][sec[i]] = "Entry"
            elif m5c[0] < r and m5c[1] < r and m5c[2] > r and ma < r:
                SaveToLog(main_log, "PPB: Buy " + sec[i])
                PPB["SL"][sec[i]] = round(m5c[0] - atr - 0.00001,5)
                PPB["TP"][sec[i]] = min(PP[pos[:2]][sec], round(m5c[0] + 2*atr + 0.00001,5))
                OpenMarketOrder(account_id, sec[i], vol, "market", "buy", PPB["TP"][sec[i]], PPB["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN)
                PPB["Open"][sec[i]] = dt
                PPB["Status"][sec[i]] = "Entry"
        elif Open_Units != 0:
            if PPB["Status"][sec[i]] == "":
                PPB["Status"][sec[i]] = "Entry"
                PPB["Open"][sec[i]] = dt
            SaveToLog(main_log, "PPB: updating stops for " + sec[i])
            Open_Trades = GetOpenTrades(account_id, sec[i], LIVE_ACCESS_TOKEN)
            for positions in Open_Trades["trades"]:
                trd_ID = positions["id"]
                trd_entry = float(positions["price"])
                trd_side = positions["side"]
                if dt - timedelta(minutes=45) < PPB["Open"][sec[i]]:
                    if trd_side == "buy":
                        if m5c[0] > 0.75*(PPB["TP"][sec[i]] - trd_entry) + trd_entry and (PPB["Status"][sec[i]] == "BE" or PPB["Status"][sec[i]] == "Entry"):
                            OpenMarketOrder(account_id, sec[i], 0.75*vol, "market", "sell", 0, 0, file_nm, LIVE_ACCESS_TOKEN)
                            PPB["SL"][sec[i]] = 0.25*(PPB["TP"][sec[i]] - trd_entry) + trd_entry
                            UpdateStopLoss(account_id, trd_ID, PPB["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN)
                            PPB["Status"][sec[i]] = "75%"
                        elif dt - timedelta(minutes=15) > PPB["Open"][sec[i]] and m5c[0] > (PPB["TP"][sec[i]] - trd_entry)/3 + trd_entry and PPB["Status"][sec[i]] == "Entry":
                            PPB["SL"][sec[i]] = round(trd_entry + min(0.00025, atr/4, abs(m5c[0] - trd_entry)/2) + 0.00001,5)
                            if PPB["SL"][sec[i]] > trd_entry and PPB["SL"][sec[i]] < m5c[0]:
                                UpdateStopLoss(account_id, trd_ID, PPB["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN) 
                                PPB["Status"][sec[i]] = "BE"                 
                    elif trd_side == "sell":
                        if m5c[0] < trd_entry - 0.75*(trd_entry - PPB["TP"][sec[i]]) and (PPB["Status"][sec[i]] == "BE" or PPB["Status"][sec[i]] == "Entry"):
                            OpenMarketOrder(account_id, sec[i], 0.75*vol, "market", "buy", 0, 0, file_nm, LIVE_ACCESS_TOKEN) 
                            PPB["SL"][sec[i]] = trd_entry - 0.25*(trd_entry - PPB["TP"][sec[i]])
                            UpdateStopLoss(account_id, trd_ID, PPB["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN)
                            PPB["Status"][sec[i]] = "75%"
                        elif dt - timedelta(minutes=15) > PPB["Open"][sec[i]] and m5c[0] < trd_entry - (trd_entry - PPB["TP"][sec[i]])/3 and PPB["Status"][sec[i]] == "Entry":
                            PPB["SL"][sec[i]] = round(trd_entry - min(0.00025, atr/4, abs(trd_entry - m5c[0])/2) + 0.00001,5)
                            if PPB["SL"][sec[i]] < trd_entry and PPB["SL"][sec[i]] > m5c[0]:
                                UpdateStopLoss(account_id, trd_ID, PPB["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN)
                                PPB["Status"][sec[i]] = "BE"
                else:
                    if PPB["Status"][sec[i]] == "Entry":
                        bounded = True
                        bound = max(abs(PPB["SL"][sec[i]] - trd_entry), abs(PPB["TP"][sec[i]] - trd_entry))
                        ubound = trd_entry + 0.1*bound
                        lbound = trd_entry + 0.1*bound
                        for t in range(14):
                            if m5c[t] > lbound and m5c[t] < ubound and bounded == True:
                                bounded = True
                            else:
                                bounded = False
                        if bounded == True:
                            ClosePositions(account_id, sec[i], file_nm, LIVE_ACCESS_TOKEN)
                        else:
                            PPB["Status"][sec[i]] = "Entry-Long"
                    if trd_side == "buy":
                        if m5c[0] > 0.5*(PPB["TP"][sec[i]] - trd_entry) + trd_entry:
                            ClosePositions(account_id, sec[i], file_nm, LIVE_ACCESS_TOKEN)
                        elif m5c[0] > (PPB["TP"][sec[i]] - trd_entry)/3 + trd_entry and (PPB["Status"][sec[i]] == "BE" or PPB["Status"][sec[i]] == "Entry-Long"):
                            OpenMarketOrder(account_id, sec[i], 0.5*vol, "market", "sell", 0, 0, file_nm, LIVE_ACCESS_TOKEN)
                            PPB["SL"][sec[i]] = round(trd_entry + min(0.00025, atr/4, abs(m5c[0] - trd_entry)/2) + 0.00001,5)
                            if PPB["SL"][sec[i]] > trd_entry and PPB["SL"][sec[i]] < m5c[0]:
                                UpdateStopLoss(account_id, trd_ID, PPB["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN)
                                PPB["Status"][sec[i]] = "50%"
                    elif trd_side == "sell":
                        if m5c[0] < trd_entry - 0.5*(trd_entry - PPB["TP"][sec[i]]):
                            ClosePositions(account_id, sec[i], file_nm, LIVE_ACCESS_TOKEN) 
                        elif m5c[0] < trd_entry - (trd_entry - PPB["TP"][sec[i]])/3 and (PPB["Status"][sec[i]] == "BE" or PPB["Status"][sec[i]] == "Entry-Long"):
                            OpenMarketOrder(account_id, sec[i], 0.5*vol, "market", "buy", 0, 0, file_nm, LIVE_ACCESS_TOKEN)
                            PPB["SL"][sec[i]] = round(trd_entry - min(0.00025, atr/4, abs(trd_entry - m5c[0])/2) + 0.00001,5)
                            if PPB["SL"][sec[i]] < trd_entry and PPB["SL"][sec[i]] > m5c[0]:
                                UpdateStopLoss(account_id, trd_ID, PPB["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN)
                                PPB["Status"][sec[i]] = "50%"

def MovingAverageContrarian(account_id, sec, vol, tf, file_nm):
    for i in range(len(sec)):
        SaveToLog(main_log, "Collecting MAC data for " + sec[i])
        c = Get_Price(sec[i], tf, 51, "c")
        ma1 = SMA(c,50,1)
        sd1 = STDEV(c,50,1)
        ma0 = SMA(c,50,0)
        sd0 = STDEV(c,50,0)
        Z1 = (c[1] - ma1)/sd1
        Z0 = (c[0] - ma0)/sd0
        Open_Units = GetOpenUnits(account_id, sec[i], sec, LIVE_ACCESS_TOKEN)
        if Open_Units == 0:
            SaveToLog(main_log, "Checking MAC signals for " + sec[i])
            if Z1 > 2 and Z0 < 2:
                SaveToLog(main_log, "MAC: Sell " + sec[i])
                SL = round(c[0] + sd/2 + 0.00001,5)
                TP = round(c[0] - sd/2 - 0.00001,5)
                OpenMarketOrder(account_id, sec[i], vol, "market", "sell", TP, SL, file_nm, LIVE_ACCESS_TOKEN)
            elif Z1 < -2 and Z0 > -2:
                SaveToLog(main_log, "MAC: Buy " + sec[i])
                SL = round(c[0] - sd/2 - 0.00001,5)
                TP = round(c[0] + sd/2 + 0.00001,5)
                OpenMarketOrder(account_id, sec[i], vol, "market", "buy", TP, SL, file_nm, LIVE_ACCESS_TOKEN)

# def BusRide(account_id, sec, vol, tf, file_nm):
#     for i in range(len(sec)):
#         SaveToLog(main_log, "Collecting BusRide data for " + sec[i])
#         c = Get_Price(sec[i], tf, 51, "c")
#         if tf == "D":
#             sell_tp, buy_tp = Get_Pivot_Points(sec, "D", c[0])
#         elif tf == "M15":
#             sell_tp = round(c[0]/1.0025 + 0.00001,5)
#             buy_tp = round(c[0]*1.0025 - 0.00001,5)
#         Open_Units = GetOpenUnits(account_id, sec[i], sec, LIVE_ACCESS_TOKEN)
#         lvl_min = round(c[2],2)
#         lvl_max = round(c[2],2) + 0.01 
#         ma = SMA(c, 50)      
#         if Open_Units == 0:
#             SaveToLog(main_log, "Checking Bus Ride signals for " + sec[i])
#             if c[2] > lvl_min and c[0] < lvl_min and ma > lvl_min:
#                 SaveToLog(main_log, "Bus Ride: Sell " + sec[i])
#                 SL = round(c[2] - 0.00001,5)
#                 OpenMarketOrder(account_id, sec[i], vol, "market", "sell", sell_tp, SL, file_nm, LIVE_ACCESS_TOKEN)
#             elif c[2] < lvl_max and c[0] > lvl_max and ma < lvl_max:
#                 SaveToLog(main_log, "Bus Ride: Buy " + sec[i])
#                 SL = round(c[2] + 0.00001,5)
#                 OpenMarketOrder(account_id, sec[i], vol, "market", "buy", buy_tp, SL, file_nm, LIVE_ACCESS_TOKEN)

def IntraTrend(account_id, sec, vol, tf, file_nm):
    for i in range(len(sec)):
        SaveToLog(main_log, "Collecting IT data for " + sec[i])
        c = Get_Price(sec[i], tf, 51, "c")
        SMA10 = SMA(c,10, 0)
        SMA21 = SMA(c,21, 0)
        SMA50 = SMA(c,50, 0)
        Open_Units = GetOpenUnits(account_id, sec[i], sec, LIVE_ACCESS_TOKEN)
        dt = datetime.now()
        if Open_Units == 0 and (dt.hour <= 18 and dt.hour >= 8):
            PPB["Open"][sec[i]] = 0
            PPB["Status"][sec[i]] = ""
            if c[0] > SMA10 and c[0] < SMA21 and c[0] < SMA50:
                SaveToLog(main_log, "ITM: Sell " + sec[i])
                ITM["TP"][sec[i]] = round(c[0] - 0.8*abs(c[0] - SMA50), 5)
                ITM["SL"][sec[i]] = round(SMA50, 5)
                OpenMarketOrder(account_id, sec[i], vol, "market", "sell", ITM["TP"][sec[i]], ITM["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN)
                ITM["Open"][sec[i]] = dt
                ITM["Status"][sec[i]] = "Entry"
            elif c[0] < SMA10 and c[0] > SMA21 and c[0] > SMA50:
                SaveToLog(main_log, "ITM: Buy " + sec[i])
                ITM["TP"][sec[i]] = round(c[0] + 0.8*abs(c[0] - SMA50), 5)
                ITM["SL"][sec[i]] = round(SMA50, 5)
                OpenMarketOrder(account_id, sec[i], vol, "market", "buy", ITM["TP"][sec[i]], ITM["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN)
                ITM["Open"][sec[i]] = dt
                ITM["Status"][sec[i]] = "Entry"
        elif Open_Units != 0:
            if PPB["Status"][sec[i]] == "":
                PPB["Status"][sec[i]] = "Entry"
                PPB["Open"][sec[i]] = dt
            Open_Trades = GetOpenTrades(account_id, sec[i], LIVE_ACCESS_TOKEN)
            for positions in Open_Trades["trades"]:
                trd_ID = positions["id"]
                trd_entry = float(positions["price"])
                trd_side = positions["side"]
                if dt - timedelta(minutes=120) < ITM["Open"][sec[i]]:
                    if trd_side == "buy":
                        if c[0] > 0.75*(ITM["TP"][sec[i]] - trd_entry) + trd_entry and (ITM["Status"][sec[i]] == "BE" or ITM["Status"][sec[i]] == "Entry"):
                            OpenMarketOrder(account_id, sec[i], 0.75*vol, "market", "sell", 0, 0, file_nm, LIVE_ACCESS_TOKEN)
                            ITM["SL"][sec[i]] = 0.25*(ITM["TP"][sec[i]] - trd_entry) + trd_entry
                            UpdateStopLoss(account_id, trd_ID, ITM["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN)
                            ITM["Status"][sec[i]] = "75%"
                        elif dt - timedelta(minutes=45) > ITM["Open"][sec[i]] and c[0] > (ITM["TP"][sec[i]] - trd_entry)/3 + trd_entry and ITM["Status"][sec[i]] == "Entry":
                            ITM["SL"][sec[i]] = round(trd_entry + min(0.00025, atr/4, abs(c[0] - trd_entry)/2) + 0.00001,5)
                            if ITM["SL"][sec[i]] > trd_entry and ITM["SL"][sec[i]] < c[0]:
                                UpdateStopLoss(account_id, trd_ID, ITM["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN) 
                                ITM["Status"][sec[i]] = "BE"    
                    elif trd_side == "sell":
                        if c[0] < trd_entry - 0.75*(trd_entry - ITM["TP"][sec[i]]) and (ITM["Status"][sec[i]] == "BE" or ITM["Status"][sec[i]] == "Entry"):
                            OpenMarketOrder(account_id, sec[i], 0.75*vol, "market", "buy", 0, 0, file_nm, LIVE_ACCESS_TOKEN) 
                            ITM["SL"][sec[i]] = trd_entry - 0.25*(trd_entry - ITM["TP"][sec[i]])
                            UpdateStopLoss(account_id, trd_ID, ITM["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN)
                            ITM["Status"][sec[i]] = "75%"
                        elif dt - timedelta(minutes=45) > ITM["Open"][sec[i]] and c[0] < trd_entry - (trd_entry - ITM["TP"][sec[i]])/3 and ITM["Status"][sec[i]] == "Entry":
                            ITM["SL"][sec[i]] = round(trd_entry - min(0.00025, atr/4, abs(trd_entry - c[0])/2) + 0.00001,5)
                            if ITM["SL"][sec[i]] < trd_entry and ITM["SL"][sec[i]] > c[0]:
                                UpdateStopLoss(account_id, trd_ID, ITM["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN)
                                ITM["Status"][sec[i]] = "BE"
                else:
                    if ITM["Status"][sec[i]] == "Entry":
                        bounded = True
                        bound = max(abs(ITM["SL"][sec[i]] - trd_entry), abs(ITM["TP"][sec[i]] - trd_entry))
                        ubound = trd_entry + 0.1*bound
                        lbound = trd_entry + 0.1*bound
                        for t in range(14):
                            if c[t] > lbound and c[t] < ubound and bounded == True:
                                bounded = True
                            else:
                                bounded = False
                        if bounded == True:
                            ClosePositions(account_id, sec[i], file_nm, LIVE_ACCESS_TOKEN)
                        else: 
                            ITM["Status"][sec[i]] = "Entry-Long"
                    if trd_side == "buy":
                        if c[0] > 0.5*(ITM["TP"][sec[i]] - trd_entry) + trd_entry:
                            ClosePositions(account_id, sec[i], file_nm, LIVE_ACCESS_TOKEN)
                        elif c[0] > (ITM["TP"][sec[i]] - trd_entry)/3 + trd_entry and (ITM["Status"][sec[i]] == "BE" or ITM["Status"][sec[i]] == "Entry-Long"):
                            OpenMarketOrder(account_id, sec[i], 0.5*vol, "market", "sell", 0, 0, file_nm, LIVE_ACCESS_TOKEN)
                            ITM["SL"][sec[i]] = round(trd_entry + min(0.00025, atr/4, abs(c[0] - trd_entry)/2) + 0.00001,5)
                            if ITM["SL"][sec[i]] > trd_entry and ITM["SL"][sec[i]] < c[0]:
                                UpdateStopLoss(account_id, trd_ID, ITM["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN)
                                ITM["Status"][sec[i]] = "50%"
                    elif trd_side == "sell":
                        if c[0] < trd_entry - 0.5*(trd_entry - ITM["TP"][sec[i]]):
                            ClosePositions(account_id, sec[i], file_nm, LIVE_ACCESS_TOKEN) 
                        elif c[0] < trd_entry - (trd_entry - ITM["TP"][sec[i]])/3 and (ITM["Status"][sec[i]] == "BE" or ITM["Status"][sec[i]] == "Entry-Long"):
                            OpenMarketOrder(account_id, sec[i], 0.5*vol, "market", "buy", 0, 0, file_nm, LIVE_ACCESS_TOKEN)
                            ITM["SL"][sec[i]] = round(trd_entry - min(0.00025, atr/4, abs(trd_entry - c[0])/2) + 0.00001,5)
                            if ITM["SL"][sec[i]] < trd_entry and ITM["SL"][sec[i]] > c[0]:
                                UpdateStopLoss(account_id, trd_ID, ITM["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN)
                                ITM["Status"][sec[i]] = "50%"


##########################################################################################################
#                                                                                                        #
#                                              Indicators                                                #
#                                                                                                        #
##########################################################################################################

def Get_Pivot_Points(sec, tf, curr_price): # Update every 24hrs
    h, l, c = Get_Price(sec, tf, 2, "hlc")
    PP["PP"][sec] = round((h[1] + l[1] + c[1])/3+0.00001,5)
    PP["S1"][sec] = round(2*PP["PP"][sec] - h[1]+0.00001,5)
    PP["S2"][sec] = round(PP["PP"][sec] - h[1] + l[1]+0.00001,5)
    PP["R1"][sec] = round(2*PP["PP"][sec] - l[1]+0.00001,5)
    PP["R2"][sec] = round(PP["PP"][sec] + h[1] - l[1]+0.00001,5)
    if curr_price >= PP["R2"][sec]: # Locate current price in Pivot Points
        PP["Position"][sec] = "R2"
    elif curr_price >= PP["R1"][sec] and curr_price < PP["R2"][sec]:
        PP["Position"][sec] = "R1-R2"
    elif curr_price >= PP["PP"][sec] and curr_price < PP["R1"][sec]:
        PP["Position"][sec] = "PP-R1"
    elif curr_price >= PP["S1"][sec] and curr_price < PP["PP"][sec]:
        PP["Position"][sec] = "S1-PP"
    elif curr_price >= PP["S2"][sec] and curr_price < PP["S1"][sec]:
        PP["Position"][sec] = "S2-S1"
    elif curr_price < PP["S2"][sec]:
        PP["Position"][sec] = "S2"
    pos = PP["Position"][sec]
    if pos == "R2":
        s, r = PP[pos][sec], 2*curr_price
    elif pos == "S2":
        s, r = 0, PP[pos][sec]
    elif pos != "":
        s, r = PP[pos[:2]][sec], PP[pos[-2:]][sec]
    return s, r # Return support and resistance

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

def SMA(c, n, offset):
    sma_val = 0.0
    for i in range(n):
        sma_val += c[i + offset]
    return sma_val/n

def STDEV(c, n, offset):
    ma = SMA(c, n, offset)
    sd_val = 0.0
    for i in range(n):
        sd_val += (ma - c[i + offset])**2 
    return (sd_val/(n-1))**(0.5)

def CORREL(c1, c2):
    ma1 = SMA(c1,len(c1))
    ma2 = SMA(c2,len(c2))
    for i in range(len(c1)):
        exy += (c1[i] - ma1)*(c2[i]-ma2)
    exy = exy/len(c1)