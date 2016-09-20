import requests
import json
from array import *
from Settings import PRICE_DOMAIN, ACCOUNT_DOMAIN, ACCESS_TOKEN, ACCOUNT_ID, STRT, STRO, STRH, STRL, STRC, STRV, STRCO
import httplib
import urllib
from datetime import datetime, timedelta
import time
import matplotlib.pyplot as plt
import numpy as np
import pypyodbc

Sec = []
Sec.append("EUR_USD")
Sec.append("GBP_USD")
Sec.append("USD_CAD")
Sec.append("AUD_USD")
Sec.append("NZD_USD")
Sec.append("USD_CHF")
Sec.append("EUR_CAD")
Sec.append("AUD_CAD")
Sec.append("NZD_CAD")
Sec_Status = []
Sec_Status.append(False)
Sec_Status.append(False)
Sec_Status.append(False)
Sec_Status.append(False)
Sec_Status.append(False)


print "Initializing..."
Account_Sum = []
Ret_Data = []
for k in range(0,9):
    Trade_Counter = 0
    Bars = 5000
    h = {'Authorization' : ACCESS_TOKEN}
    print "Retrieving Data..." # "&count=" + str(Bars) + "
    r = requests.get( ACCOUNT_DOMAIN + "instrument=" + Sec[k] + "&candleFormat=midpoint&granularity=M5&start=2015-02-01&end=2015-02-25", headers=h)     
    data = json.loads(r.text)

    def Date(index):
        return data["candles"][index][STRT]
    def Open(index):
        return data["candles"][index][STRO]
    def High(index):
        return data["candles"][index][STRH]
    def Low(index):
        return data["candles"][index][STRL]
    def Close(index):
        return data["candles"][index][STRC]
    print "Data Received..."
    Account_Chart = []
    Open_Order = 0.0
    Carry_Price = 0.0
    Lots = 10000
    n = 30
    I_D = 1
    Account = 1000
    Starting_Balance = Account
    last_entry = 0 
    spacer = 5
    last_trade = 0
    Open_Units =0
    Open_Trade = False
    Angle_SMA = 0.0
    for i in range(201,4600):
        if Open_Order == 0:
            Carry_Price = Close(i-1)

        aavg = 0.0
        for j in range(0,50):
            aavg = Close(i-j) + aavg
        SMA50 = aavg/50

        aavg = 0.0
        for j in range(0,50):
            aavg = Close(i-10-j) + aavg
        FIRSTSMA50 = aavg/50

        aavg = 0.0
        for j in range(0,21):
            aavg = Close(i-j) + aavg
        SMA21 = aavg/21

        aavg = 0.0
        for j in range(0,10):
            aavg = Close(i-j) + aavg
        SMA10 = aavg/10

        if Close(i) < SMA10 and Close(i) > SMA21 and Close(i) > SMA50 and Open_Order == 0 and SMA50/FIRSTSMA50-1 > 0.000005 and i - last_entry > 5:
            Trade_Counter += 1 
            Open_Order = 1
            Open_Price = Close(i)
            Stop_Loss = (SMA21 + SMA50)/2
            Take_Profit = 2*Close(i) - SMA50
            Carry_Price = Close(i)
            last_entry = i
        elif Close(i) > SMA10 and Close(i) < SMA21 and Close(i) < SMA50 and Open_Order == 0 and SMA50/FIRSTSMA50-1 < -0.000005 and i - last_entry > 5:
            Trade_Counter += 1 
            Open_Order = -1
            Open_Price = Close(i)
            Stop_Loss = (SMA21 + SMA50)/2
            Take_Profit = 2*Close(i)-SMA50
            Carry_Price = Close(i)
            last_entry = i

        if Open_Order == 1:
            if High(i) > Take_Profit:
                Account = Starting_Balance + (Take_Profit-Open_Price)* Lots
                Open_Order = 0
                Starting_Balance = Account
            if Low(i) < Stop_Loss:
                Account = Starting_Balance -  (Open_Price-Stop_Loss)* Lots
                Open_Order = 0 
                Starting_Balance = Account
            if High(i) < Take_Profit and Low(i) > Stop_Loss:
                Account = Starting_Balance + (Carry_Price - Open_Price) * Lots

        if Open_Order == -1:
            if High(i) > Stop_Loss:
                Account = Starting_Balance - (Stop_Loss-Open_Price) * Lots
                Open_Order = 0 
                Starting_Balance = Account
            if Low(i) < Take_Profit:
                Account = Starting_Balance + (Open_Price-Take_Profit) * Lots
                Open_Order = 0 
                Starting_Balance = Account
            if Low(i) > Take_Profit and High(i) < Stop_Loss:
                Account = Starting_Balance + (Open_Price - Carry_Price) * Lots
        
        Account_Chart.append(Account)
    plt.plot(Account_Chart)
    print Trade_Counter

    # Ret_Data = []
    # TP_Data = []
    # SL_Data = []
    # if Close(i) > SMA10 and Close(i) < SMA21 and Close(i) < SMA50 and i - last_entry > 50:
    #     Stop_Loss = SMA50
    #     Take_Profit = 2*Close(i)-SMA50
    #     print Take_Profit
    #     print Stop_Loss 
    #     for j in range(0,50):
    #         if High(i+j) < Stop_Loss and Low(i+j) > Take_Profit:
    #             ret = Close(i+j)/Close(i)- 1
    #             Ret_Data.append(ret)
    #             SL_Data.append(Stop_Loss/Close(i)-1)
    #             TP_Data.append(Take_Profit/Close(i)-1)
    #     last_entry = i
    #     plt.plot(Ret_Data)
    #     # plt.plot(TP_Data)
    #     plt.plot(SL_Data)
    # elif Close(i) > SMA10 and Close(i) < SMA21 and Close(i) < SMA50 and Open_Order == 0 and i - last_entry > 5:
    #     for j in range(0,50):
    #         ret = Close(i+j)/Close(i)- 1
    #         Ret_Data.append(ret)
    #     plt.plot(Ret_Data)
    #     last_i = i

# plt.ylim(-0.005,0.005)
plt.ylim(500,2000)
plt.show()