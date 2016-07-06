# This script handles executing specific trading plans and all related calculaitons
import requests
import json
from array import *
from Settings import PRICE_DOMAIN, ACCOUNT_DOMAIN, LIVE_ACCESS_TOKEN, ACCOUNT_ID, STRT, STRO, STRH, STRL, STRC, STRV, STRCO
import httplib
import urllib
from QF_Functions import *
from QF_Optimizer import *
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

##########################################################################################################
#                                                                                                        #
#                                              Strategies                                                #
#                                                                                                        #
##########################################################################################################

def PivotPointBreakout(account_id, sec, vol, tf, file_nm):
    for i in range(len(sec)):
        SaveToLog(main_log, "Collecting PPB data for " + sec[i])
        m15h, m15l, m15c = Get_Price(sec[i], tf[1], 101, "hlc")
        ma = SMA(m15c, 50)
        sd = STDEV(m15c,50)
        Z = (m15c[0] - ma)/sd
        atr = Get_ATR(m15h, m15l, m15c, sec[i])
        m5c = Get_Price(sec[i], tf[0], 3, "c")
        s, r = Get_Pivot_Points(sec[i], tf[2], m5c[0])
        Open_Units = GetOpenUnits(account_id, sec[i], sec)
        dt = datetime.now()
        if Open_Units == 0 and (dt.hour <= 18 and dt.hour >= 8):
            if abs(Z) > 0.1 and abs(Z) < 1.5:
                if m5c[0] < r and m5c[1] < r and m5c[2] > r and ma > r:
                    SaveToLog(main_log, "PPB: Sell " + sec[i])
                    PPB["SL"][sec[i]] = round(m5c[0] + atr + 0.00001,5)
                    TP = round(m5c[0] - 3*atr - 0.00001,5)
                    OpenMarketOrder(account_id, sec[i], vol, "market", "sell", TP, PPB["SL"][sec[i]], file_nm)
                elif m5c[0] > s and m5c[1] > s and m5c[2] < s and ma < s:
                    SaveToLog(main_log, "PPB: Buy " + sec[i])
                    PPB["SL"][sec[i]] = round(m5c[0] - atr - 0.00001,5)
                    TP = round(m5c[0] + 3*atr + 0.00001,5)
                    OpenMarketOrder(account_id, sec[i], vol, "market", "buy", TP, PPB["SL"][sec[i]], file_nm)
            elif abs(Z) > 1.5:
                if m5c[0] < r and m5c[1] < r and m5c[2] > r and ma < r and PP["Postion"][sec[i]] == ("PP-R1" or "R1-R2"):
                    SaveToLog(main_log, "PPB: Sell " + sec[i])
                    PPB["SL"][sec[i]] = round(m5c[0] + atr + 0.00001,5)
                    TP = round(m5c[0] - 3*atr - 0.00001,5)
                    OpenMarketOrder(account_id, sec[i], vol, "market", "sell", TP, PPB["SL"][sec[i]], file_nm)
                elif m5c[0] > s and m5c[1] > s and m5c[2] < s and ma > s and PP["Postion"][sec[i]] == ("S1-PP" or "S2-S1"):
                    SaveToLog(main_log, "PPB: Buy " + sec[i])
                    PPB["SL"][sec[i]] = round(m5c[0] - atr - 0.00001,5)
                    TP = round(m5c[0] + 3*atr + 0.00001,5)
                    OpenMarketOrder(account_id, sec[i], vol, "market", "buy", TP, PPB["SL"][sec[i]], file_nm)
        elif Open_Units != 0:
            SaveToLog(main_log, "PPB: updating stops for " + sec[i])
            Open_Trades = GetOpenTrades(account_id, sec[i])
            for positions in Open_Trades["trades"]:
                trd_ID = positions["id"]
                trd_entry = float(positions["price"])
                trd_side = positions["side"]
                if trd_side == "buy":
                    if m5c[0] > trd_entry + atr/2:
                        PPB["SL"][sec[i]] = round(trd_entry + 0.00001,5)
                        UpdateStopLoss(account_id, trd_ID, PPB["SL"][sec[i]], file_nm)                  
                    elif m5c[0] > trd_entry + atr:
                        PPB["SL"][sec[i]] = round(max(PPB["SL"][sec[i]], m5c[0] + atr/2) + 0.00001,5)
                        UpdateStopLoss(account_id, trd_ID, PPB["SL"][sec[i]], file_nm)
                elif trd_side == "sell":
                    if m5c[0] < trd_entry - atr/2:
                        PPB["SL"][sec[i]] = round(trd_entry - 0.00001,5)
                        UpdateStopLoss(account_id, trd_ID, PPB["SL"][sec[i]], file_nm)
                    elif m5c[0] < trd_entry - atr:
                        PPB["SL"][sec[i]] = round(min(PPB["SL"][sec[i]], m5c[0] - atr/2) - 0.00001,5)
                        UpdateStopLoss(account_id, trd_ID, PPB["SL"][sec[i]], file_nm)

def MovingAverageContrarian(account_id, sec, vol, tf, file_nm):
    for i in range(len(sec)):
        SaveToLog(main_log, "Collecting MAC data for " + sec[i])
        c = Get_Price(sec[i], tf, 50, "c")
        ma = SMA(c,50)
        sd = STDEV(c,50)
        Z = (c[0] - ma)/sd
        Open_Units = GetOpenUnits(account_id, sec[i], sec)
        if Open_Units == 0:
            SaveToLog(main_log, "Checking MAC signals for " + sec[i])
            if Z > 2:
                SaveToLog(main_log, "MAC: Sell " + sec[i])
                SL = round(c[0] + sd/2 + 0.00001,5)
                TP = round(c[0] - sd/2 - 0.00001,5)
                OpenMarketOrder(account_id, sec[i], vol, "market", "sell", TP, SL, file_nm)
            elif Z < -2:
                SaveToLog(main_log, "MAC: Buy " + sec[i])
                SL = round(c[0] - sd/2 - 0.00001,5)
                TP = round(c[0] + sd/2 + 0.00001,5)
                OpenMarketOrder(account_id, sec[i], vol, "market", "buy", TP, SL, file_nm)

def BusRide(account_id, sec, vol, tf, file_nm):
    for i in range(len(sec)):
        SaveToLog(main_log, "Collecting BusRide data for " + sec[i])
        if tf == "D":
            sell_tp, buy_tp = Get_Pivot_Points(sec, "D", c[0])
        elif tf == "M15":
            sell_tp = c[0]/1.0025
            buy_tp = c[0]*1.0025
        c = Get_Price(sec[i], tf, 51, "c")
        Open_Units = GetOpenUnits(account_id, sec[i], sec)
        lvl_min = round(c[2],2)
        lvl_max = round(c[2],2) + 0.01 
        ma = SMA(c, 50)      
        if Open_Units == 0:
            SaveToLog(main_log, "Checking Bus Ride signals for " + sec[i])
            if c[2] > lvl_min and c[0] < lvl_min and ma > lvl_min:
                SaveToLog(main_log, "Bus Ride: Sell " + sec[i])
                SL = round(c[2] - 0.00001,5)
                OpenMarketOrder(account_id, sec[i], vol, "market", "sell", sell_tp, SL, file_nm)
            elif c[2] < lvl_max and c[0] > lvl_max and ma < lvl_max:
                SaveToLog(main_log, "Bus Ride: Buy " + sec[i])
                SL = round(c[2] + 0.00001,5)
                OpenMarketOrder(account_id, sec[i], vol, "market", "buy", buy_tp, SL, file_nm)

def IntraTrend(account_id, sec, vol, tf, file_nm):
    for i in range(len(sec)):
        SaveToLog(main_log, "Collecting IT data for " + sec[i])
        c = Get_Price(sec[i], tf, 51, "c")
        SMA10 = SMA(c,10)
        SMA21 = SMA(c,21)
        SMA50 = SMA(c,50)
        Open_Units = GetOpenUnits(account_id, sec[i], sec)
        if Open_Units == 0:
            if c[0] > SMA10 and c[0] < SMA21 and c[0] < SMA50:
                SaveToLog(main_log, "IT: Sell " + sec[i])
                IT["TP"][sec[i]] = round(c[0] - 0.9*abs(c[0] - SMA50), 5)
                IT["SL"][sec[i]] = round(SMA50, 5)
                OpenMarketOrder(account_id, sec[i], vol, "market", "sell", IT["TP"][sec[i]], IT["SL"][sec[i]], file_nm)
                IT["counter"][sec[i]] = -1
                IT["BEV"][sec[i]] = 0
            elif c[0] < SMA10 and c[0] > SMA21 and c[0] > SMA50:
                IT["TP"][sec[i]] = round(c[0] + 0.9*abs(c[0] - SMA50), 5)
                IT["SL"][sec[i]] = round(SMA50, 5)
                SaveToLog(main_log, "IT: Buy " + sec[i])
                OpenMarketOrder(account_id, sec[i], vol, "market", "buy", IT["TP"][sec[i]], IT["SL"][sec[i]], file_nm)
                IT["counter"][sec[i]] = -1
                IT["BEV"][sec[i]] = 0
        elif Open_Units != 0:
            SaveToLog(main_log, "IT: updating stops for " + sec[i])
            Open_Trades = GetOpenTrades(account_id, sec[i])
            for positions in Open_Trades["trades"]:
                trd_ID = positions["id"]
                trd_entry = float(positions["price"])
                trd_side = positions["side"]
                trd_size = positions["units"]
                if tf == "D":
                    if c[0] < SMA21/1.0025 and c[0] < trd_entry and IT["counter"][sec[i]] == -1 and Open_Units == vol:
                        IT["SL"][sec[i]] = round(trd_entry - 0.00001, 5)
                        UpdateStopLoss(account_id, trd_ID, IT["SL"][sec[i]], file_nm)
                        IT["counter"][sec[i]] = 0
                    elif c[0] < ((SMA21+SMA50)/2)/1.0025 and IT["counter"][sec[i]] == -1 and Open_Units > vol:
                        IT["SL"][sec[i]] = round((SMA21 + SMA50)/2, 5)
                        UpdateStopLoss(account_id, trd_ID, IT["SL"][sec[i]], file_nm)
                        IT["counter"][sec[i]] = 0
                elif tf == "M15":
                    if c[0] < SMA21/1.0025 and c[0] < trd_entry and IT["counter"][sec[i]] == -1 and Open_Units == vol:
                        IT["SL"][sec[i]] = round(trd_entry - 0.00001, 5)
                        UpdateStopLoss(account_id, trd_ID, IT["SL"][sec[i]], file_nm)
                        IT["counter"][sec[i]] = 0
                    elif c[0] < SMA21/1.0025 and c[0] < trd_entry and IT["counter"][sec[i]] == -1 and Open_Units > vol:
                        IT["SL"][sec[i]] = round(SMA21, 5)
                        UpdateStopLoss(account_id, trd_ID, IT["SL"][sec[i]], file_nm)
                        IT["counter"][sec[i]] = 0
                elif (trd_side == "buy" and c[0] < SMA50) or (trd_side == "sell" and c[0] > SMA50):
                    ClosePositions(account_id, sec[i], file_nm)
            if IT["counter"][sec[i]] >= 3 and abs(c[2] - c[0]) >= 0.00075:
                SaveToLog(main_log, "IT: Scaling into " + sec[i])
                vol_adj = vol*(abs(IT["SL"][sec[i]] - SMA10)/abs(IT["SL"][sec[i]] - c[0]))
                if Open_Units < 5*vol and c[0] > c[1] and c[1] > c[2]:
                    OpenMarketOrder(account_id, sec[i], vol_adj, "market", "buy", IT["TP"][sec[i]], SMA10, file_nm)
                elif Open_Units < 5*vol and c[0] < c[1] and c[1] < c[2]:
                    OpenMarketOrder(account_id, sec[i], vol_adj, "market", "sell", IT["TP"][sec[i]], SMA10, file_nm)
                IT_BreakEven(account_id, sec[i], trd_entry, c[0], vol, vol_adj, file_nm)
                IT["counter"][sec[i]] = 0
            elif IT["counter"][sec[i]] != -1:
                IT["counter"][sec[i]] += 1 

def CableSnap(account_id, sec, vol, tf, file_nm):
    for i in range(len(sec)):
        SaveToLog(main_log, "Collecting CableSnap data for " + sec[i])
        c = Get_Price(sec[i], tf, 51, "c")
        SMA10 = SMA(c,10)
        SMA21 = SMA(c,21)
        SMA50 = SMA(c,50)
        Open_Units = GetOpenUnits(account_id, sec[i], sec)
        if Open_Units <= 15000 - vol:
            if c[0] > SMA10 and c[0] < SMA21 and c[0] < SMA50:
                SaveToLog(main_log, "CS: Sell " + sec[i])
                if tf == "D":
                    TP = round(c[0] - 2*abs(c[0] - SMA50), 5)
                    SL = round(SMA50, 5)
                elif tf == "M15":
                    TP = round(c[0] - abs(c[0] - SMA50), 5)
                    SL = round(SMA50, 5)
                OpenMarketOrder(account_id, sec[i], vol, "market", "sell", TP, SL, file_nm)
        elif Open_Units != 0:
            SaveToLog(main_log, "CS: updating stops for " + sec[i])
            Open_Trades = GetOpenTrades(account_id, sec[i])
            for positions in Open_Trades["trades"]:
                trd_ID = positions["id"]
                trd_entry = float(positions["price"])
                trd_side = positions["side"]
                trd_size = positions["units"]
                if tf == "D":
                    if c[0] < SMA21/1.0025 and c[0] < trd_entry and Open_Units == vol:
                        SL = round(trd_entry - 0.00001, 5)
                        UpdateStopLoss(account_id, trd_ID, SL, file_nm)
                    elif c[0] < ((SMA21+SMA50)/2)/1.0025 and Open_Units > vol:
                        SL = round((SMA21 + SMA50)/2, 5)
                        UpdateStopLoss(account_id, trd_ID, SL, file_nm)
                elif tf == "M15":
                    if c[0] < SMA21/1.0025 and c[0] < trd_entry and Open_Units == vol:
                        SL = round(trd_entry - 0.00001, 5)
                        UpdateStopLoss(account_id, trd_ID, SL, file_nm)
                    elif c[0] < SMA21/1.0025 and c[0] < trd_entry and Open_Units > vol:
                        SL = round(SMA21, 5)
                        UpdateStopLoss(account_id, trd_ID, SL, file_nm)
                elif trd_side == "sell" and c[0] > SMA50:
                    ClosePositions(account_id, sec[i], file_nm)

##########################################################################################################
#                                                                                                        #
#                                              Indicators                                                #
#                                                                                                        #
##########################################################################################################

def Get_Pivot_Points(sec, tf, curr_price): # Update every 24hrs
    h, l, c = Get_Price(sec, tf, 2, "hlc")
    PP["PP"][sec] = (h[1] + l[1] + c[1])/3
    PP["S1"][sec] = 2*PP["PP"][sec] - h[1]
    PP["S2"][sec] = PP["PP"][sec] - h[1] + l[1]
    PP["R1"][sec] = 2*PP["PP"][sec] - l[1]
    PP["R2"][sec] = PP["PP"][sec] + h[1] - l[1]
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