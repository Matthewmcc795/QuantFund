import requests
import json
from array import *
import matplotlib.pyplot as plt
import numpy as np
from Settings import PRICE_DOMAIN, ACCOUNT_DOMAIN, ACCESS_TOKEN, ACCOUNT_ID, STRT, STRO, STRH, STRL, STRC, STRV, STRCO
import pypyodbc

Sec = []
Sec.append("EUR_USD")
Sec.append("GBP_USD")
Sec.append("USD_CAD")
Sec.append("AUD_USD")
Sec.append("NZD_USD")

file_Name = "C:\Users\macky\OneDrive\Documents\Price_Database.mdb"

conn = pypyodbc.win_connect_mdb(file_Name)  
cur = conn.cursor()
cur.execute(u"""CREATE TABLE Backtest_Ret (ID INTEGER PRIMARY KEY, Day String, Test String, Ret Double)""")
#cur.execute("DELETE * From Backtestata")

Bars = 5000
I_D = 0   
for k in range(0,5):
    h = {'Authorization' : ACCESS_TOKEN}
    print "Retrieving Data..."
    r = requests.get( ACCOUNT_DOMAIN + "instrument=" + Sec[k] +"&count=" + str(Bars) + "&candleFormat=midpoint&granularity=H4", headers=h)     
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


    for m in range(0,10):
        n = 50
        last_i = 0
        spacer = 5
      
        for i in range(51,4500):
            aavg = 0.0
            SMA = 0.0
            ssd = 0.0
            sd = 0.0

            for j in range(0,n+5*m):
                aavg = Close(i-j) + aavg
            SMA = aavg/(n+5*m)
            
            for j in range(0,n+5*m):
                ssd = (Close(i-j) - SMA)**2 +ssd
            sd = (ssd/(n+5*m-1))**(0.5)
            Upper_Band = SMA + 1.5*sd
            Lower_Band = SMA - 1.5*sd
            skhetti = []

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

            if Close(i) < Lower_Band and Close(i-1) < Lower_Band and sd > 0.005 and tal > 0.0005 and i - last_i > spacer:
                for j in range(0,50):
                    ret = Close(i+j)/Close(i)- 1
                    cur.execute('''INSERT INTO Backtest_Ret(ID, Day, Test, Ret) 
                    VALUES(?,?,?,?)''', (I_D,str(Date(i)),"BUY MAC H4 " + Sec[k] + " and " + str(n+5*m) + " SMA",ret))
                    I_D = I_D + 1
                last_i = i
            elif Close(i) > Upper_Band and Close(i-1) > Upper_Band and sd > 0.005 and wik > 0.0005 and i - last_i > spacer:
                for j in range(0,50):
                    ret = Close(i+j)/Close(i)- 1
                    cur.execute('''INSERT INTO Backtest_Ret(ID, Day, Test, Ret) 
                    VALUES(?,?,?,?)''', (I_D,str(Date(i)),"Sell MAC H4 " + Sec[k] + " and " + str(n+5*m) + " SMA",ret))
                    I_D = I_D + 1
                last_i = i


cur.commit()

cur.close()
conn.commit()
conn.close()