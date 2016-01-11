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

file_Name = "C:\Users\macky\OneDrive\Documents\Price_Database.mdb"

conn = pypyodbc.win_connect_mdb(file_Name)  
cur = conn.cursor()
#cur.execute(u"""CREATE TABLE Backtestata (ID INTEGER PRIMARY KEY, Day String, Test String, SD Double, Wick Double, Tail Double, Order Integer, Account Double)""")
cur.execute("DELETE * From Backtestata")
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

Lots = 10000
n = 20
last_entry = 0 
spacer = 5
SL = -0.0100
TP = 0.0050
last_trade = 0
Open_Units =0
Open_Trade = False
Bars = 5000
I_D = 1

for k in range(0,5):

    h = {'Authorization' : ACCESS_TOKEN}
    print "Retrieving Data..."
    r = requests.get( ACCOUNT_DOMAIN + "instrument=" + Sec[k] +"&count=" + str(Bars) + "&candleFormat=midpoint&granularity=H4&dailyAlignment=3", headers=h)     
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
    S_D=[]

    for m in range(0,10):
        Account = 1000
        Starting_Balance = Account
        last_entry = 0 
        spacer = 5
        SL = -0.006
        TP = 0.0050
        last_trade = 0
        Open_Units =0
        Open_Trade = False
        for i in range(100,4500):
            if Open_Order == 0:
                Carry_Price = Close(i-1)
            aavg = 0.0
            SMA = 0.0
            ssd = 0.0
            sd = 0.0
            tail = 0.0
            wick = 0.0
            
            for j in range(0,n+5*m):
                aavg = Close(i-j) + aavg
            SMA = aavg/(n+5*m)
            
            for j in range(0,n+5*m):
                ssd = (Close(i-j) - SMA)**2 +ssd
            sd = (ssd/(n+5*m-1))**(0.5)
            S_D.append(sd)
            Upper_Band = SMA + 3*sd
            Lower_Band = SMA - 3*sd
            
            if Close(i-1) > Open(i-1):
                wick = High(i-1) - Close(i-1)
                tail = Open(i-1) - Low(i-1)
            else:
                wick = High(i-1) - Open(i-1)
                tail = Close(i-1) - Low(i-1)

            if Close(i-2) > Open(i-2):
                wick2 = High(i-2) - Close(i-2)
                tail2 = Open(i-2) - Low(i-2)
            else:
                wick2 = High(i-2) - Open(i-2)
                tail2 = Close(i-2) - Low(i-2)

            wik = (wick2 + wick)/2
            tal = (tail2 + tail)/2

            if Close(i-1) < Lower_Band and Close(i-2) < Lower_Band and sd > 0.005 and tal > 0.0005 and Open_Order == 0 and i - last_entry > spacer:
                Open_Order = 1
                Open_Price = Close(i-1)
                Stop_Loss = Open(i) + SL
                Take_Profit = Open(i) + TP
                Carry_Price = Close(i-1)
                last_entry = i
            
            if Close(i-1) > Upper_Band and Close(i-2) > Upper_Band and sd >0.005 and wik > 0.0005 and Open_Order == 0 and i - last_entry > spacer:
                Open_Order = -1
                Open_Price = Close(i-1)
                Stop_Loss = Open(i) - SL
                Take_Profit = Open(i) - TP
                Carry_Price = Close(i-1)
                last_entry = i

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
            # Account_Chart.append(Account)
     
            cur.execute('''INSERT INTO Backtestata(ID,Day,Test,Account) 
            VALUES(?,?,?,?)''', (I_D,str(Date(i)),"MAC H4 " + Sec[k] + " and " + str(n+5*m) + " SMA",Account))

            # cur.execute('''INSERT INTO Backtests_Data(ID,Day,Test,SD,Wick,Tail,Order,Account) 
            # VALUES(?,?,?,?,?,?,?,?)''', (I_D,str(Date(i)),"MAC H4 " + Sec[k],sd,wik,tal,Open_Order,Account))
            I_D = I_D + 1

cur.commit()

# plt.plot(Account_Chart)
# plt.ylim(500,2500)
# plt.show()
# plt.plot(S_D)
# plt.ylim(0,0.025)
# plt.show()
cur.close()
conn.commit()
conn.close()