import requests
import json
from array import *
from Settings import PRICE_DOMAIN, ACCOUNT_DOMAIN, DEMO_ACCESS_TOKEN, ACCOUNT_ID, STRT, STRO, STRH, STRL, STRC, STRV, STRCO
import httplib
import urllib
from datetime import datetime, timedelta
import time
import sys
import numpy as np
import pypyodbc
import matplotlib.pyplot as plt
from Backtest_Objects import *
import pandas as pd
from matplotlib.finance import candlestick2_ochl

Sec = []
Sec.append("EUR_USD")
Sec.append("GBP_USD")
Sec.append("USD_CAD")
Sec.append("AUD_USD")
Sec.append("NZD_USD")

Bars = 51
SL = -0.0016
TP = 0.0008
n = 50
name = "Log file.txt"

DDay = []
DHigh = []
DLow = []
DClose = []

st = "2016-01-25"
en = "2016-01-30"
Ticker = "EUR_USD"
tf1 = "D"
tf2 = "M5"
tf3 = "M15"

o = pOpen(Ticker, tf1, st, en)
h = pHigh(Ticker, tf1, st, en)
l = pLow(Ticker, tf1, st, en)
c = pClose(Ticker, tf2, st,  en)
d = pDate(Ticker, tf1, st, en)
m15h = pHigh(Ticker, tf3, st,  en)
m15l = pLow(Ticker, tf3, st,  en)
m15c = pClose(Ticker, tf3, st,  en)
m15d = pDate(Ticker, tf3,st,en)
mh = pHigh(Ticker, tf2, st,  en)
ml = pLow(Ticker, tf2, st,  en)
mc = pClose(Ticker, tf2, st,  en)
md = pDate(Ticker, tf2,st,en)
# print d[0]
# print d[1]
# print md
fast_ma = pMa(mc,20)
slow_ma = pMa(mc,50)
# plt.plot(c)
# plt.plot(fast_ma)
# plt.plot(slow_ma)
# fig, ax1 = plt.subplots(1, 1, sharex=True)
# ax1.set_ylabel("EUR_USD", size=20)
# Plot candles
# candlestick2_ochl(ax1, o, h, l, c, width=1, colorup='k', colordown='r', alpha=1)
# plt.ylim(min(c)*0.99,max(c)*1.01)
# plt.show()

# SkhettiStats(c,fast_ma,c,True,12,True)
# SkhettiStats(c,slow_ma,c,True,12,True)

Account = 1000
Starting_Balance = Account
last_entry = 0 
spacer = 3
last_trade = 0
Open_Units =0
Open_Trade = False
Open_Order = 0
Lots = 10000
Account_Chart = []
UpperPP = 0
LowerPP = 0
i = 0
j = 0
k = 0
# while i >= 0:
cnt_buy_trades = 0 
cnt_sell_trades = 0
cnt_wbuy_trades = 0
cnt_wsell_trades = 0
cnt_lbuy_trades = 0
cnt_lsell_trades = 0
PivP = pPivotPoints(h[j],l[j],c[j],mc[i-2])
AvgTR = pATR(m15c,m15h,m15l,14,k)
# js_close = 0
# pr = []
# St = [] 
# Portfolio_Cash = 0.0
# Portfolio_Holdings = 0.0

# Buy_Signals = []
# Sell_Signals = []
# CloseBuy_Signals = []
# CloseSell_Signals = []
# uppbnd = []
# lwrbnd = []
# mid = []

lwr = 0.0
upr = 0.0
m30_Ret = 0.0
for i in range(14,len(mc)-2):
    sumret = 0.0
    avgret = 0.0
    sumdevret = 0.0
    sdret = 0.0
    # js_close = 0
    if Open_Order == 0:
        Carry_Price = mc[i]
    if j +1 <= len(d) -1:
        if md[i] == d[j + 1]:
            j = j + 1
            PivP = pPivotPoints(h[j],l[j],c[j],mc[i-2]) 
    else:
        break
    if k +1 <= len(m15d) -1:
        if md[i] == m15d[k + 1]:
            k = k + 1
            AvgTR = pATR(m15c,m15h,m15l,14,k)
    else:
        break

    for p in range(0,11):
        sumret = sumret + mc[i-p]/mc[i-11] - 1
    avgret = sumret/12
    # print avgret*100

    for p in range(0,11):
        sumdevret = (avgret - (mc[i-p]/mc[i-11] - 1))**2 
    sdret = (sumdevret/9)**0.5
    # print sdret*100
    # print "new candle"
    # uppbnd.append((avgret + 4*sdret)*100)
    # mid.append((mc[i]/mc[i-6] - 1)*100)
    # lwrbnd.append((avgret - 4*sdret)*100)
    
    m30_Ret = (mc[i]/mc[i-2] - 1)*100
    lwr = (avgret - 2*sdret)*100
    upr = (avgret + 2*sdret)*100

    if mc[i-1] > PivP[0] and mc[i-2] < PivP[0] and i - last_entry > spacer:
        # print i
        # Buy_Signals.append(1)
        cnt_buy_trades += 1
        Open_Order = 1
        Open_Price = mc[i]
        Stop_Loss = mc[i] - AvgTR/2
        Take_Profit = mc[i] + AvgTR
        Carry_Price = mc[i]
        last_entry = i
    elif mc[i-1] < PivP[1] and mc[i-2] > PivP[1] and i - last_entry > spacer:
        # print i
        # Sell_Signals.append(1)
        cnt_sell_trades += 1
        Open_Order = -1
        Open_Price = mc[i]
        Stop_Loss = mc[i] + AvgTR/2
        Take_Profit = mc[i] - AvgTR
        Carry_Price = mc[i]
        last_entry = i
    # else:
    #     Buy_Signals.append(0)
    #     Sell_Signals.append(0)
    elif Open_Order == 1:
        # Stop_Loss = max(Stop_Loss,mc[i]-AvgTR)
        if mh[i] > Take_Profit:
            cnt_wbuy_trades += 1
            Account = Starting_Balance + (Open_Price-Take_Profit) * Lots
            Open_Order = 0
            # if Starting_Balance > Account:
            #     cnt_lbuy_trades += 1
            # else:
            #     cnt_wbuy_trades += 1
            Starting_Balance = Account
        if ml[i] < Stop_Loss:
            cnt_lbuy_trades += 1
            Account = Starting_Balance + (Open_Price-Stop_Loss) * Lots
            Open_Order = 0 
            # if Starting_Balance > Account:
            #     cnt_lbuy_trades += 1
            # else:
            #     cnt_wbuy_trades += 1
            # Starting_Balance = Account
            js_close = 1
        if ml[i] > Stop_Loss and mh[i] < Take_Profit:
            Account = Starting_Balance + (Carry_Price - Open_Price) * Lots
    elif Open_Order == -1:
        # Stop_Loss = min(Stop_Loss,mc[i]+AvgTR)
        if mh[i] > Stop_Loss:
            Account = Starting_Balance + (Open_Price-Stop_Loss) * Lots
            Open_Order = 0 
            # if Starting_Balance > Account:
            #     cnt_lsell_trades += 1
            # else:
            #     cnt_wsell_trades += 1
            Starting_Balance = Account
            js_close = 1
        if ml[i] < Take_Profit:
            Account = Starting_Balance + (Open_Price-Take_Profit) * Lots
            Open_Order = 0
            # if Starting_Balance > Account:
            #     cnt_lsell_trades += 1
            # else:
            #     cnt_wsell_trades += 1
            Starting_Balance = Account
        if mh[i] < Stop_Loss and ml[i] > Take_Profit:
            Account = Starting_Balance + (Open_Price - Carry_Price) * Lots
    # if Open_Order != 0:
    #     pr.append(mc[i])
    #     St.append(Stop_Loss)
    # elif js_close == 1:
    #     pr.append(mc[i])
    #     St.append(Stop_Loss)
    #     plt.plot(pr)
    #     plt.plot(St)
    #     plt.ylim(min(pr)*0.995,max(pr)*1.005)
    #     plt.show()
    #     js_close = 0
    #     pr = []
    #     St = []

    Account_Chart.append(Account)
# i -= 1
# plt.plot(Buy_Signals)
# plt.plot(Sell_Signals)

# Positions adjuststed for lotsize
plt.plot(Account_Chart)
# plt.plot(uppbnd)
# plt.plot(lwrbnd)
# plt.plot(mid)

# print cnt_wbuy_trades
# print cnt_wsell_trades
# print cnt_lsell_trades
# print cnt_lbuy_trades
# Total_Trades = cnt_sell_trades + cnt_buy_trades 
# Total_Win = cnt_wbuy_trades + cnt_wsell_trades
# print (Total_Win/Total_Trades)
# Acc = (cnt_wbuy_trades + cnt_wsell_trades)/(cnt_sell_trades + cnt_buy_trades)
# print Total_Trades
# print Total_Win

# print Acc
# print "Stats"
# print "Total Trades: " + str(cnt_sell_trades + cnt_buy_trades)
# print "Accuracy: " + str(Acc)
# print "Total Buy Trades: " + str(cnt_buy_trades)
# print "Buy Accuracy: " + str((cnt_wbuy_trades)/(cnt_buy_trades))
# print "Total Sell Trades: " + str(cnt_sell_trades)
# print "Sell Accuracy: " + str((cnt_wsell_trades)/(cnt_sell_trades))
plt.ylim(500,1500)
# plt.ylim(-0.5,0.5)
plt.show()