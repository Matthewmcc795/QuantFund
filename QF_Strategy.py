# This script handles executing specific trading plans and all related calculaitons
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
        if Open_Units == 0 and (dt.hour <= 12 and dt.hour >= 5) and Strat["PPB"]["Stop"] == 0:
            PPB["Open"][sec[i]] = datetime.now()
            PPB["Status"][sec[i]] = ""
            if m5c[0] < r and m5c[1] < r and m5c[2] > r and ma > r:
                SaveToLog(main_log, "PPB: Sell " + sec[i])
                PPB["SL"][sec[i]] = round(m5c[0] + atr + 0.00001,5)
                PPB["TP"][sec[i]] = round(m5c[0] - min(0.00151, 1.5*atr) - 0.00001,5)
                OpenMarketOrder(account_id, sec[i], vol, "market", "sell", PPB["TP"][sec[i]], PPB["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN)
                PPB["Open"][sec[i]] = dt
                PPB["Status"][sec[i]] = "Entry"
            elif m5c[0] > s and m5c[1] > s and m5c[2] < s and ma < s:
                SaveToLog(main_log, "PPB: Buy " + sec[i])
                PPB["SL"][sec[i]] = round(m5c[0] - atr - 0.00001,5)
                PPB["TP"][sec[i]] = round(m5c[0] + min(0.00151, 1.5*atr) + 0.00001,5)
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

# if m5c[0] < r and m5c[1] < r and m5c[2] > r and ma > r:
#     SaveToLog(main_log, "PPB: Sell " + sec[i])
#     if PPB["Op"][sec[i]] == 1:
#         PPB["TP"][sec[i]] = round(max(s, m5c[0] - 2*atr) - 0.00001,5)
#         PPB["SL"][sec[i]] = round(m5c[0] + atr + 0.00001,5)
#         Trade_Params = [True, vol, PPB["TP"][sec[i]], PPB["SL"][sec[i]]]
#         Tag = "PPB Sell " + PP["Position"][sec[i]]
#         OpResult = OptimizeTrade(sec[i], Tag, Trade_Params)
#         if OpResult[0]:
#             OpenMarketOrder(account_id, sec[i], OpResult[1], "market", "sell", OpResult[2], OpResult[3], file_nm, LIVE_ACCESS_TOKEN)
#             PPB["Open"][sec[i]] = dt
#             PPB["Status"][sec[i]] = "Entry"
#             PPB["TP"][sec[i]] = OpResult[2]
#             PPB["SL"][sec[i]] = OpResult[3]
#     else:
#         PPB["SL"][sec[i]] = round(m5c[0] + atr + 0.00001,5)
#         PPB["TP"][sec[i]] = round(max(s, m5c[0] - 2*atr) - 0.00001,5)
#         OpenMarketOrder(account_id, sec[i], vol, "market", "sell", PPB["TP"][sec[i]], PPB["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN)
#         PPB["Open"][sec[i]] = dt
#         PPB["Status"][sec[i]] = "Entry"
# elif m5c[0] > s and m5c[1] > s and m5c[2] < s and ma < s:
#     SaveToLog(main_log, "PPB: Buy " + sec[i])
#     if PPB["Op"][sec[i]] == 1:
#         PPB["TP"][sec[i]] = round(min(r, m5c[0] + 2*atr) + 0.00001,5)
#         PPB["SL"][sec[i]] = round(m5c[0] - atr - 0.00001,5)
#         Trade_Params = [True, vol, PPB["TP"][sec[i]], PPB["SL"][sec[i]]]
#         Tag = "PPB Buy " + PP["Position"][sec[i]]
#         OpResult = OptimizeTrade(sec[i], Tag, Trade_Params)
#         if OpResult[0]:
#             OpenMarketOrder(account_id, sec[i], OpResult[1], "market", "buy", OpResult[2], OpResult[3], file_nm, LIVE_ACCESS_TOKEN)
#             PPB["Open"][sec[i]] = dt
#             PPB["Status"][sec[i]] = "Entry"
#             PPB["TP"][sec[i]] = OpResult[2]
#             PPB["SL"][sec[i]] = OpResult[3]
#     else:
#         PPB["TP"][sec[i]] = round(min(r, m5c[0] + 2*atr) + 0.00001,5)
#         PPB["SL"][sec[i]] = round(m5c[0] - atr - 0.00001,5)
#         OpenMarketOrder(account_id, sec[i], vol, "market", "buy", PPB["TP"][sec[i]], PPB["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN)
#         PPB["Open"][sec[i]] = dt
#         PPB["Status"][sec[i]] = "Entry"

def MovingAverageContrarian(account_id, sec, vol, tf, file_nm):
    for i in range(len(sec)):
        SaveToLog(main_log, "Collecting MAC data for " + sec[i])
        c = Get_Price(sec[i], tf, 51, "c", "midpoint")
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
                SL = round(c[0] + 100.00001,5)
                TP = round(c[0] - 100.00001,5)
                OpenMarketOrder(account_id, sec[i], vol, "market", "sell", TP, SL, file_nm, LIVE_ACCESS_TOKEN)
            elif Z1 < -2.5 and Z0 > -2.5:
                SaveToLog(main_log, "MAC: Buy " + sec[i])
                SL = round(c[0] - 100.00001,5)
                TP = round(c[0] + 100.00001,5)
                OpenMarketOrder(account_id, sec[i], vol, "market", "buy", TP, SL, file_nm, LIVE_ACCESS_TOKEN)

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
#                 IT["TP"][sec[i]] = round(c[0] - min(0.00151, 1.5*atr), 5)
#                 IT["SL"][sec[i]] = round(min(c[0] + 0.00101, SMA210 + 0.00021), 5)
#                 OpenMarketOrder(account_id, sec[i], vol, "market", "sell", IT["TP"][sec[i]], IT["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN)
#                 IT["Open"][sec[i]] = dt
#                 IT["Status"][sec[i]] = "Entry"
#             elif c[0] > SMA100 and SMA100 > SMA210 and c[1] > SMA101 and c[2] < SMA102 and c[1] > SMA211 and c[2] > SMA212 and SMA100 - SMA500 > 0.0010:
#                 SaveToLog(main_log, "IT: Buy " + sec[i])
#                 IT["TP"][sec[i]] = round(c[0] + min(0.00151, 1.5*atr), 5)
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
#                         elif dt - timedelta(minutes=30) > IT["Open"][sec[i]] and c[0] > (IT["TP"][sec[i]] - trd_entry)/3 + trd_entry and IT["Status"][sec[i]] == "Entry":
#                             SaveToLog(main_log, "IT: BE " + sec[i])
#                             IT["SL"][sec[i]] = round(trd_entry + min(0.00025, abs(c[0] - trd_entry)/2) + 0.00001,5)
#                             UpdateStopLoss(account_id, trd_ID, IT["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN) 
#                             IT["Status"][sec[i]] = "BE"
#                     elif trd_side == "sell":
#                         if c[0] < trd_entry - 0.75*(trd_entry - IT["TP"][sec[i]]) and (IT["Status"][sec[i]] == "BE" or IT["Status"][sec[i]] == "Entry"):
#                             SaveToLog(main_log, "IT: 75% " + sec[i])
#                             OpenMarketOrder(account_id, sec[i], int(round(0.75*vol,0)), "market", "buy", 0, 0, file_nm, LIVE_ACCESS_TOKEN) 
#                             IT["SL"][sec[i]] = round(trd_entry - 0.25*(trd_entry - IT["TP"][sec[i]])  + 0.00001, 5)
#                             UpdateStopLoss(account_id, trd_ID, IT["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN)
#                             IT["Status"][sec[i]] = "75%"
#                         elif dt - timedelta(minutes=30) > IT["Open"][sec[i]] and c[0] < trd_entry - (trd_entry - IT["TP"][sec[i]])/3 and IT["Status"][sec[i]] == "Entry":
#                             SaveToLog(main_log, "IT: BE " + sec[i])
#                             IT["SL"][sec[i]] = round(trd_entry - min(0.00025, abs(trd_entry - c[0])/2) + 0.00001,5)
#                             UpdateStopLoss(account_id, trd_ID, IT["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN)
#                             IT["Status"][sec[i]] = "BE"
#                 else:
#                     if IT["Status"][sec[i]] == "Entry":
#                         bounded = True
#                         bound = max(abs(IT["SL"][sec[i]] - trd_entry), abs(IT["TP"][sec[i]] - trd_entry))
#                         ubound = trd_entry + 0.1*bound
#                         lbound = trd_entry + 0.1*bound
#                         for t in range(6):
#                             if c[t] > lbound and c[t] < ubound and bounded == True:
#                                 bounded = True
#                             else:
#                                 bounded = False
#                         if bounded == True:
#                             SaveToLog(main_log, "IT: Flat at Entry" + sec[i])
#                             ClosePositions(account_id, sec[i], file_nm, LIVE_ACCESS_TOKEN)
#                         else: 
#                             IT["Status"][sec[i]] = "Entry-Long"
#                     if trd_side == "buy":
#                         if c[0] > 0.5*(IT["TP"][sec[i]] - trd_entry) + trd_entry:
#                             SaveToLog(main_log, "IT: close " + sec[i])
#                             ClosePositions(account_id, sec[i], file_nm, LIVE_ACCESS_TOKEN)
#                         elif c[0] > (IT["TP"][sec[i]] - trd_entry)/3 + trd_entry and (IT["Status"][sec[i]] == "BE" or IT["Status"][sec[i]] == "Entry-Long"):
#                             SaveToLog(main_log, "IT: 50% " + sec[i])
#                             OpenMarketOrder(account_id, sec[i], int(round(0.5*vol,0)), "market", "sell", 0, 0, file_nm, LIVE_ACCESS_TOKEN)
#                             IT["SL"][sec[i]] = round(trd_entry + min(0.00025, abs(c[0] - trd_entry)/2) + 0.00001,5)
#                             UpdateStopLoss(account_id, trd_ID, IT["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN)
#                             IT["Status"][sec[i]] = "50%"
#                     elif trd_side == "sell":
#                         if c[0] < trd_entry - 0.5*(trd_entry - IT["TP"][sec[i]]): 
#                             SaveToLog(main_log, "IT: close " + sec[i])
#                             ClosePositions(account_id, sec[i], file_nm, LIVE_ACCESS_TOKEN) 
#                         elif c[0] < trd_entry - (trd_entry - IT["TP"][sec[i]])/3 and (IT["Status"][sec[i]] == "BE" or IT["Status"][sec[i]] == "Entry-Long"):
#                             SaveToLog(main_log, "IT: 50% " + sec[i])
#                             OpenMarketOrder(account_id, sec[i], int(round(0.5*vol,0)), "market", "buy", 0, 0, file_nm, LIVE_ACCESS_TOKEN)
#                             IT["SL"][sec[i]] = round(trd_entry - min(0.00025, abs(trd_entry - c[0])/2) + 0.00001,5)
#                             UpdateStopLoss(account_id, trd_ID, IT["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN)
#                             IT["Status"][sec[i]] = "50%"

# if c[0] < SMA100 and SMA100 < SMA210 and c[1] < SMA101 and c[2] > SMA102 and c[1] < SMA211 and c[2] < SMA212 and SMA500 - SMA100 > 0.0010:
#     SaveToLog(main_log, "IT: Sell " + sec[i])
#     if IT["Op"][sec[i]] == 1:
#         IT["TP"][sec[i]] = round(c[0] - 0.00151, 5)
#         IT["SL"][sec[i]] = round(min(c[0] + 0.00101, SMA210 + 0.00021), 5)
#         Trade_Params = [True, vol, IT["TP"][sec[i]], IT["SL"][sec[i]]]
#         Tag = "IT Sell"
#         OpResult = OptimizeTrade(sec[i], Tag, Trade_Params)
#         if OpResult[0]:
#             OpenMarketOrder(account_id, sec[i], OpResult[1], "market", "sell", OpResult[2], OpResult[3], file_nm, LIVE_ACCESS_TOKEN)
#             IT["Open"][sec[i]] = dt
#             IT["Status"][sec[i]] = "Entry"
#             IT["TP"][sec[i]] = OpResult[2]
#             IT["SL"][sec[i]] = OpResult[3]
#     else:
#         IT["TP"][sec[i]] = round(c[0] - 0.00151, 5)
#         IT["SL"][sec[i]] = round(min(c[0] + 0.00101, SMA210 + 0.00021), 5)
#         OpenMarketOrder(account_id, sec[i], vol, "market", "sell", IT["TP"][sec[i]], IT["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN)
#         IT["Open"][sec[i]] = dt
#         IT["Status"][sec[i]] = "Entry"
# elif c[0] > SMA100 and SMA100 > SMA210 and c[1] > SMA101 and c[2] < SMA102 and c[1] > SMA211 and c[2] > SMA212 and SMA100 - SMA500 > 0.0010:
#     SaveToLog(main_log, "IT: Buy " + sec[i])
#     if IT["Op"][sec[i]] == 1:
#         IT["TP"][sec[i]] = round(c[0] + 0.00151, 5)
#         IT["SL"][sec[i]] = round(min(c[0] - 0.00101, SMA210 - 0.00021), 5)
#         Trade_Params = [True, vol, IT["TP"][sec[i]], IT["SL"][sec[i]]]
#         Tag = "PPB Buy"
#         OpResult = OptimizeTrade(sec[i], Tag, Trade_Params)
#         if OpResult[0]:
#             OpenMarketOrder(account_id, sec[i], OpResult[1], "market", "buy", OpResult[2], OpResult[3], file_nm, LIVE_ACCESS_TOKEN)
#             IT["Open"][sec[i]] = dt
#             IT["Status"][sec[i]] = "Entry"
#             IT["TP"][sec[i]] = OpResult[2]
#             IT["SL"][sec[i]] = OpResult[3]
#     else:
#         IT["TP"][sec[i]] = round(c[0] + 0.00151, 5)
#         IT["SL"][sec[i]] = round(min(c[0] - 0.00101, SMA210 - 0.00021), 5)
#         OpenMarketOrder(account_id, sec[i], vol, "market", "buy", IT["TP"][sec[i]], IT["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN)
#         IT["Open"][sec[i]] = dt
#         IT["Status"][sec[i]] = "Entry"

# def Name Pending(account_id, sec, vol, tf, file_nm):
#     for i in range(len(sec)):
#         SaveToLog(main_log, "Collecting IT data for " + sec[i])
#         o, h, l, c = Get_Price(sec[i],tf,101,"ohlc", "midpoint")
#         cb, ca = Get_Price(sec[i], tf, 101, "c", "bidask")
#         SMA10 = []
#         SMA21 = []
#         SMA50 = []
#         MACD = []
#         upmarubozu = [0] * 50
#         dwnmarubozu = [0] * 50
#         hammer = [0]*50
#         shootingstar = [0]*50
#         for k in range(50):
#             SMA10.append(SMA(c,10, k))
#             SMA21.append(SMA(c,21, k))
#             SMA50.append(SMA(c,50, k))
#         for k in range(50):
#             MACD.append(SMA10[k]-SMA21[k])

#         for k in range(50):
#             if h[k] - max(o[k], c[k]) <= 0.0002 and min(o[k], c[k]) - l[k] <= 0.0002 and o[k] - c[k] > 0.0005:
#                 dwnmarubozu[k] = 1
#             if h[k] - max(o[k], c[k]) <= 0.0002 and min(o[k], c[k]) - l[k] <= 0.0002 and c[k] - o[k] > 0.0005:
#                 upmarubozu[k] = 1
#             if h[k] - max(o[k], c[k]) <= 0.0002 and min(o[k], c[k]) - l[k] > 1.5*(abs(c[k] - o[k])):
#                 hammer[k] = 1
#             if hmin(o[k], c[k]) - l[k] <= 0.0002 and h[k] - max(o[k], c[k]) > 1.5*(abs(c[k] - o[k])):
#                 shootingstar[k] = 1
        
#         for k in range(20):
#             angsma50.append(SMA50[k]/SMA50[0] - 1)

#         if angsma50[0] > 0.01:


#         Open_Units = GetOpenUnits(account_id, sec[i], sec, LIVE_ACCESS_TOKEN)
#         dt = datetime.now()
#         if Open_Units == 0 and (dt.hour <= 18 and dt.hour >= 8):
#             ITM["Open"][sec[i]] = datetime.now()
#             ITM["Status"][sec[i]] = ""
#             if c[0] > SMA10 and c[0] < SMA21 and c[0] < SMA50:
#                 SaveToLog(main_log, "ITM: Sell " + sec[i])
#                 ITM["TP"][sec[i]] = round(c[0] - 0.8*abs(c[0] - SMA50), 5)
#                 ITM["SL"][sec[i]] = round(SMA50, 5)
#                 OpenMarketOrder(account_id, sec[i], vol, "market", "sell", ITM["TP"][sec[i]], ITM["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN)
#                 ITM["Open"][sec[i]] = dt
#                 ITM["Status"][sec[i]] = "Entry"
#             elif c[0] < SMA10 and c[0] > SMA21 and c[0] > SMA50:
#                 SaveToLog(main_log, "ITM: Buy " + sec[i])
#                 ITM["TP"][sec[i]] = round(c[0] + 0.8*abs(c[0] - SMA50), 5)
#                 ITM["SL"][sec[i]] = round(SMA50, 5)
#                 OpenMarketOrder(account_id, sec[i], vol, "market", "buy", ITM["TP"][sec[i]], ITM["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN)
#                 ITM["Open"][sec[i]] = dt
#                 ITM["Status"][sec[i]] = "Entry"
#         elif Open_Units != 0:
#             SaveToLog(main_log, "ITM: Managing trade for " + sec[i])
#             if ITM["Status"][sec[i]] == "":
#                 ITM["Status"][sec[i]] = "Entry"
#                 ITM["Open"][sec[i]] = dt
#             Open_Trades = GetOpenTrades(account_id, sec[i], LIVE_ACCESS_TOKEN)
#             for positions in Open_Trades["trades"]:
#                 trd_ID = positions["id"]
#                 trd_entry = float(positions["price"])
#                 trd_side = positions["side"]
#                 if dt - timedelta(minutes=30) < ITM["Open"][sec[i]]:
#                     if trd_side == "buy":
#                         if c[0] - trd_entry > 0.0006 and ITM["Status"][sec[i]] == "Entry":
#                             SaveToLog(main_log, "ITM: BE " + sec[i])
#                             ITM["SL"][sec[i]] = round(trd_entry + 0.00011,5)
#                             UpdateStopLoss(account_id, trd_ID, ITM["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN) 
#                             ITM["Status"][sec[i]] = "BE"
#                     elif trd_side == "sell":
#                         if trd_entry - c[0] > 0.0006 and ITM["Status"][sec[i]] == "Entry":
#                             SaveToLog(main_log, "ITM: BE " + sec[i])
#                             ITM["SL"][sec[i]] = round(trd_entry - 0.00011,5)
#                             UpdateStopLoss(account_id, trd_ID, ITM["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN)
#                             ITM["Status"][sec[i]] = "BE"
#                 else:
#                     SaveToLog(main_log, "ITM: Flat at Entry" + sec[i])
#                     ClosePositions(account_id, sec[i], file_nm, LIVE_ACCESS_TOKEN)

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
# try:
#     PPB["SL"][sec[i]] = round(trd_entry - min(0.00025, atr/4, abs(trd_entry - m5c[0])/2) + 0.00001, 5)
#     UpdateStopLoss(account_id, trd_ID, PPB["SL"][sec[i]], file_nm, LIVE_ACCESS_TOKEN)
#     PPB["Status"][sec[i]] = "BE"
# except:
#     e = sys.exc_info()[0]
#     SaveToLog(main_log, "PPB: Sell 50% " + sec[i] + " " + str(e))