import requests
import json
from array import *
import matplotlib.pyplot as plt
import numpy as np
import pypyodbc

#access_token = "Bearer 1607c86b2d94c3df4dd10d7464c6b7f8-d846a5c1dbc08c065423f802437bd40e" # Live access token
access_token = "Bearer 9809f21a2365d168f6edaa79416a91a4-9945354703cd1c827171d7860046e592" # Demo access token
R_url = "https://api-fxtrade.oanda.com/v1/candles?instrument=EUR_CAD&count=4000&candleFormat=midpoint&granularity=H4"
h = {'Authorization' : access_token}
r= requests.get( R_url, headers=h)     

strT = "time"
strO = "openMid"
strH = "highMid"
strL = "lowMid"
strC = "closeMid"
strV = "volume"
strCO = "complete"

data = json.loads(r.text)

def Open(index):
    return data["candles"][4000 - index][strO]
def High(index):
    return data["candles"][4000 - index][strH]
def Low(index):
    return data["candles"][4000 - index][strL]
def Close(index):
    return data["candles"][4000 - index][strC]
def Candle(O,H,L,C):
    if (O < C and 2 * (H - O) < (O - L)) or (C < O and 2 * (H - C) < (C - L)): 
        return "Bullish Pin Bar"
    elif (O < C and 2 * (C - L) < (H - C)) or (C < O and 2 * (O - L) < (H - O)): 
        return "Bearish Pin Bar"
    elif (H - C) < 0.1 * (C - O) and C - O > 0.005 * C: 
        return "Bullish Marubozu"
    elif (C - L) < 0.1 * (O - C) and O - C > 0.005 * C: 
        return "Bearish Marubozu"
    elif abs(O - C) < 0.002 * C: 
        return "Doji"
    elif (H - L) > 0.01 * C and abs(C - O) / (H - L) < 0.5 * (H - L): 
        return "High Wave"
def SMA(index,num):
    sma_temp = 0
    for i in range(0,num-1):
        sma_temp = sma_temp + data["candles"][4000 - index- i][strC]
    return sma_temp/num
n = 50
last_i = 0
spacer = 5

cntr = 0
last_ID = 0
LowerBand = []
UpperBand = []
Return_Avg = []
Return_SD = []

file_Name = "C:\Users\macky\OneDrive\Documents\Price_Database.mdb"

conn = pypyodbc.win_connect_mdb(file_Name)  

cur = conn.cursor()

#cur.execute(u"""CREATE TABLE Return_Data (ID INTEGER PRIMARY KEY, N Integer, R Double)""")
#cur.commit()

cur.execute("DELETE * FROM Return_Data")
cur.commit

p = 0
ID = 1
r = -0.002
for i in range(101,4500):
    aavg = 0.0
    ssd = 0.0
    sd = 0.0
    S = SMA(i,n)
    for j in range(0,n):
        ssd = (Close(i-j) - S)**2 +ssd
    sd = (ssd/(n-1))**(0.5)

    Upper_Band = S + 2*sd
    Lower_Band = S - 2*sd
    if Candle(Open(i),High(i),Low(i),Close(i)) == "Doji" and i - last_i > spacer:
        for j in range(0,10):
            ret = Close(i+j)/Close(i)- 1
            cur.execute("INSERT INTO Return_Data (ID,N,R) VALUES(?,?,?)",(ID,j,ret))
            ID = ID + 1 
        last_i = i
        cntr = cntr +  1
        cur.commit()
        p = 11

test = [0] * cntr
print cntr
#cur.execute(u"""CREATE TABLE Bands_Data (ID INTEGER PRIMARY KEY, N Integer, Per Integer,P Double)""")
#cur.commit()
p = 0

cur.execute("DELETE * FROM Bands_Data")
cur.commit

ID = 1
for j in range(0,10):
    for i in range(0,cntr):
        test[i] = 0

    cur.execute("SELECT [R] FROM Return_Data WHERE [N] = " + str(j))
    results = cur.fetchall()

    for i in range(0,cntr):
        x1 = str(results[i])
        y1 = x1[1:]
        z1 = y1[:len(y1)-2]
        test[i] = float(z1)

    cur.execute("INSERT INTO Bands_Data (ID,N,Per,P) VALUES(?,?,?,?)",(ID,j,5,np.percentile(test,5)))
    cur.execute("INSERT INTO Bands_Data (ID,N,Per,P) VALUES(?,?,?,?)",(ID+1,j,25,np.percentile(test,25)))
    cur.execute("INSERT INTO Bands_Data (ID,N,Per,P) VALUES(?,?,?,?)",(ID+2,j,50,np.percentile(test,50)))
    cur.execute("INSERT INTO Bands_Data (ID,N,Per,P) VALUES(?,?,?,?)",(ID+3,j,75,np.percentile(test,75)))
    cur.execute("INSERT INTO Bands_Data (ID,N,Per,P) VALUES(?,?,?,?)",(ID+4,j,95,np.percentile(test,95)))
    p = 11
    ID = ID +5

cur.execute("SELECT [P] FROM Bands_Data WHERE [Per] = 75 ORDER BY [N] ASC")
results = cur.fetchall()
for i in range(0,10):
    x1 = str(results[i])
    y1 = x1[1:]
    z1 = y1[:len(y1)-2]
    UpperBand.append(float(z1))

cur.execute("SELECT [P] FROM Bands_Data WHERE [Per] = 25 ORDER BY [N] ASC")
results = cur.fetchall()
for i in range(0,10):
    x1 = str(results[i])
    y1 = x1[1:]
    z1 = y1[:len(y1)-2]
    LowerBand.append(float(z1)) 

'''
cur.execute("SELECT AVG([R]) FROM Return_Data GROUP BY [N]")
results = cur.fetchall()

for i in range(0,10):
    x1 = str(results[i])
    y2 = x1[1:]
    z2 = y2[:len(y2)-2]
    Return_Avg.append(float(z2))

cur.execute("SELECT (MAX([R])-MIN([R]))/6 FROM Return_Data GROUP BY [N]")
results2 = cur.fetchall()
cur.execute("DELETE * FROM Return_Data")
cur.commit
for i in range(0,10):
    x2 = str(results2[i])
    y1 = x2[1:]
    z1 = y1[:len(y1)-2]
    Return_SD.append(float(z1))

print Return_Avg
print Return_SD

'''

plt.plot(LowerBand)
plt.plot(UpperBand)
plt.ylim(-0.02,0.02)
plt.show()
