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
            M5H, M5L, M5C = Get_Price(sec[i], "M15", 17, "hlc", "midpoint")
            Indicators[sec[i]]["Z"] = Get_Z(M5C, 4)
            Indicators[sec[i]]["Max 4"] = max(M5H[1:4])
            Indicators[sec[i]]["Min 4"] = min(M5L[1:4])
            Indicators[sec[i]]["Max 16"] = max(M5H[1:16])
            Indicators[sec[i]]["Min 16"] = min(M5L[1:16])
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