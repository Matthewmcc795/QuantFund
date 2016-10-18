import requests
import json
from array import *
from Settings import LIVE_ACCESS_TOKEN, STRT, STRO, STRH, STRL, STRC, STROA, STRHA, STRLA, STRCA, STROB, STRHB, STRLB, STRCB, STRV, STRCO
import httplib
import urllib
from QF_Strategy import *
from QF_Functions import *
from datetime import datetime, timedelta
import time
import sys
main_log = "QF.txt"

##########################################################################################################
#                                            Money Manager                                               #
##########################################################################################################

def UpdateAccountBalance(account_id, strategy):
    Strat[strategy]["InitialBalance"] = GetAccountBalance(account_id, LIVE_ACCESS_TOKEN)
    Strat[strategy]["DailyPl"] = "Middle"
    Strat[strategy]["Stop"] = 0

def ManageMoney(account_id, strategy, target, limit):
    Current_Balance = GetAccountBalance(account_id, LIVE_ACCESS_TOKEN)
    if Current_Balance - Strat[strategy]["InitialBalance"] > target:
        Strat[strategy]["DailyPl"] = "AboveTarget"
    elif Current_Balance - Strat[strategy]["InitialBalance"] < -limit:
        Strat[strategy]["DailyPl"] = "BelowLimit"
        Strat[strategy]["Stop"] = 1
    else:
        Strat[strategy]["DailyPl"] = "Middle"

def UpdateOpenUnits(sec, account_id, strat):
    if strat == "PPB":
        for i in range(len(sec)):
            PPB["Units"][sec[i]] = GetOpenUnits(account_id, sec[i], sec, LIVE_ACCESS_TOKEN)
    elif strat == "IT":
        for i in range(len(sec)):
            IT["Units"][sec[i]] = GetOpenUnits(account_id, sec[i], sec, LIVE_ACCESS_TOKEN)
    elif strat == "MAC":
        for i in range(len(sec)):
            MAC["Units"][sec[i]] = GetOpenUnits(account_id, sec[i], sec, LIVE_ACCESS_TOKEN)

##########################################################################################################
#                                                 Trader                                                 #
##########################################################################################################

# def OptimizeTrade(sec, trd, strategy, params):
#     if strategy == "PPB":
#         MM = MoneyManager()
#         if MM == "":
#             if trd == "Buy":
#                 patterns = ["BullishEngulfing", "InsiderbarBreakUp", "BullKeyReversal", "UpDoji"]
#             elif trd == "Sell":
#                 patterns = ["BearishEngulfing", "InsiderbarBreakDown", "BearKeyReversal", "DownDoji"]
#         elif MM == "":
#             if trd == "Buy":
#                 patterns = ["BullishEngulfing", "InsiderbarBreakUp", "BullKeyReversal", "UpDoji"]
#             elif trd == "Sell":
#                 patterns = ["BearishEngulfing", "InsiderbarBreakDown", "BearKeyReversal", "DownDoji"]
#     elif strategy == "IT":
#         MM = MoneyManager()
#         if MM == "":
#             if trd == "Buy":
#                 patterns = ["BullishEngulfing", "InsiderbarBreakUp", "BullKeyReversal", "UpDoji"]

#             elif trd == "Sell":
#                 patterns = ["BearishEngulfing", "InsiderbarBreakDown", "BearKeyReversal", "DownDoji"]

#         elif MM == "":
#             if trd == "Buy":
#                 patterns = ["BullishEngulfing", "InsiderbarBreakUp", "BullKeyReversal", "UpDoji"]

#             elif trd == "Sell":
#                 patterns = ["BearishEngulfing", "InsiderbarBreakDown", "BearKeyReversal", "DownDoji"]

#     if Strat["PPB"]["DailyPl"] == "AboveTarget":


#     elif Strat["PPB"]["DailyPl"] == "BelowLimit":


#     for pat in patterns:
#         if PriceAction[sec][pat] == 1:
#             params = [True, vol*2, TP, SL]
#     return params

def UpdatePivotPoints(sec):
    for i in range(len(sec)):
        DH, DL, DC = Get_Price(sec[i], "D", 2, "hlc", "midpoint")
        Piv = [0,0,0,0,0]
        Piv[2] = round((DH[1] + DL[1] + DC[1])/3 +0.00001,5)
        Piv[0] = round(Piv[2] - DH[1] + DL[1],5)
        Piv[1] = round(2*Piv[2] - DH[1],5)
        Piv[3] = round(2*Piv[2] - DL[1],5)
        Piv[4] = round(Piv[2] + DH[1] - DL[1],5)
        PP["R2"][sec[i]] = Piv[4]
        PP["R1"][sec[i]] = Piv[3]
        PP["PP"][sec[i]] = Piv[2]
        PP["S1"][sec[i]] = Piv[1]
        PP["S2"][sec[i]] = Piv[0]

def LoadIndicators(sec, tf):
    for i in range(len(sec)):
        if tf == "M5":
            M5C = Get_Price(sec[i], "M5", 1, "c", "midpoint")
            Piv = [0,0,0,0,0]
            Piv[4] = PP["R2"][sec[i]]
            Piv[3] = PP["R1"][sec[i]]
            Piv[2] = PP["PP"][sec[i]]
            Piv[1] = PP["S1"][sec[i]]
            Piv[0] = PP["S2"][sec[i]]
            Pos = 0
            if M5C[0] >= Piv[4]:
                Pos = 5
            elif M5C[0] >= Piv[3] and M5C[0] < Piv[4]:
                Pos = 4
            elif M5C[0] >= Piv[2] and M5C[0] < Piv[3]:
                Pos = 3
            elif M5C[0] >= Piv[1] and M5C[0] < Piv[2]:
                Pos = 2
            elif M5C[0] >= Piv[0] and M5C[0] < Piv[1]:
                Pos = 1
            elif M5C[0] < Piv[0]:
                Pos = 0
            if Pos == 5:
                Indicators[sec[i]]["s"] =  PP["R2"][sec[i]]
                Indicators[sec[i]]["r"] = 2*M5C[0]
            elif Pos == 0:
                Indicators[sec[i]]["s"] =  0
                Indicators[sec[i]]["r"] = PP["S2"][sec[i]]
            else:
                Indicators[sec[i]]["s"] = Piv[Pos-1]
                Indicators[sec[i]]["r"] = Piv[Pos]
        elif tf == "M15":
            M15H, M15L, M15C = Get_Price(sec[i], "M15", 101, "hlc", "midpoint")
            Indicators[sec[i]]["SMA100"] = round(SMA(M15C, 10, 0),5)
            Indicators[sec[i]]["SMA101"] = round(SMA(M15C, 10, 1),5)
            Indicators[sec[i]]["SMA102"] = round(SMA(M15C, 10, 2),5)
            Indicators[sec[i]]["SMA210"] = round(SMA(M15C, 21, 0),5)
            Indicators[sec[i]]["SMA211"] = round(SMA(M15C, 21, 1),5)
            Indicators[sec[i]]["SMA212"] = round(SMA(M15C, 21, 2),5)
            Indicators[sec[i]]["SMA500"] = round(SMA(M15C, 50, 0),5)
            Indicators[sec[i]]["ATR"] = round(Get_ATR(M15H, M15L, M15C, sec[i]),6)

# def TradingSessionPrep(session):
#     if session = "NA":
#         PriceAction[sec[i]]["AtWkLow"] = 0
#         PriceAction[sec[i]]["AtWkHigh"] = 0
#         for i in range(len(sec)):
#             m5h, m5l, m5c = Get_Price(sec[i], "M5", 145, "hlc", "midpoint")
#             l = 5*m5c[0]
#             h = 0
#             for j in range(60):
#                 l = min(l, m5l[j])
#                 h = max(h, m5h[j])
#             Indicators[sec[i]]["EuLow"] = l
#             Indicators[sec[i]]["EuHigh"] = h
#             l = 5*m5c[0]
#             h = 0
#             for j in range(61, 144):
#                 l = min(l, m5l[j])
#                 h = max(h, m5h[j])
#             Indicators[sec[i]]["AsLow"] = l
#             Indicators[sec[i]]["AsHigh"] = h
#             Wkh, Wkl, Wkc = Get_Price(sec[i], "W", 2, "hlc", "midpoint")
#             Dh, Dl, Dc = Get_Price(sec[i], "D", 2, "hlc", "midpoint")
#             l = min(Wkl[1], Dl[1])
#             h = max(Wkh[1], Dh[1])
#             Indicators[sec[i]]["WkLow"] = l
#             Indicators[sec[i]]["WkHigh"] = h

# def AnalyzePricePatterns(sec):
#     for i in range(len(sec)):
#         DH, DL, DC = Get_Price(sec[i], "D", 2, "hlc", "midpoint")
#         M15C = Get_Price(sec[i], "M15", 10, "c", "midpoint")
#         M5C = Get_Price(sec[i], "M5", 1, "c", "midpoint")
#         lwr = True
#         SMA100 = Indicators[sec[i]]["SMA100"]
#         SMA101 = Indicators[sec[i]]["SMA101"]
#         SMA102 = Indicators[sec[i]]["SMA102"]
#         SMA103 = Indicators[sec[i]]["SMA103"]
#         SMA210 = Indicators[sec[i]]["SMA210"]
#         SMA211 = Indicators[sec[i]]["SMA211"]
#         SMA212 = Indicators[sec[i]]["SMA212"]
#         SMA213 = Indicators[sec[i]]["SMA213"]
#         SMA500 = Indicators[sec[i]]["SMA500"]
#         if min (SMA101 - M15C[1], SMA102 - M15C[2], SMA103 - M15C[3]) > 0:
#             PriceAction[sec[i]]["Num Candles Below MA"] = 1
#         if abs(M150[1] - M15C[1]) < 0.0005:
#             PriceAction[sec[i]]["Doji"] = 1
#         if lwr == True and M15C[0] < SMA100 and M15C[1] < SMA101 and M15C[2] < SMA102 and SMA101 - M15C[1] < 0.0002 and SMA102 - M15C[2] < 0.0002 and M15C[0] < min (M15C[1], M15C[2]) and SMA100 < SMA210 and SMA210 < SMA500:
#             PriceAction[sec[i]]["SMA10Bounce"] = 1
#         if M15C[0] > M15H[1] and M15O[1] - M15C[1] > sd_data[i]/64:
#             PriceAction[sec[i]]["BullEngulfing"] = 1
#         if M15C[0] < M15L[1] and M15C[1]-M15O[1] > sd_data[i]/64:
#             PriceAction[sec[i]]["BearEngulfing"] = 1
#         if M15H[0] < M15H[1] and M15L[0] > M15L[1] and M15C[0] > M15H[1]:
#             PriceAction[sec[i]]["InsidebarBreakUp"] = 1
#         if M15H[0] < M15H[1] and M15L[0] > M15L[1] and M15C[0] < M15L[1]:
#             PriceAction[sec[i]]["InsidebarBreakDown"] = 1
#         if M15O[0] > M15C[0] and M15O[1] < M15C[1] and M15L[0] < M15L[1] and M15H[0] > M15H[1]:
#             PriceAction[sec[i]]["BullKeyReversal"] = 1
#         if M15O[0] < M15C[0] and M15O[1] > M15C[1] and M15H[0] < M15H[1] and M15C[0] < M15L[1]:
#             PriceAction[sec[i]]["BearKeyReversal"] = 1
#         if abs(M15O[1] - M15C[1]) < 0.0002 and M15C[0] > M15H[1] and M15C[0] - M15O[0] > 0.0005:
#             PriceAction[sec[i]]["UpDoji"] = 1
#         if abs(M15O[1] - M15C[1]) < 0.0002 and M15C[0] < M15L[1] and M15O[0] - M15C[0] > 0.0005:
#             PriceAction[sec[i]]["DownDoji"] = 1
#         if Indicators[sec[i]]["WkLow"] + 0.0020 >= M5C[0]:
#             PriceAction[sec[i]]["AtWkLow"] = 1
#         if Indicators[sec[i]]["WkHigh"] - 0.0020 <= M5C[0]:
#             PriceAction[sec[i]]["AtWkHigh"] = 1
#         if Indicators[sec[i]]["SesLow"] + 0.0020 >= M5C[0]:
#             PriceAction[sec[i]]["AtSesLow"] = 1
#         if Indicators[sec[i]]["SesHigh"] - 0.0020 <= M5C[0]:
#             PriceAction[sec[i]]["AtSesigh"] = 1


#         # Congested
#         M5C = Get_Price(sec[i], "M5", 10, "c", "midpoint")
#         prices = [0]*10
#         for j in range(5):
#             if abs(M5C[j]- M5C[j+1]) <= 0.0003 and abs(M5C[0]-M5C[j]) <= 0.0005:
#                 prices[j] = 1
# # 

        # Proximity to PP or SMA prior to being in play





        # if M15H[0] - max(M15O[0], M15C[0]) and min(M15O[0], M15C[0]) - M15L[0]:
        #     PriceAction[sec[i]]["Hammer"] = 1
        # if M15H[0] - max(M15O[0], M15C[0]) and min(M15O[0], M15C[0]) - M15L[0]:
        #     PriceAction[sec[i]]["ShootingStar"] = 1

    #     if c[i] > o[i] and abs(c[i]-o[i]) > sd_data[i] and h[i] - max(o[i],c[i]) < 0.1*(c[i] - o[i]):
    #         PriceAction[sec[i]]["BullMarubozu"] = 1

    #     if c[i] < o[i] and abs(c[i]-o[i]) > sd_data[i] and 0.1*(c[i] - o[i]) > min(o[i],c[i]) - l[i]:
    #         PriceAction[sec[i]]["BearMarubozu"] = 1

    #     if abs(o[i] - c[i]) < 0.001 and h[i]-max(o[i],c[i]) > 0.004 and min(o[i],c[i]) - l[i] > 0.004 :
    #         PriceAction[sec[i]]["LongLeggedDoji"] = 1

    #     s = ShootingStar(o,h,l,c)
    #     d = Doji(o,h,l,c)
    #         if s[i] == 1 and d[i] == 1:
    #             PriceAction[sec[i]]["Gravestone"] = 1

    #     h = Hammer(o,h,l,c)
    #     d = Doji(o,h,l,c)
    #         if h[i] == 1 and d[i] == 1:
    #             PriceAction[sec[i]]["Dragonfly"] = 1

    #     be = BearishMarubozu(o,h,l,c)
    #     bu = BullishMarubozu(o,h,l,c)
    #     h = Hammer(o,h,l,c)
    #     dr = Dragonfly(o,h,l,c)
    #     do = Doji(o,h,l,c)
    #     rev = h + dr + do
    #         if rev[i] > 0 and be[i-1] == 1 and bu[i+1] == 1:
    # # Revise Morning & Evening star
    # # 3rd > 50% of 1st and engulfs 2nd
    # # 2nd usually continues the trend
    #             PriceAction[sec[i]]["MorningStar"] = 1

    #     be = BearishMarubozu(o,h,l,c)
    #     bu = BullishMarubozu(o,h,l,c)
    #     s = ShootingStar(o,h,l,c)
    #     g = Gravestone(o,h,l,c)
    #     d = Doji(o,h,l,c)
    #         if (s[i] == 0 or g[i] == 0 or d[i] == 0) and bu[i-1] == 1 and be[i+1] == 1:
    #             PriceAction[sec[i]]["EveningStar"] = 1

# Routines to try and optimize best entry prices over a certain time window
# Next 4hr prices could break out of a pattern and fall another 0.5% to let's buy half now and half then


##########################################################################################################
#                                                                                                        #
#                                              Optimizer                                                 #
#                                                                                                        #
##########################################################################################################

# class MoneyManagement():
#     def __init__(self, sec):
#         self.sec = sec
#     def UpdateOpenUnits(self, account_id, strat):
#         if strat == "PPB"
#             for i in range(len(self.sec))
#                 PPB["Units"][self.sec[i]] = GetOpenUnits(account_id, self.sec[i], self.sec, LIVE_ACCESS_TOKEN)
#         elif strat == "IT"
#             for i in range(len(self.sec))
#                 IT["Units"][self.sec[i]] = GetOpenUnits(account_id, self.sec[i], self.sec, LIVE_ACCESS_TOKEN)
#         elif strat == "MAC"
#             for i in range(len(self.sec))
#                 MAC["Units"][self.sec[i]] = GetOpenUnits(account_id, self.sec[i], self.sec, LIVE_ACCESS_TOKEN)

#     def ZScoreAnalysis(self):
#         self.SMA50 = [0]*100
#         self.SMA21 = [0]*100
#         self.SMA10 = [0]*100
#         self.SD50 = [0]*100
#         self.SD21 = [0]*100
#         self.SD10 = [0]*100
#         for i in range(100-50):
#             SMA50[100-50 - i] = SMA(self.M15C, 50, i)
#             SD50[100-50-i] = STDEV(self.M15C, 50, i)
#         for i in range(100-21):
#             SMA21[100-21 - i] = SMA(self.M15C, 21, i)
#             SD21[100-21-i] = STDEV(self.M15C, 21, i)
#         for i in range(100-10):
#             SMA10[100 -10 - i] = SMA(self.M15C, 10, i)
#             SD10[100-10-i] = STDEV(self.M15C, 10, i)
#         self.Z50 = [0]*100
#         self.Z21 = [0]*100
#         self.Z10 = [0]*100
#         for i in range(100-50):
#             Z50[100-50 - i] = (self.M15C[i] - self.SMA50[i])/self.SD50[i]
#         for i in range(100-21):
#             Z21[100-21-i] = (self.M15C[i] - self.SMA21[i])/self.SD21[i]
#         for i in range(100-10):
#             Z10[100-10-i] = (self.M15C[i] - self.SMA10[i])/self.SD10[i]   
#     def LoadIndicators(self):
#         Indicators[self.sec[i]]["ATR"] = Get_ATR(self.M15H, self.M15L, self.M15C, self.sec[i])

# def GetTradeSecurities(strat, sec):
#     sec_temp = []
#     if strat == "PPB":
#         for i in range(len(sec)):
#             c = Get_Price(sec[i], "M1", 1, "c", "midpoint")
#             if PPB["Units"][sec[i]] == 0:
#                 sec_temp.append(sec[i])
#             if PPB["Active"][sec[i]] == 1:
#                 sec_temp2.append(sec[i])
#         # if open units > 
#         # prices closer to PP get loaded earlier
#     elif strat == "IT":
#         # if open units > 0
#         # prices closer to SMAs get loaded earlier
#     elif start == "MAC":
# Good example of a script that solves on optimizer type problem
# Similar to how indicator routines are ran seperate from the strategy
# def IT_BreakEven(account_num, sec, trd_entry, curr_price, vol, vol_adj, file_nm, LIVE_ACCESS_TOKEN):
#     if IT["BEV"][sec] == 0:
#         IT["BEV"][sec] += vol + vol_adj
#         IT["SL"][sec] = trd_entry*(vol/IT["BEV"][sec]) + curr_price*(vol_adj/IT["BEV"][sec])
#     else:
#         prev_BEV = IT["BEV"][sec[i]]
#         IT["BEV"][sec] += vol_adj
#         IT["SL"][sec] = IT["SL"][sec]*(prev_BEV/IT["BEV"][sec]) + curr_price*(vol_adj/IT["BEV"][sec])
#     Open_IDs = GetOpenTradeIDs(account_num, sec)
#     for j in range(len(Open_IDs)):
#         UpdateStopLoss(account_num, Open_IDs[j], IT["SL"][sec], file_nm, LIVE_ACCESS_TOKEN)
