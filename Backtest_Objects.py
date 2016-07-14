import requests
import json
from array import *
from Settings import STRT, STRO, STRH, STRL, STRC, STRV, STRCO
import httplib
import urllib
from datetime import datetime, timedelta
import time
import matplotlib.pyplot as plt
import numpy as np
import pypyodbc
import pandas as pd
import csv
from numpy import genfromtxt
import calendar

# --------------- Backtest Functions -------------------- #

class MarketOnClosePortfolio:
    def __init__(self, symbol, bars, lots, Entry_array, Exit_array, initial_capital = 1000):
        self.symbol = symbol
        self.bars = bars
        self.initial_capital = float(initial_capital)
        self.Entry = Entry_array
        self.Exit = Exit_array
        self.lots = lots
        self.positions = self.lots*self.fill_positions()

    def fill_positions(self):
        num_trades = 0
        positions = np.zeros((1, len(self.Entry)))
        spacer = 10
        last_entry = 0
        for i in range(1, len(self.Entry)):
            if positions[0,i-1] == 1:
                if self.Exit[i] == 1:
                    positions[0,i] = 0
                else:
                    positions[0,i] = 1
            else:
                if self.Entry[i] == 1 and i - last_entry >  spacer:
                    num_trades += 1
                    positions[0,i] = 1
                    last_entry = i
                else:
                    positions[0,i] = 0
        print num_trades
        return positions[0,:]

    def backtest_portfolio(self):
        portfolio = self.positions*self.bars
        pos_diff = np.diff(self.positions)
        pos_diff = np.insert(pos_diff,0,0)
        portfolio_holdings = portfolio
        portfolio_cash =self.initial_capital - (pos_diff*self.bars).cumsum()
        portfolio_total = portfolio_holdings + portfolio_cash
        return portfolio_total

def ZScoreSpreads(mc1, mc2, window):
    price1 = pd.DataFrame(mc1)
    price2 = pd.DataFrame(mc2)
    price1_chng = price1.pct_change()
    price2_chng = price2.pct_change()
    spread = price1_chng/price2_chng
    print spread
    print pMa(price1_chng, window)
    print pStd(price1_chng, window)
    print pMa(price2_chng, window)
    print pStd(price2_chng, window)
    print pMa(spread, window)
    print pStd(spread, window)

def backtest_stats(portfolio_array):
    for j in range(0,portfolio_array.shape[0]):
        for i in range(0, portfolio_array.shape[1]):
            print portfolio_array[j, i]

    cnt_wbuy_trades = 0
    cnt_wsell_trades = 0
    cnt_lbuy_trades = 0
    cnt_lsell_trades = 0

    Total_Buy = 0
    Total_Buy = cnt_wbuy_trades + cnt_lbuy_trades
    Total_Sell = 0
    Total_Sell = cnt_wsell_trades + cnt_lsell_trades

    print "------  Stats  ------"
    print "Total Trades: " + str(Total_Buy + Total_Sell)
    print "Accuracy: " + str(round((float(cnt_wbuy_trades + cnt_wsell_trades))/(Total_Buy + Total_Sell),3))
    print "Total Buy Trades: " + str(cnt_wbuy_trades+cnt_lbuy_trades)
    print "Buy Accuracy: " + str(round(float(cnt_wbuy_trades)/(cnt_wbuy_trades+cnt_lbuy_trades),3))  
    print "Total Sell Trades: " + str(cnt_wsell_trades+cnt_lsell_trades)
    print "Sell Accuracy: " + str(round(float(cnt_wsell_trades)/(cnt_wsell_trades+cnt_lsell_trades),3))

def SaveToPlot(Plot_Array, Results_Array ,Column_Index):
    for i in range(0,len(Results_Array)):
        Plot_Array[Column_Index,i] = Results_Array[i]
    return Plot_Array
    
def MovingAverageCross(Short_MA, Long_MA):
    MAC_data = np.zeros((1,max(len(Short_MA),len(Long_MA))))
    for i in range(0,max(len(Short_MA),len(Long_MA))):
        if Short_MA[i] > Long_MA[i]:
            MAC_data[0,i] = 1
    return MAC_data[0,:]

def UpperMovingAverageBand(pr, ma_array, sd_array, mult, brk):
    UMAB_data = np.zeros((1,len(pr)))
    if brk == "U":
        for i in range(0,len(pr)):
            if pr[i] > ma_array[i] + mult*sd_array[i] and pr[i-1] < ma_array[i-1] + mult*sd_array[i-1]:
                UMAB_data[0,i] = 1
        return UMAB_data[0,:]
    elif brk == "D":
        for i in range(0,len(pr)):
            if pr[i] < ma_array[i] + mult*sd_array[i] and pr[i-1] > ma_array[i-1] + mult*sd_array[i-1]:
                UMAB_data[0,i] = 1
        return UMAB_data[0,:]

def LowerMovingAverageBand(pr, ma_array, sd_array, mult, brk):
    LMAB_data = np.zeros((1,len(pr)))
    if brk == "U":
        for i in range(0,len(pr)):
            if pr[i] > ma_array[i] - mult*sd_array[i] and pr[i-1] < ma_array[i-1] - mult*sd_array[i-1]:
                LMAB_data[0,i] = 1
        return LMAB_data[0,:]
    elif brk == "D":
        for i in range(0,len(pr)):
            if pr[i] < ma_array[i] - mult*sd_array[i] and pr[i-1] > ma_array[i-1] - mult*sd_array[i-1]:
                LMAB_data[0,i] = 1
        return LMAB_data[0,:]

def IndicatorScreen(indicatorarray, upperindicatorval, lowerindicatorval):
    IS_data = np.zeros((1,len(indicatorarray)))
    for i in range(0,len(indicatorarray)):
        if indicatorarray[i] >= lowerindicatorval and indicatorarray[i] < upperindicatorval:
            IS_data[0,i] = 1
    return IS_data[0,:]

# ------------------------- Prices ------------------------- #

def ConvertToTime(txt):
    if txt == "1 hour":
        return 3600
    elif txt == "12 hours":
        return 3600
    elif txt == "1 day":
        return 86400
    elif txt == "1 week":
        return 604800
    elif txt == "1 month":
        return 2592000
    elif txt == "3 months":
        return 7776000
    elif txt == "6 months":
        return 15552000
    elif txt == "1 year":
        return 31536000

def CheckDateRange(start,end):
    if np.busday_count(start, end ) <= 5000:
        return True
    else:
        return False

def pYear(dt):
    return int(dt[:4])

def pMonth(dt):
    mnth = dt[:7]
    return int(mnth[len(mnth)-2:])

def pDay(dt):
    return int(dt[len(dt) -2:])

def FindDateRange(start, tf):
    yr = pYear(start)
    mnth = pMonth(start)
    dy = pDay(start)
    if mnth >= 10:
        month_string = str(mnth)
    else:
        month_string = "0" + str(mnth)
    if dy >= 10:
        day_string = str(dy)
    else:
        day_string = "0" + str(dy)
    # print "from function init: " + str(yr) + "-" + month_string + "-" + day_string 
    while np.busday_count(start, str(yr) + "-" + month_string + "-" + day_string) <= 3000/(tf):
        if calendar.monthrange(yr, mnth)[1] != dy + 1:
            dy = dy + 1
            if dy >= 10:
                day_string = str(dy)
            else:
                day_string = "0" + str(dy)
        else:
            if mnth + 1 > 12:
                yr += 1
                mnth = 1
            else:
                mnth += 1
            
            if mnth >= 10:
                month_string = str(mnth)
            else:
                month_string = "0" + str(mnth)
            dy = calendar.monthrange(yr, mnth)[0]
            if dy == 0:
                dy = 1

            if dy >= 10:
                day_string = str(dy)
            else:
                day_string = "0" + str(dy)
    # print "from function: " + str(yr) + "-" + month_string + "-" + day_string 
    return str(yr) + "-" + month_string + "-" + day_string 

# def pOpen():
#     return genfromtxt('OpenPrices.csv', delimiter=',')
# def pHigh():
#     return genfromtxt('HighPrices.csv', delimiter=',')
# def pLow():
#     return genfromtxt('LowPrices.csv', delimiter=',')
# def pClose():
#     return genfromtxt('ClosePrices.csv', delimiter=',')

def pHour(md):
    Hour_Data = []
    for i in range(0, len(md)):
        x = md[i]
        x1 = str(x)
        y2 = x1[11:]
        z2 = y2[:len(y2)-14]
        Hour_Data.append(int(z2))
    return np.array(Hour_Data)

def pMinute(md):
    Minute_Data = []
    for i in range(0, len(md)):
        x = md[i]
        x1 = str(x)
        y2 = x1[14:]
        z2 = y2[:len(y2)-11]
        Minute_Data.append(int(z2))
    return np.array(Minute_Data)

def pDate(sym, tf, start, end):
    if CheckDateRange(start, end) == True:
        h = {'Authorization' : DEMO_ACCESS_TOKEN}
        url = "https://api-fxpractice.oanda.com/v1/candles?instrument=" + str(sym) + "&start=" + str(start) + "&end=" + str(end) + "&candleFormat=midpoint&granularity=" + str(tf)
        r = requests.get(url, headers=h)     
        data = json.loads(r.text)
        # print data
        iterable = (x[STRT] for x in data["candles"])
        a = np.fromiter(iterable, np.dtype('a27'), count=-1)
        return np.array(a)

def pOpen(sym, tf, start, end):
    if CheckDateRange(start, end) == True:
        h = {'Authorization' : DEMO_ACCESS_TOKEN}
        url = "https://api-fxpractice.oanda.com/v1/candles?instrument=" + str(sym) + "&start=" + str(start) + "&end=" + str(end) + "&candleFormat=midpoint&granularity=" + str(tf)
        r = requests.get(url, headers=h)     
        data = json.loads(r.text)
        # print data
        iterable = (x[STRO] for x in data["candles"])
        a = np.fromiter(iterable, np.float, count=-1)
        return np.array(a)

def pHigh(sym, tf, start, end):
    if CheckDateRange(start, end) == True:
        h = {'Authorization' : DEMO_ACCESS_TOKEN}
        url = "https://api-fxpractice.oanda.com/v1/candles?instrument=" + str(sym) + "&start=" + str(start) + "&end=" + str(end) + "&candleFormat=midpoint&granularity=" + str(tf)
        r = requests.get(url, headers=h)     
        data = json.loads(r.text)
        # print data
        iterable = (x[STRH] for x in data["candles"])
        a = np.fromiter(iterable, np.float, count=-1)
        return np.array(a)

def pLow(sym, tf, start, end):
    if CheckDateRange(start, end) == True:
        h = {'Authorization' : DEMO_ACCESS_TOKEN}
        url = "https://api-fxpractice.oanda.com/v1/candles?instrument=" + str(sym) + "&start=" + str(start) + "&end=" + str(end) + "&candleFormat=midpoint&granularity=" + str(tf)
        r = requests.get(url, headers=h)     
        data = json.loads(r.text)
        # print data
        iterable = (x[STRL] for x in data["candles"])
        a = np.fromiter(iterable, np.float, count=-1)
        return np.array(a)

def pClose(sym, tf, start, end):
    if CheckDateRange(start, end) == True:      
        h = {'Authorization' : DEMO_ACCESS_TOKEN}
        url = "https://api-fxpractice.oanda.com/v1/candles?instrument=" + str(sym) + "&start=" + str(start) + "&end=" + str(end) + "&candleFormat=midpoint&granularity=" + str(tf)
        r = requests.get(url, headers=h)     
        data = json.loads(r.text)
        # print data
        iterable = (x[STRC] for x in data["candles"])
        a = np.fromiter(iterable, np.float, count=-1)
        return np.array(a)

def COT_OpenInterest(sym):
    h = {'Authorization' : DEMO_ACCESS_TOKEN}
    url = "https://api-fxpractice.oanda.com/labs/v1/commitments_of_traders?instrument=" + str(sym)
    r = requests.get(url, headers=h)     
    data = json.loads(r.text)
    iterable = (x["oi"] for x in data[sym])
    a = np.fromiter(iterable, np.float, count=-1)
    print a

def COT_NCL(sym):
    h = {'Authorization' : DEMO_ACCESS_TOKEN}
    url = "https://api-fxpractice.oanda.com/labs/v1/commitments_of_traders?instrument=" + str(sym)
    r = requests.get(url, headers=h)     
    data = json.loads(r.text)
    iterable = (x["ncl"] for x in data[sym])
    a = np.fromiter(iterable, np.float, count=-1)
    print a

def COT_NCS(sym):
    h = {'Authorization' : DEMO_ACCESS_TOKEN}
    url = "https://api-fxpractice.oanda.com/labs/v1/commitments_of_traders?instrument=" + str(sym)
    r = requests.get(url, headers=h)     
    data = json.loads(r.text)
    iterable = (x["ncs"] for x in data[sym])
    a = np.fromiter(iterable, np.float, count=-1)
    print a

def COT_Price(sym):
    h = {'Authorization' : DEMO_ACCESS_TOKEN}
    url = "https://api-fxpractice.oanda.com/labs/v1/commitments_of_traders?instrument=" + str(sym)
    r = requests.get(url, headers=h)     
    data = json.loads(r.text)
    iterable = (x["price"] for x in data[sym])
    a = np.fromiter(iterable, np.float, count=-1)
    print a

def COT_Unit(sym):
    h = {'Authorization' : DEMO_ACCESS_TOKEN}
    url = "https://api-fxpractice.oanda.com/labs/v1/commitments_of_traders?instrument=" + str(sym)
    r = requests.get(url, headers=h)     
    data = json.loads(r.text)
    iterable = (x["unit"] for x in data[sym])
    a = np.fromiter(iterable, np.float, count=-1)
    print a

def Calendar(sym, tm):
    tm = ConvertToTime(tm)
    h = {'Authorization' : DEMO_ACCESS_TOKEN}
    url = "https://api-fxpractice.oanda.com/labs/v1/calendar?instrument=" + str(sym) + "&period=" + str(tm)
    r = requests.get(url, headers=h)     
    data = json.loads(r.text)
    iterable = (x["title"] for x in data)
    a = np.fromiter(iterable, np.dtype('a27'), count=-1)
    return a

def Calendar_Currency(sym, tm):
    tm = ConvertToTime(tm)
    h = {'Authorization' : DEMO_ACCESS_TOKEN}
    url = "https://api-fxpractice.oanda.com/labs/v1/calendar?instrument=" + str(sym) + "&period=" + str(tm)
    r = requests.get(url, headers=h)     
    data = json.loads(r.text)
    iterable = (x["currency"] for x in data)
    a = np.fromiter(iterable, np.dtype('a27'), count=-1)
    return a

def Calendar_Forecast(sym, tm):
    tm = ConvertToTime(tm)
    h = {'Authorization' : DEMO_ACCESS_TOKEN}
    url = "https://api-fxpractice.oanda.com/labs/v1/calendar?instrument=" + str(sym) + "&period=" + str(tm)
    r = requests.get(url, headers=h)     
    data = json.loads(r.text)
    print data
    # iterable = (x["forecast"] for x in data)
    # a = np.fromiter(iterable, np.float, count=-1)
    # print a

def Calendar_Previous(sym, tm):
    tm = ConvertToTime(tm)
    h = {'Authorization' : DEMO_ACCESS_TOKEN}
    url = "https://api-fxpractice.oanda.com/labs/v1/calendar?instrument=" + str(sym) + "&period=" + str(tm)
    r = requests.get(url, headers=h)     
    data = json.loads(r.text)
    iterable = (x["previous"] for x in data)
    a = np.fromiter(iterable, np.float, count=-1)
    print a

def Calendar_Actual(sym, tm):
    tm = ConvertToTime(tm)
    h = {'Authorization' : DEMO_ACCESS_TOKEN}
    url = "https://api-fxpractice.oanda.com/labs/v1/calendar?instrument=" + str(sym) + "&period=" + str(tm)
    r = requests.get(url, headers=h)     
    data = json.loads(r.text)
    # print data
    for i in range(0, 10):
        print data[i]["actual"]
    iterable = (x["actual"] for x in data)
    a = np.fromiter(iterable, np.float, count=-1)
    print a

def Calendar_Market(sym, tm):
    tm = ConvertToTime(tm)
    h = {'Authorization' : DEMO_ACCESS_TOKEN}
    url = "https://api-fxpractice.oanda.com/labs/v1/calendar?instrument=" + str(sym) + "&period=" + str(tm)
    r = requests.get(url, headers=h)     
    data = json.loads(r.text)
    iterable = (x["market"] for x in data)
    a = np.fromiter(iterable, np.float, count=-1)
    print a

# ------------------------- Candlestick Pattern ------------------------- #

def LevelizedPrice(mc, hr, End_Points, Window):
    sp = 0.0
    ep = 0.0
    lvlprice = np.zeros((1,len(mc)))
    for i in range(0, len(mc)-Window):
        if hr[i] == End_Points:
            sp = mc[i]
            ep = mc[i + Window]
            j = 0
        if sp != 0.0 and ep != 0.0:
            lvlprice[0,i] = mc[i]/(sp + j*(ep-sp)/Window)
            j += 1
    return lvlprice[0,:]


def PriceAction(hr, Price_Action, hour_time, avg_period):
    Beam6 = []
    for i in range(0,len(hr)):
        if hr[i] == hour_time:
            Beam6.append(Price_Action[i])
    return pMa(np.array(Beam6),avg_period)

def BearishReversal(o, h, l, c, rng):
    BearishReversal_Data = []
    BearishReversal_Data2 = []
    d = Doji(o,h,l,c)
    s = ShootingStar(o,h,l,c)
    g = Gravestone(o,h,l,c)
    l = LongLeggedDoji(o,h,l,c)
    e = EveningStar(o,h,l,c)
    bekr = BearishKeyReversal(o,h,l,c)
    d = np.array(d)
    s = np.array(s)
    g = np.array(g)
    l = np.array(l)
    e = np.array(e)
    bekr = np.array(bekr)
    for i in range(0,len(c)):
        if d[i] == 1 or s[i] == 1 or g[i] == 1 or l[i] == 1 or e[i] == 1 or bekr[i] == 1:
            BearishReversal_Data.append(1)
        else:
            BearishReversal_Data.append(0)
    if rng == 0:
        return BearishReversal_Data
    else:
        for i in range(0, len(c)):
            sum_data = 0
            for j in range(0,min(i,rng)):
                sum_data = sum_data + BearishReversal_Data[i-j] 
            if sum_data >=1:
                BearishReversal_Data2.append(1)
            else:
                BearishReversal_Data2.append(0)
        return BearishReversal_Data2

def BullishReversal(o, h, l, c, rng):
    BullishReversal_Data = []
    BullishReversal_Data2 = []
    d = Doji(o,h,l,c)
    h = Hammer(o,h,l,c)
    dr = Dragonfly(o,h,l,c)
    l = LongLeggedDoji(o,h,l,c)
    m = MorningStar(o,h,l,c)
    bukr = BullishKeyReversal(o,h,l,c)
    d = np.array(d)
    h = np.array(h)
    dr = np.array(dr)
    l = np.array(l)
    m = np.array(m)
    bukr = np.array(bukr)
    for i in range(0,len(c)):
        if d[i] == 1 or h[i] == 1 or dr[i] == 1 or l[i] == 1 or m[i] == 1 or bukr[i] == 1:
            BullishReversal_Data.append(1)
        else:
            BullishReversal_Data.append(0)
    if rng == 0:
        return BullishReversal_Data
    else:
        for i in range(0, len(c)):
            sum_data = 0
            for j in range(0,min(i,rng)):
                sum_data = sum_data + BullishReversal_Data[i-j] 
            if sum_data >=1:
                BullishReversal_Data2.append(1)
            else:
                BullishReversal_Data2.append(0)
        return BullishReversal_Data2


def BullishMarubozu(o, h, l, c):
    BullM_data = []
    for i in range(0, max(len(o),len(h),len(l),len(c))):
        if c[i] > o[i] and TR(h[i], l[i], o[i])/c[i] > 0.25 and h[i] - max(o[i],c[i]) < 0.1*(c[i] - o[i]) and 0.1*(c[i] - o[i]) > min(o[i],c[i]) - l[i]:
            BullM_data.append(1)
        else:
            BullM_data.append(0)
    return BullM_data

def BearishMarubozu(o, h, l, c):
    BearM_data = []
    for i in range(0, max(len(o),len(h),len(l),len(c))):
        if c[i] < o[i] and TR(h[i], l[i], o[i])/c[i] > 0.25 and h[i] - max(o[i],c[i]) < 0.1*(c[i] - o[i]) and 0.1*(c[i] - o[i]) > min(o[i],c[i]) - l[i]:
            BearM_data.append(1)
        else:
            BearM_data.append(0)
    return BearM_data

def LongLeggedDoji(o, h, l, c):
    LongLeggedDoji_data = []
    for i in range(0, max(len(o),len(h),len(l),len(c))):
        if abs(o[i] - c[i]) < 0.001 and h[i]-max(o[i],c[i]) > 0.004 and min(o[i],c[i]) - l[i] > 0.004 :
            LongLeggedDoji_data.append(1)
        else:
            LongLeggedDoji_data.append(0)
    return LongLeggedDoji_data

def Doji(o, h, l, c):
    Doji_data = []
    for i in range(0, max(len(o),len(h),len(l),len(c))):
        if abs(o[i] - c[i]) < 0.001:
            Doji_data.append(1)
        else:
            Doji_data.append(0)
    return Doji_data

def Gravestone(o,h,l,c):
    Gravestone_Data = []
    s = ShootingStar(o,h,l,c)
    d = Doji(o,h,l,c)
    for i in range(0,max(len(s),len(d))):
        if s[i] == 1 and d[i] == 1:
            Gravestone_Data.append(1)
        else:
            Gravestone_Data.append(0)
    return Gravestone_Data

def Dragonfly(o,h,l,c):
    Dragonfly_Data = []
    h = Hammer(o,h,l,c)
    d = Doji(o,h,l,c)
    g = h + d
    for i in range(0,len(g)):
        if g[i] == 2:
            Dragonfly_Data.append(1)
        else:
            Dragonfly_Data.append(0)
    return Dragonfly_Data

def Hammer(o,h,l,c):
    Hammer_data = []
    for i in range(0, max(len(o),len(h),len(l),len(c))):
        if o[i] < c[i] and 3*(abs(h[i] - o[i])) < o[i] - l[i]:
            Hammer_data.append(1)
        elif o[i] > c[i] and 3*(abs(h[i] - c[i])) < c[i] - l[i]:
            Hammer_data.append(1)
        else:
            Hammer_data.append(0)
    return Hammer_data

def ShootingStar(o,h,l,c):
    ShootingStar_data = []
    for i in range(0, max(len(o),len(h),len(l),len(c))):
        if o[i] < c[i] and 3*(abs(l[i] - c[i])) < h[i] - c[i]:
            ShootingStar_data.append(1)
        elif o[i] > c[i] and 3*(abs(o[i] - l[i])) < h[i] - o[i]:
            ShootingStar_data.append(1)
        else:
            ShootingStar_data.append(0)
    return ShootingStar_data

def MorningStar(o,h,l,c):
    be = BearishMarubozu(o,h,l,c)
    bu = BullishMarubozu(o,h,l,c)
    h = Hammer(o,h,l,c)
    dr = Dragonfly(o,h,l,c)
    do = Doji(o,h,l,c)
    MorningStar_Data = np.zeros((1,max(len(o),len(h),len(l),len(c))))
    rev = h + dr + do
    for i in range(1,max(len(o),len(h),len(l),len(c))):
        if rev[i] > 0 and be[i-1] == 1 and bu[i+1] == 1:
            MorningStar_Data[0,i] = 1
    return MorningStar_Data[0,:]

def EveningStar(o,h,l,c):
    be = BearishMarubozu(o,h,l,c)
    bu = BullishMarubozu(o,h,l,c)
    s = ShootingStar(o,h,l,c)
    g = Gravestone(o,h,l,c)
    d = Doji(o,h,l,c)
    EveningStar_Data = np.zeros((1,max(len(o),len(h),len(l),len(c))))
    for i in range(1,max(len(o),len(h),len(l),len(c))):
        if (s[i] == 0 or g[i] == 0 or d[i] == 0) and bu[i-1] == 1 and be[i+1] == 1:
            EveningStar_Data[0,i] = 1
    return EveningStar_Data[0,:]

def LongUp(c):
    LU_data = np.zeros((1,len(c)))
    sd_data = pStd(c,50)
    for i in range(0, len(c)):
        if c[i] - c[i-1] > 2*sd_data[i]:
            LU_data[0,i] = 1
    return LU_data[0,:]

def LongDown(c):
    LD_data = np.zeros((1,len(c)))
    sd_data = pStd(c,50)
    for i in range(0, len(c)):
        if c[i] - c[i-1] > 2*sd_data[i]:
            LD_data[0,i] = 1
    return LD_data[0,:]

def FallingThree(o,h,l,c):
    FT_data = np.zeros((1,len(c)))
    m = BearishMarubozu(o,h,l,c)
    for i in range(0, len(c)):
        if m[i] ==1 and m[i-4] == 1:
            max_range = max(h[i], h[i-4])
            min_range = min(l[i], l[i-4])
            if max_range > h[i-1] and max_range > h[i-2] and max_range > h[i-3] and min_range < l[i-1] and min_range < l[i-2] and min_range < l[i-3]:
                RT_data[0,i] = 1
    return FT_data[0,:]

def RisingThree(o,h,l,c):
    RT_data = np.zeros((1,len(c)))
    m = BullishMarubozu(o,h,l,c)
    for i in range(0, len(c)):
        if m[i] ==1 and m[i-4] == 1:
            max_range = max(h[i], h[i-4])
            min_range = min(l[i], l[i-4])
            if max_range > h[i-1] and max_range > h[i-2] and max_range > h[i-3] and min_range < l[i-1] and min_range < l[i-2] and min_range < l[i-3]:
                RT_data[0,i] = 1
    return RT_data[0,:]

def ThreeWhiteSoldiers(c):
    TWS_data = np.zeros((1,len(c)))
    sd_data = pStd(c,50)
    for i in range(0, len(c)):
        if c[i] - c[i-1] > 2*sd_data[i] and c[i-1] - c[i-2] > 2*sd_data[i] and c[i-2] - c[i-3] > 2*sd_data[i]:
            TWS_data[0,i] = 1
    return TWS_data[0,:]

def ThreeBlackCrows(c):
    TBC_data = np.zeros((1,len(c)))
    sd_data = pStd(c,50)
    for i in range(0, len(c)):
        if c[i] - c[i-1] < -2*sd_data[i] and c[i-1] - c[i-2] < -2*sd_data[i] and c[i-2] - c[i-3] < -2*sd_data[i]:
            TBC_data[0,i] = 1
    return TBC_data[0,:]

def InsideBar(h,l):
    InsideBar_data = np.zeros((1,max(len(h),len(l))))
    for i in range(3, max(len(h),len(l))):
        if h[i-1] > h[i] and l[i-1] < l[i]:
            InsideBar_data[0, i] = 1
        else:
            InsideBar_data[0, i] = 0
    return InsideBar_data[0,:]

def BullishKeyReversal(o,h,l,c):
    BuKR_data = np.zeros((1,len(c)))
    for i in range(0, len(c)):
        if o[i] > c[i] and o[i-1] < c[i-1] and l[i] < l[i-1] and c[i] > h[i-1]:
            BuKR_data[0,i] = 1
    return BuKR_data[0,:]

def BearishKeyReversal(o,h,l,c):
    BeKR_data = np.zeros((1,len(c)))
    for i in range(0, len(c)):
        if o[i] < c[i] and o[i-1] > c[i-1] and h[i] < h[i-1] and c[i] < l[i-1]:
            BeKR_data[0,i] = 1
    return BeKR_data[0,:]

# ------------------------- Chart Patterns ------------------------- #

def Generate_Levels(o,h,l,c):
    lvls_data = []
    r = Renko(c,0.01)
    p = Peak(r, 2, 0.0005)
    t = Trough(r, 2, 0.0005)
    # d = Doji(o,h,l,c)
    # for i in range(0,max(len(o),len(h),len(l),len(c))):
    #     if d[i] == 1:
    #         lvls_data.append(c[i])
    for i in range(0,len(r)):
        if p[i] != 0:
            lvls_data.append(p[i])
        elif t[i] != 0:
            lvls_data.append(t[i])
    for j in range(0,1):
        a = np.array(lvls_data)
        a = np.sort(a)
        lvls_data = []
        i = 0
        while i <= len(a)-2:
            if a[i+1] - a[i] < 0.001:
                lvls_data.append((a[i+1]+a[i])/2)
                i += 2
            else:
                lvls_data.append(a[i])
                i +=1
    lvls_data.append(a[len(a)-1])
    lvls_data.append(a[len(a)-2])
    return lvls_data

def Levels_Filter(lvls, c):
    Filtered_lvls = []
    lvls_Data = []
    lvls_Stats = []
    Stats = []
    lvls_count = np.zeros((1,len(lvls)))
    lvls_rec = np.zeros((1,len(lvls)))
    lvl_cnt = 0.0
    lvl_rc = 0.0
    cnt = 0
    for x in lvls:
        for i in range(0,len(c)):
            if abs(c[i] - x) < 0.0005:
                lvl_cnt += 1
        for i in range(0,len(c)):
            if abs(c[len(c) - i - 1] - x) < 0.0005:
                lvl_rc = i
                break
        lvls_count[0, cnt] = lvl_cnt
        lvls_rec[0, cnt] = lvl_rc
        cnt += 1
    ttl_cnt = np.sum(lvls_count[0,:])
    ttl_rec = np.sum(lvls_rec[0,:])
    lvls_count = (ttl_cnt - lvls_count[0,:])/(len(lvls_count[0,:])*ttl_cnt)
    lvls_rec = lvls_rec[0,:]/ttl_rec
    for i in range(0, len(lvls_count)):
        lvls_Data.append((lvls_count[i] + lvls_rec[i])/2)
    a = np.sort(lvls_Data)
    lvls_Stats = lvls_Data
    for i in range(0,len(a)):
        tst = a[len(a) - i - 1]
        index_val = lvls_Stats.index(tst)
        Filtered_lvls.append(lvls[index_val])
    return Filtered_lvls

def Levels_Locate(lvl, c, direction):
    if direction == "L":
        for i in range(0,len(c)):
            if abs(c[i]-lvl) < 0.00025:
                return i
                break
    elif direction == "R":
        for i in range(1,len(c)):
            if abs(c[len(c)-i]-lvl) < 0.00025:
                return len(c)-i
                break

def SwingHighsLows(c, t, n):
    Price_Window = []
    SHL = []
    for i in range(t,n):
        Price_Window.append(c[i])
    SwingHigh = max(Price_Window)
    SwingLow = min(Price_Window)
    SHL.append(SwingHigh)
    SHL.append(SwingLow)
    return SHL    

def Peak(c, span,mgnret):
    Peak_Data = np.zeros((1,len(c)))
    for i in range(span,len(c)-span):
        if c[i-span]/c[i]-1 < -mgnret and c[i+span]/c[i]-1 < -mgnret:
            Peak_Data[0,i] = c[i]
        else:
            Peak_Data[0,i] = 0    
    return Peak_Data[0,:]

def Trough(c, span, mgnret):
    Trough_Data = np.zeros((1,len(c)))
    for i in range(span,len(c)-span):
        if c[i-span]/c[i]-1 > mgnret and c[i+span]/c[i]-1 > mgnret:
            Trough_Data[0,i] = c[i]
        else:
            Trough_Data[0,i] = 0   
    return Trough_Data[0,:]

def Renko(c,diff):
    Renko_Data = []
    base = round(c[0],3)
    for i in range(1,len(c)):
        num_bars = (c[i] - base)/diff
        if num_bars > 0:
            for j in range(0,int(num_bars)):
                Renko_Data.append(float(base + diff))
                base = base + diff
        elif num_bars < 0:
            for j in range(0,int(abs(num_bars))):
                Renko_Data.append(float(base - diff))
                base = base - diff
    return Renko_Data

def UpCnt(c,diff):
    r = Renko(c,diff)
    UpCnt = np.zeros((1,len(r)))
    for i in range(1,len(r)):
        if r[i] > r[i-1]:
            UpCnt[0,i] = UpCnt[0,i-1] + 1
    return UpCnt[0,:]

def DwnCnt(c,diff):
    r = Renko(c,diff)
    DwnCnt = np.zeros((1,len(r)))
    for i in range(1,len(r)):
        if r[i] < r[i-1]:
            DwnCnt[0,i] = DwnCnt[0,i-1] + 1
    return DwnCnt[0,:]

def HeadShoulders(c,ADrive,BDrive,CDrive,DDrive,EDrive,FDrive,diff):
    u = UpCnt(c, diff)
    d = DwnCnt(c,diff)
    HS_Data = np.zeros((1,len(u)))
    for i in range(1,len(u)):
        if u[i - DDrive - CDrive - BDrive  - EDrive - FDrive] >= ADrive and d[i - DDrive -CDrive - EDrive - FDrive] == BDrive and u[i - DDrive - EDrive - FDrive] == CDrive  and d[i - EDrive - FDrive] == DDrive and u[i - FDrive] == EDrive and d[i] >= FDrive:
            for j in range(0,ADrive+BDrive+CDrive+DDrive+EDrive+FDrive+1):
                HS_Data[0,i-j] = 1
    return HS_Data[0,:]

def ReverseHeadShoulders(c,ADrive,BDrive,CDrive,DDrive,EDrive,FDrive,diff):
    u = UpCnt(c, diff)
    d = DwnCnt(c,diff)
    RHS_Data = np.zeros((1,len(u)))
    for i in range(1,len(u)):
        if d[i - DDrive - CDrive - BDrive  - EDrive - FDrive] >= ADrive and u[i - DDrive -CDrive - EDrive - FDrive] == BDrive and d[i - DDrive - EDrive - FDrive] == CDrive  and u[i - EDrive - FDrive] == DDrive and d[i - FDrive] == EDrive and u[i] >= FDrive:
            for j in range(0,ADrive+BDrive+CDrive+DDrive+EDrive+FDrive+1):
                RHS_Data[0,i-j] = 1
    return RHS_Data[0,:]

def TripleTop(c,ADrive,BDrive,CDrive,DDrive,diff):
    u = UpCnt(c, diff)
    d = DwnCnt(c,diff)
    TT_Data = np.zeros((1,len(u)))
    for i in range(1,len(u)):
        if u[i - DDrive - 2*CDrive - 2*BDrive] >= ADrive and d[i - 2*DDrive -2*CDrive] == BDrive and u[i - 2*DDrive - CDrive] == CDrive and d[i - DDrive -CDrive] == BDrive and u[i - DDrive] == CDrive and d[i] >= DDrive:
            for j in range(0,ADrive+2*BDrive+2*CDrive+DDrive+1):
                TT_Data[0,i-j] = 1
    return TT_Data[0,:]

def TripleBottom(c,ADrive,BDrive,CDrive,DDrive,diff):
    u = UpCnt(c, diff)
    d = DwnCnt(c,diff)
    TB_Data = np.zeros((1,len(u)))
    for i in range(1,len(u)):
        if d[i - DDrive - 2*CDrive - 2*BDrive] >= ADrive and u[i - 2*DDrive -2*CDrive] == BDrive and d[i - 2*DDrive - CDrive] == CDrive and u[i - DDrive -CDrive] == BDrive and d[i - DDrive] == CDrive and u[i] >= DDrive:
            for j in range(0,ADrive+2*BDrive+2*CDrive+DDrive+1):
                TB_Data[0,i-j] = 1
    return TB_Data[0,:]

def DoubleTop(c,ADrive,BDrive,CDrive,DDrive,diff):
    u = UpCnt(c, diff)
    d = DwnCnt(c,diff)
    DT_Data = np.zeros((1,len(u)))
    for i in range(1,len(u)):
        if u[i - DDrive - CDrive - BDrive] >= ADrive and d[i - DDrive -CDrive] == BDrive and u[i - DDrive] == CDrive and d[i] >= DDrive:
            for j in range(0,ADrive+BDrive+CDrive+DDrive+1):
                DT_Data[0,i-j] = 1
    return DT_Data[0,:]

def DoubleBottom(c,ADrive,BDrive,CDrive,DDrive,diff):
    u = UpCnt(c, diff)
    d = DwnCnt(c,diff)
    DB_Data = np.zeros((1,len(u)))
    for i in range(1,len(u)):
        if d[i - DDrive - CDrive - BDrive] >= ADrive and u[i - DDrive - CDrive] == BDrive and d[i - DDrive] == CDrive and u[i] >= DDrive:
            for j in range(0,ADrive+BDrive+CDrive+DDrive+1):
                DB_Data[0,i-j] = 1
    return DB_Data[0,:]

def ABCUp(c,ADrive,BDrive,CDrive,diff):
    u = UpCnt(c, diff)
    d = DwnCnt(c,diff)
    ABCUp_Data = np.zeros((1,len(u)))
    for i in range(1,len(u)):
        if u[i-CDrive - BDrive] >= ADrive and d[i - CDrive] <= BDrive and u[i] >= CDrive:
            for j in range(0,ADrive+BDrive+CDrive+1):
                ABCUp_Data[0,i-j] = 1
    return ABCUp_Data[0,:]

def ABCDwn(c,ADrive,BDrive,CDrive,diff):
    u = UpCnt(c, diff)
    d = DwnCnt(c,diff)
    ABCDwn_Data = np.zeros((1,len(u)))
    for i in range(1,len(u)):
        if d[i-CDrive - BDrive] >= ADrive and u[i - CDrive] <= BDrive and d[i] >= CDrive:
            for j in range(0,ADrive+BDrive+CDrive+1):
                ABCDwn_Data[0,i-j] = 1
    return ABCDwn_Data[0,:]

def pATR(close,high,low, period):
    ATR_val = []
    TrueRanges = 0.0
    ATR_val.append(0.0)
    for i in range(1, period):
        TrueRanges = TrueRanges + TR(high[len(high)-i],low[len(low)-i],close[len(close)-i-1])
        ATR_val.append(TrueRanges/period)
    ATR_Data = TrueRanges/period    
    for i in range(period, len(close)):
        ATR_Data = (ATR_Data*(period-1) + TR(high[len(high)-i],low[len(low)-i],close[len(close)-i-1]))/period
        ATR_val.append(ATR_Data)
    return np.array(ATR_val)

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

def pMa(data, window_size):
    return pd.rolling_mean(data, window_size, min_periods=1)

def pStd(data, window_size):
    return pd.rolling_std(data, window_size, min_periods=1)

def pCorr(data1, data2, window_size):
    return pd.rolling_corr(data1, data2, window_size, min_periods=1)

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

def Fibonacci(SwingHigh, SwingLow):
    FibLevels = []
    FibLevels.append(SwingHigh)
    FibLevels.append(SwingLow)
    FibLevels.append(SwingHigh - 0.618*(SwingHigh-SwingLow))
    FibLevels.append(SwingHigh - 0.5*(SwingHigh-SwingLow))
    FibLevels.append(SwingHigh - 0.382*(SwingHigh-SwingLow))
    FibLevels.append(SwingHigh - 0.236*(SwingHigh-SwingLow))
    FibLevels.append(SwingHigh + 0.618*(SwingHigh-SwingLow))
    FibLevels.append(SwingHigh - 1.618*(SwingHigh-SwingLow))
    return FibLevels

def PriceChange(close):
    PriceChange_Data = []
    PriceChange_Data.append(0)
    for i in range(0, len(close)):
        PriceChange_Data.append(close[i] - close[i-1])
    return PriceChange_Data   

def HighestHigh(h,period):
    HHData = np.zeros((1,len(h)))
    for i in range(period + 1,len(h)):
        hh = h[i]
        for j in range(0,period):
            hh = max(hh,h[i - period + j])
            if i < period +1:
                HHData[0, i] = h[i]
            else:
                HHData[0, i] = hh
    return HHData

def LowestLow(l,period):
    LLData = np.zeros((1,len(l)))
    for i in range(period + 1,len(l)):
        ll = l[i]
        for j in range(0,period):
            ll = min(ll,l[i - period + j])
            if i < period +1:
                LLData[0, i] = l[i]
                # print l[i]
            else:
                LLData[0, i] = ll
                # print ll
    return LLData

def ROC(close,period):
    ROC_Data = np.zeros((1,len(close)))
    for i in range(period +1, len(close)):
        ROC_Data[0,i] = (close[i]-close[i-period])/close[i-period]
    return ROC_Data

def Stochastic(high, low, close, kperiod, dperiod, t):
    loww = LowestLow(low,kperiod)
    highh = HighestHigh(high,kperiod)
    Stoch_K = np.zeros((1,len(close)))
    # print highh[0,:], loww[0,:]
    for i in range(0, len(close)):
        Stoch_K[0, i] = float((close[i]-max(loww[0,i],low[i])))/((max(highh[0,i],high[i])-max(loww[0,i],low[i]) + 0.000000001))
    Stoch_D = pMa(Stoch_K[0,:],dperiod)
    if t == "K":
        return Stoch_K[0, :]
    elif t == "D":
        return Stoch_D

def TypicalPrice(high, low, close):
    TP_Data = (high + low + close)/3
    return TP_Data

def CCI(high, low, close, period, constant):
    Typ = TypicalPrice(high, low, close)
    TypMA = pMa(Typ,period)

    TypSD = pStd(Typ,period)
    CCI_Data = np.zeros((1,len(close)))
    for i in range(0, len(close)):
        CCI_Data[0,i] = (Typ[i] - TypMA[i])/(constant*TypSD[i])
    return CCI_Data[0,:]

def SimpleRegression(x_array, y_array):
    SR_Data = []
    n = x_array.size
    XY = x_array*y_array
    XX = x_array*x_array
    EX = sum(x_array)
    EY = sum(y_array)
    EXY = sum(XY)
    EXX = sum(XX)
    b = (n*EXY-EX*EY)/(n*EXX - EX**2)
    a = (EY - b*EX)/n
    SR_Data.append(b)
    SR_Data.append(a)
    return SR_Data

# def RSI(close, period):
#     RSI_Data = []
#     Chng = PriceChange(close)
#     Average_Gain = np.zeros((0,len(close)))
#     Average_Loss = np.zeros((0,len(close)))
#     for i in range(0,period):
#         if Chng[i] > 0:
#             frstGaintemp = frstGain + Chng[i]
#         elif Chng[i] < 0:
#             frstLosstemp = frstLoss + Chng[i]
#     frstGaintemp = 0.0
#     frstLosstemp = 0.0
#     frstGain = 0.0
#     frstLoss = 0.0
#     frstGain = frstGaintemp/period
#     frstLoss = frstLosstemp/period
#     for i in range(period + 1 , len(close)):
#         Average_Gain[i]
#         Average_Loss[i]
#     return RSI_Data

# def ADX(close,high,low, period):
#     # ATR_val = []
#     # TrueRanges = 0.0
#     # for i in range(1, period):
#     #     TrueRanges = TrueRanges + TR(high[len(close)-i],low[len(close)-i],close[len(close)-i-1])
#     #     ATR_val.append(TrueRanges/period)
#     # ATR_Data = TrueRanges/period    
#     # for i in range(period, len(close)):
#     #     ATR_Data = (ATR_Data*(period-1) + TR(high[len(close)-i],low[len(close)-i],close[len(close)-i-1]))/period
#     #     ATR_val.append(ATR_Data)
#     # return ATR_val

