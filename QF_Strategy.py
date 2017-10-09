import requests
import json
from array import *
from Settings import LIVE_ACCESS_TOKEN, STRT, STRO, STRH, STRL, STRC, STROA, STRHA, STRLA, STRCA, STROB, STRHB, STRLB, STRCB, STRV, STRCO
import httplib
import urllib
from QF_Optimizer import *
from QF_Functions import *
from datetime import datetime, timedelta
import time
import sys
main_log = "QF.txt"

hr = [0,4,8,12,16,20]

TOD_Params = {}
TOD_Params['AUD_NZD'] = {'Buy': [5], 'Sell': [13]}
TOD_Params['GBP_AUD'] = {'Buy': [7], 'Sell': [6, 12, 18]}
TOD_Params['AUD_CAD'] = {'Buy': [4, 23], 'Sell': [13, 20]}
TOD_Params['EUR_CAD'] = {'Buy': [13, 23], 'Sell': [10]}
TOD_Params['EUR_NZD'] = {'Buy': [3], 'Sell': [5, 15]}
TOD_Params['EUR_GBP'] = {'Buy': [2, 5, 18, 22], 'Sell': []}
TOD_Params['GBP_USD'] = {'Buy': [2, 15], 'Sell': [6, 10]}
TOD_Params['AUD_USD'] = {'Buy': [1, 4, 17], 'Sell': [14, 20]}
TOD_Params['EUR_USD'] = {'Buy': [1, 15], 'Sell': [10]}
TOD_Params['USD_CAD'] = {'Buy': [], 'Sell': [2, 17]}
TOD_Params['GBP_NZD'] = {'Buy': [], 'Sell': [4, 10, 23]}
TOD_Params['NZD_USD'] = {'Buy': [4, 14, 19], 'Sell': [10]}
TOD_Params['GBP_CAD'] = {'Buy': [8], 'Sell': [6, 11, 18, 21]}
TOD_Params['EUR_AUD'] = {'Buy': [13, 20], 'Sell': [1, 10]}
TOD_Params['NZD_CAD'] = {'Buy': [4, 8, 23], 'Sell': []}

def TimeofDay(account_id, sec, vol, tf, file_nm):
    for s in sec:
        SaveToLog(main_log, "Collecting TOD data for " + s)
        c = Get_Price(s, tf, 5, "c", "midpoint")
        dt = datetime.now()
        Open_Units = GetOpenUnits(account_id, s, sec, LIVE_ACCESS_TOKEN)
        if Open_Units == 0:
            if (dt.hour in TOD_Params[s]['Sell']):
                SaveToLog(main_log, "TOD: Sell " + s)
                SL = round(c[0] + 0.010000001,5)
                TP = round(c[0] - 0.01000001,5)
                OpenMarketOrder(account_id, s, vol, "market", "sell", TP, SL, file_nm, LIVE_ACCESS_TOKEN)
                TOD["Open"][s] = dt
                TOD["Status"][s] = "Entry"
            elif (dt.hour in TOD_Params[s]['Buy']):
                SaveToLog(main_log, "TOD: Buy " + s)
                SL = round(c[0] - 0.010000001,5)
                TP = round(c[0] + 0.01000001,5)
                OpenMarketOrder(account_id, s, vol, "market", "buy", TP, SL, file_nm, LIVE_ACCESS_TOKEN)
                TOD["Open"][s] = dt
                TOD["Status"][s] = "Entry"
        elif Open_Units != 0:
            SaveToLog(main_log, "TOD: Managing trade for " + s)
            if TOD["Status"][s] == "":
                TOD["Status"][s] = "Entry"
                TOD["Open"][s] = dt
            Open_Trades = GetOpenTrades(account_id, s, LIVE_ACCESS_TOKEN)
            for positions in Open_Trades["trades"]:
                trd_ID = positions["id"]
                trd_entry = float(positions["price"])
                trd_side = positions["side"]
                if dt - timedelta(minutes=180) > TOD["Open"][s]:
                    ClosePositions(account_id, s, file_nm, LIVE_ACCESS_TOKEN)

def PivotPointBreakout(account_id, sec, vol, tf, file_nm):
    for i in range(len(sec)):
        SaveToLog(main_log, "Collecting PPB data for " + sec[i])
        m5c = Get_Price(sec[i], tf[0], 7, "c", "midpoint")
        Open_Units = PPB["Units"][sec[i]]
        dt = datetime.now()
        ma = Indicators[sec[i]]["SMA210"]
        atr = Indicators[sec[i]]["ATR"]
        s = Indicators[sec[i]]["s"]
        r = Indicators[sec[i]]["r"]
        z = Indicators[sec[i]]["Z"]
        mx4 = Indicators[sec[i]]["Max 4"]
        mx16 = Indicators[sec[i]]["Max 16"]
        mn4 = Indicators[sec[i]]["Min 4"]
        mn16 = Indicators[sec[i]]["Min 16"]
        if Open_Units == 0 and (dt.hour <= 12 and dt.hour >= 5) and Strat["PPB"]["Stop"] == 0:
            PPB["Open"][sec[i]] = datetime.now()
            PPB["Status"][sec[i]] = ""
            if m5c[0] < r and m5c[1] < r and m5c[2] > r and ma > r:
                if m5c[0] < mn4 or m5c[0] < mn16 or z < 0:
                    SaveToLog(main_log, "PPB: Sell " + sec[i])
                    PPB["SL"][sec[i]] = round(m5c[0] + atr + 0.00001,5) # atr*1.5
                    PPB["TP"][sec[i]] = round(m5c[0] - min(0.00151, 1.5*atr) - 0.00001,5) # atr or 0.0012
                    OpenMarketOrder(account_id, sec[i], vol, "market", "sell", PPB["TP"][sec[i]], PPB["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN)
                    PPB["Open"][sec[i]] = dt
                    PPB["Status"][sec[i]] = "Entry"
            elif m5c[0] > s and m5c[1] > s and m5c[2] < s and ma < s:
                if m5c[0] > mx4 or m5c[0] > mx16 or z > 0:
                    SaveToLog(main_log, "PPB: Buy " + sec[i])
                    PPB["SL"][sec[i]] = round(m5c[0] - atr - 0.00001,5) # atr*1.5
                    PPB["TP"][sec[i]] = round(m5c[0] + min(0.00151, 1.5*atr) + 0.00001,5) # atr or 0.0012
                    OpenMarketOrder(account_id, sec[i], vol, "market", "buy", PPB["TP"][sec[i]], PPB["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN)
                    PPB["Open"][sec[i]] = dt
                    PPB["Status"][sec[i]] = "Entry"
        elif Open_Units != 0:
            SaveToLog(main_log, "PPB: Managing trade for " + sec[i])
            if PPB["Status"][sec[i]] == "":
                PPB["Status"][sec[i]] = "Entry"
                PPB["Open"][sec[i]] = dt
            Open_Trades = GetOpenTrades(account_id, sec[i], LIVE_ACCESS_TOKEN)
            for positions in Open_Trades["trades"]:
                trd_ID = positions["id"]
                trd_entry = float(positions["price"])
                trd_side = positions["side"]
                if dt - timedelta(minutes=30) < PPB["Open"][sec[i]]:
                    if trd_side == "buy":
                        if m5c[0] > 0.75*(PPB["TP"][sec[i]] - trd_entry) + trd_entry and (PPB["Status"][sec[i]] == "BE" or PPB["Status"][sec[i]] == "Entry"):
                            SaveToLog(main_log, "PPB: 75% " + sec[i])
                            OpenMarketOrder(account_id, sec[i], int(round(0.75*vol,0)), "market", "sell", 0, 0, file_nm, LIVE_ACCESS_TOKEN)
                            PPB["SL"][sec[i]] = round(0.25*(PPB["TP"][sec[i]] - trd_entry) + trd_entry + 0.00001, 5)
                            UpdateStopLoss(account_id, trd_ID, PPB["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN)
                            PPB["Status"][sec[i]] = "75%"
                        elif dt - timedelta(minutes=15) > PPB["Open"][sec[i]] and m5c[0] > (PPB["TP"][sec[i]] - trd_entry)/3 + trd_entry and PPB["Status"][sec[i]] == "Entry":
                            SaveToLog(main_log, "PPB: BE " + sec[i])
                            PPB["SL"][sec[i]] = round(trd_entry + min(0.00025, atr/4, abs(m5c[0] - trd_entry)/2) + 0.00001, 5)
                            UpdateStopLoss(account_id, trd_ID, PPB["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN)
                            PPB["Status"][sec[i]] = "BE"
                    elif trd_side == "sell":
                        if m5c[0] < trd_entry - 0.75*(trd_entry - PPB["TP"][sec[i]]) and (PPB["Status"][sec[i]] == "BE" or PPB["Status"][sec[i]] == "Entry"):
                            SaveToLog(main_log, "PPB: 75% " + sec[i])
                            OpenMarketOrder(account_id, sec[i], int(round(0.75*vol,0)), "market", "buy", 0, 0, file_nm, LIVE_ACCESS_TOKEN) 
                            PPB["SL"][sec[i]] = round(trd_entry - 0.25*(trd_entry - PPB["TP"][sec[i]]) - 0.00001, 5)
                            UpdateStopLoss(account_id, trd_ID, PPB["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN)
                            PPB["Status"][sec[i]] = "75%"
                        elif dt - timedelta(minutes=15) > PPB["Open"][sec[i]] and m5c[0] < trd_entry - (trd_entry - PPB["TP"][sec[i]])/3 and PPB["Status"][sec[i]] == "Entry":
                            SaveToLog(main_log, "PPB: BE " + sec[i])
                            PPB["SL"][sec[i]] = round(trd_entry - min(0.00025, atr/4, abs(trd_entry - m5c[0])/2) + 0.00001, 5)
                            UpdateStopLoss(account_id, trd_ID, PPB["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN)
                            PPB["Status"][sec[i]] = "BE"                            
                else:
                    if PPB["Status"][sec[i]] == "Entry":
                        SaveToLog(main_log, "PPB: Flat at Entry " + sec[i])
                        bounded = True
                        bound = max(abs(PPB["SL"][sec[i]] - trd_entry), abs(PPB["TP"][sec[i]] - trd_entry))
                        ubound = trd_entry + 0.1*bound
                        lbound = trd_entry + 0.1*bound
                        for t in range(6):
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
                            SaveToLog(main_log, "PPB: Close " + sec[i])
                            ClosePositions(account_id, sec[i], file_nm, LIVE_ACCESS_TOKEN)
                        elif m5c[0] > (PPB["TP"][sec[i]] - trd_entry)/3 + trd_entry and (PPB["Status"][sec[i]] == "BE" or PPB["Status"][sec[i]] == "Entry-Long"):
                            SaveToLog(main_log, "PPB: 50% " + sec[i])
                            OpenMarketOrder(account_id, sec[i], int(round(0.5*vol,0)), "market", "sell", 0, 0, file_nm, LIVE_ACCESS_TOKEN)
                            try:
                                PPB["SL"][sec[i]] = round(trd_entry + min(0.00025, atr/4, abs(m5c[0] - trd_entry)/2) + 0.00001, 5)
                                UpdateStopLoss(account_id, trd_ID, PPB["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN)
                                PPB["Status"][sec[i]] = "50%"
                            except:
                                e = sys.exc_info()[0]
                                SaveToLog(main_log, "PPB: Buy 50% " + sec[i] + " " + str(e))
                    elif trd_side == "sell":
                        if m5c[0] < trd_entry - 0.5*(trd_entry - PPB["TP"][sec[i]]):
                            SaveToLog(main_log, "PPB: Close " + sec[i])
                            ClosePositions(account_id, sec[i], file_nm, LIVE_ACCESS_TOKEN) 
                        elif m5c[0] < trd_entry - (trd_entry - PPB["TP"][sec[i]])/3 and (PPB["Status"][sec[i]] == "BE" or PPB["Status"][sec[i]] == "Entry-Long"):
                            SaveToLog(main_log, "PPB: 50% " + sec[i])
                            OpenMarketOrder(account_id, sec[i], int(round(0.5*vol,0)), "market", "buy", 0, 0, file_nm, LIVE_ACCESS_TOKEN)
                            try:
                                PPB["SL"][sec[i]] = round(trd_entry - min(0.00025, atr/4, abs(trd_entry - m5c[0])/2) + 0.00001, 5)
                                UpdateStopLoss(account_id, trd_ID, PPB["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN)
                                PPB["Status"][sec[i]] = "50%"
                            except:
                                e = sys.exc_info()[0]
                                SaveToLog(main_log, "PPB: Sell 50% " + sec[i] + " " + str(e))

def MovingAverageContrarian(account_id, sec, vol, tf, file_nm):
    for i in range(len(sec)):
        SaveToLog(main_log, "Collecting MAC data for " + sec[i])
        c = Get_Price(sec[i], tf, 51, "c", "midpoint")
        dt = datetime.now()
        ma1 = SMA(c,50,1)
        sd1 = STDEV(c,50,1)
        ma0 = SMA(c,50,0)
        sd0 = STDEV(c,50,0)
        Z1 = (c[1] - ma1)/sd1
        Z0 = (c[0] - ma0)/sd0
        Open_Units = GetOpenUnits(account_id, sec[i], sec, LIVE_ACCESS_TOKEN)
        if Open_Units == 0:
            if Z1 > 2.5 and Z0 < 2.5:
                SaveToLog(main_log, "MAC: Sell " + sec[i])
                SL = round(c[0] + 0.010000001,5)
                TP = round(c[0] - 0.005000001,5)
                OpenMarketOrder(account_id, sec[i], vol, "market", "sell", TP, SL, file_nm, LIVE_ACCESS_TOKEN)
                MAC["Open"][sec[i]] = dt
                MAC["Status"][sec[i]] = "Entry"
            elif Z1 < -2.5 and Z0 > -2.5:
                SaveToLog(main_log, "MAC: Buy " + sec[i])
                SL = round(c[0] - 0.010000001,5)
                TP = round(c[0] + 0.005000001,5)
                OpenMarketOrder(account_id, sec[i], vol, "market", "buy", TP, SL, file_nm, LIVE_ACCESS_TOKEN)
                MAC["Open"][sec[i]] = dt
                MAC["Status"][sec[i]] = "Entry"
        elif Open_Units != 0:
            SaveToLog(main_log, "MAC: Managing trade for " + sec[i])
            if MAC["Status"][sec[i]] == "":
                MAC["Status"][sec[i]] = "Entry"
                MAC["Open"][sec[i]] = dt
            Open_Trades = GetOpenTrades(account_id, sec[i], LIVE_ACCESS_TOKEN)
            for positions in Open_Trades["trades"]:
                trd_ID = positions["id"]
                trd_entry = float(positions["price"])
                trd_side = positions["side"]
                if MAC["Status"][sec[i]] == "Entry":
                    if trd_side == "buy" and c[0] - trd_entry > 0.002:
                        SaveToLog(main_log, "MAC: BE " + sec[i])
                        OpenMarketOrder(account_id, sec[i], int(round(0.5*vol,0)), "market", "sell", 0, 0, file_nm, LIVE_ACCESS_TOKEN)
                        MAC["SL"][sec[i]] = round(trd_entry + 0.00201, 5)
                        UpdateStopLoss(account_id, trd_ID, MAC["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN)
                        MAC["Status"][sec[i]] = "BE"
                    elif trd_side == "sell" and trd_entry - c[0] > 0.002:
                        SaveToLog(main_log, "MAC: BE " + sec[i])
                        OpenMarketOrder(account_id, sec[i], int(round(0.5*vol,0)), "market", "buy", 0, 0, file_nm, LIVE_ACCESS_TOKEN)
                        MAC["SL"][sec[i]] = round(trd_entry - 0.00201, 5)
                        UpdateStopLoss(account_id, trd_ID, MAC["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN)
                        MAC["Status"][sec[i]] = "BE"

def BollingerBandBreakout1(account_id, sec, vol, tf, file_nm):
    for i in range(len(sec)):
        SaveToLog(main_log, "Collecting BBB data for " + sec[i])
        c = Get_Price(sec[i], tf, 51, "c", "midpoint")
        dt = datetime.now()
        ma2 = SMA(c,10,2)
        sd2 = STDEV(c,10,2)
        ma1 = SMA(c,10,1)
        sd1 = STDEV(c,10,1)
        Z2 = (c[2] - ma2)/sd2
        Z1 = (c[1] - ma1)/sd1
        Open_Units = GetOpenUnits(account_id, sec[i], sec, LIVE_ACCESS_TOKEN)
        if Open_Units == 0:
            if Z2 < 2.0 and Z1 > 2.0 and c[0] > c[i-1]:
                SaveToLog(main_log, "BBB: Buy " + sec[i])
                SL = round(c[0] - 0.010000001,5)
                TP = round(c[0] + 0.005000001,5)
                OpenMarketOrder(account_id, sec[i], vol, "market", "buy", TP, SL, file_nm, LIVE_ACCESS_TOKEN)
                BBB1["Open"][sec[i]] = dt
                BBB1["Status"][sec[i]] = "Entry"
            if Z2 > -2.0 and Z1 < -2.0 and c[0] < c[i-1]:
                SaveToLog(main_log, "BBB: Sell " + sec[i])
                SL = round(c[0] + 0.010000001,5)
                TP = round(c[0] - 0.005000001,5)
                OpenMarketOrder(account_id, sec[i], vol, "market", "sell", TP, SL, file_nm, LIVE_ACCESS_TOKEN)
                BBB1["Open"][sec[i]] = dt
                BBB1["Status"][sec[i]] = "Entry"
        elif Open_Units != 0:
            SaveToLog(main_log, "BBB: Managing trade for " + sec[i])
            if BBB1["Status"][sec[i]] == "":
                BBB1["Status"][sec[i]] = "Entry"
                BBB1["Open"][sec[i]] = dt
            Open_Trades = GetOpenTrades(account_id, sec[i], LIVE_ACCESS_TOKEN)
            for positions in Open_Trades["trades"]:
                trd_ID = positions["id"]
                trd_entry = float(positions["price"])
                trd_side = positions["side"]
                if BBB1["Status"][sec[i]] == "Entry":
                    if trd_side == "buy" and c[0] - trd_entry > 0.002:
                        SaveToLog(main_log, "BBB: BE " + sec[i])
                        OpenMarketOrder(account_id, sec[i], int(round(0.5*vol,0)), "market", "sell", 0, 0, file_nm, LIVE_ACCESS_TOKEN)
                        BBB1["SL"][sec[i]] = round(trd_entry + 0.00201, 5)
                        UpdateStopLoss(account_id, trd_ID, BBB1["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN)
                        BBB1["Status"][sec[i]] = "BE"
                    elif trd_side == "sell" and trd_entry - c[0] > 0.002:
                        SaveToLog(main_log, "BBB: BE " + sec[i])
                        OpenMarketOrder(account_id, sec[i], int(round(0.5*vol,0)), "market", "buy", 0, 0, file_nm, LIVE_ACCESS_TOKEN)
                        BBB1["SL"][sec[i]] = round(trd_entry - 0.00201, 5)
                        UpdateStopLoss(account_id, trd_ID, BBB1["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN)
                        BBB1["Status"][sec[i]] = "BE"

def BollingerBandBreakout2(account_id, sec, vol, tf, file_nm):
    for i in range(len(sec)):
        SaveToLog(main_log, "Collecting BBB data for " + sec[i])
        c = Get_Price(sec[i], tf, 55, "c", "midpoint")
        dt = datetime.now()
        ma2 = SMA(c,50,2)
        sd2 = STDEV(c,50,2)
        ma1 = SMA(c,50,1)
        sd1 = STDEV(c,50,1)
        Z2 = (c[2] - ma2)/sd2
        Z1 = (c[1] - ma1)/sd1
        Open_Units = GetOpenUnits(account_id, sec[i], sec, LIVE_ACCESS_TOKEN)
        if Open_Units == 0:
            if Z2 < 1.0 and Z1 > 1.0 and c[0] > c[i-1]:
                SaveToLog(main_log, "BBB: Buy " + sec[i])
                SL = round(c[0] - 0.010000001,5)
                TP = round(c[0] + 0.005000001,5)
                OpenMarketOrder(account_id, sec[i], vol, "market", "buy", TP, SL, file_nm, LIVE_ACCESS_TOKEN)
                BBB2["Open"][sec[i]] = dt
                BBB2["Status"][sec[i]] = "Entry"
            if Z2 > -1.0 and Z1 < -1.0 and c[0] < c[i-1]:
                SaveToLog(main_log, "BBB: Sell " + sec[i])
                SL = round(c[0] + 0.010000001,5)
                TP = round(c[0] - 0.005000001,5)
                OpenMarketOrder(account_id, sec[i], vol, "market", "sell", TP, SL, file_nm, LIVE_ACCESS_TOKEN)
                BBB2["Open"][sec[i]] = dt
                BBB2["Status"][sec[i]] = "Entry"
        elif Open_Units != 0:
            SaveToLog(main_log, "BBB: Managing trade for " + sec[i])
            if BBB2["Status"][sec[i]] == "":
                BBB2["Status"][sec[i]] = "Entry"
                BBB2["Open"][sec[i]] = dt
            Open_Trades = GetOpenTrades(account_id, sec[i], LIVE_ACCESS_TOKEN)
            for positions in Open_Trades["trades"]:
                trd_ID = positions["id"]
                trd_entry = float(positions["price"])
                trd_side = positions["side"]
                if BBB2["Status"][sec[i]] == "Entry":
                    if trd_side == "buy" and c[0] - trd_entry > 0.002:
                        SaveToLog(main_log, "BBB: BE " + sec[i])
                        OpenMarketOrder(account_id, sec[i], int(round(0.5*vol,0)), "market", "sell", 0, 0, file_nm, LIVE_ACCESS_TOKEN)
                        BBB2["SL"][sec[i]] = round(trd_entry + 0.00201, 5)
                        UpdateStopLoss(account_id, trd_ID, BBB2["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN)
                        BBB2["Status"][sec[i]] = "BE"
                    elif trd_side == "sell" and trd_entry - c[0] > 0.002:
                        SaveToLog(main_log, "BBB: BE " + sec[i])
                        OpenMarketOrder(account_id, sec[i], int(round(0.5*vol,0)), "market", "buy", 0, 0, file_nm, LIVE_ACCESS_TOKEN)
                        BBB2["SL"][sec[i]] = round(trd_entry - 0.00201, 5)
                        UpdateStopLoss(account_id, trd_ID, BBB2["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN)
                        BBB2["Status"][sec[i]] = "BE"

def BollingerBandBreakout3(account_id, sec, vol, tf, file_nm):
    for i in range(len(sec)):
        SaveToLog(main_log, "Collecting BBB data for " + sec[i])
        c = Get_Price(sec[i], tf, 211, "c", "midpoint")
        dt = datetime.now()
        ma2 = SMA(c,200,2)
        sd2 = STDEV(c,200,2)
        ma1 = SMA(c,200,1)
        sd1 = STDEV(c,200,1)
        Z2 = (c[2] - ma2)/sd2
        Z1 = (c[1] - ma1)/sd1
        Open_Units = GetOpenUnits(account_id, sec[i], sec, LIVE_ACCESS_TOKEN)
        if Open_Units == 0:
            if Z2 < 1.0 and Z1 > 1.0 and c[0] > c[i-1]:
                SaveToLog(main_log, "BBB: Buy " + sec[i])
                SL = round(c[0] - 0.010000001,5)
                TP = round(c[0] + 0.005000001,5)
                OpenMarketOrder(account_id, sec[i], vol, "market", "buy", TP, SL, file_nm, LIVE_ACCESS_TOKEN)
                BBB3["Open"][sec[i]] = dt
                BBB3["Status"][sec[i]] = "Entry"
            if Z2 > -1.0 and Z1 < -1.0 and c[0] < c[i-1]:
                SaveToLog(main_log, "BBB: Sell " + sec[i])
                SL = round(c[0] + 0.010000001,5)
                TP = round(c[0] - 0.005000001,5)
                OpenMarketOrder(account_id, sec[i], vol, "market", "sell", TP, SL, file_nm, LIVE_ACCESS_TOKEN)
                BBB3["Open"][sec[i]] = dt
                BBB3["Status"][sec[i]] = "Entry"
        elif Open_Units != 0:
            SaveToLog(main_log, "BBB: Managing trade for " + sec[i])
            if BBB3["Status"][sec[i]] == "":
                BBB3["Status"][sec[i]] = "Entry"
                BBB3["Open"][sec[i]] = dt
            Open_Trades = GetOpenTrades(account_id, sec[i], LIVE_ACCESS_TOKEN)
            for positions in Open_Trades["trades"]:
                trd_ID = positions["id"]
                trd_entry = float(positions["price"])
                trd_side = positions["side"]
                if BBB3["Status"][sec[i]] == "Entry":
                    if trd_side == "buy" and c[0] - trd_entry > 0.002:
                        SaveToLog(main_log, "BBB: BE " + sec[i])
                        OpenMarketOrder(account_id, sec[i], int(round(0.5*vol,0)), "market", "sell", 0, 0, file_nm, LIVE_ACCESS_TOKEN)
                        BBB3["SL"][sec[i]] = round(trd_entry + 0.00201, 5)
                        UpdateStopLoss(account_id, trd_ID, BBB3["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN)
                        BBB3["Status"][sec[i]] = "BE"
                    elif trd_side == "sell" and trd_entry - c[0] > 0.002:
                        SaveToLog(main_log, "BBB: BE " + sec[i])
                        OpenMarketOrder(account_id, sec[i], int(round(0.5*vol,0)), "market", "buy", 0, 0, file_nm, LIVE_ACCESS_TOKEN)
                        BBB3["SL"][sec[i]] = round(trd_entry - 0.00201, 5)
                        UpdateStopLoss(account_id, trd_ID, BBB3["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN)
                        BBB3["Status"][sec[i]] = "BE"

# def IntraTrend(account_id, sec, vol, tf, file_nm):
#     for i in range(len(sec)):
#         SaveToLog(main_log, "Collecting IT data for " + sec[i])
#         c = Get_Price(sec[i], tf, 7, "c", "midpoint")
#         Open_Units = IT["Units"][sec[i]]
#         dt = datetime.now()
#         SMA100 = Indicators[sec[i]]["SMA100"]
#         SMA101 = Indicators[sec[i]]["SMA101"]
#         SMA102 = Indicators[sec[i]]["SMA102"]
#         SMA210 = Indicators[sec[i]]["SMA210"]
#         SMA211 = Indicators[sec[i]]["SMA211"]
#         SMA212 = Indicators[sec[i]]["SMA212"]
#         SMA500 = Indicators[sec[i]]["SMA500"]
#         atr = Indicators[sec[i]]["ATR"]
#         if Open_Units == 0 and (dt.hour <= 12 and dt.hour >= 5) and Strat["IT"]["Stop"] == 0:
#             IT["Open"][sec[i]] = datetime.now()
#             IT["Status"][sec[i]] = ""
#             if c[0] < SMA100 and SMA100 < SMA210 and c[1] < SMA101 and c[2] > SMA102 and c[1] < SMA211 and c[2] < SMA212 and SMA500 - SMA100 > 0.0010:
#                 SaveToLog(main_log, "IT: Sell " + sec[i])
#                 IT["TP"][sec[i]] = round(c[0] - 0.00101, 5)
#                 IT["SL"][sec[i]] = round(min(c[0] + 0.00101, SMA210 + 0.00021), 5)
#                 OpenMarketOrder(account_id, sec[i], vol, "market", "sell", IT["TP"][sec[i]], IT["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN)
#                 IT["Open"][sec[i]] = dt
#                 IT["Status"][sec[i]] = "Entry"
#             elif c[0] > SMA100 and SMA100 > SMA210 and c[1] > SMA101 and c[2] < SMA102 and c[1] > SMA211 and c[2] > SMA212 and SMA100 - SMA500 > 0.0010:
#                 SaveToLog(main_log, "IT: Buy " + sec[i])
#                 IT["TP"][sec[i]] = round(c[0] + 0.00101, 5)
#                 IT["SL"][sec[i]] = round(min(c[0] - 0.00101, SMA210 - 0.00021), 5)
#                 OpenMarketOrder(account_id, sec[i], vol, "market", "buy", IT["TP"][sec[i]], IT["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN)
#                 IT["Open"][sec[i]] = dt
#                 IT["Status"][sec[i]] = "Entry"
#         elif Open_Units != 0:
#             SaveToLog(main_log, "IT: Managing trade for " + sec[i])
#             if IT["Status"][sec[i]] == "":
#                 IT["Status"][sec[i]] = "Entry"
#                 IT["Open"][sec[i]] = dt
#             Open_Trades = GetOpenTrades(account_id, sec[i], LIVE_ACCESS_TOKEN)
#             for positions in Open_Trades["trades"]:
#                 trd_ID = positions["id"]
#                 trd_entry = float(positions["price"])
#                 trd_side = positions["side"]
#                 if dt - timedelta(minutes=90) < IT["Open"][sec[i]]:
#                     if trd_side == "buy":
#                         if c[0] > 0.75*(IT["TP"][sec[i]] - trd_entry) + trd_entry and (IT["Status"][sec[i]] == "BE" or IT["Status"][sec[i]] == "Entry"):
#                             SaveToLog(main_log, "IT: 75% " + sec[i])
#                             OpenMarketOrder(account_id, sec[i], int(round(0.75*vol,0)), "market", "sell", 0, 0, file_nm, LIVE_ACCESS_TOKEN)
#                             IT["SL"][sec[i]] = round(0.25*(IT["TP"][sec[i]] - trd_entry) + trd_entry + 0.00001, 5)
#                             UpdateStopLoss(account_id, trd_ID, IT["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN)
#                             IT["Status"][sec[i]] = "75%"
#                     elif trd_side == "sell":
#                         if c[0] < trd_entry - 0.75*(trd_entry - IT["TP"][sec[i]]) and (IT["Status"][sec[i]] == "BE" or IT["Status"][sec[i]] == "Entry"):
#                             SaveToLog(main_log, "IT: 75% " + sec[i])
#                             OpenMarketOrder(account_id, sec[i], int(round(0.75*vol,0)), "market", "buy", 0, 0, file_nm, LIVE_ACCESS_TOKEN) 
#                             IT["SL"][sec[i]] = round(trd_entry - 0.25*(trd_entry - IT["TP"][sec[i]])  + 0.00001, 5)
#                             UpdateStopLoss(account_id, trd_ID, IT["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN)
#                             IT["Status"][sec[i]] = "75%"