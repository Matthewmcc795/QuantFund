import requests
import json
from array import *
from Settings import PRICE_DOMAIN, ACCOUNT_DOMAIN, ACCESS_TOKEN, ACCOUNT_ID, STRT, STRO, STRH, STRL, STRC, STRV, STRCO
import httplib
import urllib
from datetime import datetime, timedelta
import time
import sys
import numpy as np
import pypyodbc
import matplotlib.pyplot as plt

Sec = []
Sec.append("EUR_USD")
Sec.append("GBP_USD")
Sec.append("AUD_USD")

Bars = 51
SL = 0.0006
TP = 0.0004
n = 50
name = "Log file.txt"

DDay = []
DHigh = []
DLow = []
DClose = []

file_Name = "C:\Users\macky\OneDrive\Documents\Price_Database.mdb"

conn = pypyodbc.win_connect_mdb(file_Name)  
cur = conn.cursor()
#cur.execute(u"""CREATE TABLE Skhetti_Stats (ID INTEGER PRIMARY KEY, Day String, Test String, Ret Double)""")
cur.execute("SELECT [Day] FROM D_Price WHERE [Ticker] = 'EUR_USD' ;")

Data_DDay = cur.fetchall()
DDay_Count = len(Data_DDay)
for x in Data_DDay:
    x1 = str(x)
    y2 = x1[3:]
    z2 = y2[:len(y2)-3]
    DDay.append(z2)

cur.execute("SELECT [High] FROM D_Price WHERE [Ticker] = 'EUR_USD' ;")

Data_DHigh = cur.fetchall()
for x in Data_DHigh:
    x1 = str(x)
    y2 = x1[1:]
    z2 = y2[:len(y2)-2]
    DHigh.append(float(z2))

cur.execute("SELECT [Low] FROM D_Price WHERE [Ticker] = 'EUR_USD' ;")

Data_DLow = cur.fetchall()
for x in Data_DLow:
    x1 = str(x)
    y2 = x1[1:]
    z2 = y2[:len(y2)-2]
    DLow.append(float(z2))

cur.execute("SELECT [Close] FROM D_Price WHERE [Ticker] = 'EUR_USD' ;")

Data_DClose = cur.fetchall()
for x in Data_DClose:
    x1 = str(x)
    y2 = x1[1:]
    z2 = y2[:len(y2)-2]
    DClose.append(float(z2))

cur.close()
conn.commit()
conn.close()

h = {'Authorization' : ACCESS_TOKEN}
url =   "https://api-fxpractice.oanda.com/v1/candles?instrument=EUR_USD&count=5000&candleFormat=midpoint&granularity=M15"
r = requests.get(url, headers=h)     
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

def Dstart():
    for i in range(0,5000):
        for j in range(0,DDay_Count):
            if Date(i) == DDay[j]:
                return j

def M5start():
    for i in range(0,5000):
        for j in range(0,DDay_Count):
            if Date(i) == DDay[j]:
                return i

Account = 1000
Starting_Balance = Account
last_entry = 0 
spacer = 5
SL = -0.001
TP = 0.001
last_trade = 0
Open_Units =0
Open_Trade = False
Open_Order = 0
Lots = 10000
Account_Chart = []
j = Dstart()-1
UpperPP = 0
LowerPP = 0
for i in range(M5start(),4000):
    if Open_Order == 0:
        Carry_Price = Close(i)
    
    if str(Date(i)) == str(DDay[j+1]):
        PP = (DHigh[j] + DLow[j] + DClose[j])/3
        S1 = 2*PP - DHigh[j]
        S2 = PP - DHigh[j] + DLow[j]
        R1 = 2*PP - DLow[j]
        R2 = PP + DHigh[j] - DLow[j]
        if Close(i) > R2:
            UpperPP = Close(i)*2
            LowerPP = R2
        elif Close(i) > R1 and Close(i) < R2:
            UpperPP = R2
            LowerPP = R1
        elif Close(i) > PP and Close(i) < R1:
            UpperPP = R1
            LowerPP = PP
        elif Close(i) > S1 and Close(i) < PP:
            UpperPP = PP
            LowerPP = S1
        elif Close(i) > S2 and Close(i) < S1:  
            UpperPP = S1
            LowerPP = S2
        elif Close(i) < S2:
            UpperPP = S2
            LowerPP = Close(i)/2
        j = j + 1

    if Close(i) > UpperPP and Close(i-1) < UpperPP and Open_Order == 0 and i - last_entry > spacer:
        Open_Order = 1
        Open_Price = Close(i)
        Stop_Loss = Open(i) + SL
        Take_Profit = Open(i) + TP
        Carry_Price = Close(i)
        last_entry = i
    
    if Close(i) < LowerPP and Close(i-1) > LowerPP and Open_Order == 0 and i - last_entry > spacer:
        Open_Order = -1
        Open_Price = Close(i)
        Stop_Loss = Open(i) - SL
        Take_Profit = Open(i) - TP
        Carry_Price = Close(i)
        last_entry = i

    if Open_Order == 1:
        if High(i) > Take_Profit:
            Account = Starting_Balance + TP * Lots
            Open_Order = 0
            Starting_Balance = Account
        if Low(i) < Stop_Loss:
            Account = Starting_Balance + SL * Lots
            Open_Order = 0 
            Starting_Balance = Account
        if High(i) < Take_Profit and Low(i) > Stop_Loss:
            Account = Starting_Balance + (Carry_Price - Open_Price) * Lots

    if Open_Order == -1:
        if High(i) > Stop_Loss:
            Account = Starting_Balance + SL * Lots
            Open_Order = 0 
            Starting_Balance = Account
        if Low(i) < Take_Profit:
            Account = Starting_Balance + TP * Lots
            Open_Order = 0 
            Starting_Balance = Account
        if Low(i) > Take_Profit and High(i) < Stop_Loss:
            Account = Starting_Balance + (Open_Price - Carry_Price) * Lots
    Account_Chart.append(Account)

plt.plot(Account_Chart)
plt.ylim(500,2500)
plt.show()