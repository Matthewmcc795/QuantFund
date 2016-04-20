import requests
import json
from array import *
from Settings import PRICE_DOMAIN, ACCOUNT_DOMAIN, LIVE_ACCESS_TOKEN, ACCOUNT_ID, STRT, STRO, STRH, STRL, STRC, STRV, STRCO
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

Sec.append("EUR_GBP")
Sec.append("EUR_CAD")
Sec.append("EUR_AUD")
Sec.append("EUR_NZD")

Sec.append("GBP_AUD")
Sec.append("GBP_NZD")
Sec.append("GBP_CAD")

Sec.append("AUD_CAD")
Sec.append("AUD_NZD")

Sec.append("NZD_CAD")

Portfolio_Cash = 0.0
Portfolio_Holdings = 0.0
Buy_Signals = []
Sell_Signals = []
CloseBuy_Signals = []
CloseSell_Signals = []

st = "2015-01-01"
end_dt = "2016-02-01"
Ticker = "EUR_USD"
tf1 = "D"
tf2 = "M5"
tf3 = "M15"
# mc = pClose(Ticker, tf2, st,  en)
Portfolio = np.zeros((1,5000))
en = FindDateRange(st, 2)
Account = 100
while np.busday_count(en, end_dt) > 20:

    # for p in range(0,15):
    PP = 0.0
    R1 = [0,0,0,0,0]
    # R2 = [0,0,0,0,0]
    S1 = [0,0,0,0,0]
    # S2 = [0,0,0,0,0]

    Ticker = Sec[5]
    o = pOpen(Ticker, tf1, st, en)
    h = pHigh(Ticker, tf1, st, en)
    l = pLow(Ticker, tf1, st, en)
    c = pClose(Ticker, tf1, st,  en)
    d = pDate(Ticker, tf1, st, en)

    # m15h = pHigh(Ticker, tf3, st,  en)
    # m15l = pLow(Ticker, tf3, st,  en)
    # m15c = pClose(Ticker, tf3, st,  en)
    # m15d = pDate(Ticker, tf3,st,en)

    # mh = pHigh(Ticker, tf2, st,  en)
    # ml = pLow(Ticker, tf2, st,  en)
    # mc = pClose(Ticker, tf2, st,  en)
    # md = pDate(Ticker, tf2,st,en)

    # m5MA = pMa(mc,150)
    # m15MA = pMa(m15c,150)
    # m15SD = pStd(m15c,20)

    # m5UB = []
    # m5LB = []

    # m5R2 = []
    # m5R1 = []
    # m5PP = []
    # m5S1 = []
    # m5S2 = []
    # m5ATR = []
    # ub = 0.0
    # lb = 0.0
    # j = 0
    # k = 0
    # atr = 0.0
    # atr = pATR(m15c,m15h,m15l,14)
    # for i in range(0,len(mc)):
    #     if j +1 <= len(d) -1:
    #         if md[i] == d[j + 1]:
    #             j = j + 1
    #     PP = (h[j] + l[j] + c[j])/3
    #     m5R1.append(float(2*PP - l[j]))
    #     m5PP.append(float(PP))
    #     m5S1.append(float(2*PP - h[j]))

    #     if k +1 <= len(m15d) -1:
    #         if md[i] == m15d[k + 1]:
    #             k = k + 1
        
    #     # ub = m15MA[k] + 1*m15SD[k]
    #     # lb = m15MA[k] - 1*m15SD[k]
    #     m5ATR.append(atr[k])
    #     # m5MA.append(ub)
        # m5LB.append(lb)

    # plt.plot(mc)
    # plt.plot(m5UB)
    # plt.plot(m5LB)

    # plt.plot(m5R2)
    # plt.plot(m5R1)
    # plt.plot(m5PP)
    # plt.plot(m5S1)
    # plt.plot(m5S2)

    # plt.ylim(min(mc)/1.001,max(mc)*1.001)
    # plt.show()

    # plt.plot(m5ATR)
    # plt.ylim(0,0.0025)
    # plt.show()

    # Account = 119.56
    # 100 --> 100.55 --> 102.53 --> 103.91 --> 103.08 --> 104.06 --> 105.63 --> 106.07 --> 107.24 --> 108.62 --> 110.26
    # 110.15 --> 110.49 --> 113.39 --> 115.18 --> 116.06 --> 116.30 --> 117.06 --> 117.86 --> 119.56 --> 119.67 
    Starting_Balance = Account
    last_entry = 0 
    spacer = 5
    last_trade = 0
    Open_Units =0
    Open_Trade = False
    Open_Order = 0
    Lots = 500
    Account_Chart = []
    UpperPP = 0
    LowerPP = 0
    i = 0
    j = 0
    k = 0
    cnt_buy_trades = 0 
    cnt_sell_trades = 0
    cnt_wbuy_trades = 0
    cnt_wsell_trades = 0
    cnt_lbuy_trades = 0
    cnt_lsell_trades = 0

    # js_close = 0
    # pr = []
    # St = [] 
    # uppbnd = []
    # lwrbnd = []
    # mid = []

    for i in range(0,len(mc)):

        # x = md[i]
        # x1 = str(x)
        # y2 = x1[11:]
        # z2 = y2[:len(y2)-14]
        # if float(z2) >= 11 and float(z2) <= 18 :
            # if mc[i-1] > m5R1[i-1]:
            #     UpperPP = mc[i-1]*2
            #     LowerPP = m5PP[i-1]
            # elif mc[i-1] > m5PP[i-1] and mc[i-1] < m5R1[i-1]:
            #     UpperPP = m5R1[i-1]
            #     LowerPP = m5PP[i-1]
            # elif mc[i-1] > m5S1[i-1] and mc[i-1] < m5PP[i-1]:
            #     UpperPP = m5PP[i-1]
            #     LowerPP = m5S1[i-1]
            # elif mc[i-1] < m5S1[i-1]:  
            #     UpperPP = m5S1[i-1]
            #     LowerPP = mc[i-1]/2

            if mc[i] > m5S1[i] and mc[i-1] < m5S1[i] and i - last_entry > spacer:
                Buy_Signals.append(1)
                cnt_buy_trades += 1
                Open_Order = 1
                Open_Price = mc[i]
                Stop_Loss = mc[i] - m5ATR[i]
                Take_Profit = mc[i] + 2*m5ATR[i]
                Carry_Price = mc[i]
                last_entry = i
            elif mc[i] < m5R1[i] and mc[i-1] > m5R1[i] and i - last_entry > spacer:
                Sell_Signals.append(1)
                cnt_sell_trades += 1
                Open_Order = -1
                Open_Price = mc[i]
                Stop_Loss = mc[i] + m5ATR[i]
                Take_Profit = mc[i] - 2*m5ATR[i]
                Carry_Price = mc[i]
                last_entry = i
            else:
                Buy_Signals.append(0)
                Sell_Signals.append(0)
        
        if Open_Order == 1:
            if mc[i] > m5ATR[i]/2 + Open_Price:
                Stop_Loss = Open_Price +0.0002
            elif mc[i] > m5ATR[i] + Open_Price:
                Stop_Loss = max(Stop_Loss, Open_Price +0.0002, m5UB[i]-0.0002)

            if mh[i] > Take_Profit:
                cnt_wbuy_trades += 1
                Account = Starting_Balance + (Take_Profit-Open_Price) * Lots
                # print "Buy Win"
                # print Take_Profit-Open_Price
                Open_Order = 0
                # if Starting_Balance > Account:
                #     cnt_lbuy_trades += 1
                # else:
                #     cnt_wbuy_trades += 1
                Starting_Balance = Account
            if ml[i] < Stop_Loss:
                cnt_lbuy_trades += 1
                Account = Starting_Balance + (Stop_Loss-Open_Price) * Lots
                # print "Buy Loss"
                # print Stop_Loss-Open_Price
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
            if mc[i] < Open_Price - m5ATR[i]/2:
                Stop_Loss = Open_Price +0.0002
            elif mc[i] < Open_Price - m5ATR[i]:
                Stop_Loss = min(Stop_Loss, Open_Price +0.0002, m5LB[i]+0.0002)

            if mh[i] > Stop_Loss:
                Account = Starting_Balance - (Stop_Loss-Open_Price) * Lots
                # print "Sell Loss"
                # print Stop_Loss-Open_Price
                Open_Order = 0 
                # if Starting_Balance > Account:
                #     cnt_lsell_trades += 1
                # else:
                #     cnt_wsell_trades += 1
                Starting_Balance = Account
                js_close = 1
            if ml[i] < Take_Profit:
                Account = Starting_Balance - (Take_Profit-Open_Price) * Lots
                # print "Sell Win"
                # print Open_Price-Take_Profit
                Open_Order = 0
                # if Starting_Balance > Account:
                #     cnt_lsell_trades += 1
                # else:
                #     cnt_wsell_trades += 1
                Starting_Balance = Account
            if mh[i] < Stop_Loss and ml[i] > Take_Profit:
                Account = Starting_Balance + (Open_Price - Carry_Price) * Lots
        
        Portfolio[0,i] = Account
        # # i -= 1
        # # plt.plot(Buy_Signals)
        # # plt.plot(Sell_Signals)

        # # Positions adjuststed for lotsize
    #     plt.plot(Account_Chart)
    #     Ending_Account_Chart = Ending_Account_Chart + Account_Chart
    # plt.plot(Ending_Account_Chart)
    # Avg_Portfolio = Portfolio.mean(axis=0)[-1]

    Account =  Portfolio[0,len(mc)-10]
    st = en
    en = FindDateRange(en, 24*12)
    print Account

# plt.ylim(115,125)
# plt.show()

# for i in range(0,15):
#     plt.plot(Portfolio[i,:], label=str(Sec[i]))
#     plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
# # print cnt_wbuy_trades
# # print cnt_wsell_trades
# # print cnt_lsell_trades
# # print cnt_lbuy_trades
# # Total_Trades = cnt_sell_trades + cnt_buy_trades 
# # Total_Win = cnt_wbuy_trades + cnt_wsell_trades
# # print (Total_Win/Total_Trades)
# # Acc = (cnt_wbuy_trades + cnt_wsell_trades)/(cnt_sell_trades + cnt_buy_trades)
# # print Total_Trades
# # print Total_Win

# # print Acc
# # print "Stats"
# # print "Total Trades: " + str(cnt_sell_trades + cnt_buy_trades)
# # print "Accuracy: " + str(Acc)
# # print "Total Buy Trades: " + str(cnt_buy_trades)
# # print "Buy Accuracy: " + str((cnt_wbuy_trades)/(cnt_buy_trades))
# # print "Total Sell Trades: " + str(cnt_sell_trades)
# # print "Sell Accuracy: " + str((cnt_wsell_trades)/(cnt_sell_trades))
# plt.ylim(100,110)
# plt.show()