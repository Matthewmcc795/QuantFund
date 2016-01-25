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
# Cycle through Daily, H4, M5 etc. 

Sec = []
Sec.append("EUR_USD")
Sec.append("GBP_USD")
Sec.append("USD_CAD")
Sec.append("AUD_USD")
Sec.append("NZD_USD")
Sec_Status = []
Sec_Status.append(False)
Sec_Status.append(False)
Sec_Status.append(False)
Sec_Status.append(False)
Sec_Status.append(False)


print "Initializing..."
Open_Order = 0.0
Carry_Price = 0.0
Lots = 1000
n = 30
Bars = 5000
I_D = 1

h = {'Authorization' : ACCESS_TOKEN}
print "Retrieving Data..."
r = requests.get( ACCOUNT_DOMAIN + "instrument=EUR_USD&count=4000&candleFormat=midpoint&granularity=H4", headers=h)     
data = json.loads(r.text)
# print data
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

def Inside_Bar(h,l,hp,lp):
    if hp > h and lp < l:
        return True
    else:
        return False

Account = 1000
Starting_Balance = Account
last_entry = 0 
spacer = 5
SL = -0.01
TP = 0.010
last_trade = 0
Open_Units =0
Open_Trade = False
for i in range(201,3900):
    if Open_Order == 0:
        Carry_Price = Close(i-1)
    aavg = 0.0
    SMA = 0.0
    ssd = 0.0
    sd = 0.0
    tail = 0.0
    wick = 0.0
    Sum_Can = 0.0

    # for j in range(0,n):
    #     Sum_Can = Sum_Can + Close(i-j+1) - Close(i-j)

    # if Inside_Bar(High(i-1),Low(i-1),High(i-2),Low(i-2)) == True and Close(i) > High(i-1):
    #     print "buy"
    # elif Inside_Bar(High(i-1),Low(i-1),High(i-2),Low(i-2)) == True and Close(i) < Low(i-1):
    #     print "sell"


    # print Sum_Can
    # a = np.array(Can_High)
    # Highs = max(a)
    # a = np.array(Can_Low)
    # Lows = min(a)
    # # for j in range(0,n):
    #     aavg = Close(i-j) + aavg
    # SMA = aavg/n
    
    # for j in range(0,n):
    #     ssd = (Close(i-j) - SMA)**2 +ssd
    # sd = (ssd/(n-1))**(0.5)
    # Upper_Band = SMA + 2*sd
    # Lower_Band = SMA - 2*sd
    
    # if Close(i-1) > Open(i-1):
    #     wick = High(i-1) - Close(i-1)
    #     tail = Open(i-1) - Low(i-1)
    # else:
    #     wick = High(i-1) - Open(i-1)
    #     tail = Close(i-1) - Low(i-1)

    # if Close(i-2) > Open(i-2):
    #     wick2 = High(i-2) - Close(i-2)
    #     tail2 = Open(i-2) - Low(i-2)
    # else:
    #     wick2 = High(i-2) - Open(i-2)
    #     tail2 = Close(i-2) - Low(i-2)

    # wik = (wick2 + wick)/2
    # # tal = (tail2 + tail)/2
    # print Close(i) - Highs
    # print Close(i) - Lows
    if Inside_Bar(High(i-1),Low(i-1),High(i-2),Low(i-2)) == True and Close(i) > High(i-1):
        Open_Order = 1
        Open_Price = Close(i-1)
        Stop_Loss = Open(i) + SL
        Take_Profit = Open(i) + TP
        Carry_Price = Close(i-1)
        last_entry = i
        peak = Close(i)
    elif Inside_Bar(High(i-1),Low(i-1),High(i-2),Low(i-2)) == True and Close(i) < Low(i-1):
        Open_Order = -1
        Open_Price = Close(i-1)
        Stop_Loss = Open(i) - SL
        Take_Profit = Open(i) - TP
        Carry_Price = Close(i-1)
        last_entry = i
        trough = Close(i)

    # if Open_Order == 1:
    #     if Close(i) - Open_Price > 0.001 and Close(i) > peak:
    #         peak = Close(i)
    #         if Close(i) - Open_Price < (Peak-Open_Price)*0.85:
    #             Account = Starting_Balance + (Close(i)-Open_Price)* Lots
    #             Open_Order = 0
    #             Starting_Balance = Account
    #     elif High(i-1) < Take_Profit and Low(i-1) > Stop_Loss:
    #         Account = Starting_Balance + (Carry_Price - Open_Price) * Lots

    # if Open_Order == -1:
    #     if Open_Price - Close(i) > 0.001 and Close(i) < trough:
    #         trough = Close(i)
    #         if Open_Price - Close(i) < (Open_Price-trough)*0.85:
    #             Account = Starting_Balance + (Close(i)-Open_Price)* Lots
    #             Open_Order = 0
    #             Starting_Balance = Account
    #     elif High(i-1) < Take_Profit and Low(i-1) > Stop_Loss:
    #         Account = Starting_Balance + (Carry_Price - Open_Price) * Lots

    if Open_Order == 1:
        if High(i-1) > Take_Profit:
            Account = Starting_Balance + TP * Lots
            Open_Order = 0
            Starting_Balance = Account
        if Low(i-1) < Stop_Loss:
            Account = Starting_Balance + SL * Lots
            Open_Order = 0 
            Starting_Balance = Account
        if High(i-1) < Take_Profit and Low(i-1) > Stop_Loss:
            Account = Starting_Balance + (Carry_Price - Open_Price) * Lots

    if Open_Order == -1:
        if High(i-1) > Stop_Loss:
            Account = Starting_Balance + SL * Lots
            Open_Order = 0 
            Starting_Balance = Account
        if Low(i-1) < Take_Profit:
            Account = Starting_Balance + TP * Lots
            Open_Order = 0 
            Starting_Balance = Account
        if Low(i-1) > Take_Profit and High(i-1) < Stop_Loss:
            Account = Starting_Balance + (Open_Price - Carry_Price) * Lots
    
    Account_Chart.append(Account)

plt.plot(Account_Chart)
plt.ylim(500,2750)
plt.show()