import requests
import json
from array import *
from Settings import PRICE_DOMAIN, ACCOUNT_DOMAIN, DEMO_ACCESS_TOKEN, ACCOUNT_ID, STRT, STRO, STRH, STRL, STRC, STRV, STRCO
import httplib
import urllib
from datetime import datetime, timedelta
import time
import matplotlib.pyplot as plt
import numpy as np
import pypyodbc
import pandas as pd

def CheckDateRange(start,end):
    if np.busday_count(start, end ) <= 5000:
        return True
    else:
        return False

def pDate(sym, tf, start, end):
    if CheckDateRange(start, end) == True:
        h = {'Authorization' : DEMO_ACCESS_TOKEN}
        url = "https://api-fxpractice.oanda.com/v1/candles?instrument=" + str(sym) + "&start=" + str(start) + "&end=" + str(end) + "&candleFormat=midpoint&granularity=" + str(tf)
        r = requests.get(url, headers=h)     
        data = json.loads(r.text)
        iterable = (x[STRT] for x in data["candles"])
        a = np.fromiter(iterable, np.dtype('a27'), count=-1)
        return a

def pOpen(sym, tf, start, end):
    if CheckDateRange(start, end) == True:
        h = {'Authorization' : DEMO_ACCESS_TOKEN}
        url = "https://api-fxpractice.oanda.com/v1/candles?instrument=" + str(sym) + "&start=" + str(start) + "&end=" + str(end) + "&candleFormat=midpoint&granularity=" + str(tf)
        r = requests.get(url, headers=h)     
        data = json.loads(r.text)
        iterable = (x[STRO] for x in data["candles"])
        a = np.fromiter(iterable, np.float, count=-1)
        return a

def pHigh(sym, tf, start, end):
    if CheckDateRange(start, end) == True:
        h = {'Authorization' : DEMO_ACCESS_TOKEN}
        url = "https://api-fxpractice.oanda.com/v1/candles?instrument=" + str(sym) + "&start=" + str(start) + "&end=" + str(end) + "&candleFormat=midpoint&granularity=" + str(tf)
        r = requests.get(url, headers=h)     
        data = json.loads(r.text)
        iterable = (x[STRH] for x in data["candles"])
        a = np.fromiter(iterable, np.float, count=-1)
        return a

def pLow(sym, tf, start, end):
    if CheckDateRange(start, end) == True:
        h = {'Authorization' : DEMO_ACCESS_TOKEN}
        url = "https://api-fxpractice.oanda.com/v1/candles?instrument=" + str(sym) + "&start=" + str(start) + "&end=" + str(end) + "&candleFormat=midpoint&granularity=" + str(tf)
        r = requests.get(url, headers=h)     
        data = json.loads(r.text)
        iterable = (x[STRL] for x in data["candles"])
        a = np.fromiter(iterable, np.float, count=-1)
        return a

def pClose(sym, tf, start, end):
    if CheckDateRange(start, end) == True:      
        h = {'Authorization' : DEMO_ACCESS_TOKEN}
        url = "https://api-fxpractice.oanda.com/v1/candles?instrument=" + str(sym) + "&start=" + str(start) + "&end=" + str(end) + "&candleFormat=midpoint&granularity=" + str(tf)
        r = requests.get(url, headers=h)     
        data = json.loads(r.text)
        iterable = (x[STRC] for x in data["candles"])
        a = np.fromiter(iterable, np.float, count=-1)
        return a

def pMa(data, window_size):
    return pd.rolling_mean(data, window_size, min_periods=1)

def pStd(data, window_size):
    return pd.rolling_std(data, window_size, min_periods=1)

def pPivotPoints(h,l,c,c2):
    piv = []
    PP = (h + l + c)/3
    S1 = 2*PP - h
    S2 = PP - h + l
    R1 = 2*PP - l
    R2 = PP + h - l
    UpperPP = 0.0
    LowerPP = 0.0
    if c2 > R2:
        UpperPP = c2*2
        LowerPP = R2
    elif c2 > R1 and c2 < R2:
        UpperPP = R2
        LowerPP = R1
    elif c2 > PP and c2 < R1:
        UpperPP = R1
        LowerPP = PP
    elif c2 > S1 and c2 < PP:
        UpperPP = PP
        LowerPP = S1
    elif c2 > S2 and c2 < S1:  
        UpperPP = S1
        LowerPP = S2
    elif c2 < S2:
        UpperPP = S2
        LowerPP = c2/2
    piv.append(UpperPP)
    piv.append(LowerPP)
    a = np.array(piv)
    return a

def Piv(c,i,mgnret):
    if c(i-1)/c(i)-1 > mgnret and c(i+1)/c(i)-1 > mgnret:
        return "Maxpt"
    elif Close(i-1)/Close(i)-1 < -mgnret and Close(i+1)/Close(i)-1 < -mgnret:
        return "Minpt"
    else:
        return "None"

def pATR(close,high,low, period,end):
    p = len(close) - 1
    TrueRanges = 0.0
    ATR_val = 0
    while p > len(close) - 1 - period:
        TrueRanges = TrueRanges + TR(high[p],low[p],close[p-1])
        p -= 1
    ATR_val = TrueRanges/period
    while p >= end:
        ATR_val = (ATR_val*(period-1) + TR(high[p],low[p],close[p-1]))/period
        p -= 1
    return ATR_val

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

def SkhettiStats(array1, array2, array3, test, window, results):
    i = len(array1) - window - 1
    Highs = []
    Lows = []
    Index_Highs = []
    Index_Lows = []    
    while i >=0:
        Ret = []    
        if array1[i] < array2[i]:
            for j in range(0,window):
                r = (array3[i]-array3[i+j])*10000
                Ret.append(r)
            a = np.array(Ret)
            Highs.append(max(a))
            Lows.append(min(a))
            Max_indices = np.where(a == max(a))
            Min_indices = np.where(a == min(a))
            IH = str(np.take(Max_indices,[0]))
            IL = str(np.take(Min_indices,[0]))
            IH1 = IH[1:]
            IH2 = IH1[:len(IH1)-1]
            IL1 = IL[1:]
            IL2 = IL1[:len(IL1)-1]
            Index_Highs.append(float(IH2))
            Index_Lows.append(float(IL2))
        i -= 1

    a = np.array(Highs)
    print "Average of highs " + str(np.average(a))
    print "Std dev of highs " + str(np.std(a))
    print "Max High of " + str(max(a))
    print "Min High of " + str(min(a))
    a = np.array(Index_Highs)
    print "Average of location of highs " + str(np.average(a))
    print "Std dev of location of highs " + str(np.std(a))
    a = np.array(Lows)
    print "Average of lows " + str(np.average(a))
    print "Std dev of lows " + str(np.std(a))
    print "Max lows of " + str(max(a))
    print "Min lows of " + str(min(a))
    a = np.array(Index_Lows)
    print "Average of location of lows " + str(np.average(a))
    print "Std dev of location of lows " + str(np.std(a))